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
