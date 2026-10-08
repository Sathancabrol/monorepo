"""Service BUDGET — suivi mensuel, totaux LOCK/MOVE, alerte déficit.

CSV colonnes : date,libelle,categorie,type(revenu|depense),montant,statut(LOCK|MOVE)
Le fichier seed reprend les vrais chiffres de USER/FINANCES/BUDGET-MENSUEL.md.
"""
import argparse
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "budget_transactions.csv"

CAPABILITY = {
    "name": "budget",
    "service": "Finance",
    "capability": "Suivi budget mensuel : totaux par catégorie/statut, restant, alerte déficit",
    "commands": ["budget report [--month AAAA-MM]", "budget add --date --libelle --categorie --type --montant [--statut]"],
}


def load_rows(path=DATA):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["montant"] = float(r["montant"])
            rows.append(r)
    return rows


def summarize(rows, month=None):
    sel = [r for r in rows if month is None or r["date"].startswith(month)]
    rev = sum(r["montant"] for r in sel if r["type"] == "revenu")
    dep = sum(r["montant"] for r in sel if r["type"] == "depense")
    lock = sum(r["montant"] for r in sel if r["statut"] == "LOCK" and r["type"] == "depense")
    par_cat = {}
    for r in sel:
        c = par_cat.setdefault(r["categorie"], {"revenu": 0.0, "depense": 0.0})
        c[r["type"]] += r["montant"]
    return {
        "revenus": rev,
        "depenses": dep,
        "lock": lock,
        "restant": rev - dep,
        "par_categorie": par_cat,
        "n": len(sel),
    }


def euro(x):
    return f"{x:,.2f} €".replace(",", " ")


def cmd_report(args):
    rows = load_rows(Path(args.csv) if args.csv else DATA)
    s = summarize(rows, args.month)
    scope = args.month or "toutes dates"
    print(f"📊 BUDGET — {scope} ({s['n']} écritures)\n")
    print(f"  Revenus       {euro(s['revenus']):>12}")
    print(f"  Dépenses      {euro(s['depenses']):>12}")
    print(f"  dont LOCK     {euro(s['lock']):>12}")
    print(f"  ─────────────────────────────")
    print(f"  RESTANT       {euro(s['restant']):>12}")
    print("\n  Par catégorie :")
    for cat, v in sorted(s["par_categorie"].items()):
        print(f"    {cat:<20} rev {euro(v['revenu']):>10}   dép {euro(v['depense']):>10}")
    if s["restant"] < 0:
        print("\n  ⚠️  DÉFICIT STRUCTUREL — voir USER/TELOS/CURRENT_STATE/MONEY.md (pistes O1/O2/O3)")
    return 0


def cmd_add(args):
    path = Path(args.csv) if args.csv else DATA
    with open(path, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(
            [args.date, args.libelle, args.categorie, args.type, f"{args.montant:.2f}", args.statut]
        )
    print(f"✅ ajouté : {args.libelle} ({args.type} {euro(args.montant)}) dans {path.name}")
    return 0


def main(argv):
    p = argparse.ArgumentParser(prog="budget", description="Suivi budget")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("report", help="rapport mensuel")
    r.add_argument("--month", help="filtre AAAA-MM")
    r.add_argument("--csv", help="autre fichier csv")
    r.set_defaults(fn=cmd_report)
    a = sub.add_parser("add", help="ajouter une écriture")
    a.add_argument("--date", required=True)
    a.add_argument("--libelle", required=True)
    a.add_argument("--categorie", required=True)
    a.add_argument("--type", required=True, choices=["revenu", "depense"])
    a.add_argument("--montant", required=True, type=float)
    a.add_argument("--statut", default="MOVE", choices=["LOCK", "MOVE"])
    a.add_argument("--csv")
    a.set_defaults(fn=cmd_add)
    args = p.parse_args(argv)
    return args.fn(args)


def selftest():
    s = summarize(load_rows())
    assert s["n"] > 0 and s["revenus"] > 0
    return f"budget OK — {s['n']} écritures, restant {euro(s['restant'])}"
