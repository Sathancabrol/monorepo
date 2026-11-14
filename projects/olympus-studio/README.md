# OLYMPUS Studio — poste de production unifié

**État :** fondation v0.2.3 (12 novembre 2026). Développement autonome dans `projects/olympus-studio/`, branche `feat/olympus-studio-20261112`. **Aucun changement dans les projets voisins, ni fusion dans main.**

## Intention
Une **seule interface** pour réalisation/streaming OBS, montage non destructif, IA image/vidéo ComfyUI, XR/X-Ray Mirror, géospatial/Watchtower, transcription/traduction/réunions, automations Chronos, audio, captures, personnages et bibliothèque locale. Gratuit et local en priorité; respecter Windows 10 et GPU GTX 1060 6 Go / GTX 1650 4 Go.

## Démarrage
Prérequis : Node.js >= 20 (22 recommandé). Aucune dépendance npm externe pour cette première fondation.

```bash
cd projects/olympus-studio
npm start
# http://127.0.0.1:8787
npm test
```

### Windows : lancement rapide

Télécharger l'artefact `olympus-studio-preview` depuis la dernière [exécution GitHub Actions](https://github.com/Sathancabrol/monorepo/actions/workflows/olympus-studio-ci.yml) réussie, extraire le ZIP et double-cliquer `LANCER_OLYMPUS.bat` (Node.js >=20 requis). Le lanceur n'installe rien, démarre seulement le serveur local sur `127.0.0.1:8787`. **Ce paquet n'est pas un programme .exe autonome et n'inclut ni OBS, ni ComfyUI, ni modèles.**

## Vrai périmètre du code livré
- Interface unique avec navigation entre 12 espaces, une scène 2D modifiable, calques, textes, images et fichiers vidéo, bibliothèque persistante IndexedDB, un storyboard séquentiel de montage et un panneau de connexions.
- Serveur local Node pour servir l'interface et diagnostiquer **OBS TCP 4455** et **ComfyUI 8188**. Une route permet l'envoi explicite de workflows ComfyUI API JSON au serveur local, et un second endpoint interroge l'historique d'un job et la liste des fichiers produits. Aucun traitement génératif n'a lieu sans ComfyUI installé et modèles; aucun import automatique de ses médias n'est encore réalisé.
- Sauvegarde/restauration JSON des scènes et paramètres. **IndexedDB** conserve les médias importés dans l'origine locale du navigateur et permet leur reliaison via un identifiant stable. Bouton **Portable** : JSON avec images/vidéos embarquées si le total ne dépasse pas 45 Mo. Ne pas vider les données du navigateur; l'export portable reste recommandé.
- Sortie MJPEG pour OBS : dans LIVE activer **Sortie OBS**, puis ajouter à OBS une **Source navigateur** `http://127.0.0.1:8787/obs` (1280 × 720). Vidéo uniquement, jusqu’à environ 6-7 ips JPEG selon la machine; audio à capturer dans OBS. Non testé dans OBS sur la tour.
- MEETING : segments manuels, import/export SRT horodaté, export du compte rendu Markdown; les sous-titres sont **privés par défaut**, affichables sur le programme seulement après activation explicite. Pas d'ASR automatique.
- Import des anciens projets **v0.3** (JSON normal ou portable) : conversion de la géométrie, reprise des références médias, préservation des notes, clips et règles dans `legacyV03` sans les exécuter. Les fonctions UI de l'ancien v0.3 ne sont pas encore portées.
- Sélection scène, masquage des calques, ajout de textes, capture d'image PNG de la composition. La timeline principale reste une vue des calques. L'espace **EDIT** contient désormais un vrai **storyboard séquentiel** : import de médias du coffre, ordre, durée, titres, lecture de prévisualisation et export WebM **sans audio** (max. 120 secondes). Il ne s'agit pas encore d'un monteur multipiste ni d'un rendu final professionnel. Le contrôle distant d'OBS et la sortie MJPEG sont des circuits séparés.
- **Non implémenté / non testé** : streaming natif, audio multipiste avancé, montage multipiste fiable, caméra virtuelle, ASR local, reconstruction 3D, connexion réelle à OBS ou aux agents/applications du PC. Aucun droit d'accès à la tour Windows depuis cette session.

## Historique et provenance
Le prototype web local **OLYMPUS Studio v0.3** (indépendant, plus avancé sur plusieurs aspects) existe aussi dans les artefacts de la conversation : LIVE Canvas, WebM, fonctions de réunion, passerelles XR et GeoJSON, sorties vers OBS via serveur aiohttp optionnel. Un **importeur de projets v0.3** existe maintenant, mais la totalité de ses fonctions (storyboard, contrôle automatisé, éditeur de concepts) n'a **pas** été fusionnée : voir issue #11. Ne pas confondre ce socle GitHub avec une v0.3 fusionnée.

## Documents
- [Architecture](docs/ARCHITECTURE.md)
- [Régie OBS et enregistrement audio (v0.2)](docs/OBS_REMOTE.md)
- [État vérifié et limites](docs/STATUS.md)
- [Plan d'itérations et définition de terminé](docs/SESSION_PLAN.md)
- [Interventions éventuelles de l'utilisateur](docs/NEEDS_USER.md)
- [Backlog et plan de recherche](docs/ROADMAP.md)
- [Contrats d'intégration](docs/CONTRACTS.md)
- [Benchmark / licences](research/COMPARATIF.md)

## Règles
1. *Une seule fenêtre* et un modèle de projet commun, pas une juxtaposition de pages web.
2. Les moteurs tiers sont d'abord reliés **en processus séparés**, avant tout fork ou redistribution.
3. LIVE a priorité sur les traitements IA lourds; génération vidéo **différée** sur GPU modestes.
4. Aucun service cloud obligatoire, aucune clé dans Git, pas de collecte secrète, pas de scan biométrique non autorisé.
5. Toute case « terminé » doit fournir une preuve reproductible, version, plate-forme et test.

### Montage EDIT v0.2.3
- Vidéos : champs de découpe **IN/OUT** et bouton **Diviser au curseur**. La source est préservée dans la médiathèque. Tests mathématiques et JSON validés; tests navigateur/Windows à venir.
- [Mode d'emploi et limites](docs/EDIT_TRIM.md).

## Itération v0.2.4 — durée source vidéo vérifiée dans EDIT

- Lecture asynchrone des métadonnées du fichier (`HTMLVideoElement.duration`), délai d'attente borné de 4,5 s.
- Les nouvelles vidéos de 2 s ne reçoivent plus automatiquement un clip de 5 s; la première durée s'adapte à la source.
- Les champs **IN/OUT** rejettent une coupe après la fin réelle d'une vidéo lorsque la durée est connue; un ancien projet hors plage affiche un avertissement.
- 34 tests Node réussis; test Chromium headless avec une vidéo WebM synthétique de 2 s : import, durée, coupe invalide, division (sans tests Windows/IndexedDB).
- Pour reproduire le test de navigateur localement : installer Python Playwright (`python -m pip install playwright`), FFmpeg et Chromium/Chrome, puis lancer `python tests/browser_media_smoke.py`. Cela ne fait partie **ni de l'installation normale du studio, ni des 34 tests Node de CI**.
- [Documentation et limites de la découpe](docs/EDIT_TRIM.md).

## v0.2.5 — bande-son EDIT expérimentale et autonomie du chantier

- `+ Média` accepte `audio/*`. Un fichier sonore peut être placé dans la timeline EDIT, avec son heure de départ, son point IN, son volume et son activation. Le projet sauvegarde la référence `editAudioTrack` et l'export portable inclut le média audio.
- L'export EDIT tente de combiner Canvas + piste WebAudio dans WebM ; **le rendu audiovisuel n'est pas encore validé sur Windows**. Les clips vidéo restent muets dans EDIT; une seule bande-son indépendante est disponible.
- [Documentation AUDIO](docs/EDIT_AUDIO.md) · [Backlog de développement autonome](docs/AUTONOMOUS_BACKLOG.md).
- Automatisation ChatGPT active quotidiennement à 02:00 Europe/Paris; elle lit ce backlog, avance la première tâche possible et consigne tests/commits dans ce dossier, sans nécessiter la commande « continue ».
