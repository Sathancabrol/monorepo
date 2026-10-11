# Sathancabrol — Monorepo unifié

> **Un seul dépôt, 8 projets, navigation + previews intégrées.** Agrégation visuelle et cartographie logique sans casser les projets individuels. Token GitHub côté serveur uniquement (jamais exposé au client).

## 🗂 Structure

```
monorepo/
├─ projects/
│  ├─ animation-chronos/        Vite + React (dist/ buildée, base=./)
│  ├─ proto-cognitorium/        Vite + React + server.ts (dist/ buildée)
│  ├─ watchtower/               Vite + Cesium (dist/ buildée, 3D globe)
│  ├─ COGNITORIUM/              learning/ + watchtower-mods/ (statique)
│  ├─ ETAT-DE-LART-PSYCHOLOGIE/ app/ FastAPI + output/visual/*.html
│  ├─ HCSM/                     Python (ontology, model)
│  ├─ reaserch-engine/          Python (engine/)
│  ├─ Language-decoder/         README (quasi vide)
│  └─ frontignan/               Analyse territoriale + vision 2026-2040 (deck) + module climat el-nino-thau.html + console territoriale atlas.html
├─ app/                         FastAPI + Jinja (interface unifiée)
│  ├─ main.py                   API + preview server + explorer
│  └─ templates/                base, index, repos, monorepo (drawer + iframe)
├─ data/climat/                 🌊 Datasets climat canoniques : el-nino-2026 (El Niño × Thau) + frontignan-episodes-cevenols (blocages cévenols)
├─ data/atlas-frontignan/       🗺 Spec canonique de la console territoriale Atlas (Phase 0, schéma atlas-frontignan-v1)
├─ scripts/github_inventory.py  Inventaire GitHub (stdlib, 62 appels max, snapshot JSON)
├─ scripts/validate_climat_data.py + build_climat_assets.py   Validation & génération des modules climat
├─ scripts/validate_atlas_spec.py + build_atlas_assets.py     Validation & génération de la console Atlas
├─ data/github_inventory.json   Snapshot (cache serveur, refresh via POST)
├─ MANIFEST.json                Provenance (URL, branche, SHA)
└─ requirements.txt             fastapi, uvicorn, jinja2
```

## 🚀 Lancer en local

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8123 --reload
# → http://localhost:8123
# → http://localhost:8123/monorepo  (explorer + preview navigable)
# → http://localhost:8123/repos     (panorama GitHub + graphe fusion)
```

## 🔍 Panorama GitHub

- **Page `/repos`** : cartes des 8 dépôts, graphe de fusion (D3), hiérarchie `repo > branches > modules`, drawer détails (commits, fichiers, dépendances).
- **API** : `GET /api/github/snapshot` · `/api/github/repos` · `/api/github/fusion` · `POST /api/github/refresh` (régénère le snapshot côté serveur, token jamais exposé).
- **Inventaire** : `scripts/github_inventory.py` (stdlib uniquement, paginate, rate-limit). Stocke `data/github_inventory.json` → sert de cache, pas d'appel direct API depuis le navigateur.
- **Module** = dossier à manifeste (`package.json`, `pyproject.toml`, `go.mod`, …) + détection langage/stack auto.
- **Fusion** = agrégation visuelle + cartographie logique (dépendances communes, liens explicites `COGNITORIUM → watchtower` via `watchtower-mods`). Option (b) monorepo réel = déjà fait via `projects/` ; aucun conflit de dépendances car chaque projet garde son lockfile.

## 🧭 Monorepo + Preview navigable (`/monorepo`)

- **Explorateur** à gauche : onglets projets, fil d'Ariane, filtre, liste fichiers (traversal `../..` bloqué 400, MIME correct dont `wasm`).
- **Viewer** : rendu Markdown, syntaxe colorée, images, PDF en iframe, `README` cliquable.
- **Preview** en iframe same-origin :
  - `← / → / ⌂ / ⟳` + barre d'adresse synchronisée avec tes clics *dans* la preview (interception `a[href]` même origine)
  - sélecteur d'entrée, bouton ↗ nouvel onglet
- **Entrées par projet** :
  - `watchtower` → `dist/index.html` (Cesium globe, build Vite `--base=./`)
  - `animation-chronos` → `dist/index.html`
  - `proto-cognitorium` → `dist/index.html` (frontend statique ; `server.ts` Express non exécuté dans l'iframe)
  - `COGNITORIUM` → `learning/index.html` (+ PoC `el-nino-poc.html`) + `watchtower-mods/`
  - `ETAT-…` → `output/visual/index.html` + `d3_interactive.html` + `taxonomy_graph.html`
  - `HCSM` / `reaserch-engine` / `Language-decoder` → code seul + README
  - `frontignan` → `index.html` (deck 19 slides) + **module climat `el-nino-thau.html`** + **console territoriale `atlas.html`**

## 🌊 Données climat — El Niño 2026–2027 « Godzilla » × bassin de Thau

Un **dataset canonique** (`data/climat/el-nino-2026/`) enrichit les modules pertinents du monorepo : observations & projections de l'épisode (vidéo LIMIT « EL NIÑO : GODZILLA » du 11/10/2026 avec Xavier Fettweis, errata 24/09 intégré) + frise opérationnelle golfe du Lion / Thau Agglo (oct. 2026 → déc. 2027). Chaque élément porte un **statut** (`observe` / `prevu` / `incertain`) et une **attribution** — El Niño n'est pas coupable de tout.

Le dataset complémentaire **`data/climat/frontignan-episodes-cevenols/`** (schéma `territorial-risk-v1`) capture le diagnostic « Frontignan face aux épisodes cévenols » : 5 points bloquants (Gardiole→centre-ville, saturation des réseaux, littoral/étang, déplacements & secours, pollutions secondaires), 7 solutions P1/P2/P3 (PAPI Thau 2026–2031 : 46 actions, 25 communes, ≈ 6,8 M€), 4 modules Atlas opportuns et la feuille de route de l'étude pilote Gardiole → centre-ville (4/5).

| Consommateur | Artefact | Accès |
|---|---|---|
| **frontignan** (Atlas) | `projects/frontignan/el-nino-thau.html` — module interactif 9 onglets : vue d'ensemble, frise filtrable (horizon × risque), faits globaux, risques & scénarios, **épisodes cévenols (blocages & solutions)**, simulation canvas, quiz, checklist, sources | `/preview/frontignan/el-nino-thau.html` (aussi lié depuis la slide 18 du deck) |
| **COGNITORIUM** (learning) | `projects/COGNITORIUM/learning/el-nino-poc.html` — PoC « Comprendre El Niño » (10 niveaux, concept graph, transfert) | `/preview/COGNITORIUM/learning/el-nino-poc.html` |
| **watchtower** (globe) | `projects/watchtower/public/data/enso-thau-watchpoints.geojson` — 15 watchpoints (6 Thau + 9 mondiaux) + boîte Niño 3.4 ; `frontignan-cevenols-watchpoints.geojson` — 6 zones de blocage cévenols | glisser-déposer sur le globe (import GeoJSON natif) |
| **API** | endpoints climat | `GET /api/climat/datasets` · `GET /api/climat/el-nino-godzilla-2026` · `GET /api/climat/frontignan-cevenols-2026` · `GET /api/climat/{dataset}/{section}` (`thau`, `blocking_points`, `solutions`, `geo`…) |

Gouvernance : le JSON canonique est la seule source de vérité ; les artefacts modules sont **générés** (`python3 scripts/build_climat_assets.py`) et validés (`python3 scripts/validate_climat_data.py`). Les sources brutes (script de tournage, synthèse, frise) sont archivées dans `data/climat/el-nino-2026/sources/`.

## 🗺 Atlas Frontignan — console territoriale (Phase 0 : coquille jouable)

**Atlas n'est pas un logiciel d'inondation** : c'est une console de décision territoriale multi-thématiques, inspirée des interfaces 4X (Civilization : lentilles de vue, arbre technologique, yields), branchée sur le territoire réel. L'inondation n'y est qu'une branche — le fil rouge prioritaire relie pentes → écoulement → réseau pluvial → risque → moyens de sauvetage. Méthode : **tout déclarer d'abord en placeholder navigable** (statuts `EMPTY → SHELL → DATA → LIVE → SIM`), puis remplir par urgence (Phase 1 : IGN/PPRI/plan des réseaux ; Phase 3 : vraies simulations).

La spec canonique `data/atlas-frontignan/atlas-frontignan-2026.json` (schéma `atlas-frontignan-v1`) déclare : **14 lentilles**, **7 modules / 35 sous-modules**, **15 actions**, **9 indicateurs**, **43 objets carte** — dont 6 zones branchées en **DATA** sur le dataset cévenols et les watchpoints climat Thau (El Niño), mêmes sources de vérité que le module climat.

| Élément | Contenu |
|---|---|
| **Console** `projects/frontignan/atlas.html` (généré) | carte stylisée + lentilles + inspecteur (fiches & blocages DATA) + modules + arbre d'actions + scénario avant/après (placeholders assumés, jamais présentés comme estimations) + phases + méthode | 
| **Accès** | `/preview/frontignan/atlas.html` — fil rouge guidé « ▶ pentes → secours », touches 1–9, overlays météo/alertes/chantiers |
| **Liens croisés** | console → module climat (`el-nino-thau.html#cevenols`, `#sim`) ; module climat → console (carte « Réutilisation ») |
| **Gouvernance** | `python3 scripts/validate_atlas_spec.py` · `python3 scripts/build_atlas_assets.py` — artefact généré, ne pas éditer à la main |
  - Servie via `GET /preview/{project}/{path}` (FileResponse, pas de `X-Frame-Options` côté monorepo ; `watchtower` buildée sans en-têtes DENY).

## 🛠 Rebuild des previews Vite

Les 3 apps sont déjà buildées (`--base=./` → assets relatifs) :

```bash
for p in animation-chronos proto-cognitorium watchtower; do
  (cd projects/$p && npm ci && npx vite build --base=./)
done
```

Si une preview reste blanche, ouvre-la en nouvel onglet (bouton ↗) pour voir l'erreur console.

## 🔐 Sécurité

- Token GitHub lu depuis `GITHUB_TOKEN` / `GH_TOKEN` env côté serveur uniquement, jamais envoyé au client.
- Gestion erreurs : rate-limit (headers `X-RateLimit-Remaining`), repo privé sans accès → 404 propre, repo vide → module fallback, traversal bloqué 400.

## 📦 Publier vers GitHub

Ce dépôt **est** `Sathancabrol/monorepo` (branche `main`). Pour pousser :

```bash
git remote add origin https://github.com/Sathancabrol/monorepo.git  # déjà configuré
git push -u origin arena/01a07e3c-monorepo   # cette branche
# ou merger vers main après review
```

Si push 403 → vérifier dans GitHub → Settings → Applications → Installed GitHub Apps → Arena → Repository access : ajouter `monorepo` (ou passer en All repositories), puis reconnecter Arena pour régénérer le token.

## 📚 Fusion réelle (option b)

Le code est déjà importé dans `projects/` (129 Mo, 1090 fichiers). Chaque projet reste autonome (son `package.json` / `requirements.txt` inchangé). La vue `fusion` ne copie pas le code, elle cartographie les interactions ; l'import physique est lui déjà réalisé pour navigation unifiée.
