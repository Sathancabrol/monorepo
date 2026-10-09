"""Service UPDATE — boucle d'auto-mise à jour du système agentique.

Patterns implémentés (voir docs/AUTO-MAJ-SYSTEME-AGENTIQUE.md) :
- journal : trace des mises à jour (outils/recherche/décisions)
- lessons : mémoire de leçons apprise (pattern Reflexion, en fichiers)
- changelog : le système régénère son propre historique depuis git
- check : fraîcheur du registre + auto-tests (garde-fou avant toute évolution)
"""
import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
JOURNAL = DATA / "update_journal.json"
LESSONS = DATA / "update_lessons.json"

CAPABILITY = {
    "name": "update",
    "service": "Évolution",
    "capability": "Auto-mise à jour : journal des évolutions, leçons (Reflexion), changelog auto, vérification du registre",
    "commands": [
        "update journal --type outil|recherche|decision --note ...",
        "update lessons [--add 'leçon apprise']",
        "update changelog [-n 20]",
        "update check",
    ],
}


def load(path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def save(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_journal(args):
    db = load(JOURNAL, [])
    if args.list:
        for e in db[-15:]:
            print(f"[{e['date']}] ({e['type']}) {e['note']}")
        if not db:
            print("journal vide")
        return 0
    if not args.note:
        print("❌ --note requis (ou --list)")
        return 1
    db.append({"date": dt.datetime.now().isoformat(timespec="seconds"), "type": args.type, "note": args.note})
    save(JOURNAL, db)
    print(f"✅ journal : entrée {len(db)} ({args.type})")
    return 0


def cmd_lessons(args):
    db = load(LESSONS, [])
    if args.add:
        db.append({"date": dt.date.today().isoformat(), "lecon": args.add})
        save(LESSONS, db)
        print(f"✅ leçon enregistrée ({len(db)} au total) — pattern Reflexion")
        return 0
    if not db:
        print("aucune leçon enregistrée")
        return 0
    for e in db:
        print(f"• [{e['date']}] {e['lecon']}")
    return 0


def cmd_changelog(args):
    repo = BASE.parent.parent
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "log", f"-{args.n}", "--pretty=format:%ad %s", "--date=short"],
            capture_output=True, text=True, timeout=20,
        )
        lines = out.stdout.strip().splitlines()
    except Exception as e:  # noqa: BLE001
        print(f"❌ git indisponible : {e}")
        return 1
    if not lines or lines == [""]:
        print("❌ aucun commit trouvé")
        return 1
    md = "# 📜 CHANGELOG AUTO-GÉNÉRÉ\n> le système documente sa propre évolution (git log)\n\n" + "\n".join(
        f"- **{l[:10]}** — {l[11:]}" for l in lines
    )
    print(md)
    return 0


def cmd_check(args):
    from . import registry
    caps = registry.collect()
    names = sorted(c["name"] for c in caps)
    print(f"✅ registre : {len(caps)} services déclarés — {', '.join(names)}")
    failures = []
    for mod in registry.MODULES:
        try:
            mod.selftest()
        except Exception as e:  # noqa: BLE001
            failures.append(f"{mod.__name__}: {e}")
    if failures:
        for f in failures:
            print(f"  ✖ {f}")
        print("🔴 garde-fou : corriger avant toute évolution du système")
        return 1
    print("🟢 garde-fou levé : le système peut évoluer (tests verts)")
    return 0


def main(argv):
    p = argparse.ArgumentParser(prog="update", description="Auto-mise à jour du système agentique")
    sub = p.add_subparsers(dest="cmd", required=True)
    j = sub.add_parser("journal")
    j.add_argument("--type", default="decision", choices=["outil", "recherche", "decision"])
    j.add_argument("--note")
    j.add_argument("--list", action="store_true")
    j.set_defaults(fn=cmd_journal)
    l = sub.add_parser("lessons")
    l.add_argument("--add")
    l.set_defaults(fn=cmd_lessons)
    c = sub.add_parser("changelog")
    c.add_argument("-n", type=int, default=20)
    c.set_defaults(fn=cmd_changelog)
    sub.add_parser("check").set_defaults(fn=cmd_check)
    args = p.parse_args(argv)
    return args.fn(args)


def selftest():
    assert len(CAPABILITY["commands"]) == 4
    return "update OK — journal, leçons, changelog, check"
