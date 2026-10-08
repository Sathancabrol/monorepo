# 🧩 SYSTÈME COMBINÉ — GobboNet + SillyTavern + Router + couche « enterprise » : existe-t-il, ou on le construit ?

> **Date** : 2026-10-08 · **Commande** : « regarde GobboNet, Tavern AI, enterprise (poko/poki ?), airouter — trouver un système qui combine tout, ou le construire »
> **Réponse courte** : le système unique qui combine les quatre **n'existe pas sur étagère** — mais 80 % des briques existent. On le **construit en 4 couches minces** dans le monorepo, en déployant (sans copier) le routeur et les modèles.

---

## 1. 🔎 Identification des 4 références (noms approximatifs → projets réels)

| Tu as dit | Projet réel | ★ | Créé | Licence | Ce que c'est |
|---|---|---|---|---|---|
| « git style gobbonet » | **[ElodineOfficial/GobboNet](https://github.com/ElodineOfficial/GobboNet)** | 167 | 05/2026 | **NOASSERTION** ❌ (idées seulement) | Front-end IA **1-clic, 100 % local, 100 % privé** (Windows d'abord) : launcher + moteur local + modèle + **petit modèle de retrieval** qui puise dans les notes/lore du personnage à chaque tour. Pensé pour les non-techniques. |
| « tavern ai » | **[SillyTavern/SillyTavern](https://github.com/SillyTavern/SillyTavern)** (et l'ancêtre TavernAI, MIT, 2,7k★) | **34 211** | ancien | **AGPL-3.0** ⚠️ (usage service, pas de copie) | « LLM Frontend for Power Users » : personnages, cartes, extensions, presets de prompt, multi-API. La référence du chat à personas. |
| « airouter » | **[THESIS-AGENT/AIRouter](https://github.com/THESIS-AGENT/AIRouter)** (188★ MIT) — mais le standard du marché est **[BerriAI/litellm](https://github.com/BerriAI/litellm)** | 60 345 | — | licence restrictive côté serveur* | LiteLLM : « the fastest AI Gateway », 100+ fournisseurs en format OpenAI unique, fallbacks, budget, load balancing. AIRouter en est une version réduite (Python, MIT). |
| « entreprise, poko/poki ? » | Meilleure hypothèse : **[Portkey-AI/gateway](https://github.com/Portkey-AI/gateway)** (« Portkey » ≈ poko/poki) | 13 148 | — | **MIT** ✅ | Gateway IA **orienté entreprise** : 1 600+ LLMs, **50+ guardrails**, cache, observabilité, BYOK. Si tu pensais à autre chose (Picovoice ? autre ?), dis-le et je corrige. |

\* LiteLLM : cœur utilisable en lib/SDK ; le déploiement serveur a des clauses commerciales — pour un usage solo self-hosted c'est l'usage standard, mais la brique « routeur » peut aussi être une fine proxy FastAPI maison (on en a déjà le stack).

## 2. 🏪 Les systèmes « tout-en-un » qui existent déjà (et leurs trous)

| Système | ★ | Combine quoi | Ce qui manque pour nous |
|---|---|---|---|
| **[Open WebUI](https://github.com/open-webui/open-webui)** | 154 204 | Chat + Ollama + OpenAI + RAG + multi-utilisateurs | licence non-OSI, personas faibles, **aucune intégration données de vie git-first** |
| **[AnythingLLM](https://github.com/Mintplex-Labs/anything-llm)** | 66 817 | MIT, local-first, agents + docs | orienté documents, pas personas/vie perso |
| **[LibreChat](https://github.com/LibreChat-AI/LibreChat)** | 45 396 | MIT, multi-fournisseurs, Agents, MCP, Skills | idem : plateforme chat, pas système de vie |
| **[OrcaRouter-Lite](https://github.com/Continuum-AI-Corp/OrcaRouter-Lite)** | 1 728 | Routeur self-hosted + filets de sécurité, BYOK | routeur seul |
| GobboNet + SillyTavern + LiteLLM « à la main » | — | la combi que font les power users | 3 produits à maintenir, aucune donnée partagée |

**Verdict** : tous ces systèmes combinent *chat + modèles + routage*. **Aucun** ne combine ça avec *personas + lore/mémoire persistante + données de vie git-first + hook sur tes modules existants* (mail-organizer, tracker prospective, `/api/life`). Le système complet reste à construire — mais en couches minces.

## 3. 🏗️ Le plan de construction (4 couches dans le monorepo)

```
app/ (FastAPI, déjà là)
├─ L4 UI        : /chat — interface personas minimale (emprunts GobboNet + SillyTavern)
├─ L3 Personas  : USER/PERSONAS/*.md — cartes de personnages git-first (lore, ton, règles)
├─ L2 Mémoire   : retrieval markdown (pattern GobboNet : petit modèle d'embedding qui
│                 puise le lore/notes pertinent au lieu de tout relire) sur USER/ + docs/
└─ L1 Router    : /api/ai — endpoint OpenAI-compatible unique
                   → LiteLLM ou proxy fine maison : clés cloud + Ollama local,
                     fallbacks, garde-fous (pattern Portkey, version solo)
```

| Couche | Faire ou déployer | Référence volée | Effort |
|---|---|---|---|
| **L1 Router** | **Déployer** LiteLLM (Docker) OU proxy FastAPI ~200 lignes si 2-3 fournisseurs suffisent | LiteLLM/Portkey : un endpoint, fallback, budget | 0,5 j (proxy) – 1 j (LiteLLM) |
| **L2 Mémoire** | **Construire** : index markdown + petit embedding local (le « retrieval model » de GobboNet) | GobboNet : ne pas relire tout le lore, récupérer le pertinent | 2-3 j |
| **L3 Personas** | **Construire** : format carte = markdown dans USER/ (compatible Arena/Claude Code) | SillyTavern : structure des cartes (personnalité, exemples, interdits) | 1 j |
| **L4 UI** | **Construire mince** dans app/ (une route, streaming, sélecteur de persona) ; SillyTavern en *service à côté* pour l'usage power-user riche | GobboNet : simplicité 1-page ; SillyTavern : presets. **Cahier des charges complet : [`UI-MOBIGLAS.md`](UI-MOBIGLAS.md)** (design SF : mobiGlas, HUD, options LCARS) | 2-3 j |
| Modèles locaux | **Déployer** Ollama sur le futur serveur (cf. `HARDWARE-LIFE-HUB.md` : N150 → RTX/Jetson selon l'ambition) | GobboNet : « ça tourne offline pour toujours » | 0,5 j |

**Total ≈ 1 semaine de construction** pour un système qui n'existe nulle part ailleurs, et qui sera le seul à parler à tes données de vie.

## 4. ⚖️ Règles de licence appliquées (comme dans LIFE-HUB.md)
- **Copier dans le repo** : uniquement les patterns MIT/Apache (cartes SillyTavern = réécrire le format, pas le code ; Portkey = patterns de guardrails).
- **AGPL (SillyTavern)** : jamais copié ; utilisable comme service à côté si tu veux l'UI riche.
- **NOASSERTION (GobboNet, Open WebUI)** : idées seulement, zéro code.
- **Déployer sans copier** : LiteLLM, Ollama (Docker).

## 5. 🎯 Recommandation
1. **Ordre de construction** : L1 (router) → L3 (personas markdown) → L2 (retrieval) → L4 (UI). Le router d'abord, car tout le reste (Arena, app/, futurs agents) consommera le même endpoint.
2. **Ne pas installer Open WebUI/LibreChat dans le monorepo** : doublons de ce qu'on construit en plus lourd, et aucune prise sur USER/. (LibreChat reste le plan B « tout fait » si la construction L4 dérape.)
3. **Synergie avec les décisions en cours** : ce système est exactement la « couche cerveau » de `LIFE-HUB.md` + le consommateur nº1 du routeur décrit ici ; il justifie d'autant plus le serveur maison de `HARDWARE-LIFE-HUB.md` (Ollama + LiteLLM y vivent).
4. **Si « poko/poki » n'était pas Portkey** : donne-moi le bon nom, la couche « enterprise » (multi-utilisateurs, guardrails, audit) s'ajuste en L1 — c'est la seule couche concernée.

---

## 📚 Sources (vérifiées via API GitHub le 08/10/2026)
[ElodineOfficial/GobboNet](https://github.com/ElodineOfficial/GobboNet) (README : launcher, moteur, retrieval model, offline) · [SillyTavern](https://github.com/SillyTavern/SillyTavern) · [TavernAI/TavernAI-v1](https://github.com/TavernAI/TavernAI-v1) · [THESIS-AGENT/AIRouter](https://github.com/THESIS-AGENT/AIRouter) · [BerriAI/litellm](https://github.com/BerriAI/litellm) · [Portkey-AI/gateway](https://github.com/Portkey-AI/gateway) · [open-webui](https://github.com/open-webui/open-webui) · [LibreChat](https://github.com/LibreChat-AI/LibreChat) · [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) · [OrcaRouter-Lite](https://github.com/Continuum-AI-Corp/OrcaRouter-Lite)
