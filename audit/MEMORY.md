# MEMORY — Audit monorepo (index généré)

> **NE PAS ÉDITER À LA MAIN** — généré par `python3 scripts/audit_memory.py render`
> depuis `audit/state.json`. Mis à jour : 2026-10-07T12:34:11Z

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
- Phase courante : **P7 — Contrôle qualité & publication**
- Compteurs : {"findings": 52, "fichiers_locaux_mesures": 1362, "fichiers_lus_en_profondeur": "470+", "tables_produites": 13, "branches_analysees": 34, "depots_github_verifies": 9, "connecteurs_interroges": 4}

## Prochaines actions

- P7 — vérification finale des chiffres (fait : 1119/283478/237/221 ✅)
- P7 — commit + push branche arena/171a1f38-monorepo
- P7 — PR vers main avec le dossier audit/

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
- [>] P7 Contrôle qualité & publication
