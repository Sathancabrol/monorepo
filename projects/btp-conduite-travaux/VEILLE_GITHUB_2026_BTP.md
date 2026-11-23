# Veille GitHub 2026 — opportunités pour BTP Studio

**Date de veille : 23 novembre 2026**  
**Périmètre :** projet `Sathancabrol/monorepo`, dossier `projects/btp-conduite-travaux`.  
**Statut :** recherche / benchmark, **pas** une dépendance installée ni une intégration testée.

## Méthode

Ne pas confondre « Trending en 2026 » avec « dépôt populaire en 2026 ». Les sources GitHub Trending et historiques mesurent des périodes différentes (jour/semaine/mois) ; certains classements externes mesurent les étoiles gagnées. Les nombres de stars ne prouvent ni qualité, ni sécurité, ni compatibilité. Une bibliothèque mature peut être préférable à un phénomène de mode.

La sélection ci-dessous distingue **A** (popularité notable documentée en 2026), **B** (activité/release 2026, sans preuve de classement général), **C** (fondation mature pertinente). Licences mentionnées selon les pages publiques vérifiées, à recontrôler au moment d'intégrer. **Ne télécharger ni copier de code dans BTP Studio sans vérifier les licences des dépendances et les contraintes réseau/CGU.**

## 1. Repos en hausse ou remarqués en 2026

| Rang BTP | Dépôt | Signal 2026 | Usage concret pour BTP Studio | Licence / risque | Action recommandée |
|---|---|---|---|---|---|
| **P0** | [pascalorg/editor](https://github.com/pascalorg/editor) | A — GitHub Trending en septembre 2026, dépôt actif en novembre | Éditeur 3D local-first, scène modifiable, objets, CLI et MCP. Étudier les interactions d'édition et invariants de scène | MIT. Orienté bâtiment, pas terrassement/VRD natif | Benchmark d'édition de terrain / gizmos / agents, puis prototype réversible |
| **P0** | [opengeos/GeoLibre](https://github.com/opengeos/GeoLibre) | B — forte progression et versions publiées durant 2026 | SIG local/web, couches cartographiques, MapLibre/deck.gl, données géospatiales | MIT. Rust requis pour build bureau ; données externes selon les couches | Prototype calques de chantier GeoJSON et mesure d'emprises |
| **P0** | [tt-a1i/archify](https://github.com/tt-a1i/archify) | A — +36 346 étoiles en septembre selon GitTrend, 2e du mois | Diagrammes de processus, architecture, flux DCE → DOE, arborescences WBS et audits de conception | Apache-2.0 ; compétences d'agent à vérifier avant installation | Produire un diagramme reproductible de l'architecture actuelle |
| **P1** | [bilawalsidhu/gods-eye-view](https://github.com/bilawalsidhu/gods-eye-view) | A — #1 quotidien/hebdo en août selon auteur et forte croissance en septembre | Inspiration 3D SIG, globe, calques interactifs, affichages temps réel | Code MIT ; **conditions et licences propres des fonds cartographiques/sources de données** | S'inspirer des interactions de couches et légendes ; pas copier les flux OSINT |
| **P1** | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | A — forte visibilité en novembre 2026 | Critique UI/UX, qualité des écrans, audit de design, composants | Apache-2.0 | Utiliser les critères comme grille de revue des 23 modules |
| **P2** | [abhigyanpatwari/GitNexus](https://github.com/abhigyanpatwari/GitNexus) | A — présent dans snapshots Trending du 29 août 2026 | Graphe de code, dépendances et flux d'exécution pour refondre le monolithe HTML | **PolyForm Noncommercial**, pas assimilable à MIT/Apache. Ne pas intégrer son code sans revue juridique | Étudier l'approche ; reproduire de manière indépendante avec AST/diagrammes si nécessaire |
| **P2** | [debpalash/VoiceStudio](https://github.com/debpalash/VoiceStudio) | A — premier du classement de septembre 2026 | Dictée/compte rendu terrain local, éventuellement saisie vocale chantier | Vérifier licence réelle, CPU/RAM et disponibilité ; ne pas dupliquer les services déjà présents | Comparer au VoiceStudio local existant avant toute installation |

## 2. Fondations AEC/BTP actives et intéressantes (pas forcément « Trending » en 2026)

| Priorité | Projet | Valeur métier | Licence / attention | Décision |
|---|---|---|---|---|
| **P0** | [ThatOpen/engine_components](https://github.com/ThatOpen/engine_components) et [engine_fragment](https://github.com/ThatOpen/engine_fragment) | Import/visualisation IFC, composants BIM, fragments pour scènes lourdes | MIT pour les projets vérifiés ; vérifier versions compatibles du moteur et Node | Spécifier un prototype IFC autonome et tests mémoire/temps d'ouverture |
| **P0** | [IfcOpenShell/IfcOpenShell](https://github.com/IfcOpenShell/IfcOpenShell) | Traitement et validation de modèles IFC, métrés et classes d'objets | LGPL-3.0 ; binaire/Python externe selon environnement | Étudier un outil d'import/export IFC local |
| **P1** | [opf/openproject](https://github.com/opf/openproject) | Gantt, dépendances, portefeuilles, planning/ressources, tâches | GPL-3.0, application lourde ; préférer approche connecteur/benchmark | Référentiel UX et fonctionnel pour planning et portefeuille, pas copier le code |
| **P1** | [mrdoob/three.js](https://github.com/mrdoob/three.js) | WebGL 3D, gizmos, picking, profils et matériaux pour remplacer la projection Canvas | MIT, veiller au poids du rendu et carte graphique ancienne | Prototype objet modifiable + coupe 3D + tests 30/60 fps |
| **P1** | [opensource-construction/osc-directory](https://github.com/opensource-construction/osc-directory) | Répertoire sectoriel open source AEC (outils BIM, SIG, calcul, DAO, chantier) | MIT pour le répertoire, licences individuelles différentes | Source de découvertes ; ajouter aux comparatifs trimestriels |
| **P2** | [xeokit/xeokit-sdk](https://github.com/xeokit/xeokit-sdk) | Visualiseur BIM performant et précis | **AGPL-3.0**, implications de copyleft fortes ; licence commerciale possible | Veille / benchmark avant toute intégration de code |

## 3. Priorité technique : transformer les dépôts tendance en fonctionnalités mesurables

1. **Studio géométrique modifiable :** comparer la scène V2 à Pascal Editor et Three.js (création/modification/suppression d'objets, coordonnées, snap, undo/redo, caméra, maillages), viser 3 scénarios VRD complets avec quantités recoupées.
2. **BIM/IFC :** prototype séparé ThatOpen + IfcOpenShell ouvrant un modèle IFC de référence, rapportant classes, placements, quantités et conflits de structures ; ne pas fusionner sans tests de performance et licences.
3. **Cartographie :** tester une couche GeoJSON locale avec GeoLibre/MapLibre, calcul de longueurs, surfaces et emprises, croisement avec un chantier réel.
4. **UX premium :** appliquer une checklist inspirée d'Impeccable à chacun des 23 modules, mesurer lisibilité, navigation, cohérence, états d'erreur, clavier/tactile et charge cognitive.
5. **Processus/documentation :** utiliser Archify comme modèle de diagramme versionné pour WBS, DCE, préparation, exécution, réception, DOE et flux de données des agents.
6. **Contrôle du monolithe :** benchmark d'approches de graphe de code sans reprendre GitNexus sous licence non commerciale.
7. **Voix et terrain :** évaluer dictée locale sécurisée dans le RDC et les fiches via l'infrastructure VoiceStudio existante, sans connexion cloud obligatoire.

## 4. Critères avant toute intégration (garde-fous)

- Licence et licences transitives compatibles ; attribution conservée.
- Pas de dépendance à un compte, abonnement, crédit ou clé API payante.
- Mode hors ligne pour les actions essentielles ; tuiles/cartes externes explicitement facultatives.
- Tests sur PC Windows modestes (GTX 1060/1650) et option mobile réduit.
- Import/export de formats ouverts et données réversibles ; sauvegarde de projet avant migration.
- Tests unitaires des unités, métrés, dépendances de planning, prix, validation des IFC et versions.
- Comparaison visuelle et métier avant/après sur chantier pédagogique Barbazan et scénario terrassement 100 m².
- Chaque essai porte un statut clair : **repéré / évalué / prototype / testé / intégré**. Aucun item de cette veille n'est « intégré ».

## 5. Sources vérifiées au 23 novembre 2026

- GitHub Octoverse 2026 : https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/
- Historique mensuel GitTrend septembre 2026 : https://gittrend.io/monthly/2026-09
- Snapshot Trending 29 août 2026 : https://github.com/jalliance/github-trending-snapshot-2026-08-29
- Archive annuelle des gains d'étoiles : https://moststarred.com/trending/year
- Répertoire AEC maintenu : https://github.com/opensource-construction/osc-directory
- Pascal éditeur : https://github.com/pascalorg/editor
- GeoLibre : https://github.com/opengeos/GeoLibre
- BIM That Open : https://github.com/ThatOpen/engine_components
- IfcOpenShell : https://github.com/IfcOpenShell/IfcOpenShell
- xeokit : https://github.com/xeokit/xeokit-sdk

## 6. Notes de fidélité de la veille

« Tendance 2026 » ne signifie pas qu'un dépôt est né en 2026 ou qu'il vient d'être vérifié en production. Certaines métriques proviennent d'agrégateurs tiers et peuvent évoluer. Les classements n'établissent pas la qualité ni la sécurité. La veille sert à choisir des **expériences vérifiables**, pas à cloner des projets entiers et casser BTP Studio.
