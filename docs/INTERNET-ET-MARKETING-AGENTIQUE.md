# 🌍 CONNEXION INTERNET + ÉQUIPE MARKETING/RÉSEAUX — pour le système agentique

> **Demande** (09/10/2026) : des outils pour que l'app/système se connecte à internet et fasse des recherches *selon la méthode choisie* ; une équipe marketing/réseaux sociaux IA qui gère et fait de la recherche ; analyse de la méthodologie du reel de Jake Van Clief (@lostandlucky).

---

## 1. 🌐 Couche internet — « donner des yeux et des mains » au système

| Besoin | Outil recommandé | Chiffres/licence | Pourquoi lui |
|---|---|---|---|
| **Recherche web (requête → sources)** | **Tavily** | 1 000 crédits/mois gratuits, 0,008 $/crédit ensuite [1](https://brightdata.com/blog/ai/firecrawl-alternatives) | faite POUR les agents ; moteur par défaut de GPT-Researcher et Open Deep Research |
| **URL → markdown propre (lecture)** | **Jina Reader** (10 M tokens gratuits) ou **Crawl4AI** | Crawl4AI 58-78k★ Apache-2.0, local-first, Ollama, filtre BM25 [2](https://www.firecrawl.dev/blog/best-open-source-web-crawler) | Crawl4AI = zéro coût par page, données restent en local (fit privacy + budget) |
| **Aspiration de sites entiers** | **Firecrawl** (self-host Docker) | 70k+★, markdown/JSON, extraction LLM, respecte robots.txt [2](https://www.firecrawl.dev/blog/best-open-source-web-crawler) | pour les gros dossiers (docs agglo, sites mairies — offres O2) |
| **Navigateur piloté par l'agent** | **Playwright MCP** (Microsoft) | 37,8k★ Apache-2.0, lit l'arbre d'accessibilité (pas de pixels) [3](https://agentscamp.com/guides/comparations/browser-agents-compared-2026) | « la réponse par défaut dans un harness » ; complémentaire d'**Obscura** (28,7k★, déjà audité) pour les pages légères |
| **Tâches autonomes dans le navigateur** | **browser-use** | ~114-117k★ MIT, 72-78 % de réussite selon modèle [3](https://agentscamp.com/guides/comparations/browser-agents-compared-2026)[4](https://www.nxcode.io/resources/news/stagehand-vs-browser-use-vs-playwright-ai-browser-automation-2026) | « phrase en entrée, résultat en sortie » ; à sandboxer (considéré non fiable par défaut) |
| **Recherche 100 % locale** | **Local Deep Research + SearXNG** | déjà embarqué dans watchtower (stack docker) | rien ne sort de la machine ; gratuit |

### Routeur de méthodes de recherche (« selon méthode choisie »)
Le service `research` choisit la méthode selon la question :

| Type de question | Méthode | Outil |
|---|---|---|
| « Fais-moi un état de l'art / rapport sourcé » | rapport multi-agents parallèles | GPT-Researcher (Tavily) |
| « Surveille ce sujet en continu, sans cloud » | veille locale | Local Deep Research + SearXNG (watchtower) |
| « Vérifie une affirmation précise » | contradiction + vérification | **reaserch-engine** (notre couche unique) |
| « Lis cette page / ce document en ligne » | URL → markdown | Jina Reader / Crawl4AI / Obscura |
| « Va interagir avec ce site (formulaire, compte) » | navigateur agentique | browser-use / Playwright MCP |
| « Plan encyclopédique multi-points-de-vue » | interviews simulées | STORM (à ré-évaluer, peu maintenu) |

## 2. 📣 L'équipe marketing/réseaux — outillage existant

**La pièce maîtresse : [Postiz](https://github.com/gitroomhq/postiz-app)** (Apache-2.0) — Buffer/Hootsuite open source : 25-30+ plateformes (Instagram, Facebook, X, LinkedIn, TikTok, Reddit, YouTube, Threads, Mastodon…), copilotes IA, analytics, équipe, **API publique + endpoint MCP (`/api/mcp/{API_KEY}`) + agent de création de posts**, compatible n8n/Make/Zapier, tourne sur un serveur à ~5 $/mois [5](https://railway.com/deploy/postiz-open-source-social-media-scheduler-for-30-platforms--deploy-postiz).
**L'équipe-type open source** (vue sur un workflow réel d'indépendant) : n8n (planification) → recherche de tendances (Perplexity/naviro) → création par modèles locaux FOSS → **Postiz** (publication) [6](https://www.reddit.com/r/selfhosted/comments/1fl8n2b/postiz_v130_opensource_social_media_scheduling_tool/).

**Écoute sociale / recherche sur les réseaux** : les outils pros (Brandwatch, Meltwater, Talkwalker, Brand24 dès 199 $/mois) sont hors budget ; l'alternative gratuite = **Google Alerts** (gratuit) + **AnswerThePublic** (3 recherches/jour gratuites) + requêtes Reddit/X/YouTube pilotées par browser-use + méthode « 2 sources minimum » déjà dans nos leçons [7](https://brand24.com/blog/social-listening-tools/). Swello (FR, 9,99 €/mois) si petit budget un jour [8](https://iaproductive.fr/les-meilleurs-outils-ia-pour-gerer-les-reseaux-sociaux-en-2026-comparatif-recommandations/).

**Organigramme de l'équipe marketing** (rôles = dossiers, pas humains) :
```
ÉQUIPE MARKETING (agent-office/social)
├── RÉDACTEUR   — drafts par plateforme (service social draft)
├── ÉDITEUR     — porte de revue humaine (checklist social check) ← JAMAIS publié sans
├── PUBLISHER   — Postiz MCP (quand hébergé) ou export manuel
├── ÉCOUTEUR    — social listen : requêtes de veille par plateforme
└── ANALYSTE    — arena : quel post gagne en aveugle avant publication
```

## 3. 🎬 Méthodologie Jake Van Clief — analyse et comparaison avec nous

Transcript complet : [`docs/transcripts/JAKE-LOSTANDLUCKY-agent-naming-convention.md`](transcripts/JAKE-LOSTANDLUCKY-agent-naming-convention.md). Son framework : **agent = instructions (possédées) + modèle (loué, interchangeable) + portée (fichiers+outils)** ; le harness fait la boucle (« la roue est finie ») ; preuve de Dubaï : *même brief, deux modèles différents, ça marche → ce qui a de la valeur ce sont les instructions* ; Gartner : jusqu'à 70 % des projets agents « vendor-built » abandonnés d'ici 2028 (coûts, valeur floue, risque).

| Son principe | Notre équivalent | État |
|---|---|---|
| Ne jamais reconstruire la roue (harness) | on n'a PAS construit de harness : Claude Code/Arena + litellm retenus | ✅ conforme |
| Posséder les INSTRUCTIONS | README, CAPABILITY de chaque service, briefs USER/TELOS, docs méthode | ✅ notre actif principal |
| Modèle loué interchangeable | routeur litellm + `arena` qui mesure le gagnant par catégorie | ✅ prêt, sans clés |
| La PORTÉE (ce que l'IA peut toucher) | tools.json + connecteurs Gmail/Drive/Notion/Linear | ⚠️ **LE trou : internet + réseaux** → ce doc |
| Porte de vérification humaine | revue utilisateur + `arena judge` + garde-fou `update check` | ✅ discipline |
| 1 dossier = 1 agent | ICM Van Clief (même auteur, arXiv) = arborescence comme architecture | ✅ validé par la source |
| Fuir les agents vendor (Gartner 70 %) | 100 % open source assemblé, zéro abonnement | ✅ conforme |

**Conclusion : le reel décrit exactement ce qu'on fait déjà — et pointe précisément ce qui manque : la portée internet.** Ses 4 questions (outcome / how / touch / human-check) deviennent notre standard de dossier.

## 4. ✅ Implémenté ce tour + prochaine étape

- **Service `social`** dans agent-office (11ᵉ) : calendrier éditorial, drafts par plateforme avec limites réelles, checklist de publication (porte humaine), méthode d'écoute sociale hors-ligne.
- **Prochaine étape (quand hébergement dispo)** : Postiz en docker + Tavily free tier + Crawl4AI ; chaque nouveau « agent » = un dossier aux 4 questions de Jake.

---
*Sources vérifiées le 09/10/2026. Complète : AUTO-MAJ-SYSTEME-AGENTIQUE.md (veille), SYSTEMES-CONFRONTATION-MODELES.md (arena), SYSTEME-COMBINE-IA.md (harness).*
