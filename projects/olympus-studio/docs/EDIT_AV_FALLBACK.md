# EDIT — export A/V déterministe (alpha, 19/11/2026)

Le rendu **MediaRecorder** du bouton WebM reste expérimental : un test Chromium a mesuré une désynchronisation de 759 ms. Ne pas considérer ce bouton comme fiable pour un export audio final.

## Parcours alternatif explicite, gratuit et local

1. Dans **EDIT**, exporter les images PNG numérotées vers un dossier vide via le bouton de séquence PNG. Exporter séparément la piste WAV. Les images doivent s'appeler `000001.png`, `000002.png`, etc., sans trous, avec un FPS identique à celui choisi dans EDIT.
2. Installer FFmpeg/FFprobe localement et vérifier `ffmpeg -version` et `ffprobe -version`. Aucun téléchargement automatique n'est réalisé par le script.
3. Depuis `projects/olympus-studio`, lancer :

```powershell
python tools/ffmpeg_mux_fallback.py --frames-dir "C:\\Exports\\frames" --fps 24 --audio "C:\\Exports\\audio.wav" --output "C:\\Exports\\montage.webm" --av-report --max-end-delta 0.2
```

Le fichier WebM contient VP9/Opus si l'encodage réussit. `--av-report` affiche les bornes des paquets audio/vidéo mesurées par FFprobe; `--max-end-delta 0.2` refuse et supprime le fichier produit si l'écart final dépasse 200 ms. Ce seuil **ne garantit pas** une synchronisation correcte au milieu de la timeline ni une écoute satisfaisante. `--audio-offset 0.25` retarde la piste audio de 250 ms si une correction mesurée est nécessaire; ne pas régler au hasard.

**Sécurité** : ne jamais utiliser un dossier PNG contenant des fichiers inconnus; le script refuse les liens symboliques, noms non contigus et sorties existantes. Les médias sources ne sont pas modifiés. Export limité à 7 200 images et 60 FPS; l'encodage est limité à 300 s. Les tests CI utilisent des fixtures synthétiques sous Ubuntu, pas les GPU Windows.

## État de validation

- Scénario PNG → FFmpeg VP9/Opus et rapport FFprobe : déjà couvert en CI sur fixtures.
- Nouveau garde-fou `--max-end-delta` : test CLI ajouté; **CI du nouveau commit à vérifier**.
- Parcours utilisateur complet, Windows, GTX 1060/1650, qualité sonore et licences de redistribution : **non validés**.
- Les 12 espaces restent dans l'interface; FFmpeg est une dépendance locale externe et non un moteur réécrit.
