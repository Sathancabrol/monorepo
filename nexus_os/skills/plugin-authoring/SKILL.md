---
name: plugin-authoring
description: Écrire un plugin NEXUS·OS — « everything is a plugin » (DeepSeek Harness).
triggers: [plugin, extension, module, packager, distribuer, manifeste, greffer]
tags: [plugin, extensibilité, meta]
tools: [write_file, read_file, list_dir, create_skill]
license: MIT
---
# Écrire un plugin NEXUS·OS

## Contrat minimal
Un dossier, un `plugin.json`, et ce qu'il déclare :

```json
{
  "name": "mon-plugin",
  "version": "0.1.0",
  "description": "Ce que ça apporte, en une ligne",
  "skills": ["skills/ma-methode"],
  "agents": ["agents/mon-agent.json"],
  "tools": [],
  "requires": ["read_file"]
}
```

## Règles
1. **Une responsabilité par plugin.** Deux plugins qui font la même chose : fusionne-les.
2. Aucun plugin ne modifie le cœur : il ajoute des compétences, des agents, des outils.
3. Déclare tes prérequis (`requires`) : un plugin qui échoue silencieusement est pire
   qu'un plugin absent.
4. Chemins relatifs au dossier du plugin, jamais absolus.
5. Le nom du plugin devient un namespace : `plugin:outil`, `plugin/competence`.
6. Versionne dès le premier jour ; une rupture de schéma se signale, elle ne se devine pas.

## Recette de validation
1. Installe le plugin dans un `NEXUS_HOME` vierge.
2. Vérifie que `skills` et `agents` apparaissent dans les compteurs.
3. Désactive-le : l'OS doit démarrer et fonctionner exactement comme avant.

## Sortie
Arborescence → manifeste → ce que le plugin ajoute → preuve de désactivation propre.
