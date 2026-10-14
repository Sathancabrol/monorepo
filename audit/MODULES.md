# MODULES — Registre exhaustif des modules (3ᵉ passe, 2026-10-07 15:20 UTC)

> **Déclencheur** : « vérifie l'intégralité des modules, t'as raté des trucs » → vérification faite **au niveau module** (pas dépôt, pas branche) sur l'état **live à 15:20 UTC**.
> **Méthode** : re-scan des 9 dépôts + 46 branches + `_incoming` (859 fichiers) + les **commits de 14:54, 15:03 et 15:06** (postérieurs aux deux passes précédentes), lecture du shell, de l'inventaire de features et du dashboard BTP.
> Compléments : `audit/notes/S5-controle-completude.md` (2ᵉ passe) · `audit/SYNTHESE-TIMELINE-2026-10.md`.

---

## 0. Ce qui a encore été raté (3ᵉ passe) — et qui est corrigé ici

| # | Élément raté | Preuve / état live |
|---|---|---|
| 1 | **`shell/` — le squelette UX/UI Carré d'As** (commit `0ce2ddbb`, 15:06) : 11 fichiers, **14 modules / 104 fonctionnalités** navigables, assistant JARVIS, sons, design system | `shell/index.html`, `shell/data/modules.json` (949 l.), `shell/assets/{shell,registry,assistant,sounds}.js`, `shell/tools/{gen-registry,check-sources}.py` |
| 2 | **Le portail d'accès** `index-acces.html` (commit `85e423c2`, 15:06) | racine de la branche |
| 3 | **`docs/FEATURES-INVENTORY.md`** (commit `dde1e2af`, 15:03) : l'inventaire complet des features de **tous les modules et apps** | branche `arena/93b54a79` |
| 4 | **Le module BTP a été restructuré** (force-push entre mes deux scans) : il est passé de 239 fichiers à **2 HTML + ~83 scripts** ; les 154 documents ne sont plus dupliqués dans le module (ils restent à la racine du monorepo et dans `_incoming`) | compare `main...arena/01a08449` = **ahead=1, 83 fichiers** |
| 5 | **Les 21 onglets-modules du dashboard BTP** : cockpit, company, dépôt, projects_hub, planning, simulateur, flotte, catalogue, RH, OPPBTP, sécurité, RDC, compagnon mobile, obsidian, schémas, SDP, benchmark, procurement, ledger, docs, archives | `projects/btp-conduite-travaux/index.html` (1,2 Mo) |
| 6 | **137 Ko de code ETAT récupérés d'un patch jamais appliqué** : `bias_cards.py` (239 l.), `concept_details.py` (495), `experiment_templates.py` (77), `lab_endpoints.py` (75), `scientific_articles.py` (257) | `_incoming/ETAT-DE-LART-PSYCHOLOGIE/arena_01a04f7b-.../app/` |
| 7 | **`_incoming` = 859 fichiers** (et non 786 — le chiffre de 786 nettoie les doublons, le brut importé est 1 026 ; mes deux passes parlaient de périmètres différents) | 16 `_PROVENANCE.md` confirmés |
| 8 | **Nouveaux commits** : `0034230e` (+2 : shell, portail) · `93b54a79` (+1 : features-inventory) · `01a08449` (+1 : HUD 21 modules) | live 15:20 |

---

## 1. LA CIBLE — le shell Carré d'As : 14 modules, 104 fonctionnalités

**Fichier source de vérité** : `shell/data/modules.json` (v0.2.0, 07/10/2026) — régénérable par `shell/tools/gen-registry.py` ; contrôles : `shell/tools/check-sources.py` (**104/104 fonctionnalités adossées à une source réelle**), `scripts/verif-completude-repos.py`.

| # | Module | Fonctions | Ce que ça couvre (extrait) | Palier dominant |
|---|---|---:|---|---|
| 1 | **Command Center** | 7 | 4 portes, palette Ctrl+K, reprise de session, barre d'état, alertes, registre 12 catégories, mode présentation | V1 |
| 2 | **Projets & chantiers** | 6 | fiche projet, onglets contexte, détails+provenance, journal d'activité, multi-projets, pièces jointes | V1 |
| 3 | **Documents** | 7 | corpus BTP indexé, recherche plein texte + sémantique, extraction structurée, rangement auto, CV ciblé, import CV → profil, pièces justificatives | V1 |
| 4 | **Carte & territoire** | 8 | carte 2D MapLibre, bascule 2D/3D, atlas, barre 24 fonctions, grille de vérité ✅📅🔮⚠️, données ouvertes, itinéraires hors ligne, fond « prepper » | V1→V2 |
| 5 | **BTP — conduite de travaux** | 11 | DCE/marchés, étude de prix & sous-détails, métrés, suivi, sécurité/AIPR, réseaux secs, géotechnique, non-conformités, moteur multi-agents, bâti 3D, RH/formation | V1→V2 |
| 6 | **Cognition & profil** | 8 | tableau de bord cognitif, decay, biais (6 fiches), métacognition, HCSM, protocoles, évaluations, atlas psy | V1.5→V2 |
| 7 | **Graphe & arbre** | 9 | constellation, arbre de compétences, graphe temporel, vue métiers, tableau, **vue liste accessible**, zoom sémantique 5 niveaux, statut épistémique, inspecteur | V1→V1.5 |
| 8 | **Métiers & passerelles** | 6 | matching explicable, ROME, formations, passerelles, scores, trajectoire avec incertitude | V1→V2 |
| 9 | **Agents & automatisation** | 9 | **NEXUS·OS 22 agents**, 8 fournisseurs/20 modèles, 22 outils sandboxés, **MCP**, 147 tests, recherche sourcée, veille OSINT, agent scientifique, garde-fous | V1.5→V2 |
| 10 | **Référentiels & fiches** | 7 | module Fiches, état de l'art psy, base 42 champs, fiches biais illustrées, bibliothèque hors ligne (Kiwix/ZIM), ateliers & labo, sources | V1→V2 |
| 11 | **Apprentissage** | 4 | parcours « Comprendre l'argent », graphe conceptuel, retour explicatif, Kolibri hors ligne | V2 |
| 12 | **Langage & notes** | 5 | décodeur de langage, mémoire multi-IA, ontologie, dashboard, transcription Whisper locale | V1.5→V2 |
| 13 | **Assistant JARVIS** | 7 | orbe 4 états, voix entrée/sortie, guidage, sons, IA locale Ollama optionnelle, contrôle total | V1 |
| 14 | **Système & modules** | 10 | comptes, sync multi-comptes, modules à chaud, contrats de données, màj signées + rollback, licence/monétisation, gouvernance, audit qualité, accessibilité, réglages | V1→V1.5 |

**Totaux vérifiés** : **104 fonctions** → **62 disponibles · 24 à porter depuis les branches · 18 à construire** ; paliers **V1 = 48 · V1.5 = 34 · V2 = 22**. **8 portes** de navigation : Accueil, Projets, Documents, Carte, Agents, Explorer, Assistant, Système.

**Le shell lui-même** : 11 fichiers, **zéro dépendance** ; design system repris du prototype d'origine retrouvé dans `proto-cognitorium/raw/noeud neurono.html` (Void `#050508`, Plasticity `#00E5CC`, Transfer `#9B59B6`, Alert `#FF3366`, Inter + JetBrains Mono) ; assistant (orbe CSS, parole, écoute si Chrome/Edge, Ollama optionnel avec mode dégradé explicite) ; sons synthétisés Web Audio (9 gestes) + pack optionnel **uisfx** (CC0) ; accessibilité (clavier 100 %, densités, contraste, mouvement réduit, vue liste accessible).

---

## 2. Registre des modules par source (état live)

### 2.1 Sources principales

| Source | Modules / briques | Chiffres vérifiés | Statut |
|---|---|---|---|
| **`shell/`** (branche `0034230e`) | 14 modules / 104 fonctions, assistant, sons, design system, 2 outils | 11 fichiers | **squelette FAIT** (à habiller) |
| **`app/`** (monorepo `main`) | accueil, `/repos` (cartes + graphe D3), `/monorepo` (explorateur + previews), API GitHub/FS/manifest, `/preview`, bundle | pages + 10 routes | actif |
| **`projects/watchtower`** | 13 couches temps réel (avions 11 000+, navires, satellites 838+, séismes, trafic, ~800 CCTV, radio ~750 stations, vélos, feux, lancements, barrages, militaire), cockpit, hangar 3D, HUD, skins GLSL, vues territoire, épingles, **watchtower-mods** (palais mental, veille auto, comptes/niveaux, `/aide` 16 commandes, `/urgence`, dispositifs), gouverneur de quotas, proxy anti-SSRF | 583 f., 190 453 l., 208 tests, **~40 scripts QA** Puppeteer, ~86 outils au registre | alpha |
| **`projects/btp-conduite-travaux`** (branche `01a08449`, **réécrite**) | **21 onglets-modules** (liste §0.5) + **~83 scripts** (build/patch v47→v53, générateurs, illustrations, obsidian, rapports) + 2 HTML | 83 fichiers en diff | prototype avancé |
| — historique du même module (préservé dans `_incoming`, branche `0034230e`) | 154 documents (7 familles, 3 chantiers), 9 rapports (00→08), data SHA-256 + 28 sous-détails de prix, `engine/btp_multi_agent.py` | 112 fichiers importés | conservé |
| **`projects/proto-cognitorium`** | pipeline complet : onboarding → CV → extraction IA → propositions → validation → graphe → ROME → métiers → passerelles ; **1 911 fiches ROME, 17 920 compétences**, FORMACODE ; échelle épistémique 5 niveaux ; UI 5 sections (HorizonsBridge, prochaine étape, preuves) ; composants récupérés (GuidedSequence, ObsidianGraph, TargetedCv, MultiProjects, Volant…) | 184 f. distants, 111 src | le plus avancé (0 test) |
| **`projects/COGNITORIUM`** | learning/ (CLE + PoC « Comprendre l'argent » 9 niveaux + graphe conceptuel), watchtower-mods FR, constitution (10 docs), état des lieux (9 fiches), 7 audits, 13 fiches agents | 131 f. | gouvernance + PoC |
| **`projects/ETAT-DE-LART-PSYCHOLOGIE`** | API : `/api/nodes`, `/{id}`, `stats`, `timeline`, `pyramid`, `concepts-4e`, `metacognitive-traces` (GET/POST), `obsidian-graph`, `taxonomy` ; visualisations D3 ; scripts d'ajout/validation ; **+ 5 modules du patch** (bias_cards, concept_details, experiment_templates, lab_endpoints, scientific_articles — 137 Ko) | 37 + branche 300 f. | actif |
| **`projects/HCSM`** | model/ (latent-state, mathematical, temporal, uncertainty), ontology/ (hcsm-v0.1.yaml + entités/relations/namespaces), validator/ (V1 forme + V5 admissibilité + Refusal, 23 cas, 29 tests) | 87 f., 1 917 l. | M2 épinglé |
| **`projects/reaserch-engine`** | pipeline question→plan→stratégie→agents→preuves/claims→contradictions→synthèse→vérification→suffisance ; EvidenceGraph ; JsonRunStore ; CrossrefRetriever + LocalFirstRetriever | 61 f., 21 modules, 12 tests (**2 rouges**) | v0.1 |
| **`projects/animation-chronos`** | 9 composants (VesselStage, InspectionLens, TransitionSequenceBar, ProgressiveDiscoveryBar, MonographDrawer, ObservationControls, ChronosBubble, CosmicBackground, FullScreenFluidCanvas) | 30 f. | M2 |
| **`projects/frontignan`** | rapport 826 l. (249 sources), deck 18 slides, 14 figures, vision 2040 ; scripts `make_deck`, `make_figures`, `make_figures_vision`, `make_html` | 28 + atlas 21 f. | livrable |
| **`projects/Language-decoder`** (branches) | package : ontology, decoder, inference, dynamics, functioning, profile, evidence + CLI + schéma `decoded-human` ; UI dashboard, mémoire multi-IA, monde 2040 | 24 + 27 f. | branches |
| **`nexus_os`** (branche `01a08385`) | **22 agents**, routeur **8 fournisseurs / 20 modèles** + fallback, 22 outils sandboxés, serveur **MCP**, mémoire, runs/SSE, pipelines, evals, instincts, créateur d'agents | 85 f., **147 tests** | branche |
| **`projects/mail-organizer`** (branche `93b54a79`) | CLI 5 commandes (check/plan/organize/attachments/watch), moteur de règles JSON, non destructif, UTF-7, 19 tests | 15 f. | neuf |
| **`audit/`** (branche `171a1f38`) | 5 scripts rejouables (memory, inventory, s0_map, gh_drift, importance), 16 notes, 91 éléments classés, mémoire machine | 40 f. | livré (PR #3) |

### 2.2 Modules de service et d'intégration (souvent oubliés)

| Module | Rôle | Source |
|---|---|---|
| `scripts/github_inventory.py` | inventaire GitHub (stdlib, pagination, rate-limit) → snapshot cache serveur | monorepo `main` |
| `scripts/publish_monorepo.sh` | rebuild des 3 previews Vite + commit/push | monorepo `main` |
| `scripts/verif-completude-repos.py` | contrôle de complétude dépôts+branches par empreinte Git | branche `0034230e` |
| `shell/tools/check-sources.py` | vérifie que les 104 fonctionnalités ont une source réelle | branche `0034230e` |
| `shell/tools/gen-registry.py` | régénère `modules.json` + `registry.js` | branche `0034230e` |
| `app/main.py` (routes preview/API) | coquille FastAPI : explorateur, iframes, garde-fous | monorepo `main` |
| ~40 `qa-*.mjs` + `track-regression.mjs` | QA Puppeteer watchtower (trafic, voix, CCTV, labels, perf) | watchtower |
| 83 scripts BTP | générateurs/patchs (v47→v53) du dashboard BTP | branche `01a08449` |

### 2.3 `_incoming` — 16 lots importés (859 fichiers, `_PROVENANCE.md` chacun)

ETAT `01a04f7b` (244) · watchtower `01a072e1` (145) · BTP `01a08449` (112) · nexus `01a08385` (94) · watchtower `dec9cd88` (54) · **audit `171a1f38` (38)** · Language-decoder `01a05429` (28) · ETAT `01a045a1` (25) · Language-decoder `01a05471` (25) · atlas `01a08203` (23) · proto `01a08342` (15) · OSINT `watchtower_osint-workbench` (13) · ETAT `01a07d32` (12) · catalogue `feat_tool-data-catalog` (12) · ETAT `01a03aac` (11) · interface `feat_final-interface-skeleton` (8).

---

## 3. Les taxonomies qui cohabitent — et le mapping

| Système | Origine | Découpage | Usage |
|---|---|---|---|
| **Phases 0→7** | `COGNITORIUM/constitution/04-roadmap.md` (05/09) | Core, Skill+CLE, World, Design, CAD, Fabrication, Agents | la trajectoire d'origine |
| **12 domaines** | `data/interface_registry.json` (branche `feat/final-interface-skeleton`, 07/10 matin) | Command, World, Intel, Projects, Human, Knowledge, Learning, Simulation, Creation, Agents, Memory, System | catalogue de couverture par sources |
| **14 modules / 8 portes** | `shell/data/modules.json` (branche `0034230e`, 07/10 15:06) | Command, Projets, Documents, Carte, BTP, Cognition, Graphe, Métiers, Agents, Référentiels, Apprentissage, Langage, Assistant, Système | **le squelette de l'app** (le plus récent, avec statuts et paliers) |
| **v1→v5 + v0** | `audit/ANALYSE-V1-V5.md` (cet audit) | vagues d'intégration | ordonnancement du désordre |

**Mapping rapide** : World → *Carte & territoire* · Intel + Knowledge + Memory → *Documents/Référentiels/Agents* · Human → *Cognition & profil* · Learning → *Apprentissage* · Simulation → *Graphe* (à confirmer) · Creation → *(absent du shell : cohérent, c'est v4/v5)* · Nexus/Agents → *Agents & automatisation* · System → *Système & modules* ; le shell ajoute **Documents, BTP, Métiers, Langage, Assistant** que la grille de 12 ne séparait pas.

**Recommandation de canonisation** : le **shell (14 modules / 8 portes)** devient la taxonomie produit ; les **12 domaines** restent la grille de couverture (sources) ; **v1→v5** reste l'ordonnanceur ; les **phases 0-7** restent la trajectoire. Une seule table de correspondance (ci-dessus) à maintenir, pas quatre vocabulaires dans les livrables.

---

## 4. Flux constaté (le projet bouge en heures, pas en jours)

| Heure (UTC) | Commit | Apport |
|---|---|---|
| 12:38 | `4588c5c8` | brief de recherche + matrice 80 domaines |
| 13:05 | `df130862` | cadrage Carré d'As + contrat module + UI + BTP |
| 14:23 | `ea1e87e9` | 3 interfaces cliquables + réponses + écosystème local |
| 14:38 | `0559e1e5` | `_incoming` (1 026 fichier / 786 uniques) + verif-completude |
| 14:39 | `bc95401d` | resync proto (12 f.) + frontignan |
| 14:45 | `2f09e8a9` | mail-organizer (19 tests) |
| 14:54 | `1b7627b0` | HUD BTP 21 modules (force-push de la branche : 239→83 fichiers) |
| 15:03 | `dde1e2af` | `FEATURES-INVENTORY.md` (tous les modules/apps) |
| 15:06 | `0ce2ddbb` | **shell Carré d'As : 14 modules / 104 fonctions** |
| 15:06 | `85e423c2` | portail `index-acces.html` |

**Conséquence** : tout livrable d'audit doit porter **l'heure de son relevé** (déjà en place dans `audit/JOURNAL.jsonl`) et être **rafraîchi avant toute fusion**.

---

## 5. Compteurs live (15:20 UTC, 2026-10-07)

| Indicateur | Valeur |
|---|---|
| Dépôts | 9 (aucun fork déclaré, tous publics) |
| Branches | **46** : 9 `main` + **18 actives** + 19 mortes |
| Commits non fusionnés | **167** (dont 6 = audit) |
| `_incoming` | 859 fichiers · 16 provenances |
| Shell Carré d'As | 14 modules · 104 fonctions (62/24/18) |
| BTP (live) | 21 onglets · ~83 scripts · 2 HTML |
| Modules recensés dans ce registre | **~60 modules/briques nommés** (§2) |

---

## 6. Prochaine étape

1. **Fusionner dans l'ordre** : `0034230e` (Carré d'As + shell + `_incoming` + resync proto) → `93b54a79` (mail-organizer) → `01a08449` (BTP 21 modules) → PR #3 (watchtower INTEL) → `feat/final-interface-skeleton` + `feat/tool-data-catalog` → branches ETAT/Language-decoder.
2. **Trancher la taxonomie canonique** (§3) : shell = produit ; 12 domaines = couverture.
3. **Brancher le premier module réel** dans `#slot-btp` (les 154 documents du corpus, depuis la racine — plus de copie).
4. Rafraîchir ce registre **avant chaque fusion** (le projet produit un lot toutes les 20 minutes).
