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
