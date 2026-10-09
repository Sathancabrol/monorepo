"""Stockage JSON : simple, lisible, versionnable, atomique.

Un dossier par collection, un fichier `.json` par enregistrement, plus un index
`_index.json` pour les listes. Les écritures passent par un fichier temporaire
puis `os.replace` : pas de fichier à moitié écrit si ça coupe en pleine réunion.
"""

from __future__ import annotations

import json
import os
import re
import threading
import time
import unicodedata
import uuid
from pathlib import Path
from typing import Any, Iterable

_SLUG_STRIP = re.compile(r"[^a-z0-9]+")


def slug(text: str, fallback: str = "x") -> str:
    s = unicodedata.normalize("NFKD", str(text or "")).encode("ascii", "ignore").decode()
    s = _SLUG_STRIP.sub("-", s.lower()).strip("-")
    return s or fallback


def new_id(prefix: str = "id") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}"


class Store:
    def __init__(self, root: Path | str):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()

    # ---------- bas niveau ----------
    def dir(self, collection: str) -> Path:
        p = self.root / slug(collection)
        p.mkdir(parents=True, exist_ok=True)
        return p

    def path(self, collection: str, record_id: str) -> Path:
        return self.dir(collection) / f"{slug(record_id)}.json"

    def _write(self, path: Path, data: Any) -> None:
        tmp = path.with_suffix(path.suffix + f".{os.getpid()}.tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, path)

    # ---------- API ----------
    def put(self, collection: str, record_id: str, data: dict) -> dict:
        with self._lock:
            rec = dict(data)
            rec["id"] = record_id
            rec.setdefault("cree_le", time.strftime("%Y-%m-%dT%H:%M:%S"))
            rec["modifie_le"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            self._write(self.path(collection, record_id), rec)
            return rec

    def create(self, collection: str, data: dict, prefix: str = "") -> dict:
        rid = data.get("id") or new_id(prefix or slug(collection, "rec"))
        return self.put(collection, rid, data)

    def get(self, collection: str, record_id: str) -> dict | None:
        p = self.path(collection, record_id)
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return None

    def delete(self, collection: str, record_id: str) -> bool:
        with self._lock:
            p = self.path(collection, record_id)
            if p.exists():
                p.unlink()
                return True
            return False

    def all(self, collection: str) -> list[dict]:
        out = []
        d = self.dir(collection)
        for p in sorted(d.glob("*.json")):
            try:
                out.append(json.loads(p.read_text(encoding="utf-8")))
            except Exception:
                continue
        out.sort(key=lambda r: (r.get("cree_le") or ""), reverse=True)
        return out

    def find(self, collection: str, predicate) -> list[dict]:
        return [r for r in self.all(collection) if predicate(r)]

    def update(self, collection: str, record_id: str, patch: dict) -> dict | None:
        with self._lock:
            rec = self.get(collection, record_id)
            if rec is None:
                return None
            rec.update(patch)
            return self.put(collection, record_id, rec)

    # ---------- pièces jointes / fichiers générés ----------
    def blob_dir(self, collection: str = "fichiers") -> Path:
        p = self.root / "_" / slug(collection)
        p.mkdir(parents=True, exist_ok=True)
        return p

    def write_blob(self, name: str, data: bytes, collection: str = "fichiers") -> Path:
        p = self.blob_dir(collection) / name
        tmp = p.with_suffix(p.suffix + f".{os.getpid()}.tmp")
        tmp.write_bytes(data)
        os.replace(tmp, p)
        return p


def iter_records(root: Path) -> Iterable[tuple[str, dict]]:
    """Parcourt toutes les collections (utilisé pour l'export / sauvegarde)."""
    for coll in sorted(Path(root).iterdir()):
        if not coll.is_dir() or coll.name.startswith("_"):
            continue
        for p in sorted(coll.glob("*.json")):
            try:
                yield coll.name, json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                continue
