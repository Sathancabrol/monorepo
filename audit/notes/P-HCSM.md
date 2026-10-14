# P — `HCSM` (Human Cognitive State Model)

**Audit** : fait (2026-10-07) · **Risque global** : faible · **Maturité** : M2 `prototype` (spécification + validateur exécutable)
**Résumé** : cadre scientifique + ontologie + **validateur exécutable** (contrat V1 forme / V5 admissibilité). Le seul projet avec licence et citation. Statut déclaré : `PROPOSED` v0.1.1.

## C1 — Identité & provenance

| Fait | Valeur | Preuve |
|---|---|---|
| Dépôt | `Sathancabrol/HCSM`, public | `gh repo list` |
| Créé / dernier push | 2026-08-25 / 2026-08-25 | idem |
| SHA `main` | `c8fe0e3f` | `gh api` |
| Version / statut | **0.1.1** / `PROPOSED` | `README.md` |
| Licence | **`LICENSE` présente** + `CITATION.cff` | fichiers |
| Branches | 3 : `main` + 2 mortes (0 commit d'avance) | `audit/data/branches.json` |

## C2 — Dépôt, branches & synchronisation

- **Copie locale = `main`** : 87 fichiers des deux côtés, 0 écart.
- 2 branches mortes (`arena/01a03a6b`, `arena/01a03a93`) — rien à récupérer, **supprimables**.

## C3 — Structure & volumétrie

| Mesure | Valeur |
|---|---|
| Fichiers / taille | 87 / 273 Ko |
| LOC-code / données-doc | 1 917 (dont validateur) / 3 256 |
| Docs | 52 fichiers Markdown |
| Cas de test | 24 JSON (`validator/cases/valid`, `invalid`) |

## C4 — Stack & dépendances

- Python ≥ 3.10 + **PyYAML** (`validator/requirements.txt`).
- Ontologie en YAML (`ontology/hcsm-v0.1.yaml`) ; schémas JSON.
- Aucun framework lourd — choix cohérent avec un dépôt de spécification.

## C5 — Fonctionnalités & modules

| Module | Contenu |
|---|---|
| `docs/` | 15 documents structurants (00 overview → 14 limitations) : position scientifique, état de l'art, gap, modèle conceptuel, ontologie, évidence, inférence, temporalité, incertitude & provenance, contexte, fonctionnement, validation, protocole, limites |
| `ontology/` | entités, relations, namespaces, `hcsm-v0.1.yaml` |
| `model/` | 4 modèles (latent, mathématique, temporel, incertitude) |
| `scientific/` | constructs, hypotheses, literature, measures (`measure-catalog.md`), models |
| `specs/` | api-concept, data-schema, implementation-roadmap |
| `validator/` | **V1 (forme) + V5 (admissibilité)** — décide ADMIT / Refusal avant toute estimation |
| `figures/` | 6 figures conceptuelles (md) |
| `papers/`, `research/` | working paper, références ; competing-models, novelty-matrix, open-questions, scientific-audit |

## C6 — Données & ressources

- 24 fichiers de données : cas valides/invalides JSON (mini-scénarios, refus, bundles), YAML d'ontologie. Aucune donnée personnelle.

## C7 — Documentation & références

- 52 docs, README auto-explicatif (« ce que HCSM est et n'est pas »), `CITATION.cff`, `CONTRIBUTING.md`, `CHANGELOG.md`, `LICENSE`.
- Positionnement explicite vs RDoC / ICF / Cognitive Atlas / HPO (sources citées).

## C8 — Tests & qualité

- **Vérifié le 2026-10-07** (venv jetable, `pytest`) : `29 passed` sur `validator/tests`.
- **Vérifié** : `python validate.py --all` → **23/23 cas passent** (valid + invalid + bundles).
- Pas de CI.

## C9 — Sécurité & secrets

- Aucun secret, aucun `.env`, aucune donnée personnelle. Cas de test = données synthétiques.

## C10 — Exécution & déploiement

```bash
cd validator && python -m venv .venv && pip install -r requirements.txt
python validate.py --all            # 23/23
python -m pytest tests -q           # 29 passed
```

- Reproductible et documenté ; aucune dépendance système.

## C11 — Dette technique & risques

1. **Écart spécification ↔ implémentation** : le validateur est la seule brique exécutable ; « Cognition Hub » (le système qui instancie HCSM) n'existe pas (assumé v0.1).
2. Statut `PROPOSED` : l'ontologie n'est un standard pour personne tant qu'un consommateur ne l'utilise pas (`proto`, `intelTwin`).
3. Branches mortes à nettoyer.

## C12 — Maturité & complétude

**M2 `prototype`** — spécification de qualité publication + validateur testé ; pas de produit, pas de consommateur intégré.
**Prochaine étape** : brancher le validateur sur les sorties « cognitives » du proto et d'`intelTwin` (recommandation déjà présente dans `COGNITORIUM/docs/etat-des-lieux/09-synthese.md`).

## Findings

| # | Sévérité | Catégorie | Constat | Preuve | Recommandation |
|---|---|---|---|---|---|
| F-HC-01 | moyen | C5 | aucun consommateur du contrat HCSM (proto/intelTwin non branchés) | docs synthèse + inspection | brancher le validateur en amont de toute sortie cognitive |
| F-HC-02 | faible | C2 | 2 branches mortes | `branches.json` | supprimer |
| F-HC-03 | info | C1 | dernier push 2026-08-25 : projet dormant depuis 6 semaines | `gh api` | décider : réactiver ou laisser en veille |
