# Contrats d'intégration v0 — proposition

Ces contrats facilitent l'interopérabilité des moteurs existants sans copier leur code. **Non encore implémentés dans Watchtower, X-Ray Mirror et Chronos.**

## Enveloppe événement

```json
{
  "schema": "olympus.event.v0",
  "event_id": "uuid",
  "source": "xray|watchtower|obs|comfyui|meeting|chronos",
  "type": "detection|pose|gesture|caption|spatial|job|command_result",
  "source_id": "camera-1",
  "time_us": 12345678,
  "frame_id": 212,
  "confidence": 0.94,
  "payload": {}
}
```

Horodatage monotone pendant la session + relation explicite à l'horloge du projet. Pas d'inférence sur la précision (les inconnus restent inconnus).

### Détection 2D

```json
{
  "type": "detection",
  "payload": {
    "track_id": "track-3",
    "label": "person",
    "bbox_xywh_normalized": [0.1, 0.2, 0.35, 0.6],
    "confidence": 0.87
  }
}
```

### Geste

```json
{
  "type": "gesture",
  "payload": {"name": "finger_snap", "phase": "recognized", "strength": 0.7}
}
```

Les gestes déclenchent des actions **uniquement s'ils sont activés explicitement**. Configuration du seuil, délai antirebond, annulation, journal d'action.

### Spatial 3D

```json
{
  "type": "spatial",
  "payload": {
    "crs": "EPSG:4326",
    "geometry_type": "Point",
    "coordinates": [3.75, 43.45],
    "provenance": "measured|estimated|hypothesis",
    "confidence": null
  }
}
```

Un `Point` en EPSG:4326 ne se projette **pas** directement en pixels Canvas sans moteur de transformation/caméra.

### Transcription

```json
{
  "type": "caption",
  "payload": {
    "text": "Texte transcrit à vérifier",
    "speaker_id": "speaker-2",
    "speaker_assignment_confidence": null,
    "language": "fr",
    "start_us": 2100000,
    "end_us": 5600000,
    "derived_from": "audio-source-2",
    "verified": false
  }
}
```

## Traitement asynchrone IA

`GenerationJob` : `id`, `workflow_id`, `model_id`, `license`, `input_assets[]`, `output_assets[]`, `created_at`, `status:queued|running|completed|failed|cancelled`, `progress`, `hardware_snapshot`. Les sorties sont des fichiers locaux à importer dans la bibliothèque, **jamais des références temporaires seules**.

## Sécurité

- Ne pas accepter de commande exécutable depuis un message de transcription ou une donnée externe.
- OBS : authentification locale sans stockage de mot de passe en clair.
- Service local : bind `127.0.0.1` par défaut; aucun accès LAN/tunnel sans autorisation.
- Sources privées (notes, assistant) interdites dans sortie streaming par défaut.
