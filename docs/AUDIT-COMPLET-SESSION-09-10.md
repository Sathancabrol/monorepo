# 🔎 AUDIT COMPLET DE SESSION — rien de perdu ? que manque-t-il pour le carré d'as agentique ? (09/10/2026)

> Audit réel (vérifié sur disque + git, pas de mémoire) : inventaire, pertes, oublis, comparaison concurrence, et les pièces manquantes.

---

## A. ✅ Inventaire vérifié (état au commit a311801, 40 commits sur la branche)

| Bloc | État vérifié |
|---|---|
| Git | HEAD = origin, working tree propre, 40 commits de session |
| **docs/** | **30 documents** (audits, mission, stratégie, veille, études, synthèses) + `transcripts/` |
| **agent-office** | **12 services**, `registry doctor` 12/12, **20 tests OK**, `tools.json` régénéré |
| Fiches agents | 5 départements (`agents/`) couvrant les 12 services, gates QA testées |
| Données | budget CSV, 3 prospects (O1/O2/O3, étape « cible »), **13 tâches** au planning, journal **14 entrées**, leçons, 2 posts sociaux (16 & 23/10), ELO arena, knowledge db (16 nœuds / 3 arêtes, gitignorée, régénérable) |
| Mémoire utilisateur | `projects/life-hub/USER/` complet (MISSION v2 « on ne décrète pas, on teste », FINANCES, PROJECTS) |
| Livrables offres | **O1** : proto-cognitorium (dist/index.html) ; **O2** : rapport Frontignan HTML + figures ; **O3** : réseau Sobeca identifié |
| Carte | `MAP.md` racine (2 sauts max par fait) |
| Watchtower | fork God's Eye View + registre `data/thau-signaux.json` (7 signaux A/B/C) |
| Portail | `app/` (FastAPI + Jinja) existe |

## B. 🔁 Pertes : aucune (malgré 5+ « rewinds » du sandbox)

Le sandbox a reculé l'historique local **plusieurs fois** (dont 3× dans la seule dernière séance). À chaque fois : `git fetch` → détection → sauvegarde des écritures en cours → `reset --hard origin` → restauration → commit. **Vérification finale : chaque fichier attendu par la mémoire de session existe sur disque ET dans origin.** Règle désormais permanente : fetcher et comparer HEAD/origin avant chaque commit.

## C. ⚠️ Oublis réels trouvés par l'audit (corrigés ce tour)

1. **O3 Sobeca (échéance 31/10) n'était dans aucune tâche** → tâche ajoutée (préparation contact au 28/10).
2. **Posts sociaux des 16 et 23/10** : présents au calendrier éditorial mais **sans tâche de finalisation/publication** → 2 tâches ajoutées.
3. **Plateforme des 2 posts non choisie** (`plateforme: null`) → décision à prendre avec Nathan (LinkedIn ? Bluesky ?) — signalé, pas décidé à sa place.
4. **Réunion de clôture ZIFMAR 2 (07/01/2027)** absente du planning → tâche ajoutée.
5. Mineur : graphe knowledge léger (3 arêtes) — à ré-ingérer après chaque évolution notable ; les 141 PDF (416 Mo) commités à la racine avant la session alourdissent le clone (hygiène à traiter plus tard, pas bloquant).

## D. ⚔️ Comparaison avec la concurrence et nos autres repos

| Capacité | Nous | The Agency ×2 | OmniRoute | Paf MAPS | Herald OS | Odysseus | AIOS |
|---|---|---|---|---|---|---|---|
| Agents = fiches identité/règles/gates | ✅ 12 | ✅ 235+ | — | ✅ skills/routines | ✅ | ✅ | ✅ (théorie) |
| Mémoire persistante requêtable | ✅ SQLite+graphe | partiel | SQLite (config) | ✅ fichiers+carte | ✅ | ✅ local | ✅ (théorie) |
| Confrontation de modèles (ELO, aveugle) | ✅ **unique** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Couche d'accès modèles (clés, routage, fallback) | ❌ **absent** | ❌ | ✅ 359 fournisseurs | via son abo | BYO modèle | BYO | — |
| Exécution 24/7 (routines pendant l'absence) | ❌ **absent** | ❌ | n/a | ✅ VPS+sync 5 min | ✅ OS complet | ✅ local | — |
| Interface/écran « montre sans stocker » | ⚠️ `app/` non branché | app dédiée | dashboard | ✅ dashboard 6 vues | ✅ Spaces | ✅ | — |
| Ancrage business réel (offres, prospects, budget) | ✅ **unique** | ❌ (personas) | ❌ | ✅ (sa boîte) | ❌ | ❌ | ❌ |
| Sécurité graduée (porte humaine, brouillons seuls, jamais de suppression) | ✅ par règles | ❌ | sanitization opt-in | ✅ permissions fichier | ✅ 4 paliers+audit | partiel | — |

**Nos autres repos du monorepo** : 12 projets existent, mais un seul est outillé/testé (agent-office), un seul a une UI (app/), un seul une carte (watchtower). Le reste = livrables et prototypes utiles (frontignan, proto-cognitorium) ou coquilles (Certains `projects/*`). L'intégration est le sujet.

**Verdict honnête** : sur la couche « bureau agentique adossé à un vrai business », **personne dans le panel n'a notre combinaison** (fiches + mémoire + confrontation + règles sécurité + offres réelles). Ce qui nous manque, ce sont des couches, pas de la qualité.

## E. 🃏 Le carré d'as agentique — ce qu'il manque

Définition du carré : **1) Mémoire** (tout retrouver en 2 sauts) · **2) Outils** (agir réellement) · **3) Modèles** (l'intelligence branchée) · **4) Présence** (tourner et se montrer 24/7).

| As | État | Ce qui le complète |
|---|---|---|
| 🧠 Mémoire | ✅ **en main** | MAP.md, knowledge, docs, journal |
| 🛠 Outils | ✅ **en main** | 12 services testés, gates QA, registre |
| 🔌 Modèles | ❌ **manquant** | **Les clés API gratuites** (checklist `CLES-API-GRATUITES.md`, 15 min, action Nathan) → brancher `arena` en vrai, puis OmniRoute comme couche de routage |
| 📡 Présence | ❌ **manquant** | (a) le portail `app/` branché sur les données agent-office (« montre sans stocker ») ; (b) un runtime 24/7 = le VPS (reporté au 1ᵉʳ revenu) avec routines type `routines.yaml` ; (c) la distribution : publier les posts, passer les tests O1/O2/O3 |

**Ordre logique** (respecte la règle budget) :
1. **Cette semaine** : RDV O1 (15/10) + réunion ZIFMAR (16/10) + module ZAN dans le deck O2 (16/10, envoi 20/10) + BOAMP veille (13/10). Tout ça sans dépense.
2. **Dès que possible (action Nathan, 15 min)** : créer les 2-3 clés API gratuites → premier vrai duel `arena` → le système devient réellement « agentique ».
3. **Au 1ᵉʳ revenu** : VPS (Hetzner/OVH ≤6 €) = routines 24/7 + portail public + OmniRoute + (plus tard) Hermes.
4. **Fil rouge** : chaque test O1/O2/O3 et chaque réunion alimente le registre Watchtower et la mémoire.

---
*09/10/2026 — audit exécuté sur disque (git, tests, doctor, données) ; corrections intégrées au même commit.*
