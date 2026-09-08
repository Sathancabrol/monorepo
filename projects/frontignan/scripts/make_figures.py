# -*- coding: utf-8 -*-
"""Figures du rapport d'analyse territoriale — Frontignan la Peyrade (sept. 2026)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyBboxPatch
import numpy as np
import textwrap, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(OUT, exist_ok=True)

# Palette
DARK = "#0F4C5C"; TEAL = "#1B7F8C"; LIGHT = "#7FC1CC"; GOLD = "#C99A2E"
SAND = "#E9DFC8"; RED = "#B24C3A"; GREY = "#6B7A7F"; GREEN = "#4E7A4E"; ORANGE="#D08A38"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10,
    "axes.edgecolor": "#9aa8ad", "axes.linewidth": 0.8,
    "axes.titlesize": 12, "axes.titleweight": "bold",
    "figure.facecolor": "white", "axes.facecolor": "white",
})

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("ok:", name)

# ---------------------------------------------------------------- FIG 1 : entonnoir
fig, ax = plt.subplots(figsize=(9.5, 6.2))
levels = [
    ("FRANCE", "≈ 68 M hab. — ZAN 2050 · loi Climat · France 2030 (54 Md€) · Fonds vert · Action cœur de ville", 0.0, 1.0, DARK),
    ("OCCITANIE", "6 124 653 hab. (2023) · +0,8 %/an · 2e région touristique de France", 0.07, 0.86, TEAL),
    ("HÉRAULT", "1 230 289 hab. (2023) · +1,2 %/an · 2e dept le plus dynamique de France", 0.15, 0.71, "#2E93A0"),
    ("SÈTE AGGLOPÔLE MÉDITERRANÉE", "14 communes · ≈ 131 000 hab. · siège à Frontignan · présidence : Loïc Linares (Frontignan)", 0.23, 0.55, LIGHT),
    ("FRONTIGNAN LA PEYRADE", "24 136 hab. (2023) · 7e ville de l'Hérault · 2e commune de l'agglo", 0.33, 0.40, GOLD),
]
top_w, h, gap = 8.6, 1.02, 0.16
y = len(levels) * (h + gap)
for i, (title, sub, inset, frac, col) in enumerate(levels):
    wtop = top_w * (1 - inset); wbot = top_w * (1 - inset) * frac + top_w * 0.12
    yc = y - h / 2
    poly = Polygon([(-wtop/2, yc + h/2), (wtop/2, yc + h/2), (wbot/2, yc - h/2), (-wbot/2, yc - h/2)],
                   closed=True, facecolor=col, edgecolor="white", lw=2, alpha=0.95)
    ax.add_patch(poly)
    tcol = "white" if i < 3 else DARK
    ax.text(0, yc + 0.16, title, ha="center", va="center", fontsize=11.5, fontweight="bold", color=tcol)
    ax.text(0, yc - 0.26, sub, ha="center", va="center", fontsize=8.3, color=tcol, wrap=True)
    y -= (h + gap)
ax.set_xlim(-5, 5); ax.set_ylim(0, len(levels) * (h + gap) + 0.2)
ax.axis("off")
ax.set_title("Approche en entonnoir : du national au local (données INSEE 2023, sources rapport §1-4)", fontsize=11, pad=8)
save(fig, "fig1_entonnoir.png")

# ---------------------------------------------------------------- FIG 2 : population
years = [1968, 1975, 1982, 1990, 1999, 2007, 2012, 2017, 2023]
pop   = [11141, 12238, 14951, 16245, 19145, 23068, 22728, 22762, 24136]
fig, ax = plt.subplots(figsize=(9.5, 5.4))
ax.plot(years, pop, marker="o", color=DARK, lw=2.2, markersize=6, zorder=3)
ax.fill_between(years, pop, color=LIGHT, alpha=0.25)
for x, yv in zip(years, pop):
    ax.annotate(f"{yv:,}".replace(",", " "), (x, yv), textcoords="offset points", xytext=(0, 9),
                ha="center", fontsize=8.5, color=DARK)
ax.annotate("Fermeture de la raffinerie\nMobil / Esso (1986)", xy=(1986, 15600), xytext=(1973.2, 20500),
            fontsize=8.5, color=GREY, ha="center",
            arrowprops=dict(arrowstyle="->", color=GREY, lw=0.9))
ax.annotate("Stagnation 2007-2017\n(crise post-2008)", xy=(2012, 22728), xytext=(2005.5, 13300),
            fontsize=8.5, color=GREY, ha="center",
            arrowprops=dict(arrowstyle="->", color=GREY, lw=0.9))
ax.annotate("+6,0 % depuis 2017\n(attractivité résidentielle)", xy=(2023, 24136), xytext=(2019.5, 19200),
            fontsize=9, color=GOLD, fontweight="bold", ha="center",
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.2))
ax.set_ylim(10000, 26500); ax.set_xlim(1964, 2027)
ax.set_ylabel("Population (hab.)")
ax.set_title("Frontignan : population 1968 → 2023 (populations légales INSEE, RP2023)")
ax.grid(axis="y", color="#dfe6e8", lw=0.7)
ax.set_axisbelow(True)
save(fig, "fig2_population.png")

# ---------------------------------------------------------------- FIG 3 : âges + CSP
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 4.8), gridspec_kw={"width_ratios": [1.35, 1]})
groups = ["0-14", "15-24", "25-39", "40-54", "55-64", "65-79", "80+"]
v2012 = [16.4, 11.5, 16.5, 21.9, 13.5, 14.1, 6.2]
v2023 = [14.8, 10.3, 14.6, 19.9, 15.1, 17.4, 7.9]
x = np.arange(len(groups)); w = 0.38
a1.bar(x - w/2, v2012, w, label="2012", color=LIGHT)
a1.bar(x + w/2, v2023, w, label="2023", color=DARK)
for xi, v in zip(x + w/2, v2023):
    a1.annotate(f"{v:.1f}", (xi, v), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=8, color=DARK)
a1.set_xticks(x); a1.set_xticklabels(groups, fontsize=9)
a1.set_ylabel("Part de la population (%)"); a1.legend(frameon=False)
a1.set_title("Structure par âge : vieillissement marqué\n(25,3 % de 65 ans et + en 2023)")
a1.grid(axis="y", color="#dfe6e8", lw=0.7); a1.set_axisbelow(True)

csp = ["Employés", "Prof. intermédiaires", "Ouvriers", "Cadres", "Artisans,\ncommerçants, chefs", "Agriculteurs"]
share = [32.4, 27.2, 19.7, 12.7, 7.7, 0.3]
colors = [TEAL, DARK, GOLD, GREEN, ORANGE, GREY]
b = a2.barh(csp[::-1], share[::-1], color=colors[::-1])
for r, v in zip(b, share[::-1]):
    a2.annotate(f"{v:.1f} %", (v, r.get_y() + r.get_height()/2), xytext=(4, 0),
                textcoords="offset points", va="center", fontsize=8.5, color="#333")
a2.set_xlim(0, 38)
a2.set_xlabel("Part des actifs (%)")
a2.set_title("Actifs 15-64 ans par CSP (2023)\nprofil populaire & intermédiaire")
a2.grid(axis="x", color="#dfe6e8", lw=0.7); a2.set_axisbelow(True)
fig.tight_layout()
save(fig, "fig3_ages_csp.png")

# ---------------------------------------------------------------- FIG 4 : budget
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 4.9))
labels = ["BP 2022", "BP 2024", "BP 2025", "2026\n(BP + BS + reports)"]
fonc = [40.5, 45.0, 39.6, 43.9]; inv = [18.5, 24.0, 17.2, 20.9]
x = np.arange(len(labels)); w = 0.36
a1.bar(x - w/2, fonc, w, label="Fonctionnement", color=TEAL)
a1.bar(x + w/2, inv, w, label="Investissement", color=GOLD)
for xi, v in zip(x - w/2, fonc):
    a1.annotate(f"{v:.1f}", (xi, v), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=9, color=DARK)
for xi, v in zip(x + w/2, inv):
    a1.annotate(f"{v:.1f}", (xi, v), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=9, color=GOLD)
a1.set_xticks(x); a1.set_xticklabels(labels, fontsize=8.5)
a1.set_ylabel("M€"); a1.legend(frameon=False, loc="lower right")
a1.set_title("Budget principal de la commune (M€)\n2024 : répartition estimée (69 M€ dont 24 M€ d'investissement)")
a1.grid(axis="y", color="#dfe6e8", lw=0.7); a1.set_axisbelow(True); a1.set_ylim(0, 55)

ratios = ["Dette par hab.\n(2024)", "Impôts locaux\npar hab. (2024)", "Investissement\npar hab. (2024)", "Désendettement\n(années, 2024)"]
fv = [995, 1011, 270, 7.5]; st = [986, 793, 438, 5.5]
x = np.arange(4)
a2.bar(x - 0.19, fv, 0.38, label="Frontignan", color=DARK)
a2.bar(x + 0.19, st, 0.38, label="Moyenne strate 20-50k hab.", color=LIGHT)
for xi, v in zip(x - 0.19, fv):
    a2.annotate(f"{v:,.0f}".replace(",", " "), (xi, v), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=8.5, color=DARK)
for xi, v in zip(x + 0.19, st):
    a2.annotate(f"{v:,.0f}".replace(",", " "), (xi, v), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=8.5, color=TEAL)
a2.set_xticks(x); a2.set_xticklabels(ratios, fontsize=8.2)
a2.legend(frameon=False, fontsize=8.5, loc="upper right")
a2.set_title("Frontignan vs strate : fiscalité élevée,\ninvestissement/hab. contenu (Décomptes publics)")
a2.grid(axis="y", color="#dfe6e8", lw=0.7); a2.set_axisbelow(True)
fig.tight_layout()
save(fig, "fig4_budget.png")

# ---------------------------------------------------------------- FIG 5 : frise projets
events = [
    (2017.0, "Fusion Thau Agglo + CCNBT\n→ Sète Agglopôle Méditerranée\n(siège à Frontignan)"),
    (2019.5, "Lancement opération\nCœur de Ville / ORU\n(15 M€ sur 10 ans)"),
    (2021.72, "Maison des projets\net de la Citoyenneté\n(concertation Cittanova)"),
    (2020.4, "Municipales :\nMichel Arrouy (PS) élu maire"),
    (2022.6, "Début de la dépollution\nde la friche ExxonMobil\n(11 ha)"),
    (2023.45, "PEM/gare acté : 25 M€\n(Région ≤ 10 M€, agglo 20 %,\nÉtat engagé)"),
    (2022.95, "Chantier du pôle culturel\naux chais Botta"),
    (2024.35, "PPA « recomposition spatiale »\n(cartes 30/100 ans, scénario\nFrontignan-Plage, 700 k€)"),
    (2024.6, "Travaux du cœur de ville\n(5 phases, jusqu'à mi-2025)"),
    (2025.2, "Label Action cœur de Ville\n(convention juin 2025)"),
    (2025.55, "PEM gare de Sète livré ·\nUVE en service (agglo)"),
    (2025.75, "Quai Voltaire requalifié (1,5 M€)\n· ligne express bus RD2 (janv. 2026)"),
    (2025.97, "Ouverture du cinéma\nLe Quai des Lumières (19 déc. 2025)"),
    (2026.2, "Municipales : Arrouy réélu (51,2 %) ·\nLinares réélu président de l'agglo"),
    (2026.55, "Budget agglo 2026 (242 M€) :\nmarchés centre aquatique Frontignan\nlancés · friche Mobil restituée"),
    (2026.4, "Restitution de la friche Mobil\nà la Ville (27 mai 2026)"),
    (2026.75, "Chantier port de plaisance (≈ 2026-2029)\n· études usages friche (fin 2026)"),
    (2027.5, "Prise de possession de la friche ·\nenquête Mas de Chave (à confirmer)"),
    (2028.6, "Nouvelle gare + pôle d'échanges\nmultimodal (horizon 2028-2029)"),
    (2029.5, "LGV phase 1 Montpellier-Béziers :\ndébut des travaux (service 2034)"),
]
# Affectation gloutonne des niveaux pour éviter tout chevauchement d'étiquettes
MIN_GAP = 2.3  # années minimales entre deux étiquettes d'un même niveau
last_at = {}   # niveau -> dernière position étiquette
placed = []
for x, label in events:
    for lvl in (1, -1, 2, -2, 3, -3, 4, -4):
        if lvl not in last_at or (x - last_at[lvl]) >= MIN_GAP:
            break
    last_at[lvl] = x
    placed.append((x, label, lvl))
events = placed

fig, ax = plt.subplots(figsize=(14.5, 8.2))
ax.axhline(0, color=DARK, lw=2, zorder=1)
for yr in range(2017, 2035, 2):
    ax.plot(yr, 0, "o", color="white", ms=5, mec=DARK, zorder=3)
    ax.annotate(str(yr), (yr, 0), xytext=(0, -14 if yr % 4 else 14), textcoords="offset points",
                ha="center", fontsize=8.5, color=GREY)
lvl_off = {1: 0.85, -1: -0.85, 2: 1.8, -2: -1.8, 3: 2.75, -3: -2.75, 4: 3.7, -4: -3.7}
cols = {1: TEAL, -1: GOLD, 2: DARK, -2: RED, 3: GREEN, -3: GREY, 4: "#5B8FA8", -4: "#8B6F4E"}
for x, label, lvl in events:
    yv = lvl_off[lvl]
    ax.plot([x, x], [0, yv], color=cols[lvl], lw=1.1, zorder=2)
    ax.plot(x, yv, "o", color=cols[lvl], ms=5, zorder=3)
    ax.annotate(label, (x, yv), xytext=(0, 7 if lvl > 0 else -7), textcoords="offset points",
                ha="center", va="bottom" if lvl > 0 else "top", fontsize=7.3, color="#28363b",
                linespacing=1.3,
                bbox=dict(boxstyle="round,pad=0.32", fc="white", ec=cols[lvl], lw=0.8, alpha=0.95))
ax.set_xlim(2016.3, 2034.9); ax.set_ylim(-5.1, 5.0); ax.axis("off")
ax.set_title("Frise des projets structurants — Frontignan la Peyrade, 2017 → 2034 (statuts et sources : §5 du rapport)", fontsize=12, pad=10)
save(fig, "fig5_frise_projets.png")

# ---------------------------------------------------------------- FIG 6 : SWOT
fig, ax = plt.subplots(figsize=(12.2, 7.6))
quads = [
    ("FORCES", "#2E7D5B", 0.02, 0.52, [
        "Muscat AOP 1936 (90 ans en 2026) : notoriété mondiale, 800 ha, ~3 M bouteilles/an",
        "Littoral remarquable : 7 km de lido, étangs, salins, 4 sites Natura 2000, station classée",
        "Gare TER Montpellier–Sète (21 km / 7 km) + ligne express RD2 (2026)",
        "Présidence + siège de l'agglo (Loïc Linares) : poids intercommunal inédit",
        "Finances saines : dette 995 €/hab., taux stables 8 ans, épargne en hausse",
        "11 ha dépollués en cœur de ville (friche Mobil) : foncier rare en France",
        "Vacance commerciale faible (≈ 4 %) ; marché historique ; stationnement gratuit",
        "Dynamisme démographique (+1 %/an) et associatif (FIRN, joutes, muscat)"]),
    ("FAIBLESSES", RED, 0.52, 1.02, [
        "Chômage 14,0 % (28,9 % des 15-24 ans) ; pauvreté 16,5 %",
        "Vieillissement : 25,3 % de 65 ans et + ; revenu médian modeste (24 580 €)",
        "Dépendance automobile (80 % des actifs) ; 67 % de navettes hors commune",
        "Risques majeurs : submersion marine (PPRI), 2 sites Seveso seuil haut (GDH, SCORI) + PPRT",
        "Pression fiscale élevée (1 011 €/hab. vs 793 en strate) ; invest./hab. contenu (270 €)",
        "Offre hôtelière limitée (3 hôtels) ; saisonnalité touristique marquée",
        "Image industrielle passée ; coupures urbaines (canal, voie ferrée, ex-RN112)",
        "Ancrage RN fort (35,9 %) ; participation électorale fragile (38 % d'abstention)"]),
    ("OPPORTUNITÉS", TEAL, 0.52, 1.02, [
        "Action cœur de Ville (2025) : ingénierie + financements État (prolongé fin 2025)",
        "Nouvelle gare / PEM 2028-2029 et reconversion de la friche Mobil (11 ha)",
        "Plan Littoral 21 : montée en gamme, recul du trait de côte (financement jusqu'à 80 %)",
        "LGV Montpellier–Béziers (travaux 2029) : capacité libérée sur la ligne classique",
        "Œnotourisme & « Muscat 90 ans » ; tourisme fluvial (halte plaisance)",
        "Centre aquatique de l'agglo prévu à Frontignan (études 2025)",
        "Croissance Hérault (+15 000 arrivants/an) : demande en logements et services",
        "ZAN : reconquête des friches déjà engagée = avance méthodologique"]),
    ("MENACES", ORANGE, 0.02, 0.52, [
        "Changement climatique : submersion, canicules (vigilances 2026), sécheresse, incendies",
        "Baisse des dotations (FCTVA −2 pts) et du Fonds vert (2,5 Md€ → 0,83 Md€ 2026)",
        "Hausse des taux d'intérêt (intérêts agglo +27,6 % en 2025)",
        "Pollutions récurrentes de l'étang de Thau ; crise conchylicole (économie locale)",
        "Calendrier/financements LGV incertains (40 % à la charge des collectivités)",
        "Instabilité de gouvernance agglo (présidence changée 2 fois en 1 an en 2025-2026)",
        "Concurrence touristique (PACA, Corse en hausse ; littoral occitan en repli)",
        "Déficit d'encadrement des jeunes (chômage, décrochage) : risque de sécession civique"]),
]
for name, col, x0, x1, items in quads:
    row = 0 if name in ("FORCES", "FAIBLESSES") else 1
    y0 = 0.53 - row * 0.53 if name in ("FORCES", "OPPORTUNITÉS") else None
    # simpler explicit placement
for (name, col, x0, x1, items) in quads:
    if name == "FORCES":  bx, by = 0.005, 0.505
    if name == "FAIBLESSES": bx, by = 0.505, 0.505
    if name == "OPPORTUNITÉS": bx, by = 0.005, 0.005
    if name == "MENACES": bx, by = 0.505, 0.005
    box = FancyBboxPatch((bx, by), 0.49, 0.49, boxstyle="round,pad=0.008",
                         facecolor="white", edgecolor=col, lw=1.6)
    ax.add_patch(box)
    ax.text(bx + 0.245, by + 0.472, name, ha="center", va="top", fontsize=12.5,
            fontweight="bold", color=col)
    ty = by + 0.435
    for it in items:
        ax.text(bx + 0.018, ty, "•", fontsize=9, color=col, va="top")
        ax.text(bx + 0.038, ty, "\n".join(textwrap.wrap(it, 62)), fontsize=7.6,
                va="top", color="#28363b", linespacing=1.25)
        ty -= 0.052
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
ax.set_title("Matrice SWOT — Frontignan la Peyrade (synthèse des sections 4 à 7 du rapport)", fontsize=12.5, pad=10)
save(fig, "fig6_swot.png")

# ---------------------------------------------------------------- FIG 7 : priorisation
recos = [
    ("R1. Identité territoriale & signalétique\n(muscat · polar · littoral · mémoire industrielle)", 4.2, 4.4),
    ("R2. Dispositif outillé de concertation\n(friche Mobil · Mas de Chave · gare)", 4.6, 3.8),
    ("R3. Design du pôle d'échanges\ngare / PEM (2028-29)", 4.8, 2.8),
    ("R4. Expérience habitants des chantiers\n(info, parcours, vitrines travaux)", 3.6, 4.6),
    ("R5. Stratégie œnotourisme « Muscat 90 ans »\n(parcours urbain, musée, caves)", 4.0, 4.1),
    ("R6. Design du risque\n(submersion, chaleur, mémoire)", 3.8, 3.2),
    ("R7. Revitalisation commerciale\n(boutiques à l'essai, retail design)", 3.4, 4.2),
    ("R8. Écoconception des espaces publics\n(végétalisation, ombrage, eau)", 3.9, 3.4),
    ("R9. Montée en gamme Frontignan-Plage\n(Plan Littoral 21)", 4.1, 2.5),
    ("R10. Observatoire data & évaluation\n(tableau de bord territoire)", 3.2, 3.7),
]
fig, ax = plt.subplots(figsize=(10.8, 7.0))
ax.axvspan(3, 5.2, 3, 5.2, color="#e8f3ee", zorder=0)
ax.axvline(3, color=GREY, lw=1, ls="--"); ax.axhline(3, color=GREY, lw=1, ls="--")
ax.text(4.1, 5.05, "PRIORITÉS ABSOLUES", fontsize=9, color=GREEN, fontweight="bold", ha="center")
ax.text(1.6, 5.05, "CHANTIERS STRUCTURANTS", fontsize=9, color=TEAL, fontweight="bold", ha="center")
ax.text(4.1, 1.7, "VICTOIRES RAPIDES", fontsize=9, color=GOLD, fontweight="bold", ha="center")
ax.text(1.6, 1.7, "À PROGRAMMER", fontsize=9, color=GREY, fontweight="bold", ha="center")
for i, (label, imp, fais) in enumerate(recos, 1):
    ax.scatter(fais, imp, s=210, color=[TEAL, GREEN, DARK, GOLD, "#2E93A0", RED, ORANGE, GREEN, DARK, GREY][i-1],
               zorder=3, edgecolor="white", lw=1.4)
    ax.annotate(label, (fais, imp), xytext=(9, -3), textcoords="offset points", fontsize=7.8,
                color="#28363b", va="center")
ax.set_xlim(1.9, 5.35); ax.set_ylim(1.5, 5.35)
ax.set_xlabel("Faisabilité (moyens, calendrier, adhésion) →")
ax.set_ylabel("Impact attendu (attractivité, cohésion, usages) →")
ax.set_title("Matrice de priorisation des recommandations design (détail et KPI : §8.4)")
ax.grid(color="#eef2f3", lw=0.7); ax.set_axisbelow(True)
save(fig, "fig7_priorisation.png")

# ---------------------------------------------------------------- FIG 8 : parties prenantes
stake = [
    ("Maire & exécutif municipal", 4.9, 4.9, "inst"),
    ("Sète Agglopôle (Linares, Gouvernayre)", 4.7, 4.6, "inst"),
    ("Région Occitanie (gare, TER, LGV)", 4.4, 4.5, "inst"),
    ("Département de l'Hérault", 3.4, 3.7, "inst"),
    ("État / préfecture (ACV, PPRT, ZAN)", 3.9, 4.2, "inst"),
    ("ANCT (Action cœur de Ville)", 3.2, 3.0, "inst"),
    ("SNCF Réseau / transporteurs", 3.7, 3.3, "inst"),
    ("Communes voisines (Sète, Balaruc…)", 3.0, 3.5, "inst"),
    ("Vignerons & cave coopérative", 3.9, 2.9, "eco"),
    ("Industriels (Hexis, GDH, SCORI, ZA)", 3.1, 2.7, "eco"),
    ("Commerçants & artisans", 4.0, 2.4, "eco"),
    ("Conchyliculteurs & pêcheurs", 3.4, 2.2, "eco"),
    ("Professionnels du tourisme / OTI", 3.6, 2.7, "eco"),
    ("Promoteurs & aménageurs", 3.5, 3.0, "eco"),
    ("Associations (FIRN, patrimoine, env.)", 3.8, 2.2, "civ"),
    ("Habitants des QPV (Deux Pins, centre)", 4.2, 1.8, "civ"),
    ("Riverains des chantiers / Peyrade", 4.0, 2.0, "civ"),
    ("Plaisanciers & usagers du port", 3.2, 2.0, "civ"),
    ("Jeunesse & scolaires", 3.9, 1.6, "civ"),
    ("Presse locale (Midi Libre…)", 2.7, 2.4, "civ"),
]
colmap = {"inst": DARK, "eco": GOLD, "civ": TEAL}
fig, ax = plt.subplots(figsize=(10.8, 7.2))
ax.axvline(3, color=GREY, lw=1, ls="--"); ax.axhline(3, color=GREY, lw=1, ls="--")
for (name, inte, infl, grp) in stake:
    ax.scatter(inte, infl, s=170, color=colmap[grp], edgecolor="white", lw=1.2, zorder=3)
    ax.annotate(name, (inte, infl), xytext=(8, -3), textcoords="offset points",
                fontsize=7.8, color="#28363b", va="center")
ax.text(1.35, 5.0, "À GARDER SATISFAITS", fontsize=8.6, color=GREY, fontweight="bold")
ax.text(4.7, 5.0, "À GÉRER DE PRÈS", fontsize=8.6, color=DARK, fontweight="bold", ha="right")
ax.text(1.35, 1.35, "À SUIVRE", fontsize=8.6, color=GREY, fontweight="bold")
ax.text(4.7, 1.35, "À TENIR INFORMÉS", fontsize=8.6, color=TEAL, fontweight="bold", ha="right")
from matplotlib.lines import Line2D
leg = [Line2D([0], [0], marker="o", ls="", color=DARK, label="Institutionnels"),
       Line2D([0], [0], marker="o", ls="", color=GOLD, label="Acteurs économiques"),
       Line2D([0], [0], marker="o", ls="", color=TEAL, label="Société civile & habitants")]
ax.legend(handles=leg, frameon=False, loc="lower left", fontsize=8.5)
ax.set_xlim(1.2, 5.4); ax.set_ylim(1.2, 5.4)
ax.set_xlabel("Intérêt / impact sur le projet →")
ax.set_ylabel("Influence / pouvoir de blocage →")
ax.set_title("Cartographie des parties prenantes (grille intérêt / influence)")
ax.grid(color="#eef2f3", lw=0.7); ax.set_axisbelow(True)
save(fig, "fig8_parties_prenantes.png")

# ---------------------------------------------------------------- FIG 9 : mobilités
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.2, 4.6))
modes = ["Voiture", "Transports\nen commun", "Marche", "2-roues\nmotorisé", "Vélo", "Pas de\ndéplacement"]
vals = [80.0, 7.1, 4.4, 2.9, 2.6, 3.0]
b = a1.bar(modes, vals, color=[DARK, TEAL, GOLD, GREY, GREEN, LIGHT])
for r, v in zip(b, vals):
    a1.annotate(f"{v:.1f} %", (r.get_x() + r.get_width()/2, v), xytext=(0, 3),
                textcoords="offset points", ha="center", fontsize=9)
a1.set_ylabel("% des actifs ayant un emploi")
a1.set_title("Modes de transport domicile-travail (RP 2023)\nhyper-dépendance automobile")
a1.grid(axis="y", color="#dfe6e8", lw=0.7); a1.set_axisbelow(True); a1.set_ylim(0, 92)

sizes = [33.0, 67.0]
wedges, _ = a2.pie(sizes, colors=[TEAL, SAND], startangle=90, counterclock=False,
                   wedgeprops=dict(width=0.42, edgecolor="white"))
a2.annotate("33 %", (0.05, 0.18), ha="center", fontsize=13, fontweight="bold", color=DARK)
a2.annotate("67 %", (-0.15, -0.28), ha="center", fontsize=13, fontweight="bold", color=GOLD)
a2.text(0, -1.28, "Travaillent dans la commune : 3 156 actifs (9 565 au total)", ha="center", fontsize=8.6)
a2.set_title("Lieu de travail des actifs frontignanais (2023)\nvile-dortoir partielle des bassins de Sète & Montpellier")
save(fig, "fig9_mobilites.png")

print("Toutes les figures générées dans", OUT)
