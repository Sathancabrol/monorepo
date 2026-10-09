# 🧠 VEILLE — « AI Agent + SQLite + Knowledge Graph sur VPS » (vidéo, 09/10/2026)

> **Concept de la vidéo** : un agent IA + SQLite + graphe de connaissances hébergé sur VPS ; thèse : il faudra **générer du logiciel à la demande pour concourir aux jobs et au revenu** ; métaphore Fortnite : on génère des « builds » pour survivre et concourir.
> **Verdict : oui, utile — et la vidéo décrit littéralement notre trajectoire.** Décisions ci-dessous.

---

## 1. 🪞 Miroir : la vidéo décrit ce qu'on fait déjà

| Concept vidéo | Notre équivalent existant |
|---|---|
| Générer du logiciel à la demande pour concourir | agent-office (11 services générés en une nuit), clones propres (ArtCraft/WareTrack), offres O1/O2/O3 |
| « Builds » Fortnite pour survivre/concourir | boucle arena (duels + ELO) + pattern Darwin Gödel Machine (archive de variants validés empiriquement) — déjà documentés |
| Agent qui travaille 24/7 | ce qui nous manque aujourd'hui (le sandbox n'est pas permanent) → la vraie question = où l'agent vit |

## 2. 🧱 Les 3 briques de la vidéo, traduites pour nous

**SQLite — MAINTENANT** (coût 0, stdlib Python) : notre mémoire agent était en fichiers JSON/CSV épars ; SQLite la rend requêtable et durable. proto-cognitorium avait déjà un DDL SQLite 12 tables — la compétence est déjà dans le monorepo. → **implémenté ce tour : service `knowledge`** (base unique, ingestion de toutes nos données, graphe de connaissances).

**Knowledge graph — MAINTENANT** : le graphe Cognitorium existe déjà en design (prompts AI Studio « Graphe Cognitif », graphe D3 99 nœuds/137 liens d'ETAT-DE-LART). Le service `knowledge` en pose la première version opérationnelle : nœuds (offres, prospects, modèles, sources, leçons) + arêtes (vise, jugé-par, cite, appris-de).

**VPS — PLUS TARD, sous condition** :

| Pour quoi faire | Hébergement | Coût |
|---|---|---|
| Portail `app/` visible en ligne (vitrine des offres) | VPS starter | ~4-6 €/mois |
| Postiz docker (publication réseaux) + SearXNG (veille) | idem | inclus |
| Agent 24/7 (cron veille → brief → digest mail) | idem | inclus |
| Tavily/appels LLM | peu importe où | crédits API |

**Décision : pas avant le 1ᵉʳ revenu** (le déficit est de −111,51 €/mois ; 5 € de plus n'est justifié que quand il sert à en gagner). Les 3 offres O1/O2/O3 se testent **sans VPS** — un laptop suffit. Le VPS devient l'étape « industrialisation » après J+30 si une piste mord. Budget cible : Hetzner/OVH starter ≤ 6 €/mois, jamais plus sans revenu en face.

## 3. ✅ Livré ce tour

- `knowledge` (12ᵉ service agent-office) : `init`, `ingest` (aspire prospects/budget/ELO/leçons/citations dans la base), `graph`, `query` — SQLite + tables nœuds/arêtes, stdlib uniquement.
- Cette doc = décision VPS consignée (condition : 1ᵉʳ revenu).

---
*09/10/2026 · complète AUTO-MAJ-SYSTEME-AGENTIQUE.md (mémoire Letta/fichiers → SQLite+graphe) et SYNTHESE-GLOBALE-09-10.md.*
