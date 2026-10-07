---
name: design-impeccable
description: Sortir du rendu générique — décisions de design argumentées, pas un template.
triggers: [design, interface, ui, maquette, landing, refonte, look, générique, template]
tags: [design, ui, frontend]
tools: [compose_html, render_chart, read_file]
license: MIT
---
# Design non générique

## Les cinq marqueurs du « générique » à éliminer
1. Dégradé violet/bleu sur fond blanc et trois cartes icône-titre-texte alignées.
2. Un espacement uniforme partout : rien n'est hiérarchisé, donc rien n'est important.
3. Deux familles de police, quatre graisses, aucune raison.
4. Des bordures arrondies et des ombres identiques sur des éléments de nature différente.
5. Une illustration abstraite qui n'informe sur rien.

## Décisions à prendre et à énoncer
1. **Une seule** couleur d'accent ; le reste en niveaux de gris. Le sens passe par le contraste.
2. Hiérarchie par la taille et le poids, jamais par la couleur décorative.
3. Une famille sans-serif pour l'interface, une mono pour la donnée et les labels.
4. Espacement ×1,5 entre groupes, ÷2 à l'intérieur d'un groupe.
5. Chaque cellule répond à une question précise ; si elle n'en a pas, elle disparaît.

## Vérification
1. Test des 5 secondes : qu'est-ce qui est le plus important ici ? Une seule réponse.
2. Test du noir et blanc : la hiérarchie tient-elle sans couleur ?
3. Test du 390 px : tout reste lisible sans scroll horizontal.
4. Test du pourquoi : chaque décision a une raison écrite.

## Sortie
Décisions (choix → raison) → maquette → ce qui a été retiré et pourquoi.
