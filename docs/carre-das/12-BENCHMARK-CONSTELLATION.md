# Benchmark — les types d'affichage pour la vue Constellation

**Date** : 9 octobre 2026 · **Question** : quels types d'affichage existe-t-il
pour présenter un graphe de connaissances (nœuds + liens) dans une app sombre,
offline, sans dépendance externe ?

---

## 1. Ce qui existe dans nos propres repos

| Source | Type d'affichage | Ce qu'on en retient |
|---|---|---|
| `projects/_incoming/.../frontignan/atlas/` — **atlas.js** (1 266 l.) | **Trois lectures d'un même graphe** : réseau force-directed (style Obsidian), carte heuristique radiale, slides. Zéro dépendance, vanilla JS + SVG | C'est notre modèle. Moteur force maison : répulsion O(n²) + ressorts + collision douce + amortissement. Paramètres `charge` et `dist`. Layouts : force / rings / cluster |
| `projects/_incoming/.../frontignan/atlas/data/atlas.json` | **79 nœuds typés, 167 liens typés, 17 jeux de données, 11 slides**, 9 couleurs de type, 5 échelles (Frontignan → France) | C'est notre **système nœud/objet d'intérêt**, déjà construit pour le bassin de Thau |
| `projects/HCSM/figures/evidence-graph/knowledge-graph.md` | Graphe de connaissance en mermaid (construct → définition / théories / tâches) | Règle visuelle retenue : **aucun nœud personne, aucune valeur numérique** dans un graphe conceptuel |
| `projects/frontignan/figures/` (14 PNG) | Figures matplotlib : entonnoir, population, budget, frise, SWOT, priorisation, parties prenantes, mobilités | Les nœuds de l'atlas portent ces figures (`img`) — le graphe et les données chiffrées sont liés |
| `projects/ETAT-DE-LART-PSYCHOLOGIE/output/visual/` | Diagrammes d'état de l'art (matrice méthode, diagrammes) | À citer comme antécédent de visualisation sombre |

## 2. Ce qui existe sur le web (benchmark 2026)

| Outil / approche | Type | Licence | Pourquoi il compte |
|---|---|---|---|
| **Obsidian — Graph view** | Force-directed 2D, canvas, thème sombre, nœuds colorés par dossier, liens fins, zoom/pan, clic = ouvrir la note | propriétaire | **La référence** du « style constellation ». C'est ce que l'utilisateur a nommé |
| **CosmoGraph 3D** (plugin Obsidian) | **Planète 3D** : nœuds sur une sphère, relief procédural, rotation pour naviguer | communautaire | **La référence du « système planétaire »** — un monde borné plutôt qu'un canevas infini |
| **Cytoscape.js** 3.34 | Canvas, algorithmes (centralité, communautés), force layout | MIT | Trop lourd pour nous (5,7 Mo) mais la référence pour l'analyse |
| **vis-network** 10.1 | Canvas, physique, drag/drop, clustering | Apache-2.0/MIT | Bien pour l'édition interactive, pas pour la lecture |
| **Sigma.js** 3.0 | **WebGL**, graphology, grands graphes | MIT | Si un jour le graphe dépasse ~2 000 nœuds |
| **FalkorDB Canvas** | Web component standalone, force layout, canvas, thème sombre, viewport culling | OSS | Prouve qu'un graphe force-directed autonome tient dans un composant vanilla |
| **react-force-graph** | D3 force, 2D/3D/VR | MIT | Nécessite React + D3 — exclu (pas de build, pas de CDN) |

**Règle 2026 du benchmark** (PkgPulse) : *Cytoscape pour l'analyse, vis-network
pour l'édition, Sigma pour les très grands graphes* — et **benchmarker avec le
nombre de nœuds réel avant de promettre**. Nous : ~80–300 nœuds → un moteur
maison vanilla suffit, zéro dépendance, offline garanti.

## 3. Les trois systèmes retenus pour Carré d'As

| Système | Métaphore | Nœuds | Liens | Source des données |
|---|---|---|---|---|
| **Constellation** | Ciel étoilé (Obsidian) | Objets d'intérêt : entités, concepts, compétences métier, acteurs, projets, risques | compose / gouverne / dépend / coopère / finance / tension… | `atlas.json` (79 nœuds, 167 liens) + données live (profils, réunions, cas OSINT) |
| **Planétaire** | Système solaire (CosmoGraph) | Le soleil = Carré d'As · les planètes = les modules · les satellites = les objets du module | orbite = appartenance au module | `/api/modules` + collections du store |
| **Agentique** | Réseau de spécialistes | Les 22 agents | partagent un déclencheur ou une capacité | `agents.json` |

## 4. Ce qu'on construit (et ce qu'on exclut)

**Construit** :
- Moteur force-directed vanilla JS + SVG (inspiré de la physique d'atlas.js :
  répulsion, ressorts, collision douce, amortissement — pas recopié, adapté)
- Zoom/pan, clic nœud → panneau détail, filtres par type, recherche
- Layout orbital pour le système planétaire (orbites concentriques par tier)
- Thème sombre cohérent avec l'app, couleurs par type (palette atlas)

**Exclu** (et pourquoi) :
- Toute bibliothèque externe (D3, Cytoscape, Sigma) → l'app doit rester
  **standalone, offline, sans build**
- Le 3D WebGL → CosmoGraph le fait, mais un navigateur d'entrée de gamme
  sur un poste de mairie doit tenir ; le planétaire est rendu en 2D (orbites)
- Les CDN → interdit, l'app tourne hors-ligne

## 5. Images de référence

**Images web** (téléchargées en local dans `image-search/`, **non versionnées**
— ce ne sont pas nos créations) :
- `image-search/obsidian-graph-view-knowledge-graph-dark-1..3.png` — graph view Obsidian
- `image-search/3d-knowledge-planet-sphere-graph-visuali-*.jpg` — références planétaires

**Images du repo** (versionnées, ce sont les nôtres) :
- `projects/_incoming/.../frontignan/atlas/img/node-*.jpg` — les 10 nœuds illustrés de l'atlas
- `projects/frontignan/figures/*.png` — les 14 figures matplotlib du rapport
