# OUTSIDER — Documentation de production assistée par IA

## Objet

Ce dossier centralise la conception, la recherche, les règles et les contrats nécessaires pour construire **Supernatural: Outsider** bloc par bloc avec des agents IA.

Principe directeur :

RAW → INTERPRÉTATION → SYSTÈME → GAMEPLAY → FEATURE → BLOC → BUILD → TEST → ITÉRATION

Les RAW ne sont jamais supprimées ni réécrites pour faire disparaître une idée.

## Cible

Produire une base de connaissances suffisamment structurée pour qu'un agent puisse :

1. comprendre l'intention du jeu ;
2. retrouver les règles concernées ;
3. rechercher une solution existante avant de recoder ;
4. construire un bloc isolé ;
5. l'intégrer au monde ;
6. tester visuellement et fonctionnellement ;
7. corriger ;
8. documenter le résultat ;
9. passer au bloc suivant.

## Arborescence

- 00_RAW — idées et décisions brutes conservées.
- 01_GAME_DESIGN — vision, gameplay, progression, narration, UX.
- 02_SYSTEMS — contrats d'implémentation des machines.
- 03_WORLD — monde, lieux, écologie, contenu procédural.
- 04_AI_BUILD — architecture des agents et boucle de construction.
- 05_REFERENCE_TECH — catalogue des outils, repos, méthodes et sources.
- 06_ROADMAP — roadmap et critères de sortie.
- 07_AUDIT — audits des repos existants.
- 08_BENCHMARK — benchmarks externes et références de conception.

## Repos étudiés

- Sathancabrol/monorepo — archive/carré d'as et base de consolidation.
- Sathancabrol/watchtower — OSINT, monitoring, cartographie, vue intelligence.
- Sathancabrol/COGNITORIUM — visualisation cognitive.
- Sathancabrol/proto-cognitorium — prototype applicatif.

Les autres projets cités dans les discussions sont traités comme sources conceptuelles tant qu'ils ne sont pas retrouvés dans GitHub connecté.

## Règle de production

Un agent ne doit pas recevoir « construis Outsider ». Il reçoit un **BLOCK_ID**, ses dépendances, ses contrats, ses références et ses tests.

Exemple :

BLOCK B001 = maison familiale cévenole.

L'agent doit être capable de trouver : architecture, dimensions, matériaux, interactions, collisions, navigation, indices, NPC sockets, éclairage, physique, performance et critères de validation.

## État

V0.1 — consolidation documentaire initiale.
