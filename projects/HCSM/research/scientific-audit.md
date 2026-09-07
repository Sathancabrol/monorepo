# Audit scientifique du document source

**Objet audité :** document de travail « COGNITION HUB — Vers une représentation multidimensionnelle et dynamique de l'état cognitif humain à T0 » (base conceptuelle longue, ~2 091 lignes dans la version transmise).  
**Date :** 2026-08-25  
**Méthode :** lecture affirmation par affirmation sur les thèses structurantes (pas une revue ligne à ligne du texte intégral, non versé dans ce dépôt).  
**Échelle :** `solide` · `à nuancer` · `insuffisamment étayée` · `déjà existante` · `à retirer`

Le document source n'est pas recopié ici. L'audit porte sur les thèses reprises dans le travail de repositionnement.

---

## 1. Thèses structurantes

| # | Affirmation (reconstituée) | Jugement | Commentaire | Devenir dans HCSM v0.1 |
|---|---|---|---|---|
| A1 | L'objet n'est pas un score mais une ontologie dynamique de l'état, avec estimation, contexte, temps, provenance, incertitude | **solide** comme programme | Cohérent, original *comme assemblage computationnel*, pas comme chacun de ses termes | Conservée, devenue définition |
| A2 | On peut viser une représentation de l'état cognitif humain à T0 | **à nuancer** | T0 sans fenêtre est métaphysique ; « humain » est trop large pour un noyau de 6 construits | T0 = centre de fenêtre ; noyau restreint |
| A3 | Première / nouvelle intégration cognition + psychologie + physiologie + neurologie | **déjà existante** / **à retirer** | RDoC | Explicitement non revendiquée |
| A4 | Pile biologique → physiologique → psychologique → cognitif → neurologique → comportement → environnement | **à retirer** | « Neurologique » n'est pas parallèle à « cognitif » | Remplacée par voies d'évidence |
| A5 | Capacity × State × Context | **à nuancer** | Utile, incomplet sans Evidence | Evidence ajoutée |
| A6 | value + confidence + provenance + timestamp suffisent | **à nuancer** | Manquent alternatives, fenêtre, référence, refus | Contrat `ConstructEstimate` élargi |
| A7 | Attention = 0.73 peut être une sortie si on ajoute de la confiance | **insuffisamment étayée** / dangereux | Réification même avec un ± | Interdit comme objet terminal |
| A8 | Relier ce qui est déjà mesuré vaut mieux que mesurer davantage | **solide** | Phrase centrale, à conserver | Titre de la contribution |
| A9 | Un graphe unique de la cognition | **à nuancer** | Confond connaissance, évidence, inférence | Trois graphes |
| A10 | État neurologique comme catégorie opérationnelle | **à retirer** | Catégorie instable | Absente de l'ontologie |
| A11 | Filiations Atlas, RDoC, ICF, HPO | **solide** | Déjà reconnues dans le source, sous-utilisées pour borner la nouveauté | Matrice de nouveauté |
| A12 | Pont vers Cognitorium | **solide** comme architecture d'écosystème | À condition que Cognitorium ne réécrive pas l'inference graph | Frontière documentée |
| A13 | On pourra inférer le fonctionnement à partir de l'état | **insuffisamment étayée** | L'ICF l'interdit comme déduction | Projection toujours `HYPOTHESIS` |
| A14 | Multimodalité ⇒ meilleure validité | **insuffisamment étayée** | La multimodalité sans validité de construit ajoute du bruit | H3 à tester, pas à affirmer |
| A15 | Digital phenotyping comme voie naturelle | **à nuancer** | Voie légitime, validité fragile | Canal `digital_passive`, jamais un construit |

## 2. Problèmes transversaux

### 2.1. Nouveauté mal placée

Le source a une vraie intuition (liaison connaissance / mesure / personne / temps) et une fausse vitrine (intégration multi-niveaux). La vitrine est plus facile à citer, et plus facile à détruire. L'audit recommande d'inverser : vitrine = liaison ; héritage = multi-niveaux.

### 2.2. Oscillation score / anti-score

Le texte produit des scalaires, puis les critique. Cette oscillation n'est pas une dialectique utile : elle laisse une implémentation libre de n'implémenter que la première moitié. HCSM rend la première moitié *invalide*.

### 2.3. Ontologie trop large trop tôt

Une ontologie « de l'état cognitif humain » invite à l'encyclopédie. L'audit recommande un noyau falsifiable.

### 2.4. Absence de refus

Un système qui a toujours un T0 n'est pas un modèle scientifique d'état, c'est un générateur de tableaux de bord.

### 2.5. Figures ASCII

Les 7 figures du source allaient déjà dans la bonne direction (carte riche, flux, graphes). Elles ont été réécrites pour coller au repositionnement (`figures/`).

## 3. Ce qui était déjà bon et qu'il ne fallait pas perdre

- la méfiance envers le score unique ;
- la présence de la provenance et de la confiance ;
- la mention explicite d'Atlas / RDoC / ICF / HPO ;
- la distinction Capacity / State / Context ;
- la phrase sur relier plutôt que mesurer davantage ;
- la séparation conceptuelle Cognition Hub / HCSM / Cognitorium (déjà esquissée).

## 4. Verdict

Le document source est une **base conceptuelle avancée**, pas un article. Il ne mérite pas une simple réécriture. Il méritait un repositionnement. C'est ce que fait HCSM 0.1.

Statut global après audit : passer de « plateforme nouvelle de la cognition » à « contrat d'inférence personnelle entre cadres existants ».
