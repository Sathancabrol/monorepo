"""Service INVOICES — devis & factures conformes France.

- Mention franchise en base de TVA (micro-entreprise) : « TVA non applicable, art. 293 B du CGI ».
- Mentions légales : identité émetteur, numéro, dates, délai de paiement, pénalités.
- Sorties : HTML + texte. Le SIRET est à compléter (TODO signalé, jamais inventé).
"""
import argparse
import datetime as dt
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "out"

EMETTEUR = {
    "nom": "Nathan Cabrol",
    "adresse": "Sète, France",  # TODO: adresse complète
    "siret": "SIRET À COMPLÉTER",  # TODO: jamais inventé
    "forme": "Micro-entreprise",
}

CAPABILITY = {
    "name": "invoices",
    "service": "Finance",
    "capability": "Génère devis/factures conformes (franchise TVA art. 293 B CGI) en HTML+texte",
    "commands": ["invoices devis|facture --client NOM --lines 'desc|qte|pu;...' [--num N]"],
}

TVA_MENTION = "TVA non applicable, art. 293 B du CGI (franchise en base)"


def parse_lines(spec):
    lines = []
    for chunk in filter(None, spec.split(";")):
        desc, qte, pu = chunk.split("|")
        qte, pu = float(qte), float(pu)
        lines.append({"desc": desc.strip(), "qte": qte, "pu": pu, "total": qte * pu})
    return lines


def build_doc(kind, client, lines, num, date=None):
    date = date or dt.date.today().isoformat()
    total = sum(l["total"] for l in lines)
    titre = "DEVIS" if kind == "devis" else "FACTURE"
    rows_html = "".join(
        f"<tr><td>{l['desc']}</td><td style='text-align:right'>{l['qte']:g}</td>"
        f"<td style='text-align:right'>{l['pu']:,.2f} €</td>"
        f"<td style='text-align:right'>{l['total']:,.2f} €</td></tr>"
        for l in lines
    ).replace(",", " ")
    html = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<title>{titre} {num}</title>
<style>body{{font-family:Georgia,serif;max-width:760px;margin:2em auto;color:#111}}
h1{{border-bottom:3px solid #111;padding-bottom:.2em}}table{{width:100%;border-collapse:collapse;margin:1.5em 0}}
td,th{{border-bottom:1px solid #ccc;padding:.5em}}th{{text-align:left}}
.total{{font-weight:bold;font-size:1.2em}} .mentions{{font-size:.8em;color:#555;margin-top:2em}}</style></head>
<body><h1>{titre} n° {num}</h1>
<p><b>Émetteur :</b> {EMETTEUR['nom']} — {EMETTEUR['forme']} — {EMETTEUR['adresse']} — {EMETTEUR['siret']}</p>
<p><b>Client :</b> {client}</p><p><b>Date :</b> {date}</p>
<table><tr><th>Description</th><th>Qté</th><th>PU HT</th><th>Total HT</th></tr>{rows_html}
<tr><td colspan="3" class="total">TOTAL</td><td class="total">{total:,.2f} €</td></tr></table>
<p><i>{TVA_MENTION}</i></p>
<div class="mentions">Paiement à réception. Escompte : néant. Retard : pénalités légales (3× taux légal)
+ indemnité forfaitaire de recouvrement 40 €. {EMETTEUR['nom']} — {EMETTEUR['siret']}.</div>
</body></html>""".replace(",", " ").replace("3× ", "3× ")
    txt = (
        f"{titre} n° {num} — {date}\nÉmetteur : {EMETTEUR['nom']} ({EMETTEUR['siret']})\nClient : {client}\n\n"
        + "\n".join(f"  {l['desc']}: {l['qte']:g} × {l['pu']:.2f} € = {l['total']:.2f} €" for l in lines)
        + f"\n\nTOTAL : {total:.2f} €\n{TVA_MENTION}\n"
    )
    return html, txt, total


def main(argv):
    p = argparse.ArgumentParser(prog="invoices", description="Devis & factures")
    p.add_argument("kind", choices=["devis", "facture"])
    p.add_argument("--client", required=True)
    p.add_argument("--lines", required=True, help="'desc|qte|pu;desc|qte|pu'")
    p.add_argument("--num", default="001")
    p.add_argument("--out", help="chemin de base (sans extension)")
    args = p.parse_args(argv)
    html, txt, total = build_doc(args.kind, args.client, parse_lines(args.lines), args.num)
    OUT.mkdir(exist_ok=True)
    base = Path(args.out) if args.out else OUT / f"{args.kind}-{args.num}"
    base.parent.mkdir(parents=True, exist_ok=True)
    (base.with_suffix(".html")).write_text(html, encoding="utf-8")
    (base.with_suffix(".txt")).write_text(txt, encoding="utf-8")
    print(f"✅ {args.kind} {args.num} pour « {args.client} » — total {total:.2f} €")
    print(f"   {base}.html / {base}.txt")
    return 0


def selftest():
    html, txt, total = build_doc("devis", "Client Test", parse_lines("Démo|1|100"), "T1")
    assert "293 B" in html and "Client Test" in txt and total == 100.0
    return "invoices OK — mentions légales et franchise TVA présentes"
