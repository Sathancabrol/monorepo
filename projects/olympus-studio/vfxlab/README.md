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
