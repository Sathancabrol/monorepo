# Carré d’As comme hub de configuration d’agents IA — veille GitHub

**État de la veille : 8 octobre 2026** · **Portée :** repos GitHub et briques utiles pour construire un espace opérateur/administrateur d’agents, en plus des interfaces destinées aux utilisateurs.

> Cette étude est un catalogue et une proposition de direction, pas une intégration de code. Le checkout du monorepo ne contient pas encore le projet Carré d’As ni son contrat d’API. La demande produit, elle, est maintenant clarifiée : Carré d’As doit aussi permettre à son propriétaire de créer, configurer, tester, publier et gouverner ses agents.

La veille s’appuie sur les métadonnées, README et fichiers de licence des dépôts GitHub consultés le 8 octobre 2026; aucun code n’a été cloné ou importé. Les nombres d’étoiles cités sont des instantanés arrondis : ils indiquent l’intérêt de la communauté, **pas** la qualité, la sécurité, la maturité ni la compatibilité de licence. `À vérifier` signifie que l’API GitHub ne reconnaissait pas de licence SPDX simple ou que le dépôt contient des composants sous licences différentes. Toujours lire le fichier `LICENSE` du commit retenu, y compris les répertoires Enterprise.

## Synthèse — quoi étudier en premier

1. **Construire le hub d’administration dans Carré d’As**, plutôt que remplacer son interface par un chatbot générique. Les utilisateurs finaux ne devraient voir que les agents publiés; le propriétaire a un espace distinct pour les configurer.
2. **Comparer Agno AgentOS et Langflow comme références de studio/runtime**, puis prototyper les parcours dans le vrai front-end de Carré d’As. Ils offrent une interface de gestion/assemblage; ils ne doivent pas devenir une dépendance avant revue de licence, d’authentification et de séparation des données.
3. **Garder le runtime interchangeable.** Pour un socle Python, comparer PydanticAI pour des outils typés et simples, LangGraph pour les parcours stateful/durables et Microsoft Agent Framework pour ses workflows multi-agents. Le langage réel de Carré d’As n’étant pas connu, ne pas encore trancher.
4. **Utiliser MCP comme frontière de plugins/outils**, avec catalogue, schéma, scopes et permissions par outil. MCP donne accès à des outils; ce n’est ni un moteur d’agent complet ni une garantie de sécurité. A2A sert plutôt à faire communiquer des agents; AG-UI à relier un agent à une interface temps réel.
5. **Commencer localement par Ollama**, déjà configuré dans le MVP LAPLACE. Ajouter LiteLLM uniquement si une passerelle multi-fournisseurs, des quotas, du routage ou un suivi central des coûts deviennent nécessaires.
6. **Mettre les évaluations et traces dans le cycle de publication.** Shortlist : Promptfoo pour tests/régressions et red-team; Langfuse ou LangWatch pour traces/évaluations. Masquer les secrets et minimiser le contenu personnel envoyé dans les traces.
7. **Séparer agent, outils et compagnon PC.** Playwright est une bonne base déterministe pour des onglets de navigateur. L’action sur fenêtres/souris/fichiers de l’ordinateur doit passer par un compagnon local contrôlé, pas par un shell exposé à un agent distant.

### Produits de référence à essayer ou à examiner en premier

| Projet | Signal GitHub au 08/10/2026 | Pourquoi le regarder | Réserve principale |
|---|---:|---|---|
| [Agno](https://github.com/agno-agi/agno) | ≈43 k ⭐ | SDK + runtime AgentOS + UI de gestion et RBAC JWT; ressemble à un « agent platform » complet. | Architecture, compatibilité et licence de chaque composant à vérifier avant intégration. |
| [Langflow](https://github.com/langflow-ai/langflow) | ≈156 k ⭐ | Studio visuel MIT; README annonce API et exposition des flows comme serveurs/outils MCP. | À comparer au schéma et aux authz déjà présents dans Carré d’As. |
| [Dify](https://github.com/langgenius/dify) | ≈158 k ⭐ | Workflows visuels, RAG, agents, modèles et self-host. | Licence modifiée Apache : elle restreint notamment l’exploitation multi-tenant sans autorisation écrite; risque direct si Carré d’As sert plusieurs espaces/clients. |
| [BISHENG](https://github.com/dataelement/bisheng) | ≈12 k ⭐ | Plateforme intégrée : modèles, workflows, agents, données et évaluation. | Vérifier ergonomie/langue, empreinte de déploiement et intégration avec le code Carré d’As. |
| [OpenClaw](https://github.com/openclaw/openclaw) | ≈392 k ⭐ | Référence de passerelle d’assistant personnel local et multi-canaux; état, outils, skills et extensions. | Le README avertit que les outils du parcours principal peuvent s’exécuter sur l’hôte sans sandbox. Étudier le modèle de menace, ne pas exposer tel quel. |
| [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) | ≈67 k ⭐ | Application self-host/local-first, espaces, documents et agents; bon banc d’essai utilisateur. | Plus proche d’une application IA prête à l’emploi que d’un studio à intégrer dans Carré d’As. |
| [LibreChat](https://github.com/LibreChat-AI/LibreChat) | ≈45 k ⭐ | Interface chat multi-fournisseurs avec Agents, MCP et outils. | Référence d’expérience utilisateur/intégrations, pas à elle seule un plan de contrôle de tous les agents. |
| [Open WebUI](https://github.com/open-webui/open-webui) | ≈154 k ⭐ | Modèles, agents, outils, fonctions et permissions de groupes; UX self-host riche. | Licence Open WebUI personnalisée avec conditions de marque; l’étudier comme référence, pas la rebrander sans revue juridique. |
| [n8n](https://github.com/n8n-io/n8n) | ≈207 k ⭐ | Automatisations avec agents, validations humaines et grand catalogue de connecteurs. | Fair-code/Sustainable Use License, pas une licence open source OSI; valider le cas d’usage commercial et ne pas confondre workflow et runtime d’agent. |
| [CopilotKit](https://github.com/CopilotKit/CopilotKit) | ≈38 k ⭐ | Brique front-end pour interfaces agentiques et human-in-the-loop, si le front Carré d’As est React/Angular. | À ajouter seulement si elle s’accorde au front-end existant; AG-UI est une alternative d’interopérabilité plus neutre. |
| [OpenHands](https://github.com/OpenHands/OpenHands) | ≈90 k ⭐ | Référence pour agents de développement, tâches outillées et exécution sandboxée. | Domaine coding/engineering; ne pas le choisir comme cœur des agents grand public. |

## Catalogue GitHub élargi

### Studios visuels, plateformes d’agents et interfaces d’administration

| Repo | Apport potentiel pour Carré d’As | Licence / statut à retenir |
|---|---|---|
| [Agno](https://github.com/agno-agi/agno) | SDK, runtime AgentOS, UI d’administration et RBAC; candidat de comparaison le plus directement « plateforme ». | Apache-2.0 indiqué par GitHub. |
| [Langflow](https://github.com/langflow-ai/langflow) | Canvas visuel pour agents/flows, API et outils MCP; MIT. | MIT; candidat de POC. |
| [Dify](https://github.com/langgenius/dify) | App builder complet : modèles, workflows, RAG, agents, publication. | Licence propriétaire-modifiée basée sur Apache; restriction multi-tenant/branding à vérifier. |
| [BISHENG](https://github.com/dataelement/bisheng) | Plateforme GenAI/LLMOps intégrée (modèles, RAG, agents, évaluations et administration). | Apache-2.0 indiqué; vérifier les dépendances et l’UX. |
| [Inkeep Agents](https://github.com/inkeep/agents) | Builder no-code et SDK TypeScript synchronisés en deux sens. | Licence non détectée par l’API GitHub; vérifier avant réutilisation. |
| [SmythOS Studio](https://github.com/SmythOS/smythos-studio) | Builder visuel self-hostable et runtime de déploiement. | MIT indiqué; vérifier la maturité à l’échelle voulue. |
| [PySpur](https://github.com/PySpur-Dev/pyspur) | Playground visuel pour itérer sur des workflows d’agents. | Apache-2.0; activité à re-vérifier avant POC. |
| [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) | App self-host/local-first, workspace, documents, agents et plusieurs modèles. | MIT; bon prototype de parcours, plutôt qu’un composant à intégrer sans adaptation. |
| [LibreChat](https://github.com/LibreChat-AI/LibreChat) | UI multi-fournisseur avec agents, MCP et outils; utile pour benchmarker l’expérience utilisateur. | MIT. |
| [Open WebUI](https://github.com/open-webui/open-webui) | Interface locale, profils d’agents, connecteurs, audio/vidéo et permissions utilisateur/groupe. | Licence personnalisée; conditions de marque à respecter. |
| [LobeHub](https://github.com/lobehub/lobehub) | Gestion/exécution de plusieurs agents, tâches et rapports. | LobeHub Community License; distribution d’un dérivé soumise à conditions commerciales. |
| [Activepieces](https://github.com/activepieces/activepieces) | Automatisation IA, agents et connecteurs/MCP; alternative à évaluer pour l’orchestration métier. | Licence non déterminée par l’API GitHub; vérifier le dépôt et les offres hébergées. |
| [n8n](https://github.com/n8n-io/n8n) | Workflows, outils, connecteurs, approbation humaine et automatisation. | Sustainable Use/Fair-code et composants Enterprise séparés; pas de fork/white-label sans revue. |
| [LangChain](https://github.com/langchain-ai/langchain) | Grande bibliothèque d’intégrations modèles/outils, utile pour explorer l’écosystème. | MIT; éviter de l’ajouter « en bloc » si seul un sous-ensemble est nécessaire. |
| [Flowise](https://github.com/FlowiseAI/Flowise) | Ancien builder visuel populaire, utile à consulter comme historique/UX. | **Repo archivé** au jour de la veille : ne pas retenir comme nouveau socle. |

### Assistants personnels et agents exécutés par le propriétaire

| Repo | Apport potentiel | Licence / risque |
|---|---|---|
| [OpenClaw](https://github.com/openclaw/openclaw) | Gateway d’assistant personnel local, canaux, plugins, skills, nodes/compagnons et outils. | MIT; sandbox indispensable pour les outils opérant sur l’hôte. |
| [Goose](https://github.com/aaif-goose/goose) | Agent général sur le PC avec app desktop, CLI et API; extensions et choix de modèles. | Apache-2.0; benchmark pertinent pour le compagnon local. |
| [Nanobot](https://github.com/HKUDS/nanobot) | Runtime personnel léger avec WebUI, canaux, MCP, mémoire et tâches planifiées. | MIT; vérifier le périmètre des permissions avant d’en reprendre les patterns. |
| [AstrBot](https://github.com/AstrBotDevs/AstrBot) | Plateforme chatbot/agent multi-messageries, plugins, Discord, MCP et sandbox de code. | AGPL-3.0; obligations de copyleft à étudier avant intégration. |
| [Agent Zero](https://github.com/agent0ai/agent-zero) | Agent avec bureau Linux, navigateur et projets isolés; utile pour étudier les contrôles d’ordinateur. | Licence non reconnue par GitHub; exécutant à haut privilège, pas un outil à lancer sans sandbox. |
| [OpenHands](https://github.com/OpenHands/OpenHands) | Plateforme d’agents de développement et environnements d’exécution. | MIT; à garder dans une zone « agents développeur ». |

### Frameworks runtime et orchestration

| Repo | Quand l’évaluer | Licence / note |
|---|---|---|
| [LangGraph](https://github.com/langchain-ai/langgraph) | Flows stateful, reprises, tâches longues, checkpoints et human-in-the-loop. | MIT; candidat Python/TS pour workflows explicites. |
| [PydanticAI](https://github.com/pydantic/pydantic-ai) | Agents Python typés, validation de paramètres et abstraction de fournisseurs. | MIT; bon premier choix si Carré d’As est Python. |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | Workflows d’agents Python/.NET, orchestration et déploiement. | MIT; successeur recommandé par Microsoft pour les nouveaux projets AutoGen. |
| [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | Handoffs, outils, MCP, garde-fous, sessions, voix et traces; README annonce aussi des fournisseurs compatibles. | MIT; vérifier chaque fournisseur/feature et ne pas supposer que tous les outils sont locaux. |
| [Google ADK Python](https://github.com/google/adk-python) | Framework code-first, évaluation et déploiement d’agents. | Apache-2.0; écosystème multi-langage. |
| [CrewAI](https://github.com/crewAIInc/crewAI) | Définir des équipes d’agents et des tâches collaboratives. | MIT; vérifier que le multi-agent apporte une vraie valeur au cas d’usage. |
| [Hugging Face smolagents](https://github.com/huggingface/smolagents) | Framework Python léger, notamment agents qui planifient/exécutent du code. | Apache-2.0; exécution de code à isoler strictement. |
| [AgentScope](https://github.com/agentscope-ai/agentscope) | Création et débogage d’agents/multi-agents, avec visibilité d’exécution. | Apache-2.0. |
| [LlamaIndex](https://github.com/run-llama/llama_index) | Ingestion de documents, RAG et agents orientés données. | MIT; intéressant si la base de connaissances devient un axe produit. |
| [Haystack](https://github.com/deepset-ai/haystack) | Pipelines d’orchestration/RAG avec contrôles explicites. | Apache-2.0. |
| [Mastra](https://github.com/mastra-ai/mastra) | Framework TypeScript pour agents, workflows, mémoire, MCP, évaluations et human-in-the-loop. | Apache-2.0 hors répertoires `ee/`; inspecter le code utilisé. |
| [BeeAI Framework](https://github.com/i-am-bee/beeai-framework) | Framework d’agents Python et TypeScript. | Apache-2.0. |
| [AutoGen](https://github.com/microsoft/autogen) | Référence historique pour systèmes multi-agents. | Le README le marque **maintenance mode**; nouveaux projets orientés Microsoft → Agent Framework. Licence du repo affichée CC-BY-4.0, à revoir avant copie de code. |
| [OpenHands](https://github.com/OpenHands/OpenHands) | Runtime agent développeur, exploration de code et exécution en sandbox. | MIT; spécialisé code. |

### Modèles locaux, serveurs d’inférence et passerelles

| Repo | Apport | Licence / adéquation |
|---|---|---|
| [Ollama](https://github.com/ollama/ollama) | Télécharger/servir des modèles localement; c’est le chemin déjà prévu par LAPLACE. | MIT pour le logiciel; licence des poids à vérifier modèle par modèle. |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | Inférence quantifiée locale en C/C++, y compris sur matériel limité selon les modèles. | MIT; option bas niveau, nécessite de choisir les poids/quantifications. |
| [LiteLLM](https://github.com/BerriAI/litellm) | Proxy/API unifiée, routage, budgets et compatibilité avec de nombreux fournisseurs. | MIT hors répertoires Enterprise; utile quand les fournisseurs se multiplient, pas obligatoire au MVP. |
| [LocalAI](https://github.com/mudler/LocalAI) | Moteur self-host multimodal : texte, vision, audio et génération selon les backends. | MIT; tester modèles et ressources sur le PC réel. |
| [vLLM](https://github.com/vllm-project/vllm) | Serveur haute capacité/throughput pour GPU et déploiements partagés. | Apache-2.0; probablement disproportionné pour un seul PC avant inventaire matériel. |

### Protocoles, SDK et catalogue d’outils

| Repo | Fonction | Note d’intégration |
|---|---|---|
| [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) | SDK officiel Python client/serveur MCP. | MIT; candidat si backend Python. |
| [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) | SDK officiel TypeScript client/serveur MCP. | Vérifier la licence exacte de la version choisie. |
| [FastMCP](https://github.com/PrefectHQ/fastmcp) | Création rapide de serveurs MCP Python. | Apache-2.0; compare avec le SDK officiel et verrouille la version. |
| [MCP Inspector](https://github.com/modelcontextprotocol/inspector) | Inspecter, tester et déboguer serveurs et clients MCP. | Outil développeur, pas runtime de production; vérifier licence. |
| [MCP Registry](https://github.com/modelcontextprotocol/registry) | Registre communautaire des serveurs MCP. | Catalogue/découverte uniquement; ne vaut pas certification de sécurité. |
| [MCP reference servers](https://github.com/modelcontextprotocol/servers) | Exemples maintenus de serveurs et références de protocole. | Le README les qualifie de **reference implementations**, non prêtes à la production. |
| [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) | Très large index communautaire de serveurs MCP. | Aucune validation globale : auditer code, permissions, dépendances et licence de chaque serveur. |
| [Docker MCP Registry](https://github.com/docker/mcp-registry) | Catalogue Docker de serveurs MCP conteneurisés. | MIT pour le registre; conteneuriser n’est pas suffisant sans profils/seccomp, volumes minimaux et réseau limité. |
| [Composio](https://github.com/ComposioHQ/composio) | Connecteurs d’applications, authentification OAuth/outils et environnement de travail pour agents. | Repo MIT; une partie du service et des intégrations peut impliquer des services externes. Revue confidentialité requise. |
| [mcp-use](https://github.com/mcp-use/mcp-use) | Framework full-stack pour clients MCP, outils et apps MCP. | MIT; alternative de haut niveau au SDK brut. |
| [Agent2Agent / A2A](https://github.com/a2aproject/A2A) | Protocole d’interopérabilité entre agents/services distincts. | Apache-2.0; à ajouter lorsque Carré d’As doit déléguer à des agents distants. |
| [AG-UI](https://github.com/ag-ui-protocol/ag-ui) | Protocole événementiel agent ↔ application front-end. | MIT; utile pour streaming d’étapes, états et validations humaines. |
| [CopilotKit](https://github.com/CopilotKit/CopilotKit) | SDK UI d’agents, état partagé et human-in-the-loop pour React/Angular et autres surfaces. | MIT; dépend du front-end réel de Carré d’As. |

### Navigateur et actions sur le poste

| Repo | Capacités | Limite/sécurité |
|---|---|---|
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) | Pilotage du navigateur par arbre d’accessibilité et outils structurés. | Bon premier POC navigateur; ne contrôle pas automatiquement toutes les fenêtres natives du PC. |
| [Playwright CLI](https://github.com/microsoft/playwright-cli) | Commandes CLI et génération de code Playwright. | Le README recommande parfois CLI/skills pour les agents de code; MCP reste utile pour état navigateur persistant. |
| [Browser Use](https://github.com/browser-use/browser-use) | Agent/browser automation en langage naturel. | MIT; plus autonome/variable que Playwright déterministe, prévoir domaine autorisé, comptes de test et confirmation avant actions irréversibles. |
| [Stagehand](https://github.com/browserbase/stagehand) | SDK navigateur pour extraction et interactions assistées par IA. | MIT pour le repo; valider les fonctions de service/hébergement utilisées. |
| [Skyvern](https://github.com/Skyvern-AI/skyvern) | Automatisation de workflows web basés sur navigateur. | AGPL-3.0; examiner obligations d’intégration/service. |
| [Open Interpreter](https://github.com/OpenInterpreter/open-interpreter) | Agent local avec exécution de commandes, code et outils. | Apache-2.0; puissant mais trop permissif sans sandbox et approvals. |
| [UI-TARS Desktop](https://github.com/bytedance/UI-TARS-desktop) | Stack multimodale d’utilisation d’ordinateur/GUI. | Apache-2.0; vérifier OS, compatibilité du modèle et l’isolation. |
| [Agent Zero](https://github.com/agent0ai/agent-zero) | Bureau Linux complet et outils ordinateur pour agents. | Licence à éclaircir; ne pas exposer d’accès host ou shell par défaut. |

### Mémoire, connaissance et recherche

| Repo | Usage potentiel | Choix de prudence |
|---|---|---|
| [Letta](https://github.com/letta-ai/letta) | Runtime d’agents stateful et mémoire durable. | Apache-2.0; évaluer scopes, export/suppression et coût d’exploitation. |
| [Mem0](https://github.com/mem0ai/mem0) | Couche de mémoire persistante réutilisable par plusieurs agents. | Apache-2.0; exiger une clé de partition `workspace/user/guild` et une politique explicite de partage. |
| [Cognee](https://github.com/topoteretes/cognee) | Mémoire et graphes de connaissance pour agents, y compris modèles compacts. | Apache-2.0; utile si une mémoire relationnelle justifie plus que SQLite. |
| [Graphiti](https://github.com/getzep/graphiti) | Graphes de connaissances temporels et actualisés. | Apache-2.0; charge et complexité supérieures à une mémoire simple. |
| [Chroma](https://github.com/chroma-core/chroma) | Stockage/recherche vectorielle. | Apache-2.0; embeddings et vecteurs ne remplacent pas les règles d’accès source. |
| [Qdrant](https://github.com/qdrant/qdrant) | Base vectorielle scalable. | Apache-2.0; probablement inutile avant besoin concret de recherche sémantique. |
| [pgvector](https://github.com/pgvector/pgvector) | Recherche vectorielle dans PostgreSQL existant. | PostgreSQL License (SPDX non détecté par GitHub); réduit un service séparé si Carré d’As utilise déjà Postgres. |
| [Memvid](https://github.com/memvid/memvid) | Mémoire d’agent emballée dans un format local/portable. | Apache-2.0; comparer les garanties et le modèle de mise à jour avant données sensibles. |

### Traces, évaluations, qualité et politiques

| Repo | Usage potentiel | Licence / note |
|---|---|---|
| [Langfuse](https://github.com/langfuse/langfuse) | Traces, prompts versionnés, tests/évaluations et débogage; self-host. | MIT hors répertoires Enterprise; masque/redacts données avant traces. |
| [Promptfoo](https://github.com/promptfoo/promptfoo) | Tests comparatifs, suites de régression et red-teaming des prompts/agents. | MIT; adapté au CI de chaque version d’agent. |
| [DeepEval](https://github.com/confident-ai/deepeval) | Évaluations automatiques et métriques d’applications LLM. | Apache-2.0; valider les métriques sur un jeu d’essai humain. |
| [LangWatch](https://github.com/langwatch/langwatch) | Observabilité, tests, gouvernance et évaluations d’agents. | Apache-2.0; comparer à Langfuse pour éviter deux pipelines. |
| [MLflow](https://github.com/mlflow/mlflow) | Cycle de vie, suivi et évaluation de modèles/agents. | Apache-2.0; plus large et plus lourd qu’un simple outil de traces. |
| [Arize Phoenix](https://github.com/Arize-ai/phoenix) | Observabilité, expérimentation, évaluation et debugging. | Elastic License 2.0; interdit notamment de fournir un service hébergé/managed concurrent. |
| [AgentOps](https://github.com/AgentOps-AI/agentops) | Tracing et coûts pour plusieurs frameworks d’agents. | MIT; examiner la destination des traces et l’activité du SDK. |
| [Guardrails AI](https://github.com/guardrails-ai/guardrails) | Valider/contraindre les entrées et sorties des modèles. | Apache-2.0; ne remplace ni les autorisations d’outils ni les tests d’injection. |
| [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) | Politiques programmables de conversation et garde-fous. | Vérifier les licences des paquets/composants avant usage. |
| [Ragas](https://github.com/vibrantlabsai/ragas) | Évaluation RAG et réponses fondées sur des sources. | Apache-2.0; le dernier push vu par l’API était plus ancien que les autres repos de la shortlist, vérifier l’activité. |
| [Open Policy Agent](https://github.com/open-policy-agent/opa) | Politiques d’autorisation déclaratives pour outils et actions. | Apache-2.0; envisager seulement si des règles centralisées deviennent nécessaires. |
| [LLM Guard](https://github.com/protectai/llm-guard) | Ancien toolkit de sécurité des entrées/sorties. | **Repo archivé** au jour de la veille; ne pas en faire le choix par défaut. |

### Audio, voix et temps réel multimodal

| Repo | Usage potentiel | Licence / note |
|---|---|---|
| [LiveKit Agents](https://github.com/livekit/agents) | Agents voix temps réel, audio/vidéo et transport de sessions. | Apache-2.0; distinct d’un bot Discord répondant par fichier audio. |
| [whisper.cpp](https://github.com/ggml-org/whisper.cpp) | Transcription locale optimisée. | MIT; poids Whisper et configuration à gérer séparément. |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | STT rapide par CTranslate2. | MIT; mesurer RAM/VRAM sur le PC visé. |
| [Piper](https://github.com/OHF-Voice/piper1-gpl) | TTS local léger et voix françaises disponibles. | Moteur GPL-3.0; licences des voix/poids séparées. |
| [Kokoro](https://github.com/hexgrad/kokoro) | TTS multilingue compact. | Repo Apache-2.0; licence des poids/voix et qualité du français à valider. |

## Architecture cible pour Carré d’As

### Deux surfaces, un catalogue d’agents

- **Console propriétaire (`/admin/agents`)** : créer/cloner un agent, choisir fournisseur/modèle, éditer les instructions, sélectionner des outils approuvés, régler mémoire/confidentialité, tester, publier, versionner et revenir en arrière.
- **Espace utilisateur** : utiliser uniquement les agents publiés auxquels il a accès; ne pas exposer les clés, le prompt système complet, les outils d’administration ou les paramètres de sécurité.
- **Runtime séparé de l’UI** : API interne stable; LAPLACE/Discord devient un premier canal/adaptateur possible après que Carré d’As ait exposé son vrai contrat.
- **Compagnon local séparé** pour navigateur/fenêtres/fichiers; l’interface web distante ne doit pas appeler directement `localhost` côté navigateur ni recevoir un shell libre.

### Définition versionnée d’un agent

À conserver comme configuration déclarative, validée par schéma, plutôt que code libre dans une zone de texte :

```yaml
schema_version: 1
id: laplace-discord
version: 1
status: draft # draft -> tested -> published -> retired
model:
  provider: ollama
  model_id: ${MODEL_FROM_LOCAL_CONFIG}
  endpoint_ref: local-ollama
  credential_ref: null # une clé API serait un secret référencé, jamais une valeur UI/Git
instructions_ref: prompts/laplace/v1
channels: [discord]
tools:
  - id: approved-browser-read
    scope: read_only
    require_confirmation: false
memory:
  personal: explicit_opt_in
  shared_scope: guild_id
  retention_days: 30
approvals:
  file_write: always
  send_message: always
```

Le modèle exact, la température, les limites de tokens, les budgets, les fournisseurs et les canaux doivent être configurables par profil. Les secrets restent dans le stockage secret du serveur/PC et ne sont montrés qu’au moment de saisie; ne pas les sérialiser dans une définition exportable. Le YAML ci-dessus est illustratif, pas encore un schéma implémenté.

### Modèle d’autorisations minimal

- **Principal** : propriétaire/admin, utilisateur, agent/service.
- **Portée de données** : `tenant/workspace_id`, `user_id`, `guild_id`, `channel_id`, `session_id`; chaque requête porte explicitement les scopes pertinents.
- **Outil** : identifiant et version, JSON Schema des paramètres, permissions réseau, scopes OAuth, durée maximale, limites d’appels, niveau de risque, sandbox et exigence de confirmation.
- **Cycle de vie** : draft non exécutable par les utilisateurs → tests en bac à sable → publication autorisée → audit/version précédente → rollback.
- **Par défaut** : aucun outil activé, aucune mémoire commune, aucun accès au système de fichiers, aucune action d’écriture sans confirmation.

MCP peut rendre des outils portables, mais chaque serveur MCP reste un plugin exécutable qui peut lire ou modifier des données. Épingler les versions, auditer le code et les permissions, isoler l’exécution, filtrer réseau/volumes et journaliser les appels sans consigner secrets ni contenu complet par défaut.

## Démarche proposée, sans choisir encore de framework

1. Retrouver le dépôt Carré d’As et la branche/PR de l’autre travail en cours; lire sa stack, son modèle utilisateur et son API avant d’ajouter un second système.
2. Définir avec le propriétaire le périmètre du hub : un seul compte privé ou plusieurs utilisateurs/espaces? PC local uniquement ou services distants? Quels droits d’administration?
3. Prototyper la console propriétaire avec des profils **sans outil d’action**, fournisseurs factices/Ollama, versions de prompt, tests et publication.
4. Exposer les profils par un schéma API et connecter un seul agent pilote (LAPLACE) sans coupler le modèle métier à Discord.
5. Ajouter la passerelle de modèles seulement si nécessaire, puis MCP en lecture seule, puis approbations explicites pour les écritures.
6. Ajouter traces/évaluations; un agent ne passe de brouillon à publié que si les jeux de tests et permissions sont validés.
7. Tester le navigateur avec un compte/site de test; n’activer l’ordinateur complet qu’après choix OS/matériel et conception d’un compagnon local isolé.

## Éléments manquants avant intégration réelle

- URL ou chemin du dépôt Carré d’As dans ce monorepo, branche active ou contrat du travail de l’autre agent.
- Stack/version, mode de déploiement, authentification, modèle de données et routes API existantes.
- Est-ce que le studio sert uniquement le propriétaire, ou également des clients/espaces distincts? Cette réponse change la licence acceptable et les frontières multi-tenant.
- OS, RAM/VRAM et modèles `ollama list` du PC; fournisseur local/externe souhaité.
- Les médias doivent-ils être **analysés**, **générés**, ou les deux? Voix en fichier ou connexion à un salon vocal? Actions locales exactes à autoriser?

Aucun secret n’est requis pour cette phase; ne pas coller token Discord, clé API, cookie ou mot de passe dans le dépôt ou la conversation.
