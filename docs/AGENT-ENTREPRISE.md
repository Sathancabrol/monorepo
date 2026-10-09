# 🏢 AGENT-ENTREPRISE — l'IA qui fait la bureautique

> **Vision** : une entreprise d'IA où l'agent (Laplace) exécute le maximum de travail de bureau — mails, budget, marketing, recherche, prospection, planning, facturation — en s'appuyant **uniquement sur des actifs existants** du monorepo. Document enrichi après les audits `AUDIT-ACTIFS-COMPLET.md`, `SYSTEME-COMBINE-IA.md`, `BENCHMARK-HARNESS-2026.md`.

## 1. L'organigramme de l'entreprise

```
DIRECTION — registry (tools.json) : qui sait faire quoi, doctor = contrôle qualité
├── FINANCE      — budget (déficit réel suivi), invoices (devis/factures conformes)
├── COURRIER     — mail digest (lecture seule) + mail-organizer (tri réel, déjà livré)
├── MARKETING    — one-pagers / séquences / posts des offres O1·O2·O3
├── PROSPECTION  — prospects (pipeline cible→gagné, relances dues)
├── RECHERCHE    — research briefs/citations/veille → reaserch-engine
├── ORGANISATION — planning week/add/ics → Google Calendar
├── ARBITRAGE    — arena : duels en aveugle, ELO, grille ChatEval (jamais un seul juge)
├── ÉVOLUTION    — update : journal des mises à jour, leçons, changelog auto, garde-fou
├── INTERNET     — à brancher : Tavily/Crawl4AI/Firecrawl (lecture), Playwright MCP/Obscura/browser-use (navigation), Local Deep Research+SearXNG (veille) — routeur de méthodes dans docs/INTERNET-ET-MARKETING-AGENTIQUE.md
├── RÉSEAUX      — social : calendrier éditorial, drafts, porte humaine, écoute → publication via Postiz (MCP) quand hébergé
└── PRODUCTION   — app/ (portail), frontignan (livrable), proto-cognitorium (moteur)
```

Implémentation : **`projects/agent-office/`** — 11 services, zéro dépendance (stdlib), 100 % testé (`tests/`), invocations CLI `python3 -m agent_office <service>`.
Méthode de référence : Jake Van Clief — agent = instructions + modèle loué + portée, 4 questions par dossier (outcome/how/touch/human-check) ; transcript et analyse dans `docs/INTERNET-ET-MARKETING-AGENTIQUE.md`.
Auto-mise à jour : **`docs/AUTO-MAJ-SYSTEME-AGENTIQUE.md`** (Smithery/MCP, Voyager/skills, GPT-Researcher/Local Deep Research, Letta, Darwin Gödel Machine).
Conception benchmark modèles : **`docs/SYSTEMES-CONFRONTATION-MODELES.md`** (LMArena, godmode, ChatEval, Promptfoo, patrons n8n).

## 2. Règles d'or (issues des audits)

1. **Jamais de suppression** (courrier, prospects) — héritage contrainte utilisateur et mail-organizer.
2. **Zéro donnée inventée** : les chiffres seedés sont ceux de `USER/FINANCES/BUDGET-MENSUEL.md` (restant −111,51 €), les offres sont celles de `USER/TELOS/MISSION.md`, les contacts « TODO » sont à compléter, jamais remplis au hasard.
3. **Assembler, pas reconstruire** : le marketing vend des preuves déjà produites (rapport Frontignan, 271 fiches ROME, synthèse Talbot).
4. **Chaque service déclare sa capacité** dans `tools.json` — l'agent découvre ses propres outils via `registry list` avant d'agir (motif hérité du REGISTRE-OUTILS de watchtower).

## 3. Couche IA (ce que les audits ont retenu)

| Rôle | Choix audité (`SYSTEME-COMBINE-IA.md`) | Statut |
|---|---|---|
| Router LLM | **litellm** (60 345★, 100+ fournisseurs, fallbacks/budget) | à brancher quand des clés API existent |
| Gateway/garde-fous | **Portkey gateway** (MIT, BYOK, 1 600+ LLMs) | hypothèse retenue, à confirmer |
| Harness solo riche | **SillyTavern** (AGPL, cards, extension max) | option vitrine/démo |
| Option tout-en-un plan B | LibreChat (MIT) | si besoin d'une UI agents/MCP sans rien coder |
| Moteur de recherche maison | `reaserch-engine` (contradictions + vérification) | déjà là, branché sur research brief |

**Aucune brique IA externe n'est requise pour que agent-office tourne** : les outils marchent hors-ligne ; les LLM n'entrent que pour la génération de contenu, branchés plus tard via litellm.

## 4. Circuit opérationnel type (une semaine)

1. `mail digest` → quoi traiter ; `mail-organizer` → tri réel.
2. `budget report` → tenir l'œil sur le déficit (objectif : le couvrir au 1ᵉʳ forfait vendu).
3. `prospects next` → relances dues du jour.
4. `marketing sequence` → générer le mail de relance de la bonne offre.
5. `invoices devis` → transformer l'accord en devis conforme.
6. `research brief` + `reaserch-engine` → instruire les questions ouvertes.
7. `planning ics` → tout pousse dans Google Calendar.

## 5. Prochains enrichissements (backlog)

- [ ] brancher `mail digest` sur la vraie boîte (.env) — nécessite un mot de passe applicatif.
- [ ] connecter `app/` pour exposer `tools.json` et les rapports dans le portail (route /api/agent).
- [ ] synchronisation `budget` ↔ tableur (source de vérité actuelle).
- [ ] Notion : soit ré-alimenter les DB Revenus/Dépenses avec les vrais chiffres, soit acter l'abandon (données template confirmées par l'audit du 08/10).
- [ ] litellm/Portkey quand une clé API sera disponible.

---
*Créé le 08/10/2026 · enrichit la demande « une entreprise d'IA » en s'appuyant sur les audits existants plutôt que de nouveaux outils jetables.*
