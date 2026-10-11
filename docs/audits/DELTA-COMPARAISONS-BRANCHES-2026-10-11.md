# Addendum — comparaisons ciblées de branches

**Date :** 2026-10-11  
**Branche de travail :** `feat/automated-project-audit-2026-10-11`  
**Nature de la preuve :** comparaison GitHub des références et statistiques de fichiers. Ce document ne prétend pas remplacer la lecture sémantique de chaque fichier ni les tests runtime.

## Résultats vérifiés dans cette passe

| Dépôt | Référence comparée à `main` | Résultat Git | Constats utiles | Action |
|---|---|---|---|---|
| `monorepo` | `arena/01a08385-monorepo` | Divergente, 6 commits en avance, 27 en retard | La branche contient un arbre `nexus_os/` substantiel : runtime, agents JSON, application, configuration et mémoire. Le diff comprend aussi `data/github_inventory.json` et le README. | Préserver la branche ; examiner les fichiers d'exécution, la sécurité et les dépendances avant toute intégration. |
| `monorepo` | `arena/0034230e-monorepo` | Divergente, 26 en avance, 2 en retard | Carré d'As : schémas canoniques, validation d'admissibilité, génération de documents, serveur, interface desktop, moteur d'agents et profils Markdown. Workflow Windows ajouté. | Comparer ses contrats/runtime avec Nexus OS ; éviter deux orchestrateurs canoniques concurrents. |
| `monorepo` | `feat/gap-driven-audit-2026-10-11` | En avance de 16 commits, aucun retard | La branche contient déjà scripts d'inventaire/audit, registre portfolio, protocole gap-driven, handoff agent, workflow CI et mémoire adaptative. | Réutiliser cette automatisation comme voie principale ; ne pas créer un scanner parallèle. |
| `monorepo` | `feat/tool-data-catalog-2026-10` | Divergente, 13 en avance, 2 en retard | Catalogue outils/modules, schémas canoniques et graphe d'intégration ; modifications aussi sur l'interface. | Réconcilier avec la branche d'audit et le squelette d'interface avant de sélectionner la version à intégrer. |
| `monorepo` | `arena/01a08449-monorepo` | Divergente, 1 en avance, 15 en retard | Corpus BTP, inventaire CSV/JSON, ledger d'audit, confrontation théorie/état de l'art, synthèse chantiers/prix, matrice de traçabilité, index de sources réglementaires et documents DCE largement renommés/présents dans le diff. | Traiter comme un corpus BTP significatif. Vérifier provenance, droits, doublons et intégrité des sources ; ne pas fusionner aveuglément des milliers de lignes de données/documentation. |
| `watchtower` | `arena/dec9cd88-watchtower` | En avance de 7 commits, aucun retard | Ajout de données Atlas Thau/Frontignan, dossiers chantier, imprévus TP, veille officielle, import CSV, attributs territoriaux et plusieurs suites de tests dédiées. | Candidat concret pour le socle Watchtower/Atlas ; exécuter les tests et contrôler la provenance/licence des données. |
| `Language-decoder` | `arena/01a05471-language-decoder` | En avance de 3 commits, aucun retard | Code Python, CLI/serveur, inférence, dynamique, ontologie, schéma, interface et `tests/test_engine.py`. | Ne pas conclure à l'absence du moteur à partir du seul `main`. Exécuter la suite et auditer le contrat avec HCSM/Carré d'As. |
| `COGNITORIUM` | `watchtower/osint-workbench-v0.1` | En avance de 13 commits, aucun retard | Spécification OSINT étendue, registre, observations, dossiers d'enquête, relations et export JSON. | Réutiliser comme prototype/spécification ; comparer aux modules Watchtower déjà intégrés avant portage. |
| `proto-cognitorium` | `main` vs `main` | Identique | Comparaison de contrôle sans différence, pas une comparaison interbranche. | À ne pas compter comme une vérification de toutes les branches du dépôt. |

## Conclusions opérationnelles

1. **Ne pas fusionner les branches en bloc.** Plusieurs branches du monorepo sont divergentes ; un simple diff ne résout pas la compatibilité ni les conflits.
2. **Priorité 1 — orchestration :** examiner le code de démarrage, les contrats, la mémoire, les permissions, les secrets et les tests de Nexus OS et Carré d'As. Choisir un runtime canonique sur preuves.
3. **Priorité 2 — BTP/Atlas :** préserver le corpus BTP et la branche Watchtower INTEL. Séparer code, données, documents source, métadonnées de provenance et données sous licence restrictive.
4. **Priorité 3 — contrats :** comparer les schémas de Carré d'As, HCSM, Language-decoder et le catalogue d'intégration ; proposer des adaptateurs plutôt qu'une réécriture prématurée.
5. **Priorité 4 — automatisation :** utiliser le protocole et les scripts gap-driven existants pour suivre les branches et preuves non examinées.
6. **Limite :** les statistiques Git ne prouvent ni la qualité du code, ni la réussite des tests, ni l'identité des copies. Les builds/tests ne sont toujours pas exécutés dans cette session.

## Statut de cette passe

- [x] Comparaisons ciblées de 8 références de branches/prototypes pertinentes et 1 comparaison de contrôle.
- [x] Consignation des deltas et décisions d'audit.
- [ ] Comparaison exhaustive de toutes les branches restantes et lecture sémantique des fichiers pertinents.
- [ ] Exécution des suites de tests/builds dans un environnement exécutable.
- [ ] Validation par tests d'intégration du contrat mémoire commun.


## Vérification des chemins OSINT — présence et absence constatées

Une vérification ciblée des répertoires GitHub confirme que la branche `COGNITORIUM:watchtower/osint-workbench-v0.1` contient les six fichiers de `watchtower-mods/src/osint/` (README, index, case, evidence, registry, workbench). En revanche, les deux chemins suivants renvoient 404 sur les références interrogées :

- `Sathancabrol/monorepo:main/projects/COGNITORIUM/watchtower-mods/src/osint/`
- `Sathancabrol/watchtower:main/src/osint/`

**Interprétation limitée :** ce workbench n'est pas présent à ces chemins sur les références `main` vérifiées. Cela ne prouve pas son absence de toutes les branches, ni l'absence de fonctions équivalentes dans d'autres modules Watchtower. Il faut encore examiner les autres branches et chercher les concepts/fonctions équivalents avant de conclure à un vrai manque fonctionnel.

**Décision :** conserver le prototype COGNITORIUM comme source de portage potentielle ; avant portage, définir la destination canonique, vérifier les imports/contrats et ajouter des tests d'intégration. Ne pas recopier le dossier dans le monorepo en supposant que cela l'intègre à Watchtower.
