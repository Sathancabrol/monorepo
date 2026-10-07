# REFERENCE TECH — Catalogue V0.1

Ce catalogue démarre avec des références vérifiées le 7 octobre 2026. Il doit ensuite être enrichi automatiquement et manuellement.

## Priorité A — orchestration Unreal

### Unreal-MCP — IvanMurzak
https://github.com/IvanMurzak/Unreal-MCP
Usage : inspection et pilotage Unreal, acteurs, niveaux, Blueprints, assets, C++, captures.
Pourquoi : candidat majeur pour la couche d'exécution Unreal.

### GameDev-MCP-Server
https://github.com/IvanMurzak/GameDev-MCP-Server
Usage : serveur MCP moteur-agnostique partagé Unity/Godot/Unreal.
Pourquoi : architecture intéressante pour ne pas enfermer le pipeline dans un seul moteur.

### Unreal Agent Harness
https://github.com/per-simmons/unreal-agent-harness
Usage : agent + Unreal + capture + QA + PCG + villes.
Pourquoi : référence directe pour notre boucle BUILD → SEE → CHECK → FIX.

### Codex GameDev Harness
https://github.com/ddalkakgames/codex-gamedev-harness
Usage : design → systèmes → art direction → concepts → asset briefs → 3D → Unreal → gameplay → QA.
Pourquoi : architecture documentaire très proche de notre objectif.

### ATDev uemcp
https://github.com/ATDev-Inc/uemcp
Usage : Unreal piloté par Claude/MCP, avec tests de protocole et roadmap asset providers.
Pourquoi : alternative à comparer.

## Priorité A — Blender / 3D

### mcp-blender-agent
https://github.com/PoBruno/mcp-blender-agent
Usage : contrôle déterministe de Blender par outils typés ; modeling, rigging, animation, matériaux, Geometry Nodes, export.
Pourquoi : réduit l'improvisation de scripts.

### Blender Agent
https://github.com/hotspoons/blender-agent
Usage : agent autonome Blender, UI web, MCP HTTP, API compatible OpenAI, headless, skills.
Pourquoi : candidat pour pipeline local/headless.

### Kiln
https://github.com/matthew-kissinger/kiln
Usage : géométrie procédurale éditable, rendu de revue, contrôles structurels, GLB, MCP local.
Pourquoi : très intéressant pour assets paramétriques et reproductibles.

## Priorité A — génération procédurale

### Unreal PCG
https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-overview
Usage : bâtiments, biomes, outils et mondes procéduraux.
Pourquoi : cœur potentiel de génération de monde.

### AutoUE
https://github.com/Pluto156/AutoUE
Usage : génération multi-agent de jeux 3D Unreal, retrieval de documentation UE, scène + gameplay + tests.
Pourquoi : référence de recherche pour architecture multi-agent.

## Priorité A — validation

### CraftBench-UE
https://arxiv.org/abs/2609.23142
Usage : benchmark déterministe de tâches Unreal pour agents, checks build/assets/runtime.
Pourquoi : inspiration directe pour notre système de validation.

## Priorité B — catalogues à aspirer

À rechercher et importer :
- Awesome GameDev lists ;
- Free/Open Source GameDev resource lists ;
- game asset catalogues ;
- open-source games lists ;
- procedural generation lists ;
- Blender add-on lists ;
- Unreal marketplace/free samples ;
- GIS/OSM tooling lists ;
- AI agent/MCP directories ;
- academic survey/research indexes.

## Règle de classement

Chaque référence doit recevoir :
name, url, source_type, category, license, engine, version, local/cloud, GPU, dependencies, maturity, API/MCP, inputs, outputs, limitations, outsider_use, priority, last_checked.

## Références communautaires

Reddit montre deux tendances utiles :
1. les workflows multi-outils (ChatGPT/Claude/Codex + Blender MCP + Unreal MCP) sont déjà utilisés ;
2. les résultats nécessitent encore des boucles de correction, notamment pour les assets 3D.

Le pipeline cible doit donc assumer l'itération et la QA, pas promettre du one-shot.
