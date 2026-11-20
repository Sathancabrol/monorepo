# OLYMPUS Studio — matrice d'intégration (16 novembre 2026)

Échéance alpha : **18 novembre 2026**. Inventaire **du code du dépôt**, pas un audit d'installation Windows. Source machine-readable : `src/integration-registry.js`, diagnostic HTTP `GET /api/integrations`. Une sonde de port ne prouve ni authentification, ni fonctionnalité, ni compatibilité GPU.

| Espace | Brique cible existante | Adaptateur/contrat d'échange | Preuve actuelle | À intégrer/valider |
|---|---|---|---|---|
| LIVE | OBS Studio | `obs-client.js` WebSocket v5; scène/REC/événements | mock Node | OBS réel Windows |
| EDIT | Storyboard Studio, MediaRecorder; FFmpeg candidat | clips + assetId → WebM VP8/Opus | E2E Chromium intermittent | sortie A/V déterministe |
| GENERATE | ComfyUI | `/api/comfy/queue`, `/api/comfy/job`; workflow → prompt_id → outputs | HTTP + Chromium E2E avec ComfyUI simulé, import PNG et IndexedDB | ComfyUI réel / GPU non testés |
| XR | X-Ray Mirror / MediaPipe | horodatage pose/gestes → bus d'événements | non intégré | adaptateur réel, licence et version |
| AUDIO | WebAudio / Sherpa-ONNX | PCM/WAV → piste/segments | piste EDIT partielle | mixage/ASR et service local |
| MEETING | VoiceStudio Sherpa-ONNX | audio → SRT/transcription | SRT manuel testé | liaison service locale, FR/EN |
| CAPTURE | COLMAP | photos → poses/maillage | non intégré | pipeline + packaging et licence |
| CINEMA | Blender / Three.js | scène/caméra → rendu | non intégré | API d'exécution et formats |
| AUTOMATE | Hermes / Chronos | action autorisée → résultat/journal | non intégré | protocole et confirmations |
| GRAPHICS | Canvas/SVG natif | calques → images | partiel | transfert à EDIT |
| LIBRARY | IndexedDB | assetId → Blob/manifest portable | Chromium E2E | robustesse inter-modules |
| CONTROL | Serveur Studio | `/api/health`, `/api/integrations` | HTTP Node | interface de diagnostic intégrée |

## Règles d'assemblage

1. Pas de fork de moteur sans preuve que l'API/CLI ne suffit pas. Aucune dépendance téléchargée implicitement.
2. Une intégration est « opérationnelle » seulement après commande, retour, transfert d'artefact, gestion d'erreur et test E2E. `reachable` reste une simple observation de port.
3. Adapter les formats par `assetId`, horodatages, type MIME et provenance. Permissions caméra/micro/OBS explicites. Localhost seulement.
4. Licences des projets tiers à **vérifier sur les versions réellement sélectionnées** avant redistribution. Les noms ci-dessus ne sont pas une autorisation de bundling.
5. GTX 1060 / GTX 1650 : performances **non mesurées**. Garder une voie CPU/dégradée et ne pas annoncer la compatibilité avant essai.

## P0 d'ici mercredi

- Vérifier la CI du HEAD, puis isoler l'export A/V intermittent. Diagnostics CI : 83 requêtes de trames sur 2,69 s, seulement 59 paquets vidéo finissant à 2,00 s, audio 2,72 s (run 43772642086). Ne plus ajouter de temporisations arbitraires; étudier FFmpeg local à timestamps maîtrisés.
- Faire afficher la matrice de capacité dans CONTROL et connecter au moins un flux réel inter-modules (par exemple sortie ComfyUI → LIBRARY) avec tests de sécurité.
- Publier paquet alpha et procédure de lancement, distinguer démontré/non démontré. Windows/OBS réel bloqués sans machine.

Références existantes à étudier, **sans présumer intégration** : https://github.com/walterlow/freecut (licence déclarée MIT dans issue #12, à revérifier), https://github.com/openreelio/openreelio (licence déclarée MIT, pré-alpha), https://github.com/VelornLabs/velorn (GPL-3.0 déclarée), https://github.com/colmap/colmap, https://github.com/comfyanonymous/ComfyUI, https://github.com/obsproject/obs-studio.

## Contrôle du 16/11/2026, 15 h (Paris)

- PR #16 : HEAD `ff7f94937039118c5a47cf57fbb957ede6eb1501`, toujours draft.
- CI GitHub Actions [43875052510](https://github.com/Sathancabrol/monorepo/actions/runs/43875052510) : **completed / success** sur ce HEAD (état du run confirmé par API ; logs de chaque step non relus ici). Ce résultat valide le workflow, pas Windows/GTX ni la reproductibilité du timing A/V.
- Correction documentaire : l'import ComfyUI simulé → LIBRARY/IndexedDB est déjà couvert par un E2E Chromium ; ne plus le décrire comme absent. Le test ComfyUI réel reste à faire.
- Prochaine tâche P0 : diagnostiquer l'intermittence du téléchargement Portable après undo/redo et répéter l'export A/V ; ensuite fallback FFmpeg déterministe ou limitation alpha documentée. Éviter les nouveaux tests défensifs redondants.
