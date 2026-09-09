---
name: code-implementation
description: Écrire du code qui tourne — lire le contexte réel avant la première ligne.
triggers: [code, implémente, fonction, bug, refactor, script, api, python, javascript]
tags: [dev, code, qualité]
tools: [read_file, list_dir, write_file, shell]
license: MIT
---
# Implémentation

## Avant d'écrire
1. `list_dir` sur le dossier concerné, `read_file` sur les 2-3 fichiers touchés.
2. Repère la convention existante (nommage, gestion d'erreur, style d'import) et suis-la.
3. Énonce en une phrase le contrat : entrée, sortie, cas d'erreur.

## Pendant
4. Un changement = une responsabilité. Pas de refactor opportuniste dans un correctif.
5. Gère les erreurs aux frontières ; ne jamais avaler une exception sans la tracer.
6. Pas de dépendance nouvelle sans justification explicite.

## Après
7. Donne la commande qui vérifie le changement.
8. Liste : fichiers touchés, comportement modifié, risque résiduel.
