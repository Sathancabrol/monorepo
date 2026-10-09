# 🕵️ VEILLE — « Clones open source de logiciels payants » & IA reverse-engineering (09/10/2026)

> **Demande** : checker la tendance modding/décompilation qui crée des versions open source de logiciels payants (ex. getartcraft.com, WareTrack), rester à jour sur les outils IA des réseaux, et identifier l'utile pour nous.
> **Réponse courte** : la tendance réelle n'est PAS le cracking — c'est la **réimplémentation open source propre** de logiciels payants, accélérée par les agents IA. C'est exactement notre philosophie (Postiz = clone de Buffer, etc.). Deux exemples étudiés ci-dessous + 5 retombées concrètes pour nous.

---

## 1. ⚖️ Le cadre avant tout (ce qui est jouable / ce qui ne l'est pas)

| Pratique | Légalité | Notre position |
|---|---|---|
| **Clone clean-room** : étudier le comportement d'un produit payant et le réécrire de zéro avec son propre code + licence OSS | ✅ légal (idées/fonctions ne sont pas protégées, l'expression du code l'est) | ✅ c'est notre méthode (Postiz, etc.) |
| **Interopérabilité** : décompiler UNIQUEMENT pour l'interop, conditions strictes (info non obtenible autrement, partie strictement nécessaire) | ✅ encadré (dir. UE 2009/24/CE art. 6 ; CPI L122-6-1) | au cas par cas, documenté |
| **Cracking / redistribution de binaires propriétaires décompilés** | ❌ interdit (contournement de mesures techniques : DMCA §1201, CPI) | ❌ jamais — hors scope |

## 2. 🔍 Les deux exemples cités

**ArtCraft (getartcraft.com)** — ce n'est PAS un outil de décompilation : c'est **le clone open source des agrégateurs payants d'IA créative** (Krea/Freepik/MidJourney-web). Studio desktop Tauri + web (`github.com/storytold/artcraft`), slogan « Stop renting from websites » : BYO-API-keys (MidJourney, Sora, Grok, Seedance 2.5, Nano Banana 2, WorldLabs), contrôle artistique réel (posing, compositing 2D/3D, image→location, gaussians splats), 8 apps (PhotoCraft, FilmCraft, VectorCraft…). Communauté : Discord 5 455, chaîne YouTube, streams Twitch. → **Modèle économique étudié : le logiciel est gratuit, ils vendent l'accès web/support** [1](https://getartcraft.com/)[2](https://www.reddit.com/r/tauri/comments/1rlpoao/artcraft_open_source_tauri_ai_film_studio/).

**WareTrack** — le buzz X du 05/10/2026 : un dev a construit un **WMS 3D gamifié** (« ressemble plus à un jeu de stratégie qu'à un ERP ») avec **Claude Opus + React Three Fiber** : chariots animés, tracking temps réel, hubs multiples — « l'emprunt des mécaniques de jeu au logiciel industriel » [3](https://x.com/DamiDefi/status/2107084891682988445). Dans la même veine : `manziosee/WareTrack-Pro` (WMS complet TS/React/Node/Postgres, 75+ endpoints, Docker) et `F0zzi4/WareTrackX` (mini-ERP .NET dérivé d'un projet open source existant). → **Le vrai signal : les logiciels d'entreprise ennuyeux se font répliquer/embellir par IA en quelques jours.**

## 3. 🛠 L'outillage IA de reverse-engineering (état de l'art, pour info)

| Outil | Ce que c'est | Usage légitime |
|---|---|---|
| **Ghidra** (NSA, Apache-2.0, ~70k★) | décompilateur multi-architectures gratuit rival d'IDA Pro (1 800-6 500 €/an) | analyse sécurité, interop, audit de binaires qu'on possède [4](https://appsecsanta.com/ghidra) |
| **GhidraMCP** (LaurieWired) | expose Ghidra aux LLM via MCP (décompilation/renommage/rapports en langage naturel) | tri de malwares, recherche [5](https://converter.brightcoding.dev/blog/ghidramcp-ai-powered-reverse-engineering-revolution) |
| **GhidrAI / Gepetto / DecompAI / LLM4Decompile-9B** | plugins & modèles LLM pour annoter/améliorer le pseudo-code (local via Ollama possible) | analyse confidentielle locale [6](https://ayinedjimi-consultants.fr/articles/ia-reverse-engineering-malware) |
| **CAPA** (Apache-2.0) | mapping MITRE ATT&CK automatisé (87 %) | rapports sécurité |

→ Utile pour nous seulement si un besoin d'interop/sécurité surgit ; **pas d'usage cracking**.

## 4. 📡 Tendances réseaux repérées (octobre 2026)

1. **IA « agente » partout** : Meta a racheté **Manus** (navigation web autonome) pour l'intégrer à WhatsApp/Instagram — les clients délégueront leurs achats à des assistants [7](https://wordpress.com/fr/go/marketing-digital/tendances-reseaux-sociaux-2026/). Validation directe de notre pari agentique.
2. **GEO (Generative Engine Optimization)** : le SEO devient « être cité par les assistants IA » ; Gartner prévoit ~25 % des recherches via moteurs IA — nouvelle discipline marketing [8](https://jixart.fr/blog/tendances-reseaux-sociaux-2026/).
3. **Bluesky** : la plateforme la plus favorable aux petits comptes (< 100k abonnés y génèrent plus d'engagement que sur X) [7](https://wordpress.com/fr/go/marketing-digital/tendances-reseaux-sociaux-2026/) → à ajouter à notre calendrier.
4. **71 % des marketers utilisent l'IA quotidiennement** (idéation, rédaction, planning, reporting) [9](https://www.oulaoups.com/tendances-reseaux-sociaux-2026/) — notre équipe `social` est dans la norme des pros.
5. **Gamification du logiciel pro** (WareTrack) : angle produit différenciant pour les nichées industrielles.

## 5. 🎯 Ce qui est utile pour NOUS (en plus de l'existant)

| # | Retombée | Où ça s'accroche | Action |
|---|---|---|---|
| 1 | **ArtCraft** pour les visuels/vidéos des offres et de l'Outsider (M3) — gratuit, open source, BYO-clés | piste D créative + `social` (visuels des posts) | installer le jour où une clé vidéo/image existe ; repo à suivre |
| 2 | **Le pattern WareTrack pour O3** : suivi de chantier gamifié/3D — watchtower (globe 3D voix FR) + dossier BTP 220 fichiers = on a déjà les deux moitiés | offre O3 différenciée | à proposer en démo si le test Sobeca accroche |
| 3 | **GEO** : rendre les offres citables par les assistants IA | `social check` (nouvelle ligne de checklist) | fait dans ce commit |
| 4 | **Bluesky** dans les plateformes cibles | `social` (plateforme ajoutée, limite 300 car.) | fait dans ce commit |
| 5 | Méthode « clone propre » assumée comme positionnement | argumentaire des offres | « on construit l'équivalent open source de vos abonnements » — pitch anti-Gartner-70 % |

**Ne pas adopter** : le cracking/décompilation de logiciels propriétaires (illégal, et sans intérêt business pour nous).

---
*Sources vérifiées le 09/10/2026. Cadre légal = information générale, pas un avis juridique.*
