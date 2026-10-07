# S1 — Infra monorepo (app, scripts, data, docs)

**Mesuré** : 2026-10-07 · **Sources** : `app/main.py`, `app/templates/*`, `scripts/*`, `data/*`, `docs/*`, `MANIFEST.json`, `requirements.txt`
**Rôle** : c'est le **conteneur** : une app FastAPI de navigation + prévisualisation des 9 projets, un inventaire GitHub et de la documentation d'index.

## Faits

| Fait | Valeur | Preuve |
|---|---|---|
| `app/` | 6 fichiers, 41.6 Ko, **753 lignes** code | inventaire `S1-app` |
| `app/main.py` | 263 lignes — FastAPI : routes HTML, API GitHub, FS, preview | `wc -l app/main.py` |
| Templates | 4 HTML (`base`, `index`, `repos`, `monorepo`) | `app/templates/` |
| `scripts/` | 4 fichiers, 32 Ko, **708 lignes** | inventaire `S1-scripts` |
| `scripts/github_inventory.py` | inventaire GitHub stdlib, écrit `data/github_inventory.json` | en-tête du script |
| `scripts/publish_monorepo.sh` | rebuild des 3 previews Vite + commit + push | contenu du script |
| `data/github_inventory.json` | snapshot 9 dépôts (généré 2026-09-07) | JSON (`generated_at`) |
| `docs/` | 7 fichiers, 4.0 Mo, 737 lignes de code/doc | inventaire `S1-docs` |
| `docs/DOSSIER-CHANTIER-INDEX.md` | index des 220 documents (vérifié exact) | contrôle croisé P2.1 |
| `docs/GITHUB_INVENTORY.md` | synthèse de l'inventaire GitHub | fichier |
| `docs/synthese-talbot-2026/` | synthèse scientifique v4.2 (MD/HTML/DOCX + figure), 4.0 Mo | `README.md` du dossier |
| `requirements.txt` | `fastapi==0.110.0`, `uvicorn[standard]==0.29.0`, `jinja2==3.1.4`, `python-multipart==0.0.9` | fichier |
| `.gitignore` | ignore `node_modules`, `.env`, `.venv`, mais **force l'ajout de `projects/*/dist/**`** | fichier |
| Tests infra | **0** | inventaire `S1-app`, `S1-scripts` |
| TODO/FIXME infra | 8 (voir ci-dessous) | inventaire `S1-scripts` |

## Fonctionnalités réelles de l'app (vérifiées dans le code)

- `/` (accueil), `/repos` (panorama GitHub), `/monorepo` (explorateur + preview), `/health`.
- API : `/api/github/snapshot`, `/api/github/repos`, `/api/github/fusion`, `POST /api/github/refresh` (relance `scripts/github_inventory.py`), `/api/manifest`, `/api/fs/list`, `/api/fs/file`.
- `/preview/{project}/{path}` : sert les builds Vite (`dist/`), le learning de COGNITORIUM, les visuels d'ETAT-DE-LART (FileResponse, MIME dont `wasm`).
- Garde-fous : blocage traversal (`..` → 400), garde 2 Mo sur lecture texte, `POST /refresh` avec timeout 90 s.
- Le token GitHub est lu côté serveur (`GITHUB_TOKEN`/`GH_TOKEN`), jamais exposé au client (conforme au README).

## Constats

1. **Le snapshot GitHub local est périmé** (2026-09-07) alors que les dépôts ont bougé (cf. S3) — l'app affiche un panorama daté.
2. `detect_preview_entry()` ne couvre que des chemins figés : toute app sans `dist/index.html` (frontignan, HCSM, reaserch-engine, Language-decoder) n'a pas de preview (repli README).
3. `monorepo.bundle` est référencé (`/download/monorepo.bundle`, `.gitignore`) mais **absent** du dépôt.
4. Les previews committées (`projects/*/dist/`) sont des artefacts de build versionnés — pratique assumée par le README mais à risque de désynchronisation avec `src/`.
5. `docs/synthese-talbot-2026/` est un contenu **hors périmètre cognitif/chantier** : synthèse d'une session documentaire (Talbot 1991 vs état de l'art 2024-2026), archivée le 2026-10-07.
6. Aucun test, aucun lint, aucune CI pour l'app et les scripts (`S1` : tests = 0).

## Findings S1

| # | Sévérité | Catégorie | Constat | Preuve | Recommandation |
|---|---|---|---|---|---|
| F-S1-01 | moyen | C2 Dépôt, branches & synchronisation | snapshot GitHub du 2026-09-07 affiché comme « réel » dans l'app | `data/github_inventory.json:generated_at` | rafraîchir via `POST /api/github/refresh` et afficher la date |
| F-S1-02 | faible | C8 Tests & qualité | 0 test sur `app/`, 0 CI | inventaire | ajouter un test de fumée (routes, traversal) |
| F-S1-03 | info | C10 Exécution & déploiement | `monorepo.bundle` annoncé mais absent | `app/main.py` + `.gitignore` | générer ou retirer la route |
| F-S1-04 | faible | C7 Documentation & références | `docs/synthese-talbot-2026` non cité dans le README principal | `README.md` vs `docs/` | ajouter au sommaire |
