# Genjutsu-OSS — proposition d’intégration Nexus / Monorepo

**Statut :** proposition documentée; aucune installation ni exécution du projet tiers.
**Date de revue des sources :** 2026-10-10.
**Source :** https://github.com/Tschuki/genjutsu-oss

## Décision

Enregistrer Genjutsu-OSS comme candidat de recherche, pas comme dépendance validée ou moteur de production. Réutiliser en priorité ses idées d’architecture — contrats de données validés, providers interchangeables, compilation de consignes et pipeline explicite — plutôt que de copier son code immédiatement.

## Ce qui est vérifié dans le dépôt public

- Le dépôt est un projet Python destiné à s’intégrer à ComfyUI; le README indique Python 3.10+.
- Le dépôt source déclare une licence Apache-2.0.
- Il contient des contrats typés pour les paquets vidéo, références, contrôles, masques et résultats, ainsi que des interfaces de providers.
- Des nœuds ComfyUI existent pour charger une vidéo, analyser sommairement la scène, construire un paquet de contrôle et compiler un prompt.
- Le chemin de test CPU est explicitement simulé : il copie la vidéo encodée source. Il ne prouve pas que la vidéo a été transformée.
- Le README indique que les vrais backends de génération, segmentation SAM2, pose, profondeur, optical flow, stabilisation temporelle, composition avancée et export de production ne sont pas encore implémentés.
- Le registre de licences tiers du projet signale comme non vérifiées les licences des poids de modèles et plusieurs dépendances futures. La licence Apache du code ne suffit donc pas à autoriser l’usage ou la redistribution de tous les modèles.

Sources : README, LICENSE, pyproject.toml et THIRD_PARTY_LICENSES.md du dépôt public. Cette revue de sources n’est pas un test local.

## Fonctionnalités pertinentes pour Nexus

1. **Contrats de données indépendants des modèles** : un objet VideoJob référence les sources, les timecodes, les médias, les transformations demandées, les contraintes à préserver et le résultat attendu.
2. **Pipeline en étapes** : import → analyse → plan → aperçu/draft → contrôle qualité → export. Chaque étape produit un artefact versionné et un statut.
3. **Providers interchangeables** : analyse vidéo, segmentation, profondeur, pose, génération, composition, restauration et export sont des interfaces distinctes. Un backend cloud ne doit pas être imposé au cœur du système.
4. **ComfyUI comme outil spécialisé** : Nexus peut préparer ou lancer des workflows ComfyUI après confirmation, sans confondre l’interface ComfyUI avec l’orchestrateur général.
5. **Reprise et traçabilité** : conserver identifiants de tâche, paramètres, versions des modèles, coûts estimés/réels, erreurs et chemins des artefacts afin de relancer une étape sans refaire tout le travail.
6. **Validation humaine** : demander approbation avant génération coûteuse, publication, écrasement ou envoi de médias à un service externe.

## Architecture cible

Nexus UI / demande utilisateur
→ Agent Orchestrateur : plan, permissions, budget, validations
→ Media Workflow Service : état des jobs, étapes, reprise, journaux
→ Contrats média versionnés : VideoJob / ControlPackage / ResultPackage
→ Adaptateurs : FFmpeg / OpenCV / ComfyUI / Blender / Unreal / API cloud optionnelle
→ Artefacts locaux + métadonnées + rapport qualité

Les modules créatifs sont des capacités appelables par l’orchestrateur; ils ne deviennent pas chacun un orchestrateur autonome. Le catalogue d’outils du monorepo reste la source de provenance, compatibilité, licence et statut de vérification.

## Intégration dans le monorepo

- Catalogue : ajouter genjutsu-oss à data/tool_registry/creative-tools.json avec catalogue_status=research_only, licence source déclarée Apache-2.0, maturité expérimentale et statut de test local non effectué.
- Architecture : conserver le registre et son validateur existants; ajouter ce document comme fiche d’intégration spécialisée.
- API future : exposer les jobs vidéo au travers de l’API locale existante, après vérification de son contrat et de ses tests. Ne pas créer de service en arrière-plan supplémentaire sans besoin mesuré.
- UI future : écran « Atelier média » avec dépôt des sources, choix du workflow, aperçu des étapes, comparaison source/résultat, journal, budget et export.
- Stockage : garder les médias et secrets en local par défaut. Tout transfert cloud doit être explicite, avec destination et durée de conservation indiquées.
- Interopérabilité : Blender et Unreal consomment des exports et métadonnées normalisés; aucune compatibilité directe n’est présumée.

## Garde-fous techniques

- Ne jamais exécuter les commandes d’installation trouvées dans un dépôt sans revue et confirmation.
- Ne pas télécharger automatiquement des poids de modèles.
- Distinguer « déclaré par le mainteneur », « confirmé sur source », « testé localement » et « validé en production ».
- Prévoir limites de taille/durée, espace disque, timeout, annulation, reprise, empreintes de fichiers et nettoyage des fichiers temporaires.
- Conserver les pistes audio originales séparément et vérifier la synchronisation après export.
- Avant tout déploiement, vérifier la licence de chaque modèle/poids, les dépendances transitives et les conditions commerciales.

## Compatibilité matérielle et stratégie de calcul

Ne pas promettre que la génération vidéo moderne tourne correctement sur un GPU local de 6 Go de VRAM. Le test simulé peut servir à valider l’intégration logicielle, mais pas les performances de génération. À terme, proposer trois modes explicites : simulation de pipeline, traitement local léger, backend distant optionnel avec estimation de coût et consentement.

## Critères d’acceptation avant adoption

- Le catalogue se valide hors ligne et aucune installation n’est déclenchée.
- Le workflow simulé est étiqueté « simulation » et ne prétend pas transformer la vidéo.
- Un job échoué peut être inspecté et relancé à partir de la dernière étape valide.
- Les fichiers source ne sont jamais écrasés.
- Le rapport d’exécution liste les outils, versions, coûts, erreurs et artefacts.
- Un test local réel valide séparément chaque backend activé.
- Les licences des poids et les contraintes de redistribution sont documentées avant tout usage commercial.

## Prochaines étapes proposées

1. Enregistrer la fiche dans le catalogue de recherche.
2. Faire passer le dépôt tiers par un audit de dépendances et de licences.
3. Implémenter un contrat de job média minimal dans le monorepo, sans dépendance à Genjutsu-OSS.
4. Construire une preuve de concept avec fichiers locaux et provider simulé.
5. Ajouter ComfyUI comme adaptateur seulement après test local et validation des permissions.
