---
name: osint-recon
description: Recueil d'information ouverte — source tracée, recoupement, distinction signal/bruit.
triggers: [osint, veille, enquête, source, rumeur, signaux, surveille, géopolitique]
tags: [osint, veille, sources]
tools: [web_search, http_get, read_file]
license: MIT
---
# Recueil OSINT

## Chaîne de confiance
1. **Source primaire** — document original, auteur identifiable, daté.
2. **Reprise** — cite la primaire ; ne jamais citer une reprise comme si c'était l'original.
3. **Rumeur** — non attribuée : marquée comme telle, jamais reprise sans étiquette.

## Règles
1. Deux sources indépendantes minimum avant « probable » (indépendant = pas la même dépêche recopiée).
2. Toujours relever : date de publication, langue, auteur, intérêt éventuel de la source.
3. Une image ou une citation hors contexte est un piège classique : vérifie l'antériorité.
4. Sépare le **fait** (vérifiable) de l'**interprétation** (attribuée à quelqu'un).
5. Le signal passe en premier : ce qui change une décision avant ce qui est intéressant.

## Sortie
Synthèse 2 lignes → tableau (affirmation | source | date | confiance) → angles morts.
