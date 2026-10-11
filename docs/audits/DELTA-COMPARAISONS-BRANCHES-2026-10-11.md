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


## Audit du mécanisme d'audit automatisé existant

Lecture statique de `scripts/project_audit/audit_gaps.py`, `scripts/project_audit/audit_portfolio.py` et `.github/workflows/project-audit.yml` dans `feat/gap-driven-audit-2026-10-11`.

### Ce que le mécanisme fait réellement

- `audit_gaps.py` pagine la liste des branches par lots API de 100 jusqu'à épuisement, compare les SHA aux index précédents, et sélectionne les branches à inspecter par priorité.
- Il inspecte au maximum `AUDIT_MAX_BRANCH_TREES` arbres récursifs par exécution (15 par défaut dans le workflow) et consigne les chemins jugés pertinents.
- Il sépare explicitement inspection de l'arbre, revue du contenu et vérification runtime. Le script indique `runtime_verified: false` et `semantic_content_review_automated: false`.
- `audit_portfolio.py` calcule des signaux de documentation/tests/CI depuis les noms de fichiers, mais n'exécute aucun test. Sa lecture de branches est limitée à la première page de 100 et expose un indicateur `branches_truncated_possible` lorsque la page est pleine.
- Le workflow `project-audit.yml` se déclenche par planification quotidienne, `workflow_dispatch` ou push sur `main` seulement pour certains chemins. Il checkout explicitement `main` et publie les rapports sur `main`.

### Limite d'exécution constatée pendant cette session

Le connecteur GitHub accessible ici permet de lire les statuts et les exécutions, mais ne propose pas d'action pour déclencher `workflow_dispatch`. Le dernier commit de cette branche d'audit n'a retourné aucun workflow associé ni statut combiné. Il est donc impossible d'affirmer que les scripts ont été exécutés pendant cette session.

### Améliorations recommandées

1. Ajouter un déclencheur de validation PR qui exécute au minimum les tests du scanner sur fixtures locales, sans publier automatiquement de rapport sur `main`.
2. Ajouter des tests unitaires sur la pagination, le changement de SHA, les branches supprimées, les erreurs API, les arbres tronqués et le budget de 15 arbres.
3. Garder l'exécution de production qui écrit sur `main` séparée de la validation d'une branche ou PR.
4. Ajouter une file explicite de revue humaine par branche/fichier et une clôture justifiée ; un arbre inspecté ne doit pas être assimilé à un contenu audité.
5. Clarifier si le seuil de 100 branches du rapport portefeuille est acceptable ou si lui aussi doit paginer.

**Conclusion :** le scanner gap-driven est une bonne base pour éviter de perdre les branches oubliées. Il automatise la découverte et l'indexation, pas l'analyse sémantique ni les tests. Il faut l'utiliser et tester ses limites, pas lui attribuer des capacités qu'il n'a pas.


## Deuxième lot de comparaisons — interface et audit de convergence

| Branche | Relation avec `main` | Contenu du delta observé | Décision provisoire |
|---|---|---|---|
| `feat/final-interface-skeleton-2026-10-07` | Divergente, 7 commits en avance, 2 en retard | `app/templates/interface.html`, CSS/JS d'interface, `data/interface_registry.json`, audit de l'interface finale et adaptations de l'application FastAPI. | Comparer le registre des slots avec Carré d'As avant de choisir un shell. Conserver la séparation interface / registre de modules / runtime. |
| `audit/convergence-2026-10-10` | Divergente, 10 commits en avance, 2 en retard | Dossiers d'audit, taxonomie, journal, mémoire, inventaire et graphes de branches/drift, notes par projet. | Utiliser comme mémoire historique d'audit et source de pistes ; rafraîchir les SHA et revalider les alertes avant de les considérer actuelles. |
| `arena/93b54a79-monorepo` | Divergente, 45 commits en avance, 2 en retard | Office UI, inventaire de fonctionnalités, Atlas Thau, agent d'entreprise/OS, prospective, matériel, benchmarks, docs de sessions et modules. | Source d'archives à haute valeur. Indexer les actifs par chemin/SHA et porter sélectivement ; ne pas fusionner la branche en bloc. |

Ce lot confirme que l'archive contient plusieurs systèmes de documentation et d'interface qui se recoupent. La prochaine décision doit s'appuyer sur un inventaire dédupliqué des fonctions et sur les responsabilités réelles des composants, plutôt que sur la quantité de fichiers ou la fraîcheur apparente d'une branche.


## Troisième lot — branches historiques Cognitorium / HCSM

Comparaisons des branches `arena/*` découvertes dans les dépôts avec leurs `main` respectifs :

| Dépôt | Références examinées | Résultat |
|---|---|---|
| `proto-cognitorium` | `arena/01a033e8`, `01a034f2`, `01a035a5`, `01a0369e`, `01a03436`, `01a03899` | Toutes sont des ancêtres de `main` selon le comparateur GitHub : 5 à 54 commits de retard, aucun commit unique en avance et aucun fichier dans le delta. |
| `proto-cognitorium` | `arena/01a08342-proto-cognitorium` | Divergente : 5 commits en avance et 2 en retard. Le delta comprend des audits datés, une roadmap, une traceabilité CSV et des scripts d'audit (contenu, données, simulation, interaction, diagnostic ROME, runtime probe). |
| `HCSM` | `arena/01a03a6b-hcsm`, `arena/01a03a93-hcsm` | Ancêtres de `main`, respectivement 3 et 1 commits de retard, sans delta unique en avance. |
| `COGNITORIUM` | `arena/01a05ef8-cognitorium`, `arena/01a06876-cognitorium` | Ancêtres de `main`, respectivement 3 et 1 commits de retard, sans delta unique en avance. |

### Conséquence

Pour ces références précises, le risque immédiat n'est pas une fonctionnalité cachée unique dans chaque branche, mais le maintien de branches historiques. Il reste important de distinguer ce résultat du cas `arena/01a08342-proto-cognitorium`, qui contient des outils d'audit additionnels à examiner. Les scripts présents dans cette branche ne sont pas considérés comme exécutés ni fiables avant lecture et tests.


## Lecture ciblée des sondes d'audit proto-Cognitorium

La branche `proto-cognitorium:arena/01a08342-proto-cognitorium` contient un kit de sondes (runtime, interactions, données, ROME, contenu et simulation de correctifs). Le README explique que les sondes chargent les composants réels via Vite et jsdom, avec données réelles. C'est un actif utile pour tester le prototype sans réimplémenter sa logique.

**Réserves techniques relevées dans le code/documentation consultés :**

- Le README précise que le rendu canvas est stubé : le montage et une partie de la logique sont testés, mais pas le dessin réel des graphes.
- Le README indique que les sondes runtime sont un harnais de non-régression auquel il manque une assertion (référence à la roadmap §G3).
- `runtime-probe.mjs` journalise les résultats et les erreurs console ; la fin du script force une sortie de processus à code 0. Sans assertions bloquantes, un rendu `CRASH` ou `ERR` peut donc être rapporté sans nécessairement faire échouer le job.
- Les tests sont documentés comme exécutés sans `GEMINI_API_KEY`, ce qui est pertinent pour le mode de repli hors-ligne, mais ne valide pas les appels externes.
- Les résultats « 143 rendus, 0 crash, 0 erreur console » figurent dans le README ; ils sont **déclarés par la documentation de cette branche**, pas réexécutés ni confirmés dans cette session.

**Action prioritaire :** porter ou adapter ce harnais à la branche canonique de proto-Cognitorium, ajouter des assertions et codes de sortie non nuls en cas d'échec, distinguer tests hors-ligne et tests d'intégration API, puis exécuter les sondes dans CI. Ne pas importer les résultats historiques comme preuve de l'état actuel sans relancer le kit sur le SHA choisi.
