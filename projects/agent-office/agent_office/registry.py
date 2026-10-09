"""Service REGISTRY — registre des capacités (tools.json) + doctor.

Le registre est la fiche d'identité de l'entreprise d'IA : chaque service
déclare ses capacités ; l'agent (ou un humain) sait immédiatement quoi appeler.
"""
import argparse
import json
from pathlib import Path

from . import arena, budget, invoices, maildigest, marketing, planning, prospects, research, update

BASE = Path(__file__).resolve().parent.parent
TOOLS_JSON = BASE / "tools.json"
MODULES = [budget, invoices, marketing, prospects, research, maildigest, planning, arena, update]

CAPABILITY = {
    "name": "registry",
    "service": "Direction",
    "capability": "Registre des capacités de l'entreprise (tools.json) + auto-tests (doctor)",
    "commands": ["registry list", "registry build", "registry doctor"],
}


def collect():
    return [m.CAPABILITY for m in MODULES] + [CAPABILITY]


def main(argv):
    p = argparse.ArgumentParser(prog="registry", description="Registre & doctor")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    sub.add_parser("build")
    sub.add_parser("doctor")
    args = p.parse_args(argv)
    if args.cmd == "list":
        caps = collect()
        print(f"🏢 ENTREPRISE D'IA — {len(caps)} services déclarés\n")
        for c in caps:
            print(f"[{c['service']}] {c['name']:<10} {c['capability']}")
        return 0
    if args.cmd == "build":
        TOOLS_JSON.write_text(
            json.dumps({"generated_by": "agent-office", "services": collect()}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"✅ {TOOLS_JSON} régénéré")
        return 0
    if args.cmd == "doctor":
        ok = True
        for m in MODULES:
            try:
                print(f"  ✔ {m.selftest()}")
            except Exception as e:  # noqa: BLE001
                ok = False
                print(f"  ✖ {m.__name__.split('.')[-1]} : {e}")
        print("\n" + ("🟢 tous les services opérationnels" if ok else "🔴 au moins un service en défaut"))
        return 0 if ok else 1
    return 2


def selftest():
    caps = collect()
    assert len(caps) >= 8 and all("name" in c and "capability" in c for c in caps)
    return f"registry OK — {len(caps)} capacités déclarées"
