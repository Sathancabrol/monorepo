"""Persistance SQLite : sessions, messages, runs, usage des modèles.

Les *specs* d'agents et les compétences restent des fichiers lisibles (JSON /
SKILL.md) pour être versionnables ; SQLite ne garde que le volatile (historique,
compteurs de quota, journaux d'exécution).
"""
from __future__ import annotations

import json
import sqlite3
import threading
import time
import uuid
from typing import Any, Iterable

from nexus_os import config

_LOCK = threading.RLock()
_SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  title TEXT NOT NULL DEFAULT '',
  created_at REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  role TEXT NOT NULL,
  content TEXT NOT NULL,
  meta TEXT NOT NULL DEFAULT '{}',
  created_at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id, id);
CREATE TABLE IF NOT EXISTS runs (
  id TEXT PRIMARY KEY,
  session_id TEXT,
  agent_id TEXT NOT NULL,
  task TEXT NOT NULL,
  status TEXT NOT NULL,
  phases TEXT NOT NULL DEFAULT '[]',
  result TEXT NOT NULL DEFAULT '',
  model TEXT,
  provider TEXT,
  mode TEXT,
  tokens INTEGER NOT NULL DEFAULT 0,
  steps INTEGER NOT NULL DEFAULT 0,
  duration_ms INTEGER NOT NULL DEFAULT 0,
  created_at REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS usage_daily (
  day TEXT NOT NULL,
  provider_id TEXT NOT NULL,
  model TEXT NOT NULL,
  calls INTEGER NOT NULL DEFAULT 0,
  tokens INTEGER NOT NULL DEFAULT 0,
  errors INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (day, provider_id, model)
);
"""


def _connect() -> sqlite3.Connection:
    config.ensure_dirs()
    conn = sqlite3.connect(str(config.DB_PATH), timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def _today() -> str:
    return time.strftime("%Y-%m-%d", time.gmtime())


class Store:
    """Accès thread-safe à la base (un verrou process + connexion par appel)."""

    def __init__(self) -> None:
        with _LOCK, _connect() as conn:
            conn.executescript(_SCHEMA)

    # --- sessions ---------------------------------------------------------
    def create_session(self, agent_id: str, title: str = "") -> dict[str, Any]:
        sid = uuid.uuid4().hex[:12]
        with _LOCK, _connect() as conn:
            conn.execute(
                "INSERT INTO sessions (id, agent_id, title, created_at) VALUES (?,?,?,?)",
                (sid, agent_id, title or f"Session {agent_id}", time.time()),
            )
        return {"id": sid, "agent_id": agent_id, "title": title or f"Session {agent_id}"}

    def list_sessions(self, limit: int = 40) -> list[dict[str, Any]]:
        with _LOCK, _connect() as conn:
            rows = conn.execute(
                "SELECT * FROM sessions ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(r) for r in rows]

    def get_session(self, session_id: str) -> dict[str, Any] | None:
        with _LOCK, _connect() as conn:
            row = conn.execute("SELECT * FROM sessions WHERE id=?", (session_id,)).fetchone()
        return dict(row) if row else None

    def add_message(
        self, session_id: str, role: str, content: str, meta: dict[str, Any] | None = None
    ) -> int:
        with _LOCK, _connect() as conn:
            cur = conn.execute(
                "INSERT INTO messages (session_id, role, content, meta, created_at) VALUES (?,?,?,?,?)",
                (session_id, role, content, json.dumps(meta or {}, ensure_ascii=False), time.time()),
            )
            return int(cur.lastrowid or 0)

    def messages(self, session_id: str, limit: int = 100) -> list[dict[str, Any]]:
        with _LOCK, _connect() as conn:
            rows = conn.execute(
                "SELECT * FROM messages WHERE session_id=? ORDER BY id DESC LIMIT ?",
                (session_id, limit),
            ).fetchall()
        out = []
        for r in reversed(rows):
            d = dict(r)
            d["meta"] = json.loads(d.get("meta") or "{}")
            out.append(d)
        return out

    # --- runs -------------------------------------------------------------
    def start_run(self, agent_id: str, task: str, session_id: str | None = None) -> str:
        rid = uuid.uuid4().hex[:12]
        with _LOCK, _connect() as conn:
            conn.execute(
                "INSERT INTO runs (id, session_id, agent_id, task, status, created_at)"
                " VALUES (?,?,?,?,?,?)",
                (rid, session_id, agent_id, task, "running", time.time()),
            )
        return rid

    def finish_run(
        self,
        run_id: str,
        *,
        status: str,
        result: str = "",
        phases: Iterable[str] = (),
        model: str | None = None,
        provider: str | None = None,
        mode: str | None = None,
        tokens: int = 0,
        steps: int = 0,
        duration_ms: int = 0,
    ) -> None:
        with _LOCK, _connect() as conn:
            conn.execute(
                "UPDATE runs SET status=?, result=?, phases=?, model=?, provider=?, mode=?,"
                " tokens=?, steps=?, duration_ms=? WHERE id=?",
                (
                    status,
                    result,
                    json.dumps(list(phases), ensure_ascii=False),
                    model,
                    provider,
                    mode,
                    tokens,
                    steps,
                    duration_ms,
                    run_id,
                ),
            )

    def list_runs(self, limit: int = 50) -> list[dict[str, Any]]:
        with _LOCK, _connect() as conn:
            rows = conn.execute(
                "SELECT * FROM runs ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["phases"] = json.loads(d.get("phases") or "[]")
            out.append(d)
        return out

    # --- quota / usage ----------------------------------------------------
    def record_usage(
        self, provider_id: str, model: str, tokens: int, *, error: bool = False
    ) -> None:
        with _LOCK, _connect() as conn:
            conn.execute(
                "INSERT INTO usage_daily (day, provider_id, model, calls, tokens, errors)"
                " VALUES (?,?,?,?,?,?)"
                " ON CONFLICT(day, provider_id, model) DO UPDATE SET"
                "  calls=calls+excluded.calls,"
                "  tokens=tokens+excluded.tokens,"
                "  errors=errors+excluded.errors",
                (_today(), provider_id, model, 1, max(0, tokens), 1 if error else 0),
            )

    def usage_today(self) -> list[dict[str, Any]]:
        with _LOCK, _connect() as conn:
            rows = conn.execute(
                "SELECT * FROM usage_daily WHERE day=? ORDER BY tokens DESC", (_today(),)
            ).fetchall()
        return [dict(r) for r in rows]

    def tokens_today(self, provider_id: str) -> int:
        with _LOCK, _connect() as conn:
            row = conn.execute(
                "SELECT COALESCE(SUM(tokens),0) AS t FROM usage_daily WHERE day=? AND provider_id=?",
                (_today(), provider_id),
            ).fetchone()
        return int(row["t"] or 0) if row else 0

    def stats(self) -> dict[str, Any]:
        with _LOCK, _connect() as conn:
            runs = conn.execute("SELECT COUNT(*) c FROM runs").fetchone()["c"]
            ok = conn.execute("SELECT COUNT(*) c FROM runs WHERE status='done'").fetchone()["c"]
            tok = conn.execute("SELECT COALESCE(SUM(tokens),0) t FROM usage_daily").fetchone()["t"]
            msgs = conn.execute("SELECT COUNT(*) c FROM messages").fetchone()["c"]
        return {"runs": runs, "runs_ok": ok, "tokens_total": tok, "messages": msgs}


_store: Store | None = None


def store() -> Store:
    global _store
    if _store is None:
        _store = Store()
    return _store
