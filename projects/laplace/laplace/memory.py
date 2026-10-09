"""SQLite archive and explicit, provenance-aware durable memories."""

from __future__ import annotations

import json
import os
import re
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import aiosqlite


def utc_now() -> datetime:
    return datetime.now(UTC)


def iso_utc(value: datetime | None = None) -> str:
    return (value or utc_now()).isoformat(timespec="seconds")


def _safe_source_url(value: str | None) -> str | None:
    if value is None or not value.strip():
        return None
    candidate = value.strip()
    parsed = urlsplit(candidate)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("La source doit être une URL HTTPS valide, sans identifiants intégrés.")
    return candidate


def _fts_query(query: str) -> str:
    words = re.findall(r"[\wÀ-ÖØ-öø-ÿ]+", query, flags=re.UNICODE)[:12]
    return " AND ".join(f'"{word.replace(chr(34), chr(34) * 2)}"' for word in words)


class MemoryStore:
    """A small local store; chat history is per-user and never shared across users."""

    def __init__(self, database_path: str | Path) -> None:
        self.path = Path(database_path).expanduser()
        self._fts_available = False

    async def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.path) as db:
            await db.execute("PRAGMA foreign_keys = ON")
            await db.execute("PRAGMA journal_mode = WAL")
            await db.executescript(
                """
                CREATE TABLE IF NOT EXISTS interaction_archive (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    interaction_id TEXT NOT NULL UNIQUE,
                    user_id TEXT NOT NULL,
                    guild_id TEXT NOT NULL,
                    channel_id TEXT NOT NULL,
                    request TEXT NOT NULL,
                    response TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_archive_user_date
                    ON interaction_archive(user_id, created_at);

                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scope TEXT NOT NULL CHECK(scope IN ('private', 'shared')),
                    owner_user_id TEXT,
                    shared_guild_id TEXT,
                    content TEXT NOT NULL,
                    confidence REAL NOT NULL CHECK(confidence >= 0 AND confidence <= 1),
                    source_url TEXT,
                    source_interaction_id TEXT NOT NULL,
                    source_guild_id TEXT NOT NULL,
                    source_channel_id TEXT NOT NULL,
                    source_user_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    CHECK (
                        (scope = 'private' AND owner_user_id IS NOT NULL
                         AND shared_guild_id IS NULL)
                        OR (scope = 'shared' AND owner_user_id IS NULL
                            AND shared_guild_id IS NOT NULL)
                    )
                );
                CREATE INDEX IF NOT EXISTS idx_memories_owner_scope_date
                    ON memories(owner_user_id, scope, created_at);

                CREATE TABLE IF NOT EXISTS memory_revisions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    memory_id INTEGER NOT NULL REFERENCES memories(id) ON DELETE CASCADE,
                    previous_content TEXT NOT NULL,
                    new_content TEXT NOT NULL,
                    editor_user_id TEXT NOT NULL,
                    changed_at TEXT NOT NULL
                );
                """
            )
            columns_cursor = await db.execute("PRAGMA table_info(memories)")
            columns = {row[1] for row in await columns_cursor.fetchall()}
            if "shared_guild_id" not in columns:
                # Preserve the original server for each shared memory during schema migration.
                await db.execute("ALTER TABLE memories ADD COLUMN shared_guild_id TEXT")
                await db.execute(
                    "UPDATE memories SET shared_guild_id = source_guild_id WHERE scope = 'shared'"
                )
            await db.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_shared_guild "
                "ON memories(shared_guild_id, scope, created_at)"
            )
            try:
                await db.execute(
                    "CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts "
                    "USING fts5(content, tokenize='unicode61 remove_diacritics 2')"
                )
                self._fts_available = True
                missing_cursor = await db.execute(
                    """SELECT m.id, m.content FROM memories m
                       LEFT JOIN memory_fts f ON f.rowid = m.id WHERE f.rowid IS NULL"""
                )
                missing_rows = await missing_cursor.fetchall()
                if missing_rows:
                    await db.executemany(
                        "INSERT INTO memory_fts(rowid, content) VALUES (?, ?)",
                        [(row[0], row[1]) for row in missing_rows],
                    )
            except sqlite3.OperationalError:
                self._fts_available = False
            await db.commit()
        try:
            os.chmod(self.path, 0o600)
        except OSError:
            # Windows ACLs are managed by the user/OS; do not fail startup here.
            pass

    async def _connect(self) -> aiosqlite.Connection:
        db = await aiosqlite.connect(self.path)
        db.row_factory = aiosqlite.Row
        await db.execute("PRAGMA foreign_keys = ON")
        return db

    async def purge_expired(self, retention_days: int) -> int:
        """Purge raw conversations according to the configured retention (0 = purge all)."""
        db = await self._connect()
        try:
            if retention_days == 0:
                cursor = await db.execute("DELETE FROM interaction_archive")
            else:
                cutoff = iso_utc(utc_now() - timedelta(days=retention_days))
                cursor = await db.execute(
                    "DELETE FROM interaction_archive WHERE created_at < ?", (cutoff,)
                )
            await db.commit()
            return cursor.rowcount
        finally:
            await db.close()

    async def archive_interaction(
        self,
        *,
        interaction_id: int,
        user_id: int,
        guild_id: int,
        channel_id: int,
        request: str,
        response: str,
        created_at: str | None = None,
    ) -> None:
        db = await self._connect()
        try:
            await db.execute(
                """INSERT OR IGNORE INTO interaction_archive
                   (interaction_id, user_id, guild_id, channel_id, request, response, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    str(interaction_id),
                    str(user_id),
                    str(guild_id),
                    str(channel_id),
                    request,
                    response,
                    created_at or iso_utc(),
                ),
            )
            await db.commit()
        finally:
            await db.close()

    async def get_recent_turns(self, user_id: int, limit: int) -> list[dict[str, str]]:
        if limit <= 0:
            return []
        db = await self._connect()
        try:
            cursor = await db.execute(
                """SELECT request, response, created_at FROM interaction_archive
                   WHERE user_id = ? ORDER BY created_at DESC, id DESC LIMIT ?""",
                (str(user_id), limit),
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in reversed(rows)]
        finally:
            await db.close()

    async def add_memory(
        self,
        *,
        content: str,
        scope: str,
        user_id: int,
        interaction_id: int,
        guild_id: int,
        channel_id: int,
        confidence: float = 1.0,
        source_url: str | None = None,
    ) -> int:
        content = content.strip()
        if not content or len(content) > 1000:
            raise ValueError("Un souvenir doit contenir entre 1 et 1000 caractères.")
        if scope not in {"private", "shared"}:
            raise ValueError("La portée doit être private ou shared.")
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("La confiance doit être comprise entre 0 et 1.")
        source = _safe_source_url(source_url)
        timestamp = iso_utc()
        owner_user_id = str(user_id) if scope == "private" else None
        shared_guild_id = str(guild_id) if scope == "shared" else None
        db = await self._connect()
        try:
            cursor = await db.execute(
                """INSERT INTO memories
                   (scope, owner_user_id, shared_guild_id, content, confidence, source_url,
                    source_interaction_id, source_guild_id, source_channel_id,
                    source_user_id, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    scope,
                    owner_user_id,
                    shared_guild_id,
                    content,
                    confidence,
                    source,
                    str(interaction_id),
                    str(guild_id),
                    str(channel_id),
                    str(user_id),
                    timestamp,
                    timestamp,
                ),
            )
            memory_id = int(cursor.lastrowid)
            if self._fts_available:
                await db.execute(
                    "INSERT INTO memory_fts(rowid, content) VALUES (?, ?)",
                    (memory_id, content),
                )
            await db.commit()
            return memory_id
        finally:
            await db.close()

    async def list_memories(
        self,
        user_id: int,
        *,
        guild_id: int,
        include_shared: bool = True,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        if limit <= 0:
            return []
        if include_shared:
            where = (
                "((scope = 'private' AND owner_user_id = ?) OR "
                "(scope = 'shared' AND shared_guild_id = ?))"
            )
            params = (str(user_id), str(guild_id), limit)
        else:
            where = "(scope = 'private' AND owner_user_id = ?)"
            params = (str(user_id), limit)
        db = await self._connect()
        try:
            cursor = await db.execute(
                f"""SELECT id, scope, owner_user_id, shared_guild_id, content, confidence,
                           source_url, source_interaction_id, source_guild_id,
                           source_channel_id, source_user_id, created_at, updated_at
                    FROM memories WHERE {where}
                    ORDER BY updated_at DESC, id DESC LIMIT ?""",
                params,
            )
            return [dict(row) for row in await cursor.fetchall()]
        finally:
            await db.close()

    async def search_memories(
        self, user_id: int, query: str, limit: int, *, guild_id: int
    ) -> list[dict[str, Any]]:
        if limit <= 0 or not query.strip():
            return []
        scope_filter = (
            "((m.scope = 'private' AND m.owner_user_id = ?) OR "
            "(m.scope = 'shared' AND m.shared_guild_id = ?))"
        )
        db = await self._connect()
        try:
            rows: list[aiosqlite.Row] = []
            fts_expression = _fts_query(query)
            if self._fts_available and fts_expression:
                try:
                    cursor = await db.execute(
                        f"""SELECT m.id, m.scope, m.owner_user_id, m.shared_guild_id, m.content,
                                  m.confidence, m.source_url, m.source_interaction_id,
                                  m.source_guild_id, m.source_channel_id, m.source_user_id,
                                  m.created_at, m.updated_at
                           FROM memory_fts f JOIN memories m ON m.id = f.rowid
                           WHERE memory_fts MATCH ? AND {scope_filter}
                           ORDER BY m.updated_at DESC, m.id DESC LIMIT ?""",
                        (fts_expression, str(user_id), str(guild_id), limit),
                    )
                    rows = await cursor.fetchall()
                except sqlite3.OperationalError:
                    rows = []
            if not rows:
                tokens = re.findall(r"[\wÀ-ÖØ-öø-ÿ]+", query, flags=re.UNICODE)[:5]
                if not tokens:
                    return []
                where = " AND ".join("lower(m.content) LIKE ?" for _ in tokens)
                params: list[Any] = [f"%{token.lower()}%" for token in tokens]
                params.extend([str(user_id), str(guild_id), limit])
                cursor = await db.execute(
                    f"""SELECT m.id, m.scope, m.owner_user_id, m.shared_guild_id, m.content,
                               m.confidence, m.source_url, m.source_interaction_id,
                               m.source_guild_id, m.source_channel_id, m.source_user_id,
                               m.created_at, m.updated_at
                        FROM memories m WHERE ({where}) AND {scope_filter}
                        ORDER BY m.updated_at DESC, m.id DESC LIMIT ?""",
                    params,
                )
                rows = await cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            await db.close()

    async def correct_memory(
        self,
        *,
        memory_id: int,
        user_id: int,
        guild_id: int,
        new_content: str,
        can_manage_shared: bool = False,
    ) -> bool:
        new_content = new_content.strip()
        if not new_content or len(new_content) > 1000:
            raise ValueError("Le souvenir corrigé doit contenir entre 1 et 1000 caractères.")
        db = await self._connect()
        try:
            cursor = await db.execute("SELECT * FROM memories WHERE id = ?", (memory_id,))
            row = await cursor.fetchone()
            if row is None or not self._can_edit(row, user_id, guild_id, can_manage_shared):
                return False
            timestamp = iso_utc()
            await db.execute(
                """INSERT INTO memory_revisions
                   (memory_id, previous_content, new_content, editor_user_id, changed_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (memory_id, row["content"], new_content, str(user_id), timestamp),
            )
            await db.execute(
                "UPDATE memories SET content = ?, updated_at = ? WHERE id = ?",
                (new_content, timestamp, memory_id),
            )
            if self._fts_available:
                await db.execute("DELETE FROM memory_fts WHERE rowid = ?", (memory_id,))
                await db.execute(
                    "INSERT INTO memory_fts(rowid, content) VALUES (?, ?)",
                    (memory_id, new_content),
                )
            await db.commit()
            return True
        finally:
            await db.close()

    async def forget_memory(
        self,
        *,
        memory_id: int,
        user_id: int,
        guild_id: int,
        can_manage_shared: bool = False,
    ) -> bool:
        db = await self._connect()
        try:
            cursor = await db.execute("SELECT * FROM memories WHERE id = ?", (memory_id,))
            row = await cursor.fetchone()
            if row is None or not self._can_edit(row, user_id, guild_id, can_manage_shared):
                return False
            if self._fts_available:
                await db.execute("DELETE FROM memory_fts WHERE rowid = ?", (memory_id,))
            await db.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            await db.commit()
            return True
        finally:
            await db.close()

    @staticmethod
    def _can_edit(
        row: aiosqlite.Row,
        user_id: int,
        guild_id: int,
        can_manage_shared: bool,
    ) -> bool:
        if row["scope"] == "shared":
            return can_manage_shared and row["shared_guild_id"] == str(guild_id)
        return row["owner_user_id"] == str(user_id)

    async def search_archive(
        self, user_id: int, query: str, *, limit: int = 5
    ) -> list[dict[str, Any]]:
        tokens = re.findall(r"[\wÀ-ÖØ-öø-ÿ]+", query, flags=re.UNICODE)[:5]
        if not tokens:
            return []
        clauses = " AND ".join("(lower(request) LIKE ? OR lower(response) LIKE ?)" for _ in tokens)
        params: list[Any] = []
        for token in tokens:
            wildcard = f"%{token.lower()}%"
            params.extend([wildcard, wildcard])
        params.extend([str(user_id), limit])
        db = await self._connect()
        try:
            cursor = await db.execute(
                f"""SELECT interaction_id, guild_id, channel_id, request, response, created_at
                    FROM interaction_archive WHERE {clauses} AND user_id = ?
                    ORDER BY created_at DESC, id DESC LIMIT ?""",
                params,
            )
            return [dict(row) for row in await cursor.fetchall()]
        finally:
            await db.close()

    async def forget_all_user_data(self, user_id: int) -> dict[str, int]:
        db = await self._connect()
        try:
            cursor = await db.execute(
                "SELECT id FROM memories WHERE scope = 'private' AND owner_user_id = ?",
                (str(user_id),),
            )
            ids = [int(row["id"]) for row in await cursor.fetchall()]
            if self._fts_available and ids:
                await db.executemany(
                    "DELETE FROM memory_fts WHERE rowid = ?", [(item,) for item in ids]
                )
            memories_cursor = await db.execute(
                "DELETE FROM memories WHERE scope = 'private' AND owner_user_id = ?",
                (str(user_id),),
            )
            archive_cursor = await db.execute(
                "DELETE FROM interaction_archive WHERE user_id = ?", (str(user_id),)
            )
            await db.commit()
            return {"memories": memories_cursor.rowcount, "interactions": archive_cursor.rowcount}
        finally:
            await db.close()

    async def export_user_data(self, user_id: int) -> dict[str, Any]:
        db = await self._connect()
        try:
            cursor = await db.execute(
                """SELECT id, scope, content, confidence, source_url, source_interaction_id,
                          source_guild_id, source_channel_id, source_user_id, created_at, updated_at
                   FROM memories WHERE scope = 'private' AND owner_user_id = ?
                   ORDER BY id""",
                (str(user_id),),
            )
            memories = [dict(row) for row in await cursor.fetchall()]
            memory_ids = [row["id"] for row in memories]
            revisions: list[dict[str, Any]] = []
            if memory_ids:
                placeholders = ",".join("?" for _ in memory_ids)
                cursor = await db.execute(
                    f"""SELECT memory_id, previous_content, new_content, editor_user_id, changed_at
                        FROM memory_revisions WHERE memory_id IN ({placeholders}) ORDER BY id""",
                    memory_ids,
                )
                revisions = [dict(row) for row in await cursor.fetchall()]
            cursor = await db.execute(
                """SELECT interaction_id, guild_id, channel_id, request, response, created_at
                   FROM interaction_archive WHERE user_id = ? ORDER BY created_at, id""",
                (str(user_id),),
            )
            interactions = [dict(row) for row in await cursor.fetchall()]
            return {
                "exported_at": iso_utc(),
                "discord_user_id": str(user_id),
                "memories": memories,
                "memory_revisions": revisions,
                "archived_interactions": interactions,
            }
        finally:
            await db.close()

    async def close(self) -> None:
        """Connections are scoped per operation; present for a uniform lifecycle API."""
        return None


def export_json(data: dict[str, Any]) -> bytes:
    return json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
