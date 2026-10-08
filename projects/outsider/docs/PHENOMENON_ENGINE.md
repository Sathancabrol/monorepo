# ⚡ PHENOMENON_ENGINE — prochain système à formaliser

> Statut : **NEXT** (décidé le 08/10/2026, à la suite de la Société surnaturelle cachée)
> Dépendances : `SOCIETE-SURNATURELLE-CACHEE.md` (acteurs, économie, relations), `WORLD_STATE.md` (lecture/écriture)

## Mission
Maintenant qu'on sait **ce qui existe**, ce moteur définit **comment le jeu décide ce qui se produit** :

| Question | À spécifier |
|---|---|
| **Quoi ?** | Types de phénomènes (transaction, rituel, meurtre, rumeur, disparition, manifestation…) |
| **Où ?** | Sélection par territoire, lieux fréquentés, infrastructures d'organisation |
| **Quand ?** | Ticks de simulation, fenêtres horaires, conditions déclenchantes |
| **Pourquoi ?** | Chaîne causale depuis un objectif d'acteur ou une tension de relation |
| **Qui le sait ?** | Propagation d'information : témoins → rumeurs → factions → police |
| **Qui réagit ?** | Réactions d'acteurs (chasseur entend, police enquête, rival profite) |
| **Comment le joueur tombe dessus ?** | Manifestations perceptibles, accroches accidentelles (cf. RAW 46 §4), densité contrôlée |

## Contraintes de design héritées
1. Le phénomène est **produit par la simulation**, pas scripté pour le joueur (RAW 46, pilier 3).
2. Le joueur peut **ne rien faire** : l'événement suit son cours (la livraison a lieu).
3. Densité : chaque manifestation doit *mériter* d'être montrée — pas d'overload (leçon d'interface, cf. Cyberpunk).
4. Un phénomène = au moins une **piste entrante** dans une chaîne d'investigation.

## Livrables attendus de la formalisation
- Taxonomie des phénomènes (avec cause-type, visibilité, délai de prescription).
- Modèle de propagation d'information (qui sait quoi, à quelle vitesse).
- Budget d'attention du joueur (max N phénomènes actifs visibles).
- Interface avec l'investigation : format standard d'une piste (`PISTE → CIBLE → CONFIANCE → PROVENANCE`).
