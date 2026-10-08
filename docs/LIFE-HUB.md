# 🏠 LIFE HUB — Interface de vie bureautique complète (PC · tel · réel · IA)

> Recherche & architecture · 7-8 octobre 2026 · branche `arena/93b54a79-monorepo`
> Objectif : relier les modules existants du monorepo + des outils open source pour que `app/` devienne l'interface unique de la vie administrative personnelle — planning, budget, mails, tâches, documents — utilisable par l'humain **et** par les IA.
> **Stratégie : assembler plutôt qu'écrire** — copier ce qui est réutilisable (licences permissives), déployer le reste comme services, ne coder que la colle.

---

## 1. ♻️ Ce qu'on récupère sur GitHub (état de l'art vérifié)

### ✅ Copiable directement dans le monorepo (MIT / Apache)
| Repo | ★ | Ce qu'on prend |
|---|---|---|
| **matteogiorgi/second-brain** (MIT) | — | **L'architecture complète du socle** : core `notes/ projects/ areas/ journal/` + `AGENTS.md` + `workflows/` + `bin/capture` + adaptateurs agents (Claude Code…). Design hexagonal : le core ne dépend d'aucun outil ; chaque IA/éditeur n'est qu'un adaptateur jetable. → devient la structure de `data/life/` |
| **square-story/blipko** (MIT) | 10 | **Le pattern du bot budget conversationnel** : Telegram, saisie « courses 45 » en langage naturel (texte ou vocal), règle 50/30/20, `/status`, « est-ce que je peux acheter X ? », règles récurrentes, objectifs d'épargne. Stack Next.js/Prisma — on pique la logique UX/parsing, pas forcément le stack |
| **lissy93/dashy** (MIT) | 26,6k | Exemples de widgets/status checks si on veut enrichir la page `/life` |
| **actualbudget/actual** (MIT) | 29,3k | Importable comme **dépendance** (API npm) pour un vrai moteur de budget par enveloppes, ou inspiration pour le format JSONL |

### 🚀 À déployer tels quels (pas de code à maintenir, intégration par API/config)
| Outil | ★ | Licence | Rôle |
|---|---|---|---|
| **glanceapp/glance** | 37,4k | AGPL | Dashboard self-hosté tout fait : calendrier, météo, RSS, tâches, marque-pages — **piloté par un simple YAML** (on copie la config, pas le code) |
| **go-vikunja/vikunja** | 5,6k | AGPL | Tâches/planning : API REST + **CalDAV** (synchro agenda téléphone), kanban/gantt, rappels |
| **firefly-iii/firefly-iii** | 24,8k | AGPL | Comptabilité double entrée + règles d'auto-catégorisation + API REST tokens |
| **n8n-io/n8n** | 207k | fair-code | Workflows d'automatisation avec nœuds AI Agent + MCP |
| **khoj-ai/khoj** | 37,6k | AGPL | Second cerveau IA : chat sur vos docs, agents, automatisations, WhatsApp |
| **activepieces/activepieces** | 24,9k | MIT+ | Alternative n8n : chaque pièce = serveur MCP |

### ⚖️ Règle des licences (important)
- **Copier dans le repo** : uniquement MIT/Apache/BSD, avec attribution (fichier NOTICE).
- **AGPL/GPL** (Glance, Vikunja, Firefly, Khoj, Homepage) : **pas de copie de code** dans le monorepo, mais **utilisation comme service** (Docker/API) = aucun risque de contamination.
- **n8n** (fair-code) : self-host gratuit, mais code non copiable → on l'utilise, on écrit des workflows JSON (exportables/importables).
- Index permanent pour trouver d'autres outils : **awesome-selfhosted/awesome-selfhosted** (325k★).

## 2. 🧰 Choix par domaine (verdicts 2026)
- **Budget** : Actual Budget pour démarrer (MIT, PWA, ~1 h de setup) ; Firefly III pour la profondeur (règles + API) ; Blipko comme référence UX conversationnelle.
- **Planning/tâches** : Vikunja — le CalDAV rend le planning visible dans toutes les apps calendrier du téléphone.
- **Automatisation** : n8n (self-host) ; Activepieces si licence MIT exigée.
- **Assistant IA** : Khoj (ou les agents Arena déjà connectés à Gmail/Agenda/Drive).
- **Vie réelle** : ntfy (push), bot Telegram, connecteurs Google déjà actifs ici.

---

## 3. 🏗 Architecture cible : `projects/life-hub` + `app/`

```
                        ┌────────────────────────────────────┐
   HUMAIN               │            app/ (FastAPI)           │            IA
 ┌─────────┐            │  page /life (responsive + PWA 📱)   │        ┌──────────┐
 │ PC web  │◄──────────►│  API /api/life/*  (REST JSON)       │◄──────►│ Arena /  │
 │ Tel PWA │            │  exploreur monorepo existant        │        │ Khoj /   │
 │ Bot chat│            └───────────────┬────────────────────┘        │ n8n /    │
 └─────────┘                            │                               │ Claude   │
                                        ▼                               └────┬─────┘
                    ┌───────────────────────────────────────┐                │
                    │      projects/life-hub (le hub)        │◄───────────────┘
                    │  CLI `life` + règles + validation      │     (AGENTS.md + schémas JSON)
                    └───────────────┬───────────────────────┘
                                    ▼
        data/life/  (GIT-FIRST, structure copiée de second-brain, MIT)
        ├─ notes/ + projects/ + areas/ + journal/
        ├─ planning.json     événements + tâches
        ├─ budget.jsonl      transactions (append-only)
        ├─ goals.md          objectifs & revues
        └─ inbox/            captures brutes à trier
                                    │
   ┌──────────────┬─────────────────┼──────────────────┬──────────────────┐
   ▼              ▼                 ▼                  ▼                  ▼
mail-organizer  Google Calendar  Drive            research-engine    COGNITORIUM/HCSM
email→tâches    (déjà connecté)  documents        comparaisons       objectifs &
& docs admin    synchro agenda   administratifs   (forfaits…)        état perso
```

### Principes
1. **Git = base de données** : historisé, sauvegardé, lisible par toutes les IA. Zéro serveur obligatoire.
2. **Une API fine pour tous** (`/api/life/*`) : même contrat pour la page web, le bot et les agents ; écritures validées.
3. **`app/` = guichet unique** : page `/life` (agenda semaine, budget mois, tâches, docs, capture rapide), installable en PWA sur téléphone.
4. **Les modules existants = organes des sens** : mail-organizer (facture → tâche « payer »), connecteurs Arena, research-engine, COGNITORIUM/HCSM.

### Flux « vie réelle »
- **Chat** : « courses 45,90 » (pattern Blipko) → bot → API → budget.jsonl + git commit auto.
- **Mail** : facture EDF → mail-organizer → tâche « payer » + rappel ntfy à J-3.
- **Tel** : PWA `/life` = agenda + budget + saisie 2 taps.
- **IA** : « budget courses ce mois-ci ? » → lecture budget.jsonl → réponse + conseil.

---

## 4. 🗺 Roadmap (accélérée par la réutilisation)

| Phase | Contenu | Réutilisation |
|---|---|---|
| **1. MVP life-hub** | `data/life/` + API dans `app/` + CLI `life` + page `/life` | structure **second-brain** (MIT) copiée ; formats inspirés d'Actual |
| **2. Planning & budget riches** | Vikunja (CalDAV tel) + Actual Budget ou budget interne | **déploiement Docker**, zéro code |
| **3. Bots & rappels** | bot Telegram + ntfy + n8n | logique conversationnelle inspirée de **Blipko** (MIT) |
| **4. Cerveau IA** | Khoj sur `data/life/` + AGENTS.md, revue hebdo auto | Khoj déployé ; adaptateurs second-brain |
| **5. Dashboard maison** | Glance (YAML) ou page `/life` enrichie de widgets | **config Glance** copiée, pas le code |

**Sans serveur** : phase 1 + ponts Google fonctionnent immédiatement. Phases 2+ : un Docker (NAS, VPS ~5 €/mois, Raspberry Pi).

## 5. ✅ Décisions clés
| Décision | Choix | Pourquoi |
|---|---|---|
| Socle de données | copier second-brain (MIT) | architecture agents-first déjà éprouvée |
| Budget | JSONL interne d'abord, Actual/Firefly ensuite | démarrer sans setup ; monter en puissance |
| Tâches | hub interne puis Vikunja (API/CalDAV) | pas de code AGPL copié, juste de l'intégration |
| Automatisation | n8n déployé | workflows JSON réutilisables, nœuds IA natifs |
| Assistant IA | Khoj déployé ou agents Arena | données personnelles restent chez vous |

## 6. 📚 Sources (vérifiées via API GitHub le 08/10/2026)
- Star counts & licences : api.github.com (glanceapp/glance 37,4k★ AGPL ; vikunja 5,6k★ AGPL ; actual 29,3k★ MIT ; firefly-iii 24,8k★ AGPL ; n8n 207k★ ; khoj 37,6k★ AGPL ; dashy 26,6k★ MIT ; second-brain MIT ; blipko MIT ; awesome-selfhosted 325k★)
- Comparatifs budget 2026 : expensesorted.com, selfhosting.sh, pare.money
- Vikunja CalDAV : rdp.sh, selfprivacy.org · Khoj : docs.khoj.dev · n8n alternatives : composio.dev, getdynamiq.ai
