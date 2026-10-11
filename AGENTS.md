# Instructions pour les agents IA

Avant toute tâche dans ce dépôt :

1. Lire `AGENT_HANDOFF.md` à la racine. C'est le point de reprise : dernier état connu, dernière mise à jour, audit/test vérifié ou non, besoins et prochaine action.
2. Lire `AGENTS.md` (ce fichier), le `README.md`, `docs/CROSS_PROJECT_AUTOMATION_STANDARD.md`, les consignes locales et les audits/décisions pertinents.
3. Récupérer les informations pertinentes de mémoire, handoff, tâches ouvertes et audits antérieurs. Vérifier que la source, le SHA et la date sont encore valides; ne pas repartir de zéro si la preuve est toujours valable.
4. Vérifier l'état réel du dépôt, les changements récents, les branches pertinentes, les PR/issues et la demande utilisateur la plus récente. Ne pas refaire un audit déjà valide ni supposer qu'une fonction marche parce qu'elle est documentée.
5. Avant de poser une question, rechercher les réponses dans les fichiers, branches, rapports, issues/PR et sources accessibles. Ne demander que les décisions ou informations réellement impossibles à récupérer.
6. Choisir une tâche utile et prioritaire, respecter les dépendances et le périmètre, préserver les travaux existants et travailler sur une branche dédiée.
7. Exécuter les vérifications pertinentes. Consigner les commandes, le SHA testé, l'environnement, les résultats et les limites. Ne jamais déclarer un test ou audit réussi s'il n'a pas été exécuté.
8. Préparer les livrables reproductibles et vérifier leurs chemins/liens. À la fin, mettre à jour `AGENT_HANDOFF.md`, le journal append-only, la file de tâches, les rapports/KPI et la prochaine action.
9. Ne pas fusionner, déployer, supprimer, publier à l'extérieur, accéder à des secrets, changer des permissions ou dépenser sans autorisation explicite.

En cas de contradiction, conserver les faits et incertitudes visibles. Appliquer les règles de sécurité et les consignes locales pertinentes, puis la demande utilisateur la plus récente et les décisions acceptées du projet. Ne jamais résoudre silencieusement un conflit entre deux documents.

Cycle obligatoire : RECALL → DISCOVER → PLAN → EXECUTE → VERIFY → DELIVER → HANDOFF.

La présence d'un fichier, d'une branche, d'une PR ou d'un README ne prouve pas qu'une fonctionnalité est complète ou opérationnelle. Distinguer découverte, revue de contenu, test exécuté, test réussi, build, preview et acceptation humaine.
