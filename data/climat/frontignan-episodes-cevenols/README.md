# ⛈ Dataset climat — Frontignan face aux épisodes cévenols (blocages & solutions)

> **Complément territorial** du dataset [`../el-nino-2026/`](../el-nino-2026/) : diagnostic des
> **points bloquants** de Frontignan-la Peyrade lors des épisodes cévenols / méditerranéens
> (ruissellement de la Gardiole, saturation des réseaux, contraintes littoral/étang, secours,
> pollutions secondaires) et des **opportunités de solution** (connaître · alerter · protéger ·
> retenir · ralentir · évacuer · organiser), avec la feuille de route de l'étude pilote
> Gardiole → centre-ville (4/5).
>
> Fondé sur les documents communaux et intercommunaux : **PCS Frontignan (2025)**, **PPRI**,
> **programme d'études SMBT** (désordres majeurs Gardiole → centre-ville, sollicitation des
> réseaux début 2026, ruissellement urbain 2019), **PAPI de Thau 2026–2031** (46 actions,
> 25 communes, ≈ 6,8 M€), **THAU ALABRI**, **VigiThau**.

## 📦 Contenu

```
data/climat/frontignan-episodes-cevenols/
├─ frontignan-cevenols-2026.json   ← dataset canonique (schéma « territorial-risk-v1 »)
├─ README.md                       ← ce fichier
└─ sources/
   └─ analyse-blocages-solutions-2026-10-11.md   transcription verbatim du diagnostic transmis
```

## 🗂 Schéma (`frontignan-cevenols-2026.json`)

| Section | Contenu |
|---|---|
| `meta` | Identité, schéma `territorial-risk-v1`, provenance (PCS 2025, PPRI, SMBT, PAPI…), datasets liés, disclaimer |
| `key_message` | Diagnostic central (« le problème n'est pas seulement la quantité de pluie »), contexte, conclusion |
| `sources` | 10 sources (PCS 2025, PPRI, SMBT ×3, PAPI, THAU ALABRI, étude préalable PAPI, VigiThau, Ville) |
| `blocking_points` | **5 blocages** : Gardiole→ville · saturation des réseaux · littoral/étang · déplacements & secours · pollutions secondaires — chacun avec mécanisme, preuve documentaire, verrou (`blockage`) et sources |
| `solutions` | Principe + **matrice P1/P2/P3** (7 solutions : cartographie fine, capteurs/VigiThau, THAU ALABRI, désimperméabilisation, restauration des écoulements, réseaux/exutoires, plan de circulation de crise) + PAPI (46 actions, point à vérifier) |
| `atlas_opportunities` | **4 modules Atlas** : A carte des mécanismes · B simulateur (*première version disponible* → onglet Simulation) · C comparateur de solutions · D tableau de bord (ébauche → onglet Frise Thau) |
| `pilot` | Recommandation (étude pilote Gardiole → centre-ville), feuille de route **5 étapes (4/5)**, sources locales à exploiter en premier |
| `geo` | 6 zones de blocage indicatives (Gardiole, centre-ville, exutoires, plage, ZI La Peyrade, axes secours) — export GeoJSON watchtower |

## 🔌 Comment les modules l'utilisent

| Module | Artefact | Accès |
|---|---|---|
| **frontignan** (Atlas) | Onglet **« ⛈ Épisodes cévenols »** du module `el-nino-thau.html` (généré) : 5 cartes blocages avec bouton *« → Simuler ce mécanisme »* vers la simulation Gardiole→Thau, matrice solutions, modules Atlas, feuille de route pilote | `/preview/frontignan/el-nino-thau.html` |
| **watchtower** (globe) | `projects/watchtower/public/data/frontignan-cevenols-watchpoints.geojson` (généré) — 6 zones de blocage | glisser-déposer sur le globe (import GeoJSON natif) |
| **API** | endpoints climat génériques | `GET /api/climat/datasets` · `GET /api/climat/frontignan-cevenols-2026` · `GET /api/climat/frontignan-cevenols-2026/{section}` (`blocking_points`, `solutions`, `pilot`, `geo`…) |

Les artefacts marqués **(généré)** sont produits par `scripts/build_climat_assets.py` — ne pas les éditer à la main.

## 🛠 Valider & régénérer

```bash
python3 scripts/validate_climat_data.py    # valide TOUS les datasets data/climat/* (dispatch par meta.schema)
python3 scripts/build_climat_assets.py     # régénère module + PoC + les 2 GeoJSON
```

## ⚠️ Limites

1. **Diagnostic documentaire, pas une étude hydraulique** : les localisations `geo` sont indicatives ; les scénarios du module Atlas restent pédagogiques et qualitatifs.
2. **À valider** : l'affectation précise des actions/budgets/calendriers du PAPI à chaque secteur de Frontignan.
3. Toute décision d'aménagement doit s'appuyer sur les données techniques officielles et une validation par les services compétents (Ville, Sète Agglopôle, SMBT) — et faire valider les scénarios par les spécialistes.
