# P — `reaserch-engine` (Research Engine)

**Audit** : fait (2026-10-07) · **Risque global** : moyen · **Maturité** : M2 `prototype` (moteur réel, 2 tests en échec)
**Résumé** : moteur de recherche autonome v0.1 (question → dossier sourcé). 22 modules, 12 fichiers de test, 9 schémas JSON. **Seul projet sans perte de travail dans les branches** ; **2 tests échouent** (vérifié).

## C1 — Identité & provenance

| Fait | Valeur | Preuve |
|---|---|---|
| Dépôt | `Sathancabrol/reaserch-engine`, public — **nom mal orthographié** (« reaserch »), conservé tel quel | `gh repo list` |
| Créé / dernier push | 2026-08-26 / **2026-08-27** (dormant) | idem |
| SHA `main` | `ed4640d1` — « Document canonical epistemic research model » | `gh api` |
| Licence | **aucune** | `find` |
| Branches | **1 seule** (`main`) — aucun travail orphelin | `audit/data/branches.json` |

## C2 — Dépôt, branches & synchronisation

- Copie locale = `main` : 61 fichiers des deux côtés, 0 écart, 0 branche de travail. **Le projet le plus « propre » du point de vue Git.**

## C3 — Structure & volumétrie

| Mesure | Valeur |
|---|---|
| Fichiers / taille | 61 / 131 Ko |
| LOC-code / données-doc | 1 167 / 1 801 |
| `engine/` | 22 modules Python |
| `schemas/` | 9 schémas JSON (claim, conclusion, contradiction, evidence, research-action, research-run, source, sufficiency-decision, verification-report) |
| `tests/` | 12 fichiers |
| `docs/` | 16 documents |

## C4 — Stack & dépendances

- Python (stdlib en majorité) + `requests` pour Crossref ; **aucun manifeste** (`requirements.txt`/`pyproject.toml` absents) → installation implicite.

## C5 — Fonctionnalités & modules

- Pipeline : analyse de question → planification → stratégie adaptative → agents/outils → preuves & claims → contradictions → synthèse → vérification → suffisance/arrêt → dossier final.
- Modules clés : `orchestrator.py`, `state_machine.py`, `research_state.py`, `planner.py`, `research_strategy.py`, `question_analyzer.py`, `evidence_graph.py`, `claims.py`, `graph_assessment.py`, `source_quality.py`, `sufficiency.py`, `persistence.py` (`JsonRunStore` atomique), `providers.py`, `retrieval.py`.
- Sortie : dossier de recherche structuré (`dossier.py`, `research-output-spec-v0.1.md`).

## C6 — Données & ressources

- `engine/fixtures` + schémas + runs JSON. Pas de données lourdes. `tests/` : fixtures Crossref/OpenAlex sur la branche ETAT-DE-LART (agent associé).

## C7 — Documentation & références

- 16 docs : architecture (2), evidence-graph, graph-assessment, mindmap-synthesis, persistence, product-requirements, research-dossier, research-lifecycle, research-model, research-output-spec, research-protocol, academic-retrieval, glossary, ARCHITECTURE_HERMES_INTEGRATION (intégration prévue avec Hermes).
- Modèle épistémique documenté (« Document canonical epistemic research model »).

## C8 — Tests & qualité

**Vérifié le 2026-10-07** (venv jetable, `pytest`) :

```
2 failed, 17 passed in 0.08s
FAILED tests/test_agents.py::test_researcher_uses_injected_retriever        → IndexError: list index out of range
FAILED tests/test_research_strategy.py::test_contradictions_are_prioritized  → assert 'search' == 'investigate_contradiction'
```

- Aucune CI, aucun lint configuré.

## C9 — Sécurité & secrets

- Aucun secret, aucun `.env`, aucune donnée personnelle. Appels réseau limités à Crossref/web (agents).

## C10 — Exécution & déploiement

- Pas de script d'entrée (`__main__` absent ?) — utilisation par import/orchestrateur ; dépend de l'environnement Python local.
- Aucun build, aucune preview (le monorepo affiche le README).

## C11 — Dette technique & risques

1. **2 tests rouges** (agents, stratégie de contradictions) — touchent le cœur méthodologique.
2. Aucun manifeste de dépendances → non installable de façon reproductible.
3. Projet dormant depuis le 2026-08-27 ; l'appelant prévu (Hermes / Cognitorium) n'est pas branché.
4. Nom du dépôt erroné (fossile de création) — coût de recherche/navigation.

## C12 — Maturité & complétude

**M2 `prototype`** — moteur exécutable et testé à 89 %, sans interface ni persistance partagée.
**Prochaine étape** : corriger les 2 tests, ajouter `pyproject.toml`, brancher au proto/`HCSM` comme couche preuve.

## Findings

| # | Sévérité | Catégorie | Constat | Preuve | Recommandation |
|---|---|---|---|---|---|
| F-RE-01 | élevé | C8 | 2 tests du cœur en échec depuis ≥ 6 semaines | `pytest` 2026-10-07 | corriger (agents, contradictions) |
| F-RE-02 | moyen | C4 | aucun manifeste de dépendances | `ls` | `pyproject.toml` + lock |
| F-RE-03 | faible | C1 | nom du dépôt mal orthographié | `gh repo list` | renommer (redirection GitHub) ou documenter |
| F-RE-04 | moyen | C11 | aucun consommateur (HCSM/proto/Cognitorium non branchés) | docs de synthèse | brancher comme couche « preuve » |
