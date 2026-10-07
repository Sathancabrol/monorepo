# BRIEF DE RECHERCHE — Cognitorium / « Carré d'As »

**Document à remettre tel quel à un agent de recherche (ArenaAI ou équivalent).**
Version 1.1 · 7 octobre 2026 · dépôt `Sathancabrol/monorepo` (branche `arena/0034230e-monorepo`)
Fichiers compagnons : `01-PROMPT-A-COLLER.md` · `02-MATRICE-DOMAINES.csv` (85 domaines) · `03-ENRICHISSEMENTS-ET-ARBITRAGES.md` · **`../carre-das/`** (cadrage V1 : architecture modulaire, contrat de module, UI, module BTP)

---

## ⚠️ MISE À JOUR DU 2026-10-07 — décisions de l'utilisateur (à lire d'abord)

Ces décisions **corrigent et précisent** le brief ci-dessous. En cas de contradiction, ce sont elles qui font foi.

| Décision | Conséquence sur la mission |
|---|---|
| **Cible = association** (loi 1901), pas entreprise | La licence, la gouvernance, le financement et la pérennité deviennent des sujets de **premier plan** (voir nouveau domaine **D84**). L'accessibilité reste visée (WCAG 2.2 AA / RGAA 4.1) mais **n'est pas une obligation légale automatique** pour une association à but non lucratif — sauf financement/contrôle public majoritaire ou service essentiel au public. Ne pas présenter le RGAA comme une obligation générale pour ce cas précis. |
| **L'application s'appelle « Carré d'As »** | C'est la **première itération de l'application Cognitorium finale**, et le **point d'accès unique** aux fonctionnalités des modules. Le dépôt `monorepo` sera renommé `carre-das`. Cognitorium reste le nom du système global. |
| **Windows d'abord, navigateur ensuite** | Toutes les recommandations doivent être **faisables sur Windows 10/11 sans prérequis** (ni Node, ni Python, ni Docker), puis vérifiées pour un mode navigateur (capacités systématiques réduites : le dire honnêtement). |
| **Architecture : repo → sous-repo = module, plug in / plug out** | Un module doit pouvoir être installé, activé, **désactivé et désinstallé sans redémarrer l'application**, sans casser les autres. Nouveau domaine **D81** (cycle de vie et contrats) — s'appuyer sur le travail déjà fait (`core/contracts/module.schema.json`, `data/module_registry.json`, `docs/carre-das/01-CONTRAT-MODULE.md`). |
| **Le module BTP doit devenir une brique puissante** : modélisation 3D, moteur desktop, carte, stats, mise à jour via compte Google (ou autre) | Nouveaux domaines **D82** (moteur 3D desktop, scan, photogrammétrie) et **D83** (synchronisation et comptes). Le corpus réel de 154 documents BTP est le jeu de test officiel. |
| **Interface simple et affordante** | C'est un critère d'évaluation, pas un détail : voir `docs/carre-das/02-UI-PRINCIPES-ET-INSPIRATIONS.md` (5 règles, 10 règles d'affordance, inspirations issues des branches et de l'extérieur). |
| **Priorité actuelle : analyse, pas implémentation** | Tu produis des **décisions et des plans**, pas du code. Chaque recommandation doit être applicable plus tard sans être à refaire. |

**Acquis à ne pas refaire — branches identifiées (gisement interne) :** `arena/01a08385` (NEXUS·OS : 22 agents, routeur multi-fournisseurs, MCP, 147 tests) · `arena/01a08449` (module BTP : 154 documents, 7 rapports, 28 sous-détails de prix) · `feat/final-interface-skeleton-2026-10-07` (squelette d'interface, 12 catégories) · `feat/tool-data-catalog-2026-10` (contrats de module, registre, catalogue outils) · `arena/171a1f38` (audit : 52 constats) · branches watchtower `arena/01a072e1` (UI : barre unique, volant, bascule 2D/3D) et `arena/dec9cd88` (hub INTEL territorial).

---

## §0 — Ta mission, en une page

Tu es un **agent de recherche technologique et d'architecture** au service d'un projet unique et ambitieux (Cognitorium, ci-après « le projet »). Le projet existe déjà sous forme de **9 dépôts** dont le contenu réel est décrit au §2. Il a déjà une constitution, des audits et un registre de décisions (§3). Ce qui manque n'est pas la vision : c'est **l'inventaire critique de l'existant externe** et **la réorganisation totale de l'application**.

### Ce que tu dois faire

1. **Chercher** des sources, outils, standards, données et systèmes déjà fonctionnels, domaine par domaine, en suivant la matrice (§4) et les chantiers (§5).
2. **Comparer** chaque candidat avec ce que le projet possède déjà (§3) et avec les prototypes internes (§2). Dire explicitement : *conserver / fusionner / remplacer / adapter / intégrer comme plugin / réimplémenter / abandonner*.
3. **Vérifier** : licence réelle, activité (12 mois), mainteneurs, sécurité, qualité, performances, coût, verrouillage, compatibilité avec la machine cible (Windows, GTX 1060, 16 Go de RAM), exigences hors-ligne.
4. **Extraire ce qui est utile** : pas une bibliographie. Pour chaque domaine, une **décision actionable** et **le chemin d'intégration**.
5. **Préparer la réorganisation de l'app** : architecture cible, frontières de modules, plan de migration réversible, et la maquette fonctionnelle de l'interface unifiée.

### Ce que tu ne dois pas faire

- Ne **pas** proposer une technologie que tu n'as pas vérifiée (lien + date de consultation obligatoires).
- Ne **pas** re-faire le travail déjà fait (§3) : tu dois le **vérifier et l'actualiser**, pas le répéter.
- Ne **pas** inventer de chiffres (étoiles, licences, benchmarks). Si tu n'as pas la donnée, écris `inconnu` — c'est une réponse acceptable, une invention ne l'est pas.
- Ne **pas** remplacer la vision par une mode technologique. Chaque recommandation doit être justifiée par un besoin du projet.

### Contrainte de vérité (non négociable)

Le projet est gouverné par une règle d'honnêteté épistémique : **une hypothèse n'est jamais présentée comme un fait**. Chaque affirmation doit porter : `source` (URL), `date de consultation`, `niveau de confiance` (vérifié / probable / à confirmer). Les recommandations issues de ta mémoire et non vérifiées doivent être marquées `À VÉRIFIER`.

---

## §1 — Le projet en dix minutes

### 1.1 Vision

Cognitorium veut être un environnement permettant à un humain, une entreprise, une commune ou une organisation de :

> comprendre un problème → représenter le contexte → mobiliser les connaissances → apprendre → explorer des solutions → concevoir → simuler → décider → fabriquer/réaliser → observer le résultat → apprendre du résultat.

Formulation courte : **« Semantic Operating System for Human + Knowledge + World + Design + Action »**. Quatre couches : **HUMAN** (personne, compétences, cognition) · **KNOWLEDGE** (concepts, sciences, référentiels, formations) · **WORLD** (géographie, bâtiments, objets, réseaux, population, temps) · **WORLD GRAPH** (ce qui relie tout) ; puis un **Design Engine**, un **Simulation Engine**, un **Make** (CAD/fabrication) et une **boucle de retour** vers le système.

### 1.2 Sept principes de conception (déjà actés, à respecter)

| # | Principe | Conséquence pour ta recherche |
|---|---|---|
| P1 | **Honnêteté épistémique** — rien n'est affirmé sans provenance/incertitude | Toute donnée produite par un outil doit pouvoir porter source + confiance + fenêtre temporelle |
| P2 | **Ne pas coder trop vite** — chercher avant de construire | Ton travail est *en amont* du code : il doit éviter 6 mois de développement inutile |
| P3 | **BUY / BUILD / WRAP / REPLACE** | Tu dois trancher explicitement, pas suggérer |
| P4 | **Fournisseurs abstraits** — chaque brique remplaçable | Favorise les solutions à interface claire, évite le verrouillage |
| P5 | **Recherche avant décision** (10 points : existence, OSS, licence, activité, perf, communauté, intégration, coût, verrouillage, verdict) | C'est ta grille d'évaluation standard |
| P6 | **Critères de validation** : fonctionnel, UX, technique, sécurité, coût, maintenance | Un outil qui ne passe pas ces 6 filtres n'est pas recommandable |
| P7 | **Chaque brique a une place claire** | Si une fonction n'a pas de place dans l'architecture, elle est écartée |

### 1.3 Contraintes réelles (elles éliminent 80 % des solutions séduisantes)

| Contrainte | Valeur |
|---|---|
| Machine cible principale | Windows 10/11, **GTX 1060 (6 Go VRAM)**, **16 Go RAM**, CPU grand public |
| Budget | scénario 1 : **0–500 €/mois** ; toute dépense récurrente doit être justifiée ; open source/local privilégiés |
| Fonctionnement | **offline-first** ; le cloud est optionnel, jamais obligatoire |
| Installation | l'utilisateur final ne doit pas installer Node, Python ou Docker |
| Utilisateurs | mono-poste d'abord (l'utilisateur est son propre premier utilisateur) ; multi-utilisateur ensuite |
| Langue | français d'abord (BTP, collectivités, référentiels FR), anglais ensuite |
| Public | un particulier, un étudiant, un artisan/ingénieur BTP, une commune |
| Souveraineté | données sensibles (CV, données personnelles, données communales) : local ou hébergement souverain |

### 1.4 Les sept états à distinguer systématiquement

Ce qui existe déjà · ce qui est partiel · ce qui est prévu · ce qui doit être recherché · ce qui existe à l'extérieur · ce qu'il faut développer · ce qui est expérimental ou prématuré.

---

## §2 — État réel des actifs (ce que le projet possède aujourd'hui)

> Résumé factuel. Détail : `projects/COGNITORIUM/docs/etat-des-lieux/` (9 fichiers) et `docs/DOSSIER-CHANTIER-INDEX.md`.

| # | Actif | Ce que c'est réellement | État | Chemin |
|---|---|---|---|---|
| A1 | **watchtower** | Fork de God's Eye View (CesiumJS) devenu une vraie application : **~100 modules**, globe 3D gratuit sans clé, entités, couches, phasage 4D chantier, poste de commandement, HUD FR, diagnostic F3, **3 136 tests annoncés** dans la roadmap | **le plus avancé** | `projects/watchtower/` |
| A2 | **COGNITORIUM** | Vitrine + documentation de gouvernance (constitution, audits, architecture) + `learning/` (CLE PoC) + `watchtower-mods/` (57 modules d'origine) | docs fortes + 2 PoC | `projects/COGNITORIUM/` |
| A3 | **proto-cognitorium** | App React 19 + Vite + Express : graphe 5 niveaux, échelle épistémique, moteur ROME (1 911 fiches / 17 920 compétences / FORMACODE), courbe d'oubli, extraction de CV par IA, modes graphe/arbre/tableau/timeline | prototype le plus riche fonctionnellement | `projects/proto-cognitorium/` |
| A4 | **HCSM** | Modèle scientifique de l'état cognitif : ontologie YAML, modèle d'évidence, incertitude, temporalité, catalogue de mesures, validateur | spécifications | `projects/HCSM/` |
| A5 | **reaserch-engine** | Orchestrateur de recherche Python : plan → preuves → claims → contradictions → synthèse, graphe d'évidence, machine à états, checkpointing, ~20 tests | v0.1 testée | `projects/reaserch-engine/` |
| A6 | **ETAT-DE-LART-PSYCHOLOGIE** | Base de connaissances critique 2020-2026 : CSV 42 champs, Trust Factor, scripts de validation/ajout par DOI, FastAPI + SQLite | v2 opérationnelle | `projects/ETAT-DE-LART-PSYCHOLOGIE/` |
| A7 | **frontignan** | Analyse territoriale complète d'une commune (rapport, 249 sources, 14 figures, vision 2026→2040, 3 scénarios, deck autonome) | **méthode réplicable** | `projects/frontignan/` |
| A8 | **animation-chronos** | Animation React de découverte (révélation progressive) | secondaire | `projects/animation-chronos/` |
| A9 | **Language-decoder** | README quasi vide (« décodeur de langage multimodal ») | coquille vide | `projects/Language-decoder/` |
| A10 | **app/** (monorepo) | FastAPI + Jinja : explorateur de fichiers, preview par iframe, panorama GitHub (`/repos`), snapshot d'inventaire | **ébauche d'agrégation, pas un shell applicatif** | `app/` |
| A11 | **Corpus BTP** | ≈100 documents réels de chantier à la racine : CCTP, CCAP, BPU, DQE, DETAIL-ESTIMATIF, PAQ, plans (situation, profils en long, phasage), comptes rendus, essais (plaque, double-anneau), DT/DICT, AIPR, planning annuel, métré | **corpus de test réel, sous-exploité** | racine du dépôt |
| A12 | **Registre d'outils** | `audit/REFERENCE.md` (193 Ko), `CATALOGUE-OUTILS.md` (86 outils / 12 catégories), `COUTS-LICENCES-LEGAL.md`, `RND-PROPOSITIONS-2026.md` (12 constats de structure, 14 tâches) | **précieux : voir §3** | `projects/watchtower/audit/` |
| A13 | **Dossier documentaire BTP** | Index de dossier chantier | à lire | `docs/DOSSIER-CHANTIER-INDEX.md`, `docs/GITHUB_INVENTORY.md` |

### 2.1 Les 6 constats qui commandent toute réorganisation

1. **Les briques existent mais ne sont pas câblées entre elles** : aucun bus, aucun modèle de données partagé, aucune mémoire commune.
2. **Trois bases de connaissances concurrentes** sur le même domaine (proto TS, CSV ETAT-DE-LART, ontologie HCSM) — doublon à trancher.
3. **L'interface unifiée n'existe pas** : il y a un explorateur de fichiers à iframes, pas un poste de travail.
4. **Tout est éclaté par dépôt** : chaque projet a son runtime, son style, sa persistance (localStorage / JSON / SQLite).
5. **Les documents réels de l'utilisateur (BTP, commune) ne sont pas encore dans la boucle** : c'est pourtant le meilleur terrain de validation.
6. **Les clés et secrets** ont un historique sensible (audit sécurité) : toute architecture qui expose des clés côté client est disqualifiée.

---

## §3 — Déjà décidé / déjà étudié : à vérifier, pas à refaire

> **Règle : ne re-fais pas ces travaux. Actualise-les.** Pour chacun : est-ce encore vrai en octobre 2026 ? Y a-t-il un changement de licence, une alternative devenue meilleure, un abandon ?

### 3.1 Décisions d'architecture (ADR) déjà prises — chemins : `projects/COGNITORIUM/docs/constitution/09-decision-log.md`

| ADR | Décision | Ta mission |
|---|---|---|
| ADR-007 | PostgreSQL 16 + pgvector + **Apache AGE** + PostGIS comme base unique | **Vérifier AGE** (activité, compat, charge) et comparer à l'alternative embarquée ; AGE est actif au 2026-10-07 (4 874★, dernier push 2026-09-19) |
| ADR-008 | Interface `LLMProvider` unique + orchestrateur maison + outils exposés en MCP | Vérifier l'état des standards (MCP/A2A/ACP) et si un runtime éprouvé (Goose, OpenHands) doit remplacer l'orchestrateur maison |
| ADR-009 | HCSM = vocabulaire canonique, ETAT-DE-LART = contenu, proto = vue | Proposer le plan de fusion technique (schéma unique + adaptateurs) |
| ADR-010 | Book of Shapes comme source d'assets visuels (**licence à confirmer**) | Trancher la question de licence ou proposer une alternative libre |
| ADR-002/003/004/005 | proto = core React, Watchtower = fork Cesium, reaserch-engine = Python maison, persistance localStorage pour les PoC | Évaluer la trajectoire de fusion et la fin du localStorage |

### 3.2 Audits déjà produits (à utiliser comme socle)

| Fichier | Contenu |
|---|---|
| `docs/audits/internal/001-audit-global.md` | Inventaire des 8 dépôts, doublons, manques, matrice Build/Buy/Wrap v1 |
| `docs/audits/external/003-stack-donnees-memoire.md` | Comparatif base mémoire (pgvector vs Qdrant vs Chroma ; AGE vs Neo4j) avec sources |
| `docs/audits/external/004-stack-cad-fabrication.md` | CAD/fabrication (Replicad, OCCT, JSCAD, OrcaSlicer) |
| `docs/audits/external/005-stack-llm-agents.md` | LLM/agents, MCP, LangGraph |
| `docs/audits/security/001-security.md` | Secrets, framing, clés navigateur |
| `docs/audits/costs/001-costs.md` | Baseline de coûts, seule dépense variable réelle : l'API Gemini non plafonnée |
| `docs/architecture/{current,target,data-model,convergence}.md` | Modèle des 8 entités, cible, plan de convergence |
| `docs/agents/` (13 fiches) | Rôles, entrées/sorties, frontières de chaque agent |
| `projects/watchtower/audit/CATALOGUE-OUTILS.md` | **86 outils** qualifiés (licence, coût, faisabilité) en 12 catégories |
| `projects/watchtower/audit/COUTS-LICENCES-LEGAL.md` | Coûts réels, pièges de licence vérifiés repo par repo, cadre légal FR |
| `projects/watchtower/audit/RND-PROPOSITIONS-2026.md` | 12 constats structurels + 6 chantiers + 12 gabarits + 14 tâches avec critères d'acceptation |
| `projects/watchtower/audit/REFERENCE.md` | Registre de référence détaillé (rôle, faisabilité, licence, URLs, étapes) |
| `projects/watchtower/DATA_SOURCES.md` | Sources de données live + licences + attributions obligatoires |

### 3.3 Points de vigilance déjà identifiés (vérifiés ou constatés)

- **Kùzu est archivée** (base graphe embarquée : dernier commit 2025-10-10, dépôt archivé) → le successeur est **LadybugDB** (MIT, actif). *Vérifié par API GitHub le 2026-10-07.* Toute recommandation « Kùzu » doit être mise à jour.
- **`gods-eye-view` (amont de Watchtower)** : GitHub renvoie `NOASSERTION` alors que le README annonce MIT → à clarifier avant tout nouvel import amont.
- **n8n** : fair-code (non OSI) → préférer Activepieces (MIT) si le critère est la liberté.
- **Open WebUI** : BSD-3 avec clause de marque au-delà de ~50 utilisateurs.
- **TeleGeography** (données bundlées) : CC BY-NC-SA → **incompatible avec un usage commercial** ; à exclure des builds commerciaux.
- **Cesium + GTX 1060** : la roadmap interne note que « Cesium sature la carte graphique H24 » → la bascule 2D/3D est un sujet de performance, pas d'esthétique.
- **Clés API dans le navigateur** (`keySetup.js`) : dette de sécurité identifiée (constat C4 du RND) — toute solution future doit passer par le serveur local.
- **Données personnelles** : CV et données réelles ont transité dans un dépôt public (purge effectuée) → rotation recommandée, politique de données à écrire.

---

## §4 — La matrice des domaines (80 domaines)

> Tableau de pilotage. **Version longue et exploitable machine : `02-MATRICE-DOMAINES.csv`** (mêmes identifiants `D01→D85`, avec questions de recherche, pistes à vérifier et critères de succès).
> Légende priorités : **P0** = fondation, conditionne le reste · **P1** = enrichissement à forte valeur · **P2** = laboratoire/spécialisé · **P3** = écosystème.
> **Ajoutés le 2026-10-07 (décisions utilisateur)** — à traiter en priorité, détaillés dans le CSV : **D81** contrat de module et cycle de vie plug in/out · **D82** moteur 3D desktop, modélisation et scan (BTP) · **D83** synchronisation et comptes (Google/OneDrive/WebDAV) · **D84** gouvernance associative, licence et financement · **D85** statistiques et visualisation de données.

### 4.1 Fondations (D01–D28)

| ID | Domaine | Existant | Ce que tu dois rechercher | P | Décision attendue |
|---|---|---|---|---|---|
| D01 | Architecture globale | 8 dépôts + ébauche d'app | Architectures d'applications local-first modulaires (shells, sidecars, frontières de domaines, monorepos polyglottes) | P0 | Définir l'architecture cible |
| D02 | Core / modèle de données | 3 schémas concurrents | Modèles d'entités + provenance + incertitude, JSON Schema versionné, migrations | P0 | Un schéma canonique |
| D03 | Événements / bus / journal | **inexistant** (appels directs entre modules) | Event bus local, outbox, projections, journal d'audit, replay | P0 | Créer le socle événementiel |
| D04 | Persistance locale | ADR-007 PostgreSQL ; SQLite ; localStorage | Bases embarquées/serveur pour desktop : PGlite, SQLite/libSQL, DuckDB, migrations, backups | P0 | Trancher la base principale |
| D05 | Graphe de connaissances | ADR-007 AGE ; fragments | Moteurs graphe : embarqué vs serveur, GQL/Cypher, temporalité, benchmarks LDBC | P0 | Trancher le moteur (AGE / LadybugDB / SQL) |
| D06 | Recherche globale (Ctrl+K) | dispersée | Recherche hybride locale (FTS + vecteurs + fusion), index incrémental, <100 ms | P0 | Couche d'index unique |
| D07 | Mémoire / RAG | corpus docs + BTP non indexé | RAG local sur PC modeste : embeddings, chunking, rerank, évaluation, citations | P0 | Pipeline d'ingestion + index |
| D08 | Contexte partagé | fragments (intelTwin, ficheLieu) | Registres d'entités, résolution/déduplication, coordination inter-modules | P0 | Context Bus + registre |
| D09 | Entity system | voir D02 | Modélisation d'entités hétérogènes typées, ontologies de référence | P0 | Valider le modèle sur 5 cas réels |
| D10 | Project Engine | proto, watchtower chantier, frontignan | Format d'espace de travail projet (fichiers, manifeste, données, agents) | P0 | Format de projet unique |
| D11 | Identité & comptes | **aucun** | Comptes locaux, OAuth optionnel, WebAuthn, multi-utilisateurs, RGPD | P0 | Identité locale par défaut |
| D12 | Sécurité / permissions / sandbox | audit sécurité | Sandbox de code non fiable, permissions granulaires, secrets, isolation | P0 | Modèle de sécurité **avant** les plugins |
| D13 | Plugin SDK + manifeste | 57 modules auto-déclarés (`window.WT.*`) | Systèmes de plugins : manifeste, cycle de vie, permissions, sandbox, hot-reload | P0 | SDK officiel + dogfooding |
| D14 | MCP / A2A / ACP | ADR-008 (MCP visé) | État des standards d'interopérabilité agents/outils et leur gouvernance en 2026 | P0 | Adopter MCP (+ A2A) comme couche |
| D15 | Hardware / budgets | renderGovernor | Détection et profils matériels (ECO/STANDARD/PERFORMANCE), budgets par module | P0 | Profil de capacités exposé au core |
| D16 | Installateur & distribution | aucun | Installeurs Windows sans prérequis, portable, mises à jour, rollback, signature | P0 | 1 installeur, 0 prérequis |
| D17 | Offline-first / sync | idée | CRDT (Yjs/Automerge/Loro), moteurs de sync, conflits, présence | P1 | Sync optionnelle, local primaire |
| D18 | Datasets & licences | DATA_SOURCES.md, ADR-010 | Formats, licences, mise à jour, attribution, compatibilité commerciale | P0 | Dataset Manager + License Matrix |
| D19 | Observabilité / diagnostic | diagnostic F3 | Traces/logs/crash hors-ligne, OpenTelemetry local, profilage | P1 | Diagnostic Center intégré |
| D20 | Tests & Quality Gate | 20 tests + 3 136 annoncés | Tests polyglottes, contrats inter-modules, property-based, mutation, CI locale | P0 | 1 commande = tout vérifier |
| D21 | Documentation as code | excellente mais éclatée | ADR automatisés, Diátaxis, catalogue de modules, site unique | P1 | Doc unifiée du monorepo |
| D22 | i18n / accessibilité / **RGAA** | **absent** | WCAG 2.2 / RGAA 4.1 (**obligation légale** pour les téléservices publics FR), i18n FR/EN | P0 | Contrainte de conception, pas un ajout |
| D23 | RGPD / conformité / souveraineté | audit sécurité | Minimisation, registre, rétention, hébergement souverain, chiffrement local | P0 | Politique de données écrite |
| D24 | Repo Intelligence Agent | inventaire GitHub | Audit de dépôts externes : structure, ADR, CI, activité, bus factor, sécurité, viabilité | P0 | Protocole d'audit + agent |
| D25 | Migration & reprise | 8 dépôts copiés | Monorepo vs multi-repos, verrous, historique Git, strangler-fig, builds reproductibles | P0 | Plan de migration réversible |
| D26 | Coûts IA & métering | Gemini non plafonné | Mesure/plafonds par tâche, cache sémantique, routage coût/qualité | P0 | Proxy LLM avec budgets |
| D27 | Shell UI unifiée | iframes (ébauche) | Shells applicatifs : navigation, command palette, dock, panneaux, workspace multi-vues | P0 | Stack UI + trajectoire de fusion |
| D28 | Performance / budget ressources | renderGovernor ; Cesium lourd | Budgets par module, lazy loading, workers, WASM, streaming, 2D/3D | P0 | Budget mesuré sur la machine cible |

### 4.2 Agents & outils d'exécution (D29–D40)

| ID | Domaine | Existant | Ce que tu dois rechercher | P | Décision attendue |
|---|---|---|---|---|---|
| D29 | Agent Runtime | reaserch-engine | Runtimes réels : boucle outil↔modèle, sandbox d'exécution, PTY, worktrees, permissions, coût par run | P0 | Runtime interne + standards |
| D30 | Multi-agent | 13 fiches, 1 agent | Orchestration : sessions, délégation, mémoire partagée, human-in-the-loop, exécution durable | P0 | Orchestrateur t maison vs framework |
| D31 | Research Agent | reaserch-engine v0.1 | Recherche multi-sources (web, GitHub, docs, papers, discussions) + preuves vérifiables | P0 | Brancher des sources réelles |
| D32 | Integration Agent | aucun | Agents qui modifient du code : plans, patchs, worktrees, tests, rollback | P0 | Agent d'intégration borné |
| D33 | Maintenance Agent | aucun | Dépendances, CVE, dette, releases, code mort | P1 | Tableau de bord de santé |
| D34 | Verification Agent | HCSM validator | Validation de schéma, cohérence épistémique, contradictions, sécurité | P0 | Garde-fou avant persistance |
| D35 | Agent UX & transparence | chatConsole | Plans visibles, approbations, coût, replay, « pourquoi cette réponse » | P1 | UI d'agent digne de confiance |
| D36 | IA locale | Ollama cité | Inférence locale sur GTX 1060 6 Go : modèles, qualité FR, embeddings, STT/TTS | P1 | Point d'entrée LLM local |
| D37 | IA cloud multi-provider | Gemini en dur (dette) | Abstraction fournisseurs, routage, fallback, prompts versionnés, évaluations | P1 | `LLMProvider` + routage |
| D38 | Automatisation / jobs | pipelines ad hoc | Déclencheurs, files, reprise, human-in-the-loop, journal | P1 | Un seul moteur de workflows |
| D39 | OSINT / renseignement | watchtower (sources live) | Sources ouvertes légales, graphes d'entités, anomalies, timeline, note de situation | P0 | Couche d'analyse + légal |
| D40 | Monitoring / veille | sources live | Veille RSS/API/web, détection de changement, scoring, digest, alertes | P0 | Moteur d'alertes local |

### 4.3 Knowledge (D41–D47)

| ID | Domaine | Existant | Ce que tu dois rechercher | P | Décision attendue |
|---|---|---|---|---|---|
| D41 | Cognition / HCSM | HCSM (specs + validator) | Instrumentation psychométrique, validité, biais, incertitude, éthique | P0 | Implémenter le Cognition Hub |
| D42 | Compétences / métiers | moteur ROME complet | ESCO, O*NET, Lightcast, alignements de référentiels, API officielles, licences | P0 | Import référentiels + matching explicable |
| D43 | Learning Engine (CLE) | CLE PoC (2 scénarios) | Knowledge tracing, spaced repetition (FSRS), mastery learning, xAPI/cmi5, LTI, H5P | P1 | Boucle pédagogique industrialisée |
| D44 | Base de connaissances sourcée | ETAT-DE-LART (42 champs) | Revues systématiques (PRISMA, GRADE), gestion bibliographique, qualité de preuve | P0 | Industrialiser l'ingestion DOI→fiche |
| D45 | Recherche scientifique | CrossrefRetriever | OpenAlex, Crossref, Semantic Scholar, HAL, theses.fr, GROBID, synthèses | P1 | Méta-connecteur scientifique |
| D46 | OCR / documents | corpus BTP réel (100 docs) | Extraction fiable FR (CCTP/DQE/plans/XLS/DOC), tableaux chiffrés, formulaires, vérification | P0 | Pipeline documentaire local |
| D47 | Base personnelle (Obsidian) | docs/ (usage Obsidian) | Interopérabilité vault : markdown, wikilinks, propriétés, double sens | P1 | Lire/écrire sans transformer |

### 4.4 World / territoire (D48–D55)

| ID | Domaine | Existant | Ce que tu dois rechercher | P | Décision attendue |
|---|---|---|---|---|---|
| D48 | Cartographie / GIS | Cesium (~100 modules) | Stack géo moderne : 2D/3D, tuiles, PMTiles/COG/GeoParquet, serveurs, traitement local | P0 | Pile GIS principale + rôle de QGIS |
| D49 | Données géo FR/UE | Esri/CARTO/OSM sans clé | IGN (LiDAR HD, BD TOPO), BAN, cadastre, DVF, OCS GE, INSEE, Géorisques, BRGM, Copernicus, STAC | P0 | Connecteur « données publiques FR » |
| D50 | Territory Engine | méthode Frontignan (249 sources) | Modèles territoriaux réplicables (socio-éco, budget, foncier, prospectives), comparaison de communes | P0 | Généraliser Frontignan en moteur |
| D51 | Timeline / 4D | éclaté (watchtower, proto, CLE) | Bi-temporalité, timelines unifiées, animation de données, rejouabilité | P0 | Primitive Timeline partagée |
| D52 | Digital Twin | fiches lieu, chantier | BIM+GIS+capteurs+temps, standards (IFC, CityGML, 3D Tiles, IoT), plateformes | P1 | Portée réaliste du jumeau v1 |
| D53 | Risques & résilience | DT/DICT, essais, EONET | Inondation, RGA, incendie, sismique, industriel, réseaux, sécurité chantier | P0 | Module risque territoire + chantier |
| D54 | Climat / énergie / environnement | guide ICE, qualité de l'eau | ACV, carbone, RE2020, INIES, ADEME, microclimat, biodiversité | P1 | Indicateurs environnementaux |
| D55 | Mobilité | frontignan (mobilités, PEM) | GTFS/GTFS-RT, trafic, accessibilité, simulation de déplacement | P1 | Indicateurs d'accessibilité |

### 4.5 BTP / Make (D56–D63)

| ID | Domaine | Existant | Ce que tu dois rechercher | P | Décision attendue |
|---|---|---|---|---|---|
| D56 | Chantier / suivi de travaux | corpus complet + watchtower chantier | Pilotage : planning, avancement, métrés, NC, essais, OS, situations, DOE, ERP métier | P0 | Module chantier sur le Core |
| D57 | OpenBIM / IFC | roadmap IFC | IfcOpenShell, visionneuses web, IDS/BCF, quantités (QTO), bSDD, Speckle | P0 | WRAP IFC + couche métier |
| D58 | CAD / CAO conceptuel | néant | Noyaux B-rep/CSG, paramétrique, STEP/DXF/DWG, courbe d'apprentissage | P1 | WRAP Replicad/OCCT + FreeCAD |
| D59 | 3D / rendu | Cesium, three.js | Chargés 3D, conversion, performance WebGL2/WebGPU, splats | P1 | Moteur 3D + pipeline d'assets |
| D60 | Drone / photogrammétrie | aucun | Chaîne acquisition → orthophoto/nuage → GIS/BIM, coût GPU | P1 | Pipeline local reproductible |
| D61 | Nuages de points | aucun | LAS/LAZ/E57/COPC, visualisation web, mesures, comparaison de scans | P1 | Visualisation + contrôle qualité |
| D62 | Slicer / fabrication | OrcaSlicer visé | Slicers, profils, G-code, CNC, coût matière | P2 | WRAP |
| D63 | Métré / prix / devis | **corpus DQE/BPU/DETAIL-ESTIMATIF réel** | Extraction de quantités, bases de prix, index BT, décomposition, comparaison de devis | P0 | Moteur DQE/BPU sur données réelles |

### 4.6 Simulation & décision (D64–D68)

| ID | Domaine | Existant | Ce que tu dois rechercher | P | Décision attendue |
|---|---|---|---|---|---|
| D64 | Simulation Engine | néant | DES, ABM, Monte Carlo, files d'attente, sensibilité, reproductibilité | P0 | Moteur léger unifié |
| D65 | Physique & ingénierie | néant | Code_Aster, CalculiX, OpenFOAM, EnergyPlus, limites et responsabilité | P2 | WRAP solveurs validés |
| D66 | Réseaux & fluides | plans AEP/assainissement | EPANET/WNTR, SWMM, pandapower, QGIS | P1 | Données → modèle → vérification |
| D67 | Scénarios / décision | 3 scénarios Frontignan | MCDA (AHP, ELECTRE, PROMETHEE), arbres de décision, jeux sérieux | P1 | Scenario Engine commun |
| D68 | Jeu / stratégie | animation-chronos, vues | Mécaniques de stratégie réutilisables et leurs licences | P1 | Extraire sans copier |

### 4.7 Plateforme, sécurité, produit (D69–D80)

| ID | Domaine | Existant | Ce que tu dois rechercher | P | Décision attendue |
|---|---|---|---|---|---|
| D69 | Reverse engineering | besoin exprimé | Ghidra, Rizin, x64dbg, Frida, JADX, angr — environnement isolé | P2 | Module Lab séparé |
| D70 | Chaîne d'approvisionnement | aucun SBOM | SBOM, signatures (Sigstore), SLSA, scan CVE, reproductibilité | P1 | Politique de dépendances |
| D71 | Modèle de menaces | audit sécurité | STRIDE/LINDDUN, OWASP ASVS, OWASP LLM Top 10, ANSSI, sandbox | P0 | Menaces écrites avant plugins |
| D72 | Marché & positionnement | competitors.md (à enrichir) | Palantir, Esri, Autodesk, Procore, Odoo ; modèles open-core ; achat public FR | P1 | Note de marché + modèle de prix |
| D73 | Gouvernance & licences | LICENSE par dépôt | Compatibilité MIT/AGPL/GPL/LGPL/NOASSERTION dans un monorepo redistribué | P2 | Matrice de licences |
| D74 | Marketplace | idée | Écosystèmes d'extensions : validation, sécurité, versions, monétisation | P2 | Définir manifeste + permissions |
| D75 | Veille technologique | REFERENCE.md (86 outils) | Processus de veille durable, sources de qualité, réévaluation des ADR | P1 | Rituel + registre |
| D76 | Notifications | bandeau live | Centre de notifications : priorités, digest, silencing, canaux | P1 | Notifications unifiées |
| D77 | Qualité de données | validateurs partiels | Contrats de données, tests, doublons, fraîcheur, traçabilité | P1 | Contrats par domaine |
| D78 | Backups / continuité | aucun | Sauvegarde locale, snapshots, restauration sélective, chiffrement | P1 | Stratégie testée |
| D79 | Environnement de dev reproductible | fichiers épars | uv, mise/devbox, monorepo tooling, CI locale, tâches | P1 | Bootstrap en 1 commande |
| D80 | Test terrain / retours | usage réel en cours | Boucles de retour respectueuses, instrumentation, priorisation par usage | P1 | Rituel de retour hebdomadaire |

---

## §5 — Les 10 chantiers de recherche P0 (fiches de mission détaillées)

> Pour chaque chantier : **objectif**, **questions de recherche précises**, **pistes de départ** (`à vérifier` = issues de connaissances générales, non vérifiées), **livrable attendu**.
> Les pistes sont des *points de départ*, pas des recommandations.

### CH-1 — Fondations techniques (D01, D03, D04, D05, D13, D15, D16, D28, D79)

**Objectif :** définir le socle exécutable : processus, bus, persistance, graphe, plugins, budgets, installation.

**Questions**
1. Comment des applications desktop réelles (Obsidian, Blender, QGIS, VS Code, Kdenlive, FreeCAD) découpent-elles **shell / modules / extensions / processus auxiliaires** ? Quels sont les invariants ?
2. Pour une app mono-poste Windows, quelle est la meilleure combinaison : **Tauri 2 + sidecar Python**, Electron, ou web local ? Comparer poids, démarrage, sécurité, auto-update, compatibilité GTX 1060, courbe d'apprentissage.
3. Quelle base locale ? **PGlite** (Postgres en WASM, Apache-2.0, actif), **SQLite/libSQL**, ou **PostgreSQL serveur** dès le départ — sachant que l'ADR-007 vise PostgreSQL+pgvector+AGE+PostGIS et que les PoC utilisent localStorage ?
4. Le graphe : **Apache AGE** (actif), **LadybugDB** (successeur de Kùzu, MIT, actif), **DuckDB DuckPGQ**, **Memgraph**, **FalkorDB**, ou **SQL récursif** ? Mesurer sur 10 requêtes réelles du projet (prérequis de compétences, profil↔métier, lieu↔objet). **Attention** : Kùzu est archivée (vérifié 2026-10-07).
5. Event bus local : quels patterns pour un bus typé, journalisé, rejouable, sans infra lourde ? Comment garantir la compatibilité ascendante des événements entre modules ?
6. Plugin SDK : comparer **Extism** (WASM, BSD-3, actif), WASI/Wasmtime, le modèle VS Code, le modèle Obsidian. Comment obtenir permissions granulaires + isolation + hot-reload en local ?
7. Comment détecter le matériel et dégrader gracieusement (profils ECO/STANDARD/PERFORMANCE) sur un portable/desktop modeste ?
8. Installeur Windows sans prérequis : bundler Tauri, uv/PyInstaller pour le Python, mise à jour signée, mode portable.
9. Monorepo polyglotte : **pnpm + uv workspaces + Turborepo/Nx** suffisent-ils, ou faut-il Bazel/Buck2/Dagger ? Comparer sur le cas réel (8 projets, JS+Python+Rust).

**Pistes à vérifier :** Tauri 2 (Apache-2.0, 111 638★, actif 2026-10-07) · PGlite (Apache-2.0, 16 129★) · LadybugDB (MIT, 1 821★) · Apache AGE (4 874★, actif) · Extism (BSD-3, 5 787★) · DuckDB (MIT, 41 959★) · ElectricSQL, PowerSync, Yjs, Automerge, Loro.

**Livrable :** une **architecture cible** (schéma + ADR) + un **banc d'essai** reproductible (démarrage, RAM, taille, compat) réalisé ou décrit au pas près.

---

### CH-2 — Données, mémoire et recherche (D02, D06, D07, D08, D09, D18, D77, D78)

**Objectif :** une seule source de vérité pour les entités, une mémoire utilisable, une recherche universelle.

**Questions**
1. Comment unifier les 3 schémas (types.ts du proto, ontologie HCSM YAML, CSV 42 champs) en **un schéma canonique** sans casser les dépôts ? Proposer la structure exacte (JSON Schema + projection SQL).
2. Comment scanner **100 documents BTP réels** (PDF, DOC, XLS) et produire des données structurées fiables (CCTP, DQE, BPU, métrés, essais) ? Quels outils pour les **tableaux chiffrés** et les **anciens formats .xls/.doc** ? Comment vérifier qu'aucun chiffre n'est perdu ?
3. RAG local : quels modèles d'embeddings multilingues tiennent sur 6 Go de VRAM ou en CPU ? Quel reranker ? Comment évaluer la qualité des réponses (jeu de test réel) ?
4. Recherche hybride : comment combiner FTS (SQLite FTS5 / Tantivy / ParadeDB) et vecteurs avec fusion RRF, indexation incrémentale, filtres par permissions, et latence <100 ms ?
5. Résolution d'entités : comment éviter les doublons (même lieu écrit de trois façons, même personne dans deux documents) sans intervention manuelle systématique ?
6. Datasets : comment versionner, attribuer et **exclure automatiquement** un dataset non compatible (ex. CC BY-NC-SA) selon l'usage (perso/commercial) ?
7. Sauvegarde/restauration : quelle stratégie simple et testée pour un utilisateur non technique (local + disque externe) ?

**Pistes à vérifier :** LanceDB · pgvector · fastembed · bge-m3 · bge-reranker · Chonkie · SQLite FTS5 · Tantivy · Meilisearch · ParadeDB · Splink/Dedupe (déduplication) · restic/Kopia (backup).

**Livrable :** schéma canonique v0.1 + pipeline documentaire fonctionnel sur **5 documents réels du corpus** (avec taux d'erreur mesuré) + index de recherche unifié.

---

### CH-3 — Sécurité, vie privée, conformité (D12, D22, D23, D70, D71, D73)

**Objectif :** pouvoir dire « c'est sûr » avant d'ouvrir la plateforme aux plugins et aux agents.

**Questions**
1. Modèle de menaces complet : quels actifs, quels adversaires, quelles frontières (navigateur, plugins, LLM, fichiers, réseau, agents) ? Appliquer STRIDE + LINDDUN.
2. Exécution de code non fiable (plugins, scripts d'agents) : quelle isolation est **réellement** disponible sous Windows (AppContainer, Job Objects, WASM, sandbox de navigateur) ? Comparer au coût d'un conteneur.
3. Secrets : où vivent les clés API dans une app desktop ? (OS keyring, fichier chiffré, proxy local) Comment empêcher structurellement l'exposition au client ?
4. OWASP LLM Top 10 : quelles protections minimales pour un agent qui lit des documents et écrit du code (injection de prompt, exfiltration, confusion d'outils) ?
5. Accessibilité et RGAA : pour une commune cliente, quelles obligations exactes (RGAA 4.1, dossier d'accessibilité, déclaration) et quels outils de test ?
6. RGPD : registre de traitement, minimisation, durée de conservation, droits des personnes, chiffrement au repos, sous-traitance — pour un outil qui traite CV, documents communaux et données de chantier.
7. Licences : construire la **matrice de compatibilité** du monorepo (MIT, Apache-2.0, LGPL, GPL, AGPL, NOASSERTION, fair-code) selon trois scénarios : usage privé, diffusion open source, distribution commerciale.

**Pistes à vérifier :** STRIDE · LINDDUN · OWASP ASVS · OWASP LLM Top 10 · guides ANSSI · CyCloneDX/SPDX · Syft/Grype/Trivy · Sigstore · OpenSSF Scorecard · axe-core · REUSE/SPDX pour les licences.

**Livrable :** modèle de menaces daté + politique de données + matrice de licences + tests de sécurité automatisés.

---

### CH-4 — Agents, interopérabilité et exécution (D14, D29, D30, D31, D32, D34, D35, D36, D37, D38)

**Objectif :** un système d'agents fiable, observable, interopérable — sans réécrire ce qui existe.

**Questions**
1. État des standards en octobre 2026 : **MCP** (spec, SDK, registre, authentification, sécurité), **A2A**, **ACP**, `AGENTS.md`, `llms.txt`. Qui gouverne, quelles évolutions, quels risques ?
2. Runtimes éprouvés : **Goose** (Apache-2.0, 55 032★, dépôt déplacé vers `aaif-goose`), **OpenHands** (MIT, 90 161★), Aider, SWE-agent, Cline, Continue, opencode. Que peut-on **réutiliser** plutôt que réécrire ? Où est la frontière (orchestrateur maison vs runtime adopté) ?
3. Exécution durable : quand un simple orchestrateur ne suffit-il plus et faut-il Temporal/Restate/DBOS ? Quel est le coût d'exploitation local ?
4. Sandbox d'exécution de code : quelle solution tient sur un poste Windows (WASM, conteneur, VM, job object) ?
5. Mémoire d'agent : comment relier la mémoire d'un agent au Core (D02) sans créer une seconde base ? Intérêt réel de Graphiti (Apache-2.0, 31 513★) ou cognee (31 522★) vs notre graphe ?
6. LLM local vs cloud : quels modèles (taille/quantification) donnent une qualité française acceptable sur 6 Go VRAM, pour quelles tâches exactement (extraction, classement, rédaction, code) ? Où le cloud reste indispensable ?
7. Coût : comment mesurer, plafonner et afficher le coût par tâche/utilisateur ? Comment mettre en cache sans dégrader la qualité ?
8. Vérification : comment empêcher structurellement un agent d'écrire une affirmation non sourcée en base ?

**Pistes à vérifier :** MCP (spec, 9 400★) · A2A (Apache-2.0, 26 039★) · Goose · OpenHands · LangGraph · Temporal/Restate/DBOS · LiteLLM · DSPy · promptfoo · Outlines/Instructor (JSON garanti) · Langfuse (traces).

**Livrable :** un document « runtime d'agents » + **une démonstration** : 3 agents coopèrent sur une tâche réelle avec permissions, journal, coût et arbitrage humain.

---

### CH-5 — Interface unifiée et expérience (D10, D21, D25, D27, D28, D79)

**Objectif :** passer d'un explorateur de fichiers à iframes à **un poste de travail unique**.

**Questions**
1. Quelle stack UI ? (React — déjà partout —, Solid, Svelte, Vue ; Radix/shadcn, Ark, Base UI ; Tailwind ou CSS modules.) Critères : réutilisation du code existant (proto React, verdict des 3 136 tests Watchtower en vanilla JS), performance, accessibilité, courbe.
2. Comment **fusionner progressivement** : shell + modules natifs + iframes pour ce qui existe (Cesium, decks HTML autonomes), puis remplacement module par module ?
3. Quelle architecture de panneaux (dock, onglets, split, fenêtres détachables, plein écran carte) ? Comparer Dockview, Golden Layout, FlexLayout, ou maison.
4. Command palette (Ctrl+K) : quelles conventions UX (Raycast, Linear, VS Code, Obsidian) et quelle architecture (registre de commandes unifié) ?
5. Comment le **Design System** s'articule-t-il avec les contraintes RGAA et la lisibilité des données techniques (tableaux BTP, plans, cartes) ?
6. Onboarding : comment présenter une plateforme large sans noyer l'utilisateur (patterns : révélation progressive — déjà explorée par `animation-chronos`) ?
7. Monorepo : comment organiser packages partagés (`ui/`, `core/`, `gis/`, `agents/`) sans casser les 8 projets actuels ?
8. Mesure : quels indicateurs de performance en continu sur la machine cible (démarrage, RAM, fps, latence de recherche) ?

**Pistes à vérifier :** shadcn/Radix · TanStack (Query/Table/Virtual) · Dockview · mapbox/maplibre composants · Style Dictionary (tokens) · Playwright (tests visuels + a11y).

**Livrable :** une **maquette fonctionnelle** du shell (navigation, palette, panneaux, contexte projet) + un **plan de fusion par étapes** + la décision de stack argumentée.

---

### CH-6 — Knowledge, cognition, apprentissage (D41, D42, D43, D44, D45, D46, D47)

**Objectif :** transformer les PoC de connaissance en système industrialisé et sourcé.

**Questions**
1. Cognition : quels instruments et catalogues de mesures existe-t-il (au-delà de ce que HCSM référence déjà) ? Comment un système peut-il **refuser d'estimer** correctement ? Quelles obligations éthiques et limites ?
2. Compétences : ESCO vs ROME vs O*NET — alignements officiels disponibles, licences, API, fraîcheur ; comment construire un matching explicable (« pourquoi », « il manque quoi ») sur des référentiels officiels ?
3. Apprentissage : quel algorithme de répétition espacée retenir en 2026 (FSRS vs SM-2) ? Comment modéliser la maîtrise (BKT/DKT) sans collecter massivement des données ?
4. Ingestion documentaire : quelle chaîne pour passer d'un PDF de recherche à une fiche structurée 42 champs (extraction, tableaux, DOI, métadonnées) avec vérification humaine ?
5. Interopérabilité : xAPI/cmi5/LTI/H5P — utile ou surcoût pour un usage personnel et professionnel ?
6. Obsidian : comment interagir avec un vault sans le corrompre (concurrence d'écriture, wikilinks, propriétés) ?

**Livrable :** plan d'industrialisation de la base de connaissances (1 domaine pilote de bout en bout, du PDF à la fiche en base avec Trust Factor).

---

### CH-7 — Monde, territoire, cartographie (D48, D49, D50, D51, D52, D53, D54, D55)

**Objectif :** faire de la méthode Frontignan un moteur réutilisable et rendre la carte vraiment utile sur une machine modeste.

**Questions**
1. Pile GIS : quel ensemble pour 2D fluide + 3D ponctuelle, hors ligne, sur GTX 1060 ? Quand Cesium est-il nécessaire, quand suffit-il de MapLibre ? Comment gérer les tuiles hors ligne (PMTiles, Martin, cache) ?
2. Données publiques FR : pour chaque besoin (bâti, cadastre, topographie, risques, socio-éco, réseaux, urbanisme), quel **endpoint exact**, quelle licence, quelle fréquence de mise à jour, quel volume ? (Construire le catalogue complet, avec exemples d'appels.)
3. Territoire : quels modèles et indicateurs existent déjà (observatoires, UrbanSim, CityScope, outils INSEE) et que peut-on répliquer pour produire un dossier territorial automatisé ?
4. Temporalité : comment modéliser proprement des faits datés et des corrections (bi-temporalité) pour que la timeline soit fiable ?
5. Risques : quelles données officielles (Géorisques, BRGM, PPRI, Vigicrues, Météo-France) sont exploitables par API, avec quelles licences ? Comment croiser aléas et enjeux d'un projet ?
6. Digital twin : quelle portée minimale utile dès maintenant (un chantier, une commune, un bâtiment) ?
7. Mobilité : les flux GTFS/GTFS-RT des réseaux locaux (Sète Agglopôle, Hérault) sont-ils ouverts, et que permettent-ils ?

**Pistes à vérifier :** MapLibre GL JS · CesiumJS · deck.gl · GDAL · DuckDB Spatial · Martin · PMTiles · Titiler · STAC (stac-fastapi) · QGIS · IGN (BD TOPO, LiDAR HD, RGE ALTI) · BAN · DVF · OCS GE · INSEE (Filosofi, BPE) · Géorisques · BRGM · Copernicus.

**Livrable :** catalogue de données FR (endpoints + licences + exemples) + démonstration : **une commune produite automatiquement** (bâti, population, risques, projets) à l'écran, hors ligne.

---

### CH-8 — BTP, chantier, BIM, fabrication (D56, D57, D58, D59, D60, D61, D63)

**Objectif :** rendre le corpus réel de l'utilisateur exploitable et créer le premier module à valeur immédiate.

**Questions**
1. Comment un **DQE/BPU/DPGF** réel peut-il être importé, normalisé, comparé et **recoupé** avec un métré et un estimatif ? Quels formats (XLS, PDF, tableaux) et quels outils ?
2. OpenBIM : quelle chaîne minimale pour lire un IFC, en extraire des quantités, les comparer à un DQE, et visualiser dans le navigateur (IfcOpenShell + visionneuse web) ?
3. ERP métier : existe-t-il un ERP open source (Odoo, ERPNext, Tryton) capable de porter devis/facturation/chantier, et vaut-il mieux l'intégrer ou l'imiter ?
4. Photogrammétrie drone : la chaîne OpenDroneMap → orthophoto/nuage → intégration GIS/BIM est-elle réalisable sur la machine cible (ou un serveur) et à quel coût réel ?
5. Contrôle qualité : quelles données officielles (normes NF/DTU, CCTG, guides ICE/IDRRIM) sont réutilisables légalement dans un logiciel ?
6. Sécurité chantier : comment intégrer AIPR, DT/DICT, autorisations de voirie, arrêtés de circulation dans la timeline d'un projet ?
7. Quels « quick wins » BTP pour l'utilisateur dès les 30 premiers jours (ex. : génération de comptes rendus, extraction de prix, suivi de NC) ?

**Livrable :** **un module chantier pilote fonctionnel** sur 5 documents réels de son corpus, avec taux d'extraction mesuré, plus la décision BIM (quel chemin, quel coût).

---

### CH-9 — Simulation et décision (D64, D65, D66, D67, D68)

**Objectif :** simuler sans mentir : incertitude, hypothèses, reproductibilité.

**Questions**
1. Quel moteur léger unifie DES + ABM + Monte Carlo pour un usage desktop, avec reproductibilité (graines, versions) et visualisation ?
2. Comment connecter la simulation aux données réelles du Core (projets, ressources, budget, territoire) sans couplage fort ?
3. Réseaux : EPANET/WNTR (eau), SWMM (assainissement), pandapower (élec) — quel niveau de compétence requis, quelles limites, quelle responsabilité ?
4. Aide à la décision : quelles méthodes multicritères sont réellement utilisables par un non-expert (AHP, ELECTRE, PROMETHEE, MACBETH) et comment présenter l'incertitude ?
5. Jeux/stratégie : quelles mécaniques (ressources, exploration, contraintes) servent la compréhension d'un territoire sans tomber dans la gamification excessive ?

**Livrable :** un « Scenario Engine » v0 : un cas réel (chantier ou commune) → 3 options → simulation 1000 fois → distribution de résultats + facteurs sensibles.

---

### CH-10 — Plateforme, coûts, gouvernance, marché (D19, D20, D24, D26, D33, D39, D40, D69, D72, D74, D75, D76, D80)

**Objectif :** que le projet reste vivable (coût, maintenance, temps) et vendable si l'utilisateur le décide.

**Questions**
1. Modèle économique : open-core, on-premise collectivités, SaaS vertical, licence duale ? Quelles contraintes d'achat public en France (marchés publics, UGAP, code de la commande publique, RGPD, hébergement) ?
2. Concurrence : Qui, exactement, fait déjà tout ou partie (Palantir Foundry, Esri, Autodesk, Procore, Odoo + plugins métier, kairnial, Batiscript, Finalcad, logiciels d'étude de prix) ? Quelle est la place réelle de « couche qui relie » ?
3. Viabilité d'un projet solo assisté par agents : quels composants **doivent** être achetés/loués plutôt que maintenus (infra, e-mail, cartes, CI) ?
4. Comment maintenir une veille sans dispersion, et quand réévaluer les ADR (déclencheurs) ?
5. OSINT : jusqu'où aller sans franchir la ligne (données personnelles, scraping, CGU) ? Quelle doctrine écrite ?
6. Qualité et tests : quelle stratégie de test pour un projet massif mené par une personne avec des agents (contrats, régression visuelle, smoke tests) ?
7. Observabilité minimale viable : que journaliser, où, comment le lire sans infrastructure ?

**Livrable :** note de marché + modèle de coûts (3 scénarios) + doctrine OSINT + stratégie de test + tableau de bord de santé du monorepo.

---

## §6 — Méthode de recherche (comment, où, et comment ne pas se faire piéger)

### 6.1 Sources à privilégier, par ordre de fiabilité

1. **Le dépôt officiel** (README, LICENSE, releases, CHANGELOG, ADR, issues, discussions, CI) — la vérité.
2. **La documentation officielle** du projet (pas un blog tiers).
3. **La spécification du standard** (W3C, ISO, OGC, IETF, CNCF, Linux Foundation) pour l'interopérabilité.
4. **Les benchmarks reproductibles** avec méthode publiée (et non les tableaux marketing).
5. **Les discussions de mainteneurs** (issues, RFC, roadmap) pour anticiper les abandons.
6. **Les listes curées** (awesome-*, selfh.st, OSI) pour découvrir — jamais pour décider.
7. **Pas** les articles « top 10 outils » sans date, ni les contenus sponsorisés, ni les réponses d'assistants non sourcées.

### 6.2 Requêtes GitHub utiles (API + opérateurs)

```
# Recherche ciblée
https://api.github.com/search/repositories?q=<mots-clés>+language:<lang>&sort=stars
https://api.github.com/search/repositories?q=topic:<topic>+archived:false+pushed:>2025-10-01
https://api.github.com/search/code?q=<symbole>+repo:<org>/<repo>

# Opérateurs web GitHub
org:  repo:  language:  topic:  stars:>500  pushed:>2025-10-01  archived:false  license:mit
is:issue label:"good first issue"  is:pr is:merged  in:readme in:name

# Vérifications ponctuelles (à faire pour CHAQUE candidat)
gh api repos/<owner>/<repo> --jq '{license:.license.spdx_id, stars:.stargazers_count, pushed:.pushed_at, archived:.archived, issues:.open_issues_count}'
gh api repos/<owner>/<repo>/releases?per_page=5
gh api repos/<owner>/<repo>/contributors --jq 'length'
gh api repos/<owner>/<repo>/commits?per_page=1
```

### 6.3 Indicateurs à relever pour chaque candidat (fiche standard)

| Indicateur | Comment | Seuil d'alerte |
|---|---|---|
| Licence réelle | `LICENSE` + API GitHub (`spdx_id`) + `NOASSERTION` à investiguer | non-OSI, clause commerciale, NOASSERTION inexpliqué |
| Activité | dernier commit, dernier commit **d'un mainteneur principal**, 12 derniers mois | <5 commits/an, ou 1 seul contributeur depuis 18 mois |
| Bus factor | nombre de contributeurs ≥ 30 % des commits | 1 personne = risque |
| Adoption | étoiles, dépendants (deps.dev), téléchargements (npm/PyPI), avis d'utilisateurs | étoiles élevées mais 0 dépendant réel |
| Qualité | tests, CI, couverture, releases versionnées, changelog | pas de tests, pas de releases |
| Sécurité | avis GitHub/OSV, Scorecard, dépendances, secrets | CVE non corrigées > 90 jours |
| Performance | benchmarks publiés, ou **mesure maison** sur machine cible | aucune donnée de perf |
| Coût | licence, service managé, GPU, stockage, e-mail, quotas | coût récurrent non plafonnable |
| Verrouillage | format de données, protocole, possibilité d'export | format propriétaire sans export |
| Effort d'intégration | langage, taille, dépendances, doc, alternatives | > 1 semaine sans preuve de faisabilité |
| Communauté FR | documentation française, support, exemples métier | aucun cas d'usage proche |
| Longévité | âge du projet, financement, gouvernance, fondation | projet d'une start-up sans plan de survie |

### 6.4 Sources de découverte (à utiliser, pas à croire)

`awesome-*` (par domaine) · Hugging Face (trending modèles/datasets) · Papers with Code · OSS Insight / GitHub trending · Hacker News (filtré) · selfh.st / awesome-selfhosted · OpenSSF / CNCF landscape · Software Heritage (archivage et pérennité, SWHID) · deps.dev / Libraries.io (dépendants) · OSV.dev (vulnérabilités) · AlternativeTo (pour trouver un équivalent libre) · listes de l'ANSSI et de la DINUM (pour le secteur public FR).

### 6.5 Comment tester un candidat sans l'installer définitivement

1. **Lecture** : README + LICENSE + dernière release + issues ouvertes (les 10 plus anciennes disent souvent la vérité).
2. **Banc d'essai isolé** : dossier temporaire, Docker ou environnement jetable ; jamais dans le dépôt.
3. **Test sur données réelles du projet** : 5 documents du corpus BTP, 3 requêtes du graphe, 1 profil ROME. Un outil qui ne passe pas ce test ne passe pas le filtre.
4. **Mesure** : temps, RAM, taille, précision. Noter la méthode (pour qu'un autre agent puisse reproduire).
5. **Verdict** : décision + conditions de réévaluation (déclencheurs, comme les ADR existants).

---

## §7 — Format de sortie exigé

Tu produis **quatre livrables** (dans cet ordre de priorité) :

### Livrable 1 — `FICHES-OUTILS.md` (le cœur)
Une fiche par outil retenu (pas par outil examiné) :

```markdown
## <Nom de l'outil> — <domaine Dxx>
- **Ce qu'il fait** : <2 lignes>
- **Pourquoi lui** : <le besoin exact du projet qu'il couvre>
- **Licence** : <spdx> (source + date)
- **Activité** : dernier commit <date>, contributeurs <n>, releases <n> (<date>) — vérifié le <date>
- **Adoption** : <étoiles>, <téléchargements/dépendants>
- **Performance** : <mesurée ou publiée, avec méthode>
- **Coût** : <0 € / usage / abonnement>, plafonnable ? <oui/non>
- **Intégration** : <effort réel, langage, dépendances, chemins dans le projet>
- **Risques** : <licence, bus factor, verrouillage, sécurité>
- **Décision** : CONSERVER / FUSIONNER / REMPLACER / ADAPTER / PLUGIN / RÉIMPLÉMENTER / ABANDONNER
- **Alternative écartée** : <nom + raison en une ligne>
- **Source** : <URL> (consulté le <date>)
```

### Livrable 2 — `DECISIONS-ADR.md`
Pour chaque décision structurante : ADR au format du projet (contexte, options, décision, conséquences, déclencheurs de réévaluation). Numérotation à partir de **ADR-011**.

### Livrable 3 — `ARCHITECTURE-CIBLE.md`
- Schéma des couches et modules (Mermaid), frontières et contrats.
- Découpage en modules avec propriétaire de chaque donnée (qui écrit quoi).
- Plan de migration réversible par phases, avec l'état de chaque dépôt actuel à chaque phase.
- Maquette fonctionnelle décrite du shell unifié (navigation, palette, panneaux, contexte).

### Livrable 4 — `SYNTHESE-POUR-DECISION.md` (3 pages maximum)
- Ce qu'il faut faire dans les 30 / 90 / 180 jours.
- Les 10 décisions les plus structurantes, chacune en 3 lignes (choix, raison, risque).
- Ce qui a été **écarté** et pourquoi (aussi important que ce qui est retenu).
- Les incertitudes qui subsistent et ce qui les lèverait.
- Le coût total estimé (logiciel, matériel, temps) et le temps de mise en œuvre.

### Règles de forme
- Écrire en **français**, termes techniques conservés en anglais quand c'est l'usage.
- Chaque affirmation : source + date. Chaque estimation : méthode + intervalle.
- Tableaux plutôt que prose pour les comparaisons. Trois options maximum par décision.
- Marquer `⚠️ LICENCE` et `⚠️ ABANDON` quand le cas se présente : ce sont les deux pièges les plus coûteux.

---

## §8 — Règles de conduite (à respecter strictement)

1. **Une hypothèse n'est pas un fait.** Marquer `[hypothèse]` quand tu déduis sans preuve.
2. **Pas de source, pas d'affirmation.** Un chiffre sans source est supprimé.
3. **Ne pas confondre étoiles et qualité.** Un projet populaire peut être abandonné, mal licencié ou inadapté.
4. **Ne pas proposer de solutions impossibles sur la machine cible.** Vérifier RAM, VRAM, OS, hors-ligne.
5. **Ne pas créer de dépendance à un service payant non plafonnable.**
6. **Ne pas dupliquer une brique existante** sans dire explicitement ce qui est remplacé et ce qu'il advient des données.
7. **Ne jamais copier du code sous licence incompatible.** Vérifier avant de proposer un fork.
8. **Signaler les contradictions** (entre deux sources, entre une source et l'existant) au lieu de choisir en silence.
9. **Prioriser par le besoin réel** : les documents BTP, le territoire, le chantier et la commune sont les cas d'usage qui comptent davantage que la complétude théorique.
10. **Dire ce que tu ne sais pas.** `inconnu` est une réponse valorisée ; une invention ne l'est pas.

---

## §9 — Ce qui est attendu pour réorganiser l'application

L'objectif final n'est pas une liste d'outils : c'est **une application unifiée** qui remplace l'éclatement actuel. Tu dois donc traiter ces cinq questions comme centrales :

1. **Quel shell ?** Une seule application installable (desktop), avec des modules ; l'ébauche actuelle (`app/` : explorateur + iframes) est un point de départ, pas la cible.
2. **Quelles frontières de modules ?** Découper selon les domaines **et** selon les données : qui possède les entités, qui écrit, qui lit. Un module doit pouvoir être désactivé, testé et remplacé seul.
3. **Quel socle commun ?** Bus d'événements, store, identité, permissions, recherche, i18n/a11y, observabilité, datasets, coût. C'est ce qui évite le prochain éclatement.
4. **Quel chemin de fusion ?** Partir des briques existantes (React proto, Watchtower vanilla/Cesium, CLE, FastAPI) et les intégrer **progressivement**, sans réécriture massive : quoi garder tel quel, quoi encapsuler, quoi réécrire, dans quel ordre.
5. **Quel premier palier démontrable ?** Il faut un objectif à 90 jours qui soit *déjà utile* à l'utilisateur (par exemple : ouvrir un dossier de chantier réel, extraire le DQE, le relier au plan et au planning, produire un compte rendu). Propose ce palier.

---

## §10 — Questions ouvertes à l'utilisateur

> **Mise à jour du 2026-10-07 :** les questions 1 (nom), 2 (priorité), 3 (multi-utilisateur), 4 (cloud), 6 (GPU), 9 (ambition V1) et 10 (langue) ont reçu une réponse — voir la mise à jour en tête de document et `../carre-das/00-CADRAGE-CARRE-D-AS.md`. Restent ouvertes : **5** (usage des documents clients comme jeu de test — réponse partielle : le corpus BTP sert de jeu de test, l'anonymisation reste à décider), **7** (licence : à trancher, recommandation Apache-2.0 + AGPL-3.0 dans le cadrage) et **8** (temps disponible pour les validations).

1. **Nom du produit** — ✅ tranché : **Carré d'As** (application), Cognitorium (système).
2. **Priorité commerciale** — ✅ tranché : **association**, sans objectif de profit ; les modules métier (BTP) restent la valeur démontrable.
3. **Multi-utilisateur** — ✅ mono-poste d'abord, multi-poste via synchronisation ensuite.
4. **Acceptation du cloud** — ✅ optionnel et explicite uniquement (comptes Google/OneDrive/WebDAV), jamais requis.
5. **Données clients** : les documents BTP réels servent-ils de jeu de test officiel (avec anonymisation) ?
6. **Matériel** — ✅ concevoir pour 6 Go de VRAM (GTX 1060) ; documenter ce que 12-16 Go apporteraient.
7. **Ouverture / licence** : privé, open source, ou mixte ? (recommandation au §2.3 du cadrage)
8. **Temps disponible** : combien d'heures par semaine pour décider et valider ?
9. **Ambition V1** — ✅ **une tranche verticale parfaite** (chantier + documents + carte + agents).
10. **Langue** — ✅ français d'abord.

---

## Annexe A — Acquis à ne pas refaire (index des ressources internes)

| Ressource | Chemin | Usage |
|---|---|---|
| Constitution (vision, principes, architecture conceptuelle, roadmap, budget, risques, concurrents, ADR) | `projects/COGNITORIUM/docs/constitution/` | Cadre de toute décision |
| État des lieux exhaustif des 8 dépôts | `projects/COGNITORIUM/docs/etat-des-lieux/` | Ne pas ré-auditer : mettre à jour |
| Audits externes et interne | `projects/COGNITORIUM/docs/audits/` | Socle des recherches |
| Architecture (actuel, cible, convergence, modèle de données) | `projects/COGNITORIUM/docs/architecture/` | Point de départ de CH-1 et CH-2 |
| 13 fiches d'agents | `projects/COGNITORIUM/docs/agents/` | Périmètre des agents de CH-4 |
| Glossaire unifié | `projects/COGNITORIUM/docs/glossary.md` | Vocabulaire imposé |
| Registre d'outils (86 outils) | `projects/watchtower/audit/CATALOGUE-OUTILS.md` | À vérifier/actualiser, pas à refaire |
| Registre de référence détaillé | `projects/watchtower/audit/REFERENCE.md` | Fiches complètes existantes |
| Coûts, licences, légal | `projects/watchtower/audit/COUTS-LICENCES-LEGAL.md` | Base de CH-3 et CH-10 |
| R&D structurelle (12 constats, 14 tâches) | `projects/watchtower/audit/RND-PROPOSITIONS-2026.md` | Entrée directe de CH-1 et CH-5 |
| Sources de données et attributions | `projects/watchtower/DATA_SOURCES.md` | Base de CH-7 et D18 |
| Feuille de route de l'app la plus avancée | `projects/watchtower/ROADMAP.md` | 100 modules, 3 136 tests |
| Diagnostics et performance | `projects/watchtower/docs/{DIAGNOSTIC,PERFORMANCE,KNOWN-ISSUES}.md` | Base de D28 |
| Corpus de test réel | racine du dépôt (≈100 PDF/XLS/DOC BTP) | Jeu de données des CH-2 et CH-8 |
| Méthode territoriale | `projects/frontignan/` | Modèle de CH-7 |
| Base de connaissances modèle | `projects/ETAT-DE-LART-PSYCHOLOGIE/` | Modèle de CH-6 |

## Annexe B — Glossaire minimal (pour l'agent)

| Terme | Définition |
|---|---|
| **Core** | Noyau de données du projet : `User · Project · Knowledge · Skill · Object · Place · Task · Event` + relations |
| **HCSM** | Modèle scientifique de l'état cognitif humain (ontologie, évidence, incertitude, refus d'estimer) |
| **CLE** | Cognitorium Learning Engine : apprendre par résolution de problèmes |
| **Watchtower** | Module monde : globe 3D, lieux, entités, chantier, 4D |
| **Trust Factor** | Score de confiance d'une publication (base de connaissances) |
| **Socle épistémique** | Provenance + confiance + incertitude + fenêtre temporelle + alternatives, portés par chaque entité |
| **BUY / BUILD / WRAP / REPLACE** | Modes de décision technologique du projet |
| **ADR** | Architecture Decision Record (décision + justification + conséquences) |
| **MCP / A2A / ACP** | Protocoles d'interopérabilité agent↔outils / agent↔agent / agent↔client |
| **BUY/WRAP** | Utiliser tel quel / construire une couche autour |
| **OpenBIM / IFC** | Standard d'échange du bâtiment (maquette numérique) |
| **DQE / BPU / DPGF** | Documents de prix et de quantités du marché de travaux |
| **DOE** | Dossier des ouvrages exécutés (livrable de fin de chantier) |
| **DT / DICT** | Déclaration de travaux / déclaration d'intention de commencement de travaux |
| **AIPR** | Autorisation d'intervention à proximité des réseaux (sécurité chantier) |
| **RGAA / WCAG** | Accessibilité numérique (obligations françaises / standard international) |
| **local-first** | L'utilisateur possède ses données localement ; le cloud est optionnel |
| **P0 / P1 / P2 / P3** | Priorité : fondation / enrichissement / laboratoire / écosystème |

---

**Fin du brief.** Si une information de ce document te semble contradictoire avec ce que tu observes dans le dépôt, **c'est le dépôt qui a raison** : signale l'écart et mets à jour l'analyse.
