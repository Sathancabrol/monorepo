# Mission : auditer, comparer, réorganiser — Carré d'As

**Destinataire :** un agent de recherche (ArenaAI) disposant d'un accès web / GitHub.
**Émetteur :** Sathancabrol — 8 octobre 2026.
**Dépôt concerné :** `github.com/Sathancabrol/monorepo`, branche `arena/0034230e-monorepo`.
**Documents joints :** `01-TABLEAU-DOMAINES.md` (93 domaines) · `02-CONCEPT-ART-ET-PROMPTS.md` (direction visuelle + prompts) ·
`03-LICENCES-VERIFIEES.md` (97 dépôts contrôlés) · `data/domaines.json` + `data/licences-2026-10-08.tsv` (versions machine).

---

## 0. La mission en une phrase

**Ne cherche pas des bibliothèques : cherche des systèmes qui fonctionnent déjà**, comprends comment ils sont
construits (code, issues, discussions, commits, documentation, benchmarks), compare-les à ce que ce dépôt contient
**déjà**, puis dis pour chaque besoin : *conserver, fusionner, remplacer, adapter, intégrer comme plugin, réécrire ou abandonner* —
avec des preuves (URL, commit, mesure) et en respectant les licences.

Le but final : **Carré d'As**, une application **locale, modulaire, open source, utilisable sur un PC modeste**,
qui réunit les fonctionnalités de 9 projets et 13 branches aujourd'hui séparés — sans perdre une seule fonctionnalité.

---

## 1. Le projet en dix lignes

Carré d'As est un **poste de travail de connaissance et d'action** : il observe (veille, OSINT, territoire),
comprend (graphe de connaissances, cognition, compétences), décide (projets, chantiers, scénarios, simulation)
et agit (documents, agents IA, automatisation). Il est **local d'abord** (il fonctionne sans Internet),
**modulaire** (chaque capacité est un module qu'on branche ou débranche), **gratuit** (aucune dépendance payante
obligatoire) et **portable** (Windows en premier, navigateur ensuite). Il appartient à un projet associatif et
**doit pouvoir être monétisé plus tard** sans tout réécrire. Il est guidé par un **assistant vocal et visuel**
(style JARVIS, sans excès décoratif). Sa première version doit être **fonctionnelle, installable et rapide**.

---

## 2. Où en est le projet — état **vérifié** le 08/10/2026

Ne redemande pas cet inventaire : il est mesuré, pas déclaratif.

| Élément | État réel |
|---|---|
| **Projets dans le dépôt** | 9 : COGNITORIUM (131 f., 24 Mo), proto-cognitorium (210 f., 87 Mo), watchtower (999 f., 52 Mo), frontignan (28 f., 14 Mo), animation-chronos (36 f.), HCSM (87 f.), reaserch-engine (61 f.), ETAT-DE-LART-PSYCHOLOGIE (37 f.), Language-decoder |
| **Branches récupérées** | 13 branches distantes ; tout le contenu utile est rapatrié dans `projects/_incoming/` (859 fichiers, 31 Mo) avec `_PROVENANCE.md` |
| **Complétude** | `scripts/verif-completude-repos.py` compare par empreinte Git : **2 157 fichiers examinés, 0 manquant** |
| **Brique agent** | `nexus_os` (branche `arena_01a08385`) : **8 303 lignes de Python**, **22 agents**, 30 compétences, runtime, *harness*, *evals*, contexte, mémoire, *providers*, *creator*, plugins, MCP, 8 fichiers de tests |
| **Brique BTP** | branche `arena_01a08449` : 22 rapports, 11 documents sources, `engine/btp_multi_agent.py` ; corpus `raw/` : **61 fichiers dont 43 PDF** (DCE, CCTP, CCAP, BPU, signalisation OPPBTP, AIPR, métrés, DT/DICT) |
| **Interfaces existantes** | `proto-cognitorium/raw/noeud neurono.html` (**le prototype d'origine**, 48 Ko : design system Void/Plasticity/Transfer, graphe, session N-back, vue liste accessible), watchtower (barre de 24 fonctions, globe 3D), 3 maquettes comparées (`docs/carre-das/maquettes/`), **14 fichiers HTML** dans les branches |
| **Squelette applicatif** | `shell/` : portail **8 portes · 14 modules · 104 fonctionnalités**, palette `Ctrl+K`, assistant vocal/visuel, sons libres, aucun asset externe — **104/104 fonctionnalités adossées à un fichier réel** du dépôt (`shell/tools/check-sources.py`) |
| **Cadrage** | `docs/carre-das/00→08` : architecture, contrat de module, UI, BTP, 3 propositions d'interface, réponses (licence, P0→P6, chronologie), écosystème libre, inventaire des fonctionnalités, squelette |
| **Recherche déjà faite** | `docs/recherche/` : brief, matrice de **85 domaines**, enrichissements et arbitrages (LadybugDB, IfcOpenShell, MCP, PMTiles…) |

**Ce qui manque et que tu dois aider à trancher :** le **Core** (modèle de données, événements, contexte, permissions),
le **moteur d'agents unifié**, la **synchronisation des vues 2D/3D/temps**, le **moteur de simulation**, le **Digital Twin**,
le **runtime de plugins**, l'**installeur Windows** et la **persistance**. Aujourd'hui ces briques existent à l'état d'idées
ou de prototypes dispersés.

---

## 3. Ce que tu dois produire

Pour **chacun des 93 domaines** de `01-TABLEAU-DOMAINES.md`, un bloc au format suivant (JSON, une ligne par domaine) :

```json
{
  "domaine": "D48",
  "verdict": "adapter | conserver | fusionner | remplacer | plugin | réécrire | abandonner | sursis",
  "solution_retenue": "MapLibre GL JS (2D/3D) + PMTiles hors ligne, Cesium seulement si un globe est indispensable",
  "alternatives_ecartees": [
    {"nom": "mapbox-gl-js", "raison": "licence propriétaire (TOS) — incompatible avec la monétisation"}
  ],
  "preuves": [
    {"type": "commit|issue|discussion|doc|benchmark|licence", "url": "…", "ce_que_ca_montre": "…"}
  ],
  "licence": {"spdx": "BSD-3-Clause", "risque": "aucun", "obligations": "mention du copyright"},
  "maturite": {"etoiles": 11825, "derniere_publication": "2026-10-08", "gouvernance": "communauté/fondation",
               "bus_factor": "sain|fragile|inconnu", "issues_ouvertes": 0},
  "performance": {"ram_mo": 0, "gpu": "non requis", "taille_installee_mo": 0, "temps_demarrage_ms": 0,
                  "source_de_la_mesure": "benchmark X / issue Y"},
  "integration": {"mode": "embarque|sidecar|service|wasm|inspiration", "effort": "S|M|L|XL",
                  "risques": ["…"], "dependances_supplementaires": ["…"]},
  "idees_d_architecture": ["ce que leur code fait mieux que ce qu'on avait prévu"],
  "impact_carre_d_as": {"modules": ["carte"], "fonctionnalites_du_registre": ["…"], "regressions_evitees": ["…"]},
  "questions_au_proprietaire": ["…"],
  "confiance": "haute|moyenne|faible",
  "sources_insuffisantes": "ce que tu n'as pas pu vérifier"
}
```

Puis, en synthèse finale :

1. **Le tableau de décision** (93 lignes, une par domaine) trié par priorité — lisible en un écran.
2. **L'architecture cible proposée** : schéma texte + justification, avec les **10 briques transversales** (§7) en évidence.
3. **Le plan de migration** : ce qu'on garde tel quel, ce qu'on déplace, ce qu'on jette, dans quel ordre, sans rien casser.
4. **Le budget de ressources** : ce qui doit tenir sur **GTX 1060 / 16 Go / i5** en mode ECO / STANDARD / PERFORMANCE.
5. **Les 4 planches d'images** décrites dans `02-CONCEPT-ART-ET-PROMPTS.md` (générées à partir des prompts fournis).
6. **La liste des fonctionnalités non couvertes** — s'il en reste une seule des 104 du registre sans solution, dis-le explicitement.

---

## 4. Les six questions à répondre pour chaque domaine

1. **Qui a déjà résolu ce problème, en vrai** (pas en démo) ? Donne 3 à 5 candidats, du plus sérieux au plus exotique.
2. **Comment est-ce construit ?** Lis les *issues* et *discussions* fermées : elles disent ce qui casse, ce qui a été abandonné et pourquoi.
3. **Combien ça coûte** en RAM, CPU, GPU, disque, temps de démarrage ? Sur un PC modeste, ça tient ?
4. **Quelle licence**, et qu'est-ce que ça interdit si on veut vendre un jour ? (voir `03-LICENCES-VERIFIEES.md`)
5. **Qu'est-ce qui est plus intelligent chez eux que dans notre plan ?** — c'est la question la plus importante : cherche des **idées d'architecture**, pas seulement des paquets.
6. **Quel est le plan de sortie** si le projet meurt ou change de licence ? (forks, standards ouverts, alternatives)

---

## 5. Protocole de recherche

| Où | Quoi | Comment |
|---|---|---|
| **GitHub** | dépôts, *releases*, *commits*, **branches**, *issues*, *discussions*, *pull requests* fermées | API (`/repos`, `/issues?state=all`, `/discussions`), recherche `gh` |
| **Code** | comment c'est *vraiment* fait | lire les fichiers d'architecture, les `CONTRIBUTING`, les schémas, les tests |
| **Documentation** | promesses vs réalité | comparer la doc et le code ; chercher les limites assumées |
| **Mesures** | performance, poids | *benchmarks* du dépôt, issues de performance, expériences d'utilisateurs, `bundlephobia`/`cargo bloat` quand c'est pertinent |
| **Communauté** | maturité réelle | fréquence des *commits* (12 derniers mois), nombre de mainteneurs, temps de réponse aux issues, Reddit/HN quand c'est éclairant |
| **Standards** | durabilité | RFC, spécifications (MCP, A2A, PMTiles, IFC), formats ouverts — **préférer ce qui est standard à ce qui est propriétaire** |
| **Données** | licences, qualité, mise à jour | IGN, OSM/ODbL, ROME, ESCO, O*NET, OpenAlex, INSEE, données locales |

**Règles de méthode :**
- Une affirmation sans URL ne compte pas. Une étoile ne prouve rien : regarde la **dernière publication**, les **issues** et la **gouvernance**.
- Vérifie **toujours** la licence par l'API (`GET /repos/{owner}/{repo}` → `license.spdx_id`) et **lis le fichier** quand GitHub dit `NOASSERTION` (26 cas rencontrés, dont 5 pièges sérieux).
- Cherche **les alternatives permissives** de chaque dépendance copyleft : c'est un livrable.
- Distingue **« ce qui marche aujourd'hui »** de **« ce qui est prometteur »** : le projet doit être installable cette année.
- Signale ce que tu **n'as pas pu vérifier** : c'est plus utile qu'une affirmation fausse.

---

## 6. Grille d'évaluation (à appliquer, pas à paraphraser)

| Critère | Poids | Ce qui disqualifie |
|---|---|---|
| Licence compatible avec la monétisation | **bloquant** | SSPL, non-commercial, propriétaire, AGPL **dans le cœur** |
| Fonctionne hors ligne, sans compte | **bloquant** | service obligatoire, *cloud only*, télémétrie obligatoire |
| Ressources sur i5 / GTX 1060 / 16 Go | **bloquant** | > 2 Go de RAM pour une brique de base |
| Maturité (dernière publication < 6 mois, issues traitées) | fort | dépôt abandonné (> 18 mois) |
| Qualité d'architecture (séparation, tests, extension) | fort | *monolithe* non testé |
| Effort d'intégration (S/M/L/XL) | fort | réécriture complète non assumée |
| Qualité de la documentation et de la communauté | moyen | aucun exemple, aucune réponse |
| Pérennité / plan de sortie | moyen | un seul mainteneur, format fermé |

---

## 7. Les 10 briques transversales (le vrai cœur du projet)

Ces briques ne se voient pas, mais **tout le reste en dépend**. C'est là que ta comparaison avec l'existant doit être la plus dure.

| # | Brique | Rôle | À comparer avec |
|---|---|---|---|
| 1 | **Identité universelle d'entité** | chaque personne, lieu, chantier, entreprise, document, événement, compétence, source a le même type d'identité | schémas Vault/Obsidian, Notion, Palantir, Wikidata, CIDOC-CRM |
| 2 | **Context Engine** | donner à chaque module et agent le contexte pertinent sans dupliquer les données | D08, mémoire de `nexus_os`, Graphiti, Letta/MemGPT |
| 3 | **Event Bus + journal** | tout changement devient un événement exploitable, rejouable | D03, EventStoreDB, Redux/NgRx, *event sourcing* |
| 4 | **Knowledge Graph** | relie entités, sources, événements, lieux, projets, documents | LadybugDB (MIT), Graphiti, Neo4j, notion de *provenance graph* |
| 5 | **Timeline universelle** | la même échelle de temps pour veille, chantier, cognition, territoire | Chronos, Vis.js, timelines SIG, *time-series* |
| 6 | **Dossier d'entité universel** | une fiche 360° alimentée par tous les modules | Palantir, Maltego, OSINT *dossiers*, cas d'usage `nexus_os` |
| 7 | **Synchronisation 2D ↔ 3D ↔ temps** | une sélection sur la carte met à jour la 3D, la timeline et la fiche | Kepler.gl, deck.gl, QGIS (liaisons), Gotham |
| 8 | **Nexus Orchestrator** | choisit l'agent, l'outil, la source, la méthode et coordonne | Goose, OpenHands, OpenClaw, Alethe, Claude Code, ACP |
| 9 | **Boucle de vérification** | un agent produit, un autre vérifie, sources et tests tranchent | `nexus_os/evals.py`, *verifiers*, revue croisée, abstention |
| 10 | **Contrat de données partagé** | tous les modules parlent la même langue de données | JSON Schema, Protobuf, JSON-LD, Pydantic |

**Principe :** Watchtower, BTP, Cognitorium, Atlas, HCSM, Research, Nexus ne sont plus des applications indépendantes ;
ce sont des **capacités branchées sur ces briques**. Toute architecture que tu proposes doit le démontrer.

---

## 8. Ce qui est déjà tranché — ne le refais pas

| Décision | État |
|---|---|
| Licence du projet | **Apache-2.0 + CLA + protection de marque + *open core*** (pour garder la porte de la monétisation ouverte) |
| Cible | **association** (loi 1901, franchise ≈ 81 051 €/an) |
| Ordre des plateformes | **Windows d'abord**, navigateur ensuite |
| Interface | design system **hérité du prototype d'origine** (`noeud neurono.html`) : `#050508`, **#00E5CC**, **#9B59B6**, Inter + JetBrains Mono ; **aucune interface validée sans 3 propositions comparées** |
| BTP | **2D par défaut**, 3D à la demande (mesure : Cesium 21 357 ms vs MapLibre 3 ms sur la branche `arena_01a072e1`) |
| IA | **locale par défaut, optionnelle** : `llama.cpp`/Ollama, modèles ≤ 6 Go de VRAM ; cloud en option |
| Graphe | **LadybugDB** (MIT, successeur de Kuzu archivé) — **ne pas reproposer Kuzu** |
| Hors ligne | Kiwix, ZIM, Project NOMAD, Organic Maps : déjà arbitrés dans `06-ECOSYSTEME-LOCAL-GRATUIT.md` |
| Sound design | `romainsimon/uisfx` (code MIT, audio **CC0**, pack `scifi`) ou sons synthétisés Web Audio |
| Corpus | reste **dans Git** (décision explicite ; seuil de sortie 1 Go non atteint) |

---

## 9. Les pièges déjà identifiés (corrige ton plan en conséquence)

Ton tableau initial citait des noms que j'ai vérifiés le 08/10/2026. Trois étaient inexacts ou piégés :

| Cité | Réalité vérifiée | À faire |
|---|---|---|
| « Mapbox » dans la pile GIS | **mapbox-gl-js est propriétaire** (TOS) | Utiliser **MapLibre** (BSD-3), fork communautaire |
| « Neo4j / FalkorDB » pour le graphe | **FalkorDB = SSPL**, Neo4j = GPL-3.0 | Rester sur **LadybugDB (MIT)** ; comparer FalkorDB seulement comme outil externe |
| « Gaussian splatting » sans licence | l'implémentation de référence (INRIA) est **non-commerciale** | Utiliser **gsplat** ou **Brush** (Apache-2.0), **GaussianSplats3D** (MIT) |
| « Gods-Eye-View » | existe : `bilawalsidhu/gods-eye-view` ★49 027 **MIT** — et `WorldPixelMap/android-gods-eye-view`, très proche de Watchtower mais **non-commercial** | S'inspirer du premier, ignorer le second |
| « GeoLibre » | existe : `opengeos/GeoLibre` ★7 871 **MIT** (+ `geolibre-rust`, `geolibre-plugins`) | **À évaluer sérieusement** comme plateforme GIS de référence |
| « Argos » | **introuvable** (aucun projet d'agent de ce nom) | Vérifier le nom, ou l'écarter |
| « Alethe » | existe : `Kc1t/alethe-agents` ★832 — espace de travail desktop local-first pour agents | À comparer à `nexus_os` |
| « OpenClaw » | existe : `openclaw/openclaw` ★391 640 — agent multi-plateforme | **Le plus gros écosystème d'agents du marché : à auditer en priorité** |
| « Docker » dans la pile | contredit « installable sans Docker » (décision du projet) | Docker = outillage de développement uniquement, **jamais requis** pour l'utilisateur |

---

## 10. Les quatre planches d'images à produire

Les prompts complets sont dans `02-CONCEPT-ART-ET-PROMPTS.md`. Types attendus :

| Type | Rôle | Nombre |
|---|---|---|
| 01 — Vision globale | montrer Carré d'As entier (le schéma de l'image de référence) | 1 planche |
| 02 — Concept art par module | l'identité visuelle de chaque module | 12 + 8 modules |
| 03 — UI fonctionnelle | à quoi ressemblent concrètement panneaux, cartes, graphes, interactions | 6 écrans clés |
| 04 — Architecture système | comment les briques communiquent | 1 schéma + 3 coupes |

**Contraintes de style (non négociables) :** sombre graphite/bleu nuit, verre sombre maîtrisé, cartographie réaliste
(pas d'hologramme cliché), accents sobres, typographie technique, **données réellement lisibles**, inspiration
centres opérationnels + logiciels scientifiques + jeux de stratégie, **aucun cyberpunk décoratif**, densité maîtrisée.
Palette imposée : `#050508`, `#0A0A12`, `#1A1A2E`, texte `#E8E8F0`/`#8A8AA8`, accent **#00E5CC**, transfert **#9B59B6**,
alerte `#FF3366`.

---

## 11. Contraintes non négociables (un livrable qui les viole est rejeté)

1. **Aucune fonctionnalité perdue** : les **104 fonctionnalités** du registre (`shell/data/modules.json`) doivent toutes avoir une solution.
2. **Gratuit et open source** : pas de dépendance payante dans le chemin principal ; un service payant ne peut être qu'une **option**.
3. **Hors ligne** : tout doit fonctionner sans Internet ; l'Internet apporte un supplément, jamais une condition.
4. **PC modeste** : i5, GTX 1060 (6 Go), 16 Go de RAM. Fournis un budget par brique et par profil (ECO/STANDARD/PERFORMANCE).
5. **Installable par un non-développeur** : sous Windows, sans Node, sans Python, sans Docker.
6. **Réversible** : mise à jour signée, retour arrière, données locales sauvegardables et lisibles (formats ouverts).
7. **Traçable** : chaque affirmation → une URL ; chaque fonctionnalité → une source ; chaque licence → un SPDX.
8. **Sobre** : pas de télémétrie, pas de compte obligatoire, pas de « fausse précision » (`UX-09`), et toute visualisation a un équivalent textuel.

---

## 12. Ordre de travail conseillé

1. **P0 Fondations** (D01→D28, D86→D93) : Core, données, événements, contexte, entités, recherche, plugins, MCP, sécurité, installateur, hardware. *C'est là que tout se gagne ou se perd.*
2. **P0 Modules majeurs** : Watchtower/Intel (D39, D48→D55), Territoire (D50), Projets (D10), Cognitorium (D41→D43), BTP (D56→D63, D82, D88).
3. **P0 Agents** (D29→D35, D89, D90) : compare `nexus_os` (22 agents, 8 303 lignes) à Goose, OpenHands, OpenClaw, Alethe, **puis propose un runtime unique**.
4. **P1** : simulation (D64→D68), recherche scientifique (D45), 3D/splat (D59), apprentissage (D43), drone (D60), synchronisation (D17, D83).
5. **P2** : laboratoire (D69), marketplace (D74), collaboration (D92).
6. **En continu** : licences (D18, D84), veille et santé des briques (D93), benchmark (D28).

---

## 13. Checklist de fin de mission

- [ ] Les **93 domaines** ont un bloc JSON complet, chacun avec **au moins 2 preuves URL**.
- [ ] Chaque **dépendance citée** a une licence SPDX vérifiée **et** un plan de sortie.
- [ ] Les **10 briques transversales** ont une proposition d'architecture argumentée.
- [ ] Les **104 fonctionnalités** du registre sont couvertes (ou explicitement signalées comme non couvertes).
- [ ] Un **plan de migration** existe : quoi garder, quoi déplacer, quoi jeter, dans quel ordre.
- [ ] Le **budget de ressources** tient sur GTX 1060 / 16 Go, par profil.
- [ ] Les **4 planches d'images** sont produites à partir des prompts.
- [ ] Une section **« ce que je n'ai pas pu vérifier »** est présente et honnête.

---

*Document produit le 8 octobre 2026 à partir de l'état réel du dépôt (mesuré, pas déclaratif). Tout chiffre de ce document est rejouable :
`python3 scripts/verif-completude-repos.py`, `python3 shell/tools/check-sources.py`, `python3 scripts/gen-dossier-arena.py`.*
