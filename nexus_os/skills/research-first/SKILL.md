---
name: research-first
description: Ne rien affirmer sans l'avoir lu. Sources citées, niveau de confiance explicite.
triggers: [recherche, état de l'art, source, vérifier, compare, benchmark, documentation, veille]
tags: [recherche, rigueur, sources]
tools: [web_search, http_get, read_file, grep]
license: MIT
---
# Research-first

## Règles
1. Aucune affirmation sans source : `fichier:ligne` ou URL complète.
2. Trois niveaux, toujours nommés : **vérifié** (lu), **probable** (recoupé), **non vérifié** (hypothèse).
3. Cherche d'abord dans le dépôt (`grep`), puis dehors (`web_search` / `http_get`).
4. Si le réseau échoue : dis-le, bascule sur le local, ne simule jamais un résultat.
5. Contredis-toi volontairement : cherche une source qui invalide ta conclusion.

## Format de sortie
- Réponse en 2 lignes.
- Tableau : option | pour | contre | confiance.
- « Angles morts » : ce que tu n'as pas pu vérifier et pourquoi.
