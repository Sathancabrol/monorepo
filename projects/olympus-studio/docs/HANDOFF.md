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

## Reprise v0.2.1 — développement du soir du 12 novembre

**Sources réelles :** dernier code sur `feat/olympus-studio-20261112`; CI GitHub `.github/workflows/olympus-studio-ci.yml`. Le paquet de test doit être téléchargé dans la dernière exécution **verte** (les artefacts de CI sont emballés dans un ZIP GitHub contenant un second ZIP du studio).

### Progrès codés
- `src/media-store.js` : coffre IndexedDB, conversion portable ≤45 Mo, reliaison automatique par layer ID ou `assetId`.
- `src/app.js` : export Portable; réhydratation des images/vidéos au chargement, y compris après import d'anciens projets.
- `src/meeting-utils.js` : import/export SRT et compte rendu Markdown, confidentialité des sous-titres par défaut.
- `src/v03-migration.js` : import de projet legacy v0.3, coordonnées 1280×720 vers normalisées, conservation de `meeting`, `edit`, `automation` sous `legacyV03` sans exécution.
- `tests/{media-store,meeting-utils,v03-migration}.test.mjs` pour garantir la sémantique de ces fonctions. Tous les tests passés doivent être vérifiés au **dernier** commit avant toute annonce.

### Blocages
- Browser Playwright dans l'environnement ChatGPT : `net::ERR_BLOCKED_BY_ADMINISTRATOR`, impossible de confirmer comportement IndexedDB réel ici.
- Tour Windows/GTX non accessible : aucune mesure FPS/VRAM/OBS réel/ComfyUI réel.
- Tâches ChatGPT 5/5 : demande d'agent récurrent non créée. Voir `docs/NEEDS_USER.md`.

### Trois actions suivantes
1. **S01** Tester v0.3 `smoke-portable.json` et fichier JSON actuel sur véritable Chromium (environnement approprié); corriger toutes pertes de média ou données; préparer une migration des notes/stories vers interface éditable.
2. **S04** Portage vertical storyboard/édition : clip media, trims, lecture, export A/V sur cas test, sans déclarer NLE complet.
3. **S02/S03** Validation OBS réel + transcription locale au choix de source audio (Sherpa/Whisper) avec export synchronisé.

Ne pas confondre **plan de sessions** (`docs/SESSION_PLAN.md`) et **sessions effectivement automatisées** ; ces dernières nécessitent une place ChatGPT libérée ou un agent externe réellement installé et autorisé.

## Checkpoint v0.2.2 — EDIT storyboard séquentiel

- `src/storyboard.js` : math de clips (image/vidéo), durée, résolution temporelle, réordonnancement, références média pour export portable.
- `src/app.js` : espace EDIT avec preview Canvas séparée de la scène LIVE, clips ajoutés depuis LIBRARY, ordre, durée, titre, lecture et export WebM silencieux (≤120s). Un changement d'espace arrête un export en cours.
- Les références clips sont incluses dans le JSON et les médias de clips dans l'export « Portable » (≤45 Mo).
- Aucun éditeur audio multipiste ni rendu image+audio combiné dans EDIT. La sortie LIVE reste indépendante.
- `tests/storyboard.test.mjs` : modèle de clips et union des références testés ; refaire `npm test` et vérifier la CI après chaque commit.
- **Vérification Chromium Windows obligatoire avant de déclarer le montage fonctionnel en production.**
- Limite automate inchangée : ChatGPT 5/5, planning stocké dans SESSION_PLAN mais pas d'agent programmé.

## Checkpoint immédiat — 12 novembre 2026, v0.2.3

**Exécution immédiate de la tâche automatique** `6af632ef3df88191a7ef46e372054ac4` demandée par l'utilisateur, en plus du planning quotidien à 02:00 Europe/Paris.

**Livrable S04 :** `src/storyboard.js` expose `trimVideoClip`, `splitVideoClip`, `splitStoryboardAt`; `src/app.js` ajoute le bouton « Diviser au curseur » et les champs vidéo IN/OUT. Le projet reste séquentiel et l'export reste vidéo seule; les sources IndexedDB ne changent pas. [Procédure](EDIT_TRIM.md).

**Preuve CI :** https://github.com/Sathancabrol/monorepo/actions/runs/43316401111 (29 tests réussis). Le dernier commit de documentation/version peut déclencher une nouvelle exécution; vérifier à la prochaine session.

**Prochaines trois priorités :**
1. Relecture matérielle réelle d'un fichier vidéo : relever `duration`, bloquer OUT au-delà, vérifier la prévisualisation après split/trims, créer un test navigateur E2E exécutable.
2. Intégration de l'audio dans EDIT et export A/V synchronisé sans dégrader LIVE.
3. Audit FreeCut/OpenReelio (licences et interchange), puis migration contrôlée du prototype v0.3 et ajout du module XR/Meeting.

Aucun merge main; aucun accès à la tour, aucun nouveau logiciel tiers installé.

## Checkpoint v0.2.4 — 13 novembre 2026

- `src/video-duration.js` (nouveau) : durée réelle `HTMLVideoElement`, cas timeout/erreur, `initialClipDuration` et contrôle IN/OUT fondé sur métadonnées.
- `src/app.js` : affiche la durée source, adapte le premier clip, refuse OUT au-delà du fichier quand la durée est connue. Anciennes coupes invalides signalées, jamais raccourcies sans accord.
- `tests/video-duration.test.mjs` : métadonnées immédiates/asynchrones, rejet valeurs invalides et source-bounded trim.
- `tests/browser_media_smoke.py` : smoke UI avec vidéo WebM 2 s, vérifié dans Chromium headless au cours de la session. Le test utilise les modules en mémoire car l'environnement de navigateur bloque toute navigation HTTP; il ne valide pas IndexedDB ni OBS/ComfyUI.
- `docs/EDIT_TRIM.md` mis à jour. Tests `npm test` : 34/34 réussis en CI puis localement sur Node.js 22 au cours de la session, sous réserve de revérifier le dernier commit.
- Sur GitHub branche dédiée uniquement; automatisation quotidienne à 02:00 Europe/Paris maintenue.

### Trois priorités pour la prochaine session
1. Tester la persistance IndexedDB et la sauvegarde/reprise du même clip scindé dans un navigateur avec vraie origine HTTP (Windows ou environnement autorisé), puis corriger les divergences.
2. Ajouter un parcours audio EDIT cohérent : provenance, synchronisation des clips et export WebM A/V contrôlé (sans rompre LIVE).
3. Comparer FreeCut / OpenReelio sur un exemple concret et choisir une stratégie d'intégration; poursuivre les passerelles X-Ray / Watchtower / Chronos.

Aucun merge de `main` ni installation distante; les résultats de tests Chromium ne doivent pas être présentés comme essais matériels Windows.

## Checkpoint session nocturne — 13 novembre 2026, correctif EDIT

- Relecture du checkpoint v0.2.4, STATUS, SESSION_PLAN, ROADMAP et PR #16 avant modification.
- Correction d'un contournement de validation : le champ « Durée » modifiait directement `outPoint` sans respecter la durée réelle du fichier, contrairement aux champs IN/OUT. Désormais `setClipDuration` passe par `trimWithinVideoDuration`, conserve les fichiers originaux et refuse une durée hors source.
- Modification du montage bloquée pendant un export en cours; les durées invalides provoquent un message explicite. Ajout d'un test de régression pour ce chemin UI.
- Commit de test : `cc4ebc9fc71e67e91d65ff943fe6e0df6ebb3f75`. Vérifier le run CI correspondant avant de déclarer cette itération validée.
- État : **codé et testé au niveau unitaire après CI**, pas de test de l'interface modifiée sur Windows; aucun merge, aucune installation distante.

### Prochaines priorités
1. E2E navigateur sur vraie origine HTTP et IndexedDB : importer/sauvegarder/recharger des clips vidéo scindés, vérifier médias et bornes.
2. S04 : piste audio EDIT, synchronisation A/V, export WebM avec audio et tests de dérive.
3. S02/S06 : essais OBS et ComfyUI réels sous Windows autorisé, puis intégration XR et Watchtower.
