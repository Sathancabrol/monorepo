# Intégration Carré d'As — état et contrat à obtenir

## Intention produit clarifiée

Le 8 octobre 2026, le propriétaire a précisé que Carré d'As doit être **un hub d'agents IA pour lui**, en plus des fonctions offertes aux utilisateurs : créer/configurer, tester, versionner, publier et gouverner des agents, leurs modèles, leurs outils et leurs politiques. La veille des solutions et dépôts GitHub est dans [`docs/AGENT-HUB-RESEARCH.md`](../../../docs/AGENT-HUB-RESEARCH.md).

Cette précision clarifie l'objectif, mais ne donne pas encore accès au code Carré d'As ni à son contrat d'intégration. Une inspection du monorepo ne trouve toujours aucun projet, dossier, API ou documentation identifiés comme Carré d'As. L'implémentation native reste donc en attente; aucun endpoint n'est inventé et aucun cookie/session web n'est utilisé.

## Ce qui est prêt côté LAPLACE

LAPLACE est un bot Discord autonome en Python avec un fournisseur Ollama local par défaut, une option d'API compatible OpenAI, une mémoire SQLite privée/partagée séparée, et des contrôles de confidentialité. Son agent et son interface Discord sont actuellement dans le même module; le brancher proprement à Carré d'As demandera un adaptateur/API explicite, pas un accès direct à une base privée ou à une session web.

## Informations nécessaires pour relier les projets

Fournir le dépôt/chemin Carré d'As et, si possible, le travail de l'autre agent en cours, sans secret. Il faudra ensuite identifier :

- le framework/version, les routes et le modèle de données existants;
- le mode d'authentification et les rôles propriétaire/administrateur/utilisateur;
- si le studio ne sert qu'un propriétaire ou plusieurs espaces/clients — important pour l'isolation et les licences des composants;
- le contrat attendu pour enregistrer, configurer, tester et publier un agent (HTTP, paquet, plugin, événement, MCP ou autre);
- l'endroit où les clés des fournisseurs et les connexions d'outils sont stockées.

Une URL de dépôt/API publique suffit pour l'étude. Ne transmettre aucun token, cookie, clé API ou mot de passe.

## Direction recommandée

Traiter Carré d'As comme le **plan de contrôle** et l'interface d'administration; traiter LAPLACE comme un premier agent/canal possible. Garder distincts :

1. le profil d'agent déclaratif et versionné (instructions, fournisseur/modèle, outils autorisés, scopes mémoire, canaux, validations);
2. le runtime qui exécute l'agent;
3. les adaptateurs (Discord, web et éventuellement voix);
4. les outils avec permissions minimales et approbation humaine pour les écritures;
5. un compagnon local séparé pour navigateur/PC, sandboxé et autorisé explicitement.

Le catalogue, les candidats, les statuts d'activité et les réserves de licence sont détaillés dans la recherche d'écosystème. Aucun framework n'est retenu avant lecture du projet Carré d'As, comparaison avec l'autre travail en cours et revue de la licence.
