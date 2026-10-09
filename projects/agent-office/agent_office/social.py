"""Service SOCIAL — l'équipe marketing/réseaux (rôles = rédacteur/éditeur/publisher/écouteur).

Publication réelle déléguée à Postiz (MCP) quand il sera hébergé ; ici :
calendrier éditorial, drafts par plateforme (limites réelles), checklist de
porte humaine, méthode d'écoute sociale. Jamais de publication automatique.
"""
import argparse
import datetime as dt
import json
from pathlib import Path

from .marketing import OFFERS

DATA = Path(__file__).resolve().parent.parent / "data" / "social_calendar.json"

CAPABILITY = {
    "name": "social",
    "service": "Marketing",
    "capability": "Équipe réseaux : calendrier éditorial, drafts par plateforme, checklist humaine, écoute sociale",
    "commands": [
        "social calendar", "social add --titre t --plateformes x,linkedin --date AAAA-MM-JJ",
        "social draft --offer O1 --plateforme x", "social check", "social listen --theme t",
    ],
}

PLATFORMES = {
    "x": 280,
    "linkedin": 3000,
    "instagram": 2200,
    "facebook": 5000,
    "tiktok": 2200,
    "threads": 500,
}


def load():
    if DATA.exists():
        return json.loads(DATA.read_text(encoding="utf-8"))
    return []


def save(db):
    DATA.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")


def draft(offer_key, plateforme):
    o = OFFERS[offer_key]
    limite = PLATFORMES[plateforme]
    corps = (
        f"{o['promesse']}\n\nDéjà produit : {o['preuves'][0]}.\n\n{o['cta']}."
        if plateforme != "x" else
        f"{o['titre']} — {o['promesse'].split(',')[0]}. Preuve : {o['preuves'][0].lower()}. {o['cta']}."
    )
    if len(corps) > limite:
        corps = corps[: limite - 1].rstrip() + "…"
    return f"[{plateforme.upper()} — max {limite} car. | {len(corps)} utilisés]\n{corps}"


def cmd_calendar(args):
    db = load()
    for e in sorted(db, key=lambda x: x["date"]):
        print(f"[{e['id']}] {e['date']} · {e['statut']:<9} · {e['titre']} ({', '.join(e['plateformes'])})")
    if not db:
        print("calendrier vide — social add …")
    return 0


def cmd_add(args):
    db = load()
    nid = max([e["id"] for e in db], default=0) + 1
    plateformes = [p.strip() for p in args.plateformes.split(",") if p.strip() in PLATFORMES]
    db.append({"id": nid, "titre": args.titre, "plateformes": plateformes,
               "date": args.date, "statut": "brouillon"})
    save(db)
    print(f"✅ post {nid} planifié : « {args.titre} » le {args.date} sur {', '.join(plateformes)}")
    return 0


def cmd_draft(args):
    print(draft(args.offer, args.plateforme))
    print("\n→ porte humaine OBLIGATOIRE avant publication : social check")
    return 0


def cmd_check(args):
    print("""📋 CHECKLIST PUBLICATION (porte humaine — rien ne part sans validation)

1. [ ] Le post sert UNE offre (O1/O2/O3) ou une preuve réelle du monorepo
2. [ ] Aucune donnée personnelle, aucun chiffre inventé, sources citées
3. [ ] Ton : concret, sans jargon « IA magique » ; une seule demande claire
4. [ ] Relu par un humain (Nathan) — l'agent propose, l'humain publie
5. [ ] Si plusieurs versions : arena battle entre elles, la gagnante part

Publication : Postiz (MCP) quand hébergé ; sinon copier-coller manuel.""")
    return 0


def cmd_listen(args):
    t = args.theme
    print(f"""👂 ÉCOUTE SOCIALE — thème « {t} » (méthode hors-ligne, à exécuter via navigateur)

Requêtes à lancer (2 sources minimum par conclusion, cf. update lessons) :
  • Google Alerts : « {t} » (gratuit, alertes mail)
  • Reddit  : site:reddit.com « {t} » + r/france + r/artificial
  • X       : recherche « {t} » → tri « Derniers » + comptes qui reviennent
  • LinkedIn: « {t} » → Publications, noter les 5 posts les plus réagis
  • YouTube : « {t} » → tri par date, vidéos < 6 mois

Livrable : 1 paragraphe synthèse + 3 comptes à suivre + 1 opportunité de post.
Outils (quand réseau) : browser-use / Playwright MCP pour automatiser ces requêtes.""")
    return 0


def main(argv):
    p = argparse.ArgumentParser(prog="social", description="Équipe marketing/réseaux")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("calendar").set_defaults(fn=cmd_calendar)
    a = sub.add_parser("add")
    a.add_argument("--titre", required=True)
    a.add_argument("--plateformes", required=True, help="x,linkedin,instagram…")
    a.add_argument("--date", required=True)
    a.set_defaults(fn=cmd_add)
    d = sub.add_parser("draft")
    d.add_argument("--offer", required=True, choices=sorted(OFFERS))
    d.add_argument("--plateforme", required=True, choices=sorted(PLATFORMES))
    d.set_defaults(fn=cmd_draft)
    sub.add_parser("check").set_defaults(fn=cmd_check)
    l = sub.add_parser("listen")
    l.add_argument("--theme", required=True)
    l.set_defaults(fn=cmd_listen)
    args = p.parse_args(argv)
    return args.fn(args)


def selftest():
    d = draft("O2", "x")
    assert "X" in d.split("\n")[0]
    assert len(d.split("\n", 1)[1]) <= PLATFORMES["x"]
    return "social OK — calendrier, drafts limités, checklist, écoute"
