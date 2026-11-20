# Architecture cible

## Interconnexion
```
OLYMPUS Studio — shell et document de projet commun
  ├── LIVE : OBS externe (obs-websocket v5), composition locale
  ├── EDIT : FreeCut (MIT) ou OpenReelio (MIT) — choix après benchmark
  ├── GENERATE : ComfyUI API, jobs différés, coûts nuls si modèles locaux
  ├── XR / CAPTURE : X-Ray Mirror → détections/poses/gestes
  ├── SPATIAL / CINEMA : Watchtower/Cesium, Blender, COLMAP/SLAM
  ├── MEETING / AUDIO : WhisperLiveKit ou sherpa-onnx, traduction optionnelle
  ├── AUTOMATE : Chronos/Hermes comme service out-of-process
  └── LIBRARY/CONTROL : SQLite, media store, droits d'accès, observabilité
```

## Point d'intégration unique
Chaque moteur doit fournir des **capacités** (`available`, `configured`, `tested`), des **commandes** (`request_id`, `dry_run`, `ack`), des **événements** horodatés monotoniques et des **ressources** (`media_id`, `scene_id`, `asset_uri`).

Référence temporelle : horloge projet, timestamps `time_us`, ancrages `source_id`. L'état du projet n'est pas la lecture des dossiers de chaque outil : on synchronise les actions et conserve les sources.

## Limites architecturales
- L'interface web n'est pas un remplacement de libobs. Pilotage par OBS WebSocket en premier, moteur natif envisagé plus tard.
- Une scène Cesium 3D ne se fusionne pas magiquement avec une scène Canvas 2D. Échanger un rendu vidéo / texture, une caméra et des métadonnées.
- Les inférences vidéo, la transcription, le montage et la génération ne doivent pas bloquer le thread de capture.
- L'import d'un dépôt tiers demande audit des licences et attribution, même quand le code est public.
- La transmission de médias et d'identifiants doit respecter consentement, confidentialité et provenance; API locales uniquement au départ.

## Paliers
A. Shell + projets + status adaptateurs ; B. sortie OBS + capture/audio et sauvegarde ; C. éditeur multipiste validé ; D. XR et réunion ; E. génération et VFX ; F. 3D spatiale ; G. industrialisation Windows.
