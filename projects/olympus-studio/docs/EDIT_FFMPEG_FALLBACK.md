# EDIT — secours FFmpeg (alpha du 18/11/2026)

Cette procédure est **manuelle, locale et facultative**. Elle ne corrige pas les images déjà perdues par MediaRecorder. FFmpeg et ffprobe doivent être installés séparément ; aucun téléchargement implicite.

1. Dans EDIT, sélectionner les clips et la piste audio, puis utiliser **Vidéo seule (secours FFmpeg)**. Attendre le téléchargement WebM. Garder l'onglet visible pendant la capture ; cette voie utilise encore MediaRecorder pour la vidéo.
2. Utiliser **Télécharger audio source** pour obtenir les octets originaux de la piste audio choisie dans IndexedDB. Cette action exige une piste activée. **Important :** ce fichier n'est PAS le rendu de la timeline : le départ, le point IN, le volume, les silences et les découpes ne sont pas appliqués. Si nécessaire, préparer manuellement l'audio dans un outil libre avant le multiplexage.
3. Dans un terminal ouvert à la racine de Studio, exécuter :
   
   ```bash
   python tools/ffmpeg_mux_fallback.py --video "video.webm" --audio "audio.wav" --output "montage-final.webm"
   ```

   Pour un décalage constant connu, ajouter `--audio-offset 0.25` (retarde l'audio de 250 ms) ou une valeur négative pour l'avancer. Limite ±120 secondes.
4. Contrôler le résultat avec `ffprobe -v error -show_streams montage-final.webm`, puis **visionner et écouter** le fichier. Les tests automatiques de codecs ne remplacent pas l'écoute.

**Garanties et limites :** les sources ne sont pas écrasées ; un fichier de sortie déjà existant est refusé ; un résultat partiel est supprimé après échec. Le multiplexage réencode VP9/Opus et peut être lent sur CPU. La source audio brute peut contenir une durée supérieure à la vidéo ; `-shortest` arrête au flux le plus court. Les problèmes de cadence, de synchronisation variable, de rendu des clips et de perte d'images ne sont pas corrigés par un décalage constant.

**Statut de recette :** parcours utilisateur nouvellement exposé, mais pas encore validé sur Windows, GTX 1060/1650 ni par écoute humaine. Le mode A/V direct demeure expérimental.