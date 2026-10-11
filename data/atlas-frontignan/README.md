# 🗺 Atlas Frontignan — console territoriale (spec Phase 0)

> **Spécification canonique** de la console de décision territoriale « Atlas Frontignan » :
> une carte stratégique jouable du territoire réel, inspirée des interfaces 4X
> (lentilles de vue, arbre d'actions, indicateurs « yields »), dont **l'inondation n'est
> qu'une branche**. Méthode : **placeholder complet d'abord** — modes, modules, objets,
> actions et indicateurs existent comme structure navigable — puis remplissage progressif
> par urgence.
>
> Fondée sur les synthèses de discussion du 11/10/2026 (voir `sources/`) et sur les
> datasets climat canoniques (PCS 2025, SMBT, PAPI Thau 2026–2031 → `../climat/frontignan-episodes-cevenols/`).

## 📦 Contenu

```
data/atlas-frontignan/
├─ atlas-frontignan-2026.json   ← spec canonique (schéma « atlas-frontignan-v1 »)
├─ README.md                    ← ce fichier
└─ sources/
   └─ syntheses-discussion-2026-10-11.md   transcriptions verbatim des 2 synthèses fondatrices
```

## 🗂 Schéma (`atlas-frontignan-2026.json`)

| Section | Contenu |
|---|---|
| `meta` | Identité, métaphore produit, boucle Observer→Diagnostiquer→Simuler→Décider→Suivre, méthode, datasets liés, disclaimer |
| `key_message` | Vision en une phrase, fil rouge (pentes→…→secours), 4 étapes de méthode, **point de vigilance placeholder/donnée/simulation** |
| `statuses` | **EMPTY → SHELL → DATA → LIVE → SIM** (couleurs + définitions — la règle du jeu) |
| `modes` | **14 lentilles de vue** : territoire, relief & pentes, eau, pluvial, inondation, secours, réseaux, urbanisme, nature, climat, mobilités, économie, gouvernance, scénario — chacune avec question de lecture, note et couches statuées |
| `modules` | **7 branches / 35 sous-modules** : risques, pluvial, secours, eau, aménagement, nature & climat, société-économie-gouvernance |
| `actions` | **15 actions** (arbre) : coût, délai, prérequis, effets multi-indicateurs (`basis: placeholder`), preview carte, hook de simulation |
| `indicators` | **9 yields** : risque, performance pluviale, préparation crise, nature, ICU, budget (PAPI, documenté), acceptabilité, ZAN, conformité |
| `units` | 6 types d'« unités » : zones, réseaux, ouvrages, bâtiments enjeux, équipes mobiles, projets fantômes |
| `overlays` | météo, alertes, chantiers, annotations |
| `map` | **43 objets carte** (projection stylisée + lat/lon indicatifs) dont **6 zones branchées `data_link` sur le dataset cévenols** (statut DATA) |
| `phases` | Phase 0 (coquille, livrée) → Phase 4 (élargissement, LIVE) |
| `data_sources` | 12 sources de remplissage (IGN, Géorisques, mairie, SMBT, Météo-France…) avec phase cible |
| `links` / `sources` | Artefacts liés + synthèses fondatrices |

## 🔌 Comment les modules la consomment

| Module | Artefact | Accès |
|---|---|---|
| **frontignan** (console) | `projects/frontignan/atlas.html` **(généré)** — coquille jouable : carte stylisée SVG, 14 lentilles, inspecteur (fiches objets + blocages cévenols DATA), 7 modules, arbre d'actions, scénario avant/après (placeholders assumés), phases, méthode | `/preview/frontignan/atlas.html` |
| **module climat** (réciproque) | `el-nino-thau.html` référence la console dans sa carte « Réutilisation » ; liens croisés par ancre `#cevenols` / `#sim` depuis la console | `/preview/frontignan/el-nino-thau.html` |
| **API** | la spec est un JSON statique dans `data/` (pas encore d'endpoint dédié — les datasets climat qu'elle référence sont servis par `/api/climat/{dataset}`) | — |

Les zones **DATA** de la console sont alimentées par `frontignan-cevenols-2026` (6 watchpoints → blocages documentés) et `el-nino-godzilla-2026` (watchpoints climat Thau) — même source de vérité que le module climat, l'API et les GeoJSON watchtower.

## 🛠 Valider & régénérer

```bash
python3 scripts/validate_atlas_spec.py    # cohérence de la spec (refs modes/actions/indicateurs/data_link)
python3 scripts/build_atlas_assets.py     # régénère projects/frontignan/atlas.html
python3 scripts/build_atlas_assets.py --check
```

## ⚠️ Règles & limites

1. **La règle du jeu** : un placeholder, une donnée réelle, une prévision officielle et un résultat simulé restent distingués (statuts affichés partout ; les deltas du scénario sont taggés « placeholder » et jamais présentés comme des estimations).
2. **Carte stylisée** : ni étude hydraulique ni géodésie — localisations indicatives ; les données réglementaires (PPRI, AZI) et techniques (plan des réseaux) arrivent en Phase 1.
3. **Pas un outil de crise** : rien n'est temps réel (LIVE) en Phase 0 ; les bulletins officiels priment toujours.
4. Artefacts **(généré)** : ne pas les éditer à la main — modifier la spec puis relancer le builder.
