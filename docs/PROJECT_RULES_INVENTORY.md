# Inventaire des règles projet — état initial

> Statut : inventaire partiel vérifié sur les branches par défaut accessibles au 2026-10-11. Ce document ne remplace pas les consignes locales. Un dépôt ou une branche non inspecté(e) n'est pas déclaré(e) sans règles.

## Règles transversales

Source canonique : [CROSS_PROJECT_AUTOMATION_STANDARD.md](CROSS_PROJECT_AUTOMATION_STANDARD.md), [AGENTS.md](../AGENTS.md), [AGENT_HANDOFF.md](../AGENT_HANDOFF.md).

- Lire le handoff, les instructions applicables et les audits pertinents au début d'une session.
- Rechercher dans la mémoire, les fichiers, branches, PR/issues et CI avant de demander à l'utilisateur de répéter une information.
- Conserver les sources, dates, SHA, incertitudes et preuves; ne pas déclarer une fonctionnalité opérationnelle sur la seule présence de code/documentation.
- Tester avant de conclure; consigner commande, environnement, SHA testé et résultat.
- Préserver le travail existant; ne pas fusionner, déployer, supprimer, publier à l'extérieur ou engager de dépense sans autorisation.
- Mettre à jour le handoff et le journal à la fin de chaque unité de travail.

## Règles confirmées par projet

| Projet | Source vérifiée | Règles / contraintes observées | Limite de l'audit |
|---|---|---|---|
| Watchtower | AGENTS.md, blob SHA 260d560843a27f0cb16fa08cebfbf11035e303ca ; [fichier](https://github.com/Sathancabrol/watchtower/blob/260d560843a27f0cb16fa08cebfbf11035e303ca/AGENTS.md) | **Ne pas éditer** AGENTS.md, REFERENCE.md ni les registres générés : modifier audit/reference/generate-reference.py, puis régénérer. Pas de fonctionnalité visant une personne physique. Rejeter les licences absentes, NOASSERTION, Other ou fair-code sauf justification. Zéro clé par défaut; .env protégé et jamais commité; pas de binding 0.0.0.0; afficher tout repli cloud. Toute nouvelle intégration doit avoir rôle, tier, prix, licence, URL, étapes d'installation et vérificateur doctor.py. Journaliser les flux publics avant d'afficher la couche; un événement est un alignement temporel, pas une assertion ni une accusation. Lancer doctor.py avant/après installation; vérifier prix/quotas à la date d'écriture. | Le fichier indique qu'il est généré le 2026-09-07; autres règles peuvent se trouver dans REFERENCE.md, le générateur, les workflows et branches non encore lues. |
| Research Engine | README.md, blob SHA 35119628002c2cb9d1bec6fb0b49208229746726 ; [fichier](https://github.com/Sathancabrol/reaserch-engine/blob/35119628002c2cb9d1bec6fb0b49208229746726/README.md) | Local-first : inspecter d'abord les sources locales disponibles. Gates fixes de qualité scientifique, stratégie adaptative selon le type de question, lacunes, contradictions et gain d'information attendu. La provenance, la vérification et la logique d'arrêt appartiennent au moteur, pas seulement au LLM. Les conclusions doivent être traçables; l'incertitude et les preuves insuffisantes restent visibles. Cycle décrit : recherche → preuves → affirmations → contradictions → synthèse → vérification → suffisance → prochaine action. | README seulement; code, tests, licences, CI et autres règles à auditer avant réutilisation. |
| HCSM | README.md, blob SHA 16ef5c60e4b135a56d2c677e6c8c9531a657a941 ; [fichier](https://github.com/Sathancabrol/HCSM/blob/16ef5c60e4b135a56d2c677e6c8c9531a657a941/README.md) | Le dépôt se décrit comme un cadre scientifique de représentation multidimensionnelle, contextualisée, temporelle et fondée sur les preuves. HCSM est le modèle scientifique; Cognition Hub l'instanciation computationnelle; Cognitorium l'architecture globale. Ne pas réduire le modèle à un score cognitif unique ou à un « QI 2.0 ». Les revendications de nouveauté doivent rester réfutables et ne pas être présentées comme des faits sans preuve. | README partiellement inspecté; lire les sections complètes, spécifications, validations, sources et décisions. |
| État de l'art psychologie | README.md, blob SHA 36f02ecc214ca43a7da64cd9d39e52e90cb43d53 ; [fichier](https://github.com/Sathancabrol/ETAT-DE-LART-PSYCHOLOGIE/blob/36f02ecc214ca43a7da64cd9d39e52e90cb43d53/README.md) | Employer la formulation « cartographie critique préliminaire » plutôt qu'une promesse d'exhaustivité. Protocole transparent, PRISMA 2020, évaluation des biais, programme de recherche testable. S'appuyer sur les stratégies de recherche reproductibles, le flux PRISMA, le template de données et le guide de remplissage IA référencés par le README. | README seulement; le protocole, le guide IA, les critères de qualité et la base doivent être examinés en détail. |
| COGNITORIUM | README.md, blob SHA c431659a00f2945e12c76c6010d363e6e490a958 ; [fichier](https://github.com/Sathancabrol/COGNITORIUM/blob/c431659a00f2945e12c76c6010d363e6e490a958/README.md) | Le README désigne docs/ comme lieu de la vision, de la gouvernance, des audits, de l'architecture, des agents et du journal de décisions. Le PoC Learning Engine part de situations concrètes, propose plusieurs choix, explique les conséquences, nomme les concepts associés, relie les concepts et met à jour un graphe de compétences/concepts. | Lire la constitution, les décisions, l'architecture, les consignes d'agents et les tests avant de modifier le module. |
| Language-decoder | README.md, blob SHA ff27dad48051736ea9d17fde2d7613c1b6d4ddfb ; [fichier](https://github.com/Sathancabrol/Language-decoder/blob/ff27dad48051736ea9d17fde2d7613c1b6d4ddfb/README.md) | Le README de la branche par défaut ne contient que le titre du projet; ne pas conclure que le moteur est absent sans auditer les branches et l'historique. | À traiter en priorité dans la réconciliation des branches, car le README principal est manifestement insuffisant comme point d'entrée. |
| proto-cognitorium | AGENTS.md, blob SHA 6fb4eccc481cf587d9fb035ffa64eb32579553d0, et AGENT_HANDOFF.md, blob SHA 0581015595393d5c2d7491480a7245e44dd11114, branche chore/agent-handoff-2026-10-11 | Lire le handoff, les instructions locales et les audits; vérifier l'état réel avant de conclure; travailler sur une tâche limitée et une branche dédiée; préserver le travail; noter commandes/tests/résultats; mettre à jour le handoff et le journal append-only; ne jamais prétendre qu'un test a réussi s'il n'a pas été exécuté; pas de fusion/déploiement/suppression/dépense sans autorisation. | README.md n'a pas été trouvé sur main. Le code, les autres branches et les règles métier restent à auditer. |
| animation-chronos | AGENTS.md, blob SHA 6fb4eccc481cf587d9fb035ffa64eb32579553d0, et AGENT_HANDOFF.md, blob SHA 82d12159a319ab27f61de9f8b9e7b98adb2542e4, branche chore/agent-handoff-2026-10-11 | Même contrat agent : lire le handoff, les consignes locales, les audits et l'état réel; examiner manifests, interface et commits; préserver le travail; vérifier avant de conclure; actualiser le handoff et le journal; pas d'action irréversible sans autorisation. Le handoff précise que le périmètre du projet est à confirmer. | README.md n'a pas été trouvé sur main; déterminer la fonction réelle du dépôt à partir du code et des branches.

## Accès ou consignes racine non trouvés

Les requêtes directes sur la branche par défaut n'ont pas trouvé AGENTS.md dans plusieurs dépôts. Des consignes existent cependant sur des branches non principales : proto-cognitorium et animation-chronos possèdent toutes deux AGENTS.md et AGENT_HANDOFF.md sur chore/agent-handoff-2026-10-11. Le scanner doit donc inspecter les branches, pas seulement main.

- proto-cognitorium : README.md non trouvé sur main; consignes agent trouvées sur la branche de handoff.
- animation-chronos : README.md non trouvé sur main; consignes agent trouvées sur la branche de handoff.
- COGNITORIUM, HCSM, ETAT-DE-LART-PSYCHOLOGIE, reaserch-engine, Language-decoder : aucun AGENTS.md racine trouvé dans la branche par défaut via la requête directe. Inspecter les autres noms de fichiers de règles et les instructions imbriquées.
- Watchtower possède un AGENTS.md généré : toute mise à jour doit respecter son mécanisme de génération, pas le remplacer par le standard global.

## Système « JEV »

Aucune occurrence exploitable de « JEV » n'a été identifiée par les recherches GitHub effectuées sur les dépôts configurés. Ne pas assimiler ce nom à Nexus OS, HCSM ou à un autre projet sans preuve. Il reste à identifier par son URL, son nom exact ou son emplacement.

## Prochaine revue à automatiser

1. Énumérer toutes les branches paginées et les SHAs de chaque dépôt configuré.
2. Rechercher les fichiers de règles, scripts de génération, tests, workflows, handoffs, mémoires, roadmaps, décisions et politiques.
3. Lire les contenus des fichiers pertinents sur les branches prioritaires et comparer avec la branche par défaut.
4. Construire un registre machine-readable : projet, règle, source, SHA, portée, état, conflit, dépendance, test d'acceptation, date de révision.
5. Détecter automatiquement les fichiers de règles modifiés et marquer les constats dépendants comme périmés.
6. Garder une approbation humaine pour les arbitrages métier, les conflits qui changent le comportement produit et les actions irréversibles.
