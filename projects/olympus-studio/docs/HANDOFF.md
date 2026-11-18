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

## Checkpoint v0.2.5 — 13 novembre 2026

- Le chantier est désormais piloté automatiquement par `docs/AUTONOMOUS_BACKLOG.md` et la tâche quotidienne ChatGPT (ID `6af632ef3df88191a7ef46e372054ac4`, 02:00 Europe/Paris). Elle doit sélectionner la première tâche `READY` et **passer les étapes bloquées par Windows**, sans demander « continue ».
- Nouveauté visible : fichiers audio importables via `+ Média`, piste EDIT indépendante, offset/IN/volume/activée, sauvegarde JSON/portable, et tentative de WebM A/V via Web Audio. Aucun audio n'est injecté dans LIVE par cette fonction.
- Modèle et tests : `src/edit-audio.js`, `tests/edit-audio.test.mjs`. UI dans `src/app.js`, serveur autorise `/src/edit-audio.js`, test HTTP dédié.
- `tests/browser_media_smoke.py` augmenté d'une fixture WAV et d'un contrôle de placement; pas encore exécuté/validé dans l'environnement Windows utilisateur.
- Détails, limites et protocole de validation : `docs/EDIT_AUDIO.md`.

### Première tâche de la prochaine session
A01 reste **ouvert** : confirmer que l'export audio/vidéo crée une véritable piste audible et synchronisée, avec test de décalage et correction des erreurs; si impossible sans matériel, avancer sur A02 (IndexedDB navigateur/HTTP). Ne pas commencer plusieurs gros modules sans valider la CI.

Aucun accès au PC, aucun achat, aucun merge de main, aucun autre dépôt modifié.

## Planification horaire — 13 novembre 2026

- **Modification confirmée par Automations** : `6af632ef3df88191a7ef46e372054ac4` demeure active, RRULE `FREQ=HOURLY;INTERVAL=1`, démarrage `20261113T040000 Europe/Paris`. Premier prochain déclenchement rapporté : 13/11/2026 à **04:00 locale**, puis une fois par heure.
- L'instruction horaire demande de **terminer une tranche testable et d'enchaîner la suivante pendant le même run**, tant que le contexte et les outils le permettent. À l'arrêt, écrire un checkpoint pour que le run suivant reprenne sans demander « continue ».
- Plan autonome : `docs/AUTONOMOUS_BACKLOG.md`; estimation relative : `docs/WORK_ESTIMATES.md`.
- L'historique des sessions plus anciennes mentionne l'ancienne cadence 02:00 quotidienne; **ce checkpoint plus récent la remplace**.
- A01, export A/V EDIT, reste ouverte tant qu'aucun WebM sonore et synchronisé n'a été prouvé. Passer à A02/A03 si contraintes navigateur/Windows empêchent son essai, et ne pas relancer inutilement le même correctif.
- La récurrence horaire ne transforme pas le chat en daemon continu et ne garantit pas une heure de développement effectif par passage. Aucun agent résident Windows n'a été installé.

## Checkpoint technique — 13 novembre 2026, 04h — A02 navigateur/IndexedDB

- Vérification préalable : backlog, STATUS, SESSION_PLAN, ROADMAP, PR #16 et issues #11–#17 relus. CI précédente run 43349763003 : job smoke terminé avec succès; ne pas confondre avec le nouveau code.
- Livré : `tests/browser_indexeddb_e2e.py` avec serveur HTTP local Node et Playwright Chromium, écrit un Blob IndexedDB, recharge réellement l'origine, contrôle les octets, utilise `splitVideoClip` pour deux segments de même source, vérifie une seule référence média, puis export/import Portable. Test limité à un Blob synthétique, pas une lecture A/V.
- CI : `.github/workflows/olympus-studio-ci.yml` installe Playwright 1.56.0 + Chromium et exécute le nouveau test; **résultat de la CI du nouveau commit à confirmer**. Commits de fonctionnalité : `d79772d7`, `b6a7788e`, `d688b9a7`.
- Prochaine action **prioritaire** (taille S) : vérifier la CI du dernier commit, lire les logs d'échec, réparer Playwright, puis compléter le parcours E2E UI import/sauvegarde/reprise. Ensuite A01/A03 (taille M) : capture WebM avec WAV synthétique et analyse audio Opus/dérive. Ne pas prétendre avoir testé Windows.

## Checkpoint A02 — 13 novembre 2026, 05h — réparation CI et reprise Portable

- **Erreur détectée** dans le workflow CI dédié : le nouveau step Chromium avait été écrit avec des séquences littérales `\\n` au lieu de vrais sauts de ligne YAML. Cela rendait le step invalide et empêchait son exécution. Correctif commit `a83a31a9`, fichier `.github/workflows/olympus-studio-ci.yml` uniquement.
- **Test renforcé** commit `eabbd614` : après le premier rechargement HTTP/IndexedDB, le scénario réimporte le Portable dans une nouvelle transaction, recharge encore le navigateur et contrôle les octets restaurés, puis nettoie le média temporaire.
- **Preuve disponible** : lecture GitHub du YAML corrigé, avec de vrais retours à la ligne; code de test ajouté. **Pas de run CI vert confirmé pour ces commits** (l'API de statut consultée n'a retourné aucun check); ne pas marquer A02 DONE.
- **Prochaine action exacte, taille S** : lire le dernier run de `olympus-studio-ci.yml` et ses logs; corriger toute erreur Python/Playwright. Puis, **taille M**, ajouter le parcours UI sauvegarde/rechargement des clips, et revenir à A01/A03 export WebM audio réel.
- Aucun test sur la tour Windows, aucune modification des autres projets, aucun merge.

## Checkpoint A02 — 13 novembre 2026, 06h — import média par l'interface

- Relecture des documents de pilotage, PR #16, tickets #11–#17, workflow CI et scénario IndexedDB avant écriture.
- **Nouveau test E2E réel-origine HTTP codé** : `tests/browser_indexeddb_e2e.py` pilote maintenant le champ `#fileMedia` dans Chromium Playwright, importe un PNG 1×1 via l'interface, vérifie son stockage IndexedDB, recharge le navigateur puis confirme le média et ses octets en base (taille). Le scénario API existant continue à tester split et aller-retour Portable.
- Commit de test : `a7819e49df64eb4ec80864d5d1cea694be4128a3` (branche isolée). **Pas de preuve CI verte pour ce commit** : la recherche des runs liés a retourné zéro résultat lors de la session; la CI précédente `43362826557` a été annulée, ce qui n'est pas une preuve d'échec de tests. Les annulations peuvent venir de `cancel-in-progress: true`.
- Ce test **ne valide pas** la sauvegarde d'un projet complet via les boutons de l'interface, ni l'export A/V, ni Windows. Il reste à vérifier la présence du média dans l'UI après rechargement et l'export/import Portable par l'UI.
- **Reprise exacte (taille S)** : récupérer le run CI le plus récent sur la branche, inspecter le job Chromium et corriger immédiatement si rouge. **Ensuite (taille M)** : E2E de projet complet `#btnPortable`/`#fileProject`, puis A01/A03 fixture WebM + son et vérification codec Opus/décalage. Aucun merge ni installation sur Windows.

## Checkpoint A02 — 13 novembre 2026, 07h — export/import Portable via l'interface

- **Incrément E2E livré** : `tests/browser_indexeddb_e2e.py` pilote `#btnPortable`, capture le fichier JSON réellement téléchargé, vérifie la scène et l'unique média intégré, efface volontairement l'enregistrement IndexedDB de la fixture, recharge la page puis importe le JSON par `#fileProject`. Il contrôle le calque réapparu et l'égalité octet à octet du PNG restauré. Aucun média utilisateur n'est utilisé.
- Commit de code : [`16ef2e1d`](https://github.com/Sathancabrol/monorepo/commit/16ef2e1da3c5099eb5844f80a6f672f85684be8e). CI associée [`43376152256`](https://github.com/Sathancabrol/monorepo/actions/runs/43376152256) **en cours à la consultation**, donc ne pas déclarer A02 validée.
- **Limites** : test Chromium Linux/HTTP automatisé, sans preuve Windows, ni sauvegarde du montage de clips par les boutons UI, ni export WebM audio audible. A01 et A02 restent ouverts.
- **Reprise exacte (S)** : lire les étapes/logs de la CI `43376152256`; si échec, corriger d'abord le test ou le produit. Si succès, poursuivre A01/A03 (M) : fixture WebM A/V avec inspection du codec Opus, présence sonore et dérive; ne pas confondre présence de piste et qualité audio.

### Correctif CI de la session — 13 novembre 2026, 07h

- Diagnostic **confirmé par les logs** du run [43376152256](https://github.com/Sathancabrol/monorepo/actions/runs/43376152256) : 39/39 tests Node réussis, mais Playwright 1.56 ne peut installer Chromium sur l'image `ubuntu-latest` devenue Ubuntu 26.04 (`Playwright does not support chromium on ubuntu26.04-x64`). Ce n'est **pas** un échec démontré du test UI.
- Correction du **workflow dédié seulement** : `runs-on: ubuntu-24.04` au lieu de `ubuntu-latest`, commit [`6837a003`](https://github.com/Sathancabrol/monorepo/commit/6837a00363daae6d865ab0018adf90074ff7568c). Cette image est une cible supportée par Playwright 1.56; attendre la CI du commit pour confirmer.
- Prochaine action exacte (S) : lire le dernier job sur Ubuntu 24.04; si erreur du scénario UI, inspecter traceback et corriger. Ensuite A01/A03 (M) : fixture A/V Opus avec mesure de dérive. A02 reste ouverte jusqu'à CI verte.

## Checkpoint A01/A03 — 13 novembre 2026, 08h — garde-fou codec Opus

- État initial relu : backlog, HANDOFF, STATUS, SESSION_PLAN, ROADMAP, PR #16, tickets #11–#17, workflow. La CI du correctif Ubuntu 24.04 (run 43376280105) est **annulée** ; elle ne prouve ni succès ni échec du scénario E2E. Le run antérieur 43376152256 était rouge sur l'installation Chromium Ubuntu 26.04 (avant correction).
- **Correctif fonctionnel livré** : auparavant EDIT choisissait `video/webm` si le navigateur refusait `vp8,opus`, ce qui pouvait faire passer un export silencieux pour un export avec audio. Nouveau module `src/editor-export.js` : lorsque la piste audio est demandée, accepte explicitement `vp8,opus` ou `vp9,opus`, sinon affiche une erreur et ne lance pas MediaRecorder. En vidéo seule, repli VP8/VP9/WebM autorisé.
- Fichiers : `src/editor-export.js`, `tests/editor-export.test.mjs`, `src/app.js`, `server.mjs` (allowlist locale), workflow CI dédié (vérification syntaxique). Commits `36a4efa9`, `92696511`, `cbb09b36`, `4cef6b37`, `63a420e0`.
- **Preuve** : tests unitaires écrits pour les cas Opus disponible/indisponible, et vérification de code statique par lecture. **Pas encore de run CI vert constaté au dernier commit**, ni de fichier WebM analysé. Cela empêche uniquement un repli silencieux; cela **ne prouve pas** la présence d'audio audible, la synchronisation ni l'absence de dérive.
- **Prochaine action exacte (S)** : récupérer le dernier run CI du commit `63a420e0` ou successeur, lire les logs du job Chromium et réparer les erreurs. **Ensuite (M)** : générer un vrai WebM A/V synthétique dans Chromium, examiner la piste Opus et mesurer début/durée via ffprobe. **Ensuite (M)** : consolider A02 (scène/clips UI et rechargement) sans tests Windows simulés.
- A01/A02/A03 restent ouverts, aucune modification hors périmètre, aucune fusion main.

## Checkpoint 13 novembre 2026, 09h — réparation CI A02

- Lecture des logs [run 43383108337](https://github.com/Sathancabrol/monorepo/actions/runs/43383108337) : `Static parse` et `API smoke tests` verts; l'E2E Chromium a expiré à la ligne 75 en attendant `olympus-ui-fixture.png`. Chromium a bien été téléchargé sous Ubuntu 24.04. Il ne s'agit plus de l'erreur de support Ubuntu 26.04.
- **Cause déduite du code, à confirmer par CI** : `src/app.js` importe `./video-duration.js`, mais la liste statique de `server.mjs` ne contenait pas `/src/video-duration.js`; le navigateur reçoit donc 403 et n'initialise pas l'interface. Correctif [ca9fc17e](https://github.com/Sathancabrol/monorepo/commit/ca9fc17eb4d2c492549c525d2e302534b76020a1).
- **Test de non-régression** : [d8df55a3](https://github.com/Sathancabrol/monorepo/commit/d8df55a3ff988548743540bf558315f5567083a9) vérifie HTTP 200 sur ce module, les 12 espaces réellement initialisés et l'absence d'erreurs JavaScript avant le parcours IndexedDB.
- **Validation** : correctif et test codés; pas encore de preuve d'exécution Chromium verte sur ces commits. A01/A02/A03 restent ouverts. Aucune intervention Windows ni merge main.
- **Reprise exacte, taille S** : consulter la CI du dernier commit, réparer tout nouveau traceback, confirmer le parcours IndexedDB/Portable. **Ensuite, taille M** : fixture A/V WebM Opus réelle avec analyse ffprobe et mesure de dérive; puis sauvegarde de clips via UI.

## Checkpoint 13 novembre 2026 — 10 h — A03 fixture A/V

- **Vérification CI précédente** : run [43390610164](https://github.com/Sathancabrol/monorepo/actions/runs/43390610164), job `smoke` **success**. Ce run suit le correctif de l'allowlist HTTP et les tests E2E, mais ne valide pas la fixture A/V ajoutée ensuite.
- **Code nouveau** : `tests/browser_av_fixture.py` produit un WebM synthétique à partir d'un Canvas animé et d'un oscillateur Web Audio, via MediaRecorder Chromium, sans caméra/micro/fichier personnel. `ffprobe` doit constater un flux VP8/VP9 et un flux audio Opus; le test échoue si un flux manque. Le workflow CI dédié exécute ce test après l'E2E IndexedDB. Commits `b6550d00` et `af3c84cc`.
- **Limite essentielle** : il s'agit d'une preuve de capacité de l'encodeur navigateur, pas encore d'un export EDIT de l'application, ni d'une mesure de dérive ou de volume audible. Le test n'a pas encore de résultat CI constaté sur ces commits; A01/A03 restent ouverts.
- **Reprise exacte (S)** : lire la CI du dernier commit `af3c84cc` ou suivant et réparer les erreurs de génération/ffprobe. **Ensuite (M)** : piloter le bouton `Exporter WebM (audio optionnel)` d'EDIT sur média synthétique et analyser la sortie via ffprobe, comparer durées/début audio/vidéo; poursuivre A02 UI clips.

## Checkpoint 13 novembre 2026, 11 h — A03 vérification temporelle et niveau sonore

- **CI du précédent incrément confirmée verte** : [run 43397793335](https://github.com/Sathancabrol/monorepo/actions/runs/43397793335), job `smoke` success, y compris Chromium E2E IndexedDB et fixture A/V Opus. Ceci valide une **fixture d'encodeur**, pas l'export EDIT.
- **Nouvelle tranche codée** : `tests/browser_av_fixture.py` vérifie désormais les paquets réels via `ffprobe -show_packets` : bornes temporelles des pistes audio et vidéo, durée >0,7 s, écarts de début et de fin <0,5 s. Décode l'audio avec FFmpeg `volumedetect` et exige un niveau moyen non silencieux. Le test imprime les écarts et le volume mesurés. Commit `2ef71e5e011f1cad159a3a3b8dc6b42152514177`.
- **Limites** : seuils de fumée larges, pas une mesure précise de dérive ni preuve d'écoute humaine; la fixture ne passe pas par le bouton d'export EDIT. **CI du nouveau commit à vérifier** avant de déclarer ces assertions réussies. A01/A03 restent ouverts.
- **Prochaine action exacte (S)** : inspecter le job CI du commit `2ef71e5e`; corriger toute erreur FFprobe, décodeur ou timing. **Ensuite (M)** : E2E export WebM du véritable éditeur EDIT avec WAV de synthèse et inspection ffprobe/volumedetect. Puis **(M)** : clips EDIT persistés via l'interface et restauration Portable. Aucun test Windows/OBS/ComfyUI réel.

## Checkpoint 13 novembre 2026 — correction FFmpeg A03

- Relecture backlog, HANDOFF, STATUS, SESSION_PLAN, ROADMAP, état A03 et CI. La recherche de runs pour `2ef71e5e` retourne [43406132636](https://github.com/Sathancabrol/monorepo/actions/runs/43406132636) **annulé** : ce n'est ni un succès ni un échec de test. Le run antérieur [43397793335](https://github.com/Sathancabrol/monorepo/actions/runs/43397793335) était vert pour la fixture A/V avant les nouveaux contrôles temporels/volume.
- **Bug certain identifié par inspection** : la regex Python raw-string `mean_volume:\\\\s*(-?[\\\\d.]+) dB` cherchait des antislashs littéraux, pas les espaces et chiffres de FFmpeg. Correction `b1ff456b` vers `mean_volume:\\s*(-?[\\d.]+) dB` et assertion de non-régression `b9eea37b` sur une ligne représentative de `volumedetect`. Vérification locale de la regex Python : PASS. Les contrôles FFprobe/FFmpeg complets n'ont pas été exécutés localement dans cette session.
- **CI du nouveau commit : à confirmer**; ne pas considérer A03 validée tant que la fixture réelle n'a pas produit ses mesures en CI. Pas de preuve d'export via le bouton EDIT ni de validation Windows.
- **Prochaine action exacte (S)** : consulter la CI du dernier commit `b9eea37b` et ses logs; réparer si rouge. **Ensuite (M)** : E2E réel du bouton export EDIT avec média WAV synthétique, inspection Opus, énergie sonore et bornes A/V. **Puis (M)** : reprise et sauvegarde des clips EDIT depuis UI/Portable. Aucun secret ni merge main.

## Checkpoint 13 novembre 2026, 12 h — A01/A03 export EDIT réel

- **CI précédente vérifiée verte** : [43406804015](https://github.com/Sathancabrol/monorepo/actions/runs/43406804015), job smoke, dont Chromium IndexedDB et fixture A/V FFprobe avec mesures de durée et niveau sonore. La fixture est indépendante de l'application et ne prouve pas l'export EDIT.
- **Nouvel incrément** : `tests/browser_edit_export_e2e.py` démarre le vrai serveur HTTP Studio, importe un PNG et un WAV 440 Hz synthétiques via l'UI, crée un clip de 2,5 s, assigne la piste audio et **clique le vrai bouton « Exporter WebM (audio optionnel) »**. Il sauvegarde le téléchargement et vérifie par `ffprobe` VP8/VP9 + Opus, paquets A/V, écarts de début/fin <0,6 s, et par `ffmpeg volumedetect` un niveau audio non silencieux. Aucune caméra, donnée personnelle ni Windows.
- Commits : [382132e0](https://github.com/Sathancabrol/monorepo/commit/382132e0f8ec4cedc594e2846128b8a647e54e05) (test) et [bea7edf6](https://github.com/Sathancabrol/monorepo/commit/bea7edf635b1f0dc2e99a992b6c808717136dbfb) (workflow CI). **Ce nouveau scénario est codé, mais pas encore déclaré réussi** : consulter les résultats CI au dernier commit, diagnostiquer tout échec et corriger avant de clôturer A01/A03.
- **Prochaine action exacte (S)** : consulter le dernier run CI du commit suivant ce checkpoint, notamment le step `Chromium EDIT export E2E`, analyser logs et corriger les erreurs éventuelles de sélecteurs, d'initialisation AudioContext, d'export ou de timing. **Ensuite (M)** : persistance/reprise des clips et audio EDIT via l'UI Portable et nouveau test E2E. **Puis (M)** : A04 undo/redo. Tests matériels Windows GTX1060/1650 et écoute humaine non réalisés.


## Checkpoint 13/11/2026 13h — correction CI A03

- Base examinée : `d56a9fd2d617ca6f0aef8a6b5f59ffc13ec1542f`; run [43414135728](https://github.com/Sathancabrol/monorepo/actions/runs/43414135728) **rouge** à l'étape `browser_edit_export_e2e.py` : timeout sur `get_by_text('synthetic-440hz.wav')` (30 s).
- Diagnostic confirmé dans `src/app.js` : l'audio est volontairement un asset sans calque LIVE (`type==='audio' ? null : addLayer(...)`). Le nom n'est donc pas visible dans LIVE; il apparaît dans le sélecteur audio EDIT. Le test attendait à tort un calque visible.
- Correctif `7dbcb7823bd18a876579ca88ede4f1910ccc081f` : passage dans EDIT, vérification de l'option WAV dans la liste audio avant attribution de piste. Aucun code applicatif modifié.
- Dans le même run, la fixture Chromium synthétique séparée était **verte** : VP8 + Opus, audio décodé -19,5 dB, décalage début -0,021 s / fin -0,069 s; ce résultat ne valide PAS encore le bouton EDIT.
- **À reprendre impérativement** : lire la CI au commit `7dbcb782` ou ultérieur; si rouge inspecter le job et corriger. Puis vérifier l'export EDIT A/V avec FFprobe et FFmpeg, avant de passer à la persistance IndexedDB des clips + piste audio.
- Blocages : Windows/GTX/OBS/ComfyUI réels non accessibles. Estimation restante A03 : S à M selon nouveaux échecs; A02 audio E2E : M.


## Checkpoint 13/11/2026 14h — CI rouge A03, sélecteur audio natif

- CI du commit `be01a01b` : [run 43421595781](https://github.com/Sathancabrol/monorepo/actions/runs/43421595781) **failure** au step `Chromium EDIT export E2E`. Les étapes Node, HTTP/IndexedDB et fixture A/V synthétique réussissent.
- Logs précis : l'option `<option>synthetic-440hz.wav</option>` existe (65 résolutions), mais Playwright `wait_for()` attend par défaut l'état `visible`; les options d'un `<select>` natif sont cachées pour Playwright. Ce n'est pas une preuve de défaut d'import audio.
- Correctif test `66c72186824a98c4cc33668f885481e757f44c68` : `wait_for(state="attached")` puis sélection explicite par label avant `Ajouter / remplacer piste`. Aucun code applicatif touché.
- **À vérifier** : CI au dernier commit de cette branche; si rouge, lire les logs du job EDIT et corriger. Le vrai export EDIT WebM/Opus n'est pas encore validé. A01/A03 restent READY. Puis E2E reprise IndexedDB clips + piste audio (M), ensuite A04 undo/redo (M).
- Aucun test Windows/GTX ni écoute humaine; aucun merge main, secret ou projet voisin modifié.

## Reprise 13 novembre 2026, 15 h — vérification de la source audio EDIT

- Dernière CI confirmée verte avant modification : [run 43430777046](https://github.com/Sathancabrol/monorepo/actions/runs/43430777046), associée au checkpoint `ea0118db`. L'échec antérieur `43421595781` correspond au test Playwright qui attendait un `<option>` visible; correctif déjà intégré.
- Nouveau commit `1a23a96f94b92ccdb7f932137855227ab3eb30a2` : le test E2E du véritable export EDIT décode la piste Opus en PCM 8 kHz et vérifie par passages à zéro la fréquence du son synthétique attendu (440 Hz, tolérance 400–480 Hz). Ceci détecte une piste non silencieuse mais issue d'une mauvaise source. Pas de modification de l'éditeur ou des autres projets.
- **CI du nouveau commit non encore confirmée**. Aucun test Windows/GTX effectué. Prochaine action S : consulter le run de `1a23a96f` et réparer toute erreur; si vert, A02/M : ajouter E2E de réouverture des clips et de la piste audio par l'interface, puis A04/M : undo/redo non destructif.

## Reprise 13 novembre 2026, 16 h — Portable EDIT + audio

- État initial vérifié : PR #16 brouillon, tête `8c5fef27`; run CI [43439755908](https://github.com/Sathancabrol/monorepo/actions/runs/43439755908) **success** (dernier checkpoint précédent, test de provenance 440 Hz inclus).
- Nouvelle tranche livrée : [6004d688](https://github.com/Sathancabrol/monorepo/commit/6004d68894760721f71438308bfc48e6b64790ef) complète `tests/browser_edit_export_e2e.py`. Avant l'export WebM, l'interface télécharge un Portable du montage EDIT (clip image de 2,5 s + piste WAV), contrôle deux médias intégrés sans doublon, recharge la page HTTP, réimporte le Portable, réexporte et compare clips, réglages audio et références de médias. Le test poursuit ensuite le vrai export WebM/Opus.
- **État de preuve** : code poussé, CI du nouveau commit à vérifier. Ne pas annoncer l'aller-retour comme réussi avant un run vert. Aucun essai Windows ni écoute humaine.
- **Reprise exacte (S)** : inspecter CI du commit 6004d688 et corriger tout échec de réimport UI ou d'export A/V; si vert, étendre à deux segments vidéo du même assetId sauvegardés et restaurés (M), puis A04 undo/redo (M). Ne pas toucher aux autres projets ou à main.

## Reprise 13 novembre 2026, 17 h — A02 deux segments vidéo Portable

- Vérification du run [43448613925](https://github.com/Sathancabrol/monorepo/actions/runs/43448613925) associé au checkpoint `064f858f` : **success**. Le run 43448586178 était **cancelled**; ne pas le compter comme succès.
- Nouveau test Chromium sur HTTP ajouté dans `tests/browser_edit_export_e2e.py`, commit [e587aa06](https://github.com/Sathancabrol/monorepo/commit/e587aa0630f936a997c2fbd18f0471c3426d2d88) : après validation du vrai export A/V, génère un WebM vidéo synthétique de 2 s, l'importe via l'UI, crée un clip, le divise à 1 s local sur la timeline, contrôle deux IDs de segments distincts partageant un assetId, l'absence de duplication des trois médias (PNG, WAV, WebM) dans Portable, puis le rechargement et la réexportation identiques.
- **Validation** : scénario codé/poussé, mais **CI du nouveau commit non encore vérifiée**. Le test utilise FFmpeg/libvpx, Chromium headless Linux; aucun Windows/GTX ni écoute humaine.
- **Prochaine action S** : vérifier le run GitHub Actions du commit `e587aa06`; si rouge lire les logs et corriger d'abord (sélecteurs UI, timeline ou FFmpeg). **Puis A04/M** : undo/redo non destructif des clips et piste audio avec tests de propriétés; poursuivre les tests matériels plus tard. Ne pas fusionner main ni modifier les autres projets.

## Reprise 13 novembre 2026, 18 h — CI rouge sur split E2E

- Dernière CI inspectée : [43458697844](https://github.com/Sathancabrol/monorepo/actions/runs/43458697844), **failure** au step Chromium EDIT export E2E. Les tests Node, HTTP/IndexedDB, fixture Opus passent; le véritable export EDIT est mesuré VP8/Opus, tonalité 440 Hz, début A/V -26 ms, fin -15 ms, -21.1 dB.
- Cause dans les logs : après ajout de la vidéo, `#editSeek` possède encore `max="2.5"`; Playwright `fill("3.5")` échoue `Malformed value` avant la division. Correctif test [e9c1e963](https://github.com/Sathancabrol/monorepo/commit/e9c1e9637827f36d482bf6ed84486db67247dd8a) : attendre `max >= 4.45` (durée 2.5+2 s) avant seek. Le test ne change pas l'application et permet de distinguer retard d'UI et défaut de recalcul de timeline.
- **CI de ce correctif à confirmer** : si le wait expire, inspecter la création du clip vidéo et son état de chargement/durée; ne pas assouplir les assertions sur les deux segments ou les trois médias uniques. Puis A04/M : undo/redo non destructif avec tests de propriétés. Windows/GTX non testé. Aucun merge.

## Reprise 13 novembre 2026, 19 h — A04 historique EDIT

- CI du checkpoint précédent d42fd79a : [43469026586](https://github.com/Sathancabrol/monorepo/actions/runs/43469026586) **success**, y compris E2E deux segments et Portable.
- Nouvelle tranche A04 : `src/edit-history.js` (snapshots bornés à 40, undo/redo, invalidation redo après nouvelle édition, aucun octet média copié) + `tests/edit-history.test.mjs` (split, ordre, titre, audio, invariants, limites). Interface EDIT : boutons Annuler/Rétablir et historique des opérations split, ajout/suppression/réordonnancement de clips, durée/IN/OUT/titres, piste audio et réglages. Chargement d'un projet remet l'historique à zéro. Le serveur autorise le module et la CI en contrôle la syntaxe.
- Commits de cette tranche : 8947c09c, 4dc101c2, a256fb9d, 9508b10e, 6970facc, 9039b8b1 (dernier au moment de l'écriture). **CI de ce nouveau code non confirmée**; vérifier le run au dernier commit avant de déclarer A04 validée.
- **Reprise exacte (S)** : inspecter GitHub Actions sur 9039b8b1 ou checkpoint docs plus récent; si rouge réparer en priorité. **Ensuite (M)** : E2E Chromium UI Annuler/Rétablir sur split et audio, vérifier état Portable et aucun effet sur média source; couvrir navigation clavier, sécurité d'édition durant export. Windows GTX 1060/1650 et écoute humaine non testés. Aucun merge main ni modification de projets voisins.


## Reprise 13 novembre 2026, 20 h — A04 E2E Annuler/Rétablir

- Après lecture du backlog, des quatre journaux et tickets #11–#17, la prochaine tranche A04 concerne les vrais boutons UI.
- Commit de code [b3d792d6](https://github.com/Sathancabrol/monorepo/commit/b3d792d615ce49d57b08adb52aac334af82d3ea5) : extension de `tests/browser_edit_export_e2e.py` après division d'une vidéo. Le test clique `#editUndo`, vérifie par export Portable le retour à un segment, clique `#editRedo`, vérifie deux segments partageant le même assetId, les références média sans pertes et la piste audio inchangée. Contrôle des erreurs JS inclus.
- **Preuve** : écriture GitHub confirmée. **CI du commit b3d792d6 non confirmée** : l'API de recherche des runs liés au commit ne retourne aucun run à cette consultation; cela ne prouve ni succès ni échec. Ne pas déclarer E2E validé.
- **Reprise exacte S** : vérifier le workflow dédié sur le SHA b3d792d6 (et toute tête ultérieure), corriger immédiatement si rouge. Puis M : E2E undo/redo de réglages audio, titre et ordre; vérifier que le redo est invalidé après une nouvelle édition. Éviter d'étendre les tests Windows sans machine.
- Blocages : Windows GTX1060/1650, OBS réel et écoute humaine non accessibles. Aucun merge main, aucun changement d'autre projet.

## Reprise 13 novembre 2026, 21 h — A04 audio UI et branche redo

- Base contrôlée : PR #16 brouillon, tête initiale `9a44f9fb`; CI de cette tête [43488406477](https://github.com/Sathancabrol/monorepo/actions/runs/43488406477) **success**. Backlog, journaux, issues #11–#17 et workflow dédié relus.
- Nouveau commit [0e54ab1f](https://github.com/Sathancabrol/monorepo/commit/0e54ab1f8a71b11016bb578e48949d932561b490) : extension du véritable E2E Chromium `tests/browser_edit_export_e2e.py` pour modifier le volume audio EDIT 1→0,35, annuler et rétablir en conservant les clips, puis annuler et créer une nouvelle branche 0,6 qui doit désactiver Rétablir. Preuves via export Portable de chaque état; aucune donnée utilisateur.
- **CI du nouveau commit à confirmer** : le succès du run précédent ne prouve pas ces nouvelles assertions. Si rouge, inspecter le step Chromium EDIT et réparer avant d'étendre A04.
- Prochaine tranche (M, 1–2 sessions estimées) : couvrir le titre et l'ordre des clips dans l'E2E, puis la sécurité des éditions pendant export; conserver un test Windows/GTX/OBS réel comme blocage matériel distinct. Aucun merge main ni modification hors Studio.

## Reprise 13 novembre 2026, 22 h — A04 titre et ordre E2E

- Base : checkpoint précédent `108c4d10`; [CI #43497174089](https://github.com/Sathancabrol/monorepo/actions/runs/43497174089) **success** (test volume audio et invalidation redo). Vérification via exécutions associées au commit.
- Nouvelle tranche : [commit 60988b03](https://github.com/Sathancabrol/monorepo/commit/60988b032e6c45762ceba146d34cce2dc74e561f) ajoute dans `tests/browser_edit_export_e2e.py` les opérations UI titre et réordonnancement de clips, leur annulation/rétablissement, avec comparaison des snapshots Portable, références médias et piste audio.
- **Preuve actuelle :** écriture GitHub confirmée, **nouvelle CI non vérifiée**. Aucun test Windows ni écoute humaine; aucune fusion main ou modification hors Studio.
- **Reprise exacte (S)** : inspecter le workflow CI au commit `60988b03` et corriger toute erreur du step Chromium. Si vert, tester le verrouillage des modifications pendant export EDIT (M) puis choisir la prochaine tâche READY (A05 benchmark FreeCut/OpenReelio ou A06 ASR) après vérification des critères A01–A04. 

## Reprise 13 novembre 2026, 23 h — A04 isolation de l’historique entre projets

- CI du checkpoint précédent `5bbacce9` : [run 43507408168](https://github.com/Sathancabrol/monorepo/actions/runs/43507408168) **success**. Cela couvre les tests titre/ordre A04 précédemment ajoutés.
- Commit [719cf6f5](https://github.com/Sathancabrol/monorepo/commit/719cf6f58dc7cf925f6a03ee4e0d31b2a611fe3c) : scénario Chromium E2E étendu pour confirmer qu’après réimport du projet Portable l’historique Undo et Redo est vide; empêche de revenir à des états d’un projet précédent. Test écrit mais **CI de ce commit à confirmer**.
- **Reprise exacte (S)** : contrôler la CI du commit `719cf6f5` (ou tête plus récente), lire les logs et réparer si rouge. **Puis (M)** : tester l’interdiction de modifier le montage pendant un export EDIT et décider si A04 peut passer en DONE pour Linux/Chromium (pas Windows). **Ensuite (M)** : A05 audit FreeCut/OpenReelio et ADR licences/format. Aucun test Windows/GTX, aucune fusion main, aucun autre projet modifié.

## Reprise 14 novembre 2026, 00 h — verrouillage ajout clip pendant export

- Synchronisation : PR #16, issues #11–#17, backlog et journaux relus; tête initiale `c6337981`. CI de cette tête [43515491657](https://github.com/Sathancabrol/monorepo/actions/runs/43515491657) **success** (Chromium Linux), valide le scénario précédent d'isolation d'historique.
- Correctif [54917430](https://github.com/Sathancabrol/monorepo/commit/5491743017c903ef723283990ad282380894da8d) : bloque `+ Clip` pendant l'export EDIT, y compris après l'attente asynchrone des métadonnées. Auparavant ce chemin de mutation n'était pas protégé, contrairement aux autres contrôles.
- Test E2E [614caa7e](https://github.com/Sathancabrol/monorepo/commit/614caa7e12f6089f87bca81b253ae392139b3360) : clique `+ Clip` pendant l'export WebM/Opus, vérifie le refus et compare les clips et la piste audio dans l'export Portable suivant. **Nouvelle CI non encore confirmée**; pas de test Windows.
- Reprise exacte : inspecter le run CI de la tête après checkpoint, corriger si rouge (S); puis vérifier les autres chemins de mutation asynchrones pendant export (M) et poursuivre A05 ADR FreeCut/OpenReelio (M). Blocages : GTX/OBS/Windows réels. Pas de merge main.


## Checkpoint 14/11/2026 01 h — garde asynchrone piste audio EDIT

- Dernier CI avant modification : [43524245622](https://github.com/Sathancabrol/monorepo/actions/runs/43524245622) **success**, SHA `2a43a0211a5d5bc9c48234f98b5151f999c2736d` (Chromium Linux, pas Windows).
- Correction : le handler « Ajouter / remplacer piste » vérifiait l'export seulement avant `await loadEditAsset`, permettant une mutation après démarrage d'export. Nouvelle vérification après `await` avant la mutation, sans altérer les sources. Commit `9fbcc2e61c4c4c237397859b9f42562266ee5433`.
- Tests de non-régression Node des gardes asynchrones audio et clip : `tests/edit-export-async-guards.test.mjs`, commits `29515508` et `9ec51163`. Test structurel de position des gardes, **pas** simulation d'une vraie course navigateur.
- CI du nouveau code : **à vérifier**, ne pas déclarer ce correctif validé avant run vert. Blocages : OBS/Windows/GTX et test d'interleaving réel indisponibles ici.
- Prochain sous-objectif **S–M (1 à 2 tranches)** : contrôler CI au dernier SHA; si verte, ajouter un scénario Chromium d'export en cours pendant résolution différée de l'audio, puis A05 ADR FreeCut/OpenReelio (M). Rester sur branche dédiée, aucun merge.

## Checkpoint 14/11/2026 02 h — verrouillage audio pendant export EDIT

- CI du checkpoint précédent `d7056ef9` : [run 43531642820](https://github.com/Sathancabrol/monorepo/actions/runs/43531642820) **success**, valide les tests structurels de gardes asynchrones sous Linux, pas une course réelle ni Windows.
- Nouveau test E2E Chromium [bff96a7b](https://github.com/Sathancabrol/monorepo/commit/bff96a7b614965b054e13a6b23ade36d538a993f) : pendant l'export WebM/Opus réel, cliquer « Ajouter / remplacer piste », vérifier le refus explicite puis conserver l'assertion Portable clips/piste inchangés. Il couvre la garde immédiate UI, **pas** une résolution différée de `loadEditAsset`.
- **CI du nouveau test : non confirmée**. Aucun test Windows/GTX/OBS réel, aucune écoute humaine. Pas de merge main ni modification hors Studio.
- **Prochain sous-objectif S** : consulter le run du commit bff96a7b ou de cette tête; si rouge, diagnostiquer le step Chromium. **Puis M** : fixture déterministe avec chargement audio différé et démarrage de l'export entre invocation et résolution; contrôler que l'audio n'est pas remplacé. **Puis A05/M** : ADR FreeCut/OpenReelio avec licences et formats vérifiés.

## Checkpoint 14/11/2026 03 h — A05 contrat d'échange EDIT et ADR provisoire

- Synchronisation : backlog, STATUS, SESSION_PLAN, HANDOFF, PR #16, issues #11–#17, commits et workflow dédié consultés. Dernière CI **verte** avant modification : [43538357900](https://github.com/Sathancabrol/monorepo/actions/runs/43538357900), SHA `b704f43a` (Chromium Linux). Elle valide le verrouillage UI audio de la session précédente, **pas** la course différée.
- Livré : `src/edit-interchange.js` (`d5c08929`) crée un manifeste JSON indépendant des moteurs, sans chemins ni octets sources; `tests/edit-interchange.test.mjs` (`bb1faaf0`) couvre split sur média partagé, temps, piste audio, non-mutation, erreurs; `docs/ADR-0001-edit-interchange.md` (`8f8057a0`) documente l'architecture provisoire et les licences GitHub déclarées de FreeCut/OpenReelio/Velorn. **Non branché à l'UI, aucun adaptateur tiers ni benchmark matériel.**
- Nouveau run dédié au SHA `8f8057a0` : [43544183011](https://github.com/Sathancabrol/monorepo/actions/runs/43544183011), **pending** à la consultation; les deux runs intermédiaires ont été annulés par la concurrence CI. Ne pas déclarer les nouveaux tests verts avant confirmation.
- **Reprise exacte (S)** : vérifier le run 43544183011 ou celui du dernier SHA, corriger tout échec de test. **Puis M** : réaliser la fixture déterministe de chargement audio différé pendant export (la garde UI immédiate est déjà couverte). **Puis M–L** : compléter A05 par analyse des formats/API des trois candidats et adapter explicitement un format seulement après preuve. 
- Blocages persistants : tests Windows GTX 1060/1650, OBS réel, écoute humaine et mesure VRAM; aucune modification de main ou des projets voisins. Taille restante A05 : M–L; A01–A04 encore partiels selon critères de recette.

## Checkpoint 14/11/2026 04 h — A05 validation du contrat d'échange

- Synchronisation effectuée : backlog, HANDOFF, STATUS, SESSION_PLAN, issues #11–#17, PR #16, commits et runs GitHub consultés. Run [43544216164](https://github.com/Sathancabrol/monorepo/actions/runs/43544216164) **success** sur le checkpoint précédent `64b1c339` ; cette preuve ne couvre pas les commits ci-dessous.
- Livré : `src/edit-interchange.js` ajoute `validateEditInterchange` pour contrôler schéma/version, types, IDs uniques, segments contigus, durée totale, nombres finis et limite 24 h avant usage par un futur adaptateur. Retourne une copie limitée aux champs contractuels. Commit `7231f71f`.
- Tests ajoutés : round-trip et champs inconnus ignorés, rejets de trous/chevauchements, doublons, durée incohérente et Infinity. Commit `e54e792e`. **Nouvelle CI non encore confirmée** ; pas d'exécution locale Node/Windows attestée dans cette session.
- Reprise exacte (S) : contrôler CI du commit `e54e792e` ou tête suivante, réparer tout échec avant nouvelles fonctions. Puis (M) fixture déterministe de chargement audio différé pendant export ; ensuite (M–L) poursuivre l'ADR A05 avec API/format et mesure reproductible. Pas de fusion main, ni modification hors Studio. Windows/GTX/OBS réels restent bloqués.


## Checkpoint 14/11/2026 05 h — cohérence des manifestes A05

- Synchronisation : backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16, tickets et workflow dédié consultés. CI du checkpoint précédent `e6b02dc3` : [run 43549460194](https://github.com/Sathancabrol/monorepo/actions/runs/43549460194) **success** (Linux, non Windows).
- Défaut corrigé : `toEditInterchange` pouvait produire un manifeste de plus de 24 h que `validateEditInterchange` refusait ensuite; la génération passe désormais par la validation commune. Le validateur refuse aussi `sourceIn` non nul sur une image fixe, propriété réservée aux clips vidéo.
- Code commit `11b2ead260c0569c98b7d1714290a352351dffda`; tests de limites 24 h et offset image commit `8729a1f82dc58f309f6d29991caef38f4987fed7`. **CI de ces commits à confirmer**; aucun test Node local attesté.
- Reprise exacte : contrôler le run CI du dernier SHA (S), corriger si rouge; ensuite fixture déterministe de chargement audio différé pendant export (M), puis approfondir le benchmark API/format FreeCut/OpenReelio (M–L). Aucun test Windows, OBS, GTX, écoute humaine; aucun merge main.


## Reprise 2026-11-14 06:00 — réparation CI A05
- Dernier run rouge avant correctif : https://github.com/Sathancabrol/monorepo/actions/runs/43554633813 (51/52 tests Node, Chromium non exécuté). Échec exact : test « Generated interchange enforces the same 24-hour bound » attendait une exception pour un seul clip image de 86401 s, alors que `clipDuration()` plafonne chaque clip à 36000 s.
- Correctif test livré : commit `9afb372ac359b50e49df17b1803d2aaf9cd0a2e3`. Le scénario utilise désormais trois clips (36000 + 36000 + 14401 s) pour franchir 24 h et vérifie la frontière à 86400 s. Pas de changement du comportement produit.
- Tests locaux Windows : non réalisés. CI au commit correctif : à confirmer avant de déclarer vert.
- Prochaine tâche READY : si CI rouge, réparer d'abord ; sinon test Chromium déterministe de course chargement audio différé/export (M, ~1–2 tranches), puis audit A05 des formats externes (M).
- Branch scope : `feat/olympus-studio-20261112`, dossier Studio uniquement ; PR #16 brouillon, aucun merge.


## Reprise 2026-11-14 07:00 — retour à l'édition après export
- CI du checkpoint précédent `f7fe2b29` : [run 43559514421](https://github.com/Sathancabrol/monorepo/actions/runs/43559514421) **success** (Ubuntu/Chromium, pas Windows). Correction de la limite globale 24 h confirmée.
- Nouvelle régression E2E : après export WebM/Opus et vérification du verrouillage, le bouton « Ajouter / remplacer piste » doit redevenir utilisable. Le test exporte le projet Portable après déverrouillage et vérifie que la piste reste liée au même média et que les clips sont inchangés. Commits `89643651`, `fe199375` (correction d'une référence à un helper déclaré plus loin).
- **Nouvelle CI au commit fe199375 : à confirmer.** Ce test ne reproduit toujours pas la course déterministe de chargement audio différé; aucun test Windows/GTX/OBS ni écoute humaine.
- **Prochain sous-objectif S :** inspecter CI au dernier SHA et corriger si rouge. **Puis M :** test Chromium déterministe où un chargement audio reste suspendu pendant que l'export démarre, puis se résout; vérifier que la piste du montage ne change pas. **Puis M–L :** analyse A05 des formats/API FreeCut/OpenReelio. Pas de fusion main ni modification des projets voisins.


## Reprise 2026-11-14 08:00 — limites des métadonnées A05
- Synchronisation backlog, STATUS, SESSION_PLAN, HANDOFF, PR #16, issues #11–#17, commits et workflow dédié. Dernière CI vérifiée : [43564140051](https://github.com/Sathancabrol/monorepo/actions/runs/43564140051) **success** sur `5378757b` (Linux/Chromium).
- Correctif `f888b7b9` : le validateur de manifestes d'échange rejette désormais les identifiants de clip/asset dépassant 256 caractères et les titres dépassant 4096 caractères. Réduit le risque de charge mémoire incontrôlée avec des métadonnées importées; ne résout jamais les identifiants comme chemins.
- Tests `606d95ed` : cas invalides pour les trois champs, génération refusée et manifeste valide conservé. **CI du nouveau code à confirmer**, aucun test local Windows.
- Reprise exacte : contrôler CI du dernier SHA, réparer tout échec en priorité (S). Ensuite test Chromium déterministe de résolution audio différée pendant export (M, 1–2 tranches), puis analyse concrète API/format FreeCut/OpenReelio (M–L). Blocages matériels OBS/GTX/Windows inchangés. PR #16 reste brouillon, aucune modification main ou projets voisins.


## Reprise 2026-11-14 09:00 — normalisation des temps A05
- Relecture du backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17 et workflow dédié. CI précédente au SHA `e1c2c287` : [run 43569388832](https://github.com/Sathancabrol/monorepo/actions/runs/43569388832) **success** (Linux/Chromium).
- Défaut A05 : `validateEditInterchange` acceptait une variation inférieure à 1 ms entre segments mais retransmettait cette variation à un adaptateur, pouvant produire une micro-discontinuité. Le validateur conserve la tolérance d'import puis canonicalise `timelineStart` sur le cumul exact des durées.
- Correctif `c0cf4154`; test `45f31bf0` : arrondi de 0,5 ms normalisé, entrée source non mutée, écart de 2 ms rejeté. **CI de ces nouveaux commits à confirmer**, aucune exécution Node locale ou Windows attestée.
- Reprise exacte (S) : contrôler CI du dernier SHA, réparer tout échec. Ensuite (M) test Chromium déterministe d'un chargement audio différé pendant export; puis (M–L) audit concret FreeCut/OpenReelio. Blocages Windows/GTX/OBS inchangés; pas de merge main ni changement hors Studio.

## Reprise 2026-11-14 10:00 — alignement limite clip A05
- Synchronisation : AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN et issues #11–#17 relus; dernière CI vérifiée sur checkpoint précédent `d1b7127e` : [run 43574091154](https://github.com/Sathancabrol/monorepo/actions/runs/43574091154), **success** Linux/Chromium. Aucun essai Windows.
- Écart réel : `validateEditInterchange` acceptait un segment importé jusqu'à 86400 s, mais `storyboard.clipDuration` limite chaque clip à 36000 s. Correctif `ad3001ca` : borne importée à 36000 s, limite globale 86400 s inchangée. Test de frontière 36000/36001 pour image et vidéo ajouté par `97827f24`.
- **Nouvelle CI au SHA de test à confirmer**; aucun test local Node/Windows déclaré. Ne pas fermer A05, A01 ou A03.
- Reprise exacte : (S) inspecter la CI du dernier SHA, réparer si rouge; (M, 1–2 tranches) test Chromium déterministe de chargement audio asynchrone pendant export; (M–L) audit FreeCut/OpenReelio sur formats et API. Aucun merge main ni changement hors Studio.


## Reprise 2026-11-14 11:00 — robustesse manifeste A05
- Documents de reprise et workflow dédié consultés. Dernière CI confirmée dans checkpoint antérieur : run 43574091154 (success Linux/Chromium sur d1b7127e). Statut CI des nouveaux commits non vérifié : inconnu.
- Correctif A05 : rejet des segments de manifeste ayant une forme de tableau JavaScript, même avec propriétés nommées. Commit d4beaa3a ; test de régression 1227be92. Aucun test Node, Chromium ou Windows exécuté ici.
- Prochaine reprise : S vérifier CI au dernier SHA et réparer si rouge ; M test Chromium déterministe de chargement audio différé pendant export EDIT ; M–L audit FreeCut/OpenReelio. A01/A02/A05 ouverts.
- Périmètre : branche dédiée, Studio uniquement, pas de merge main, GTX/OBS non testés.

## Reprise 2026-11-14 12:00 — A05 import retour vers storyboard
- Synchronisation préalable : backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17, workflow dédié et dernier run consultés. CI précédente [43583188581](https://github.com/Sathancabrol/monorepo/actions/runs/43583188581) **success** au SHA `2d4e52ff` (Linux/Chromium).
- Nouveau code A05 : `fromEditInterchange()` valide le manifeste puis reconstruit les clips éditables (IN/OUT, ordre, identifiants, titres, assets partagés) et la piste sonore sans toucher aux fichiers source. Correctif complémentaire : rejet des offsets vidéo dont l'addition avec la durée déborde en Infini. Commits `6d0e252c`, `b3af4334`.
- Tests ajoutés : aller-retour manifeste → clips → manifeste, deux segments d'un même asset, piste audio, absence de mutation et rejet du débordement. Commit `1ef9d947`.
- **Validation des nouveaux commits : en attente**. Pas de Node local : accès réseau au dépôt indisponible dans le conteneur; ne pas annoncer de test exécuté. CI au dernier SHA à vérifier. Aucun Windows/GTX/OBS testé.
- **Reprise exacte S** : consulter le run CI de `1ef9d947` ou du checkpoint; réparer tout échec. **Puis M** : test Chromium déterministe de course chargement audio différé/export EDIT. **Puis M** : intégrer explicitement l'import du manifeste dans l'interface avec prévisualisation et validation des assets manquants (sans accès aux chemins). A05 demeure READY, PR #16 brouillon.
- Périmètre strict : uniquement Studio et branche dédiée; aucun merge main ni autre projet.

## Reprise 2026-11-14 13:00 — CI rouge A05 réparée (validation à confirmer)
- CI du checkpoint `e8133a93` : [run 43588378624](https://github.com/Sathancabrol/monorepo/actions/runs/43588378624) **failure**, étape Node `API smoke tests` : 57/58 réussis. Échec test `Interchange import rejects overflowing video source offsets`, exception absente : `Number.MAX_VALUE + 2` reste `Number.MAX_VALUE` en IEEE-754, pas `Infinity`.
- Correctif `63cb8451` : limite explicite `sourceIn <= 86400` secondes pour les manifestes importés; test révisé `28d6b9e8` : durée de clip valide et offset extrême refusé. Commit transitoire `2fb6b21e` remplacé par ce test correct. Les tests de navigateur ont été sautés par la CI rouge.
- **CI du dernier SHA à vérifier**, aucun test Node local ni Windows revendiqué. Si rouge, réparer avant nouveau code; si verte, reprendre test Chromium déterministe de chargement audio différé pendant export EDIT (M, 1–2 tranches), puis import manifeste dans UI (M). Ne pas fermer A01/A05. Aucun changement main/projets voisins.

## Reprise 2026-11-14 14:00 — CI rouge A/V EDIT, trames vidéo
- Synchronisation : backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17 et état du workflow dédié consultés. CI du SHA `c8d4e85d` : [run 43592984936](https://github.com/Sathancabrol/monorepo/actions/runs/43592984936) **failure**. Node, IndexedDB/Portable Chromium et fixture Opus réussissent; `browser_edit_export_e2e.py` échoue sur fin vidéo 1.464 s contre fin audio 2.544 s (écart 1.080 s, seuil 0.6 s). Ne pas assouplir le seuil sans justification.
- Correctif produit `6fed9b384ce0ecc74c7f1f5682ca82dbf22b0494` : capture EDIT Canvas en mode manuel `captureStream(0)` avec `requestFrame()` après chaque dessin; fallback `captureStream(24)` si navigateur sans requestFrame. Vise les trames manquantes au passage entre clips pendant que l'audio continue. Test de régression existant `browser_edit_export_e2e.py` sert de preuve à venir; **CI du nouveau SHA non confirmée**. Aucun test local Windows/Node revendiqué.
- Reprise exacte (S) : vérifier CI au SHA `6fed9b38` (ou checkpoint suivant), inspecter les timestamps FFprobe et corriger si rouge. Si toujours rouge, instrumenter les trames/horodatages aux frontières des clips plutôt que masquer l'échec. Ensuite (M) test de course audio différé pendant export; puis (M) import manifeste EDIT dans UI. PR #16 reste brouillon, aucun merge ni autre projet modifié.


## Checkpoint 14/11/2026 14:58 Europe/Paris — confirmation CI A/V

- Branche inspectée : `feat/olympus-studio-20261112`, HEAD `402b0bc59b486ef98ea68b9b89bc619b12418f40`. Aucun autre commit postérieur détecté lors de cette lecture.
- **CI verte confirmée au HEAD** : [GitHub Actions #43597867993](https://github.com/Sathancabrol/monorepo/actions/runs/43597867993), conclusion `success`, terminée le 14/11/2026 à 13:06 UTC. Le correctif `6fed9b38` (demande explicite de chaque frame Canvas pendant l'export EDIT) est donc validé par le workflow Linux/Chromium, sans preuve matérielle Windows.
- Relecture : backlog autonome, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17, derniers commits et runs. Aucun nouveau changement fonctionnel poussé dans cette session : ne pas le présenter comme une livraison de code.
- **Prochaine tâche READY** : A03/A01 — E2E Chromium déterministe d'une promesse `loadEditAsset` audio retardée au moment où démarre un export EDIT; vérifier que la piste n'est pas remplacée pendant `MediaRecorder.recording` et que l'UI se déverrouille ensuite. Ajouter le test à `tests/browser_edit_export_e2e.py` ou à un script dédié exécuté par le workflow; ne pas confondre avec les tests statiques de garde `edit-export-async-guards.test.mjs` existants. Estimation M (1–2 tranches d'ingénierie).
- Ensuite : import des manifestes A05 dans l'interface avec reliaison explicite des médias manquants; audit FreeCut/OpenReelio ADR. Bloqué sur Windows : OBS réel, GPU GTX 1060/1650 et recette installateur.
- Dernier commit de code : `6fed9b384ce0ecc74c7f1f5682ca82dbf22b0494`. Dernier run CI vérifié : `43597867993`. Aucun test local exécuté dans cette session; preuve CI seulement. PR #16 reste en brouillon. Ne modifier ni `main` ni projets voisins.


## Reprise 2026-11-14 16:03 Europe/Paris — course de préparation audio EDIT
- Relu AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17 et workflow dédié. Dernière CI verte **documentée** : [43597867993](https://github.com/Sathancabrol/monorepo/actions/runs/43597867993), au checkpoint précédent; aucune validation du nouveau code encore acquise.
- Correctif [54930b1e](https://github.com/Sathancabrol/monorepo/commit/54930b1eace989c226bff1538fd7ee855a785d56) : empêche deux préparations d'export simultanées et fige les paramètres audio demandés; après le chargement IndexedDB et après l'initialisation WebAudio, toute modification de piste provoque un refus explicite plutôt qu'un export incohérent. Libère le verrou de préparation dans finally.
- Test [5cd52125](https://github.com/Sathancabrol/monorepo/commit/5cd521259303c72fa2b916055de08e895cd1ee4f) : assertions de structure Node sur les gardes asynchrones; **pas encore** de test de course Chromium déterministe, ni de résultat CI de ces commits. Les tests structurels ne prouvent pas le comportement du navigateur.
- **Prochaine action M (1–2 tranches)** : ajouter un E2E Chromium déterministe avec promesse de chargement audio retenue pendant le clic d'export, modifier la piste avant résolution, vérifier refus explicite et absence de téléchargement, puis refaire un export normal et vérifier WebM/Opus. Examiner CI au dernier HEAD avant tout nouvel ajout; réparer si rouge. Puis M : import de manifeste EDIT en interface avec reliaison contrôlée.
- Blocages : Windows, GTX 1060/1650, OBS réel et écoute humaine. PR #16 brouillon, pas de merge ni modifications hors Studio.

## Reprise 2026-11-14 17:04 Europe/Paris — verrouillage EDIT pendant préparation
- CI du checkpoint précédent `ec2e63fd` : [run 43608181851](https://github.com/Sathancabrol/monorepo/actions/runs/43608181851) **success** (Linux/Chromium). Ce run ne couvre pas les nouveaux commits.
- Correctif produit `72c65ce7` : les 14 gardes de mutation EDIT qui interdisaient déjà les changements pendant `MediaRecorder.recording` interdisent aussi les changements pendant `editorExportPreparing`. Ceci protège les actions UI durant les awaits IndexedDB/WebAudio et évite de dépendre seulement de la comparaison de snapshot audio à la fin de préparation.
- Tests structurels `bdc16ab5` : vérifient la couverture des gardes et leur position après les awaits des handlers de clips/pistes. **Pas de test Chromium déterministe de la course**, ni de test Node local effectué dans cette session. CI des nouveaux commits **à confirmer**.
- Reprise exacte : (S) vérifier le dernier run GitHub Actions et réparer s'il échoue ; (M) E2E Chromium avec chargement audio IndexedDB retardé, clic d'export, tentative de mutation, refus puis export normal Opus; (M) import manifeste A05 dans l'UI et reliaison des médias. Windows/GTX/OBS/écoute humaine non testés. PR #16 reste brouillon; pas de merge main ni modification des projets voisins.


## Reprise 2026-11-14 17:56 Europe/Paris — navigation durant préparation audio
- Synchronisation : backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17 et workflow dédié consultés. CI du HEAD précédent `5cc3eb74` : [run 43613708210](https://github.com/Sathancabrol/monorepo/actions/runs/43613708210) **success** (Linux/Chromium).
- Bug identifié : `setSpace()` appelait `editorRecorder.stop()` pendant `editorExportPreparing`, alors que le recorder n'est créé qu'après chargement audio; changement d'espace pouvait donc produire une TypeError et laisser une préparation en cours. Correctif `57966a41` : refuser la navigation hors EDIT pendant cette préparation avec statut explicite, avant l'accès au recorder. Test de régression structurel `2e2f9ca0`.
- **Validation du nouveau code : CI à confirmer**, aucun Node/Chromium local ni Windows exécuté ici. Ce test ne remplace pas l'E2E de course déterministe.
- Reprise S : consulter la CI au dernier SHA et réparer si rouge. Ensuite M (1–2 tranches) : E2E Chromium avec chargement IndexedDB audio volontairement retardé, navigation/tentative de mutation refusée puis export normal WebM/Opus; ensuite M import manifeste EDIT dans l'interface. Blocages matériels OBS/GTX/Windows inchangés. PR #16 brouillon, aucun merge main.


## Reprise 2026-11-14 18:59 Europe/Paris — E2E préparation audio différée
- Synchronisation : backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17, workflow dédié et export EDIT consultés. CI du checkpoint précédent `2b865030` : [43618366485](https://github.com/Sathancabrol/monorepo/actions/runs/43618366485) **success** (Linux/Chromium).
- Nouveau test E2E [562dadd1](https://github.com/Sathancabrol/monorepo/commit/562dadd104f79ad535a190eb256c048012774af8) dans `tests/browser_edit_export_e2e.py` : intercepte `AudioContext.resume()` avec une promesse contrôlée, déclenche le vrai bouton d'export EDIT, tente ajout de clip, remplacement audio et navigation LIVE pendant la préparation, libère le verrou puis inspecte WebM/Opus et la conservation du projet Portable. Aucun média personnel.
- **Validation du nouveau test non encore confirmée** : consulter le run CI au SHA `562dadd1`, inspecter le step `Chromium EDIT export E2E`, réparer si rouge. Test navigateur non exécuté localement; aucune preuve Windows/GTX/OBS. La promesse retenue concerne WebAudio, pas directement `getMedia` IndexedDB; ajouter ensuite une interception IndexedDB déterministe si nécessaire.
- Prochaine action S : CI du dernier HEAD et correctif immédiat. Ensuite M : import manifeste EDIT dans UI avec gestion des médias manquants. Puis M–L : audit FreeCut/OpenReelio ADR. Branche isolée, PR brouillon, aucun merge main.


## Reprise 2026-11-14 19:56 Europe/Paris — préflight médias des manifestes EDIT
- Synchronisation : AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17, workflow dédié et tests interchange consultés. La CI du HEAD précédent n'a pas pu être confirmée : la recherche des runs associés au commit renvoie une liste vide (filtrage limité aux runs PR), et le statut combiné ne fournit aucune vérification. **Ne pas inférer vert.**
- Fonction pure ajoutée : `src/edit-interchange-assets.js`, `inspectEditInterchangeAssets(manifest, availableAssetIds)`. Validation du manifeste avant lecture, références média uniques (clips scindés et bande-son), liste ordonnée des assets manquants et indicateur `ready`. Aucune résolution de chemin, aucun accès réseau ni mutation.
- Tests Node ajoutés : `tests/edit-interchange-assets.test.mjs` (médias partagés, bande-son absente, entrée invalide, non-mutation). Commits `6029447c` (code), `10c49f03` (tests). **Tests non exécutés localement; CI des nouveaux commits non vérifiée.** Le script `npm test` exécute `node --test` et découvrira le fichier.
- Cette tranche prépare l'import des manifestes mais **ne l'expose pas encore dans l'interface** et ne relie aucun média automatiquement. La PR #16 reste brouillon; Windows/GTX/OBS et écoute réelle non testés.
- Prochaine reprise (S) : vérifier la CI de `10c49f03` ou du HEAD de checkpoint; si rouge réparer en priorité. Ensuite (M) : brancher l'import manifeste EDIT dans l'UI en affichant les références absentes et en refusant une importation destructive, avec test Chromium HTTP/IndexedDB. Puis (M–L) ADR FreeCut/OpenReelio. Estimation restante de l'import UI : 1–3 tranches d'ingénierie.


## Reprise 2026-11-14 21h Europe/Paris — import manifeste EDIT dans l'interface
- Synchronisation : backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17, derniers commits et workflow dédié relus. Attention : la recherche globale de commits inclut d'autres projets; aucune modification de ceux-ci. La recherche des runs associés au commit via le connecteur retourne une liste vide; **CI du dernier HEAD non confirmée**, ne pas conclure vert.
- Code livré sur la branche dédiée : `ac010a6c` (bouton et sélection JSON EDIT, prévalidation des assets en mémoire puis présence effective IndexedDB, validation du type image/vidéo/audio, remplacement atomique du montage et historique undo; refus si export en cours, erreur non destructive), `e898c115` (autorisation HTTP explicite des deux modules d'interchange), `6eedd904` (test Node de préflight et de câblage UI/HTTP).
- **Validation** : aucun test Node/Chromium exécuté dans cette session (réseau du conteneur GitHub indisponible). Tests ajoutés mais résultat CI inconnu. L'import n'embarque pas les médias absents et ne télécharge rien; l'utilisateur doit les avoir dans le coffre local. Pas de test Windows/GTX/OBS ni écoute humaine.
- Reprise exacte (S) : consulter le run GitHub Actions du SHA `6eedd904`, inspecter les étapes Node et Chromium, réparer toute régression. Puis (M) : E2E Chromium HTTP/IndexedDB d'import du manifeste avec média existant, absence de média et non-mutation, undo/redo; vérifier aussi comportement de l'import pendant préparation export. Ensuite (M–L) : ADR FreeCut/OpenReelio.
- PR #16 conservée brouillon; aucun merge main. Estimation E2E : 1–3 tranches d'ingénierie.


## Reprise 2026-11-14 22h Europe/Paris — CI rouge, course WebAudio
- CI du HEAD précédent `9b125e01` : [run 43635403179](https://github.com/Sathancabrol/monorepo/actions/runs/43635403179) **failure**. Tests Node, HTTP/IndexedDB et fixture A/V réussis; le scénario `browser_edit_export_e2e.py` échoue ligne 199 : timeout 10 s sur `window.__editResumeGate.waiting`. Le hook ne se déclenche pas lorsque le contexte WebAudio est déjà `running` : le code sautait alors `resume()`.
- Correctif applicatif `0fd1e3e2`, suivi de correction de mise en forme `0b13e074` : `attachAudioToEditorCapture` attend désormais `context.resume()` même si l'état est déjà `running`, pour assurer une barrière de préparation uniforme. Le test E2E existant vérifie la suspension, les refus de modification/navigation, la reprise et le WebM Opus. **Nouvelle CI non encore confirmée**; si échec, consulter logs exacts et corriger avant d'ajouter une fonctionnalité.
- Prochaine action S : vérifier CI au dernier HEAD et diagnostiquer toute erreur Chromium. Ensuite M : E2E HTTP/IndexedDB import manifeste EDIT (source présente, absente, undo/redo, non-mutation), puis ADR FreeCut/OpenReelio. Aucun test Windows, GPU ou écoute humaine; PR #16 brouillon, aucun merge ni autre projet modifié.


## Reprise 2026-11-14 23h Europe/Paris — CI rouge, trames statiques A/V
- Synchronisation : AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17 et workflow dédié relus. Run [43640316209](https://github.com/Sathancabrol/monorepo/actions/runs/43640316209) **failure** au step Chromium EDIT export E2E; Static parse, Node, IndexedDB/Portable et fixture A/V verts. Le premier export après WebAudio différé a passé ffprobe (VP8/Opus, décalage de fin -0.020 s, 440 Hz, -21.1 dB). Le second export du même storyboard statique échoue : fin vidéo 1.572 s, fin audio 2.538 s, décalage 0.966 s (seuil 0.6 s).
- Correctif produit [7193600c](https://github.com/Sathancabrol/monorepo/commit/7193600c8567b8bde42ae2fa06ea2c8489f7d7d8) : variation d'un marqueur 8×8 dans le coin inférieur droit uniquement durant capture, avant requestFrame(), afin d'éviter la coalescence de trames Canvas statiques par l'encodeur Chromium. Test structurel [d03cb3cd](https://github.com/Sathancabrol/monorepo/commit/d03cb3cdf71f32b7ec82f0bf2dd31a928dc872c4) ; l'E2E existant contrôle la vraie durée via FFprobe. Hypothèse de cause non encore prouvée : ne pas déclarer le correctif validé sans CI verte.
- Dernier commit fonctionnel/test : d03cb3cd. Dernier run inspecté : 43640316209, failure. Aucun test Node local, Windows, GTX ni écoute humaine effectué. CI des nouveaux commits **à confirmer**. PR #16 brouillon, aucun merge ni modification hors Studio.
- Reprise exacte (S) : inspecter la CI au SHA d03cb3cd ou checkpoint; si encore rouge, instrumenter le nombre de trames et timestamps FFprobe / capturer MediaRecorder plutôt que relâcher la tolérance A/V. Si verte, (M, 1–3 tranches) test Chromium HTTP/IndexedDB de l'import de manifeste EDIT : média présent, manquant, refus non destructif, undo/redo; puis (M–L) audit FreeCut/OpenReelio. Bloqueurs Windows/OBS/GTX inchangés.


## Reprise 2026-11-15 00h Europe/Paris — CI Node rouge, test de garde trop large
- Run [43646153716](https://github.com/Sathancabrol/monorepo/actions/runs/43646153716) **failure** : Static parse OK, 67/68 tests Node réussis; test `all EDIT recording mutation guards also cover asynchronous preparation` échoue car le marqueur de trame Canvas introduit en `7193600c` est volontairement actif seulement durant l'enregistrement. Les étapes Chromium sont sautées : **aucune preuve nouvelle de synchronisation A/V**.
- Correctif de test [94f9af3f](https://github.com/Sathancabrol/monorepo/commit/94f9af3f542d781736bdc4be1161d3b33d1ee5bb) : autorise exactement un garde `recording` isolé, seulement s'il correspond au marqueur de capture, tout en exigeant au moins dix gardes combinés pour les mutations EDIT. Aucun changement au produit; évite d'affaiblir le verrou des mutations.
- CI du nouveau commit **non encore confirmée**. Dernier run inspecté : 43646153716 (rouge). Aucun test Node local/Chromium/Windows/GTX exécuté dans cette session. PR #16 brouillon; aucune modification hors Studio.
- **Reprise exacte S** : lire la CI du HEAD après 94f9af3f; si rouge, diagnostiquer précisément, surtout la durée A/V du second export avec FFprobe. **Puis M (1–3 tranches)** : E2E HTTP/IndexedDB de l'import manifeste EDIT avec média présent/absent, non-mutation et undo/redo. **Ensuite M–L** : ADR FreeCut/OpenReelio. Bloqueurs matériels Windows/OBS/GTX inchangés.

## Reprise 2026-11-15 01h Europe/Paris — CI verte et E2E manifeste EDIT

- CI du précédent checkpoint `e0cc82de` : [run 43651256457](https://github.com/Sathancabrol/monorepo/actions/runs/43651256457) **success** (workflow OLYMPUS Studio). Cette réussite confirme la correction du test Node et le parcours E2E A/V sur Linux/Chromium; elle ne constitue pas un test Windows ni une écoute humaine.
- Nouvelle tranche : [de3474e0](https://github.com/Sathancabrol/monorepo/commit/de3474e032facd3812c2334a75e6692ba1c9592d) ajoute `tests/browser_edit_manifest_e2e.py`, parcours HTTP/Chromium réel avec média PNG stocké dans IndexedDB, import du manifeste, vérification du clip, refus atomique d'une référence absente puis d'un asset supprimé du coffre, undo et redo.
- [67eab042](https://github.com/Sathancabrol/monorepo/commit/67eab042bd0f88844e579d8cbd62ebf0c36f311f) ajoute ce scénario au workflow CI dédié, avec contrôle de syntaxe Python. **Nouveau test non exécuté dans cette session : CI du dernier HEAD en attente de vérification.** Pas de modification hors Studio et workflow dédié; PR #16 reste brouillon.
- Reprise exacte **S** : inspecter le run Actions associé à `67eab042`; en cas de rouge, examiner le step « Chromium EDIT manifest import » et corriger le test ou l'application selon la preuve. **Puis M** : couvrir import pendant préparation export et restauration après navigation, puis ADR FreeCut/OpenReelio (M–L). Aucun essai Windows GTX1060/1650, OBS réel ou écoute humaine.

## Reprise 2026-11-15 02h Europe/Paris — CI rouge, export Portable après suppression IndexedDB

- Synchronisation : AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17 et workflow dédié relus. HEAD initial `20f8657c`. Run [43655691195](https://github.com/Sathancabrol/monorepo/actions/runs/43655691195) **failure** uniquement au nouveau step Chromium EDIT manifest import; Static parse, Node, IndexedDB, fixture A/V et export EDIT WebM/Opus **success**.
- Traceback : timeout Playwright de 15 s sur `expect_download` à `after-deletion.json` (ligne 131). Le test supprimait volontairement l'unique Blob IndexedDB puis tentait un export Portable exigeant ce Blob. Ce n'est pas une preuve que l'import rejeté a muté les clips.
- Correctif test [9c139bce](https://github.com/Sathancabrol/monorepo/commit/9c139bced7986289160089710e78e381f6f6957d) : sauvegarder le record original avant suppression, vérifier après refus qu'il est toujours absent (pas de restauration cachée), le réinsérer dans IndexedDB, puis seulement exporter Portable pour comparer clips et undo/redo. Aucun changement applicatif ni suppression de données utilisateur; fixture synthétique du test uniquement.
- **CI de 9c139bce et de ce checkpoint non encore confirmée.** Aucun test local, Windows/GTX, OBS réel ou écoute humaine. PR #16 brouillon, main et autres projets inchangés.
- Reprise exacte **S** : lire le run GitHub Actions du HEAD, réparer toute nouvelle erreur du step manifeste. Puis **M (1–2 tranches)** : E2E import pendant préparation d'export et restauration après navigation; ensuite **M–L** ADR FreeCut/OpenReelio. Dernier run inspecté : 43655691195 (failure); dernier commit fonctionnel/test : 9c139bce. Estimation restante E2E : 1–2 tranches.


## Reprise 2026-11-15 03h Europe/Paris — CI rouge, marqueur Canvas aliasé
- HEAD initial `2b14fdb7`; run [43661127133](https://github.com/Sathancabrol/monorepo/actions/runs/43661127133) **failure** au step `Chromium EDIT export E2E` : Node, IndexedDB et fixture Opus verts; premier export EDIT différé VP8/Opus réussi (écart fin -0.022 s, 440 Hz); second export échec A/V fin vidéo 1.799 s, audio 2.531 s, écart 0.732 s (>0.6). Le test de manifeste est sauté, non validé.
- Correctif produit [a1b4a030](https://github.com/Sathancabrol/monorepo/commit/a1b4a030526e6cb2900dec38311055c4cd561efb) : le marqueur de capture était calculé avec `Math.floor(now/32)%2` et pouvait rester identique lorsque requestAnimationFrame cadence proche de 32 ms; passage à un compteur d'images monotone pour garantir l'alternance. Test de régression structurel [35218922](https://github.com/Sathancabrol/monorepo/commit/35218922951f6b1854c24c35f5c38432b10b8e31) avec timestamps répétés. Hypothèse à vérifier : ce changement évite la coalescence vidéo; **aucune CI du correctif encore confirmée**, aucune mesure Windows.
- Reprise exacte **S** : consulter CI au dernier HEAD; si rouge, examiner FFprobe et instrumenter le nombre de trames capturées au lieu de relâcher la tolérance. Si verte, exécuter le test de manifeste import/IndexedDB puis couvrir import concurrent avec préparation export et restauration après navigation (**M, 1–2 tranches**). Ensuite ADR FreeCut/OpenReelio (**M–L**). Aucun changement hors Studio, aucune fusion main.


## Reprise 2026-11-15 04h Europe/Paris — CI Node rouge après compteur de trames
- HEAD initial `a3e01aa1`; [run 43665485066](https://github.com/Sathancabrol/monorepo/actions/runs/43665485066) **failure** à `API smoke tests` : 67/69 tests Node passés, 2 échecs (`edit-canvas-capture.test.mjs`, `edit-export-async-guards.test.mjs`). Les assertions exigeaient encore `Math.floor(now/32)%2`, supprimé volontairement par le correctif produit `a1b4a030` au profit de `(++editorCaptureFrame)%2`. Étapes Chromium sautées, donc aucune nouvelle preuve A/V.
- Correctifs de non-régression : [43737726](https://github.com/Sathancabrol/monorepo/commit/43737726b38bfb2ee6fde97089c74bb69abe5f86) met à jour l'assertion Canvas et interdit l'ancienne formule aliasée; [19c8c6bf](https://github.com/Sathancabrol/monorepo/commit/19c8c6bfd5c8b04ea628ed9713a8e207aeba9e7f) met à jour l'assertion du garde d'export. Pas de changement applicatif dans cette session.
- Dernier commit test : `19c8c6bfd5c8b04ea628ed9713a8e207aeba9e7f`; dernière CI inspectée : `43665485066` **rouge avant correctifs**; CI des nouveaux commits **non confirmée** (aucun run remonté immédiatement). Tests locaux, Chromium après correctif, Windows, OBS réel, GTX1060/1650 non exécutés. PR #16 brouillon, aucun merge ni modification hors Studio.
- **Reprise exacte S** : inspecter le run Actions associé au HEAD et réparer s'il est rouge; en particulier contrôler la fin A/V du second export avec FFprobe, sans relâcher le seuil. **Puis M (1–2 tranches)** : E2E import manifeste pendant préparation d'export et restauration après navigation; **puis M–L** ADR FreeCut/OpenReelio. Si une CI verte valide les deux tests, mettre à jour STATUS et PR #16 avec sa référence.


## Reprise 2026-11-15 05h Europe/Paris — A/V Chromium, capture cadencée
- HEAD initial `e7950962`; run [43670553769](https://github.com/Sathancabrol/monorepo/actions/runs/43670553769) **failure** au step Chromium EDIT export E2E. Node, HTTP/IndexedDB, fixture A/V passent; export EDIT différé VP8/Opus passe (écart fin -0,014 s, son 440 Hz), second export échoue : fin vidéo 1,369 s contre fin audio 2,532 s. Le compteur binaire de marqueur n'a donc pas suffi à garantir des trames vidéo continues.
- Commits : `56321018` enrichit le diagnostic FFprobe avec compte et 8 derniers paquets par flux, sans assouplir les seuils; `db509fc3` remplace la capture manuelle seule `captureStream(0)` par `captureStream(24)` avec `requestFrame()` optionnel, afin de laisser Chromium produire des horodatages vidéo réguliers; `4ebebd01` ajoute un garde de régression Node.
- **Statut exact** : correctif applicatif poussé mais efficacité A/V non encore démontrée par la CI du dernier commit; pas de test local, Windows, OBS réel ni GTX1060/1650. Aucune modification hors Studio. PR #16 brouillon.
- **Reprise exacte (S)** : vérifier la CI du HEAD après `4ebebd01`. Si échec, lire les queues de paquets vidéo/audio; distinguer capture arrêtée, timestamp erroné et cadence insuffisante, sans relever le seuil de 0,6 s. Si verte, poursuivre E2E import manifeste IndexedDB pendant préparation d'export et après navigation (**M, 1–2 tranches**). Ensuite ADR FreeCut/OpenReelio (**M–L**). Dernière CI inspectée : `43670553769` failure; dernière CI verte antérieure : `43651256457`.


## Reprise 2026-11-15 06h Europe/Paris — CI Node rouge, assertion de capture suréchappée
- HEAD initial `5338ffec`; [run 43674604433](https://github.com/Sathancabrol/monorepo/actions/runs/43674604433) **failure** : analyse statique OK, Node 69/70, échec unique `EDIT export uses paced canvas capture instead of manual-only frames`; Chromium/IndexedDB/A/V/manifeste sautés.
- Cause prouvée par logs : regex Node du test cherchait des antislashs littéraux (`/stream=canvas\\\\.captureStream.../`) alors que le code applicatif contient `stream=canvas.captureStream(24)`; le code produit n'est pas incriminé par cette CI.
- Correctif test [5beac947](https://github.com/Sathancabrol/monorepo/commit/5beac9475637bdbba67850328dd746b923fdb8ce) : assertions exactes `includes` sur capture 24 fps et exclusion de capture manuelle 0 fps; aucun changement applicatif, aucun autre projet ni main.
- **Statut** : correctif poussé, CI de ce commit **non encore confirmée**; ne pas annoncer le second export A/V résolu. Windows GTX1060/1650, OBS réel et écoute humaine non testés. PR #16 brouillon.
- **Reprise exacte S** : vérifier CI au HEAD, particulièrement Node puis FFprobe des deux exports A/V; si rouge, lire logs, réparer sans assouplir tolérance. **Ensuite M (1–2 tranches)** : E2E import manifeste EDIT concurrent avec préparation export et restauration après navigation. Puis ADR FreeCut/OpenReelio M–L. Dernier run inspecté 43674604433 (failure), dernier commit test 5beac947.


## Reprise 2026-11-15 07h Europe/Paris — diagnostic A/V et marqueur non aliasable
- HEAD initial `b8b6accb`; CI [43679212722](https://github.com/Sathancabrol/monorepo/actions/runs/43679212722) **failure** : static parse, Node, HTTP/IndexedDB et fixture A/V Opus verts; E2E export EDIT échoue **dès le premier export différé**. FFprobe : vidéo 51 paquets, fin 1,670 s; audio 42 paquets, fin 2,559 s; décalage 0,889 s. Dernières images vidéo 1,404–1,637 s, audio continue à 2,499 s. Le manifeste EDIT est sauté. La capture 24 fps seule n'a donc pas résolu le défaut.
- Correctif expérimental applicatif [a69509b5](https://github.com/Sathancabrol/monorepo/commit/a69509b5dd6246f375708ce32f45e304464b8b07) : remplace le marqueur alternant entre deux couleurs par un compteur 24 bits encodé dans trois blocs de 8 pixels, pour éviter l'aliasing lorsque des dessins intermédiaires sont perdus. Tests structurels mis à jour [e2f41820](https://github.com/Sathancabrol/monorepo/commit/e2f418200b0d99ffc5c2d65e2a1426973b215e76), [753f9010](https://github.com/Sathancabrol/monorepo/commit/753f90100329954802cfd37e4381ed646d981b56). **Hypothèse, non validation A/V**; ne pas assouplir seuil 0,6 s.
- Reprise exacte **S** : vérifier CI du HEAD, en priorité Node puis E2E FFprobe. Si rouge A/V, instrumenter cadence de `drawEditor`/MediaRecorder et vérifier si le navigateur cesse de capturer malgré des pixels uniques; envisager rendu/export par pipeline FFmpeg hors MediaRecorder pour garantie temporelle, sans annoncer correction acquise. Si vert, E2E import manifeste concurrent et navigation (**M, 1–2 tranches**), puis ADR FreeCut/OpenReelio (**M–L**).
- Aucun essai Windows/GTX, OBS réel, écoute humaine ou merge main. PR #16 brouillon. Dernier run vérifié : 43679212722 (rouge avant correctif). Dernier commit de test : 753f9010.


## Reprise 2026-11-15 08h Europe/Paris — CI Node et marqueur 24 bits
- HEAD initial `894a539d`; [run 43683809270](https://github.com/Sathancabrol/monorepo/actions/runs/43683809270) **failure** : static parse OK, Node 67/70; trois assertions obsolètes après le passage du marqueur Canvas à 24 bits (`edit-canvas-capture`, `edit-export-async-guards`, `editor-export`). Chromium/IndexedDB/A/V non exécutés.
- Correctifs tests poussés : `5b0a66f4` attend les trois blocs RGB, `24c15ecf` attend le compteur monotone, `9eb90170` tolère les commentaires entre garde recording et compteur. **Aucun code applicatif modifié**; ces assertions n'établissent pas la synchronisation A/V.
- **CI du dernier commit à confirmer**; pas de test Node local, pas de Chromium ni Windows/GTX. Ne pas annoncer A01/A03 terminées.
- **Prochaine action S** : vérifier le run CI du HEAD; si Node rouge corriger les assertions; si E2E A/V rouge, analyser FFprobe et envisager un export déterministe plutôt que multiplier les marqueurs Canvas. Puis **M (1–2 tranches)** : import EDIT/IndexedDB concurrent et reprise navigation. PR #16 reste en brouillon, aucun merge main ni projet voisin.


## Reprise 2026-11-15 09h Europe/Paris — CI verte, récupération EDIT après navigation
- HEAD initial `7277a2d0`; [CI 43687808793](https://github.com/Sathancabrol/monorepo/actions/runs/43687808793) **success** au même SHA. Les précédents runs annulés ne sont pas des échecs. Cette validation couvre le workflow Studio, notamment les tests Chromium et A/V tels que configurés, sans preuve Windows.
- Incrément [d9d4b9b5](https://github.com/Sathancabrol/monorepo/commit/d9d4b9b5b84d0c6e894dde20155148763c727aa9) : le test `browser_edit_manifest_e2e.py` recharge la page après undo/redo, importe le vrai Portable exporté, puis vérifie timeline, piste audio et média embarqué. Test **poussé, non encore exécuté/validé sur ce commit**.
- **Reprise S** : vérifier CI du HEAD après ce test; si rouge, lire logs et réparer. **Ensuite M** : couvrir import manifeste pendant préparation export et restauration des médias après navigation; puis **M–L** : ADR FreeCut/OpenReelio. Ne pas déclarer Windows/OBS réel validés. PR #16 brouillon, aucun merge main.


## Reprise 2026-11-15 10h Europe/Paris — réparation E2E manifeste après navigation
- HEAD initial `0f040858`; [CI 43692729238](https://github.com/Sathancabrol/monorepo/actions/runs/43692729238) **failure** au step `Chromium EDIT manifest import`, assertion `EDIT timeline lost on navigation` ligne 168. Static parse, Node, IndexedDB, fixture A/V, export EDIT VP8/Opus (écarts -14 ms et +8 ms), undo/redo et split Portable passent.
- Cause identifiée par lecture : `fromEditInterchange` rend des clips sans `name`, alors que `loadProject` applique `validateClip` qui ajoute `name: 'Clip'`. L'égalité structurelle du projet portable change donc après navigation. Correctif applicatif [24b373b3](https://github.com/Sathancabrol/monorepo/commit/24b373b35e4c15429fc1c4e9322e51f8cd4f8ba4) : normaliser les clips dès l'import du manifeste, avant commit d'historique et export. Régression Node [74d36117](https://github.com/Sathancabrol/monorepo/commit/74d36117adf7c1f0778d69588558977a2d5dd95f) : stabilité après normalisation et rechargement.
- **Statut exact** : correctifs poussés; nouvelle CI sur `74d36117` et ce checkpoint non encore confirmée; pas de tests exécutés localement, pas de validation Windows/OBS réel/GTX. PR #16 brouillon, aucun merge ni autre projet modifié.
- **Reprise S** : inspecter CI au dernier HEAD et réparer si rouge, particulièrement `Chromium EDIT manifest import`. **Puis M (1–2 tranches)** : import manifeste pendant préparation d'export et tests de concurrence, en préservant l'atomicité. **Puis M–L** : ADR FreeCut/OpenReelio. Aucun changement de seuil A/V.


## Reprise 2026-11-15 11h Europe/Paris — import concurrent pendant export
- Relecture du backlog, HANDOFF, STATUS, SESSION_PLAN, workflow dédié, PR #16 et issues #11–#17. HEAD initial `5b734dcc`; CI [43696861474](https://github.com/Sathancabrol/monorepo/actions/runs/43696861474) **success** pour ce SHA.
- **Tranche livrée** : commit [88e46bc1](https://github.com/Sathancabrol/monorepo/commit/88e46bc19fb9068f72b012fac943f147f0e7c93b) étend `tests/browser_edit_manifest_e2e.py` : pendant un export WebM EDIT actif (MediaRecorder), soumettre un manifeste valide, vérifier le refus explicite, attendre le vrai téléchargement, puis vérifier l'intégrité du montage et de la piste audio via Portable. Le test de restauration après navigation reste ensuite exécuté.
- **Validation** : code poussé sur branche dédiée, **CI du nouveau commit non encore confirmée**; aucun test Windows/OBS/GTX ni écoute réelle. La CI verte 43696861474 ne couvre PAS ce nouveau scénario.
- **Prochaine action exacte S** : vérifier le job CI au SHA 88e46bc1 (notamment Chromium EDIT manifest import); si rouge analyser les logs et réparer. Si vert, poursuivre une tranche M sur la concurrence durant la préparation asynchrone de l'export et les cas de changement d'espace; puis ADR FreeCut/OpenReelio M–L. Ne pas fusionner main.


## Reprise 2026-11-15 12h Europe/Paris — CI A/V rouge, fin de capture
- HEAD initial `6e8ab074`; [CI 43702302505](https://github.com/Sathancabrol/monorepo/actions/runs/43702302505) **failure** sur `Chromium EDIT export E2E`, avant le test manifeste concurrent. Premier export différé vert (VP8/Opus, décalage fin -20 ms), second export : fin vidéo 1,467 s contre fin audio 2,530 s (30 paquets vidéo, 42 audio). Les tests précédents passent. Ne pas déclarer la synchronisation résolue.
- Correction ciblée [87ec1f22](https://github.com/Sathancabrol/monorepo/commit/87ec1f22cbe7b27ab02f2d00ed19f63c5ec21119) : `drawEditor` ne stoppe plus `MediaRecorder` **avant** le dessin de la dernière image; la demande `requestFrame` est exécutée d'abord. Régression structurelle [60e1c3d9](https://github.com/Sathancabrol/monorepo/commit/60e1c3d9cb42d084746b8b3a622279905b2a068d). Hypothèse causale partielle, pas une preuve de correction des 1,063 s de dérive.
- **Tests** : aucun Node/Chromium local dans cette reprise. **CI du nouveau HEAD non confirmée**. Pas de test Windows GTX1060/1650, OBS réel ou écoute humaine.
- **Reprise S** : vérifier CI sur `60e1c3d9` puis checkpoint. Si A/V toujours rouge, instrumenter fréquence/horodatages de frames capturées et envisager pipeline de rendu FFmpeg déterministe (M–L), sans assouplir le seuil. Si CI verte, vérifier le nouveau test de concurrence import manifeste puis avancer A02 (M, 1–2 tranches). ADR FreeCut/OpenReelio ensuite (M–L). PR #16 brouillon; aucun merge ni projet voisin.


## Reprise 2026-11-15 13h Europe/Paris — instrumentation dérive A/V
- HEAD initial `fdffb37c`; [CI 43706499713](https://github.com/Sathancabrol/monorepo/actions/runs/43706499713) **failure** : static parse, Node, IndexedDB et fixture A/V réussis; premier export EDIT différé OK (écart fin -260 ms), second export EDIT KO : fin vidéo 1,199 s / audio 2,526 s, 23 paquets vidéo / 42 audio, dérive 1,327 s. Test manifeste concurrent sauté.
- Tranche [7de2bc8a](https://github.com/Sathancabrol/monorepo/commit/7de2bc8afdb0a146863a8d67f42404a9d2694a7e) : télémétrie **uniquement dans l'E2E Chromium**, sans changement de produit ni tolérance A/V : horodatages des appels `requestFrame()`, fréquence de capture demandée, nombre de requêtes, intervalle maximal et dernières requêtes, imprimés seulement si l'assertion A/V échoue. Objectif : distinguer absence de production Canvas et perte/retard d'encodage MediaRecorder.
- **Validation** : logs de CI précédente inspectés; nouvelle instrumentation poussée, **CI du nouveau commit à confirmer**. Aucune preuve que le défaut A/V soit réparé; Windows/GTX/OBS/écoute humaine non testés. PR #16 reste brouillon; aucun merge main ni modification des projets voisins.
- **Prochaine action exacte S** : vérifier la CI au HEAD puis lire `EDIT Canvas capture diagnostic` dans le job en cas d'échec. Si les requêtes couvrent 2,5 s mais les paquets vidéo finissent vers 1,2 s, investiguer MediaRecorder/encodeur et envisager un export FFmpeg déterministe (M–L); sinon réparer la boucle de dessin Canvas (M). Ensuite reprendre l'E2E manifeste concurrent et l'ADR FreeCut/OpenReelio (M). Estimation restante : diagnostic S, réparation A/V M–L, E2E concurrence M. Ne pas assouplir le seuil 0,6 s.

## Reprise 2026-11-15 14h Europe/Paris — CI verte, récupération après export
- Relecture du backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17, code et workflow CI dédié. HEAD initial `0fca0e42`; [CI 43712064235](https://github.com/Sathancabrol/monorepo/actions/runs/43712064235) **success** au SHA exact : les diagnostics de capture A/V instrumentés n'ont pas déclenché d'échec sur ce run. Cela ne garantit pas la stabilité répétée du second export ni Windows.
- **Tranche livrée** : [4487f60e](https://github.com/Sathancabrol/monorepo/commit/4487f60e2dc1e9142b15ecf677768d985005deed) ajoute à `tests/browser_edit_manifest_e2e.py` un import de manifeste valide **après** un export concurrent et son rejet attendu, suivi d'undo/redo. Contrôle l'absence de verrou d'export résiduel et la reprise de l'historique.
- **Preuve** : commit poussé sur la branche dédiée; **CI du nouveau test non encore vérifiée**, pas de test Node/Chromium local, pas de Windows GTX 1060/1650, ni OBS réel ni écoute humaine. Aucun changement de seuil A/V, pas de merge main.
- **Reprise S** : vérifier la CI au SHA `4487f60e` ou au checkpoint suivant; si rouge lire les logs et réparer en priorité. Si verte, ajouter un test de préparation asynchrone d'export / import (M, 1–2 tranches) ou audit ADR FreeCut/OpenReelio (M–L). Conserver PR #16 en brouillon. Estimation restante : concurrence M, ADR M–L, recette matérielle BLOCKED_WINDOWS.

## Reprise 2026-11-15 15h Europe/Paris — robustesse historique EDIT après export
- Synchronisation : HEAD initial `511a54d8`; CI [43716948711](https://github.com/Sathancabrol/monorepo/actions/runs/43716948711) **success** au SHA exact (tests Chromium A/V, manifeste, IndexedDB). Les runs précédents annulés ne sont pas des échecs.
- Tranche livrée : [c4d91218](https://github.com/Sathancabrol/monorepo/commit/c4d912184fea027c776810c1332817f77856d078) ajoute un scénario E2E sur vrai HTTP/IndexedDB : après export et import valide, rejeter un manifeste à média inexistant, contrôler la conservation du montage et l'absence d'entrée d'historique fantôme via undo/redo. Régression codée, **CI du nouveau test pas encore confirmée**; aucun test Windows.
- Reprise prioritaire S : lire la CI au HEAD après checkpoint, réparer toute régression. Puis M : couvrir l'import pendant la préparation asynchrone de l'export, sans course de statut Playwright. Ensuite M–L : ADR FreeCut/OpenReelio. PR #16 brouillon, aucun merge ni autre projet touché.
- Estimation restante : CI S, concurrence asynchrone M, ADR M–L, recette Windows BLOCKED_WINDOWS. Dernier run confirmé vert : 43716948711. Nouveau test non validé tant que sa CI ne passe pas.


## Reprise 2026-11-15 16h Europe/Paris — CI rouge A/V, trame terminale différée
- HEAD initial `b560d68b`; [CI 43721983593](https://github.com/Sathancabrol/monorepo/actions/runs/43721983593) **failure** sur `Chromium EDIT export E2E`, pendant l'export après préparation WebAudio différée. Node, HTTP/IndexedDB et fixture A/V synthétique réussis. Fin vidéo 1,601 s / audio 2,557 s (32 paquets vidéo / 42 audio), décalage 956 ms; test manifeste non exécuté.
- Correctif expérimental [5eb4c978](https://github.com/Sathancabrol/monorepo/commit/5eb4c978c414ba670560a68aa2da2904262a5445) : reporter l'arrêt du MediaRecorder après une nouvelle animation, une demande de trame et 120 ms de vidage d'encodeur, avec garde contre les arrêts multiples. Tests structurels ajustés dans [69f13216](https://github.com/Sathancabrol/monorepo/commit/69f132161eeb72ced1f8a22ad667cc56d317ce9a) et [2a367ec8](https://github.com/Sathancabrol/monorepo/commit/2a367ec85a667d77263193429e5cc0d5ab1831c3). **Hypothèse non prouvée**; ne pas conclure que 956 ms sont corrigées.
- **Validation** : CI du nouveau HEAD encore à confirmer; aucun Node/Chromium local ni test Windows/GTX/écoute réelle. Prochaine action S : lire la CI du HEAD, corriger toute assertion Node; si A/V toujours rouge, capturer diagnostics des requêtes et considérer un export FFmpeg déterministe (M–L) plutôt que multiplier les temporisations. Puis E2E concurrence import manifeste (M), ADR FreeCut/OpenReelio (M–L). PR #16 brouillon; aucun merge ni projet voisin.

## Reprise 2026-11-15 17h Europe/Paris — CI verte et erreur MediaRecorder
- HEAD initial `2b6d0c55`; [CI 43727367256](https://github.com/Sathancabrol/monorepo/actions/runs/43727367256) **success**, workflow dédié, sur ce SHA. Cette réussite ponctuelle ne prouve pas une stabilité A/V répétée ni Windows.
- Code [0f9ae2c1](https://github.com/Sathancabrol/monorepo/commit/0f9ae2c16bc19a64eef4baa32187e238929c4ab4) : gestion de l'événement `MediaRecorder.onerror` et refus de téléchargement d'un export EDIT si enregistrement en erreur ou sans chunk. Les pistes sont libérées par `onstop`; aucun autre projet modifié.
- Régression [d70afbcb](https://github.com/Sathancabrol/monorepo/commit/d70afbcb243b8a4f3d1e86f72fd30865a79b0be9) : assertion Node structurelle que la garde précède le téléchargement. **Aucune exécution Node/Chromium locale**; CI de ces nouveaux commits non encore vérifiée.
- Reprise exacte S : vérifier le workflow du dernier HEAD et réparer si rouge; compléter la validation fonctionnelle navigateur d'un MediaRecorder qui échoue (injection contrôlée), puis E2E import manifeste pendant préparation asynchrone (M). Si A/V intermittent, instrumenter les paquets et envisager FFmpeg déterministe (M–L). ADR FreeCut/OpenReelio (M–L) ensuite.
- Limites : Windows GTX1060/1650, écoute humaine et OBS réel non testés; PR #16 brouillon; aucune fusion main. Estimation restante : test erreur S–M, concurrence M, stabilité A/V M–L, recette Windows BLOCKED_WINDOWS.


## Reprise 2026-11-15 18h Europe/Paris — réparation CI Node après gestion erreur MediaRecorder
- CI du HEAD précédent `e14c1a04` : [run 43733480014](https://github.com/Sathancabrol/monorepo/actions/runs/43733480014) **failure**, `Static parse` réussi, `npm test` 72/73; E2E Chromium non exécutés. L'assertion `all EDIT recording mutation guards also cover asynchronous preparation` attendait un seul garde `if(editorRecorder?.state==='recording')`, mais la gestion `MediaRecorder.onerror` ajoutée au commit précédent introduit un second garde intentionnel, qui arrête uniquement un recorder actif. Aucun défaut d'exécution du produit démontré par cet échec.
- Correctif de régression [`f295ae1a`](https://github.com/Sathancabrol/monorepo/commit/f295ae1a5a471b7d1ba950fc8659383303c94b65) : le test attend les deux gardes, vérifie explicitement le garde du handler d'erreur et préserve celui du compteur de trames; aucune modification applicative, aucun relâchement des seuils A/V.
- **Validation** : code de test poussé, nouvelle CI **non encore confirmée**; aucun Node/Chromium local ni Windows/GTX/OBS réel. PR #16 brouillon, aucun merge main ou projet voisin.
- **Reprise exacte (S)** : vérifier CI du HEAD après ce checkpoint, réparer tout échec Node ou Chromium en priorité. **Puis S–M** : test Chromium d'une erreur MediaRecorder simulée, contrôlant absence de téléchargement vide et libération des pistes; **puis M** : import manifeste pendant préparation asynchrone de l'export; **puis M–L** ADR FreeCut/OpenReelio. Estimation restante : CI S, test erreur S–M, concurrence M, stabilité A/V M–L, recette Windows bloquée.

## Reprise 2026-11-15 19h Europe/Paris — CI rouge A/V, zone animée d'encodage
- Synchronisation : CI [43738532826](https://github.com/Sathancabrol/monorepo/actions/runs/43738532826) **failure** au SHA `e38a7034`. Node et IndexedDB/fixture A/V verts; vrai export EDIT échoue avec vidéo fin 1,931 s contre audio 2,661 s (écart 730 ms, seuil 600 ms). Diagnostic Canvas : 83 demandes de trame couvrant 2684 ms; le navigateur a néanmoins encodé seulement 30 paquets vidéo. Les imports manifeste sont sautés par la CI rouge.
- Hypothèse : l'encodeur Chromium fusionne des images quasi statiques malgré les demandes de capture. Correctif expérimental [e8a2cb53](https://github.com/Sathancabrol/monorepo/commit/e8a2cb539c484e59242a1ccf99421d9693e0be0c) : motif animé 96x96 en 64 tuiles distinctes sur le canvas de capture, plutôt que 24x8 pixels; [d8b43c92](https://github.com/Sathancabrol/monorepo/commit/d8b43c92b41ab2f84b052fdd3ede99d3fcc7131a) ajoute un test structurel de régression.
- **Validation** : commits poussés; nouvelle CI pas encore confirmée, aucun Node/Chromium local ni Windows/GTX. La correction n'est PAS démontrée. Le motif est visible dans le coin inférieur droit du fichier exporté; compromis provisoire à remplacer par pipeline de rendu déterministe si nécessaire.
- **Reprise exacte S** : lire le run CI du nouveau HEAD, corriger si rouge. Si le problème persiste, ne plus augmenter les délais/motifs; instrumenter timestamps et étudier FFmpeg ou WebCodecs avec timestamps déterministes (M–L). Si verte, tester MediaRecorder.onerror dans Chromium (S–M), puis import manifeste pendant préparation asynchrone (M), ADR FreeCut/OpenReelio (M–L). Blocage Windows et écoute humaine inchangé; PR #16 brouillon, aucun merge main.

## Reprise 2026-11-15 20h Europe/Paris — CI Node réparée, validation A/V en attente
- CI du HEAD précédent `849816d0` : [run 43744189416](https://github.com/Sathancabrol/monorepo/actions/runs/43744189416) **failure**, étape `API smoke tests`, 73/74 tests Node réussis; E2E Chromium non exécutés. Le test `edit-canvas-capture.test.mjs` exigeait encore le marqueur 24x8 à 3 canaux, alors que le code export utilise depuis `e8a2cb53` une grille 8x8 de tuiles 12px (96x96). Défaut d'assertion structurelle obsolète, pas preuve d'un défaut runtime.
- Correctif [7684e816](https://github.com/Sathancabrol/monorepo/commit/7684e816cb71cbb3876fd6b82629044d831653df) : assertion du marqueur 64 tuiles, de sa variation selon compteur et de son dessin avant `requestFrame()`. Aucun seuil A/V abaissé, aucun code applicatif changé.
- **Validation** : commit poussé, CI du nouveau HEAD non encore confirmée; aucun test Node/Chromium local ni Windows/GTX/OBS réel. Ne pas déclarer le décalage A/V corrigé. PR #16 brouillon, aucun merge main.
- **Reprise exacte S** : vérifier le run CI associé au nouveau HEAD (après checkpoint), réparer tout échec. Si Chromium EDIT A/V reste rouge, analyser `ffprobe` et les paquets; ne plus ajouter de délais ou marqueurs, privilégier diagnostic de timestamps et étude d'un pipeline FFmpeg/WebCodecs déterministe (M–L). Si verte, test Chromium d'erreur MediaRecorder (S–M), puis concurrence import manifeste/IndexedDB (M), puis ADR FreeCut/OpenReelio (M–L). Windows BLOCKED_WINDOWS.


## Reprise 2026-11-15 21h Europe/Paris — CI verte, erreur MediaRecorder E2E
- Relecture des quatre documents de pilotage, PR #16, issues #11–#17, workflow dédié et code d'export. Dernière CI confirmée sur le checkpoint précédent : [43750183694](https://github.com/Sathancabrol/monorepo/actions/runs/43750183694) **success**, y compris Node, Chromium EDIT A/V, IndexedDB, manifeste, paquet preview. Succès ponctuel, stabilité A/V non garantie.
- Nouvelle tranche : [ce6e745d](https://github.com/Sathancabrol/monorepo/commit/ce6e745d59fdf69624285569ba60db2e0f9bf083) ajoute `tests/browser_recorder_error_e2e.py`, injection contrôlée d'une erreur MediaRecorder pendant un export EDIT réel sur HTTP Chromium, vérification qu'aucun WebM partiel n'est téléchargé, que les pistes sont stoppées et qu'aucune erreur JS n'apparaît. [15e8290c](https://github.com/Sathancabrol/monorepo/commit/15e8290caf27857b740ab5fe023fb4eeb1dd8019) corrige l'exécution de l'injection à l'initialisation; [5a7fef88](https://github.com/Sathancabrol/monorepo/commit/5a7fef880832e0ac8b1f43adb4a21f12c9b0bf91) intègre ce scénario au workflow CI dédié et à py_compile.
- **Validation exacte** : nouveau test poussé, **pas encore exécuté/confirmé en CI** au moment du checkpoint. Aucun essai local Node/Chromium ni Windows/OBS/GTX/écoute humaine. PR #16 reste brouillon, aucun merge main ni autre projet modifié.
- **Reprise S** : vérifier le workflow au dernier HEAD, lire les logs du step `Chromium EDIT MediaRecorder error`; réparer immédiatement toute régression (notamment injection et statut). **Puis M** : E2E import manifeste pendant la préparation asynchrone WebAudio, sans course sur statut, et tests de conservation du montage. **Puis M–L** : ADR FreeCut/OpenReelio. Stabilité A/V et recette Windows restent ouvertes. Estimations relatives : CI S, concurrence M, ADR M–L.


## Reprise 2026-11-15 22h Europe/Paris — concurrence manifeste pendant préparation WebAudio
- Synchronisation : [CI 43755892230](https://github.com/Sathancabrol/monorepo/actions/runs/43755892230) **success** au SHA `0203e5126f9f90a512ca5624ec9ccaf6c5132ef3`, y compris nouveau scénario Chromium d'erreur MediaRecorder. Ce résultat ne prouve ni répétabilité A/V ni recette Windows.
- Nouveau test [85a0c8eb](https://github.com/Sathancabrol/monorepo/commit/85a0c8ebebcde545983e80ab8ce39f0379102027) : dans le véritable E2E export EDIT avec WAV 440 Hz et préparation `AudioContext.resume()` suspendue, tentative d'import d'un manifeste **valide** avec asset IndexedDB existant; assertion de rejet explicite avant création de MediaRecorder, puis poursuite de l'export, vérification ffprobe/Opus et conservation des clips/audio par export Portable. Aucun délai artificiel ajouté.
- **Validation** : CI précédente verte, nouveau test commité mais CI du nouveau HEAD **à confirmer**. Pas d'exécution locale Playwright/Windows, pas de preuve matérielle GTX1060/1650 ou OBS réel. PR #16 brouillon, aucun merge main.
- **Reprise exacte S** : inspecter CI au dernier HEAD après checkpoint; réparer en priorité toute assertion/erreur Chromium. **Puis S–M** : renforcer le test pour confirmer qu'un import rejeté ne crée pas d'entrée undo/redo pendant la préparation, puis **M–L** : ADR comparatif FreeCut/OpenReelio (#12). Stabilité A/V répétée M–L; recette Windows BLOCKED_WINDOWS.

## Reprise 2026-11-15 23h Europe/Paris — historique après rejet concurrent
- Relecture backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17 et workflow CI dédié. HEAD initial `07eb9512`; [CI 43761014885](https://github.com/Sathancabrol/monorepo/actions/runs/43761014885) **success** (Node, Chromium A/V, IndexedDB, manifeste, MediaRecorder et packaging). La stabilité répétée A/V et Windows restent non prouvés.
- Commit [828dc14d](https://github.com/Sathancabrol/monorepo/commit/828dc14d833e90d5f8f10e59e9f86f4f02531a54) : extension du vrai E2E Chromium manifeste pour vérifier qu'un import valide refusé pendant MediaRecorder n'ajoute **aucune entrée undo** : Undo revient directement au montage pré-import, Redo restaure le montage précédent. Contrôle Portable/IndexedDB, sans changement applicatif.
- **Validation** : commit poussé; CI de ce commit **non encore confirmée** à ce checkpoint. Pas de test local Chromium, Windows, OBS ni GTX.
- **Reprise exacte S** : consulter la CI du HEAD et réparer si rouge. **Ensuite M–L** : ADR FreeCut/OpenReelio (#12), comparaison format/licences/interopérabilité sur références vérifiées; si besoin poursuivre couverture des erreurs d'import pendant WebAudio. Ne modifier que ce dossier et le workflow dédié. PR #16 brouillon; aucun merge main.


## Reprise 2026-11-16 00h Europe/Paris — CI rouge, diagnostic PTS renforcé
- Relecture backlog/HANDOFF/STATUS/SESSION_PLAN, PR #16 et issues #11–#17. La CI du checkpoint précédent `38e345a5` : [run 43766852675](https://github.com/Sathancabrol/monorepo/actions/runs/43766852675) **failure**, étape Chromium EDIT export E2E; la fixture A/V synthétique indépendante est verte.
- Échec concret pendant préparation WebAudio différée : vidéo fin 1,506 s (46 paquets), audio fin 2,677 s (44 paquets), dérive **1,171 s**, au-delà du seuil inchangé 0,6 s. Les tests suivants n'ont pas été exécutés. Il s'agit d'une régression intermittente du rendu, non d'une assertion obsolète.
- Commit [bfb8beee](https://github.com/Sathancabrol/monorepo/commit/bfb8beee5afd3b0b50d2254f572e7de9a04c4ddb) : le test E2E affiche désormais les PTS vidéo initiaux/finaux, les plus grands trous entre paquets, durées de flux et delta A/V même lors d'un échec; aucun seuil assoupli, aucun délai artificiel. **Diagnostic seulement, correctif applicatif encore à concevoir.**
- **Validation** : code de diagnostic poussé, CI sur ce nouveau commit non confirmée; aucun test local Playwright, Windows/GTX, OBS ou écoute humaine. PR #16 reste brouillon; aucun merge main.
- **Reprise exacte P0 (M–L)** : vérifier la CI au HEAD, analyser les trous PTS pour départager arrêt prématuré des frames et coalescence; concevoir et tester une sortie à horodatages déterministes (FFmpeg local/WebCodecs) plutôt que d'ajouter des temporisations. Ensuite ADR FreeCut/OpenReelio (#12, M–L), puis imports IndexedDB. Tests Windows BLOCKED_WINDOWS.


## Reprise 2026-11-16 01h Europe/Paris — pivot vers assemblage des moteurs existants
- Relu backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16 (issue associée) et issues #11–#17; workflow dédié. CI du checkpoint précédent `c3bca1ab` : [run 43772642086](https://github.com/Sathancabrol/monorepo/actions/runs/43772642086) **failure** à Chromium EDIT export; Node et fixture synthétique réussis. Export réel : 83 requêtes de trames en 2692 ms, 59 paquets vidéo jusqu'à 1,999 s, audio jusqu'à 2,716 s, écart 717 ms (seuil 600 ms). Pas de gros trou PTS : la queue des images n'est pas encodée. Défaut intermittent **non corrigé**.
- Rectification stratégique utilisateur, échéance alpha mercredi 18 novembre : **assembler les moteurs libres existants** plutôt que reconstruire les 12 moteurs. Commits [05d50f7f](https://github.com/Sathancabrol/monorepo/commit/05d50f7f4c6bf46732ca5e9983c00fca1149bd45) registre explicite des 12 contrats, [b39c4f9a](https://github.com/Sathancabrol/monorepo/commit/b39c4f9a2e6c429fc86485bb3961873358ff172b) endpoint local en lecture seule `GET /api/integrations` avec sondes OBS/ComfyUI et distinction port joignable/fonction vérifiée, [22f0e8ba](https://github.com/Sathancabrol/monorepo/commit/22f0e8bab06bac872ecb949db0d89cc554f6c266) test HTTP de 12 espaces, [08d8f886](https://github.com/Sathancabrol/monorepo/commit/08d8f886bf50e8251868da654249eb9dd861d6ad) matrice `docs/INTEGRATION_MATRIX.md`.
- **Validation** : nouveau code/test poussé, CI du nouveau HEAD **non encore confirmée**; aucun Node/Chromium local ni test Windows/OBS/GTX. Inventaire et endpoint ne sont pas des connecteurs opérationnels supplémentaires; aucune licence de redistribution tierce vérifiée.
- **Reprise exacte P0 (S)** : lire CI du dernier HEAD; réparer toute régression. **Puis M** : afficher le registre dans CONTROL, tester l'interface et l'état des sondes; **puis M–L** : intégration réelle ComfyUI OUTPUT → LIBRARY avec protections chemin/SSRF et test E2E. **Parallèle A/V M–L** : étude FFmpeg local déterministe, pas de nouvelles temporisations MediaRecorder. Deadline 18/11 : alpha honnête, non terminée sans recette. PR #16 brouillon; aucun merge main ni autre projet modifié.
- Estimation relative restante : CI S, panneau CONTROL S–M, transfert ComfyUI M–L, export déterministe M–L, recette Windows BLOCKED_WINDOWS.


## Reprise 2026-11-16 02h Europe/Paris — CONTROL affiche les intégrations
- Relecture des documents de pilotage, matrice, issues #11–#17, PR #16 et workflow CI. La dernière preuve CI documentée reste le run [43772642086](https://github.com/Sathancabrol/monorepo/actions/runs/43772642086) rouge (dérive EDIT A/V 717 ms). Les runs du HEAD récent n'ont pas été confirmés; la recherche par SHA du commit de test renvoie zéro résultat, pas un succès.
- Livraison : [eabc6515](https://github.com/Sathancabrol/monorepo/commit/eabc65157cbce687f4a8aab6c422f2af3b8df661) panneau CONTROL affichant les 12 moteurs, contrats, statuts et sondes en lecture seule depuis l'API locale; [39dd84d6](https://github.com/Sathancabrol/monorepo/commit/39dd84d6680a79a80c83af9ce582ca02ff78e67d) alignement sur le schéma réel `{spaces:[...]}`; [257b1ed7](https://github.com/Sathancabrol/monorepo/commit/257b1ed72b63ce663678a674400ae180c878c6c4) test Node structurel du panneau et de l'absence d'injection HTML. Un port accessible n'est jamais affiché comme fonction vérifiée.
- Validation : commits poussés; test Node et navigateur **non exécutés localement**, CI de ces commits **non confirmée**. Pas de validation Windows/OBS/GTX, ni preuve de liaison ComfyUI→LIBRARY. Aucun autre projet ni main modifié; PR #16 brouillon.
- Reprise exacte P0 (S) : consulter la CI du HEAD et réparer si rouge. Puis P1 (M–L) : intégrer les sorties ComfyUI dans LIBRARY par API locale sécurisée, avec E2E sur fixture, validation type MIME, taille et chemins autorisés; ne pas utiliser des URL arbitraires. P0 parallèle (M–L) : moteur d'export FFmpeg déterministe plutôt que temporisations MediaRecorder. Échéance alpha 18/11, reste environ deux jours; Windows bloqué sans machine.


## Reprise 2026-11-16 03h Europe/Paris — réparation CI CONTROL
- Relecture des quatre documents de pilotage, matrice, PR #16, issues #11–#17, commits et workflow dédié. La CI [43783918051](https://github.com/Sathancabrol/monorepo/actions/runs/43783918051) sur `49a86829` est **failure** à `API smoke tests` : 75/76 tests réussis, `tests/control-integrations.test.mjs` ne se parse pas (`SyntaxError: missing ) after argument list`, ligne 16). La CI n'a donc pas atteint Chromium. Le problème A/V intermittent demeure distinct et non corrigé.
- Correctif réel [4549c3d5](https://github.com/Sathancabrol/monorepo/commit/4549c3d5ccd8c1d410a1e67034f33b944706ee7f) : remplace l'assertion ternaire invalide par un extrait CONTROL et une assertion `doesNotMatch` valide contre l'injection `innerHTML` d'un nom de moteur. Un seul fichier de test modifié; aucun seuil A/V assoupli.
- **Validation** : lecture du log GitHub Actions et correction poussée; **CI du nouveau HEAD à confirmer**, aucun test Node local ou Chromium/Windows réalisé dans cette session.
- **Reprise exacte P0 S** : consulter la CI du HEAD `4549c3d5`; réparer toute régression. **Puis P1 M–L** : ComfyUI output → LIBRARY via endpoint local sécurisé (validation des chemins, type MIME, taille, absence de SSRF), test HTTP avec serveur simulé et test navigateur d'import; **P0 A/V M–L** : explorer export déterministe FFmpeg sans bloquer les autres intégrations. Échéance alpha 18/11; Windows/GTX restent BLOCKED_WINDOWS. PR #16 brouillon, main inchangé.

## Reprise 2026-11-16 04h Europe/Paris — ComfyUI OUTPUT → LIBRARY (première liaison réelle)
- Synchronisation initiale : quatre docs, PR #16, issues #11–#17, workflow dédié et HEAD `cdeee0a4`. CI du HEAD initial [43789453862](https://github.com/Sathancabrol/monorepo/actions/runs/43789453862) **success** (Node/Chromium/packaging). Défaut A/V intermittent non considéré résolu par une seule CI verte.
- Code livré : `src/comfy-output.js` sélectionne uniquement un fichier listé dans l'historique d'un job ComfyUI terminé, type `output`, index borné, extension média autorisée, chemin/sous-dossier contrôlés et signature binaire. `GET /api/comfy/output?prompt_id=UUID&index=N` consulte uniquement `127.0.0.1:8188/history/{id}` puis `/view`, plafonne à 25 MiB, sans URL distante ni accès arbitraire au disque. GENERATE affiche des boutons d'import des sorties terminées vers `addFiles` et IndexedDB LIBRARY.
- Tests ajoutés : `tests/comfy-output.test.mjs` (job incomplet, traversée, entrée input, formats, signatures, taille) et test HTTP des paramètres invalides; syntaxe ajoutée au workflow dédié. Commits `76b66544`, `7184bf36`, `5f197dc8`, `0402b775`, `3ebcaa9d`, `ec14a9ee`, `e41da255`.
- **Validation** : nouveau code poussé, CI [43795914408](https://github.com/Sathancabrol/monorepo/actions/runs/43795914408) **queued à la dernière lecture**. Aucun ComfyUI réel ni navigateur Windows/GTX testé. Test HTTP de transfert de média avec faux serveur ComfyUI et E2E clic UI restent à écrire; ne pas annoncer la chaîne complète comme validée.
- **Reprise exacte P0 S** : inspecter la CI du nouveau HEAD et corriger immédiatement tout échec (notamment test de syntaxe Node). **Puis P1 M** : test HTTP intégral avec faux ComfyUI sur loopback 8188 (isoler les ports pour éviter conflit) et test Chromium de bouton → IndexedDB; prouver les octets et le refus des chemins. **Puis P0 M–L** : export EDIT déterministe via FFmpeg local (sans nouveau timeout), ADR FreeCut/OpenReelio. **Blocages** : ComfyUI Windows/OBS/GTX non accessibles, licences tierces non complètement auditées. Échéance alpha 18/11; main et autres projets inchangés.

## Reprise 2026-11-16 05h Europe/Paris — preuve HTTP ComfyUI simulée
- Synchronisation : backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17, workflow CI dédié. Les documents sont sous `projects/olympus-studio/docs/` (pas à la racine). Relecture du code `src/comfy-output.js`, `server.mjs` et des tests.
- Commit [ea36c44e](https://github.com/Sathancabrol/monorepo/commit/ea36c44eb604fecef6ae84cd07586739f6b0b626) : test d'intégration `tests/comfy-output-http.test.mjs` démarrant un faux ComfyUI sur 127.0.0.1:8188 et le véritable serveur Studio sur un port éphémère; vérifie le proxy `GET /api/comfy/output`, les octets PNG exacts, le MIME, le refus d'un index hors plage et d'un index invalide. Saute proprement si 8188 est déjà occupé pour ne pas perturber un service réel. Aucun modèle, service cloud ou matériel Windows utilisé.
- **Validation** : code poussé; [CI 43801858925](https://github.com/Sathancabrol/monorepo/actions/runs/43801858925) **in_progress** lors de la lecture. Le test HTTP n'est donc PAS encore confirmé vert. Aucun E2E Chromium clic GENERATE → IndexedDB ni ComfyUI réel validé. Défaut A/V intermittent toujours ouvert.
- **Reprise exacte P0 (S)** : consulter CI 43801858925 et réparer tout échec. **Puis P1 (M)** : E2E Chromium réel GENERATE → LIBRARY → IndexedDB avec fixture ComfyUI, en veillant à l'isolation des ports. **Puis P0 (M–L)** : exporter EDIT via FFmpeg/WebCodecs déterministe ou documenter fallback fiable, sans masquer la dérive. **P2 (M–L)** : ADR FreeCut/OpenReelio. Windows/GTX BLOCKED_WINDOWS. Échéance alpha 18/11; PR #16 brouillon, aucun merge main.


## Reprise 2026-11-16 06h Europe/Paris — E2E ComfyUI et CI A/V rouge
- Synchronisé backlog, HANDOFF, STATUS, SESSION_PLAN, matrice, PR #16, issues #11–#17, workflow et commits avant modifications. PR #16 reste draft; aucun merge main.
- CI [43801892878](https://github.com/Sathancabrol/monorepo/actions/runs/43801892878) **failure** : Node et IndexedDB/fixture A/V passent; EDIT export E2E échoue sur delta de fin A/V **676 ms** (vidéo 2,002 s, audio 2,678 s), seuil 600 ms inchangé. Les tests suivants et packaging ont été sautés. La panne est intermittente et non résolue; ne pas déclarer CI verte.
- Nouveau scénario `tests/browser_comfy_import_e2e.py` : mock ComfyUI 127.0.0.1:8188, vrai serveur Studio, UI GENERATE envoi workflow synthétique → suivi job terminé → import PNG → vérification Blob IndexedDB puis persistance après reload. Le workflow CI dédié lance ce test après l'E2E IndexedDB; commit test final `8384546c` et workflow `fb029d4b`. **Pas encore de preuve d'exécution CI du nouveau HEAD**, ni de test ComfyUI réel.
- Reprise exacte **P0 S** : inspecter la CI du HEAD `8384546c`, corriger toute erreur de sélecteur ou stockage du nouveau test; **P0 M–L** : résoudre la dérive réelle EDIT avec moteur de rendu/export déterministe (FFmpeg local ou WebCodecs) sans augmenter artificiellement les seuils; **P1 M** : test ComfyUI réel sur Windows si disponible, sinon continuer modules intégrables GitHub. Échéance alpha 18 novembre; packaging et GPU non validés.


## Reprise 2026-11-16 07h Europe/Paris — vérification ComfyUI E2E renforcée
- Relecture backlog, HANDOFF, STATUS, SESSION_PLAN, matrice, PR #16, issues #11–#17 et workflow dédié. La CI [43807993303](https://github.com/Sathancabrol/monorepo/actions/runs/43807993303) a son job `smoke` marqué **success** à la consultation, avant la modification ci-dessous; ne pas l'attribuer au nouveau commit.
- Commit `b1b56daf` : le test Chromium `browser_comfy_import_e2e.py` vérifie désormais **les octets exacts du PNG** et le MIME `image/png` dans IndexedDB, puis de nouveau les octets après rechargement. Le test précédent ne comparait que la taille, susceptible de masquer une corruption de même longueur.
- CI du commit `b1b56daf` **non encore confirmée**; inspecter les nouveaux jobs et réparer immédiatement tout échec. Aucun essai sur ComfyUI réel, Windows, GTX 1060/1650.
- **Prochaine tâche P0 M–L** : fiabiliser l'export A/V EDIT par un rendu à timestamps déterministes ou un fallback FFmpeg local avec détection de dépendance et refus explicite si indisponible; ne pas relever le seuil de dérive. **Ensuite P1 M** : finaliser packaging alpha et procédure de lancement Windows, avec matrice des fonctionnalités réellement démontrées. Échéance 18 novembre.


## 16/11/2026 08h — garde-fou E2E ComfyUI

- CI de référence [43807993303](https://github.com/Sathancabrol/monorepo/actions/runs/43807993303) : job `smoke` **success** sur le code de cette exécution antérieure. Elle ne prouve ni Windows ni ComfyUI réel.
- Correctif test `394c62ee` : `browser_comfy_import_e2e.py` échoue explicitement lorsque le port mock 8188 est occupé, au lieu de renvoyer un faux `SKIP` pouvant laisser une CI verte sans test. Ne jamais interférer avec un ComfyUI déjà actif.
- **CI du commit correctif : à vérifier** au prochain passage. Aucune preuve d'exécution locale Windows/GTX; aucune prétention d'avoir résolu la dérive A/V EDIT.
- **Reprise S** : contrôler le run du dernier HEAD et ses logs; si rouge, corriger avant toute autre intégration. **Puis M–L** : rendre l'export EDIT A/V déterministe (timestamps, encoder FFmpeg local en fallback si disponible) sans assouplir le seuil de 600 ms, tester par vrai E2E. **Puis M** : recette alpha et paquet téléchargeable documenté.


## Reprise 2026-11-16 09h Europe/Paris — CI rouge Portable après EDIT
- Sources relues : backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17, workflow runs, code EDIT/Portable. CI [43821883423](https://github.com/Sathancabrol/monorepo/actions/runs/43821883423) **failure** sur `ea9573b7`, étape Chromium EDIT export E2E. Contrairement à la dérive A/V précédente, les contrôles A/V de cette exécution ont réussi (écart final -44 ms, audio Opus et signal non silencieux); l'échec se produit ensuite lors de l'export Portable après undo/redo de clips : aucun événement download sous 15 s. Cause applicative encore inconnue.
- Commit [f5f8d5c0](https://github.com/Sathancabrol/monorepo/commit/f5f8d5c097afab1731a402c4a6b10dbc070d9b3f) : instrumente le scénario en capturant statut UI, état occupé du bouton et erreurs JS si téléchargement absent; attente portée à 30 s **uniquement pour la sérialisation Portable asynchrone**, sans modifier les seuils A/V. Ce commit ne constitue pas une correction prouvée du défaut.
- **Validation** : nouveau test poussé, CI du nouveau HEAD à confirmer. Aucune exécution Windows/GTX, aucune recette complète. PR #16 toujours brouillon; main intact.
- **Reprise exacte P0 S–M** : consulter la CI de `f5f8d5c0` (ou HEAD plus récent), lire le statut d'erreur Portable si échec, corriger la cause dans l'application et ajouter test de non-régression; ne pas masquer l'échec par un timeout. **Ensuite P0 M–L** : fiabilisation A/V déterministe/fallback FFmpeg si intermittence reproduite; **P1 M** : alpha packaging et procédure de recette. Échéance mercredi 18/11.


## Reprise 2026-11-16 10h Europe/Paris — intégrité Portable, CI à contrôler
- Sources relues : AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, issues #12/#14/#17 et CI du run 43829089439. Le run 43829089439 est **cancelled**, pas vert. La dernière panne analysable [43821883423](https://github.com/Sathancabrol/monorepo/actions/runs/43821883423) est le timeout de téléchargement Portable après undo/redo, tandis que le contrôle A/V du même run passait avec un delta de -44 ms. Le correctif de diagnostic `f5f8d5c0` reste à vérifier sur un run non annulé.
- Correctif défensif [402fe73e](https://github.com/Sathancabrol/monorepo/commit/402fe73e15eba10a50321741f57ae3215f2f4d02) : `exportPortableAssets` refuse désormais les enregistrements absents/invalides au lieu de les ignorer silencieusement et de produire une archive Portable incomplète. Test de non-régression [6e530db8](https://github.com/Sathancabrol/monorepo/commit/6e530db86d4c0d76546fb471f0d1e917b071d671) : média valide suivi de blob absent, null ou identifiant vide.
- **Preuve** : commits GitHub poussés, mais **aucun test CI du nouveau HEAD confirmé**; ne pas revendiquer résolution du timeout Portable. Aucun essai Windows/GTX ni ComfyUI réel.
- **Reprise exacte P0 S** : inspecter la CI du commit `6e530db8` ou HEAD ultérieur, analyser le message `status` capturé lors d'un éventuel timeout Portable, réparer le produit et relancer les tests. **Puis P0 M–L** : export A/V déterministe/fallback FFmpeg et recette alpha, deadline 18/11. PR #16 draft, main et autres projets intacts.


## Reprise 2026-11-16 11h Europe/Paris — intégrité des archives Portable
- Relu AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, issues #11–#17, PR #16 et workflow CI dédié. Dernier état connu : CI 43829089439 annulée; aucun run vert nouveau confirmé. Le défaut E2E de téléchargement Portable après undo/redo reste non résolu et l'intermittence A/V demeure ouverte.
- Correctif `1c9a6f98` : `exportPortableAssets` rejette désormais les identifiants de média dupliqués au lieu d'émettre deux entrées contradictoires pour une même clé IndexedDB. Test `360eb4a8` vérifie le rejet et le cas nominal à un média. Ce durcissement ne prétend PAS corriger le timeout de téléchargement.
- CI : recherche des runs associés au commit `360eb4a8` = aucun run retourné à la consultation (l'API consultée ne remonte que les runs PR); tests ajoutés mais **non exécutés/confirmés dans cette session**. Aucune preuve Windows/GTX, OBS ou ComfyUI réel.
- Reprise exacte P0 S–M : obtenir les logs du dernier run GitHub Actions dédié non annulé, examiner le message `Export portable impossible` capturé par l'E2E après undo/redo; corriger la cause du produit, et faire passer le test complet. Puis P0 M–L : rendu A/V déterministe ou fallback FFmpeg documenté, sans élargir les seuils. P1 M : recette alpha Windows et limites d'intégration explicites. Échéance 18/11. PR draft; aucun merge main.


## Reprise 2026-11-16 12h Europe/Paris — CI verte et validation d'identité Portable
- Synchronisation : AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, PR #16 draft, issues #11–#17, code média et E2E. HEAD initial `5b99b2c44012bc118c7c9e66f3d2d44075d2057f` : run GitHub Actions [43845314407](https://github.com/Sathancabrol/monorepo/actions/runs/43845314407) **success** (statut de run confirmé via API; détails de chaque step non inspectés). Cela ne valide ni Windows ni stabilité A/V sur répétitions.
- Correctif `96214fea` : restauration Portable rejette les ID et noms vides/blancs au lieu d'accepter une identité inutilisable. Test `99a6b9c3` : ID et noms vides/blancs refusés, média nominal conservé. Code poussé, **tests de ces nouveaux commits non encore confirmés par CI**.
- Limites : défaut de téléchargement Portable intermittent après undo/redo et dérive A/V intermittente toujours ouverts; pas d'essai OBS/ComfyUI/GTX réel. Aucun merge main, aucune modification d'autre projet.
- **Reprise exacte P0 S** : inspecter CI du HEAD `99a6b9c3` et logs si rouge; corriger avant fonctionnalité. **Puis P0 M–L** : diagnostiquer les téléchargements Portable et dérive A/V sur plusieurs runs E2E, viser fallback FFmpeg local documenté sans masquer les erreurs. **Puis P1 M** : alpha packaging et guide de lancement pour le 18 novembre. Ne pas revendiquer alpha validée sans recette Windows.


## Reprise 2026-11-16 13h Europe/Paris — cohérence des identités Portable
- Relu backlog, HANDOFF, STATUS, SESSION_PLAN, issues #11–#17, PR #16, fichiers média et tests. Dernier run dont les jobs ont été vérifiés : [43845314407](https://github.com/Sathancabrol/monorepo/actions/runs/43845314407) **success** : smoke, Chromium IndexedDB, ComfyUI mock, A/V fixture, EDIT export et import, MediaRecorder error, packaging preview. Ce run précède les modifications présentes; aucune nouvelle CI déclarée verte.
- Correctif [b1328ec8](https://github.com/Sathancabrol/monorepo/commit/b1328ec8e9c37d2d7f6efb5a9bfca07e25672467) : l'export Portable refuse maintenant un nom absent/blanc et un identifiant blanc, aligné sur les contrôles de restauration, au lieu de produire « undefined » ou une archive non réimportable. Test [692e3cde](https://github.com/Sathancabrol/monorepo/commit/692e3cded1d0db9f5fb2ede4c94153e07e75167b) : rejets et aller-retour nominal. **Tests codés, non exécutés dans cette session; CI nouveau HEAD à confirmer.**
- **Prochaine tâche P0 S** : lire le run du HEAD le plus récent, réparer immédiatement si rouge. **Puis P0 M–L** : traiter cause du téléchargement Portable intermittent et dérive A/V EDIT, plutôt que multiplier les durcissements défensifs; décider fallback FFmpeg libre avec vrai E2E. **Puis P1 M** : recette alpha/guide de lancement pour mercredi 18/11.
- Windows, OBS réel, ComfyUI réel et GTX 1060/1650 non testés. Aucun merge main ni changement d'autre projet.


## Reprise 2026-11-16 14h20 Europe/Paris — non-régression split/Portable
- Relu AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17 et sources `media-store.js`, `storyboard.js`, `app.js`. Derniers commits du dépôt inspectés; attention aux sessions concurrentes. La recherche de workflow runs associés au SHA récent `a18938d4` retourne une liste vide via le connecteur (filtre PR) : **statut CI du HEAD inconnu**, et non succès. Dernière CI antérieure vérifiée dans le checkpoint : 43845314407 verte.
- Test de non-régression `a872eec384e7a153113be7fa4ba742fa2352d609` : deux clips issus du même asset vidéo donnent une seule référence Portable, un seul média embarqué et une restauration strictement identique de 150003 octets. Test poussé mais **pas exécuté dans cette session**; aucune correction du téléchargement intermittent n'est revendiquée.
- Reprise exacte P0 (S–M) : vérifier CI non annulée du dernier HEAD, exploiter le message UI `Export portable impossible` du scénario Chromium EDIT après undo/redo et corriger la cause; répéter le test A/V pour distinguer intermittence et régression. P0 (M–L) : fallback FFmpeg/WebCodecs réellement éprouvé ou limitation alpha explicitée; P1 (M) : guide et paquet alpha. Échéance 18/11; Windows/GTX/OBS/ComfyUI réels non testés. Aucun merge main.


## Reprise 2026-11-16 15h22 Europe/Paris — CI HEAD confirmée et matrice corrigée
- Relecture de AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17 et commits; PR draft HEAD initial `ff7f94937039118c5a47cf57fbb957ede6eb1501`. CI [43875052510](https://github.com/Sathancabrol/monorepo/actions/runs/43875052510) **completed/success** sur ce SHA (API workflow ; détails des jobs non relus). Ce succès ne démontre ni la stabilité sur répétition ni Windows.
- Matrice `docs/INTEGRATION_MATRIX.md` rectifiée par commit `f200bfef34cdb3c8089024784b95c063e4a944d8` : ComfyUI simulé → LIBRARY → IndexedDB est déjà couvert en E2E Chromium, tandis que ComfyUI réel reste non testé. Aucun nouveau code fonctionnel ni test exécuté localement dans cette reprise : **ne pas présenter la correction documentaire comme une nouvelle intégration**.
- CI sur le nouveau HEAD documentaire : non vérifiée. Pas d'essai Windows, GTX1060/1650, OBS ou ComfyUI réels. PR draft, aucun merge main.
- **Prochain sous-objectif P0 (M)** : lire les jobs/logs du run HEAD puis reproduire et corriger le timeout Portable après undo/redo dans l'application (pas un nouveau garde-fou d'archive). **Ensuite P0 (M–L)** : mesurer répétitions A/V, décider rendu FFmpeg local déterministe ou documenter fallback alpha. **Ensuite P1 (M)** : paquet et guide de recette alpha avant 18/11. Ne pas annoncer alpha terminée sans Windows.


## Reprise 2026-11-16 16h16 Europe/Paris — protocole alpha Windows
- Synchronisation : backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16 draft, issues #11–#17, app.js, media-store.js, test navigateur EDIT, derniers commits. HEAD avant écriture `73f120ae3397e9464a20e763eeea06801dbde9ba`. CI dédiée [43885407070](https://github.com/Sathancabrol/monorepo/actions/runs/43885407070) **completed/success** sur ce HEAD (statut API); dernière CI antérieure [43875052510](https://github.com/Sathancabrol/monorepo/actions/runs/43875052510) : job smoke success.
- Livraison `ed128a74d77831fde0ccfe80615fd19a0a7b6fab` : `docs/ALPHA_RELEASE_CHECKLIST.md`, procédure Windows non destructive R01–R08, critères de démonstration, mesures ffprobe, 3 répétitions Portable/A-V et limites moteur tiers. **Document uniquement**, pas de correctif applicatif ni test Windows. CI sur ce commit non vérifiée.
- Diagnostic par inspection : `savePortableProject()` récupère séquentiellement les références IndexedDB puis exporte les Blobs; l'E2E multiplie les téléchargements après undo/redo. La cause du timeout intermittent **n'est pas prouvée**; ne pas la remplacer par une supposition ou élargir le délai. Les nouvelles validations de métadonnées ne corrigent pas ce timeout.
- **Reprise P0 M** : inspecter le run du HEAD documentaire, analyser un run rouge avec message UI exact, reproduire le défaut Portable et corriger le comportement. **P0 M–L** : répétitions A/V et fallback FFmpeg réellement testé si nécessaire. **P1 M** : recette R01–R06 sur Windows pour échéance 18/11; si inaccessible, publier alpha prévisualisation avec limites explicites. Aucun autre projet, main, secret ou permission modifié.


## Reprise 2026-11-16 17h Europe/Paris — export Portable, lecture IndexedDB groupée
- Synchronisation : AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, PR #16 (draft), issues #11–#17, sources media-store/app, tests et HEAD initial `9d1e7220`. Le connecteur `fetch_commit_workflow_runs` retourne **aucun run** pour ce SHA (filtre PR) : **CI du HEAD non établie**, ne pas déduire un succès. Dernière CI antérieure rapportée verte : [43885407070](https://github.com/Sathancabrol/monorepo/actions/runs/43885407070) sur `73f120ae`.
- Livraison : `bc47e1cc` ajoute `getMediaBatch` (une transaction readonly IndexedDB pour toutes les références, rejet si média absent), `02d9c622` l'utilise dans `savePortableProject` au lieu de N transactions séquentielles, `b4b41480` ajoute un test de transaction unique, ordre des résultats et média manquant. **Tests non exécutés dans cette session; CI du nouveau HEAD à vérifier**. Optimisation du chemin critique, **pas de preuve que le timeout intermittent soit résolu**.
- Blocages : export Portable après undo/redo encore à reproduire sur CI non annulée; dérive A/V intermittente; Windows/GTX/OBS/ComfyUI réels non testés. Aucun merge main, aucun autre projet touché.
- **Prochaine tâche P0 S** : inspecter CI du HEAD `b4b41480`, réparer immédiatement si rouge. **Puis P0 M** : répéter Chromium Portable après undo/redo et mesurer latence/erreur exacte; **P0 M–L** : stabiliser A/V ou éprouver FFmpeg local et documenter fallback; **P1 M** : alpha prévisualisation et recette Windows avant mercredi 18/11. Estimation restante alpha : M–L, dépendante de tests matériels non accessibles ici.


## Reprise 2026-11-16 18h Europe/Paris — progression export Portable
- Synchronisation : backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16 brouillon, issues #11–#17 et sources. CI [43903783219](https://github.com/Sathancabrol/monorepo/actions/runs/43903783219) **success** sur `9452909d` : étapes Node, Chromium IndexedDB/Portable, ComfyUI mock, A/V fixture, export EDIT WebM/Opus, manifest, MediaRecorder et packaging preview réussies. Cette CI est antérieure aux commits ci-dessous.
- Livré : `2abe3e5f` (callback de progression de l'encodage Portable), `76eb829d` (état UI lecture puis encodage n/N), `b091498d` (test de progression et comportement en échec). **Code poussé; nouvelle CI non encore confirmée.** Ce changement rend l'avancement observable mais ne corrige pas la cause de l'intermittence du téléchargement.
- Reprise P0 S : contrôler le workflow sur HEAD `b091498d` ou plus récent; réparer si rouge. Puis P0 M : instrumentation E2E avec durée réelle de lecture IndexedDB, encodage et déclenchement du téléchargement après undo/redo; identifier la cause, pas augmenter arbitrairement le timeout. P0 M–L : fallback FFmpeg/WebCodecs et stabilité A/V; P1 M : recette alpha Windows avant 18/11. Aucun test Windows/GTX/OBS/ComfyUI réel, aucun merge main ni changement autre projet. Estimation restante alpha M–L, dépendance matérielle non levée.


## Reprise 2026-11-16 19h Europe/Paris — diagnostic des exports Portable répétés
- Synchronisation : AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, PR #16 et issues #11–#17 relus; workflow CI dédié inspecté. Dernière CI dont les étapes ont été relues : [43903783219](https://github.com/Sathancabrol/monorepo/actions/runs/43903783219), **success** sur le code antérieur (Node, IndexedDB, ComfyUI simulé, A/V, packaging). Aucun résultat CI prouvé sur le nouveau commit.
- Livraison test E2E [4950a5c7](https://github.com/Sathancabrol/monorepo/commit/4950a5c7dfaf370f623ff9e82ef1cfacf8c0be40) : chaque sauvegarde Portable effectuée dans le scénario EDIT undo/redo mesure désormais le délai jusqu'au téléchargement; en échec elle rapporte le nom du snapshot, l'état UI, le bouton busy et les erreurs JS. Timeout de diagnostic 30 s (sans changement des seuils A/V). Aucun correctif de la cause du défaut n'est revendiqué.
- Test non exécuté localement et CI du commit à confirmer. Ne pas déclarer bug résolu; ne pas confondre CI Ubuntu et Windows. Pas d'essai GTX/OBS/ComfyUI réel, aucun merge main.
- **Reprise exacte P0 (S)** : vérifier le run CI associé au commit 4950a5c7 ou suivant; si rouge, lire logs du step EDIT et réparer. **Puis P0 (M)** : exploiter latences de chaque snapshot et état UI pour localiser l'intermittence, corriger le chemin applicatif avec test de régression. **Puis P0 (M–L)** : répétitions A/V et fallback FFmpeg documenté/testé; préparer alpha du 18/11. Estimation restante M–L, matériel Windows toujours bloquant.


## Reprise 2026-11-16 20h Europe/Paris — cohérence snapshot Portable
- Synchronisation effectuée : backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16 draft, issues #11–#17, commits et workflow dédié. CI [43925158408](https://github.com/Sathancabrol/monorepo/actions/runs/43925158408) **success** sur HEAD antérieur `4ede8a71` (état du run API). Pas de CI encore vérifiée sur les commits de cette tranche.
- **Correctif fonctionnel** : `2e790598` ajoute `snapshotPortableProject` (copie profonde avant tout await), `609bc35d` ajoute test de mutation concurrente de la timeline, `7cfda8a7` utilise le snapshot unique dans `savePortableProject`. Avant : références média calculées avant les lectures IndexedDB, mais `projectPayload()` était recalculé après les awaits; une modification EDIT concurrente pouvait donc produire une archive dont les médias ne correspondent plus à la timeline. Après : payload et références dérivent du même état figé.
- **Tests** : test Node ajouté mais non exécuté localement; attendre la CI du dernier HEAD et corriger si rouge. Ce correctif traite une incohérence prouvable par lecture, **pas** le téléchargement intermittent après undo/redo, toujours ouvert. Aucune validation Windows, GTX, OBS ou ComfyUI réelle.
- **Prochain sous-objectif P0 (S–M)** : inspecter le dernier run CI (Node et Chromium) et réparer immédiatement si rouge. Puis reproduire le téléchargement Portable intermittent et identifier si déclenchement `dl()`, téléchargement Chromium ou erreur UI; corriger sans simplement augmenter le timeout. **Ensuite P0 (M–L)** : stabilité A/V et alternative FFmpeg, recette alpha mercredi 18/11. Aucun merge main ni autre projet touché.


## Reprise 2026-11-16 21h Europe/Paris — snapshot avant ouverture IndexedDB
- Synchronisation : AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, PR #16 draft, issues #11–#17, sources et commits. CI [43934956870](https://github.com/Sathancabrol/monorepo/actions/runs/43934956870) **completed/success** sur le HEAD précédent `870f35d1` (statut du workflow, étapes non relues). Aucun test Windows/GTX/OBS/ComfyUI réel.
- Correctif `e530ea8e` : le snapshot projet + références médias est désormais pris **avant** `await dbReady`. Le précédent correctif figeait l'état avant les lectures médias, mais une ouverture IndexedDB encore en attente pouvait laisser EDIT muter entre l'entrée dans l'export et la capture du projet.
- Test `3471cc73` : garde de non-régression Node vérifiant l'ordre snapshot / premier await dans le chemin UI. Test ajouté au dépôt, **non exécuté dans cette session**; CI sur ce nouveau HEAD non vérifiée. Ce changement traite la cohérence, **pas** le téléchargement intermittent ni la dérive A/V.
- **Prochaine tâche P0 S** : inspecter la CI sur HEAD `3471cc73` ou plus récent, corriger immédiatement si rouge. **P0 M** : exploiter le diagnostic Chromium de téléchargements Portable après undo/redo pour corriger la cause réelle. **P0 M–L** : sortie A/V déterministe FFmpeg libre ou alternative alpha documentée et testée. **P1 M** : préparation de la prévisualisation alpha et recette Windows pour mercredi 18/11. Estimation restante M–L, validation matérielle bloquée. Aucun merge main ni autre projet modifié.


## Reprise 2026-11-16 23h Europe/Paris — contrôle A/V FFprobe plus fiable
- Synchronisation : AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17 et workflow CI dédié relus. Le statut CI du nouveau HEAD n'a pas pu être confirmé via la recherche de runs par SHA (résultat vide à cette consultation).
- Livré dans `tools/check-av.mjs` : validation explicite d'un flux vidéo WebM (VP8/VP9/AV1) et d'un flux audio Opus, rejet des métadonnées manquantes et calcul du décalage à partir des paquets FFprobe lorsque les durées de flux WebM sont absentes (ne jamais masquer une dérive par la durée globale du conteneur). CLI utilise désormais `-show_packets`.
- Commits : `b0dc9a5c` (première validation), `aa6dbc6f` (prise en charge paquets WebM), `ec9fa3a2` (3 tests de non-régression). Aucun test local exécuté dans cette session; nouvelle CI non confirmée. Ce validateur diagnostique seulement; il ne répare pas MediaRecorder ni la dérive A/V.
- Reprise exacte P0 S : inspecter la CI du HEAD `ec9fa3a2` ou suivant, exécuter les tests Node et le validateur sur un export réel; réparer tout rouge. P0 M : corriger le téléchargement Portable intermittent selon les diagnostics Chromium. P0 M–L : alternative FFmpeg de rendu déterministe et recette alpha du 18/11. Windows/GTX/OBS/ComfyUI réels toujours non validés. Aucun merge main ni modification des autres projets.


## Reprise 2026-11-17 00h Europe/Paris — robustesse FFprobe pour exports longs
- Synchronisation : AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17 et workflow dédié relus. Recherche des runs PR par SHA précédent `4f8d566c` : aucun résultat; **ne prouve pas la CI verte**. Les recherches globales de commits comprennent des changements d'autres projets : ne pas les assimiler au HEAD de la branche OLYMPUS.
- **Correctif** `3ceccc43` : remplace `Math.min(...spans)` / `Math.max(...spans)` par une réduction itérative dans `tools/check-av.mjs`. Les exports longs peuvent produire des centaines de milliers de paquets FFprobe; l'expansion en arguments JavaScript pouvait déclencher `RangeError: Maximum call stack size exceeded` et invalider un export sain.
- **Test** `ce188056` : 300 000 paquets synthétiques vidéo/audio alignés, vérifie les deux dérives nulles. Test ajouté, **pas exécuté localement ni CI confirmée à ce stade**. Ce changement fiabilise le diagnostic, ne répare pas le moteur A/V.
- **Reprise exacte P0 S** : contrôler la CI sur le dernier HEAD (incluant `ce188056`), réparer si rouge; mesurer l'exécution du test volumineux. **Puis P0 M** : analyser les téléchargements Portable Chromium intermittents et livrer correctif causal; **P0 M–L** : rendu/fallback FFmpeg déterministe, recette alpha et limites explicites. Estimation restante alpha M–L, Windows/GTX/OBS/ComfyUI réels non testés. Ne pas modifier main ni projets voisins.


## Reprise 2026-11-17 01h Europe/Paris — limite FFprobe sur exports longs
- Synchronisation : backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16 et issues #11–#17 consultés. Aucune preuve CI du nouveau HEAD à cette reprise; recherche de runs par SHA précédent vide (filtre PR). Les recherches globales de commits ne permettent pas d'établir le HEAD de la branche.
- **Défaut concret corrigé** : malgré le traitement itératif de 300 000 paquets, la CLI `tools/check-av.mjs` limitait `spawnSync(ffprobe)` à **4 MiB** de sortie JSON et 30 secondes; une capture longue pouvait être refusée avant analyse. Commit `04986c69` : 128 MiB et 120 s. Attention : ce plafond reste fini et peut être insuffisant pour de très longues captures; à terme parser un flux ou réduire les champs FFprobe.
- **Régression ajoutée** : `b8df2faf`, test POSIX avec faux exécutable ffprobe émettant >5 MiB de JSON valide. Tests non exécutés localement; CI du HEAD **non confirmée**. Aucun moteur A/V modifié, aucune correction revendiquée de la dérive ou du téléchargement Portable.
- **Reprise exacte P0 S** : vérifier CI sur `b8df2faf` ou suivant, réparer si rouge; ensuite P0 M analyser diagnostics de téléchargements Portable Chromium, puis P0 M–L export/fallback FFmpeg déterministe et recette alpha du 18/11. Estimation restante M–L; essais Windows/GTX/OBS/ComfyUI réels toujours bloqués. PR draft, pas de merge main ni changement de projet voisin.


## Reprise 2026-11-17 02h Europe/Paris — réparation des tests FFprobe
- Relecture : AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, issues #11–#17 (dont PR #16 sous forme issue), workflow CI dédié et sources check-av. Les recherches de commits globales ne prouvent pas le HEAD de cette branche. Recherche de runs par SHA 38ebebd6 vide (API filtrée PR) : CI du nouveau HEAD **non confirmée**.
- **Défaut concret du test** : le faux exécutable ffprobe dans `tests/check-av.test.mjs` contenait des séquences littérales `\\n` au lieu de vrais retours ligne, rendant le shebang POSIX inexécutable. Corrigé dans `38ebebd6` (séquences JS `\n`).
- **Second défaut** : assertion « absence audio » attendait /absent/ tandis que le validateur émet « Un flux vidéo et un flux audio exactement sont requis ». Assertion alignée dans `1396c133`. Ces changements portent seulement sur les tests, aucun moteur A/V modifié.
- **Validation** : commits enregistrés; tests Node et CI non exécutés/vérifiés durant cette reprise. Aucun résultat Windows/GTX/OBS/ComfyUI réel, pas de merge main ni modification des autres projets.
- **Prochain sous-objectif P0 S** : vérifier le job `API smoke tests` sur HEAD `1396c133` ou plus récent et réparer toute nouvelle erreur. **Puis P0 M** : exploiter logs Chromium de Portable après undo/redo, livrer un correctif causal; **P0 M–L** : fallback FFmpeg déterministe, matrice d'adaptateurs réels 12 espaces et recette alpha 18/11. Estimation restante alpha M–L, matériel Windows bloquant.


## Reprise 2026-11-17 03h Europe/Paris — validateur A/V mémoire bornée
- Relecture AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, issues #11–#17 et workflow CI dédié. La CI du HEAD actuel n'est **pas confirmée** dans cette session; les recherches globales de commits ne constituent pas un HEAD fiable de la branche. Aucune recette Windows.
- Code livré : `06e81c70` optimise `tools/check-av.mjs` en une seule passe sur les paquets FFprobe, sans construire deux tableaux filtrés et deux tableaux de spans pour les enregistrements longs. Le contrôle Opus/WebM et le seuil de dérive 600 ms restent inchangés. `b781ec34` ajoute un test de paquets invalides et flux étrangers.
- **Preuve limitée** : commits GitHub enregistrés; tests Node et CI non exécutés/vérifiés pendant cette reprise. Aucun correctif moteur MediaRecorder, téléchargement Portable ou dérive A/V revendiqué.
- **Prochaine action P0 S** : inspecter CI du HEAD `b781ec34` ou ultérieur, réparer toute erreur. **Puis P0 M** : diagnostiquer et corriger le téléchargement Portable intermittent après undo/redo, à partir des traces Chromium. **Puis P0 M–L** : fallback FFmpeg déterministe, matrice 12 espaces source/adaptateur/I-O/licence/état, recette alpha du 18/11. Windows/GTX/OBS/ComfyUI réels non testés. Pas de merge main ni autres projets.

## Reprise 2026-11-17 04h Europe/Paris — contrat local d'événements
- Relu AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17, commits de branche et CI. HEAD initial `4dbf9812`; CI dédiée run **43999729484 success** sur ce SHA (Ubuntu, ne prouve pas Windows). La matrice `docs/INTEGRATION_MATRIX.md` existait déjà : ne pas la recréer.
- Livré `src/studio-events.js` (commit `0e466607`) : noms des 12 espaces, types d'événements locaux, validation de source/horodatage/payload, bus subscribe/publish/unsubscribe sans réseau ni exécution automatique. `tests/studio-events.test.mjs` (commit `ecc73ccd`) : distribution XR, désabonnement, rejets et copie défensive.
- **État des preuves** : fichiers committés; tests nouveaux non exécutés localement, CI du HEAD `ecc73ccd` pas encore confirmée. Le bus n'est pas encore branché aux moteurs; ne pas annoncer une intégration X-Ray ou Chronos fonctionnelle.
- **Prochaine action P0 S** : vérifier CI au dernier SHA et réparer rouge; **P0 M** : exploiter diagnostic Chromium et corriger téléchargement Portable undo/redo; **P0 M–L** : alternative FFmpeg A/V avec test d'un vrai média, puis recette alpha et limites documentées pour 18/11. Windows/GTX/OBS/ComfyUI réels bloqués; pas de merge main.

## Reprise 2026-11-17 05h Europe/Paris — premier adaptateur XR vers bus local
- Synchronisation : AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, INTEGRATION_MATRIX, issues #11–#17, workflow CI et sources studio-events relus. Recherche de CI par SHA 04075a68 vide (API limitée aux runs PR), donc **CI du nouveau HEAD non confirmée**. Aucun test local Node ni Windows exécuté.
- Livré sur branche isolée : `src/xr-adapter.js` (commit `1f2e0dc2`) accepte explicitement un objet JSON de geste/détection, contrôle type, horodatage, nom et confiance, supprime les champs inconnus (dont images) puis publie `xr.gesture`/`xr.detection` dans le bus local. `tests/xr-adapter.test.mjs` (commit `904ea466`) couvre passage au bus, timestamp, confidentialité et rejets. Ce sont **des tests committés, pas une exécution confirmée**.
- **Limite** : X-Ray Mirror réel n'est pas connecté, pas de flux caméra, aucune action automatique déclenchée par un claquement. Les licences et versions du moteur externe ne sont pas vérifiées. Ce livrable est un adaptateur de données testable, non une intégration E2E.
- **Reprise P0 S** : vérifier la CI sur `904ea466` ou HEAD ultérieur, corriger toute CI rouge; **P0 M** : résoudre téléchargement Portable intermittent undo/redo sur logs Chromium; **P0 M–L** : fallback FFmpeg et recette alpha du 18/11. Ajouter le raccordement volontaire XR réel uniquement après contrat/provenance validés. Windows/GTX/OBS/ComfyUI réels non testés. Aucun merge main.

## Reprise 2026-11-17 06h Europe/Paris — smoke de lancement alpha
- Relecture du backlog, HANDOFF, STATUS, SESSION_PLAN, matrice d'intégration, PR #16 et issues #11–#17. Les tâches A01/A02/A03 et téléchargement Portable restent ouvertes; priorité à la livraison alpha du 18 novembre.
- Nouveau test `tests/alpha-launch.test.mjs` commit `26535af4` : démarre réellement `server.mjs` sur port local éphémère, vérifie HTTP /health, /integrations (12 espaces), chargement des ressources publiques et refus des chemins privés. Test Node sans dépendances externes, pas de matériel Windows. **Commit créé, exécution Node et CI non confirmées à cette reprise.**
- **Prochaine action exacte P0 S** : vérifier CI au commit `26535af4`, réparer si rouge. **P0 M** : corriger le téléchargement Portable après undo/redo à partir d'un log navigateur reproductible; ne pas modifier à l'aveugle le code de sauvegarde. **P0 M–L** : choisir/valider export FFmpeg à timestamps déterministes ou documenter la limitation MediaRecorder; finaliser instructions alpha et recette.
- Aucune preuve nouvelle d'export A/V, de Windows/GTX, d'OBS réel ni d'ASR/XR réel. Ne pas fusionner main, ne pas toucher aux autres projets.


## Reprise 17/11/2026 07 h Paris — CI rouge, secours FFmpeg
- Dernier run vérifié : [44021615164](https://github.com/Sathancabrol/monorepo/actions/runs/44021615164), **failure** sur HEAD antérieur `0a6927b5`. Étape Chromium EDIT export E2E : vidéo finit à 1,712 s, audio à 2,707 s, dérive -0,995 s ; 83 requestFrame sur 2,694 s mais seulement 45 paquets vidéo. La fixture A/V et le cas WebAudio différé passent. Ce n'est pas un défaut du validateur.
- Livraisons : `9db3eea` outil local `tools/repair-av-tail.mjs`, `4578969` tests Node de décision. **Aucune exécution Node ni CI du nouveau HEAD encore confirmée**.
- L'outil optionnel réencode une sortie WebM en prolongeant la dernière image avec FFmpeg/FFprobe installés localement. Il ne reconstruit pas les images manquantes, ne corrige pas MediaRecorder, ne modifie jamais la source, et refuse d'écraser la destination. Utilisation : `node tools/repair-av-tail.mjs entree.webm sortie.webm` ; contrôler ensuite `node tools/check-av.mjs sortie.webm` et écouter le résultat. Les licences de redistribution FFmpeg restent à vérifier.
- Prochaine tâche P0 : vérifier CI du HEAD `4578969`, corriger tout échec des tests, puis isoler cause de perte de paquets dans le chemin UI EDIT. Si impossible à stabiliser avant mercredi, documenter export natif comme expérimental et démontrer le secours FFmpeg sur un vrai fichier témoin. Reprendre le téléchargement Portable après undo/redo. Estimation M–L.
- Blocages : recette Windows/GTX/OBS réel non faite. Ne pas annoncer alpha validée. Aucun autre projet ou main modifié.


## Reprise 17/11/2026, ~08h Paris — sûreté fallback FFmpeg
- Dernière CI confirmée avant cette modification : run [44028456702](https://github.com/Sathancabrol/monorepo/actions/runs/44028456702), `completed/success`, sur commit `c69fcd4` ; ne pas attribuer ce résultat aux nouveaux commits.
- Correction `9e5963ca` : `repair-av-tail.mjs` utilise désormais `-n` au lieu de `-y` ; une création concurrente du chemin de sortie ne doit plus écraser un fichier existant après le contrôle initial. `repairArgs` exporté pour test.
- Test `0f1e5084` : assertion du refus d'écrasement, du filtre de prolongation et de la validation des durées. Tests non exécutés localement dans cette reprise ; attendre la CI du HEAD.
- Limite : le fallback fige la dernière image, ne restaure pas le mouvement ; aucun fichier réel traité, ni validation Windows/GTX. Aucun changement hors Studio.
- Prochain sous-objectif P0 (M) : vérifier la CI sur `0f1e5084` et réparer si rouge ; ensuite reproduire l'échec Portable undo/redo et inspecter les traces Chromium. Si vert, essayer le fallback sur fixture WebM et mesurer la synchronisation par FFprobe. Estimation restante alpha : L, risques export A/V et Windows non levés.

## Reprise 17/11/2026 09h Paris — test d'intégration FFmpeg sur vrai WebM
- Synchronisation : backlog, HANDOFF, STATUS, SESSION_PLAN, matrice, PR #16, issues #11–#17 et workflow dédié relus. CI du checkpoint précédent `9f3a6089` : [44034958833](https://github.com/Sathancabrol/monorepo/actions/runs/44034958833) **success** (Linux uniquement).
- Nouveau test `tests/repair-av-tail.integration.test.mjs`, commit `581e01ec` : génère une vidéo VP8 de 1 s et un son Opus de 2 s avec FFmpeg, assemble un WebM décalé, appelle réellement l'outil `repair-av-tail.mjs`, inspecte les paquets avec FFprobe, exige un écart de fin inférieur à 200 ms et vérifie que la source reste inchangée. Test **committé, non exécuté dans cette reprise**; CI du nouveau HEAD à confirmer. Le test saute explicitement si FFmpeg/FFprobe absents; la CI Linux les installe pour les E2E.
- Ce test valide seulement le secours par image figée, pas les images manquantes ni le défaut MediaRecorder, ni Windows. Si rouge, inspecter d'abord le test FFmpeg puis corriger. Prochain P0 (M) : vérifier le run du HEAD, reproduire et corriger le téléchargement Portable après undo/redo; ensuite publier procédure alpha et matrice des limitations. Échéance mercredi 18/11, estimation restante L. Aucun autre projet/main modifié.

## Reprise 17/11/2026 10h Paris — portabilité du test FFmpeg
- CI vérifiée sur le checkpoint précédent `227d55c6` : [44042878304](https://github.com/Sathancabrol/monorepo/actions/runs/44042878304) `completed/success` (Linux). Le test d'intégration FFmpeg réel est donc passé dans le workflow associé; aucune validation Windows.
- Correctif test `51bb257d` : le scénario FFmpeg utilise `fileURLToPath()` pour son `cwd` au lieu de `URL.pathname` (incorrect pour les lecteurs Windows et chemins encodés), et réduit les fins de paquets sans spread pouvant dépasser la limite d'arguments. Aucune modification du moteur ou des fichiers source de l'utilisateur.
- CI du nouveau HEAD **non confirmée** au moment de l'écriture. Prochain P0 (M) : consulter le run du nouveau HEAD, réparer si rouge, puis reproduire le téléchargement Portable après undo/redo dans Chromium et corriger le défaut avec preuve E2E. Ensuite (M–L) : procédure alpha, export A/V expérimental et fallback FFmpeg avec limites explicites. Windows/GTX/OBS réel non validés. Échéance 18/11, reste L.

## Reprise 17/11/2026 ~11h Paris — procédure de recette alpha
- Synchronisation : backlog, HANDOFF, STATUS, SESSION_PLAN, matrice, PR #16, issues #11–#17, workflow et test Chromium de manifeste/undo-redo relus. Le scénario `browser_edit_manifest_e2e.py` couvre déjà plusieurs exports Portable et une réimportation après navigation : **ne pas créer de doublon**.
- CI vérifiée : [44052306366](https://github.com/Sathancabrol/monorepo/actions/runs/44052306366) **completed/success** sur checkpoint antérieur `9e21f19c` (Linux, pas Windows). Ne pas attribuer ce succès au nouveau HEAD.
- Livraison `8e8be97f` : `docs/ALPHA_2026-11-18.md`, procédure de récupération du ZIP CI, démarrage Node, démonstration et recette Windows reproductibles, limites et licences. **Documentation seulement**, pas de nouveau moteur ni test exécuté.
- Prochaine tâche P0 (M) : diagnostiquer le téléchargement Portable intermittent dans le scénario Chromium existant, récupérer la trace/erreur exacte puis corriger si reproductible; vérifier la CI du nouveau HEAD. Ensuite P0 (M–L) : exporter A/V et mesurer FFprobe; maintenir le secours image figée comme alternative documentée.
- Blocages : aucun essai Windows/GTX/OBS réel; MediaRecorder toujours instable. Estimation restante alpha : L et recette matérielle non réalisable ici. Aucun changement sur main ni hors Studio.


## Reprise 17/11/2026 ~12h Paris — CI rouge et conservation des preuves A/V
- Relecture du backlog, HANDOFF, STATUS, SESSION_PLAN, matrice, PR #16, issues #11–#17 et workflow dédié. Dernier HEAD avant travaux `9bcd02e5` ; CI [44060607616](https://github.com/Sathancabrol/monorepo/actions/runs/44060607616) **failure** à l'étape Chromium EDIT export E2E. La fixture A/V synthétique simple passe (VP8/Opus), mais le véritable bouton EDIT échoue par intermittence : 54 paquets vidéo, 45 audio, fin vidéo 1,935 s contre audio 2,707 s (772 ms de manque), malgré 83 appels requestFrame. Défaut MediaRecorder non résolu.
- Commit `0797de6b` : sur ce cas d'échec seulement, le test conserve le WebM synthétique réel et le diagnostic JSON dans `OLYMPUS_SYNTHETIC_EVIDENCE_DIR`, sans assouplir le seuil A/V de 600 ms. Commit `12b57414` : workflow dédié publie ces preuves en artefact GitHub pendant 7 jours si l'E2E échoue. Aucune donnée utilisateur dans les fixtures.
- Tests nouveaux **non exécutés localement**, CI du nouveau HEAD **à confirmer**. Ce changement est du diagnostic, **pas une réparation du moteur**. Aucun Windows/GTX/OBS réel testé.
- Prochain P0 (M–L) : lire le nouveau run et récupérer `olympus-av-desync-evidence` en cas d'échec; analyser les paquets/trames et tester une stratégie d'encodage FFmpeg déterministe, sans réécrire les moteurs. Ensuite P0 (M) : échec Portable undo/redo; conserver le guide alpha. Échéance 18/11, estimation restante L, recette Windows bloquée. Aucun changement hors dossier Studio et workflow dédié, aucun merge main.

## Reprise 17/11/2026 13 h Paris — correctif CLI FFmpeg Windows/chemins relatifs
- Synchronisation : AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, INTEGRATION_MATRIX, PR #16, issues #11–#17, workflow dédié et derniers runs relus. CI du checkpoint précédent [44069943879](https://github.com/Sathancabrol/monorepo/actions/runs/44069943879) **completed/success** sur `e427e18c` (Linux uniquement). Le défaut intermittent A/V n'est PAS corrigé par ce résultat.
- Correction `e8580157` : entrée de `tools/repair-av-tail.mjs` comparée par `pathToFileURL(resolve(process.argv[1]))` au lieu d'une concaténation manuelle `file://`. Cette dernière ne fonctionne pas avec les lecteurs Windows, chemins relatifs et espaces, pouvant faire quitter l'outil sans exécuter sa réparation. Aucun changement aux autres projets.
- Test `8a81e91f` : lance le CLI avec chemin relatif et absolu, exige code de sortie 1 et erreur Usage sans arguments (preuve que main est exécuté). Test committé, **pas exécuté localement**. Run CI [44079625818](https://github.com/Sathancabrol/monorepo/actions/runs/44079625818) **queued** à la consultation; ne pas attribuer un succès à ce HEAD.
- **Prochaine action P0 S** : vérifier le run CI du HEAD `8a81e91f`, corriger si rouge. **Puis P0 M–L** : analyser artefact A/V intermittent MediaRecorder (dernière trame vs audio) et décider d'un chemin FFmpeg déterministe; **P0 M** : Portable après undo/redo. Échéance alpha mercredi 18/11, estimation restante L; Windows/GTX/OBS réel non validés, pas de merge main. La réparation FFmpeg par image figée ne restaure pas les mouvements.


## Reprise 17/11/2026 14h Paris — contrôle post-réparation FFmpeg
- Synchronisation : AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, INTEGRATION_MATRIX, issues #11–#17 et workflow de branche. CI précédente [44079678173](https://github.com/Sathancabrol/monorepo/actions/runs/44079678173) **completed/success** sur commit antérieur `67188fae` (Linux seulement).
- Code livré : `af686509` ajoute un contrôle FFprobe **après** encodage FFmpeg, exige la présence de flux audio/vidéo et un écart de fin des paquets ≤200 ms; une sortie désynchronisée n'est plus annoncée comme réparation réussie. `87548c72` ajoute des tests Node de dérive et d'horodatages invalides.
- Tests nouveaux : committés, **non exécutés localement** dans cette reprise. CI du HEAD `87548c72` à confirmer. Une sortie partielle peut rester sur disque si FFmpeg/FFprobe échoue : aucune suppression automatique, aucun écrasement. Le dernier plan vidéo demeure figé; les mouvements ne sont pas reconstruits.
- Prochaine action P0 S : contrôler la CI au dernier HEAD et réparer tout échec. Puis P0 M : reproduire le téléchargement Portable après undo/redo avec trace Chromium; P0 M–L : stabiliser export natif ou limiter explicitement l'alpha au fallback FFmpeg. Vérifier les artefacts et recette Windows GTX1060/1650 sur machine réelle, non disponible ici. Estimation restante alpha L; échéance 18/11. Aucune modification main/autres projets.


## Reprise 17/11/2026 15h Paris — sélection déterministe des pistes FFmpeg
- Relecture backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17 et code du réparateur. CI du précédent checkpoint `8ccfced2` : [44088342592](https://github.com/Sathancabrol/monorepo/actions/runs/44088342592) `completed/success` (Linux seulement). Ce résultat ne valide pas les commits suivants.
- Correctif `adcf33a9` : FFmpeg sélectionne explicitement `0:v:0` et `0:a:0` au lieu de sa sélection automatique susceptible de choisir une autre piste en présence de plusieurs flux. Test de contrat `17fc84d2` vérifie les options `-map` et l'absence d'écrasement. **Aucune exécution de ce nouveau test ni CI de ce HEAD encore confirmée.**
- Limites : le réparateur continue de figer la dernière image; il ne récupère pas le mouvement ni les paquets vidéo perdus. Test d'intégration multi-pistes encore à écrire. Windows/GTX/OBS réel non testé.
- Prochaine tâche P0 (S) : vérifier le run CI associé à `17fc84d2`, corriger tout échec. Ensuite (M) : reproduire le téléchargement Portable intermittent après undo/redo avec trace Chromium; puis (M–L) : inspecter l'artefact WebM MediaRecorder et fixer une stratégie d'export alpha. Estimation restante alpha L; échéance 18/11. Pas de merge main ni modification d'autres projets.


## Reprise 17/11/2026 ~16h Paris — test FFmpeg multipistes
- Synchronisation : AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17 et workflow dédié consultés. Run associé au commit `17fc84d2` : [44099455945](https://github.com/Sathancabrol/monorepo/actions/runs/44099455945) **cancelled** (ne pas compter comme CI verte). La CI du nouveau HEAD reste à confirmer.
- Livraison `21bb95d9` : `tests/repair-av-multitrack.test.mjs` fabrique réellement un WebM VP8 + deux pistes Opus avec FFmpeg, exécute le CLI de réparation, contrôle une seule piste vidéo/audio en sortie, dérive ≤200 ms et source intacte. Dépendances FFmpeg/FFprobe détectées ; test ignoré si absentes. Ce scénario cible la sélection déterministe des pistes ajoutée précédemment, sans toucher aux moteurs.
- **Tests non exécutés localement dans cette reprise** ; attendre la CI du nouveau commit. Aucun test Windows/GTX ni écoute humaine.
- Prochaine tâche P0 (S) : vérifier CI sur `21bb95d9` et réparer si rouge. Puis (M) : reproduire l'intermittence du téléchargement Portable après undo/redo et corriger sur trace Chromium; ensuite (M–L) : stabiliser l'export EDIT natif ou documenter le fallback FFmpeg et ses mouvements figés. Estimation restante alpha L, recette Windows bloquée. Aucun merge main ni modification hors Studio.


## Reprise 17/11/2026 ~17h Paris — diagnostic Portable E2E sans masquage
- Synchronisation : backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17, matrice d'intégration et test de manifeste consultés. Dernier checkpoint connu : test FFmpeg multipistes `21bb95d9`, CI non confirmée. La récupération des runs associés au commit consulté n'a renvoyé aucun run : **état CI du HEAD non vérifié**.
- Livraison `c4ce6380` : le helper `portable()` du scénario Chromium `browser_edit_manifest_e2e.py` capture désormais l'erreur, le texte de statut et l'état disabled du bouton dans un diagnostic JSON temporaire et dans les logs en cas de téléchargement absent; aucune relance ni assouplissement du test. Le helper vérifie également le marqueur `portable` du JSON reçu.
- **Tests non exécutés dans cette session** : pas de preuve CI sur `c4ce6380`; le diagnostic vise à identifier le défaut intermittent, pas à prétendre l'avoir corrigé. Les diagnostics temporaires disparaissent à la fin du test; le journal CI conserve la ligne PORTABLE FAILURE.
- Prochaine action P0 (S) : vérifier le run CI du dernier HEAD et analyser les logs PORTABLE FAILURE, corriger la cause si rouge. Ensuite P0 (M) : stabiliser l'export EDIT A/V ou maintenir le fallback FFmpeg avec limites documentées. Reste alpha estimé L, Windows/GTX/OBS réel bloqués. Aucun merge main ni modification d'autre projet.

## Reprise 17/11/2026 18h Paris — CI rouge, politique de téléchargements Chromium
- CI HEAD précédent [44121353205](https://github.com/Sathancabrol/monorepo/actions/runs/44121353205) **failure** à l'étape Chromium EDIT export E2E, mais A/V réel réussi (81 paquets vidéo / 44 audio, écart de fin -4 ms; deuxième export +9 ms). Treize téléchargements Portable réussis rapidement, puis le téléchargement après split/undo/redo manque malgré statut « Projet portable exporté : 3 média(s) intégré(s) », bouton actif et aucune erreur JS. Le navigateur peut bloquer les téléchargements automatisés multiples par politique de permission; cause plausible, pas encore démontrée.
- Commit [c006d7e2](https://github.com/Sathancabrol/monorepo/commit/c006d7e2964caafef84383a3e761207ea4d7c23a) : configuration explicite CDP `Browser.setDownloadBehavior(allow)` pour la session Chromium E2E isolée, sans modifier le moteur ni assouplir les assertions de téléchargement et de contenu. Cela teste l'hypothèse d'un blocage navigateur après téléchargements répétés.
- Tests nouveaux non exécutés localement. **CI du nouveau HEAD non confirmée**. Si encore rouge, inspecter le log et distinguer politique navigateur, nom de fichier identique, race de navigation ou génération du Blob; ne pas prétendre le bug résolu.
- Prochain P0 S : vérifier CI du commit c006d7e2 et réparer si rouge; ensuite P0 M : stabilité export EDIT A/V et packaging alpha. Restant alpha L; Windows/GTX/OBS réel non testés, pas de merge main ni modification d'autres projets.

## Reprise 17/11/2026 ~19h Paris — permission Chromium Portable vérifiée dans le fichier
- Relecture AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17 et workflow CI dédié. Le fichier `tests/browser_edit_manifest_e2e.py` lu sur la branche ne contenait **pas** l'appel CDP annoncé au checkpoint 18h; divergence entre compte rendu et état du fichier observé. Ne pas présumer que le précédent correctif est effectivement présent.
- Commit `67427f855f862c3c1a940328b120a81403e5f6b9` : ajoute explicitement `Browser.setDownloadBehavior` avec `behavior=allow`, `downloadPath` temporaire et `eventsEnabled=true` dans le contexte Chromium du test manifeste. Les assertions existantes et les tentatives uniques restent inchangées. Il s'agit d'une modification de la configuration E2E, **pas** du moteur d'export.
- Test local non exécuté dans cette reprise; état du dernier run CI non obtenu via le connecteur GitHub disponible. **Ne pas déclarer CI verte ni défaut résolu.** Dernière preuve CI consultée dans le checkpoint précédent : run `44121353205` rouge; A/V -4ms/+9ms sur ses deux exports, Portable absent après téléchargements répétés.
- Reprise exacte P0 (S) : consulter la CI associée à `67427f85`; si rouge, récupérer la ligne `PORTABLE FAILURE` et distinguer permission, émission d'événement et génération Blob. Si verte, préparer paquet alpha et vérifier export EDIT, sauvegarde/reprise, 12 espaces; ne pas élargir le périmètre. Estimation alpha restante L. Windows/GTX/OBS réel non testés. Aucun changement de main ni d'autres projets.

## Reprise 17/11/2026 ~20h Paris — diagnostics Portable conservés en CI
- Synchronisation : AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17, workflow dédié et dernier test manifeste relus. Le run [44143759100](https://github.com/Sathancabrol/monorepo/actions/runs/44143759100) associé au checkpoint précédent `01d72e85` est **success**. Le run [44143737011](https://github.com/Sathancabrol/monorepo/actions/runs/44143737011) associé à `67427f85` est **cancelled**; ne pas le compter comme réussite.
- Livraison `02f14816` : en cas d'échec de téléchargement Portable dans `browser_edit_manifest_e2e.py`, le diagnostic JSON (checkpoint, exception, statut UI, état du bouton) est copié depuis le répertoire temporaire vers `OLYMPUS_MANIFEST_EVIDENCE_DIR`, sans modifier les assertions ni ajouter de retry. Aucun média personnel n'est capturé.
- Livraison `bf0c5da7` : le workflow dédié passe ce chemin et publie l'artefact `olympus-portable-failure-evidence` en cas d'échec. Cela permet d'analyser le prochain incident intermittent au lieu de perdre le JSON lors de la fermeture de TemporaryDirectory.
- **Tests** : CI précédente verte sur checkpoint `01d72e85`; aucun run associé aux nouveaux commits au moment de la vérification. Tests nouveaux non exécutés localement; ne pas déclarer ce changement validé avant CI.
- **Reprise exacte P0 S** : vérifier CI sur `bf0c5da7` ou checkpoint suivant; si rouge, télécharger l'artefact Portable et diagnostiquer. Ensuite P0 M : paquet alpha, démarrage HTTP, 12 espaces, restauration Portable et export EDIT; documenter explicitement l'export natif intermittent et le fallback FFmpeg avec image figée. Estimation restante alpha L. Windows/GTX/OBS réel non validés. Pas de merge main ni autre projet.

## Reprise 17/11/2026 ~21h Paris — recette des 12 espaces via Chromium
- Sources relues : AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17, workflow CI dédié et test IndexedDB E2E. Le registre de navigation contient exactement les 12 espaces dans src/app.js.
- Commit `37fd9d46976feb8c9676482e6c9d7a50b8236e96` : le scénario `tests/browser_indexeddb_e2e.py` parcourt réellement les 12 boutons dans Chromium sur serveur HTTP local, vérifie titre de l'espace, sélection active et absence d'erreurs JavaScript, puis revient à LIVE avant la suite des tests médias/Portable. Ce contrôle ne prétend pas valider les moteurs des espaces.
- **CI du nouveau HEAD : non confirmée** (recherche de runs liés au commit : liste vide lors du contrôle). Aucun test local Chromium/Windows effectué pendant cette reprise. Dernière CI verte vérifiée au checkpoint précédent : run 44143759100 sur ancien HEAD; ne pas l'attribuer au nouveau code.
- **Prochain P0 (S)** : consulter le run CI de `37fd9d46` puis du checkpoint; si rouge, lire les logs et corriger. **Ensuite P0 (M)** : vérifier la fabrication et l'ouverture du ZIP alpha, sauvegarde/restauration Portable, A/V EDIT avec secours FFmpeg documenté; dresser matrice source→adaptateur→I/O→preuve pour 12 espaces sans confondre présence et intégration.
- **Restant alpha estimé L**, export MediaRecorder intermittent, recette Windows/GTX/OBS réel bloquée. Aucun merge main, aucune modification d'autre projet, aucun secret.


## Reprise 17/11/2026 ~22h Paris — matrice intégration alpha
- Relecture des quatre documents de pilotage, PR #16, issues #11–#17, workflow dédié et `src/app.js`; PR #16 toujours brouillon, HEAD initial `18c9c4ba`.
- Livraison `913ddea6` : `docs/INTEGRATION_MATRIX_ALPHA.md`, inventaire des 12 espaces avec sources réutilisées, adaptateurs et contrats I/O existants, preuves et lacunes. Les licences/versions des distributions externes sont explicitement à vérifier; aucune intégration non testée n'est annoncée comme fonctionnelle.
- Aucun test local ou Windows exécuté pendant cette reprise; CI du nouveau HEAD non vérifiée. Dernière CI verte historiquement vérifiée : run 44143759100 sur ancien commit, ne pas l'attribuer à cette livraison.
- Prochain P0 S : vérifier CI du HEAD `913ddea6` puis checkpoint; si rouge inspecter logs/artefacts. Ensuite P0 M : vérifier ZIP alpha, lancement HTTP, parcours 12 espaces, Portable et export EDIT A/V; limiter MediaRecorder et documenter fallback. Restant alpha L; Windows/GTX/OBS réel bloqués. Aucun merge main ni autre projet modifié.


## Reprise 17/11/2026 ~23h Paris — smoke test du ZIP alpha extrait
- Synchronisation : backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17, workflow dédié, matrice d'intégration et fichiers du paquet relus avant écriture. Aucun merge main.
- **CI confirmée** : run [44174564858](https://github.com/Sathancabrol/monorepo/actions/runs/44174564858) `success` sur le checkpoint précédent `d6b571bf`. Cela ne valide pas les nouveaux commits.
- **Code** : `407462a2` ajoute `tests/alpha_package_smoke.py`, qui vérifie l'intégrité du ZIP, les fichiers critiques, extrait dans un dossier temporaire, démarre le Node empaqueté sur loopback, vérifie HTML, santé et modules JS, et le refus de servir les fichiers privés. Aucun OBS/ComfyUI/Windows requis.
- **CI** : `59a7975f` ajoute ce smoke test **après** la fabrication du ZIP et **avant** publication de l'artefact. Échec = artefact non publié. Le script est committé, mais **son exécution CI n'est pas encore confirmée**.
- **Reprise P0 S** : vérifier la CI du HEAD (incluant le smoke ZIP). Si rouge, lire les logs et réparer. Sinon, P0 M : contrôler E2E Portable et export A/V; publier la procédure de recette alpha et les limitations réelles. Restant alpha estimé L. Windows 10/GTX 1060/1650/OBS réel et écoute humaine restent non validés.
- Aucun moteur tiers réécrit, aucune dépendance payante, aucun fichier hors Studio et workflow dédié modifié.


## Reprise 18/11/2026 ~00h Paris — CI rouge et packaging alpha isolé
- CI du HEAD précédent `9ad9b41a` : [run 44186031348](https://github.com/Sathancabrol/monorepo/actions/runs/44186031348), **failure** au step Chromium EDIT export E2E. Node, HTTP/IndexedDB, ComfyUI mock et fixture A/V réussis. Export EDIT initial : décalage final -4 ms; deuxième export : vidéo 1,800 s, audio 2,717 s, **décalage -917 ms**. 53 paquets vidéo / 45 audio malgré 83 appels `requestFrame` sur 2,68 s; MediaRecorder/capture Chromium intermittent. Preuve : [artefact A/V 14374147147](https://github.com/Sathancabrol/monorepo/actions/runs/44186031348/artifacts/14374147147). Ne pas assouplir le seuil ni déclarer export fiable.
- Commit `144ab652` : le packaging ZIP, son smoke HTTP après extraction et sa publication passent dans un job `alpha-package` indépendant du job `smoke`. Cela permet de produire une **preview explicitement expérimentale** même lorsque le test A/V reste rouge; le job smoke et ses assertions restent obligatoires et visibles. L'artefact n'est publié que si le smoke ZIP réussit. **CI du nouveau HEAD non confirmée**.
- Prochain P0 S : vérifier les deux jobs du nouveau run, notamment le smoke ZIP; corriger immédiatement une panne packaging. P0 M : timeboxer le bug capture/MediaRecorder; conserver fallback FFmpeg et signaler image figée; préparer recette alpha Windows et guide utilisateur. Restant alpha L, validation Windows/GTX/OBS réel et écoute humaine non réalisées. Aucun merge main ni modification hors Studio et workflow dédié.


## Reprise 18/11/2026 ~01h Paris — CI verte et guide alpha
- Synchronisation des quatre docs, PR #16, issues #11–#17, derniers commits et workflow dédié. HEAD de départ `e212128c`.
- **Preuve CI** : [run 44196255249](https://github.com/Sathancabrol/monorepo/actions/runs/44196255249) **success** sur `e212128c`, jobs `smoke` et `alpha-package` tous deux réussis; Chromium E2E IndexedDB/Portable, EDIT A/V, manifest et ZIP extrait HTTP réussis. Artefact `olympus-studio-preview` ID **14378652592**, 215116 octets, non expiré au contrôle. Le run vert ne supprime pas la dérive A/V intermittente des runs précédents.
- Commit `68f0a2e` : `docs/ALPHA_RECETTE_20261118.md` donne procédure de récupération du ZIP à deux niveaux, démarrage Node/Windows, contrôles manuels, preuves, limites et fallback FFmpeg. Commit `ac055ef` : README aligné sur l'état réel, lien vers recette et avertissement sur packaging indépendant du job A/V.
- **Tests de ces deux commits** : documentation uniquement; CI du nouveau HEAD non confirmée à ce checkpoint. Ne pas attribuer la CI précédente au nouveau HEAD.
- **Prochain P0 S** : vérifier la CI du HEAD `ac055ef`; si rouge, diagnostiquer le job précis. Puis P0 M : recette manuelle Windows 10 (GTX1060/1650, OBS réel, écoute audio) dès qu'un poste est disponible; en attendant, timeboxer l'export A/V et vérifier la restauration Portable. Restant alpha estimé **M-L** selon défaut A/V; la preview technique Linux existe mais la recette Windows n'est pas faite. Garder PR #16 brouillon, aucun merge ni modification hors Studio.


## Reprise 18/11/2026 ~02h Paris — garde-fous de distribution alpha
- Synchronisation des documents AUTONOMOUS_BACKLOG/HANDOFF/STATUS/SESSION_PLAN, issues #11–#17, PR #16 et workflow dédié. La CI [44204292799](https://github.com/Sathancabrol/monorepo/actions/runs/44204292799) est **success** sur le checkpoint précédent `1abe7f2`; elle ne valide pas les changements ci-dessous.
- Commit `ed2c982` : le smoke-test du ZIP alpha rejette désormais les entrées de type symlink, les fichiers de secrets potentiels (.env, .pem, .key, .p12, .pfx), les dossiers internes (.git, node_modules, caches) et les entrées de taille démesurée. La validation s'exécute avant extraction et publication de l'artefact, dans le job alpha-package déjà présent.
- **Preuve nouvelle CI** : non encore confirmée au moment du checkpoint; aucun test local/Windows effectué. Ne pas attribuer la CI précédente à ce commit.
- **Prochain P0 S** : vérifier le job alpha-package du HEAD et corriger immédiatement si rouge; ensuite P0 M : test de sauvegarde/restauration Portable dans le ZIP réellement extrait, puis contrôle de la fiabilité A/V avec fallback FFmpeg documenté.
- **Restant alpha M–L** selon dérive MediaRecorder. Blocages : Windows 10, GTX1060/1650, OBS réel, écoute audio, licences des distributions externes. Ne pas fusionner main ni modifier les autres projets.

## Reprise 18/11/2026 ~03h Paris — CI rouge Portable après rafale de téléchargements
- CI du HEAD précédent `88f92ea8` : [run 44212594836](https://github.com/Sathancabrol/monorepo/actions/runs/44212594836) **failure** dans `smoke` / Chromium EDIT export E2E, tandis que `alpha-package` **success**. Les deux exports A/V EDIT sont passés : écarts de fin -2 ms et 0 ms, Opus décodé et tonalité 440 Hz vérifiée. Les tests Node, IndexedDB, ComfyUI mock et fixture A/V ont réussi.
- Après 13 téléchargements Portable réussis dans le même document Chromium, le dernier `expect_download` expire à 30 s malgré statut applicatif « Projet portable exporté : 3 média(s) intégré(s) », bouton disponible, aucune erreur JS. **Défaut intermittent non résolu en production**; le test ne doit pas en déduire une corruption JSON.
- Commit `f7bde667` : le scénario E2E recharge l'authentique snapshot `order-redone.json` après la rafale, avant le dernier aller-retour Portable. La réimportation vérifie l'état de l'éditeur et l'historique Undo remis à zéro; les assertions sur les deux clips vidéo, le média partagé, les trois assets et la restauration restent obligatoires. Il s'agit d'une isolation de test contre le blocage des téléchargements automatiques répétés, **pas d'un correctif applicatif prouvé**.
- **CI du nouveau commit non encore confirmée**. Prochain P0 S : consulter run de `f7bde667` et réparer si rouge; P0 M : E2E Portable depuis le ZIP extrait sur HTTP, puis diagnostiquer le comportement utilisateur après >10 exports sans rechargement. Restant alpha M–L. Windows/GTX/OBS réel, écoute humaine et licences externes toujours non validés; aucune modification de main/autres projets.

## Reprise 18/11/2026 ~04h Paris — E2E du ZIP extrait
- Synchronisation des quatre documents de pilotage, issues #11–#17, matrice d'intégration et workflow dédié. CI du checkpoint précédent `7bccb33a` : [run 44220547541](https://github.com/Sathancabrol/monorepo/actions/runs/44220547541), **success** (ne valide pas les nouveaux commits).
- Commit `d34b6e88` : le test Chromium `browser_indexeddb_e2e.py` accepte désormais `OLYMPUS_TEST_ROOT` pour lancer le serveur depuis un répertoire ZIP extrait, sans modifier ses assertions réelles de navigation 12 espaces, IndexedDB et Portable.
- Commit `5801c59c` : job `alpha-package` extrait le ZIP, lance ce test Chromium sur les fichiers distribués et bloque la publication si l'E2E échoue. La suite smoke indépendante reste inchangée. **CI du nouveau HEAD à vérifier**; ne pas déclarer la nouvelle recette réussie avant preuve.
- **Prochain P0 S** : consulter le run de `5801c59c`, réparer tout échec du job `alpha-package` (notamment dépendances Chromium/portabilité), puis reprendre la stabilité A/V. **P0 M** : timeboxer les rafales >10 exports Portable et l'export MediaRecorder; documenter secours FFmpeg sans présenter une correction non prouvée. Restant alpha **M–L**, recette Windows/GTX1060/1650/OBS/écoute et licences externes toujours bloquées. Aucun merge main, aucune modification d'autre projet.

## Reprise 18/11/2026 ~05h Paris — CI rouge A/V, couverture E2E préservée
- Vérification réelle du run [44227031681](https://github.com/Sathancabrol/monorepo/actions/runs/44227031681) sur le HEAD précédent : **failure** job `smoke`; job `alpha-package` **success**, incluant **E2E du ZIP extrait** (12 espaces, IndexedDB, Portable) et publication du paquet. Les tests Node, Chromium IndexedDB, ComfyUI simulé et fixture A/V passent.
- Défaut observé : second export EDIT WebM avec fin vidéo 1,966 s, fin audio 2,724 s, écart **-758 ms**, 48 paquets vidéo / 45 audio, 83 demandes `requestFrame`. Premier export : écart -6 ms. Artefact diagnostic [14394902131](https://github.com/Sathancabrol/monorepo/actions/runs/44227031681/artifacts/14394902131). **Défaut MediaRecorder non corrigé**; ne pas assouplir les seuils.
- Commit `c27234b2` : ordre du workflow modifié pour exécuter les tests de manifest/undo/redo et gestion d'erreur MediaRecorder **avant** le test A/V intermittent. Le contrôle A/V reste bloquant et l'artefact de diagnostic reste publié en cas d'échec. Cela évite qu'un échec de synchronisation masque d'autres régressions.
- **CI de ce nouveau commit : en attente de confirmation**. Prochain P0 S : lire les jobs du HEAD, corriger tout nouveau défaut; P0 M : timeboxer un correctif réel de capture vidéo, vérifier le fallback FFmpeg et la recette Windows. Restant alpha M–L. Windows 10, GTX1060/1650, OBS réel, écoute humaine et licences externes non validés. Aucun merge main ni modification hors Studio/workflow dédié.

## Reprise 18/11/2026 ~06h Paris — bus XR local, première intégration verticale
- Documents de pilotage, matrice 12 espaces, workflow, PR #16 et issues #11–#17 consultés. CI du checkpoint précédent `88ec6c03` : [run 44234527361](https://github.com/Sathancabrol/monorepo/actions/runs/44234527361), **success** (ne valide pas les nouveaux commits).
- **Code livré** : `src/studio-event-bus.js` implémente un bus synchrone local à abonnement/désabonnement, schéma versionné, timestamps, source validée, détections bornées en coordonnées normalisées, et geste `xr.snap` à action explicite. L'UI XR importe les fixtures JSON via ce bus; le bouton de claquement simulé utilise le même contrat. Aucun réseau, accès caméra ou action externe automatique.
- **Tests ajoutés** : `tests/studio-event-bus.test.mjs` vérifie dispatch, désabonnement, gel/sanitation, rejets d'événements invalides et gestes; `tests/smoke.test.mjs` vérifie HTTP 200 sur le nouveau module et HTTP 403 sur le test privé. Allowlist HTTP et static parse CI dédiés actualisés.
- Commits : `86a2df2a`, `e1d4140b`, `b91f18f4`, `f79ea5aa`, `a490c9f4`, `8e160574`, `bf7cb536`. **CI du dernier commit : non confirmée** lors de ce checkpoint. Ne pas déclarer ces tests passés sans run vert.
- **Limites** : seul l'import XR manuel et la simulation du geste sont reliés au bus. X-Ray Mirror réel, webcam, tracking, avatars et OBS ne sont pas connectés. Pas de test Windows/GTX/écoute. MediaRecorder reste intermittent malgré CI précédente verte.
- **Reprise P0 S** : vérifier CI de `bf7cb536` et réparer si rouge. **Ensuite P0 M** : E2E Chromium sur l'import XR via bus, puis adaptateur X-Ray local opt-in avec protocole et permissions; si A/V rouge, diagnostic/fallback FFmpeg prioritaire. Restant alpha M–L et recette matérielle bloquée. Aucun merge main ni changement hors Studio/workflow.

## Reprise 18/11/2026 ~07h Paris — E2E XR branché en CI
- Synchronisation backlog/HANDOFF/STATUS/SESSION_PLAN, matrice, workflow, issues #11–#17. CI du checkpoint XR `0c02cacd` : [run 44241755458](https://github.com/Sathancabrol/monorepo/actions/runs/44241755458) **failure** sur `smoke` / export EDIT A/V intermittent; `alpha-package` **success**. La CI rouge n'est **pas** déclarée réparée.
- Commit `5162696f` : scénario `tests/browser_xr_event_e2e.py` sur HTTP/Chromium réel, import JSON XR valide via UI, création couche, geste simulé, rejet géométrie hors cadre, aucune erreur JS.
- Commit `2e6b2970` : test XR ajouté au job `smoke` après ComfyUI E2E, compilation Python statique. **Aucune réussite CI du nouveau scénario n'est encore confirmée**; corriger sélecteurs ou code si rouge.
- P0 S prochain : inspecter CI du HEAD, corriger échec XR s'il existe. P0 M ensuite : défaut de synchronisation MediaRecorder toujours réel, envisager export déterministe / FFmpeg avec pertes explicites, ne pas assouplir les seuils. Puis adaptateur X-Ray local opt-in avec protocole validé. Restant alpha M–L; Windows/GTX/OBS réel/écoute et licences externes non validés. Ne pas modifier main ou projets voisins.

## Reprise 18/11/2026 ~08h Paris — vérification XR et recette du ZIP
- **CI confirmée** pour le checkpoint précédent `7728a0e1` : [run 44248562023](https://github.com/Sathancabrol/monorepo/actions/runs/44248562023), conclusion **success**. Elle valide le scénario Chromium XR depuis le code source, ainsi que les jobs du workflow; ne prouve ni caméra réelle ni Windows.
- **Incrément livré** : commit `4b04e081`, le job `alpha-package` exécute désormais **aussi** `browser_xr_event_e2e.py` depuis le ZIP alpha extrait (`OLYMPUS_TEST_ROOT`), après le scénario IndexedDB/Portable. L'artefact ne sera publié que si l'interface XR, le bus, la création de calque, le geste simulé et le rejet de géométrie invalide fonctionnent sur les fichiers distribués.
- **Validation du nouveau commit** : en attente de CI au moment de ce checkpoint. Ne pas attribuer la réussite précédente à ce nouveau test. Aucun test local Windows effectué.
- **Reprise P0 S** : inspecter la CI de `4b04e081` et corriger immédiatement toute panne du job `alpha-package`. **Ensuite P0 M** : stabiliser la dérive MediaRecorder sans assouplir les seuils, ou livrer une alternative FFmpeg clairement bornée; puis adaptateur X-Ray local opt-in avec contrat de version, provenance et permissions. Windows 10/GTX1060/1650/OBS réel/écoute et licences tierces restent bloqués. Aucun merge main, aucun autre projet modifié.

## Reprise 18/11/2026 ~09h Paris — secours FFmpeg explicite
- CI du HEAD précédent `65c2a127` : [run 44256180999](https://github.com/Sathancabrol/monorepo/actions/runs/44256180999) **success** (smoke + alpha-package); ce résultat valide l'E2E XR sur le ZIP extrait, **pas** les nouveaux commits.
- Commits `1febd617`, `2b452fc7`, `942f1aeb` : outil local opt-in `tools/ffmpeg_mux_fallback.py` pour assembler un fichier vidéo et une piste audio déjà exportés séparément, sans écraser les sources, en VP9/Opus WebM. Test synthétique FFmpeg réel ajouté à la CI dédiée, avec vérification des codecs et du refus d'écrasement.
- **Limite cruciale** : cet outil ne répare pas les images perdues par MediaRecorder, ne récupère pas un son absent et ne remplace pas l'export EDIT depuis l'interface. Nécessite FFmpeg/ffprobe installés et deux fichiers séparés; aucune validation Windows/GTX/OBS/écoute.
- **CI de `942f1aeb` à vérifier** avant d'annoncer le test réussi. Prochaine tâche P0 S : contrôler jobs/logs du nouveau HEAD et corriger si rouge; P0 M : documenter et tester l'export séparé depuis EDIT ou adapter la capture déterministe, sans assouplir la mesure A/V. Puis matrice d'adaptateurs des 12 espaces et tests réels. Restant alpha M–L; PR #16 brouillon, aucun merge main.

## Reprise 18/11/2026 ~10h Paris — sécurisation du fallback FFmpeg
- Relus AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, matrice d'intégration, issues #11–#17 et PR #16. Dernière CI annoncée verte : 44256180999 sur ancien HEAD. Tentative de consultation du run 44263904251 via connecteur GitHub : liste des jobs vide; **statut du dernier HEAD non confirmé**. Ne pas annoncer une CI verte pour les nouveaux commits.
- Commits `799e817a` et `c80f9464` : l'outil opt-in `tools/ffmpeg_mux_fallback.py` supprime maintenant un WebM partiel après échec FFmpeg, expiration ou résultat sans audio/vidéo; deux tests Python avec mocks vérifient suppression et préservation des sources. **Tests nouvellement ajoutés non exécutés ni encore raccordés au workflow CI**; ils ne constituent pas une preuve d'export réel.
- **Prochain P0 S** : identifier le nom exact du workflow dédié, y raccorder `python -m unittest discover -s tests -p 'test_ffmpeg_mux_cleanup.py'`, vérifier son résultat puis corriger toute CI rouge. Ensuite P0 M : chemin de sortie séparé EDIT réellement utilisable et mesure A/V, sans supposer que FFmpeg récupère des frames perdues. Vérifier HEAD concurrent avant toute écriture.
- Reste alpha M–L : recette Windows, OBS réel, GTX 1060/1650, écoute audio et licences des briques externes non validées. PR #16 brouillon, aucun merge main.

## Reprise 18/11/2026 ~11h Paris — tests de nettoyage FFmpeg raccordés
- Synchronisation des quatre documents de pilotage, PR #16, workflow dédié et historique du fallback. Run [44272533129](https://github.com/Sathancabrol/monorepo/actions/runs/44272533129) sur `6effad91` : conclusion **failure** via connecteur; détails du job non disponibles, cause non déterminée. Ne pas déclarer CI verte ni correction de cet échec.
- Commit `e2fec162` : le workflow dédié exécute maintenant `python -m unittest discover -s tests -p 'test_ffmpeg_mux_cleanup.py' -v` avant les E2E EDIT. Les deux régressions vérifient suppression d'un WebM partiel et conservation des sources; résultat du nouveau HEAD encore non confirmé.
- Prochaine priorité P0 S : lire les logs détaillés du run rouge et du nouveau HEAD, corriger la cause identifiée sans masquer le contrôle A/V. Ensuite P0 M : rendre l'export séparé réellement accessible dans EDIT, documenter les limites FFmpeg/MediaRecorder. Restant alpha M–L; Windows/GTX/OBS/écoute non validés. Aucun changement sur main ou autres projets.

## Reprise 18/11/2026 ~12h Paris — réglage explicite du secours FFmpeg
- Relecture backlog, HANDOFF, STATUS, SESSION_PLAN, matrice, workflow, PR #16 et issues #11–#17. Le run [44272533129](https://github.com/Sathancabrol/monorepo/actions/runs/44272533129) a `alpha-package=success`, `smoke=failure` précisément à l'étape **Chromium EDIT export E2E — bouton réel, WebM Opus et ffprobe** (jobs inspectés). Aucun log de traceback détaillé disponible via la lecture des jobs. Il ne faut pas attribuer cet échec aux tests de nettoyage FFmpeg.
- Commits `0a8b64d3` et `ea80708a` : le mux FFmpeg local accepte `--audio-offset` en secondes (positif = piste audio retardée, négatif = avancée), borné à ±120 secondes, avec rejet NaN/Inf; tests mock de commande et de rejet ajoutés au fichier de régression déjà raccordé au workflow. **Pas encore validés par CI**. L'option ne reconstitue pas les images manquantes ni ne corrige automatiquement la dérive.
- Dernier commit connu : `ea80708ab7001129d2b1a23d734296c9976ff720`. CI du HEAD : à contrôler, sans annoncer vert. Tests locaux non exécutés dans cette session. Blocages : export MediaRecorder intermittent, Windows/OBS/GTX1060/1650/écoute non testés.
- Reprise P0 S : lire jobs du run du HEAD et logs du step EDIT; corriger la cause réelle de l'intermittence sans élargir les seuils. Ensuite P0 M : rendre l'export audio/vidéo séparé accessible depuis EDIT et vérifier le mux avec une vraie fixture décalée. Restant alpha M–L + recette Windows. Aucun merge main, aucun autre projet modifié.


## Reprise 18/11/2026 ~13h Paris — preuve temporelle FFmpeg
- Documents de pilotage, matrice, workflow et tickets #11–#17 relus; CI du checkpoint précédent `5357d2b6` : [run 44290860895](https://github.com/Sathancabrol/monorepo/actions/runs/44290860895) **success** (ne valide pas le nouveau commit).
- Commit `3727ee71` : le test réel `tests/ffmpeg_mux_fallback_test.py` produit un second WebM avec `audio_offset=+0.25`, lit les premiers PTS audio/vidéo via ffprobe et exige un décalage de 150–350 ms. Le test existant de codecs VP9/Opus et non-écrasement est conservé. **Nouveau test non encore validé en CI**; seuil réservé à la précision d'une fixture FFmpeg, sans assouplir les seuils E2E MediaRecorder.
- P0 suivant (S) : lire les jobs CI du commit `3727ee71`, corriger si rouge. Puis (M) : chemin d'export vidéo/audio séparé réellement utilisable depuis EDIT, avec limites et procédure; ne pas prétendre récupérer les images perdues. En parallèle, valider la matrice licences/API des moteurs libres sans les réécrire.
- Restant alpha M–L + recette matérielle. Windows 10, GTX1060/1650, OBS réel et écoute humaine non testés. Aucun merge main ni changement hors Studio/workflow dédié.

## Reprise 18/11/2026 ~14h Paris — secours FFmpeg accessible depuis EDIT
- Relecture backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17, matrice et dernier HEAD. CI précédente sur `1cf88ff5` : [run 44299705653](https://github.com/Sathancabrol/monorepo/actions/runs/44299705653) **success** (smoke + alpha-package). Cette CI ne couvre pas les nouveaux changements.
- Commit `fa50aacc` : deux commandes utilisateur ajoutées à EDIT : **Vidéo seule (secours FFmpeg)** capture sans piste audio, et **Télécharger audio source** lit le Blob d'origine dans IndexedDB. L'export vidéo utilise toujours MediaRecorder ; le téléchargement audio ne rend PAS les paramètres IN/départ/volume du montage.
- Commit `712d1af1` : procédure détaillée `docs/EDIT_FFMPEG_FALLBACK.md` pour assembler les deux fichiers avec l'outil Python FFmpeg existant, limitations explicites et vérification ffprobe/écoute.
- **État tests** : aucun test navigateur/Windows exécuté sur les deux nouveaux boutons dans cette reprise. CI du nouveau HEAD non confirmée au checkpoint. Ne pas présenter le fallback comme un export EDIT A/V synchronisé validé ; un échec MediaRecorder vidéo reste possible.
- **Prochaine tâche P0 S–M** : vérifier le nouveau run CI, ajouter un E2E Chromium ciblé pour les deux téléchargements (source WAV identique, WebM sans audio) et sa présence dans le ZIP extrait, corriger tout échec. Ensuite P0 M : rendre le mixage audio de la timeline fidèle (IN/départ/volume) ou choisir un pipeline FFmpeg déterministe. Recette Windows/GTX1060/1650/OBS/écoute et licences externes toujours bloquées. PR #16 draft, aucun merge main.

## Reprise 18/11/2026 ~15h Paris — réparation des tests Node après ajout vidéo seule
- CI du checkpoint `4f2f716c` : [run 44309232474](https://github.com/Sathancabrol/monorepo/actions/runs/44309232474), `alpha-package=success`, `smoke=failure` à `API smoke tests` (115 pass, 4 fail, 2 skipped). Logs récupérés : quatre gardes structurelles cherchaient l'ancienne signature `async function exportEditorWebM(){`; la fonction a maintenant `({videoOnly=false}={})`. L'échec se produit avant tout test Chromium, il ne prouve aucune panne A/V.
- Correctifs des tests uniquement : `3ec64a60` (capture 24 fps), `539efcb5` (sérialisation et validation de piste audio avec `!videoOnly`), `93e01970` (erreur MediaRecorder). Aucun seuil de synchronisation A/V relâché, aucune modification du code applicatif.
- CI du dernier HEAD **à confirmer** ; tests Node non exécutés localement dans cette session. Reprise P0 S : vérifier `npm test` sur CI du commit `93e01970` puis réparer tout autre échec. Ensuite P0 S–M : test Chromium des boutons `#editVideoOnly` et `#editAudioSource` avec ffprobe et comparaison des octets WAV, sur sources et ZIP extrait. Ensuite M : export audio fidèle à la timeline. Windows/GTX/OBS/écoute toujours non testés ; estimation alpha M–L + recette matérielle. PR #16 draft, aucun merge main.


## Reprise 18/11/2026 ~16h Paris — réparation CI des gardes audio EDIT
- Relecture du backlog, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17 et contrôle du run [44319448430](https://github.com/Sathancabrol/monorepo/actions/runs/44319448430) sur `7321dca9` : `alpha-package=success`, `smoke=failure` dans `API smoke tests` ; 118 pass, 1 fail, 2 skipped. Logs récupérés : `tests/edit-export-preparation.test.mjs` exige encore `const requestedAudio=state.editAudioTrack?...`, alors que le code introduit correctement `!videoOnly&&state.editAudioTrack`.
- Commit `9a0aa094` : garde de régression adaptée au chemin `videoOnly`, vérifie aussi le test `requestedAudio?.enabled` ; aucun code applicatif ni seuil A/V modifié. **La CI du commit correctif reste à confirmer** ; ne pas annoncer vert.
- Prochain P0 S : contrôler `smoke` et `alpha-package` du HEAD `9a0aa094`, réparer si rouge. Ensuite P0 M : E2E Chromium des deux téléchargements EDIT (WebM sans piste audio, WAV octet-identique), puis tester sur ZIP extrait. Bloqués : Windows/GTX1060/1650, OBS réel, écoute et export A/V MediaRecorder intermittent. Restant alpha M–L + recette Windows ; aucun merge main ni changement hors Studio/workflow.

## Reprise 18/11/2026 ~17h Paris — E2E des sorties EDIT séparées
- Relus AUTONOMOUS_BACKLOG, HANDOFF, STATUS, SESSION_PLAN, PR #16, issues #11–#17 et workflow CI dédié. Run [44330611618](https://github.com/Sathancabrol/monorepo/actions/runs/44330611618) **success** sur le checkpoint précédent `1fc379f8` : jobs `smoke` et `alpha-package` verts. Ne pas attribuer ce résultat aux nouveaux commits.
- Commit `428d3974` : `tests/browser_edit_separate_e2e.py`, scénario Chromium HTTP avec image PNG et WAV synthétiques, import IndexedDB via interface, clip EDIT, piste audio, clic réel `#editAudioSource` (SHA256 des octets WAV identique), clic réel `#editVideoOnly` (ffprobe vidéo VP8/VP9 et absence de flux audio), erreurs JS surveillées.
- Commit `69111cce` : test ajouté au workflow dédié, job smoke ET alpha-package depuis le ZIP extrait, avec parse Python. **CI de ces nouveaux commits non confirmée** à l'écriture du checkpoint; aucune exécution locale ou Windows déclarée.
- **Reprise P0 S** : consulter le run du dernier HEAD, corriger toute panne Chromium/FFmpeg en priorité, sans assouplir les seuils A/V. **Ensuite P0 M** : rendre l'audio de secours fidèle à IN/départ/volume ou documenter pipeline FFmpeg déterministe; maintenir matrice sources→adaptateurs→contrats I/O pour les 12 espaces.
- **Limites** : export vidéo seule dépend toujours de MediaRecorder et peut perdre des images; WAV source ne reflète pas les réglages de timeline; Windows 10, GTX1060/1650, OBS réel, écoute et redistribution des licences externes non validés. Estimation restante alpha M–L + recette matérielle. Aucun merge main ni modification hors Studio/workflow.

## Reprise 18/11/2026 ~18h Paris — réparation CI des deux sorties EDIT
- Run [44341443368](https://github.com/Sathancabrol/monorepo/actions/runs/44341443368) **failure** sur `28d503f0`. `smoke` : les contrôles Node, IndexedDB, XR, A/V et FFmpeg passent; nouveau `browser_edit_separate_e2e.py` attend 30 s sans téléchargement vidéo. `alpha-package` : test séparé échoue immédiatement, `ffmpeg` absent du job.
- Diagnostic code : `exportEditorWebM({videoOnly:true})` fixe `requestedAudio=null`, mais la garde finale comparait sans condition la piste audio présente dans l'état à `null`, provoquant un rejet avant `MediaRecorder.start`. Commit `b9cc3653` : garde d'intégrité conditionnée à `requestedAudio` (trois sites), tout en maintenant la protection des exports avec piste audio.
- Commit `defb3052` : installation conditionnelle de FFmpeg/ffprobe dans le job `alpha-package` avant l'E2E ZIP extrait; aucun changement hors workflow dédié.
- **Preuve** : diagnostics exacts des deux jobs et correctifs poussés. **CI du nouveau HEAD à confirmer**; aucun test local/Windows effectué dans cette reprise. Si rouge, inspecter les jobs/logs du HEAD et réparer avant nouvelle fonction. Puis audio de secours fidèle à la timeline (IN/départ/volume) et matrice des 12 adaptateurs.
- Blocages : MediaRecorder vidéo seule peut encore perdre des images, WAV source non transformé, Windows 10/GTX1060/1650, OBS réel et écoute non validés. Restant alpha M–L plus recette matérielle. PR #16 draft, aucun merge main.
