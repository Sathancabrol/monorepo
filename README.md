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
│  └─ frontignan/               Analyse territoriale + vision 2026-2040 (deck : index.html)
├─ app/                         FastAPI + Jinja (interface unifiée)
│  ├─ main.py                   API + preview server + explorer + montage de NEXUS·OS sous /os
│  └─ templates/                base, index, repos, monorepo (drawer + iframe)
├─ nexus_os/                    ⬢ NEXUS·OS — agentic OS (routeur + agents + créateur)
│  ├─ providers.py llm.py       routeur multi-fournisseurs + repli hors-ligne
│  ├─ runtime.py agents.py      boucle par phases, délégation, 10 agents spécialisés
│  ├─ creator.py skills.py      créateur d'agent + 14 compétences SKILL.md
│  ├─ tools.py memory.py db.py  14 outils sandboxés, mémoire, SQLite
│  ├─ app.py templates/ static/ API JSON + SSE + bureau web
│  └─ tests/                    59 tests pytest
├─ scripts/github_inventory.py  Inventaire GitHub (stdlib, 62 appels max, snapshot JSON)
├─ data/github_inventory.json   Snapshot (cache serveur, refresh via POST)
├─ MANIFEST.json                Provenance (URL, branche, SHA)
└─ requirements.txt             fastapi, uvicorn, jinja2
```

## 🚀 Lancer en local

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt          # ou requirements-dev.txt (avec pytest + httpx)
uvicorn app.main:app --host 0.0.0.0 --port 8123 --reload
# → http://localhost:8123
# → http://localhost:8123/monorepo  (explorer + preview navigable)
# → http://localhost:8123/repos     (panorama GitHub + graphe fusion)
# → http://localhost:8123/os/       (⬢ NEXUS·OS — agentic OS)
```

## ⬢ NEXUS·OS — agentic OS (`/os/`)

Un système d'exploitation pour agents IA, monté dans l'interface unifiée (ou
lançable seul : `uvicorn nexus_os.app:app --port 8124`). Détails :
[`nexus_os/README.md`](nexus_os/README.md).

- **Routeur de modèles** (façon OmniRoute) : 8 fournisseurs, 20 modèles, un seul
  point d'entrée, sélection par quota du jour + coût, **bascule automatique** en
  cas d'erreur, repli sur un moteur local → l'OS tourne avec ou sans clé API.
- **10 agents spécialisés** : 🧭 orchestrateur, 🔎 chercheur, 🛠️ ingénieur,
  ✍️ rédacteur, 📐 architecte, 📊 analyste, 🛡️ revendeur, 🌐 pilote, 🎯 coach,
  🧬 créateur. L'orchestrateur route automatiquement vers le bon spécialiste.
- **Créateur d'agent intégré** : une description → prompt système, compétences,
  outils, triggers, cycle de vie. Un agent peut même en créer un autre (outil
  `create_agent`).
- **14 compétences `SKILL.md`** (recherche, code, tests, revue, sécurité,
  copywriting, SEO, diagrammes, données, navigateur, HTML, sortie ADHD,
  mémoire, conception d'agent) — les tiennes se posent dans `.nexus/skills/`.
- **Cycle de vie** (façon ECC) : plan → recherche → implémentation → revue →
  vérification → mémorisation → amélioration, avec outils réellement exécutés.
- **Sandbox** : les agents n'écrivent que dans `.nexus/workspace/`, les secrets
  sont illisibles, `shell`/`python_exec` sont désactivés par défaut.

```bash
python -m nexus_os status                                   # état du système
python -m nexus_os route "rédige une landing page"          # qui doit traiter ?
python -m nexus_os run "audite la structure du dépôt"       # exécute (streaming)
python -m nexus_os create "un agent qui relit les contrats" # crée un agent
.venv/bin/python -m pytest nexus_os/tests -q                # 59 tests
```

## 🧪 Tests

```bash
pip install -r requirements-dev.txt
python -m pytest nexus_os/tests -q        # 59 tests : routeur, skills, sandbox,
                                          # créateur, runtime, SSE, montage /os
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
    - `COGNITORIUM` → `learning/index.html` + `watchtower-mods/`
    - `ETAT-…` → `output/visual/index.html` + `d3_interactive.html` + `taxonomy_graph.html`
    - `HCSM` / `reaserch-engine` / `Language-decoder` → code seul + README
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
