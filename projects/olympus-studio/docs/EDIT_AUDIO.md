# OLYMPUS Studio v0.2.5 — première piste audio dans EDIT

## Capacités déjà codées

- **+ Média** accepte désormais les fichiers `audio/*` (MP3/WAV/OGG si le navigateur sait les lire), en plus des images/vidéos.
- Le fichier audio est conservé dans le coffre IndexedDB existant, avec référence `assetId`; il n'est pas ajouté comme calque à la scène LIVE.
- Depuis **EDIT**, sélectionner un fichier dans « Piste audio EDIT », puis « Ajouter / remplacer piste ». Une seule piste sonore de fond est possible dans cette version.
- Réglages de la piste : départ sur le projet (secondes), point IN dans la source, volume de 0 à 1, activée/désactivée.
- Prévisualisation pilotée par l'horloge globale `editTime`. La position sonore vaut `inPoint + editTime - offset` pendant la fenêtre active.
- `projectPayload().editAudioTrack` conserve les paramètres; l'export « Portable » inclut aussi le fichier son, s'il existe dans IndexedDB.
- **Exporter WebM (audio optionnel)** tente de créer un `MediaStreamDestination` Web Audio local et d'ajouter sa piste sonore à la capture Canvas vidéo (MediaRecorder).

## Ce qui reste à vérifier et à construire

- **Pas encore validé sur l'ordinateur Windows** : lecture MP3/WAV, permission/autoplay, prévisualisation audible, enregistrement WebM réellement sonore, codec et dérive A/V sur 30 minutes.
- L'audio natif **des clips vidéo** n'est pas encore conservé dans EDIT : les vidéos de la timeline restent muettes; seule la piste sonore ajoutée peut être enregistrée dans l'export expérimental.
- Une piste sonore seulement, sans enveloppes, fondu, effets, waveform, ducking, automation de volume ni mixage multi-sources. Ce n'est pas encore un NLE/mixeur complet.
- Le chargement depuis IndexedDB dépend de l'origine du navigateur : pour changer de PC ou d'origine, utiliser « Portable ». La vérification complète de la réouverture après fermeture sur vrai HTTP/Windows reste ouverte.

## Preuves

- Contrat : `src/edit-audio.js`, fonctions `validateEditAudioTrack` et `audioAtTimeline`.
- Intégration : `src/app.js`, `src/storyboard.js:referencedAssetIds`, `server.mjs`, `index.html`.
- Node : `tests/edit-audio.test.mjs` teste validation, timing, source IN/offset, fin de piste, mute et références portables.
- Browser (facultatif, non inclus dans CI) : `tests/browser_media_smoke.py` crée un fichier WAV synthétique et teste le chargement/placement dans EDIT. **Une preuve d'exécution audio n'est pas encore disponible.**
- Les tests de CI sont syntaxiques/unitaires/HTTP : succès ne signifie pas que le son sera audible dans un WebM Windows.

## Prochaine validation reproductible

1. Sur Windows, importer un WAV de 2 secondes et une vidéo témoin, placer l'audio à +0,5 s, exporter WebM.
2. Ouvrir le fichier exporté avec un lecteur et `ffprobe` ; vérifier présence audio Opus, longueur, premier son et décalage son/image.
3. Enregistrer preuve et environnement (navigateur, modèle GPU, fps, taille) puis traiter les défaillances et ajouter des tests de régression.
4. Ensuite seulement : plusieurs pistes, audio des vidéos, transitions et mixage avancé.
