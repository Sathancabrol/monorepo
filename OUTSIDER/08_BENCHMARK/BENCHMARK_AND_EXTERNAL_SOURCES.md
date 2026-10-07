# BENCHMARK & SOURCES EXTERNES

## Jeux / systèmes

- Dishonored — systèmes systémiques, létal/non-létal, conséquences.
- Hitman World of Assassination — connaissances, opportunités, sandbox, replay.
- Metal Gear Solid V — reconnaissance, préparation, CQC, létal/non-létal.
- Shadows of Doubt — ville persistante, routines, preuves.
- Kingdom Come Deliverance — progression par pratique.
- RDR2 — vie quotidienne et simulation.
- Vampire Bloodlines — factions et social/surnaturel.
- Witcher 3 — préparation, bestiaire, folklore.
- Control — anomalies, recherche, documents, containment comme inspiration conceptuelle.
- Alan Wake 2 — investigation et espaces de pensée.
- Prey — liberté systémique.
- Persona — calendrier et vie sociale.
- Bully — vie scolaire.
- Detroit / Until Dawn / The Quarry — conséquences et mortalité.
- Disco Elysium — compétences comme processus/voix.
- Watch Dogs — information et téléphone.
- Ghost Recon — reconnaissance/préparation.
- Dying Light — jour/nuit et mobilité.
- Cyberpunk — ville/technologie/UI.
- Supernatural — structure case-of-week + mythologie + bestiaire + humour/drame/horror.

## Technologie

### Unreal
PCG est conçu par Epic pour aller des utilitaires d'assets jusqu'aux bâtiments, biomes et mondes entiers.

### Unreal MCP
IvanMurzak/Unreal-MCP expose un pont entre agents MCP et Unreal Editor. La documentation du projet indique un plugin UE, un sidecar .NET, des outils typés et un mode local.

### Blender
mcp-blender-agent privilégie des opérations typées et structurées plutôt que des scripts Python improvisés.

### Kiln
Kiln propose une approche locale où l'agent écrit un programme de géométrie procédurale, reçoit des rendus et contrôles structurels, puis révise.

### Agent Harness
Unreal Agent Harness formalise une boucle :
act → capture → decode → read → correct.
Il impose aussi une sérialisation des mutations de l'éditeur.

### AutoUE
AutoUE explore une architecture multi-agent pour génération de jeux Unreal avec retrieval de documentation et playtesting automatisé.

### CraftBench-UE
CraftBench-UE montre qu'un asset peut être correct alors que le gameplay runtime est faux : les tests runtime doivent donc être explicites.

## Sources actuelles vérifiées

- https://github.com/per-simmons/unreal-agent-harness
- https://github.com/ddalkakgames/codex-gamedev-harness
- https://github.com/PoBruno/mcp-blender-agent
- https://github.com/hotspoons/blender-agent
- https://github.com/matthew-kissinger/kiln
- https://github.com/IvanMurzak/Unreal-MCP
- https://github.com/IvanMurzak/GameDev-MCP-Server
- https://github.com/Pluto156/AutoUE
- https://arxiv.org/abs/2609.23142
- https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-overview

## Reddit / retours terrain

Les retours récents montrent que :
- les workflows spécialisés multi-agents sont plus crédibles qu'un générateur unique ;
- Blender MCP + Unreal MCP est déjà utilisé comme chaîne ;
- la génération 3D nécessite souvent plusieurs passes ;
- la recette « objectif + référence + règles + vérification » est particulièrement utile.

## À faire

Le catalogue externe doit être enrichi par une collecte systématique des Awesome Lists et répertoires de ressources déjà existants, puis dédoublonné et scoré pour Outsider.
