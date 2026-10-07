# MEMORY — Audit monorepo (index généré)

> **NE PAS ÉDITER À LA MAIN** — généré par `python3 scripts/audit_memory.py render`
> depuis `audit/state.json`. Mis à jour : 2026-10-07T15:22:46Z

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

- 0. (rappel) RELECTURE avant fusion : le projet produit un lot toutes les 20 min — relancer les compares
- 1. Fusionner arena/0034230e (Carre d'As + shell 14 modules + _incoming + resync proto)
- 2. Fusionner arena/93b54a79 (mail-organizer + FEATURES-INVENTORY) puis arena/01a08449 (BTP 21 modules)
- 3. PR #3 watchtower INTEL ; feat/final-interface-skeleton + feat/tool-data-catalog ; branches ETAT/Language-decoder
- 4. Trancher la taxonomie canonique (shell 14 modules = produit ; 12 domaines = couverture)
- 5. Brancher le premier module reel dans #slot-btp (corpus racine, sans copie)

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
