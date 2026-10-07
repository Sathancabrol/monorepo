# Audit de capacités — 7 octobre 2026

**Prochaine action** — fusionner les 4 branches à fort contenu avant qu'elles ne pourrissent :
`watchtower/arena/01a072e1` (+42 commits, 145 fichiers), `ETAT-DE-LART/arena/01a04f7b` (+38,
300 fichiers), `monorepo/arena/01a08449` (+24, 252 fichiers),
`COGNITORIUM/watchtower/osint-workbench-v0.1` (+13, 12 fichiers).

**État en un chiffre** : **144 commits non fusionnés**, répartis sur **14 branches** de travail
— sur 32 branches hors `main`, 41 au total, pour 9 dépôts. Tout le reste de cet audit découle de là.

---

## 1. Ce qui fonctionne déjà, vérifié à l'instant

Serveur : `uvicorn app.main:app --host 0.0.0.0 --port 8123` (process
`monorepo-nexus-os-c35fef7f`), plus NEXUS·OS seul sur 8124.

| Ce qu'on peut faire | Preuve (mesurée ce jour) |
|---|---|
| Ouvrir les 4 pages du monorepo | `/`, `/repos`, `/monorepo`, `/os/` → **4 × 200** |
| Prévisualiser les **9 projets** dans le navigateur | `/preview/{projet}` → **9 × 200** |
| Utiliser NEXUS·OS monté dans le monorepo | `/os/api/status` → 200 (10 agents, 14 compétences) |
| Lire l'inventaire GitHub | `/api/manifest`, `/api/github/snapshot` → 200 |
| **Régénérer l'inventaire** depuis l'API GitHub | `POST /api/github/refresh` → `ok: true`, 28 appels API, 9 dépôts, horodaté `2026-10-07T05:42:19Z` |
| Lancer une tâche d'agent en streaming | SSE `/api/run` → 19 événements, statut `done`, artefact `workspace/compositions/*.html` |
| Créer un agent à la volée | `POST /api/agents/create` → spec complète enregistrée |
| Reconstruire les apps Vite | registry npm joignable (`npm view vite version` → `8.3.3`), `node v22.22.3`, `npm 10.9.8` |
| S'appuyer sur du code testé | `pytest nexus_os/tests -q` → **59 passed, 1 skipped** |

**Les 3 apps Vite sont déjà buildées** (`dist/` commité) : `animation-chronos` (2 fichiers),
`proto-cognitorium` (2), `watchtower` (9, Cesium inclus). Les `node_modules` sont absents —
la preview marche sans rebuild, le rebuild marche si besoin.

---

## 2. Ce qui dort dans les branches (le vrai gisement)

**41 branches** au total sur les 9 dépôts, dont **32 de travail** (hors `main`).
Comparaison `main...branche` via l'API GitHub (`ahead_by` / `behind_by`), le 7 octobre 2026 :
**14 branches contiennent du travail non fusionné, 18 sont mortes.**

### 14 branches avec du travail réel non fusionné

| Dépôt | Branche | Commits | Fichiers | Contenu |
|---|---|---:|---:|---|
| watchtower | `arena/01a072e1-watchtower` | **+42** | 145 | `feat(fil): le panneau de réglage du fil — chantier G terminé` |
| ETAT-DE-LART-PSYCHOLOGIE | `arena/01a04f7b-…` | **+38** | 300 | `fix: homepage noire + vues cassées — TDZ planets0/ovals` |
| monorepo | `arena/01a08449-monorepo` | **+24** | 252 | `feat(ui): complete comprehensive UI/UX overhaul` |
| COGNITORIUM | `watchtower/osint-workbench-v0.1` | **+13** | 12 | `docs(watchtower): align OSINT roadmap with master spec` |
| ETAT-DE-LART-PSYCHOLOGIE | `arena/01a07d32-…` | +5 | 11 | `Route /download/monorepo.bundle : secours push 403` |
| Language-decoder | `arena/01a05429-…` | +5 | 27 | `Add HCSM HUD stills: K-E-I flow, live metrics, Sankey` |
| proto-cognitorium | `arena/01a08342-…` | +5 | 14 | `audit: registre à jour (SEC-04, UX-04, 3 aggravations)` |
| watchtower | `arena/dec9cd88-watchtower` | +4 | 45 | `INTEL — base territoriale consolidée + atlas + veille` |
| ETAT-DE-LART-PSYCHOLOGIE | `arena/01a03aac-…` | +2 | 10 | `feat: Cognitorium v8 — graphe 3D, 40 fiches concepts` |
| monorepo | `arena/01a08277-monorepo` | +2 | 5 | `docs: synthèse Talbot 2026 v4.2` |
| ETAT-DE-LART-PSYCHOLOGIE | `arena/01a045a1-…` | +1 | 24 | `feat(agent): agent de recherche littéraire scientifique v1` |
| Language-decoder | `arena/01a05471-…` | +1 | 23 | `feat: Language-decoder human decoding engine + UI` |
| monorepo | `arena/01a08385-monorepo` | +1 | 51 | `feat(nexus_os): NEXUS·OS` (cette branche) |
| monorepo | `arena/01a08203-monorepo` | +1 | 22 | `frontignan : atlas interactif (graphe, carte, slides)` |

### 18 branches mortes (0 commit d'avance, uniquement en retard)

`proto-cognitorium` en compte 6 à elle seule (jusqu'à −54 commits de retard),
`ETAT-DE-LART` 4, `monorepo` 2, `HCSM` 2, `COGNITORIUM` 2, `watchtower` 2,
`Language-decoder` 0. **À supprimer** : elles ne contiennent rien que `main` n'ait déjà.

> Lecture : le travail n'est pas « en cours », il est **terminé et jamais fusionné**.
> `watchtower/arena/01a072e1` annonce un chantier G *terminé* avec 42 commits d'avance.

---

## 3. Ce que NEXUS·OS sait faire aujourd'hui

| Capacité | Détail vérifié |
|---|---|
| **10 agents spécialisés** | orchestrateur, chercheur, ingénieur, rédacteur, architecte, analyste, revendeur, pilote, coach, créateur |
| **14 compétences `SKILL.md`** | research-first, code, tests, revue, sécurité, copywriting, SEO, diagrammes, data, navigateur, HTML, sortie ADHD, mémoire, conception d'agent |
| **14 outils sandboxés** | `list_dir`, `read_file`, `write_file`, `grep`, `web_search`, `http_get`, `shell`, `python_exec`, `memory_remember`, `memory_recall`, `diagram`, `compose_html`, `handoff`, `create_agent` |
| **Routage automatique** | `route "rédige une landing page"` → Rédacteur score 7,08 ; l'orchestrateur délègue seul |
| **Cycle de vie ECC** | plan → recherche → implémentation → revue → vérification → mémorisation → amélioration |
| **Multi-agents** | chaînes (`/api/pipeline`), délégation bornée à 2 niveaux |
| **Auto-construction** | un agent peut créer un agent (`create_agent`) |
| **Routeur de modèles** | 8 fournisseurs, 20 modèles, quota + coût, bascule automatique, repli local |

### Limites actuelles (assumées, pas des bugs)

| Limite | Cause | Comment la lever |
|---|---|---|
| Mode **hors-ligne** | aucune clé API dans ce sandbox + sorties HTTPS vers `api.openai.com` bloquées | poser `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` dans `.nexus/secrets.env` |
| `shell` / `python_exec` refusés | désactivés par défaut | `NEXUS_ALLOW_SHELL=1` |
| `web_search` sans résultat | sorties HTTPS bloquées ici (sauf hosts autorisés) | exécuter hors sandbox |
| Base locale remise à zéro | `.nexus/` est gitignoré et le sandbox est réinitialisé | 1 run et 1 composition au compteur ce jour |
| L'inventaire GitHub ne remonte pas les ⭐ | le script ne collecte pas `stargazers_count` | 2 lignes à ajouter dans `scripts/github_inventory.py` |

---

## 4. État de l'art sur GitHub — octobre 2026

Classement par étoiles, d'après les trackers du 1<sup>er</sup> au 7 octobre 2026
([agents-radar 07/10](https://github.com/yaojiejia/agents-radar/issues/257),
[coddykit 04-05/10](https://www.coddykit.com/pages/blog-detail?id=5129956),
[gittrend 04/10](https://gittrend.io/trending/ai-agent),
[OmniRoute](https://github.com/diegosouzapw/OmniRoute)). Les chiffres varient selon la
source et la date ; ordre de grandeur fiable, valeur exacte non.

| Projet | ⭐ | Ce que c'est | Ce qu'on a déjà en face |
|---|---:|---|---|
| `obra/superpowers` | ~295 k | framework de compétences agentiques | ✅ `skills.py` + 14 `SKILL.md` |
| `mattpocock/skills` | ~275 k | skills « pour vrais ingénieurs » | ✅ même format, périmètre plus étroit |
| `affaan-m/ECC` | ~273 k | plan → test → review → verify → remember | ✅ cycle de vie ECC dans `runtime.py` |
| `dify` | ~158 k | workflows agentiques + RAG, self-hosted | ⚠️ pas de RAG ici |
| `msitarzewski/agency-agents` | ~157 k | collection d'agents | ✅ 10 agents + créateur |
| `open-webui` | ~154 k | UI multi-modèles | ⚠️ bureau web plus léger |
| `browser-use` | ~117 k | agents navigateur | ⚠️ agent `pilot` sans moteur de rendu |
| `thedotmack/claude-mem` | ~97 k | mémoire persistante inter-sessions | ✅ `memory.py` (facts/décisions/leçons) |
| `OpenCut` | ~92 k | éditeur vidéo open source | ❌ rien |
| `Panniantong/Agent-Reach` | ~91 k | yeux sur Twitter/Reddit/YouTube/GitHub, 0 frais d'API | ⚠️ `web_search`/`http_get` seulement |
| `stablyai/orca` | ~85 k | ADE : piloter une flotte d'agents en parallèle | ⚠️ chaînes séquentielles, pas de parallèle |
| `diegosouzapw/OmniRoute` | **73,4 k** (10,5 k forks, 359 fournisseurs, 1200+ modèles) | passerelle + quota + compression 15-95 % + MCP/A2A | ⚠️ routeur 8 fournisseurs, **pas de compression de tokens**, pas de MCP |
| `calesthio/OpenMontage` | ~63 k | production vidéo agentique, 100+ outils, 700+ skills | ❌ rien |
| `coreyhaines31/marketingskills` | ~53 k | CRO, copywriting, SEO, growth | ✅ 2 skills (marketing-copy, seo-content) |
| `HKUDS/nanobot` | ~49 k | agents personnels légers, self-hosted | ✅ philosophie proche de NEXUS·OS |
| `zhayujie/CowAgent` | ~47 k | assistant personnel multi-agents | ✅ orchestrateur + délégation |
| `langgraph` | ~43 k | orchestration par graphe | ⚠️ chaînes linéaires, pas de graphe |
| `cathrynlavery/diagram-design` | ~32 k | diagrammes brandés Mermaid/draw.io | ✅ skill `diagram-design` + outil `diagram` |
| `ayghri/i-have-adhd` | ~29 k | sortie « action d'abord » | ✅ skill `adhd-output`, appliquée partout |
| `neilsonnn/image-blaster` | 9,3 k (**+3,1 k/jour**, nouveau 2026) | image-to-world pour Claude | ❌ rien |
| `tester-army/e2e` | ~3,4 k | tests E2E web + mobile par agents | ⚠️ skill `test-and-verify`, pas d'E2E |

**Montée rapide à surveiller** (faible total, forte vélocité) : `morluto/rea…` (4,3 k,
+1,7 k/jour), `mvschwarz/openrig` (multi-agent harness, +624), `mksglu/context-mode`
(−98 % de tokens en sandboxant la sortie des outils), `heygen-com/hyperframes`
(HTML → vidéo, +349), `ComposioHQ/awesome-claude-skills` (+123).

---

## 5. Écarts à combler, du plus rentable au plus coûteux

| # | Action | Effort | Gain |
|---|---|---|---|
| 1 | Fusionner `watchtower/arena/01a072e1` (+42) et `ETAT-DE-LART/arena/01a04f7b` (+38) | ~30 min | récupère 80 commits de travail fini |
| 2 | Supprimer les 18 branches mortes | ~10 min | y voir clair |
| 3 | Ajouter `stargazers_count` + `open_issues` à l'inventaire GitHub | ~15 min | la page `/repos` affiche les ⭐ |
| 4 | Ajouter les ⭐ des dépôts *externes* suivis (veille outillage) | ~1 h | radar intégré, façon agents-radar |
| 5 | Compression de contexte (façon OmniRoute RTK / `context-mode`) | ~3 h | −15 à −95 % de tokens |
| 6 | Exécution **parallèle** d'agents (façon `orca`) | ~4 h | flotte au lieu de chaînes |
| 7 | Client MCP (façon OmniRoute, 110 outils) | ~1 j | brancher l'écosystème outils existant |
| 8 | Moteur navigateur réel pour l'agent `pilot` (Playwright) | ~2 h + install | le pilote passe de `http_get` à du vrai clic |
| 9 | RAG sur les 9 dépôts (façon `ragflow`) | ~1 j | les agents citent *ton* corpus, pas le web |
| 10 | Rendu vidéo HTML → MP4 (façon `hyperframes` / `OpenMontage`) | bloqué | **`ffmpeg` absent** du sandbox |

---

## 6. Reproduction de cet audit

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --host 0.0.0.0 --port 8123     # pages + previews + /os/
python -m pytest nexus_os/tests -q                   # 59 passed, 1 skipped
curl -X POST http://localhost:8123/api/github/refresh  # régénère l'inventaire
```

Chiffres de cet audit mesurés le 7 octobre 2026 sur la branche
`arena/01a08385-monorepo` (commit `b6646a0`), sandbox Python 3.11.2 / node v22.22.3.
