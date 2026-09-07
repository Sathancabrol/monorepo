# Inventaire GitHub — Sathancabrol (9 dépôts, 8 sources + monorepo)

Généré par `scripts/github_inventory.py` (stdlib, sans dépendance tierce).

## Résumé

- **Utilisateur** : `Sathancabrol`
- **Dépôts** : 9 au total (8 sources + `monorepo` lui-même)
- **Date** : voir `data/github_inventory.json:generated_at`
- **Mode** : snapshot JSON côté serveur (`data/github_inventory.json`) + refresh `POST /api/github/refresh` (token côté serveur uniquement).

## Liste

| Repo | Lang | Branches | Modules | Fichiers locaux |
|------|------|----------|---------|-----------------|
| animation-chronos | TypeScript | 1 | 1 (package.json) | 28 |
| COGNITORIUM | JavaScript | 4 | 1 | 131 |
| ETAT-DE-LART-PSYCHOLOGIE | HTML | 9 | 1 | 36 |
| HCSM | Python | 3 | 1 | 86 |
| Language-decoder | — | 3 | 1 | 1 |
| proto-cognitorium | TypeScript | 7 | 1 | 159 |
| reaserch-engine | Python | 1 | 1 | 60 |
| watchtower | JavaScript | 4 | 2 | 579 |
| monorepo | — | 1 | 0 | — |

*(monorepo exclu de la vue fusion — c'est le conteneur)*

## Définition de “module”

- Dossier contenant un manifeste : `package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`, `Cargo.toml`, etc.
- Détection auto langage/stack via GitHub `language` + `languages` + manifeste.
- Si aucun manifeste : dossier racine = module générique.

## Profondeur d'analyse

- **Branches** : toutes (via `/repos/{owner}/{repo}/branches`).
- **Commits** : 20 derniers sur la branche par défaut (prudent vs rate-limit).
- **Topics, size, description, updated_at, pushed_at** : inclus.

## Fusion / Cartographie

- **Type** : (a) agrégation visuelle + (c) simulation logique. Le code *est* aussi physiquement importé dans `projects/` (option b) mais sans tentative de résolution de conflits inter-projets : chaque repo garde ses dépendances/version/CI.
- **Graphe** : nœuds = dépôts (couleur langage), liens = dépendances partagées ≥2 (ex: `react`, `vite`, `tailwind`) ou lien explicite `COGNITORIUM → watchtower` (dossier `watchtower-mods`).
- **Révélations** : `animation-chronos` ↔ `proto-cognitorium` partagent socle React/Vite/Tailwind (17 deps communes), `vite` aussi dans `watchtower` ; `Language-decoder` quasi vide (1 fichier).

## Gestion erreurs

- Rate-limit : lecture `X-RateLimit-Remaining` / `Reset`, pause 0.15s entre repos.
- Repo privé sans accès : entrée absente (ou 404 si token insuffisant).
- Repo vide : module fallback `"."` + `file_count_local = 0`.
- Traversal `../..` dans l'explorateur : 400 bloqué côté API.

## Reproductibilité

```bash
GITHUB_TOKEN=ghp_xxx python scripts/github_inventory.py --user Sathancabrol --out data/github_inventory.json
# anonyme possible mais 60 req/h seulement
```

Le snapshot est servi via `GET /api/github/snapshot` (jamais d'appel direct API GitHub depuis le navigateur).

## Limites connues

- Pas d'analyse des forks/archivés filtrée (inclus si non-archivés ; à filtrer côté UI si besoin).
- Historique limité à 20 commits (configurable via `--per-page` dans le script).
- Détection modules profondeur 2 (évite `node_modules`).
