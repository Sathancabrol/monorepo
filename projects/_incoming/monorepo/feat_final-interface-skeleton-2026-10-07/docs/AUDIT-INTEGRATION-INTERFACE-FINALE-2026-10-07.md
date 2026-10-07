# Audit d'intégration — interface finale Cognitorium
Date: 2026-10-07

## Décision d'architecture
monorepo devient la coquille d'intégration et l'interface finale. Les dépôts sources restent les autorités de référence tant qu'une brique n'a pas été migrée, testée et validée.

Règle: inventaire → catégorisation → meilleur prototype → point d'entrée UI → branchement → test → suppression éventuelle des doublons.

## Dépôts audités
| Dépôt | Branches | Apport principal |
|---|---:|---|
| COGNITORIUM | 4 | CLE + Watchtower mods + architecture agents |
| proto-cognitorium | 8 | UI, profils, graphes, ROME, CV, decay, lab |
| ETAT-DE-LART-PSYCHOLOGIE | 9 | atlas scientifique, lab, agents recherche, cosmos |
| HCSM | 3 | ontologie cognitive, preuves, incertitude, temporalité, validation |
| reaserch-engine | 1 | recherche orchestrée, evidence graph, contradictions, sufficiency |
| Language-decoder | 3 | decoded-human, ontology, inference, dynamics, dashboard |
| watchtower | 5 | monde 3D, territoire, intel, OSINT, chantier, monitoring |
| animation-chronos | 1 | expérience temporelle, inspection, progressive discovery |
| monorepo | 8 | intégration, BTP, Frontignan, catalogue outils, Nexus OS |

## Branches à forte valeur
### Watchtower
arena/dec9cd88-watchtower apporte le dossier INTEL territorial, Frontignan/Thau, import CSV, projets, lacunes, veille officielle, sources, imprévus TP, dossiers chantier et traçabilité.

arena/01a072e1-watchtower ajoute une architecture UI particulièrement réutilisable: barre unique de fonctions, volant, carte 2D, panneau FIL, niveaux INTEL, dossier territorial et contrôle de rendu.

### Monorepo
arena/01a08385-monorepo apporte Nexus OS: routeur multi-provider, agents, créateur d'agents, skills, tools, MCP, mémoire, runtime, tâches, evals, sandbox et SSE.

arena/01a08449-monorepo apporte le module BTP: corpus documentaire, DCE, étude de prix, DT/DICT/AIPR, suivi, DOE, plans, rapports et dashboard théorie/état de l'art/in-situ.

feat/tool-data-catalog-2026-10 apporte le registre structuré des outils.

### Cognitorium / proto
Actifs à préserver: graphe de compétences, profils, ROME, CV alignment, decay, preuves, épistémique, expériences, psychologie, graphes réseau et temporels, validation.

### HCSM
HCSM doit rester le vocabulaire canonique pour construct, observation, evidence, provenance, uncertainty, context, temporal state et inference.

### Research Engine
Moteur: question → plan → retrieval → evidence → claims → contradictions → synthesis → verification → sufficiency.

### Language Decoder
La branche Python arena/01a05471-language-decoder apporte ontology, decoder, inference, dynamics, functioning, profile, evidence et schema decoded-human.

### Animation Chronos
À intégrer comme composant d'expérience temporelle, pas comme application séparée.

## Taxonomie finale
1. Command Center
2. World / Territory
3. Intel / OSINT
4. Projects / BTP
5. Human / Cognition
6. Knowledge / Research
7. Learning Engine
8. Simulation / Lab
9. Design / CAD / Fabrication
10. Nexus / Agents
11. Data / Memory / Provenance
12. System / Settings

## Premier squelette
Branche: feat/final-interface-skeleton-2026-10-07.

Fichiers ajoutés: app/templates/interface.html, app/static/interface.css, app/static/interface.js, data/interface_registry.json, docs/AUDIT-INTEGRATION-INTERFACE-FINALE-2026-10-07.md.

Routes: /interface et /api/interface-registry.

Le squelette affiche 12 domaines, leurs capacités, leur statut et la matrice source → cible.

## Gaps prioritaires
À intégrer: Watchtower territoire/Intel, BTP, Nexus OS, catalogue outils, Language Decoder, Research Engine, HCSM validator et CLE.

À construire: modèle de données commun, registre de modules branchés, navigation globale, mémoire unifiée, provider abstraction, recherche globale, workspace projets, simulation sandbox, CAD/fabrication, coffre de clés local et permissions/privacy.

## Règle de migration
Ne pas copier aveuglément les dépôts. Le monorepo devient une plateforme de modules avec une navigation et un modèle de données communs. Les dépôts historiques deviennent sources d'implémentations, données, tests et références.

## Prochaine passe
Construire la matrice détaillée: fonction → dépôt → branche → fichier/module → état → meilleure version → dépendances → destination monorepo → test.

Statuts: KEEP, IMPORT, ADAPT, MERGE, REBUILD, MISSING, DEFER.
