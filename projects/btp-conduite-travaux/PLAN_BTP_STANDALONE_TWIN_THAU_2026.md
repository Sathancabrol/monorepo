# BTP Studio autonome — jumeau numérique dépôt + chantier Thau (plan technique 2026)

**Établi le : 23 novembre 2026** · **Statut : benchmark et plan d'intégration, non livré.**
**Objectif non négociable : BTP Studio s'exécute seul, sans Watchtower, sans abonnement ni crédit obligatoire.** Watchtower est un connecteur facultatif.

## Expérience utilisateur

- Lancement direct BTP Studio (web localhost ou package Windows).
- Scène 3D locale : zoom depuis une carte d'Occitanie/Thau vers un **dépôt sélectionné** (géométrie réelle si disponible, détails de cour explicitement importés ou reconstitués).
- Même scène 3D : HUD **BTP INTEL**, arborescence Dépôt > zones > stocks / Chantiers > affaire > lot > ouvrage > phase > tâche / Engins / Personnel (accès contrôlé) / Documents.
- Clic « chantier prioritaire » => caméra cadrée sur la vraie emprise ; sélectionner chantier, basculer terrain/coupe/réseaux/engins, slider 4D (prévisionnel vs constaté), lien documents/fiches.
- Activation via clic dans la scène **ou** icônes/tuiles des 23 modules actuels. Modules métier conservés et testés, pas simplement des boutons décoratifs.
- Information **live** seulement quand un flux autorisé existe et que sa fraîcheur est affichée. Reste = import, historique, prévu, simulation, ou inconnu.

## Principaux repos libres vérifiés / en évaluation

| Rôle | Outil | URL | Licence | Intégration conseillée |
|---|---|---|---|---|
| Scène géospatiale | CesiumJS | https://github.com/CesiumGS/cesium | Apache-2.0 | Moteur principal 3D géoréférencé dans BTP Studio autonome |
| IFC BIM | That Open Engine | https://github.com/ThatOpen/engine_components | MIT | Viewer et propriétés IFC; prototype intégration Cesium via exports glTF/3D Tiles |
| Exemple appli BIM complète | IFC Viewer | https://github.com/chilldanil/ifc-viewer-app | MIT | Étudier code et intégration bibliothèque/desktop, coupes, sélections, édition de propriétés |
| Exemple de 4D complet | 4DBIM | https://github.com/iman48HK/4DBIM | MIT | Réutiliser logique Gantt ↔ objets BIM, adapter au WBS/phasage VRD |
| Desktop BIM | Bonsai / IfcOpenShell | https://bonsaibim.org/studio.html ; https://github.com/IfcOpenShell/IfcOpenShell | Bonsai GPL-3.0+, libs selon sous-projet | Production IFC locale, pas dépendance runtime |
| SIG local | QGIS / Qgis2threejs | https://qgis.org ; https://github.com/minorua/Qgis2threejs | GPL / vérifier plugin | Créer MNT, aligner géoréférences, exporter glTF |
| Nuages LiDAR | Potree | https://github.com/potree/potree | open source (vérifier termes exacts du composant) | Visualiser gros points LAZ, tester performance avec GTX 1060 |
| Photogrammétrie | WebODM / ODX | https://github.com/WebODM/WebODM | AGPL-3.0 | Outil de production hors runtime; copie GPL/AGPL à encadrer |
| SIG web/desktop | GeoLibre | https://github.com/opengeos/GeoLibre | MIT | Inspirer couches et outils, éviter doublon avec Cesium |
| CAO/BIM exécutable | OpenConstructionDesign | https://github.com/datadrivenconstruction/OpenConstructionDesign | AGPL-3.0-only | Benchmark édition BIM/IFC, Windows zip ; ne pas intégrer son code sans revue licence |
| Traitement 3D Tiles | Digital Twin Toolbox | https://github.com/geosolutions-it/digital-twin-toolbox | GPL-3.0 | Expérimental / pas production-ready : tester conversion LAS + Shapefile en 3D Tiles |
| Viewer LiDAR léger | LiDAR HD Viewer | https://www.data.gouv.fr/reuses/lidar-hd-viewer | licence libre à créditer | Preuve de concept de récupération COPC sur emprise |

Les descriptions de fonctionnalités viennent des pages projet et nécessitent un essai sur des fichiers réels ; **aucune intégration des dépôts tiers n'est déclarée livrée**. Revoir licences transitoires des assets tiers et termes géoservices. Les projets sous AGPL/GPL ne sont pas « copiables sans conditions » ; préférer l'usage séparé ou implémentations conformes.

## Données géographiques disponibles en France

- **BD TOPO** (bâtiments, routes, infrastructures), **BD ORTHO**, **RGE ALTI**, cadastre, GeoJSON, OSM : fond et emprises en open data sous conditions de crédit.
- **LiDAR HD IGN** : sol / sursol / bâtiments / végétation ; produits MNT, MNS, nuages classifiés LAS/LAZ. Données lourdes (dalle 1 km² potentiellement 0,5–2 Go), découpe par emprise avant visualisation.
- Le **téléchargement des dalles spécifiques d'un site du bassin de Thau doit être vérifié** sur https://cartes.gouv.fr/telechargement/IGNF_MNT-LIDAR-HD et portail LiDAR HD ; les pages nationales ne garantissent pas la disponibilité/qualité pour chaque adresse.
- Sète Agglopôle Méditerranée est un territoire de **14 communes** ; son catalogue propre sur data.gouv ne fournissait, lors de cette recherche, que deux jeux de données sans modèles 3D du dépôt ni suivi d'exécution des chantiers. Ne pas supposer qu'un dépôt réel, ses stocks ou ses chantiers sont téléchargeables.
- Pour un dépôt : adresse/emprise > fond IGN > volume/hauteur approximative bâtiment > relevés autorisés, inventaire d'entreprise, photos intérieures, plans, photos/drone avec droits > scène détaillée.
- Pour un chantier : emprise géolocalisée > topo MNT > plans DCE > ouvrages IFC/GLB/GeoJSON > WBS/Gantt > tâche/engins > suivi journalier.
- Réseaux enterrés : les données OSM ou aériennes ne font pas foi. Les plans opérateurs et procédures **DT-DICT** via https://reseaux-et-canalisations.ineris.fr/ sont nécessaires avant travaux ; l'affichage dans l'app doit garder source/precision/classe de réseau et statut de validation.
- Les données LiDAR n'indiquent pas la présence actuelle de personnes, engins, matériaux, état d'un chantier **aujourd'hui**. Pas de surveillance individuelle sans base légale, transparence et contrôle d'accès.

## Pile cible et interfaces

```
BTP STUDIO (application autonome / localhost / package Windows)
  |
  +-- Shell 3D (CesiumJS) : terrain, bâtiments, caméra, calques, outil focus
  +-- HUD BTP INTEL (arborescence ; recherche ; inspecteur ; KPIs sourcés)
  +-- BTP Core (23 modules métier existants : tâches, Gantt, coûts, RH, flotte, stock, DOE)
  +-- Model Bridge (IFC -> fragments ou glTF ; GIS -> GeoJSON/3D Tiles ; LiDAR -> points/MNT)
  +-- Scene Editor (sélection/move/scale/undo, tranchées, chaussées, réseaux, coupes et volumes)
  +-- 4D Planner (phase > tâche WBS > géométries > état prévu/réel)
  +-- SQLite/IndexedDB + fichiers locaux, sauvegarde et export avec provenance
  +-- Connectors OPTIONNELS : Watchtower, GPS, capteurs, flux terrain, IA locale CRONOS/Ollama
```

Les services entre moteur scène et BIM doivent être une couche d'adaptation; les objets géoréférencés sont attachés par ID, pas par noms de mesh aléatoires. Un seul contexte caméra/session dans BTP. Prévoir affichage dégradé pour GTX 1060 6 Go + 16 Go RAM / ordinateur portable GTX 1650 4 Go ; téléchargement à la demande, LOD et paramètres GPU.

## Méthode de démonstration avec un site de Thau

1. Choisir un **site réel précis** dans le territoire de Thau, avec coordonnées ou adresse et autorisation d'utiliser ses données. On peut commencer avec un dépôt anonymisé ou une parcelle publique.
2. Contrôler les dalles LiDAR HD / BD TOPO disponibles ; télécharger uniquement l'emprise utile, documenter précision et millésime.
3. Générer un terrain et les volumes des bâtiments; permettre l'inspection et une visite en orbite/première personne.
4. Ajouter cour, racks, engins et stocks depuis inventaire test **DEMO** étiqueté; créer l'arborescence et les objets cliquables.
5. Ajouter une emprise chantier de Thau ou un dossier Barbazan d'archives **historique**, jamais marqué « en cours » si ce n'est pas le cas. Pour un vrai chantier Thau, demander plans/emprise et autorisations.
6. Ajouter ouvrages VRD : terrassement, tranchée, couches, réseaux, phasage, tâches Gantt et coûts ; vérifier correspondance un à un des IDs métier.
7. Tester parcours complet **BTP Studio démarré sans Watchtower**, y compris offline. Rapport automatisé et captures sur vrai matériel.

## Critères de succès / tests indispensables

- [ ] `npm run dev` ou exécutable BTP ouvre la **scène 3D locale** sans Watchtower, tokens payants ou connexion réseau obligatoire.
- [ ] Les **23 modules** restent accessibles et exécutent leurs fonctions (pas seulement des onglets).
- [ ] Dépôt sélectionnable par clic 3D et par vignette ; mêmes données et même identifiant.
- [ ] Arborescence chantier triable par montant / risque / délai ; raison de classement exposée.
- [ ] Clic sur chantier cadre l'emprise ; retour au dépôt, persistance état caméra.
- [ ] IFC/GLB/GeoJSON réels importés avec contrôle CRS, altitude, dates, provenance.
- [ ] Coupe, mesure, géométries VRD et sous-sol visibles, précision réseau explicitée.
- [ ] Phasage 4D lié au planning, tâches, quantités et écarts de réalisation.
- [ ] Données fictives et temps réel distingués et horodatés ; droit d'accès à la localisation des personnes.
- [ ] Perte réseau propre, données locales disponibles, fonctions non disponibles signalées.
- [ ] Scénarios de calcul 100 m² × 0,30 m = 30 m³ ; tranchée = 60 m³ ; imports invalides rejetés.
- [ ] Tests Windows + charge GPU/fps sur GTX 1060 ; aucune disparition des 23 modules.

## Stratégie prioritaire

Livrer d'abord la **tranche verticale totalement fonctionnelle** BTP Studio autonome → sélectionner dépôt réel/DEMO → ouvrir BTP INTEL → sélectionner chantier → vol caméra → terrain + réseaux + phase Gantt → fiche outil/tâche → modifier état → sauvegarder/recharger. Ensuite étendre les vingt-trois modules sur la même base ; ne pas attendre un moteur BIM industriel complet avant une première tranche vérifiable.
