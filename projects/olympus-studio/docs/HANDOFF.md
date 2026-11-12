# Checkpoint de reprise — 2026-11-12

## Références
- Dépôt : https://github.com/Sathancabrol/monorepo
- Branche de travail : `feat/olympus-studio-20261112`
- Dossier : `projects/olympus-studio/`
- Suivi : https://github.com/Sathancabrol/monorepo/issues/11 à #15\n- Pull request brouillon non fusionnée : https://github.com/Sathancabrol/monorepo/pull/16\n- CI ciblée : `.github/workflows/olympus-studio-ci.yml` (créée ; exécution non confirmée)
- Prototype plus ancien dans la conversation : `olympus_studio_v03.zip` (artefact local non encore importé intégralement).

## Ce qui est livré
- 12 espaces dans la même interface.
- Canvas 2D et scènes/calques, texte/forme, fichiers image/vidéo et webcam autorisée, PNG, WebM Canvas **sans piste audio**, transcription manuelle, export SRT, événement de détection XR importé manuellement.
- Serveur HTTP Node sans dépendances, diagnostic des ports OBS et ComfyUI, envoi volontaire de workflow API JSON vers ComfyUI local, + flux MJPEG `/obs` depuis les images JPEG postées par la scène (pas d’audio).
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

## Reprise après itération v0.2 — 12 novembre, soir

- Commits sur la branche `feat/olympus-studio-20261112` uniquement; PR #16 toujours brouillon.
- Interface unique : régie OBS WebSocket v5 via `src/obs-client.js`, `src/obs-panel.js`; commandes scènes et REC (tests simulés uniquement).
- Capture écran / micro autorisée, piste audio optionnelle dans WebM ; non validée sous Windows.
- **Correctif sécurité** : le serveur refusait mal les dotfiles; liste blanche stricte de ressources et contrôle Origin/Host ajoutés.
- CI de référence : https://github.com/Sathancabrol/monorepo/actions/runs/43288150897 (13 tests / 13 réussis). Les nouveaux commits docs peuvent déclencher d'autres runs.
- Procédure Windows : `docs/OBS_REMOTE.md`.

### Trois priorités techniques révisées
1. **Essai OBS réel** : relier OBS 28+ depuis le panneau, changer de scène, démarrer/arrêter REC, vérifier les événements et les erreurs d'authentification. Préserver sorties privées/public.
2. **Essai audio/écran** : capture onglet et micro, exporter WebM, vérifier présence/qualité audio, fps et mémoire sur GTX 1060 puis GTX 1650.
3. **Convergence v0.3 / édition** : comparer l'archive locale du prototype v0.3 au socle GitHub et rapatrier IndexedDB, scènes/transitions, sous-titres et storyboard progressivement sous tests.

**Planification** : aucune automatisation nouvelle n'a été créée; la limite de 5 tâches actives n'a pas été contournée.

### Complément technique — GENERATE
- ComfyUI `/history/{prompt_id}` disponible via le proxy local `/api/comfy/job` et le bouton « Vérifier le dernier job ». Vérifier ComfyUI réellement démarré, job réussi/échoué, et gestion des types de sorties image/vidéo; import dans bibliothèque encore absent.
- Conserver les secrets et prompts sensibles sur la machine; le serveur bloque les requêtes web cross-origin pour les écritures.
