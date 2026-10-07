# 🍯 Frontignan la Peyrade — analyse territoriale & vision 2026-2040

Dossier d'appui pour l'accompagnement de la municipalité de Frontignan (Hérault, Sète Agglopôle Méditerranée) — septembre 2026.

## 📦 Contenu

| Fichier | Contenu |
|---|---|
| **`atlas/index.html`** | 🕸️ **Atlas interactif** — 4 modes : graphe de connaissance façon Obsidian, carte heuristique repliable, présentation en slides, explorateur de données. 79 nœuds (image + nom + texte), 167 liens typés, 17 jeux de données recalculés |
| **`index.html`** | 🎞️ **Deck de présentation** « Frontignan 2026→2040, focale 2030 » — 18 slides, autonome (images intégrées), scroll vertical, ← → au clavier, Ctrl+P → export PDF paysage |
| `vision-frontignan-2026-2040.md` | 🔮 **Vision prospective** macro/micro 2026→2040 (focale 2030) — source éditable |
| `vision-frontignan-2026-2040.html` | Même document, version consultation autonome (images base64) |
| `rapport-frontignan-analyse-territoriale.md` | 📊 **Rapport d'analyse territoriale** complet — entonnoir France→ville, 11 sections, 13 fiches projets, 249 sources |
| `rapport-frontignan-analyse-territoriale.html` | Version consultation autonome |
| `figures/` | 14 figures matplotlib (entonnoir, population, budget, frise projets, SWOT, priorisation, parties prenantes, mobilités, trajectoire 2026-2040, focus 2030, macro 2050, scénarios 2040, schéma territorial) |
| `visuals/` | 2 illustrations (vue isométrique « Frontignan 2030 », carte d'identité stylisée) |
| `atlas/data/` | `atlas.json` (graphe + statistiques, ~150 Ko) et `communes-thau.csv` (les 14 communes, export réutilisable) |
| `atlas/img/` | 10 visuels de nœuds (friche Mobil, gare/PEM, muscat, lagune de Thau, littoral, cœur de ville, port, gouvernance, Sète, Montpellier) |
| `scripts/` | Générateurs Python : `make_figures.py`, `make_figures_vision.py` (matplotlib), `make_html.py` (md→html autonome), `make_deck.py` (deck), `atlas_data.py` + `atlas_graph.py` + `build_atlas.py` (atlas) |

## 🔎 Points clés

- **Fenêtre rare 2026-2032** : friche Mobil (11 ha) dépolluée et restituée (27 mai 2026), gare/PEM 25 M€ acté, SCoT du bassin de Thau en approbation, présidence de l'agglo.
- **Focale 2030** : 5 conditions de succès (PEM livré *et desservi*, friche programmée *et financée*, +300-600 emplois, qualité de l'eau de Thau, mixité du centre).
- **3 scénarios 2040** : S1 « Thau tranquille » · S2 « Couronne métropolitaine » · S3 « Pôle de la transition » ★.
- **Méthode** : sources croisées et datées, balises ✅ engagé / 📅 annoncé / 🔮 tendance / ⚠️ incertain, estimations propres distinguées des prévisions officielles.

## 🕸️ L'atlas interactif

`atlas/index.html` — quatre lectures d'un même corpus, sans aucune dépendance externe (moteur de graphe et bibliothèque de graphiques écrits à la main, ~90 Ko de JS) :

| Mode | Raccourci | Ce qu'il fait |
|---|---|---|
| **Graphe** | `1` | Réseau force-directed façon Obsidian : nœuds à image + nom, halo et estompage des voisins au survol, glisser-déposer, zoom/pan, 3 dispositions (libre, anneaux par échelle, familles), filtres par échelle / type de nœud / type de lien |
| **Carte heuristique** | `2` | Arbre radial ou horizontal, repliable branche par branche ; clic = plier/déplier, double-clic = nouvelle racine, profondeur réglable |
| **Slides** | `3` | Déroulé de présentation (11 slides) avec graphiques vivants ; ← → pour naviguer, Ctrl+P pour l'export PDF |
| **Données** | `4` | Explorateur : 17 jeux de données, tableau triable des 14 communes, export CSV/JSON |

**Cinq échelles emboîtées** : Frontignan → la ville → l'agglo de Thau → les environs (Hérault, Montpellier, Occitanie) → la France.
**Neuf types de nœuds** (territoire, commune, acteur, projet, risque, politique publique, ressource, prospective, données) et **neuf types de liens** (gouverne, finance, dessert, coopère, tension, dépend de, exposé à, produit, compose).

Statistiques recalculées au build à partir des données sources : effectif, moyenne (simple et pondérée), médiane, écart-type, variance, coefficient de variation, étendue, quartiles, IQR, MAD, asymétrie, IC 95 %, z-scores, valeurs atypiques de Tukey, indice de Gini et courbe de Lorenz, corrélations de Pearson et Spearman avec régression (pente, R², test t).

`/` cherche un nœud, `Échap` ferme le panneau de détail.

## ▶️ Voir le deck

Ouvrir `index.html` dans un navigateur (fichier 100 % autonome, aucune connexion requise) — ou via le preview du monorepo : `/preview/frontignan/`. Un bouton en haut à droite du deck mène à l'atlas.

⚠️ L'atlas charge `data/atlas.json` en `fetch` : il doit être servi en HTTP (`/preview/frontignan/atlas/index.html` ou `python3 -m http.server` depuis `projects/frontignan`), pas ouvert en `file://`.

## 🛠 Régénérer

```bash
pip install matplotlib markdown pillow
cd projects/frontignan
python3 scripts/make_figures.py            # 9 figures du rapport -> figures/
python3 scripts/make_figures_vision.py     # 5 figures de la vision -> figures/
python3 scripts/make_html.py rapport-frontignan-analyse-territoriale   # md -> html autonome
python3 scripts/make_html.py vision-frontignan-2026-2040
python3 scripts/make_deck.py               # deck -> index.html
python3 scripts/build_atlas.py             # atlas -> atlas/data/atlas.json + communes-thau.csv
```

Le contenu de l'atlas se modifie dans deux fichiers seulement :
`scripts/atlas_data.py` (données brutes sourcées : communes, échelles, budgets, projets, acteurs, scénarios) et
`scripts/atlas_graph.py` (nœuds, liens, arborescence heuristique, scénario de slides). `build_atlas.py` recalcule
toutes les statistiques et réécrit le JSON.

### Servir l'atlas en local

```bash
cd projects/frontignan && python3 -m http.server 8000
# puis http://localhost:8000/atlas/index.html
```
