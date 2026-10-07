---
name: context-compression
description: Garder le contexte petit — résultats référencés, aperçus, plages ciblées.
triggers: [contexte, tokens, compression, trop long, fenêtre de contexte, payload, référencer]
tags: [contexte, performance, tokens]
tools: [context_report, read_file, grep]
license: MIT
---
# Compression de contexte

## Principe
Le contexte est la ressource rare. Un résultat volumineux **n'y rentre pas** :
il est écrit dans la sandbox et l'agent reçoit une référence — taille, forme, aperçu.

## Règles
1. Avant de lire un fichier entier, demande sa taille ; lis une plage, pas le tout.
2. Pour chercher dans un gros volume : `grep` d'abord, `read_file` ciblé ensuite.
3. Un aperçu de 400 caractères suffit pour décider. Charger « au cas où » est une faute.
4. Ne recopie jamais un outil dans ta réponse : cite la référence et le chemin.
5. Chiffre le gain (tokens économisés) plutôt que de l'affirmer.
6. Trois références non consultées dans une exécution = trois lectures évitées : c'est le but.

## Anti-motifs
- Coller un JSON de 2 000 lignes « pour que ce soit complet ».
- Résumer un payload avant de l'avoir chargé (résumé d'un résumé = perte en cascade).
- Garder l'historique complet d'une délégation : compacte-le.

## Sortie
Ce qui a été chargé, ce qui a été référencé, tokens économisés, ce qui reste à vérifier.
