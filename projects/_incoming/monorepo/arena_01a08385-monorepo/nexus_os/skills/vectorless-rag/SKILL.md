---
name: vectorless-rag
description: Retrouver sans base vectorielle — index raisonné, graphe, citations vérifiables.
triggers: [rag, retrieval, index, base vectorielle, embedding, connaissance, document, graphe]
tags: [rag, indexation, documents]
tools: [grep, read_file, list_dir, diagram]
license: MIT
---
# Retrieval sans vecteurs

## Pourquoi
Une base vectorielle répond « ce qui ressemble », pas « ce qui suit ». Pour un
dépôt, un contrat ou une procédure, la structure porte plus d'information que la
similarité — et elle est explicable.

## Méthode
1. **Index raisonné** : découpe le corpus selon sa structure réelle (chapitres,
   fonctions, clauses), pas en fenêtres de N tokens.
2. **Graphe de relations** : qui appelle qui, quelle clause renvoie à quelle définition.
3. **Requête par navigation** : point d'entrée → voisinage → preuve. Pas de top-k aveugle.
4. **Citation obligatoire** : toute affirmation renvoie à un chemin et une ligne.

## Règles
1. `grep` avant tout embedding : un motif exact bat une similarité approchée.
2. Un résultat sans chemin vérifiable n'est pas une réponse.
3. Si le corpus tient dans le contexte, ne construis aucun index.
4. Un graphe de 12 nœuds utiles vaut mieux qu'un index de 10 000 morceaux opaques.
5. Signale ce que la structure ne permet pas de conclure.

## Sortie
Chemin de navigation → extraits cités (chemin:ligne) → limite de la méthode.
