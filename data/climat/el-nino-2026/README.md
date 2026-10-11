# 🌊 Dataset climat — El Niño 2026–2027 « Godzilla » × bassin de Thau

> **Une seule source de vérité** pour tout ce que le monorepo sait de l'épisode El Niño 2026–2027 :
> observations globales (vidéo LIMIT « EL NIÑO : GODZILLA » du 11/10/2026, avec Xavier Fettweis — ULiège),
> errata du 24/09/2026, synthèse stratégique et **frise opérationnelle golfe du Lion / Thau Agglo**
> (Frontignan · Sète · Marseillan · lagune de Thau, octobre 2026 → décembre 2027).

## 📦 Contenu

```
data/climat/el-nino-2026/
├─ el-nino-godzilla-2026.json          ← dataset canonique structuré (88 Ko, FR)
├─ README.md                           ← ce fichier (schéma + usage)
└─ sources/                            ← transcriptions verbatim des documents transmis
   ├─ limit-script-tournage-2026-09-24.md      texte de tournage LIMIT (partiel : coupé au chap. 2)
   ├─ synthese-strategique-2026-10-11.md       synthèse stratégique complète (sections 1–12, errata inclus)
   └─ frise-thau-golfe-lion-2026-2027.md       section 13 : frise opérationnelle Thau + outils + tableau de suivi
```

## 🗂 Schéma du dataset (`el-nino-godzilla-2026.json`)

| Section | Contenu |
|---|---|
| `meta` | Identité, version, provenance (vidéo/expert/errata), légendes `status` et `attribution`, disclaimer |
| `key_message` | Idée centrale, les 3 niveaux (observations / prévisions / hypothèses), leçon essentielle |
| `sources` | 15 sources référencées (LIMIT, OMM, NOAA/CPC, Berkeley Earth, Climate Impact Lab, Oxfam, JMA, Météo-France, SMBT, Ville de Frontignan, Vigicrues, Géorisques…) |
| `glossary` | 18 termes (alizés, upwelling, Niño 3.4, RONI, goutte froide, épisode méditerranéen, PAPI, PCS, PPRI, DICRIM…) |
| `mechanism` | Pacifique normal vs El Niño, chaîne causale, périodicité, métaphore pédagogique |
| `indicators` | Niño 3.4 (+3,07 °C le 22/09/2026), RONI (+1,4 été 2026), évolution des probabilités NOAA (25→60→69→75 %), persistance OMM (~100 % jusqu'en février), eau précipitable, Clausius–Clapeyron |
| `quotes` | 5 citations horodatées de Xavier Fettweis (00:00, 01:48, 04:01, 04:57, 06:11) |
| `global_facts` | 10 faits régionaux (Pérou, Panama, Corredor Seco, cyclones, Atacama, Nagoya, Indonésie, Inde, Europe/Belgique, Méditerranée) avec `status`, `attribution`, chiffres, mécanisme, perspectives |
| `projections` | Projections saisonnières, mortalité Climate Impact Lab (451 000 / 239 000 — **projections, pas des bilans**), records |
| `scenarios` | 3 cadres de planification A/B/C (favorable, intermédiaire, cascade) |
| `effects_matrix` | Effets positifs/négatifs par domaine (8 lignes) |
| `second_order_risks` | Cascades systémiques (exemple sécheresse agricole + 6 cascades + leçon 1877) |
| `prevention` | 4 priorités d'action (pertes humaines, eau/alimentation, infrastructures, gouvernance de crise) |
| `epistemics` | Bien établi / plausible / à présenter avec prudence / à ne pas attribuer automatiquement |
| `conclusions` | Les 10 conclusions à retenir |
| `thau` | **Focus territorial** : contexte saisonnier Météo-France (5/10), fait local (épisode 29/09–1/10, vigilance rouge Hérault, >250 mm), 7 risques communaux, **frise en 6 phases** avec filtres (`horizons`, `risk_types`), outils territoriaux (PAPI Thau 46 actions/25 communes/6,8 M€, PCS-PPRI Frontignan, vigilances), tableau de bord de surveillance (8 indicateurs), plan d'action temporel, règle de primauté des bulletins locaux |
| `geo` | 15 watchpoints géolocalisés (6 locaux Thau + 9 globaux) — export GeoJSON pour watchtower |
| `quiz` | 10 questions pédagogiques (attribution, RONI, projections vs bilans, PAPI…) |
| `learning` | Scénario complet du PoC COGNITORIUM « Comprendre El Niño : du Pacifique au bassin de Thau » (10 niveaux, graphe de concepts, question de transfert) |

### Vocabulaires contrôlés

- **`status`** : `observe` (observé/rapporté) · `prevu` (prévision/projection) · `incertain` (hypothèse/attribution à confirmer)
- **`attribution`** : `el_nino` (conséquence établie) · `mixte` (El Niño + météo locale/fond) · `meteo_locale` · `rechauffement_fond` · `non_attribue`

## 🔌 Comment les modules l'utilisent

| Module | Artefact | Accès |
|---|---|---|
| **API monorepo** (`app/main.py`) | endpoints JSON | `GET /api/climat/datasets` · `GET /api/climat/el-nino` · `GET /api/climat/el-nino/{section}` (ex. `thau`, `quiz`, `geo`) |
| **frontignan** (Atlas) | `projects/frontignan/el-nino-thau.html` — module interactif autonome (frise filtrable, faits globaux, risques & scénarios, mini-simulation pluie/mer, quiz, checklist prévention, sources) | preview `/preview/frontignan/el-nino-thau.html` ou ouverture directe du fichier ; slide dédiée dans le deck `index.html` |
| **COGNITORIUM** (learning) | `projects/COGNITORIUM/learning/el-nino-poc.html` + `el-nino-poc.js` (généré) — PoC « Comprendre El Niño » sur le modèle du PoC argent | preview `/preview/COGNITORIUM/learning/el-nino-poc.html`, lié depuis `learning/index.html` |
| **watchtower** (globe) | `projects/watchtower/public/data/enso-thau-watchpoints.geojson` (généré) — 15 watchpoints + boîte Niño 3.4 | glisser-déposer le fichier sur le globe (import GeoJSON natif du fork), ou servir via le preview |

Les artefacts marqués **(généré)** sont produits par `scripts/build_climat_assets.py` à partir du JSON canonique — ne pas les éditer à la main.

## 🛠 Régénérer & valider

```bash
python3 scripts/validate_climat_data.py     # valide le schéma du dataset (stdlib)
python3 scripts/build_climat_assets.py      # régénère les 3 artefacts modules
```

## ⚠️ Règles d'usage

1. **Projections ≠ bilans** : les 451 000 décès (juin 2026→février 2027, Climate Impact Lab, non évalué par les pairs) et les 239 000 (fenêtre courte, errata) sont des projections de modèle — toujours les étiqueter avec période, modèle et incertitude.
2. **Attribution ≠ automatisme** : Nagoya (front stationnaire / tempête Krovanh) et l'Atacama (goutte froide) ne sont pas des conséquences directes d'El Niño ; le Pérou (upwelling coupé) si.
3. **Contexte ≠ déclencheur local** : les prévisions El Niño sont un contexte pour Thau — les décisions opérationnelles se prennent sur les bulletins locaux (Météo-France, Vigicrues, arrêtés préfectoraux).
4. Les chiffres proviennent des documents transmis (vidéo + synthèse + errata) ; ils ne constituent pas une vérification indépendante de chaque source.
