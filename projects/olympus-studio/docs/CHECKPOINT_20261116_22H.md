# Reprise 2026-11-16 22h Europe/Paris — vérification A/V alpha

Branche isolée : `feat/olympus-studio-20261112`. PR #16 brouillon. Lecture effectuée : AUTONOMOUS_BACKLOG, HANDOFF (fin), STATUS, SESSION_PLAN, PR #16, issues #11–#17 et workflow dédié.

## Livré
- `c25b14f668e0b8c0ab2f1040de604306697cc56d` : `tools/check-av.mjs`, outil Node hors ligne appelant FFprobe installé localement, vérifie présence vidéo et audio Opus et écart début/fin maximal 0,6 s. Pas de modification de l'export applicatif.
- `e06d0f7b5e96067357a86d9ee8cc3b040f50c0b8` : tests Node du validateur (cas aligné, dérive 700 ms, absence audio, durée négative). `npm test` découvre automatiquement ces tests.
- Tests non exécutés localement dans cette session. Le dernier CI vérifié auparavant était 43934956870 vert sur `870f35d1`; CI du HEAD actuel non confirmée. La recherche des runs par SHA court `3471cc73` n'a rien retourné : ne pas interpréter comme succès.
- Aucune validation Windows, GTX 1060/1650, OBS réel ou ComfyUI réel.

## Reprise exacte
1. P0 S : vérifier CI du HEAD `e06d0f7b` ou plus récent, inspecter jobs Node/Chromium, réparer immédiatement si rouge.
2. P0 M : reproduire le téléchargement Portable après undo/redo, exploiter diagnostics Chromium et corriger le chemin applicatif. Ne pas déclarer résolu.
3. P0 M–L : mesurer export A/V réel avec `node tools/check-av.mjs chemin/export.webm`; cet outil est un **contrôle**, pas un fallback de rendu. Si dérive, documenter et intégrer une alternative FFmpeg libre réellement testée.
4. P1 M : préparer paquet alpha mercredi 18 novembre et recette Windows; documenter explicitement limites.

Estimation restante alpha M–L, dépendance aux essais Windows non levée. Ne modifier ni main ni les autres projets.
