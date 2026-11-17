# OLYMPUS Studio — matrice d'intégration pour l'alpha du 18/11/2026

Ce tableau distingue **présence de l'interface**, **adaptateur codé**, **preuve automatisée** et **validation sur matériel réel**. Les chemins ci-dessous désignent le code sur la branche dédiée, pas des installations garanties. Les licences et versions des exécutables externes doivent être vérifiées sur les distributions effectivement utilisées avant redistribution. Aucun binaire tiers n'est inclus par cette matrice.

| Espace | Source réutilisée / état de licence | Adaptateur et contrat I/O observables | Niveau de preuve / limite |
|---|---|---|---|
| LIVE | Canvas navigateur (API Web), OBS externe (GPL, à confirmer pour version distribuée) | `src/app.js` scène/calques → Canvas; `src/obs-client.js` / `src/obs-panel.js` commandes WebSocket v5 | Tests simulés OBS; OBS réel et audio de sortie non validés |
| EDIT | MediaRecorder/WebAudio natifs; FFmpeg externe libre, licence du build à vérifier | `src/storyboard.js`, `src/edit-audio.js`, `src/editor-export.js`; clips + piste audio → WebM; réparation FFmpeg séparée | E2E Chromium A/V intermittent; secours peut figer la dernière image, ne restaure pas les mouvements |
| GENERATE | ComfyUI externe (licence/version à auditer) | `server.mjs` API locale, `src/comfy-output.js` sortie de job → média de bibliothèque | Mock HTTP/Chromium; vrai ComfyUI et modèles GPU non testés |
| XR | X-Ray Mirror externe, licence/version à auditer | `src/app.js` événements de détection JSON → superposition Canvas | Import manuel, pas de bus temps réel ni de tracking validé |
| AUDIO | WebAudio navigateur | `src/edit-audio.js` asset audio + IN/départ/volume → mixage EDIT | Audio EDIT testé en E2E synthétique; pas de station multipiste autonome validée |
| MEETING | Utilitaires SRT locaux, ASR sherpa-onnx/Whisper envisagés (licences à vérifier) | `src/meeting-utils.js` segments ↔ SRT/Markdown | Tests utilitaires; transcription ASR réelle non intégrée |
| CAPTURE | COLMAP/SLAM envisagés, aucune distribution validée | Pas de contrat d'entrée/sortie 3D opérationnel prouvé | Espace navigable uniquement, reconstruction non validée |
| CINEMA | Canvas navigateur; moteurs 3D à sélectionner | Pas de pipeline caméra/lumière/VFX autonome prouvé | Espace navigable, moteur non validé |
| AUTOMATE | Hermes/Chronos externes | Aucun contrat de permissions et journal d'actions vérifié | Espace navigable, orchestration non intégrée |
| GRAPHICS | Canvas navigateur | Scènes et calques texte/formes `src/app.js` → image PNG | Fonction Canvas présente; animation dédiée non validée |
| LIBRARY | IndexedDB navigateur | `src/media-store.js` Blob ↔ assetId, projet JSON Portable ↔ médias | E2E HTTP/Chromium; téléchargement répété parfois intermittent; Windows non testé |
| CONTROL | Diagnostics locaux OBS/ComfyUI | `server.mjs` états de services locaux → UI | Diagnostics HTTP, pas de mesures GPU réelles |

## Contrat transversal cible (non encore implémenté intégralement)

- Identifiant média stable `assetId`, Blob local et provenance; aucune URL arbitraire distante.
- Événement `{type, timestampMs, source, payload, schemaVersion}` validé avant routage. Un schéma proposé **n'est pas** un bus fonctionnel.
- Adaptateur déclaré `{id, version, capabilities, inputSchema, outputSchema, offline, license, health}` et résultat de test attaché; une dépendance installée ne vaut pas intégration.
- Les permissions micro/caméra/OBS/agents sont explicites; aucune action externe automatique.

## Décision de livraison

Pour l'alpha : préserver les 12 espaces accessibles, prioriser EDIT, IndexedDB/Portable, paquet ZIP et lancement HTTP. Documenter les espaces non opérationnels au lieu d'ajouter des moteurs inachevés. GTX 1060 6 Go et GTX 1650 4 Go : **compatibilité non mesurée**; limiter les traitements simultanés et éviter toute promesse de FPS/VRAM.

## Recette bloquante

1. CI du **HEAD** verte, avec téléchargement ZIP et `unzip -t`.
2. Ouvrir le paquet extrait, démarrer le serveur local, parcourir 12 espaces.
3. Importer média, couper deux segments, sauvegarder/recharger, restaurer Portable et vérifier octets.
4. Exporter EDIT avec audio et contrôler pistes/horodatages/écoute; en cas d'échec, documenter le secours FFmpeg et ses pertes.
5. Essais Windows 10, OBS réel, GTX 1060/1650, licences redistribuées : **non effectués**; ne pas annoncer une recette complète.
