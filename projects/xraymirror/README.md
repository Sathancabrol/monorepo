# X-Ray Mirror Studio — socle expérimental v0.7

> Perception locale dans le navigateur : visage, mains, pose, objets, sons, overlays anatomiques schématiques, AirPaint, nutrition, cognition et centre de plugins.
>
> **Statut : prototype expérimental.** Ce dossier ne remplace pas les checkpoints
> v0.6.0 testés sur Windows par Hermes, et ne contient ni Écorché ni les 634
> structures anatomiques. Aucune validation webcam/GTX 1060 n'a été effectuée ici.

## Démarrage

```bash
cd projects/xraymirror
npm install
npm run dev          # http://localhost:4173
npm run build        # tsc --noEmit + vite build (dist/ committable)
npm test             # Vitest, cœur déterministe
```

La production statique est servie par le monorepo via `/preview/xraymirror/`
puisque `dist/index.html` est généré avec `base=./`.

### Modèles et wasm

- Les fichiers WASM MediaPipe nécessaires à `FilesetResolver` sont copiés dans
  `public/mediapipe/wasm/` (28 Mo, inclus dans le dépôt car sans eux aucune
  inférence n'est possible).
- Les modèles `.task`/`.tflite` **ne sont pas** committés (plusieurs dizaines de
  Mo). Les URLs Google épinglées sont utilisées à la première inférence, puis
  le cache HTTP du navigateur s'en charge. Pour un fonctionnement hors ligne :
  suivre `public/models/README.md`.
- Les SHA-256 du catalogue sont marqués `PENDING` : aucune vérification
  d'intégrité n'est prétendue dans cette version.

## Architecture

```
src/
├─ core/
│  ├─ types.ts            manifestes plugins, événements, réglages
│  ├─ eventBus.ts         bus borné + export JSONL
│  ├─ filters.ts          One Euro (lissage dépendant du temps)
│  ├─ gestures.ts         classifieur géométrique + stabilisateur
│  ├─ anatomy.ts          ancrages schématiques depuis pose 33
│  ├─ rules.ts            moteur Quand → Conditions → Action (sur events)
│  ├─ mediapipe.ts        Face/Hands/Pose/Objects/Gestures Tasks Vision
│  ├─ perception.ts       boucle cadencée, snapshots, métriques
│  ├─ audio.ts            analyse temps réel locale + transitoires
│  ├─ modelManager.ts     catalogue, cache local, URLs épinglées
│  ├─ paint.ts            traits + export SVG
│  ├─ nutrition.ts        Open Food Facts + cache local
│  └─ clientStore.ts      persistance localStorage
├─ ui/
│  ├─ useStudio.ts        orchestration caméra / moteurs / overlay
│  ├─ components.tsx      cartes, toggles, toasts
│  └─ panels/             12 panneaux fonctionnels
└─ App.tsx                navigation et assemblage
```

### Règles de conception

1. **Aucun plugin expérimental ne bloque le noyau.** Un moteur qui échoue
   affiche une erreur locale ; les autres continuent.
2. **Un seul gros travail GPU à la fois.** La boucle est sérialisée (`busy`).
3. **Rendu découplé de l'inférence.** Canvas en `requestAnimationFrame`,
   inférence cadencée (face/mains ~24 Hz, pose ~16 Hz, objets ~6 Hz).
4. **Événements bornés.** 3 000 événements en mémoire, export JSONL.
5. **Aucune frame vidéo n'est envoyée au réseau.** Le micro reste local aussi.
   Le seul appel réseau de contenu est Open Food Facts, déclenché par l'utilisateur.
6. **Honnêteté des statuts.** `ready` = code branché, pas « validé terrain » ;
   `preview` = démonstration à confirmer ; `planned` = pas de bouton actif.

## Ce qui fonctionne réellement dans ce socle

- Démarrage/arrêt caméra et micro avec gestion des permissions.
- Face Landmarker 478 points + blendshapes (sourire, clignement émis en events).
- Hand Landmarker, deux mains, geste local + geste MediaPipe optionnel.
- Pose Landmarker, overlay squelette et ancrages anatomiques schématiques.
- EfficientDet Lite0 : objets COCO, boîtes, compteurs.
- Audio : niveau temps réel + détection de transitoires (claquement).
- Règles locales et rétroaction (ex. claquement → couches anatomiques).
- Timeline, filtres, export JSONL, capture PNG.
- AirPaint : dessin par pincement, poing optionnel pour effacer, export SVG.
- Nutrition : recherche EAN Open Food Facts + cache local 7 jours.
- Exercices temps de réaction / mémoire spatiale avec export.
- Persistance des réglages, centre de plugins avec manifestes complets.

## Ce qui n'est **pas** implémenté (ne pas surestimer)

- Reconnaissance alimentaire par image, scan caméra de codes-barres, calories.
- OCR, VLM de scène, segmentation SAM, classification YAMNet/BEATs.
- Identification de personne, analyse d'émotion « réelle », mesure cognitive live.
- Atlas Écorché, BodyParts3D, 634 structures, maillages anatomiques.
- Installateur Windows, télémétrie, synchronisation, multi-utilisateur.
- Tests réels webcam/GTX 1060, audit de sécurité ou de licences.

## Intégration au monorepo

Le serveur racine détecte `dist/index.html`; après `npm run build`, l'entrée
`xraymirror` apparaît dans `/monorepo` et est servie par
`GET /preview/xraymirror/`.

## Licence et provenance

Code de ce socle : expérimental, à intégrer selon la licence du projet
X-Ray Mirror Studio. MediaPipe Tasks Vision et les modèles Google sont
Apache-2.0 (voir `src/core/modelManager.ts`). Open Food Facts est une base
ouverte avec ses propres conditions d'utilisation.

Le dépôt public `toyxyz/toyxyz_RGBMocap` reste une référence externe pour la
reconstruction 3D hors ligne ; il n'est pas intégré ici.

## Prévisualisation dans le monorepo

`dist/` est committée (assets + wasm) pour que `/preview/xraymirror/` fonctionne
sans build côté serveur. Les sources wasm de `public/mediapipe/` sont ignorées
par Git ; elles sont régénérées par :

```bash
npm ci
npm run prepare:wasm
npm run build
```

Le serveur statique autonome (sans Vite) et le test d'assets complet :

```bash
npm run serve                 # http://0.0.0.0:4173, sert dist/
npm run verify:preview -- http://127.0.0.1:4173/
```
