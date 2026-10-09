# Sources techniques

Sources consultées le 7 octobre 2026. Les liens décrivent des contrats ou fonctionnalités ; aucune clé, donnée du serveur Olympus ou ressource Carré d'As privée n'a été utilisée.

## Discord

- [Discord Developer Documentation](https://discord.com/developers/docs/intro) — API officielle.
- [OAuth2](https://discord.com/developers/docs/topics/oauth2) — installation officielle de l'application/bot.
- [Application Commands](https://discord.com/developers/docs/interactions/application-commands) — slash commands et commandes contextuelles.
- [Gateway Intents](https://discord.com/developers/docs/events/gateway#gateway-intents) — intents disponibles et Message Content privilégié.
- [discord.py — API reference](https://discordpy.readthedocs.io/en/stable/) — client et application commands Python.

## Modèles et stockage

- [Ollama — OpenAI compatibility](https://ollama.com/blog/openai-compatibility) — client Chat Completions compatible pour un service Ollama local.
- [Ollama API](https://docs.ollama.com/api/introduction) — endpoints locaux et cloud.
- [OpenAI Help — facturation ChatGPT et API séparée](https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform).
- [SQLite FTS5](https://www.sqlite.org/fts5.html) — index plein texte local.
- [Python `sqlite3`](https://docs.python.org/3/library/sqlite3.html) — moteur SQLite utilisé par le stockage asynchrone.

## Pistes média non encore intégrées

- [sanoTTS](https://github.com/Ampixa/sanoTTS) et [paquet Python](https://pypi.org/project/sanotts/) — famille de TTS locaux très compacts ; voix françaises à évaluer avant sélection.
- [Piper — voix disponibles](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/VOICES.md) — listes de voix, dont le français.
- [Kokoro](https://github.com/hexgrad/kokoro) — modèle TTS open weights multilingue, plus volumineux.
- [whisper.cpp](https://github.com/ggml-org/whisper.cpp) — piste de transcription/STT locale, non intégrée.

## Vision par caméra, facial et IRMf — veille du 9 octobre 2026

- [Recherche comparative LAPLACE — modèles vision, webcam et IRMf](RECHERCHE-MODELES-VISION-IRMf.md) — panorama des modèles pré-entraînés, licences et adéquation aux contraintes local-first, photo ponctuelle consentie, absence d’inférence mentale non justifiée. Aucun modèle ni poids n’est intégré.
- [MediaPipe Face Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker) et [Object Detector](https://ai.google.dev/edge/mediapipe/solutions/vision/object_detector) — repères faciaux, mouvements descriptifs et détection d’objets.
- [OpenCV Zoo — YuNet](https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet) et [SFace](https://github.com/opencv/opencv_zoo/tree/main/models/face_recognition_sface) — distinguer détection de visage et reconnaissance d’identité; licences spécifiques par modèle.
- [Places365](https://github.com/CSAILVision/places365) — classification de scènes; les poids publiés demandent attribution CC BY.
- [EmotiEffLib](https://github.com/sb-ai-lab/EmotiEffLib) et la revue [Emotional Expressions Reconsidered](https://pmc.ncbi.nlm.nih.gov/articles/PMC6640856/) — classificateur de mouvements faciaux et limites d’inférence émotionnelle.
- [GazeFollower](https://github.com/GanchengZhu/GazeFollower), [OpenVINO Open Model Zoo](https://github.com/openvinotoolkit/open_model_zoo) et [rPPG-Toolbox](https://github.com/ubicomplab/rPPG-Toolbox) — regard, estimation physiologique et licences à vérifier.
- [BrainLM](https://github.com/vandijklab/BrainLM), [fm-MAE](https://github.com/MedARC-AI/fmri-fm) et [CortexMAE](https://github.com/MedARC-AI/CortexMAE) — modèles dépendant d’entrées IRMf; non applicables directement à une webcam.

## Portée de la recherche

Les recherches dans le dépôt n'ont trouvé aucun module Carré d'As. Aucun service public/API officielle sous ce nom n'a été confirmé dans cette session. Ne pas interpréter cette absence de résultat comme la preuve qu'aucune API privée n'existe.
