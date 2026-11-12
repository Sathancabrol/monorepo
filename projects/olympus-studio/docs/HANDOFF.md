# Checkpoint de reprise — 2026-11-12

## Références
- Dépôt : https://github.com/Sathancabrol/monorepo
- Branche de travail : `feat/olympus-studio-20261112`
- Dossier : `projects/olympus-studio/`
- Suivi : https://github.com/Sathancabrol/monorepo/issues/11 à #15
- Prototype plus ancien dans la conversation : `olympus_studio_v03.zip` (artefact local non encore importé intégralement).

## Ce qui est livré
- 12 espaces dans la même interface.
- Canvas 2D et scènes/calques, texte/forme, fichiers image/vidéo et webcam autorisée, PNG, WebM Canvas **sans piste audio**, transcription manuelle, export SRT, événement de détection XR importé manuellement.
- Serveur HTTP Node sans dépendances, diagnostic des ports OBS et ComfyUI, envoi volontaire de workflow API JSON vers ComfyUI local.
- Sauvegarde et chargement JSON **sans médias embarqués**, tests HTTP décrits mais pas encore exécutés sur Windows.
- Les moteurs OBS, FreeCut/OpenReelio, Whisper et Watchtower ne sont PAS intégrés dans ce scaffold.

## Vérifications conduites
- Les fichiers GitHub ont été créés avec succès sur la branche.
- `src/app.js` : parse JavaScript isolé réussi.
- `server.mjs` : parse du corps après adaptation de `import.meta` réussi, **pas test du serveur**.
- Prototype local v0.3 distinct : `python smoke_test.py` = all tests passed (cette vérification n'est pas un test Windows).

## Prochaines 3 actions techniques
1. Télécharger/extraire le socle GitHub sur un poste test et exécuter `npm test`, `npm start`; corriger tout échec. En parallèle réunir la version local v0.3 en copie de sauvegarde et réaliser sa migration contrôlée (issue #11).
2. Benchmark import/export FreeCut vs OpenReelio : format projet, ressources GPU, vidéo synthétique de référence et stratégie d'éditeur unique (issue #12).
3. Interface OBS WebSocket v5 avec contrôle de scène et enregistrement sur bouton, plus capture audio système séparée (issue #13).

## Reprise sûre
Ne toucher qu'au dossier `projects/olympus-studio/` et à sa branche tant qu'un merge n'a pas été autorisé. Ne modifier ni Watchtower ni Cognitorium ni les réglages Hermes. Conserver une matrice « annoncé / codé / testé / testé chez l'utilisateur ». Aucun programme ne travaille en continu hors tâche explicitement planifiée.
