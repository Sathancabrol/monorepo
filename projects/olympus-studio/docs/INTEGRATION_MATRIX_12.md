# Matrice d'intégration des 12 espaces — audit de code, 20/11/2026

**Règle de preuve** : « codé » signifie qu'un adaptateur existe dans ce dépôt; « CI » signifie uniquement test Linux/Chromium automatisé documenté; « réel » exige un moteur externe effectivement lancé. La présence d'un nom ou d'un port ne prouve aucune intégration. Matrice fondée sur les fichiers de cette branche, sans inspection des versions installées sur Windows. La liste exploitable par le serveur est `src/integration-registry.js` et `GET /api/integrations`.

| Espace | Source existante / adaptateur actuel | Contrat entrée → sortie | Preuve et limite | Licence / hors ligne / GTX |
|---|---|---|---|---|
| LIVE | OBS Studio → `src/obs-client.js`, `src/obs-panel.js`; sortie MJPEG `/obs` | commandes scènes/REC, Canvas JPEG → flux local | commandes mockées; OBS réel non essayé | OBS GPL; connexion externe, redistribution à auditer; local; GPU non mesuré |
| EDIT | Storyboard interne + `src/edit-frame-renderer.js` + FFmpeg CLI externe | clips + médias → PNG/WAV → VP9/Opus WebM, FFprobe | fixture FFmpeg CI; export MediaRecorder A/V instable; Windows non essayé | FFmpeg licence dépend de la compilation; exécution locale; encodage CPU/GPU à mesurer |
| GENERATE | ComfyUI → `server.mjs` API locale + import `src/comfy-output.js` | workflow JSON → job → média validé → IndexedDB | mock HTTP/Chromium; ComfyUI réel non essayé | licence ComfyUI et modèles distinctes à relever par version; offline après installation; VRAM non mesurée |
| XR | X-Ray Mirror / MediaPipe → `src/studio-event-bus.js` (import manuel) | détections/gestes horodatés → calques | UI synthétique testée, pas de flux caméra X-Ray réel | licence/versions à contrôler; local possible; GPU non mesuré |
| AUDIO | WebAudio + `src/edit-audio.js` | média audio + IN/offset/gain → piste EDIT/WAV | contrat Node et navigateur partiels, écoute non prouvée | API navigateur; local; matériel audio non testé |
| MEETING | SRT manuel `src/meeting-utils.js`; Sherpa-ONNX VoiceStudio envisagé | segments → SRT/Markdown; PCM → ASR **absent** | tests utilitaires, pas de transcription automatique | licence/version ASR et modèle à vérifier; offline visé |
| CAPTURE | COLMAP / photogrammétrie envisagé; aucun adaptateur | images/vidéo → poses/maillage **absent** | non intégré | licences/API/version et charge GPU à évaluer |
| CINEMA | Blender/Three.js envisagés; Canvas existant distinct | scène/caméra → rendu **absent** | non intégré | licences et mécanisme IPC à évaluer; GTX non mesurée |
| AUTOMATE | Hermes / Chronos envisagé; aucun adaptateur actif | commande autorisée → événement/résultat **absent** | non intégré; pas d'exécution distante | licence/permissions et offline à vérifier |
| GRAPHICS | Canvas 2D local dans `src/app.js` | calques → images/composition | fonctions UI codées; pas d'éditeur motion complet | API navigateur; offline |
| LIBRARY | `src/media-store.js` IndexedDB + Portable | assetId → Blob + manifeste JSON | Chromium HTTP/Portable testé; scénario WebM restauré validé sur CI antérieure; décodage nouveau à confirmer | API navigateur; offline; limite export 45 Mo |
| CONTROL | `server.mjs` `/api/health`, `/api/integrations` | sondes locales → état informatif | HTTP testé; port joignable ≠ API/auth opérationnelles | Node local; aucun moteur lancé automatiquement |

## Décisions d'intégration

1. **Réutiliser** les moteurs en processus externes via adaptateurs explicites, sans copier leur code ni télécharger silencieusement modèles ou dépendances.
2. Conserver le bus événementiel `src/studio-event-bus.js` comme contrat interne, mais ne pas déclarer X-Ray/Chronos/Watchtower connectés tant que l'entrée réelle et les tests de bout en bout manquent.
3. Pour EDIT, conserver le fallback FFmpeg PNG/WAV déterministe et son contrôle FFprobe. Timeboxer MediaRecorder et garder le test de désynchronisation rouge si défaut réel.
4. **Licence non vérifiée ≠ compatible** : avant redistribution, relever version, URL source, SPDX/texte licence, licences des modèles et options de build (particulièrement FFmpeg). Ne pas redistribuer ces moteurs dans l'alpha sans audit.
5. **GTX 1060 / 1650** : aucune compatibilité opérationnelle garantie; ne pas inférer FPS, VRAM ni support d'encodeur à partir de fiches théoriques.

## Contrat d'acceptation d'un nouvel adaptateur

Documenter source/version/licence; entrée typée, sortie typée, erreurs et timeout; permissions explicites; test fixture sans moteur; test d'intégration sur vrai moteur; comportement hors ligne; charge CPU/RAM/VRAM sur cible; journal de provenance. Les statuts `mock-tested`, `partial`, `not-integrated` ne deviennent pas « réel » sur simple disponibilité d'un port.

**Prochaine tranche** : exposer le fallback FFmpeg depuis EDIT par un guide contextualisé, puis E2E du parcours et vérification CI du nouveau décodage WebM; la recette Windows reste indépendante.
