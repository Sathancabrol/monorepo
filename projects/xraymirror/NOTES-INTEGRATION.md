# X-Ray Mirror Studio — notes d'intégration

## Ce que ce dossier est

`projects/xraymirror/` est un **nouveau socle expérimental**, construit à part,
pour préparer l'expansion demandée (maximum d'outils et d'options) sans toucher
au code v0.6.0 que Hermes teste sur la tour Windows.

Le dépôt public `toyxyz/xray-mirror` n'était pas accessible depuis cet
environnement (`repository not found`), donc **aucun code de l'ancien
projet n'a été copié ou reconstitué ici**. Ce socle est autonome et se branche
par conventions (plugins, événements, modèles), pas par fusion de fichiers.

## État vérifié dans cet environnement

| Élément | État | Preuve |
|---|---|---|
| Compilation TypeScript stricte | OK | `npm run typecheck` |
| Tests unitaires + rendu | 37 tests / 11 fichiers | `npm test` |
| Build de production | OK (≈ 496 Ko JS, 14 Ko CSS) | `npm run build` |
| Preview monorepo | redirige vers `dist/index.html` | `curl /preview/xraymirror/` |
| Assets JS/CSS/WASM | HTTP 200, MIME correct, magic `\0asm` | `npm run verify:preview` |
| Webcam + modèles | **non validés** | pas de caméra ni GPU dans la sandbox |
| Modèles lourds (VLM, OCR, SAM) | **non intégrés** | marqués `planned` |
| Atlas Écorché / 634 structures | **non intégrés** | overlay schématique seulement |

## Correctifs apportés au monorepo

1. `app/main.py` : une entrée de preview imbriquée (`dist/index.html`,
   `output/visual/index.html`, `learning/index.html`…) redirige désormais vers
   son vrai chemin. Sans cela, `/preview/xraymirror/` renvoyait le HTML mais
   ses assets relatifs (`./assets/...`) étaient résolus à la racine du projet,
   donc en 404 — et `./mediapipe/wasm/...` également.
2. `app/templates/monorepo.html` : les iframes de preview autorisent
   `camera; microphone; fullscreen` via l'attribut `allow`, sinon la webcam
   serait bloquée par la politique d'autorisations du navigateur.
3. `.gitignore` racine : `projects/xraymirror/public/mediapipe/` est ignoré
   (28 Mo de wasm source). Le wasm **compilé** reste dans `dist/`, lui-même
   versionné par la règle existante `!projects/*/dist/**`.

## Ce qui a été volontairement refusé

- Faux boutons « Activer » pour des plugins non intégrés : le catalogue
  affiche « Prévu » et désactive l'action.
- Faux statut « installé » ou « prêt » : trois états seulement (`core`,
  `ready`, `preview`, `planned`).
- Fausse « anonymisation » : le floutage des captures est réellement appliqué
  aux zones de visage détectées (`blur` avant `toDataURL`), avec tests
  géométriques.
- Faux mode hors ligne : `local-only` échoue explicitement si le modèle est
  absent au lieu de télécharger silencieusement depuis Google.
- Faux ancrages anatomiques : la couverture ne compte que les segments dont
  les deux extrémités ont une visibilité ≥ 0,35 ; les 15 ancrages réels sont
  comptés, pas 13 ni 634.

## Prochaine étape recommandée

1. Brancher le scan caméra de codes-barres (`BarcodeDetector` natif, avec
   repli `@zxing/browser`) dans le plugin Nutrition, en conservant l'action
   explicite avant tout réseau.
2. Ajouter un vrai classifieur audio (YAMNet/TFLite ou Sherpa-ONNX) à la place
   du détecteur de transitoires, avec un cache local et une empreinte SHA-256.
3. Préparer le connecteur avec le vrai dépôt Studio : importer les 12 fichiers
   de modules validés par Hermes sous `src/legacy/` et les exposer via des
   adaptateurs, sans mélanger les dépendances.
4. Ajouter un test de performance reproductible (120 s de replay vidéo) avec
   p50/p95 par moteur, VRAM et FPS, exécutable par Hermes sur la GTX 1060.

## Limites de sécurité

- Aucune authentification, aucun stockage distant, aucune télémétrie.
- Deux appels réseau possibles, tous deux explicites : Google MediaPipe
  (téléchargement des modèles) et Open Food Facts (recherche d'un EAN).
- Aucune exécution de code arbitraire depuis une règle ou un preset.
