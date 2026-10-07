---
name: html-composition
description: Livrer des pages HTML autonomes — un fichier, zéro build, rendu immédiat.
triggers: [html, page, rapport visuel, composition, landing, slide, rendu]
tags: [production, html]
tools: [compose_html, write_file]
license: MIT
---
# Composition HTML

Inspiré de l'approche « écris du HTML, obtiens un rendu » (hyperframes) :

1. Un fichier autonome : CSS inline dans `<style>`, aucune dépendance de build.
2. Sémantique d'abord (`header`, `main`, `section`, `table`), style ensuite.
3. Palette : fond sombre `#0b0f17`, texte `#e6edf3`, un seul accent.
4. Responsive par défaut ; lisibilité à 320 px comme à 1920 px.
5. Animations discrètes et désactivables (`prefers-reduced-motion`).
6. Indique le chemin du fichier produit et l'URL d'aperçu.
