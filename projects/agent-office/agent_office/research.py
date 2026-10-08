"""Service RESEARCH — briefs, citations, veille.

S'articule avec projects/reaserch-engine : les briefs produits ici peuvent
être injectés comme questions d'entrée du moteur (question → evidence → synthèse).
"""
import argparse
import datetime as dt
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
OUT = DATA.parent / "out"

CAPABILITY = {
    "name": "research",
    "service": "Recherche",
    "capability": "Briefs de recherche structurés, registre de citations, liste de veille (→ reaserch-engine)",
    "commands": ["research brief --question '...'", "research cite --url u --titre t", "research watch --query q"],
}

BRIEF_TPL = """# Brief de recherche — {q}
> produit le {date} par agent-office/research · destiné à reaserch-engine

## 1. Contexte & motivation
À COMPLÉTER : pourquoi cette question maintenant, pour quelle offre (O1/O2/O3) ?

## 2. Questions clés à trancher
- [ ] Q1 :
- [ ] Q2 :
- [ ] Q3 :

## 3. Types de sources attendues
- [ ] littérature académique
- [ ] retours terrain / interviews
- [ ] données publiques (open data)
- [ ] veille concurrentielle

## 4. Sources candidates
| # | URL | Titre | Fiabilité (1-5) | Note |
|---|-----|-------|-----------------|------|
| 1 |     |       |                 |      |

## 5. Critère de succès
La recherche est close quand : À COMPLÉTER.

## 6. Contradictions à chercher (méthode reaserch-engine)
- thèse :
- antithèse :
"""


def main(argv):
    p = argparse.ArgumentParser(prog="research", description="Recherche & veille")
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("brief")
    b.add_argument("--question", required=True)
    b.add_argument("--out")
    c = sub.add_parser("cite")
    c.add_argument("--url", required=True)
    c.add_argument("--titre", required=True)
    c.add_argument("--note", default="")
    w = sub.add_parser("watch")
    w.add_argument("--query", required=True)
    args = p.parse_args(argv)
    today = dt.date.today().isoformat()
    if args.cmd == "brief":
        OUT.mkdir(exist_ok=True)
        slug = "".join(ch if ch.isalnum() else "-" for ch in args.question.lower())[:60].strip("-")
        path = Path(args.out) if args.out else OUT / f"brief-{slug}.md"
        path.write_text(BRIEF_TPL.format(q=args.question, date=today), encoding="utf-8")
        print(f"✅ brief → {path}")
        return 0
    if args.cmd == "cite":
        f = DATA / "citations.json"
        db = json.loads(f.read_text(encoding="utf-8")) if f.exists() else []
        db.append({"date": today, "url": args.url, "titre": args.titre, "note": args.note})
        f.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ citation enregistrée ({len(db)} au total)")
        return 0
    if args.cmd == "watch":
        f = DATA / "watch_queries.json"
        db = json.loads(f.read_text(encoding="utf-8")) if f.exists() else []
        if args.query not in db:
            db.append(args.query)
        f.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ veille ajoutée : « {args.query} » ({len(db)} requêtes)")
        return 0
    return 2


def selftest():
    assert "reaserch-engine" in BRIEF_TPL
    return "research OK — gabarit brief avec contradictions et registre citations"
