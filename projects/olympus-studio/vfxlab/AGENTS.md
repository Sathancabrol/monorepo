# Mandat agents — OLYMPUS VFX Lab
## Mission
Construire un laboratoire VFX réellement utilisable dans Olympus Studio et autonome si nécessaire. Inspirer l'expérience de GLAZE CRT, sans copier assets propriétaires. Local-first, budget 0 EUR, sans abonnement, Windows 10/11, GTX 1060 6 Go et GTX 1650 4 Go. Priorité fluidité LIVE ; pas de cloud obligatoire.
## Première action
Lire README, BENCHMARK, ARCHITECTURE, puis les docs et sources Olympus Studio. Sur la tour, détecter les clones, versions locales, disque externe, OBS, FFmpeg, navigateurs, pilotes, NTSCRT et autres candidats avant de télécharger quoi que ce soit. Ne jamais effacer ni écraser un travail local non commité. Utiliser un worktree ou branche de travail. Rechercher les versions Olympus les plus avancées avant fusion ; préserver leurs fonctions.
## Loop autonome
1. Examiner git status/log, tests et backlog ; choisir une petite tâche vérifiable.
2. Rechercher les solutions existantes, vérifier licence et dépendances, comparer au besoin.
3. Concevoir, implémenter, tester les cas normaux et erreurs ; contrôler performances et confidentialité.
4. Critiquer le résultat, corriger, documenter preuve, limites et prochaine tâche ; commit atomique et push branche si autorisé.
5. Recommencer sur la tâche suivante. Après deux échecs identiques, consigner le blocage et avancer ailleurs. Ne pas créer de boucle infinie ; limite par run 45 minutes ou quota inférieur, 0 EUR, arrêt propre et checkpoint. N'installer que les dépendances libres utiles et validées, pas de privilèges administrateur sans nécessité et accord.
## Organisation Hermes / Codex
Utiliser skills, Kanban, cron disponibles après inventaire. Trois chantiers : moteur GPU/qualité ; interface et presets ; intégrations/QA. Un responsable coordonne, évite les edits simultanés du même fichier, relit les diffs. Ne pas prétendre à des tâches programmées si elles n'existent pas. Tous les agents mettent à jour STATUS.md.
## Backlog
P0 : fixture synthétique et mesures ; moteur WebGL2 + fallback Canvas ; chaîne non destructive, presets versionnés, preview A/B ; webcam/fichier/écran avec consentement ; export image/vidéo ; raccord à LIVE et EDIT sans double ouverture caméra. P1 : CRT (masque phosphore, courbure, blooming), VHS (chroma, tracking, bruit temporel), glitch, feedback, pixel sort, keyframes, blend modes et masque ; OBS source/filtre avec auth, FFmpeg export A/V, annulation jobs. P2 : graphe de nodes, LFO/audio-réactivité, XR/3D, CLI/MCP limité à commandes typées, presets de Cronos. P3 : packaging portable, raccourci de bureau, découverte locale, recovery.
## Critères de fini
Démarrage un clic, sources locales, réglages visibles en temps réel, zéro faux boutons, arrêt/libération des flux, sauvegarde/restauration, erreurs explicites, export relisible, aucune donnée secrète/privée diffusée sans opt-in. Mesurer 720p30 cible sur GPU de référence ; si non atteint, proposer qualité adaptative et rapport. Tests unitaires + navigateur + Windows/OBS réels avant déclarer compatible. Les tests simulés ne valent pas validation matérielle.
## Sécurité
Pas de collecte cachée, pas de secrets dans git, localhost par défaut, pas d'exécution arbitraire via MCP ni lecture hors dossier autorisé. Gérer licences, hashes, permissions et quotas. Pas de téléchargement massif de modèles inutiles.
