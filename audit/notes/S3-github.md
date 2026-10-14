# S3 — Réel GitHub (état des 9 dépôts au 2026-10-07)

**Mesuré** : 2026-10-07 · **Méthode** : `gh api` (branches, compare, trees, PR, runs) + `scripts/audit_gh_drift.py`
**Données** : `audit/data/branches-all.json`, `audit/data/drift.json`, `audit/data/monorepo-branches.json`

## 1. Les 9 dépôts (état réel)

| Dépôt | Créé | Dernier push | Langage | Taille GitHub | Branches | PR (ouvertes/fusionnées) | CI |
|---|---|---|---|---|---|---|---|
| `monorepo` | 2026-09-07 | 2026-10-07 11:40 | JavaScript | 317 Mo | **9** | 0 / 2 | — |
| `watchtower` | 2026-09-01 | **2026-10-07 09:32** | JavaScript | 10 Mo | 5 | **1 / 2** | ✅ `ci.yml` (27 runs) |
| `Language-decoder` | 2026-08-30 | **2026-10-07 06:17** | — | 2.4 Mo | 3 | 0 / 0 | — |
| `proto-cognitorium` | 2026-08-24 | 2026-09-10 | TypeScript | 94 Mo | 8 | 0 / 6 | — |
| `ETAT-DE-LART-PSYCHOLOGIE` | 2026-08-24 | 2026-09-07 | HTML | 10 Mo | 9 | 0 / 2 | — |
| `COGNITORIUM` | 2026-08-02 | 2026-09-07 | JavaScript | 22 Mo | 4 | 0 / 2 | — |
| `animation-chronos` | 2026-09-02 | 2026-09-02 | TypeScript | 3.6 Mo | 1 | 0 / 0 | — |
| `reaserch-engine` | 2026-08-26 | 2026-08-27 | Python | 96 Ko | 1 | 0 / 0 | — |
| `HCSM` | 2026-08-25 | 2026-08-25 | Python | 118 Ko | 3 | 0 / 2 | — |

**Vérifié** : `watchtower` est le **seul dépôt avec une CI** (l'API renvoie 404 pour `.github/workflows` partout ailleurs — attention, un `len()` naïf sur la réponse d'erreur donne « 3 », piège rencontré et corrigé).

## 2. Le fait central : 153 commits non fusionnés sur 15 branches

| Mesure | Valeur |
|---|---:|
| Branches hors `main` | **34** |
| Branches **avec du travail** (`ahead > 0`) | **15** |
| Branches **mortes** (`ahead = 0`) | **19** |
| **Commits non fusionnés** (somme des `ahead`) | **153** |
| Fichiers portés par ces branches (arbre cumulé) | 12 471 |

### 15 branches avec travail réel (par avance)

| Dépôt | Branche | + | − | Fichiers | Taille | Dernier commit | Contenu |
|---|---|---:|---:|---:|---:|---|---|
| watchtower | `arena/01a072e1-watchtower` | **43** | 10 | 650 | 22.9 Mo | 2026-10-07 | docs/audit + UI (volant, carte 2D, panneau FIL, INTEL) |
| ETAT-DE-LART | `arena/01a04f7b-…` | **38** | 1 | 1 818 | 19.6 Mo | 2026-09-02 | `agent/` (30 fichiers), `cosmos/`, 221 sorties |
| COGNITORIUM | `watchtower/osint-workbench-v0.1` | 13 | 0 | 143 | 22.9 Mo | 2026-09-07 | modules OSINT + specs |
| monorepo | `feat/tool-data-catalog-2026-10` | 13 | 0 | 1 813 | 410 Mo | 2026-10-07 | `core/contracts`, `data/*registry.json`, docs architecture |
| watchtower | `arena/dec9cd88-watchtower` | 7 | 0 | 623 | 23.8 Mo | 2026-10-07 | **PR #3** : INTEL, import CSV, carte stratégique |
| Language-decoder | `arena/01a05429-…` | 7 | 0 | 27 | 0.6 Mo | 2026-10-07 | pages, docs, données |
| monorepo | `feat/final-interface-skeleton-2026-10-07` | 7 | 0 | 1 810 | 410 Mo | 2026-10-07 | interface finale + audit d'intégration |
| monorepo | `arena/01a08385-monorepo` | 6 | 25 | 1 666 | 181 Mo | 2026-10-07 | **nexus_os** (85 fichiers, 10 agents, 59 tests) |
| proto-cognitorium | `arena/01a08342-…` | 5 | 2 | 173 | 73.8 Mo | 2026-09-10 | `tools/audit/*` + rapports d'audit |
| ETAT-DE-LART | `arena/01a07d32-…` | 5 | 0 | 46 | 3.8 Mo | 2026-09-07 | route bundle, secours push |
| Language-decoder | `arena/01a05471-…` | 3 | 0 | 24 | 2.0 Mo | 2026-10-07 | **moteur Python + UI + tests** |
| ETAT-DE-LART | `arena/01a03aac-…` | 2 | 1 | 39 | 3.4 Mo | 2026-08-25 | Cognitorium v8 (graphe 3D, 40 fiches) |
| monorepo | `arena/01a08449-monorepo` | 2 | 13 | 1 987 | 449 Mo | 2026-10-07 | **btp-conduite-travaux** (154 documents sources, 7 rapports) + `scripts/` |
| ETAT-DE-LART | `arena/01a045a1-…` | 1 | 1 | 54 | 3.2 Mo | 2026-09-07 | agent de recherche littéraire |
| monorepo | `arena/01a08203-monorepo` | 1 | 25 | 1 598 | 184 Mo | 2026-09-08 | atlas interactif Frontignan |

### Branches mortes (19) — supprimables sans perte

`proto-cognitorium` 6 · `ETAT-DE-LART` 4 · `monorepo` 2 · `HCSM` 2 · `COGNITORIUM` 2 · `watchtower` 2 · `reaserch-engine` 0 · `animation-chronos` 0 · `Language-decoder` 0.

## 3. PR (état réel)

| Dépôt | PR | État | Titre | CI |
|---|---|---|---|---|
| watchtower | **#3** | **OUVERTE** (créée 2026-10-06) | TERRITOIRE (carte stratégique + import CSV) & INTEL (base territoriale) | ✅ verte (5 runs) |
| watchtower | #1, #2 | fusionnées | itérations 7-9 ; audit de 14 liens → 86 outils | — |
| monorepo | #1, #2 | fusionnées (08/09, **07/10**) | frontignan ; dossier de chantier + synthèse Talbot | — |
| proto-cognitorium | #1–#6 | fusionnées (24-26/08) | — | — |
| COGNITORIUM | #1, #2 | fusionnées (03/09, 06/09) | WATCHTOWER v14 ; gouvernance + état des lieux | — |
| ETAT-DE-LART | #1, #2 | fusionnées (25/08) | — | — |
| HCSM | #1, #2 | fusionnées (25/08) | cadre scientifique ; validateur V1/V5 | — |
| `reaserch-engine`, `animation-chronos`, `Language-decoder` | — | jamais de PR | — | — |

## 4. Synchronisation copie locale ↔ distant (mesurée fichier par fichier)

| Projet | Local | Distant (`main`) | +local | +distant | Δtaille | Verdict |
|---|---:|---:|---:|---:|---:|---|
| `proto-cognitorium` | 161 | 184 | 2 | **25** | 12 | **périmé** |
| `animation-chronos` | 30 | 30 | 1 | 1 | 0 | écart mineur (lockfile, .gitignore) |
| `COGNITORIUM` | 131 | 131 | 0 | 0 | 0 | à jour |
| `HCSM` | 87 | 87 | 0 | 0 | 0 | à jour |
| `reaserch-engine` | 61 | 61 | 0 | 0 | 0 | à jour |
| `ETAT-DE-LART` | 37 | 37 | 0 | 0 | 0 | à jour (mais branches orphelines) |
| `watchtower` | 583 | 583 | 0 | 0 | 0 | à jour (mais branches orphelines) |
| `Language-decoder` | 1 | 1 | 0 | 0 | 0 | à jour… sur un `main` vide |

> **Lecture** : la copie locale du monorepo (snapshot `MANIFEST.json` du 2026-09-07) est fidèle à l'instantané, mais **l'état réel du travail est dans les branches** : 153 commits, 15 branches, dont 5 actives le jour de l'audit (watchtower ×2, Language-decoder ×2, monorepo ×3).

## 5. Sources internes déjà produites (à ne pas dupliquer)

| Document | Où | Objet |
|---|---|---|
| `docs/AUDIT-2026-10-07.md` (14.8 Ko) | watchtower, branche `dec9cd88` | audit dépôts/outils/capacités du 07/10 (mesuré) |
| `docs/CAPACITES-2026-10-07.md` | monorepo, branche `01a08385` | audit de capacités, recense 144 commits non fusionnés sur 41 branches |
| `docs/AUDIT-INTEGRATION-INTERFACE-FINALE-2026-10-07.md` | monorepo, `feat/final-interface-skeleton…` | décision d'architecture + taxonomie en 12 domaines |
| `docs/TOOL-DATA-CATALOG.md` | monorepo, `feat/tool-data-catalog-2026-10` | catalogue outils/données |
| `docs/AUDIT_2026-09-{08,09,10}*.md`, `TRACEABILITE.csv` | proto-cognitorium, `01a08342` | audits incrémentaux du proto (42→45 anomalies) |
| `audit/REFERENCE.md` + `REGISTRE-OUTILS.json` | watchtower (`main`) | 86 outils, licences, coûts |
| `docs/etat-des-lieux/*` et `docs/audits/*` | COGNITORIUM (`main`) | état des lieux 8 dépôts (sept. 2026) |

**Différence avec cet audit** : les documents ci-dessus sont soit **par dépôt**, soit **embarqués dans une branche non fusionnée**. `audit/AUDIT-2026-10.md` est le premier état des lieux **transverse et consolidé**, mesuré au 2026-10-07, avec méthode et preuves reproductibles.

## 6. Findings GitHub

| # | Sévérité | Catégorie | Constat | Preuve | Recommandation |
|---|---|---|---|---|---|
| F-GH-01 | **critique** | C2 | 153 commits non fusionnés sur 15 branches ; 5 branches actives le jour de l'audit | `branches-all.json` | plan de fusion (voir P7) |
| F-GH-02 | élevé | C2 | PR #3 watchtower CI verte, ouverte depuis le 06/10 | `gh pr list`, `gh run list` | fusionner |
| F-GH-03 | élevé | C2 | `Language-decoder` : projet réel jamais sur `main` | `drift.json` | PR moteur → `main` |
| F-GH-04 | moyen | C2 | 19 branches mortes | `branches-all.json` | supprimer |
| F-GH-05 | moyen | C2 | `main` de `proto-cognitorium` avancé sans PR (push direct du 10/09) | `gh api` | ouvrir des PR systématiquement |
| F-GH-06 | moyen | C8 | 1 seul dépôt sur 9 a une CI | API `.github/workflows` (404 × 8) | généraliser la CI (au moins lint/build) |
| F-GH-07 | faible | C1 | dépôts sans licence : 7 sur 9 | `find` | choisir une licence par dépôt |
