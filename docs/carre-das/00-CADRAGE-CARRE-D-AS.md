# CARRÉ D'AS — cadrage de la V1

**Statut :** `ANALYSE` — proposition de cadrage, rien n'est implémenté.
**Date :** 7 octobre 2026 · **Dépôt :** `Sathancabrol/monorepo` (à renommer `carre-das`)
**Décisions utilisateur intégrées :** cible **association** · Windows d'abord, navigateur ensuite · monorepo renommé **Carré d'As** = première itération de l'application Cognitorium finale · **modules plug in/out** · **BTP comme brique puissante** · interface **simple et affordante**.

Documents liés : `01-CONTRAT-MODULE.md` (le contrat plug in/out) · `02-UI-PRINCIPES-ET-INSPIRATIONS.md` (l'interface) · `03-MODULE-BTP.md` (la brique BTP) · `../recherche/` (le dossier à donner à l'agent de recherche).

---

## 1. Ce que le nom change

| Terme | Ce qu'il désigne | Conséquence |
|---|---|---|
| **Cognitorium** | le système/écosystème complet (vision : Human + Knowledge + World + Design + Action) | reste l'horizon, la documentation de gouvernance reste valable |
| **Carré d'As** | **l'application** : la première itération installable, le point d'accès unique aux modules | nouveau nom du dépôt, de l'installateur, de l'UI, des releases |

Le nom « Carré d'As » n'apparaissait nulle part dans le dépôt : c'est donc une décision neuve. Lecture proposée (à valider) : **quatre figures fondatrices** = *Human* (personne, compétences) · *Knowledge* (documents, savoirs sourcés) · *World* (territoire, chantier, 3D) · *Action* (projets, agents, décisions). C'est une bonne accroche pour une association : quatre cartes, un jeu complet, accessible à tous.

> Première conséquence pratique : le renommage du dépôt GitHub (`monorepo` → `carre-das`) peut être fait maintenant (GitHub redirige), mais il vaut mieux le faire **au moment de la fusion des branches**, pour ne pas mélanger les deux opérations.

---

## 2. Cible association — ce que ça change réellement

Une association loi 1901 change **plus de choses que le nom**. Voici ce qui est en jeu, avec les implications concrètes.

### 2.1 Ce qui est gagné

| Point | Effet |
|---|---|
| **Légitimité d'intérêt général** | accès aux subventions publiques (numérique, transition, territoire), au mécénat, aux appels à projets ; crédibilité auprès des collectivités et des établissements d'enseignement |
| **Non-lucrativité** | cohérence totale avec le local-first et l'open source : ce qui est produit appartient au commun |
| **Gratuité assumée** | pas de pression commerciale sur la V1 ; on peut livrer aux associations, aux communes et aux artisans sans facturation |
| **Gouvernance** | collégiale, documentée, adaptée à la contribution bénévole |

### 2.2 Ce qui devient obligatoire ou délicat

| Sujet | Ce qu'il faut faire | Pourquoi |
|---|---|---|
| **Licence** | **décider maintenant** (voir §2.3) | une association qui distribue du logiciel doit savoir sous quels termes ; c'est aussi ce qui la protège d'une appropriation privée |
| **RGPD** | registre de traitement, minimisation, durée de conservation, information des personnes | l'app traite des CV, des données de chantier et des données d'élus/agents ; une association est responsable de traitement comme une autre structure |
| **Accessibilité** | viser **WCAG 2.2 / RGAA 4.1** même sans obligation stricte | ⚠️ **rectification importante** : le RGAA ne s'impose pas automatiquement à une association (les organismes privés à but non lucratif sont **exclus**, sauf s'ils fournissent des services essentiels au public ou des services destinés aux personnes handicapées — et sauf si l'association est **majoritairement financée par des personnes publiques**, créée par elles, ou si plus de la moitié de ses administrateurs sont désignés par elles : dans ce cas elle est **dans le champ** de l'article 47). Si les clients sont des collectivités, l'accessibilité devient de toute façon une **exigence contractuelle**. Et le RGAA 5 (aligné WCAG 2.2) est annoncé **fin 2026** |
| **Comptabilité & transparence** | comptes annuels, rapport d'activité, publication | conditionne les subventions et la confiance |
| **Assurance & responsabilité** | attention aux modules qui produisent des calculs d'ingénierie | un prédimensionnement affiché sans avertissement engage ; la règle « jamais de calcul de sécurité seul » de la constitution couvre ce point |
| **Pérennité (« bus factor »)** | documentation, modules découplés, données exportables, aucune dépendance à un service payant | aujourd'hui, une seule personne porte tout le projet : c'est le **risque n°1** du passage en association |

### 2.3 La licence : trois options, une recommandation

| Option | Effet | Pour qui |
|---|---|---|
| **A. Cœur Apache-2.0 / MIT + services AGPL-3.0** | adoption maximale (entreprises, collectivités), protection du service en réseau | ⭐ **recommandée** : c'est le modèle « open-core » compatible association |
| **B. AGPL-3.0 partout** | tout dérivé diffusé doit rester libre, y compris en SaaS | si l'objectif est de garantir la non-appropriation avant tout |
| **C. Licence mixte** | gratuit pour associations/particuliers, payant pour entreprises | possible **plus tard**, mais incompatible avec une association si la licence est propriétaire ; à faire via **services** (hébergement, formation, intégration), pas via la licence |

> ⚠️ Le dépôt contient déjà des composants sous **LGPL-3.0** (IfcOpenShell envisagé), **GPL** (CloudCompare, Potrace…), **AGPL** (OpenDroneMap, SearxNG…) et des cas **NOASSERTION** (amont `gods-eye-view`). Un mélange non traité est le piège n°1 d'un projet qui se distribue. **La matrice de licences par composant est un prérequis de la V1**, pas un document tardif.

### 2.4 Financement : pistes à vérifier (aucune ne doit entrer dans l'architecture)

- Subventions numériques et territoriales (État, Région Occitanie, Sète Agglopôle, département) ;
- appels à projets « communs numériques » / logiciel libre ;
- mécénat technique (hébergement, CI, comptes développeur, matériel) ;
- formation / accompagnement facturé aux entreprises (compatible association si activité accessoire) ;
- contributions en nature (documents, relectures, tests terrain).

À noter : **les briques techniques doivent rester viables à budget nul**. Aucune subvention ne doit devenir une dépendance d'architecture.

---

## 3. « V1 fonctionnelle installable et utilisable facilement et rapidement » — la définition du fini

C'est l'objectif qui doit commander tout le reste. Voici la grille que je propose (à valider) :

| Critère | Seuil V1 |
|---|---|
| Installation | **1 fichier** téléchargé, installé sur Windows 10/11 **sans installer Node, Python, Docker** |
| Poids | < 150 Mo installé (hors données utilisateur) |
| Premier lancement | écran d'accueil clair, **aucune configuration obligatoire**, choix du dossier de données |
| Premier résultat utile | **< 5 minutes** : créer un projet, déposer des documents, voir la carte |
| Fonctionne hors ligne | oui, par défaut ; le réseau n'améliore que ce qui peut l'être |
| Modules | installables/désactivables **sans réinstaller** l'application |
| Mise à jour | automatique, signée, avec retour arrière possible |
| Données | **exportables à tout moment** dans un format lisible, sans l'application |
| Mise en route d'un tiers | une personne non technique de l'association peut installer et démarrer seule, avec le guide |

---

## 4. Le gisement : ce que les branches contiennent déjà

C'est la découverte la plus importante de ce tour : **la V1 est déjà largement écrite**, mais éparpillée dans des branches non fusionnées. Audit interne : **144 commits non fusionnés sur 14 branches**, dont 4 à fort contenu.

| Branche | Contenu réel | Ce qu'on en garde |
|---|---|---|
| `monorepo/arena/01a08385` — **NEXUS·OS** | runtime d'agents : routeur **8 fournisseurs / 20 modèles** avec repli, 22 agents, 30 compétences `SKILL.md`, 22 outils sandboxés, client **MCP**, mémoire, tâches, évaluations, créateur d'agents, export vers 12 harnais, **147 tests**, interface « bureau » montée sur `/os/` | **le module Agents de la V1** : c'est le plus gros actif logiciel neuf du dépôt |
| `monorepo/arena/01a08449` — **module BTP** | `projects/btp-conduite-travaux/` : **154 documents classés** en 7 familles, **7 rapports** (DCE/juridique, étude de prix, technique voirie-réseaux, DICT/AIPR, pilotage in-situ, réception/DOE/BIM, schéma directeur), **matrice de traçabilité**, inventaire JSON avec SHA-256, **28 sous-détails de prix** avec simulateur de marge, dashboard interactif | **le cœur métier de la V1** : matière, structure et contenus |
| `monorepo/feat/final-interface-skeleton-2026-10-07` | squelette d'interface unifiée, taxonomie en **12 catégories**, registre de capacités `interface_registry.json`, route `/interface` | **la trame de navigation** de Carré d'As |
| `monorepo/feat/tool-data-catalog-2026-10` | architecture modulaire documentée : `core/contracts/module.schema.json`, `canonical-record.schema.json`, `data/module_registry.json`, `integration_graph.json`, dossier `modules/`, catalogue unifié des données et outils | **le socle du contrat de module** — c'est exactement le « repo → sous-repo = module » demandé |
| `watchtower/arena/01a072e1` (+42 commits, 145 fichiers) | une maturité d'interface rare : **barre unique de fonctions** (24 fonctions, 4 catégories), **volant** (radial), **bascule 2D↔3D franche**, panneau FIL, planchers de lisibilité, docs `AUDIT-UI.md`, `CHARGE-MENTALE.md`, `CARTE-2D.md`, `VOLANT.md` | **les principes d'API et d'ergonomie** (voir `02-UI…`) |
| `watchtower/arena/dec9cd88` (+4 commits, 45 fichiers) | **hub INTEL** : socle territorial à 5 échelles, grille de certitude ✅ engagé / 📅 annoncé / 🔮 tendance / ⚠️ incertain, faits tracés, garde-fou codé « un fait sans source ne peut pas être marqué engagé » | **le modèle de vérité affichée** — à généraliser à toute l'app |
| `monorepo/arena/171a1f38` (PR #3, ouverte) | audit d'état des lieux 2026-10 : **9 projets, 52 constats**, inventaire, graphe, dérive main↔dépôts | **la carte des dettes** à traiter dans la V1 |
| `monorepo/arena/01a08385` (doc CAPACITES) | état mesuré : 3 apps Vite déjà buildées, 4 pages du monorepo en 200, NEXUS·OS monté, SSE fonctionnel, pytest 59 passed | **la preuve que ça tourne** |

**Conséquence directe :** la première phase de la V1 n'est pas « coder », c'est **consolider** (fusionner ces branches après revue), puis **découper en modules** selon le contrat. On économise des mois.

---

## 5. Architecture cible : Carré d'As est le shell, les modules sont les briques

### 5.1 La règle demandée

> **repo → sous-repo = module, plug in/out si besoin** — pour l'entretien et l'enrichissement.

Traduction en architecture :

```
                        CARRÉ D'AS (le shell installable)
   ┌───────────────────────────────────────────────────────────────────┐
   │  Accueil · Recherche (Ctrl+K) · Notifications · Comptes · Système │
   ├────────────┬────────────┬────────────┬────────────┬──────────────┤
   │   CARTE    │  CHANTIER  │ DOCUMENTS  │  AGENTS    │   COGNITION  │  ← modules
   │ Territo…   │  BTP/TP    │ DCE/prix   │ NEXUS·OS   │  HCSM/ROME   │     (plug in/out)
   ├────────────┴────────────┴────────────┴────────────┴──────────────┤
   │  CORE : contrats · registre · événements · permissions ·          │
   │         provenance · i18n · diagnostic · licences                 │
   ├──────────────────────────────────────────────────────────────────┤
   │  RUNTIME : fichiers · base locale · index de recherche · jobs ·    │
   │            réseau contrôlé · mises à jour · coffre de secrets      │
   ├──────────────────────────────────────────────────────────────────┤
   │  ADAPTATEURS : ponts vers projects/ (l'existant non encore migré)  │
   └───────────────────────────────────────────────────────────────────┘
```

### 5.2 Structure de dépôt (reprend et prolonge `feat/tool-data-catalog-2026-10`)

```
carre-das/
├─ apps/
│  └─ carre-das/          le shell (UI + runtime desktop) — un seul livrable installable
├─ core/
│  ├─ contracts/          schémas : module, record canonique, événement, permission
│  ├─ registry/           registre des modules + résolution des capacités
│  └─ sdk/                outillage pour écrire un module (JS et Python)
├─ modules/               UN DOSSIER = UN MODULE (auto-suffisant)
│  ├─ carte/              GIS : 2D, 3D, couches, entités, offline
│  ├─ chantier/           BTP : DCE, prix, suivi, plans, DOE
│  ├─ documents/          ingestion, OCR, extraction, index
│  ├─ agents/             NEXUS·OS (runtime, MCP, mémoire, évals)
│  ├─ cognition/          profils, compétences, ROME  [v1.1]
│  ├─ territoire/         indicateurs, dossiers communaux
│  ├─ recherche/          preuves, sources, claims (reaserch-engine)
│  ├─ temporal/           timeline, phasage 4D, chronos
│  └─ systeme/            paramètres, comptes, mises à jour, diagnostic
├─ adapters/              ponts vers l'existant (projets non migrés)
├─ projects/              sources historiques, gelées, pendant la migration
├─ data/                  données locales de l'utilisateur (hors dépôt en production)
├─ tools/                 scripts reproductibles (audit, inventaire, releases)
└─ docs/
```

### 5.3 Ce qui rend un module « plug in/out » (détail : `01-CONTRAT-MODULE.md`)

| Règle | Pourquoi |
|---|---|
| **Manifeste** (`module.json`) : id, version, domaine, capacités, permissions, événements consommés/produits, dépendances | la machine peut savoir ce qui est installable, compatible et autorisé |
| **Cycle de vie** : découvrir → installer → activer → désactiver → désinstaller, **sans redémarrer l'application** | c'est la demande explicite ; et c'est ce qui rend l'entretien supportable |
| **Isolation** : chaque module a ses dépendances, ses tests, son dossier de données ; un module cassé ne casse pas le shell | entretien et enrichissement |
| **Permissions** déclarées et journalisées (fichiers, réseau, exécution, comptes) | un module tiers ne doit rien pouvoir faire en silence |
| **Contrat d'événements** versionné (bus) plutôt qu'appels directs entre modules | ajouter un module ne doit pas obliger à modifier les autres |
| **Propriété des données** : une donnée a **un seul** module propriétaire, les autres la lisent | évite les 3 bases concurrentes actuelles |
| **Compatibilité** : `coreVersion` requise ; un module trop ancien est refusé avec un message clair | grossir sans casser |
| **Sandbox pour les tiers** : modules tiers en **WebAssembly** (Extism/WASI) | sécurité (voir §9) |

---

## 6. Contenu de la V1 : quels modules embarquent, lesquels attendent

| Module | V1 ? | Ce qu'il fait en V1 | Source principale |
|---|:--:|---|---|
| **Accueil / Command Center** | ✅ | point d'accès, état du système, derniers documents, actions rapides, recherche | squelette d'interface + NEXUS·OS |
| **Chantier (BTP)** | ✅ | projets, documents DCE, étude de prix (28 SDP), suivi (CR, NC, essais), plans, puis 3D | branche `01a08449` + corpus |
| **Documents** | ✅ | dépôt de fichiers, OCR, extraction (PDF/XLS/DOC), index, recherche instantanée | à construire (voir CH-2 du brief) |
| **Carte / Territoire** | ✅ | 2D MapLibre + IGN/OSM sans clé, cadastre, bâti 3D à la demande, entités, offline | Watchtower (2D) + socle INTEL |
| **Agents** | ✅ (léger) | chat, recherche documentaire, rédaction assistée, MCP ; 22 agents disponibles | NEXUS·OS |
| **Système** | ✅ | comptes (Google/OneDrive/local), mises à jour, diagnostic, licences, sauvegardes | à construire |
| **Recherche globale (Ctrl+K)** | ✅ | entités + documents + code + événements, avec provenance | à construire (core) |
| **Cognition / compétences** | ⏳ v1.1 | profils, ROME, graphe de compétences | proto-cognitorium |
| **Recherche & preuves** | ⏳ v1.1 | question → dossier sourcé | reaserch-engine |
| **Territoire (dossiers)** | ⏳ v1.1 | dossier communal automatisé | frontignan + INTEL |
| **Learning / CLE** | ⏳ v2 | apprentissage par problèmes | COGNITORIUM/learning |
| **Simulation, CAD, 3D avancé, OSINT, Language** | ⏳ v2+ | — | voir dossier recherche |

**Le principe de la V1 : une seule tranche verticale complète et irréprochable** (chantier + documents + carte + agents), pas une couverture large et superficielle.

---

## 7. Le module BTP comme brique puissante

Résumé — détail dans `03-MODULE-BTP.md`.

| Pilier | V1 | Au-delà |
|---|---|---|
| **Documents & DCE** | 154 documents déjà classés, recherche instantanée, extraction de quantités/prix | veille marchés publics, comparaison multi-chantiers |
| **Étude de prix** | 28 sous-détails de prix, simulateur déboursé sec / marge, comparaison DQE↔BPU↔DE | bibliothèque de prix partagée, index BT, révision de prix |
| **Suivi de chantier** | planning, comptes rendus, non-conformités, essais, DICT/AIPR, photos géolocalisées | avancement automatisé, facturation/situations, DOE généré |
| **Carte** | plan du chantier, phasage, réseaux, servitudes, DICT | jumeau numérique de chantier |
| **3D / modélisation** | visionneuses (IFC, glTF, nuages de points), mesures, coupes | modélisation paramétrique simple, scan→maquette, orthophoto |
| **Stats** | tableaux de bord (prix, délais, écarts, qualité) | analyses comparatives, prévisions |
| **Synchronisation** | compte Google (dossier applicatif) et/ou OneDrive, ou dossier réseau/NAS | multi-poste, partage contrôlé avec l'équipe |

Décision structurante à prendre pour la 3D : **Carré d'As assemble et visualise ; il ne réécrit pas un modeleur.** Les outils métier reconnus (FreeCAD/BIM, Blender, CloudCompare, IfcOpenShell, OpenDroneMap) sont **pilotés** et **branchés**, pas remplacés. C'est ce qui permet d'avoir une 3D utile en V1 sans trois ans de développement.

---

## 8. Interface : simple, affordante, cohérente

Résumé — détail dans `02-UI-PRINCIPES-ET-INSPIRATIONS.md`.

**Cinq règles que je propose d'imposer dès la V1 :**

1. **Un point d'accès, quatre portes.** L'accueil montre quatre grandes cartes (Projets/Chantiers · Carte · Documents · Agents) + la recherche. Pas de menu imbriqué.
2. **Rien n'est perdu.** Si une fonction existe, elle est atteignable ; sinon l'app le dit (règle issue de `AUDIT-UI.md` de la branche Watchtower).
3. **Chaque action répond.** Un clic produit toujours un retour visible (chargement, résultat, refus explicite). Aucun bouton muet.
4. **La vérité est visible.** Chaque donnée affiche sa provenance et sa certitude (✅ engagé / 📅 annoncé / 🔮 tendance / ⚠️ incertain) — modèle du hub INTEL, à généraliser.
5. **On ne montre jamais plus que nécessaire, mais jamais moins que utile.** Réduire la *charge extrinsèque* (la présentation), pas la complexité métier — la théorie de la charge cognitive et la mesure (NASA-TLX/RTLX) sont déjà analysées dans `CHARGE-MENTALE.md`.

**Inspirations retenues** (détail et sources dans le document UI) : de **tes branches** — barre unique de fonctions, volant, bascule 2D/3D franche, planchers de lisibilité, grille de certitude ; de **l'extérieur** — le *Command Palette Dock* de PowerToys 0.98 (2026) comme modèle de dock persistant et d'extensions, Linear/Raycast pour le clavier d'abord, Obsidian pour les modules et les coffres locaux, Milanote/Craft pour les cartes et les blocs, Dropbox Dash pour la recherche universelle.

---

## 9. Windows puis navigateur — implications

| Sujet | Windows (V1) | Navigateur (V2) |
|---|---|---|
| Enveloppe | **Tauri 2** (installeur NSIS/MSI, updater signé) | même UI React servie par un petit serveur local ou un hébergement statique |
| Fichiers | système complet, dossiers surveillés, gros fichiers | **File System Access API** + OPFS, avec limites explicites |
| Base locale | SQLite/PGlite sur disque | OPFS/IndexedDB (PGlite fonctionne en WASM) |
| Jobs lourds (OCR, photogrammétrie) | processus locaux, file d'attente, progression | impossible → soit serveur, soit outil externe |
| Comptes | coffre OS (Windows Credential Manager) | OAuth dans le navigateur, jetons jamais en clair |
| 3D | WebView2 + GPU local (⚠️ GTX 1060 : 2D par défaut) | mêmes limites GPU |
| Mises à jour | updater Tauri signé | déploiement continu |

**Règle d'architecture :** toute capacité système (fichier, processus, coffre, notification) passe par une **interface de runtime** avec deux implémentations (desktop, web). Un module ne doit jamais appeler `fs` ou `process` directement — sinon la version navigateur devient impossible.

⚠️ **Contrainte honnête** : certaines fonctions ne seront **jamais** équivalentes dans un navigateur (photogrammétrie locale, gros nuages de points, OCR massif). La version navigateur sera un **mode consultation/édition**, pas un clone du desktop converti.

---

## 10. Séquencement proposé de la V1

| Phase | Contenu | Critère de sortie |
|---|---|---|
| **P0 — Consolidation** (semaines 1-3) | fusionner les branches à fort contenu après revue (NEXUS·OS, BTP, interface, contrat de module, PR d'audit) ; **nommer le dépôt Carré d'As** ; nettoyer le corpus hors de Git ; figer la licence | un `main` unique, sans branche orpheline, avec licence et matrice de licences |
| **P1 — Socle** | contrat de module + registre + bus d'événements + permissions + base locale + recherche unifiée + i18n/a11y + Quality Gate | un module factice s'installe, s'active, se désactive **sans redémarrer** |
| **P2 — Shell** | l'application Carré d'As : accueil 4 portes, navigation, Ctrl+K, notifications, paramètres, comptes | l'app se lance, on navigue, on cherche, on configure |
| **P3 — Tranche BTP** | documents → extraction → prix → suivi → carte | un chantier réel de bout en bout sur les 154 documents |
| **P4 — Installable** | installeur Windows, premier lancement, mises à jour, sauvegarde/export | **la définition du fini du §3 est atteinte** |
| **P5 — 3D + sync** | visionneuses 3D, nuages de points, synchronisation compte Google/OneDrive | un plan 3D et une synchro qui ne perdent rien |
| **P6 — Navigateur** | runtime web, mode consultation | l'app s'ouvre dans un navigateur, sans installation |

---

## 11. Risques de cette trajectoire

| Risque | Gravité | Parade |
|---|---|---|
| **Fusionner les branches en aveugle** (144 commits, 14 branches) | élevée | revue branche par branche, tests avant fusion, ne rien jeter sans décision écrite |
| **Bus factor = 1** | très élevée | documentation opérationnelle, modules découplés, agents capables de reprendre (c'est déjà la pratique du projet) |
| **Licences hétérogènes** (LGPL, GPL, AGPL, NOASSERTION amont) | élevée | matrice de licences **avant** distribution ; exclure les composants incompatibles par option de build |
| **Corpus binaire dans Git** (~100 documents à la racine) | moyenne | sortir le corpus du dépôt (stockage + manifeste), garder les métadonnées |
| **Google OAuth** (quotas, révocations, vérification, confidentialité) | moyenne | scopes non sensibles (`drive.appdata`, `drive.file`), jetons dans le coffre OS, jamais de secret dans le client ; prévoir un mode sans compte |
| **Promesse d'accessibilité non tenue** | moyenne | RGAA/WCAG dès le design system, tests automatisés (axe-core) en CI |
| **Dispersion** (le risque permanent du projet) | élevée | la V1 est **une tranche verticale** ; tout le reste est explicitement « v1.1+ » |
| **Attentes de « modeleur 3D »** | moyenne | dire clairement ce qui est assemblé/piloté plutôt que réécrit (voir `03-MODULE-BTP.md`) |

---

## 12. Décisions à prendre maintenant

| # | Question | Recommandation |
|---|---|---|
| 1 | Licence | **cœur Apache-2.0 + services AGPL-3.0** ; matrice de licences obligatoire avant toute distribution |
| 2 | Périmètre V1 | **chantier BTP + documents + carte + agents**, rien de plus |
| 3 | Structure | shell Tauri + modules/ selon le contrat ; `projects/` gelé pendant migration |
| 4 | Nom du dépôt | renommer en `carre-das` **pendant la consolidation**, pas avant |
| 5 | Corpus | sortir les ~100 documents du dépôt Git (stockage + manifeste) |
| 6 | Sync comptes | Google (`drive.appdata`) **et** OneDrive **et** dossier local/NAS, derrière une interface unique |
| 7 | Accessibilité | viser WCAG 2.2 AA ; RGAA 5 à réévaluer à sa publication (fin 2026) |
| 8 | Agents | intégrer NEXUS·OS comme **module**, pas comme app séparée |
| 9 | Branches | fusionner après revue, sans exception, avant d'écrire du code neuf |
| 10 | Mesure | instrumenter localement (usage, performance, erreurs) — jamais d'envoi de données sans consentement explicite |

---

## 13. Ce que je n'ai pas tranché (et pourquoi)

- **Le périmètre exact de la 3D** : entre « visionneuse » et « modeleur », l'écart est de plusieurs mois. Recommandation : visionneuse + mesures en V1, décision sur le modeleur après P3.
- **Le sort de `proto-cognitorium`** : c'est l'UI la plus riche (ROME, decay, graphe 5 niveaux) mais elle repose sur React + Express + Gemini. À migrer ou à encapsuler ? À trancher au moment du module Cognition (v1.1).
- **La place de l'OSINT** : Watchtower le porte déjà ; pour une association, la doctrine légale (données personnelles, CGU, scraping) doit être écrite **avant** toute mise en avant.
- **Le rythme de fusion** des 14 branches : dépend de ton temps de validation. Les 4 branches à fort contenu d'abord, le reste au fil de l'eau.
