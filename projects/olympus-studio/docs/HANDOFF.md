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
