"""Journal applicatif : fichier tournant + diffusion aux écouteurs (UI temps réel)."""

from __future__ import annotations

import json
import threading
import time
from collections import deque
from pathlib import Path

LEVELS = {"debug": 10, "info": 20, "warn": 30, "error": 40}

_lock = threading.RLock()
_buffer: deque = deque(maxlen=500)
_listeners: list = []
_file: Path | None = None
_level = LEVELS["info"]


def configure(path: Path | str | None = None, level: str = "info"):
    global _file, _level
    _level = LEVELS.get(level, 20)
    if path:
        _file = Path(path)
        _file.parent.mkdir(parents=True, exist_ok=True)


def set_level(level: str):
    global _level
    _level = LEVELS.get(level, 20)


def on(fn):
    with _lock:
        _listeners.append(fn)
    return fn


def _emit(rec: dict):
    with _lock:
        _buffer.append(rec)
        listeners = list(_listeners)
    if _file:
        try:
            with _file.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        except Exception:
            pass
    for fn in listeners:
        try:
            fn(rec)
        except Exception:
            pass


def write(level: str, source: str, message: str, **extra):
    if LEVELS.get(level, 20) < _level:
        return
    rec = {"t": time.strftime("%H:%M:%S"), "ts": time.time(),
           "niveau": level, "source": source, "message": str(message)}
    if extra:
        rec.update(extra)
    _emit(rec)


def debug(source, message, **kw):
    write("debug", source, message, **kw)


def info(source, message, **kw):
    write("info", source, message, **kw)


def warn(source, message, **kw):
    write("warn", source, message, **kw)


def error(source, message, **kw):
    write("error", source, message, **kw)


def recent(limit=100):
    with _lock:
        return list(_buffer)[-limit:]
