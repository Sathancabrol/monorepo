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


## Quatrième lot — branches supplémentaires, Frontignan et outils de recherche

### Comparaisons supplémentaires

| Dépôt / branche | Relation avec `main` | Éléments distinctifs vus dans le diff | Décision provisoire |
|---|---|---|---|
| `monorepo:arena/0d411b29-monorepo` | Divergente, 7 en avance, 2 en retard | Projet `bone` avec persona, LLM, permissions, scripts de lancement/packaging, interface et tests dédiés. | Actif potentiel d'interface/persona ; audit de permissions et du comportement du bot avant toute réutilisation. |
| `monorepo:arena/00f44a26-monorepo` | Divergente, 1 en avance, 2 en retard | Projet `laplace`, agent et politique d'exécution, documentation Carré d'As, confidentialité, sources et tests de mémoire/politique/configuration. | À comparer à Nexus OS/Carré d'As comme troisième candidat ; ne pas le laisser devenir un runtime concurrent par défaut. |
| `monorepo:arena/01a08203-monorepo` | Divergente, 1 en avance, 27 en retard | Atlas Frontignan : interface, données Atlas JSON, CSV des communes de Thau, graphe, génération d'atlas et deck. | Réutiliser comme archive de données/visuel ; vérifier date, sources, géométrie, licence et différences avec Watchtower INTEL. |
| `monorepo:arena/1bad5f9b-monorepo` | En avance de 1 commit | Delta limité à `projects/proto-cognitorium/server.ts` et `src/App.tsx`. | Vérifier le delta exact avant de le porter ; il s'agit d'un changement d'application, pas d'une preuve de convergence globale. |
| `monorepo:arena/15c77b59-monorepo` | Divergente, 1 en avance, 2 en retard | Grande archive documentaire Carré d'As : roadmaps, traces de sessions d'agents, plans et documentation d'implémentation. | Indexer comme archive de décisions et provenance ; ne pas ingérer sans filtre les discussions brutes dans la mémoire active. |
| `monorepo:arena/171a1f38-monorepo` | Divergente, 8 en avance, 2 en retard | Historique d'audit avec inventaires de branches, drift, graphes, mémoire, journal et notes projet. | Source d'historique ; les snapshots doivent être rafraîchis et les alertes revérifiées. |
| `monorepo:feat/creative-toolchain-registry` | Divergente, 10 en avance, 2 en retard | Registre d'outils créatifs, doc d'architecture, benchmark vidéo IA, validateur et tests du registre. | Réutiliser le motif de registre validé par schéma ; rapprocher du catalogue outil existant au lieu de créer deux catalogues incompatibles. |
| `monorepo:feat/mobile-ar-fastpath-2026-10-11` | En avance de 18 commits | Registre portfolio, audit gap-driven, mémoire adaptative et dossier HUD mobile/AR. | Branche de travail la plus avancée pour l'automatisation d'audit ; elle ne prouve pas l'exécution CI ni la validation du HUD sur appareil. |
| `watchtower:arena/01a072e1-watchtower` | Divergente, 43 en avance, 10 en retard | Audit Watchtower, architecture modulaire, charge mentale, vue Intel territoire, carte 2D, volant UI, parité des sources et tests JS. | Branche à haute priorité de revue ; elle contient à la fois documentation d'audit et tests de composants, à confronter au canonique. |
| `ETAT-DE-LART-PSYCHOLOGIE:arena/01a04f7b` | Divergente, 38 en avance, 1 en retard | Agent chercheur « Uranus », 11 compétences de recherche, fixtures hors-ligne, pipeline de sources, PRISMA, trust scoring, visualisations, SOL/Vénus et suites de tests. | Actif de grande valeur pour Research Engine/Cognitorium ; inspecter le code, les métriques de confiance et les preuves de validation avant fusion. |
| `ETAT-DE-LART-PSYCHOLOGIE:arena/01a03aac` | Divergente, 2 en avance, 1 en retard | Application Python/SQLite avec données de concepts, laboratoire et statistiques. | Candidat à comparer au simulateur cognitif ; vérifier si les modèles et données sont compatibles ou duplicatifs. |
| `ETAT-DE-LART-PSYCHOLOGIE:arena/01a045a1` | Divergente, 1 en avance, 1 en retard | Agent de recherche avec pipeline, modèle, confiance, rapport, outils et données de démonstration. | Comparer avec Uranus avant de retenir l'une des variantes. |
| `ETAT-DE-LART-PSYCHOLOGIE:arena/01a07d32` | En avance de 5 commits | Application d'inventaire GitHub et monorepo, documentation, script d'inventaire et requirements. | Fonction utilitaire ; comparer avec le scanner gap-driven et éviter les inventaires parallèles. |

### Détails sur l'agent de recherche « Uranus »

Le README de la branche `arena/01a04f7b` décrit un agent hybride à règles déterministes par défaut, LLM optionnel, fixtures hors-ligne, traces de run et compétences dédiées (recherche multi-bases, DOI, déduplication, validation de champs, estimation de confiance, dépistage de biais, PRISMA, synthèse et veille). Les répertoires `agent/core`, `agent/skills` et `tests` existent effectivement dans cette branche.

Ces éléments en font un candidat de réutilisation plus concret qu'une simple spécification. Toutefois, les nombres de tests et les affirmations de couverture figurant dans le README restent **déclaratifs** tant que la suite n'est pas exécutée sur le SHA candidat. Le score « trust » ne doit pas être traité comme une probabilité calibrée de vérité sans validation empirique et documentation de la méthode.

### Décisions de convergence mises à jour

1. **Runtime d'agents :** ne pas choisir entre Nexus OS, Carré d'As et Laplace sur le seul nombre de fonctionnalités. Construire une matrice comparative : permissions, isolation, persistance, reprise, appels outils, observabilité, coût, tests et exécution locale.
2. **Recherche scientifique :** comparer Uranus (branche EDL) à `reaserch-engine` et aux outils de recherche existants ; identifier les briques manquantes, réutiliser les compétences testées et garder un seul graphe de preuves canonique.
3. **Territoire :** Watchtower INTEL et Atlas Frontignan partagent un domaine, mais pas nécessairement les mêmes sources ni les mêmes versions. Centraliser les sources/identifiants et exposer des adaptateurs plutôt que dupliquer les jeux de données.
4. **Mémoire :** garder les logs bruts et historiques accessibles, mais ne pas les injecter systématiquement dans le contexte actif ; les résumer avec provenance et liens vers les traces originales.
5. **Tests :** réutiliser les tests existants comme base, mais exiger des assertions bloquantes, des codes de sortie corrects et des runs CI observables avant de déclarer un module validé.


## Cinquième lot — revue statique des risques et de la qualité de preuve

### Uranus / ETAT-DE-LART-PSYCHOLOGIE

Fichiers lus sur `arena/01a04f7b-etat-de-lart-psychologie` : `agent/skills/trust_scoring.py`, `agent/skills/search_literature.py`, `tests/test_agent.py` et le README.

- **Réutilisable :** architecture par compétences enregistrées, normalisation Crossref/OpenAlex/PubMed, fixtures hors-ligne, export JSON/CSV et tests de bout en bout décrits dans le dépôt.
- **Limite du Trust Factor :** le score est explicitement heuristique, ce qui est sain, mais certains signaux sont des proxys discutables : la taille d'échantillon contribue à une composante nommée « réplication », tandis que le repérage d'un design randomisé ne modifie pas réellement le score. Il faut séparer méthodologie, puissance/précision, reproductibilité, transparence et confiance dans la source. Ne pas présenter le score global comme une probabilité de vérité.
- **Limite de la recherche :** le dédoublonnage visible privilégie DOI ou un préfixe du titre ; il faut tester les DOI absents, variantes de titre, métadonnées incomplètes et collisions. Les résultats Crossref/OpenAlex/PubMed doivent conserver leur provenance et le statut en ligne/hors-ligne.
- **Limite des tests :** plusieurs tests créent des runs et artefacts sous le répertoire `output/agent_runs` du projet ; prévoir un répertoire temporaire isolé et une remise à zéro contrôlée pour rendre les tests répétables sans salir l'arbre source.
- **Licence :** aucun fichier `LICENSE` n'apparaît à la racine de la référence interrogée. Cela ne prouve pas qu'aucune licence n'existe ailleurs, mais les droits de portage ne sont pas établis par la liste des fichiers consultée.

### Laplace / monorepo

Le `pyproject.toml` de `monorepo:arena/00f44a26-monorepo/projects/laplace` déclare Python >=3.11, dépendances `aiosqlite`, `discord.py`, `openai`, `python-dotenv`, et extras de test/qualité. Le champ de licence est `UNLICENSED`. **Bloquer le portage ou la redistribution jusqu'à clarification écrite des droits**. L'existence de tests de politique, configuration et mémoire est confirmée par les noms de fichiers, pas par leur exécution.

### Bone / monorepo

Le projet `bone` déclare `discord.py==2.4.0` et `python-dotenv==1.0.1`, avec tests pour LLM, permissions et persona. Le fichier `perms.py` expose des packs d'autorisations incluant modération, gestion de salons/rôles, webhooks et un pack administrateur. Les noms de packs ne prouvent pas la sécurité de l'implémentation : l'intégration devra exiger le moindre privilège, un consentement explicite à chaque capacité, une journalisation et des tests des URL d'invitation. Aucun fichier `LICENSE` n'apparaît à la racine de la référence interrogée ; droits à clarifier.

### Impacts sur la matrice de réutilisation

| Actif | Statut technique actuel | Statut licence actuel | Prochaine étape |
|---|---|---|---|
| Uranus / agent chercheur | Architecture et tests déclarés ; revue statique partielle | Licence racine non établie par la liste consultée | Exécuter les tests, corriger les métriques de confiance, isoler les artefacts, clarifier les droits |
| Laplace | Code Python/Discord/SQLite et tests présents | `UNLICENSED` dans `pyproject.toml` | Ne pas redistribuer/porter avant autorisation ; audit sécurité et tests |
| Bone | Bot Discord, packs de permissions et tests présents | Licence racine non établie par la liste consultée | Audit moindre privilège, tests, clarification des droits |
| Watchtower INTEL | Branche fortement divergente avec tests de composants visibles | À vérifier pour code et données séparément | Comparaison fonctionnelle, exécution CI et provenance des données |

**Règle de décision :** « code visible » ≠ « licence claire » ≠ « tests réussis » ≠ « intégration validée ». Ces quatre statuts restent distincts dans le registre.
