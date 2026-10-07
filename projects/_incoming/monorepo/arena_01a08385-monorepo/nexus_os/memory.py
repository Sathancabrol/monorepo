"""Mémoire persistante des agents (le « remember » du cycle ECC).

Stockage JSON plat, rappel par score lexical. Trois niveaux :
`fact` (fait vérifié), `decision` (choix + justification), `lesson` (ce qui a
marché / échoué, réinjecté dans les tâches suivantes).
"""
from __future__ import annotations

import json
import re
import time
import uuid
from pathlib import Path
from typing import Any

from nexus_os import config

KINDS = ("fact", "decision", "lesson")


def _norm(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-zà-ÿ0-9]{3,}", (s or "").lower())}


class Memory:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or config.MEMORY_FILE
        self._items: list[dict[str, Any]] | None = None

    # --- io ---------------------------------------------------------------
    def _load(self) -> list[dict[str, Any]]:
        if self._items is None:
            if self.path.exists():
                try:
                    data = json.loads(self.path.read_text(encoding="utf-8"))
                    self._items = data if isinstance(data, list) else []
                except Exception:
                    self._items = []
            else:
                self._items = []
        return self._items

    def _flush(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self._load(), ensure_ascii=False, indent=2), encoding="utf-8"
        )

    # --- api ---------------------------------------------------------------
    def remember(
        self, content: str, *, kind: str = "fact", agent: str = "", tags: list[str] | None = None
    ) -> dict[str, Any]:
        kind = kind if kind in KINDS else "fact"
        item = {
            "id": uuid.uuid4().hex[:10],
            "kind": kind,
            "content": str(content).strip(),
            "agent": agent,
            "tags": tags or [],
            "ts": time.time(),
        }
        self._load().append(item)
        self._flush()
        return item

    def recall(self, query: str = "", *, kind: str | None = None, limit: int = 5) -> list[dict[str, Any]]:
        items = self._load()
        if kind:
            items = [i for i in items if i.get("kind") == kind]
        q = _norm(query)
        if not q:
            items = sorted(items, key=lambda i: -i.get("ts", 0))
            return items[:limit]

        def score(i: dict[str, Any]) -> float:
            words = _norm(i.get("content", "") + " " + " ".join(i.get("tags", [])))
            if not words:
                return 0.0
            inter = len(q & words)
            return inter / (1 + 0.1 * len(words))

        ranked = sorted(items, key=lambda i: (-score(i), -i.get("ts", 0)))
        return [i for i in ranked if score(i) > 0][:limit]

    def recent(self, limit: int = 10) -> list[dict[str, Any]]:
        return sorted(self._load(), key=lambda i: -i.get("ts", 0))[:limit]

    def forget(self, item_id: str) -> bool:
        items = self._load()
        keep = [i for i in items if i.get("id") != item_id]
        if len(keep) == len(items):
            return False
        self._items = keep
        self._flush()
        return True

    def clear(self) -> int:
        n = len(self._load())
        self._items = []
        self._flush()
        return n

    def render(self, query: str = "", limit: int = 5) -> str:
        items = self.recall(query, limit=limit)
        if not items:
            return ""
        return "\n".join(f"- [{i['kind']}] {i['content']}" for i in items)

    def count(self) -> int:
        return len(self._load())


_memory: Memory | None = None


def memory() -> Memory:
    global _memory
    if _memory is None:
        _memory = Memory()
    return _memory
