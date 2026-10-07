---
name: ux-heuristics
description: Critiquer une interface par critères vérifiables — contraste WCAG, cibles 44px, états d'abord.
triggers: [design, interface, ui, ux, ergonomie, accessibilité, contraste, responsive, refonte, mise en page]
tags: [design, ux]
tools: [compose_html, read_file]
license: MIT
---
# Heuristiques d'interface

## Critères vérifiables (pas des goûts)
1. **Contraste** — ratio WCAG : 4,5:1 pour le texte, 3:1 pour le texte large et les composants.
2. **Cibles tactiles** — 44 × 44 px minimum, espacement ≥ 8 px.
3. **Hiérarchie** — par taille, poids, espacement. Jamais par la couleur seule.
4. **Un seul accent** ; le reste en niveaux de gris. L'accent perd son sens s'il est partout.
5. **Cohérence** — un jeu unique de rayons et d'espacements (échelle ×1,5).

## Les 4 états à concevoir avant l'état idéal
Vide · chargement · erreur · chargé.

## Sortie
Findings classés BLOQUANT / MAJEUR / MINEUR, chacun avec le critère et la mesure. Pas de « c'est plus joli ».
