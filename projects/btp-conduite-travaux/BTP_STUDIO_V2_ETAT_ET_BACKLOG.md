# BTP Studio V2 — état, limitations et backlog maximal

> Branche de développement : feat/btp-all-modules-workbench-20261123
> Objectif : suite BTP gratuite/local-first, de l'analyse de l'offre à la livraison du DOE, riche en visualisations et en outils métier.

## Livré dans la branche V2

| Composant | Fichier | Fait | À ne pas confondre |
|---|---|---|---|
| Dashboard | index.html | 21 modules historiques préservés, navigation corrigée, style amélioré, accès à 2 nouveaux modules | Certaines données de l'ancien cockpit sont fictives |
| Atelier 3D | atelier-3d.html | tranchée, talus/bassin, chaussée multicouche; dimensions, vues, poignées, rotation, zoom, calques, phasage, quantités, exports et sauvegarde locale | rendu 3D par projection Canvas, pas encore un BIM/IFC ou un moteur WebGL |
| Fiches métier | fiches-taches.html | 15 opérations du DCE au DOE, séquences, moyens, risques, prérequis, calculs indicatifs, contrôles, recherche, exports | fiches initiales non exhaustives et non contractuelles |

Les rendements, coûts, vitesses, météo, montants et noms d'entreprise non sourcés restent **illustratifs**. Ne pas présenter les anciens « PDF conformes » ou pseudo-certifications du prototype comme des documents opposables. Une validation par l'utilisateur et les pièces contractuelles réelles reste obligatoire.

## P0 — sûreté et fiabilité (priorité absolue)

- [ ] Audit automatique de toutes les interactions, calculateurs, rendus et exports des 23 modules.
- [ ] Extraction du grand HTML monolithique en modules séparés avec une seule table de navigation.
- [ ] Données typées et versionnées : affaire, lot, ouvrage, tâche, ressources, moyens, contrôles, preuves, DOE.
- [ ] Distinguer systématiquement DONNÉE RÉELLE, SIMULATION, EXEMPLE, IMPORT et SOURCE VÉRIFIÉE.
- [ ] Détecter valeurs irréalistes, trous de séries, champs vides, dérives de prix et unités incohérentes.
- [ ] Suite de tests de calcul et de non-régression; gestion d'erreurs et d'accès sans réseau.
- [ ] Supprimer toute affirmation trompeuse de certification / conformité automatique.
- [ ] Sauvegarde locale robuste, import/export versionnés, intégrité et restauration.
- [ ] Installer les dépendances sous licence compatible, packager pour Windows et Android, mode offline.

## P1 — Design et UX premium

- [ ] Système de design global (couleurs, typographie, densité, composants, grilles, icônes).
- [ ] Shell : sidebar stable, onglets, fil d'Ariane, recherche globale, command palette, favoris.
- [ ] Modes conducteur / chef / opérateur / dirigeant / étudiant, novice ou expert.
- [ ] Cartes chantier synthétiques avec progression par tâche, lot, coût, délai et risques.
- [ ] Graphiques de courbe en S, histogrammes ressources, cash-flow, comparateur prévu/réel.
- [ ] Gantt pilotable par glisser-déposer, dépendances, plan de charge et alertes de conflit.
- [ ] Cartographie SIG par calques, légende, provenance de chaque couche et filtrage.
- [ ] Tableaux avancés : tris, colonnes personnalisables, filtres, historique et vues sauvegardées.
- [ ] Responsive terrain, clavier, tactile, contrastes AA, réduction des mouvements.

## P1 — Atelier 3D géométrie et édition

- [ ] Migrer les modèles vers WebGL/Three.js/Babylon avec fallback adapté aux PC modestes.
- [ ] Editeur d'objet : sélection, déplacement, rotation, dimensionnement, multi-sélection, undo/redo.
- [ ] Grille d'accrochage, règles, unités, repères NGF, géoréférencement et profils long/travers.
- [ ] Terrain MNT/XYZ/GeoTIFF, import topographie, maillages déblais/remblais, volumes différentiels.
- [ ] Tranchées : profil paramétrique, talus, blindage, lits de pose, enrobages et remblaiement.
- [ ] Réseaux secs/humides : conduites, gaines, regards, altimétrie, pentes et conflits.
- [ ] Chaussées : géométrie, couches de structure, bordures, caniveaux, pentes et métrés.
- [ ] Bassins, talus et fossés, zones humides, rampes d'engins, cheminements et emprises.
- [ ] Bibliothèque d'objets 3D libres (engins, accessoires, éléments VRD), import GLB/glTF.
- [ ] Export glTF, DXF via convertisseur, IFC via schémas appropriés et contrôle des exports.
- [ ] Phasage 4D relié à une vraie activité du Gantt avec quantités et temps restants.
- [ ] Coupe dynamique, annotations 3D, points de mesure, calques géoréférencés, images de chantier.
- [ ] Simulation de circulation et manœuvres, rayon de braquage et zones de danger.
- [ ] Contrôle qualité du maillage, collisions, incohérences géométriques, tolérances.

## P1 — Fiches de tâche exhaustives

- [ ] Décomposer chaque poste de BPU en WBS jusqu'à l'opération élémentaire sans doublons.
- [ ] Sous-niveaux par métiers : études, marché, implantation, déblais, remblais, réseaux, voirie, enrobés, contrôles, réception, DOE.
- [ ] Détails systématiques : moyens humains, engins, outils, fournitures, consommables, EPI, logistique.
- [ ] Temps d'installation, transport, cycle pelle, chargement, attente, pause, repli et aléas.
- [ ] Formules tracées et testées : cubatures, foisonnement, compactage, densités, rendement, rotations, coût.
- [ ] Critères de contrôle selon CCTP/CCAG/CCTG/normes pertinentes, datation et bibliographie.
- [ ] Photos d'exemple, coupe 3D liée à la fiche, tâche cliquable dans le jumeau numérique.
- [ ] Enregistrer prévisionnel et observé, rapprocher rendement réel et théorique.
- [ ] Fiche terrain compacte avec points d'arrêt, date, responsable et preuves jointes.
- [ ] Déclencher documents requis et vérifier complétude avant réception.

## P2 — Gestion économique et exploitation

- [ ] Import DCE, BPU, DQE, SDP, devis fournisseurs, métrés et plans.
- [ ] Déboursés secs détaillés, prix unitaires, frais de chantier, frais généraux, marge, aléas.
- [ ] Matériel : VGP, maintenance, exploitation, disponibilité, consommables et réparations.
- [ ] Fournisseurs, sous-traitants, demandes de prix, bons de commande, livraisons et stocks.
- [ ] Planning équipes/engins, prévisions météo sourcées, arrêts et justificatifs.
- [ ] Contrats, situations, décomptes, avenants, travaux supplémentaires et trésorerie.
- [ ] Journaux RDC, photos, pointage, observations, essais et écarts.
- [ ] Déchets et terres : classement, traçabilité, transporteurs et exutoires.
- [ ] Non-conformités, demandes de validation, levées de réserves et historique.

## P3 — Documents, automatisation et IA

- [ ] Génération sûre de rapports de chantier, BPU/DQE, OS, PV, plans de récolement et DOE.
- [ ] GED structurée, versions, signatures légales hors-prototype, références croisées, métadonnées.
- [ ] OCR documentaire *optionnel* pour plans et documents scannés, contrôles humains obligatoires.
- [ ] Assistant métier local, citations de chaque réponse vers les pièces contractuelles.
- [ ] Agent d'analyse DCE, écart devis, checklist DOE, suivi journaliers, avec approbation avant écriture.
- [ ] Routage local Ollama prioritaire, cloud gratuit facultatif, pas d'abonnement obligatoire.
- [ ] Mode hors ligne sur PC et mobile, synchronisation explicite et piste d'audit.
- [ ] Benchmark modèles/calculateurs avec jeux de tests métier et mesures de précision.

## Architecture cible

Affaire → marché → lot → ouvrage → tâche → ressources → métriques et coûts → contrôle → preuve → document → réception.

Exiger traçabilité par source, date et version. Distinction claire hypothèse / relevé / quantité contractuelle. Le chantier pédagogique Barbazan et les dossiers existants doivent constituer les scénarios de tests.

## Tests de référence obligatoires

| Scénario | Entrée | Sortie attendue |
|---|---|---|
| Terrassement naturel | 100 m² × 0,30 m | 30 m³ avant foisonnement |
| Tranchée trapézoïdale | largeur fond 2 m, profondeur 1 m, talus 1H/1V, longueur 20 m | largeur tête 4 m, section 3 m², volume 60 m³ |
| Couches de chaussée | 100 m², 25 cm GNT, 12 cm GB, 6 cm BBSG | 25, 12, 6 m³ respectivement |
| Phasage | 4 étapes liées à une tâche Gantt | géométrie et quantités synchronisées |
| Import invalide | JSON corrompu | rejet sans modification de l'état |
| Hors ligne | ouverture locale | aucun abonnement obligatoire |
| Normes/sécurité | règle non documentée | signalement, aucune « conformité » fictive |

## Définition d'une V2 complète

Faire effectivement le cycle **DCE → étude de prix → préparation → planning → modélisation et métrés → suivi terrain → contrôles → réception et DOE** sur un dossier exemple, avec des résultats traçables et exportables, une interface testée et aucune fonctionnalité déclarée livrée sur la seule présence d'un bouton.

## Journal — 24 novembre 2026, 14 h 55

- Commit `7ab1b4573ebf42339d6aecc453db60f6589fa9fb` : contrôle des décalages calendaires entiers, bornes AAAA-MM-JJ et durée calculée maximale de 10 000 jours (alignée sur la durée imposée).
- Relecture distante du correctif effectuée. Tests moteur et UI non exécutés ; ne pas considérer le P0 validé.
- À tester : 29 février, passage d'année, dépassement 9999-12-31, durée 10 001 jours, tâche nulle, chaîne de dépendances, validation numérique du commit précédent.
- Veille relue ; aucune dépendance intégrée. Restent notamment précision financière, provenance, dépendances et sauvegarde.


### 2026-11-24 — validation provenance et régression moteur

- Commit `ecde3efe3668eed7cb920cd9c1146bcc0ae10eb2` : rejet des provenances explicites inconnues ; absence de provenance conserve le comportement historique.
- 19 assertions JavaScript exécutées avec succès avant publication : exemple 1830 € / 6 jours, trois provenances admises, cinq invalides, quatre types numériques invalides, deux limites calendaires, deux dépendances invalides et durée excessive.
- Tests navigateur non exécutés ; précision financière et provenance absente restent à traiter. Aucun ajout de dépendance ni intégration AEC.


### 2026-11-25 — fiabilité financière et provenance historique

- `a9740685a16a41389f940021fb78efb9d0d0c275` : avertissement coûts réels partiels.
- `0ddfcfac7907dc022422b6c03be97728971885bd` et `9aa39df8f24309e3eb7a52dc7dd8e7c079fbba21` : arrondis décimaux et garde-fous en centimes, tests financiers.
- `f477779cbd9ca1167c1161ac337578599c8c9572` : provenance absente normalisée en `unknown`, avertissement explicite ; les trois provenances historiques explicites restent admises.
- `734b5523703be96db767d54b81ed13279ecf6756` : test de provenance, aller-retour et rejet des valeurs inconnues non prévues.
- Preuve : 19/19 scénarios exécutés sur le moteur modifié dans un environnement JavaScript avec adaptateur minimal des assertions Node. Commande native à reproduire : `node --test projects/btp-conduite-travaux/tests/project-core.test.cjs`.
- À faire : adapter et tester tous les affichages/imports/exports de provenance, vérifier les parcours navigateur et exécuter Node natif. Aucun critère P0 global clôturé. Les données déjà normalisées en `user` ne peuvent pas être rétroactivement identifiées sans source.
- Veille existante relue ; aucune dépendance ajoutée ni nouveau benchmark AEC.
