# AI BUILD ARCHITECTURE

## Principe

L'IA de production est une équipe d'agents spécialisés, pas un prompt monolithique.

## Boucle

INTENT → BLOCK SPEC → REFERENCE RETRIEVAL → PLAN → BUILD → CAPTURE → INSPECT → TEST → PATCH → VALIDATE → LOG

## Agents

### Orchestrator
Décompose le travail et respecte les dépendances.

### Research Agent
Cherche d'abord une solution existante : repo, plugin, dataset, procédure, documentation.

### World Builder
Construit terrain, bâtiments, végétation et espaces.

### Asset Agent
Crée ou adapte les assets.

### Physics Agent
Collisions, rigid bodies, destruction, véhicules, interactions.

### Gameplay Agent
Systèmes, Blueprints/C++, interactions.

### NPC Agent
Routines, perception, mémoire, relations.

### Investigation Agent
Indices, provenance, graphes de connaissances.

### QA Agent
Tests runtime, screenshots, logs, overlaps, navigation, performance.

### Lore Agent
Vérifie cohérence canon / original / hypothèse.

### Performance Agent
Profiling, LOD, budgets, streaming.

## Documentation agent

Chaque agent doit lire :
1. projet ;
2. BLOCK_ID ;
3. contrat système ;
4. dépendances ;
5. références ;
6. critères d'acceptation.

Il ne doit pas charger toute la base si une sous-partie suffit.

## Règle « search before build »

Avant de coder :
1. rechercher dans le catalogue local ;
2. rechercher dans GitHub ;
3. rechercher les docs officielles ;
4. vérifier licence ;
5. vérifier compatibilité moteur ;
6. vérifier hardware ;
7. comparer avec alternatives ;
8. seulement ensuite implémenter.

## Boucle visuelle

Pour les blocs 3D :
BUILD → CAPTURE → ANALYSE → PATCH.

Trois vues minimales :
top-down, eye-level, player-eye.

## Mémoire

Chaque bloc produit :
- build log ;
- décisions ;
- erreurs ;
- tests ;
- références utilisées ;
- dépendances ;
- hash/version ;
- captures de validation.

## Sécurité de production

- pas de mutation concurrente du même éditeur ;
- sauvegarde avant modifications destructives ;
- petits commits ;
- changements réversibles ;
- tests avant expansion.

## Critère de succès

Un agent qui reçoit B001 doit pouvoir produire un résultat reproductible sans connaître oralement toute la conversation.
