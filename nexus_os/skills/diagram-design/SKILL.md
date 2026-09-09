---
name: diagram-design
description: Diagrammes d'architecture, flux et séquences lisibles — Mermaid, 9 nœuds max par vue.
triggers: [diagramme, schéma, architecture, flux, mermaid, séquence, dépendances]
tags: [architecture, visualisation]
tools: [diagram, compose_html]
license: MIT
---
# Conception de diagrammes

## Une vue = une question
- Composants : « qu'est-ce qui existe et qui parle à qui ? »
- Flux de données : « où naît, circule et meurt la donnée ? »
- Séquence : « dans quel ordre, et qui attend qui ? »

## Règles
1. 9 nœuds maximum ; au-delà, découpe et nomme les vues.
2. Arêtes nommées par ce qui circule (`HTTP POST /run`, `événement job.done`), jamais « vers ».
3. Aucune boîte générique (« Service », « Backend ») sans rôle dans le libellé.
4. Regroupe par frontière de confiance ou de déploiement, pas par dossier.
5. Livre le Mermaid + le fichier produit + 3 décisions justifiées.
