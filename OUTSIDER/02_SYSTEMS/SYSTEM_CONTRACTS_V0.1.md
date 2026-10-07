# SYSTEM CONTRACTS V0.1

Format obligatoire :
MACHINE → OBJECTIF → ENTRÉES → ÉTAT → RÈGLES → SORTIES → CONSÉQUENCES → INTERACTIONS → UI → DONNÉES → TEST

## 01 Life Simulation

OBJECTIF : simuler une vie crédible autour des contraintes de jeu.

Entrées : âge, lieu, calendrier, relations, besoins, événements, études, travail, ressources.

Sorties : disponibilité, relations, connaissances, traces, fatigue, progression.

Test : 20 minutes dans le village doivent produire une impression de vie autonome.

## 02 World State

Entités minimales :
Player, NPC, Location, Object, Creature, Clue, Event, Faction, Relation, Perk, Item, Evidence, Rumor, Belief, Consequence.

Chaque entité possède un identifiant stable et un historique minimal.

## 03 Time / Event Engine

Deux catégories :
- événements fixes de timeline ;
- événements conditionnels contextuels.

Règle : le joueur peut retarder une situation, mais pas rendre le monde infiniment immobile.

Pipeline :
CALENDRIER → SCHEDULE → WORLD STATE → CONDITIONS → EVENT → OBSERVATION → CONSEQUENCE.

## 04 NPC Simulation

NPC = routine + objectifs + besoins + mémoire + perception + relations + connaissances + état émotionnel.

Le NPC ne doit pas connaître ce que le joueur n'a pas transmis.

## 05 Information Engine

INFORMATION BORN → SOURCE → OBSERVATION → INTERPRÉTATION → VÉRIFICATION → CONNAISSANCE → ACTION POSSIBLE.

La provenance est conservée.

## 06 Consequence Engine

Une conséquence possède :
- déclencheur ;
- portée ;
- délai ;
- systèmes affectés ;
- visibilité ;
- réversibilité ;
- provenance.

Types : immédiate, différée, locale, relationnelle, factionnelle, mondiale, NG+.

## 07 Investigation

Les indices sont des objets du monde, pas seulement des marqueurs de quête.

Le joueur peut :
observer, photographier, enregistrer, mesurer, comparer, interroger, suivre, fouiller, expérimenter, relier.

## 08 Lethal / Non-Lethal

Le système doit générer des conséquences réelles, notamment disparition d'un témoin, corps, preuve, dette, relation, réputation ou transformation.

## 09 Miasma

La perturbation surnaturelle modifie progressivement l'écosystème.

Symptômes → accumulation → nid → prolifération → incidents → danger majeur.

## 10 Reputation / Police

Séparer :
Truth / Evidence / Narrative / Wanted / Supernatural reputation / Public network.

Les autorités voient les conséquences observables, pas automatiquement la vérité surnaturelle.

## 11 Base

Base = espace de sauvegarde/préparation/recherche/production.

Chaque pièce ou équipement doit apporter une capacité fonctionnelle.

## 12 NG+

Séparer :
- persistence dans une vie ;
- persistence entre vies ;
- mémoire consciente ;
- connaissance méta ;
- modifications du monde.

## 13 Validation

Chaque machine doit posséder des tests :
- unitaires si possible ;
- simulation ;
- runtime ;
- visuels ;
- régression.

Aucun bloc n'est considéré terminé parce qu'il « compile ».
