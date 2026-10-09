# MEMORY — Audit monorepo (index généré)

> **NE PAS ÉDITER À LA MAIN** — généré par `python3 scripts/audit_memory.py render`
> depuis `audit/state.json`. Mis à jour : 2026-10-09T12:45:35Z

## Où est quoi

| Fichier | Rôle |
|---|---|
| `audit/PLAN.md` | plan de processus, périmètre, méthode |
| `audit/CATEGORIES.md` | taxonomie canonique (noms de catégories + règles) |
| `audit/state.json` | **source de vérité machine** (statuts, faits, actions) |
| `audit/JOURNAL.jsonl` | journal append-only des itérations |
| `audit/notes/*.md` | notes factuelles par périmètre |
| `audit/graph.json` | graphe de connaissances (projets ↔ docs ↔ dépendances) |
| `audit/AUDIT-2026-10.md` | livrable final (tableaux) |

## État courant

- Audit : `audit-2026-10` — Audit complet monorepo Sathancabrol
- Phase courante : **P7 (audit terminé) — **
- Compteurs : {"findings": 52, "fichiers_locaux_mesures": 1362, "fichiers_lus_en_profondeur": "470+", "tables_produites": 13, "branches_analysees": 34, "depots_github_verifies": 9, "connecteurs_interroges": 4}

## Prochaines actions

- PR #3 : faire merger la PR d'audit (ouverte, head b15a1a8)
- Ordre de fusion du travail produit (RELANCER LES COMPARES AVANT CHAQUE FUSION — le repo bouge vite) : 0034230e (Carre d'As + shell 14 modules + _incoming 859 f.) -> 93b54a79 (mail-organizer + FEATURES-INVENTORY) -> 01a08449 (BTP 21 onglets) -> PR #3 (watchtower INTEL) -> feat/final-interface-skeleton + feat/tool-data-catalog -> branches ETAT / Language-decoder
- Canoniser la taxonomie : 14 modules shell = produit ; 12 domaines = couverture ; v1->v5 = ordonnancement
- Brancher le 1er module reel dans #slot-btp (corpus en racine, sans copie)
- reaserch-engine : 2 tests rouges (test_researcher_uses_injected_retriever, test_contradictions_are_prioritized)
- Drift proto 161 vs 184 fichiers (-25 auth) a reconcilier ; licences watchtower/HCSM NOASSERTION ; LD (m0) et formation frontignan a integrer

## Projets

| Projet | Statut | Phase | Risque | Notes |
|---|---|---|---|---|
| COGNITORIUM | fait | P3 | moyen | audit/notes/P-COGNITORIUM.md |
| proto-cognitorium | fait | P3 | élevé | audit/notes/P-proto-cognitorium.md |
| HCSM | fait | P3 | faible | audit/notes/P-HCSM.md |
| reaserch-engine | fait | P3 | moyen | audit/notes/P-reaserch-engine.md |
| ETAT-DE-LART-PSYCHOLOGIE | fait | P3 | élevé | audit/notes/P-ETAT-DE-LART-PSYCHOLOGIE.md |
| watchtower | fait | P3 | moyen | audit/notes/P-watchtower.md |
| animation-chronos | fait | P3 | faible | audit/notes/P-animation-chronos.md |
| Language-decoder | fait | P3 | élevé | audit/notes/P-Language-decoder.md |
| frontignan | fait | P3 | moyen | audit/notes/P-frontignan.md |

## Phases

- [x] P0 Cadrage & plan
- [x] P1 Mémoire & instrumentation
- [x] P2 Inventaire factuel
- [x] P3 Audit par projet
- [x] P4 Audit transversal
- [x] P5 Audit externe (GitHub + connecteurs)
- [x] P6 Synthèse & tableaux
- [x] P7 Contrôle qualité & publication
