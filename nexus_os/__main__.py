"""CLI NEXUS·OS — `python -m nexus_os <commande>`.

    python -m nexus_os status
    python -m nexus_os agents
    python -m nexus_os skills
    python -m nexus_os models
    python -m nexus_os route "rédige une landing page"
    python -m nexus_os run "audite la structure du dépôt" --agent orchestrator
    python -m nexus_os create "un agent qui relit les contrats"
    python -m nexus_os serve --port 8124
"""
from __future__ import annotations

import argparse
import json
import sys

from nexus_os import __version__


def _print_json(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2, default=str))


def cmd_status(_: argparse.Namespace) -> int:
    from nexus_os.runtime import Runtime

    _print_json(Runtime().status())
    return 0


def cmd_agents(_: argparse.Namespace) -> int:
    from nexus_os.agents import registry

    for a in registry().all():
        print(f"{a.emoji} {a.id:<14} {a.name:<14} {a.role}")
        print(f"   compétences : {', '.join(a.skills) or '—'}")
        print(f"   outils      : {', '.join(a.tools) or '—'}")
        print(f"   cycle       : {' → '.join(a.lifecycle)}  [{a.source}/{a.autonomy}]")
    return 0


def cmd_skills(_: argparse.Namespace) -> int:
    from nexus_os.skills import library

    for s in library().all():
        print(f"📚 {s.name:<20} {s.description}")
    return 0


def cmd_models(_: argparse.Namespace) -> int:
    from nexus_os.llm import router

    for m in router().catalog():
        state = "prêt " if m["ready"] else ("clé " if m["has_key"] else "—    ")
        price = "gratuit" if m["free"] else f"${m['price_in']}/${m['price_out']}"
        print(f"{state} {m['provider']:<11} {m['id']:<28} {m['context']:>9,} ctx  {price}")
    return 0


def cmd_route(args: argparse.Namespace) -> int:
    from nexus_os.runtime import Runtime

    _print_json(Runtime().route(args.task, limit=args.limit))
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    from nexus_os.runtime import Runtime

    rt = Runtime()
    for ev in rt.run(args.task, args.agent):
        t = ev["type"]
        if t == "phase":
            print(f"\n── {ev['index']}/{ev['total']} {ev['title']} ({ev['phase']}) " + "─" * 20)
        elif t == "tool_call":
            print(f"   ↳ {ev['name']}({json.dumps(ev['args'], ensure_ascii=False)[:200]})")
        elif t == "tool_result":
            head = ev["result"].splitlines()[:3]
            print(f"   {'✓' if ev['ok'] else '✗'} {ev['name']}: " + " | ".join(head)[:200])
        elif t == "thinking" and ev.get("text"):
            print(f"   · {ev['model']} [{ev['mode']}]")
        elif t == "routing":
            print("   routage : " + ", ".join(
                f"{c['name']}={c['score']}" for c in ev["candidates"]))
        elif t == "handoff":
            print(f"   ⇢ délégation à {ev['to']}")
        elif t == "message":
            if ev.get("depth", 0) > 0:
                head = ev["text"].strip().splitlines()[:4]
                print("   ⤷ réponse du spécialiste : " + " / ".join(head)[:240])
            else:
                print("\n" + "=" * 72 + f"\n{ev['text']}\n" + "=" * 72)
        elif t == "run_end":
            prefix = "   ⤷ " if ev.get("depth", 0) > 0 else "\n"
            print(f"{prefix}[{ev['status']}] {ev['steps']} étapes · {ev['tokens']} tokens · "
                  f"{ev['duration_ms']} ms · artefacts : {', '.join(ev['artifacts']) or 'aucun'}")
        elif t == "error":
            print(f"   ✗ {ev['message']}", file=sys.stderr)
    return 0


def cmd_create(args: argparse.Namespace) -> int:
    from nexus_os.creator import create_and_save, draft

    if args.dry_run:
        res = draft(args.description, name=args.name or "", use_llm=not args.offline)
        _print_json({"engine": res.engine, "rationale": res.rationale,
                     "test_recipe": res.test_recipe, "spec": res.spec.to_dict()})
        return 0
    res = create_and_save(args.description, name=args.name or "", use_llm=not args.offline)
    print(f"✔ agent créé : {res.spec.id} ({res.spec.name})")
    for line in res.rationale:
        print(f"  - {line}")
    print(f"  recette : {res.test_recipe}")
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    import uvicorn

    uvicorn.run("nexus_os.app:app", host=args.host, port=args.port, reload=args.reload)
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="nexus_os", description=f"NEXUS·OS v{__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="état du système").set_defaults(fn=cmd_status)
    sub.add_parser("agents", help="liste des agents").set_defaults(fn=cmd_agents)
    sub.add_parser("skills", help="liste des compétences").set_defaults(fn=cmd_skills)
    sub.add_parser("models", help="catalogue de modèles du routeur").set_defaults(fn=cmd_models)

    r = sub.add_parser("route", help="quel agent doit traiter cette tâche ?")
    r.add_argument("task")
    r.add_argument("--limit", type=int, default=5)
    r.set_defaults(fn=cmd_route)

    run = sub.add_parser("run", help="exécute une tâche avec un agent")
    run.add_argument("task")
    run.add_argument("--agent", default="orchestrator")
    run.set_defaults(fn=cmd_run)

    c = sub.add_parser("create", help="crée un agent spécialisé")
    c.add_argument("description")
    c.add_argument("--name", default="")
    c.add_argument("--offline", action="store_true", help="moteur de règles, sans modèle live")
    c.add_argument("--dry-run", action="store_true", help="affiche la spec sans l'enregistrer")
    c.set_defaults(fn=cmd_create)

    s = sub.add_parser("serve", help="démarre l'interface web")
    s.add_argument("--host", default="0.0.0.0")
    s.add_argument("--port", type=int, default=8124)
    s.add_argument("--reload", action="store_true")
    s.set_defaults(fn=cmd_serve)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
