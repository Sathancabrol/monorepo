# -*- coding: utf-8 -*-
"""Deck HTML 'Frontignan 2026-2040' — autonome, scroll vertical (sans JS requis), images base64 JPEG."""
import base64, os
from io import BytesIO
from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def img64(path, maxw=1300, quality=74):
    """PNG/JPG -> data URI JPEG compressé."""
    im = Image.open(os.path.join(BASE, path)).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    buf = BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")

FIG = "figures/"
F = {n: img64(FIG + n + ".png") for n in [
    "fig1_entonnoir", "fig2_population", "fig4_budget", "fig5_frise_projets",
    "fig6_swot", "fig7_priorisation", "fig8_parties_prenantes", "fig9_mobilites",
    "figV1_trajectoire_2026_2040", "figV2_focus_2030", "figV3_macro_2050",
    "figV4_scenarios_2040", "figV5_schema_territorial"]}
HERO = img64("visuals/hero-frontignan-2030.jpg", maxw=1500, quality=78)
HERO_S = img64("visuals/hero-frontignan-2030.jpg", maxw=900, quality=70)
HERO_BG = img64("visuals/hero-frontignan-2030.jpg", maxw=1100, quality=62)
MAP = img64("visuals/carte-identite-frontignan.jpg", maxw=1200, quality=72)

K = "0F4C5C"; T = "1B7F8C"; G = "C99A2E"

slides = []
def slide(html, cls=""):
    slides.append(f'<section class="slide {cls}">{html}</section>')

# 1 — titre
slide(f'''
<div class="hero-bg" style="background-image:url('{HERO}')"></div>
<div class="title-box">
  <div class="kicker">Vision territoriale · septembre 2026</div>
  <h1>Frontignan la Peyrade</h1>
  <h2>2026 → 2040 <span>· focale 2030</span></h2>
  <p>Du national au local : trajectoires, jalons et enjeux de design<br>
  <em>Document d'appui pour l'accompagnement de la municipalité</em></p>
  <div class="badges"><span>24 136 hab.</span><span>2ᵉ ville de Sète Agglopôle</span><span>Siège de l'agglo</span><span>Littoral · étang de Thau</span></div>
</div>''')

# 2 — entonnoir
slide(f'''
<h3>Où se situe Frontignan ? L'entonnoir du national au local</h3>
<img class="tall" src="{F['fig1_entonnoir']}" alt="entonnoir">
<p class="foot">France (+ZAN, fonds vert en repli) → Occitanie (6,25 M hab., +0,8 %/an) → Hérault (1,26 M, +1,2 %/an) → Sète Agglopôle (14 communes, ≈131 000 hab.) → <b>Frontignan (24 136 hab.)</b></p>''')

# 3 — macro 2050
slide(f'''
<h3>Quatre forces macro cadrent le jeu local jusqu'en 2050</h3>
<img class="tall" src="{F['figV3_macro_2050']}" alt="macro">
<p class="foot">Démographie INSEE Omphale 2022 · Climat Météo-France TRACC · LGV (2034/2040) · ZAN & finances publiques</p>''')

# 4 — démographie
slide(f'''
<h3>Démographie : la marche à deux visages</h3>
<div class="cols2">
<div>
<img src="{F['fig2_population']}" alt="population">
</div>
<div class="txt">
<p><b>La région croît</b> : Occitanie +640 000 hab. et +570 000 ménages d'ici 2050 ; Hérault → 1,43 M hab., dont 60 % des gains dans le Montpelliérain.</p>
<p><b>Le bassin de Thau stagne</b> : +0,05 %/an (INSEE) ≈ 127 000 hab. en 2050. Frontignan (+6 % depuis 2017) vit de son attractivité résidentielle — <b>une variable réversible</b>.</p>
<p><b>Vieillissement</b> : 65+ = 25 % aujourd'hui, ≈ 27-29 % en 2030 ; personnes seules = 45 % des ménages régionaux en 2050.</p>
<p class="hl">→ Enjeu : capter la croissance métropolitaine <em>sans</em> perdre identité ni mixité sociale.</p>
</div>
</div>''')

# 5 — climat & littoral
slide(f'''
<h3>Climat : un littoral sous contrainte croissante — et connue</h3>
<div class="stats">
<div class="stat"><b>+2,5 °C</b><span>en été dans l'Hérault dès 2050 (TRACC)</span></div>
<div class="stat"><b>×6</b><span>jours &gt; 35 °C en 2050 (7,7/an contre 1,3)</span></div>
<div class="stat"><b>+24 cm</b><span>de niveau de mer en 2050 (+62-81 cm en 2100)</span></div>
<div class="stat"><b>2,00 m</b><span>PHE centennale du PPRI de Frontignan</span></div>
</div>
<div class="txt">
<p><b>La réponse institutionnelle existe</b> : PPA « recomposition spatiale » (2024) — cartes 30/100 ans, plan-guide du triangle Sète-Balaruc-Frontignan, <b>scénario dédié Frontignan-Plage</b>, association des habitants.</p>
<p><b>La lagune = l'indicateur vital</b> : crise conchylicole (déc. 2025), 120 M€ d'assainissement en 10 ans, 13,1 M€ fléchés en 2026 par l'agglo.</p>
<p class="hl">→ Le design du risque (submersion, chaleur, mémoire industrielle) est un <b>projet à part entière</b>, pas une contrainte.</p>
</div>''')

# 6 — bassin de Thau
slide(f'''
<h3>Le bassin de Thau : la règle du jeu collective 2026-2043</h3>
<div class="cols2">
<div class="txt">
<p><b>SCoT révisé</b> (approbation attendue fin 2026) : <b>−54 % d'artificialisation</b>, ≈ 1 000 logements/an, +12 à 16 400 hab. à l'horizon 2043-2045 — un rabot démographique assumé, priorité aux <b>friches</b> (30 ha à remobiliser).</p>
<p><b>Projet de territoire agglo horizon 2040</b> en refonte (Linares) : « reconstruire la ville sur la ville », économie bleue et verte, 10-15 M€ de compensations LGV à réinvestir.</p>
<p><b>Mobilités</b> : TCSP phase 1 en service (janv. 2026), sections Frontignan ≈ 30 M€, PEM Sète livré, réseau repensé.</p>
<p class="hl">→ Frontignan cumule un triple siège : <b>siège + présidence + VP tourisme</b> de l'agglo.</p>
</div>
<div>
<img class="tall" src="{MAP}" alt="carte identité">
</div>
</div>''')

# 7 — trajectoire
slide(f'''
<h3>La trajectoire 2026 → 2040 : tout se joue avant 2032</h3>
<img class="tall" src="{F['figV1_trajectoire_2026_2040']}" alt="trajectoire">
<p class="foot">2026-2030 : fenêtre d'exécution (gare, friche, piscine, port, TCSP) · 2032 : municipales-bilan · 2034 : bascule LGV · 2040 : ligne complète & horizon SCoT</p>''')

# 8 — focus 2030
slide(f'''
<h3>Focale 2030 : l'état probable de la ville</h3>
<img class="tall" src="{F['figV2_focus_2030']}" alt="focus 2030">
<p class="foot">5 conditions de succès : PEM livré <em>et desservi</em> · friche programmée <em>et financée</em> · +300 à +600 emplois locaux · qualité de l'eau de Thau · mixité sociale du centre préservée</p>''')

# 9 — schéma territorial
slide(f'''
<h3>Le territoire en 2030 : un schéma pour se repérer</h3>
<img class="tall" src="{F['figV5_schema_territorial']}" alt="schéma territorial">
<p class="foot">L'axe structurant : canal ↔ chais Botta ↔ passerelle ↔ gare/PEM ↔ friche (11 ha) — la « couture » des trois centralités (centre · La Peyrade · plage)</p>''')

# 10 — friche & gare
slide(f'''
<h3>Le cœur de la décennie : friche Mobil + gare/PEM</h3>
<div class="cols2">
<div class="txt">
<p><b>11 ha dépollués, restitués à la Ville le 27 mai 2026</b> — pollueur-payeur (Esso/North Atlantic), 170 000 m³ excavés, 40 ans de contentieux soldés.</p>
<p><b>Programme</b> : PEM 25 M€ (Région ≤ 10 M€ · agglo 20 % · État · Ville) livrable 2028-29 ; quartier sans logements — économie circulaire, tertiaire, loisirs, culture ; bâtiment administratif conservé (mémoire).</p>
<p><b>Positions 2026</b> : Arrouy — écologie industrielle + PME de transition, foncier public ; Delapierre (RN) — emplois privés, numérique ; Cléret — pôle culturel 1 500 places.</p>
<p class="hl">→ Usages transitoires dès 2027 ; masterplan co-construit = <b>le chantier design n°1</b>.</p>
</div>
<div>
<img src="{HERO_S}" alt="vision 2030" style="border-radius:8px">
</div>
</div>''')

# 11 — mobilités
slide(f'''
<h3>Mobilités : la bascule 2026 → 2034</h3>
<div class="cols2">
<div>
<img src="{F['fig9_mobilites']}" alt="mobilites">
</div>
<div class="txt">
<p><b>Aujourd'hui</b> : 80 % des actifs en voiture, 67 % travaillent hors commune.</p>
<p><b>2026</b> : TCSP RD2 phase 1 + ligne express électrique Sète-Balaruc-Sète + nouveau réseau SAMobilité (5 janvier 2026).</p>
<p><b>2028-29</b> : PEM et gare nouvelle de Frontignan (25 M€) — parkings relais, passerelle, vélos.</p>
<p><b>2034</b> : LGV phase 1 en service — gares de Sète et Frontignan « orphelines des TGV », compensation par les TER (objectif SERM : un train/10 min aux heures de pointe, cars express Montpellier-Poussan).</p>
<p class="hl">→ La gare nouvelle aura 5 ans d'avance sur la bascule : elle doit être « prête à tout ».</p>
</div>
</div>''')

# 12 — économie
slide(f'''
<h3>Économie : réindustrialiser l'identité</h3>
<div class="txt">
<p><b>Base actuelle</b> : 6 311 emplois salariés (40 % public/santé/social, 16 % industrie — Hexis, ZA La Peyrade), muscat (800 ha AOP, ~3 M bouteilles, 90 ans en 2026), tourisme très saisonnier (3 hôtels, 6 campings, 20,6 % de résidences secondaires), port rentable (excédent 607 k€ en 2025).</p>
<p><b>Leviers 2026-2030</b> : ZAE du Barnier requalifiée (2,7 M€, livrée juin 2027) ; friche Mobil — entreprises « non délocalisables » de la transition ; œnotourisme « Muscat 90 ans » ; FIRN et saison culturelle ; tourisme fluvial (halte plaisance) ; montée en gamme Plan Littoral 21.</p>
<p class="hl">→ Cible 2030 : <b>+300 à +600 emplois locaux</b> et un tourisme 4 saisons — sinon la ville reste une ville-dortoir à 67 % de navetteurs.</p>
</div>
<img src="{F['fig4_budget']}" alt="budget">''')

# 13 — finances
slide(f'''
<h3>Finances : saines mais contraintes — l'ère des cofinancements</h3>
<div class="cols2">
<div class="txt">
<p><b>Commune</b> : BP 2025 = 56,2 M€ (70 % fonctionnement) ; épargne nette 1,4 M€ (×2 vs 2024) ; dette 995 €/hab. (moyenne de strate) ; taux stables 8 ans — mais pression fiscale élevée (1 011 €/hab.) et investissement contenu (270 €/hab.).</p>
<p><b>Agglo 2026</b> : 242 M€ dont 68 M€ d'investissement ; épargne brute 18,4 % ; désendettement 6,3 ans ; budget « tagué climat » (I4CE) ; plan conchylicole 7,4 M€.</p>
<p><b>Fenêtres</b> : Action cœur de Ville (2025), politique de la ville « Quartiers 2030 », Plan Littoral 21, AAP friches Région — pendant que le Fonds vert national fond (2,5 Md€ → 0,83 Md€).</p>
<p class="hl">→ Chaque projet design doit être <b>« prêt à candidater »</b> : livrables rapides, preuve de valeur, phasage.</p>
</div>
<div>
<img class="tall" src="{F['fig5_frise_projets']}" alt="frise">
</div>
</div>''')

# 14 — scénarios
slide(f'''
<h3>Trois futurs possibles en 2040</h3>
<img class="tall" src="{F['figV4_scenarios_2040']}" alt="scénarios">
<p class="foot">Signaux à surveiller : cadence TER post-2034 · vitesse PLU/Mas de Chave · foncier & résidences secondaires · remplissage des équipements · abstention 2032 · jours de fermeture sanitaire de Thau</p>''')

# 15 — design
slide(f'''
<h3>Ce que le design peut faire — et quand</h3>
<div class="cols2">
<div>
<img src="{F['fig7_priorisation']}" alt="priorisation">
</div>
<div class="txt">
<p><b>2026-2027</b> : concertation outillée (friche · gare · Mas de Chave) · identité territoriale & signalétique · « kit transitions » chantiers · visualisation des cartes PPA · saison Muscat 90 ans.</p>
<p><b>2028-2030</b> : design du pôle gare/quartier · identité du centre aquatique · parcours muscat-polar-canal · premiers aménagements de la plage · tableau de bord « Frontignan 2030 ».</p>
<p><b>2032-2040</b> : mémoire & usages du quartier de la transition · recomposition Frontignan-Plage (PPA opérationnel) · services aux publics vieillissants · tourisme 4 saisons.</p>
<p class="hl">→ Priorité absolue : <b>masterplan co-construit friche/PEM</b> + continuités douces canal-cœur de ville-gare + identité (muscat · Thau · polar).</p>
</div>
</div>''')

# 16 — SWOT
slide(f'''
<h3>Synthèse stratégique (SWOT)</h3>
<img class="tall" src="{F['fig6_swot']}" alt="swot">''')

# 17 — parties prenantes
slide(f'''
<h3>Avec qui construire : la carte des parties prenantes</h3>
<img class="tall" src="{F['fig8_parties_prenantes']}" alt="parties prenantes">
<p class="foot">Dynamiques à surveiller : couple ville/agglo (exécutifs imbriqués) · relation Sète-Frontignan · clivage centre/Peyrade/plage · fatigue démocratique (abstention 38 %, RN 35,9 %)</p>''')

# 18 — conclusion
slide(f'''
<div class="hero-bg dim" style="background-image:url('{HERO_BG}')"></div>
<div class="title-box">
<h3>En résumé — Frontignan 2026-2040</h3>
<div class="txt left">
<p><b>Une fenêtre rare</b> : friche dépolluée (11 ha), gare actée (25 M€), label ACV, présidence de l'agglo, mandat frais — tout est engagé <em>avant</em> 2032.</p>
<p><b>Un horizon clair</b> : 2030 = la ville rééquipée ; 2034 = la bascule ferroviaire ; 2040 = le littoral recomposé.</p>
<p><b>Un rôle pour le design</b> : donner du sens (identité, mémoire), de la méthode (concertation, scénarios), de la qualité (espaces publics, pôle gare) et de la preuve (indicateurs, usages transitoires).</p>
</div>
<p class="sources">Sources & méthode : rapport d'analyse territoriale + vision 2026-2040 (annexes sources datées, 270+ références) · Figures générées à partir de données INSEE, agglopôle, Météo-France, SMBT, presse locale · Septembre 2026</p>
</div>''')

CSS = f'''
* {{ box-sizing:border-box; margin:0; }}
html {{ scroll-behavior:smooth; }}
body {{ background:linear-gradient(160deg,#eef3f4 0%,#e2eaec 100%); font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif; }}
.slide {{ position:relative; overflow:hidden; min-height:100vh; display:flex; flex-direction:column; justify-content:center;
  padding:56px 72px 68px; background:linear-gradient(160deg,#fbfefd 0%,#f2f6f7 100%); color:#1d2b30;
  border-bottom:1px solid #cdd8db; }}
.slide h3 {{ font-size:40px; color:{K}; margin-bottom:22px; border-bottom:5px solid {G}; padding-bottom:12px; line-height:1.15; }}
.slide p {{ font-size:19px; line-height:1.5; margin:8px 0; text-align:left; }}
.slide img {{ max-width:92%; max-height:70vh; margin:6px auto; border:1px solid #dde5e7; border-radius:8px;
  box-shadow:0 4px 22px rgba(15,76,92,.10); background:#fff; }}
.slide img.tall {{ max-height:74vh; }}
.foot {{ font-size:15px !important; color:#5a6a70; text-align:center !important; margin-top:10px; }}
.cols2 {{ display:flex; gap:36px; align-items:center; }}
.cols2 > div {{ flex:1; }}
.txt p {{ font-size:18px; }}
.txt .hl {{ background:#fdf6e7; border-left:5px solid {G}; padding:10px 14px; border-radius:0 6px 6px 0; font-size:18px; }}
.stats {{ display:flex; gap:18px; margin:14px 0 18px; flex-wrap:wrap; }}
.stat {{ flex:1; min-width:180px; background:{K}; color:#fff; border-radius:10px; padding:16px 18px; text-align:center; }}
.stat b {{ display:block; font-size:38px; color:#ffd98a; }}
.stat span {{ font-size:14.5px; line-height:1.3; display:block; margin-top:4px; }}
.hero-bg {{ position:absolute; inset:0; background-size:cover; background-position:center; }}
.hero-bg.dim {{ opacity:0.16; }}
.title-box {{ position:relative; text-align:center; max-width:1000px; margin:0 auto; }}
.kicker {{ color:{T}; font-weight:700; letter-spacing:2px; text-transform:uppercase; font-size:15px; margin-bottom:14px; }}
.title-box h1 {{ font-size:64px; color:{K}; line-height:1.05; }}
.title-box h2 {{ font-size:38px; color:{T}; margin:10px 0 18px; }}
.title-box h2 span {{ color:{G}; }}
.title-box p {{ font-size:19px; text-align:center; color:#33474e; }}
.badges {{ margin-top:20px; }}
.badges span {{ display:inline-block; background:{K}; color:#fff; border-radius:999px; padding:7px 16px; margin:4px; font-size:14.5px; }}
.txt.left {{ text-align:left; }}
.txt.left p {{ text-align:left; }}
.sources {{ font-size:13px !important; color:#6b7a7f; margin-top:26px; }}
#bar {{ position:fixed; top:0; left:0; height:5px; background:{G}; width:0; z-index:99; }}
#nav {{ position:fixed; bottom:14px; right:20px; background:{K}; color:#fff; border-radius:999px; padding:6px 14px; font-size:13px; z-index:99; }}
@media print {{
  html,body {{ background:#fff; }}
  .slide {{ min-height:0; width:297mm; height:167mm; page-break-after:always; }}
  #bar,#nav {{ display:none; }}
  .slide img {{ max-height:60vh; }}
}}
'''

html = f'''<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Frontignan la Peyrade 2026-2040 — présentation</title>
<style>{CSS}</style></head>
<body>
<div id="bar"></div>
{"".join(slides)}
<div id="nav">1 / {len(slides)}</div>
<script>
(function() {{
  var S = document.querySelectorAll('.slide');
  var bar = document.getElementById('bar'), nav = document.getElementById('nav');
  function cur() {{
    var y = window.scrollY + window.innerHeight / 2, k = 0;
    for (var j = 0; j < S.length; j++) {{ if (S[j].offsetTop <= y) k = j; }}
    return k;
  }}
  function update() {{
    var k = cur();
    bar.style.width = ((k + 1) / S.length * 100) + '%';
    nav.textContent = (k + 1) + ' / ' + S.length;
  }}
  window.addEventListener('scroll', update);
  window.addEventListener('resize', update);
  document.addEventListener('keydown', function(e) {{
    var k = cur(), t;
    if (['ArrowRight','ArrowDown','PageDown'].indexOf(e.key) >= 0) t = S[Math.min(k + 1, S.length - 1)];
    else if (['ArrowLeft','ArrowUp','PageUp'].indexOf(e.key) >= 0) t = S[Math.max(k - 1, 0)];
    else if (e.key === 'Home') t = S[0];
    else if (e.key === 'End') t = S[S.length - 1];
    if (t) {{ e.preventDefault(); t.scrollIntoView({{behavior:'smooth'}}); }}
  }});
  update();
}})();
</script>
<a href="atlas/index.html" style="position:fixed;right:18px;top:18px;z-index:999;background:#0F4C5Cdd;color:#fff;border:1px solid #C99A2E;border-radius:24px;padding:9px 16px;font:600 13px/1 system-ui,sans-serif;text-decoration:none;box-shadow:0 8px 24px rgba(0,0,0,.35)">🕸️ Atlas interactif — graphe, carte heuristique, données</a>
</body></html>'''

out = os.path.join(BASE, "index.html")
open(out, "w", encoding="utf-8").write(html)
print("OK :", out, "-", round(os.path.getsize(out) / 1024 / 1024, 2), "Mo,", len(slides), "slides")
