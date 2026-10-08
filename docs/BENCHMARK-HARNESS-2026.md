# 🏁 BENCHMARK HARNESS 2026 — les nouveaux systèmes de vie IA (avril → octobre 2026)

> **Date** : 2026-10-08 · **Commande** : « trouver d'autres harness — les derniers 3, fenêtre maintenant − 6 mois, benchmark complet »
> **Méthode** : recherche GitHub API (8 requêtes croisées : « life os », « personal operating system », « ai chief of staff », « second brain agent », « personal ai os », « agent harness personal », « markdown vault claude »…), filtre `created:>2026-04-08`, puis lecture README + arborescence + métadonnées des candidats. Aucune donnée marketing — stars, forks, dates, licences, code.
> **Contexte** : la décision d'adopter [danielmiessler/LifeOS](https://github.com/danielmiessler/LifeOS) (voir `LIFE-HUB.md`) est mise en regard de ce qui est apparu dans les 6 derniers mois.

---

## 1. 📡 Le radar complet (tout ce qui est né dans la fenêtre)

| Projet | Créé le | ★ | Licence | Ce que c'est | Pertinence Life Hub |
|---|---|---|---|---|---|
| **undefined-ui/second-brain-os** | 07/09/2026 | **1 010** | MIT ✅ | Second cerveau auto-maintenu par agent (guide + vault + skills) | ⭐⭐⭐ directe |
| **agentverse-os/AgentVerse-OS** | 12/09/2026 | **977** | Apache-2.0 ✅ | OS cloud perso mono-serveur pour humains + agents | ⭐⭐ infra |
| **Wayn-Git/Amethyst** | 20/08/2026 | 72 | MIT ✅ | OS personnel local-first FastAPI/React/SQLite | ⭐⭐⭐ directe |
| mateaix/mateclaw | 04/04/2026 | 1 148 | Apache-2.0 | Second brain multi-agents (Spring AI Alibaba — Java) | ⭐ (stack lourd) |
| coreyhaines31/makerskills | 03/06/2026 | 848 | MIT ✅ | Skills agent « opérateur personnel » (décisions, recherche…) | ⭐⭐ patterns |
| swarmclawai/swarmvault | 06/04/2026 | 708 | MIT ✅ | Wiki LLM local-first, graphe de connaissances | ⭐⭐ patterns |
| itechmeat/open-second-brain | 06/05/2026 | 430 | MIT ✅ | Mémoire agent dans vault Obsidian + « dream passes » nocturnes | ⭐⭐ patterns |
| mcncarl/agent-memory-vault | 20/06/2026 | 313 | MIT ✅ | Vault mémoire markdown + SQLite + git + audit | ⭐⭐ patterns |
| georgeding/Relate | 23/09/2026 | 119 | AGPL ⚠️ | Chief of staff de chats (mémoire des promesses) | usage service seul |
| indigoai-us/hq-core | 21/04/2026 | 86 | MIT ✅ | Scaffold « personal OS for AI workers » (npx create-hq) | ⭐ à surveiller |
| vincenzo-afk/Synapse | 25/07/2026 | 38 | MIT ✅ | PWA local-first : habitudes, tâches, sport, finances | ⭐ idée |
| jdpolasky/chief-of-staff-2 | 08/08/2026 | 39 | MIT ✅ | Chief of staff markdown dans vault Obsidian, v2 | ⭐ idée |
| EverlastingAI-Official/LifeContextOS | 04/09/2026 | 40 | **aucune** ❌ | Mémoires de vie on-device, format standard | non copiable |
| alirezarezvani/gaios | 05/06/2026 | 46 | **NOASSERTION** ❌ | Blueprint AIOS Claude Code/Codex | non copiable en l'état |
| seandavi/lifeos-template | 15/05/2026 | 44 | **NOASSERTION** ❌ | Life-OS agentique markdown + boucles de revue | non copiable en l'état |
| lifeos-plus/lifeos-cli | 09/04/2026 | 14 | Apache-2.0 ✅ | LifeOS terminal + web UI optionnelle | ⭐ idée |

> Hors fenêtre mais toujours actifs : assafkip/kipi-system (13/03, 112★ MIT), danielmiessler/LifeOS (09/2025, 19,3k★ MIT), loganhc-09/claude-chief-of-staff (12/03, 79★ MIT).

**Premier constat** : en 6 mois, l'écosystème a explosé (16+ projets nouveaux) mais **aucun n'est un « LifeOS complet » de plus** — la vague s'est spécialisée en 3 niches : ① connaissance auto-maintenue, ② OS personnel local-first, ③ infra serveur pour agents.

---

## 2. 🔬 Les 3 derniers — audit complet

### 2.1 undefined-ui/second-brain-os — « la connaissance qui se range toute seule »
**Né le 07/09/2026 · 1 010 ★ · 163 forks en 31 jours · MIT · HTML/docs + Python sans dépendances · [secondbrainos.dev](https://secondbrainos.dev/)**

- **Ce que c'est** : pas une app — un **guide de 65 pages + un vault de départ + 18 skills + 72 commandes slash + 6 subagents + des plugins**, pour Claude Code + Obsidian. L'agent *construit et entretient* ta base de connaissances : tu clips/sauvegardes/dump, il range dans `raw/`, extrait, relie, écrit des pages wiki liées. « The filing work humans stop doing after two weeks — hand it to an agent. »
- **Architecture** : deux couches séparées — **wiki** (ce que tu sais : sources/concepts/entités/synthèses) et **projets** (ce que tu fais : pipeline Inputs/Process/Outputs/Feedback, un `CLAUDE.md` par projet). Maintenance planifiée : « wake up to a vault that filed itself ». Données live : calendrier, mail, chat.
- **Santé** : croissance la plus rapide du radar (0→1k★ en 1 mois), 1 seule issue, site web dédié, handbooks de craft (graphs, **harnesses**, loops, evals).
- **Limites** : pas de budget, pas de dashboard, pas de santé — c'est une couche *connaissance*, pas un système de vie. Obsidian-dépendant pour l'UI humaine.
- **Verdict** : **la meilleure couche « mémoire/connaissance » apparue cette année.** Copiable (MIT) intégralement ou à piller en patterns (skills, commandes, la séparation wiki/projets, la maintenance planifiée).

### 2.2 agentverse-os/AgentVerse-OS — « ton cloud privé pour toi et tes agents »
**Né le 12/09/2026 · 977 ★ · 26 forks · Apache-2.0 · Rust (cloudd) + Svelte 5 · alpha 0.2**

- **Ce que c'est** : un OS cloud personnel sur **un seul serveur Ubuntu** : bureau fenêtré dans le navigateur (PC/tablette/téléphone), workspaces isolés (Incus + Docker) avec VS Code et agents (Claude Code, Codex, Gemini CLI, pi), **store de 945 apps** (catalogues Runtipi + Coolify + Umbrel fusionnés), backups ZFS + restic, mises à jour avec rollback.
- **Idée-force** : « capabilities instead of addresses » — un projet demande `storage.s3` ou `llm`, le cœur branche le fournisseur sans toucher au projet. Accès **uniquement via Tailscale**, rien d'exposé.
- **Santé** : alpha assumée (« lives on a single test box »), 1 utilisateur, pas de comptes/permissions, UI EN/RU/UK/ES. Prérequis : Ubuntu 22.04+ propre, 8 Go RAM, disque ZFS.
- **Limites** : ce n'est **pas** un système de *contenu de vie* (pas de budget/planning/santé) — c'est la **couche d'hébergement** des agents et des apps. Poids d'infra élevé pour un usage solo aujourd'hui.
- **Verdict** : **le concurrent de notre strate « serveur maison »** (le tiers Proxmox/mini-PC de `HARDWARE-LIFE-HUB.md`), pas du Life Hub lui-même. À re-benchmarker quand le N150/Ryzen sera acheté — il pourrait remplacer l'empilement manuel Docker.

### 2.3 Wayn-Git/Amethyst — « le jumeau FastAPI de notre app/ »
**Né le 20/08/2026 · 72 ★ · 15 issues · MIT · Python 3.11/FastAPI + React 19 + SQLite · Docker + Vercel prêts**

- **Ce que c'est** : un OS personnel **local-first** : une boucle agent (reason/act/observe) qui **stream chaque tour, trace chaque outil, et demande avant d'écrire**. Vues : chat, **Today** (briefing du jour + événements + dettes), Tasks (board + moteur calendrier qui trouve les créneaux libres), **Library** (tout ce qui a une URL → markdown sur disque, recherche hybride), **Memory** (mémoires extraites par conversation), Mail (**Gmail via Google Workspace** ou AgentMail), Plugins/connecteurs (To Do, Google Workspace, GitHub, Spotify…), Automations (prompt sur intervalle + historique), palette ⌘K, mode Code (OpenCode embarqué).
- **Stack** : FastAPI + SQLite + React — **exactement notre pile** ; Ollama local pour zéro coût/zéro cloud, ou 21 providers cloud ; recherche tolérante aux pannes (4 providers + circuit breaker) ; MCP ; `AGENTS.md` à la racine ; capture depuis téléphone/bookmarklet/Instagram.
- **Santé** : jeune et petit (72★) mais poussé **aujourd'hui**, 15 issues ouvertes = communauté qui teste, docs d'architecture écrites, fiabilité traitée sérieusement (une instance garantie par le kernel, tests).
- **Limites** : **pas de module budget/finances**, pas de santé, pas de wiki de connaissances structuré (la Library s'en approche), agent propriétaire (pas Claude Code/Arena) — mais connecteurs MCP + AGENTS.md le rendent pontable.
- **Verdict** : **le seul du radar qui soit un vrai « Life Hub » au sens app+agent+données, né dans la fenêtre, en licence copiable, sur notre stack.** Plus jeune et moins complet que LifeOS (pas de finances, pas de Work System), mais plus moderne côté agentique (permissions, traces, subagents, automations).

---

## 3. ⚖️ Benchmark final — les 3 derniers vs LifeOS (le socle actuel)

| Critère (pondération) | **LifeOS** (09/2025, 19,3k★) | **second-brain-os** (09/2026) | **AgentVerse-OS** (09/2026) | **Amethyst** (08/2026) |
|---|---|---|---|---|
| Budget/finances (3) | ✅✅ page /finances + USER/FINANCES | ❌ | ❌ | ⚠️ « what is owed » seulement |
| Planning/tâches (3) | ✅ Work System + DASchedule | ⚠️ couche projets | ❌ (workspaces dev) | ✅✅ board + moteur calendrier |
| Mails (2) | ✅ TOOLS/gmail.ts | ⚠️ données live | ❌ | ✅ Gmail/AgentMail |
| Mémoire IA/connaissance (3) | ✅ Cortex | ✅✅✅ le cœur | ❌ | ✅ Library + Memory |
| Dashboard (2) | ✅✅ PULSE 31 modules | ❌ (Obsidian) | ✅ bureau navigateur | ✅✅ vues natives |
| Qualité agentique (2) | ⚠️ pensée Claude Code | ✅✅ skills/commandes/subagents | ✅✅ multi-agents managés | ✅✅✅ traces, permissions, subagents, automations |
| Données git-first/possédées (3) | ✅✅ markdown USER/ | ✅✅ vault markdown | n/a (infra) | ⚠️ SQLite + markdown Library |
| Compatibilité monorepo FastAPI/Linux (2) | ⚠️ bun à ajouter | ✅ zéro runtime | ❌ serveur dédié | ✅✅ natif |
| Maturité/risque (2) | ✅✅ v7.40, 2,4k forks | ⚠️ 1 mois | ❌ alpha solo | ⚠️ 7 semaines |
| Licence copiable (1) | ✅ MIT | ✅ MIT | ✅ Apache-2.0 | ✅ MIT |
| **TOTAL /23** | **18,5** | **12** | **5** | **16** |

Lecture : **LifeOS reste devant sur la couverture « vie »** (budget + planning + mails + dashboard), **Amethyst est devant sur la qualité agentique et la compatibilité de stack**, **second-brain-os est devant sur la connaissance auto-maintenue**, **AgentVerse-OS ne joue pas dans la même catégorie** (infra).

---

## 4. 🎯 Recommandation révisée (08/10/2026)

1. **Socle : LifeOS reste le choix nº1** pour les organes de vie (USER/ + PULSE + TOOLS, MIT) — aucun des 3 derniers ne couvre budget+planning+mails ensemble. La décision d'adoption tient.
2. **Mais la vague de septembre change le plan de Phase 5 (« cerveau IA »)** : au lieu d'attendre Cortex seul, **greffer les patterns de second-brain-os** (séparation wiki/projets, skills de maintenance planifiée, `/ingest`) sur USER/ — MIT, copiable, et c'est exactement ce que fait notre workflow actuel (capture → tri → liaison).
3. **Amethyst passe en « jumeau observé »** : même pile que `app/`, c'est le meilleur réservoir d'idées d'implémentation (permissions avant écriture, traces d'outils, Library à 8 portes d'entrée, automations). Si l'adaptation de PULSE s'avère trop coûteuse, Amethyst est le plan A' crédible — plus jeune, mais natif FastAPI.
4. **AgentVerse-OS → rendez-vous au moment d'acheter le serveur maison** (`HARDWARE-LIFE-HUB.md`) : si l'alpha a mûri, il remplace l'empilement Proxmox+Docker manuel. Re-benchmarker : T1 2027 (aussi la date de la 1ʳᵉ revue du `PROSPECTIVE-TRACKER.md`).
5. **Anti-pattern évité** : ne pas collectionner les harness. Trois systèmes simultanés = trois fois la maintenance pour zéro capitalisation. **Un socle (LifeOS) + une couche connaissance (patterns second-brain-os) + des emprunts ciblés (Amethyst)** — c'est tout.

---

## 5. 📚 Sources
- GitHub API (requêtes `search/repositories`, fenêtre `created:>2026-04-01/08`) : undefined-ui/second-brain-os · agentverse-os/AgentVerse-OS · Wayn-Git/Amethyst · + 13 autres projets du radar §1
- READMEs lus intégralement : [second-brain-os](https://github.com/undefined-ui/second-brain-os) (guide 65 p., quickstart, architecture raw→wiki) · [AgentVerse-OS](https://github.com/agentverse-os/AgentVerse-OS) (architecture cloudd/gates/capabilities, quick start) · [Amethyst](https://github.com/Wayn-Git/Amethyst) (features, Library, fiabilité)
- Référence socle : [danielmiessler/LifeOS](https://github.com/danielmiessler/LifeOS) (audit dans `docs/LIFE-HUB.md` §1 & §7)
