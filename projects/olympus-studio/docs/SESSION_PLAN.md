# OLYMPUS Studio — plan d'itérations vers une version complète

**Mis à jour : 2026-11-12.** Dossier unique `projects/olympus-studio/`, branche `feat/olympus-studio-20261112`, PR #16 (brouillon). Aucun merge `main` et aucune modification des projets voisins par défaut.

## Définition de « terminé »

Le projet n'est pas terminé tant qu'on ne peut pas, depuis **une seule interface**, créer un projet, enregistrer une scène et des pistes audio/vidéo synchronisées, brancher OBS, analyser ou enrichir une réunion (transcription/traduction), piloter un avatar XR, générer au moins une séquence via un modèle **gratuit/local**, monter les médias et exporter une vidéo finale; les données doivent survivre à un redémarrage, les traitements être isolés, les licences vérifiées, et les tests Windows 10 (GTX 1060 et/ou GTX 1650) documentés.

Les fonctionnalités très coûteuses (génération temps réel photoréaliste, reconstruction 3D dense) restent options matérielles dans le périmètre long terme, mais **la dégradation de mode** doit être testée.

## Cadence et automatisation

- Lancer une **itération de travail** à chaque session agent disponible : consulter STATUS, HANDOFF, PR #16 et tickets #11 à #15 ; sélectionner une tâche ; implémenter ; ajouter des tests ; vérifier GitHub Actions ; documenter la preuve ; mettre à jour les tickets ; conserver le travail sur la branche.
- Les **tests GitHub Actions** s'exécutent déjà automatiquement aux pushes sur `feat/olympus-studio-20261112` et sur PR. Une exécution CI n'est **pas** un agent qui écrit du nouveau code.
- **Tâche ChatGPT activée le 12/11/2026** : `OLYMPUS Studio — développement` (`6af632ef3df88191a7ef46e372054ac4`), reprise quotidienne à **02:00 Europe/Paris**. Une exécution immédiate a été déclenchée à la demande de l'utilisateur le 12/11.
- Une tâche planifiée exécute des sessions **bornées**; pas de programmation ou génération garantie en continu. Accès GitHub et qualité CI à revérifier à chaque passage.

## Ordre de travail, critères et preuves

| Séquence | Livrable | Critères d'acceptation | Dépendances |
|---|---|---|---|
| S01 — consolidation | Coffre IndexedDB, export portable, migration du prototype v0.3 | Importer image/vidéo, fermer/recharger, rouvrir projet, retrouver les médias; export/import portable sous 45 Mo; tests Node et Chromium | Partiellement codé; test navigateur réel et quota à faire |
| S02 — LIVE fiable | OBS WebSocket, commandes scènes/sources/REC, monitoring, capture Windows | Connexion réelle OBS v5, scénario mauvais mot de passe, 30 min stable, absence de fuite des notes privées | OBS Windows et autorisation micro/écran |
| S03 — Audio/Meeting | Sélection des sources audio, sherpa-onnx/WhisperLiveKit, SRT, traduction, diarisation | Un fichier test FR et EN transcrit et exporté; corriger les sous-titres; distinguer incertitude et identités | Modèles ASR légers libres |
| S04 — Éditeur | Timeline de clips, coupes, trims, transitions, mixage, rendu de fichier, annulation | Import vidéo témoin, coupe, réordonne, sauvegarde/recharge, export A/V synchronisé | Benchmark FreeCut/OpenReelio et choix ADR |
| S05 — XR & avatar | Events X-Ray horodatés, tracker gestes, Three-VRM et rendu 3D | Webcam → avatar/overlay animé → OBS → export ; test « claquement de doigts » | Contrat événements X-Ray, matériel test |
| S06 — IA générative | File ComfyUI/WanGP, modèle gratuit, progression et import médias | 1 job réel, échec/reprise, artefact importé, travail LIVE prioritaire | ComfyUI et modèle compatible VRAM |
| S07 — Spatial | Vidéo Android → tracking / COLMAP, profondeur estimée, Watchtower/Cesium | Une scène test construite et enregistrée; séparer précision mesurée/estimée | Accès vidéos, pas besoin de LiDAR |
| S08 — Cinéma/graphics | Caméras, titres, diagrammes, animations et automatisations Chronos | Storyboard → scène animée → export; actions agents journalisées | Moteur de scènes stabilisé |
| S09 — Livraison | Installateur Windows, détection existant, sauvegardes, licences, tests de régression | Installation machine vierge, hors ligne hors setup, tests E2E et manuel, package versionné | Tests réels et audit sécurité/licences |

## Fonctionnement de chaque session

1. **Lire** `docs/HANDOFF.md`, `docs/STATUS.md`, `docs/SESSION_PLAN.md` et PR #16 ; inspecter les derniers échecs CI.
2. **Choisir une seule tranche verticale** testable de 1 à 3 fonctions complémentaires, et **une nouveauté visible par version** (pas seulement des refactorings).
3. **Implémenter** sur la branche isolée, en préservant le mode local sans cloud/paywall ; ne jamais envoyer une clé/API privée au dépôt.
4. **Ajouter des tests** (syntaxiques, API, unitaires, E2E si navigateur disponible), confirmer le workflow GitHub Actions après le dernier commit.
5. **Tracer** fonctionnalité annoncée vs codée vs testée vs validée Windows ; documenter la provenance des modules tiers/licences.
6. **Transmettre** les bloqueurs matériels uniquement quand un essai ne peut pas avancer sans l'utilisateur ; ne pas demander une nouvelle installation par réflexe.
7. **Conserver l'état** dans les tickets #11-#15 et docs/HANDOFF ; si CI en échec, fixer avant d'annoncer réussite.

## Ressources déjà disponibles

- Repo : https://github.com/Sathancabrol/monorepo/tree/feat/olympus-studio-20261112/projects/olympus-studio
- PR : https://github.com/Sathancabrol/monorepo/pull/16
- CI : https://github.com/Sathancabrol/monorepo/actions/workflows/olympus-studio-ci.yml
- X-Ray et Watchtower : bibliothèques **externes** ; lire les contrats et preuves avant toute attribution d'une fonction « intégrée ».
- Archive v0.3 indépendante dans la conversation `OLYMPUS_STUDIO_reprise_2026-11-12.zip`, non fusionnée.

## Session immédiate — v0.2.3, 12 novembre au soir
- S04 : édition vidéo avec réglages IN/OUT et découpage au curseur sur la timeline globale (sans mutation des fichiers sources).
- Fonctions pures `trimVideoClip`, `splitVideoClip`, `splitStoryboardAt` testées, sérialisation JSON stable.
- Preuve : https://github.com/Sathancabrol/monorepo/actions/runs/43316401111 — **29/29 tests réussis** sur Node/Ubuntu.
- Critère S04 **partiel** : export vidéo sans audio, durée source non contraignante, validation Chromium/Windows requise.
