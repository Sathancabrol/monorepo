# 🔑 Obtenir des clés API de modèles IA SANS payer (09/10/2026)

> **Contexte** : budget à −111,51 €/mois, règle « pas de dépense avant le 1ᵉʳ revenu ». Nos systèmes (`arena`, le futur routage OmniRoute, les agents) ont besoin de modèles — voici où trouver des clés **gratuites**, dans quel ordre, et leurs vraies limites.
> **Principe** : on **empile** les free tiers (aucun seul ne suffit), on ne s'abonne à rien.

---

## 1. 🥇 Le stack recommandé (ordre d'activation)

| # | Fournisseur | Comment | Gratuit tant que | Pour quoi chez nous |
|---|---|---|---|---|
| 1 | **GitHub Models** | Déjà un compte GitHub ! Un simple PAT suffit | ~150 req/jour (petits modèles), ~50 req/jour (GPT-4o/o3), 8K tokens en entrée | juges `arena`, tests rapides de prompts |
| 2 | **Mistral La Plateforme** (plan « Experiment ») | console.mistral.ai, sans carte (vérif SMS) | ~1 Md de tokens/mois, débit faible (~2 req/min) | **fournisseur principal des livrables clients** : entreprise française, données UE, garantie contractuelle non-entraînement sur l'API |
| 3 | **Google AI Studio** (Gemini Flash) | ai.google.dev avec un compte Google | ~1 500 req/jour (quotas resserrés en 2026) | le gros volume quotidien (drafts, digests, veille) ⚠️ le tier gratuit peut servir à entraîner leurs produits → pas de données clients sensibles |
| 4 | **Groq** ou **Cerebras** | inscription, sans carte | Groq : des milliers de req/jour sur Llama ; Cerebras ~1 Md tokens/jour | inférence rapide et bon marché pour les tâches répétitives |
| 5 | **Hugging Face** | token gratuit hf.co | **0,10 $/mois de crédit** (routeur vers les fournisseurs partenaires) + Hub API ~1 000 appels/jour | dépannage, petits modèles ouverts, embeddings — le crédit est minuscule, c'est un complément |
| 6 | **OpenRouter** (modèles `:free`) | openrouter.ai, sans carte | variantes gratuites limitées (~50 req/jour sans crédit) | accès ponctuel à d'autres modèles pour les duels `arena` |

**Total empilé : plusieurs milliers de requêtes/jour pour 0 €.** Largement suffisant pour faire tourner arena, les drafts et les premiers livrables clients.

## 2. 📋 À vérifier avant usage (honnête)

- **Usage commercial** : GitHub Models gratuit = usage commercial conditionné à un plan Azure payant. Pour les livrables clients, préférer **Mistral** (API = pas d'entraînement, UE) ou un tier payant plus tard, après le 1ᵉʳ revenu.
- **Données** : tiers gratuit Google = les prompts peuvent entraîner leurs modèles (documenté). Règle : jamais de données client/privées sur les tiers gratuits d'entraînement ; Mistral API a une garantie contractuelle contraire.
- **Les free tiers OAuth « détournés »** (ex. comptes Gemini CLI via OmniRoute) : zone grise côté CGU — on évite tant qu'on n'a pas lu les conditions du fournisseur.
- **Sécurité des clés** : chaque clé va dans `projects/agent-office/.env` (fichier **gitignoré**, jamais commité) — jamais dans le code ni dans un doc.

## 3. 🗺 Ce que ça débloque dans notre système

1. Dès 2-3 clés activées → brancher `arena` en vrai : duels entre GPT (GitHub) × Mistral × Gemini (duels en aveugle + ELO déjà prêts dans le service).
2. Le jour où une clé payante/abonnement arrive → **OmniRoute** devient la couche unique sous `arena` et le portail `app/` (fallback abonnement → gratuit, voir `docs/AGENT-OS-ET-AGENCY-VEILLE.md` §4).
3. Les « juges » des **QA gates** (fiches agents) peuvent être des petits modèles dédiés quasi gratuits — voir actualités ci-dessous.

---

## 4. 📰 Actualités IA utiles cette semaine (01→09/10/2026)

| Annonce | Pourquoi c'est utile pour nous |
|---|---|
| **Mistral Large 4** en préversion (06/10) — ~1 000 Md de paramètres (49 Md actifs), multimodal, entraîné en Europe ; poids promis fin octobre | 🇫🇷 le champion français remonte (index 38 vs 9 pour Large 3). À tester via le plan Experiment dès que dispo — argument « IA française/UE » pour les offres O1/O2 |
| **Cloudflare Clef / Clef-flash** (01/10, Apache 2.0) — modèles de **décision** : sorties typées + probabilités, sans blabla | Parfait pour nos **gates QA et arbitrages** : un verdict structuré à très bas coût (Workers AI ≈ 10 000 « neurons »/jour gratuits). Patron à copier dans arena |
| **Amazon Strands Decider 2B** (01/10, Apache 2.0) — modèle de décision local CPU | Idem, version 100 % locale si un VPS arrive |
| **Index-Translate-35B** (Apache 2.0, 150 langues) | Traduction gratuite des livrables/prospects |
| **LTX-2.5** vidéo sur Hugging Face | Déjà supporté par Wan2GP — conforte le choix d'atelier vidéo (quand GPU) |
| Rumeur **Claude Haiku 5.5** avant le 15/10 ; **GPT-6 Luna** à ~0,07 $/tâche | La classe « pas cher et rapide » devient viable pour des agents 24/7 — à re-chiffrer au moment du VPS |
| **OpenClaw Enterprise** (01/10) — « Kubernetes pour agents », plan de contrôle gratuit | Veille : orchestration multi-agents gratuite si notre org grandit |
| À éviter : sites qui vendent de fausses « installations Wan2GP », agrégateurs de free tiers OAuth douteux | On reste sur les canaux officiels |

---

## 5. ✅ Checklist pour Nathan (15 min, zéro euro)

1. GitHub → Settings → Developer settings → **Personal access token** (accès Models) → tester dans le playground github.com/marketplace/models.
2. console.mistral.ai → compte → plan **Experiment** → clé API.
3. ai.google.dev → clé API Gemini (compte Google existant).
4. (optionnel) Groq + Cerebras + token Hugging Face.
5. Mettre les clés dans `projects/agent-office/.env` (jamais dans git) → on branche `arena`.

*09/10/2026 — sources : revues spécialisées free-tiers 2026, docs fournisseurs, presse tech IA de la semaine.*
