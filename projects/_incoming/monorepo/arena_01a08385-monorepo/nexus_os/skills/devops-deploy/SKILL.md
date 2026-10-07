---
name: devops-deploy
description: Déployer sans casse — diagnostic d'abord, idempotence, versions verrouillées, retour arrière prévu.
triggers: [déploie, ci, pipeline, docker, build, github actions, serveur, rollback, environnement]
tags: [devops, infra]
tools: [shell, read_file, write_file]
license: MIT
---
# Déploiement

1. **Diagnostique avant de modifier** : lis la config réelle et l'erreur réelle.
2. Toute commande destructive ou exposée sur internet est annoncée et attend une validation.
3. Versions verrouillées — une dépendance flottante est une panne programmée.
4. Idempotence : chaque étape rejouable à l'identique, sans effet de bord cumulé.
5. Le plan de retour arrière s'écrit **avant** le déploiement.
6. Secrets : variable d'environnement ou gestionnaire de secrets. Jamais en clair dans un fichier versionné.
7. Vérifie le déploiement par une sonde réelle (code HTTP, contenu), pas par « la commande a réussi ».
