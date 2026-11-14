# EDIT — coupes non destructives (S04, première tranche)

## Fonctionnalités ajoutées
- **IN / OUT** pour chaque clip vidéo, en secondes de la source. Modifie le clip du projet, jamais le média conservé en IndexedDB.
- **Diviser au curseur** : scinde la vidéo sous le curseur de la timeline globale en deux clips avec le même `assetId` et des `id` différents. Le point de coupe est converti en temps de la source, y compris si le clip commence à un temps IN non nul.
- Les coupes et leur ordre sont conservés dans le JSON du projet; les deux segments réutilisent le même fichier de la médiathèque lors de l'export portable.
- Chaque portion doit avoir une durée >= 0,1 s. Les coupes hors du clip, sur une image, avec horodatages invalides ou trop proches des bords sont refusées.
- Dans EDIT, déplacer le curseur de prévisualisation sur un clip vidéo, cliquer **Diviser au curseur**, puis ajuster les champs **IN (s)** et **OUT (s)**.

## Limites
- Cette étape ne constitue pas un éditeur de montage multipiste. Pas encore de transitions, audio synchronisé dans l'export EDIT, gestion de la fréquence d'images source, snapping ni touches J/K/L.
- **Depuis v0.2.4**, EDIT lit la durée des vidéos via `loadedmetadata`/`durationchange` et refuse un OUT supérieur à cette durée lorsqu'elle est connue. Il adapte la durée du premier clip (maximum 5 secondes) aux vidéos courtes. Quand les métadonnées ne peuvent pas être lues, le contrôle ne peut pas garantir la limite; l'interface affiche « durée inconnue ».
- Un ancien projet dont la coupe OUT dépasse le fichier n'est pas modifié silencieusement : un avertissement s'affiche lorsque la durée source devient connue.
- L'export reste un WebM Canvas en temps réel, sans audio, limité à 120 s.
- Tests du modèle Node **et essai Chromium headless** avec une vraie vidéo WebM synthétique de 2 s : import, détection 2,00 s, refus OUT=5 s et division au curseur sans erreur JavaScript. La navigation HTTP étant bloquée dans l'environnement de test, les modules ont été chargés en mémoire ; **IndexedDB, la persistance et l'export réel sur Windows ne sont pas validés**.
- Test navigateur reproductible (facultatif, dépendances de développement) : `python -m pip install playwright` ; installer FFmpeg et Chromium, puis `python tests/browser_media_smoke.py`. Le script n'utilise ni réseau ni modèle IA.

## Preuves
- Code : `src/storyboard.js` (`trimVideoClip`, `splitVideoClip`, `splitStoryboardAt`) et `src/app.js` (panneau EDIT).
- Tests : `tests/storyboard.test.mjs` vérifie la conservation des sources, les bornes, le point de coupe global, la durée et la sauvegarde JSON.
- L'état de la CI GitHub figure dans `docs/STATUS.md`; une CI verte ne prouve pas un montage Windows fonctionnel.

## Étape suivante
Tester avec IndexedDB actif sur un véritable serveur HTTP/Windows : sauvegarder, recharger, relire les segments. Ajouter une piste audio synchronisée et comparer FreeCut/OpenReelio avant de remplacer le moteur simple.
