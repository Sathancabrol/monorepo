# OLYMPUS • VFX Lab
Module local d'effets vidéo temps réel, inspiré de GLAZE CRT sans reprendre son code ni ses ressources. Version 0.1 : prototype navigateur autonome, sans dépendances, image/vidéo locale, webcam explicite, réglages CRT/VHS, PNG. L'intégration native dans le pipeline LIVE/EDIT reste à réaliser.
## Démarrer
Dans Olympus Studio (Node >=20), lancer `npm start` depuis `projects/olympus-studio`, ouvrir http://127.0.0.1:8787 et cliquer VFX LAB. Navigation séparée dans le même onglet ; le projet LIVE n'est pas partagé, sauvegarder avant de quitter. Seul index.html est autorisé par le serveur Studio.
### Mode autonome
Depuis ce dossier : `python -m http.server 8790 --bind 127.0.0.1`, ouvrir http://127.0.0.1:8790. Pour un simple test image, ouvrir index.html directement. Caméra : contexte sécurisé localhost et permission explicite. Les médias ne sont pas téléversés.
## Documents
- [AGENTS.md](AGENTS.md) : mandat, boucle, critères d'acceptation.
- [BENCHMARK.md](BENCHMARK.md) : registre des références.
- [ARCHITECTURE.md](ARCHITECTURE.md) : interfaces et feuille de route.
Ne pas considérer la compatibilité Windows, les performances, OBS ou l'intégration au Studio comme validées avant tests réels.

## Reality Lite 0.2 — 26 novembre 2026
Accessible dans VFX LAB depuis Olympus Studio (pas depuis le serveur Python statique pour le mode IA).
- Mode graphique : feedback temporel, teinte, contraste, saturation, rotation, mélange et ellipse centrale. Aucun modèle, aucun réseau.
- Mode IA : ComfyUI sur 127.0.0.1:8188, détection explicite des checkpoints, génération img2img manuelle ou répétée (une requête à la fois, 500 ms de pause après résultat), affichage du dernier résultat, seed fixe. Aucun cloud.
- L'ellipse est un masque de composition manuel, pas une segmentation ou un masque ControlNet. Les images sont redimensionnées en carré puis réétirées; la génération ne garantit pas la cohérence temporelle. Pas encore de motion capture connecté.
- Les captures JPEG et sorties restent dans les dossiers input/output de ComfyUI. Consentement explicite avant transmission. Arrêt de la boucle et rejet des résultats obsolètes lors d'un changement de source ; un job ComfyUI déjà soumis peut se terminer. Nettoyer manuellement les fichiers olympus-* et olympus_reality* lorsque nécessaire.
- Ne pas lancer simultanément Ollama GPU et génération IA si la VRAM est insuffisante. Ne pas télécharger automatiquement de modèle.

### Installation et essai sur Windows
1. Vérifier les moteurs et modèles déjà installés, espace disque externe, pilote et VRAM via nvidia-smi. ComfyUI doit être accessible localement sur le port 8188. Si absent : https://github.com/comfyanonymous/ComfyUI (choisir un environnement PyTorch/CUDA compatible Pascal ou Turing ; ne pas supposer que les builds récents supportent sm_61).
2. Utiliser un checkpoint complet SD-Turbo compatible CheckpointLoaderSimple (https://huggingface.co/stabilityai/sd-turbo, lire la licence), dans ComfyUI/models/checkpoints. Une variante Diffusers en plusieurs fichiers ne suffit pas. Si nécessaire, lancer ComfyUI avec --lowvram ou --cpu pour diagnostic ; CPU sera lent. Ne pas télécharger de poids si déjà présents.
3. npm start, ouvrir http://127.0.0.1:8787, VFX LAB. Tester le signal synthétique avec le mode graphique. Puis activer une webcam ou importer une vidéo.
4. Choisir Diffusion IA, Détecter modèles locaux, choisir SD-Turbo, autoriser les captures, sélectionner 256 ou 320, cliquer Générer une image. Vérifier le résultat et le temps. Seulement ensuite démarrer la boucle.
5. Tour GTX 1060 6 Go : débuter 320, puis 384/512 si stable. Portable GTX 1650 4 Go / RAM 8 Go : commencer 256, une seule image, garder la diffusion désactivée si OOM. Les deux profils utilisent 4 steps, denoise 0.5, CFG 1. Aucun FPS garanti.
6. npm test : inclut tests de contrat avec ComfyUI simulé, validation et garde anti-file. Mesurer latence, VRAM et FPS UI sur matériel réel ; les tests mock ne valident pas CUDA, ComfyUI ni le rendu.

### Backlog
SDXS (https://github.com/IDKiro/SDXS) : tester l'encodeur/conditionnement réellement disponible ; ne pas assimiler automatiquement txt2img à img2img. SD 1.5 + LCM : workflow dédié. stable-diffusion.cpp (https://github.com/leejet/stable-diffusion.cpp) : tester Vulkan/CUDA Pascal, quantification et TAESD, puis adaptateur persistant. StreamDiffusion V1 et LivePortrait : benchmark. V2 / Wan 1.3B : hors priorité locale. Reconnecter les landmarks X-Ray Mirror, segmentation MediaPipe, flow et warp entre keyframes, partager la caméra avec LIVE, sortie OBS, mesure VRAM/FPS, conservation limitée et purge opt-in. Pas de nouveau téléchargement lourd avant audit local.

## Reality Lite 0.3 — suivi corporel local
Le mode facultatif MediaPipe Pose Landmarker Lite (CPU) fournit les 33 points du corps, un masque de silhouette souple, un masque inverse du décor et un masque approximatif de la tête à partir des oreilles/nez. Ce ne sont pas des masques de diffusion/inpainting : ils servent à composer le rendu. Sans détection valide, les zones sémantiques n'appliquent pas l'effet. Le déplacement du centre épaules/hanches translate la dernière image IA (pas de déformation articulée ni d'optical flow). La capture IA est letterboxée, puis recadrée à l'affichage. Le moteur conserve une capture par session serveur (réécriture) et demande des sorties temporaires PreviewImage ; les fichiers peuvent subsister sur disque selon ComfyUI.
Depuis le dossier Studio, lancer explicitement `powershell -NoProfile -File scripts/install-reality-pose.ps1` après vérification des assets existants et des licences. Ce script récupère le runtime MediaPipe 0.10.14 et le modèle Lite version 1, sans admin et sans télécharger de modèle de diffusion. Le runtime est local ensuite. Ne pas committer vfxlab/vendor (assets tiers et lourds). Démarrer Studio, activer suivi corps local, puis choisir Personne/Décor/Tête ou afficher squelette. Tester en mode graphique avant IA. CPU adaptatif, pas de FPS garanti.
Installation physique et test Windows : voir [mandat Codex](CODEX_INSTALL.md). Les anciennes indications sur l'absence de suivi et la sauvegarde systématique des sorties décrivent 0.2, remplacées ici.
