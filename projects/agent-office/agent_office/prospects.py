"""Service PROSPECTS — mini-CRM pipeline + relances dues.

Étapes : cible → contacté → rdv → proposition → gagné | perdu.
Jamais de suppression : `move` vers 'perdu' + notes.
"""
import argparse
import datetime as dt
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "prospects.json"
ETAPES = ["cible", "contacté", "rdv", "proposition", "gagné", "perdu"]

CAPABILITY = {
    "name": "prospects",
    "service": "Prospection",
    "capability": "Pipeline prospects par offre (O1/O2/O3), prochaines actions, relances dues",
    "commands": ["prospects list [--etape x]", "prospects next", "prospects add ...", "prospects move --id N --etape x"],
}


def load():
    return json.loads(DATA.read_text(encoding="utf-8"))


def save(db):
    DATA.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")


def main(argv):
    p = argparse.ArgumentParser(prog="prospects", description="Mini-CRM")
    sub = p.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("list")
    l.add_argument("--etape")
    sub.add_parser("next", help="actions dues aujourd'hui ou en retard")
    a = sub.add_parser("add")
    for f in ["nom", "org", "offre", "contact", "action", "echeance", "notes"]:
        a.add_argument(f"--{f}", default="")
    m = sub.add_parser("move")
    m.add_argument("--id", required=True, type=int)
    m.add_argument("--etape", required=True, choices=ETAPES)
    m.add_argument("--note", default="")
    args = p.parse_args(argv)
    db = load()
    if args.cmd == "list":
        for x in db:
            if args.etape and x["etape"] != args.etape:
                continue
            print(f"[{x['id']}] {x['nom']} ({x['org']}) — {x['offre']} · {x['etape']}")
            if x.get("action"):
                print(f"      → {x['action']} (échéance {x.get('echeance', '?')})")
        return 0
    if args.cmd == "next":
        today = dt.date.today().isoformat()
        due = [x for x in db if x.get("echeance") and x["echeance"] <= today and x["etape"] not in ("gagné", "perdu")]
        if not due:
            print("✅ aucune relance due aujourd'hui")
            return 0
        for x in due:
            print(f"⏰ [{x['id']}] {x['nom']} — {x.get('action', 'relancer')} (dû {x['echeance']})")
        return 0
    if args.cmd == "add":
        nid = max([x["id"] for x in db], default=0) + 1
        db.append({"id": nid, "nom": args.nom, "org": args.org, "offre": args.offre, "etape": "cible",
                   "contact": args.contact, "action": args.action, "echeance": args.echeance, "notes": args.notes})
        save(db)
        print(f"✅ prospect {nid} ajouté : {args.nom}")
        return 0
    if args.cmd == "move":
        for x in db:
            if x["id"] == args.id:
                x["etape"] = args.etape
                if args.note:
                    x["notes"] = (x.get("notes", "") + " | " + args.note).strip(" |")
                save(db)
                print(f"✅ [{args.id}] → {args.etape}")
                return 0
        print(f"❌ prospect {args.id} introuvable")
        return 1
    return 2


def selftest():
    db = load()
    assert db and all("id" in x and "etape" in x for x in db)
    return f"prospects OK — {len(db)} fiches pipeline"
