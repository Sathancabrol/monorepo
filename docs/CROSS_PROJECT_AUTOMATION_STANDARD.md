# Standard d'automatisation interprojets

## Objectif

Réduire au minimum les interventions de l'utilisateur sur les opérations répétitives de construction logicielle. L'utilisateur fixe les objectifs, les priorités métier et les décisions à risque; l'agent effectue le travail de fond autorisé, avec preuves et reprise persistante.

## Règle d'entrée de session

Au début de toute session de travail sur l'écosystème :

1. Lire le handoff du dépôt actif et les consignes applicables (AGENTS.md, CLAUDE.md, GEMINI.md, CONTRIBUTING.md, consignes locales et workflows).
2. Récupérer les tâches ouvertes, décisions, mémoire de projet et audits précédents pertinents. Réutiliser une conclusion seulement si sa source, son SHA et sa date sont encore valides.
3. Examiner les changements récents, les branches pertinentes, les PR/issues et les résultats CI accessibles.
4. Déduire les inconnues exactes et chercher les preuves dans les fichiers/branches avant de poser une question à l'utilisateur.
5. Ne poser une question que si une décision ou une information indispensable ne peut pas être obtenue par les sources accessibles, ou si une action exige une approbation.

Cette règle décrit le comportement attendu des agents et des runners; elle ne signifie pas qu'un processus s'exécute entre les conversations sans runner planifié.

## Cycle commun

RECALL → DISCOVER → PLAN → EXECUTE → VERIFY → DELIVER → HANDOFF

- **RECALL** : état validé, mémoire, handoff, tâches ouvertes, règles locales.
- **DISCOVER** : dépôts, branches paginées, SHAs, fichiers de règles, documents de conception, tests, workflows, PR/issues et sources externes utiles.
- **PLAN** : une unité de travail prioritaire, dépendances, risques, permissions, critères d'acceptation.
- **EXECUTE** : modifications isolées, diff lisible, conservation des travaux existants.
- **VERIFY** : tests/builds/preview réellement exécutés, SHA exact, commande, environnement, code de sortie, durée, logs et artefacts.
- **DELIVER** : livrable utilisable, instructions courtes, liens exacts et limitations connues.
- **HANDOFF** : mise à jour du handoff, journal append-only, file de tâches, roadmap, KPI et prochaine action.

Chaque cycle doit se terminer par une preuve et une prochaine action explicite. Une tâche ne passe à DONE que si ses critères d'acceptation sont vérifiés. Une branche créée, un fichier écrit ou une PR ouverte ne sont pas une validation.

## Inventaire de règles à rechercher

À l'échelle de chaque dépôt et des branches pertinentes, rechercher notamment :

- AGENTS.md, CLAUDE.md, GEMINI.md, COPILOT_INSTRUCTIONS.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md;
- README*, CONTRIBUTING*, DEVELOPMENT*, ARCHITECTURE*, DECISIONS*, ADR/*, docs/*;
- .github/workflows/*, templates d'issues/PR, hooks Git, Makefile, scripts de build/test/release;
- configurations de formatage, lint, typecheck, sécurité, dépendances, licences, CI/CD et publication;
- fichiers de handoff, mémoire, journal, roadmap, critères d'acceptation, politiques de sécurité et de données;
- instructions imbriquées qui s'appliquent uniquement à un sous-répertoire.

Ne pas supposer que les consignes d'une branche ou d'un dépôt s'appliquent partout. Enregistrer leur portée, leur source, la branche/SHA, la date et les conflits éventuels.

## Résolution des contradictions

Ordre par défaut, à vérifier selon la portée réelle :

1. exigences de sécurité et permissions de la plateforme;
2. demande explicite la plus récente de l'utilisateur pour le besoin concerné;
3. instructions locales applicables au chemin modifié;
4. contrat d'architecture et décisions acceptées du projet;
5. standards transversaux du monorepo;
6. conventions usuelles.

Une consigne locale plus stricte peut rester applicable. Ne pas effacer un conflit en choisissant silencieusement une règle : consigner les deux sources, leur portée, la résolution proposée et l'éventuelle décision humaine requise.

## Automatisations obligatoires à privilégier

- découverte paginée des dépôts, branches, commits, PR/issues et workflows;
- détection de nouveaux SHAs, branches oubliées, preuves périmées et divergences;
- inventaire des règles, conflits, commandes de test et prérequis par projet;
- file de tâches persistante avec identifiants stables, dépendances, checkpoints et reprise;
- tests de syntaxe/configuration, lint, types, tests unitaires/intégration et build selon la stack;
- contrôle des licences, secrets accidentels, dépendances vulnérables et artefacts générés;
- génération des livrables, rapports, changelog, instructions d'installation et manifestes;
- vérification des chemins/liens/livrables et somme de contrôle si utile;
- mise à jour du handoff, journal, roadmap et dashboard à partir des résultats réels;
- détection de régression et relance ciblée après échec, avec limite de tentatives et arrêt sur risque.

L'automatisation doit réutiliser les outils déjà présents dans Nexus OS, Research Engine, HCSM et les dépôts concernés après audit de leur fonctionnement. Ne pas créer un deuxième système parallèle si une brique existante est adaptée et vérifiée.

## Niveaux d'autonomie

### Sans approbation, une fois l'accès configuré

Lecture, recherche, inventaire, comparaison, création de rapports, préparation de tâches, tests isolés, modifications sur branche dédiée et livrables internes réversibles.

### Approbation obligatoire par défaut

Fusion dans la branche principale, déploiement/publication externe, suppression/archivage, changements de permissions, accès ou transfert de secrets/données privées, installation d'intégrations, dépenses, modifications destructrices et toute action irréversible.

## Format minimal d'une preuve

Chaque résultat important conserve : objectif, dépôt, branche, SHA, chemin, date, commande/action, environnement, résultat, source/log/artefact, niveau de confiance, limites, prochaine action et critère d'acceptation associé.

États distincts : NOT_INSPECTED, DISCOVERED, CONTENT_REVIEWED, TEST_NOT_RUN, TEST_FAILED, TEST_PASSED, BUILD_PASSED, PREVIEW_VERIFIED, ACCEPTED. Ne jamais transformer une étape en une autre par inférence.

## Livrable standard

Quand une tâche produit un livrable, fournir automatiquement autant que possible :

- l'artefact exact et un lien vérifié;
- une procédure d'utilisation/installation adaptée à Windows si c'est la cible;
- les dépendances et prérequis;
- le résultat des tests et ce qui n'a pas été testé;
- les changements et fichiers concernés;
- les risques, limites, approbations restantes et prochaine action;
- une option de reprise sans recommencer l'audit.

## Règle de fermeture

Aucune affirmation « terminé », « fonctionnel », « complet » ou « prêt » sans critères d'acceptation explicites et preuves proportionnées. Si une étape ne peut pas être automatisée avec les permissions ou outils disponibles, l'indiquer comme blocage précis et préparer la plus petite action requise de l'utilisateur.
