# Benchmark VFX Lab — registre initial 25/11/2026
Référentiel issu de la recherche GLAZE CRT. Les liens sont des pistes de référence ; vérifier existence, licence SPDX, release, activité, API et résultats avant intégration. Pas de mesure comparative réalisée ; étoiles non figées.
| Projet | Référence | Usage envisagé | Priorité |
|---|---|---|---|
| GLAZE CRT | https://faceworld.video/product/glaze | UX, CRT, VHS, circuit bending ; propriétaire, inspiration uniquement | P0 |
| NTSCRT | https://github.com/finnmckenty/NTSCRT | Application CRT/VHS, automatisation MCP/CLI à confirmer | P0 |
| ntsc-rs | https://github.com/ntsc-rs/ntsc-rs | Moteur NTSC/VHS, export hors ligne | P0 |
| ShaderGlass | https://github.com/mausimus/ShaderGlass | Shaders écran, comparaison GPU Windows | P0 |
| OBS Retro Effects | https://github.com/FiniteSingularity/obs-retro-effects | Filtres live OBS | P0 |
| OBS ShaderFilter | https://github.com/exeldro/obs-shaderfilter | Shaders custom, OBS | P0 |
| BENDR | https://github.com/clickysteve/bendr | Feedback, glitch, montage créatif | P1 |
| BitRot | https://github.com/squintdev/BitRot | CRT/VHS expérimental | P1 |
| ShaderBeam | https://github.com/mausimus/ShaderBeam | Balayage CRT | P2 |
| AnalogForge | https://github.com/XonistReal/vhs-suite | VHS audio/vidéo | P2 |
| PurzOS OFX | https://github.com/purzbeats/purzos-ofx | Plugins vidéo | P2 |
| Video Glitcher | https://github.com/non-npc/Video-Glitcher | Effets procéduraux | P2 |
| SeeRT Overlay | https://github.com/lanecwheeler/SeeRT-Overlay | Overlay Windows | P2 |
| CRTinator | https://github.com/kunal-png/crtinator | Overlay CRT | P2 |
| CathodeDisplay | https://github.com/skulitom/CathodeDisplay | Moniteur simulé | P2 |
| CRT View | https://github.com/mattiasgustavsson/crtview | Images CRT | P2 |
| RetroMac | https://github.com/klotzbrocken/RetroMac | Bureau rétro | P2 |
| RetroVisor | https://github.com/dirkwhoffmann/RetroVisor | Shaders et capture | P2 |
| Liquid LSD | https://github.com/greenjon/liquid-lsd | Audio-réactivité | P2 |
| ImWeb | https://github.com/imweb-project/ImWeb | Synthèse vidéo web | P2 |
| RetroArch slang shaders | https://github.com/libretro/slang-shaders | Bibliothèque shaders, licences par fichier | P1 |
| FFmpeg | https://ffmpeg.org/ | Encodage local, filtres et audio | P0 |
| OBS Studio | https://github.com/obsproject/obs-studio | Régie, capture et streaming | P0 |
## Protocole reproductible
Inventorier localement avant téléchargement : chemin, version, installateur, hash, taille, licence, présence sur disque externe, intégration réelle. Pour chaque candidat vérifier README, LICENSE et releases à un commit précis. Statut initial: non audité au niveau de la licence et non testé. N'utiliser aucun code sans licence compatible ; conserver les notices.
Comparer même clip synthétique 720p/1080p, webcam autorisée, séquence 60s : FPS médian/p95 temps de frame, images perdues, VRAM/RAM/CPU, latence, fidélité visuelle, alpha, audio, export, API, coût, dépendances, fonctionnement hors-ligne. Tester sur GTX 1060 6 Go et GTX 1650 4 Go ; ne pas inventer de résultats. Noter métriques, version et preuve. Choisir moteur interne WebGL2 et adaptateurs externes selon résultats.
