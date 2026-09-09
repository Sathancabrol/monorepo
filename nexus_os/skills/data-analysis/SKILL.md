---
name: data-analysis
description: Analyse honnête — source et taille d'échantillon toujours déclarées.
triggers: [données, data, csv, métrique, statistique, tendance, kpi, dashboard]
tags: [data, analyse]
tools: [read_file, python_exec, compose_html]
license: MIT
---
# Analyse de données

1. Déclare toujours : fichier lu, nombre de lignes, période couverte.
2. 3 chiffres significatifs maximum ; ordre de grandeur avant précision.
3. Corrélé ≠ causal : nomme le mécanisme ou renonce à la causalité.
4. Vérifie les pièges : doublons, valeurs manquantes, unités mélangées, saisonnalité.
5. Toute analyse se termine par « ce que ces données ne permettent PAS de conclure ».
6. Un résultat non exécuté est marqué comme tel — jamais présenté comme un calcul fait.
