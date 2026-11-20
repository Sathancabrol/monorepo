# Repérage des projets intégrables — 2026-11-12

| Produit | Couverture forte | Licence constatée | Stratégie | Risque principal |
|---|---|---|---|---|
| [FreeCut](https://github.com/walterlow/freecut) | Montage multipiste, WebGPU, WebCodecs, IA navigateur | MIT | **Candidat montage n°1** : auditer les modules réutilisables | GPU WebGPU / navigateur vieillissant |
| [OpenReelio](https://github.com/openreelio/openreelio) | NLE Tauri/Rust, FFmpeg, agent CLI/MCP, historique des commandes | MIT, pré-alpha | Alternative native Windows | maturité/stabilité, moteur Rust distinct |
| [Velorn](https://github.com/VelornLabs/velorn) | Génération ComfyUI, timeline, planification et 100+ outils MCP | GPL-3.0 | Référence intégration GENERATE; PoC comme service séparé | obligations GPL si fusion ; ComfyUI requis pour génération |
| [OBS Studio](https://github.com/obsproject/obs-studio) | Capture, mixage, streaming, caméra virtuelle, multiscènes | GPL-2.0 | **Piloter** OBS via obs-websocket ou Browser Source | API différente de timeline EDIT |
| [ComfyUI](https://github.com/comfyanonymous/ComfyUI) | IA image/vidéo par graphes, API HTTP | GPL-3.0 | Exécuter séparément et lier au catalogue de jobs | GPU / modèles / nœuds / licences |
| [XR Animator](https://github.com/ButzYung/SystemAnimatorOnline) | Avatars et tracking webcam | Vérifier conditions exactes des fichiers | Référence technique, adaptateurs non fusionnés | droit commercial et perfs |
| [SuperSplat](https://github.com/playcanvas/supersplat) | Éditeur de Gaussian splats | Vérifier licence/version avant réutilisation | Spatial/CINEMA | moteur GPU et formats |
| [COLMAP](https://github.com/colmap/colmap) | Reconstruction image vers 3D | Licence à revalider | Capture après enregistrement | calcul lourd et qualité de prises de vue |
| [WhisperLiveKit](https://github.com/QuentinFuxa/WhisperLiveKit) | ASR temps réel et diarisation | Vérifier fichiers/modèles | MEETING, serveur local | latence et provenance des transcriptions |
| [React Flow](https://github.com/xyflow/xyflow) | Graphes interactifs / automation | Vérifier package spécifique | AUTOMATE | dépendance / intégration |
| [Rerun](https://github.com/rerun-io/rerun) | Timeline multimodale, nuages de points | Vérifier licence/version | Inspection des données | pas un éditeur vidéo généraliste |
| [PRISM Live Studio](https://github.com/naver/prism-live-studio) | Régie basée sur OBS | Multilicence à auditer | Benchmark LIVE, pas un cœur de montage | coût de fork/maintenance |

**Conclusion provisoire :** aucune application validée ne couvre à elle seule le cahier des charges LIVE + EDIT + IA vidéo + XR + 3D + MEETING. Préférer une *seule interface Olympus* pilotant plusieurs processus locaux, avec bibliothèque/projet commun.

Sources vérifiées :
- FreeCut https://github.com/walterlow/freecut (README, licence MIT).
- Velorn https://github.com/VelornLabs/velorn (GPL-3.0; génération actuelle via ComfyUI).
- OpenReelio https://github.com/openreelio/openreelio (MIT et statut pré-alpha).
- OBS Browser Source https://obsproject.com/kb/browser-source.

**Exclusion de base** : Remotion n'est pas entièrement open source OSI et ses conditions changent selon l'usage et la redistribution. Voir https://www.remotion.dev/docs/license/pricing.
