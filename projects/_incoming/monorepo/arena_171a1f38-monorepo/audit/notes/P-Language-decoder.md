# P — `Language-decoder`

**Audit** : fait (2026-10-07) · **Risque global** : **élevé** · **Maturité** : M0 `vide` sur `main` — **M2 `prototype` dans les branches**
**Résumé** : le dépôt le plus « invisible » : `main` = un README de **19 octets**, 1 commit (2026-08-30). Mais **deux branches poussées le 2026-10-07** contiennent un moteur Python complet (`language_decoder/`, 12 modules), une UI et des tests.

## C1 — Identité & provenance

| Fait | Valeur | Preuve |
|---|---|---|
| Dépôt | `Sathancabrol/Language-decoder`, public | `gh repo list` |
| Créé / dernier push | 2026-08-30 / **2026-10-07 06:17** (activité de branche) | idem |
| SHA `main` | `583f37ab` — « Initial commit » | `gh api` |
| Taille dépôt | 2.4 Mo (dont ~2.0 Mo sur la branche UI) | `gh repo list` |
| Licence | **aucune sur `main`** ; `CC-BY-4.0` déclarée dans `pyproject.toml` de la branche `01a05471` | `pyproject.toml` (branche) |
| Branches | 2 de travail | `branches.json` |

## C2 — Dépôt, branches & synchronisation

| Branche | Avance | Fichiers | Contenu |
|---|---:|---:|---|
| `arena/01a05429-language-decoder` | +7 | 27 (0.58 Mo) | pages + `docs/` (design, HUD, incertitude, mémoire, conversations) + `data/` (`memoire.json`, `monde-2040.json`, `ontology.json`) + 3 images HUD |
| `arena/01a05471-language-decoder` | +3 | 24 (2.02 Mo) | **Moteur Python** `language_decoder/` (12 modules : decoder 15 Ko, ontology 30 Ko, inference 15 Ko, dynamics, functioning, evidence, profile, cli, serve) + `ui/` (dashboard, 1.9 Mo de PNG) + `tests/test_engine.py` + `pyproject.toml` |
| `main` | — | **1** (19 o) | `# Language Decoder\n\nTODO` |

- Copie locale = `main` (1 fichier) : **100 % du projet est invisible dans le monorepo**.

## C3 — Structure & volumétrie (branche `01a05471`)

| Mesure | Valeur |
|---|---|
| Fichiers | 24 |
| Code Python | ~127 Ko de modules + 9.9 Ko de tests |
| UI | `index.html`, `app.js` (11.5 Ko), `styles.css` (18.8 Ko), `data/profile.json` (55 Ko) |
| Docs | `architecture.md`, `fondements.md` |
| Assets | 1 PNG 1.9 Mo (`hcsm_kei_dashboard.png`) |

## C4 — Stack & dépendances

- `pyproject.toml` : Python ≥ 3.10, setuptools ; `dev = ["pytest>=7"]` ; package `language_decoder` ; **tests « deterministic, stdlib-only »** (déclaré dans l'en-tête du fichier de test).
- Aucune dépendance runtime lourde — cohérent avec un moteur déterministe.

## C5 — Fonctionnalités & modules

D'après `pyproject.toml` (description) : « Moteur de décodage de l'humain : physique, mental, capacité d'action et fonctionnement, avec provenance et garde-fou épistémique ».
Modules : `ontology` (4 domaines, constructs), `decoder` (`decode_human`), `inference` (`InferenceEngine`), `evidence` (Observation, Provenance, TemporalWindow), `dynamics` (Retention, transferability), `functioning`, `profile`, `cli`, `serve` + schéma `decoded-human.schema.json`.
- **Convergence réelle avec `HCSM`** (vocabulaire : provenance, incertitude, fonctionnement, temporalité) — brique candidate pour la couche « Human » de la vision.

## C6 — Données & ressources

- `data/ontology.json`, `memoire.json`, `monde-2040.json`, `session-simulee.json` (branche docs) ; `ui/data/profile.json` 55 Ko ; image dashboard 1.9 Mo.
- 3 images HUD dans `docs/`.

## C7 — Documentation & références

- `docs/architecture.md`, `docs/fondements.md` (branche Python) ; `docs/` riche sur la branche docs (design visuel, HUD, hardware, incertitude, minimisation, format HTML, conversations datées 2026-08-30).

## C8 — Tests & qualité

- **1 fichier de test** (`tests/test_engine.py`, 9.9 Ko) sur la branche Python ; tests déclarés stdlib-only → exécutables sans installation. **Non exécutés dans cette session** (fichier distant, environnement local sans le package) — statut : `déclaré`.

## C9 — Sécurité & secrets

- Aucun secret détecté dans les branches inspectées. `ui/data/profile.json` = profil de démonstration (à vérifier avant publication : données personnelles ?).

## C10 — Exécution & déploiement

- `python -m language_decoder` / `cli.py` / `serve.py` (branche) ; UI statique dans `ui/`.
- `main` : rien à exécuter. Preview monorepo = README vide.

## C11 — Dette technique & risques

1. **Écart maximal du monorepo** : `main` vide vs 2 branches actives (poussées le jour de l'audit).
2. Licence CC-BY-4.0 seulement dans une branche (pas dans `main`) → statut légal flou du dépôt.
3. 72 % du poids de la branche UI = 1 PNG (1.9 Mo) ; `profile.json` 55 Ko dans `ui/data`.
4. Aucune PR ouverte : le travail n'a **pas de chemin de fusion** tracé.

## C12 — Maturité & complétude

**M0 `vide`** pour `main` → **M2 `prototype`** pour la branche `01a05471` (moteur + UI + tests, non fusionné).
**Prochaine étape** : PR de la branche moteur vers `main`, exécuter les tests, décider du lien avec `HCSM`.

## Findings

| # | Sévérité | Catégorie | Constat | Preuve | Recommandation |
|---|---|---|---|---|---|
| F-LD-01 | **critique** | C2 | `main` vide, projet réel sur 2 branches non fusionnées (poussées le 2026-10-07) | `gh api`, `branches.json` | ouvrir une PR, fusionner le moteur dans `main` |
| F-LD-02 | moyen | C1 | licence absente de `main` | `gh api` | rapatrier CC-BY-4.0 (ou choisir) |
| F-LD-03 | faible | C6 | PNG 1.9 Mo + `profile.json` 55 Ko dans Git | API arbre | compresser / externaliser |
| F-LD-04 | moyen | C5 | convergence non exploitée avec `HCSM` (vocabulaire commun) | comparaison docs | articuler les deux (HCSM = contrat) |
