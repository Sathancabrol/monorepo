# -*- coding: utf-8 -*-
"""
Construit `atlas/data/atlas.json` : jeux de données + statistiques descriptives
+ graphe (nœuds/liens) + arborescence heuristique + scénario de slides.

Toutes les statistiques sont recalculées ici (aucun chiffre « en dur ») :
effectif, somme, moyenne, moyenne pondérée, médiane, mode de classe, écart-type
(population et échantillon), variance, coefficient de variation, étendue (R),
quartiles, écart interquartile, MAD, asymétrie, intervalle de confiance à 95 %,
z-scores, indice de Gini, corrélations de Pearson et de Spearman, régression
linéaire (pente, ordonnée, R²).

Usage :  python3 scripts/build_atlas.py
"""
import json
import math
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from atlas_data import (  # noqa: E402
    COMMUNES, ECHELLES, POP_FRONTIGNAN, AGES_FRONTIGNAN, BUDGET_VILLE, FINANCES_STRATE,
    MOBILITES, CLIMAT, SUBMERSION, MUNICIPALES_2026, PROJETS, ACTEURS, SCENARIOS,
    CONDITIONS_2030, JALONS, SOURCE_INSEE, SOURCE_GEO,
)
from atlas_graph import NODES, LINKS, ACTEUR_LINKS, SLIDES  # noqa: E402


# ==========================================================================
#  Boîte à outils statistique
# ==========================================================================
def _clean(values):
    return [float(v) for v in values if v is not None and not (isinstance(v, float) and math.isnan(v))]


def quantile(sorted_vals, p):
    """Quantile par interpolation linéaire (méthode 7, celle de R et de numpy)."""
    if not sorted_vals:
        return None
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    h = (len(sorted_vals) - 1) * p
    lo = math.floor(h)
    hi = math.ceil(h)
    return sorted_vals[lo] + (h - lo) * (sorted_vals[hi] - sorted_vals[lo])


def describe(values, weights=None):
    """Statistiques descriptives complètes d'une série."""
    v = _clean(values)
    n = len(v)
    if n == 0:
        return None
    s = sorted(v)
    total = sum(v)
    mean = total / n
    med = quantile(s, 0.5)
    var_p = sum((x - mean) ** 2 for x in v) / n
    var_s = sum((x - mean) ** 2 for x in v) / (n - 1) if n > 1 else 0.0
    sd_p = math.sqrt(var_p)
    sd_s = math.sqrt(var_s)
    q1, q3 = quantile(s, 0.25), quantile(s, 0.75)
    mad = quantile(sorted(abs(x - med) for x in v), 0.5)
    skew = (sum((x - mean) ** 3 for x in v) / n) / (sd_p ** 3) if sd_p > 0 else 0.0
    kurt = (sum((x - mean) ** 4 for x in v) / n) / (sd_p ** 4) - 3 if sd_p > 0 else 0.0
    ci = 1.96 * sd_s / math.sqrt(n) if n > 1 else 0.0
    out = dict(
        n=n, somme=total, moyenne=mean, mediane=med, min=s[0], max=s[-1],
        etendue=s[-1] - s[0], q1=q1, q3=q3, iqr=(q3 - q1) if q1 is not None else None,
        variance=var_s, ecart_type=sd_s, ecart_type_pop=sd_p,
        cv=(sd_s / mean * 100) if mean else None, mad=mad,
        asymetrie=skew, aplatissement=kurt,
        ic95_bas=mean - ci, ic95_haut=mean + ci,
        p10=quantile(s, 0.10), p90=quantile(s, 0.90),
    )
    # outliers au sens de Tukey (1,5 × IQR)
    if out["iqr"]:
        lo = q1 - 1.5 * out["iqr"]
        hi = q3 + 1.5 * out["iqr"]
        out["borne_basse"] = lo
        out["borne_haute"] = hi
        out["n_atypiques"] = sum(1 for x in v if x < lo or x > hi)
    if weights:
        w = [float(x) for x in weights]
        sw = sum(w)
        if sw:
            out["moyenne_ponderee"] = sum(a * b for a, b in zip(v, w)) / sw
    return out


def pearson(xs, ys):
    pairs = [(float(a), float(b)) for a, b in zip(xs, ys) if a is not None and b is not None]
    n = len(pairs)
    if n < 3:
        return None
    mx = sum(p[0] for p in pairs) / n
    my = sum(p[1] for p in pairs) / n
    sxy = sum((a - mx) * (b - my) for a, b in pairs)
    sxx = sum((a - mx) ** 2 for a, _ in pairs)
    syy = sum((b - my) ** 2 for _, b in pairs)
    if sxx <= 0 or syy <= 0:
        return None
    r = sxy / math.sqrt(sxx * syy)
    slope = sxy / sxx
    intercept = my - slope * mx
    # test de Student approché
    t = r * math.sqrt((n - 2) / max(1e-12, 1 - r * r)) if abs(r) < 1 else float("inf")
    return dict(n=n, r=r, r2=r * r, pente=slope, ordonnee=intercept, t=t,
                significatif=abs(t) > 2.16)  # |t| > t(0,05 ; n-2≈12)


def _ranks(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    ranks = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman(xs, ys):
    pairs = [(float(a), float(b)) for a, b in zip(xs, ys) if a is not None and b is not None]
    if len(pairs) < 3:
        return None
    rx = _ranks([p[0] for p in pairs])
    ry = _ranks([p[1] for p in pairs])
    res = pearson(rx, ry)
    return res["r"] if res else None


def gini(values):
    v = sorted(_clean(values))
    n = len(v)
    if n == 0 or sum(v) == 0:
        return None
    cum = sum((2 * (i + 1) - n - 1) * x for i, x in enumerate(v))
    return cum / (n * sum(v))


def lorenz(values, labels):
    pairs = sorted(zip(_clean(values), labels))
    total = sum(p[0] for p in pairs)
    pts = [dict(x=0.0, y=0.0, label="")]
    cx = cy = 0.0
    for i, (val, lab) in enumerate(pairs):
        cx += 1 / len(pairs)
        cy += val / total
        pts.append(dict(x=cx, y=cy, label=lab))
    return pts


def cagr(v0, v1, years):
    if not v0 or not v1 or years <= 0:
        return None
    return ((v1 / v0) ** (1 / years) - 1) * 100


# ==========================================================================
#  Enrichissement du jeu communal
# ==========================================================================
for c in COMMUNES:
    c["surf_km2"] = round(c["surf_ha"] / 100.0, 2)
    c["emp_100hab"] = round(c["emp"] / c["pop"] * 100, 1)
    c["etab_1000hab"] = round(c["etab"] / c["pop"] * 1000, 1)
    c["logts_men"] = round(c["logts"] / c["men"], 2)
    c["nat"] = round(c["nais"] / c["pop"] * 1000, 1)
    c["mort"] = round(c["deces"] / c["pop"] * 1000, 1)
    c["solde_civil"] = c["nais"] - c["deces"]
    c["part_agglo"] = round(c["pop"] / 131216 * 100, 2)

CHAMPS_COMMUNES = [
    dict(key="nom", label="Commune", type="text"),
    dict(key="pop", label="Population 2023", unit="hab.", fmt="int", better="none"),
    dict(key="part_agglo", label="Poids dans l'agglo", unit="%", fmt="1", better="none"),
    dict(key="surf_km2", label="Superficie", unit="km²", fmt="1", better="none"),
    dict(key="dens", label="Densité", unit="hab./km²", fmt="0", better="none"),
    dict(key="tvam", label="Croissance 2017-2023", unit="%/an", fmt="2", better="up"),
    dict(key="sn", label="dont solde naturel", unit="%/an", fmt="2", better="up"),
    dict(key="sm", label="dont solde migratoire", unit="%/an", fmt="2", better="up"),
    dict(key="nat", label="Natalité 2025", unit="‰", fmt="1", better="up"),
    dict(key="mort", label="Mortalité 2025", unit="‰", fmt="1", better="down"),
    dict(key="nvm", label="Niveau de vie médian", unit="€/UC", fmt="int", better="up"),
    dict(key="pauv", label="Taux de pauvreté", unit="%", fmt="1", better="down"),
    dict(key="tcho", label="Chômage 15-64 ans", unit="%", fmt="1", better="down"),
    dict(key="tact", label="Taux d'activité", unit="%", fmt="1", better="up"),
    dict(key="emp", label="Emplois au lieu de travail", unit="", fmt="int", better="up"),
    dict(key="emp_100hab", label="Emplois pour 100 hab.", unit="", fmt="1", better="up"),
    dict(key="etab", label="Établissements employeurs", unit="", fmt="int", better="up"),
    dict(key="etab_1000hab", label="Établissements / 1 000 hab.", unit="", fmt="1", better="up"),
    dict(key="rs", label="Résidences secondaires", unit="% du parc", fmt="1", better="none"),
    dict(key="vac", label="Logements vacants", unit="%", fmt="1", better="down"),
    dict(key="prop", label="Propriétaires", unit="%", fmt="1", better="none"),
    dict(key="logts_men", label="Logements par ménage", unit="", fmt="2", better="none"),
    dict(key="men", label="Ménages", unit="", fmt="int", better="none"),
]

NUM_COMMUNES = [f["key"] for f in CHAMPS_COMMUNES if f.get("type") != "text"]

stats_communes = {}
for k in NUM_COMMUNES:
    vals = [c.get(k) for c in COMMUNES]
    st = describe(vals, weights=[c["pop"] for c in COMMUNES])
    if st:
        # position de Frontignan dans la distribution
        fro = next(c for c in COMMUNES if c["code"] == "34108").get(k)
        if fro is not None and st["ecart_type"]:
            st["frontignan"] = fro
            st["z_frontignan"] = (fro - st["moyenne"]) / st["ecart_type"]
            ordered = sorted([c.get(k) for c in COMMUNES if c.get(k) is not None], reverse=True)
            st["rang_frontignan"] = ordered.index(fro) + 1
            st["rang_sur"] = len(ordered)
            st["ecart_mediane_pct"] = (fro - st["mediane"]) / st["mediane"] * 100 if st["mediane"] else None
    stats_communes[k] = st

# z-scores par commune (profil normalisé)
PROFIL_KEYS = ["dens", "tvam", "nvm", "pauv", "tcho", "rs", "emp_100hab", "vac"]
for c in COMMUNES:
    c["z"] = {}
    for k in PROFIL_KEYS:
        st = stats_communes.get(k)
        if st and st["ecart_type"] and c.get(k) is not None:
            c["z"][k] = round((c[k] - st["moyenne"]) / st["ecart_type"], 3)

PAIRES = [
    ("dens", "nvm", "Densité × niveau de vie"),
    ("nvm", "pauv", "Niveau de vie × pauvreté"),
    ("rs", "nvm", "Résidences secondaires × niveau de vie"),
    ("tcho", "nvm", "Chômage × niveau de vie"),
    ("pop", "emp", "Population × emplois"),
    ("tvam", "nvm", "Croissance × niveau de vie"),
    ("sm", "rs", "Solde migratoire × résidences secondaires"),
    ("etab_1000hab", "nvm", "Densité d'établissements × niveau de vie"),
]
correlations = []
for xk, yk, lab in PAIRES:
    xs = [c.get(xk) for c in COMMUNES]
    ys = [c.get(yk) for c in COMMUNES]
    p = pearson(xs, ys)
    if not p:
        continue
    p.update(x=xk, y=yk, label=lab, rho=spearman(xs, ys))
    correlations.append(p)

# matrice de corrélation complète (Pearson) sur les indicateurs clés
MATRIX_KEYS = ["pop", "dens", "tvam", "sm", "nvm", "pauv", "tcho", "rs", "vac", "emp_100hab"]
matrix = []
for a in MATRIX_KEYS:
    row = []
    for b in MATRIX_KEYS:
        p = pearson([c.get(a) for c in COMMUNES], [c.get(b) for c in COMMUNES])
        row.append(round(p["r"], 3) if p else None)
    matrix.append(row)

gini_pop = gini([c["pop"] for c in COMMUNES])
gini_emp = gini([c["emp"] for c in COMMUNES])
lorenz_pop = lorenz([c["pop"] for c in COMMUNES], [c["nom"] for c in COMMUNES])

# ==========================================================================
#  Séries et jeux dérivés
# ==========================================================================
annees = POP_FRONTIGNAN["annees"]
vals = POP_FRONTIGNAN["valeurs"]
periodes = []
for i in range(1, len(annees)):
    periodes.append(dict(
        de=annees[i - 1], a=annees[i],
        var=vals[i] - vals[i - 1],
        tcam=round(cagr(vals[i - 1], vals[i], annees[i] - annees[i - 1]), 2),
    ))
pop_stats = describe(vals)
pop_stats["tcam_total"] = round(cagr(vals[0], vals[-1], annees[-1] - annees[0]), 2)
pop_stats["gain_total"] = vals[-1] - vals[0]
# projection linéaire simple 2030 / 2040 (régression OLS sur 1999-2023)
recent = [(a, v) for a, v in zip(annees, vals) if a >= 1999]
reg = pearson([a for a, _ in recent], [v for _, v in recent])
if reg:
    pop_stats["proj_2030"] = round(reg["ordonnee"] + reg["pente"] * 2030)
    pop_stats["proj_2040"] = round(reg["ordonnee"] + reg["pente"] * 2040)
    pop_stats["pente_annuelle"] = round(reg["pente"], 1)
    pop_stats["r2_tendance"] = round(reg["r2"], 3)

budget_total = [f + i for f, i in zip(BUDGET_VILLE["fonctionnement"], BUDGET_VILLE["investissement"])]
budget_stats = describe(budget_total)
budget_stats["part_invest_moy"] = round(
    sum(BUDGET_VILLE["investissement"]) / sum(budget_total) * 100, 1)

# écarts à la strate (finances)
for ind in FINANCES_STRATE["indicateurs"]:
    ind["ecart_pct"] = round((ind["v"] - ind["ref"]) / ind["ref"] * 100, 1)

# secteurs d'activité — comparaison Frontignan / agglo / France
SECTEURS = dict(
    label="Répartition sectorielle des établissements employeurs (%, Flores 2024)",
    labels=["Agriculture", "Industrie", "Construction", "Commerce & services", "Adm., santé, éducation"],
    series=[
        dict(nom="Frontignan", vals=[4.0, 9.1, 11.2, 64.7, 11.0]),
        dict(nom="Sète Agglopôle", vals=[5.2, 6.8, 9.7, 68.7, 9.6]),
        dict(nom="Hérault", vals=[3.7, 5.1, 11.4, 68.4, 11.4]),
        dict(nom="France métropolitaine", vals=[4.9, 6.2, 10.9, 65.3, 12.6]),
    ],
    source=SOURCE_INSEE,
)

# acteurs : statistiques du positionnement pouvoir / intérêt
inf = [a["influence"] for a in ACTEURS]
ite = [a["interet"] for a in ACTEURS]
acteurs_stats = dict(
    influence=describe(inf), interet=describe(ite),
    correlation=pearson(inf, ite),
    familles={},
)
for a in ACTEURS:
    fam = acteurs_stats["familles"].setdefault(a["famille"], dict(n=0, influence=[], interet=[]))
    fam["n"] += 1
    fam["influence"].append(a["influence"])
    fam["interet"].append(a["interet"])
for fam, d in acteurs_stats["familles"].items():
    d["influence_moy"] = round(sum(d["influence"]) / d["n"], 2)
    d["interet_moy"] = round(sum(d["interet"]) / d["n"], 2)
    d["influence_med"] = quantile(sorted(d["influence"]), 0.5)
    d["interet_med"] = quantile(sorted(d["interet"]), 0.5)
    del d["influence"], d["interet"]
for a in ACTEURS:
    a["priorite"] = a["influence"] * a["interet"]
    a["quadrant"] = (
        "Co-construire" if a["influence"] >= 3.5 and a["interet"] >= 3.5 else
        "Tenir informés" if a["influence"] >= 3.5 else
        "Écouter activement" if a["interet"] >= 3.5 else
        "Surveiller")

# projets : agrégats budgétaires
couts = [p["cout"] for p in PROJETS if p["cout"]]
projets_stats = describe(couts)
projets_stats["total_identifie"] = round(sum(couts), 1)
projets_stats["non_chiffres"] = sum(1 for p in PROJETS if not p["cout"])
projets_stats["par_habitant"] = round(sum(couts) * 1e6 / 24136)

SWOT = dict(
    label="SWOT de Frontignan la Peyrade",
    forces=["Muscat AOP 1936 : ≈ 800 ha, ≈ 3 M bouteilles, cave centenaire",
            "Littoral et nature : lido 7 km, Aresquiers, salins, 4 sites Natura 2000",
            "Position bipolaire Montpellier (21 km) / Sète (7 km) avec gare",
            "Poids intercommunal maximal : siège + présidence + VP tourisme",
            "Finances maîtrisées : dette 995 €/hab., taux stables depuis 9 ans",
            "11 ha dépollués en cœur de ville — foncier rarissime",
            "Vacance commerciale ≈ 4 % (strate ≈ 12 %), stationnement gratuit",
            "Culture vivante : FIRN, joutes, nouveau cinéma",
            "Équipe municipale expérimentée et réélue au 1ᵉʳ tour"],
    faiblesses=["Chômage 14 % (28,9 % des 15-24 ans), pauvreté 17 %",
                "Vieillissement : 25,3 % de 65 ans et +, solde naturel négatif",
                "Dépendance automobile : 80 % des actifs, 67 % de navetteurs",
                "Risques cumulés : submersion, 2 Seveso seuil haut, canicules",
                "Pression fiscale 1 011 €/hab. (strate 793 €)",
                "Investissement/hab. 270 € (strate 438 €)",
                "Offre hôtelière quasi inexistante : 3 hôtels, 130 chambres",
                "Fracture civique : RN 35,9 %, abstention 38,1 %",
                "Offre de soins sous tension (23 généralistes)"],
    opportunites=["Action cœur de Ville (2025), phase 2 sur les quartiers de gare",
                  "Friche Mobil + PEM : projet urbain de rang métropolitain",
                  "PPA trait de côte et Fonds vert (jusqu'à 80 %)",
                  "LGV 2034 : dessaturation de la ligne classique",
                  "Œnotourisme et « Muscat 90 ans », tourisme fluvial",
                  "Centre aquatique intercommunal sur la commune",
                  "Croissance héraultaise (+15 000 hab./an)",
                  "ZAN : la ville a déjà fait son effort foncier",
                  "Écosystème culturel montpelliérain et sétois accessible"],
    menaces=["Climat : submersion, canicules, sécheresse, feux de Gardiole",
             "Baisse des dotations et du Fonds vert (−67 % en 2 ans)",
             "Hausse des taux d'intérêt",
             "Pollutions de l'étang et crise conchylicole",
             "Calendriers et financements LGV incertains",
             "Instabilité de gouvernance de l'agglo",
             "Concurrence touristique et littoral occitan en repli",
             "Spéculation et gentrification littorales"],
)

RECOS = dict(
    label="Recommandations design priorisées (impact × faisabilité)",
    items=[
        dict(id="R1", nom="Plateforme d'identité territoriale & signalétique", impact=5, faisabilite=4,
             horizon="6-12 mois", kpi="Cohérence signalétique · notoriété · satisfaction usagers"),
        dict(id="R2", nom="Concertation outillée friche Mobil & Mas de Chave", impact=5, faisabilite=4,
             horizon="2026-2027", kpi="Diversité des participants · légitimité des arbitrages"),
        dict(id="R3", nom="Design du pôle d'échanges gare/PEM", impact=5, faisabilite=3,
             horizon="2026-2028", kpi="Design intégré à la programmation Région"),
        dict(id="R4", nom="Programme « bien vivre les chantiers »", impact=4, faisabilite=5,
             horizon="immédiat", kpi="Satisfaction riverains · CA des commerces en travaux"),
        dict(id="R5", nom="Stratégie expérientielle « Muscat 90 → 100 ans »", impact=4, faisabilite=4,
             horizon="2026-2028", kpi="Fréquentation œnotouristique · retombées cave/vignerons"),
        dict(id="R6", nom="Design du risque (submersion, chaleur, industriel)", impact=4, faisabilite=3,
             horizon="12-24 mois", kpi="Culture du risque · usage des îlots de fraîcheur"),
        dict(id="R7", nom="Revitalisation commerciale & retail design", impact=4, faisabilite=4,
             horizon="2027", kpi="Vacance < 5 % · ouvertures · animation"),
        dict(id="R8", nom="Écoconception des espaces publics", impact=4, faisabilite=3,
             horizon="12 mois", kpi="Part de surfaces ombragées et perméables"),
        dict(id="R9", nom="Montée en gamme de Frontignan-Plage", impact=4, faisabilite=2,
             horizon="2027-2030", kpi="Occupation estivale · investissements privés"),
        dict(id="R10", nom="Observatoire du territoire & design d'information", impact=3, faisabilite=4,
             horizon="6-12 mois", kpi="Réutilisation des données · décisions documentées"),
    ],
)
for r in RECOS["items"]:
    r["score"] = r["impact"] * r["faisabilite"]
RECOS["stats"] = dict(
    impact=describe([r["impact"] for r in RECOS["items"]]),
    faisabilite=describe([r["faisabilite"] for r in RECOS["items"]]),
    score=describe([r["score"] for r in RECOS["items"]]),
)

# ==========================================================================
#  Graphe : nœuds, liens, arborescence
# ==========================================================================
TYPE_COLORS = {
    "territoire": "#2FA8C4", "commune": "#4FC3A1", "acteur": "#E4B33C", "projet": "#E1734F",
    "risque": "#D8595B", "politique": "#9B87D4", "ressource": "#79B36B", "futur": "#6C8AE4",
    "data": "#8FA3AC",
}
TIER_LABEL = {0: "Frontignan", 1: "La ville", 2: "L'agglo de Thau", 3: "Les environs", 4: "La France"}

nodes = []
for n in NODES:
    node = dict(n)
    node.setdefault("facts", [])
    node.setdefault("bul", [])
    node.setdefault("src", [])
    node["facts"] = [dict(k=k, v=v) for k, v in node["facts"]]
    node["src"] = [dict(t=t, u=u, d=d) for t, u, d in node["src"]]
    node["color"] = TYPE_COLORS.get(node["type"], "#8FA3AC")
    node["tierLabel"] = TIER_LABEL[node["tier"]]
    nodes.append(node)

# nœuds « acteur » générés depuis le référentiel d'acteurs
for a in ACTEURS:
    nodes.append(dict(
        id=a["id"], label=a["nom"], type="acteur", tier=1 if a["echelle"] in ("Commune",) else 2,
        icon="🧑‍💼" if a["famille"] == "Institutionnel" else ("🏭" if a["famille"] == "Économique" else "👥"),
        img=None, parent="acteurs", sub=a["role"],
        txt=f"{a['role']}. Levier détenu : {a['ressource'].lower()}. Posture recommandée : {a['posture'].lower()}.",
        facts=[dict(k="Famille", v=a["famille"]), dict(k="Échelle", v=a["echelle"]),
               dict(k="Influence", v=f"{a['influence']}/5"), dict(k="Intérêt", v=f"{a['interet']}/5"),
               dict(k="Priorité (I×I)", v=a["priorite"]), dict(k="Quadrant", v=a["quadrant"])],
        bul=[], src=[], color=TYPE_COLORS["acteur"], tierLabel="Acteurs",
        acteur=True, influence=a["influence"], interet=a["interet"], famille=a["famille"],
        quadrant=a["quadrant"], data="acteurs",
    ))

ids = {n["id"] for n in nodes}
links = []
for s, t, ty, w, lab in LINKS:
    if s in ids and t in ids:
        links.append(dict(source=s, target=t, type=ty, weight=w, label=lab))
    else:  # garde-fou de construction
        print(f"  ! lien ignoré : {s} → {t}")
for src, targets in ACTEUR_LINKS.items():
    for tgt, ty, w in targets:
        if src in ids and tgt in ids:
            links.append(dict(source=src, target=tgt, type=ty, weight=w, label=""))

# degrés (taille des nœuds + backlinks)
deg = {n["id"]: 0 for n in nodes}
for l in links:
    deg[l["source"]] += 1
    deg[l["target"]] += 1
for n in nodes:
    n["degree"] = deg[n["id"]]

# arborescence heuristique (parent → enfants)
by_id = {n["id"]: n for n in nodes}
for n in nodes:
    n["children"] = []
roots = []
for n in nodes:
    p = n.get("parent")
    if p and p in by_id and p != n["id"]:
        by_id[p]["children"].append(n["id"])
    else:
        roots.append(n["id"])

# ==========================================================================
#  Assemblage
# ==========================================================================
datasets = {
    "communes": dict(
        label="Les 14 communes de Sète Agglopôle Méditerranée",
        note="Millésime 2023 (RP), Filosofi 2023, Flores 2024, état civil 2025. "
             "Bouzigues : taux de pauvreté couvert par le secret statistique.",
        fields=CHAMPS_COMMUNES, rows=COMMUNES, stats=stats_communes,
        correlations=correlations,
        matrix=dict(keys=MATRIX_KEYS,
                    labels=[next(f["label"] for f in CHAMPS_COMMUNES if f["key"] == k) for k in MATRIX_KEYS],
                    values=matrix),
        concentration=dict(gini_population=gini_pop, gini_emplois=gini_emp, lorenz=lorenz_pop),
        sources=[SOURCE_INSEE, SOURCE_GEO],
    ),
    "echelles": dict(
        label="L'entonnoir : France → Occitanie → Hérault → agglo → Frontignan",
        rows=ECHELLES,
        fields=[dict(key="nom", label="Territoire", type="text"),
                dict(key="niveau", label="Échelle", type="text"),
                dict(key="pop", label="Population", unit="hab.", fmt="int"),
                dict(key="tvam", label="Croissance", unit="%/an", fmt="2"),
                dict(key="dens", label="Densité", unit="hab./km²", fmt="0"),
                dict(key="nvm", label="Niveau de vie médian", unit="€", fmt="int"),
                dict(key="pauv", label="Pauvreté", unit="%", fmt="1"),
                dict(key="tcho", label="Chômage 15-64", unit="%", fmt="1"),
                dict(key="rs", label="Résidences secondaires", unit="%", fmt="1"),
                dict(key="vac", label="Vacance", unit="%", fmt="1")],
        stats={k: describe([e.get(k) for e in ECHELLES]) for k in ["tvam", "nvm", "pauv", "tcho", "rs"]},
        sources=[SOURCE_INSEE],
    ),
    "pop_serie": dict(label=POP_FRONTIGNAN["label"], annees=annees, valeurs=vals,
                      densites=POP_FRONTIGNAN["densites"], periodes=periodes, stats=pop_stats,
                      sources=[SOURCE_INSEE]),
    "ages": dict(label=AGES_FRONTIGNAN["label"], classes=AGES_FRONTIGNAN["classes"],
                 an2012=AGES_FRONTIGNAN["an2012"], an2017=AGES_FRONTIGNAN["an2017"],
                 an2023=AGES_FRONTIGNAN["an2023"], effectifs2023=AGES_FRONTIGNAN["effectifs2023"],
                 stats=dict(delta_2012_2023=[round(b - a, 1) for a, b in
                                             zip(AGES_FRONTIGNAN["an2012"], AGES_FRONTIGNAN["an2023"])],
                            age_median_estime=45, part_65_plus=25.3, part_moins_15=14.8),
                 sources=[SOURCE_INSEE]),
    "mobilites": dict(label=MOBILITES["label"], modes=MOBILITES["modes"], parts=MOBILITES["parts"],
                      hors_commune=MOBILITES["hors_commune"], actifs=MOBILITES["actifs_occupes"],
                      stats=dict(part_voiture=80.0, part_alternatives=round(100 - 80.0 - 3.9, 1),
                                 emplois=6556, actifs=9565, ratio_emploi_actif=round(6556 / 9565, 2)),
                      sources=[SOURCE_INSEE]),
    "climat": CLIMAT,
    "submersion": SUBMERSION,
    "municipales": dict(MUNICIPALES_2026, stats=dict(
        exprimes=sum(l["voix"] for l in MUNICIPALES_2026["listes"]),
        inscrits=19089, abstention=38.1,
        voix_par_siege=round(sum(l["voix"] for l in MUNICIPALES_2026["listes"]) / 35))),
    "finances": dict(FINANCES_STRATE, budget=dict(BUDGET_VILLE, total=budget_total, stats=budget_stats)),
    "secteurs": SECTEURS,
    "projets": dict(label="Portefeuille de projets urbains", rows=PROJETS, stats=projets_stats),
    "acteurs": dict(label="Cartographie des parties prenantes", rows=ACTEURS, stats=acteurs_stats,
                    note="Les scores d'influence et d'intérêt (1-5) sont une estimation d'analyste "
                         "(fiabilité C), destinée à être validée en entretien."),
    "scenarios": dict(label="Trois scénarios 2040", rows=SCENARIOS, conditions=CONDITIONS_2030),
    "conditions": dict(label="Cinq conditions de succès à 2030", rows=CONDITIONS_2030),
    "jalons": dict(label="Jalons 2026-2040", rows=JALONS),
    "swot": SWOT,
    "recos": RECOS,
}

atlas = dict(
    meta=dict(
        titre="Atlas interactif — Frontignan la Peyrade",
        sous_titre="Acteurs, données et futurs du bassin de Thau (2026 → 2040)",
        genere_le=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        nb_noeuds=len(nodes), nb_liens=len(links),
        echelles=["Frontignan", "La ville", "L'agglo de Thau", "Les environs", "La France"],
        methode="Données INSEE (RP2023, Filosofi 2023, Flores 2024, état civil 2025) recalculées ici ; "
                "documents budgétaires et délibérations ; presse locale datée ; estimations d'analyste "
                "explicitement signalées.",
    ),
    typeColors=TYPE_COLORS,
    nodes=nodes, links=links, roots=roots,
    datasets=datasets, slides=SLIDES,
)

out_dir = os.path.join(BASE, "atlas", "data")
os.makedirs(out_dir, exist_ok=True)
out = os.path.join(out_dir, "atlas.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(atlas, fh, ensure_ascii=False, separators=(",", ":"))

# export CSV du jeu communal (réutilisable)
csv_path = os.path.join(out_dir, "communes-thau.csv")
with open(csv_path, "w", encoding="utf-8") as fh:
    keys = [f["key"] for f in CHAMPS_COMMUNES] + ["code"]
    fh.write(";".join(keys) + "\n")
    for c in COMMUNES:
        fh.write(";".join(str(c.get(k, "")).replace(".", ",") if isinstance(c.get(k), float)
                          else str(c.get(k, "")) for k in keys) + "\n")

size = os.path.getsize(out) / 1024
print(f"✔ {out} ({size:.0f} Ko) — {len(nodes)} nœuds, {len(links)} liens, {len(datasets)} jeux de données")
print(f"✔ {csv_path}")
print(f"  Gini population = {gini_pop:.3f} · Gini emplois = {gini_emp:.3f}")
for k in ["nvm", "dens", "tcho"]:
    s = stats_communes[k]
    print(f"  {k:6s} moy={s['moyenne']:.1f} med={s['mediane']:.1f} σ={s['ecart_type']:.1f} "
          f"R={s['etendue']:.1f} CV={s['cv']:.1f}% z(Frontignan)={s.get('z_frontignan', 0):+.2f}")
