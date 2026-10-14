# S2 — Inventaire factuel des 9 projets locaux

**Mesuré** : 2026-10-07 · **Outil** : `python3 scripts/audit_inventory.py --all` → `audit/data/inventory.json`
**Note de méthode** : `dist/` et `node_modules/` sont **exclus** des comptages (artefacts de build), sauf mention contraire. « LOC-code » = lignes de code hors JSON/CSV/Markdown ; « LOC-données/doc » = le reste des fichiers texte.

## Tableau maître (à réutiliser tel quel)

| Projet | Fichiers | Taille | LOC-code | LOC-données/doc | Fichiers code | Tests | Docs | Données | Noms sensibles | TODO/FIXME |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `COGNITORIUM` | 131 | 22.9 Mo | 27 691 | 2 291 | 118 | 0 | 53 | 0 | 0 | 2 |
| `proto-cognitorium` | 161 | 73.8 Mo | 53 334 | 5 624 | 78 | 0 | 57 | 4 | 1 | 0 |
| `watchtower` | 583 | 22.8 Mo | 190 453 | 13 661 | 558 | **208** | 35 | 19 | 2 | 0 |
| `HCSM` | 87 | 273 Ko | 1 917 | 3 256 | 83 | 1 | 52 | 24 | 0 | 0 |
| `reaserch-engine` | 61 | 131 Ko | 1 167 | 1 801 | 60 | **12** | 16 | 9 | 0 | 0 |
| `ETAT-DE-LART-PSYCHOLOGIE` | 37 | 3.6 Mo | 2 569 | 2 683 | 31 | 0 | 20 | 4 | 0 | 0 |
| `animation-chronos` | 30 | 3.8 Mo | 2 583 | 4 362 | 22 | 0 | 0 | 4 | 1 | 0 |
| `frontignan` | 28 | 13.6 Mo | 3 764 | 635 | 10 | 0 | 3 | 0 | 0 | 0 |
| `Language-decoder` | **1** | **19 o** | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| **Total (9 projets)** | **1 119** | **141.4 Mo** | **283 478** | **34 313** | **901** | **221** | **237** | **64** | **4** | **2** |

## Répartition par langage (LOC-code cumulées)

| Langage | Lignes | Fichiers | Projet dominant |
|---|---:|---:|---|
| JavaScript | 186 246 | 645 | `watchtower` (178 707 sur `src/`) |
| TypeScript | 66 559 | 128 | `proto-cognitorium` (≈ 40 k), `COGNITORIUM` (watchtower-mods) |
| Python | 21 585 | 129 | `reaserch-engine`, `HCSM` (+ validateurs), `frontignan/scripts` |
| HTML | 4 087 | 22 | `COGNITORIUM/learning`, `ETAT-DE-LART/output` |
| CSS | 10 071 | 9 | `watchtower/style.css`, `proto-cognitorium` |
| Shell / PowerShell | 1 182 | 12 | `watchtower/scripts`, `COGNITORIUM` |
| Autres (SQL, YAML, TOML, C…) | ~1 700 | 20 | `proto-cognitorium/raw`, `HCSM` |

*(Le détail par projet figure dans `audit/data/inventory.json` → `scopes.P-<projet>.loc`.)*

## Fichiers les plus volumineux (top 8)

| Fichier | Taille | Projet |
|---|---:|---|
| `projects/proto-cognitorium/raw/slide carte représentation.pptx` | 21.8 Mo | proto-cognitorium |
| `projects/proto-cognitorium/raw/Manuel_exploitation.pdf` | 9.0 Mo | proto-cognitorium |
| `projects/proto-cognitorium/src/data/romeData.ts` | 5.5 Mo | proto-cognitorium |
| `projects/proto-cognitorium/raw/Cabrol.Rapport de stage.pdf` | 5.4 Mo | proto-cognitorium |
| `projects/watchtower/src/data/local_data/datacenters/datacenters.geojsonl` | 2.4 Mo | watchtower |
| `projects/proto-cognitorium/raw/Soutenance-fin-de-stage-FINAL.pdf` | 2.9 Mo | proto-cognitorium |
| `projects/watchtower/src/data/local_data/natural_earth/regions.json` | 1.9 Mo | watchtower |
| `projects/proto-cognitorium/raw/SeQuelec_Guide_3.pdf` | 2.3 Mo | proto-cognitorium |

## Constats immédiats

1. **`Language-decoder` : 1 fichier de 19 octets** en local — c'est le projet le plus vide (M0). La copie locale est un README vide ; le dépôt GitHub associé pèse 2.4 Mo et a bougé aujourd'hui (cf. S3) → **écart majeur local/distant**.
2. **`watchtower` est de loin le plus gros code** (190 k lignes, 583 fichiers, 208 fichiers de test) — le projet « réel » le plus avancé.
3. **`proto-cognitorium` pèse 73.8 Mo dont 64 Mo dans `raw/`** (61 fichiers : PDF de stage, PowerPoint de 21.8 Mo) — données brutes lourdes dans Git.
4. **`COGNITORIUM` (22.9 Mo)** contient 10+ images générées non nommées + `watchtower-mods/` (code Cesium) — mélange dépôt vitrine/code.
5. **Tests concentrés sur 2 projets** : `watchtower` (208) et `reaserch-engine` (12). Les 7 autres : 0.
6. **`frontignan` n'est pas sur GitHub** (pas de dépôt distant) — projet local seulement, 13.6 Mo dont 12 Mo de figures/visuels.
7. **`ETAT-DE-LART-PSYCHOLOGIE` local (37 fichiers)** : version localement réduite par rapport aux 9 branches distantes (cf. S3).
8. **TODO/FIXME quasi absents** (2) : la dette est surtout implicite (docs, versions, sync), pas annotée dans le code.

## Findings S2

| # | Sévérité | Catégorie | Constat | Preuve | Recommandation |
|---|---|---|---|---|---|
| F-S2-01 | élevé | C2 Dépôt, branches & synchronisation | `Language-decoder` local (19 o) ≠ GitHub (2.4 Mo, poussé le 2026-10-07) | inventaire + `gh api` | resynchroniser ou archiver |
| F-S2-02 | moyen | C6 Données & ressources | 64 Mo de `raw/` (dont 21.8 Mo pptx) dans `proto-cognitorium` | inventaire | externaliser (LFS ou hors dépôt) |
| F-S2-03 | moyen | C8 Tests & qualité | 7 projets sur 9 sans aucun test | inventaire | cibler : `proto-cognitorium`, `COGNITORIUM/learning`, infra |
| F-S2-04 | faible | C3 Structure & volumétrie | `COGNITORIUM` = vitrine + images générées + code Cesium | inventaire | séparer les images du code |
| F-S2-05 | info | C1 Identité & provenance | `frontignan` sans dépôt GitHub | `gh repo list` | décider : publier ou documenter comme local |
