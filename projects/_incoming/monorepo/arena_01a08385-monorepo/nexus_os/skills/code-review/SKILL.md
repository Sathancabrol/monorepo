---
name: code-review
description: Relecture à froid, classée par sévérité, avec correctif minimal.
triggers: [revue, review, relis, audit, qualité, dette technique]
tags: [qualité, revue]
tools: [read_file, grep]
license: MIT
---
# Revue de code

## Lecture
1. Lis le diff réel, pas sa description.
2. Commence par les frontières : entrées utilisateur, IO, concurrentiel, argent.

## Classification
- **BLOQUANT** : casse la prod, corrompt des données, trou de sécurité.
- **MAJEUR** : bug probable, dette qui coûtera cher, test absent sur un chemin critique.
- **MINEUR** : lisibilité, nommage, duplication tolérable.
- **NIT** : goût personnel — à signaler sans insister.

## Sortie
`SEVERITE fichier:ligne — problème — correctif minimal`. Verdict final : FUSIONNER / CORRIGER / REPOUSSER.
