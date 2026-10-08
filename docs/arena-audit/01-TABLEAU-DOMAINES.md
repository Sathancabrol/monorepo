# Tableau maître des domaines — Carré d'As

> **93 domaines** : les **85 déjà cadrés** (`docs/recherche/02-MATRICE-DOMAINES.csv`) augmentés de **8 manquants**
> identifiés le 08/10/2026 (D86 → D93). Chaque domaine a : son état **vérifié**, ses **candidats testés le 08/10/2026**
> (étoiles + licence contrôlées par l'API GitHub), **ce qu'ArenaAI doit auditer**, ce qu'il faut **construire**, la **décision attendue**
> et la **fiche concept art** correspondante (`02-CONCEPT-ART-ET-PROMPTS.md`).

> ⚠️ Colonne « Candidats » : ce sont des **pistes vérifiées**, pas des choix. Le travail d'ArenaAI est de
> **trancher** (conserver / fusionner / remplacer / adapter / plugin / réécrire / abandonner) avec preuves à l'appui.

---

## Fondations — 32 domaines

### D01 · Architecture globale de l'application — *P0*
- **Dans le dépôt** : docs/carre-das/00→03 ; shell/ (portail 14 modules/104 fonctions, non encore branché aux données)
- **Existant (cadrage initial)** : monorepo/projects/*, docs/architecture/target.md, app/ (FastAPI+Jinja)
- **À auditer par ArenaAI** : Architectures d'applications desktop local-first modulaires : shells applicatifs, sidecars, processus separés, frontières de domaines, monorepos polyglottes (JS+Python+Rust), comment des produits réels (Obsidian, Blender, QGIS, VS Code, Raycast) découpent leurs modules
- **Pistes d'origine à vérifier** : Tauri 2 (Apache-2.0, 111k★, actif 2026-10-07) ; Wails ; Electron ; Neutralino ; sidecar process ; backends locaux (FastAPI/uvicorn, axum)
- **Décision attendue** : Definir l'architecture cible : un shell + N modules, contrats d'interface versionnés, aucune dépendance croisée entre modules
- **Critère de succès** : Un document d'architecture cible + ADR + 3 schémas Mermaid, validé contre les 8 dépôts existants
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · tesseract-ocr/tesseract ★76 861 [Apache-2.0]
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : ocrmypdf/OCRmyPDF [MPL-2.0] : fichier par fichier
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, c, a, r, t, e
- **Concept art** : `art-19`

### D02 · Core / modèle de données unifié (socle epistemique) — *P0*
- **Dans le dépôt** : docs/carre-das/00→03 ; shell/ (portail 14 modules/104 fonctions, non encore branché aux données)
- **Existant (cadrage initial)** : docs/architecture/data-model.md (8 entités), proto/src/types.ts, HCSM/ontology, ETAT-DE-LART 42 champs, raw/01_cognitorium_schema_ddl.sql
- **À auditer par ArenaAI** : Modèles d'entités universels (Entity-relationship + provenance + incertitude), patterns 'knowledge graph backed app', JSON Schema versionné et migrations, format d'échange inter-modules
- **Pistes d'origine à vérifier** : HCSM hcsm-v0.1.yaml ; Schema.org ; PROV-O (W3C provenance) ; SKOS ; JSON Schema 2020-12 ; OpenLineage ; ontologies BTP (bSDD)
- **Décision attendue** : Fusionner en UN schéma canonique + projection SQL + JSON Schema versionné ; règles d'extension par domaine
- **Critère de succès** : JSON Schema v0.1 + migration SQL + 1 adaptateur de preuve (proto) qui passe les tests
- **Candidats vérifiés (08/10/2026)** : LadybugDB/ladybug ★1 825 [MIT] · getzep/graphiti ★31 553 [Apache-2.0] · neo4j/neo4j ★17 284 [GPL-3.0] · FalkorDB/FalkorDB ★7 967 [SSPL-1.0] · duckdb/duckdb ★41 982 [MIT] · sqlite/sqlite ★10 620 [Domaine public] · apache/arrow ★17 188 [Apache-2.0] · pola-rs/polars ★40 008 [MIT] · asg017/sqlite-vec ★8 170 [Apache-2.0]
- **⚠️ Licence** : FalkorDB/FalkorDB [SSPL-1.0] : ⛔ à écarter
- **⚠️ Licence** : neo4j/neo4j [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, b, t, p, c, o, g, n, i, r, a, h, e
- **Concept art** : `art-19`

### D03 · Événements / bus / journal (event sourcing) — *P0*
- **Existant (cadrage initial)** : inexistant (modules s'appellent directement ; constat C3 de RND-PROPOSITIONS-2026.md)
- **À auditer par ArenaAI** : Event bus local, outbox pattern, projections, journal d'audit immuable, replay, idempotence, ordre causal, event sourcing en local (pas en cloud)
- **Pistes d'origine à vérifier** : EventTarget/DOM, Redux Toolkit, XState v5, Nano Stores, Effector, RxDB reactivity, DuckDB append-only, SQLite WAL, OpenTelemetry events
- **Décision attendue** : BUILD léger : bus + store + journal append-only + projections ; interdiction des appels directs entre modules
- **Critère de succès** : Un module peut être désactivé/rejoué sans casser les autres ; 200 derniers événements visibles en mode debug
- **Candidats vérifiés (08/10/2026)** : duckdb/duckdb ★41 982 [MIT] · sqlite/sqlite ★10 620 [Domaine public] · apache/arrow ★17 188 [Apache-2.0] · pola-rs/polars ★40 008 [MIT] · asg017/sqlite-vec ★8 170 [Apache-2.0]
- **Modules du shell concernés** : systeme, command
- **Concept art** : `art-19`

### D04 · Persistance locale (base principale) — *P0*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : ADR-007 (PostgreSQL+pgvector+AGE+PostGIS) ; SQLite (ETAT-DE-LART) ; localStorage (proto, CLE) ; JSON (reaserch-engine)
- **À auditer par ArenaAI** : Bases embarquées/serveur pour app desktop mono-poste : PGlite (Postgres WASM), SQLite/libSQL, DuckDB, fichiers + migrations, sauvegarde/restauration, chiffrement au repos
- **Pistes d'origine à vérifier** : PGlite (Apache-2.0, 16k★, actif 2026-10-07) ; libSQL/Turso ; SQLite (FTS5, JSONB, WAL2) ; DuckDB 1.x ; rqlite ; pour serveur : PostgreSQL 18 + extensions
- **Décision attendue** : Trancher : (a) PostgreSQL serveur dès v1, (b) PGlite/SQLite embarqué puis promotion vers PostgreSQL, (c) hybride (embarqué + serveur optionnel) — mêmes migrations
- **Critère de succès** : Une seule vérité par donnée, migrations rejouables, restore testé, 0 perte à la coupure
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · duckdb/duckdb ★41 982 [MIT]
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, c, a, r, t, e
- **Concept art** : `art-19`

### D05 · Graphe de connaissances (moteur) — *P0*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : ADR-007 (Apache AGE) ; fragments intelTwin/ficheLieu/chantier ; HCSM prérequis de compétences
- **À auditer par ArenaAI** : Moteurs graphe : embarqué vs serveur, Cypher/GQL standard (ISO), traversées 1-3 sauts, recherche vectorielle + FTS dans le graphe, temporalité (bi-temporalité), benchmarks LDBC
- **Pistes d'origine à vérifier** : ATTENTION VÉRIFIÉ le 2026-10-07 : kuzudb/kuzu est ARCHIVÉ (dernier push 2025-10-10) → successeur LadybugDB (MIT, actif) ; Apache AGE actif (4.9k★) ; Memgraph ; FalkorDB ; Neo4j ; DuckDB DuckPGQ ; Graphiti/Zep (Apache-2.0, 31.5k★) ; cognee (31.5k★)
- **Décision attendue** : Trancher le moteur principal + la couche mémoire temporelle agent ; verifier AGE vs LadybugDB vs PostgreSQL-only (SQL récursif) selon la charge réelle 1-2 sauts
- **Critère de succès** : Décision argumentée + benchmark reproductible sur 10 requêtes réelles du projet (prérequis compétences, profil↔métier, place↔objet)
- **Candidats vérifiés (08/10/2026)** : LadybugDB/ladybug ★1 825 [MIT] · getzep/graphiti ★31 553 [Apache-2.0] · neo4j/neo4j ★17 284 [GPL-3.0] · FalkorDB/FalkorDB ★7 967 [SSPL-1.0] · asg017/sqlite-vec ★8 170 [Apache-2.0]
- **⚠️ Licence** : FalkorDB/FalkorDB [SSPL-1.0] : ⛔ à écarter
- **⚠️ Licence** : neo4j/neo4j [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, b, t, p, c, o, g, n, i, r, a, h, e
- **Concept art** : `art-06`

### D06 · Recherche globale (Ctrl+K universel) — *P0*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : dispersé (aucune recherche inter-modules)
- **À auditer par ArenaAI** : Recherche hybride locale : FTS lexical + vecteurs + fusion (RRF), index incrémental, tolérance aux fautes, latence <100 ms, recherche dans documents + code + entités + événements
- **Pistes d'origine à vérifier** : SQLite FTS5 ; Tantivy ; Meilisearch (MIT) ; Typesense ; ParadeDB pg_search ; pgvector ; LanceDB ; Orama ; MiniSearch ; Tantivy-py ; Quickwit
- **Décision attendue** : BUILD une couche d'index unifiée (lexical+vectoriel) exposée à tous les modules via une API unique
- **Critère de succès** : 1 barre de recherche qui trouve entités, fichiers, documents, code, événements, avec extraits et provenance
- **Candidats vérifiés (08/10/2026)** : duckdb/duckdb ★41 982 [MIT] · sqlite/sqlite ★10 620 [Domaine public] · apache/arrow ★17 188 [Apache-2.0] · pola-rs/polars ★40 008 [MIT] · asg017/sqlite-vec ★8 170 [Apache-2.0]
- **Modules du shell concernés** : systeme, command, d, o, c, u, m, e, n, t, s
- **Concept art** : `art-05`

### D07 · Mémoire / RAG (documents & conversations) — *P0*
- **Dans le dépôt** : branche arena_01a08449 : 22 rapports, 11 documents_sources, engine/btp_multi_agent.py ; corpus raw : 61 fichiers (43 PDF, 5 xlsm) dont DCE/CCTP/CCAP/BPU, signalisation OPPBTP, AIPR
- **Existant (cadrage initial)** : EtAT-DE-LART (CSV), docs/, corpus BTP local (PDF/XLS), corpus web
- **À auditer par ArenaAI** : RAG local sur PC modeste (GTX 1060 6 Go, 16 Go RAM) : embeddings locaux, chunking, reranking, évaluation de la qualité (RAGAS-like), indexation incrémentale, citations vérifiables
- **Pistes d'origine à vérifier** : LanceDB (Apache-2.0) ; pgvector ; Qdrant ; fastembed ; sentence-transformers ; bge-m3 ; rerankers (bge-reranker v2 m3) ; chunkie (MIT) ; ColBERT/late-interaction ; evaluation : RAGAS, TruLens
- **Décision attendue** : WRAP : index local + pipeline d'ingestion versionné ; chaque réponse porte ses sources et son score de confiance
- **Critère de succès** : Question sur le corpus (docs + 100 PDF BTP) répondue avec 3 sources citées et vérifiables, en <10 s, hors ligne
- **Candidats vérifiés (08/10/2026)** : tesseract-ocr/tesseract ★76 861 [Apache-2.0] · ocrmypdf/OCRmyPDF ★34 960 [MPL-2.0] · PaddlePaddle/PaddleOCR ★90 775 [Apache-2.0] · mindee/doctr ★6 381 [Apache-2.0] · apache/tika ★4 091 [Apache-2.0] · opendatalab/MinerU ★81 295 [Apache-2.0] · docling-project/docling ★68 537 [MIT] · Unstructured-IO/unstructured ★15 548 [Apache-2.0]
- **⚠️ Licence** : ocrmypdf/OCRmyPDF [MPL-2.0] : fichier par fichier
- **Modules du shell concernés** : systeme, command, b, t, p, d, o, c, u, m, e, n, s
- **Concept art** : `art-06`

### D08 · Contexte partagé (Context Bus / Entity Registry) — *P0*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : intelTwin 'carte cognitive T0', fiches lieu, chantier (fragments)
- **À auditer par ArenaAI** : Registres d'entités partagés entre modules, résolution d'entités (déduplication, alias), 'single source of truth' côté client, patterns de state management inter-apps
- **Pistes d'origine à vérifier** : Entity registry patterns ; OpenRefine (algo de dedup) ; Splink ; Dedupe (dedupe.io) ; Zingg ; Record linkage (Python recordlinkage)
- **Décision attendue** : BUILD : le bus (D03) + un registre d'entités typé ; chaque module déclare ses entités et ses capacités
- **Critère de succès** : Un lieu créé dans Watchtower est immédiatement visible dans Cognitorium, le projet BTP et la timeline
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · moj-analytical-services/splink ★2 462 [MIT]
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **Modules du shell concernés** : systeme, command, c, a, r, t, e, b, p, o, g, n, i
- **Concept art** : `art-02`

### D09 · Entity system (modèle universel) — *P0*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : Voir D02 ; proto: nœuds/compétences ; HCSM: construits/observations
- **À auditer par ArenaAI** : Comment modéliser des entités hétérogènes (personne, lieu, projet, objet, document, événement, compétence) avec relations typées + provenance + incertitude, sans tout figer trop tôt
- **Pistes d'origine à vérifier** : Schema.org ; PROV-O ; CIDOC-CRM (patrimoine) ; ISO 15926 (industrie) ; bSDD (BTP) ; OWL/RDFS limites ; ontologie ESCO
- **Décision attendue** : Valider le modèle D02 sur 5 cas d'usage réels tirés du corpus (chantier, profil, territoire, document, simulation)
- **Critère de succès** : 5 cas passés au validateur ; 0 ambiguïté de sens entre deux modules
- **Modules du shell concernés** : systeme, command, b, t, p, c, o, g, n, i, d, u, m, e, s
- **Concept art** : `art-05`

### D10 · Project Engine (workspace projet) — *P0*
- **Dans le dépôt** : nexus_os : 22 agents, 30 skills, runtime/harness/evals/context/memory/providers/creator ; Kc1t/alethe-agents (★832) et openclaw/openclaw (★391 640) à comparer
- **Existant (cadrage initial)** : proto (projets), watchtower (chantier), frontignan (territoire), CLE
- **À auditer par ArenaAI** : Espaces de travail projet : fichiers, agents, événements, cartes, budget, planning ; comment des outils (VS Code workspaces, Obsidian vaults, Kdenlive, Blender) structurent un 'projet'
- **Pistes d'origine à vérifier** : vs code workspace ; Obsidian vault ; .project-meta patterns ; Git worktrees ; Peritext-style rich docs ; Cargo workspaces pour l'analogie
- **Décision attendue** : Definir le format de projet (dossier + manifeste + données) réutilisable par tous les modules
- **Critère de succès** : Un projet BTP réel ouvert dans l'app : documents, plan, agents, budget, planning, timeline
- **Candidats vérifiés (08/10/2026)** : aaif-goose/goose ★55 067 [Apache-2.0] · OpenHands/OpenHands ★90 275 [MIT] · openclaw/openclaw ★391 640 [MIT] · Kc1t/alethe-agents ★832 [AGPL-3.0] · modelcontextprotocol/modelcontextprotocol ★9 406 [Apache-2.0] · a2aproject/A2A ★26 073 [Apache-2.0] · agentclientprotocol/agent-client-protocol ★4 391 [Apache-2.0] · tesseract-ocr/tesseract ★76 861 [Apache-2.0] · ocrmypdf/OCRmyPDF ★34 960 [MPL-2.0] · PaddlePaddle/PaddleOCR ★90 775 [Apache-2.0] · mindee/doctr ★6 381 [Apache-2.0] · apache/tika ★4 091 [Apache-2.0]
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : ocrmypdf/OCRmyPDF [MPL-2.0] : fichier par fichier
- **Modules du shell concernés** : systeme, command, c, a, r, t, e, b, p, g, n, s
- **Concept art** : `art-02`

### D11 · Identité & comptes — *P0*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : grep: aucune authentification dans app/ ; 'Guest/local/Google' évoqué dans la discussion
- **À auditer par ArenaAI** : Comptes locaux sans cloud, OAuth optionnel, WebAuthn/passkeys, multi-utilisateurs sur un même poste, séparation identité/données, RGPD
- **Pistes d'origine à vérifier** : Ory Kratos ; Zitadel ; Keycloak ; Authentik ; SuperTokens ; Auth.js ; Lucia ; hanko (passkeys) ; WebAuthn (FIDO2)
- **Décision attendue** : BUILD local-first : identité locale par défaut, fédération optionnelle ; jamais de donnée liée à un compte cloud par défaut
- **Critère de succès** : L'app fonctionne hors ligne sans compte ; l'ajout d'un compte ne change aucune donnée locale
- **Modules du shell concernés** : systeme, command
- **Concept art** : `art-05`

### D12 · Sécurité / permissions / sandbox — *P0*
- **Dans le dépôt** : nexus_os/plugins.py + mcp.py + mcp_demo.py (branche arena_01a08385) : 8 303 lignes Python, 22 agents, 30 compétences, 8 fichiers de tests
- **Existant (cadrage initial)** : docs/audits/security/001-security.md ; ALLOW_FRAMING ; clés navigateur (constat C4)
- **À auditer par ArenaAI** : Sandbox d'exécution de code non fiable (plugins, agents), permissions granulaires, secrets hors du dépôt, isolation par capacité, audit des accès
- **Pistes d'origine à vérifier** : Extism (BSD-3, actif 2026-10-07) ; Wasmtime/WASI ; Deno permissions ; Landlock/bubblewrap ; gVisor ; microsandbox ; OPA/Cedar ; age/SOPS ; Windows AppContainer
- **Décision attendue** : Écrire le modèle de sécurité (menaces, frontières, capacités) AVANT les plugins ; 'deny by default'
- **Critère de succès** : Un plugin tiers n'accède ni au réseau ni aux fichiers sans permission explicite et journalisée
- **Candidats vérifiés (08/10/2026)** : extism/extism ★5 789 [BSD-3-Clause] · bytecodealliance/wasmtime ★18 698 [Apache-2.0] · modelcontextprotocol/modelcontextprotocol ★9 406 [Apache-2.0] · aaif-goose/goose ★55 067 [Apache-2.0] · OpenHands/OpenHands ★90 275 [MIT] · openclaw/openclaw ★391 640 [MIT] · Kc1t/alethe-agents ★832 [AGPL-3.0] · a2aproject/A2A ★26 073 [Apache-2.0] · agentclientprotocol/agent-client-protocol ★4 391 [Apache-2.0]
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **Modules du shell concernés** : systeme, command, a, g, e, n, t, s
- **Concept art** : `art-07`

### D13 · Plugin SDK + manifest + registre — *P0*
- **Dans le dépôt** : nexus_os/plugins.py + mcp.py + mcp_demo.py (branche arena_01a08385) : 8 303 lignes Python, 22 agents, 30 compétences, 8 fichiers de tests
- **Existant (cadrage initial)** : aucun (57 modules Watchtower s'auto-déclarent via window.WT.*)
- **À auditer par ArenaAI** : Systèmes de plugins modernes : manifeste, cycle de vie, versions d'API, permissions, sandbox, hot-reload, découverte, compatibilité descendante
- **Pistes d'origine à vérifier** : Extism ; VS Code Extensions API (modèle) ; Obsidian plugin API ; Wasm Component Model ; Tauri plugins ; Electron preload+RPC ; MCP comme couche outil
- **Décision attendue** : BUILD un SDK officiel (manifeste JSON + permissions + points d'extension) ; tous les modules internes passent par ce SDK (dogfooding)
- **Critère de succès** : Écrire un module tiers de 50 lignes qui ajoute une couche carte, sans toucher au core
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · extism/extism ★5 789 [BSD-3-Clause]
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : ocrmypdf/OCRmyPDF [MPL-2.0] : fichier par fichier
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, c, a, r, t, e
- **Concept art** : `art-02`

### D14 · MCP / A2A / ACP (interop agents-outils) — *P0*
- **Dans le dépôt** : nexus_os/plugins.py + mcp.py + mcp_demo.py (branche arena_01a08385) : 8 303 lignes Python, 22 agents, 30 compétences, 8 fichiers de tests
- **Existant (cadrage initial)** : ADR-008 (MCP visé), docs/audits/external/005
- **À auditer par ArenaAI** : État du standard : MCP (spec, SDK, registre, sécurité, auth), A2A (Linux Foundation), ACP, AGENTS.md, llms.txt, gouvernance et évolutions 2026
- **Pistes d'origine à vérifier** : VÉRIFIÉ 2026-10-07 : modelcontextprotocol/spec actif ; a2aproject/A2A Apache-2.0 26k★ ; aaif-goose/goose (ex-block/goose) Apache-2.0 55k★ ; OpenHands MIT 90k★
- **Décision attendue** : WRAP MCP + A2A comme couche d'interopérabilité ; nos outils exposés en MCP, nos agents découvrables en A2A
- **Critère de succès** : Un agent externe (Goose/OpenHands) pilote 3 outils du projet via MCP, avec permissions
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · aaif-goose/goose ★55 067 [Apache-2.0]
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, c, a, r, t, e, g, n, s
- **Concept art** : `art-19`

### D15 · Hardware / capacités / budgets de ressources — *P0*
- **Dans le dépôt** : COGNITORIUM (131 fichiers, 24 Mo), proto-cognitorium (87 Mo), HCSM (87 fichiers), ETAT-DE-LART-PSYCHOLOGIE (37 fichiers) + 137 Ko de code récupéré du patch 01a0389d, docs/carre-das/07
- **Existant (cadrage initial)** : watchtower renderGovernor.js ; machine cible GTX 1060 / 16 Go / Windows
- **À auditer par ArenaAI** : Détection et adaptation : profils matériels (ECO/STANDARD/PERFORMANCE), budget CPU/GPU/RAM par module, dégradation gracieuse, mesure réelle, thermal throttling, WebGPU fallback
- **Pistes d'origine à vérifier** : sysinfo (Rust) ; NVML/nvidia-smi ; LibreHardwareMonitor ; Windows WMI/DXGI ; WebGPU adapter info ; WebGL capability ; perf budgets web (web-vitals)
- **Décision attendue** : BUILD : un profil de capacités exposé au core ; chaque module déclare son budget et est désactivé/purgé au-delà
- **Critère de succès** : L'app reste fluide (≥30 fps) sur la machine cible avec 20 modules actifs ; le profil est affiché et modifiable
- **Candidats vérifiés (08/10/2026)** : GuillaumeGomez/sysinfo ★2 748 [MIT] · gfx-rs/wgpu ★18 234 [Apache-2.0] · CesiumGS/cesium ★15 811 [Apache-2.0] · visgl/deck.gl ★14 636 [MIT] · mrdoob/three.js ★116 356 [MIT] · bilawalsidhu/gods-eye-view ★49 027 [MIT] · WorldPixelMap/android-gods-eye-view ★38 [NON-COMMERCIAL]
- **⚠️ Licence** : WorldPixelMap/android-gods-eye-view [NON-COMMERCIAL] : ⛔ à écarter
- **Modules du shell concernés** : systeme, command
- **Concept art** : `art-11`

### D16 · Installateur & distribution — *P0*
- **Existant (cadrage initial)** : README (à faire) ; aucun installeur
- **À auditer par ArenaAI** : Installeurs Windows sans prérequis (Node/Python/Docker), portables, mises à jour et rollback, signature (SmartScreen), MSIX/NSIS/WiX, sidecars Python/Rust
- **Pistes d'origine à vérifier** : Tauri 2 (bundler NSIS/MSI) ; WiX ; Inno Setup ; Electron Builder ; uv (Python embarqué) + PyInstaller/PyOxidizer ; Winget ; Scoop ; MSIX
- **Décision attendue** : BUILD un installeur unique Windows + mode portable + auto-update signé (ou script lisible si pas de certificat)
- **Critère de succès** : Un utilisateur non technique installe et lance l'app sur Windows 10/11 sans rien installer d'autre
- **Modules du shell concernés** : systeme, command
- **Concept art** : `art-19`

### D17 · Offline-first / synchronisation — *P1*
- **Existant (cadrage initial)** : idée local-first (discussion) ; localStorage
- **À auditer par ArenaAI** : Synchronisation locale→distante optionnelle : CRDT (Yjs/Automerge/Loro), sync moteur (ElectricSQL, PowerSync), résolution de conflits, présence, hors-ligne long, chiffrement
- **Pistes d'origine à vérifier** : Yjs (actif) ; Automerge (MIT, actif 2026-10-07) ; Loro (MIT) ; electric-sql/electric (Apache-2.0, 10k★) ; PowerSync ; RxDB ; TinyBase ; Triplit ; InstantDB
- **Décision attendue** : WRAP : ajouter la synchronisation SANS rendre le cloud obligatoire ; le local reste la vérité primaire
- **Critère de succès** : 2 postes hors ligne fusionnent leurs modifications sans perte ni corruption
- **Candidats vérifiés (08/10/2026)** : organicmaps/organicmaps ★15 613 [Apache-2.0] · osmandapp/OsmAnd ★6 062 [GPL-3.0] · kiwix/kiwix-tools ★961 [GPL-3.0] · openzim/zim-tools ★221 [GPL-3.0] · Crosstalk-Solutions/project-nomad ★39 287 [Apache-2.0] · duckdb/duckdb ★41 982 [MIT] · sqlite/sqlite ★10 620 [Domaine public] · apache/arrow ★17 188 [Apache-2.0] · pola-rs/polars ★40 008 [MIT] · asg017/sqlite-vec ★8 170 [Apache-2.0] · yjs/yjs ★22 910 [MIT] · automerge/automerge ★6 650 [MIT]
- **⚠️ Licence** : kiwix/kiwix-tools [GPL-3.0] : copyleft fort
- **⚠️ Licence** : openzim/zim-tools [GPL-3.0] : copyleft fort
- **⚠️ Licence** : osmandapp/OsmAnd [GPL-3.0] : copyleft fort
- **⚠️ Licence** : syncthing/syncthing [MPL-2.0] : fichier par fichier
- **Modules du shell concernés** : systeme, command
- **Concept art** : `art-19`

### D18 · Datasets & licences (Dataset Manager) — *P0*
- **Dans le dépôt** : docs/recherche/02 (D64→D68) ; aucune base de code
- **Existant (cadrage initial)** : DATA_SOURCES.md (Watchtower) ; ADR-010 (Book of Shapes, licence à confirmer) ; docs/audits/costs
- **À auditer par ArenaAI** : Gestion des jeux de données : formats, licences (ODbL, CC-BY-NC, Etalab, IGN), mise à jour, versionnage, compression, stockage, attribution automatique, conformité de redistribution
- **Pistes d'origine à vérifier** : Etalab 2.0 ; ODbL ; CC-BY-NC-SA (TeleGeography à exclure du commercial) ; IGN (Licence Ouverte / Etalab) ; SPEC ; DVC ; git-lfs ; parquet/GeoParquet ; zstd
- **Décision attendue** : BUILD un Dataset Manager + une License Matrix obligatoire (source, licence, usage autorisé, attribution obligatoire)
- **Critère de succès** : Aucun dataset livré sans licence identifiée et attribution affichée ; un build commercial peut exclure les datasets non compatibles en 1 commande
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · LadybugDB/ladybug ★1 825 [MIT]
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : FalkorDB/FalkorDB [SSPL-1.0] : ⛔ à écarter
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **⚠️ Licence** : neo4j/neo4j [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, c, o, m, a, n, d, g, r, p, h, e
- **Concept art** : `art-06`

### D19 · Observabilité / diagnostic / crash — *P1*
- **Dans le dépôt** : COGNITORIUM (131 fichiers, 24 Mo), proto-cognitorium (87 Mo), HCSM (87 fichiers), ETAT-DE-LART-PSYCHOLOGIE (37 fichiers) + 137 Ko de code récupéré du patch 01a0389d, docs/carre-das/07
- **Existant (cadrage initial)** : watcthower/diagnostic.js, docs/DIAGNOSTIC.md ; aucun crash report
- **À auditer par ArenaAI** : Observabilité locale-first (sans cloud) : traces, logs structurés, corrélation, profiling, rapports de crash locaux, export de diagnostic, OpenTelemetry hors ligne
- **Pistes d'origine à vérifier** : OpenTelemetry + collector local ; Grafana/Loki/Tempo ; GlitchTip (Sentry self-host léger) ; DuckDB pour logs Parquet ; pprof/py-spy ; Chrome tracing
- **Décision attendue** : BUILD un 'Diagnostic Center' intégré ; rien n'est envoyé sans consentement explicite
- **Critère de succès** : Un utilisateur exporte un rapport de diagnostic complet (logs, état, versions, dernière action) en 1 clic
- **Candidats vérifiés (08/10/2026)** : organicmaps/organicmaps ★15 613 [Apache-2.0] · osmandapp/OsmAnd ★6 062 [GPL-3.0] · kiwix/kiwix-tools ★961 [GPL-3.0] · openzim/zim-tools ★221 [GPL-3.0] · Crosstalk-Solutions/project-nomad ★39 287 [Apache-2.0]
- **⚠️ Licence** : kiwix/kiwix-tools [GPL-3.0] : copyleft fort
- **⚠️ Licence** : openzim/zim-tools [GPL-3.0] : copyleft fort
- **⚠️ Licence** : osmandapp/OsmAnd [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command
- **Concept art** : `art-07`

### D20 · Tests & Quality Gate — *P0*
- **Dans le dépôt** : COGNITORIUM (131 fichiers, 24 Mo), proto-cognitorium (87 Mo), HCSM (87 fichiers), ETAT-DE-LART-PSYCHOLOGIE (37 fichiers) + 137 Ko de code récupéré du patch 01a0389d, docs/carre-das/07
- **Existant (cadrage initial)** : reaserch-engine ~20 tests ; HCSM validator ; Watchtower: 3136 tests annoncés (ROADMAP) ; pas de CI monorepo
- **À auditer par ArenaAI** : Stratégie de test pour app desktop polyglotte (JS+Python), tests de non-régression UI, property-based testing, mutation testing, tests de contrats inter-modules, CI locale et GitHub Actions
- **Pistes d'origine à vérifier** : Vitest ; Playwright ; pytest ; Hypothesis ; fast-check ; mutmut ; Stryker ; testcontainers ; act (GitHub Actions local) ; Nx/Turborepo task caching
- **Décision attendue** : BUILD une Quality Gate unique (lint+types+tests+contrats+licences+deps) exécutable en local ET en CI
- **Critère de succès** : 1 commande = tout vérifier ; une PR ne peut pas casser un contrat de module sans le signaler
- **Candidats vérifiés (08/10/2026)** : duckdb/duckdb ★41 982 [MIT] · sqlite/sqlite ★10 620 [Domaine public] · apache/arrow ★17 188 [Apache-2.0] · pola-rs/polars ★40 008 [MIT] · asg017/sqlite-vec ★8 170 [Apache-2.0] · OpenTTD/OpenTTD ★8 345 [GPL-2.0] · OpenRCT2/OpenRCT2 ★16 397 [GPL-3.0] · OpenMW/openmw ★6 609 [GPL-3.0] · freeciv/freeciv ★1 602 [GPL-2.0] · godotengine/godot ★118 272 [MIT]
- **⚠️ Licence** : OpenTTD/OpenTTD [GPL-2.0] : copyleft fort
- **⚠️ Licence** : freeciv/freeciv [GPL-2.0] : copyleft fort
- **⚠️ Licence** : OpenRCT2/OpenRCT2 [GPL-3.0] : copyleft fort
- **⚠️ Licence** : OpenMW/openmw [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, c, o, g, n, i, t
- **Concept art** : `art-07`

### D21 · Documentation as code — *P1*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : excellent niveau actuel (docs/, ADR, audits) mais éclaté par dépôt
- **À auditer par ArenaAI** : Documentation générée/agrégée : ADR automatisés, docs de référence API, guides Diátaxis, catalogage de modules, recherche dans la doc, site unique
- **Pistes d'origine à vérifier** : Diátaxis ; MkDocs Material ; Docusaurus ; Starlight ; log4brains/adr-tools ; Mermaid ; Structurizr/C4 ; arc42 ; Backstage (catalogue)
- **Décision attendue** : CONSERVER la méthode actuelle, l'unifier au niveau monorepo : un site de doc généré depuis docs/ + les dépôts
- **Critère de succès** : Toute décision structurante apparaît dans un ADR ; la doc se construit en 1 commande
- **Candidats vérifiés (08/10/2026)** : aaif-goose/goose ★55 067 [Apache-2.0] · OpenHands/OpenHands ★90 275 [MIT] · openclaw/openclaw ★391 640 [MIT] · Kc1t/alethe-agents ★832 [AGPL-3.0] · modelcontextprotocol/modelcontextprotocol ★9 406 [Apache-2.0] · a2aproject/A2A ★26 073 [Apache-2.0] · agentclientprotocol/agent-client-protocol ★4 391 [Apache-2.0]
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **Modules du shell concernés** : systeme, command, a, g, e, n, t, s, d, o, c, u, m
- **Concept art** : `art-19`

### D22 · Internationalisation / Accessibilité / RGAA — *P0*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : absent (aucune mention dans les docs)
- **À auditer par ArenaAI** : Accessibilité (WCAG 2.2 / RGAA 4.1 — OBLIGATION LÉGALE en France pour les téléservices publics), i18n FR/EN, formats de dates/nombres/devises, textes techniques BTP, lecteurs d'écran, contraste, navigation clavier, reduced-motion
- **Pistes d'origine à vérifier** : axe-core ; Playwright a11y ; RGAA 4.1 (DINUM) ; WCAG 2.2 ; i18next ; ICU MessageFormat ; Fluent ; Intl.* ; Lighthouse
- **Décision attendue** : BUILD dès le design system : a11y et i18n sont des contraintes de conception, pas des ajouts
- **Critère de succès** : Le shell passe un audit axe-core sans erreur critique ; 100% des textes UI externalisés
- **Modules du shell concernés** : systeme, command, b, t, p
- **Concept art** : `art-19`

### D23 · RGPD / conformité / souveraineté — *P0*
- **Dans le dépôt** : watchtower/index.html (55 Ko) + branche arena_01a072e1 (comparatif Cesium 21 357 ms vs MapLibre 3 ms) ; frontignan (28 fichiers, 14 Mo, deck 18 slides)
- **Existant (cadrage initial)** : docs/audits/security ; hébergement GitHub public ; CV et données personnelles dans un dépôt public (audit interne §10)
- **À auditer par ArenaAI** : Conformité RGPD pour un outil manipulant des CV, des données de santé/finances communales, des données de chantier ; ancrage de minimisation ; hébergement souverain ; SecNumCloud/HDS ; politique de rétention
- **Pistes d'origine à vérifier** : CNIL (guides, registre, AIPD) ; ANSSI (guides, SecNumCloud) ; HDS ; OWASP ASVS ; privacy-by-design ; chiffrement local (age/SQLCipher)
- **Décision attendue** : Écrire la politique de données (ce qui est collecté, où, combien de temps) + séparer strictement données personnelles et dépôt public
- **Critère de succès** : Aucune donnée personnelle dans le dépôt Git ; registre de traitement rédigé ; purge et export utilisateur fonctionnels
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · duckdb/duckdb ★41 982 [MIT]
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **Modules du shell concernés** : systeme, command, c, a, r, t, e, b, p
- **Concept art** : `art-19`

### D24 · Repo Intelligence Agent (archéologie Git) — *P0*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : README.md (page /repos, scripts/github_inventory.py) ; MANIFEST.json
- **À auditer par ArenaAI** : Analyser des dépôts EXTERNES avant de les adopter : structure, ADR, CI, activité, mainteneurs, bus factor, issues/discussions, licences, sécurité, benchmarks, viabilité ; et archéologie de NOS dépôts (branches mortes, dette)
- **Pistes d'origine à vérifier** : GitHub GraphQL API ; Software Heritage (SWHID, archivage pérenne) ; tree-sitter ; ast-grep ; Semgrep ; repomix ; gitingest ; code2prompt ; Zoekt/livegrep ; git-sizer ; cloc/scc ; OSV.dev ; OpenSSF Scorecard ; deps.dev
- **Décision attendue** : BUILD un protocole reproductible 'Audit de dépôt externe' (fiche + scorecard + verdict) + un agent qui l'exécute
- **Critère de succès** : Tout outil recommandé porte une fiche : licence, activité (12 mois), bus factor, sécurité, coût d'intégration, verdict
- **Candidats vérifiés (08/10/2026)** : LadybugDB/ladybug ★1 825 [MIT] · getzep/graphiti ★31 553 [Apache-2.0] · neo4j/neo4j ★17 284 [GPL-3.0] · FalkorDB/FalkorDB ★7 967 [SSPL-1.0] · aaif-goose/goose ★55 067 [Apache-2.0] · OpenHands/OpenHands ★90 275 [MIT] · openclaw/openclaw ★391 640 [MIT] · Kc1t/alethe-agents ★832 [AGPL-3.0] · modelcontextprotocol/modelcontextprotocol ★9 406 [Apache-2.0] · a2aproject/A2A ★26 073 [Apache-2.0] · agentclientprotocol/agent-client-protocol ★4 391 [Apache-2.0]
- **⚠️ Licence** : FalkorDB/FalkorDB [SSPL-1.0] : ⛔ à écarter
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : neo4j/neo4j [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, a, g, e, n, t, s, r, p, h
- **Concept art** : `art-19`

### D25 · Migration & reprise de l'existant — *P0*
- **Dans le dépôt** : 9 projets + 13 branches ; _incoming 859 fichiers/31 Mo ; scripts/verif-completude-repos.py : 2 157 fichiers, 0 manquant
- **Existant (cadrage initial)** : 8 dépôts copiés dans projects/ (129 Mo, 1090 fichiers) ; monorepo.bundle ; scripts/publish_monorepo.sh
- **À auditer par ArenaAI** : Migration sans casse : monorepo réel vs multi-repos, dépendances entre projets, verrous (lockfiles), imports historiques, strangler-fig pattern, préservation de l'historique Git, builds reproductibles
- **Pistes d'origine à vérifier** : git subtree/submodule ; git-filter-repo ; Bazel/Buck2 (hermétique) ; pnpm workspaces ; uv workspaces ; Turborepo ; Nx ; mise/devbox/flox ; Dagger
- **Décision attendue** : Décider : monorepo unique (pnpm+uv) ou ensemble de dépôts pilotés par manifeste ; plan de migration par phases réversible
- **Critère de succès** : Les 8 projets se buildent en 1 commande depuis la racine ; aucun projet n'est cassé par un autre
- **Modules du shell concernés** : systeme, command
- **Concept art** : `art-19`

### D26 · Coûts IA & métering — *P0*
- **Existant (cadrage initial)** : docs/audits/costs/001-costs.md ; Gemini pay-per-use non plafonné
- **À auditer par ArenaAI** : Mesure et plafonnement des coûts LLM (tokens in/out, par utilisateur, par session, par tâche), cache sémantique, routage coût/qualité, budget local (GPU) vs cloud, télémétrie de coûts
- **Pistes d'origine à vérifier** : LiteLLM (budgets, virtual keys, logging) ; Langfuse (coûts par trace) ; OpenLLMetry ; prompt caching (providers) ; GPTCache ; semantic cache
- **Décision attendue** : WRAP : proxy LLM unique avec budgets et journalisation ; aucune clé payante sans plafond
- **Critère de succès** : Un plafond mensuel est appliqué et vérifié ; le coût par tâche est affiché à l'utilisateur
- **Candidats vérifiés (08/10/2026)** : GuillaumeGomez/sysinfo ★2 748 [MIT] · gfx-rs/wgpu ★18 234 [Apache-2.0] · ggml-org/llama.cpp ★130 687 [MIT] · ollama/ollama ★182 569 [MIT]
- **Modules du shell concernés** : systeme, command
- **Concept art** : `art-19`

### D27 · Shell UI unifiée (Design System) — *P0*
- **Dans le dépôt** : animation-chronos (36 fichiers, 5,3 Mo)
- **Existant (cadrage initial)** : app/ FastAPI+Jinja (explorateur + iframes de preview) = ébauche d'agrégation, PAS le shell cible
- **À auditer par ArenaAI** : Shell applicatif : navigation, command palette, dock, panneaux redimensionnables, workspace multi-vues, notifications, états vides, cartes, timeline, thème, design tokens, cohérence avec les 3 UI existantes (proto React, Watchtower vanilla+Cesium, CLE)
- **Pistes d'origine à vérifier** : Radix UI / shadcn ; Tailwind ; Base UI ; Ark UI ; Solid/React/Vue (arbitrage) ; Dockview ; Golden Layout ; FlexLayout ; cmdk ; TanStack (Query/Table/Virtual) ; design tokens (Style Dictionary)
- **Décision attendue** : Décider la stack UI unique et la trajectoire de fusion (progressif : shell + iframes → composants natifs)
- **Critère de succès** : Une seule app installable où les 5 modules (carte, profil, docs, chantier, recherche) partagent navigation, recherche et contexte
- **Candidats vérifiés (08/10/2026)** : duckdb/duckdb ★41 982 [MIT] · sqlite/sqlite ★10 620 [Domaine public] · apache/arrow ★17 188 [Apache-2.0] · pola-rs/polars ★40 008 [MIT] · asg017/sqlite-vec ★8 170 [Apache-2.0]
- **Modules du shell concernés** : systeme, command, c, a, r, t, e
- **Concept art** : `art-19`

### D28 · Performance & budget de ressources — *P0*
- **Dans le dépôt** : nexus_os/plugins.py + mcp.py + mcp_demo.py (branche arena_01a08385) : 8 303 lignes Python, 22 agents, 30 compétences, 8 fichiers de tests
- **Existant (cadrage initial)** : watchtower renderGovernor, Cesium lourd (constat interne : Cesium sature la carte graphique)
- **À auditer par ArenaAI** : Performance sur PC modeste : budget par module, lazy loading, workers, WASM, virtualisation de listes, streaming, purge mémoire, coût du globe 3D, alternatives 2D/3D
- **Pistes d'origine à vérifier** : MapLibre GL JS (actif 2026-10-07) ; deck.gl ; FlatGeobuf/PMTiles ; Web Workers ; WASM (Rust) ; React Compiler ; virtualization (TanStack Virtual) ; Partytown ; OffscreenCanvas ; WebGPU
- **Décision attendue** : BUILD un budget de ressources par module + bascule 2D/3D et purge automatique
- **Critère de succès** : 20 modules actifs + globe = mémoire <1,5 Go, démarrage <3 s, pas de fuite sur 2 h d'usage
- **Candidats vérifiés (08/10/2026)** : GuillaumeGomez/sysinfo ★2 748 [MIT] · gfx-rs/wgpu ★18 234 [Apache-2.0] · maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT]
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : FalkorDB/FalkorDB [SSPL-1.0] : ⛔ à écarter
- **⚠️ Licence** : WorldPixelMap/android-gods-eye-view [NON-COMMERCIAL] : ⛔ à écarter
- **⚠️ Licence** : tldraw/tldraw [Licence maison tldraw (filigrane)] : ⛔ à écarter
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **⚠️ Licence** : neo4j/neo4j [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, b, t, p, g, r, a, h, e
- **Concept art** : `art-06`

### D81 · Contrat de module : cycle de vie plug in/out — *P0*
- **Dans le dépôt** : docs/carre-das/00→03 ; shell/ (portail 14 modules/104 fonctions, non encore branché aux données)
- **Existant (cadrage initial)** : core/contracts/module.schema.json + data/module_registry.json (branche feat/tool-data-catalog-2026-10) ; 57 modules Watchtower auto-declares ; docs/carre-das/01-CONTRAT-MODULE.md
- **À auditer par ArenaAI** : Systemes d'extensions et de plugins (mise en oeuvre reelle) : manifeste, resolution de dependances, compatibilite de versions, activation/desactivation a chaud sans redemarrage, conflits de propriete de donnees, permissions, migration de donnees a l'installation
- **Pistes d'origine à vérifier** : Modele VS Code Extensions API ; Obsidian plugins ; Tauri 2 plugins ; Extism/WASM Component Model (tiers sandboxes) ; OSGi (reference historique) ; pnpm workspaces ; plugins navigateur (isolation) ; Backstage (catalogue)
- **Décision attendue** : Etendre le schema existant (coreVersion, permissions, points d'extension, owns/reads) et trancher le modele d'isolation des modules tiers
- **Critère de succès** : Un module factice s'installe, s'active, se desactive et se desinstalle SANS redemarrer l'app, donnees intactes
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · extism/extism ★5 789 [BSD-3-Clause]
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : ocrmypdf/OCRmyPDF [MPL-2.0] : fichier par fichier
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, c, a, r, t, e
- **Concept art** : `art-19`

### D83 · Synchronisation & comptes (Google, OneDrive, WebDAV) — *P0*
- **Existant (cadrage initial)** : aucun (constat : cles API cote navigateur, localStorage, pas de sync)
- **À auditer par ArenaAI** : OAuth desktop (loopback/PKCE), dossier applicatif masque vs fichiers visibles, coffre de secrets OS, detection et presentation des conflits, deduplication par empreinte, chiffrement, dossier partage multi-poste, mode hors ligne long
- **Pistes d'origine à vérifier** : Google Drive API (drive.appdata, drive.file : scopes non sensibles) ; appDataFolder ; Microsoft Graph/OneDrive ; WebDAV/Nextcloud ; rclone ; Syncthing ; Automerge/Yjs (etat applicatif) ; Windows Credential Manager ; age (chiffrement)
- **Décision attendue** : Construire une interface de synchronisation unique avec 4 fournisseurs + regles de conflit ; le local reste la verite primaire
- **Critère de succès** : Deux postes se synchronisent sans perte ; un conflit est presente et resolu par l'utilisateur ; restauration possible sans l'app
- **Candidats vérifiés (08/10/2026)** : organicmaps/organicmaps ★15 613 [Apache-2.0] · osmandapp/OsmAnd ★6 062 [GPL-3.0] · kiwix/kiwix-tools ★961 [GPL-3.0] · openzim/zim-tools ★221 [GPL-3.0] · Crosstalk-Solutions/project-nomad ★39 287 [Apache-2.0] · LadybugDB/ladybug ★1 825 [MIT] · getzep/graphiti ★31 553 [Apache-2.0] · neo4j/neo4j ★17 284 [GPL-3.0] · FalkorDB/FalkorDB ★7 967 [SSPL-1.0] · yjs/yjs ★22 910 [MIT] · automerge/automerge ★6 650 [MIT] · syncthing/syncthing ★89 219 [MPL-2.0]
- **⚠️ Licence** : kiwix/kiwix-tools [GPL-3.0] : copyleft fort
- **⚠️ Licence** : FalkorDB/FalkorDB [SSPL-1.0] : ⛔ à écarter
- **⚠️ Licence** : openzim/zim-tools [GPL-3.0] : copyleft fort
- **⚠️ Licence** : osmandapp/OsmAnd [GPL-3.0] : copyleft fort
- **⚠️ Licence** : syncthing/syncthing [MPL-2.0] : fichier par fichier
- **⚠️ Licence** : neo4j/neo4j [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, g, r, a, p, h, e
- **Concept art** : `art-06`

### D89 · Registre d'outils (Tool Registry) — *P0*
- **Dans le dépôt** : nexus_os/plugins.py + mcp.py + mcp_demo.py (branche arena_01a08385) : 8 303 lignes Python, 22 agents, 30 compétences, 8 fichiers de tests
- **Existant (cadrage initial)** : nexus_os/tools + 30 skills
- **À auditer par ArenaAI** : Comment Goose, OpenHands, OpenClaw, Alethe déclarent-ils leurs outils ? Y a-t-il un format commun (MCP tools, JSON Schema) ?
- **Pistes d'origine à vérifier** : MCP (spécification), aaif-goose/goose, OpenHands/OpenHands, openclaw/openclaw
- **Décision attendue** : Définir le format unique de déclaration d'un outil (schéma d'entrée/sortie, permissions)
- **Critère de succès** : Ajouter un outil = un fichier de description, sans toucher au reste
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · aaif-goose/goose ★55 067 [Apache-2.0]
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **Modules du shell concernés** : systeme, command, c, a, r, t, e
- **Concept art** : `art-02`

### D91 · Mise à jour & retour arrière (Update Manager) — *P1*
- **Dans le dépôt** : nexus_os/plugins.py + mcp.py + mcp_demo.py (branche arena_01a08385) : 8 303 lignes Python, 22 agents, 30 compétences, 8 fichiers de tests
- **Existant (cadrage initial)** : décidé dans docs/carre-das/00 (MAJ signée + rollback)
- **À auditer par ArenaAI** : Mécanique de mise à jour Tauri (tauri-plugin-updater, signatures), stratégies de migration locale des données
- **Pistes d'origine à vérifier** : tauri-apps/plugins-workspace, mécanismes NSIS/MSIX, delta updates
- **Décision attendue** : Implémenter : canal stable, signature, migration de schéma, retour arrière en un clic
- **Critère de succès** : Une mise à jour échouée revient à l'état précédent sans perte
- **Candidats vérifiés (08/10/2026)** : extism/extism ★5 789 [BSD-3-Clause] · bytecodealliance/wasmtime ★18 698 [Apache-2.0] · modelcontextprotocol/modelcontextprotocol ★9 406 [Apache-2.0] · OpenTTD/OpenTTD ★8 345 [GPL-2.0] · OpenRCT2/OpenRCT2 ★16 397 [GPL-3.0] · OpenMW/openmw ★6 609 [GPL-3.0] · freeciv/freeciv ★1 602 [GPL-2.0] · godotengine/godot ★118 272 [MIT]
- **⚠️ Licence** : OpenTTD/OpenTTD [GPL-2.0] : copyleft fort
- **⚠️ Licence** : freeciv/freeciv [GPL-2.0] : copyleft fort
- **⚠️ Licence** : OpenRCT2/OpenRCT2 [GPL-3.0] : copyleft fort
- **⚠️ Licence** : OpenMW/openmw [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command
- **Concept art** : `art-19`

## Agents — 8 domaines

### D29 · Agent Runtime — *P0*
- **Dans le dépôt** : nexus_os : 22 agents, 30 skills, runtime/harness/evals/context/memory/providers/creator ; Kc1t/alethe-agents (★832) et openclaw/openclaw (★391 640) à comparer
- **Existant (cadrage initial)** : reaserch-engine (orchestrateur + fetch/retrieval) ; CONTEXT/ROADMAP Watchtower (chatConsole, voix)
- **À auditer par ArenaAI** : Runtimes d'agents réels : boucle outil↔modèle, exécution de code isolée, PTY, worktrees Git, permissions, mémoire, reprise sur erreur, coût par run, observabilité
- **Pistes d'origine à vérifier** : aaif-goose/goose (Apache-2.0, 55k★, vérifié 2026-10-07) ; OpenHands (MIT, 90k★) ; Aider ; Cline/Roo ; continue ; SWE-agent ; opencode ; LangGraph ; Temporal/Restate/DBOS (durabilité)
- **Décision attendue** : BUILD un runtime interne léger (garde ADR-008) MAIS adopter les standards (MCP) et s'inspirer des runtimes éprouvés ; ne pas réimplémenter un sandbox de code
- **Critère de succès** : Un agent exécute une tâche de 20 étapes, reprend après crash, et tout est journalisé avec coût
- **Candidats vérifiés (08/10/2026)** : adewaskar/jarvis ★412 [MIT] · LadybugDB/ladybug ★1 825 [MIT] · getzep/graphiti ★31 553 [Apache-2.0] · neo4j/neo4j ★17 284 [GPL-3.0] · FalkorDB/FalkorDB ★7 967 [SSPL-1.0] · aaif-goose/goose ★55 067 [Apache-2.0] · OpenHands/OpenHands ★90 275 [MIT] · openclaw/openclaw ★391 640 [MIT] · Kc1t/alethe-agents ★832 [AGPL-3.0] · modelcontextprotocol/modelcontextprotocol ★9 406 [Apache-2.0] · a2aproject/A2A ★26 073 [Apache-2.0] · agentclientprotocol/agent-client-protocol ★4 391 [Apache-2.0]
- **⚠️ Licence** : FalkorDB/FalkorDB [SSPL-1.0] : ⛔ à écarter
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : neo4j/neo4j [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, a, g, e, n, t, s, r, p, h
- **Concept art** : `art-06`

### D30 · Multi-agent orchestration — *P0*
- **Dans le dépôt** : nexus_os/plugins.py + mcp.py + mcp_demo.py (branche arena_01a08385) : 8 303 lignes Python, 22 agents, 30 compétences, 8 fichiers de tests
- **Existant (cadrage initial)** : docs/agents/ (13 fiches) ; reaserch-engine (1 agent)
- **À auditer par ArenaAI** : Orchestration multi-agents : sessions, délégation, rôles, mémoire partagée, human-in-the-loop, parallélisme, arbitrage de conflits, garde-fous, budget partagé
- **Pistes d'origine à vérifier** : LangGraph (états durables) ; CrewAI ; AutoGen/AG2 ; OpenAI Agents SDK ; Temporal (durable execution) ; Restate ; dbos ; A2A (interop) ; MCP
- **Décision attendue** : Décider : orchestrateur maison + MCP/A2A, ou framework externe pour les workflows durables ; documenter le critère de bascule
- **Critère de succès** : 3 agents (recherche, intégration, vérification) coopèrent sur une tâche réelle avec arbitrage humain
- **Candidats vérifiés (08/10/2026)** : LadybugDB/ladybug ★1 825 [MIT] · getzep/graphiti ★31 553 [Apache-2.0] · neo4j/neo4j ★17 284 [GPL-3.0] · FalkorDB/FalkorDB ★7 967 [SSPL-1.0] · aaif-goose/goose ★55 067 [Apache-2.0] · OpenHands/OpenHands ★90 275 [MIT] · openclaw/openclaw ★391 640 [MIT] · Kc1t/alethe-agents ★832 [AGPL-3.0] · modelcontextprotocol/modelcontextprotocol ★9 406 [Apache-2.0] · a2aproject/A2A ★26 073 [Apache-2.0] · agentclientprotocol/agent-client-protocol ★4 391 [Apache-2.0]
- **⚠️ Licence** : FalkorDB/FalkorDB [SSPL-1.0] : ⛔ à écarter
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : neo4j/neo4j [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, a, g, e, n, t, s, r, p, h
- **Concept art** : `art-06`

### D31 · Research Agent (web / git / docs / papers) — *P0*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : reaserch-engine (CrossrefRetriever, planner, evidence graph) ; agents/research-agent.md
- **À auditer par ArenaAI** : Recherche multi-sources : web (SearXNG/Crawl4AI), GitHub, docs, papers (OpenAlex/Crossref/S2), discussions, veille, extraction de preuves, déduplication, contradiction, citations vérifiables
- **Pistes d'origine à vérifier** : SearXNG (AGPL) ; Vane/Perplexica (MIT) ; Crawl4AI (Apache-2.0) ; OpenAlex ; Crossref ; Semantic Scholar ; GROBID ; Elicit/Consensus (produits) ; Zotero ; PaperQA2 ; STORM
- **Décision attendue** : BUILD sur l'existant (evidence graph) en le branchant à de vraies sources + un LLM abstrait
- **Critère de succès** : Une question de recherche produit un dossier sourcé avec 10+ sources datées, contradictions signalées, incertitude explicite
- **Candidats vérifiés (08/10/2026)** : LadybugDB/ladybug ★1 825 [MIT] · getzep/graphiti ★31 553 [Apache-2.0] · neo4j/neo4j ★17 284 [GPL-3.0] · FalkorDB/FalkorDB ★7 967 [SSPL-1.0] · asg017/sqlite-vec ★8 170 [Apache-2.0] · aaif-goose/goose ★55 067 [Apache-2.0] · OpenHands/OpenHands ★90 275 [MIT] · openclaw/openclaw ★391 640 [MIT] · Kc1t/alethe-agents ★832 [AGPL-3.0] · modelcontextprotocol/modelcontextprotocol ★9 406 [Apache-2.0] · a2aproject/A2A ★26 073 [Apache-2.0] · agentclientprotocol/agent-client-protocol ★4 391 [Apache-2.0]
- **⚠️ Licence** : FalkorDB/FalkorDB [SSPL-1.0] : ⛔ à écarter
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : neo4j/neo4j [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, a, g, e, n, t, s, d, o, c, u, m, r, p, h
- **Concept art** : `art-03`

### D32 · Integration Agent (code) — *P0*
- **Dans le dépôt** : nexus_os : 22 agents, 30 skills, runtime/harness/evals/context/memory/providers/creator ; Kc1t/alethe-agents (★832) et openclaw/openclaw (★391 640) à comparer
- **Existant (cadrage initial)** : aucun (l'utilisateur travaille avec des agents externes)
- **À auditer par ArenaAI** : Agents qui modifient du code en sécurité : compréhension de dépôt, plans, patchs, tests, régression, revue, worktrees, rollback
- **Pistes d'origine à vérifier** : Aider ; OpenHands ; SWE-agent ; Cline ; Continue ; repomix ; repomap (aider) ; ast-grep ; Playwright (vérification visuelle)
- **Décision attendue** : BUILD/ADOPTER : un 'agent d'intégration' qui propose un plan, modifie dans un worktree, lance la Quality Gate, et ne merge jamais seul
- **Critère de succès** : Une modification de code proposée, testée, expliquée et reversible, avec diff lisible
- **Candidats vérifiés (08/10/2026)** : aaif-goose/goose ★55 067 [Apache-2.0] · OpenHands/OpenHands ★90 275 [MIT] · openclaw/openclaw ★391 640 [MIT] · Kc1t/alethe-agents ★832 [AGPL-3.0] · modelcontextprotocol/modelcontextprotocol ★9 406 [Apache-2.0] · a2aproject/A2A ★26 073 [Apache-2.0] · agentclientprotocol/agent-client-protocol ★4 391 [Apache-2.0]
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **Modules du shell concernés** : systeme, command, a, g, e, n, t, s
- **Concept art** : `art-07`

### D33 · Maintenance Agent — *P1*
- **Dans le dépôt** : nexus_os : 22 agents, 30 skills, runtime/harness/evals/context/memory/providers/creator ; Kc1t/alethe-agents (★832) et openclaw/openclaw (★391 640) à comparer
- **Existant (cadrage initial)** : inexistant
- **À auditer par ArenaAI** : Maintenance continue : dépendances obsolètes/vulnérables, migrations, code mort, dette, releases, changelog, breaking changes
- **Pistes d'origine à vérifier** : Renovate ; Dependabot ; OSV.dev ; osv-scanner ; pip-audit ; npm audit ; cargo-deny ; knip ; vulture (Python) ; Skott ; deptry ; cyclonedx
- **Décision attendue** : BUILD : tableau de bord de santé du monorepo + PR automatiques bornées
- **Critère de succès** : Aucune dépendance critique >6 mois de retard sans justification écrite
- **Candidats vérifiés (08/10/2026)** : aaif-goose/goose ★55 067 [Apache-2.0] · OpenHands/OpenHands ★90 275 [MIT] · openclaw/openclaw ★391 640 [MIT] · Kc1t/alethe-agents ★832 [AGPL-3.0] · modelcontextprotocol/modelcontextprotocol ★9 406 [Apache-2.0] · a2aproject/A2A ★26 073 [Apache-2.0] · agentclientprotocol/agent-client-protocol ★4 391 [Apache-2.0] · PDAL/PDAL ★1 422 [BSD-3-Clause] · CloudCompare/CloudCompare ★4 788 [GPL-2.0] · potree/potree ★5 632 [BSD (2 ou 3 clauses)] · colmap/colmap ★12 874 [BSD-3-Clause]
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : CloudCompare/CloudCompare [GPL-2.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, b, t, p, a, g, e, n, s
- **Concept art** : `art-19`

### D34 · Verification Agent (qualité, épistémique, sécurité) — *P0*
- **Dans le dépôt** : nexus_os : 22 agents, 30 skills, runtime/harness/evals/context/memory/providers/creator ; Kc1t/alethe-agents (★832) et openclaw/openclaw (★391 640) à comparer
- **Existant (cadrage initial)** : HCSM validator ; proto epistemics.ts ; docs/agents/verification-agent.md
- **À auditer par ArenaAI** : Vérification automatique : validation de schéma, cohérence épistémique (fait/inférence/hypothèse), détection de contradictions, vérification de sources, tests de sécurité, revue de code
- **Pistes d'origine à vérifier** : HCSM validator ; JSON Schema/Ajv ; Z3/SMT (cohérence) ; Deequ/Great Expectations (qualité de données) ; Semgrep ; Trivy ; guardrails (NeMo Guardrails)
- **Décision attendue** : BUILD : tout nœud/claim passe un validateur avant persistance ; refus explicite si preuves insuffisantes (pattern Refusal HCSM)
- **Critère de succès** : Aucune affirmation non sourcée ne peut entrer en base ; 100% des claims ont une provenance
- **Candidats vérifiés (08/10/2026)** : aaif-goose/goose ★55 067 [Apache-2.0] · OpenHands/OpenHands ★90 275 [MIT] · openclaw/openclaw ★391 640 [MIT] · Kc1t/alethe-agents ★832 [AGPL-3.0] · modelcontextprotocol/modelcontextprotocol ★9 406 [Apache-2.0] · a2aproject/A2A ★26 073 [Apache-2.0] · agentclientprotocol/agent-client-protocol ★4 391 [Apache-2.0] · ggml-org/llama.cpp ★130 687 [MIT] · ollama/ollama ★182 569 [MIT]
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **Modules du shell concernés** : systeme, command, c, o, g, n, i, t, a, e, s
- **Concept art** : `art-07`

### D35 · Agent UX & transparence — *P1*
- **Dans le dépôt** : nexus_os : 22 agents, 30 skills, runtime/harness/evals/context/memory/providers/creator ; Kc1t/alethe-agents (★832) et openclaw/openclaw (★391 640) à comparer
- **Existant (cadrage initial)** : chatConsole (Watchtower) ; orchestra dans reaserch-engine
- **À auditer par ArenaAI** : Expérience utilisateur des agents : plans visibles, approbations, journal des actions, coût affiché, confiance, interruption, annulation, replay, 'pourquoi cette réponse'
- **Pistes d'origine à vérifier** : Agent transparency patterns ; Langfuse ; OpenTelemetry GenAI semantic conventions ; Trace viewers (Arize/LangSmith) ; approval gates
- **Décision attendue** : BUILD : une UI d'agent digne de confiance (plan → étapes → preuves → coût → annulation)
- **Critère de succès** : L'utilisateur peut expliquer, après coup, tout ce qu'un agent a fait et pourquoi
- **Candidats vérifiés (08/10/2026)** : aaif-goose/goose ★55 067 [Apache-2.0] · OpenHands/OpenHands ★90 275 [MIT] · openclaw/openclaw ★391 640 [MIT] · Kc1t/alethe-agents ★832 [AGPL-3.0] · modelcontextprotocol/modelcontextprotocol ★9 406 [Apache-2.0] · a2aproject/A2A ★26 073 [Apache-2.0] · agentclientprotocol/agent-client-protocol ★4 391 [Apache-2.0]
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **Modules du shell concernés** : systeme, command, a, g, e, n, t, s
- **Concept art** : `art-05`

### D90 · Compétences d'agents (Skill Registry) — *P0*
- **Dans le dépôt** : nexus_os : 22 agents, 30 skills, runtime/harness/evals/context/memory/providers/creator ; Kc1t/alethe-agents (★832) et openclaw/openclaw (★391 640) à comparer
- **Existant (cadrage initial)** : nexus_os : 30 compétences Python
- **À auditer par ArenaAI** : Comment Alethe et OpenClaw empaquettent-ils des compétences réutilisables (dossiers, manifestes, résolution) ?
- **Pistes d'origine à vérifier** : Kc1t/alethe-agents, openclaw/openclaw, aaif-goose/goose
- **Décision attendue** : Unifier skills et plugins sous un même manifeste (module.json)
- **Critère de succès** : Une compétence écrite une fois est utilisable par tous les agents
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · aaif-goose/goose ★55 067 [Apache-2.0]
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **Modules du shell concernés** : c, a, r, t, e, o, g, n, i, s
- **Concept art** : `art-02`

## Outils — 6 domaines

### D36 · IA locale (inférence) — *P1*
- **Existant (cadrage initial)** : watchtower (Ollama mentionné), audit/CATALOGUE-OUTILS (Ollama, LM Studio, llama.cpp)
- **À auditer par ArenaAI** : Inférence locale sur GTX 1060 6 Go / 16 Go RAM : modèles qui tiennent (3-8B quantifiés), qualité FR, embeddings, rerankers, vision, TTS/STT locaux, latence, VRAM, alternatives CPU
- **Pistes d'origine à vérifier** : llama.cpp (MIT) ; Ollama ; LM Studio ; vLLM/SGLang (serveur) ; ONNX Runtime ; WebLLM/Transformers.js (navigateur) ; Whisper.cpp ; Piper ; Kokoro ; Qwen3 (familles) ; Gemma ; Mistral
- **Décision attendue** : WRAP : un seul point d'entrée LLM local (API OpenAI-compatible) + un modèle de secours cloud plafonné
- **Critère de succès** : Question posée hors-ligne : réponse en <15 s avec un modèle local, GPU non saturé, pas de fuite réseau
- **Candidats vérifiés (08/10/2026)** : GuillaumeGomez/sysinfo ★2 748 [MIT] · gfx-rs/wgpu ★18 234 [Apache-2.0] · ggml-org/llama.cpp ★130 687 [MIT] · ollama/ollama ★182 569 [MIT]
- **Concept art** : `art-19`

### D37 · IA cloud multi-provider & routage — *P1*
- **Dans le dépôt** : 9 projets + 13 branches ; _incoming 859 fichiers/31 Mo ; scripts/verif-completude-repos.py : 2 157 fichiers, 0 manquant
- **Existant (cadrage initial)** : proto (Gemini en dur — dette identifiée) ; ADR-008 (LLMProvider)
- **À auditer par ArenaAI** : Abstraction multi-fournisseurs : routage par coût/qualité/latence, fallback, prompts versionnés, évaluations comparatives, cache, conformité (données envoyées), quotas gratuits
- **Pistes d'origine à vérifier** : LiteLLM ; OpenRouter ; Groq ; Cerebras ; GitHub Models ; Google AI ; Anthropic ; OpenAI ; DSPy (optimisation) ; promptfoo (évaluations)
- **Décision attendue** : WRAP : interface LLMProvider unique + routage déclaratif + plafonds (voir D26)
- **Critère de succès** : Changer de fournisseur = 1 ligne de configuration, 0 changement de code métier
- **Candidats vérifiés (08/10/2026)** : ggml-org/llama.cpp ★130 687 [MIT] · ollama/ollama ★182 569 [MIT]
- **Modules du shell concernés** : systeme, command
- **Concept art** : `art-08`

### D38 · Automatisation / workflows / jobs — *P1*
- **Existant (cadrage initial)** : watchtower (monitoring), reaserch-engine (pipeline)
- **À auditer par ArenaAI** : Orchestration de tâches locales : déclencheurs (fichier, planification, événement), files, reprise, parallélisme, journal, human-in-the-loop
- **Pistes d'origine à vérifier** : Activepieces (MIT) ; n8n (fair-code, non OSI) ; Windmill ; Prefect ; Dagster ; Temporal ; Restate ; DBOS ; BullMQ ; Celery ; Quartz ; node-cron
- **Décision attendue** : Décider entre un moteur de workflow généraliste intégré et des jobs internes ; éviter une double architecture
- **Critère de succès** : Un workflow 'nouveau document → OCR → indexation → notification → agent' tourne sans intervention
- **Candidats vérifiés (08/10/2026)** : aaif-goose/goose ★55 067 [Apache-2.0] · OpenHands/OpenHands ★90 275 [MIT] · openclaw/openclaw ★391 640 [MIT] · Kc1t/alethe-agents ★832 [AGPL-3.0] · modelcontextprotocol/modelcontextprotocol ★9 406 [Apache-2.0] · a2aproject/A2A ★26 073 [Apache-2.0] · agentclientprotocol/agent-client-protocol ★4 391 [Apache-2.0] · ggml-org/llama.cpp ★130 687 [MIT] · ollama/ollama ★182 569 [MIT]
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **Modules du shell concernés** : systeme, command, a, g, e, n, t, s
- **Concept art** : `art-03`

### D39 · OSINT / renseignement — *P0*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : watchtower (globe, entités, intelTwin, sources clés), audit/CATALOGUE-OUTILS §E (11 outils OSINT)
- **À auditer par ArenaAI** : Sources ouvertes exploitables légalement : flux géopolitiques, maritimes (AIS), aériens (ADS-B), satellite, marchés, presse, ONG, données publiques ; graphes d'entités ; détection d'anomalies ; timeline
- **Pistes d'origine à vérifier** : GDELT ; AISStream ; OpenSky ; adsb.lol ; CelesTrak ; EONET ; OSM/Overpass ; BOAMP/TED (marchés publics) ; INSEE/SIRENE ; Overture Maps ; GLEIF ; OpenSanctions
- **Décision attendue** : WRAP les collecteurs existants ; CONSTRUIRE la couche d'analyse (graphe + timeline + alertes) ; cadrer le légal (données personnelles)
- **Critère de succès** : Le module Watchtower produit une note de situation sourcée et géolocalisée en <10 min
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · CesiumGS/cesium ★15 811 [Apache-2.0]
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : OpenDroneMap/ODM [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : FalkorDB/FalkorDB [SSPL-1.0] : ⛔ à écarter
- **⚠️ Licence** : WebODM/WebODM [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : WorldPixelMap/android-gods-eye-view [NON-COMMERCIAL] : ⛔ à écarter
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **⚠️ Licence** : neo4j/neo4j [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, c, a, r, t, e, g, n, s, p, h
- **Concept art** : `art-04`

### D40 · Monitoring / veille / alerting — *P0*
- **Existant (cadrage initial)** : watchtower (sources live), reaserch-engine ; aucune alerte structurée
- **À auditer par ArenaAI** : Veille automatisée : RSS, APIs, pages web (changements), détection de nouveauté, scoring de pertinence, alertes, résumé LLM, déduplication
- **Pistes d'origine à vérifier** : FreshRSS ; Miniflux ; changedetection.io ; RSS-Bridge ; Huginn ; ntfy ; Apprise ; Watchtower (containrrr) ; SearXNG
- **Décision attendue** : BUILD un moteur d'alertes local (règles + scoring + digest) branché au centre de notifications
- **Critère de succès** : Une alerte pertinente (marché public, actualité du territoire) arrive dans l'app, avec source et résumé
- **Candidats vérifiés (08/10/2026)** : aaif-goose/goose ★55 067 [Apache-2.0] · OpenHands/OpenHands ★90 275 [MIT] · openclaw/openclaw ★391 640 [MIT] · Kc1t/alethe-agents ★832 [AGPL-3.0] · modelcontextprotocol/modelcontextprotocol ★9 406 [Apache-2.0] · a2aproject/A2A ★26 073 [Apache-2.0] · agentclientprotocol/agent-client-protocol ★4 391 [Apache-2.0] · ggml-org/llama.cpp ★130 687 [MIT] · ollama/ollama ★182 569 [MIT] · moj-analytical-services/splink ★2 462 [MIT]
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **Modules du shell concernés** : a, g, e, n, t, s
- **Concept art** : `art-03`

### D85 · Statistiques & visualisation de donnees — *P1*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : dashboard BTP (branche 01a08449) ; figures matplotlib de frontignan ; graphes D3 de ETAT-DE-LART
- **À auditer par ArenaAI** : Librairies de graphiques performantes et honnetes (incertitude affichee), tableaux de donnees volumineux, tableaux croises, export, analyse locale sans serveur, impression/PDF
- **Pistes d'origine à vérifier** : ECharts ; visx ; Recharts ; Observable Plot ; D3 ; DuckDB (analyse locale) ; TanStack Table ; Univer (tableur) ; matplotlib pour les rapports ; Vega-Lite
- **Décision attendue** : Choisir 1-2 librairies et un composant de tableau standard, avec regle d'affichage de la provenance et de l'incertitude
- **Critère de succès** : 5 indicateurs de chantier fiables, methode de calcul affichee, export PDF/CSV teste
- **Candidats vérifiés (08/10/2026)** : LadybugDB/ladybug ★1 825 [MIT] · getzep/graphiti ★31 553 [Apache-2.0] · neo4j/neo4j ★17 284 [GPL-3.0] · FalkorDB/FalkorDB ★7 967 [SSPL-1.0] · tesseract-ocr/tesseract ★76 861 [Apache-2.0] · ocrmypdf/OCRmyPDF ★34 960 [MPL-2.0] · PaddlePaddle/PaddleOCR ★90 775 [Apache-2.0] · mindee/doctr ★6 381 [Apache-2.0] · apache/tika ★4 091 [Apache-2.0] · opendatalab/MinerU ★81 295 [Apache-2.0] · docling-project/docling ★68 537 [MIT] · Unstructured-IO/unstructured ★15 548 [Apache-2.0]
- **⚠️ Licence** : FalkorDB/FalkorDB [SSPL-1.0] : ⛔ à écarter
- **⚠️ Licence** : ocrmypdf/OCRmyPDF [MPL-2.0] : fichier par fichier
- **⚠️ Licence** : neo4j/neo4j [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, b, t, p, g, r, a, h, e
- **Concept art** : `art-06`

## Knowledge — 8 domaines

### D41 · Cognition / HCSM (état cognitif) — *P0*
- **Dans le dépôt** : COGNITORIUM (131 fichiers, 24 Mo), proto-cognitorium (87 Mo), HCSM (87 fichiers), ETAT-DE-LART-PSYCHOLOGIE (37 fichiers) + 137 Ko de code récupéré du patch 01a0389d, docs/carre-das/07
- **Existant (cadrage initial)** : HCSM (specs, ontologie, validator, modèles mathématiques)
- **À auditer par ArenaAI** : Instrumentation et mesure : quels instruments/catalogues de mesures existent, validité psychométrique, biais, incertitude, éthique, refus d'estimer ; état de l'art 2026
- **Pistes d'origine à vérifier** : HCSM v0.1 ; catalogues psychométriques (IPIP, Big Five, RIASEC, SDT) ; frameworks de mesure en éducation ; psychométrie moderne (IRT, CAT) ; documentation des limites
- **Décision attendue** : CONSERVER le cadre HCSM ; l'implémenter progressivement (Cognition Hub) et l'exposer comme service
- **Critère de succès** : Toute estimation d'état cognitif porte valeur + incertitude + fenêtre + preuves + alternatives
- **Modules du shell concernés** : systeme, command, c, o, g, n, i, t, d, u, m, e, s
- **Concept art** : `art-11`

### D42 · Compétences / métiers / référentiels — *P0*
- **Existant (cadrage initial)** : proto: moteur ROME (1911 fiches, 17920 compétences, FORMACODE) ; Skill Graph implicite
- **À auditer par ArenaAI** : Référentiels et ontologies : ESCO (UE), ROME (FR), O*NET, Lightcast, taxonomies de compétences transversales, alignements entre référentiels, API officielles, licences d'usage
- **Pistes d'origine à vérifier** : ESCO (API + SPARQL) ; ROME/France Travail (API) ; O*NET (API, US) ; ESCO-ROME mappings ; DigComp ; SFIA ; Ontologie SKOS
- **Décision attendue** : WRAP : importer les référentiels officiels + construire la couche de matching explicable (pourquoi / il manque quoi)
- **Critère de succès** : Un profil réel obtient 5 métiers pertinents avec justification sourcée sur référentiel officiel
- **Candidats vérifiés (08/10/2026)** : LadybugDB/ladybug ★1 825 [MIT] · getzep/graphiti ★31 553 [Apache-2.0] · neo4j/neo4j ★17 284 [GPL-3.0] · FalkorDB/FalkorDB ★7 967 [SSPL-1.0]
- **⚠️ Licence** : neo4j/neo4j [GPL-3.0] : copyleft fort
- **⚠️ Licence** : FalkorDB/FalkorDB [SSPL-1.0] : ⛔ à écarter
- **Modules du shell concernés** : c, o, g, n, i, t, r, a, p, h, e
- **Concept art** : `art-06`

### D43 · Learning Engine (pédagogie) — *P1*
- **Dans le dépôt** : docs/carre-das/00→03 ; shell/ (portail 14 modules/104 fonctions, non encore branché aux données)
- **Existant (cadrage initial)** : COGNITORIUM/learning (CLE PoC 2 scénarios) ; learning/ARCHITECTURE.md
- **À auditer par ArenaAI** : Apprentissage adaptatif : knowledge tracing (BKT/DKT), spaced repetition (SM-2/FSRS), mastery learning, simulation pédagogique, xAPI/cmi5, LTI, H5P, apprentissage par problèmes
- **Pistes d'origine à vérifier** : FSRS ; Anki (algo) ; BKT/DKT/pyKT ; Open edX ; H5P ; xAPI/cmi5 ; LTI 1.3 ; Moodle ; Cogrammar-like ; Merrill/4C-ID
- **Décision attendue** : BUILD la boucle pédagogique sur le CLE existant ; WRAP les standards (xAPI) pour l'interopérabilité
- **Critère de succès** : Un parcours adaptatif ajuste la difficulté selon les réponses et prouve le transfert
- **Candidats vérifiés (08/10/2026)** : LadybugDB/ladybug ★1 825 [MIT] · getzep/graphiti ★31 553 [Apache-2.0] · neo4j/neo4j ★17 284 [GPL-3.0] · FalkorDB/FalkorDB ★7 967 [SSPL-1.0] · mesa/mesa ★3 877 [Apache-2.0] · JuliaDynamics/Agents.jl ★919 [MIT] · OpenTTD/OpenTTD ★8 345 [GPL-2.0] · OpenRCT2/OpenRCT2 ★16 397 [GPL-3.0] · OpenMW/openmw ★6 609 [GPL-3.0] · freeciv/freeciv ★1 602 [GPL-2.0] · godotengine/godot ★118 272 [MIT]
- **⚠️ Licence** : OpenTTD/OpenTTD [GPL-2.0] : copyleft fort
- **⚠️ Licence** : FalkorDB/FalkorDB [SSPL-1.0] : ⛔ à écarter
- **⚠️ Licence** : freeciv/freeciv [GPL-2.0] : copyleft fort
- **⚠️ Licence** : OpenRCT2/OpenRCT2 [GPL-3.0] : copyleft fort
- **⚠️ Licence** : OpenMW/openmw [GPL-3.0] : copyleft fort
- **⚠️ Licence** : neo4j/neo4j [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, c, o, g, n, i, t, m, a, d
- **Concept art** : `art-19`

### D44 · Base de connaissances sourcée — *P0*
- **Dans le dépôt** : COGNITORIUM (131 fichiers, 24 Mo), proto-cognitorium (87 Mo), HCSM (87 fichiers), ETAT-DE-LART-PSYCHOLOGIE (37 fichiers) + 137 Ko de code récupéré du patch 01a0389d, docs/carre-das/07
- **Existant (cadrage initial)** : ETAT-DE-LART (CSV 42 champs, Trust Factor, PRISMA) ; docs/
- **À auditer par ArenaAI** : Trust Factor ; gestion bibliographique ; revues systématiques ; qualité de preuve (GRADE) ; provenance
- **Pistes d'origine à vérifier** : ETAT-DE-LART-PSYCHOLOGIE ; outils de revue systématique (Covidence, Rayyan) ; Zotero ; BetterBibTeX ; PRISMA 2020 ; GRADE ; Scholia ; Wikidata comme hub d'identifiants
- **Décision attendue** : CONSERVER la méthode ; l'industrialiser (ingestion DOI → fiche → graphe) et l'ouvrir à d'autres domaines (BTP, territoire)
- **Critère de succès** : Ajouter une publication coûte <5 min et alimente automatiquement le graphe et la recherche
- **Candidats vérifiés (08/10/2026)** : LadybugDB/ladybug ★1 825 [MIT] · getzep/graphiti ★31 553 [Apache-2.0] · neo4j/neo4j ★17 284 [GPL-3.0] · FalkorDB/FalkorDB ★7 967 [SSPL-1.0] · duckdb/duckdb ★41 982 [MIT] · sqlite/sqlite ★10 620 [Domaine public] · apache/arrow ★17 188 [Apache-2.0] · pola-rs/polars ★40 008 [MIT] · asg017/sqlite-vec ★8 170 [Apache-2.0] · ourresearch/openalex-guts ★157 [MIT] · CrossRef/rest-api-doc ★801 [MIT (doc propriétaire)] · docling-project/docling ★68 537 [MIT]
- **⚠️ Licence** : FalkorDB/FalkorDB [SSPL-1.0] : ⛔ à écarter
- **⚠️ Licence** : neo4j/neo4j [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : c, o, g, n, i, t, r, a, p, h, e
- **Concept art** : `art-06`

### D45 · Recherche scientifique (moteurs) — *P1*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : reaserch-engine (CrossrefRetriever) ; ETAT-DE-LART (scripts DOI)
- **À auditer par ArenaAI** : Accès programmatique à la littérature : OpenAlex, Crossref, Semantic Scholar, PubMed, arXiv, HAL, theses.fr, DOAJ, Unpaywall, accès ouvert ; extraction structurée (GROBID) ; synthèses
- **Pistes d'origine à vérifier** : OpenAlex API ; Crossref ; Semantic Scholar API ; arXiv ; HAL ; theses.fr ; Unpaywall ; GROBID ; PaperQA2 ; STORM ; Scite (citations)
- **Décision attendue** : WRAP : méta-connecteur scientifique unifié (idempotent, cache, provenance) alimentant le Research Agent
- **Critère de succès** : Une revue de littérature sur un sujet BTP/territoire produite en 1 h avec 30 sources liées
- **Candidats vérifiés (08/10/2026)** : ourresearch/openalex-guts ★157 [MIT] · CrossRef/rest-api-doc ★801 [MIT (doc propriétaire)] · docling-project/docling ★68 537 [MIT] · opendatalab/MinerU ★81 295 [Apache-2.0]
- **Modules du shell concernés** : systeme, command, d, o, c, u, m, e, n, t, s
- **Concept art** : `art-14`

### D46 · Documents / OCR / extraction de tableaux — *P0*
- **Dans le dépôt** : branche arena_01a08449 : 22 rapports, 11 documents_sources, engine/btp_multi_agent.py ; corpus raw : 61 fichiers (43 PDF, 5 xlsm) dont DCE/CCTP/CCAP/BPU, signalisation OPPBTP, AIPR
- **Existant (cadrage initial)** : corpus local (≈100 PDF/XLS BTP à la racine du dépôt) ; audit/CATALOGUE-OUTILS §B/§D (Marker, Docling, Tesseract, PaddleOCR, ocrmypdf)
- **À auditer par ArenaAI** : Extraction fiable sur documents techniques FR : CCTP, CCAP, BPU, DQE, plans, essais, .doc/.xls anciens, tableaux chiffrés, formulaires ; structure + chiffres + tableaux ; qualité/vérification
- **Pistes d'origine à vérifier** : marker (Apache-2.0, 40k★) ; MinerU (actif) ; Docling/IBM ; olmOCR ; Surya ; PaddleOCR ; Tesseract ; Camelot/pdfplumber (tableaux) ; Apache Tika ; markitdown (MIT, 188k★) ; unpdf ; LibreOffice headless (xls→xlsx)
- **Décision attendue** : BUILD un pipeline documentaire local (PDF/XLS/DOC → markdown + JSON structuré + tableaux vérifiés) avec provenance page
- **Critère de succès** : Un DQE ou un BPU .xls/.pdf devient un tableau exploitable et comparable, avec 0 perte de chiffre
- **Candidats vérifiés (08/10/2026)** : tesseract-ocr/tesseract ★76 861 [Apache-2.0] · ocrmypdf/OCRmyPDF ★34 960 [MPL-2.0] · PaddlePaddle/PaddleOCR ★90 775 [Apache-2.0] · mindee/doctr ★6 381 [Apache-2.0] · apache/tika ★4 091 [Apache-2.0] · opendatalab/MinerU ★81 295 [Apache-2.0] · docling-project/docling ★68 537 [MIT] · Unstructured-IO/unstructured ★15 548 [Apache-2.0]
- **⚠️ Licence** : ocrmypdf/OCRmyPDF [MPL-2.0] : fichier par fichier
- **Modules du shell concernés** : b, t, p, d, o, c, u, m, e, n, s
- **Concept art** : `art-07`

### D47 · Base documentaire personnelle / Obsidian — *P1*
- **Dans le dépôt** : corpus raw (43 PDF) ; docs/recherche/03 (Marker, MinerU, Docling déjà arbitrés)
- **Existant (cadrage initial)** : docs/ (Obsidian précisé par l'utilisateur)
- **À auditer par ArenaAI** : Interopérabilité avec un vault Obsidian : markdown, wikilinks, tags, propriétés, dataview, sync, import/export, double sens (l'app lit et écrit dans le vault)
- **Pistes d'origine à vérifier** : Obsidian (format) ; Foam ; Quartz ; Dataview ; Obsidian Bases ; markdown-it ; remark ; link resolution ; Zettelkasten
- **Décision attendue** : WRAP : l'app lit/écrit le vault Obsidian de l'utilisateur sans le transformer
- **Critère de succès** : Un document modifié dans l'app apparaît correctement dans Obsidian (et inversement)
- **Candidats vérifiés (08/10/2026)** : duckdb/duckdb ★41 982 [MIT] · sqlite/sqlite ★10 620 [Domaine public] · apache/arrow ★17 188 [Apache-2.0] · pola-rs/polars ★40 008 [MIT] · asg017/sqlite-vec ★8 170 [Apache-2.0] · yjs/yjs ★22 910 [MIT] · automerge/automerge ★6 650 [MIT] · syncthing/syncthing ★89 219 [MPL-2.0] · tesseract-ocr/tesseract ★76 861 [Apache-2.0] · ocrmypdf/OCRmyPDF ★34 960 [MPL-2.0] · PaddlePaddle/PaddleOCR ★90 775 [Apache-2.0] · mindee/doctr ★6 381 [Apache-2.0]
- **⚠️ Licence** : syncthing/syncthing [MPL-2.0] : fichier par fichier
- **⚠️ Licence** : ocrmypdf/OCRmyPDF [MPL-2.0] : fichier par fichier
- **Modules du shell concernés** : d, o, c, u, m, e, n, t, s
- **Concept art** : `art-19`

### D87 · Language Decoder (langage & cognition) — *P1*
- **Dans le dépôt** : COGNITORIUM (131 fichiers, 24 Mo), proto-cognitorium (87 Mo), HCSM (87 fichiers), ETAT-DE-LART-PSYCHOLOGIE (37 fichiers) + 137 Ko de code récupéré du patch 01a0389d, docs/carre-das/07
- **Existant (cadrage initial)** : Language-decoder, 2 branches dans _incoming
- **À auditer par ArenaAI** : Analyse linguistique locale : spaCy FR, Stanza, UDPipe, LanguageTool, modèles HF de parsing
- **Pistes d'origine à vérifier** : spaCy (MIT), Stanza (Apache-2.0), LanguageTool (LGPL-2.1), UDPipe (MPL-2.0)
- **Décision attendue** : Brancher le décodeur comme compétence du profil cognitif (module langage)
- **Critère de succès** : Un texte fourni produit une analyse réutilisable par le profil
- **Modules du shell concernés** : c, o, g, n, i, t
- **Concept art** : `art-11`

## World — 9 domaines

### D48 · Cartographie / GIS — *P0*
- **Dans le dépôt** : watchtower/index.html (55 Ko) + branche arena_01a072e1 (comparatif Cesium 21 357 ms vs MapLibre 3 ms) ; frontignan (28 fichiers, 14 Mo, deck 18 slides)
- **Existant (cadrage initial)** : watchtower (Cesium, 100 modules, 27 couches), atlas, KML/GeoJSON, intelTwin ; GEOPORTAIL.pdf
- **À auditer par ArenaAI** : Stack géo moderne : rendu 2D/3D, tuiles vectorielles/3D/terrain, formats (PMTiles, COG, GeoParquet, FlatGeobuf), moteurs de service, traitement local, échelle planète→objet
- **Pistes d'origine à vérifier** : MapLibre GL JS (vérifié actif) ; CesiumJS (Apache-2.0) ; deck.gl ; GDAL ; DuckDB Spatial (MIT) ; Apache Sedona ; Martin (tuiles, 4k★) ; PMTiles ; Titiler (COG) ; STAC (stac-fastapi) ; QGIS (bureau)
- **Décision attendue** : Décider la pile principale (MapLibre 2D + Cesium 3D ponctuel ?) et le rôle de QGIS (bureau, exports) ; budget GPU obligatoire
- **Critère de succès** : Affichage fluide d'un territoire à 3 échelles avec données IGN, OSM et du projet, hors ligne
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · CesiumGS/cesium ★15 811 [Apache-2.0]
- **⚠️ Licence** : kobotoolbox/kpi [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : FalkorDB/FalkorDB [SSPL-1.0] : ⛔ à écarter
- **⚠️ Licence** : ocrmypdf/OCRmyPDF [MPL-2.0] : fichier par fichier
- **⚠️ Licence** : WorldPixelMap/android-gods-eye-view [NON-COMMERCIAL] : ⛔ à écarter
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **⚠️ Licence** : neo4j/neo4j [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : c, a, r, t, e, b, p, g, h
- **Concept art** : `art-02`

### D49 · Données géographiques (FR/UE) — *P0*
- **Dans le dépôt** : branche arena_01a08449 : 22 rapports, 11 documents_sources, engine/btp_multi_agent.py ; corpus raw : 61 fichiers (43 PDF, 5 xlsm) dont DCE/CCTP/CCAP/BPU, signalisation OPPBTP, AIPR
- **Existant (cadrage initial)** : DATA_SOURCES.md (Esri/CARTO/OSM, sans clé) ; IGN/Géoportail cités ; frontignan (données territoriales)
- **À auditer par ArenaAI** : Sources ouvertes françaises et européennes exploitables : limites administratives, cadastre, topographie LiDAR HD, ortho, occupation du sol, risques, réseaux, données socio-économiques, qualité et licences
- **Pistes d'origine à vérifier** : IGN (BD TOPO, LiDAR HD, RGE ALTI, ortho) ; BAN ; Cadastre/Etalab ; DVF ; OCS GE ; INSEE (Filosofi, BPE, RP) ; Géorisques ; BRGM/InfoTerre ; Copernicus/Sentinel ; STAC ; Géoportail de l'urbanisme ; data.gouv.fr
- **Décision attendue** : WRAP : un connecteur 'données publiques FR' avec cache et licences ; Documenter chaque flux (endpoint, licence, fréquence)
- **Critère de succès** : Un profil territorial complet (population, bâti, risques, réseaux) assemblé automatiquement pour une commune
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · LadybugDB/ladybug ★1 825 [MIT]
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : FreeCAD/FreeCAD [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : OpenDroneMap/ODM [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : FalkorDB/FalkorDB [SSPL-1.0] : ⛔ à écarter
- **⚠️ Licence** : LinuxCNC/linuxcnc [GPL-2.0] : copyleft fort
- **⚠️ Licence** : neo4j/neo4j [GPL-3.0] : copyleft fort
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **⚠️ Licence** : WebODM/WebODM [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : openscad/openscad [GPL-2.0] : copyleft fort
- **Modules du shell concernés** : c, a, r, t, e, b, p, g, h
- **Concept art** : `art-06`

### D50 · Territory Engine — *P0*
- **Dans le dépôt** : watchtower/index.html (55 Ko) + branche arena_01a072e1 (comparatif Cesium 21 357 ms vs MapLibre 3 ms) ; frontignan (28 fichiers, 14 Mo, deck 18 slides)
- **Existant (cadrage initial)** : frontignan (analyse territoriale + vision 2040, 249 sources) ; watchtower (intelTwin)
- **À auditer par ArenaAI** : Modèles territoriaux réplicables : socio-économie, mobilité, budget communal, projets, foncier, services, indicateurs, prospective, comparaison de communes
- **Pistes d'origine à vérifier** : Filosofi/BPE/RP (INSEE) ; OpenDataSoft ; data.gouv ; Observatoire des territoires ; SCoT/PLU (GPU) ; DVF (DGFiP) ; Base Mérimée ; OSM ; UrbanSim ; Landuse models ; CityScope
- **Décision attendue** : BUILD : généraliser la méthode Frontignan en moteur paramétrable (commune → dossier complet)
- **Critère de succès** : Une nouvelle commune produit un dossier territorial structuré (sources datées, estimations marquées) en 1 jour
- **Candidats vérifiés (08/10/2026)** : GuillaumeGomez/sysinfo ★2 748 [MIT] · gfx-rs/wgpu ★18 234 [Apache-2.0] · duckdb/duckdb ★41 982 [MIT] · sqlite/sqlite ★10 620 [Domaine public] · apache/arrow ★17 188 [Apache-2.0] · pola-rs/polars ★40 008 [MIT] · asg017/sqlite-vec ★8 170 [Apache-2.0]
- **Modules du shell concernés** : systeme, command, c, a, r, t, e
- **Concept art** : `art-02`

### D51 · Timeline / temporalité / 4D — *P0*
- **Dans le dépôt** : animation-chronos (36 fichiers, 5,3 Mo)
- **Existant (cadrage initial)** : watchtower (28 modules 4D mentionnés dans RND), animation-chronos, proto (timeline), CLE (decay)
- **À auditer par ArenaAI** : Modélisation temporelle : bi-temporalité (valide/transactionnel), timelines unifiées, 4D chantier, frise, animation de données, rejouabilité, échelles de temps, événements géolocalisés
- **Pistes d'origine à vérifier** : vis-timeline ; D3 ; Recharts ; deck.gl Timeline ; Gantt (frappe-gantt, dhtmlx) ; hifitime/Arrow temporal ; Event sourcing ; interval trees
- **Décision attendue** : BUILD : une primitive Timeline partagée par tous les modules (chantier, territoire, apprentissage, veille)
- **Critère de succès** : La même timeline affiche un marché public, une compétence oubliée, une phase de chantier et un événement satellite
- **Modules du shell concernés** : systeme, command, c, a, r, t, e, b, p
- **Concept art** : `art-04`

### D52 · Digital Twin — *P1*
- **Dans le dépôt** : docs/carre-das/00→03 ; shell/ (portail 14 modules/104 fonctions, non encore branché aux données)
- **Existant (cadrage initial)** : watchtower (ficheLieu, intelTwin, chantier), BTP + BIM + 3D + capteurs
- **À auditer par ArenaAI** : Architectures de jumeau numérique : BIM+GIS+capteurs+temps, standards (IFC, CityGML, 3D Tiles, IoT), plateformes (NVIDIA Omniverse, Eclipse Ditto, FIWARE), coût de mise en œuvre
- **Pistes d'origine à vérifier** : Eclipse Ditto ; FIWARE ; NVIDIA Omniverse ; Cesium 3D Tiles ; CityGML 3.0 ; IoT (MQTT, Sparkplug B) ; Asset Administration Shell (Industrie 4.0)
- **Décision attendue** : Décider la portée réaliste du jumeau v1 (chantier ? territoire ? bâtiment ?) et les standards de données
- **Critère de succès** : Un jumeau de chantier restitue l'état réel (phasage, capteurs, documents) et le simule
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · CesiumGS/cesium ★15 811 [Apache-2.0]
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : xeokit/xeokit-sdk [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : WorldPixelMap/android-gods-eye-view [NON-COMMERCIAL] : ⛔ à écarter
- **⚠️ Licence** : IfcOpenShell/IfcOpenShell [LGPL-3.0] : copyleft faible
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **⚠️ Licence** : ThatOpen/engine_web-ifc [MPL-2.0] : fichier par fichier
- **Modules du shell concernés** : systeme, command, c, a, r, t, e, b, p
- **Concept art** : `art-19`

### D53 · Risques & résilience — *P0*
- **Dans le dépôt** : branche arena_01a08449 : 22 rapports, 11 documents_sources, engine/btp_multi_agent.py ; corpus raw : 61 fichiers (43 PDF, 5 xlsm) dont DCE/CCTP/CCAP/BPU, signalisation OPPBTP, AIPR
- **Existant (cadrage initial)** : corpus BTP (DT/DICT, essais), frontignan (qualité de l'eau), watchtower (EONET, inondation)
- **À auditer par ArenaAI** : Analyse de risques territoriaux et chantier : inondation, RGA (sécheresse), incendie, sismique, industriel, réseaux enfouis, sécurité des travailleurs (AIPR), ordres de service, DICT
- **Pistes d'origine à vérifier** : Géorisques (API) ; PPRI ; Institut des risques majeurs ; BRGM (BSS, RGA) ; Météo-France (Vigilance) ; Vigicrues ; AIPR/INRS ; OPPBTP ; DT/DICT (réformes travaux) ; Sogelink/Veox pour les réseaux
- **Décision attendue** : BUILD : un module risque (territoire + chantier) qui croise aléas, enjeux et dates
- **Critère de succès** : Un projet de voirie affiche automatiquement les aléas, servitudes et DICT à produire, avec sources
- **Modules du shell concernés** : systeme, command, c, a, r, t, e, b, p, o, m, n, d
- **Concept art** : `art-09`

### D54 · Climat / énergie / environnement — *P1*
- **Dans le dépôt** : watchtower/index.html (55 Ko) + branche arena_01a072e1 (comparatif Cesium 21 357 ms vs MapLibre 3 ms) ; frontignan (28 fichiers, 14 Mo, deck 18 slides)
- **Existant (cadrage initial)** : guide-conception-ice.pdf ; frontignan (qualité de l'eau, littoral)
- **À auditer par ArenaAI** : Évaluation environnementale : ACV, carbone, énergie, eau, biodiversité, chaleur urbaine, règlementation (RE2020, taxonomie UE, CSRD) et données
- **Pistes d'origine à vérifier** : RE2020 ; INIES (FDES) ; base carbone ADEME ; Climate Data Store (ERA5) ; Copernicus ; UMEP/SOLWEIG (microclimat) ; EnergyPlus ; OpenLCA ; Bilan Carbone
- **Décision attendue** : WRAP des bases officielles ; BUILD une couche d'indicateurs environnementaux par projet
- **Critère de succès** : Un projet de voirie/chaussée affiche son empreinte carbone et une comparaison de variantes
- **Candidats vérifiés (08/10/2026)** : duckdb/duckdb ★41 982 [MIT] · sqlite/sqlite ★10 620 [Domaine public] · apache/arrow ★17 188 [Apache-2.0] · pola-rs/polars ★40 008 [MIT] · asg017/sqlite-vec ★8 170 [Apache-2.0] · tesseract-ocr/tesseract ★76 861 [Apache-2.0] · ocrmypdf/OCRmyPDF ★34 960 [MPL-2.0] · PaddlePaddle/PaddleOCR ★90 775 [Apache-2.0] · mindee/doctr ★6 381 [Apache-2.0] · apache/tika ★4 091 [Apache-2.0] · opendatalab/MinerU ★81 295 [Apache-2.0] · docling-project/docling ★68 537 [MIT]
- **⚠️ Licence** : FreeCAD/FreeCAD [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : LinuxCNC/linuxcnc [GPL-2.0] : copyleft fort
- **⚠️ Licence** : openscad/openscad [GPL-2.0] : copyleft fort
- **⚠️ Licence** : ocrmypdf/OCRmyPDF [MPL-2.0] : fichier par fichier
- **Modules du shell concernés** : c, a, r, t, e
- **Concept art** : `art-19`

### D55 · Mobilité — *P1*
- **Dans le dépôt** : watchtower/index.html (55 Ko) + branche arena_01a072e1 (comparatif Cesium 21 357 ms vs MapLibre 3 ms) ; frontignan (28 fichiers, 14 Mo, deck 18 slides)
- **Existant (cadrage initial)** : frontignan (mobilités, PEM), watchtower (OSM traffic, GTFS non branché ?)
- **À auditer par ArenaAI** : Mobilité : GTFS/GTFS-RT (réseaux de transport), trafic, vélo/piéton, stationnement, simulation d'accessibilité, PEM (pôle d'échange multimodal)
- **Pistes d'origine à vérifier** : GTFS / GTFS-RT ; OSM ; SUMO ; MATSim ; OpenTripPlanner ; Valhalla ; GraphHopper ; TransportAPI ; Modos ; Vélo & Territoires
- **Décision attendue** : WRAP les flux ; BUILT des indicateurs (accessibilité, temps de trajet, jonctions)
- **Critère de succès** : Une commune visualise l'accessibilité en transports avant/après un projet
- **Candidats vérifiés (08/10/2026)** : LadybugDB/ladybug ★1 825 [MIT] · getzep/graphiti ★31 553 [Apache-2.0] · neo4j/neo4j ★17 284 [GPL-3.0] · FalkorDB/FalkorDB ★7 967 [SSPL-1.0] · mesa/mesa ★3 877 [Apache-2.0] · JuliaDynamics/Agents.jl ★919 [MIT]
- **⚠️ Licence** : FalkorDB/FalkorDB [SSPL-1.0] : ⛔ à écarter
- **⚠️ Licence** : neo4j/neo4j [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : c, a, r, t, e, o, m, n, d, g, p, h
- **Concept art** : `art-02`

### D86 · Synchronisation 2D ↔ 3D ↔ Temps (sélection unifiée) — *P0*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : watchtower (2D/3D) + animation-chronos + proto-cognitorium (graphe temporel)
- **À auditer par ArenaAI** : Comment relient-ils carte, globe, timeline et fiche entité chez Palantir Gotham, Kepler.gl, QGIS (plugins de synchronisation) ? Un seul modèle d'état partagé ?
- **Pistes d'origine à vérifier** : deck.gl + MapLibre + Cesium, maplibre-gl-sync-move, Kepler.gl, LadybugDB
- **Décision attendue** : Définir le contrat de synchronisation des vues (un identifiant sélectionné → toutes les vues réagissent)
- **Critère de succès** : Sélectionner un objet sur la carte met à jour 3D, timeline et dossier en moins de 100 ms
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · CesiumGS/cesium ★15 811 [Apache-2.0]
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : FalkorDB/FalkorDB [SSPL-1.0] : ⛔ à écarter
- **⚠️ Licence** : syncthing/syncthing [MPL-2.0] : fichier par fichier
- **⚠️ Licence** : WorldPixelMap/android-gods-eye-view [NON-COMMERCIAL] : ⛔ à écarter
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **⚠️ Licence** : neo4j/neo4j [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, c, a, r, t, e, b, p, o, g, n, i, h
- **Concept art** : `art-02`

## BTP — 10 domaines

### D56 · Chantier / suivi de travaux — *P0*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : corpus BTP racine (CCAP, CCTP, BPU, DQE, PAQ, plans, compte-rendus, essais, DT/DICT, AIPR) ; watchtower (chantier, phasage 4D, BOAMP)
- **À auditer par ArenaAI** : Pilotage de chantier : replanification, avancement, métrés, non-conformités, essais, comptes rendus, ordres de service, facturations/situations, sous-traitance, sécurité, qualité, DOE
- **Pistes d'origine à vérifier** : Odoo (modules chantier) ; ERPNext ; Tryton ; Procore/Fieldwire (référents marché) ; Batiscript/Kairnial/Finalcad ; GanttProject ; LibrePlan ; Synchro (4D) ; Kizeo Forms
- **Décision attendue** : BUILD : un module chantier sur le Core (documents + événements + tasks + timeline) alimenté par le corpus réel de l'utilisateur
- **Critère de succès** : Un chantier réel suivi de bout en bout dans l'app : planning, métrés, essais, non-conformités, DOE
- **Candidats vérifiés (08/10/2026)** : yjs/yjs ★22 910 [MIT] · automerge/automerge ★6 650 [MIT] · syncthing/syncthing ★89 219 [MPL-2.0] · FreeCAD/FreeCAD ★34 025 [LGPL-2.1] · openscad/openscad ★10 392 [GPL-2.0] · LinuxCNC/linuxcnc ★2 484 [GPL-2.0]
- **⚠️ Licence** : LinuxCNC/linuxcnc [GPL-2.0] : copyleft fort
- **⚠️ Licence** : syncthing/syncthing [MPL-2.0] : fichier par fichier
- **⚠️ Licence** : FreeCAD/FreeCAD [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : openscad/openscad [GPL-2.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, b, t, p
- **Concept art** : `art-19`

### D57 · OpenBIM / IFC / normes — *P0*
- **Dans le dépôt** : watchtower/index.html (55 Ko) + branche arena_01a072e1 (comparatif Cesium 21 357 ms vs MapLibre 3 ms) ; frontignan (28 fichiers, 14 Mo, deck 18 slides)
- **Existant (cadrage initial)** : watchtower (roadmap IFC→3D Tiles dans SOURCES-FR) ; corpus plans/DT
- **À auditer par ArenaAI** : OpenBIM : lecture/écriture IFC, visualisation web, contrôle qualité (IDS/BCF), quantités (QTO), passerelles vers CAD/GIS, standards (bSDD, IFD), échanges avec les logiciels du marché
- **Pistes d'origine à vérifier** : IfcOpenShell (LGPL-3.0, vérifié actif 2026-10-07) ; Bonsai/BlenderBIM ; web-ifc / IFC.js ; Speckle (Apache-2.0) ; xeokit ; bSDD ; IDS ; BCF ; FreeCAD BIM
- **Décision attendue** : WRAP IfcOpenShell + une visionneuse web IFC ; BUILD la couche métier (extraction de données, vérification, quantités)
- **Critère de succès** : Un IFC de maquette s'ouvre dans l'app, ses quantités sont extraites et comparées au DQE
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · CesiumGS/cesium ★15 811 [Apache-2.0]
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : FreeCAD/FreeCAD [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : xeokit/xeokit-sdk [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : LinuxCNC/linuxcnc [GPL-2.0] : copyleft fort
- **⚠️ Licence** : WorldPixelMap/android-gods-eye-view [NON-COMMERCIAL] : ⛔ à écarter
- **⚠️ Licence** : IfcOpenShell/IfcOpenShell [LGPL-3.0] : copyleft faible
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **⚠️ Licence** : ThatOpen/engine_web-ifc [MPL-2.0] : fichier par fichier
- **⚠️ Licence** : openscad/openscad [GPL-2.0] : copyleft fort
- **Modules du shell concernés** : c, a, r, t, e, b, p
- **Concept art** : `art-02`

### D58 · CAD / CAO conceptuel — *P1*
- **Dans le dépôt** : branche arena_01a08449 : 22 rapports, 11 documents_sources, engine/btp_multi_agent.py ; corpus raw : 61 fichiers (43 PDF, 5 xlsm) dont DCE/CCTP/CCAP/BPU, signalisation OPPBTP, AIPR
- **Existant (cadrage initial)** : néant (three.js dans proto) ; docs/audits/external/004
- **À auditer par ArenaAI** : Noyaux géométriques : B-rep vs CSG, paramétrique, formats d'échange (STEP, IGES, DXF, DWG), moteurs web et desktop, courbes de difficulté
- **Pistes d'origine à vérifier** : OpenCascade (OCCT) ; OCCT.js ; replicad ; CADQuery ; FreeCAD ; SolveSpace ; OpenSCAD ; JSCAD ; Zoo/KittyCAD ; LibreDWG ; ezdxf ; dxf-parser
- **Décision attendue** : WRAP Replicad/OCCT pour le paramétrique simple ; WRAP FreeCAD pour l'avancé ; ne pas écrire de noyau géométrique
- **Critère de succès** : Un novice modélise une pièce utile et l'exporte en STEP/DXF en <15 min
- **Candidats vérifiés (08/10/2026)** : FreeCAD/FreeCAD ★34 025 [LGPL-2.1] · openscad/openscad ★10 392 [GPL-2.0] · LinuxCNC/linuxcnc ★2 484 [GPL-2.0]
- **⚠️ Licence** : LinuxCNC/linuxcnc [GPL-2.0] : copyleft fort
- **⚠️ Licence** : FreeCAD/FreeCAD [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : openscad/openscad [GPL-2.0] : copyleft fort
- **Modules du shell concernés** : b, t, p
- **Concept art** : `art-19`

### D59 · 3D / rendu / temps réel — *P1*
- **Dans le dépôt** : branche arena_01a08449 : 22 rapports, 11 documents_sources, engine/btp_multi_agent.py ; corpus raw : 61 fichiers (43 PDF, 5 xlsm) dont DCE/CCTP/CCAP/BPU, signalisation OPPBTP, AIPR
- **Existant (cadrage initial)** : watchtower (Cesium + three.js dans proto) ; aholo-viewer (3DGS) dans l'audit outils
- **À auditer par ArenaAI** : Rendus : chargés (glTF/3D Tiles/splats), scènes de chantier, matériaux, lumière/ombre, performance WebGL2/WebGPU, pipelines de conversion
- **Pistes d'origine à vérifier** : Three.js ; Babylon.js ; Cesium ; aholo-viewer (3DGS) ; PlayCanvas ; Godot (si jeu) ; Blender (pipeline) ; glTF-Transform ; gaussian splatting
- **Décision attendue** : WRAP : un moteur 3D principal + un pipeline de conversion d'assets versionné
- **Critère de succès** : Une scène de chantier (maquette + nuage + terrain) s'affiche à 30+ fps
- **Candidats vérifiés (08/10/2026)** : GuillaumeGomez/sysinfo ★2 748 [MIT] · gfx-rs/wgpu ★18 234 [Apache-2.0] · maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT]
- **⚠️ Licence** : OpenTTD/OpenTTD [GPL-2.0] : copyleft fort
- **⚠️ Licence** : graphdeco-inria/gaussian-splatting [NON-COMMERCIAL] : ⛔ à écarter
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : OpenMW/openmw [GPL-3.0] : copyleft fort
- **⚠️ Licence** : freeciv/freeciv [GPL-2.0] : copyleft fort
- **⚠️ Licence** : WorldPixelMap/android-gods-eye-view [NON-COMMERCIAL] : ⛔ à écarter
- **⚠️ Licence** : tldraw/tldraw [Licence maison tldraw (filigrane)] : ⛔ à écarter
- **⚠️ Licence** : OpenRCT2/OpenRCT2 [GPL-3.0] : copyleft fort
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, b, t, p, c, o, m, a, n, d
- **Concept art** : `art-09`

### D60 · Drone / photogrammétrie — *P1*
- **Dans le dépôt** : watchtower/index.html (55 Ko) + branche arena_01a072e1 (comparatif Cesium 21 357 ms vs MapLibre 3 ms) ; frontignan (28 fichiers, 14 Mo, deck 18 slides)
- **Existant (cadrage initial)** : matériel vidéo cité dans l'audit OSINT ; aucun pipeline
- **À auditer par ArenaAI** : Chaîne complète : plan de vol, acquisition, photogrammétrie, nuage de points, maillage, orthophoto, intégration GIS/BIM, métrologie, coûts GPU
- **Pistes d'origine à vérifier** : OpenDroneMap/WebODM (AGPL) ; COLMAP ; OpenMVS ; Meshroom (AliceVision) ; Metashape (payant) ; PDAL ; CloudCompare ; QGIS ; ODM (Docker)
- **Décision attendue** : WRAP : pipeline local reproductible (dossier photos → livrables géoréférencés) documenté pas à pas
- **Critère de succès** : Un jeu de photos de chantier produit une orthophoto et un nuage exploitables dans l'app
- **Candidats vérifiés (08/10/2026)** : GuillaumeGomez/sysinfo ★2 748 [MIT] · gfx-rs/wgpu ★18 234 [Apache-2.0] · maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT]
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : OpenDroneMap/ODM [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : xeokit/xeokit-sdk [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : CloudCompare/CloudCompare [GPL-2.0] : copyleft fort
- **⚠️ Licence** : WebODM/WebODM [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : WorldPixelMap/android-gods-eye-view [NON-COMMERCIAL] : ⛔ à écarter
- **⚠️ Licence** : IfcOpenShell/IfcOpenShell [LGPL-3.0] : copyleft faible
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **⚠️ Licence** : ThatOpen/engine_web-ifc [MPL-2.0] : fichier par fichier
- **Modules du shell concernés** : systeme, command, c, a, r, t, e, b, p, g, n, s
- **Concept art** : `art-02`

### D61 · Scan 3D / nuages de points — *P1*
- **Dans le dépôt** : branche arena_01a08449 : 22 rapports, 11 documents_sources, engine/btp_multi_agent.py ; corpus raw : 61 fichiers (43 PDF, 5 xlsm) dont DCE/CCTP/CCAP/BPU, signalisation OPPBTP, AIPR
- **Existant (cadrage initial)** : aucun ; corpus plans/essais
- **À auditer par ArenaAI** : Traitement de nuages : formats (LAS/LAZ/E57/COPC), visualisation web, mesure, comparaison de scans, détection d'écarts, segmentation
- **Pistes d'origine à vérifier** : PDAL ; Entwine ; COPC ; Potree ; THREE.js (points) ; CloudCompare ; Open3D ; laspy ; untwine
- **Décision attendue** : WRAP : visualisation web + mesures ; BUILD les cas d'usage (avancement, contrôle qualité)
- **Critère de succès** : Comparer deux scans d'un même site et visualiser l'écart en 3D
- **Candidats vérifiés (08/10/2026)** : CesiumGS/cesium ★15 811 [Apache-2.0] · visgl/deck.gl ★14 636 [MIT] · mrdoob/three.js ★116 356 [MIT] · bilawalsidhu/gods-eye-view ★49 027 [MIT] · WorldPixelMap/android-gods-eye-view ★38 [NON-COMMERCIAL] · PDAL/PDAL ★1 422 [BSD-3-Clause] · CloudCompare/CloudCompare ★4 788 [GPL-2.0] · potree/potree ★5 632 [BSD (2 ou 3 clauses)] · colmap/colmap ★12 874 [BSD-3-Clause]
- **⚠️ Licence** : CloudCompare/CloudCompare [GPL-2.0] : copyleft fort
- **⚠️ Licence** : WorldPixelMap/android-gods-eye-view [NON-COMMERCIAL] : ⛔ à écarter
- **Modules du shell concernés** : b, t, p
- **Concept art** : `art-09`

### D62 · Slicer / fabrication — *P2*
- **Dans le dépôt** : branche arena_01a08449 : 22 rapports, 11 documents_sources, engine/btp_multi_agent.py ; corpus raw : 61 fichiers (43 PDF, 5 xlsm) dont DCE/CCTP/CCAP/BPU, signalisation OPPBTP, AIPR
- **Existant (cadrage initial)** : docs/audits/external/004 (OrcaSlicer visé)
- **À auditer par ArenaAI** : Fabrication : slicers, profils machines/matériaux, G-code, impression 3D, CNC, découpe, coût matière, temps
- **Pistes d'origine à vérifier** : OrcaSlicer (AGPL) ; PrusaSlicer ; Cura ; Klipper ; FreeCAD Path/CAM ; LinuxCNC ; grbl
- **Décision attendue** : WRAP (slicer déjà excellent) ; BUILD uniquement l'orchestration (modèle → fichier prêt)
- **Critère de succès** : Du modèle à la pièce prête à imprimer sans quitter l'app
- **Candidats vérifiés (08/10/2026)** : CesiumGS/cesium ★15 811 [Apache-2.0] · visgl/deck.gl ★14 636 [MIT] · mrdoob/three.js ★116 356 [MIT] · bilawalsidhu/gods-eye-view ★49 027 [MIT] · WorldPixelMap/android-gods-eye-view ★38 [NON-COMMERCIAL] · FreeCAD/FreeCAD ★34 025 [LGPL-2.1] · openscad/openscad ★10 392 [GPL-2.0] · LinuxCNC/linuxcnc ★2 484 [GPL-2.0]
- **⚠️ Licence** : LinuxCNC/linuxcnc [GPL-2.0] : copyleft fort
- **⚠️ Licence** : WorldPixelMap/android-gods-eye-view [NON-COMMERCIAL] : ⛔ à écarter
- **⚠️ Licence** : FreeCAD/FreeCAD [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : openscad/openscad [GPL-2.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, b, t, p
- **Concept art** : `art-11`

### D63 · Métré / coût / devis / économie de la construction — *P0*
- **Dans le dépôt** : branche arena_01a08449 : 22 rapports, 11 documents_sources, engine/btp_multi_agent.py ; corpus raw : 61 fichiers (43 PDF, 5 xlsm) dont DCE/CCTP/CCAP/BPU, signalisation OPPBTP, AIPR
- **Existant (cadrage initial)** : corpus DQE/BPU/DETAIL-ESTIMATIF/Bibliothèque Prix Fournitures/fiches de tâches (fichiers XLS/PDF) ; watchtower (BOAMP)
- **À auditer par ArenaAI** : Étude de prix et métrés : extraction de quantités, bases de prix (Batiprix, index BT01, indices INSEE), décomposition prix unitaires, comparaison de devis, révision de prix, analyse de variantes, écarts DQE réel
- **Pistes d'origine à vérifier** : Batiprix (données) ; indices INSEE BT01 ; base de données de prix unitaires ; logiciels métier FR (Attic+, Estima, Onaya) ; IFC QTO (IfcOpenShell) ; Openpyxl/Pandas/Univer (tableurs)
- **Décision attendue** : BUILD : un moteur DQE/BPU (import → normalisation → quantités → prix → comparaison) sur le corpus réel
- **Critère de succès** : Un DQE importé est mis en correspondance avec un BPU et un estimatif, écarts calculés et expliqués
- **Candidats vérifiés (08/10/2026)** : duckdb/duckdb ★41 982 [MIT] · sqlite/sqlite ★10 620 [Domaine public] · apache/arrow ★17 188 [Apache-2.0] · pola-rs/polars ★40 008 [MIT] · asg017/sqlite-vec ★8 170 [Apache-2.0] · tesseract-ocr/tesseract ★76 861 [Apache-2.0] · ocrmypdf/OCRmyPDF ★34 960 [MPL-2.0] · PaddlePaddle/PaddleOCR ★90 775 [Apache-2.0] · mindee/doctr ★6 381 [Apache-2.0] · apache/tika ★4 091 [Apache-2.0] · opendatalab/MinerU ★81 295 [Apache-2.0] · docling-project/docling ★68 537 [MIT]
- **⚠️ Licence** : xeokit/xeokit-sdk [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : IfcOpenShell/IfcOpenShell [LGPL-3.0] : copyleft faible
- **⚠️ Licence** : ThatOpen/engine_web-ifc [MPL-2.0] : fichier par fichier
- **⚠️ Licence** : ocrmypdf/OCRmyPDF [MPL-2.0] : fichier par fichier
- **Modules du shell concernés** : systeme, command, b, t, p, c, o, g, n, i, d, u, m, e, s
- **Concept art** : `art-05`

### D82 · Moteur 3D desktop, modelisation et scan — *P0*
- **Dans le dépôt** : branche arena_01a08449 : 22 rapports, 11 documents_sources, engine/btp_multi_agent.py ; corpus raw : 61 fichiers (43 PDF, 5 xlsm) dont DCE/CCTP/CCAP/BPU, signalisation OPPBTP, AIPR
- **Existant (cadrage initial)** : watchtower (Cesium, bati OSM 3D) ; corpus plans ; roadmap IFC ; docs/carre-das/03-MODULE-BTP.md
- **À auditer par ArenaAI** : Visionneuses 3D performantes (IFC, glTF, nuages de points, orthophoto), noyaux parametriques embarquables, scan-to-BIM open source, photogrammetrie locale, formats et budgets memoire sur GPU 6 Go
- **Pistes d'origine à vérifier** : web-ifc / IFC.js ; xeokit ; three.js ; Babylon.js ; CesiumJS ; Potree ; COPC/LOD ; IfcOpenShell (LGPL-3.0, actif) ; PDAL ; CloudCompare (GPL) ; OpenDroneMap ; COLMAP ; Cloud2BIM (arXiv 2503.11498, 2025) ; OCCT/replicad ; FreeCAD/BIM ; Blender
- **Décision attendue** : Trancher les 3 paliers (voir / livrer / assembler / modeliser) et le mode de pilotage des outils externes
- **Critère de succès** : Un IFC, un nuage de points et une orthophoto s'ouvrent, se mesurent et s'annoter dans l'app sur la machine cible
- **Candidats vérifiés (08/10/2026)** : GuillaumeGomez/sysinfo ★2 748 [MIT] · gfx-rs/wgpu ★18 234 [Apache-2.0] · CesiumGS/cesium ★15 811 [Apache-2.0] · visgl/deck.gl ★14 636 [MIT] · mrdoob/three.js ★116 356 [MIT] · bilawalsidhu/gods-eye-view ★49 027 [MIT] · WorldPixelMap/android-gods-eye-view ★38 [NON-COMMERCIAL] · IfcOpenShell/IfcOpenShell ★2 841 [LGPL-3.0] · ThatOpen/engine_components ★710 [MIT] · ThatOpen/engine_web-ifc ★1 057 [MPL-2.0] · xeokit/xeokit-sdk ★944 [AGPL-3.0] · FreeCAD/FreeCAD ★34 025 [LGPL-2.1]
- **⚠️ Licence** : FreeCAD/FreeCAD [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : OpenDroneMap/ODM [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : xeokit/xeokit-sdk [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : CloudCompare/CloudCompare [GPL-2.0] : copyleft fort
- **⚠️ Licence** : WebODM/WebODM [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : LinuxCNC/linuxcnc [GPL-2.0] : copyleft fort
- **⚠️ Licence** : WorldPixelMap/android-gods-eye-view [NON-COMMERCIAL] : ⛔ à écarter
- **⚠️ Licence** : IfcOpenShell/IfcOpenShell [LGPL-3.0] : copyleft faible
- **⚠️ Licence** : ThatOpen/engine_web-ifc [MPL-2.0] : fichier par fichier
- **⚠️ Licence** : openscad/openscad [GPL-2.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, b, t, p
- **Concept art** : `art-06`

### D88 · Conformité & sécurité chantier (DT/DICT/AIPR, OPPBTP) — *P0*
- **Dans le dépôt** : branche arena_01a08449 : 22 rapports, 11 documents_sources, engine/btp_multi_agent.py ; corpus raw : 61 fichiers (43 PDF, 5 xlsm) dont DCE/CCTP/CCAP/BPU, signalisation OPPBTP, AIPR
- **Existant (cadrage initial)** : corpus raw : signalisation OPPBTP, AIPR ×3, pv de marquage, guide croisement réseaux, DT/DICT
- **À auditer par ArenaAI** : Automatisation des DT/DICT (déclaration de travaux) : existe-t-il des API/SDK ouverts (reseaux-et-canalisations.ineris.fr, Réseaux et Canalisations) ?
- **Pistes d'origine à vérifier** : Réseaux et Canalisations (service public FR), INERIS, référentiels OPPBTP
- **Décision attendue** : Construire le contrôle de conformité (DT/DICT, AIPR, signalisation) à partir du corpus
- **Critère de succès** : Un chantier déclaré soulève les obligations manquantes avant travaux
- **Candidats vérifiés (08/10/2026)** : aaif-goose/goose ★55 067 [Apache-2.0] · OpenHands/OpenHands ★90 275 [MIT] · openclaw/openclaw ★391 640 [MIT] · Kc1t/alethe-agents ★832 [AGPL-3.0] · modelcontextprotocol/modelcontextprotocol ★9 406 [Apache-2.0] · a2aproject/A2A ★26 073 [Apache-2.0] · agentclientprotocol/agent-client-protocol ★4 391 [Apache-2.0]
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **Modules du shell concernés** : systeme, command, b, t, p, a, g, e, n, s
- **Concept art** : `art-09`

## Simulation — 5 domaines

### D64 · Simulation Engine (systèmes) — *P0*
- **Dans le dépôt** : nexus_os : 22 agents, 30 skills, runtime/harness/evals/context/memory/providers/creator ; Kc1t/alethe-agents (★832) et openclaw/openclaw (★391 640) à comparer
- **Existant (cadrage initial)** : néant (seule 'simulation' = budget/planning chantier) ; docs/agents/simulation-agent.md
- **À auditer par ArenaAI** : Moteurs de simulation générale : événements discrets, agents, Monte Carlo, files d'attente, systèmes dynamiques, scénarios, sensibilité, propagation d'incertitude
- **Pistes d'origine à vérifier** : SimPy (DES, MIT) ; Salabim ; Mesa (ABM) ; NetLogo ; JuPedSim (foules) ; cadCAD ; PyMC (bayésien) ; Salib (sensibilité) ; SciPy ; AnyLogic (payant, référence)
- **Décision attendue** : BUILD un moteur léger unifié (scénarios + incertitude + reproductibilité) branché au Core et à la timeline
- **Critère de succès** : Un scénario (budget, délai, ressources) est simulé 1000 fois avec distribution de résultats et facteurs sensibles
- **Candidats vérifiés (08/10/2026)** : aaif-goose/goose ★55 067 [Apache-2.0] · OpenHands/OpenHands ★90 275 [MIT] · openclaw/openclaw ★391 640 [MIT] · Kc1t/alethe-agents ★832 [AGPL-3.0] · modelcontextprotocol/modelcontextprotocol ★9 406 [Apache-2.0] · a2aproject/A2A ★26 073 [Apache-2.0] · agentclientprotocol/agent-client-protocol ★4 391 [Apache-2.0] · IfcOpenShell/IfcOpenShell ★2 841 [LGPL-3.0] · ThatOpen/engine_components ★710 [MIT] · ThatOpen/engine_web-ifc ★1 057 [MPL-2.0] · xeokit/xeokit-sdk ★944 [AGPL-3.0] · FreeCAD/FreeCAD ★34 025 [LGPL-2.1]
- **⚠️ Licence** : OpenTTD/OpenTTD [GPL-2.0] : copyleft fort
- **⚠️ Licence** : FreeCAD/FreeCAD [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : xeokit/xeokit-sdk [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : OpenMW/openmw [GPL-3.0] : copyleft fort
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **⚠️ Licence** : LinuxCNC/linuxcnc [GPL-2.0] : copyleft fort
- **⚠️ Licence** : freeciv/freeciv [GPL-2.0] : copyleft fort
- **⚠️ Licence** : IfcOpenShell/IfcOpenShell [LGPL-3.0] : copyleft faible
- **⚠️ Licence** : OpenRCT2/OpenRCT2 [GPL-3.0] : copyleft fort
- **⚠️ Licence** : ThatOpen/engine_web-ifc [MPL-2.0] : fichier par fichier
- **⚠️ Licence** : openscad/openscad [GPL-2.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, b, t, p, a, g, e, n, s, c, o, m, d
- **Concept art** : `art-07`

### D65 · Physique & ingénierie — *P2*
- **Dans le dépôt** : branche arena_01a08449 : 22 rapports, 11 documents_sources, engine/btp_multi_agent.py ; corpus raw : 61 fichiers (43 PDF, 5 xlsm) dont DCE/CCTP/CCAP/BPU, signalisation OPPBTP, AIPR
- **Existant (cadrage initial)** : aucun
- **À auditer par ArenaAI** : Simulation physique utile au BTP : structure, thermique, hydraulique, acoustique, sols ; solveurs open source et leurs limites ; quand un calcul doit être sous-traité/validé par un ingénieur
- **Pistes d'origine à vérifier** : Code_Aster (EDF) ; CalculiX ; OpenFOAM ; Salome_Meca ; EnergyPlus ; OpenStudio ; Radiance ; FreeCAD FEM ; FEniCS ; Elmer ; PLAXIS (payant)
- **Décision attendue** : WRAP des solveurs validés ; BUILD seulement la préparation des données et la lecture des résultats (jamais le calcul de sécurité seul)
- **Critère de succès** : Un pré-dimensionnement simple est calculé et ses hypothèses affichées, avec avertissement explicite
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · FreeCAD/FreeCAD ★34 025 [LGPL-2.1]
- **⚠️ Licence** : LinuxCNC/linuxcnc [GPL-2.0] : copyleft fort
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : FreeCAD/FreeCAD [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : openscad/openscad [GPL-2.0] : copyleft fort
- **Modules du shell concernés** : b, t, p, c, o, m, a, n, d
- **Concept art** : `art-09`

### D66 · Réseaux & fluides — *P1*
- **Dans le dépôt** : nexus_os/plugins.py + mcp.py + mcp_demo.py (branche arena_01a08385) : 8 303 lignes Python, 22 agents, 30 compétences, 8 fichiers de tests
- **Existant (cadrage initial)** : corpus AEP/assainissement (plans, essais hydrauliques), guide ICE
- **À auditer par ArenaAI** : Réseaux : eau potable, assainissement, eaux pluviales, électricité, chauffage urbain, télécom ; modélisation, transferts, défauts
- **Pistes d'origine à vérifier** : EPANET + WNTR (eau) ; SWMM / EPA SWMM5 / canoë ; pandapower (élec) ; PyPSA ; DistrictHeating ; QGIS plugins
- **Décision attendue** : WRAP les solveurs ; BUILD l'interface données (plans + essais) → modèle
- **Critère de succès** : Un réseau d'assainissement modélisé depuis les plans du corpus produit une vérification de capacité
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · extism/extism ★5 789 [BSD-3-Clause]
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **Modules du shell concernés** : systeme, command, c, a, r, t, e
- **Concept art** : `art-02`

### D67 · Scénarios / vue stratégique / décision — *P1*
- **Dans le dépôt** : docs/recherche/02 (D64→D68) ; aucune base de code
- **Existant (cadrage initial)** : frontignan (3 scénarios 2040), watchtower (phases), CLE (situations)
- **À auditer par ArenaAI** : Aide à la décision : MCDA (AHP, ELECTRE, PROMETHEE, MACBETH), scénarios, arbres de décision, jeux sérieux, exploration d'un espace de solutions, récit
- **Pistes d'origine à vérifier** : MCDA (Python) ; pymcdm ; scikit-criteria ; Decision tree ; Exploration de Pareto ; serious games ; OpenTTD/0 A.D. comme sources de mécaniques
- **Décision attendue** : BUILD un 'Scenario Engine' commun : situation → options → conséquences → choix → trace
- **Critère de succès** : Trois scénarios territoriaux comparés avec critères pondérés et incertitudes visibles
- **Candidats vérifiés (08/10/2026)** : OpenTTD/OpenTTD ★8 345 [GPL-2.0] · OpenRCT2/OpenRCT2 ★16 397 [GPL-3.0] · OpenMW/openmw ★6 609 [GPL-3.0] · freeciv/freeciv ★1 602 [GPL-2.0] · godotengine/godot ★118 272 [MIT]
- **⚠️ Licence** : OpenTTD/OpenTTD [GPL-2.0] : copyleft fort
- **⚠️ Licence** : freeciv/freeciv [GPL-2.0] : copyleft fort
- **⚠️ Licence** : OpenRCT2/OpenRCT2 [GPL-3.0] : copyleft fort
- **⚠️ Licence** : OpenMW/openmw [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : c, o, m, a, n, d
- **Concept art** : `art-15`

### D68 · Jeu / stratégie (mécaniques) — *P1*
- **Dans le dépôt** : docs/recherche/02 (D64→D68) ; aucune base de code
- **Existant (cadrage initial)** : frontignan (vision), animation-chronos (narration), watchtower (vues stratégiques)
- **À auditer par ArenaAI** : Mécaniques de jeux de stratégie réutilisables (gestion de ressources, diplomatie, exploration, brouillard, tech tree), moteurs open source, et pièges (licences de contenu)
- **Pistes d'origine à vérifier** : OpenTTD (GPL) ; 0 A.D. (GPL) ; FreeCiv (GPL) ; OpenRCT2 ; Godot ; Minetest/Luanti ; Citybound ; Terra Nil-like
- **Décision attendue** : WRAP (extraire des idées et éventuellement le moteur), jamais copier du contenu sous licence incompatible
- **Critère de succès** : Une vue stratégique du territoire (ressources, projets, contraintes) jouable comme un jeu de simulation
- **Candidats vérifiés (08/10/2026)** : OpenTTD/OpenTTD ★8 345 [GPL-2.0] · OpenRCT2/OpenRCT2 ★16 397 [GPL-3.0] · OpenMW/openmw ★6 609 [GPL-3.0] · freeciv/freeciv ★1 602 [GPL-2.0] · godotengine/godot ★118 272 [MIT]
- **⚠️ Licence** : OpenTTD/OpenTTD [GPL-2.0] : copyleft fort
- **⚠️ Licence** : freeciv/freeciv [GPL-2.0] : copyleft fort
- **⚠️ Licence** : OpenRCT2/OpenRCT2 [GPL-3.0] : copyleft fort
- **⚠️ Licence** : OpenMW/openmw [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, c, o, m, a, n, d
- **Concept art** : `art-15`

## Plateforme — 15 domaines

### D69 · Reverse engineering & analyse logicielle — *P2*
- **Dans le dépôt** : corpus raw (43 PDF) ; docs/recherche/03 (Marker, MinerU, Docling déjà arbitrés)
- **Existant (cadrage initial)** : besoin exprimé (analyse logicielle) ; aucun outil
- **À auditer par ArenaAI** : Analyse de binaires et de logiciels : désassemblage, débogage, instrumentation, extraction de formats, compatibilité de fichiers, sécurité
- **Pistes d'origine à vérifier** : Ghidra ; Rizin ; Cutter ; x64dbg ; Frida ; JADX ; angr ; Binwalk ; Detect It Easy ; dnSpy ; Wireshark
- **Décision attendue** : ISOLER dans un module Lab séparé (sécurité + légal) ; WRAP uniquement
- **Critère de succès** : Une analyse de format/format-logiciel produite dans un environnement isolé, sans effet sur le reste
- **Candidats vérifiés (08/10/2026)** : NationalSecurityAgency/ghidra ★81 650 [Apache-2.0] · rizinorg/rizin ★3 942 [LGPL-3.0] · rizinorg/cutter ★19 942 [GPL-3.0] · x64dbg/x64dbg ★49 739 [GPL-3.0] · frida/frida ★22 146 [wxWindows-Library-Licence-3.1] · skylot/jadx ★50 780 [Apache-2.0] · angr/angr ★9 131 [BSD-2-Clause]
- **⚠️ Licence** : frida/frida [wxWindows-Library-Licence-3.1] : type LGPL
- **⚠️ Licence** : rizinorg/cutter [GPL-3.0] : copyleft fort
- **⚠️ Licence** : x64dbg/x64dbg [GPL-3.0] : copyleft fort
- **⚠️ Licence** : rizinorg/rizin [LGPL-3.0] : copyleft faible
- **Modules du shell concernés** : systeme, command, d, o, c, u, m, e, n, t, s
- **Concept art** : `art-04`

### D70 · Chaîne d'approvisionnement logicielle — *P1*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : aucun SBOM
- **À auditer par ArenaAI** : SBOM, provenance, signatures, vérification des dépendances, CI durcie, reproductibilité, gestion des secrets
- **Pistes d'origine à vérifier** : CycloneDX ; SPDX ; Syft ; Grype ; Trivy ; Sigstore/cosign ; SLSA ; osv-scanner ; Renovate ; Scorecard ; in-toto
- **Décision attendue** : BUILD une politique de dépendances (licences + CVE + provenance) appliquée automatiquement
- **Critère de succès** : Aucune dépendance ajoutée sans contrôle licence+CVE+maintenance
- **Candidats vérifiés (08/10/2026)** : PDAL/PDAL ★1 422 [BSD-3-Clause] · CloudCompare/CloudCompare ★4 788 [GPL-2.0] · potree/potree ★5 632 [BSD (2 ou 3 clauses)] · colmap/colmap ★12 874 [BSD-3-Clause]
- **⚠️ Licence** : CloudCompare/CloudCompare [GPL-2.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, b, t, p
- **Concept art** : `art-19`

### D71 · Modèle de menaces & sécurité applicative — *P0*
- **Dans le dépôt** : nexus_os/plugins.py + mcp.py + mcp_demo.py (branche arena_01a08385) : 8 303 lignes Python, 22 agents, 30 compétences, 8 fichiers de tests
- **Existant (cadrage initial)** : docs/audits/security/001-security.md
- **À auditer par ArenaAI** : Modèle de menaces complet pour une app locale manipulée par des agents : frontières, actifs, adversaires, surface (navigateur, plugins, LLM, fichiers, réseau), durcissement
- **Pistes d'origine à vérifier** : STRIDE ; LINDDUN (vie privée) ; OWASP ASVS ; OWASP LLM Top 10 ; ANSSI (guides) ; MITRE ATT&CK (pour l'OSINT) ; sandbox WASM
- **Décision attendue** : Écrire le modèle de menaces AVANT le SDK de plugins ; réviser à chaque nouveau canal (agent, plugin, réseau)
- **Critère de succès** : Un document de menaces daté + mitigations testées + journal d'audit des accès
- **Candidats vérifiés (08/10/2026)** : extism/extism ★5 789 [BSD-3-Clause] · bytecodealliance/wasmtime ★18 698 [Apache-2.0] · modelcontextprotocol/modelcontextprotocol ★9 406 [Apache-2.0] · aaif-goose/goose ★55 067 [Apache-2.0] · OpenHands/OpenHands ★90 275 [MIT] · openclaw/openclaw ★391 640 [MIT] · Kc1t/alethe-agents ★832 [AGPL-3.0] · a2aproject/A2A ★26 073 [Apache-2.0] · agentclientprotocol/agent-client-protocol ★4 391 [Apache-2.0] · ggml-org/llama.cpp ★130 687 [MIT] · ollama/ollama ★182 569 [MIT]
- **⚠️ Licence** : Kc1t/alethe-agents [AGPL-3.0] : copyleft réseau
- **Modules du shell concernés** : systeme, command, a, g, e, n, t, s
- **Concept art** : `art-03`

### D72 · Positionnement / marché / modèle économique — *P1*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : docs/constitution/08-competitors.md (à enrichir)
- **À auditer par ArenaAI** : Marché et positionnement : concurrents directs/indirects (Palantir Foundry, Esri, Autodesk, Procore, Odoo), alternatives open source, modèles (open-core, dual licensing, SaaS vertical, on-premise collectivités), prix, contraintes d'achat public (UGAP, marchés publics, code de la commande publique)
- **Pistes d'origine à vérifier** : Analyse concurrentielle ; rapports ; UGAP ; BOAMP/TED ; open-core benchmarks ; pricing pages ; Gartner/Forrester (public)
- **Décision attendue** : CONSERVER la posture 'couche qui relie' ; produire une note de marché chiffrée et un modèle de prix
- **Critère de succès** : Une note de marché de 10 pages avec 20 concurrents, 3 modèles économiques chiffrés et les contraintes d'achat public
- **Modules du shell concernés** : systeme, command, b, t, p
- **Concept art** : `art-19`

### D73 · Communauté / gouvernance / contribution — *P2*
- **Dans le dépôt** : COGNITORIUM (131 fichiers, 24 Mo), proto-cognitorium (87 Mo), HCSM (87 fichiers), ETAT-DE-LART-PSYCHOLOGIE (37 fichiers) + 137 Ko de code récupéré du patch 01a0389d, docs/carre-das/07
- **Existant (cadrage initial)** : CONTRIBUTING.md (HCSM, Watchtower), LICENSE (par dépôt)
- **À auditer par ArenaAI** : Gouvernance open source : licences compatibles à l'échelle du monorepo, CoC, RFC, processus de contribution, gestion des forks amont, CLA/DCO, réutilisation de code externe
- **Pistes d'origine à vérifier** : Choose a License ; SPDX ; REUSE spec ; DCO ; CLA Assistant ; CoC (Contributor Covenant) ; OSI ; Software Heritage (archivage)
- **Décision attendue** : Écrire la politique de licence du monorepo (matrice) AVANT toute fusion de dépôts hétérogènes (MIT, AGPL, GPL, LGPL, NOASSERTION)
- **Critère de succès** : Une matrice de licences par composant, sans ambiguïté, validée par un scénario de distribution commerciale
- **Candidats vérifiés (08/10/2026)** : adewaskar/jarvis ★412 [MIT]
- **Modules du shell concernés** : systeme, command, c, o, g, n, i, t, s, y, e, m
- **Concept art** : `art-19`

### D74 · Marketplace / extensions — *P2*
- **Dans le dépôt** : nexus_os/plugins.py + mcp.py + mcp_demo.py (branche arena_01a08385) : 8 303 lignes Python, 22 agents, 30 compétences, 8 fichiers de tests
- **Existant (cadrage initial)** : idée (discussion) ; rien dans le dépôt
- **À auditer par ArenaAI** : Écosystèmes d'extensions : découverte, installation, permissions, versions, compatibilité, sécurité (soumission), monétisation éventuelle, signature
- **Pistes d'origine à vérifier** : VS Code Marketplace ; Obsidian community plugins ; Firefox AMO ; Extism/WASM ; Tauri updater ; Open VSX ; npm registry privé
- **Décision attendue** : BUILD plus tard, mais définir dès maintenant le manifeste et les permissions (D13)
- **Critère de succès** : Un module tiers est installé, mis à jour et révoqué sans casser l'app
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1] · extism/extism ★5 789 [BSD-3-Clause]
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **⚠️ Licence** : ocrmypdf/OCRmyPDF [MPL-2.0] : fichier par fichier
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **Modules du shell concernés** : systeme, command, c, a, r, t, e, s, y, m
- **Concept art** : `art-02`

### D75 · Veille technologique continue — *P1*
- **Dans le dépôt** : reaserch-engine (61 fichiers, 301 Ko)
- **Existant (cadrage initial)** : audit/REFERENCE.md (86 outils) ; docs/audits/external
- **À auditer par ArenaAI** : Processus de veille : comment rester à jour sans se disperser ; sources de qualité, listes de suivi, évaluation périodique, dette de veille, cycles de réévaluation des ADR
- **Pistes d'origine à vérifier** : Awesome lists ; GitHub trending/OSS Insight ; Hacker News (filtré) ; Papers with Code ; Hugging Face (trending) ; LibreProjects/selfh.st ; Changelog newsletter ; deps.dev ; OpenSSF
- **Décision attendue** : BUILD un rituel (mensuel) + un registre de veille qui alimente les ADR (déclencheurs de réévaluation déjà prévus)
- **Critère de succès** : Chaque trimestre, ≤10 outils évalués et ≤3 ADR révisés, sans dispersion
- **Candidats vérifiés (08/10/2026)** : ourresearch/openalex-guts ★157 [MIT] · CrossRef/rest-api-doc ★801 [MIT (doc propriétaire)] · docling-project/docling ★68 537 [MIT] · opendatalab/MinerU ★81 295 [Apache-2.0]
- **Modules du shell concernés** : a, g, e, n, t, s
- **Concept art** : `art-03`

### D76 · Notifications & centre d'alertes — *P1*
- **Existant (cadrage initial)** : watchtower (bandeau live), aucune notifications unifiées
- **À auditer par ArenaAI** : Notifications locales : priorités, regroupement (digest), canaux (app, système, e-mail optionnel), silencing, historique, actions rapides
- **Pistes d'origine à vérifier** : ntfy ; Apprise ; Windows Toast ; Notification API ; inbox pattern ; Linear/Slack UX patterns
- **Décision attendue** : BUILD un centre de notifications unique, branché sur le bus et le monitoring
- **Critère de succès** : Une alerte critique reste visible jusqu'à action ; le reste est regroupé
- **Concept art** : `art-19`

### D77 · Design de données & qualité de données — *P1*
- **Dans le dépôt** : COGNITORIUM (131 fichiers, 24 Mo), proto-cognitorium (87 Mo), HCSM (87 fichiers), ETAT-DE-LART-PSYCHOLOGIE (37 fichiers) + 137 Ko de code récupéré du patch 01a0389d, docs/carre-das/07
- **Existant (cadrage initial)** : ETAT-DE-LART (validation), HCSM validator
- **À auditer par ArenaAI** : Qualité des données : validation de schéma, tests de données, détection de doublons/contradictions, complétude, fraîcheur, traçabilité, contrats de données
- **Pistes d'origine à vérifier** : JSON Schema/Ajv ; Pydantic ; Pandera ; Great Expectations ; Soda ; dbt (analytique) ; OpenLineage ; Deequ
- **Décision attendue** : BUILD : contrats de données par domaine + tests automatiques sur les jeux réels
- **Critère de succès** : Un dataset importé est validé, scoré et rejeté s'il ne respecte pas son contrat
- **Modules du shell concernés** : systeme, command, c, o, g, n, i, t
- **Concept art** : `art-19`

### D78 · Backups / restauration / continuité — *P1*
- **Dans le dépôt** : 9 projets + 13 branches ; _incoming 859 fichiers/31 Mo ; scripts/verif-completude-repos.py : 2 157 fichiers, 0 manquant
- **Existant (cadrage initial)** : aucun
- **À auditer par ArenaAI** : Sauvegarde locale : snapshots, versionnage de fichiers, restauration sélective, export lisible, tests de restauration, chiffrement
- **Pistes d'origine à vérifier** : Restic ; Borg ; Kopia ; git-annex ; SQLite backup API ; Litestream ; pgBackRest ; zstd
- **Décision attendue** : BUILD une stratégie simple (local + disque externe) testée, sans cloud obligatoire
- **Critère de succès** : Restaurer un projet à une date donnée, en <5 min, sans assistance
- **Candidats vérifiés (08/10/2026)** : duckdb/duckdb ★41 982 [MIT] · sqlite/sqlite ★10 620 [Domaine public] · apache/arrow ★17 188 [Apache-2.0] · pola-rs/polars ★40 008 [MIT] · asg017/sqlite-vec ★8 170 [Apache-2.0]
- **Modules du shell concernés** : systeme, command
- **Concept art** : `art-08`

### D79 · Environnement de développement reproductible — *P1*
- **Existant (cadrage initial)** : requirements.txt ; package-lock par projet ; pas d'unification
- **À auditer par ArenaAI** : Environnements reproductibles polyglottes : gestion des runtimes, versionnage, tâches, CI locale
- **Pistes d'origine à vérifier** : uv (Python) ; mise ; devbox ; flox ; Nix ; pnpm ; Turborepo/Nx ; Dagger ; Task ; Just ; act
- **Décision attendue** : BUILD un 'bootstrap' en 1 commande pour un nouveau poste ou un nouvel agent
- **Critère de succès** : Cloner + 1 commande = environnement identique, tests verts
- **Modules du shell concernés** : systeme, command
- **Concept art** : `art-07`

### D80 · Test terrain & retours utilisateurs — *P1*
- **Dans le dépôt** : branche arena_01a08449 : 22 rapports, 11 documents_sources, engine/btp_multi_agent.py ; corpus raw : 61 fichiers (43 PDF, 5 xlsm) dont DCE/CCTP/CCAP/BPU, signalisation OPPBTP, AIPR
- **Existant (cadrage initial)** : l'utilisateur est le premier utilisateur réel (BTP, commune)
- **À auditer par ArenaAI** : Boucles de retour : instrumentation respectueuse, tests d'usage, journal de friction, priorisation par usage réel, mesure d'utilité
- **Pistes d'origine à vérifier** : Umami/Plausible (analytics respectueux) ; session replay auto-hébergé (option) ; questionnaires ; NPS ; journal d'usage
- **Décision attendue** : BUILD un rituel de retour (hebdomadaire) alimenté par l'usage réel du chantier et de la commune
- **Critère de succès** : 3 décisions produit prises sur la base d'un retour terrain documenté
- **Candidats vérifiés (08/10/2026)** : getodk/central ★228 [Apache-2.0] · kobotoolbox/kpi ★185 [AGPL-3.0] · danielbrendel/hortusfox-web ★1 680 [MIT] · learningequality/kolibri ★1 136 [MIT]
- **⚠️ Licence** : kobotoolbox/kpi [AGPL-3.0] : copyleft réseau
- **Modules du shell concernés** : systeme, command, b, t, p
- **Concept art** : `art-09`

### D84 · Gouvernance associative, licence et financement — *P1*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : docs/constitution/06-budget.md ; LICENSE par depot ; cible association loi 1901 (decision utilisateur 2026-10-07)
- **À auditer par ArenaAI** : Statut associatif et logiciel libre : choix de licence (Apache/MIT vs AGPL), obligations comptables et RGPD, acces aux subventions et au mecenat, gouvernance ouverte et contribution benevole, perennite au-dela du fondateur, modes de financement des communs numeriques
- **Pistes d'origine à vérifier** : CNIL (associations, registre) ; FDVA et AAP communs numeriques ; NLnet / fonds de dotation ; modeles open-core ; chartes de gouvernance (Contributor Covenant) ; REUSE/SPDX ; guides de l'economie sociale et solidaire
- **Décision attendue** : Trancher la licence et ecrire la politique de gouvernance (qui decide quoi, comment on contribue, comment on perenne)
- **Critère de succès** : Licence choisie et matrice de licences complete ; gouvernance ecrite ; un tiers peut contribuer sans ambiguite
- **Candidats vérifiés (08/10/2026)** : maplibre/maplibre-gl-js ★11 825 [BSD-3-Clause] · maplibre/martin ★3 983 [Apache-2.0] · protomaps/PMTiles ★3 074 [BSD-3-Clause] · opengeos/GeoLibre ★7 871 [MIT] · OSGeo/gdal ★6 087 [MIT] · duckdb/duckdb-spatial ★714 [MIT] · osm-search/Nominatim ★4 512 [GPL-3.0] · Project-OSRM/osrm-backend ★8 126 [BSD-2-Clause] · valhalla/valhalla ★6 292 [MIT (à confirmer : voir COPYING)] · OSGeo/PROJ ★2 030 [MIT] · libgeos/geos ★1 513 [LGPL-2.1]
- **⚠️ Licence** : osm-search/Nominatim [GPL-3.0] : copyleft fort
- **⚠️ Licence** : libgeos/geos [LGPL-2.1] : copyleft faible
- **Modules du shell concernés** : systeme, command, c, a, r, t, e
- **Concept art** : `art-19`

### D92 · Collaboration & partage (multi-utilisateur) — *P2*
- **Existant (cadrage initial)** : aucun
- **À auditer par ArenaAI** : Partage local-first : Automerge/Yjs + serveur minimal, partage de projet par dossier, pas de compte obligatoire
- **Pistes d'origine à vérifier** : yjs/yjs (MIT), automerge/automerge (MIT), syncthing/syncthing (MPL-2.0)
- **Décision attendue** : Définir si le partage arrive en V2 (aujourd'hui : mono-utilisateur assumé)
- **Critère de succès** : Deux postes peuvent partager un dossier projet sans serveur central
- **Candidats vérifiés (08/10/2026)** : yjs/yjs ★22 910 [MIT] · automerge/automerge ★6 650 [MIT] · syncthing/syncthing ★89 219 [MPL-2.0]
- **⚠️ Licence** : syncthing/syncthing [MPL-2.0] : fichier par fichier
- **Modules du shell concernés** : systeme, command
- **Concept art** : `art-19`

### D93 · Benchmark & santé des briques (veille continue) — *P0*
- **Dans le dépôt** : prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)
- **Existant (cadrage initial)** : aucun ; docs/recherche/03 contient des mesures ponctuelles (Cesium 21 357 ms vs MapLibre 3 ms)
- **À auditer par ArenaAI** : Comment mesurer et suivre la santé d'une dépendance (activité, bus factor, issues ouvertes, temps de réponse, RAM) ? Outils : OpenSSF Scorecard, deps.dev, endoflife.date
- **Pistes d'origine à vérifier** : ossf/scorecard, deps.dev API, libs.io, OpenHub
- **Décision attendue** : Automatiser une fiche de santé par dépendance, rejouée à chaque montée de version
- **Critère de succès** : Toute dépendance a une fiche santé datée et un plan de remplacement
- **Modules du shell concernés** : systeme, command, a, g, e, n, t, s
- **Concept art** : `art-19`

