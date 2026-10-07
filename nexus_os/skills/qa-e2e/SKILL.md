---
name: qa-e2e
description: Tests de bout en bout — reproduire d'abord, chasser le flaky, nommer le chemin réellement exécuté.
triggers: [test, qa, e2e, régression, bug, cas limite, reproduis, couverture, flaky]
tags: [qa, tests]
tools: [python_exec, shell, read_file, write_file]
license: MIT
---
# Tests & bout en bout

1. **Reproduis avant de corriger** : un test qui échoue, puis passe. Sinon tu n'as rien prouvé.
2. Trois cas minimum : nominal, limite, erreur — nommés dans le test.
3. Un test qui n'a pas traversé le code modifié ne prouve rien : nomme la fonction réellement exécutée.
4. **Chasse le flaky** : temps réel, ordre d'exécution, réseau, port fixe, hasard non fixé, attente par `sleep`.
5. Données de test isolées et reconstruites ; aucun test ne dépend de l'état laissé par un autre.
6. Exit code 0 avec une sortie inattendue = échec. Lis la sortie.
7. Test non exécuté = déclaré non exécuté, jamais « vérifié ».
