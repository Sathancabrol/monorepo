---
provenance: interview-mined
last_updated: 2026-10-08
source: MANIFEST.json, projects/, docs/ (08/10/2026)
---

# Projets actifs et en dormance

## 🔥 Actifs (cette session)
| Projet | Où | État |
|---|---|---|
| **Life Hub** | `projects/life-hub/` + `docs/LIFE-HUB.md` | Phase 1 ✅ (LifeOS adopté) — Phase 2 : interview en cours |
| **Système IA combiné** | `docs/SYSTEME-COMBINE-IA.md` | Plan 4 couches validé — construction non commencée |
| **OUTSIDER** (RPG enquête Supernatural) | `projects/outsider/` | Fondation ✅ — next : PHENOMENON_ENGINE + WORLD_STATE |
| **Prospective scorée** | `docs/PROSPECTIVE-TRACKER.md` | 24 prédictions suivies — 1ʳᵉ revue janvier 2027 |
| **app/** (portail FastAPI) | `app/` | Existante (port 8123) — appelée à servir le Life Hub |

## 🧰 Infrastructure & outils
| Projet | Où | État |
|---|---|---|
| **mail-organizer** | `projects/mail-organizer/` | Expédié (19 tests) — tri/archivage sans suppression |
| **reaserch-engine** | `projects/reaserch-engine/` | Présent dans le monorepo |
| **watchtower** | `projects/watchtower/` | Présent dans le monorepo |

## 🧠 Le produit nº1 (révélé par l'audit du 08/10) : COGNITORIUM
| Pièce | Où | Rôle |
|---|---|---|
| HCSM | `projects/HCSM/` | modèle scientifique de l'état cognitif (v0.1.1) |
| ETAT-DE-LART-PSYCHOLOGIE | `projects/ETAT-DE-LART-PSYCHOLOGIE/` | revue de littérature PRISMA 2020 (2020-2026) : la caution scientifique |
| proto-cognitorium | `projects/proto-cognitorium/` | moteur : 271 fiches ROME France Travail + Formacode + DDL SQLite + maquettes |
| Cognitarium City / Frontignan | `projects/frontignan/` + Drive (prompts AI Studio, « Vision Pilot 1.2.mp4 ») | application territoriale : rapport 249 sources + deck 18 slides |
| Atelier de design | Drive / Google AI Studio (7 prompts, 28/07→27/08/2026) | cahier des charges produit : profil cognitif, graphe, onboarding (82 Mo), frise historique |
| OpenBCI Research Collection | Drive (partagé openbci.com) | veille capteurs / mesure réelle |
| animation-chronos | repo dédié | visuel de marque |
→ Voir `docs/AUDIT-ACTIFS-COMPLET.md` : offres O1/O2/O3 assemblées sur cet existant.

## 🤖 L'entreprise IA
| Pièce | Où | Rôle |
|---|---|---|
| **agent-office** | `projects/agent-office/` | 12 services bureautiques zéro-dépendance (budget, invoices, marketing, prospects, research, mail, planning, arena, social, knowledge SQLite+graphe, update, registry) — `python3 -m agent_office registry doctor` |
| Architecture | `docs/AGENT-ENTREPRISE.md` | organigramme, règles d'or, couche IA (litellm/Portkey retenus par l'audit), circuit hebdo |
| Benchmark modèles | `docs/SYSTEMES-CONFRONTATION-MODELES.md` | LMArena, godmode, ChatEval, Promptfoo, patrons n8n → service `arena` (duels aveugles + ELO) |
| Auto-mise à jour | `docs/AUTO-MAJ-SYSTEME-AGENTIQUE.md` | Smithery/MCP, Voyager/skills, GPT-Researcher/Local Deep Research, Letta, Darwin Gödel Machine → service `update` |
| mail-organizer | `projects/mail-organizer/` | tri IMAP réel, déjà livré (jamais de suppression) |
| reaserch-engine | `projects/reaserch-engine/` | moteur recherche branché sur les briefs `research` |

## 🗂 Sites & orga perso
- **Notion** : « Budget mensuel » + tâches hebdo (templates d'août 2026) — pont vers USER/ ; budget réel = tableur (FINANCES/BUDGET-MENSUEL.md).
- **Drive** : archive Cognitorium (« Polsia - Cognitorium et Mnéoterr », « Slack Cognitrum »), dossier Gmail classé.
- **Linear** : vide — disponible comme kanban offres/Outsider.

## 🧠 Recherche & cognition (dormants / à ré-évaluer)
- **COGNITORIUM** (+ `projects/proto-cognitorium/`) — modules cognitifs, cité dans l'architecture cible du Life Hub
- **HCSM** — état personnel, idem
- **ETAT-DE-LART-PSYCHOLOGIE** — recherche
- **Language-decoder**, **animation-chronos**, **frontignan** — projets annexes

## 🏗️ Hors monorepo (boulot)
- **Dossier de chantier** (Lotissement Pruniaux / Giratoire de Barbazan / NOE) — 220 fichiers marché construction sur `main` (`docs/DOSSIER-CHANTIER-INDEX.md`), + synthèse Talbot 2026.

---
*TODO (interview) : priorisation officielle entre actifs ; statut réel des dormants.*
