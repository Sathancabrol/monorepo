# ANALYSE V1 → V5 — Importance de chaque élément des dépôts pour l'application finale Cognitorium

**Statut : `ANALYSE`** — ce document **ordonne** le chaos ; il ne restructure rien. Aucune donnée déplacée, aucun code fusionné.
**Date** : 2026-10-07 · **Base** : `audit/AUDIT-2026-10.md` + les branches distantes + `data/interface_registry.json` (branche `feat/final-interface-skeleton-2026-10-07`)
**But** : attribuer à chaque élément proposé dans les repos un **niveau v1→v5** (vague d'intégration dans l'application finale), pour préparer la restructuration.

---

## 0. En une page

| Question | Réponse (résumé) |
|---|---|
| Qu'est-ce que l'application finale ? | **12 domaines d'interface** (Command Center → System), **8 entités Core** (User·Project·Knowledge·Skill·Object·Place·Task·Event), une chaîne de valeur en 11 étapes (comprendre → … → apprendre du résultat). |
| Combien d'éléments classés ? | **79 éléments** dans 9 dépôts + 8 branches + 2 dossiers locaux (détail machine : `audit/data/importance.json`). |
| Répartition | **v1 = 20** · **v2 = 23** · **v3 = 16** · **v4 = 10** · **v5 = 2** · **v0/archive = 8**. |
| Le constat central | Le « Core » (v1) **n'existe quasi nulle part en code** : il est spécifié (ADR-007, data-model, HCSM) mais non construit. À l'inverse, les briques **v2/v3 existent déjà en abondance** (watchtower, proto, ETAT, reaserch-engine) — **mais sur des branches non fusionnées**. |
| Ce que dit l'international | Les plateformes de référence (Palantir, Graphiti/Zep, World Monitor, Earth AI) convergent sur : **ontologie opérationnelle centrale**, **bi-temporalité native**, **provenance par épisode**, **fusion multi-source avouant ses lacunes**, **orchestration agentique au-dessus**, **contrats d'interface**. Ce sont exactement les briques v1 à ne pas improviser. |
| La conséquence pour la restructuration | On ne range pas par projet (9 dépôts) mais **par domaine cible** (12) → les dépôts deviennent des **fournisseurs** ; la coquille `monorepo` les assemble. L'ordre v1→v5 est la séquence de restructuration. |

---

## 1. La cible, telle qu'elle est écrite dans les dépôts (sourcée)

| Élément de cible | Source exacte |
|---|---|
| Vision : « Semantic Operating System for Human + Knowledge + World + Design + Action » | `projects/COGNITORIUM/docs/constitution/00-vision.md` |
| Chaîne : comprendre → représenter → mobiliser → apprendre → explorer → concevoir → simuler → décider → fabriquer → observer → apprendre du résultat | idem |
| Équation : Skill Graph + Knowledge Graph + Learning Engine + World Graph + Digital Twin + World Model + Design Engine + CAD + Simulation + Manufacturing + AI Agents = COGNITORIUM | idem |
| Phases 0→7 (Core · Skill/CLE · Gods Eye View · Design Engine · 3D/CAD · Fabrication · Agents) | `projects/COGNITORIUM/docs/constitution/04-roadmap.md` |
| 8 entités Core + provenance/incertitude/contexte | `projects/COGNITORIUM/docs/architecture/data-model.md` |
| Base unique : PostgreSQL + pgvector + Apache AGE + PostGIS (ADR-007) | `projects/COGNITORIUM/docs/architecture/target.md` |
| 8 câblages de convergence (qui consomme quoi, en quelle phase) | `projects/COGNITORIUM/docs/architecture/convergence.md` |
| **12 domaines de l'interface finale** (le squelette réel de l'app) | `data/interface_registry.json` — branche `feat/final-interface-skeleton-2026-10-07` |
| Règle d'intégration : « le monorepo est la coquille ; les dépôts sources restent autorités tant qu'une brique n'est pas migrée/testée/validée » | `docs/AUDIT-INTEGRATION-INTERFACE-FINALE-2026-10-07.md` |
| Positionnement : « la couche qui oriente, relie et orchestre » (ne pas remplacer NVIDIA/Google/Palantir/Autodesk) | `constitution/00-vision.md`, `08-competitors.md` |

**Les 12 domaines cibles** (avec leur état actuel déclaré dans le registre) :

| # | Domaine | État déclaré | Sources déclarées |
|---|---|---|---|
| 1 | Command Center | skeleton | monorepo |
| 2 | World / Territory | partial | watchtower, frontignan |
| 3 | Intel / OSINT | partial | watchtower, watchtower-mods, reaserch-engine |
| 4 | Projects / BTP | partial | watchtower, btp-conduite-travaux |
| 5 | Human / Cognition | partial | proto-cognitorium, HCSM, Language-decoder |
| 6 | Knowledge / Research | partial | ETAT-DE-LART, reaserch-engine, HCSM |
| 7 | Learning Engine | prototype | COGNITORIUM |
| 8 | Simulation / Lab | partial | proto, ETAT, animation-chronos |
| 9 | Design / CAD / Fabrication | **missing** | COGNITORIUM |
| 10 | Nexus / Agents | branch | nexus_os, reaserch-engine |
| 11 | Data / Memory / Provenance | partial | HCSM, reaserch-engine, watchtower, monorepo |
| 12 | System / Settings | skeleton | nexus_os, watchtower, monorepo |

---

## 2. Comment c'est fait à l'international (multi-domaine, multi-modal, temporel)

Six références examinées, six leçons directement applicables au classement v1→v5.

| Référence | Ce qu'elle fait | Leçon pour Cognitorium | Niveau impacté |
|---|---|---|---|
| **Palantir Foundry/Gotham** ([analyse](https://www.puppygraph.com/blog/palantir-ontology), [détail 3 couches](https://blog.pebblous.ai/project/CURK/ontology/palantir-vs-classic-ontology/en/)) | Ontologie **opérationnelle** en 3 couches : *Semantic* (objets, propriétés, liens) + *Kinetic* (actions, fonctions, sécurité) + *Dynamic* (apprentissage) ; couche **matérialisée et indexée** (pas de fédération pure) ; CDC pour rester à jour ; LLM branché **sur** l'ontologie (« OAG »), pas à côté | Le Core n'est pas un schéma mort : il doit porter des **actions** et rester **indexé**. À acter en v1, sinon tout le reste se construit sur du sable | **v1 (Core)** |
| **Graphiti / Zep** ([repo](https://github.com/getzep/graphiti), [papier Zep](https://storage.ghost.io/c/79/c4/79c4903e-2432-4c0e-b8c8-c8988fef71ec/content/files/2025/01/ZEP__USING_KNOWLEDGE_GRAPHS_TO_POWER_LLM_AGENT_MEMORY_2025011700.pdf)) | Graphe **bi-temporel** : temps valide *T* (quand c'est vrai dans le monde) + temps d'ingestion *T′* ; **invalidation d'arêtes** (on ne supprime jamais, on périme) ; tout fait trace vers un **épisode** (provenance totale) ; retrieval hybride sémantique+BM25+graphe, sub-seconde | La **temporalité est un choix de schéma dès v1** : HCSM a déjà *temporal state* + *uncertainty* + *provenance* → c'est lui le contrat. Un journal d'événements (épisodes) vaut mieux qu'un CRUD | **v1 (schéma)** |
| **World Monitor** ([repo](https://github.com/anwarchk/worldmonitor-ai)) | Fusion multi-sources temps réel : clustering par région/pays, sévérité, **détection d'anomalie par baseline temporelle** (90 jours), **circuit breakers** par flux, « **show what you can't see** » (déclarer les sources en panne au lieu de les cacher), corrélation multi-signaux (aucune source seule ne déclenche), cache 3 niveaux, APIs contract-first | L'INTEL de watchtower est proche *visuellement* mais pas *analytiquement* (pas de baseline, pas de gaps visibles, pas de corrélation). C'est le saut v3 à prévoir — pas à improviser maintenant | **v3 (Intel)** |
| **OSIRIS** ([analyse](https://techloghub.com/open-source/osiris)) | OSINT géospatial : MapLibre GPU, 15 calques intelligents, flux live (aviation, sismique, CCTV, news, GDELT, maritime…), panneaux par domaine | Le pattern « **un canevas, N flux, des panneaux** » est déjà celui de watchtower — la référence confirme le choix, et donne la liste des flux manquants (GDELT, scanner) | **v2→v3** |
| **Google Earth AI** ([papier](https://arxiv.org/html/2510.18318v2)) | Modèles géospatiaux multi-modaux **orchestrés par un agent de raisonnement** ; croisement de domaines séparés ; limite reconnue : **alignement des granularités spatiales/temporelles** | L'orchestration agentique est **l'aboutissement**, pas le point de départ. Confirme l'ordre : Core+données (v1) → domaines (v2) → agents (v3) → fusion multi-modale (v4) | **v3→v4 (agents)** |
| **Fusion multi-INT** ([article](https://geospatialworld.net/article/multi-int-intelligence-effective-multi-sensor-data-fusion/)) | La fusion a besoin de raisonnements **spatial, temporel et hiérarchique** supportés par la base ; analyse récursive continue de l'état des entités | PostGIS + temps + hiérarchie (AGE) ne sont pas des options « GIS » : ce sont des **capacités de raisonnement du Core** | **v1 (PostGIS/AGE)** |

**Les 6 règles internationales convergentes** → appliquées au classement :

1. **Ontologie d'abord** (Palantir) → HCSM + data-model sont **v1**, pas des docs.
2. **Bi-temporalité native** (Graphiti) → décision de schéma **v1** ; migrer plus tard coûte cher.
3. **Provenance = épisode** (Graphiti) → `JsonRunStore`, preuves watchtower, sources frontignan sont **v2** (premiers producteurs d'épisodes).
4. **Fusion qui avoue** (World Monitor) → les « gaps » INTEL sont **v3**, une feature, pas un détail.
5. **Agent au-dessus, pas à la place** (Earth AI) → nexus_os **v3**, pas v1.
6. **Contract-first** (World Monitor/OSIRIS + règle d'intégration monorepo) → le registre `interface_registry.json` est **v1**.

---

## 3. La grille v1 → v5 (définition opérationnelle)

| Niveau | Nom | Critère d'affectation | Test simple |
|---|---|---|---|
| **v1** | **Socle** | Sans cet élément, l'app finale n'existe pas ; tout le reste en dépend ; ou bien : le corriger *plus tard* coûte très cher (schéma, licences, hygiène). | « Si on le rate, on reconstruit tout ? » |
| **v2** | **Cœur d'usage** | Première valeur quotidienne réelle pour l'utilisateur ; briques déjà quasi prêtes ; première version publique crédible. | « Peut-on montrer l'app sans ça ? » |
| **v3** | **Puissance analytique** | Rend le système *intelligent* (INTEL avancé, agents noyau, learning, métier BTP) ; dépend de v1+v2 stabilisés. | « Est-ce que ça exploite les données déjà là ? » |
| **v4** | **Conception & simulation** | Transforme l'observateur en concepteur (labo, simulation, CAD, multimodal avancé) ; gros chantiers neufs. | « Est-ce qu'on *crée* ou est-ce qu'on *regarde* ? » |
| **v5** | **Horizon** | Fabrication, world model, jumeau numérique complet : aucune base existante aujourd'hui, à garder en vision. | « Est-ce réaliste dans les 2-3 ans ? » |
| **v0** | **Archive / hors-vision** | Doublons, code mort, données à risque, travail abandonné : à figer proprement, ne pas intégrer. | « Est-ce que ça contredit ou duplique la cible ? » |

**Barème d'état réutilisé** (issu de l'audit) : `existe` (testé/mesuré) · `branche` (prêt, non fusionné) · `fragment` (partiel) · `spécifié` (doc seulement) · `absent`.

---

## 4. Tableau maître — les 12 domaines cibles

> Lecture : chaque ligne = un élément réel, nommé exactement, avec sa source. « v » = vague d'intégration.

### D1 · Command Center — la coquille

| Élément | Source | État | v | Pourquoi |
|---|---|---|---|---|
| Interface finale (HTML/CSS/JS + 12 domaines) | `app/templates/interface.html`, `app/static/interface.{css,js}` + `data/interface_registry.json` — branche `feat/final-interface-skeleton-2026-10-07` | branche | **v1** | C'est **le** squelette de l'app finale ; rien ne se range sans lui |
| Coquille FastAPI (explorateur, previews, garde anti-traversée, token serveur) | `app/main.py` (753 l.) — monorepo `main` | existe | **v1** | L'intégration fonctionne déjà ; c'est le point d'ancrage |
| Registre des outils/données (9 domaines, 5 capacités, règle « référencer→adapter→normaliser→extraire ») | `docs/TOOL-DATA-CATALOG.md` — branche `feat/tool-data-catalog-2026-10` | branche | **v1** | Gouvernance d'intégration : évite le re-doublonnage pendant la restructuration |
| Tableau de bord global, recherche globale, timeline d'activité | domaine 1 du registre (skeleton) | spécifié | **v2** | Utile quand ≥ 3 domaines sont branchés |
| Snapshot GitHub rafraîchi + daté en UI | `data/github_inventory.json` (périmé 07/09) | existe (périmé) | **v1** | Information fausse en UI = perte de confiance immédiate |

### D2 · World / Territory — le monde

| Élément | Source | État | v | Pourquoi |
|---|---|---|---|---|
| Globe Cesium, ~29 calques (avions, navires, satellites, séismes, feux, radio, CCTV…), docks, vues territoire, épingles, bâti 3D | `projects/watchtower` — 583 f., 190 453 l., 208 tests | existe | **v2** | Le cœur « World » est **déjà le plus avancé du dépôt** ; seule brique prête pour une v2 |
| Barre unique de fonctions, **carte 2D IGN**, minicarte, volant, panneau FIL, archives/crues, charge mentale | branche `arena/01a072e1-watchtower` (+43 commits, 11 docs) | branche | **v2** | Architecture UI explicitement jugée « particulièrement réutilisable » par l'audit d'intégration |
| INTEL territorial Frontignan/Thau, import CSV, projets, lacunes, veille officielle, imprévus TP | branche `arena/dec9cd88-watchtower` = **PR #3** (CI verte) | branche | **v2** | Valeur territoiale immédiate ; 1 clic pour fusionner |
| Dossier territoire Frontignan : rapport 826 l., **249 sources datées**, vision 2040, deck 18 slides | `projects/frontignan` (hors GitHub) | existe | **v2** | Modèle de sourçage pour tout le domaine Territory/Knowledge |
| Atlas interactif Frontignan / « Cognitarium City » | branche `arena/01a08203-monorepo` | branche | **v3** | Enrichissement, pas socle |
| Couche « solar system » | watchtower | existe | **v5** | Démonstratif, hors chaîne de valeur |
| **Fork `watchtower-mods` (62/62 fichiers en doublon de watchtower)** | `projects/COGNITORIUM/watchtower-mods/` | doublon | **v0** | Source de vérité = `watchtower` ; archiver après décision |

### D3 · Intel / OSINT — la veille

| Élément | Source | État | v | Pourquoi |
|---|---|---|---|---|
| intelTwin, OSINT case, evidence registry, source registry, veille, empreinte économique | watchtower (main + PR #3) | fragment | **v3** | Nécessite le Core (provenance) et la corrélation |
| Dossier de recherche : claims, contradictions, suffisance | `reaserch-engine` (21 modules `engine/`) | existe (2 tests rouges) | **v2** | C'est le **moteur de preuves** ; alimente Intel ET Knowledge |
| Corrélation multi-signaux + **baseline temporelle** + **gaps visibles** | **absent** (à construire — modèle World Monitor) | absent | **v3** | Le saut qualitatif qui sépare « carte » de « renseignement » |
| OSINT workbench (modules + specs) | `projects/COGNITORIUM` — branche `watchtower/osint-workbench-v0.1` (+13) | branche | **v3** | À évaluer vs ce que watchtower apporte déjà (risque de doublon) |
| Flux GDELT, scanner, news | absent (références OSIRIS) | absent | **v3** | Élargit la couverture sans clé |
| Garde-fou « aucune fonctionnalité visant une personne physique » | `projects/watchtower/AGENTS.md` | existe | **v1** | Contrainte **éthique/ToS** transversale : à conserver comme règle du domaine |

### D4 · Projects / BTP — le métier

| Élément | Source | État | v | Pourquoi |
|---|---|---|---|---|
| Module BTP complet : corpus 154 sources, DCE→DOE, prix, DT/DICT/AIPR, sécurité, qualité, dashboard théorie/état-de-l'art/in-situ | branche `arena/01a08449-monorepo` (`projects/btp-conduite-travaux/`) | branche | **v3** | Domaine métier à haute valeur **mais** secondaire vs cognition/territoire |
| Corpus racine : 220 documents, 225 Mo, 12 familles | racine du monorepo | existe | **v3 données / v0 stockage** | Données = v3 ; leur **stockage en Git** = v0 (à externaliser) |
| Couche chantier watchtower : 81 fiches imprévus, suivi, géolocalisation engins | watchtower | fragment | **v3** | S'aligne sur le module BTP |
| Phasage 4D / BIM / jumeau numérique de chantier | registre domaine 4 (placeholder) | absent | **v4** | Dépend du 3D/CAD |
| Dossier de chantier dupliqué (154 fichiers sur la branche BTP **et** à la racine) | `projects/btp-conduite-travaux/documents_sources/` vs racine | doublon | **v0** | Dédupliquer avant fusion |

### D5 · Human / Cognition — l'humain

| Élément | Source | État | v | Pourquoi |
|---|---|---|---|---|
| **HCSM** : ontologie YAML, constructs, observation/evidence/provenance/uncertainty/context/temporal state/inference, validateur V1/V5 (23 cas, 29 tests) | `projects/HCSM` | existe | **v1** | C'est **le vocabulaire canonique du Core** (ADR-009, câblage n°1) — le seul composant déjà testé de la couche sémantique |
| Profils (6), graphe de compétences 5 niveaux, ROME (1 911 fiches), decay, échelle épistémique, signature cognitive, CV alignment | `projects/proto-cognitorium` (53 334 l.) | existe | **v2** | Le « Human » est le deuxième pilier ; attention : **copie locale périmée de 25 fichiers** → resynchroniser d'abord |
| Atlas psychologie + PsyRef + labo (expériences, évaluations, métacognition, boucles) | proto, composants `PsychologyAtlasView`, `ExperimentStudio`, `MetacogLoopView`, `data/psychologyAtlas.ts` | existe | **v2 (atlas) / v4 (labo)** | L'atlas = connaissance v2 ; le labo = simulation v4 |
| **Language-decoder** : moteur Python 12 modules (ontology, decoder, inference, dynamics, functioning, profile, evidence), schéma `decoded-human`, UI dashboard | branche `arena/01a05471-language-decoder` + `arena/01a05429` | branche | **v2** | « Décodage du langage » = entrée naturelle vers le profil cognitif ; tout est écrit, rien n'est fusionné |
| 3 bases de connaissances psy concurrentes (proto `psychologyAtlas`/`psyRefLibrary`/`psyRefSources` vs ETAT CSV vs HCSM YAML) | proto + ETAT + HCSM | doublon | **v1 (décision)** | **ADR-009 à fermer** : 1 propriétaire par donnée, sinon le Core naîtra avec 3 vérités |
| Biais cognitifs, métacognition, histoire de vie | proto (`cognitiveBiasesData.ts`, distant) | fragment | **v3** | Enrichissement du profil |

### D6 · Knowledge / Research — le savoir

| Élément | Source | État | v | Pourquoi |
|---|---|---|---|---|
| reaserch-engine : question → plan → retrieval → evidence → claims → contradictions → synthèse → vérification → suffisance (21 modules, 9 schémas, `JsonRunStore`) | `projects/reaserch-engine` | existe (**2 tests rouges**, pas de manifeste) | **v2** | Moteur épistémique complet ; les 2 tests rouges sont à corriger **avant** intégration |
| ETAT-DE-LART : base 42 champs, app FastAPI+SQLite, taxonomie, PRISMA, scripts DOI, 4 visualisations D3 | `projects/ETAT-DE-LART-PSYCHOLOGIE` | existe | **v2** | Contenu scientifique sourcé prêt à nourrir le Knowledge Graph |
| Agent de recherche littéraire, cosmos, 221 sorties | branche `arena/01a04f7b-ETAT-DE-LART` (+38 commits) | branche | **v2** | Le plus gros gisement non fusionné du domaine |
| Cognitorium v8 (graphe 3D, 40 fiches) | branche `arena/01a03aac-ETAT-DE-LART` (+2) | branche | **v3** | Visualisation avancée |
| Méthode Talbot v4.2 (registre de claims ✅/⚠️/❌, 12 corrections, 7 fabrications éliminées) | `docs/synthese-talbot-2026/` | existe | **v1 (méthode)** | Fournit **le protocole de provenance** que le Core doit appliquer ; à généraliser en registre de claims |
| Frontignan : 249 sources datées + balises de statut | `projects/frontignan` | existe | **v2** | Déjà conforme au protocole |
| Rédaction d'articles / paper writing | registre domaine 6 | absent | **v4** | Dépend de la synthèse stabilisée |

### D7 · Learning Engine — apprendre

| Élément | Source | État | v | Pourquoi |
|---|---|---|---|---|
| CLE : `learning-engine.js`, PoC « turboréacteur », PoC « money », architecture | `projects/COGNITORIUM/learning/` | fragment | **v3** | Phase 2 de la roadmap ; dépend du Skill Graph persistant (v2) |
| Scénario / challenge / operations cognitives / boucle adaptative / transfert | registre domaine 7 (prototype) | fragment | **v3** | Le vrai différenciateur pédagogique, mais après le socle profil |
| Pattern de révélation progressive | `animation-chronos` (`ProgressiveDiscoveryBar`) | existe | **v4 (composant)** | Sert l'onboarding, pas le moteur |

### D8 · Simulation / Lab — explorer

| Élément | Source | État | v | Pourquoi |
|---|---|---|---|---|
| Experiment Studio + catalogue d'évaluations + boucle métacognitive | proto (`ExperimentStudio.tsx`, `evaluationsCatalog.ts`, `MetacogLoopView.tsx`) | existe | **v4** | Le labo devient utile quand des données réelles l'alimentent |
| Graphes temporels & réseau interactifs | proto (`TemporalNetworkGraph.tsx`, `NetworkGraph.tsx`) | existe | **v3 (viz) / v4 (analyse)** | Brique de lecture du temps — réutilisable plus tôt comme visualisation |
| Expérience temporelle Chronos (9 composants : `VesselStage`, `InspectionLens`, `TransitionSequenceBar`…) | `projects/animation-chronos` | existe | **v4** | À intégrer **comme composant d'expérience**, jamais comme app séparée |
| Sandbox de simulation | registre domaine 8 (placeholder) | absent | **v5** | Nécessite moteurs physiques/données |

### D9 · Design / CAD / Fabrication — concevoir

| Élément | Source | État | v | Pourquoi |
|---|---|---|---|---|
| Décisions techniques CAD (Replicad + OpenCascade.js ; JSCAD CSG jetable) et slicer (OrcaSlicer local) | `constitution/03-architecture.md`, `docs/audits/external/004-stack-cad-fabrication.md` | spécifié | **v4 (CAD) / v5 (slicer)** | Rien à intégrer aujourd'hui ; les décisions sont déjà prises, c'est suffisant |
| three.js présent dans proto (rendu, pas de CAD) | proto (`package.json`) | fragment | **v4** | Base de départ du 3D objet |
| Espace objet 3D, CAO paramétrique, CSG, import/export, impression | registre domaine 9 (missing) | absent | **v4/v5** | Chantier neuf — **à ne pas commencer** avant v1-v3 |
| Book of Shapes / audit CAD | `docs/audits/external/002-bookofshapes.md`, `004-…` | existe (doc) | **v4 (socle doc)** | La recherche est déjà faite |

### D10 · Nexus / Agents — agir

| Élément | Source | État | v | Pourquoi |
|---|---|---|---|---|
| **nexus_os** : 22 agents JSON, routeur multi-provider + fallback, skills, tools, MCP, mémoire, runtime, runs/SSE, sandbox, evals, instincts (59 tests) | branche `arena/01a08385-monorepo` (`nexus_os/`) | branche | **v3** | Plateforme d'agents déjà testée — **le** candidat orchestration ; à brancher *après* le Core |
| 13 fiches d'agents (orchestrateur, research, data, CAD, simulation, GIS, learning, project, manufacturing, verification…) | `projects/COGNITORIUM/docs/agents/` | spécifié | **v3 (design)** | Le cahier des charges des agents existe ; nexus_os en est l'implémentation partielle |
| Agent de recherche reaserch-engine (1 agent réel) | reaserch-engine | existe | **v2** | Déjà fonctionnel — premier agent utile |
| Orchestrateur maison + MCP | `constitution/03-architecture.md` (ADR-008) | spécifié | **v3** | nexus_os fournit MCP + routeur : à réconcilier avec l'ADR |
| Creator d'agents, evals, sandbox d'exécution | nexus_os | branche | **v4** | Méta-outillage, dépend d'agents stabilisés |

### D11 · Data / Memory / Provenance — la mémoire (le cœur caché)

| Élément | Source | État | v | Pourquoi |
|---|---|---|---|---|
| **Base unique PostgreSQL + pgvector + Apache AGE + PostGIS (ADR-007)** | `architecture/target.md` + `data-model.md` | spécifié | **v1** | Palantir/Multi-INT le confirment : c'est **la** fondation ; tout câblage de convergence en dépend |
| **Schéma bi-temporel (temps valide T + temps d'ingestion T′)** | **absent** du data-model actuel (leçon Graphiti/Zep) | absent | **v1 (décision)** | À acter *avant* la première migration ; HCSM fournit déjà *temporal state* |
| HCSM : provenance, incertitude, observation/evidence/inference | `projects/HCSM` | existe | **v1** | Contrat sémantique du Core (câblage n°1) |
| `JsonRunStore` : un épisode JSON atomique par run + reconstruit le graphe | reaserch-engine (`engine/persistence.py`) | existe | **v2** | Premier producteur d'« épisodes » conforme au pattern international |
| Inventaires SHA-256, audit trail, import/export, frontière de vie privée, coffre à clés | registre domaine 11 | spécifié | **v2** | Hygiène de confiance |
| 5 mécanismes de persistance hétérogènes (localStorage ×2, JSON, SQLite, 39 clés watchtower) | les 9 projets | dette | **v0 (remplacer)** | À résorber par le Core, un par un — pas à maintenir |
| Mémoire d'audit (`state.json`, `MEMORY.md`, `JOURNAL.jsonl`, graphe) | `audit/` | existe | **v1 (méta)** | C'est l'outil pour piloter la restructuration sans re-scan |

### D12 · System / Settings — la confiance

| Élément | Source | État | v | Pourquoi |
|---|---|---|---|---|
| Politique secrets : zéro clé par défaut, `.env` 600, jamais commité, pas de `0.0.0.0` | `projects/watchtower/AGENTS.md` + `.env.example` ×4 | existe (partiel) | **v1** | Seul projet avec une doctrine complète ; à généraliser |
| Licences : décider pour les 6 projets sans licence ; attribuer le fork `watchtower` (MIT © Bilawal Sidhu) | audit C1 | manquant | **v1** | Bloque toute publication ; coût quasi nul maintenant |
| Modes gratuit/payant + pré-validation des clés (`keySetupCore.mjs`, 16 Ko) | watchtower | existe | **v2** | Réutilisable tel quel dans System/Settings |
| Provider manager (multi-LLM), plugins, feature flags, diagnostics, backup | nexus_os + registre domaine 12 | branche/skeleton | **v2** | Standard, à réutiliser plutôt qu'écrire |
| CI minimale (lint/build/tests) sur les 9 dépôts | audit C8 (1 CI sur 9) | manquant | **v1** | Garde-fou de la restructuration elle-même |

---

## 5. Transverse — hygiène, dette, archives (v1 et v0)

| Élément | Source | État | v | Action type |
|---|---|---|---|---|
| PR #3 watchtower (CI verte) | branche `arena/dec9cd88-watchtower` | branche | **v2** | fusionner |
| Branche watchtower +43 (UI réutilisable) | `arena/01a072e1-watchtower` | branche | **v2** | PR puis fusion |
| ETAT +38 (agent, cosmos, 221 sorties) | `arena/01a04f7b-ETAT-DE-LART` | branche | **v2** | revue puis fusion |
| Language-decoder (moteur + UI + tests) | `arena/01a05471` (+ `01a05429`) | branche | **v2** | PR vers `main` |
| proto resync (25 fichiers manquants dont auth/onboarding) | `projects/proto-cognitorium` | dette | **v1** | `git pull` + resync |
| 2 tests rouges reaserch-engine | `tests/test_agents.py`, `tests/test_research_strategy.py` | dette | **v1** | corriger (bloque la confiance) |
| 19 branches mortes | 9 dépôts | dette | **v0** | supprimer |
| `watchtower-mods` (doublon 62/62) | COGNITORIUM | doublon | **v0** | archiver |
| Dossier de chantier en double (racine vs branche BTP) | monorepo | doublon | **v0** | dédupliquer |
| 289 Mo de binaires en Git (225 + 64 Mo) | racine + `proto/raw` | dette | **v0** | externaliser (LFS/archive) + SHA-256 |
| Données RH sensibles (grilles salariales, corrigés AIPR) publiques | racine | risque | **v0** | décision : retirer / restreindre |
| Snapshot GitHub périmé | `data/github_inventory.json` | dette | **v1** | régénérer + dater |
| `reaserch-engine` mal orthographié | dépôt GitHub | dette | **v1 (cosmétique)** | renommer avant d'en faire la référence « Research » |
| ADR-009 (3 bases de connaissances) non tranchée | COGNITORIUM | décision | **v1** | fermer l'ADR |
| Doc `animation-chronos` inexistante | projet | dette | **v2** | README d'intention (ou archive M A) |

---

## 6. Où va chaque dépôt (résumé par source)

| Dépôt / source | Rôle dans l'app finale | Domaine(s) cible(s) | v global | Sort proposé (à décider) |
|---|---|---|---|---|
| `monorepo` (coquille) | **L'app elle-même** (intégration + UI) | D1, et accueil de tous | **v1** | conserver, renforcer |
| `HCSM` | **Contrat sémantique du Core** | D5, D11 | **v1** | promouvoir en autorité |
| `COGNITORIUM` (docs) | Gouvernance, vision, agents, méthode | D1, D10 | **v1 (docs)** | conserver comme autorité documentaire |
| `COGNITORIUM/learning` | Moteur d'apprentissage | D7 | **v3** | intégrer plus tard |
| `COGNITORIUM/watchtower-mods` | doublon | — | **v0** | archiver |
| `watchtower` (+2 branches) | **World/Territory + Intel + System** | D2, D3, D12 | **v2** | promouvoir en autorité « monde » |
| `proto-cognitorium` | **Human/Cognition + Lab** | D5, D8 | **v2** | resynchroniser puis démembrer par domaine |
| `ETAT-DE-LART` (+4 branches) | **Knowledge/Research** | D6 | **v2** | fusionner la branche, garder comme contenu |
| `reaserch-engine` | **Moteur de preuves** | D3, D6, D11 | **v2** | corriger tests, packager |
| `Language-decoder` (2 branches) | **Entrée cognition** | D5 | **v2** | PR vers `main` |
| `animation-chronos` | **Composant d'expérience temporelle** | D8 | **v4** | cesser d'être une app |
| `frontignan` | Contenu territoire exemplaire | D2, D6 | **v2** | dépôt dédié ou archive assumée |
| `nexus_os` (branche) | **Orchestration agents** | D10, D12 | **v3** | intégrer après Core |
| module BTP (branche) | Domaine métier | D4 | **v3** | intégrer après territoire |
| interface skeleton (branche) | **Le squelette de l'app** | D1 | **v1** | **fusionner en premier** |

---

## 7. L'ordre — la séquence de restructuration proposée (à décider, non exécutée)

**Étape 0 — Hygiène (préalable, ~1 semaine).** Fusionner PR #3 · resynchroniser proto · corriger les 2 tests rouges · licences (6 projets) + attribution du fork · CI minimale · régénérer le snapshot · décider du sort des 220 Mo et des données RH · supprimer les 19 branches mortes.

**Étape 1 — v1, le Socle.** Fusionner `feat/final-interface-skeleton` + `feat/tool-data-catalog`. Acter et construire : schéma Core **bi-temporel** (T/T′, episodes, invalidation) + PostgreSQL/pgvector/AGE/PostGIS (ADR-007) · HCSM promu contrat (ADR-009 fermée) · registre de claims (méthode Talbot généralisée) · politique secrets/licences. **Rien d'autre ne se construit avant.**

**Étape 2 — v2, la valeur visible.** World (watchtower main + 2 branches) · Human (proto resync + Language-decoder PR) · Knowledge (ETAT branche + reaserch-engine) · Territory (frontignan). Les dépôts deviennent des **fournisseurs branchés au Core**, pas des apps.

**Étape 3 — v3, la puissance.** Intel analytique (baseline, corrélation, gaps) · module BTP · Learning Engine · nexus_os (agents noyau) · viz temporelles. C'est ici que le système commence à « penser ».

**Étape 4 — v4, concevoir.** Simulation/Lab · Design/CAD (Replicad) · agents complets · multimodal avancé (fusion des granularités, leçon Earth AI).

**Étape 5 — v5, l'horizon.** Fabrication (slicer local) · world model · jumeau numérique complet.

**Règle de fusion** (reprise du registre) : `référencer → adapter → normaliser → extraire`. Et : une fonctionnalité n'est copiée que si elle devient un composant réellement partagé.

---

## 8. Ce qu'il ne faut PAS faire maintenant (anti-scope)

1. **Ne pas commencer le CAD / la fabrication** (v4/v5) même si c'est excitant : rien ne s'y branche aujourd'hui.
2. **Ne pas intégrer `watchtower-mods`** ni aucune copie : la source de vérité est unique.
3. **Ne pas construire d'agents avant le Core** : ils reproduiraient les 5 mémoires éclatées actuelles.
4. **Ne pas migrer dans PostgreSQL sans le schéma bi-temporel** : la reprise coûterait plus cher que la décision.
5. **Ne pas garder 3 bases de connaissances** : ADR-009 d'abord.
6. **Ne pas exposer de fonctionnalité visant des personnes physiques** (garde-fou watchtower, à ériger en règle du plateau).
7. **Ne pas garder les 289 Mo de binaires dans Git** pendant la restructuration : chaque clone les paiera.

---

## 9. Findings de l'analyse

| # | Sévérité | Constat | Preuve |
|---|---|---|---|
| F-V1-01 | **critique** | Le v1 (Core) est **spécifié mais pas construit** ; les 8 câblages de convergence en dépendent tous | `architecture/target.md` vs inventaire (0 fichier de schéma SQL) |
| F-V1-02 | élevé | La **bi-temporalité n'est nulle part dans le data-model** alors qu'HCSM la déclare déjà (`temporal state`) : la décision manque au moment où elle coûte le moins cher | `data-model.md` + benchmark Graphiti |
| F-V1-03 | élevé | Les briques **v2/v3 existent mais sur branches** : sans Étape 0, la restructuration partira d'un état faux | `branches-all.json` |
| F-V1-04 | élevé | L'app finale **dépend d'une décision à prendre** (ADR-009) qui traîne : 3 bases psy concurrentes | `convergence.md` règle 2 |
| F-V1-05 | moyen | Le domaine **D9 (Design/CAD) est `missing`** : c'est 2 niveaux (v4/v5) de la cible — cohérent avec la roadmap, mais à assumer | `interface_registry.json` |
| F-V1-06 | moyen | Le fossé INTEL : watchtower **montre** mais ne **corrèle** pas (pas de baseline, pas de gaps, pas de multi-signal decisional) | comparaison World Monitor |
| F-V1-07 | moyen | `frontignan` (PAS de dépôt) porte pourtant le **meilleur sourçage** du dépôt : risque de perte | audit C1/C7 |
| F-V1-08 | faible | Le vocabulaire de niveaux n'existait pas : chaque projet avait le sien — ce document le fige (v1→v5, v0 archive) | ce document |

---

## 10. Suite

- Machine : `audit/data/importance.json` (79 éléments : `id`, `element`, `source`, `domaine`, `etat`, `v`, `action`, triés v1→v0) — régénérable par script.
- Mémoire : `audit/state.json` (`analyse.v1v5`), journal, `MEMORY.md`.
- **La restructuration n'a pas commencé** : ce document est l'entrée de la phase suivante (« ordonner puis restructurer »). Prochaine décision attendue : **valider la grille v1→v5 et l'Étape 0**.
