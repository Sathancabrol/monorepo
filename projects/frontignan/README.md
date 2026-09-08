# 🍯 Frontignan la Peyrade — analyse territoriale & vision 2026-2040

Dossier d'appui pour l'accompagnement de la municipalité de Frontignan (Hérault, Sète Agglopôle Méditerranée) — septembre 2026.

## 📦 Contenu

| Fichier | Contenu |
|---|---|
| **`index.html`** | 🎞️ **Deck de présentation** « Frontignan 2026→2040, focale 2030 » — 18 slides, autonome (images intégrées), scroll vertical, ← → au clavier, Ctrl+P → export PDF paysage |
| `vision-frontignan-2026-2040.md` | 🔮 **Vision prospective** macro/micro 2026→2040 (focale 2030) — source éditable |
| `vision-frontignan-2026-2040.html` | Même document, version consultation autonome (images base64) |
| `rapport-frontignan-analyse-territoriale.md` | 📊 **Rapport d'analyse territoriale** complet — entonnoir France→ville, 11 sections, 13 fiches projets, 249 sources |
| `rapport-frontignan-analyse-territoriale.html` | Version consultation autonome |
| `figures/` | 14 figures matplotlib (entonnoir, population, budget, frise projets, SWOT, priorisation, parties prenantes, mobilités, trajectoire 2026-2040, focus 2030, macro 2050, scénarios 2040, schéma territorial) |
| `visuals/` | 2 illustrations (vue isométrique « Frontignan 2030 », carte d'identité stylisée) |
| `scripts/` | Générateurs Python : `make_figures.py`, `make_figures_vision.py` (matplotlib), `make_html.py` (md→html autonome), `make_deck.py` (deck) |

## 🔎 Points clés

- **Fenêtre rare 2026-2032** : friche Mobil (11 ha) dépolluée et restituée (27 mai 2026), gare/PEM 25 M€ acté, SCoT du bassin de Thau en approbation, présidence de l'agglo.
- **Focale 2030** : 5 conditions de succès (PEM livré *et desservi*, friche programmée *et financée*, +300-600 emplois, qualité de l'eau de Thau, mixité du centre).
- **3 scénarios 2040** : S1 « Thau tranquille » · S2 « Couronne métropolitaine » · S3 « Pôle de la transition » ★.
- **Méthode** : sources croisées et datées, balises ✅ engagé / 📅 annoncé / 🔮 tendance / ⚠️ incertain, estimations propres distinguées des prévisions officielles.

## ▶️ Voir le deck

Ouvrir `index.html` dans un navigateur (fichier 100 % autonome, aucune connexion requise) — ou via le preview du monorepo : `/preview/frontignan/`.

## 🛠 Régénérer

```bash
pip install matplotlib markdown pillow
cd projects/frontignan
python3 scripts/make_figures.py            # 9 figures du rapport -> figures/
python3 scripts/make_figures_vision.py     # 5 figures de la vision -> figures/
python3 scripts/make_html.py rapport-frontignan-analyse-territoriale   # md -> html autonome
python3 scripts/make_html.py vision-frontignan-2026-2040
python3 scripts/make_deck.py               # deck -> index.html
```
