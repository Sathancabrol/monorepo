# 🖥 VEILLE — Herald OS, The Agency & les « Agent OS » (09/10/2026)

> **Demande** : vérifier Herald OS, les autres OS agents, « the agency » sur GitHub (~140 agents) ; trouver un système agent plus performant que le nôtre pour s'enrichir, ou tweaker.
> **Verdict** : rien à remplacer — notre base tient. **Deux adoptions immédiates** (fiches agents + QA gates) et **deux mises sous surveillance** (Herald OS, Hermes Agent) pour l'étape VPS.

---

## 1. 🔎 Les trois trouvailles

**Herald OS** (`iamlukethedev/Herald-OS`, MIT, 271★, alpha 0.1, poussé aujourd'hui) : un **OS agent-natif** — l'agent (Hermes de Nous Research) EST l'interface de l'ordinateur : dashboard, **Spaces (un espace par client/entreprise !)**, missions, mémoire, fichiers, automations, voix « hey Hermes ». Sécurité : **4 niveaux de permission** (Read → Act → Mutate → Destructive : les deux derniers demandent toujours) + **journal d'audit** de chaque action. macOS Apple Silicon + Linux ; nécessite Hermes + un fournisseur de modèle. Indépendant de Nous [1](https://www.techcityauthority.com/2026/10/herald-os-hermes-agent-linux.html)[2](https://juliangoldie.com/herald-os/).

**The Agency n°1 — `msitarzewski/agency-agents`** (MIT, ~102k★, 68 contributeurs) : **144→298 agents spécialistes** en 12-19 divisions. Chaque agent = **un fichier markdown** : identité, mission, règles, workflow, livrables, métriques. Compatible Claude Code natif, Cursor, Copilot, Gemini CLI… « Pas de magie : chaque agent est un fichier qu'on peut ouvrir, lire, modifier » [3](https://flaviocopes.com/agency-agents/)[4](https://explainx.ai/blog/agency-agents-ai-specialists-complete-guide-2026).

**The Agency n°2 — `Tekkiiiii/the-agency`** : « Claude Code, réparé pour tout le monde » — 235+ agents / 16 départements / 287 skills, et surtout les patterns qui nous manquaient : **mémoire qui survit aux sessions (SQLite task-store.db)**, **QA gates avant « terminé »**, routage économe en tokens, hooks de sécurité (scan secrets, cost-tracker), chaîne PD → Coord → Mini-Coord → Exec [5](https://github.com/Tekkiiiii/the-agency).

**La catégorie « Agent OS »** : formalisée par **AIOS** (arXiv 2403.16971) — le tableau de correspondance OS classique → agent : scheduler = boucle agent, RAM = contexte, **filesystem = mémoire persistante**, apps = skills, cron = tâches proactives, **drivers = MCP**. Hermes Agent (Nous, MIT, février 2026) est l'implémentation auto-hébergeable de référence [6](https://www.requesty.ai/blog/the-rise-of-the-agent-operating-system).

## 2. ⚖️ Comparaison avec notre système (honnête)

| Ce qu'ils ont de plus | Notre état | Verdict |
|---|---|---|
| Agents = fiches identité/règles/livrables (Agency) | services avec CAPABILITY courte | ⚠️ **à adopter** — fait ce tour |
| QA gates systématiques avant « done » | update check + arena + porte humaine, mais non formalisés en gate par livrable | ⚠️ **à adopter** — fait ce tour (règle dans les fiches) |
| Permission tiers + audit log (Herald) | règles d'or (jamais de suppression, porte humaine) | ✅ équivalent fonctionnel ; gradation documentée |
| Mémoire persistante (Tekkiiiii task-store) | **déjà là : knowledge SQLite+graphe** (ajouté cette nuit) | ✅ |
| Espaces par client (Herald) | prospects/offres par pipeline | ✅ équivalent |
| 24/7 + voix + OS complet | sandbox + repo | ⏳ étape VPS ; Hermes est le candidat harness |
| Ce que NOUS avons qu'ils n'ont pas | confrontation ELO (arena), garde-fou « jamais un seul juge », offres adossées à de vrais livrables | avantage |

## 3. ✅ Adopté ce tour / 📌 Surveillé

- ✅ **`projects/agent-office/agents/`** : nos 12 services deviennent des **fiches agents par département** au format The Agency (identité, mission, règles, workflow, livrables, métriques, **gate QA**) — lisibles par Claude Code/Cursor tels quels, modifiables à volonté.
- ✅ Règle gate généralisée : *aucun livrable n'est « terminé » sans sa porte de validation* (test, arena, ou humain).
- 📌 **Herald OS** : alpha à suivre ; concepts « Spaces/Missions/permissions » à copier pour le portail app/.
- 📌 **Hermes Agent** : candidat n°1 au rôle d'agent résident le jour du VPS (MIT, mémoire-first, MCP) — nécessite une clé modèle.
- ❌ Pas d'adoption d'AIOS (noyau de recherche, lourd) ni remplacement d'aucun de nos services.

---
*09/10/2026 · sources vérifiées web + API GitHub.*
