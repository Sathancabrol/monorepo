# EDIT — pont FFmpeg local (expérimental, CLI)

Le montage EDIT peut désormais produire un WebM VP9/Opus à partir d'un **fichier vidéo seule existant**, d'une **source audio locale** et du contrat de piste `src/edit-audio.js`. Cette voie réutilise FFmpeg et n'exige aucun cloud.

```sh
node scripts/render-edit-av.mjs video.webm audio.wav track.json 2 sortie.webm
```

Exemple de `track.json` : `{"assetId":"source-audio","inPoint":0.2,"offset":0.25,"volume":0.4,"enabled":true}`.

- Le pont rend d'abord un WAV temporaire 48 kHz stéréo avec IN/départ/volume/mute, puis encode VP9 et Opus dans WebM. Il vérifie les codecs via ffprobe et nettoie le WAV temporaire.
- Il refuse une sortie déjà existante, les chemins source/sortie identiques, les durées invalides et les fichiers absents. Aucune donnée personnelle n'est envoyée.
- **Limite importante :** la vidéo provient d'un fichier déjà encodé; si MediaRecorder a perdu des images, ce pont **ne recrée pas** les images perdues et ne garantit pas la synchronisation. La vérification A/V réelle et la génération déterministe des frames restent ouvertes.
- Ce script n'est **pas** connecté à un bouton de l'interface. L'installation FFmpeg/ffprobe et les droits de redistribution doivent être vérifiés séparément. Aucun test Windows/GTX ou écoute humaine n'est revendiqué.

Preuve automatisée : `tests/render-edit-av-real.test.mjs` génère des fixtures FFmpeg et vérifie VP9/Opus, non-écrasement et intégrité des sources via `npm test`.
