# Modules

Les modules sont les capacites fonctionnelles du systeme. Ils ne doivent pas contenir de copie des projets historiques tant qu'une extraction n'est pas validee.

| Module | Role |
|---|---|
| GIS | carte, couches, 3D, geospatial |
| Territory | indicateurs et scenarios territoriaux |
| Chantier | documents, taches, quantites, risques, planning |
| Research | sources, preuves, claims, contradictions |
| Cognition | ontologie, connaissances, competences |
| Learning | simulation pedagogique et transfert |
| Temporal | chronologie, animation, phasage |
| Agents | orchestration inter-modules |
| Language | analyse linguistique |

Le registre machine-readable est `data/module_registry.json`.

Le code partage va dans `core/` ou `modules/`. Les projets sources restent dans `projects/` pendant la migration.