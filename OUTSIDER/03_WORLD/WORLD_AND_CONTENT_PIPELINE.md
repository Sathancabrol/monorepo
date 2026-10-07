# WORLD & CONTENT PIPELINE

## Philosophie

Le monde doit être à la fois authored et procedural.

L'IA ne doit pas générer chaque objet indépendamment si une règle/générateur peut produire une famille cohérente.

## Pipeline

RÉFÉRENCE RÉELLE
→ DONNÉES
→ RÈGLES
→ GÉNÉRATEUR
→ SEED
→ ASSET
→ INTÉGRATION MOTEUR
→ VALIDATION
→ PATCH

## Bloc de contenu

Chaque BLOCK possède :
- BLOCK_ID
- objectif
- contexte narratif
- dépendances
- références
- données d'entrée
- générateur ou asset source
- interactions
- contraintes physiques
- gameplay
- performance
- validation
- statut
- historique des modifications.

## Exemple B001 — maison familiale cévenole

Doit fournir :
- géométrie intérieure/extérieure ;
- échelle ;
- pièces ;
- jardin ;
- garage ;
- portes/fenêtres interactives ;
- collisions ;
- navigation ;
- points de spawn ;
- emplacements d'indices ;
- objets examinables ;
- éclairage ;
- matériaux ;
- zones de fuite ;
- couverture ;
- possibilités de combat ;
- possibilités d'enquête ;
- contraintes de performance.

## Génération procédurale

Priorité à :
- terrain ;
- végétation ;
- architecture répétitive ;
- routes ;
- villages ;
- distribution de mobilier ;
- variantes de créatures/environnements ;
- météo ;
- dégâts ;
- miasma.

## Réel / géospatial

Les données réelles peuvent fournir :
- empreintes de bâtiments ;
- routes ;
- relief ;
- hydrographie ;
- végétation ;
- points d'intérêt.

Mais la donnée réelle doit être transformée en contenu jouable et ne doit pas devenir une dépendance réseau obligatoire pour jouer.

## World state

Le décor peut changer à cause :
- météo ;
- saison ;
- temps ;
- activité humaine ;
- construction/dégradation ;
- miasma ;
- créatures ;
- actions du joueur ;
- actions de factions ;
- conséquences différées.

## QA spatial

Minimum :
1. vue aérienne ;
2. vue à hauteur humaine ;
3. vue joueur.

Vérifier :
overlap, collisions, navigation, accessibilité, échelle, lisibilité, performance, cohérence visuelle.
