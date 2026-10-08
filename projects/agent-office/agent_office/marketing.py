"""Service MARKETING — one-pagers, séquences de prospection, posts.

Les offres O1/O2/O3 sont celles définies dans USER/TELOS/MISSION.md et
docs/AUDIT-ACTIFS-COMPLET.md (assemblées sur des actifs existants).
"""
import argparse
import datetime as dt
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "out"

OFFERS = {
    "O1": {
        "titre": "Cognitorium Emploi",
        "promesse": "Un profil cognitif vivant qui relie compétences réelles et métiers (ROME/Formacode), pour un accompagnement enfin personnalisé.",
        "cibles": ["Conseillers France Travail", "Missions locales (Sète/Thau)", "Organismes de formation", "Cabinats RH"],
        "preuves": ["271 fiches ROME structurées", "Base Formacode", "Revue de littérature PRISMA 2020 (ETAT-DE-LART-PSYCHOLOGIE)", "Maquettes d'interface + parcours d'onboarding designé"],
        "prix": "démo gratuite puis licence/dossier à définir",
        "cta": "Demander une démonstration de 20 minutes",
    },
    "O2": {
        "titre": "Intelligence territoriale",
        "promesse": "Une analyse de territoire sourcée et actionnable : 249 sources, 13 fiches projets, vision chiffrée — livrée en rapport + deck.",
        "cibles": ["Équipes de design de services", "Collectivités & agglos", "Cabinets d'urbanisme"],
        "preuves": ["Rapport Frontignan 2026-2040 (249 sources)", "Deck 18 slides autonome", "Moteur reaserch-engine (contradictions & vérification)"],
        "prix": "forfait analyse 900-2 500 € selon périmètre",
        "cta": "Recevoir le deck Frontignan en exemple",
    },
    "O3": {
        "titre": "IA pour chantiers BTP",
        "promesse": "Vos dossiers de chantier (CCTP, DICT, plans, mémoires) lus, indexés et synthétisés par une IA entraînée sur vos pratiques.",
        "cibles": ["PME travaux publics", "Conducteurs de travaux", "Réseau Sobeca"],
        "preuves": ["220 fichiers de dossiers réels analysés", "Synthèse Talbot", "mail-organizer livré (zéro dépendance, zéro suppression)"],
        "prix": "forfait dossier 300-800 €",
        "cta": "Confier un dossier pilote",
    },
}

CAPABILITY = {
    "name": "marketing",
    "service": "Marketing",
    "capability": "One-pagers HTML, séquences de prospection 3 touches, posts sociaux — offres O1/O2/O3 réelles",
    "commands": ["marketing onepager --offer O1", "marketing sequence --offer O1", "marketing post --offer O1"],
}

ONEPAGER_TPL = """<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{titre}</title>
<style>body{{font-family:Georgia,serif;max-width:720px;margin:3em auto;color:#111;line-height:1.5}}
h1{{font-size:2.2em;margin-bottom:0}} .promesse{{font-size:1.2em;color:#333;border-left:4px solid #c8a24a;
padding-left:1em;margin:1.5em 0}} li{{margin:.4em 0}} .cta{{background:#111;color:#fff;padding:1em 1.5em;
display:inline-block;margin-top:2em;text-decoration:none}} footer{{margin-top:3em;font-size:.8em;color:#666}}</style>
</head><body><h1>{titre}</h1><p class="promesse">{promesse}</p>
<h2>Pour qui</h2><ul>{cibles}</ul><h2>Preuves déjà produites</h2><ul>{preuves}</ul>
<p><b>Tarification :</b> {prix}</p><a class="cta" href="#">{cta}</a>
<footer>Nathan Cabrol — produit le {date} par agent-office · actifs issus du monorepo (audit 2026-10-08)</footer>
</body></html>"""


def onepager(offer_key):
    o = OFFERS[offer_key]
    return ONEPAGER_TPL.format(
        titre=o["titre"], promesse=o["promesse"],
        cibles="".join(f"<li>{c}</li>" for c in o["cibles"]),
        preuves="".join(f"<li>{p}</li>" for p in o["preuves"]),
        prix=o["prix"], cta=o["cta"], date=dt.date.today().isoformat(),
    )


def sequence(offer_key):
    o = OFFERS[offer_key]
    return f"""SÉQUENCE DE PROSPECTION — {o['titre']} ({offer_key})

✉️ Touche 1 — J0 (accroche)
Objet : {o['titre']} — une démonstration à partir de vos dossiers
Bonjour {{prénom}},
{ o['promesse']}
Je vous propose une démonstration de 20 minutes, construite sur un cas réel.
Bien cordialement, Nathan Cabrol

✉️ Touche 2 — J+3 (preuve)
Objet : la preuve : {o['preuves'][0]}
Bonjour {{prénom}},
Pour concrétiser : { ' ; '.join(o['preuves'][:2]) }.
Puis-je vous les montrer cette semaine ?

✉️ Touche 3 — J+7 (dernier relance, porte de sortie propre)
Objet : je clos le dossier {offer_key}
Bonjour {{prénom}}, sans retour de votre part je clos ce dossier.
Si le sujet revient : {o['cta'].lower()}.
"""


def post(offer_key):
    o = OFFERS[offer_key]
    return f"""POSTS — {o['titre']} ({offer_key})

[LinkedIn]
{ o['promesse']}
Ce que j'ai déjà produit : {o['preuves'][0]}, {o['preuves'][1]}.
{o['cta']}. #IA #{offer_key}

[X / court]
{ o['titre']} : {o['promesse'].split(',')[0].lower()}. Démo sur cas réel → MP.

[Sans jargon, pour réseau local]
Je cherche 2-3 personnes pour tester un outil {o['titre'].lower()} — gratuit, 20 min, cas réel. Intéressé·e ?
"""


def main(argv):
    p = argparse.ArgumentParser(prog="marketing", description="Marketing des offres O1/O2/O3")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, fn, out_suffix in [
        ("onepager", onepager, ".html"), ("sequence", sequence, ".md"), ("post", post, ".md"),
    ]:
        s = sub.add_parser(name)
        s.add_argument("--offer", required=True, choices=sorted(OFFERS))
        s.add_argument("--out")
        s.set_defaults(fn=fn, suffix=out_suffix)
    args = p.parse_args(argv)
    content = args.fn(args.offer)
    OUT.mkdir(exist_ok=True)
    path = Path(args.out) if args.out else OUT / f"{args.cmd}-{args.offer}{args.suffix}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"✅ {args.cmd} {args.offer} → {path}")
    if args.cmd != "onepager":
        print("\n" + content)
    return 0


def selftest():
    assert "Cognitorium" in onepager("O1") and "J+7" in sequence("O2")
    return "marketing OK — one-pagers et séquences O1/O2/O3 générables"
