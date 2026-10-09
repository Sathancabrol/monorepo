# 🧭 SYNTHÈSE GLOBALE — session 08→09/10/2026 (nuit)

> Tout ce qui a été fait, vu, récupéré, voulu ; objectifs et dates ; budget. Fichier de référence à relire avant chaque reprise.

---

## 1. 🪪 Le cap (pourquoi tout ça)

- **DA nommée** : Laplace · **Principal** : Nathan Cabrol, Sète, Europe/Paris.
- **Mission** : inconnue au départ → méthode par **hypothèses testées** (`USER/TELOS/MISSION.md`) : sens M1 « IA pour ceux qui construisent », M2 « posséder/apprendre des systèmes », M3 « créer des mondes (Outsider) ».
- **Situation financière réelle** (tableur importé dans `USER/FINANCES/BUDGET-MENSUEL.md`) :

| Poste | €/mois |
|---|---|
| Revenu France Travail | **+977,10** |
| LOCK : loyer 832,83 + élec 126,44 + assurance 75,36 + internet 29,99 + tél 23,99 | **−1 088,61** |
| **RESTANT avant MOVE** | **−111,51 €** |

**Objectif financier n°1 : effacer le déficit dès le 1ᵉʳ forfait vendu (300-800 €).**

## 2. 🔎 Ce qu'on a VU (audits & veilles)

**Audit des actifs** (`docs/AUDIT-ACTIFS-COMPLET.md`, 2 passes) : 9 repos GitHub, ~220 fichiers BTP à la racine, projets frontignan (livrable pro 249 sources + deck 18 slides), reaserch-engine, proto-cognitorium (271 fiches ROME + Formacode + SQLite), ETAT-DE-LART-PSYCHOLOGIE (revue PRISMA), watchtower (globe 3D + audits), outsider (GDD), mail-organizer (livré) ; Drive = atelier de design Cognitarium (7 prompts AI Studio, onboarding 82 Mo, Vision Pilot) + coquilles vides (« Polsia », « Mnéoterr ») ; Notion = template abandonné ; Linear vide ; Calendar vierge ; GitHub sans rien de caché.
→ **Verdict : le fil = COGNITORIUM**, produit à trois têtes déjà avancé ; les offres s'**assemblent**, rien à construire de zéro.

**Veilles techniques** (7 docs) : systèmes combinés IA (litellm 60k★ routeur, Portkey gateway, SillyTavern, LibreChat), UI mobiGlas (SF → design), confrontation de modèles (LMArena ELO, godmode skills, ChatEval jury multi-rôles, Promptfoo/DeepEval/Inspect, patrons n8n), auto-mise à jour (Smithery/Toolbox MCP, Voyager skill-library, GPT-Researcher/Local Deep Research, Letta/MemGPT, Darwin Gödel Machine), couche internet (Tavily, Crawl4AI 58-78k★, Firecrawl, Jina Reader, Playwright MCP, browser-use ~115k★, Obscura 28,7k★), marketing/réseaux (Postiz MCP, écoute sociale gratuite, GEO, Bluesky), clones open source & RE (ArtCraft, WareTrack, Ghidra/GhidraMCP — cadre légal posé : clones propres oui, cracking non).

## 3. 📦 Ce qu'on a RÉCUPÉRÉ / SAUVÉ dans le repo (à l'abri des pertes)

- Budget réel (l'image source a disparu du sandbox → contenu pérennisé en markdown).
- USER/ instancié (11 fichiers minés sans invention), MISSION v2, FINANCES.
- Transcripts & références : Jake Van Clief (ICM + reel « agent = naming convention »), chiffres LMArena, étoiles/licences de chaque outil cité.
- Tout le travail est poussé sur `origin/arena/93b54a79-monorepo` — **3 rewinds du sandbox réparés depuis origin** (méthode : fetch → reset origin → restauration).

## 4. 🏗 Ce qu'on a VOULU → construit (l'entreprise d'IA)

**`projects/agent-office/` — 11 services, zéro dépendance, 16 tests verts, doctor 11/11 :**

| Service | Rôle |
|---|---|
| budget | le déficit réel suivi en CLI |
| invoices | devis/factures conformes (franchise TVA art. 293 B) |
| marketing | one-pagers/séquences/posts des offres réelles |
| prospects | pipeline O1/O2/O3 + relances dues |
| research | briefs, citations, veille → reaserch-engine |
| mail | digest IMAP lecture seule |
| planning | agenda + export .ics |
| arena | duels de modèles en aveugle + ELO + grille ChatEval |
| update | journal d'évolution, leçons (Reflexion), changelog auto, garde-fou |
| social | calendrier éditorial, drafts aux limites réelles, porte humaine, écoute |
| registry | tools.json + doctor |

**Docs d'architecture** : AGENT-ENTREPRISE.md (organigramme + règles d'or), SYSTEME-COMBINE-IA.md, SYSTEMES-CONFRONTATION-MODELES.md, AUTO-MAJ-SYSTEME-AGENTIQUE.md, INTERNET-ET-MARKETING-AGENTIQUE.md, VEILLE-CLONES-OPEN-SOURCE-ET-RE-IA.md, AUDIT-ACTIFS-COMPLET.md.
**Règle d'or actée** : assembler l'existant, jamais un seul juge, porte humaine avant publication, aucune donnée inventée, jamais de suppression.

## 5. 📅 OBJECTIFS & DATES

| Date | Quoi | Statut |
|---|---|---|
| **15/10/2026** | Test O1 : RDV conseiller France Travail, démo maquette Cognitorium Emploi | à faire (fiche prospect n°1) |
| 16/10/2026 | Post réseaux n°1 (deck Frontignan — brouillon prêt, porte humaine) | brouillon |
| **20/10/2026** | Test O2 : envoyer le deck Frontignan existant aux destinataires réels | à faire (prospect n°2) |
| 23/10/2026 | Post réseaux n°2 (preuves ROME/PRISMA) | brouillon |
| 31/10/2026 | Test O3 en réserve : démo dossier lu par l'IA au réseau Sobeca | à faire si O1/O2 muets |
| **07/11/2026** | **Révision J+30** : garder/abandonner M1-M3 et O1/O2/O3 selon les résultats | planifié (tasks.json) |

**Séquence budgétaire** : 1ᵉʳ forfait (O1 démo gratuite puis payante, ou O2 forfait 900-2 500 €) → couvre −111,51 € → puis rythme mensuel à viser ≥ 200 € de marge.

## 6. ▶️ Prochains gestes concrets (dans l'ordre)

1. Préparer le kit RDV conseiller FT (1 page + maquette + argumentaire) — tout existe déjà.
2. Retrouver le destinataire réel du rapport Frontignan (Drive/emails) et lui envoyer le deck.
3. Quand clés API/hébergement : brancher Tavily (1 000 crédits gratuits) + Local Deep Research sur la stack SearXNG de watchtower + Postiz docker.
4. 07/11 : révision J+30 avec les chiffres des tests.

---
*État au 09/10/2026 ~01h · commit 9e11437 sur arena/93b54a79-monorepo · tout est testé (16 tests) et poussé.*
