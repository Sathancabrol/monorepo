# ⬢ NEXUS·OS — Agentic Operating System

Un système d'exploitation pour agents IA, dans ce monorepo. Un seul point d'entrée,
plusieurs fournisseurs de modèles, un runtime d'agents, un **créateur d'agent
intégré** et **10 agents spécialisés** prêts à l'emploi.

> Inspiré de [OmniRoute](https://github.com/diegosouzapw/OmniRoute) (passerelle
> multi-fournisseurs avec repli), [ECC](https://github.com/affaan-m/ECC) (cycle
> plan → test → implémente → review → vérifie → mémorise → améliore),
> [superpowers](https://github.com/obra/superpowers) /
> [openai/skills](https://github.com/openai/skills) (compétences `SKILL.md`),
> [marketingskills](https://github.com/coreyhaines31/marketingskills),
> [diagram-design](https://github.com/cathrynlavery/diagram-design),
> [browser-use](https://github.com/browser-use/browser-use),
> [hyperframes](https://github.com/heygen-com/hyperframes) et
> [i-have-adhd](https://github.com/ayghri/i-have-adhd) (sortie « action d'abord »).

---

## Démarrage

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt

# interface web (seule)
uvicorn nexus_os.app:app --host 0.0.0.0 --port 8124     # → http://localhost:8124

# ou montée dans l'interface unifiée du monorepo
uvicorn app.main:app --host 0.0.0.0 --port 8123         # → http://localhost:8123/os/
```

CLI :

```bash
python -m nexus_os status                                   # état du système
python -m nexus_os agents                                   # les 10 agents
python -m nexus_os route "rédige une landing page"          # qui doit traiter ?
python -m nexus_os run "audite la structure du dépôt"       # exécute (streaming)
python -m nexus_os create "un agent qui relit les contrats" # crée un agent
python -m nexus_os serve --port 8124                        # interface web
```

---

## Architecture

```
nexus_os/
├─ providers.py    routeur de modèles : catalogue, quota-aware, repli automatique
├─ llm.py          complétion unifiée (OpenAI / Anthropic / moteur local) + bascule
├─ skills.py       framework SKILL.md : découverte, frontmatter, scoring par triggers
├─ tools.py        14 outils sandboxés (fs, grep, exec opt-in, net, mémoire, diagram…)
├─ memory.py       mémoire persistante : facts, décisions, leçons
├─ agents.py       specs d'agents (JSON) + registre + scoring d'affinité
├─ creator.py      créateur d'agents : description → spec complète
├─ runtime.py      boucle d'exécution par phases, délégation, pipelines
├─ app.py          API JSON + SSE + bureau web
├─ agents/         10 agents intégrés (JSON)
├─ skills/         14 compétences intégrées (SKILL.md)
├─ templates/ static/   interface « bureau »
└─ tests/          59 tests (pytest)
```

### 1. Routeur de modèles (façon OmniRoute)

8 fournisseurs, 20 modèles, un seul point d'entrée : `Router.route(ModelRequest(...))`.

- sélection par **quota restant du jour** + coût, préférence aux modèles gratuits ;
- filtres de capacité (`need_tools`, `need_vision`, `need_reasoning`, `min_context`) ;
- **bascule automatique** : erreur réseau/HTTP ⇒ cooldown de 5 min sur le modèle,
  passage au suivant de la chaîne ;
- repli final sur le **moteur local** : l'OS tourne toujours, même sans clé API.

Clés lues dans l'environnement ou dans `.nexus/secrets.env` (`CLÉ=valeur`), jamais
exposées au client :

| Fournisseur | Variable |
|---|---|
| Anthropic | `ANTHROPIC_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| Google | `GEMINI_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| Groq | `GROQ_API_KEY` |
| Mistral | `MISTRAL_API_KEY` |
| Ollama | `OLLAMA_API_KEY` (n'importe quelle valeur) |

Sans clé : mode **hors-ligne**. Les outils sont réellement exécutés ; seule la
génération de texte devient déterministe (et l'UI l'affiche).

### 2. Agents spécialisés (10 intégrés)

| Agent | Rôle |
|---|---|
| 🧭 `orchestrator` | découpe, route vers le bon spécialiste, consolide |
| 🔎 `researcher` | recherche sourcée, état de l'art, niveau de confiance |
| 🛠️ `coder` | implémentation : lit avant d'écrire, teste, corrige |
| ✍️ `writer` | copywriting, SEO, growth |
| 📐 `architect` | diagrammes Mermaid + HTML (composants, flux, séquences) |
| 📊 `analyst` | données & métriques, honnêteté sur l'échantillon |
| 🛡️ `reviewer` | revue qualité & sécurité, classée par sévérité |
| 🌐 `pilot` | automatisation navigateur, une action à la fois |
| 🎯 `coach` | focus : prochaine action, estimation en minutes |
| 🧬 `builder` | conçoit d'autres agents (l'OS se construit) |

### 3. Créateur d'agent intégré

`POST /api/agents/draft` (aperçu) puis `POST /api/agents` (enregistrement), ou
l'outil `create_agent` depuis n'importe quel agent.

Une description libre produit : id, nom, rôle, **prompt système** à règles
numérotées, 2–4 compétences, le minimum d'outils, les triggers de routage et le
cycle de vie. Deux moteurs : le modèle live (JSON strict) ou un moteur de règles
déterministe hors-ligne. Aucun outil ni compétence n'est inventé : tout est
validé contre le registre.

### 4. Compétences `SKILL.md`

```markdown
---
name: diagram-design
description: Diagrammes d'architecture, flux et séquences lisibles.
triggers: [diagramme, schéma, architecture, mermaid]
tags: [architecture, visualisation]
tools: [diagram, compose_html]
---
# corps markdown = instructions injectées dans le prompt système
```

Découvertes dans `nexus_os/skills/` (intégrées) et `.nexus/skills/` (les tiennes,
prioritaires à nom égal). Une compétence est activée soit parce que l'agent la
déclare, soit parce que ses `triggers` correspondent à la tâche.

### 5. Sécurité des outils

- écriture **uniquement** sous `.nexus/workspace/` (sandbox) — traversal bloqué ;
- lecture dans le dépôt, **sauf secrets** (`.env`, `secrets.env`, clés SSH…) ;
- `shell` / `python_exec` **désactivés par défaut** : `NEXUS_ALLOW_SHELL=1` ;
- liste de refus de commandes destructives, timeout systématique ;
- réseau contrôlé par `NEXUS_ALLOW_NETWORK`.

---

## API

| Méthode | Route | Rôle |
|---|---|---|
| GET | `/api/status` | mode live/hors-ligne, compteurs, flags |
| GET | `/api/agents` · `/api/agents/{id}` | liste / spec + export Markdown |
| POST | `/api/agents/draft` · `/api/agents/create` | créateur (aperçu / création) |
| POST · DELETE | `/api/agents` · `/api/agents/{id}` | enregistrer / supprimer |
| GET | `/api/skills` · `/api/skills/{name}` | bibliothèque de compétences |
| GET | `/api/tools` | registre d'outils + schémas |
| GET | `/api/providers` · `/api/models` | état du routeur |
| POST | `/api/route` | quel agent doit traiter cette tâche |
| GET | `/api/run?task=&agent=` | exécution **streamée (SSE)** |
| GET | `/api/pipeline?task=&agents_chain=` | chaîne multi-agents streamée |
| GET | `/api/runs` · `/api/usage` | journal + consommation |
| GET · POST · DELETE | `/api/memory` | mémoire persistante |
| GET | `/workspace/{path}` | artefacts produits par les agents |

Événements SSE : `run_start`, `routing`, `phase`, `thinking`, `tool_call`,
`tool_result`, `artifact`, `handoff`, `consolidation`, `agent_created`,
`message`, `run_end`, `result`, `error`.

---

## Tests

```bash
.venv/bin/python -m pytest nexus_os/tests -q     # 59 tests
```

Les tests exercent le vrai code : routage du routeur, découverte des
compétences, sandbox des outils, création d'agent, boucle d'exécution avec
outils réellement écrits sur disque, délégation bornée, pipelines, API HTTP et
flux SSE, montage dans l'app du monorepo.

## Variables d'environnement

| Variable | Défaut | Effet |
|---|---|---|
| `NEXUS_HOME` | `.nexus/` | base, mémoire, agents créés, sandbox |
| `NEXUS_ALLOW_SHELL` | `0` | autorise `shell` / `python_exec` |
| `NEXUS_ALLOW_NETWORK` | `1` | autorise `http_get` / `web_search` |
| `NEXUS_PREFER_FREE` | `1` | préfère les modèles gratuits |
| `NEXUS_DAILY_TOKEN_BUDGET` | `1500000` | quota de tokens/jour par fournisseur |
| `NEXUS_MAX_STEPS` | `8` | plafond de phases par exécution |
| `NEXUS_REQUEST_TIMEOUT` | `60` | timeout des appels modèles (s) |
