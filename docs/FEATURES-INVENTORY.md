# 📋 Inventaire des features — modules & apps du monorepo

> Généré le 7 octobre 2026 · branche `arena/93b54a79-monorepo`
> Objectif : cartographie complète des fonctionnalités de chaque module, avec un focus sur les features d'automatisation « à la mail-organizer » (CLI, règles, watch, scripts utilitaires, QA bots, APIs).

---

## 🧭 Vue d'ensemble

| Module | Type | Stack | Statut |
|---|---|---|---|
| `app/` | Interface unifiée | FastAPI + Jinja | ✅ actif |
| `scripts/github_inventory.py` | CLI inventaire GitHub | Python stdlib | ✅ actif |
| `projects/mail-organizer` | CLI tri de mails | Python stdlib (IMAP) | ✅ nouveau (07/10/2026) |
| `projects/watchtower` | Console OSINT globe 3D | Cesium + JS vanilla + Vite | ✅ build prêt |
| `projects/proto-cognitorium` | Proto orientation métiers | React + Express + Gemini | ✅ build prêt |
| `projects/COGNITORIUM` | Visualisation cognitive | JS vanilla statique | ✅ PoC |
| `projects/ETAT-DE-LART-PSYCHOLOGIE` | Base État de l'art | FastAPI + SQLite | ✅ actif |
| `projects/HCSM` | Modèle scientifique | Markdown + YAML + Python | 🟡 PROPOSED |
| `projects/reaserch-engine` | Moteur de recherche autonome | Python | ✅ v0.1 + tests |
| `projects/animation-chronos` | Visualisation artistique 3D | React + Gemini API | ✅ build prêt |
| `projects/frontignan` | Analyse territoriale | HTML/MD + scripts Python | ✅ livrable |
| `projects/Language-decoder` | — | — | ⬜ quasi vide |

---

## 1. `app/` — Interface unifiée (FastAPI)

**Pages**
- `/` — accueil · `/repos` — panorama GitHub (cartes, graphe de fusion D3, drawer) · `/monorepo` — explorateur + previews iframe (drawer, fil d'Ariane, filtre, viewer Markdown/syntaxe/PDF) · `/health`

**API**
- `GET /api/github/snapshot|repos|fusion` · `POST /api/github/refresh` (régénère le snapshot côté serveur, token jamais exposé)
- `GET /api/fs/list` + `/api/fs/file` (exploration fichiers, traversal `../..` bloqué 400)
- `GET /api/manifest` (provenance des repos) · `GET /download/monorepo.bundle`

**Preview**
- `GET /preview/{project}/{path}` — FileResponse même origine, entrées auto par projet (`dist/index.html`, `learning/index.html`, `output/visual/*.html`…), sans en-têtes anti-iframe.

## 2. `scripts/github_inventory.py` — CLI inventaire (stdlib)

- Fetch GitHub API paginé + gestion rate-limit (headers `X-RateLimit-Remaining`)
- Détection des modules locaux (`package.json`, `pyproject.toml`…), langage/stack auto
- Snapshot JSON `data/github_inventory.json` servant de cache serveur (62 appels max)

## 3. `projects/mail-organizer` — Tri automatique de boîte mail 🆕

- **CLI** : `check` / `plan` / `organize` / `attachments` / `watch` (0 dépendance, IMAP)
- **Moteur de règles** configurable (JSON) : domaines, expéditeurs, sujets, présence d'en-têtes (`List-Unsubscribe` = filet newsletters) ; comparaison insensible aux accents ; première règle gagnante
- **Classement non destructif** : COPY + retrait du dossier source, jamais de suppression ; création auto des dossiers (UTF-7 modifié RFC 3501)
- **plan** = dry-run + statistiques des domaines pour découvrir de nouvelles règles
- **attachments** = téléchargement daté des pièces jointes par dossier
- **watch** = boucle continue (compatible cron) — Gmail & Outlook/Hotmail via mot de passe d'application
- 19 tests unitaires ✅

## 4. `projects/watchtower` — Console de renseignement temps réel (globe 3D)

**Couches de données temps réel**
- ✈️ Avions (OpenSky + adsb.lol, 11 000+ appareils) + vols militaires · 🚢 Navires (AISStream) · 🛰 Satellites (CelesTrak, 838 objets + coquille Starlink, propagation SGP4) · 🌍 Séismes (USGS 24 h) · 🚦 Trafic (TomTom/OSM) · 📹 ~800 caméras CCTV (Austin, Caltrans, Londres TfL) projetées en 3D · 📻 Radio géolocalisée (tuner analogique, ~750 stations) · 🚲 Vélos en libre-service (GBFS) · 🔥 Feux actifs (NASA FIRMS / EONET sans clé) · 🚀 Lancements spatiaux 30 j (Launch Library 2) · 🏗 Barrages · 🎖 Installations militaires (OSM)

**Interactions**
- Contrôle vocal : OpenAI Realtime OU **voix navigateur FR/EN sans clé** (« va à Paris », « montre les avions »…) ; whiteboard vocal (annotations géographiques)
- Vue cockpit embarquée, click-to-track avec traînées, hangar 3D par classe d'appareil, Q&A entités avec contexte de scène, cadrage cinématique
- HUD militaire, overlay de détection (bounding boxes), skins capteurs GLSL (CRT, NVG, FLIR, Noir, Snow), directeur de scène, liens de partage sérialisés
- Vues du territoire : communale (tracé animé + couche AR d'équipements), quartier (3D rasante), immersion, orbite, heatzones ; épingles persistantes ; minicarte canvas ; bâti 3D rapide (2 draw-calls, worker, hauteurs estimées OSM/cadastre)

**Modes maison (watchtower-mods)**
- 🧠 Palais mental (dossier/outils interactifs) · veille auto (HUD masqué après 15 s) · comptes & niveaux (clés en localStorage) · chat `/aide` (16 commandes) · mode `/urgence` (procédures, secours, itinéraire, mascotte) · dispositifs (caméras/mics/capteurs) · cadrans découpés au tracé communal

**Ingénierie**
- Gouverneur de quotas (OpenSky, TomTom, cache TLE), proxy serveur durci anti-SSRF, datum vertical géoïde, interpolation + dead reckoning des flux
- Fork « tout gratuit » : globe Esri, tuiles CARTO Voyager, géocodage Photon/Nominatim, feux EONET

**Outillage**
- `npm run doctor` (diagnostic), install Pinokio en un clic, `opensky:import`
- **~40 scripts QA Puppeteer** (`qa-*.mjs`) : trafic, voix, câbles, CCTV, labels, perf, floor-hold, routes cinématiques…
- Tests unitaires + `track-regression.mjs` + fixtures
- `tools/` : rendu Cesium headless, streetview panorama/headings, sat-ortho, pano-pinhole

## 5. `projects/proto-cognitorium` — Prototype d'orientation professionnelle

- **Pipeline complet** : Onboarding → CV/parcours → Extraction IA (Gemini) → Propositions → Validation humaine → Graphe cognitif → Référentiel ROME → Métiers compatibles → « Pourquoi ? / Il manque quoi ? » → Passerelle formation → Prochaine action
- `scripts/build_rome_data.py` : génération des données ROME officielles France Travail → **1 911 fiches métiers, 17 920 compétences, mapping FORMACODE**
- Moteur de matching ROME explicable (index par jeton, cache par profil, ~327 ms pour 1 911 fiches) + recherche libre
- **Échelle épistémique à 5 niveaux** (fait → compétence → capacité → hypothèse → conclusion) + garde-fous (« pas de conclusion psychologique », IA *propose* en statut pending)
- API Gemini (`server.ts`) : `POST /api/distill-experience` · `/api/explore-horizons` · `/api/synthesize-profile`
- UI : 5 sections de représentation, HorizonsBridge, « prochaine étape » calculée, preuves structurées (Source/Mission/Résultat/Contexte/Validation)

## 6. `projects/COGNITORIUM` — Outils de visualisation cognitive

- **Learning Engine PoC v0.1** (architecture CLE : Scenario/Challenge/Cognitive/Skill Graph Engine + boucle adaptative)
- PoC « Comprendre l'argent » : parcours 9 niveaux (broc → monnaie → … → investissement), situations concrètes, conséquences explicatives, graphe conceptuel dynamique, question de transfert, événements de session en local
- `watchtower-mods/` : modules FR injectés dans watchtower (voir §4) + docs d'application (`APPLIQUER.md`, `SOURCES-FR.md`)
- Documentation riche : constitution, audits, architecture cible, registre de décisions

## 7. `projects/ETAT-DE-LART-PSYCHOLOGIE` — État de l'art (FastAPI + base)

- **API** : `/api/nodes` (recherche + filtres domaine), `/api/nodes/{id}`, `/api/stats`, `/api/timeline`, `/api/pyramid`, `/api/concepts-4e`, `/api/metacognitive-traces` (GET + POST), `/api/obsidian-graph`, `/api/taxonomy`
- Visualisations : `output/visual/` (index, D3 interactif, graphe de taxonomie)
- Scripts : `add_entry.py` (ajout d'entrée), `validate_entry.py` (validation)

## 8. `projects/HCSM` — Human Cognitive State Model (v0.1.1, PROPOSED)

- **model/** : latent-state, mathematical, temporal, uncertainty
- **ontology/** : `hcsm-v0.1.yaml` + entités, relations, namespaces
- **validator/** : CLI de validation JSON — V1 forme (vs ontologie + data-schema) et V5 admissibilité (inférence autorisée ou `Refusal`) ; cas de tests inclus
- Intégration revendiquée : RDoC, ICF, Cognitive Atlas, HPO, psychométrie, digital phenotyping

## 9. `projects/reaserch-engine` — Moteur de recherche autonome (v0.1)

- Pipeline : analyse de question → planification → **stratégie adaptative** → agents/outils → preuves + claims → **analyse de contradictions** → synthèse → vérification → **gates de suffisance** → dossier final
- **EvidenceGraph** : Source → Evidence → supports/contradicts → Claim ; conflits qualifiés ; snapshot JSON inspectable
- **JsonRunStore** : checkpoints atomiques de runs (reprise après interruption, sans BDD)
- Retrieval injectable : `CrossrefRetriever` (DOI) + `LocalFirstRetriever` (local d'abord) ; modèle de qualité des sources
- Tests inclus

## 10. `projects/animation-chronos` — « Ferrofluid Consciousness Vessel »

- Visualisation scientifique-artistique 3D photoréaliste (vaisseau ovoïde, ferrofluide en microgravité près d'un horizon des événements)
- React + Vite + Motion, générée via **Gemini API** (capacité server-side)

## 11. `projects/frontignan` — Analyse territoriale Frontignan 2026-2040

- Rapport MD/HTML + deck (`index.html`) + figures
- Scripts de génération : `make_deck.py`, `make_figures.py`, `make_figures_vision.py`, `make_html.py`

## 12. `projects/Language-decoder`

- README seul, projet quasi vide (candidat à suppression ou redémarrage).

---

## 🔁 Features transverses « à la mail-organizer » (automatisation & utilitaires)

| Pattern | Où ? |
|---|---|
| **CLI Python stdlib** | `mail-organizer`, `scripts/github_inventory.py`, `HCSM/validator/validate.py`, `ETAT/scripts/{add_entry,validate_entry}.py`, `frontignan/scripts/make_*.py`, `proto-cognitorium/scripts/build_rome_data.py` |
| **Moteurs de règles** | `mail-organizer` (règles JSON), `proto-cognitorium` (matching ROME + épistémique), `reaserch-engine` (sufficiency gates + stratégie adaptative) |
| **Watch / boucles** | `mail-organizer watch` ; watchtower (rafraîchissement flux + gouverneur de quotas) |
| **Zéro dépendance** | `mail-organizer`, `github_inventory.py`, `COGNITORIUM/learning`, watchtower (JS vanilla) |
| **Dry-run / plan** | `mail-organizer plan`, watchtower QA probes |
| **QA bots & tests auto** | watchtower (~40 scripts Puppeteer + regression tracking), mail-organizer (19 tests), reaserch-engine, HCSM validator |
| **APIs serveur** | `app/` (FastAPI), ETAT (FastAPI), proto-cognitorium (Express), watchtower (proxys sécurisés) |
| **Snapshot / cache** | `data/github_inventory.json`, watchtower (TLE, budgets de tuiles) |

## 💡 Lacunes détectées (features candidates « style mail-organizer »)

1. **Pas de lanceur unifié** — un `scripts/check_all.py` (ou Makefile) lançant tous les tests de tous les modules d'un coup.
2. **Pas de health-check des sources** — watchtower dépend de dizaines de flux ; un watcher « sources OK/KO » avec rapport serait utile.
3. **Pas d'index des features exposé** — `app/` pourrait servir `/api/modules` listant automatiquement les features de chaque module (ce document en serait la source).
4. **ETAT-DE-LART** : pas d'import automatique de nouvelles entrées (only `add_entry.py` manuel).
5. **Language-decoder** : vide — soit le démarrer, soit le retirer de l'inventaire.
6. **Notifications** — aucun module ne pousse d'alertes (mail-organizer pourrait notifier les messages importants classés en « Administratif et factures »).
