# 🏠 LIFE HUB — Interface de vie bureautique complète (PC · tel · réel · IA)

> Recherche & architecture · 7-8 octobre 2026 · branche `arena/93b54a79-monorepo`
> Objectif : relier les modules existants du monorepo + des outils open source pour que `app/` devienne l'interface unique de la vie administrative personnelle — planning, budget, mails, tâches, documents — utilisable par l'humain **et** par les IA.
> **Stratégie mise à jour le 08/10 : partir d'un système déjà complet et l'adapter** plutôt que d'assembler brique par brique (voir §1).
> **✅ DÉCISION ACTÉE LE 08/10/2026 : LifeOS est adopté** (renforcée par `BENCHMARK-HARNESS-2026.md`). Phase 1 réalisée dans **`projects/life-hub/`** : adoption sélective au commit upstream `5e2f2e8c` (USER template + ALGORITHM + ATLAS + RULES + WORKFLOW, NOTICE MIT, 142 fichiers). Prochaine étape : instancier `USER/` via le workflow Interview.

---

## 1. 🎯 Des briques déjà assemblées existent — audit des suites « tout-en-un »

Vérifié via l'API GitHub le 08/10/2026 (stars + licences) :

| Suite | ★ | Licence | Planning | Budget | Notes/docs | Mails | IA | Verdict |
|---|---|---|---|---|---|---|---|---|
| **danielmiessler/LifeOS** | **19,3k** | **MIT ✅** | ✅ (Work System, DASchedule) | ✅ (page /finances, USER/FINANCES) | ✅ (wiki, mémoire Cortex) | ✅ (TOOLS/gmail.ts) | ✅✅ (cœur du système) | **⭐ Le seul qui couvre (presque) tout** |
| AppFlowy | 77,2k | AGPL | ✅ kanban/docs | ❌ | ✅ | ❌ | ✅ intégré | Notion-like + IA, pas de budget/mail |
| AFFiNE | 73,3k | MIT-ish* | ✅ | ❌ | ✅ docs+whiteboard | ❌ | partiel | Idées UI seulement |
| memos | 63,6k | MIT ✅ | ❌ | ❌ | ✅ notes rapides | ❌ | ❌ | Complément capture rapide |
| SiYuan | 46,7k | AGPL | partiel | ❌ | ✅ | ❌ | ✅ | Base de connaissances |
| Logseq | 45,2k | AGPL | partiel | ❌ | ✅ | ❌ | ❌ | Notes quotidiennes |
| Nextcloud | 37,0k | AGPL | ✅ agenda+tâches | ❌ | ✅ fichiers | ✅ app Mail | ❌ | La suite « bureau » classique, pas IA-first |
| Trilium | 38,2k | AGPL | ❌ | ❌ | ✅ | ❌ | ❌ | Notes hiérarchiques |
| SilverBullet | 6,3k | MIT ✅ | ✅ requêtes | partiel | ✅ markdown | ❌ | ❌ | PWA self-host, hackable |
| Anytype | 8,9k | source-available | ✅ objets | ❌ | ✅ | ❌ | ❌ | Local-first, licence non-OSI |

\* licence AFFiNE = MIT + partie entreprise à part.

### ⭐ danielmiessler/LifeOS : le système complet, MIT, copiable

« The AI-Powered Life Operating System » — 2 658 fichiers, TypeScript/Bun, très actif (v7.40, août 2026). Ce qu'il contient **déjà assemblé** :

- **`USER/`** — le coffre de données personnel en **markdown git-first** : ABOUTME, BASICINFO, CONTACTS, GOALS, **FINANCES/ACCOUNTS.md**, DIGITAL_ASSISTANT (mémoire de l'IA). Exactement la philosophie qu'on avait prévue pour `data/life/`.
- **PULSE** — le dashboard **Next.js** (port 31337) : page **/finances** (diagrammes Sankey, graphes dépenses/revenus), /health, **kanban de travail**, wiki, notifications **voix**, iMessage/Siri.
- **TOOLS** (207 outils TypeScript) : **gmail.ts**, **DASchedule.ts** (planning), healthsync (Apple Health/Oura/Eight Sleep), imports, etc.
- **Cortex** — mémoire persistante de l'assistant (capture automatique, recherche).
- **Atlas** — inventaire de tout ce qu'on possède (actifs, comptes).
- **Work System** — capture → GitHub Issues comme système d'enregistrement.
- **TELOS + Algorithm** — boucle « état actuel → état idéal » avec vérification.

**Limites à connaître** : pensé pour un harnais IA type Claude Code (s'installe dans `~/.claude`), orienté macOS (iMessage, Apple Health), Pulse tourne sous Bun. → il faut l'**adapter** à notre environnement (monorepo FastAPI, agents Arena, Linux), pas l'installer à l'aveugle.

### Conséquence sur le plan
On **ne réécrit pas** le dashboard, le format de données, la mémoire IA ni les outils gmail/planning : on **copie LifeOS (MIT, avec attribution NOTICE)** et on adapte. Le code maison restant = la colle avec le monorepo existant (mail-organizer, connecteurs Google, modules cognitifs).

## 2. ♻️ Compléments réutilisables (si besoin au-delà de LifeOS)

### ✅ Copiable directement dans le monorepo (MIT / Apache)
| Repo | ★ | Ce qu'on prend |
|---|---|---|
| **danielmiessler/LifeOS** (MIT) | 19,3k | **Le socle complet** : USER/ + PULSE + TOOLS (voir §1) |
| **matteogiorgi/second-brain** (MIT) | — | Patterns de workflows agents (`triage/ask/connect/distill`) pour compléter |
| **square-story/blipko** (MIT) | 10 | Pattern du bot budget conversationnel (« courses 45 » en langage naturel) |
| **lissy93/dashy** (MIT) | 26,6k | Idées de widgets/status checks |
| **actualbudget/actual** (MIT) | 29,3k | Moteur de budget par enveloppes si LifeOS/FINANCES devient trop léger |

### 🚀 À déployer tels quels, seulement si un besoin précis apparaît
| Outil | ★ | Licence | Rôle |
|---|---|---|---|
| **go-vikunja/vikunja** | 5,6k | AGPL | CalDAV : rendre le planning synchro natif téléphone |
| **firefly-iii/firefly-iii** | 24,8k | AGPL | Comptabilité double entrée avancée |
| **n8n-io/n8n** | 207k | fair-code | Workflows d'automatisation (nœuds IA/MCP) |
| **khoj-ai/khoj** | 37,6k | AGPL | Chat IA sur tous les documents |
| **glanceapp/glance** | 37,4k | AGPL | Dashboard YAML tout fait (alternative à PULSE) |
| **activepieces/activepieces** | 24,9k | MIT+ | Alternative n8n |

### ⚖️ Règle des licences (inchangée)
- **Copier dans le repo** : uniquement MIT/Apache/BSD, avec attribution (fichier NOTICE).
- **AGPL/GPL** : jamais de copie de code, seulement utilisation comme service (Docker/API).
- **n8n** (fair-code) : utilisation + workflows JSON, pas de copie.
- Index permanent : **awesome-selfhosted/awesome-selfhosted** (325k★).

## 3. 🧰 Choix par domaine (verdicts 2026, mis à jour)
- **Budget** : page /finances + USER/FINANCES de LifeOS d'abord ; Actual Budget en renfort si besoin.
- **Planning/tâches** : Work System + DASchedule de LifeOS ; Vikunja (CalDAV) seulement pour la synchro téléphone native.
- **Mails** : TOOLS/gmail.ts de LifeOS **+ notre mail-organizer** (IMAP hotmail) + connecteurs Arena déjà actifs.
- **Automatisation** : hooks LifeOS + n8n seulement pour les workflows lourds.
- **Assistant IA** : Cortex (mémoire LifeOS) + agents Arena ; Khoj en option.
- **Vie réelle** : notifications voix Pulse, ntfy, bot Telegram (pattern Blipko).

---

## 4. 🏗 Architecture cible révisée

```
                        ┌─────────────────────────────────────┐
   HUMAIN               │         app/ (FastAPI, portail)      │            IA
 ┌─────────┐            │  /life → PULSE (dashboard LifeOS)    │        ┌──────────┐
 │ PC web  │◄──────────►│  /api/life/* (API unifiée)           │◄──────►│ Arena /  │
 │ Tel PWA │            │  + modules monorepo existants        │        │ Cortex   │
 └─────────┘            └───────────────┬─────────────────────┘        └────┬─────┘
                                        ▼                                    │
                    ┌───────────────────────────────────────┐                │
                    │  projects/life-hub = adaptation        │◄───────────────┘
                    │  LifeOS (USER/, PULSE/, TOOLS/)        │   (AGENTS.md + schémas)
                    │  + ponts mail-organizer & Google       │
                    └───────────────┬───────────────────────┘
                                    ▼
        USER/  (coffre de données markdown, GIT-FIRST — format LifeOS)
        ├─ ABOUTME / GOALS / CONTACTS / DIGITAL_ASSISTANT (mémoire IA)
        ├─ FINANCES/ACCOUNTS.md + transactions
        ├─ planning / tâches (Work System → fichiers ou GitHub Issues)
        └─ captures, journal
                                    │
   ┌──────────────┬─────────────────┼──────────────────┬──────────────────┐
   ▼              ▼                 ▼                  ▼                  ▼
mail-organizer  Google Calendar  Drive            research-engine    COGNITORIUM/HCSM
(email→tâches)  (déjà connecté)  documents        comparaisons       état perso
```

### Principes (mis à jour)
1. **LifeOS fournit les organes** : données, dashboard, mémoire, outils — MIT, donc copiés avec NOTICE d'attribution.
2. **Git = base de données** : USER/ versionné, lisible par toutes les IA.
3. **`app/` = guichet unique** : sert le dashboard PULSE + l'API `/api/life/*` + les modules existants.
4. **Les modules du monorepo restent branchés** : mail-organizer, connecteurs Google, research-engine, COGNITORIUM/HCSM.
5. **Pas de duplication** : Actual/Vikunja/n8n/Glance ne seront ajoutés que si un manque concret apparaît.

---

## 5. 🗺 Roadmap révisée (beaucoup moins de code maison)

| Phase | Contenu | Réutilisation |
|---|---|---|
| **1. Adoption LifeOS** | Copier USER/ + PULSE + TOOLS utiles dans le monorepo, NOTICE, adapter au contexte français + Linux, données perso dans USER/ | **100 % LifeOS** (MIT) |
| **2. Branchement monorepo** | `app/` sert PULSE + API ; ponts mail-organizer (facture→tâche), connecteurs Google (agenda, drive) | colle fine maison |
| **3. Vie réelle** | notifications (voix Pulse, ntfy), bot Telegram (pattern Blipko), saisie budget en langage naturel | patterns Blipko (MIT) |
| **4. Renforts ciblés (si besoin)** | Vikunja pour CalDAV téléphone, Actual pour enveloppes, n8n pour gros workflows | déploiements Docker, zéro code |
| **5. Cerveau IA** | Cortex + agents Arena sur USER/ ; revue hebdo auto ; Khoj en option | LifeOS + Arena |

## 6. ✅ Décisions clés (mise à jour 08/10)
| Décision | Choix | Pourquoi |
|---|---|---|
| Socle global | **LifeOS copié et adapté** (MIT) | système complet déjà assemblé : budget+planning+mails+mémoire IA+dashboard |
| Données | USER/ markdown git-first (format LifeOS) | compatible avec notre vision + toutes les IA |
| Dashboard | PULSE (Next.js) servi via `app/` | déjà écrit, page finances incluse |
| Budget | FINANCES LifeOS, Actual en renfort éventuel | démarrer sans setup |
| Tâches | Work System LifeOS, Vikunja seulement si CalDAV requis | éviter les briques superflues |
| Automatisation | hooks LifeOS + n8n au besoin | moins de dépendances au départ |

## 7. 🔬 Approfondissement LifeOS — faisabilité réelle (08/10/2026)

> **MAJ 08/10 (soir)** : benchmark des harness nés dans les 6 derniers mois (second-brain-os, AgentVerse-OS, Amethyst…) → [`BENCHMARK-HARNESS-2026.md`](BENCHMARK-HARNESS-2026.md). Verdict : LifeOS reste le socle, second-brain-os pour la couche connaissance, Amethyst comme jumeau FastAPI observé.

### Santé du projet
- Créé 09/2025, dernier push 04/09/2026, **2 488 forks**, 45 issues ouvertes, v7.40 — actif et déjà adopté.
- Docs officielles complètes : docs.ourlifeos.ai (55 documents, 33 sections).
- Écosystème : **Fabric** (44,2k★ MIT, même auteur) = bibliothèque de patterns IA déjà intégrée ; Arbol = exécution cloud (Cloudflare, optionnel).

### Ce qu'il faut pour le faire tourner
| Dépendance | Statut | Notes |
|---|---|---|
| **bun** | requis | runtime TypeScript ; s'installe en une ligne sous Linux |
| **gh** CLI | requis (Work System) | les tâches vivent dans un **repo GitHub privé** — cohérent avec notre vision git-first, `gh` est déjà configuré ici |
| ripgrep, ImageMagick… | optionnels | philosophie officielle : tout **dégrade proprement** ; `Doctor.ts decline <x>` désactive proprement chaque capability |
| ElevenLabs | optionnel | notifications voix (une clé API) |
| Cloudflare | optionnel | jobs planifiés « pendant que tu dors » (Arbol) |
| macOS (iMessage/Siri/Apple Health) | optionnel | à décliner sur Linux — prévu par design |

### Points d'attention (honnêtes)
1. **Parties privées** : l'implémentation du sous-système Assistant (DA) et le CLI Bunker ne sont **pas** dans la release publique (concept documenté seulement). Le reste (Cortex/mémoire, Pulse 31 modules, TOOLS, USER/) est public.
2. **Pulse = démon Bun** (port 31337, un process, modules isolés des crashes) + dashboard Next.js 15 classique → faisable sous Linux, mais il faut assumer le runtime bun à côté de notre FastAPI (ou porter le dashboard Next.js seul).
3. **Module Telegram retiré** (15/07/2026) → notre bot budget (pattern Blipko) resterait à écrire si on veut le chat.
4. Installateur pensé pour Claude Code (`~/.claude`) → on adapte les chemins vers le monorepo (travail d'adaptation, documenté par leurs `Tools/InstallEngine.ts`).

### Les autres pistes « tout assemblé », écartées en connaissance de cause
| Piste | Pourquoi écartée (ou gardée en réserve) |
|---|---|
| **Templates Notion « Life OS / Ultimate Brain »** (Thomas Frank, Easlo…) | Tout-en-un réel et **zéro code**, utilisable immédiatement (ton connecteur Notion est déjà actif dans Arena). Mais : données chez Notion (pas de git local), budget basique, IA = Notion AI payant, templates souvent payants. **Gardé comme plan B « ultra-simple ».** |
| Repos « personal OS » GitHub (Dex 493★, claude-chief-of-staff 438★, openclaw-n8n-stack 137★…) | 10-40× plus petits que LifeOS, moins complets, communautés naissantes |
| AppFlowy / AFFiNE / Anytype / SiYuan / Nextcloud / SilverBullet | Excellents dans UN domaine (docs, agenda+mails…) mais aucun ne combine budget + planning + mails + mémoire IA ; servis comme renforts éventuels (§2) |

## 8. 📚 Sources (vérifiées via API GitHub le 08/10/2026)
- **danielmiessler/LifeOS** 19,3k★ MIT — README, ARCHITECTURE_SUMMARY.md, arbre complet (2 658 fichiers : PULSE/finances, TOOLS/gmail.ts, DASchedule.ts, USER/FINANCES/ACCOUNTS.md), GETTING-STARTED.md, PULSE/package.json, docs.ourlifeos.ai (PulseSystem) — métadonnées : créé 2025-09, push 2026-09-04, 2 488 forks
- **danielmiessler/Fabric** 44,2k★ MIT (patterns IA, écosystème LifeOS) · recherche « personal operating system ai » (Dex 493★, claude-chief-of-staff 438★…)
- Templates Notion Life OS / Second Brain 2026 : notioneverything.com, notion4management.com
- Suites : AppFlowy 77,2k★ AGPL ; AFFiNE 73,3k★ ; memos 63,6k★ MIT ; SiYuan 46,7k★ AGPL ; Logseq 45,2k★ AGPL ; Trilium 38,2k★ AGPL ; Nextcloud 37,0k★ AGPL ; Anytype 8,9k★ source-available ; SilverBullet 6,3k★ MIT
- Briques : glance 37,4k★ AGPL ; vikunja 5,6k★ AGPL ; actual 29,3k★ MIT ; firefly-iii 24,8k★ AGPL ; n8n 207k★ ; khoj 37,6k★ AGPL ; dashy 26,6k★ MIT ; second-brain MIT ; blipko MIT ; awesome-selfhosted 325k★
- Comparatifs budget 2026 : expensesorted.com, selfhosting.sh, pare.money · Vikunja CalDAV : rdp.sh, selfprivacy.org · Khoj : docs.khoj.dev
