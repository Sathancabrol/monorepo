#!/usr/bin/env python3
"""
audit_memory.py — Mémoire d'audit : rapide, compacte, sans dépendance.

Source de vérité  : audit/state.json          (machine, lisible/écrivable)
Index compact     : audit/MEMORY.md           (généré : `render`)
Journal           : audit/JOURNAL.jsonl       (append-only : `log`)
Graphe de connaissances : audit/graph.json    (nœuds/arêtes : `graph`)
Notes détaillées  : audit/notes/*.md          (une par périmètre)

But : limiter les tokens. `status`/`get`/`next` n'impriment que l'essentiel.
Aucune connexion réseau. Stdlib uniquement.

Usage :
  python3 scripts/audit_memory.py init
  python3 scripts/audit_memory.py status            # tableau compact
  python3 scripts/audit_memory.py get projects.COGNITORIUM.status
  python3 scripts/audit_memory.py set projects.COGNITORIUM.status done
  python3 scripts/audit_memory.py set phase.current P3
  python3 scripts/audit_memory.py next              # prochaines actions
  python3 scripts/audit_memory.py log "message" --tag P2
  python3 scripts/audit_memory.py fact projects.COGNITORIUM.facts.files 131
  python3 scripts/audit_memory.py render            # régénère MEMORY.md + graph.json
  python3 scripts/audit_memory.py check
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / "audit"
STATE = AUDIT / "state.json"
MEMORY = AUDIT / "MEMORY.md"
JOURNAL = AUDIT / "JOURNAL.jsonl"
GRAPH = AUDIT / "graph.json"
NOTES = AUDIT / "notes"

PHASES = {
    "P0": "Cadrage & plan",
    "P1": "Mémoire & instrumentation",
    "P2": "Inventaire factuel",
    "P3": "Audit par projet",
    "P4": "Audit transversal",
    "P5": "Audit externe (GitHub + connecteurs)",
    "P6": "Synthèse & tableaux",
    "P7": "Contrôle qualité & publication",
}


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def save(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def get_dotted(data, dotted: str):
    cur = data
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        elif isinstance(cur, list) and part.isdigit():
            cur = cur[int(part)]
        else:
            raise KeyError(dotted)
    return cur


def set_dotted(data, dotted: str, value) -> None:
    parts = dotted.split(".")
    cur = data
    for part in parts[:-1]:
        if isinstance(cur, dict):
            cur = cur.setdefault(part, {})
        elif isinstance(cur, list):
            cur = cur[int(part)]
    cur[parts[-1]] = value


def parse_value(raw: str):
    if raw.lower() in {"true", "false"}:
        return raw.lower() == "true"
    if raw.lower() in {"null", "none"}:
        return None
    try:
        return json.loads(raw)
    except Exception:
        return raw


def cmd_init(_args) -> None:
    AUDIT.mkdir(exist_ok=True)
    NOTES.mkdir(exist_ok=True)
    if not STATE.exists():
        save(STATE, {
            "schema": 1,
            "audit": {"id": "audit-2026-10", "title": "Audit complet monorepo Sathancabrol",
                      "started_at": now(), "updated_at": now(), "operator": "agent"},
            "phase": {"current": "P0", "done": [], "phases": PHASES},
            "scope": {"root_dossier_documents": 0, "projects": {}, "other_docs": 0},
            "projects": {},
            "counters": {"findings": 0, "files_examined": 0, "tables": 0},
            "next_actions": [],
        })
        print(f"init: {STATE.relative_to(ROOT)}")
    else:
        print(f"init: {STATE.relative_to(ROOT)} existe déjà")
    JOURNAL.touch()
    cmd_render(None)


def cmd_status(_args) -> None:
    st = load(STATE, {})
    ph = st.get("phase", {})
    print(f"AUDIT {st.get('audit',{}).get('id','?')} | phase {ph.get('current','?')} "
          f"| maj {st.get('audit',{}).get('updated_at','?')}")
    done = set(ph.get("done", []))
    print("Phases: " + " ".join(
        f"{k}{'✓' if k in done else ('→' if k == ph.get('current') else '·')}"
        for k in sorted(ph.get("phases", PHASES))))
    projs = st.get("projects", {})
    if projs:
        print(f"\n{'Projet':<32} {'Statut':<10} {'Notes':<28} {'Risque':<8} Faits")
        for name, p in projs.items():
            facts = p.get("facts", {})
            fact_s = ",".join(f"{k}={v}" for k, v in list(facts.items())[:3])
            print(f"{name:<32} {str(p.get('status','?')):<10} {str(p.get('notes',''))[:27]:<28} "
                  f"{str(p.get('risk','-')):<8} {fact_s}")
    nxt = st.get("next_actions", [])
    if nxt:
        print("\nProchaines actions :")
        for a in nxt[:8]:
            print(f"  - {a}")
    print(f"\nCompteurs : {st.get('counters', {})}")


def cmd_get(args) -> None:
    st = load(STATE, {})
    try:
        val = get_dotted(st, args.path)
    except KeyError:
        print(f"absent: {args.path}", file=sys.stderr)
        sys.exit(1)
    if isinstance(val, (dict, list)):
        print(json.dumps(val, ensure_ascii=False))
    else:
        print(val)


def cmd_set(args) -> None:
    st = load(STATE, {})
    set_dotted(st, args.path, parse_value(args.value))
    st.setdefault("audit", {})["updated_at"] = now()
    save(STATE, st)
    print(f"set {args.path} = {args.value}")


def cmd_fact(args) -> None:
    st = load(STATE, {})
    set_dotted(st, f"projects.{args.project}.facts.{args.key}", parse_value(args.value))
    st.setdefault("audit", {})["updated_at"] = now()
    save(STATE, st)
    print(f"fact {args.project}.{args.key} = {args.value}")


def cmd_next(_args) -> None:
    st = load(STATE, {})
    for a in st.get("next_actions", []):
        print(f"- {a}")


def cmd_log(args) -> None:
    entry = {"ts": now(), "tag": args.tag or "", "msg": args.message}
    with JOURNAL.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print("log ok")


def cmd_render(_args) -> None:
    st = load(STATE, {})
    ph = st.get("phase", {})
    done = set(ph.get("done", []))
    rows = ["| Projet | Statut | Phase | Risque | Notes |", "|---|---|---|---|---|"]
    for name, p in st.get("projects", {}).items():
        rows.append(f"| {name} | {p.get('status','?')} | {p.get('phase','-')} | "
                    f"{p.get('risk','-')} | {p.get('notes','-')} |")
    nxt = "\n".join(f"- {a}" for a in st.get("next_actions", [])) or "- (vide)"
    phases = "\n".join(
        f"- [{'x' if k in done else ('>' if k == ph.get('current') else ' ')}] {k} {v}"
        for k, v in sorted(ph.get("phases", PHASES).items()))
    MEMORY.write_text(f"""# MEMORY — Audit monorepo (index généré)

> **NE PAS ÉDITER À LA MAIN** — généré par `python3 scripts/audit_memory.py render`
> depuis `audit/state.json`. Mis à jour : {now()}

## Où est quoi

| Fichier | Rôle |
|---|---|
| `audit/PLAN.md` | plan de processus, périmètre, méthode |
| `audit/CATEGORIES.md` | taxonomie canonique (noms de catégories + règles) |
| `audit/state.json` | **source de vérité machine** (statuts, faits, actions) |
| `audit/JOURNAL.jsonl` | journal append-only des itérations |
| `audit/notes/*.md` | notes factuelles par périmètre |
| `audit/graph.json` | graphe de connaissances (projets ↔ docs ↔ dépendances) |
| `audit/AUDIT-2026-10.md` | livrable final (tableaux) |

## État courant

- Audit : `{st.get('audit',{}).get('id','?')}` — {st.get('audit',{}).get('title','?')}
- Phase courante : **{ph.get('current','?')} — {ph.get('phases',PHASES).get(ph.get('current',''),'')}**
- Compteurs : {json.dumps(st.get('counters',{}))}

## Prochaines actions

{nxt}

## Projets

{chr(10).join(rows) if len(rows) > 2 else '(pas encore initialisé)'}

## Phases

{phases}
""", encoding="utf-8")
    save(GRAPH, build_graph(st))
    print(f"render ok -> {MEMORY.relative_to(ROOT)} + {GRAPH.relative_to(ROOT)}")


def build_graph(st) -> dict:
    """Graphe de connaissances minimal : nœuds + arêtes, requêtable."""
    nodes, edges = [], []
    for name, p in st.get("projects", {}).items():
        nodes.append({"id": f"project:{name}", "type": "project", "status": p.get("status"),
                      "repo": p.get("repo"), "facts": p.get("facts", {})})
        for dep in p.get("depends_on", []):
            edges.append({"from": f"project:{name}", "to": f"project:{dep}", "rel": "depends_on"})
        for dup in p.get("duplicates", []):
            edges.append({"from": f"project:{name}", "to": dup, "rel": "duplicates"})
    for f in st.get("artifacts", []):
        nodes.append({"id": f, "type": "artifact"})
    edges += st.get("extra_edges", [])
    return {"generated_at": now(), "nodes": nodes, "edges": edges}


def cmd_check(_args) -> None:
    st = load(STATE, {})
    problems = []
    for key in ("schema", "audit", "phase", "projects", "counters"):
        if key not in st:
            problems.append(f"clé manquante: {key}")
    for name, p in st.get("projects", {}).items():
        for key in ("status", "notes"):
            if key not in p:
                problems.append(f"{name}: champ manquant {key}")
        if p.get("status") == "done" and not p.get("facts"):
            problems.append(f"{name}: marqué done sans faits")
    if not (AUDIT / "PLAN.md").exists():
        problems.append("audit/PLAN.md manquant")
    if not (AUDIT / "CATEGORIES.md").exists():
        problems.append("audit/CATEGORIES.md manquant")
    print("check: " + ("OK" if not problems else "\n- " + "\n- ".join(problems)))
    sys.exit(1 if problems else 0)


def main() -> None:
    ap = argparse.ArgumentParser(description="Mémoire d'audit (rapide, JSON + MD généré)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init").set_defaults(fn=cmd_init)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    sub.add_parser("next").set_defaults(fn=cmd_next)
    sub.add_parser("render").set_defaults(fn=cmd_render)
    sub.add_parser("check").set_defaults(fn=cmd_check)
    g = sub.add_parser("get"); g.add_argument("path"); g.set_defaults(fn=cmd_get)
    s = sub.add_parser("set"); s.add_argument("path"); s.add_argument("value"); s.set_defaults(fn=cmd_set)
    f = sub.add_parser("fact"); f.add_argument("project"); f.add_argument("key"); f.add_argument("value"); f.set_defaults(fn=cmd_fact)
    lg = sub.add_parser("log"); lg.add_argument("message"); lg.add_argument("--tag", default=""); lg.set_defaults(fn=cmd_log)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
