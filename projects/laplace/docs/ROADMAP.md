# Feuille de route LAPLACE

Les fonctionnalités visées et leurs critères d’acceptation sont détaillés dans [FEATURES.md](FEATURES.md). Les choix du propriétaire sont : profil général en premier; audio en fichier puis salon vocal live; photo/selfie envoyée puis capture locale ponctuelle; analyse et génération média, local d’abord et API externe activée explicitement par capacité. L’analyse d’image jointe est implémentée; les documents, la génération média, l’audio et la voix restent à développer. Une [veille comparative sur les modèles vision, webcam et IRMf](RECHERCHE-MODELES-VISION-IRMf.md) documente les candidats et leurs limites sans intégrer de poids ni modifier le périmètre caméra.

Le catalogue de frameworks pour un futur studio d’agents Carré d’As est dans [`docs/AGENT-HUB-RESEARCH.md`](../../../docs/AGENT-HUB-RESEARCH.md).

## v0.1 — socle Discord texte (implémenté)

- Bot Discord officiel, slash commands, allowlist guild/salon, sans Message Content Intent.
- `/parler` avec Ollama local ou endpoint compatible optionnel.
- Archive brute configurable; souvenirs privés par utilisateur, souvenirs partagés isolés par serveur, provenance, confiance, correction versionnée, recherche plein texte, export et effacement.
- Réponses privées par défaut et documentation d’installation.

## v0.2 — mémoire et profil général (en cours)

- **Socle mémoire — implémenté :** espaces privés et partagés isolés, provenance, confiance, corrections versionnées, recherche plein texte, export et effacement.
- **À poursuivre :** rendre les sources plus faciles à inspecter et améliorer l’ergonomie des contrôles et de l’oubli.
- Mettre le profil général en configuration versionnée avec consignes et limites explicites.
- Recherche sémantique facultative, après choix d’un modèle local compatible; conserver une recherche textuelle de repli et des scopes séparés.
- Ne pas partager implicitement de souvenirs entre utilisateurs ou serveurs.

## v0.3 — analyse des fichiers (en cours)

- **Image jointe — implémentée :** `/analyser_image image question` accepte JPEG/PNG/WebP jusqu’à 8 Mio, si `VISION_MODEL` est configuré; la réponse est éphémère et l’image n’entre pas dans la mémoire ou l’archive.
- **Documents — à faire :** accepter uniquement les fichiers volontairement envoyés, extraire/OCR et répondre avec des références aux pages ou sections.
- Signaler les incertitudes, borner format/taille, traiter les fichiers temporaires sans conservation automatique.
- Externe uniquement après opt-in spécifique à la capacité.

## v0.4 — voix en fichiers (à faire)

- Recevoir un clip audio Discord, transcrire, puis répondre en texte.
- TTS à la demande en fichier audio privé; comparer la qualité française et la latence des moteurs locaux sur le PC cible.
- Pas de conservation automatique audio/transcription; tailles, durées et fréquences d’usage plafonnées.

## v0.5 — génération multimédia et temps réel (à concevoir)

- Générer image/audio/vidéo si un modèle local compatible est configuré; garder chaque capacité désactivée tant qu’elle n’est pas testée.
- Autoriser un fournisseur externe uniquement après activation opt-in de la capacité concernée et avertissement sur le transfert de données/coût.
- Prototyper séparément la vidéo jointe (images-clés/transcription) et les conversations en salon vocal Discord (latence, permissions, consentement, indicateur d’écoute et arrêt immédiat).

## v0.6 — compagnon caméra et actions locales (à concevoir)

- Le parcours selfie commence par une photo explicitement envoyée dans Discord; un bot standard ne peut pas activer la caméra du client.
- Ajouter une capture ponctuelle via compagnon local seulement avec installation explicite, indicateur de caméra actif et confirmation à chaque capture; aucun accès en arrière-plan.
- Ouvrir des actions navigateur avec Playwright isolé; contrôler fenêtres/fichiers uniquement par liste blanche, audit et confirmation avant mutation; aucun shell libre.
- Choisir le compagnon après confirmation de l’OS, du matériel et des capacités autorisées.

## Intégration Carré d’As (bloquée par l’absence du dépôt/API)

L’objectif est de faire de Carré d’As un studio propriétaire pour créer, configurer, tester, versionner, publier et gouverner les agents, en complément des parcours utilisateurs. Le code Carré d’As et son contrat d’intégration ne sont pas dans ce checkout. Voir [l’état et les prérequis](CARRE-DAS-INTEGRATION.md) ainsi que la [veille GitHub sur le hub d’agents](../../../docs/AGENT-HUB-RESEARCH.md). Aucune API n’est simulée.
