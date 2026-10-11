# Audit de réutilisation — Watchtower, Cognitorium et briques cognitives

**Date de l'audit :** 2026-10-11  
**Statut :** audit statique initial — non exécuté localement  
**Branche :** `feat/automated-project-audit-2026-10-11`  
**Objectif :** inventorier les capacités déjà présentes avant toute nouvelle implémentation, en particulier mémoire, recherche, contexte, graphe, apprentissage, territoire et orchestration.

> Cet audit s'appuie sur les arbres de fichiers et le code consultés via GitHub. Les tests ne sont pas déclarés passants : aucune exécution locale du build/test n'a été effectuée pendant cet audit. Les conclusions marquées « présent » signifient que le code ou le contrat est visible dans le dépôt, pas que toute la chaîne est intégrée et validée en production.

## 1. Résumé exécutif

Le stock actuel contient déjà une grande partie des briques conceptuelles nécessaires. Le problème principal n'est pas l'absence générale de modules : c'est leur **dispersion, duplication et absence de contrats communs entre applications**.

| Besoin | Brique existante | État vérifié | Décision provisoire |
|---|---|---|---|
| Interface territoriale 3D / données géospatiales | `Sathancabrol/watchtower` | Application Vite/Cesium importante, sources et calques, nombreuses suites de tests | Réutiliser comme socle Watchtower/Atlas ; auditer les sources et les limites de licence séparément |
| Contexte immédiat d'une entité sélectionnée | Watchtower `src/data/contextStore.js` | Store en mémoire navigateur, sélection et rafraîchissement des sujets suivis ; tests dédiés présents | Réutiliser comme **contexte de session**, pas comme mémoire persistante |
| Questions sur les données déjà chargées | Watchtower `src/data/analystEngine.js` | Moteur de requêtes sur tableaux locaux, filtres et contexte de vue ; follow-up limité à l'instance | Réutiliser pour l'analytique locale ; ne pas le confondre avec une mémoire à long terme |
| Dossiers explorables / arbre de cartes | Watchtower `src/data/dossiers.js` | Normalisation, aplatissement et filtrage d'arbres de dossiers | Réutiliser comme modèle d'exploration ; ajouter provenance et persistance si nécessaire |
| Recherche en langage naturel et commandes | Watchtower `src/chatConsole.js`, `src/commandes.js` | Chat textuel sans clé avec commandes, réponses rapides contextuelles et sources publiques | Réutiliser pour l'interface de commande ; séparer commandes déterministes et réponses LLM |
| Graphe professionnel, preuves, ROME | `proto-cognitorium` | Graphe de nœuds, catalogue, matching ROME explicable, validation humaine et extraction d'expérience visibles dans le code | Réutiliser comme base du cœur Cognitorium ; auditer persistance et tests avant intégration |
| Décroissance / réactivation de compétences | `proto-cognitorium/src/utils/decay.ts` | Modèle heuristique exponentiel, plancher de rétention et effort de réactivation estimé | Réutiliser uniquement comme simulation heuristique, pas comme mesure scientifique validée |
| Niveau de preuve / limites d'inférence | `proto-cognitorium/src/utils/epistemics.ts` | Échelle fait → compétence inférée → capacité candidate → hypothèse ; refuse l'automatisation d'une conclusion psychologique | Réutiliser et aligner avec HCSM |
| Journal de métacognition | `proto-cognitorium/src/components/MetacogLoopView.tsx` | Journal localStorage, limité aux 20 dernières entrées | Réutiliser le flux UX ; remplacer/adapter le stockage pour export, recherche et conservation maîtrisée |
| Validation humaine | `proto-cognitorium/src/components/ValidationCenterModal.tsx` | Nœuds en attente/inférés éditables, validables ou rejetables | Réutiliser comme garde-fou de validation |
| Apprentissage par situations | `COGNITORIUM/learning/` | Architecture CLE documentée : situation → action → conséquence → concept → transfert → évaluation → mise à jour du graphe | Réutiliser la conception ; vérifier le prototype et rendre les scénarios versionnés |
| Preuves et recherches reproductibles | `reaserch-engine` | Orchestrateur, EvidenceGraph, agents injectables, checkpoints JSON atomiques, historique et tests automatisés présents | Réutiliser comme moteur de recherche/preuves commun |
| Contrat de données cognitives avec incertitude | `HCSM` | Ontologie, schéma proposé et validateur V1/V5 avec tests documentés | Réutiliser comme **contrat de validation**, pas comme moteur d'estimation implémenté |
| Archive des modules | `COGNITORIUM/watchtower-mods/` et `monorepo/projects/COGNITORIUM/watchtower-mods/` | Copies de modules Watchtower également présentes dans le dépôt Watchtower principal | Dédupliquer et déclarer une source canonique ; éviter les corrections divergentes |

## 2. Watchtower : capacités à conserver

### 2.1 Modules repérés

- **Globe / cartographie / calques** : Cesium, géospatial 3D, couches de données publiques et sources spécialisées.
- **Cockpit et HUD** : navigation, disposition des panneaux, affichage et contexte de vue.
- **Contexte des entités** : `src/data/contextStore.js` enregistre des métadonnées d'entités, l'identité sélectionnée et l'horodatage de sélection.
- **Moteur d'analyste** : `src/data/analystEngine.js` interroge les enregistrements déjà chargés ; la documentation précise qu'il n'effectue pas lui-même la collecte générale et que les suivis de requêtes sont limités à une instance.
- **Dossiers explorables** : `src/data/dossiers.js` transforme les objets en arbre filtrable.
- **Commandes / chat** : `src/commandes.js` constitue un registre commun aux commandes, à l'aide et aux suggestions rapides ; `src/chatConsole.js` fournit l'interface textuelle.
- **Annotations et suivi** : modules d'annotations, sujets suivis et politiques de rendu accompagnés de tests.
- **Qualité** : scripts `npm test`, suivi des régressions et contrôles de carte déclarés dans `package.json`.

### 2.2 Limite pour la mémoire souhaitée

Le `contextStore` est un **état de session** : il vit dans `window`, et non dans un dépôt mémoire durable. Le moteur analyste conserve un contexte de suivi de requête pour les relances, mais ce mécanisme est local à son instance. Ces deux modules sont utiles pour la mémoire de travail de Watchtower, mais ne satisfont pas à eux seuls les besoins de mémoire à long terme, de consolidation, de rappel inter-projets et de fiches de recherche Markdown.

### 2.3 Réutilisation recommandée

1. Garder Watchtower comme interface territoriale et couche de visualisation.
2. Réutiliser le contexte de sélection pour fournir à l'assistant un « contexte actif » : entité, couche, lieu, période, source et date de mise à jour.
3. Faire passer toute information collectée dans une enveloppe de données commune : identifiant stable, source, horodatage, statut de fraîcheur, confiance, licence/conditions d'usage et lien vers la preuve.
4. Ne pas laisser le contexte de session devenir la source de vérité ; la persistance doit être assurée par une couche séparée.
5. Avant de réutiliser les modules de données, examiner les conditions de chaque API/source et les limites d'usage ; le statut open source du code n'accorde pas automatiquement des droits sur les données tierces.

## 3. Proto-Cognitorium : capacités à conserver

### 3.1 Modules repérés

- `src/utils/decay.ts` : vitalité estimée des compétences, décroissance exponentielle et estimation du temps de réactivation.
- `src/utils/epistemics.ts` : échelle épistémique et garde-fou contre les conclusions psychologiques automatiques.
- `src/utils/romeMatching.ts` : matching de compétences et fiches ROME, avec correspondance exacte/floue.
- `src/utils/resourceSearch.ts` : recherche textuelle pondérée de ressources.
- `src/components/DecayTimeline.tsx` : visualisation temporelle et action de réactivation.
- `src/components/MetacogLoopView.tsx` : journal planification/monitoring/ajustement/évaluation stocké dans localStorage (20 entrées maximum).
- `src/components/ValidationCenterModal.tsx` : validation humaine des propositions.
- `src/components/ExperienceDistillerModal.tsx` : proposition de nœuds/relations depuis un récit d'expérience.
- Graphe cognitif, gestion de profil, vues d'évaluation, atlas, ressources, CV ciblé et catalogue de savoirs.

### 3.2 Limites à traiter avant intégration

- Le calcul de décroissance est explicitement heuristique. Les valeurs de plancher, de demi-vie et les durées de réactivation ne doivent pas être présentées comme des lois individuelles établies sans calibration et validation.
- Le journal de métacognition est un stockage navigateur borné ; ce n'est pas un historique de recherche versionné, exportable et interrogeable par les autres modules.
- Le prototype dépend de `@google/genai` côté application serveur : l'architecture n'est donc pas entièrement locale par défaut.
- Les catalogues et les données générées doivent garder leur provenance, leur date et leur statut (déclaré, extrait, inféré, vérifié par humain).

### 3.3 Réutilisation recommandée

Conserver les composants UX et le graphe comme référence fonctionnelle. Ne pas recopier la logique de mémoire dans plusieurs composants : extraire ultérieurement un contrat commun de « fait / expérience / concept / preuve / décision / état temporel », avec adaptateurs vers les données Cognitorium.

## 4. COGNITORIUM : stock d'interface et apprentissage

Le dépôt `COGNITORIUM` contient la documentation de gouvernance, les audits, les rôles d'agents, le prototype CLE dans `learning/` et une copie de `watchtower-mods/`.

**CLE** est la meilleure brique disponible pour la boucle d'amélioration pédagogique : une action produit une conséquence, le concept nécessaire émerge, l'apprenant formalise, transfère et évalue, puis le graphe est mis à jour. Il faut préserver les scénarios et leurs concepts associés plutôt que les remplacer par une simple succession de pages de cours.

**Risque de duplication :** une partie des modules Watchtower est également présente dans le dépôt `watchtower` et dans les archives du monorepo. Les copies archivées sont utiles pour retrouver l'historique, mais elles ne doivent pas être traitées comme trois implémentations indépendantes.

## 5. HCSM et Research Engine : les associer sans les confondre

### HCSM

- L'ontologie et `specs/data-schema.md` définissent des objets incluant fenêtre temporelle, contexte, provenance, observations, incertitude et possibilité de refus.
- `validator/` est un validateur de structure/admissibilité ; la documentation dit explicitement qu'il n'est ni estimateur, ni API, ni lecteur de capteurs.
- Les statuts HCSM sont largement `PROPOSED`. Il faut donc traiter le validateur comme une barrière de conformité et ne pas affirmer qu'il mesure déjà un état cognitif.

### Research Engine

- L'architecture documentée est question → plan → recherche → preuves → claims → contradictions → synthèse → vérification → décision de suffisance.
- `EvidenceGraph` garde les liens source → preuve → affirmation → contradiction → conclusion.
- `JsonRunStore` écrit des checkpoints JSON atomiques, avec état, révision, contexte, graphe et historique des agents ; c'est la meilleure base existante pour rendre une recherche reprenable.
- La persistance des runs ne remplace pas encore un index de mémoire global, une consolidation périodique ni une recherche transversale entre dossiers.

### Contrat d'intégration proposé

- **Research Engine** produit un dossier de recherche, ses sources, preuves, affirmations, contradictions, conclusions et checkpoints.
- **HCSM** valide les objets cognitifs structurés et impose les champs de provenance/contexte/fenêtre/incertitude quand le type d'objet le requiert.
- **Cognitorium** consomme les preuves et propositions, les affiche avec leur statut épistémique et attend une validation humaine lorsque nécessaire.
- **Watchtower** fournit le contexte géospatial et les données d'observation ; les observations restent distinctes des interprétations.
- **Monorepo** indexe les fiches et l'état des projets, mais n'est pas la base d'exécution unique de toutes les applications.

## 6. Architecture cible de mémoire — en réutilisant le stock

Ne pas implémenter un second moteur complet avant d'avoir relié les briques existantes. Le découpage minimal à prototyper est :

1. **Mémoire active / contexte de travail** : état de session Watchtower et tâche courante.
2. **Épisodes / runs** : checkpoints du Research Engine, décisions, corrections, résultats de tâche.
3. **Fiches de recherche Markdown** : une fiche principale par question, liée aux sources et aux artefacts ; sous-dossiers uniquement si le volume le justifie.
4. **Mémoire conceptuelle** : concepts stabilisés, alias, relations, projets concernés et pointeurs vers les épisodes/preuves d'origine.
5. **Index de rappel** : recherche lexicale d'abord ; recherche sémantique/graphique seulement si un benchmark local démontre son utilité.
6. **Consolidation et oubli** : réduire la priorité des souvenirs rarement utiles, mais ne jamais effacer silencieusement une preuve source. Toute abstraction doit garder un chemin vers la source.
7. **Boucle qualité** : après chaque tâche, enregistrer objectif, résultat, écart, erreur/correction, décision de conservation et action d'amélioration.

## 7. Matrice de décision

| Élément | Décision | Motif |
|---|---|---|
| Watchtower Cesium et couches territoriales | **RÉUTILISER** | Base visuelle et géospatiale déjà substantielle |
| Watchtower contextStore | **RÉUTILISER / ADAPTER** | Très bon contexte actif ; aucune persistance durable |
| Watchtower analystEngine | **RÉUTILISER** | Requêtes sur données chargées et suivi de relance limités |
| Watchtower dossiers.js | **RÉUTILISER / ADAPTER** | Arbre de navigation utile ; ajouter identifiants/provenance normalisés |
| Proto decay.ts | **RÉUTILISER AVEC RÉSERVE** | Heuristique utile pour simulation, pas validation scientifique |
| Proto epistemics.ts | **RÉUTILISER** | Garde-fou de statut et d'inférence |
| Proto ROME matching + catalogue | **RÉUTILISER / AUDITER** | Forte valeur métier ; vérifier données, génération et provenance |
| Proto localStorage metacog | **ADAPTER** | Conserver UX, extraire le stockage dans un service commun |
| CLE | **RÉUTILISER** | Boucle apprentissage/feedback/transfert alignée avec l'amélioration continue |
| Research Engine + JsonRunStore | **RÉUTILISER EN PRIORITÉ** | Runs reprenables et graphe de preuves déjà conçus |
| HCSM validator | **RÉUTILISER COMME CONTRAT** | Valide l'admissibilité ; n'est pas un estimateur cognitif |
| Copies `watchtower-mods` dans COGNITORIUM/monorepo | **DÉDUPLIQUER LOGIQUEMENT** | Garder l'archive, déclarer une source canonique et tracer les versions |
| Ajouter maintenant Mem0/Letta/Cognee ou un autre moteur externe | **DIFFÉRER** | Évaluer seulement après un test de lacunes face aux briques existantes |

## 8. Vérifications encore nécessaires

- Exécuter réellement les suites de tests/build sur une machine de travail et enregistrer les versions d'environnement.
- Auditer les branches actives et les différences entre le dépôt canonique, les copies et les branches de travail.
- Inspecter les schémas d'export/import et la persistance réelle des graphes Cognitorium.
- Vérifier si les fiches de recherche Markdown sont déjà générées par des scripts ailleurs dans le monorepo.
- Faire un inventaire des dépendances/licences et des sources de données, notamment pour Watchtower.
- Définir un test de référence : interrompre/reprendre une recherche, retrouver une fiche par formulation différente, mettre à jour un fait contradictoire, et vérifier que la preuve originale reste accessible.
- Comparer les résultats avec et sans index lexical/graphique ; ne choisir une base vectorielle ou un graphe supplémentaire qu'après mesure.

## 9. Sources de code principales

- [Watchtower — package.json](https://github.com/Sathancabrol/watchtower/blob/main/package.json)
- [Watchtower — contextStore.js](https://github.com/Sathancabrol/watchtower/blob/main/src/data/contextStore.js)
- [Watchtower — analystEngine.js](https://github.com/Sathancabrol/watchtower/blob/main/src/data/analystEngine.js)
- [Watchtower — dossiers.js](https://github.com/Sathancabrol/watchtower/blob/main/src/data/dossiers.js)
- [Proto-Cognitorium — decay.ts](https://github.com/Sathancabrol/proto-cognitorium/blob/main/src/utils/decay.ts)
- [Proto-Cognitorium — epistemics.ts](https://github.com/Sathancabrol/proto-cognitorium/blob/main/src/utils/epistemics.ts)
- [Proto-Cognitorium — romeMatching.ts](https://github.com/Sathancabrol/proto-cognitorium/blob/main/src/utils/romeMatching.ts)
- [Proto-Cognitorium — MetacogLoopView.tsx](https://github.com/Sathancabrol/proto-cognitorium/blob/main/src/components/MetacogLoopView.tsx)
- [Cognitorium — CLE architecture](https://github.com/Sathancabrol/COGNITORIUM/blob/main/learning/ARCHITECTURE.md)
- [HCSM — data schema](https://github.com/Sathancabrol/HCSM/blob/main/specs/data-schema.md)
- [HCSM — validator](https://github.com/Sathancabrol/HCSM/blob/main/validator/README.md)
- [Research Engine — README](https://github.com/Sathancabrol/reaserch-engine/blob/main/README.md)
- [Research Engine — persistence.py](https://github.com/Sathancabrol/reaserch-engine/blob/main/engine/persistence.py)
- [Cognitorium — historical global audit](https://github.com/Sathancabrol/COGNITORIUM/blob/main/docs/audits/internal/001-audit-global.md) (historical claims must be revalidated against current trees)


## 10. Autres dépôts et modules de l'écosystème (« + etc. »)

| Dépôt / dossier | Contenu repéré | Décision provisoire |
|---|---|---|
| `ETAT-DE-LART-PSYCHOLOGIE` | Cartographie critique 2020–2026, stratégies de recherche, protocole PRISMA, taxonomie, modèles CSV, scripts d'ajout/validation, vues HTML de taxonomie | **Réutiliser comme corpus et pipeline documentaire**, mais auditer la qualité et la traçabilité de chaque entrée. L'arbre consulté contient 37 fichiers et aucun fichier de test nommé comme tel ; ce n'est pas une preuve d'absence de tests manuels, mais la validation automatisée doit être vérifiée. |
| `animation-chronos` | Application React/Vite, étapes d'animation et composants de révélation progressive, drawer monographique, contrôles d'observation | **Réutiliser les patterns UX** de découverte graduelle pour CLE/Cognitorium ; pas un moteur mémoire. Le manifeste contient aussi `@google/genai`, donc ne pas le considérer local-first sans adaptation. |
| `Language-decoder` | README seul dans l'arbre actuel consulté | **Classer en attente / à définir**. Ne pas lui attribuer une capacité d'exécution avant de trouver du code ou une autre branche pertinente. |
| `monorepo/projects/frontignan` | Analyse territoriale, vision 2026–2040, deck HTML, rapport Markdown/HTML, figures et scripts de génération | **Réutiliser comme contenu et démonstrateur Atlas**, pas comme moteur cartographique autonome. Connecter ensuite les scénarios et indicateurs aux couches de Watchtower via un contrat explicite. |
| `monorepo/projects/proto-cognitorium/raw/` | Sources brutes, référentiels et documents de chantier (PDF/XLSM notamment) | **Conserver comme sources**, indexer les métadonnées et produire des fiches dérivées avec pointeurs vers les originaux ; ne pas recopier les documents dans chaque module. |
| Modules chantier de Watchtower | `src/chantier.js` et modules géospatiaux/lieux, ainsi que les documents de chantier présents dans l'archive | **Réutiliser après audit métier**. Vérifier que les workflows, formulaires, données de terrain et contrôles réglementaires ne sont pas seulement des écrans ou prototypes. |
| Nexus OS / BTP en dépôt autonome | Aucun dépôt portant exactement ces noms n'est présent dans la liste des dépôts accessibles consultée ; des éléments peuvent néanmoins exister sous d'autres noms ou dans des branches/fichiers d'archive | **Non conclu** : rechercher les noms et manifests dans l'ensemble des branches et de l'arborescence du monorepo avant de déclarer ces modules absents. |

### Inventaire quantitatif initial des dépôts (arbre `main` consulté)

| Dépôt | Fichiers suivis repérés | Fichiers dont le nom correspond à test/spec | Lecture |
|---|---:|---:|---|
| `watchtower` | 583 | nombreux fichiers `.test.mjs` et scripts QA | Base applicative la plus substantielle du périmètre géospatial ; compter les tests exécutables au prochain passage |
| `proto-cognitorium` | 184 | plusieurs composants et scripts ; tests non encore quantifiés dans ce passage | Prototype fonctionnel étendu, avec serveur et dépendances cloud |
| `COGNITORIUM` | 131 | surtout documentation, CLE et archive Watchtower | Agrégateur, gouvernance, apprentissage et archive de modules |
| `HCSM` | 87 | validateur Python et tests présents | Contrat scientifique et garde-fous, non moteur d'inférence complet |
| `reaserch-engine` | 61 | suite de tests Python visible | Moteur de recherche/reprise de run |
| `ETAT-DE-LART-PSYCHOLOGIE` | 37 | aucun nom de test repéré | Corpus et outils de recherche documentaire |
| `animation-chronos` | 30 | un chemin de test/spec repéré | Démonstrateur d'UX progressive |
| `Language-decoder` | 1 | aucun | README uniquement dans `main` |
| `monorepo` | 1 806 | inventaire, previews, projets copiés et nombreux documents | Archive/agrégateur ; ses copies ne prouvent pas que les versions sont synchronisées |

Ces nombres décrivent les fichiers suivis dans les arbres consultés sur la branche `main`, pas les lignes de code, la maturité produit ou l'état de toutes les branches.

## 11. Licence, provenance et risque d'intégration

Le dépôt Watchtower affiche une licence MIT pour le code, mais son fichier `LICENSE` exclut explicitement les données tierces du périmètre de cette licence. Il signale notamment des données de câbles sous-marins TeleGeography sous CC BY-NC-SA 3.0 (non-commercial, partage à l'identique), ainsi que des données OSM/ Open Infrastructure Map sous ODbL et des flux soumis aux conditions de chaque fournisseur.

**Conséquence :** on peut envisager de réutiliser le code sous MIT en respectant ses conditions, mais il faut créer un registre séparé des données/actifs, avec licence, attribution, restrictions commerciales, conditions API, date de vérification et procédure de retrait. Le statut open source du dépôt ne rend pas automatiquement tous les jeux de données utilisables commercialement.

## 12. Prochaine tranche d'audit automatisé

Ordre de travail recommandé :

1. **Réconcilier les branches et les copies** : lister branches actives de chaque dépôt, comparer les versions de `watchtower-mods` entre `watchtower`, `COGNITORIUM` et `monorepo`, puis désigner une source canonique par module.
2. **Chercher les modules cachés** : scanner tous les manifests et dossiers de toutes les branches pertinentes, en particulier Nexus OS, BTP, Atlas et simulateur cognitif ; produire une matrice de chemins, pas une liste de noms supposés.
3. **Tester les moteurs existants** : build/tests Watchtower, tests Research Engine, validateur HCSM, lint/build proto-Cognitorium, puis conserver les logs et les versions.
4. **Tracer le cycle de recherche** : vérifier si une recherche peut réellement être reprise depuis `JsonRunStore`, exporter une fiche Markdown, indexer la fiche, la retrouver avec une formulation différente et suivre chaque conclusion jusqu'à sa preuve.
5. **Ne choisir aucune nouvelle base de mémoire avant le benchmark** : comparer d'abord la solution légère existante (JSON + Markdown + recherche lexicale + EvidenceGraph) à un éventuel moteur externe sur un jeu de tâches représentatif.


## 13. Découvertes majeures dans les branches — correctif de l'inventaire

La lecture des rapports déjà présents dans `audit/convergence-2026-10-10`, puis les comparaisons de branches ciblées, révèlent que certains modules importants ne sont pas dans `main`. Il faut donc **traiter les branches comme du stock réel à examiner**, pas comme du bruit.

| Élément découvert | Branche / chemin | Éléments observés | Décision |
|---|---|---|---|
| **NEXUS·OS** | `monorepo:arena/01a08385-monorepo/nexus_os/` | Runtime d'agents, registre de 22 agents, routage de modèles, tools, MCP, contexte/compression, mémoire JSON de faits/décisions/leçons, tâches, évaluations, UI FastAPI | **Candidat majeur à réutiliser pour Nexus et l'orchestration.** La présence du code ne prouve pas encore sa sûreté ni son fonctionnement ; auditer permissions, sandbox, secrets, tests et persistance. |
| **Carré d'As / moteur d'agents** | `monorepo:arena/0034230e-monorepo/carredas/` | Contrat canonique, validation d'admissibilité, générateur de documents, cycle plan → recherche → production → revue → vérification → mémoire ; fiches d'agents Markdown | **Candidat à comparer à Nexus OS avant toute fusion.** Éviter deux orchestrateurs parallèles : choisir un runtime canonique et garder l'autre comme adaptateur, interface ou prototype si ses fonctions sont distinctes. |
| **BTP — conduite de travaux** | `monorepo:arena/01a08449-monorepo/projects/btp-conduite-travaux/` | Dashboard, corpus de 154 documents décrit dans le README, inventaire avec empreintes, matrice de traçabilité, rapports, études de prix, DCE, sécurité et réception | **Module substantiel en branche, non présent dans la version actuelle de main au même niveau.** Préserver cette branche et vérifier le delta complet avant intégration ; ne pas reconstituer le module depuis les documents bruts. |
| **Watchtower INTEL / Atlas Thau** | `watchtower:arena/dec9cd88-watchtower` | Dossiers Frontignan/Thau, import CSV, veille officielle, imprévus TP, attributs territoriaux, sources, tests dédiés et données territoriales | **Branche à examiner avant de construire Atlas.** Elle contient déjà une couche territoriale et chantier plus spécifique que le seul globe général. |
| **Watchtower OSINT Workbench** | `COGNITORIUM:watchtower/osint-workbench-v0.1/watchtower-mods/src/osint/` | Registre de sources, observations, cas d'enquête, relations, export JSON, distinctions FACT/INFERENCE/HYPOTHESIS/UNKNOWN et validation humaine dans la spécification | **Réutiliser comme modèle OSINT et de cas d'enquête**, après comparaison avec les modules du dépôt Watchtower et le contrat canonique Carré d'As. Certains éléments sont encore une démo/spécification, pas une intégration prouvée au runtime principal. |
| **Language-decoder — moteur humain** | `Language-decoder:arena/01a05471-language-decoder/` | 12 modules Python, schéma JSON, UI, CLI/serveur et `tests/test_engine.py` ; licence CC-BY-4.0 déclarée dans `pyproject.toml` de cette branche | **Candidat central pour le pont HCSM ↔ Cognitorium.** Le dépôt `main` ne contient qu'un README ; ne pas déclarer le projet vide sans inspecter ces branches. La licence et la provenance doivent suivre la branche intégrée. |
| **Language-decoder — maquettes et mémoire** | `Language-decoder:arena/01a05429-language-decoder/` | Dashboard, ontologie, données de mémoire, session simulée, monde 2040 et documentation de minimisation/incertitude | **Conserver comme matériaux de conception**, puis réconcilier avec le moteur Python de l'autre branche. |
| **Inventaire des fonctionnalités** | `monorepo:arena/93b54a79-monorepo/docs/FEATURES-INVENTORY.md` | Inventaire fonctionnel des modules et apps, portail/office et outils auxiliaires | **Réutiliser comme source d'indexation**, en recalculant les statuts à partir des SHA courants. |
| **Catalogue outils/données** | `monorepo:feat/tool-data-catalog-2026-10` | `data/tool_registry.json`, `data/module_registry.json`, schémas canoniques et graphe d'intégration | **Réutiliser le modèle de registre** au lieu de créer un troisième catalogue parallèle. |
| **Squelette d'interface unifiée** | `monorepo:feat/final-interface-skeleton-2026-10-07` | Registre d'interface, slots et preview dans FastAPI/Jinja | **Comparer avec le shell Carré d'As** et l'interface actuelle avant de choisir une UI canonique. |
| **Audit automatique des lacunes** | `monorepo:feat/gap-driven-audit-2026-10-11` | `audit_gaps.py`, inventaire de branches paginé, index de branches, file de preuves à examiner, distinction découverte de fichiers / lecture sémantique / tests runtime | **Réutiliser en priorité** pour la suite de l'audit. C'est déjà l'implémentation du protocole « chercher les branches non auditées » ; ne pas recréer ce scanner dans une autre branche. |
| **Audit de convergence précédent** | `monorepo:audit/convergence-2026-10-10` | Plan, taxonomie, état, journal, rapports par projet, graphe, script de mémoire, tableau transversal et historique des branches | **Réutiliser comme mémoire d'audit antérieure**, en revérifiant les SHA : le document mentionne déjà des écarts, dont deux tests rouges dans Research Engine et un drift de fichiers proto-Cognitorium, à recontrôler avant d'en tirer une conclusion actuelle. |

### 13.1 Conséquence architecturale

Le stock de mémoire est plus riche que la première passe ne le laissait penser :

- `nexus_os/memory.py` : mémoire JSON persistante `fact / decision / lesson`, rappel lexical et horodatage ;
- `carredas` : fiches Markdown d'agents et cycle de travail qui se termine par la consignation en mémoire ;
- `reaserch-engine` : checkpoints de run et graphe de preuves ;
- `Language-decoder` : dynamique temporelle, rétention/réactivation/transfert et objets avec provenance ;
- `proto-cognitorium` : décroissance heuristique des compétences et journal métacognitif ;
- `HCSM` : contrat de contexte, temporalité, provenance et incertitude ;
- `watchtower` : contexte de session, événements, observations et dossiers d'enquête ;
- `feat/gap-driven-audit` : index persistant des branches, statuts d'audit et file de lacunes.

**Conclusion mise à jour :** il ne faut pas démarrer un moteur de mémoire neuf. Il faut comparer et connecter ces implémentations. La priorité devient la convergence des contrats, la sélection d'un runtime d'agents canonique, l'indexation Markdown et la preuve de rappel/reprise par tests.

### 13.2 Attention aux divergences

Les branches `audit/convergence-2026-10-10`, `feat/tool-data-catalog-2026-10`, `feat/final-interface-skeleton-2026-10-07`, `arena/93b54a79-monorepo`, `arena/0034230e-monorepo`, `arena/01a08385-monorepo` et `arena/01a08449-monorepo` sont divergentes par rapport à `main`. Ne pas les fusionner en bloc : comparer les deltas fichier par fichier et relancer les vérifications après résolution des conflits.

### 13.3 Statut de validation

- **Vérifié statiquement :** présence des chemins, contenu de fichiers ciblés, différences de branches retournées par l'API GitHub.
- **Déclaré par la documentation de branche :** nombres de modules/agents, résultats de tests antérieurs et fonctions présentées comme prêtes.
- **Non vérifié ici :** exécution de builds/tests, sécurité réelle du sandbox, qualité de l'inférence humaine, fonctionnement complet des interfaces et compatibilité de fusion.


## 14. Décisions proposées pour convergence mémoire et intégration

### 14.1 Ne pas fusionner les mémoires avant de normaliser leur contrat

| Système | Persistance actuelle visible | Rappel visible | Decay / consolidation | Usage cible |
|---|---|---|---|---|
| Nexus OS `nexus_os/memory.py` | JSON local, faits/décisions/leçons horodatés | score lexical par mots communs, date en départage | pas de decay/consolidation visibles dans le fichier inspecté | mémoire des agents et leçons d'exécution |
| Carré d'As `carredas/modules/agents/` | fiches Markdown d'identité/rôle, génération de documents et cycle de travail | registre/routage déterministe ; mémoire de cycle dans le pipeline | pas de moteur universel de decay établi dans les fichiers consultés | runtime déterministe, documents de dossier, mémoire des agents |
| Research Engine | checkpoints JSON par run et graphe de preuves | reprise du run et récupération des objets de preuve | persistance d'exécution, pas encore mémoire transversale démontrée | mémoire épisodique / recherche |
| Language-decoder `dynamics.py` | données d'observation et profils structurés ; persistance globale à confirmer | objets de sortie décodés ; index global non établi | rétention, réactivation et transfert modélisés | dynamique temporelle du fonctionnement humain |
| proto-Cognitorium `decay.ts` | état de prototype, notamment journal navigateur limité | graphe/ressources de l'application | décroissance heuristique des compétences | visualisation et hypothèse de travail sur la réactivation |
| Watchtower `contextStore.js` | mémoire de session en `window` | entité/contexte actif | pas de consolidation durable visible | mémoire de travail UI |
| Audit gap-driven | index JSON de branches et queue de preuves prévue | retrouver l'état d'audit et les éléments non examinés | statut d'audit et détection de drift, pas mémoire personnelle | mémoire de travail de l'agent d'audit |

Le futur service de mémoire doit être un **adaptateur commun** au-dessus de ces stockages, pas une copie qui efface les responsabilités spécialisées. Il peut commencer par indexer des fiches Markdown et conserver des pointeurs stables vers les runs, preuves, profils et dossiers d'origine.

### 14.2 Contrat minimal recommandé

Chaque objet qui traverse les modules devrait pouvoir porter, selon son type :

- `id` stable et `kind` explicite (observation, claim, preuve, concept, expérience, décision, leçon, tâche, run, dossier) ;
- `content` ou référence vers un artefact, sans copier automatiquement les documents sources ;
- `source_ref`, `provenance`, `created_at`, `observed_at`, `retrieved_at`, et fenêtre de validité si pertinente ;
- `status` parmi `fact / inference / hypothesis / unknown` (ou correspondance explicitement documentée) ;
- `confidence` seulement si sa définition et son échelle sont connues ; ne pas confondre confiance, qualité de source et certitude ;
- `project_ids`, `task_id`, `run_id`, relations et références croisées ;
- `last_used_at`, `retrieval_count`, `salience` ou équivalent pour prioriser le rappel, sans supprimer la preuve source ;
- `human_validation` et historique de correction quand une personne a validé/rejeté une inférence.

Le schéma canonique de `carredas/core/canonical.py` est un candidat sérieux à confronter au schéma HCSM et au schéma `decoded-human` de Language-decoder. Ne pas créer un quatrième schéma sans comparer leurs champs et leurs contraintes.

### 14.3 Benchmark d'acceptation minimal

| Test | Procédure | Critère d'acceptation |
|---|---|---|
| Reprise de recherche | Lancer un run, l'interrompre après une preuve, relancer depuis son checkpoint | même `run_id`, preuves déjà collectées conservées, reprise sans doublons silencieux |
| Rappel par paraphrase | Stocker une fiche Markdown avec termes métier ; la demander avec synonymes/contexte différent | retrouver la fiche correcte et montrer le chemin vers les preuves ; mesurer les faux positifs |
| Contradiction | Ajouter une observation incompatible plus récente | conserver les deux sources, dater le conflit, ne pas écraser l'ancien fait sans trace |
| Decay et récupération | Rendre une connaissance peu saillante, puis la demander explicitement | baisse de priorité active sans perte de l'artefact ; réactivation accessible |
| Provenance bout en bout | Suivre une affirmation affichée dans Watchtower/Cognitorium vers sa source | source, date, statut et transformation consultables |
| Correction humaine | Rejeter une inférence et réexécuter une tâche similaire | la correction est conservée comme leçon, mais ne transforme pas rétroactivement la preuve en fait |
| Minimisation | Indexer un document local sensible | index sans copie inutile du contenu intégral ; source locale et politique de rétention explicites |

Le seuil de réussite et le jeu de données doivent être fixés avant d'ajouter une base vectorielle ou un service mémoire externe. Mesurer au minimum : précision@k, rappel@k, taux d'affirmations sans preuve, perte de provenance, duplications après reprise, taux de correction et coût de rappel.

### 14.4 Source canonique et copies Watchtower

Décision provisoire par responsabilité :

- `Sathancabrol/watchtower` : source canonique de l'application Watchtower et de ses composants déjà intégrés dans cette application.
- `Sathancabrol/COGNITORIUM:watchtower/osint-workbench-v0.1` : prototype de workbench OSINT à comparer puis porter sélectivement ; ne pas considérer la branche comme automatiquement intégrée à Watchtower.
- `monorepo/projects/COGNITORIUM/watchtower-mods` : copie d'archive/agrégateur utile à l'exploration ; ne pas modifier cette copie en espérant que le dépôt Watchtower soit mis à jour automatiquement.
- `monorepo:arena/93b54a79-monorepo` et `monorepo:arena/01a08385-monorepo` : archives de fonctionnalités et prototypes ; fusionner seulement après comparaison fraîche des deltas.

Ce choix est une règle de gouvernance proposée pour éviter les forks involontaires ; il ne prétend pas que les copies sont identiques.

### 14.5 Blocages honnêtes

Aucun workflow CI associé au commit de cet audit n'a été trouvé dans les résultats consultés. Les tests des dépôts n'ont donc pas été exécutés ni certifiés par ce rapport. L'ancien audit de convergence signale deux tests rouges dans Research Engine ; il faut vérifier si ces échecs sont toujours actuels en lançant la suite sur un clone local ou via un workflow CI autorisé. La branche Language-decoder contient un fichier de tests, mais sa présence ne vaut pas réussite.
