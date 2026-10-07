---
name: security-review
description: Traquer injection, chemins non validés, secrets en dur et erreurs avalées.
triggers: [sécurité, vulnérabilité, injection, secret, audit sécurité, owasp]
tags: [sécurité, revue]
tools: [grep, read_file]
license: MIT
---
# Revue sécurité

Cherche activement, dans cet ordre :
1. **Injection** : SQL/shell/HTML construit par concaténation ; commande passée à `shell=True`.
2. **Chemin** : `..`, chemin absolu fourni par l'utilisateur, symlink, résolution sans contrôle de racine.
3. **Secrets** : clé en dur, secret loggé, `.env` commité, token dans une URL.
4. **Erreurs avalées** : `except: pass`, stack trace renvoyée au client.
5. **Authentification/autorisations** : contrôle contournable, ID devinable, absence de rate-limit.
6. **Dépendances** : non épinglées, source non vérifiée.

Pour chaque finding : impact concret + correctif minimal. Pas de FUD sans exploit décrit.
