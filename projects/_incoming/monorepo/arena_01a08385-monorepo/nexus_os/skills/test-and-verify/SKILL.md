---
name: test-and-verify
description: Vérifier pour de vrai — nommer le chemin de code exécuté, pas seulement un exit code.
triggers: [test, vérifie, pytest, couverture, assertion, non régression]
tags: [tests, qualité, preuve]
tools: [shell, python_exec, read_file]
license: MIT
---
# Test & vérification

1. Un test qui passe sans avoir traversé le code modifié ne prouve rien : nomme la fonction réellement exécutée.
2. Un cas nominal, un cas aux limites, un cas d'erreur. Dans cet ordre.
3. Asserts sur le comportement observable, pas sur l'implémentation interne.
4. Exit code 0 avec une sortie inattendue = échec. Lis la sortie.
5. Si l'exécution est impossible (shell désactivé, dépendance manquante) : installe, débloque, ou déclare la vérification non faite — jamais « c'est bon » par déduction.
