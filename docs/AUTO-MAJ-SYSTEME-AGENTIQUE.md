# 🔄 AUTO-MISE À JOUR DU SYSTÈME AGENTIQUE — outils & recherche

> **Question** (09/10/2026) : « trouver un système pour que le système agentique puisse se mettre à jour niveau outils et recherche — existe-t-il des processus ou outils déjà existants ? »
> **Réponse courte** : OUI, à toutes les couches — et la plupart s'assemblent sur ce qu'on a déjà. Le motif gagnant partout : **créer → vérifier empiriquement → committer → raffiner**, jamais d'auto-modification sans benchmark (c'est le rôle de notre `arena`).

---

## 1. 🧰 Couche OUTILS — découverte & acquisition automatique

| Système | Ce que c'est | Chiffres/état | Pour nous |
|---|---|---|---|
| **Smithery** | Registre + hébergement de serveurs MCP : recherche, install CLI, API registre (`GET /servers`), et **Toolbox** — un meta-MCP qui route l'agent vers le bon serveur **au runtime** | 6 000+ serveurs, freemium [1](https://tooldirectory.ai/tools/smithery) | le jour où le harness est branché : l'agent découvre et branche ses propres outils |
| **mcp.so / glama.ai / awesome-mcp-servers** | Annuaires MCP complémentaires | 20 222 serveurs indexés sur mcp.so [2](https://roxyapi.com/blogs/mcp-registries-where-to-list-your-server) | sources de veille outils |
| **Agent Skills** (standard `.agents/skills/`) | Compétences = fichiers portables installables ; marketplaces : skillsllm.com (avec scan sécurité), lobehub, plugin marketplaces (godmode en a un) | godmode déjà audité | **notre format natif** : chaque service agent-office est un skill potentiel |
| **Voyager** (pattern fondateur, 2023) | L'agent **écrit ses propres outils** (code), les stocke dans une bibliothèque persistante indexée par description, avec auto-vérification avant commit | Minecraft, GPT-4 [3](https://arxiv.org/pdf/2305.16291) | le motif à copier : skill = code + description + test, jamais commité sans vérification |
| **MUSE-Autoskill / AutoSkill / EvoSkill / SkillGen** (2026) | Skills comme « actifs vivants » : cycle complet création → mémoire → gestion → évaluation → raffinement → partage inter-agents | arXiv 2605.27366 [4](https://arxiv.org/html/2605.27366v2) | la feuille de route du cycle de vie d'un outil |

## 2. 🔎 Couche RECHERCHE — mise à jour automatique des connaissances

| Système | Job exact | État 2026 | Pour nous |
|---|---|---|---|
| **GPT-Researcher** | question → planificateur → chercheurs parallèles → rapport cité (20+ sources), MCP, installable comme skill | 29,9k★ Apache-2.0, actif (push 10/2026), ~0,20-1,00 $/tâche [5](https://www.digitalapplied.com/blog/open-source-deep-research-agents-2026-guide)[6](https://agentindex.app/tool/gpt-researcher/) | le moteur de veille « connecté » quand clés API |
| **Open Deep Research** (LangChain) | graphe researcher/summarize/compress/report, modèles & recherche interchangeables | 12,5k★ MIT, très actif [5](https://www.digitalapplied.com/blog/open-source-deep-research-agents-2026-guide) | idem, version orchestration |
| **Stanford STORM** | interviews d'experts simulés → plans encyclopédiques | 30,8k★ MIT mais **~10 mois sans push** — signal de maintenance faible [5](https://www.digitalapplied.com/blog/open-source-deep-research-agents-2026-guide) | à surveiller, pas à adopter tel quel |
| **Local Deep Research** | boucle de recherche **100 % locale** : SearXNG, arXiv, PubMed, docs perso — rien ne sort de la machine | ~8,9k★ permissif [5](https://www.digitalapplied.com/blog/open-source-deep-research-agents-2026-guide) | **meilleur fit immédiat** : watchtower embarque déjà une stack SearXNG docker |
| **reaserch-engine** (à nous) | contradictions + vérification des claims | v0.1 | la couche critique qui manque aux quatre autres |

## 3. 🧠 Couche MÉMOIRE — l'agent met à jour son propre état

- **Letta (ex-MemGPT)** — `cpacker/MemGPT` : mémoire **auto-éditée par l'agent via outils** (`core_memory_append/replace`, `archival_memory_search`), 3 étages (core = RAM, recall = cache, archival = froid), boucle heartbeat. L'agent décide lui-même quoi retenir/corriger/archiver [7](https://medium.com/@piyush.jhamb4u/stateful-ai-agents-a-deep-dive-into-letta-memgpt-memory-models-a2ffc01a7ea1)[8](https://zenn.dev/akky_tech/articles/25_12_ai_learned_with_letta?locale=en).
- **Mem0** : alternative « couche mémoire passive » (extraction automatique), plus prévisible, moins autonome [9](https://vectorize.io/articles/mem0-vs-letta).
- **Version fichiers** : la doc Letta elle-même note qu'on peut implémenter le même pattern « avec CLAUDE.md ou des fichiers » [8](https://zenn.dev/akky_tech/articles/25_12_ai_learned_with_letta?locale=en) → **nos fichiers USER/*.md et `update journal` sont des blocs mémoire Letta transposés en fichiers** (cohérent avec ICM Van Clief).

## 4. 🧬 Couche CODE — l'agent améliore son propre code (avec garde-fous)

- **Darwin Gödel Machine** (Sakana + UBC, arXiv 2505.22954, code `jennyzzt/dgm`) : l'agent réécrit son propre code, chaque variante est **validée empiriquement sur benchmarks**, archive darwinienne des variants ; SWE-bench 20 %→50 %. Improvements découverts : validation de patch, meilleurs outils d'édition, historique des échecs [10](https://sakana.ai/dgm/)[11](https://arxiv.org/abs/2505.22954).
- **ADAS** (Automated Design of Agentic Systems) : l'ancêtre — méta-agent qui designe des agents.
- **Reflexion** : sans toucher au code — l'agent verbalise la leçon après un échec et la stocke en mémoire. Le moins cher des auto-updates.
- ⚠️ Contreparties documentées : DGM « redécouvre des bonnes pratiques connues » plus qu'il n'innove [12](https://medium.com/@AIchats/darwin-g%C3%B6del-machines-a-self-improving-ai-8b5074de161a) ; et **toute auto-modification sans benchmark = danger** → d'où la règle : passage par `arena`/tests obligatoire.

## 5. 🎯 Assemblage recommandé (rien à construire de zéro)

**Maintenant, sans clé ni réseau** — livré avec ce doc : service **`update`** dans agent-office :
- `update journal` : journal des auto-mises à jour (outils ajoutés, recherches, décisions) ;
- `update lesson` : mémoire de leçons (pattern Reflexion en fichiers) ;
- `update changelog` : le système régénère son propre historique depuis git ;
- `update check` : cohérence du registre (tools.json frais + doctor).
Discipline « skill Voyager » actée : *toute nouvelle capacité = fichier + entrée registre + test, commitée seulement si vérifiée*.

**Dès réseau + clés disponibles** :
1. **Local Deep Research + SearXNG** (déjà dans watchtower) pour la veille `research watch` ;
2. **GPT-Researcher** en skill si budget API ;
3. **Smithery/Toolbox** pour la découverte d'outils MCP ;
4. **Letta ou blocs-mémoire fichiers** pour la mémoire persistante.

**Plus tard, avec garde-fous** : boucle DGM maison — l'agent propose une amélioration de son propre code, elle n'est acceptée que si `tests` + `arena` la valident (notre benchmark empirique existe déjà).

---
*Sources vérifiées le 09/10/2026. Voir aussi : SYSTEME-COMBINE-IA.md §6 (ICM/Obscura), SYSTEMES-CONFRONTATION-MODELES.md (les benchmarks-garde-fous).*
