# P — `ETAT-DE-LART-PSYCHOLOGIE`

**Audit** : fait (2026-10-07) · **Risque global** : **élevé** · **Maturité** : M2 `prototype` (local) / M3 potentiel (branches)
**Résumé** : base de connaissances critique 2020-2026 sur la psychologie cognitive + app FastAPI/SQLite + visualisations D3. **38 commits non fusionnés** (branche `arena/01a04f7b`) apportant un agent de recherche complet, `cosmos/` et 221 fichiers de sortie.

## C1 — Identité & provenance

| Fait | Valeur | Preuve |
|---|---|---|
| Dépôt | `Sathancabrol/ETAT-DE-LART-PSYCHOLOGIE`, public | `gh repo list` |
| Créé / dernier push | 2026-08-24 / 2026-09-07 | idem |
| SHA `main` réel | `258ddadf` — « Add files via upload » (2026-08-30) | `gh api` |
| Licence | **aucune** | `find` |
| Branches | **9** — 8 hors `main`, **4 avec du travail non fusionné** | `audit/data/branches.json` |

## C2 — Dépôt, branches & synchronisation

| Branche | Avance | Fichiers | Contenu (dernier commit) |
|---|---:|---:|---|
| `arena/01a04f7b-…` | **+38** | 300 modifiés / 1 818 dans l'arbre, 19.6 Mo | `fix: homepage noire + vues cassées` — apporte `agent/` (30 fichiers), `cosmos/` (24), `output/` (221) |
| `arena/01a07d32-…` | +5 | 46 | route `/download/monorepo.bundle` (secours push 403) |
| `arena/01a03aac-…` | +2 | 39 | « Cognitorium v8 — graphe 3D, 40 fiches concepts » |
| `arena/01a045a1-…` | +1 | 54 | « agent de recherche littéraire scientifique v1 » |
| 4 autres | 0 | — | mortes |

- Copie locale = `main` (37 fichiers, 0 écart) → **tout le travail des branches est invisible localement**.

## C3 — Structure & volumétrie (local, `main`)

| Mesure | Valeur |
|---|---|
| Fichiers / taille | 37 / 3.6 Mo |
| LOC-code / données-doc | 2 569 / 2 683 |
| Docs | 20 fichiers Markdown |
| `output/` | CSV consolidés, tableaux, mermaid, `visual/` (D3 interactif, graphe taxonomique, images) |

## C4 — Stack & dépendances

- Backend `app/` : **FastAPI + SQLite** (`app/database.py`, `app/main.py`) — premier backend persistant de l'écosystème.
- `scripts/` : `add_entry.py`, `validate_entry.py` (ajout/validation par DOI, Crossref).
- Front : HTML/JS + D3 (visualisations dans `output/visual/`), PPTX de présentation.

## C5 — Fonctionnalités & modules

| Brique | État local | État branche |
|---|---|---|
| Base CSV 42 champs (`data/nodes_etat_art_psychologie.csv`) | oui | enrichie |
| App FastAPI + templates | oui | corrigée (bug homepage noire) |
| Scripts DOI (ajout + validation) | oui | — |
| Graphes D3 (interactif, taxonomie) | oui | v8 graphe 3D + 40 fiches |
| **Agent de recherche littéraire** (`agent/`) | non | **oui (+38)** : core agent/planner/registry/context/llm + fixtures Crossref/OpenAlex |
| `cosmos/` (visualisation ?) | non | oui (24 fichiers) |
| Sorties étendues (`output/` 221 fichiers) | non | oui |

## C6 — Données & ressources

- `data/` CSV (42 champs, Trust Factor), `output/` CSV/MD/PNG, `Cognition_Distribuee_2025.pptx`, 2 images. Aucune donnée personnelle sensible identifiée.

## C7 — Documentation & références

- 20 docs dont : `ETAT_ART_CRITIQUE_PSYCHOLOGIE_2020_2026_CORRIGE.md` (état de l'art sourcé), `TAXONOMIE_PSYCHOLOGIE_COGNITIVE.md`, `SEARCH_STRATEGIES.md`, `PRISMA_FLOW.md`, `ARCHITECTURE_BASE_DE_DONNEES.md`, `GUIDE_REMPLISSAGE_IA.md`, `INDEX_PROJET.md`, `ANALYSE_CONCEPTS_COGNITORIUM_4E.md`, `METACOGNITION_EDUCATION_2025_2026.md`, `TEMPLATE_CHAMPS.csv`.
- Méthodologie de revue documentée (PRISMA, stratégies de recherche) — **la plus rigoureuse des bases de connaissances du dépôt**.

## C8 — Tests & qualité

- **0 test** dans `main` et dans les branches inspectées. Scripts de validation de données (`validate_entry.py`) = garde-fou partiel.

## C9 — Sécurité & secrets

- Aucun secret. L'agent (branche) prévoit un `llm.py` — à surveiller lors de la fusion (clé API à externaliser).

## C10 — Exécution & déploiement

- App FastAPI lançable localement (uvicorn) ; preview monorepo = `output/visual/index.html`. Dépendances Python non déclarées (pas de `requirements.txt`).

## C11 — Dette technique & risques

1. **Perte de valeur la plus élevée du dépôt** : 38 commits (agent complet + 221 sorties + cosmos) jamais fusionnés ni testés.
2. `main` est un « Add files via upload » : pas d'historique de conception.
3. Pas de `requirements.txt`, pas de tests, pas de CI.
4. Trois bases de connaissances parallèles (ici, `proto`, `HCSM`) → doublon documenté (ADR-009 ouverte).

## C12 — Maturité & complétude

**M2 `prototype`** pour `main` (base + app + viz) ; les branches atteignent un périmètre M3.
**Prochaine étape** : **fusionner `arena/01a04f7b`** (priorité n°1 de l'audit), ajouter `requirements.txt` + tests.

## Findings

| # | Sévérité | Catégorie | Constat | Preuve | Recommandation |
|---|---|---|---|---|---|
| F-EL-01 | **critique** | C2 | +38 commits non fusionnés (agent, cosmos, 221 sorties) | `branches.json` | fusionner sous 7 jours |
| F-EL-02 | élevé | C4/C8 | pas de `requirements.txt`, 0 test | inspection | les ajouter à la fusion |
| F-EL-03 | moyen | C7 | doublon de base de connaissances avec `proto`/`HCSM` | doc synthèse COGNITORIUM | trancher ADR-009 (HCSM = vocabulaire) |
| F-EL-04 | faible | C2 | 4 branches mortes | `branches.json` | supprimer |
