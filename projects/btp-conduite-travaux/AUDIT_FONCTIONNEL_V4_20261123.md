# BTP Studio V4 — audit de fonctionnement et état de l'itération

**Date : 23 novembre 2026**  
**Dépôt :** `Sathancabrol/monorepo`  
**Branche de travail :** `feat/btp-all-modules-workbench-20261123`  
**Périmètre :** `projects/btp-conduite-travaux/`

## Définition de « fonctionnel »

- **Présent :** une page ou un contrôle existe. Ce seul état ne prouve rien.
- **Câblé :** un événement déclenche du code et ne pointe plus sur une fonction absente.
- **Statique testé :** syntaxe, identifiants, imports et formules élémentaires contrôlés.
- **Navigateur testé :** parcours et résultat observés dans une version figée par commit.
- **Métier validé :** scénario BTP réaliste, source, hypothèses, calcul, validation, traçabilité, export et récupération vérifiés.

**N'annoncer la complétion du module que lorsqu'il atteint les deux derniers niveaux sur son parcours principal.**

## Bilan des réparations de cette itération

| Module | Développement réel | Validé en navigateur ? | Limite actuelle |
|---|---|---|---|
| Cockpit | Couche Workbench, recherche et diagnostic 23 modules, affichage du dossier actif | Câblage déjà vérifié antérieurement | KPI hérités = exemples |
| Entreprise / trésorerie | Coûts théoriques et valorisation issus du dossier actif | Non (dernière itération) | Pas une comptabilité ni une trésorerie bancaire |
| Dépôt | Entrées/sorties locales, refus stock négatif, consultation, export CSV | Formulaire **visible confirmé** | Plan 2D/3D historique indépendant du stock |
| Hub Chantiers | Gestion CRUD des affaires, tâches, dépendances, Gantt, JSON/CSV | Moteur testé statiquement, interface partiellement vérifiée antérieurement | Pas de gestion contractuelle complète |
| Planning | Vue mensuelle basée sur les tâches + registre local des constats d'intempérie | Pas encore sur commit actuel | Jours calendaires, pas ouvrés ; aucun droit automatique à prolongation |
| Watchtower / SIG | Lecture phasage 4D et contexte projet | Pas encore | Cartes, couches et visualisations à auditer ; pas du temps réel |
| Flotte | Fiches engins, état disponible/affecté/maintenance, contrôle à prévoir, CSV | Formulaire **visible confirmé** | Télémétrie historique fictive, pas d'API GPS |
| Catalogue matériaux | Navigation maintenue, fiche et catégories existantes | Pas encore | Devis et prix historiques à vérifier |
| RH / équipes | Heures théoriques par tâche liées au dossier actif | Non (dernière itération) | Pas de paie ni de pointage RH certifié |
| OPPBTP / balisage | Simulateurs conservés et accès aux contrôles | Non (dernière itération) | Simulation pédagogique, pas un plan de prévention validé |
| Sécurité / AIPR | Briefings imprimables et points de contrôle par tâche | Non (dernière itération) | Jamais de conformité QSE automatique |
| RDC | Rapports réels en localStorage, pointages, livraisons, captures PNG réelles archivées localement | Pas encore sur commit actuel | Validation humaine, stockage navigateur et permissions caméra |
| Mode compagnon | Vue terrain ancienne préservée | Navigation déjà testée antérieurement | Pas de PWA synchronisée/offline complète |
| Obsidian / connaissance | Vue de base documentaire conservée | Non (dernière itération) | Connexion Obsidian à consolider |
| Technique & analyse | Manning-Strickler, ruissellement brut, chute de tension, éclairage explicitement indéterminé sans données, Bruckner éditable | **Hydraulique et électrique validés en navigateur** | Données géotechniques/hydrologiques à confirmer ; pas de conformité normative automatique |
| SDP / DQE | Métres et déboursés unitaires du projet actif | Non (dernière itération) | BPU contractuel/quantités complexes non intégrés |
| Benchmark | Tri des données historiques, affichage PU locaux | Non (dernière itération) | Prix de la concurrence et références externes non vérifiés |
| Fournisseurs / approvisionnement | Annuaire local éditable, tri, recherche, export CSV | Non (dernière itération) | Anciennes cartes commerciales fictives |
| Ledger / audit | Registre historique conservé | Non (dernière itération) | Un hash n'est pas une certification ni une signature |
| Documentation / normes | Contrôles déclaratifs du dossier actif | Non (dernière itération) | Références et normes à vérifier source par source |
| Archives / GED | Archivage réel de fichiers dans IndexedDB, restauration, suppression, SHA-256 optionnel | Non (dernière itération) | Stockage du navigateur non équivalent à un coffre-fort légal |
| Atelier 3D | Tranchée, bassin, chaussée, quantités, lien explicite vers poste de métré | Test navigateur antérieur sur quantités / changements de modes | Projection Canvas 3D simplifiée, pas encore BIM/IFC |
| Fiches tâches | 15 fiches méthodes, recherche et calculs | Test navigateur antérieur : 100m²×0,30m = 30m³ | Bibliothèque non exhaustive ni contractuelle |

## Vérifications réellement effectuées

### Contrôle statique
- **23 panneaux HTML** préservés.
- **372 attributs d'événements HTML** présents; une comparaison conservatrice de leurs appels avec les définitions du JS (classique + correctifs V4) ne trouve plus de nom de fonction manifestement absent. Ce contrôle regex n'équivaut **pas** à une exécution.
- Sept premiers correctifs V4 ont passé l'analyse syntaxique (`new Function`).
- Correction du doublon HTML `btn-layer-osm` entre Watchtower et Fournisseurs ; les commandes sont désormais isolées par module.

### Calculs navigateur sur commit immuable
Référence testée : `cb53d48a23a5c78d0d961da1856a9d0d874035b2`.

- Réseau circulaire **DN300, K100, I=1,50%, h/D=50%** : débit affiché **76,98 L/s** (pleine section 153,96 L/s). Calcul simplifié Manning-Strickler sous hypothèses explicites.
- Monophasé **230V, 1800W, 250m, cuivre, 6mm²** : **14,67V, 6,38%**. Calcul résistif simplifié, pas validation réglementaire.
- Formulaires nouveaux **Dépôt** et **Flotte** présents dans le navigateur.

Un précédent test sur URL de branche montrait les anciens champs constants (le service de prévisualisation semblait mettre en cache une version obsolète). Toujours tester l'**URL d'un commit immuable**, avec les ressources du même commit.

### Anomalies encore ouvertes
- Un test antérieur du diagnostic a capturé **trois erreurs JavaScript**, mais leur détail n'était pas encore affiché dans la version testée. L'interface du diagnostic a été enrichie pour rendre les messages visibles. **À analyser et corriger**.
- Les parcours CRUD complets (saisie, rechargement, suppression et export) de tous les nouveaux modules ne sont **pas encore testés en navigateur**.
- Les **données d'exemple** des modules anciens restent abondantes : empêcher tout amalgame avec le projet actif.
- Certaines anciennes sorties « PDF » sont en réalité des **vues imprimables HTML** ; le RDC V4 imprime honnêtement un brouillon et les sorties historiques portent désormais une mention de démonstration.
- Les modèles de géométrie/sécurité et les modules SIG doivent être testés sans connexion et avec données réelles avant toute production.

## Backlog priorisé des prochaines passes autonomes

1. **P0** Recueillir et résoudre toutes les erreurs JS capturées par Diagnostics 23 (source, ligne, reproduction, test de régression).
2. **P0** Exécuter des scénarios navigateur de bout en bout pour chaque module : entrée → modification → sauvegarde → rechargement → export → reprise sans réseau.
3. **P0** Extraire les données fictives dans un jeu de démonstration distinct, ne plus afficher de prix ou statut réel par défaut.
4. **P0** Renforcer sauvegardes/versionnage, clés, gestion des pièces sensibles et copie de secours sur disque.
5. **P1** Compléter la chaîne RDC → pointage → avancement et Quantité 3D → poste DQE → planning 4D.
6. **P1** Faire un vrai registre des achats/commandes/stock en liant fournisseurs et catalogues.
7. **P1** Chiffrage BPU/DQE avancé avec déboursé ressources et frais + pièces du marché.
8. **P1** Tester performances sur GTX 1060, Android et navigateur hors ligne, puis éditeur WebGL/IFC.
9. **P1** Étendre les fiches de tâches élémentaires et vérifier méthodes/temps/matériels sur Barbazan.
10. **P2** Agent IA local : assister, citer les pièces, aucune action sensible sans confirmation.
11. **P2** Registre d'audit probant, GED/DOE, contrôles et réception avec validation humaine.
12. **P2** Corriger tous les modules restants, tests automatisés répétables et critères de complétion explicites.

## Ressources

- Roadmap globale : `BTP_STUDIO_V2_ETAT_ET_BACKLOG.md`
- Veille GitHub 2026 : `VEILLE_GITHUB_2026_BTP.md`
- Moteur de calcul : `assets/project-core-v1.js`
- Registres V4 : `assets/*-repairs-v4.js`
- Tests locaux : `tests/project-core.test.cjs`, `tests/ui-structure.test.cjs`, `tests/legacy-v4.test.cjs`

**Statut actuel : itération importante livrée, BTP Studio complet non atteint.**
