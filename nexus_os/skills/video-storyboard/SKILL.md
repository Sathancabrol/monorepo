---
name: video-storyboard
description: Découper en plans — un plan une idée, premier plan sous 2s, sous-titres 42 caractères.
triggers: [vidéo, storyboard, séquence, animation, motion, montage, plan, teaser, sous-titres]
tags: [vidéo, motion]
tools: [compose_html, write_file]
license: MIT
---
# Storyboard

## Un plan = une ligne de tableau
`n° | durée | visuel | texte à l'écran | audio | transition`

## Rythme
1. Premier plan sous 2 secondes — l'attention se joue là.
2. Changement toutes les 3 à 5 secondes.
3. Une idée par plan ; deux idées = deux plans.

## Sous-titres
- 42 caractères par ligne, 2 lignes maximum.
- Lisibles : le texte reste à l'écran le temps d'être lu à voix haute.
- Contraste garanti (voile sombre derrière si l'image est claire).

## Technique
- Animations pilotées par une horloge de composition (positionnables image par image), pas par l'horloge murale.
- Respecte `prefers-reduced-motion`.
- Signale ce qui exige un moteur de rendu (ffmpeg, Puppeteer) absent de l'environnement.
