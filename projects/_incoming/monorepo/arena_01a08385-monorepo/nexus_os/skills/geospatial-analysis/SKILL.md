---
name: geospatial-analysis
description: Analyse territoriale rigoureuse — échelle, millésime et producteur toujours déclarés.
triggers: [territoire, carte, commune, population, atlas, urbanisme, géographique, bassin de vie]
tags: [géo, territoire]
tools: [read_file, compose_html, python_exec]
license: MIT
---
# Analyse territoriale

1. Toute donnée porte : producteur (INSEE, IGN, collectivité), millésime, échelle.
2. Comparer deux millésimes sans le dire est interdit ; signale les ruptures de série.
3. Ratios avant absolus : « 12 % de plus de 65 ans », pas « beaucoup de retraités ».
4. Une carte = une question. Titre = question, légende = unité, source en bas.
5. Attention aux effets de seuil (découpage administratif) et à l'écologie fallacieuse (déduire l'individu de l'agrégat).
6. Échelles à ne jamais mélanger : commune, EPCI, SCOT, bassin de vie, aire d'attraction.
