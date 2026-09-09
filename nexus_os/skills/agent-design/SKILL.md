---
name: agent-design
description: Concevoir un agent spécialisé qui tient la route — périmètre étroit, règles vérifiables.
triggers: [crée un agent, nouvel agent, agent spécialisé, conçois un agent, prompt système]
tags: [meta, design, agent]
tools: [create_agent]
license: MIT
---
# Concevoir un agent

## Les 6 décisions
1. **Résultat** : une phrase — « il produit X à partir de Y ». Si deux verbes, c'est deux agents.
2. **Périmètre** : ce qu'il refuse de faire, explicitement.
3. **Compétences** : 2 à 4, choisies dans la bibliothèque existante.
4. **Outils** : le minimum suffisant ; chaque outil ajouté est une surface d'erreur.
5. **Cycle de vie** : les phases utiles parmi plan → research → implement → review → verify → remember → improve.
6. **Recette** : la tâche exacte qui prouve qu'il fonctionne.

## Prompt système
- Règles numérotées et vérifiables. Les adjectifs sont interdits (« sois utile », « sois rigoureux »).
- Une section « interdit » courte et concrète.
- Le format de sortie imposé, pas suggéré.
