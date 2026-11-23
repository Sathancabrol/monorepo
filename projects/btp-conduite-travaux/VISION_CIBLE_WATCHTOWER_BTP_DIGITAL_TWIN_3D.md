# WATCHTOWER × BTP INTEL — vision cible Digital Twin 3D unifié

**Date** : 2026-11-23
**Statut** : spécification de vision / critères d'acceptation, **non implémenté**.
**Branche de cadrage** : `feat/btp-all-modules-workbench-20261123`
**Priorité** : P0 pour l'architecture cible ; réalisation progressive et testée.
**Principes** : gratuit/local-first, zéro abonnement obligatoire, fonctionnement hors ligne dégradé, traçabilité, contrôle humain, respect de la vie privée.

## 1. Invariant d'expérience

L'interface principale finale est un **monde 3D géoréférencé et persistant** (Watchtower). L'utilisateur peut y entrer par clic sur un objet du monde OU via une icône d'application/vignette/recherche. Les modules (BTP, INTEL, gestion entreprise, RH, engins, dépôts, chantiers, fiches, documents, conception, suivi) sont des **modes/lentilles contextuels superposés** à **une même scène**, pas une juxtaposition de sites, iframes, nouvelles cartes ou caméras isolées.

Les panneaux métier, arborescences, formulaires, timelines, documents, graphiques et tableaux restent possibles **en HUD 2D accessible sur la scène 3D**. Pas de 3D forcée pour de longues écritures ; les documents et l'accessibilité conservent des composants 2D, sans sortie du contexte.

L'utilisateur peut revenir à tout moment aux vues globales, dépôt ou chantier, avec fil d'Ariane, retour caméra, favoris et recherche. Préserver les fonctionnalités existantes pendant migration.

## 2. Parcours canonique de référence : dépôt → BTP INTEL → chantier

1. **Monde Watchtower.** Voir territoire, routes, parcelles, entreprises, dépôts, travaux, actifs, limites administratives. Chaque entité visible doit avoir un identifiant métier stable, source et précision géographique.
2. **Sélection dépôt.** Cliquer sur un bâtiment/une emprise OU ouvrir la vignette BTP > Dépôts. Déplacement caméra fluide vers le dépôt. Mode « dépôt » : bâtiment, cour, zones de stockage, rayonnages, engins, matériel, stocks, accès et circulation. N'afficher personnes/positions que si les données sont effectivement collectées avec droit d'accès, information et consentement/base légale appropriée ; sinon « non disponible ».
3. **BTP INTEL.** Activation contextuelle sans recréer la scène. HUD : alertes, portefeuille chantiers, encours, budgets, équipes, moyens disponibles, retards, livraisons, contrôle sécurité, provenance et fraîcheur des données.
4. **Arborescence des chantiers en cours.** Trier par « importance » explicite et modifiable (montant, délai critique, risque, effectif, marge, ou score pondéré). Ne jamais choisir « le plus important » sans montrer le critère. Déplier affaire > marché > lot > ouvrage > phase > tâche.
5. **Sélection premier chantier.** Centrer caméra sur l'emprise SIG (polygon/centroïde/bounding sphere) ; adapter cadrage, altitude et angle. Conserver HUD, filtres, couches, date et contexte ; possibilité de retour direct au dépôt.
6. **Mode chantier/terrain.** Charger terrain, MNT, ortho, plans géoréférencés, modèles 3D/IFC/GLB, réseaux, installations, engins, ouvrages, zones de travaux et éléments cliquables. Séparer strictement « projeté », « relevé », « réel observé », « simulé », « absent ».
7. **Phasage 4D.** Axe temps et jalons liés aux tâches réelles (Gantt/WBS). Rejouer les phases, comparer prévu/réel, visualiser déblais/remblais, tranchées, pose de réseaux, remblais, couches de chaussée, contrôles, circulation. Curseur 4D non assimilé à un suivi « en direct » sans source de mise à jour.
8. **Sélection d'objet.** Clic sur pelle, conduite, regard, équipe, stock, zone ou phase ouvre fiche lisible : identité, tâche, quantités, coûts, temps, rendement, dépendances, documents, risques, contrôles, preuves, dernière synchronisation. De fiche à objet et d'objet à fiche, aller-retour.
9. **Actions.** Annotation, mesure, coupe, comparaison, demande de validation, rapport journalier, réservation matériel, simulation de scénario ; écriture confirmée par l'utilisateur, historisée, exportable.

## 3. Architecture logique

```text
WATCHTOWER SHELL (scène unique Cesium / carte / caméra / sélection / timeline)
  ├── Monde / SIG / terrain / bâtiments
  ├── Registre d'entités : IDs stables + géométries + provenance
  ├── Gestionnaire de lentilles : INTEL | BTP INTEL | ENTREPRISE | TERRAIN | ...
  ├── Gestionnaire d'actions : focus / zoom / coupe / mesurer / annoter / naviguer
  ├── HUD contextuel : arborescence / inspecteur / timeline / alertes / recherche
  └── Bus événements métier + gestion état / permissions
        ├── BTP Core (affaire, marché, lot, ouvrage, tâche, ressources, preuves, DOE)
        ├── Dépôt et flotte (stock, lieu, rangement, mouvement, affectation, VGP)
        ├── Ressources RH (disponibilité, compétences, équipes ; privacy by design)
        ├── Planning / Gantt / WBS / phasage 4D
        ├── SIG / BIM (GeoJSON, MNT, raster, glTF/GLB, IFC, 3D Tiles si pertinent)
        ├── Documents (DCE, plans, DICT, PV, photos, DOE, versions)
        └── Sources horodatées / synchronisation locale / journaux d'audit
```

**Ne pas avoir 2 scènes en concurrence.** Réutiliser CesiumJS existant dans Watchtower pour les coordonnées, caméra et terrain. Démontrer un petit modèle de dépôt/chantier en glTF/GLB puis implémenter l'éditeur de géométrie, en évaluant Three.js/ThatOpen pour les sous-systèmes spécialisés sans imposer une deuxième navigation ou une réécriture totale. Adapter les objets BTP Canvas actuels ; ne pas appeler « BIM » une simple projection Canvas.

**Source de vérité unifiée** pour les entités :
`entity.id, entity.type, entity.parentId, entity.geometry, entity.crs, entity.source, entity.sourceVersion, entity.recordedAt, entity.updatedAt, entity.validFrom, entity.validTo, entity.confidence, entity.dataMode, entity.permissions, entity.links`.
Lier `companyId/depotId/projectId/lotId/workPackageId/taskId/assetId` ; une ressource peut être au dépôt, réservée, en transit ou affectée à un chantier à un instant donné.

**Événements normalisés** :
- `app.mode.open({mode:'btp-intel',entityId})`
- `world.focus({entityId,bounds,transition:'flyTo'})`
- `site.open({projectId,view:'terrain'})`
- `tree.expand({entityId})`
- `layers.toggle({siteId,layerId,visible})`
- `timeline.seek({projectId,at,comparison:'planned-vs-actual'})`
- `object.inspect({entityId})`
- `state.restore({camera,mode,selection,layers,at})`

Les événements ci-dessus sont des **contrats à développer**, pas des API existantes.

## 4. Modes de lecture de la même scène

- **MONDE / CONTEXTE** : macro territoire et situation.
- **BTP INTEL** : analyses transversales, hiérarchie, synthèses, alertes, chantiers, décisions.
- **DÉPÔT / LOGISTIQUE** : espaces, stock exact, mouvements, équipements, disponibilité, parc.
- **CHANTIER / TERRAIN** : emprise, contexte topographique, installations, équipes, engins, travaux, réseaux.
- **TECHNIQUE / BIM-SIG** : plans, réseaux secs/humides, altimétrie, profils, coupes, collisions, métrés.
- **TEMPS / 4D** : phases, interventions prévues/constatées, simulations, correspondance Gantt.
- **ÉCONOMIE / 5D** : déboursés, quantités, achats, consommé, estimé à terminaison, écarts.
- **QUALITÉ / SÉCURITÉ / DOE** : anomalies, réserves, essais, photos, pièces, preuves, validations.
- **OPÉRATEUR TERRAIN** : interface tactile légère pour saisies, photos et fiches, conservant le contexte.

La sélection d'un ouvrage, d'une tâche ou d'un engin doit être synchronisée entre hiérarchie, rendu 3D, planning, coûts, documents et inspecteur.

## 5. Vérité des données / personnes / temps réel

- **LIVE** seulement avec télémétrie validée, permissions, latence/fraîcheur connues (GPS, balise matériel, pointage métier, captation autorisée). Un objet 3D animé ne prouve pas une observation en temps réel.
- **IMPORTÉ / RELEVÉ** : horodatage, précision, date et source visibles.
- **SIMULATION / PRÉVU** : distinction visuelle permanente, jamais substituée au réel.
- **INCONNU / ABSENT / PÉRIMÉ** : message explicite, pas de personnel, engins ou avancement inventés.
- Personnel : aucune surveillance implicite, ni suivi individuel automatique ; minimisation, bases légales, contrôle d'accès par rôle, journalisation, limitation de conservation.
- Les réseaux enterrés approximatifs (p. ex. OSM) ne valent **jamais** localisation sûre ; exiger pièces et procédures DT-DICT, retours concessionnaires, investigations et validations métier avant intervention.

## 6. Performances et compatibilité

- PC avec GPU ancien (GTX 1060) : LOD progressifs, chargement de tuiles et modèles à la demande, culling, limite de détails des engins, option réduire effets, budget mémoire, pause simulations.
- Mobile : vue interactive simplifiée, HUD tactile, données synchronisées, dégradations explicites ; pas besoin d'un service payant pour les scènes locales.
- Mode local hors ligne : cache géographique et assets autorisés, BTP Core et fichiers locaux disponibles ; services « live » désactivés proprement si indisponibles.
- Accessibilité : navigation clavier, arbre et inspecteur tabulaires, contrastes, réductions animations, export lisible sans dépendance 3D.

## 7. Réemploi direct vérifié le 23 novembre 2026

Dans `Sathancabrol/watchtower` (branche `main`) :
- `src/intelTwin.js` : INTEL et arborescence cliquable.
- `src/chantier.js` : hub métier, phasage, équipes, inventaire, suivi et simulation (fonctionnalités à tester séparément).
- `src/vuesIntel.js` : lentilles INTEL et vues territoriales.
- `src/hq.js`, `src/camera.js`, `src/worldFocus.js` : objets 3D/caméra/focus.
- `src/osmBuildings3D.js`, `src/scenes/*`, `src/tracabilite.js` : bâti, scènes, provenance.

Dans `Sathancabrol/monorepo`, branche `feat/btp-all-modules-workbench-20261123` :
- `projects/btp-conduite-travaux/index.html` + `assets/workbench-v3.js` : 23 modules de travail (dont dépôt, chantiers, équipe, flotte).
- `atelier-3d.html` : éditeur/projection Canvas à migrer pour le vrai 3D.
- `fiches-taches.html`, `assets/project-core-v1.js`, `assets/metres-v1.cjs` : fiches, cœur métier, métrés.
- `BTP_STUDIO_V2_ETAT_ET_BACKLOG.md` : backlog technique préexistant.

**Cible de développement** : aucun module supprimé avant équivalence validée ; adopter le monde Watchtower comme shell commun. Le BTP Studio peut rester lançable séparément **uniquement en mode test, maintenance ou secours**, pas comme une seconde interface principale finale.

## 8. Démonstrateur et tests d'acceptation bloquants

**Scénario étalon** : un dépôt fictif clairement étiqueté DEMO, au moins deux chantiers fictifs et un dossier Barbazan réel importé comme **archive historique/pédagogique**, jamais présenté comme chantier live.

- [ ] Depuis la scène globale, clic sur le dépôt = focus caméra sur la bonne emprise et inspecteur dépôt.
- [ ] Le même focus est accessible par vignette BTP > Dépôts ; les deux chemins aboutissent au même état.
- [ ] Mode BTP INTEL ne recrée pas le globe, ne perd pas la sélection et affiche la provenance.
- [ ] L'arborescence « chantiers en cours » permet classement justifié, dépliage et sélection.
- [ ] Sélection chantier = mouvement caméra et cadrage de l'emprise correcte (avec retour dépôt).
- [ ] Le mode chantier ouvre au minimum les couches terrain, plans, réseaux, ouvrages, engins et phases.
- [ ] Un clic sur un objet ouvre la même fiche liée à son ID dans hiérarchie, 3D et planning.
- [ ] Curseur 4D fait varier ouvrages/étapes et affiche prévu vs constaté sans simuler du live.
- [ ] La géométrie d'une tranchée et les volumes sont reliés à la même tâche que la fiche.
- [ ] Sans télémétrie, aucune position de salarié ni état live n'est fabriqué.
- [ ] Perte Internet : scène locale et documents demeurent accessibles, sources live signalées indisponibles.
- [ ] 23 modules métiers conservés ou re-routés vers des panneaux fonctionnels ; aucun bouton inerte.
- [ ] Import erroné, CRS inconnu, coordonnées incohérentes et données périmées gérés sans corruption.
- [ ] Tests unitaires de métrés + tests navigateur E2E couvrant les parcours et le retour caméra.

## 9. Ordre de réalisation conseillé

**Lot 0 — Audit & données.** Inventaire de toutes les scènes et panneaux existants, références images, objets 3D, source IDs, arborescences, et cartographie de dépendances. Fixer le schéma d'entité commun et le contrat de navigation.

**Lot 1 — Tranche verticale démontrable.** Scène Watchtower → dépôt 3D fictif → BTP INTEL → liste chantiers → focus chantier → couches terrain/phasage → fiche cliquable → retour. Les données peuvent être DEMO explicitement déclarées mais les actions doivent toutes fonctionner.

**Lot 2 — Vrai contenu chantier.** Associer dossier Barbazan, plans, emprises, profils, tâche de terrassement, métrés, phase, contrôle et documents à la scène. Import GEOJSON/GLB/IFC expérimental validé.

**Lot 3 — Compléter 23 modules.** Dépôt/stock, RH, flotte, achats, coûts, planning, calculs, documents, sécurité et suivi, avec tests et provenance.

**Lot 4 — Exploitation et synchronisation.** Journalisation, permissions, états d'actifs, capteurs *optionnels*, offline et multiappareil ; aucun abonnement obligatoire.

**Critère final** : la 3D est le **système de navigation central**, les informations métier restent **vraies, digestes et opérables**. Une scène spectaculaire sans données fiables ni actions n'est pas un jumeau numérique opérationnel.
