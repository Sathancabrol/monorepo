---
name: prompt-engineering
description: Prompts à contraintes vérifiables — format imposé par l'exemple, échecs anticipés.
triggers: [prompt, consigne, system prompt, instruction, réglage, format de sortie]
tags: [prompt, meta]
tools: [read_file, write_file]
license: MIT
---
# Ingénierie de prompts

## Structure, dans cet ordre
1. **Rôle** — une phrase.
2. **Contexte** — ce que le modèle doit savoir, rien de plus.
3. **Contraintes** — numérotées et vérifiables. « Sois clair » est supprimé d'office.
4. **Format de sortie** — imposé par un exemple, pas par une description.

## Règles
1. Une contrainte non vérifiable est une contrainte morte.
2. Anticipe les 3 façons dont le prompt échoue et traite-les explicitement.
3. Few-shot : un bon exemple **et** un contre-exemple, sinon le modèle imite la forme sans la règle.
4. Sépare ce qui est stable (rôle, format) de ce qui varie (contexte) — cela permet de réutiliser.
5. Livre le test de recette : l'entrée exacte qui révèle si le prompt tient.
