# Audit de convergence — monorepo Sathancabrol
Date de vérification : 2026-10-10  
Branche d'audit : `audit/convergence-2026-10-10`  
Méthode : comparaison GitHub `main...branche` et lecture de fichiers représentatifs.  
Limite : ce document ne prétend pas remplacer l'exécution locale des tests ni une revue exhaustive de tous les fichiers.

## Décision immédiate

**Ne pas fusionner les branches en bloc et ne pas remplacer les projets sources par des copies du monorepo.** Conserver le principe déjà posé dans `feat/final-interface-skeleton-2026-10-07` : le monorepo est la coquille d'intégration ; les dépôts sources restent autoritaires tant qu'une capacité n'a pas été migrée, testée et vérifiée.

Ordre recommandé :
1. Mettre à jour l'inventaire GitHub et vérifier l'état actuel des PR/CI.
2. Préserver les branches riches (Watchtower, Nexus OS, BTP, catalogues d'outils) et les comparer fichier par fichier.
3. Fusionner d'abord les contrats de données et registres, puis le squelette d'interface, puis les adaptateurs.
4. Ne déclarer une capacité « opérationnelle » qu'après un test reproductible sur l'application.
5. Valider un seul parcours vertical : observation territoriale → preuve/source → objet géographique → scénario temporel → conséquences estimées → validation humaine.

## Comparaisons de branches observées

Les nombres ci-dessous proviennent des comparaisons GitHub effectuées le 2026-10-10. « En avance » signifie des commits présents dans la branche comparée et absents de `main`; « en retard » signifie que `main` contient des commits absents de cette branche. Une branche divergente doit être intégrée par revue, pas par écrasement.

| Dépôt | Branche comparée à main | En avance | En retard | Fichiers dans le diff | Décision |
|---|---|---:|---:|---:|---|
| monorepo | `feat/tool-data-catalog-2026-10` | 13 | 2 | 11 | **À préserver et intégrer après rebase/merge contrôlé** : contrats canoniques, registre modules/outils, graphe d'intégration. |
| monorepo | `feat/final-interface-skeleton-2026-10-07` | 7 | 2 | 7 | **Candidat principal pour l'interface** : squelette, registre des 12 domaines, routes. Vérifier les conflits avec le catalogue et Nexus. |
| monorepo | `feat/creative-toolchain-registry` | 10 | 2 | 6 | **À intégrer comme registre de recherche** : Blender, Unreal, MCP et outils créatifs ; le statut est explicitement `research_only`, ne pas déclencher d'installation. |
| monorepo | `arena/171a1f38-monorepo` | 8 | 2 | 41 | **Audit utile mais daté** : réutiliser ses scripts, données d'inventaire et rapports ; actualiser les données avant décision. |
| monorepo | `arena/01a08385-monorepo` | 6 | 27 | 93 | **Ne pas fusionner directement** : contient `nexus_os/` et des fichiers de racine anciens. Porter les modules Nexus vers une branche d'intégration récente après tests. |
| monorepo | `arena/01a08449-monorepo` | 1 | 15 | 257 | **Extraire sélectivement le module BTP** : corpus, matrice de traçabilité, rapports et dashboard. Le diff contient de nombreux fichiers déplacés/renommés ; ne pas faire une fusion aveugle. |
| watchtower | `arena/dec9cd88-watchtower` | 7 | 0 | 53 | **Candidat fort** : données INTEL, atlas Thau, import CSV, dossiers chantier et tests. Vérifier PR et CI actuelles avant intégration. |
| watchtower | `arena/01a072e1-watchtower` | 43 | 10 | 145 | **Référence UX complémentaire** : barre de fonctions, carte 2D, contrôles et audit UI. Branche très divergente ; sélectionner les composants utiles plutôt que fusionner en bloc. |
| COGNITORIUM | `watchtower/osint-workbench-v0.1` | 13 | 0 | 12 | **Candidat d'adaptation** : dossiers OSINT, observations, relations et registre de preuves ; les données de démonstration doivent rester explicitement marquées comme telles. |
| proto-cognitorium | `arena/01a08342-proto-cognitorium` | 5 | 2 | 14 | **À revoir pour ses sondes d'audit** : contenu, données, interactions, ROME et runtime ; ne pas considérer les outils d'audit comme preuve que toute l'application est validée. |
| ETAT-DE-LART-PSYCHOLOGIE | `arena/01a07d32-etat-de-lart-psychologie` | 5 | 0 | 11 | **À tester puis intégrer sélectivement** : explorateur GitHub/monorepo et inventaire. Ne pas confondre interface d'inventaire avec résultats scientifiques validés. |
| HCSM | `arena/01a03a6b-hcsm` | 0 | 3 | 0 | **Pas de nouveau contenu propre identifié dans cette comparaison** ; consulter `main` comme base de travail, vérifier les autres branches avant toute suppression. |
| Language-decoder | `arena/01a05471-language-decoder` | 3 | 0 | 24 | **À préserver impérativement** : le moteur Python, schéma `decoded-human`, UI et tests sont dans la branche, pas dans `main`. Auditer licence, dépendances et tests avant intégration. |

## Architecture cible — ce qui doit être partagé

| Contrat ou service | Source candidate | Règle d'intégration |
|---|---|---|
| Registre des modules et capacités | `data/module_registry.json`, `data/tool_registry.json` sur `feat/tool-data-catalog-2026-10` | Un identifiant stable par module/outil ; statut explicite : concept, recherche, prototype, testé, opérationnel. |
| Graphe d'intégration | `data/integration_graph.json` | Déclarer les dépendances ; valider que chaque relation cible un module existant. |
| Interface unifiée | `data/interface_registry.json` et `app/templates/interface.html` sur `feat/final-interface-skeleton-2026-10-07` | La navigation affiche le statut réel et la source du module ; une carte de fonction ne prouve pas que la fonction marche. |
| Preuves et provenance | HCSM + Research Engine + registre OSINT de COGNITORIUM | Distinguer FACT / OBSERVATION / INFERENCE / HYPOTHESIS / UNKNOWN ; conserver source, date, méthode, confiance et contexte. |
| Territoire | Watchtower + données Frontignan/Thau | Identifiants géographiques stables ; source et date par couche ; ne pas confondre données statiques et flux en direct. |
| Temps et scénarios | Animation Chronos + Atlas + données de chantier | Conserver état observé, historique, scénario et résultat réel séparément. |
| Chantier | Branche BTP + `imprevusTp.js` et dossiers chantier Watchtower | Document → tâche → ressource → coût/délai → risque ; les scénarios ne deviennent des prédictions qu'après validation sur données réelles. |
| Orchestration | `nexus_os/` dans `arena/01a08385-monorepo` | Portage contrôlé ; clés et fichiers sensibles côté local/serveur ; outils à privilèges réduits, confirmation humaine pour les actions risquées. |
| Outils créatifs | `data/tool_registry/creative-tools.json` | Conserver le statut `research_only` jusqu'à vérification de licence, version, sécurité, dépendances et compatibilité machine. |

## Parcours vertical minimal à valider

**Cas d'essai proposé : fermeture temporaire d'une rue pendant un chantier à Frontignan.**

1. Importer une observation sourcée : rue, période, cause et statut.
2. Afficher l'objet sur la carte et dans la frise temporelle.
3. Lier le chantier, les tâches, les ressources et les documents disponibles.
4. Montrer les conséquences possibles sur les itinéraires et le planning ; toute valeur inconnue reste « inconnue ».
5. Créer au moins deux scénarios comparables : calendrier initial et retard hypothétique.
6. Enregistrer les hypothèses, sources, calculs, incertitudes et validation humaine.
7. Quand le résultat réel est disponible, comparer prévision et observation pour mesurer l'erreur.

Critère de réussite : l'utilisateur peut retrouver la source de chaque donnée, modifier une hypothèse, comprendre ce qui change, et distinguer ce qui a été calculé de ce qui est seulement suggéré.

## Garde-fous avant toute fusion

- Aucun merge massif de toutes les branches `arena/*`.
- Aucun écrasement de `main` ni suppression de branche avant comparaison et sauvegarde.
- Vérifier les licences et la provenance des projets tiers et des données.
- Vérifier les tests réellement exécutés aujourd'hui ; les nombres consignés dans des audits du 7 octobre ne constituent pas un statut CI du 10 octobre.
- Exécuter les validateurs de schéma et tests des registres ; ajouter une validation de graphe pour détecter les références de modules absentes.
- Vérifier les données de démonstration et marquer visiblement les valeurs simulées.
- Aucun secret dans le dépôt, les logs, le registre d'interface ou les exports.
- Pour les cartes, prévoir un mode dégradé/hors ligne et déclarer les dépendances réseau : CesiumJS est open source, mais les fonds de carte et les contenus peuvent dépendre de fournisseurs externes.

## Sources GitHub

- [Registre des outils et modules](https://github.com/Sathancabrol/monorepo/tree/feat/tool-data-catalog-2026-10)
- [Squelette de l'interface finale](https://github.com/Sathancabrol/monorepo/tree/feat/final-interface-skeleton-2026-10-07)
- [Registre des outils créatifs](https://github.com/Sathancabrol/monorepo/tree/feat/creative-toolchain-registry)
- [Audit antérieur du monorepo](https://github.com/Sathancabrol/monorepo/tree/arena/171a1f38-monorepo/audit)
- [Watchtower — atlas/INTEL/import CSV](https://github.com/Sathancabrol/watchtower/tree/arena/dec9cd88-watchtower)
- [Watchtower — composants UX](https://github.com/Sathancabrol/watchtower/tree/arena/01a072e1-watchtower)
- [Nexus OS](https://github.com/Sathancabrol/monorepo/tree/arena/01a08385-monorepo/nexus_os)
- [Module BTP](https://github.com/Sathancabrol/monorepo/tree/arena/01a08449-monorepo/projects/btp-conduite-travaux)
- [Language Decoder](https://github.com/Sathancabrol/Language-decoder/tree/arena/01a05471-language-decoder)

## Statut de ce livrable

- [x] Comparaisons GitHub et lecture des fichiers représentatifs.
- [x] Branche d'audit créée séparément de `main`.
- [x] Plan de convergence et premier parcours vertical documentés.
- [ ] Exécution locale des tests.
- [ ] Vérification de l'état actuel des PR et CI.
- [ ] Fusion ou portage du code (non réalisé dans cette étape).


## Vérification complémentaire — PR Watchtower #3 (10 octobre 2026)

- État GitHub consulté : **ouverte**, non fusionnée ; dernière mise à jour indiquée le **9 octobre 2026 à 12:47 UTC**.
- Dernier run CI retourné par l'API : **succès**, sur le commit `4151e2e25b27efcdb500f4a47601cca96bb03388`, déclenché le **7 octobre 2026**.
- Le corps de la PR déclare `npm test` : 3 279 tests, 3 278 réussis, 1 ignoré, 0 échec, et `npm run build` vert. C'est une déclaration de la PR ; je n'ai pas exécuté ces commandes dans un environnement local durant cet audit.
- La PR indique explicitement que la fusion dans `main` attend l'accord du propriétaire. **Ne pas fusionner automatiquement** ; la décision doit venir de l'utilisateur.
- Lien : https://github.com/Sathancabrol/watchtower/pull/3

## État des actions au terme de cette session

- [x] État de la PR Watchtower #3 consulté.
- [x] Dernier run CI disponible consulté ; succès daté du 7 octobre, donc pas une preuve d'exécution le 10 octobre.
- [ ] Rejouer les tests dans un environnement local ou CI fraîchement déclenchée.
- [ ] Ouvrir une PR de convergence après revue des conflits ; aucune PR de convergence n'a été créée ici.
