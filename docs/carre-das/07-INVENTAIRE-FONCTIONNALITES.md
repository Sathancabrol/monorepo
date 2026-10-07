# Inventaire des fonctionnalités — **rien ne doit manquer**

**Statut :** `FAIT` (inventaire + récupération) · **Date :** 7 octobre 2026 · **Périmètre :** les 9 dépôts de `Sathancabrol` + toutes leurs branches + le monorepo lui-même.
**Question posée :** « toutes les fonctionnalités disponibles dans tous les dépôts doivent être présentes ici ».
**Réponse :** elles y sont maintenant **toutes**. Ce document le prouve, fichier par fichier, et dit **où chaque fonctionnalité atterrit dans Carré d'As**.

---

## 1. Le contrôle, chiffres à l'appui

| Étape | Résultat |
|---|---|
| Fichiers comparés dans les 8 dépôts satellites (HEAD de `main` vs `projects/` du monorepo) | **1 114** fichiers |
| Fichiers manquants au départ | **26** → tous restaurés (25 composants de `proto-cognitorium/src` + 1 `.gitignore`) |
| Branches contenant du travail **jamais fusionné** sur `main` | **17 branches** dans 6 dépôts |
| Fichiers importés depuis ces branches | **1 026** → **786 uniques** après retrait de **240 doublons exacts** (46,2 Mo économisés, liste dans les `_DEDUP.md`) |
| Gros fichiers non importés automatiquement (> 2 Mo) | **17** → vérifiés un par un : **16 existaient déjà** dans le dépôt, **1 importé en seconde passe** (`laplace_nebula.png`) |
| **Couverture finale** | **100 %** — aucun fichier, aucune branche, aucune fonctionnalité laissée de côté |

**Preuve rejouable :** `python3 scripts/verif-completude-repos.py` (compare à nouveau chaque dépôt et chaque branche avec le monorepo).

### Les 25 composants qui étaient perdus (et qui sont revenus)

C'étaient les plus importants : ils portaient l'**onboarding**, le **graphe** et le **CV**.

`CognitoriumGuidedSequence` (55 Ko) · `CognitoriumObsidianGraph` (49 Ko) · `TargetedCvView` (46 Ko) · `MultiProjectsView` (35 Ko) · `CognitoriumNodeVolant` (33 Ko) · `CvEditModal` (33 Ko) · `CognitoriumOrganicStudio` (31 Ko) · `CognitiveBiasesView` (19 Ko) · `cognitoriumCatalog` (18 Ko) · `VolantSidebar` (18 Ko) · `CognitoriumAuthPortal` · `CognitoriumSignUpFlow` · `AccountLoginGate` · `ProfileManagementModal` · `TopHeaderBar` · `CognitoriumLiveTreeVisualizer` · `CognitoriumTutorialOnboarding` · `CognitoriumVolantSkeleton` · `SkyrimIntroTransition` · `CognitoriumBrandSplash` · `CognitoriumErrorBoundary` · `cvAlignment` · `cvTypes` · `cognitiveBiasesData` · `authTypes`

### Où tout se trouve maintenant

```
projects/
├── COGNITORIUM/ …………… visualisation cognitive + gouvernance + learning engine  (131 fichiers, complet)
├── proto-cognitorium/ …… l'app la plus avancée : 111 fichiers src + corpus raw  (184 fichiers, complet)
├── ETAT-DE-LART-PSYCHOLOGIE/  cartographie critique PRISMA 2020              (37, complet)
├── HCSM/ …………………… modèle scientifique d'état cognitif                      (87, complet)
├── reaserch-engine/ …… moteur de recherche autonome (evidence-first)          (61, complet)
├── Language-decoder/ …  décodage de langage multimodal                        (1 + 51 importés)
├── watchtower/ ……… poste de travail cartographique (2D/3D)                   (583, complet)
├── animation-chronos/ … animations d'identité visuelle                        (30, complet)
├── frontignan/ ………… analyse territoriale + atlas                             (complet + 21 importés)
└── _incoming/   ……… TOUT le travail des branches, par dépôt et par branche
                     16 dossiers, chacun avec son _PROVENANCE.md (dépôt · branche · commit · liste des fichiers)
```

Chaque dossier de `_incoming/` commence par un `_PROVENANCE.md` qui dit : dépôt d'origine, nom de la branche, **SHA du commit**, nombre de fichiers, ce qui a été écarté et pourquoi.

---

## 2. Le trésor caché dans les branches (ce qui n'était nulle part dans `main`)

| Dépôt · branche | Fonctionnalité | Fichiers | Où c'est maintenant |
|---|---|---|---|
| **monorepo** · `arena/01a08385` | **NEXUS·OS** — 8 fournisseurs / 20 modèles, 22 agents, 22 outils sandboxés, serveur MCP, 147 tests | 93 | `_incoming/monorepo/arena_01a08385-monorepo/nexus_os/` |
| **monorepo** · `arena/01a08449` | **Module BTP complet** : 154 documents sources en 7 familles, inventaire SHA-256, matrice de traçabilité, moteur multi-agents, synthèse chantiers & prix | 239 | `_incoming/monorepo/arena_01a08449-monorepo/projects/btp-conduite-travaux/` |
| **monorepo** · `arena/171a1f38` | **Audit** : 52 constats, analyse V1→V5, journal, mémoire, plan | 37 | `_incoming/monorepo/arena_171a1f38-monorepo/audit/` |
| **monorepo** · `feat/final-interface-skeleton-2026-10-07` | **Command Center** + `interface_registry.json` (12 catégories, couverture des sources) | 7 | `_incoming/monorepo/feat_final-interface-skeleton-2026-10-07/` |
| **monorepo** · `feat/tool-data-catalog-2026-10` | **Contrats de module** (JSON Schema), `module_registry`, `tool_registry`, graphe d'intégration | 11 | `_incoming/monorepo/feat_tool-data-catalog-2026-10/` |
| **monorepo** · `arena/01a08203` | **Atlas de Frontignan** (données, cartes, nœuds, communes THAU) | 21 | `_incoming/monorepo/arena_01a08203-monorepo/projects/frontignan/atlas/` |
| **COGNITORIUM** · `watchtower/osint-workbench-v0.1` | **OSINT Workbench** : registre, dossier, preuves, démo + spec et roadmap complètes | 12 | `_incoming/COGNITORIUM/watchtower_osint-workbench-v0.1/watchtower-mods/` |
| **proto-cognitorium** · `arena/01a08342` | Évolutions de l'app (14 fichiers src) | 14 | `_incoming/proto-cognitorium/arena_01a08342-proto-cognitorium/` |
| **watchtower** · `arena/01a072e1` | **Poste de travail territorial** : barre 24 fonctions, volant, bascule 2D/3D, `INTEL-TERRITOIRE.md` (grille ✅📅🔮⚠️) | 144 | `_incoming/watchtower/arena_01a072e1-watchtower/` |
| **watchtower** · `arena/dec9cd88` | Évolutions antérieures (53 fichiers) | 53 | `_incoming/watchtower/arena_dec9cd88-watchtower/` |
| **ETAT-DE-LART** · `arena/01a04f7b` | **Application complète** : app Flask (concepts, lab, stats), **agent de recherche scientifique** (planificateur, collecte, vérification, rapport), 299 fichiers | 299 | `_incoming/ETAT-DE-LART-PSYCHOLOGIE/arena_01a04f7b-…/` |
| **ETAT-DE-LART** · `arena/01a03aac`, `01a07d32`, `01a045a1` | Interfaces web, inventaire GitHub, monorepo docs, agent Python (3 variantes) | 45 | `_incoming/ETAT-DE-LART-PSYCHOLOGIE/…` |
| **Language-decoder** · `arena/01a05471` | **Package `language_decoder`** : decoder, dynamics, evidence, functioning, inference + CLI + docs de fondements | 24 | `_incoming/Language-decoder/arena_01a05471-…/` |
| **Language-decoder** · `arena/01a05429` | Dashboard, ontologie, mémoire, monde 2040, conversations, design visuel | 27 | `_incoming/Language-decoder/arena_01a05429-…/` |

---

## 3. La matrice : **quel dépôt apporte quoi, et où ça va dans Carré d'As**

Légende des paliers : **V1** = la première version livrable · **V1.5** · **V2** = plus tard. Aucune ligne n'est « abandonnée ».

### 3.1 `proto-cognitorium` — l'application la plus avancée (React + TypeScript)

| Fonctionnalité (fichier) | Nature | Destination dans Carré d'As | Palier |
|---|---|---|---|
| `OnboardingModal`, `CognitoriumGuidedSequence`, `CognitoriumTutorialOnboarding`, `CognitoriumBrandSplash`, `SkyrimIntroTransition` | parcours d'entrée guidé | **le premier lancement** (P1/P2 du plan) | V1 |
| `CognitoriumAuthPortal`, `CognitoriumSignUpFlow`, `AccountLoginGate`, `ProfileManagementModal` | compte & profils | écran **Système › Comptes** | V1 |
| `VolantSidebar`, `CognitoriumNodeVolant`, `CognitoriumVolantSkeleton`, `TopHeaderBar`, `Header`, `MotionCreateButton` | **le « volant »** : navigation radiale + barre haute | **shell Carré d'As** (rail + barre + palette) | V1 |
| `NetworkGraph`, `TemporalNetworkGraph`, `CognitoriumObsidianGraph`, `TreeView`, `CognitoriumLiveTreeVisualizer`, `MetiersGraph`, `GraphLegendModal`, `NodeInspectorModal` | 6 représentations du même modèle | **V3 « L'Arbre »** + module **Graphe** | V1→V1.5 |
| `DashboardView`, `CognitiveSignature`, `DecayTimeline`, `MetacogLoopView` | tableau de bord cognitif, décroissance, métacognition | **Command Center** + module **Cognition** | V1→V1.5 |
| `ValidationCenterModal`, `ExperienceDistillerModal`, `QuickAddNodeModal`, `utils/epistemics` | **distillation + validation humaine** (✅📅🔮⚠️) | **cœur du produit** : la règle « toute proposition IA est validable » | V1 |
| `TargetedCvView`, `CvEditModal`, `cvAlignment`, `cvTypes` | CV ciblé (adapter le CV à une offre) | module **Documents › CV** | V1.5 |
| `MultiProjectsView` | plusieurs projets en parallèle | **V1 « Le Carré »** (la porte Projets) | V1 |
| `CognitiveBiasesView`, `cognitiveBiasesData` | biais cognitifs | module **Cognition** (mode expert) | V2 |
| `PsychologyAtlasView`, `PsyRefView`, `psyRefLibrary`, `psyRefSources` | atlas de psychologie + références | module **Référentiels** | V2 |
| `ExperimentStudio`, `MesEvaluationsView`, `evaluationsCatalog`, `experimentCatalog` | atelier d'expériences et évaluations | module **Recherche** | V2 |
| `ResourcesView`, `savoirs/*`, `atlas/*`, `lab/*`, `cognitoriumCatalog` | bibliothèque de ressources + ateliers | module **Fiches & Références** | V1.5 |
| `data/romeData.ts`, `utils/metiersGraphData`, `HorizonsBridge`, `MetiersGraph` | ROME, métiers, passerelles | module **Métiers** | V1.5 |
| `data/*Profile.ts` (amélie, gianni, nathan, pierre, étudiant, transition) | **profils de démonstration** | jeux d'essai + **mode présentation** | V1 |
| `utils/decay`, `graphDimensions`, `nodeVisualDescriptor`, `resourceSearch` | moteurs (décroissance, mise en page, recherche) | **Core** | V1 |
| `CognitoriumErrorBoundary` | robustesse (un module qui plante ne tue pas l'app) | exigence **contrat de module** | V1 |

### 3.2 `watchtower` — le poste de travail territorial

| Fonctionnalité | Destination | Palier |
|---|---|---|
| Globe 3D + bascule 2D/3D (2D MapLibre = 3 ms, Cesium = 21 357 ms mesurés) | **module Carte** : 2D par défaut, 3D à la demande | V1.5 |
| Barre de 24 fonctions, volant, panneaux | **shell** (inspiration directe) | V1 |
| `INTEL-TERRITOIRE.md` : grille de vérité ✅📅🔮⚠️ | **règle d'affichage** dans toute l'app | V1 |
| Mode GRATUIT / PAYANT (chaque fonction payante a sa version gratuite) | **principe** : aucune fonction essentielle derrière une clé API | V1 |
| `AGENTS.md`, `ROADMAP.md`, `DATA_SOURCES.md`, `audit/` | gouvernance + registre de sources | V1 |
| Dette identifiée : 366 `getElementById`, 9 623 lignes de CSS | **à ne pas reproduire** : composants + design tokens | V1 |

### 3.3 `COGNITORIUM` — la doctrine

| Fonctionnalité | Destination | Palier |
|---|---|---|
| `docs/constitution/` (vision, principes, journal de décisions) | **gouvernance du produit** | V1 |
| `docs/etat-des-lieux/`, `docs/audits/`, `docs/architecture/`, `docs/agents/` | dossier de cadrage | V1 |
| **Learning Engine PoC** (« Comprendre l'argent » : troc → monnaie → inflation…) | module **Apprentissage** | V2 |
| `watchtower-mods/` + **OSINT Workbench** (importé) | module **Veille/OSINT** | V2 |
| 11 visuels d'interface datés (27 juil → 1er août) | **design system** (analyse dans `04`) | V1 |

### 3.4 `HCSM` — le modèle scientifique

| Fonctionnalité | Destination | Palier |
|---|---|---|
| Ontologie, spécifications, `validator/` (32 fichiers), `scientific/`, `papers/` | **Core** : le modèle de données Cognitorium, versionné et validable | V1.5 |
| Figures et documentation (16 docs) | Références scientifiques affichées dans l'app | V2 |

### 3.5 `reaserch-engine` — le moteur de recherche autonome

| Fonctionnalité | Destination | Palier |
|---|---|---|
| Pipeline : question → plan → recherche → preuves → affirmations → contradictions → synthèse → **vérification** → suffisance | module **Agents › Recherche** | V1.5 |
| `schemas/` (9), `tests/` (12), `engine/` (23), `docs/` (15) | idem + **garde-fous de qualité** | V1.5 |

### 3.6 `ETAT-DE-LART-PSYCHOLOGIE` — la rigueur scientifique

| Fonctionnalité | Destination | Palier |
|---|---|---|
| Cartographie critique PRISMA 2020, 12 domaines, équations de recherche reproductibles | module **Référentiels › Psychologie** | V2 |
| Base 42 champs (14 entrées validées, trust avg 73,2) + guide IA de remplissage | **modèle de fiche scientifique** (réutilisé pour les fiches ID) | V1.5 |
| App Flask (concepts, lab, stats) — *importée d'une branche* | module **Ateliers** | V2 |
| Agent Python de recherche scientifique (planificateur, LLM, rapport) — *importé* | fusion avec `reaserch-engine` | V1.5 |

### 3.7 `Language-decoder` — le langage

| Fonctionnalité | Destination | Palier |
|---|---|---|
| `language_decoder` (decoder, dynamics, evidence, functioning, inference, CLI) — *importé* | module **Langage & Notes** (analyse de texte, conversations) | V2 |
| Data : ontologie, mémoire, monde 2040, session simulée, dashboard | idem + jeux de données de démonstration | V2 |

### 3.8 `frontignan` — le territoire

| Fonctionnalité | Destination | Palier |
|---|---|---|
| Analyse territoriale (249 sources, 13 fiches projets, 11 sections) | module **Territoire** | V1.5 |
| Vision 2026→2040 + deck 18 slides autonome (export PDF) | **mode présentation** | V1 |
| Atlas (données + images + communes THAU) — *importé* | module **Carte › Atlas** | V1.5 |
| 14 figures matplotlib + générateurs Python | module **Stats & dataviz** | V1.5 |

### 3.9 `animation-chronos` — le visuel

| Fonctionnalité | Destination | Palier |
|---|---|---|
| Animations (ferrofluide, cœur de conscience, pont hémisphérique) | **identité visuelle** + écran de démarrage | V1 |

### 3.10 Les branches du monorepo — le chantier en cours

| Fonctionnalité | Destination | Palier |
|---|---|---|
| **NEXUS·OS** : 8 fournisseurs / 20 modèles, 22 agents, 22 outils sandbox, **MCP**, 147 tests | module **Agents** (le vrai cœur « IA ») | V1.5 |
| **Module BTP** (154 documents, 7 familles, matrice de traçabilité, multi-agents, prix) | module **BTP** | V1 |
| **Contrats de module** (`module.schema.json`, `canonical-record.schema.json`), registres | **le contrat plug in/out** | V1 |
| **Command Center** + `interface_registry.json` (12 catégories) | **V1 « Le Carré »** + navigation | V1 |
| **Audit** (52 constats, analyse V1→V5, journal) | gouvernance + feuille de route | V1 |

---

## 4. Vue inversée : chaque module de Carré d'As est déjà alimenté

| Module / écran de Carré d'As | Ce qui l'alimente (déjà présent dans le dépôt) |
|---|---|
| **Command Center / 4 portes** | `DashboardView`, `MultiProjectsView`, `interface_registry.json` (Command Center), frontignan (présentation) |
| **Documents** (154 pièces) | `btp-conduite-travaux` (corpus + inventaire), `TargetedCvView` + `cv/`, Marker/MinerU (recherche) |
| **Carte** | watchtower (2D/3D, 24 fonctions), atlas Frontignan, `INTEL-TERRITOIRE`, IGN/DVF |
| **BTP** | `arena/01a08449` : 154 docs, prix, métrés, multi-agents, matrices |
| **Cognition** | `proto-cognitorium` (dashboard, decay, biais, métacognition), `HCSM` (modèle) |
| **Graphe / Arbre** | 6 représentations de `proto-cognitorium`, `html ghierarchi.png` (le modèle tranché) |
| **Agents** | **NEXUS·OS** (22 agents, MCP), `reaserch-engine`, agent scientifique de l'état de l'art |
| **Recherche / Veille** | `reaserch-engine` + **OSINT Workbench** |
| **Référentiels & Fiches** | `ETAT-DE-LART-PSYCHOLOGIE` (42 champs), `psyRefLibrary`, `ROME`, Kiwix/ZIM (recherche `06`) |
| **Territoire** | `frontignan` (rapport + vision + atlas + 14 figures) |
| **Langage & Notes** | `Language-decoder` (2 branches) |
| **Système / Comptes** | `auth/*`, `ProfileManagementModal`, `CognitoriumErrorBoundary`, Google `drive.appdata` |
| **Apprentissage** | Learning Engine PoC de `COGNITORIUM` |

**Il n'existe donc aucune fonctionnalité orpheline** : les 9 dépôts et leurs 17 branches sont tous rattachés à un module de l'application.

---

## 5. Ce qui reste à faire (et qui n'est pas de la récupération, mais de l'intégration)

1. **Trancher la forme** : je propose de **garder `_incoming/`** comme archive de référence (avec ses `_PROVENANCE.md`) et de **porter dans `projects/<dépôt>/` uniquement ce qui entre dans la V1** — sinon on duplique deux fois le même code et on ne sait plus lequel fait foi.
2. **Fusionner `reaserch-engine` + l'agent scientifique de l'état de l'art** : deux moteurs qui font presque la même chose (c'est le cas typique « conserver / fusionner » de ton mandat).
3. **Aligner `HCSM` sur le Core** de Carré d'As (c'est lui qui donne le modèle de données).
4. **Extraire NEXUS·OS** de la branche vers un module **Agents** propre (147 tests déjà écrits = un vrai atout).
5. **Choisir l'interface** (les 3 maquettes de `04`) — puis figer le design system à partir des visuels de `COGNITORIUM` et de l'expérience `watchtower`.

## 6. Comment vérifier toi-même

```bash
python3 scripts/verif-completude-repos.py        # compare les 8 dépôts + les branches avec le monorepo
python3 scripts/verif-completude-repos.py --branches   # inclut le détail branche par branche
```

Le script ne modifie rien : il liste ce qui manquerait. Attendu aujourd'hui : **« aucun fichier manquant »**.
