---
name: agent-reach
description: Donner des yeux à un agent — veille multi-plateformes sans frais d'API.
triggers: [veille, twitter, reddit, youtube, github, communauté, tendance, signaux faibles, reach]
tags: [veille, sources, automatisation]
tools: [web_search, http_get, grep, memory_remember]
license: MIT
---
# Veille multi-plateformes

## Ce que chaque plateforme dit vraiment
1. **GitHub** — les stars montantes : ce qui est en train de devenir un standard.
2. **Reddit / forums** — les problèmes réels, avant qu'ils ne deviennent des tickets.
3. **X / Twitter** — l'annonce et la controverse ; rarement la preuve.
4. **YouTube** — la démonstration ; utile pour vérifier qu'un outil tourne vraiment.
5. **Docs officielles** — la seule source normative.

## Règles
1. Une tendance sans date et sans volume n'est pas une tendance : c'est une impression.
2. Sépare **l'annonce** (ce qui est promis) de **l'usage** (ce qui est démontré).
3. Trois plateformes concordantes > dix posts sur une seule.
4. Privilégie les pages publiques : aucune clé, aucun quota, aucune donnée personnelle.
5. Ne jamais scraper ce qui exige une authentification ou contourne une limite.
6. Horodate chaque relevé : une veille non datée est inutilisable six mois plus tard.

## Sortie
Signal (1 ligne) → preuves datées par plateforme → ce que ça change → angle mort.
