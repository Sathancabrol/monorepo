# Journal des preuves — initialisation 2026-11-12

| Élément | Preuve | État |
|---|---|---|
| Dépôt choisi | `Sathancabrol/monorepo`, branche isolée `feat/olympus-studio-20261112` | Création confirmée |
| Prototype OLYMPUS Studio v0.3 local | Tests `smoke_test.py` : all tests passed; documentation des fonctions et limites | Artefact local distinct de ce dossier |
| Connexions OBS / ComfyUI | Diagnostic de ports et POST local ComfyUI codés; MJPEG `/obs` + POST `/api/frame` codés | Vérification syntaxique seulement; test direct OBS/ComfyUI à faire |
| Capture caméra / micro | Dépend des autorisations navigateur | Non validé sur machines utilisateur |
| X-Ray Mirror | Conversations : moteur de détections et gestes; version du dépôt local non inspectée dans cette session | Adaptateur à écrire |
| Watchtower | `src/main.js`, `src/batiRapide.js`, `src/osmBuildings3D.js` inspectés sur GitHub | Code présent, exécution 3D non vérifiée |
| Montage FreeCut / Velorn | Docs publiques consultées le 12/11/2026 | Candidats, NON intégrés |
| Workflow GitHub Actions ciblé | `.github/workflows/olympus-studio-ci.yml` ajouté sur branche | Exécution / résultat non confirmé |\n| Distribution Windows, perf GTX | Aucun résultat | À faire |

## Règle de signalement
**Proposé** ≠ **codé** ≠ **test isolé** ≠ **test navigateur** ≠ **test sur Windows de l'utilisateur** ≠ **déployé**. Garder ces colonnes séparées.

## Blocages
- Pas d'accès à la tour pendant cette conversation.
- La limite de 5/5 automatisations ChatGPT empêche l'ajout d'un suivi nocturne sans libérer une place. Aucune tâche existante n'a été remplacée.
- La première génération GitHub n'inclut pas tous les fichiers du prototype local v0.3.

## Itération v0.2 — 12 novembre 2026 (soir)

| Élément | Preuve reproductible | Résultat |
|---|---|---|
| Client OBS v5 | `src/obs-client.js`, `src/obs-panel.js`, `tests/obs-client.test.mjs` | Implémenté ; authentification/changement de scène/REC testés contre serveur WebSocket simulé |
| Capture écran et micro | `src/app.js`, boutons `btnScreen` et `btnMicrophone` | Implémentée ; autorisation utilisateur requise ; non testée sur PC |
| WebM avec piste audio | Assemblage MediaRecorder, clone de piste ou mélange Web Audio | Codé ; codecs/capture réelle à valider |
| Protection fichiers et origines HTTP | `server.mjs`, `tests/smoke.test.mjs` | Corrigée ; requêtes interdites en tests automatiques |
| GitHub Actions | https://github.com/Sathancabrol/monorepo/actions/runs/43288150897 | 13/13 tests réussis, Ubuntu / Node.js 22 |

**Ne pas confondre** la simulation protocolaire OBS avec une véritable connexion OBS/Windows, ni l'export WebM codé avec un test audiovisuel de bout en bout.

### Complément — suivi de génération ComfyUI

- API `GET /api/comfy/job?prompt_id=<UUID>` : interroge l'historique **du ComfyUI local** et normalise le statut / les métadonnées des sorties. L'interface GENERATE contient « Vérifier le dernier job ».
- Protection des identifiants UUID ; test HTTP d'identifiant invalide ajouté. **Aucun ComfyUI réel ou modèle IA testé** ; les fichiers produits sont listés, pas encore importés dans la médiathèque.

## Itération v0.2.1 — coffre média, réunions et migration v0.3

| Élément | Preuve code / test | Validation |
|---|---|---|
| Stockage images/vidéos | `src/media-store.js` IndexedDB (assets, version 3), `src/app.js` reliaison des références | Unitaire Node sur encodage/décodage/référence; navigateur Windows non testé |
| Projet portable | Bouton « Portable », export JSON avec médias ≤45 Mo et import réhydrateur | Tests binaires au-delà de 64 Ko réussis; grand projet non testé |
| Réunions privées | `src/meeting-utils.js`, import/export SRT, compte rendu MD; sous-titres privés par défaut | Tests SRT réussis; pas de transcription IA |
| Import legacy v0.3 | `src/v03-migration.js`, géométrie pixel 1280×720 → normalisée, `legacyV03` préserve notes/automation/timeline | Tests synthétiques réussis, portage du montage **non fait** |
| Session automatique ChatGPT | Création tentée le 12/11/2026 | **Refusée : 5 automations actives sur 5** ; aucune tâche existante arrêtée |
| Test E2E Chromium | Tentatives sur `127.0.0.1` et route Playwright virtuelle | **Bloqué par net::ERR_BLOCKED_BY_ADMINISTRATOR** ; ne pas compter comme réussi |

**Règle :** `legacyV03` préserve les données du prototype précédent pour migration ultérieure, mais ne rend pas les fonctions storyboard/XR/automate opérationnelles. L'import de fichiers v0.3 réels doit encore être éprouvé sur navigateur et des fixtures complètes.

L'application n'est **pas terminée**. Le socle unifié existe, mais un véritable éditeur audiovisuel complet, ASR/translation, VFX génératif, X-Ray et Watchtower actifs restent à réaliser.

## Itération v0.2.2 — storyboard EDIT

| Élément | Preuve | État |
|---|---|---|
| Modèle non destructif de clips | `src/storyboard.js` + `tests/storyboard.test.mjs` | Durées, ordre, mapping temporel et références média testés Node |
| Espace EDIT | `src/app.js` | UI codée : choix de médias, ordre, durée, titres, aperçu Canvas et lecture; test navigateur réel restant |
| Export EDIT | `exportEditorWebM`, `MediaRecorder` sur Canvas dédié | Code présent, **vidéo sans audio**; export limité à 120 sec, non testé en conditions réelles |
| Sauvegarde des clips | `projectPayload().clips`, `loadProject`, `referencedAssetIds` | Série de clips conservée dans JSON, médias EDIT inclus dans portable |
| Multimédia avancé | Transitions, pistes audio, coupure de clips par points IN/OUT dans UI, MP4 | **Non implémenté** ; pas équivalent à FreeCut/Kdenlive |

La piste éditoriale suivante consiste à valider la lecture vidéo et les exports sur Chromium Windows, intégrer la sélection et synchronisation audio, puis seulement évaluer une intégration plus profonde de FreeCut ou d'un moteur de montage natif.

## Exécution immédiate — EDIT v0.2.3, 12 novembre 2026
| Fonction | Code / preuve | État |
|---|---|---|
| Vidéo IN/OUT | `src/storyboard.js`: `trimVideoClip`; champs dans EDIT | **Codé**, tests mathématiques réussis |
| Division au curseur | `splitStoryboardAt`, nouvelle commande dans EDIT | **Codé**, timeline globale et conservation assetId testées |
| Conserver les médias | Aucune réécriture des Blob IndexedDB; clips partagent assetId | **Modèle testé**, navigateur non vérifié |
| Tests de régression | https://github.com/Sathancabrol/monorepo/actions/runs/43316401111 | **29/29 sur Node/Ubuntu** |
| Planification quotidienne | Tâche `6af632ef3df88191a7ef46e372054ac4` créée et exécution immédiate déclenchée | **Active**, 02:00 Europe/Paris |

Limitations : aucun mixage audio EDIT, aucune coupe bornée par métadonnées de durée réelle du fichier, aucun test sur la tour Windows. La modification est sur branche seulement, PR #16 brouillon.

## Itération v0.2.4 — 13 novembre 2026, source vidéo réelle

| Fonction | Preuve | Niveau |
|---|---|---|
| Durée source | `src/video-duration.js`, `loadedmetadata`, `durationchange` et cache par assetId | Codé; tests Node et vidéo Chromium |
| Création de clip | Vidéo WebM témoin 2,00 s → durée initiale 2,00 s | **Vérifié dans Chromium headless**, source en mémoire |
| IN/OUT bornés | OUT=5 s rejeté pour source 2 s, message explicite | **Vérifié dans Chromium headless**, pas encore Windows |
| Division vidéo | Split au curseur sur le même média après import réel | **Vérifié dans Chromium headless** |
| Cas erreurs | Source inconnue, timeout, vidéo endommagée | 5 tests Node nouveaux |
| Browser smoke reproductible | `tests/browser_media_smoke.py`, Python Playwright + FFmpeg + Chromium, sans réseau | Ajouté; exécution manuelle locale sur environnement de test |
| Persistance IndexedDB, export audiovisuel, GPU | Navigateur de test utilise modules en mémoire, IndexedDB bloqué | **Non vérifié** |

Les métadonnées peuvent être inconnues ou invalides (ex. flux live, conteneurs incomplets). Dans ce cas les coupes ne sont pas présentées comme vérifiées. L'essai Chromium ne certifie pas les performances sur la tour Windows.

## Session nocturne — 13 novembre 2026, validation du champ Durée

| Fonction | État | Preuve |
|---|---|---|
| Contrôle du champ « Durée » vidéo selon la durée source | Codé | `src/app.js`, `src/video-duration.js:setClipDuration` |
| Préservation du média source et rejet de la durée hors fichier | Test unitaire ajouté | `tests/video-duration.test.mjs` ; test UI Windows non réalisé |
| Blocage des modifications pendant export | Codé, non testé navigateur | `src/app.js` |
| E2E IndexedDB / export audio / Windows GPU | Non vérifié | Aucun accès matériel autorisé |

Le champ Durée constituait un contournement des bornes IN/OUT de v0.2.4 ; ce chemin est désormais unifié. Revalider la CI du dernier commit avant toute publication de package.

## v0.2.5 — 13 novembre 2026 — audio EDIT et suivi autonome

| Fonction | État réel | Preuve |
|---|---|---|
| Import `audio/*` séparé de LIVE | Codé, test navigateur à confirmer | `index.html`, `src/app.js:addFiles` |
| Une piste audio EDIT : départ / IN / volume / active | Codé, logique testée Node | `src/edit-audio.js`, `tests/edit-audio.test.mjs` |
| Projet/portable incluent la piste audio | Code et test de références médias | `src/app.js:projectPayload`, `src/storyboard.js:referencedAssetIds` |
| Export Canvas + MediaStreamDestination A/V | Codé, **pas encore validé sur sortie WebM réelle** | `src/app.js:attachAudioToEditorCapture` |
| Import WAV Chromium | Scénario test ajouté, **exécution non confirmée** | `tests/browser_media_smoke.py` |
| Reprise autonome quotidienne | Automatisation mise à jour avec backlog séquentiel | Tâche `6af632ef3df88191a7ef46e372054ac4`, `docs/AUTONOMOUS_BACKLOG.md` |

Ne déclarer la piste A/V fonctionnelle en conditions réelles qu'après capture/lecture du fichier exporté et vérification du codec/décalage. Une CI verte ne suffit pas.

## Itération A02 — 13 novembre 2026, 04h

- **Codé** : `tests/browser_indexeddb_e2e.py`, test Playwright Chromium sur **véritable origine HTTP** et serveur Node local. Il écrit un Blob vidéo synthétique dans IndexedDB, ferme la connexion, recharge la page, vérifie les octets, découpe réellement un clip en deux via `splitVideoClip`, confirme une seule référence `assetId`, et effectue un aller-retour Portable base64. Le test supprime son média temporaire à la fin.
- **CI configurée** : `.github/workflows/olympus-studio-ci.yml` installe Playwright/Chromium et exécute le scénario en plus de `npm test` ; ceci n'est pas une preuve d'exécution tant que le nouveau run n'est pas vert.
- **Preuve de code** : commits `d79772d7`, `b6a7788e`, `d688b9a7`. Le run précédent 43349763003 était vert, **avant ces modifications**.
- **Limites** : pas de test d'export WebM sonore, pas de vraie vidéo décodable dans la fixture Blob, pas de Windows/GTX. A02 n'est pas DONE avant une CI verte et le test d'interface sauvegarde/reprise complet.

## A02 — correction CI et seconde persistance Portable (13 novembre, 05h)

| Composant | État | Preuve |
|---|---|---|
| Syntaxe du step Chromium CI | **Corrigée dans le code**, pas encore validée par run | `a83a31a9`, retours à la ligne YAML réels |
| Import Portable → écriture IndexedDB → second reload | **Scénario ajouté**, exécution à confirmer | `eabbd614`, `tests/browser_indexeddb_e2e.py` |
| CI du nouveau scénario | **Inconnue**, ne pas déclarer verte | Aucun check renvoyé pour les nouveaux SHA lors de la consultation |
| Export WebM sonore et test Windows | **Non vérifiés** | Nécessitent essais A/V et Windows distincts |

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


### Point 13/11/2026 — sécurité de l'export A/V EDIT

- **Codé** : `src/editor-export.js` impose un `MediaRecorder` compatible WebM/Opus pour tout export EDIT avec piste audio. L'ancien repli générique `video/webm` pouvait produire une vidéo muette présentée comme audiovisuelle; désormais une erreur explicite empêche cet export trompeur. Le mode vidéo seule garde ses formats de repli.
- **Tests écrits, CI à confirmer** : `tests/editor-export.test.mjs` vérifie la sélection VP8/Opus, VP9/Opus et le refus d'un encodeur audio absent. Workflow dédié et allowlist HTTP mis à jour.
- **Non validé** : lecture audible, synchronisation A/V, export réel et recette Windows. A01/A03 non clos; dernière CI du commit `63a420e0` non confirmée au checkpoint.

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
