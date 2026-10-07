"""Tâches asynchrones — primitive **Tasks** de MCP (SEP-1686) appliquée aux runs.

Le motif « call-now / fetch-later » : on lance, on reçoit un identifiant, on
revient chercher l'état quand on veut. C'est ce qui manquait à NEXUS·OS — une
exécution n'existait que tant qu'un flux SSE était ouvert. Ferme l'onglet, le
travail disparaissait de la vue.

États, ceux de la spécification :

===============  ==============================================================
`working`        l'agent tourne
`input_required` une autorisation est attendue (mode `smart`/`manuel`)
`completed`      terminé, résultat disponible
`failed`         erreur
`cancelled`      arrêté par l'utilisateur
===============  ==============================================================

Les résultats sont persistés : un run lancé avant un redémarrage reste lisible.
"""
from __future__ import annotations

import json
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Callable

from nexus_os import config

STATES = ("working", "input_required", "completed", "failed", "cancelled")
TASKS_FILE = config.NEXUS_HOME / "tasks.json"
#: Nombre d'événements conservés par tâche (le détail complet vit dans la base).
EVENT_TAIL = 200


class TaskError(RuntimeError):
    """Tâche inconnue ou transition interdite."""


def _load() -> dict[str, dict[str, Any]]:
    if not TASKS_FILE.exists():
        return {}
    try:
        raw = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
        return raw if isinstance(raw, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _flush(data: dict[str, dict[str, Any]]) -> None:
    TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = TASKS_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(TASKS_FILE)


_lock = threading.RLock()
#: État vivant des tâches en cours (les threads ne se sérialisent pas).
_live: dict[str, dict[str, Any]] = {}


def _record(task_id: str) -> dict[str, Any]:
    with _lock:
        if task_id in _live:
            return _live[task_id]
        stored = _load().get(task_id)
        if not stored:
            raise TaskError(f"tâche inconnue : {task_id}")
        return stored


def _save(rec: dict[str, Any]) -> None:
    with _lock:
        data = _load()
        data[rec["id"]] = rec
        _flush(data)


# -------------------------------------------------------------------------- #
# Cycle de vie
# -------------------------------------------------------------------------- #
def submit(task: str, agent_id: str, *, approval: str = "smart",
           session_id: str | None = None, max_steps: int | None = None,
           approved_tools: list[str] | None = None) -> str:
    """Lance une exécution en arrière-plan et rend son identifiant aussitôt."""
    from nexus_os.agents import registry

    if not task.strip():
        raise ValueError("tâche vide")
    if not registry().get(agent_id):
        raise KeyError(f"agent inconnu : {agent_id}")

    task_id = uuid.uuid4().hex[:12]
    rec: dict[str, Any] = {
        "id": task_id, "state": "working", "task": task, "agent_id": agent_id,
        "approval": approval, "session_id": session_id, "max_steps": max_steps,
        "events": [], "event_count": 0, "steps": 0, "tokens": 0,
        "pending_tools": [], "result": "", "error": "", "artifacts": [],
        "created": time.time(), "updated": time.time(), "duration_ms": 0,
        "approved": list(approved_tools or []),
    }
    with _lock:
        _live[task_id] = rec
        rec["_cancel"] = False
    _save({k: v for k, v in rec.items() if not k.startswith("_")})

    threading.Thread(target=_worker, args=(task_id,), daemon=True).start()
    return task_id


def _worker(task_id: str) -> None:
    from nexus_os.runtime import Runtime

    rec = _live[task_id]
    rt = Runtime()

    def on_event(ev: dict[str, Any]) -> None:
        if rec.get("_cancel"):
            raise _Cancelled()
        rec["events"].append(ev)
        rec["event_count"] += 1
        del rec["events"][:-EVENT_TAIL]
        if ev.get("type") == "tool_result":
            rec["steps"] += 1
        if ev.get("type") == "approval_required":
            tool = ev.get("name", "")
            if tool and tool not in rec["pending_tools"]:
                rec["pending_tools"].append(tool)
            rec["state"] = "input_required"
        elif ev.get("type") == "run_end":
            rec["tokens"] += ev.get("tokens", 0)
            rec["artifacts"] = list({*rec["artifacts"], *(ev.get("artifacts") or [])})
        rec["updated"] = time.time()
        if rec["event_count"] % 5 == 0:
            _save({k: v for k, v in rec.items() if not k.startswith("_")})

    started = time.time()
    try:
        gen = rt.run(rec["task"], rec["agent_id"], session_id=rec["session_id"],
                     approval=rec["approval"], approved_tools=rec["approved"],
                     max_steps=rec["max_steps"])
        result = None
        try:
            while True:
                on_event(next(gen))
        except StopIteration as stop:
            result = stop.value
        if result is not None:
            rec["result"] = result.result
            rec["tokens"] = result.tokens
            rec["steps"] = result.steps
            rec["artifacts"] = result.artifacts
            rec["confidence"] = result.confidence
            rec["pending_tools"] = list(dict.fromkeys(
                [*rec["pending_tools"], *result.pending_approvals]))
        # Un run qui s'arrête sur une autorisation en attente n'a pas abouti :
        # l'état `input_required` est ce qui permet de le débloquer ensuite.
        rec["state"] = "input_required" if rec["pending_tools"] else "completed"
    except _Cancelled:
        rec["state"] = "cancelled"
    except Exception as e:
        rec["state"] = "failed"
        rec["error"] = f"{type(e).__name__}: {e}"
    finally:
        rec["duration_ms"] = int((time.time() - started) * 1000)
        rec["updated"] = time.time()
        _save({k: v for k, v in rec.items() if not k.startswith("_")})
        with _lock:
            _live.pop(task_id, None)


class _Cancelled(Exception):
    """Le consommateur d'événements a demandé l'arrêt."""


def cancel(task_id: str) -> bool:
    rec = _record(task_id)
    if rec["state"] not in {"working", "input_required"}:
        raise TaskError(f"tâche déjà {rec['state']} : {task_id}")
    if task_id in _live:
        _live[task_id]["_cancel"] = True
    else:                                   # tâche orpheline (redémarrage) : on marque
        rec["state"] = "cancelled"
        rec["updated"] = time.time()
        _save(rec)
    return True


def approve(task_id: str, tools: list[str] | None = None) -> str:
    """Débloque une tâche `input_required` en relançant avec les outils autorisés.

    Le runtime ne reprend pas un générateur interrompu : il rejoue la même tâche
    avec les autorisations. C'est le même contrat que le paramètre `approve` de
    l'API SSE — mais ici l'identifiant de tâche change, et l'ancien reste lisible.
    """
    rec = _record(task_id)
    if rec["state"] != "input_required":
        raise TaskError(f"rien à autoriser : tâche {rec['state']}")
    allowed = list(dict.fromkeys([*rec["pending_tools"], *(tools or [])]))
    if not allowed:
        raise TaskError("aucun outil en attente d'autorisation")
    # `smart` et non `manuel` : l'utilisateur vient d'autoriser explicitement ces
    # outils ; les rejouer en mode manuel les rebloquerait un par un, sans fin.
    new_id = submit(rec["task"], rec["agent_id"], approval="smart",
                    session_id=rec["session_id"], max_steps=rec["max_steps"],
                    approved_tools=allowed)
    with _lock:
        _live[new_id]["supersedes"] = task_id
    rec["state"] = "cancelled"
    rec["error"] = f"relancée avec autorisations : {new_id}"
    rec["updated"] = time.time()
    _save({k: v for k, v in rec.items() if not k.startswith("_")})
    return new_id


# -------------------------------------------------------------------------- #
# Lecture (fetch-later)
# -------------------------------------------------------------------------- #
def _public(rec: dict[str, Any], tail: int = 40) -> dict[str, Any]:
    out = {k: v for k, v in rec.items() if not k.startswith("_")}
    out["events"] = rec.get("events", [])[-tail:]
    out["progress"] = {
        "events": rec.get("event_count", 0),
        "steps": rec.get("steps", 0),
        "tokens": rec.get("tokens", 0),
        "artifacts": rec.get("artifacts", []),
        "pending_tools": rec.get("pending_tools", []),
    }
    return out


def get(task_id: str, *, tail: int = 40) -> dict[str, Any]:
    return _public(_record(task_id), tail)


def events(task_id: str, *, since: int = 0, limit: int = 200) -> dict[str, Any]:
    """Récupération incrémentale : ne renvoie que ce qui est arrivé après `since`."""
    rec = _record(task_id)
    all_events = rec.get("events", [])
    base = max(0, rec.get("event_count", 0) - len(all_events))
    start = max(0, since - base)
    chunk = all_events[start:start + limit]
    return {"id": task_id, "state": rec["state"], "next": since + len(chunk),
            "events": chunk, "total": rec.get("event_count", 0)}


def list_tasks(*, limit: int = 20, state: str | None = None) -> list[dict[str, Any]]:
    rows = list(_load().values())
    rows.sort(key=lambda r: r.get("created", 0), reverse=True)
    if state:
        rows = [r for r in rows if r.get("state") == state]
    return [_public(r, tail=0) for r in rows[:limit]]


def wait(task_id: str, *, timeout: float = 60.0, poll: float = 0.05) -> dict[str, Any]:
    """Bloque jusqu'à un état terminal — pratique en test et en CLI."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        rec = _record(task_id)
        if rec["state"] not in {"working"}:
            return _public(rec)
        time.sleep(poll)
    raise TaskError(f"tâche encore `working` après {timeout}s : {task_id}")


def summarize() -> dict[str, Any]:
    rows = list(_load().values())
    by_state = {s: sum(1 for r in rows if r.get("state") == s) for s in STATES}
    return {"count": len(rows), "by_state": by_state, "running": len(_live),
            "recent": [_public(r, tail=0) for r in
                       sorted(rows, key=lambda r: r.get("created", 0), reverse=True)[:10]]}


def clear(*, terminal_only: bool = True) -> int:
    data = _load()
    keep = {k: v for k, v in data.items()
            if not terminal_only or v.get("state") in {"completed", "failed", "cancelled"}}
    removed = len(data) - len(keep)
    _flush(keep)
    return removed
