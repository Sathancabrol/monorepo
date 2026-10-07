# SYNTHÈSE-TIMELINE — État du projet au 7 octobre 2026 (point de situation)

> **Nature de ce document** : photographie exhaustive à date — qui fait quoi, quelle branche apporte quoi, quels besoins sont couverts. C'est le **point zéro** à partir duquel la roadmap (`audit/ROADMAP-2050-2026.md`) descend vers maintenant.
> **Sources** : `audit/AUDIT-2026-10.md`, `audit/ANALYSE-V1-V5.md`, `audit/data/branches-all.json` (live 2026-10-07), `data/interface_registry.json`.
> **Conventions** : v1→v5 = vague d'intégration (ANALYSE-V1-V5) · domaines D1–D12 = domaines de l'interface finale · `+n` = commits d'avance sur `main` · statut live.
> **Révision du 2026-10-07 (soir)** : la matinée du 07/10 a produit un chantier nouveau (**Carré d'As** + dossier **recherche** + récupération `_incoming` + module **mail-organizer**) après mon relevé matinal. Intégré ici ; contrôle complet : `audit/notes/S5-controle-completude.md`.
> **Nommage acté par ce chantier** : **Cognitorium** = le système/écosystème (horizon) · **Carré d'As** = **l'application** (V1 installable, cible association loi 1901, Windows d'abord).

---

## 1. Chronologie du projet (ce qui s'est passé, avec dates vérifiées)

| Date | Événement | Preuve |
|---|---|---|
| 2018–2024 | Matériaux sources : dossier de chantier (marchés 2021–2024), publications de psychologie (2018), protocoles | racine + Drive |
| 2026-07-28 | Prompt AI Studio « Cognitarium City : Frontignan 2026 » (13 Mo) — matrice du produit frontignan | Drive |
| 2026-07-31 | Prompt AI Studio « Interface Cognitorium : Graphe Cognitif » (68 Mo) — matrice de proto-cognitorium | Drive |
| **2026-08-02** | Création du dépôt `COGNITORIUM` (vitrine + docs + learning) | GitHub |
| **2026-08-24** | Création de `proto-cognitorium` et `ETAT-DE-LART-PSYCHOLOGIE` | GitHub |
| **2026-08-25** | Création de `HCSM` (framework scientifique v0.1 + validateur V1/V5, fusionné le jour même) | GitHub |
| **2026-08-26** | Création de `reaserch-engine` (pipeline épistémique complet, 1 jour) | GitHub |
| **2026-08-30** | Création de `Language-decoder` (README seul) | GitHub |
| **2026-09-01** | Création de `watchtower` (fork God's Eye View + mods) | GitHub |
| **2026-09-02** | Création de `animation-chronos` (expérience visuelle) | GitHub |
| **2026-09-05** | **Phase 0 de la roadmap constitution : audit réalisé** — `docs/etat-des-lieux/` (9 fiches), architecture cible, ADR-001→010 | `constitution/04-roadmap.md` |
| **2026-09-07** | Création du `monorepo` (PR #1 : 8 projets + previews). Dernier push de COGNITORIUM, HCSM, ETAT | GitHub |
| 2026-09-07→08 | Branches monorepo : fix Starlette, **atlas Frontignan** (`01a08203`), index du dossier de chantier | `branches-all.json` |
| 2026-09-10 | Dernier push de `proto-cognitorium` (registre d'audit SEC-04/UX-04) — **la copie locale du monorepo reste 25 fichiers en retard** | `drift.json` |
| 2026-09-20 | « Cognitorium est en ligne » — vitrine hébergée Polsia (20 $/mois), cible à trancher (techniques/élus) | Gmail |
| 2026-10-01 | Relance Polsia : « Une piste pour Cognitorium » | Gmail |
| **2026-10-07** (matin) | **Journée charnière** : PR #2 fusionnée (index 220 docs) · **PR #3 ouverte** (watchtower INTEL, CI verte) · création des branches `nexus_os`, BTP, interface finale, catalogue, atlas · 2 branches Language-decoder (moteur) · espace **Linear** créé · audit produit (52 findings, 79 éléments v1→v5) | GitHub + connecteurs |
| **2026-10-07** 12:38 | Brief de recherche pour agent + **matrice de 80 domaines** (P0→P3) | branche `arena/0034230e` |
| 13:05 | **Carré d'As** : cadrage V1 + contrat de module + principes UI + spécification du module BTP | idem |
| 14:23 | **3 interfaces cliquables** (Le Carré · L'Atelier · L'Arbre) + réponses (licence/monétisation, séquence P0→P6, chronologie réelle) + écosystème local gratuit | idem |
| 14:38 | **Récupération complète** : 1 026 fichiers de toutes les branches (786 uniques, 240 doublons retirés) rangés dans `projects/_incoming/` avec `_PROVENANCE.md` + `verif-completude-repos.py` | idem |
| 14:39 | **Resync proto** (12 fichiers) + variante `frontignan/index.html` ; frontignan passe de 28 à 49 fichiers dans le monorepo | idem |
| 14:45 | Module **`mail-organizer`** (tri d'emails IMAP, 19 tests, stdlib) | branche `arena/93b54a79` |

**Lecture** : tout le projet a ~2 mois (02/08 → 07/10/2026). En 9 semaines : 9 dépôts, 283 478 lignes de code, **46 branches** (36 hors `main`, **17 avec travail non fusionné**), 16 PR fusionnées, 1 PR ouverte, **et zéro Core construit** — mais désormais un **nom, une cible et un contrat** (Carré d'As).

---

## 2. Quel dépôt fait quoi (fiches « rôle »)

| Dépôt | Rôle actuel réel | Ce qu'il contient | Apporte à la cible | Domaine(s) | v | Autorité proposée |
|---|---|---|---|---|---|---|
| **`monorepo`** | **La coquille d'intégration** (et futur produit) | FastAPI (explorateur + previews), 9 projets copiés, dossier racine 220 docs, snapshot GitHub, branches nexus/BTP/interface/catalogue | D1 Command Center : le squelette de l'app finale | D1+accueil | **v1** | devient **l'app** |
| **`watchtower`** | **Le monde** (le plus avancé : 190 453 l., 208 tests, seule CI) | Globe Cesium, 29 calques, docks, INTEL, chantier, 86 outils, doctor, Pinokio | D2 World/Territory + D3 Intel + D12 System | D2, D3, D12 | **v2** | autorité « monde » |
| **`proto-cognitorium`** | **L'humain** (53 334 l., 0 test) | Graphe compétences 5 niveaux, 6 profils, ROME 1 911, decay, épistémique, atlas psy, labo, CV | D5 Human/Cognition + D8 Lab | D5, D8 | **v2** | autorité « humain » (après resync) |
| **`HCSM`** | **Le contrat sémantique** (seul testé de sa couche : 29 tests + 23 cas) | Ontologie YAML, constructs, provenance/incertitude/contexte/temps, validateur V1/V5, CITATION | D11 Data/Memory — le vocabulaire du Core | D5, D11 | **v1** | autorité « sémantique » |
| **`reaserch-engine`** | **Le moteur de preuves** | Pipeline question→suffisance (21 modules), evidence graph, claims, contradictions, `JsonRunStore` | D6 Knowledge + D3 Intel + D11 épisodes | D3, D6, D11 | **v2** | autorité « recherche » |
| **`ETAT-DE-LART-PSYCHOLOGIE`** | **Le savoir scientifique** | Base 42 champs, app FastAPI+SQLite, PRISMA, taxonomie, scripts DOI, viz D3 | D6 Knowledge (contenu) | D6 | **v2** | autorité « contenu » |
| `frontignan` (hors GitHub) | **Le territoire (contenu exemplaire)** | Rapport 826 l. (249 sources datées), deck 18 slides, 14 figures, vision 2040 | D2 World/D6 (sourçage) | D2, D6 | **v2** | à doter d'un dépôt |
| **`Language-decoder`** | **L'entrée cognition** (main vide) | (branches) moteur 12 modules, schéma decoded-human, UI | D5 Human (décodage) | D5 | **v2** | à fusionner |
| **`COGNITORIUM`** | **La gouvernance + le moteur d'apprentissage** | Constitution 10 docs, état des lieux 9 fiches, 7 audits, 13 fiches agents, `learning/` CLE, fork watchtower-mods | D1 (doc) + D7 Learning | D1, D7 | **v1 doc / v3 code** | autorité **documentaire** |
| `animation-chronos` | **Le composant d'expérience temporelle** | 9 composants (VesselStage, InspectionLens, TransitionSequenceBar…), 0 doc | D8 (expérience) | D8 | **v4** | composant, pas app |
| `nexus_os` (branche) | **L'orchestration agents** | 22 agents JSON, routeur multi-provider, skills/tools/MCP, mémoire, runs/SSE, sandbox, evals (59 tests) | D10 Nexus | D10, D12 | **v3** | à promouvoir |
| module `btp` (branche) | **Le métier chantier** | 154 sources, DCE→DOE, prix, DT/DICT/AIPR, dashboard 3 volets | D4 Projects/BTP | D4 | **v3** | à promouvoir |

---

## 2 bis. Modules et chantiers (tout ce qui n'est ni dépôt ni copie)

| Module / chantier | Où | Contenu réel vérifié | Domaine | v |
|---|---|---|---|---|
| **Carré d'As** (le dossier de cadrage de l'app) | `docs/carre-das/` — branche `arena/0034230e` | 8 documents : cadrage V1 (installation 1 fichier, < 150 Mo, premier résultat < 5 min, hors ligne par défaut, données exportables), **contrat de module plug in/out** (manifeste `module.json`, permissions « rien par défaut », bus d'événements), principes UI (10 règles d'affordance), **spécification du module BTP** (7 piliers, 3D en 3 paliers), 9 concept arts + **3 interfaces cliquables**, réponses (licence recommandée **cœur Apache-2.0/MIT + services AGPL-3.0**, séquence P0→P6, ordre chronologique réel), écosystème local gratuit (modèles ≤ 6 Go de VRAM, 6 briques à créer), inventaire « rien ne manque » | D1 | **v1** |
| **Dossier recherche** (à confier à un agent) | `docs/recherche/` — même branche | Brief auto-suffisant + prompt + **matrice de 80 domaines** (`D01→D80`, priorités P0→P3, pistes vérifiées le 07/10 : Tauri 2, PGlite, LadybugDB (succède à Kuzu archivé), Graphiti/Zep, Extism, MCP/A2A…) + 10 chantiers P0 + enrichissements/arbitrages | D1/D11 | **v1** |
| **Récupération `_incoming`** | `projects/_incoming/` — même branche | **786 fichiers uniques** (1 026 importés − 240 doublons exacts) : 16 dossiers, chacun avec `_PROVENANCE.md` (dépôt, branche, SHA, écartés) — dont les **25 composants proto perdus** (onboarding, graphe Obsidian, CV ciblé, biais cognitifs, auth) | D11/accueil | **v1** |
| **Module BTP** (la brique forte) | `projects/btp-conduite-travaux/` — branche `arena/01a08449` + spec `03-MODULE-BTP.md` | **174 fichiers** : 154 documents (7 familles, 3 chantiers), 9 rapports (00→08) dont schéma directeur A→Z, données avec **SHA-256 par document**, **28 sous-détails de prix** avec simulateur déboursé sec/marge, dashboard 1,2 Mo, `engine/btp_multi_agent.py` ; spec cible : DCE/DQE/métrés, suivi, carte 2D IGN, 3D (3 paliers), IA locale (Granite 4.2 pour l'extraction) | D4 | **v3** |
| **nexus_os** (orchestration d'agents) | branche `arena/01a08385` | 85 fichiers : **22 agents**, 8 fournisseurs / 20 modèles avec fallback, 22 outils, **serveur MCP**, mémoire, runs/SSE, sandbox, evals — **~147 tests** (146 fonctions vérifiées) | D10 | **v3** |
| **mail-organizer** | branche `arena/93b54a79` | Tri automatique d'emails IMAP (règles configurables, jamais de suppression, extraction de pièces jointes, mode watch, statistiques), **19 tests**, zéro dépendance Python | D11 | **v3** |
| **OSINT Workbench** | branche `COGNITORIUM/watchtower/osint-workbench-v0.1` (12 fichiers récupérés) | Registre, dossier, preuves, démo + **OSINT-MASTER-SPEC** et roadmap | D3 | **v3** |
| **Atlas Frontignan** | branche monorepo `arena/01a08203` (21 fichiers) | Données, cartes, nœuds, communes du THAU — atlas interactif du dossier territoire | D2 | **v3** |

---

## 3. Quelle branche de quel dépôt ajoute quoi (les 17 branches actives)

> Chaque ligne = une branche avec du travail non fusionné (`ahead > 0`), au 2026-10-07. Colonnes : **fonctionnalité** (ce qu'elle ajoute), **possibilité** (ce qu'elle rend faisable), **besoin** (à quoi ça répond), domaine, vague.

| # | Dépôt · branche | + | Fonctionnalité apportée | Possibilité nouvelle | Besoin couvert | Dom. | v |
|---|---|---:|---|---|---|---|---|
| 1 | `watchtower` · `arena/dec9cd88` = **PR #3** (CI verte) | 7 | Vue TERRAIN (6 sources officielles), gabarit CHANTIER, import CSV, dossier INTEL territorial (Frontignan/Thau), imprévus TP, traçabilité | Suivre un territoire **et** un chantier dans le globe, données officielles à l'appui | **Décider sur le terrain réel** (Thau) | D2/D3/D4 | v2 |
| 2 | `watchtower` · `arena/01a072e1` | 43 | Barre de fonctions unique, volant, **carte 2D IGN**, minicarte, panneau FIL, archives & crues, charge mentale, 11 docs d'architecture | Piloter le monde en 2D pro + confort d'usage (fin des chevauchements UI) | **Exploiter sans surcharge** (industrialiser l'UI) | D2 | v2 |
| 3 | `ETAT-DE-LART` · `arena/01a04f7b` | 38 | Agent de recherche littéraire, cosmos (planètes/ovals), 221 sorties, corrections des vues | Recherche scientifique **assistée** + visualisation 3D de l'état de l'art | **Connaître l'état de l'art** de façon fiable (PRISMA) | D6 | v2 |
| 4 | `monorepo` · `arena/01a08385` | 6 | **nexus_os** : 22 agents, routeur multi-provider + fallback, skills, tools, **MCP**, mémoire, runs/SSE, sandbox, evals, instincts (59 tests) + `/api/tools` | Des agents **exécutants** qui agissent et vérifient, avec choix du modèle | **Agir/vérifier** (D10) sans dépendre d'un seul LLM | D10/D12 | v3 |
| 5 | `monorepo` · `arena/01a08449` | 2 | Module **BTP** : corpus 154 sources, DCE/CCTP/CCAP/BPU/DQE, étude de prix, DT/DICT/AIPR, suivi, DOE, dashboard théorie/état-de-l'art/in-situ | **Conduire un chantier** de bout en bout dans le monorepo | **Métier réel** : le chantier comme cas d'usage complet | D4 | v3 |
| 6 | `monorepo` · `feat/final-interface-skeleton-2026-10-07` | 7 | **Interface finale** : 12 domaines (Command→System), routes `/interface` + `/api/interface-registry`, audit d'intégration | **LA coquille produit** : chaque brique a sa place prévue | **Unifier** les 9 dépôts en une app | D1 | **v1** |
| 7 | `monorepo` · `feat/tool-data-catalog-2026-10` | 13 | Catalogue outils/données (9 domaines, 5 capacités), contrats `core/`, docs d'architecture modulaire, registres | **Gouvernance d'intégration** : référencer→adapter→normaliser→extraire | **Éviter le re-doublonnage** pendant la restructuration | D1/D11 | **v1** |
| 8 | `COGNITORIUM` · `watchtower/osint-workbench-v0.1` | 13 | Modules OSINT + specs alignées sur le master spec (143 fichiers) | Enquête OSINT **outillée** (rétro-ingénierie de la veille) | **Renseignement ouvert** pour le territoire | D3 | v3 |
| 9 | `proto-cognitorium` · `arena/01a08342` | 5 | Sondes d'audit, registre à jour (SEC-04, UX-04, 3 améliorations), 3 rapports d'audit | Qualité/audit **continu** du proto | **Fiabiliser** avant intégration au Core | D5 | v2 |
| 10 | `monorepo` · `arena/01a08203` | 1 | Atlas interactif Frontignan (graphe Obsidian, carte heuristique) | Naviguer le **dossier territoire** comme un graphe | **Restituer** Frontignan/Thau | D2 | v3 |
| 11 | `Language-decoder` · `arena/01a05471` | 3 | Moteur `language_decoder` : 12 modules (decoder, inference, dynamics, functioning, profile, evidence…), schéma `decoded-human`, tests | **Décoder le langage** → profil humain structuré | **Entrée cognition** (Human) : comprendre l'humain | D5 | v2 |
| 12 | `Language-decoder` · `arena/01a05429` | 7 | Home page (schémas de purpose/outils), pages, docs, données, onboarding visuel | Présenter le produit **clairement** | **Onboarding / clarté** d'usage | D5 | v2 |
| 13 | `ETAT-DE-LART` · `arena/01a07d32` | 5 | Route `/download/monorepo.bundle` (secours push 403) | Transférer un dépôt **sans push Git** | **Contourner les blocages d'accès** (livraison) | D1 | v2 |
| 14 | `ETAT-DE-LART` · `arena/01a03aac` | 2 | « Cognitorium v8 » : graphe 3D, 40 fiches concept | Explorer le savoir **en 3D** | **Comprendre les liens** entre concepts | D6 | v3 |
| 15 | `ETAT-DE-LART` · `arena/01a045a1` | 1 | Agent de recherche littéraire **v1** (précurseur de #3) | Automatiser la veille scientifique | **Automatiser la connaissance** | D6 | v2 |
| 16 | `monorepo` · `arena/0034230e` **_(07/10 après-midi)_** | 5 | **Carré d'As** (cadrage, contrat de module, UI, BTP, 3 interfaces + maquettes, réponses, écosystème local, inventaire) · **dossier recherche** (80 domaines) · **`_incoming`** (786 fichiers tracés) · **resync proto** (12 fichiers) · variante frontignan | **Nommer, cadrer et contractualiser la V1** ; rendre visible tout le travail des branches ; réparer la perte de 25 composants | **Étape 0 + spécification de la V1** | D1/D11 | **v1** |
| 17 | `monorepo` · `arena/93b54a79` **_(07/10 après-midi)_** | 1 | Module **`mail-organizer`** : tri d'emails IMAP par règles, extraction de pièces jointes, watch, stats ; 19 tests | **Ingérer la boîte mail** dans l'app (sources documentaires) | **Flux entrant** (emails → connaissances) | D11 | v3 |

### Les 19 branches mortes (0 commit d'avance) — aucune perte, mais du bruit

Leur contenu est **déjà dans `main`** (ahead = 0 ⇒ la branche est un ancêtre de `main`). Trois exemples marquants : `monorepo` · `arena/01a07e3c` (le monorepo unifié initial = PR #1), `arena/01a08168` (fix Starlette), `arena/01a08277` (index du dossier = PR #2). Les autres : proto ×6 (`01a033e8` graphe 5 niveaux, `01a034f2`, `01a035a5`, `01a0369e` vue réseau temporelle, `01a03436` dossier `raw/`, `01a03899` Savoirs), HCSM ×2 (`01a03a6b` framework v0.1, `01a03a93` validateur V1/V5), ETAT ×5 (`01a03adf`, `01a035f7`, `01a0369b`, `01a0389d` v7 graphe Obsidian 99 nœuds), COGNITORIUM ×2 (`01a05ef8` v14 poste de commandement, `01a06876` docs gouvernance), watchtower ×2 (`01a06ebe` état de reprise it.21, `01a0730a` merge audit).
→ **À supprimer** (v0, cosmétique) : 19 pointeurs périmés, zéro risque.

---

## 4. Matrice — quel dépôt sert quel domaine de l'app finale

| Domaine | Fournisseurs identifiés | État le plus avancé |
|---|---|---|
| D1 Command Center | `monorepo` (+ branches interface & catalogue) | **skeleton (branche)** |
| D2 World / Territory | `watchtower` (+2 branches), `frontignan` (+atlas) | **existe (watchtower main)** |
| D3 Intel / OSINT | `watchtower` (PR #3), `reaserch-engine`, `COGNITORIUM/osint` | fragment |
| D4 Projects / BTP | branche BTP `monorepo`, couche chantier `watchtower` | **branche** |
| D5 Human / Cognition | `proto`, `HCSM`, `Language-decoder` | existe (proto) / branche (decoder) |
| D6 Knowledge / Research | `ETAT` (+3 branches), `reaserch-engine`, `frontignan` | existe / branche (+38) |
| D7 Learning Engine | `COGNITORIUM/learning` (CLE) | fragment (PoC) |
| D8 Simulation / Lab | `proto` (studio/labo), `animation-chronos` | existe (fragments) |
| D9 Design / CAD / Fab | — (décisions seulement : Replicad, OrcaSlicer) | **missing** |
| D10 Nexus / Agents | `nexus_os` (branche, 22 agents), agent `reaserch-engine` | **branche** |
| D11 Data / Memory / Prov. | `HCSM` (contrat), `reaserch-engine` (épisodes), audit/ | **spécifié (ADR-007)** |
| D12 System / Settings | `watchtower` (secrets, gratuit/payant), `nexus_os` | existe (partiel) |

---

## 5. Besoins — couverts, partiellement couverts, non couverts

| Besoin | État | Ce qui le couvre (ou manque) | v |
|---|---|---|---|
| Comprendre un territoire | ✅ existe | watchtower + frontignan + PR #3 | v2 |
| Comprendre un humain (profil, compétences) | 🟡 presque | proto (resync requis) + Language-decoder (branche) | v2 |
| Garantir la **provenance/incertitude** des savoirs | 🟡 contrat | HCSM (contrat v1, non branché) + méthode Talbot | v1 |
| Rechercher des preuves de façon réplicable | 🟡 moteur prêt | reaserch-engine (**2 tests rouges**) | v2 |
| Restituer un savoir scientifique | ✅ contenu | ETAT (base + PRISMA) + branche +38 | v2 |
| **Mémoriser** (base unique, temps, vecteurs, géo) | ❌ **manquant** | ADR-007 spécifié, **rien construit** | **v1** |
| Unifier tout ça en une app | 🟡 squelette | branche interface 12 domaines | **v1** |
| Orchestrer des agents | 🟡 prêt | nexus_os (branche, 59 tests) | v3 |
| Apprendre (Learning Engine) | 🟡 PoC | CLE `learning/` | v3 |
| Corréler du renseignement (analytique) | ❌ manquant | watchtower montre, ne corrèle pas (baseline/gaps absents) | v3 |
| Conduire un chantier | 🟡 prêt | branche BTP (154 sources) | v3 |
| Concevoir (CAD) / fabriquer | ❌ manquant | décisions prises, zéro code | v4/v5 |
| Sécuriser/licencier (publication) | 🟡 partiel | watchtower 😀 ; 6 projets sans licence | v1 |

---

## 6. Le désordre en chiffres (point de situation)

| Indicateur | Valeur au 2026-10-07 | Source |
|---|---|---|
| Dépôts | 9 (+1 projet hors GitHub) | GitHub |
| Lignes de code (9 projets) | 283 478 | `inventory.json` |
| Documents | 237 (projets) + 220 (racine) + 16 (audit) + 20 (Carré d'As / recherche) | inventaire + branches |
| Branches | **46 au total** : 9 en `main`, **17 avec travail non fusionné**, 19 mortes, +2 nouvelles du 07/10 après-midi | GitHub live |
| Commits non fusionnés | **159** (153 + 6) | idem |
| Modules hors dépôt | **8** : Carré d'As, recherche, `_incoming` (786 fichiers), BTP, nexus_os, mail-organizer, OSINT workbench, atlas Frontignan | `S5-controle-completude.md` |
| PR | 16 fusionnées, **1 ouverte (CI verte)**, 16 fermées sans fusion | GitHub |
| CI | **1 dépôt sur 9** | GitHub |
| Tests | 221 fichiers (3 projets sur 9) ; 2 rouges | exécutions |
| Core (schéma/base/vecteurs) | **0 fichier construit** | inventaire |
| Éléments classés v1→v5 | **91** (v1=29, v2=24, v3=18, v4=10, v5=2, v0=8) — révision du soir incluse | `importance.json` |
| Audit | 52 findings | `AUDIT-2026-10.md` |
| Poids Git | ~317 Mo `monorepo` (289 Mo de binaires) | GitHub |

---

## 7. Où lire quoi (index de référence)

| Question | Document |
|---|---|
| L'état des lieux complet (C1–C12, findings) | `audit/AUDIT-2026-10.md` |
| L'importance de chaque élément (v1→v5) | `audit/ANALYSE-V1-V5.md` + `audit/data/importance.json` |
| **Ce document** : point timeline + branches | `audit/SYNTHESE-TIMELINE-2026-10.md` |
| La trajectoire 2050 → maintenant | `audit/ROADMAP-2050-2026.md` |
| Le détail GitHub (PR, CI, branches) | `audit/notes/S3-github.md` |
| Le détail transverse (doublons, sécurité, données) | `audit/notes/S4-transverse.md` |
| Le hors-dépôt (Drive, Linear, Gmail) | `audit/notes/S4-externe.md` |
| La vision d'origine (auteur) | `projects/COGNITORIUM/docs/constitution/00-vision.md` |
| Le plan de convergence (câblages) | `projects/COGNITORIUM/docs/architecture/convergence.md` |
| Les domaines de l'app finale | branche : `data/interface_registry.json` |
| La reprise autonome | `python3 scripts/audit_memory.py status` / `next` |
