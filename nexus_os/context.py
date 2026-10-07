"""Résultats référencés et compression de contexte.

Deux constats convergents de l'écosystème 2026 :

* la feuille de route MCP introduit les **résultats référencés** — le client
  décide *quand* tirer un gros payload en contexte, au lieu de le subir ;
* ``mksglu/context-mode`` (~98 % de réduction annoncée) sandboxe la sortie des
  outils et ne remonte qu'un résumé.

Le principe appliqué ici : **un résultat d'outil volumineux ne rentre pas dans
le contexte**. Il est écrit dans la sandbox, et l'agent reçoit une *référence*
— taille, forme, aperçu — qu'il peut charger ensuite, au bon moment, avec
``read_file``. Le gain en tokens est mesuré, pas supposé.

La seconde moitié du module compacte un historique d'exécution en résumé
sémantique (motif ``claude-mem`` : hooks de cycle de vie + injection ciblée).
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any, Iterable

from nexus_os import config

#: Au-delà de cette taille, un résultat devient une référence.
THRESHOLD_CHARS = int(getattr(config, "REFERENCE_THRESHOLD", 1_800))
#: Longueur de l'aperçu conservé dans le contexte.
PREVIEW_CHARS = 420
#: Ratio characters→tokens utilisé pour chiffrer le gain (4 car. ≈ 1 token).
CHARS_PER_TOKEN = 4

REF_DIRNAME = "references"
INDEX_NAME = "index.json"


# -------------------------------------------------------------------------- #
# Références
# -------------------------------------------------------------------------- #
def _ref_dir() -> Path:
    d = Path(config.WORKSPACE_DIR) / REF_DIRNAME
    d.mkdir(parents=True, exist_ok=True)
    return d


def _slug(text: str, limit: int = 34) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "ref").lower()).strip("-")
    return (s[:limit].rstrip("-")) or "ref"


def _index_path() -> Path:
    return _ref_dir() / INDEX_NAME


def _load_index() -> list[dict[str, Any]]:
    p = _index_path()
    if not p.exists():
        return []
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
        return raw if isinstance(raw, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _save_index(rows: list[dict[str, Any]]) -> None:
    _index_path().write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")


def tokens_of(text: str) -> int:
    """Estimation basse, volontairement conservative."""
    return max(1, len(text or "") // CHARS_PER_TOKEN)


def reference(ctx: Any, text: str, *, kind: str = "", preview: int = PREVIEW_CHARS) -> str:
    """Renvoie `text` tel quel s'il est court, sinon une référence compacte.

    `ctx` est un `ToolContext` (on n'utilise que `workspace` et `agent_id`), ce
    qui évite d'importer `tools` ici et donc toute importation circulaire.
    """
    text = text if isinstance(text, str) else json.dumps(text, ensure_ascii=False, default=str)
    if len(text) <= THRESHOLD_CHARS:
        return text

    root = Path(getattr(ctx, "workspace", None) or config.WORKSPACE_DIR) / REF_DIRNAME
    root.mkdir(parents=True, exist_ok=True)
    rows = _load_index()
    rid = f"ref-{len(rows) + 1:04d}"
    fname = f"{rid}-{_slug(kind or 'resultat')}.txt"
    (root / fname).write_text(text, encoding="utf-8")

    saved_chars = len(text) - preview
    rows.append({
        "id": rid, "path": f"{REF_DIRNAME}/{fname}", "kind": kind or "resultat",
        "chars": len(text), "tokens": tokens_of(text),
        "saved_chars": saved_chars, "saved_tokens": tokens_of(text) - tokens_of(text[:preview]),
        "agent_id": getattr(ctx, "agent_id", "") or "", "ts": time.time(),
    })
    _save_index(rows)

    shape = _shape_of(text)
    return "\n".join([
        f"[référence {rid} · {kind or 'résultat'} · {len(text):,} caractères "
        f"≈ {tokens_of(text):,} tokens · {saved_chars // CHARS_PER_TOKEN:,} tokens économisés]",
        f"forme : {shape}",
        f"aperçu ({preview} premiers caractères) :",
        text[:preview].rstrip(),
        "…",
        f'Charge le reste avec read_file("{REF_DIRNAME}/{fname}") — '
        "ou demande une plage précise plutôt que tout le contenu.",
    ])


def _shape_of(text: str) -> str:
    """Une empreinte structurelle : ce que l'agent doit savoir avant de charger."""
    lines = text.count("\n") + 1
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, ValueError):
        data = None
    if isinstance(data, list):
        keys = sorted({k for it in data[:20] if isinstance(it, dict) for k in it})[:8]
        return f"JSON array, {len(data)} éléments" + (f", champs {', '.join(keys)}" if keys else "")
    if isinstance(data, dict):
        return f"JSON object, clés {', '.join(sorted(data)[:8])}"
    if text.lstrip().startswith("<"):
        return f"balisage, {lines} lignes"
    return f"texte, {lines} lignes, {len(set(text.lower().split()))} mots distincts"


def stats() -> dict[str, Any]:
    rows = _load_index()
    total_chars = sum(r.get("chars", 0) for r in rows)
    saved_chars = sum(r.get("saved_chars", 0) for r in rows)
    return {
        "threshold_chars": THRESHOLD_CHARS,
        "preview_chars": PREVIEW_CHARS,
        "references": len(rows),
        "chars_referenced": total_chars,
        "chars_saved": saved_chars,
        "tokens_saved": sum(r.get("saved_tokens", 0) for r in rows),
        "ratio": round(saved_chars / total_chars, 3) if total_chars else 0.0,
        "recent": rows[-8:],
    }


def clear() -> int:
    rows = _load_index()
    root = _ref_dir()
    for r in rows:
        (root / Path(r["path"]).name).unlink(missing_ok=True)
    _save_index([])
    return len(rows)


# -------------------------------------------------------------------------- #
# Compression d'historique (motif claude-mem)
# -------------------------------------------------------------------------- #
#: Ce qui mérite de survivre à la compression.
_KEPT_TYPES = {"message", "tool_call", "tool_result", "artifact", "agent_created",
               "approval_required", "error", "handoff"}


def compact(events: Iterable[dict[str, Any]], *, limit: int = 900,
            task: str = "") -> str:
    """Résumé sémantique d'une exécution : ce qui a été fait, pas ce qui a été dit.

    Déterministe et hors-ligne : aucun appel LLM, donc reproductible en test.
    """
    kept = [e for e in events if e.get("type") in _KEPT_TYPES]
    lines: list[str] = []
    if task:
        lines.append(f"Tâche : {task[:160]}")
    for e in kept:
        t = e["type"]
        if t == "tool_call":
            lines.append(f"- outil {e.get('name')}({json.dumps(e.get('args', {}), ensure_ascii=False)[:90]})")
        elif t == "tool_result":
            ok = "ok" if e.get("ok") else "échec"
            lines.append(f"- {e.get('name')} → {ok} : {str(e.get('result', ''))[:90]}")
        elif t == "artifact":
            lines.append(f"- artéfact {e.get('path')}")
        elif t == "agent_created":
            a = e.get("agent", {})
            lines.append(f"- agent créé {a.get('id')}")
        elif t == "approval_required":
            lines.append(f"- autorisation demandée : {e.get('name')} ({e.get('reason', '')})")
        elif t == "handoff":
            lines.append(f"- délégation → {e.get('to')}")
        elif t == "error":
            lines.append(f"- erreur : {str(e.get('message'))[:120]}")
        elif t == "message":
            body = str(e.get("text", "")).strip().splitlines()
            lines.append(f"- conclusion ({e.get('confidence', '—')}) : {body[0][:120] if body else ''}")
    out = "\n".join(lines).strip() or "(rien à retenir de cette exécution)"
    return out if len(out) <= limit else out[:limit].rsplit("\n", 1)[0] + "\n…"


def compaction_ratio(events: Iterable[dict[str, Any]], summary: str, *,
                     task: str = "") -> float:
    """Part du volume d'origine conservée après compression (0.05 = 95 % perdus)."""
    events = list(events)
    raw = len(task) + sum(len(json.dumps(e, ensure_ascii=False, default=str)) for e in events)
    return round(len(summary) / raw, 4) if raw else 0.0
