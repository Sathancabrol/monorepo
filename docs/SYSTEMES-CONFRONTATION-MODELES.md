# ⚔️ SYSTÈMES DE CONFRONTATION & D'ITÉRATION MULTI-MODÈLES

> **Demande** (09/10/2026) : « check arena ai, godmod, trouver des systèmes de confrontation itération n8n pour que le système agentique se benchmark, compare les réponses de différents modèles ».
> **Verdict court** : tout existe déjà en open source ; la bonne combinaison pour l'entreprise d'IA = **arena locale en aveugle (déjà ajoutée à agent-office)** + protocole **ChatEval** (jury multi-rôles) + **Promptfoo** quand des clés API existeront + **litellm** comme routeur des gagnants.

---

## 1. 🏟 Arena AI = LMArena (ex-Chatbot Arena)

La référence mondiale de la confrontation : **duel aveugle** — deux modèles anonymes répondent à la même question, un humain vote, un score **ELO** (comme aux échecs) est mis à jour sur des millions de duels [1](https://www.chatbot.fr/chatbot-arena/).

**État 2026** : rebaptisée LMArena en janvier 2026 ; 369 modèles classés, 7,1 M+ votes ; le top 10 texte se tient en < 30 points (Claude Fable 5 ≈1509, Opus 4.6/4.7/4.8, Gemini 3.x, GPT-5.5) [1](https://www.chatbot.fr/chatbot-arena/)[2](https://localaimaster.com/blog/lmarena-chatbot-arena-leaderboard). Kimi K3 (open-weight, Moonshot) a pris la tête du classement **code** à 1 679 ELO en juillet 2026 — premier modèle ouvert à le faire [3](https://www.swfte.com/lmsys-leaderboard).

**Leçons directement utilisables** :
- **Le classement par catégorie prime sur le général** : un modèle 1ᵉʳ en « créatif » peut être 7ᵉ en « code ». Catégories : Expert (5,5 % de prompts les plus durs), Coding, Math, Instruction Following, Multi-Turn, Hard Prompts, Occupational [2](https://localaimaster.com/blog/lmarena-chatbot-arena-leaderboard). → notre arena locale doit taguer les duels par catégorie.
- Les scores « preview » à peu de votes sont fragiles → il faut un nombre minimum de duels avant de conclure.
- Source publique des données : dépôt `lmarena-ai/arena-leaderboard` [5](https://www.swfte.com/blog/lmsys-arena-leaderboard-may-2026).
- Un benchmark local indépendant a retrouvé le même phénomène : sur 90 tests, un modèle local gratuit (MiniMax M2.7) a égalé un modèle cloud payant (87/90 chacun) → **le routage hybride par tâche** prime sur « le meilleur modèle absolu » [8](https://flowtivity.ai/blog/ai-agent-benchmark-local-vs-cloud/).

## 2. 🔓 « Godmod » = godmode (thiientv) — identifié

**thiientv/godmode** — 96★, MIT, Python, créé août 2026 [9](https://skillsllm.com/skill/godmode) : des **Agent Skills** de niveau production pour agents de code — workflows composables de planning, TDD, debug, review, **evals** [9](https://skillsllm.com/skill/godmode).
Contenu vérifié du repo : `evals/` (grilles d'évaluation JSON par compétence), `benchmarks/golden-tasks.json` (tâles étalons), `docs/p0-quality-loop.md`, `docs/failure-taxonomy.md`, `docs/evidence-ledger.md` — et surtout les skills **`dispatching-parallel-agents`** et **`subagent-driven-development`** (cycles implémentation/revue autour d'un plan) [vérifié via API GitHub le 09/10].
→ **C'est exactement le motif « confrontation/itération » appliqué au travail agentique** : chaque production est vérifiée par un autre passage agent + preuve fraîche (`completion-verification`). Installable en copiant `skills/*` dans `.agents/skills/` — compatible Claude Code / Codex CLI [9](https://skillsllm.com/skill/godmode).

Deux homonymes à ne pas confondre : *godmode.space* (FOLLGAD, 2023 — AutoGPT dans le navigateur, obsolète) [10](https://easywithai.com/ai-agents/godmode/) et un skill « godmode » de red-team/jailbreak multi-modèles (« ULTRAPLINIAN multi-model racing ») [11](https://lobehub.com/skills/nazicc-hermes-agent-godmode) — seule l'idée de **course multi-modèles** est à retenir de celui-ci, pas le but.

## 3. 🧬 Les 5 familles de systèmes de confrontation (état de l'art)

| Famille | Représentants | Principe | Pour nous |
|---|---|---|---|
| **Arena aveugle à votes** | LMArena | duel anonyme + vote + ELO | ✅ reproduit dans `agent-office/arena` |
| **Jury multi-agents (débat)** | **ChatEval** (ICLR 2024) : 2-4 juges à rôles divers (Critic, Scientist, Psychologist…) débattent puis notent ; **+6,2 % de précision vs juge unique** ; la diversité des rôles est LA condition du gain [4](https://arxiv.org/pdf/2308.07201)[5](https://www.emergentmind.com/topics/chateval) | juger une sortie avec un panel plutôt qu'un seul modèle | ✅ protocole repris pour `arena judge` |
| **Débat factuel** | MAD-Fact (2025) : Clerk/Jury/Judge pour vérifier les textes longs [6](https://arxiv.org/html/2510.22967v1) ; DEBATE (Scorer/Critic/Commander), CourtEval, MAJ-EVAL, Agent-as-a-Judge [7](https://arxiv.org/html/2508.02994v1) | confrontation itérative = robuste aux biais du juge unique | motif général : **jamais un seul juge** |
| **Harness d'évaluation (CI)** | **Promptfoo** (MIT, YAML, A/B multi-modèles + red-team 500+ vecteurs ; racheté par OpenAI 03/2026 mais reste MIT) [12](https://genai.qa/blog/promptfoo-vs-deepeval-vs-ragas/)[13](https://www.cognee.ai/llm-agent-evaluation-tools) ; **DeepEval** (pytest, portes CI) ; Ragas (RAG) ; **Inspect AI** (agents en environnement contrôlé) ; lm-evaluation-harness (200+ benchmarks académiques) [14](https://inference.net/content/llm-evaluation-tools-comparison/) | comparer systématiquement modèles/prompts sur jeu de tests | → quand clés API dispo |
| **Orchestration workflows** | **n8n** : workflow « Local Multi-LLM Testing & Performance Tracker » (n8n.io #2442 : modèles LM Studio → métriques → Google Sheets) [15](https://n8n.io/workflows/2442-local-multi-llm-testing-and-performance-tracker/) ; patrons de framework d'éval (appel → parsing → mesure → stockage → A/B continu) [16](https://www.allogenai.com/comment-construire-un-framework-devaluation-llm-avec-n8n-rapidement/) ; le niveau « Benchmarker » de la communauté n8n = tester/comparer/itérer [17](https://community.n8n.io/t/pourquoi-vos-agents-ia-echouent-et-comment-y-remedier/236306) ; comparateur de modèles [18](https://n8nlab.io/ai-configurator) | la boucle prompt → N modèles → collecte → score en tuyaux visuels | → si n8n est déployé un jour |

## 4. 🎯 Recommandation pour le système agentique (assemblage, pas reconstruction)

1. **Dès maintenant (sans clé API)** — `agent-office arena` (livré avec ce doc) :
   - `arena battle` enregistre un duel en aveugle (prompt + réponses A/B, catégorie) ;
   - `arena page` génère la page de vote aveugle ; `arena vote` met à jour l'**ELO local** ;
   - `arena judge` affiche la **grille ChatEval** (3 rôles) pour un jugement humain structuré ;
   - le hook LLM-juge (litellm) est en place pour le jour où une clé existe.
2. **Itération** — motif godmode : chaque livrable passe par un second passage agent (revue) + une preuve fraîche ; les grilles `evals/` de godmode sont un modèle à copier pour nos propres services.
3. **Quand des clés API arrivent** — brancher dans l'ordre : **litellm** (routeur : la catégorie gagnante de l'ELO local route vers le bon modèle, déjà retenu dans SYSTEME-COMBINE-IA) → **Promptfoo** (matrices YAML, A/B, red-team en CI) → **Inspect AI** si on veut benchmarker des agents complets en environnement clos.
4. **Jamais un seul juge** : tout jugement automatique doit être un panel (≥2 rôles) ou un vote humain — biais de style et de préférence documentés du juge unique [7](https://arxiv.org/html/2508.02994v1)[4](https://arxiv.org/pdf/2308.07201).
5. **Références publiques à suivre** : `lmarena-ai/arena-leaderboard` (données ELO), classements par catégorie plutôt qu'overall [3](https://www.swfte.com/lmsys-leaderboard).

---
*Sources vérifiées le 09/10/2026 (web + API GitHub). Les chiffres ELO sont des instantanés mouvants — toujours revérifier avant de citer.*
