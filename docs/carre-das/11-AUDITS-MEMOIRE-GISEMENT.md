# Audits, mémoire et travail non fusionné — recensement du 9 octobre 2026

**Pourquoi ce fichier.** Avant de construire quoi que ce soit, il faut savoir ce
qui existe déjà. Trois passes de lecture ont été nécessaires pour le trouver ;
ce fichier évite une quatrième.

**Règle** : *référencer → adapter → normaliser → extraire*. Jamais recopier.

---

## 1. L'audit complet — 52 findings

**Emplacement** : `projects/_incoming/monorepo/arena_171a1f38-monorepo/audit/`
(branche `arena/171a1f38-monorepo`, PR ouverte).

| Fichier | Rôle |
|---|---|
| `MEMORY.md` | mémoire générée — état courant, projets, phases, prochaines actions |
| `state.json` | **source de vérité machine** (statuts, faits, actions) |
| `JOURNAL.jsonl` | journal append-only des itérations |
| `ANALYSE-V1-V5.md` | grille de maturité v1→v5, Étape 0 |
| `AUDIT-2026-10.md` | livrable final, 13 tableaux (452 lignes) |
| `notes/P-*.md` | 9 fiches projet |
| `notes/S0`→`S4` | racine, infra, inventaire, GitHub, transverse |
| `graph.json` | graphe projets ↔ documents ↔ dépendances |
| `scripts/audit_*.py` | 5 scripts pour rejouer l'audit |

**Compteurs** : 52 findings · 1 362 fichiers mesurés · 470+ lus en profondeur ·
13 tableaux · 34 branches analysées · 9 dépôts vérifiés.

### Les findings qui nous concernent

| # | Sév. | Finding |
|---|---|---|
| A1 | **critique** | 153 commits / 15 branches non fusionnés |
| A3 | élevé | `ETAT-DE-LART` : +38 commits dont un agent complet |
| A6 | élevé | 289 Mo de binaires dans Git |
| A7 | élevé | 6/9 projets sans test ; 1 CI sur 9 dépôts |
| A16 | moyen | grilles salariales + corrigés AIPR publics dans le dépôt |
| A17 | moyen | ADR-007 (mémoire unifiée) décidée mais non implémentée ; 5 persistances |

### Recommandation n°11 (P2) — non réalisée

> **Créer un registre de claims commun** (méthode Talbot/frontignan) pour
> toutes les affirmations publiées.

C'est précisément ce que `carredas/core/` est en train de devenir.

---

## 2. Le gisement — 16 branches de travail réel

`AUDIT-2026-10.md` §7. Ce qui nous est utile pour le 16 octobre :

| Pri. | Branche | + | Contenu |
|---|---|---:|---|
| **P0** | `ETAT-DE-LART` · `arena/01a04f7b` | 38 | **agent de recherche**, cosmos, 221 sorties |
| **P1** | `monorepo` · `arena/01a08385` | 6 | **`nexus_os`** — 22 agents, 14 skills, 59 tests |
| **P1** | `monorepo` · `arena/01a08449` | 2 | **module BTP** — 154 sources, 7 rapports, `btp_multi_agent.py` |
| P1 | `COGNITORIUM` · `watchtower/osint-workbench-v0.1` | 13 | modules OSINT + registre JS |
| P2 | `monorepo` · `feat/tool-data-catalog-2026-10` | 13 | contrats `core/` — **déjà adopté** |
| — | 19 branches mortes | 0 | à supprimer |

### `nexus_os` — le système agentique, déjà écrit

`projects/_incoming/monorepo/arena_01a08385-monorepo/nexus_os/` — 6 485 lignes
de Python, **59 tests au vert**.

- **22 agents** définis en JSON (`agents/*.json`) : orchestrateur, chercheur,
  rédacteur, architecte, analyste, **géo**, **juriste**, **OSINT**, pm, qa,
  reviewer, teacher, translator, devops, designer, coder, coach, builder,
  promptsmith, videomaker, pilot, archiviste
- **Routage par déclencheurs** : chaque agent porte ses mots-clés, un score, et
  l'orchestrateur délègue
- **Cycle de vie ECC** : plan → recherche → implémentation → revue →
  vérification → mémorisation
- **14 compétences** `SKILL.md` · **14 outils sandboxés** · client MCP
- Routeur de modèles : 8 fournisseurs, 20 modèles, quota + coût, repli local
- `memory.py` (faits / décisions / leçons) · `instincts.py` (règles apprises) ·
  `evals.py` (barème reproductible)

C'est la réponse directe à la priorité n°1. **Non fusionné.**

---

## 3. La méthode Frontignan — la nôtre, sur le même territoire

**`projects/frontignan/`** — dossier d'appui pour la municipalité de
**Frontignan (Hérault, Sète Agglopôle Méditerranée)**, septembre 2026. Soit
l'agglomération exacte du rendez-vous du 16 octobre.

- `rapport-frontignan-analyse-territoriale.md` — 826 lignes, 11 sections,
  **13 fiches projets, 249 sources datées**
- `vision-frontignan-2026-2040.md` — focale 2030, 3 scénarios 2040
- `index.html` — **deck de 18 slides**, autonome, Ctrl+P → PDF paysage
- 14 figures matplotlib + générateurs (`make_figures.py`, `make_html.py`,
  `make_deck.py`)

### La grille de lecture (§2 du rapport)

| Marqueur | Statut | Critère |
|---|---|---|
| ✅ | Fait vérifié | croisé ≥ 2 sources indépendantes, **ou** source officielle primaire |
| ≈ | Estimation | ordre de grandeur, source unique, ou calcul reconstitué |
| ❓ | Incertain / à vérifier | contradiction entre sources ou donnée manquante |

**Règles annexes** : données de référence < 2 ans (sinon signalées comme
tendances) ; distinction systématique **commune** vs **intercommunalité** ;
périmètres budgétaires explicités ; vigilance sur les homonymies.

### Ce que le rapport contient sur l'Agglo elle-même (§5.3)

Budget 2025 : 245 M€ tous budgets · épargne nette > 14 M€ · investissement
82,4 M€ (634 €/hab.) · dette 99,7 M€ · désendettement 5 ans.
Budget 2026 : 242 M€, 68 M€ d'investissement, épargne brute 18,4 %,
désendettement 6,3 ans, emprunt 10,1 M€.
Projets : RD2 en voie de bus prioritaire (12 M€) · ligne express
Sète-Frontignan (1,8 M€) · centre aquatique de Frontignan · conchyliculture
13,1 M€ · assainissement 19 M€ · GEMAPI 3 M€ · budget « tagué climat » (I4CE).

---

## 4. Ce qui a été fait à partir de tout ça

| Apport | Intégration |
|---|---|
| Grille ✅ / ≈ / ❓ | `canonical.MARQUEURS` — le vocabulaire de lecture de l'application |
| Critère du fait vérifié | `admissibilite.fait_non_croise` — 2 sources ou 1 source officielle |
| Registre de 86 outils Watchtower | `modules/osint/registries.py` · **120 outils** |
| `SOURCES-FR.md` + `DATA_SOURCES.md` | `modules/watchtower/data/sources.json` · **34 sources** |
| Validateur HCSM + anti-pattern n°7 | `core/admissibilite.py` · 7 règles |
| Contrats de la branche `tool-data-catalog` | `core/canonical.py` + schémas publiés |

---

## 5. Ce qui reste à décider

1. **Système agentique** — porter `nexus_os` (22 agents, 59 tests) dans Carré
   d'As, ou en adopter seulement les définitions d'agents et le routage ?
2. **Module BTP** — `arena/01a08449` contient 154 sources et
   `btp_multi_agent.py`.
3. **Frontignan** — en faire un module « Territoire » plutôt qu'un dossier
   isolé ? Le deck et la méthode sont réutilisables telle quelle pour les 13
   autres communes.
4. **Nettoyage** — 19 branches mortes, 289 Mo de binaires, grilles salariales
   et corrigés AIPR publics (A16).
