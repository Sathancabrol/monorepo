# EDIT — coupes non destructives (S04, première tranche)

## Fonctionnalités ajoutées
- **IN / OUT** pour chaque clip vidéo, en secondes de la source. Modifie le clip du projet, jamais le média conservé en IndexedDB.
- **Diviser au curseur** : scinde la vidéo sous le curseur de la timeline globale en deux clips avec le même `assetId` et des `id` différents. Le point de coupe est converti en temps de la source, y compris si le clip commence à un temps IN non nul.
- Les coupes et leur ordre sont conservés dans le JSON du projet; les deux segments réutilisent le même fichier de la médiathèque lors de l'export portable.
- Chaque portion doit avoir une durée >= 0,1 s. Les coupes hors du clip, sur une image, avec horodatages invalides ou trop proches des bords sont refusées.
- Dans EDIT, déplacer le curseur de prévisualisation sur un clip vidéo, cliquer **Diviser au curseur**, puis ajuster les champs **IN (s)** et **OUT (s)**.

## Limites
- Cette étape ne constitue pas un éditeur de montage multipiste. Pas encore de transitions, audio synchronisé dans l'export EDIT, gestion de la fréquence d'images source, snapping ni touches J/K/L.
- Les champs IN/OUT ne sont **pas encore bornés par la durée réellement lue dans le média** (metadata). Saisir un OUT supérieur à la durée réelle peut produire une image figée ou vide pendant la prévisualisation.
- L'export reste un WebM Canvas en temps réel, sans audio, limité à 120 s.
- Tests du modèle purs Node, **pas de test navigateur/Windows** : la reproductibilité de la prévisualisation et de l'export sur les GTX 1060 / GTX 1650 reste à vérifier.

## Preuves
- Code : `src/storyboard.js` (`trimVideoClip`, `splitVideoClip`, `splitStoryboardAt`) et `src/app.js` (panneau EDIT).
- Tests : `tests/storyboard.test.mjs` vérifie la conservation des sources, les bornes, le point de coupe global, la durée et la sauvegarde JSON.
- L'état de la CI GitHub figure dans `docs/STATUS.md`; une CI verte ne prouve pas un montage Windows fonctionnel.

## Étape suivante
Tester dans Chromium avec une vraie vidéo; lire `duration` pour limiter les bornes, préserver le montage à la réouverture, puis ajouter une piste audio synchronisée et comparer FreeCut/OpenReelio avant de remplacer le moteur simple.
