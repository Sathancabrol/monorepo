"""Service ARENA — confrontation de modèles/réponses : duels en aveugle + ELO.

Reproduit le principe LMArena en local : duel A/B anonyme, vote, mise à jour ELO.
Le jugement peut être humain (page de vote) ou structuré par la grille ChatEval
(jury multi-rôles). Le hook LLM-judge (litellm) est prêt pour le jour où une
clé API existe — jamais obligatoire.
"""
import argparse
import datetime as dt
import html
import json
import random
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
OUT = BASE / "out"
BATTLES = DATA / "arena_battles.json"
ELO = DATA / "arena_elo.json"
K = 32
INITIAL = 1200

CAPABILITY = {
    "name": "arena",
    "service": "Arbitrage",
    "capability": "Confrontation de modèles : duels en aveugle, votes, classement ELO local, grille de jugement ChatEval",
    "commands": [
        "arena battle --prompt P --a-file f --b-file g [--model-a X --model-b Y --categorie C]",
        "arena page --battle N", "arena vote --battle N --winner a|b|tie",
        "arena elo", "arena judge --battle N",
    ],
}

GRILLE_CHATEVAL = """🧑‍⚖️ GRILLE DE JUGEMENT (protocole ChatEval — 3 rôles, jamais un seul juge)

Rôle 1 — LE CRITIQUE (exactitude) :
  • fautes factuelles ? contradictions internes ? sources absentes ?
Rôle 2 — LE PRAGMATIQUE (utilité) :
  • la réponse sert-elle réellement la tâche (offre O1/O2/O3, bureautique) ?
  • directement utilisable ou à réécrire ?
Rôle 3 — LE STYLISTE (forme) :
  • clarté, ton, longueur adaptée ? (attention : ne PAS laisser le style
    dominer l'exactitude — biais connu du juge unique)

Décision : a / b / égalité, avec 1 phrase de justification.
"""


def load(path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def save(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def elo_expected(ra, rb):
    return 1.0 / (1.0 + 10 ** ((rb - ra) / 400.0))


def elo_update(ratings, a, b, result):
    """result: 1.0 = a gagne, 0.0 = b gagne, 0.5 = égalité."""
    ra, rb = ratings.get(a, INITIAL), ratings.get(b, INITIAL)
    ea, eb = elo_expected(ra, rb), elo_expected(rb, ra)
    ratings[a] = round(ra + K * (result - ea))
    ratings[b] = round(rb + K * ((1.0 - result) - eb))
    return ratings


def read_text(value, file_value):
    if file_value:
        return Path(file_value).read_text(encoding="utf-8")
    return value or ""


def cmd_battle(args):
    a, b = read_text(args.a, args.a_file), read_text(args.b, args.b_file)
    if not a or not b:
        print("❌ il faut deux réponses (--a/--a-file et --b/--b-file)")
        return 1
    battles = load(BATTLES, [])
    side = random.random() < 0.5
    entry = {
        "id": len(battles) + 1,
        "date": dt.date.today().isoformat(),
        "prompt": args.prompt,
        "categorie": args.categorie or "general",
        "gauche": {"modele": args.model_a or "modele-a", "texte": a},
        "droite": {"modele": args.model_b or "modele-b", "texte": b},
        "melange": side,  # True = a affiché à droite (aveugle)
        "vote": None,
        "note": None,
    }
    battles.append(entry)
    save(BATTLES, battles)
    print(f"✅ duel {entry['id']} enregistré ({len(a)} vs {len(b)} caractères, ordre aveugle)")
    print(f"   → page de vote : python3 -m agent_office arena page --battle {entry['id']}")
    return 0


def page_html(entry):
    gauche, droite = entry["gauche"], entry["droite"]
    if entry.get("melange"):
        gauche, droite = droite, gauche
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Duel #{entry['id']}</title>
<style>body{{font-family:Georgia,serif;max-width:1100px;margin:2em auto;color:#111}}
.cols{{display:flex;gap:2em}}.col{{flex:1;border:1px solid #ccc;border-radius:8px;padding:1em}}
h2{{margin-top:0}}pre{{white-space:pre-wrap;font-family:inherit}}
details{{margin-top:2em}}.q{{background:#f5f0e6;padding:1em;border-radius:8px}}</style></head>
<body><h1>⚔️ Duel #{entry['id']} — {entry['categorie']}</h1>
<div class="q"><b>Prompt :</b><br>{html.escape(entry['prompt'])}</div>
<div class="cols"><div class="col"><h2>Réponse A</h2><pre>{html.escape(gauche['texte'])}</pre></div>
<div class="col"><h2>Réponse B</h2><pre>{html.escape(droite['texte'])}</pre></div></div>
<p>Votez en aveugle, puis : <code>arena vote --battle {entry['id']} --winner a|b|tie</code></p>
<details><summary>révéler les identités</summary>
<p>A = {html.escape(gauche['modele'])} · B = {html.escape(droite['modele'])}</p></details>
</body></html>"""


def get_battle(n):
    battles = load(BATTLES, [])
    for e in battles:
        if e["id"] == n:
            return e
    return None


def cmd_page(args):
    e = get_battle(args.battle)
    if not e:
        print(f"❌ duel {args.battle} introuvable")
        return 1
    OUT.mkdir(exist_ok=True)
    path = OUT / f"arena-duel-{e['id']}.html"
    path.write_text(page_html(e), encoding="utf-8")
    print(f"✅ {path} — votez en aveugle puis `arena vote --battle {e['id']} --winner …`")
    return 0


def cmd_vote(args):
    battles = load(BATTLES, [])
    e = get_battle(args.battle)
    if not e:
        print(f"❌ duel {args.battle} introuvable")
        return 1
    if e["vote"]:
        print(f"⚠️  duel {args.battle} déjà voté ({e['vote']}) — jamais de suppression, nouveau vote ignoré")
        return 1
    # après mélange éventuel : gauche = modèle affiché sous « A », droite = « B »
    gauche, droite = e["gauche"]["modele"], e["droite"]["modele"]
    if e.get("melange"):
        gauche, droite = droite, gauche
    if args.winner == "tie":
        result, gagnant = 0.5, "egalite"
    elif args.winner == "a":
        result, gagnant = 1.0, gauche
    else:
        result, gagnant = 0.0, droite
    ratings = elo_update(load(ELO, {}), gauche, droite, result)
    e["vote"], e["note"] = gagnant, args.note
    save(ELO, ratings)
    save(BATTLES, battles)
    print(f"✅ duel {args.battle} : vainqueur « {gagnant} » — ELO mis à jour")
    return 0


def cmd_elo(args):
    ratings = load(ELO, {})
    if not ratings:
        print("classement vide — lancez un duel : arena battle …")
        return 0
    print("🏆 CLASSEMENT ELO LOCAL (K=32, base 1200)")
    for i, (m, r) in enumerate(sorted(ratings.items(), key=lambda kv: -kv[1]), 1):
        print(f"  {i}. {m:<28} {r}")
    return 0


def cmd_judge(args):
    e = get_battle(args.battle)
    if not e:
        print(f"❌ duel {args.battle} introuvable")
        return 1
    try:
        import litellm  # noqa: F401
        print("ℹ️  litellm détecté — brancher ici le jury LLM multi-rôles (3 appels, agrégation majorité).")
    except Exception:
        pass
    print(GRILLE_CHATEVAL)
    print(f"Duel {args.battle} — prompt : {e['prompt'][:120]}…")
    return 0


def main(argv):
    p = argparse.ArgumentParser(prog="arena", description="Confrontation de modèles (aveugle + ELO)")
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("battle")
    b.add_argument("--prompt", required=True)
    b.add_argument("--a")
    b.add_argument("--a-file")
    b.add_argument("--b")
    b.add_argument("--b-file")
    b.add_argument("--model-a")
    b.add_argument("--model-b")
    b.add_argument("--categorie")
    b.set_defaults(fn=cmd_battle)
    pg = sub.add_parser("page")
    pg.add_argument("--battle", type=int, required=True)
    pg.set_defaults(fn=cmd_page)
    v = sub.add_parser("vote")
    v.add_argument("--battle", type=int, required=True)
    v.add_argument("--winner", required=True, choices=["a", "b", "tie"])
    v.add_argument("--note")
    v.set_defaults(fn=cmd_vote)
    sub.add_parser("elo").set_defaults(fn=cmd_elo)
    j = sub.add_parser("judge")
    j.add_argument("--battle", type=int, required=True)
    j.set_defaults(fn=cmd_judge)
    args = p.parse_args(argv)
    return args.fn(args)


def selftest():
    r = elo_update({}, "m1", "m2", 1.0)
    assert r["m1"] > INITIAL and r["m2"] < INITIAL
    return "arena OK — duels aveugles + ELO + grille ChatEval"
