# OLYMPUS Studio — poste de production unifié

**État :** fondation v0.1 (12 novembre 2026). Développement autonome dans `projects/olympus-studio/`, branche `feat/olympus-studio-20261112`. **Aucun changement dans les projets voisins, ni fusion dans main.**

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

## Vrai périmètre du code livré
- Interface unique avec navigation entre 12 espaces, une scène 2D modifiable, calques, textes, images et fichiers vidéo, bibliothèque de session, chronologie simple et panneau de connexions.
- Serveur local Node pour servir l'interface et diagnostiquer **OBS TCP 4455** et **ComfyUI 8188**. Une route permet l'envoi explicite de workflows ComfyUI API JSON au serveur local; aucune génération n'a lieu sans ComfyUI installé et modèles.
- Sauvegarde/restauration JSON des scènes et paramètres textuels. Les médias ajoutés comme objets URL navigateur ne survivent pas à un redémarrage : rechargement requis.
- Sélection scène, masquage des calques, ajout de textes, capture d'image PNG de la composition. La timeline est encore une vue d'édition illustrative, pas un NLE complet.
- **Non implémenté / non testé** : sortie OBS complète, streaming natif, montage multipiste fiable, caméra virtuelle, ASR local, reconstruction 3D, connexion réelle aux agents ou applications du PC. Aucun droit d'accès à la tour Windows depuis cette session.

## Historique et provenance
Le prototype web local **OLYMPUS Studio v0.3** existe aussi dans les artefacts de la conversation : LIVE Canvas, WebM, fonctions de réunion, passerelles XR et GeoJSON, sorties vers OBS via serveur aiohttp optionnel. Il n'est **pas encore importé intégralement dans ce dossier GitHub** : l'import complet est le premier chantier à réaliser après consolidation et tests. Ne pas confondre ce socle GitHub avec une v0.3 fusionnée.

## Documents
- [Architecture](docs/ARCHITECTURE.md)
- [État vérifié et limites](docs/STATUS.md)
- [Backlog et plan de recherche](docs/ROADMAP.md)
- [Contrats d'intégration](docs/CONTRACTS.md)
- [Benchmark / licences](research/COMPARATIF.md)

## Règles
1. *Une seule fenêtre* et un modèle de projet commun, pas une juxtaposition de pages web.
2. Les moteurs tiers sont d'abord reliés **en processus séparés**, avant tout fork ou redistribution.
3. LIVE a priorité sur les traitements IA lourds; génération vidéo **différée** sur GPU modestes.
4. Aucun service cloud obligatoire, aucune clé dans Git, pas de collecte secrète, pas de scan biométrique non autorisé.
5. Toute case « terminé » doit fournir une preuve reproductible, version, plate-forme et test.
