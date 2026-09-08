# -*- coding: utf-8 -*-
"""Figures de la vision prospective Frontignan 2026-2040 (focale 2030)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Circle, FancyArrowPatch
import numpy as np, textwrap, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(OUT, exist_ok=True)

DARK = "#0F4C5C"; TEAL = "#1B7F8C"; LIGHT = "#7FC1CC"; GOLD = "#C99A2E"
SAND = "#E9DFC8"; RED = "#B24C3A"; GREY = "#6B7A7F"; GREEN = "#4E7A4E"; ORANGE = "#D08A38"
BLUE2 = "#5B8FA8"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
    "axes.edgecolor": "#9aa8ad", "axes.linewidth": 0.8, "axes.titlesize": 12,
    "axes.titleweight": "bold", "figure.facecolor": "white", "axes.facecolor": "white"})

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig); print("ok:", name)

# ================================================================ FIG V1 : trajectoire 2026-2040
macro = [
    (2027.1, "Législatives + présidentielle"),
    (2028.3, "Départ. + régionales"),
    (2029.3, "Travaux LGV phase 1\nMontpellier-Béziers"),
    (2030.3, "DUP LGV phase 2\njalon ZAN 2031"),
    (2032.2, "Municipales\nFrontignan & Sète"),
    (2034.2, "Service LGV P1 :\ngares Sète/Frontignan\n« orphelines de TGV »\n→ compensation TER"),
    (2036.0, "Horizon PLU\n(révision en cours)", 0),
    (2040.3, "Service LGV P2\nBéziers-Perpignan", 0),
]
micro = [
    (2026.15, "SCoT Thau approuvé\n(horizon 2043)"),
    (2026.8, "Barnier requalifié\n(2,7 M€, juin 2027)"),
    (2026.6, "Budget agglo 2026 :\nmarchés centre aquatique\nlancés"),
    (2027.4, "Études usages friche →\nprogrammation ; prise de\npossession du site"),
    (2028.3, "PEM / nouvelle gare\n(25 M€) — horizon 2028-29"),
    (2028.8, "Centre aquatique\nHiérles (chantier) ;\nport à 750 anneaux (fin)"),
    (2029.4, "TCSP RD2 : sections\nFrontignan (~30 M€)"),
    (2030.0, "★ FRONTIGNAN 2030"),
    (2030.8, "Mas de Chave :\npremiers logements"),
    (2031.5, "Quartier de la friche :\npremière tranche"),
    (2033.0, "Boucle friche/gare/canal\nopérée"),
    (2035.5, "Friche : tranches\nsuivantes (tertiaire,\nloisirs, culture)"),
    (2038.0, "Horizon SCoT :\nbassin +12 à 16 400 hab."),
    (2040.0, "★ 2040 : ligne\nMontpellier-Perpignan\ncomplète"),
]

fig, ax = plt.subplots(figsize=(15, 8.6))
ax.axhline(0, color=DARK, lw=2.5, zorder=2)
# bande focus 2030
ax.axvspan(2029.55, 2030.45, color=GOLD, alpha=0.18, zorder=0)
ax.text(2030.0, 0.06, "FOCALE 2030", ha="center", va="bottom", fontsize=10,
        fontweight="bold", color=GOLD)

def place(events, base, step, color, above):
    last = {}
    for ev in events:
        x, label = ev[0], ev[1]
        lvl = 0
        while (lvl in last) and (x - last[lvl]) < 1.15:
            lvl += 1
        last[lvl] = x
        y = base + (lvl + 1) * step * (1 if above else -1)
        ax.plot([x, x], [0, y], color=color, lw=0.9, zorder=1, alpha=0.7)
        ax.plot(x, y, "o", color=color, ms=4.5, zorder=3)
        ax.annotate(label, (x, y), xytext=(0, 4 if above else -4), textcoords="offset points",
                    ha="center", va="bottom" if above else "top", fontsize=7.2,
                    linespacing=1.25, color="#222d31",
                    bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=color, lw=0.8, alpha=0.95))

place(macro, 0.35, 0.78, BLUE2, above=True)
place(micro, -0.35, 0.78, TEAL, above=False)
ax.text(2019.4, 4.6, "MACRO — France & région", fontsize=10, fontweight="bold", color=BLUE2)
ax.text(2019.4, -4.75, "MICRO — Frontignan la Peyrade", fontsize=10, fontweight="bold", color=TEAL)
for yr in range(2026, 2042, 2):
    ax.plot(yr, 0, "o", color="white", mec=DARK, ms=5, zorder=4)
    ax.annotate(str(yr), (yr, 0), xytext=(0, -14 if yr % 4 else 14), textcoords="offset points",
                ha="center", fontsize=8.4, color=GREY)
ax.set_xlim(2019, 2042.4); ax.set_ylim(-5.6, 5.4); ax.axis("off")
ax.set_title("Trajectoire Frontignan 2026 → 2040 : jalons macro (haut) et micro (bas) — focale 2030", fontsize=13, pad=10)
save(fig, "figV1_trajectoire_2026_2040.png")

# ================================================================ FIG V2 : focus 2030
fig, ax = plt.subplots(figsize=(13.6, 7.4))
cols = [
    ("LIVRÉS D'ICI 2030", GREEN, 0.005, [
        "✓ PEM & nouvelle gare (25 M€, visé 2028-29)",
        "✓ Centre aquatique intercommunal (Hiérles)",
        "✓ Port de plaisance restructuré : 750 anneaux",
        "✓ ZAE du Barnier requalifiée (2,7 M€, 2027)",
        "✓ Salle de spectacle Maison Mathieu (≈150 pl.)",
        "✓ TCSP RD2 phase 1 + ligne express (2026)",
        "✓ Cœur de ville / ORU : phases principales",
        "✓ SCoT du Bassin de Thau approuvé (2026)",
        "✓ PLU communal révisé (attendu 2027-2028)",
        "✓ Cartes locales recul du trait de côte (PPA)",
    ]),
    ("EN CHANTIER / EN JEU À 2030", GOLD, 0.34, [
        "→ Quartier de la friche Mobil : 1ʳᵉ tranche",
        "   (économie circulaire, tertiaire, équipements)",
        "→ Mas de Chave : premiers logements (≈400)",
        "→ TCSP RD2 sections Frontignan (~30 M€)",
        "→ Requalification BUC / entrées de ville",
        "→ PPA : scénario de recomposition",
        "   Frontignan-Plage (méthode, foncier)",
        "→ Projet de territoire agglo horizon 2040",
        "→ Friche Lafarge : renaturation engagée ?",
        "→ Habitat : OPAH/ACV en cours de déploiement",
    ]),
    ("INDICATEURS 2030 (estimations)", DARK, 0.675, [
        "Population ≈ 25 200 – 25 800 hab.",
        "   (croissance ralentie vs 2017-2023)",
        "Part des 65 ans et + ≈ 27-29 %",
        "Ménages d'1 personne en hausse",
        "   (tendance régionale +45 % mén.)",
        "Gare nouvelle : pôle bus/vélo/parking relais",
        "Navettes domicile-travail toujours ≈ 65 %",
        "   si l'emploi local ne progresse pas",
        "Vacance commerciale à maintenir < 5-6 %",
        "Emplois : cible +300 à +600 postes locaux",
        "   (friche, Barnier, tourisme 4 saisons)",
    ]),
]
for title, col, x0, items in cols:
    box = FancyBboxPatch((x0, 0.03), 0.325, 0.93, boxstyle="round,pad=0.008",
                         facecolor="white", edgecolor=col, lw=1.8)
    ax.add_patch(box)
    ax.add_patch(FancyBboxPatch((x0, 0.875), 0.325, 0.085, boxstyle="round,pad=0.004",
                                facecolor=col, edgecolor=col, lw=1.8))
    ax.text(x0 + 0.1625, 0.917, title, ha="center", va="center", fontsize=11.5,
            fontweight="bold", color="white")
    ty = 0.845
    for it in items:
        bold = it.startswith(("✓", "→"))
        ax.text(x0 + 0.014, ty, it, fontsize=8.6, va="top",
                color="#1d2b30" if not it.startswith("   ") else "#5a6a70",
                fontweight="bold" if bold else "normal", linespacing=1.3)
        ty -= 0.079
ax.text(0.5, 0.005, "Estimations propres (croissance démographique régionale ralentie, INSEE Omphale 2022) — à considérer comme fourchettes de travail, non comme des prévisions.",
        ha="center", fontsize=8, color=GREY, style="italic")
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
ax.set_title("FOCUS 2030 — Frontignan la Peyrade : l'état probable de la ville", fontsize=14, pad=12)
save(fig, "figV2_focus_2030.png")

# ================================================================ FIG V3 : macro 2026-2050
fig, axes = plt.subplots(2, 2, figsize=(12.6, 8.2))
# (1) démographie
a = axes[0][0]
years = [2021, 2030, 2040, 2050]
occ = [6.09, 6.46, 6.68, 6.73]      # +640k (Omphale, scénario central, arrondi)
her = [1.185, 1.27, 1.36, 1.43]     # +245k
thau = [0.126, 0.1265, 0.127, 0.127]  # territoire "Étang de Thau" ~ +0,05%/an
a.plot(years, occ, "o-", color=DARK, lw=2, label="Occitanie (Mhab)")
a.plot(years, her, "o-", color=TEAL, lw=2, label="Hérault (Mhab)")
a2 = a.twinx()
a2.plot(years, [v*1000 for v in thau], "o--", color=GOLD, lw=2, label="Bassin de Thau (khab)")
a2.set_ylim(124, 129); a2.set_ylabel("Bassin de Thau (milliers)", color=GOLD, fontsize=9)
a2.tick_params(axis="y", colors=GOLD, labelsize=8)
a.set_ylim(0, 7.6); a.set_ylabel("millions d'hab.")
a.set_title("Démographie : le littoral de Thau\nquasi stable face à la croissance régionale")
a.legend(frameon=False, fontsize=8, loc="center left")
a.annotate("Montpelliérain :\n+60 % des gains du dept", xy=(2040, 1.36), xytext=(2032.5, 3.4),
           fontsize=8, color=GREY, arrowprops=dict(arrowstyle="->", color=GREY, lw=0.9))
a.annotate("+570 000 ménages\nen Occitanie 2021-2050\n(29 000 logts/an)", xy=(2050, 6.73), xytext=(2035.5, 5.6),
           fontsize=8, color=DARK, arrowprops=dict(arrowstyle="->", color=DARK, lw=0.9))
a.grid(axis="y", color="#e5ebee", lw=0.6)
# (2) chaleur
a = axes[0][1]
cats = ["Jours > 35 °C", "Nuits > 20 °C", "Jours sols secs", "Jours risque feu"]
ref = [1.3, 5, 93, 2.5]; f50 = [7.7, 24, 126, 6.7]; f100 = [17.8, 40, 149, 18.8]
x = np.arange(4); w = 0.26
a.bar(x - w, ref, w, label="1976-2005", color=LIGHT)
a.bar(x, f50, w, label="2050 (TRACC)", color=ORANGE)
a.bar(x + w, f100, w, label="2100", color=RED)
a.set_xticks(x); a.set_xticklabels(cats, fontsize=8.4)
a.set_ylabel("jours / an")
a.set_title("Climat en Occitanie (Météo-France, TRACC)\nHérault : +2,5 °C en été dès 2050")
a.legend(frameon=False, fontsize=8)
a.grid(axis="y", color="#e5ebee", lw=0.6)
for xi, v in zip(x, f50):
    a.annotate(f"{v}", (xi, v), xytext=(0, 3), textcoords="offset points", ha="center", fontsize=8, color=ORANGE)
# (3) mer
a = axes[1][0]
per = ["2026", "2050", "2100"]
cm = [8, 24, 71]  # 2100: 62-81 -> milieu 71
bars = a.bar(per, cm, color=[LIGHT, ORANGE, RED], width=0.55)
for r, v, lab in zip(bars, cm, ["≈ +8 cm*", "+24 cm", "+62 à +81 cm"]):
    a.annotate(lab, (r.get_x() + r.get_width()/2, v), xytext=(0, 4),
               textcoords="offset points", ha="center", fontsize=9, fontweight="bold")
a.set_ylabel("hausse du niveau de la mer (cm)")
a.set_title("Montée des eaux en Méditerranée\n(submersion : PPRI à PHE 2,00 m)")
a.annotate("*ordre de grandeur 2026 ; PHE centennale\nfrontignanaise déjà fixée à 2,00 m", xy=(0.5, -0.24),
           xycoords="axes fraction", ha="center", fontsize=7.5, color=GREY)
a.grid(axis="y", color="#e5ebee", lw=0.6)
a.set_ylim(0, 95)
# (4) mobilités / LGV
a = axes[1][1]
timeline = [(2026, "TCSP P1 +\nligne express"), (2028.5, "PEM Frontignan\n(horizon)"),
            (2029, "travaux LGV P1"), (2034, "LGV P1 en service\n→ +TER (SERM)"),
            (2040, "LGV P2 en service")]
axh = a
axh.axhline(0.5, color=DARK, lw=2)
for x, lab in timeline:
    axh.plot(x, 0.5, "o", color=GOLD, ms=9, mec=DARK)
    axh.annotate(lab, (x, 0.5), xytext=(0, 14 if timeline.index((x, lab)) % 2 == 0 else -30),
                 textcoords="offset points", ha="center", fontsize=7.8, linespacing=1.2)
axh.set_xlim(2024.5, 2041.5); axh.set_ylim(0, 1); axh.axis("off")
axh.set_title("Mobilités : la décennie ferroviaire\n(gare nouvelle avant la bascule LGV 2034)")
fig.suptitle("Les 4 tendances macro 2026 → 2050 qui encadrent le projet frontignanais", fontsize=13.5, fontweight="bold", y=1.0)
fig.tight_layout(rect=[0, 0, 1, 0.96])
save(fig, "figV3_macro_2050.png")

# ================================================================ FIG V4 : scénarios 2040
fig, ax = plt.subplots(figsize=(14, 8.2))
scen = [
    ("S1 — « THAU TRANQUILLE »", GREY, 0.005,
     "La stagnation gagne (bassin +0,05 %/an) : vieillissement, solde migratoire neutre, "
     "friche partiellement aménagée, gare nouvelle sous-utilisée. Frontignan devient une "
     "banlieue résidentielle vieillissante de Montpellier/Sète.",
     ["Population ≈ 24-25 000 hab., 65+ > 30 %", "Friche : logistique basique, peu d'emplois",
      "Commerces de centre-ville sous pression", "Budgets : épargne contrainte par les charges",
      "Écosystème muscat/FIRN maintenu mais statique"]),
    ("S2 — « LA COURONNE MÉTROPOLITAINE »", GOLD, 0.34,
     "La pression montpelliéraine déborde (le Montpelliérain capte 60 % des gains du dept) : "
     "arrivée massive d'actifs, gentrification du littoral, spéculation, conflits d'usages. "
     "La ville double de dynamisme mais se paupérise au centre et s'uniformise.",
     ["Population > 27 000 hab., poussée résidentielle", "Résidences secondaires → 25-30 % du parc",
      "Mas de Chave + friche : promotion privée dominante", "Équipements publics en retard sur la demande",
      "RN en tête des municipales 2032 (rejet des mutations)"]),
    ("S3 — « LE PÔLE DE LA TRANSITION » ★", GREEN, 0.675,
     "La trajectoire portée par la friche dépolluée, le PEM, le centre aquatique et l'identité "
     "muscat/polar/Thau porte ses fruits : Frontignan devient le laboratoire de la recomposition "
     "littorale (PPA) et un pôle d'emplois de l'économie bleue et circulaire.",
     ["Population ≈ 26 000 hab., attractivité familiale", "Friche : pôle économique + culturel intercommunal",
      "+500 à +1 000 emplois locaux (Barnier, friche, tourisme)", "Recomposition Frontignan-Plage lancée (PPA)",
      "Modèle reproduit sur les 30 ha de friches du bassin"]),
]
for title, col, x0, desc, bullets in scen:
    ax.add_patch(FancyBboxPatch((x0, 0.05), 0.325, 0.9, boxstyle="round,pad=0.008",
                                facecolor="#fbfcfc", edgecolor=col, lw=2))
    ax.add_patch(FancyBboxPatch((x0, 0.865), 0.325, 0.085, boxstyle="round,pad=0.004",
                                facecolor=col, edgecolor=col, lw=2))
    ax.text(x0 + 0.1625, 0.907, title, ha="center", va="center", fontsize=11,
            fontweight="bold", color="white")
    ax.text(x0 + 0.015, 0.835, "\n".join(textwrap.wrap(desc, 44)), fontsize=8.4,
            va="top", color="#28363b", linespacing=1.3)
    ty = 0.44
    ax.text(x0 + 0.015, ty + 0.035, "Signaux caractéristiques :", fontsize=8.6,
            fontweight="bold", color=col, va="top")
    for b in bullets:
        ax.text(x0 + 0.015, ty, "• " + "\n".join(textwrap.wrap(b, 44)), fontsize=8,
                va="top", color="#28363b", linespacing=1.25)
        ty -= 0.072
ax.text(0.5, 0.015, "Scénarios exploratoires 2040 (hypothèses de travail — ni prévisions ni probabilités). "
        "S3 correspond à la trajectoire portée par les documents de planification en cours (SCoT, PPA, projet de territoire agglo).",
        ha="center", fontsize=8.2, color=GREY, style="italic")
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
ax.set_title("Trois futurs possibles pour Frontignan en 2040", fontsize=14, pad=12)
save(fig, "figV4_scenarios_2040.png")

# ================================================================ FIG V5 : schéma territorial 2030
fig, ax = plt.subplots(figsize=(13.2, 9))
ax.set_facecolor("#f7fafb")
# Étang de Thau (gauche)
ax.add_patch(Polygon([(-5, -1), (0.6, -0.8), (0.9, 2.2), (0.2, 5.6), (-5, 5.6)],
                     closed=True, facecolor="#bfe0e8", edgecolor="#8fc3cf", lw=1.2))
ax.text(-2.2, 2.6, "ÉTANG DE THAU\n(7 500 ha, conchyliculture)", ha="center", fontsize=10,
        color="#20565f", fontweight="bold", linespacing=1.4)
ax.text(-2.2, 1.9, "mas conchylicoles · ports de pêche", ha="center", fontsize=8, color="#20565f")
# Mer (bas droite)
ax.add_patch(Polygon([(4.6, -1), (10.5, -1), (10.5, 2.2), (6.6, 2.35), (4.6, 2.3)],
                     closed=True, facecolor="#cfe7ee", edgecolor="#8fc3cf", lw=1.2))
ax.text(7.6, 0.6, "MER MÉDITERRANÉE", ha="center", fontsize=10, color="#20565f", fontweight="bold")
# lido
ax.add_patch(Polygon([(4.6, 2.3), (6.6, 2.35), (6.6, 2.75), (4.6, 2.7)],
                     closed=True, facecolor=SAND, edgecolor="#c9b98a"))
ax.text(5.6, 2.52, "lido · Aresquiers · Frontignan-Plage ★ recomposition (PPA)", ha="center", fontsize=7.8, color="#6b5b2c")
# étang d'Ingril
ax.add_patch(Polygon([(3.2, 2.35), (4.5, 2.3), (4.5, 3.9), (3.2, 3.85)],
                     closed=True, facecolor="#bfe0e8", edgecolor="#8fc3cf", lw=1))
ax.text(3.85, 3.1, "étang\nd'Ingril", ha="center", fontsize=8, color="#20565f")
# Gardiole
ax.add_patch(Polygon([(0.8, 4.6), (6.4, 4.9), (7.6, 6.4), (1.0, 6.4)],
                     closed=True, facecolor="#d8e8d4", edgecolor="#9dbd97", lw=1.2))
ax.text(4.0, 5.6, "MASSIF DE LA GARDIOLE (223 m)\nvignoble AOP muscat (800 ha) · garrigue", ha="center",
        fontsize=9, color="#3c5c38", fontweight="bold", linespacing=1.4)
# canal du Rhône à Sète
ax.plot([6.9, 3.4, 0.9, -1.2], [6.1, 3.6, 2.5, 1.3], color=BLUE2, lw=6, alpha=0.75, solid_capstyle="round")
ax.text(4.35, 3.95, "canal du Rhône à Sète", rotation=-38, fontsize=8, color="#20565f")
# ville : centre
ax.add_patch(FancyBboxPatch((1.7, 2.1), 2.4, 1.9, boxstyle="round,pad=0.12",
                            facecolor="#f3e6cf", edgecolor=GOLD, lw=2))
ax.text(2.9, 3.62, "FRONTIGNAN-CENTRE", ha="center", fontsize=9.5, fontweight="bold", color="#6b4f14")
for i, t in enumerate(["cœur de ville / ORU (15 M€)", "chais Botta · Le Quai", "halles · tour de Joye",
                       "QPV Calmette-Centre", "Maison Mathieu (spectacle)"]):
    ax.text(2.9, 3.32 - i * 0.24, "· " + t, ha="center", fontsize=7.6, color="#4a3a10")
# La Peyrade
ax.add_patch(FancyBboxPatch((4.55, 3.95), 2.0, 1.05, boxstyle="round,pad=0.1",
                            facecolor="#f3e6cf", edgecolor=GOLD, lw=1.6))
ax.text(5.55, 4.78, "LA PEYRADE", ha="center", fontsize=9, fontweight="bold", color="#6b4f14")
ax.text(5.55, 4.55, "Z.A. (Hexis…) · Barnier ★ (2,7 M€)", ha="center", fontsize=7.4, color="#4a3a14")
ax.text(5.55, 4.34, "friche Lafarge ★ renaturation", ha="center", fontsize=7.4, color="#4a3a14")
# friche Mobil + gare
ax.add_patch(FancyBboxPatch((0.95, 1.15), 2.6, 0.85, boxstyle="round,pad=0.1",
                            facecolor="#e3f0e6", edgecolor=GREEN, lw=2.4))
ax.text(2.25, 1.82, "FRICHE EXXONMOBIL (11 ha, dépolluée 2026)", ha="center", fontsize=8.8,
        fontweight="bold", color="#2c5530")
ax.text(2.25, 1.55, "★ PEM & nouvelle gare (25 M€, 2028-29) · quartier de la transition", ha="center",
        fontsize=7.6, color="#2c5530")
ax.text(2.25, 1.33, "parking 150 pl. · passerelle vers chais Botta", ha="center", fontsize=7.2, color="#2c5530")
# plage
ax.add_patch(FancyBboxPatch((6.7, 2.75), 1.7, 0.6, boxstyle="round,pad=0.08",
                            facecolor="#eef6ef", edgecolor=TEAL, lw=1.8))
ax.text(7.55, 3.18, "FRONTIGNAN-PLAGE", ha="center", fontsize=8.6, fontweight="bold", color=DARK)
ax.text(7.55, 2.97, "port de plaisance 603→750 anneaux", ha="center", fontsize=7.2, color=DARK)
# Mas de Chave
ax.add_patch(FancyBboxPatch((4.15, 5.05), 1.75, 0.75, boxstyle="round,pad=0.08",
                            facecolor="#f6f0e4", edgecolor=ORANGE, lw=1.6, linestyle="--"))
ax.text(5.02, 5.6, "MAS DE CHAVE ★", ha="center", fontsize=8.2, fontweight="bold", color="#8a5a1c")
ax.text(5.02, 5.38, "≈ 400 logements + parc 2 ha", ha="center", fontsize=7.2, color="#8a5a1c")
ax.text(5.02, 5.2, "(en instruction PLU)", ha="center", fontsize=6.8, color="#8a5a1c")
# Sète & Montpellier flèches
ax.annotate("SÈTE 7 km\n(PEM livré 2025,\nTCSP 2026)", xy=(-1.3, 1.2), xytext=(-4.4, 0.1),
            fontsize=8.4, color=DARK, fontweight="bold", ha="center", linespacing=1.3,
            arrowprops=dict(arrowstyle="-", color=DARK, lw=1))
ax.annotate("MONTPELLIER 21 km\n(aire d'attraction,\n+60 % des gains de pop.)", xy=(8.9, 5.9), xytext=(8.9, 5.9),
            fontsize=8.4, color=DARK, fontweight="bold", ha="center", linespacing=1.3)
# légende
ax.text(-4.6, 6.05, "★ = projet structurant 2026-2030\nSchéma de compréhension — non à l'échelle (données : rapport §5-§9)",
        fontsize=8.4, color=GREY, linespacing=1.4)
ax.set_xlim(-5, 10.5); ax.set_ylim(-1, 6.8); ax.axis("off")
ax.set_title("Frontignan la Peyrade à l'horizon 2030 — schéma territorial des projets", fontsize=14, pad=10)
save(fig, "figV5_schema_territorial.png")

print("Figures vision générées.")
