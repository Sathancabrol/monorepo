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
