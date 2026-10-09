# 🖥 VEILLE — Herald OS, The Agency & les « Agent OS » (09/10/2026)

> **Demande** : vérifier Herald OS, les autres OS agents, « the agency » sur GitHub (~140 agents) ; trouver un système agent plus performant que le nôtre pour s'enrichir, ou tweaker.
> **Verdict** : rien à remplacer — notre base tient. **Deux adoptions immédiates** (fiches agents + QA gates), **surveillance renforcée** (Herald OS, Hermes Agent, **OmniRoute**) pour l'étape modèles/VPS ; **Wan2GP** = futur atelier vidéo si GPU (màj 09/10 : section 4).

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

## 4. 🔎 MàJ — Wan2GP & OmniRoute (09/10/2026)

**Wan2GP → WanGP** (`deepbeepmeep/Wan2GP`, Python, ~10 200★, push 07/10/2026) : générateur **vidéo IA pour « GPU pauvres »** (dès 6 Go VRAM) — Gradio UI, file d'attente, LoRAs, mode headless + API. Modèles : Wan 2.1/2.2, Minimax H3, LTX-2, Hunyuan Video, Qwen Image, Flux [7](https://github.com/deepbeepmeep/Wan2GP)[8](https://wanvideogenerator.com/blog/wan2gp-free-guide). Attention : licence non standard (NOASSERTION), et le projet alerte sur les sites payants frauduleux qui usurpent son nom. **Verdict : pas adoptable maintenant** (pas de GPU ici, ni de budget pour en louer — le VPS est déjà reporté au 1ᵉʳ revenu). **Candidat « atelier vidéo » du département RÉSEAUX** le jour où une machine GPU existe (locale ou Colab gratuit) : clips pour LinkedIn/Bluesky sans payer d'outil. Alternative immédiate sans GPU : générer les visuels des posts autrement et réserver la vidéo aux offres type O3.

**OmniRoute** (`diegosouzapw/OmniRoute`, TypeScript, MIT, ~74 300★, push hier) : **passerelle IA locale** — UN point d'entrée OpenAI-compatible (`localhost:20128/v1`) derrière lequel il route **359 fournisseurs / 1200+ modèles**, avec **fallback 4 niveaux** (abonnement → clé API → pas cher → gratuit), suivi de quotas en temps réel, compression de tokens RTK+Caveman (−15 à −95 %), serveur MCP (110 outils) + protocole A2A. Tourne sur laptop/VPS/Termux (~15 Mo), `npm install -g omniroute` ou Docker [9](https://github.com/diegosouzapw/OmniRoute)[10](https://devtoollab.com/blog/omniroute-free-ai-gateway)[11](https://hoangyell.com/omniroute-explained/).
- **Pour nous c'est LA pièce manquante du jour** : le jour où on a des clés/abonnements modèles, OmniRoute devient la couche sous `arena` (accès multi-modèles bon marché pour les duels) et sous le futur portail `app/`.
- **Pas maintenant** : sans aucun fournisseur de modèle configuré, une passerelle ne route rien — et les free tiers OAuth posent des questions de CGU fournisseurs (à lire avant usage).
- **Pattern à copier dès maintenant** dans `docs/SYSTEMES-CONFRONTATION-MODELES.md` quand on branchera des modèles : fallback par palier + lockout par modèle (on ne coupe pas tout un fournisseur pour un modèle en échec) + quotas visibles.

| Projet | État | Verdict |
|---|---|---|
| Wan2GP (WanGP) | actif, ~10 k★ | 📌 atelier vidéo — condition : accès GPU |
| OmniRoute | très actif, ~74 k★, MIT | 📌 couche routage modèles — condition : 1ᵉʳ fournisseur/clé ; patterns notés |

---
*09/10/2026 · sources vérifiées web + API GitHub.*
