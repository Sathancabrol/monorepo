# REPO AUDIT — 7 octobre 2026

## Repos utilisateur retrouvés

### Sathancabrol/monorepo
Rôle : archive/carré d'as.
État observé : très volumineux, JavaScript, branche main, mis à jour le 7 octobre 2026. Le dépôt contient de nombreux documents BTP/TP, plans, tableaux, PDF, et des éléments hétérogènes. Il est utile comme source/archive mais ne doit pas devenir la structure finale de production sans index.

### Sathancabrol/watchtower
Rôle : OSINT/monitoring/cartographie/vue intelligence.
État observé : JavaScript/Vite, présence de src, tools et gros fichier CSS. À exploiter comme source de patterns UI, cartographie, outils et organisation fonctionnelle.

### Sathancabrol/COGNITORIUM
Rôle : visualisation cognitive.
État observé : JavaScript, docs, learning et watchtower-mods présents. Utile comme source de concepts d'interface, graphe, apprentissage et modules.

### Sathancabrol/proto-cognitorium
Rôle : prototype applicatif.
État observé : TypeScript, dérivé d'un template Google AI Studio. À comparer pour architecture applicative et prototypes d'agents.

## Conséquence pour Outsider

Ces repos ne doivent pas être fusionnés aveuglément dans le jeu.

Ils doivent être traités comme :
SOURCE → EXTRACTION → NORMALISATION → ADAPTATION.

## Problème monorepo

Le monorepo actuel est une archive de grande taille avec des documents hétérogènes. Sa valeur est élevée comme mémoire et source de données, mais sa valeur comme base directe de production est faible tant que les contenus ne sont pas indexés.

## Action recommandée

Ajouter un index :
- source_repo ;
- source_path ;
- module ;
- capability ;
- reusable ;
- license ;
- dependency ;
- extracted_from ;
- status.

## Branching

Cette documentation est développée dans :
outsider/documentation-v0.1

La branche main n'est pas modifiée directement par cette première consolidation.
