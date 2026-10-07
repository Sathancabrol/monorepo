# Analyse de la discussion, enrichissements et arbitrages

**Statut :** `ANALYSE` — opinions argumentées de l'agent, à valider par l'utilisateur. Rien ici n'est une décision.
Vérifications en ligne effectuées le **2026-10-07** via l'API GitHub (licence, activité, archivage). Le reste est marqué `[hypothèse]` ou `À VÉRIFIER`.
Comparer avec : `00-BRIEF-ARENA-RECHERCHE.md` (la mission confiée à l'agent de recherche) et `02-MATRICE-DOMAINES.csv` (le tableau).

---

## 1. Ce que la discussion apporte de solide

1. **La bonne intuition structurelle** : ne pas chercher des bibliothèques, mais **des systèmes déjà fonctionnels**, puis décider *conserver / fusionner / remplacer / adapter / plugin / réimplémenter / abandonner*. C'est exactement la bonne méthode, et elle est cohérente avec le principe P3 du projet.
2. **L'idée d'interface unifiée** comme finalité (et non la collection de modules).
3. **La détection des bons domaines lourds** : GIS, OSINT, agents, BTP, jumeau numérique, simulation, plugins, MCP, IA locale, licences, installation sans prérequis.
4. **Le classement P0→P3** comme tentative de priorisation.
5. **L'intuition juste sur plusieurs outils** : LadybugDB (voir §3.1 — c'est bien le successeur d'un projet clé), le trio MCP/ACP/A2A, Tauri pour l'installation, PostgreSQL+pgvector pour la mémoire.
6. **La mention de « git recherche en ligne / discussion / doc »** : l'analyse de dépôts (branches, issues, discussions, ADR) est en effet la source la plus fiable — et c'est exactement ce que le projet appelle déjà « Repo Intelligence Agent » (D24).

## 2. Le diagnostic de fond : le problème n'est pas les outils

La discussion parle surtout d'outils à intégrer. Or l'audit interne du projet dit autre chose, et je le confirme après lecture du dépôt :

| Ce que dit la discussion | Ce que dit le dépôt |
|---|---|
| « prototypes à exploiter » | Watchtower est une **application** (≈100 modules, 3 136 tests annoncés), pas un prototype ; proto-cognitorium est le **produit le plus riche fonctionnellement** (ROME, échelle épistémique, decay) |
| « fusionner en une UI cohérente » | il n'y a **pas d'UI à fusionner** : il y a un explorateur de fichiers à iframes (`app/`) et trois UI hétérogènes |
| « créer un Core minimal partagé » | exact — mais le vrai blocage est **le modèle de données et l'absence de bus d'événements**, pas le choix de la base |
| « choisir la stack GIS / graphe / etc. » | les choix sont **déjà pris** (ADR-007/008/009) ; il faut les **vérifier et les mettre à jour**, pas recommencer |
| « transformer Watchtower en module OSINT » | Watchtower est déjà un module monde+renseignement avancé ; c'est la **cible d'accueil**, pas la brique à transformer |
| « PC faible » | la contrainte réelle est une **GTX 1060 (6 Go VRAM)** — ce qui élimine beaucoup de solutions IA locales ambitieuses |

**Conséquence :** la réorganisation n'est pas un projet d'intégration d'outils, c'est un projet de **fondations** (shell + Core + bus + recherche + plugins + conformité) dans lequel on **verse** l'existant. Une liste d'outils sans ces fondations produira un deuxième éclatement.

## 3. Les sept corrections à apporter à la discussion

### 3.1 Kùzu est archivée → LadybugDB est le successeur *(VÉRIFIÉ le 2026-10-07)*

- `kuzudb/kuzu` : **dépôt archivé**, dernier commit **2025-10-10** (MIT, 4 022★).
- `LadybugDB/ladybug` : **MIT, actif** (1 821★, commit le 2026-10-07), avec liaisons Go/Ruby, un format de graphe proposé (`Ladybug-Memory/icebug-format`) et des benchmarks publics (graph-benchmark, LDBC).
- À l'inverse, `apache/age` est **actif** (4 874★, dernier commit 2026-09-19).

**Ce que ça change :** l'ADR-007 (PostgreSQL + AGE) reste valide **en mode serveur**, mais l'option « graphe embarqué » qui manquait au projet a maintenant un candidat sérieux. La discussion mentionnait « LadybugDB » sans expliquer — c'était l'intuition juste, il faut la formaliser.

### 3.2 Le tableau fait tout passer en P0 (≈45 domaines)

Un P0 qui contient tout ne priorise rien. Il faut trois vagues maximum par exercice :

- **Vague 1 (fondations, 0–3 mois)** : shell, Core + modèle, bus/événements, persistance, recherche, pipeline documentaire, identité/permissions minimales, conformité (RGAA/RGPD), Quality Gate.
- **Vague 2 (valeur visible, 3–9 mois)** : module chantier/BTP plein, GIS/territoire, agents (recherche + vérification), plugins, notifications/veille.
- **Vague 3 (élargissement, 9–24 mois)** : simulation, 3D/CAD/BIM avancés, apprentissage, sync multi-poste, marketplace.

Tout le reste est **P1/P2/P3 réel**, pas P0.

### 3.3 Trois domaines juridiques manquent, dont un est une obligation légale

- **Accessibilité / RGAA 4.1** : pour un téléservice destiné à une commune, l'accessibilité est **une obligation légale française** (et un critère d'achat public). Le tableau ne la mentionne pas. Elle doit être une contrainte de conception du design system, pas un chantier tardif.
- **RGPD / protection des données** : le projet traite des CV, des documents de chantier et des données communales ; la discussion le range dans « sécurité ». C'est insuffisant : il faut un registre, une minimisation, une politique de rétention et une séparation stricte entre données personnelles et dépôt public (l'audit interne signale déjà un incident passé).
- **Souveraineté / hébergement** : si demain une collectivité est cliente, les questions d'hébergement (SecNumCloud, HDS) et de sous-traitance arrivent immédiatement.

### 3.4 Les standards d'interopérabilité sont absents

Le tableau cite des outils, pas les **normes** qui rendent les données durables : IFC / bSDD / IDS / BCF (BIM), CityGML / 3D Tiles / OGC API (ville), PROV-O (provenance), SKOS (référentiels), GTFS (mobilité), OCS GE / INSPIRE (occupation du sol), xAPI (apprentissage). **Un outil se remplace, un standard reste.** C'est le meilleur rempart contre le verrouillage.

### 3.5 Les métiers réels de l'utilisateur sont sous-représentés

Le dépôt contient un corpus **réel et rare** : CCTP, CCAP, BPU, DQE, DETAIL-ESTIMATIF, métré, plans de phasage, profils en long, PAQ, essais (plaque, double-anneau), fiches de non-conformité, DT/DICT, AIPR, comptes rendus, planning annuel. Autrement dit : **l'étude de prix, le métré et le suivi de chantier**, qui ne figurent pas dans le tableau. C'est pourtant :
- le meilleur jeu de test du pipeline documentaire (CH-2) ;
- le cas d'usage qui prouve la valeur en 90 jours ;
- la source de revenus la plus évidente.

Manquent aussi : **risques & résilience** (inondation, RGA/sécheresse — critique en Occitanie), **mobilité** (PEM de Frontignan), **climat/énergie/environnement**, **réseaux et fluides** (AEP, assainissement), **physique/ingénierie**.

### 3.6 La discussion ignore la dette de fond du dépôt

- **Corpus de ~100 documents à la racine du dépôt** : pratique pour l'accès, coûteux pour Git (binaires lourds, historique définitif). À terme : `corpus/` versionné à part ou hors Git, avec manifeste.
- **Clés API dans le navigateur** (constat C4 du R&D) : incompatible avec toute ouverture multi-utilisateur ou LAN.
- **`localStorage`** comme persistance des PoC : à remplacer, mais **après** avoir défini le modèle de données (sinon on migre deux fois).
- **`gods-eye-view` amont en NOASSERTION** malgré un README MIT : à clarifier avant tout nouvel import.
- **Données non commerciales** (TeleGeography en CC BY-NC-SA) : à isoler dans un paquet exclu des builds commerciaux.

### 3.7 La discussion confond « outils puissants » et « outils adaptés »

Exemples typiques de pièges sur cette machine et ce contexte :
- **Unreal Engine** : disproportionné (GTX 1060, 0 €/mois, projet solo) — l'idée de moteur 3D doit rester sur Three.js/Babylon/Cesium.
- **Neo4j** : à écarter sauf besoin réel de traversées profondes (ADR-007 le dit déjà) ; le projet est à 1–2 sauts.
- **Frameworks multi-agents lourds** : à n'adopter que si l'exécution durable devient nécessaire (ADR-008 le prévoit déjà).
- **n8n** (fair-code, non OSI) : contradiction si le projet vise une licence libre.
- **Qdrant/Milvus** : surdimensionnés tant que le corpus reste < 1 M de vecteurs.
- **Ghidra/angr/Frida** : excellents mais hors sujet tant que le socle n'existe pas (P2, module isolé).
- **Marketplace** : à définir (manifeste + permissions) mais à construire **après** les plugins.

---

## 4. Ce que je prendrais pour le monorepo (proposition, à challenger)

> Statut : **proposition argumentée**. Chaque ligne devra être confirmée ou infirmée par l'agent de recherche (vérification licence/activité/performance) avant décision.

| # | Brique | Proposition | Pourquoi | Risque / à vérifier |
|---|---|---|---|---|
| 1 | **Shell** | **Tauri 2** + UI web (React/TS) + **sidecar Python** (le FastAPI existant) | 1 installeur Windows, 0 prérequis (Node/Python/Docker), empreinte mémoire faible, sécurité par capacités, écosystème actif (Apache-2.0, 111 638★, actif) | WebView2 requis (présent sur Win10/11) ; maturité de l'updater signé |
| 2 | **UI** | React 19 + TS + **Tailwind + shadcn/Radix**, **TanStack** (Query/Table/Virtual), **Dockview** pour les panneaux, palette `cmdk`-like | Réutilise le proto React existant ; accessibilité Radix (RGAA) ; dock éprouvé | Uniformiser avec le vanilla JS de Watchtower : prévoir une encapsulation progressive (iframe → composants) |
| 3 | **Carte** | **MapLibre GL JS en 2D par défaut**, **Cesium en 3D à la demande** | Cesium est déjà là mais la roadmap interne dit qu'il « sature la carte graphique » ; la 2D couvre 80 % des besoins | Vérifier le coût réel de la bascule et le cache hors ligne (PMTiles + Martin) |
| 4 | **Données** | Un **schéma canonique** (8 entités + socle épistémique) ; **démarrage embarqué** (PGlite ou SQLite), **migrations SQL identiques** pour PostgreSQL serveur | Une seule vérité par donnée ; pas de double migration ; mono-poste d'abord, serveur ensuite | PGlite (WASM) : maturité pour un usage intensif ; à mesurer |
| 5 | **Graphe** | Commencer par **SQL récursif** ; évaluer **LadybugDB** (embarqué, MIT) ; garder **AGE** pour le mode serveur | Le projet fait des traversées 1–2 sauts ; Kùzu étant archivée, LadybugDB est l'option embarquée crédible | LadybugDB est **jeune** (1 821★) : vérifier support, docs, stabilité, format de fichier |
| 6 | **Événements** | **Construire** un bus typé + journal append-only + projections (≈200–400 lignes) | C'est ce qui manque le plus (constat C3 : les modules s'appellent directement) ; trop spécifique pour un achat | Discipline d'équipe : interdire les appels directs module↔module |
| 7 | **Recherche** | **Un seul index** : FTS (SQLite FTS5 ou Tantivy) + vecteurs (sqlite-vec / pgvector) + fusion RRF | Le « Ctrl+K universel » est un pilier d'expérience ; un index par module = échec garantie | Performances sur 100 k documents + vecteurs ; mesure obligatoire |
| 8 | **Documents** | Pipeline **Marker / Docling / MinerU** + **camelot/pdfplumber** (tableaux) + **LibreOffice headless** (.xls/.doc) + Tesseract/OCRmyPDF (scans) | Le corpus BTP contient les deux pires cas : vieux formats et tableaux chiffrés | **Vérifier l'exactitude des chiffres** : un DQE mal extrait est plus dangereux qu'une absence d'extraction |
| 9 | **IA** | **Un point d'entrée unique** (LiteLLM ou maison) : local (llama.cpp/Ollama, modèles 3–8B quantifiés) + cloud plafonné en secours ; **Outlines/Instructor** pour le JSON garanti | Le projet exige l'abstraction fournisseur (P4/ADR-008) et le plafonnement (audit coûts) | 6 Go VRAM : beaucoup de tâches devront rester cloud — le dire honnêtement |
| 10 | **Agents** | **MCP d'abord** ; réutiliser les patterns de **Goose** (Apache-2.0, 55 032★) et **OpenHands** (MIT, 90 161★) ; **garder l'orchestrateur de preuves maison** (reaserch-engine) comme cœur recherche/vérification | Ne pas réécrire un runtime, mais ne pas perdre l'avance du projet sur la traçabilité des preuves | Vérifier les licences et la dépendance à des modèles payants |
| 11 | **Plugins** | **Extism** (WASM, BSD-3, 5 787★) + manifeste + permissions, avec **dogfooding** des ≈100 modules Watchtower | Isolation réelle, multi-langage, pas de redémarrage ; c'est la réponse aux 57 modules auto-déclarés | Définir les permissions **avant** d'ouvrir aux tiers (D12) |
| 12 | **Qualité** | `uv` (Python) + `pnpm` + **Turborepo** + **Quality Gate en 1 commande** ; **Playwright** pour les tests visuels et l'accessibilité | Le projet a du code dans 3 langages et des modules fragiles | Le monorepo tooling ne doit pas devenir un projet en soi |
| 13 | **Conformité** | RGAA/WCAG + RGPD **dans le design system dès le départ** | Public cible = collectivités ; l'accessibilité est une obligation légale, pas une option | Audit axe-core à intégrer en CI |
| 14 | **BIM / IFC** | **IfcOpenShell** (LGPL-3.0, vérifié actif) + visionneuse web (web-ifc) ; **quantités** comparées au DQE | Le lien BIM ↔ économie de la construction est la vraie valeur, pas la 3D décorative | LGPL : vérifier les conditions de distribution ; tester l'extraction sur un vrai IFC |
| 15 | **Données publiques FR** | Un connecteur unique et cachable : IGN (BD TOPO, LiDAR HD), BAN, cadastre, DVF, OCS GE, INSEE, Géorisques, BRGM | C'est ce qui rend la carte **utile** localement, pas juste belle | Licences et volumes à documenter flux par flux |

## 5. Ce que j'écarte ou reporte explicitement

| Écarté / reporté | Raison |
|---|---|
| Unreal Engine, moteurs 3D lourds | Machine cible, budget, utilité |
| Neo4j en v1 | ADR-007 : charge à 1–2 sauts |
| Qdrant/Milvus en v1 | Sous-dimensionné → surdimensionné |
| Marketplace (D74) maintenant | Dépend du SDK de plugins (D13) |
| Reverse engineering (D69) maintenant | Hors périmètre tant que le socle n'existe pas |
| Multi-utilisateur (D11 complet) en vague 1 | Mono-poste d'abord ; l'identité locale suffit |
| `localStorage` comme persistance cible | À remplacer après le modèle de données, pas avant |
| Cesium comme moteur de carte par défaut | Coût GPU constaté |
| n8n comme socle d'automatisation | Licences non OSI ; Activepieces ou maison |
| Dépendance à Claude Code et services non plafonnables | Budget, verrouillage |
| Construire un noyau géométrique, un LLM ou une base graphe | Principe P3 : on ne réimplémente pas ce qui existe |

## 6. Le premier palier démontrable que je proposerais : « le chantier vivant »

**Pourquoi ce palier :** il utilise le corpus réel, il traverse tout le socle (documents → données → carte → temps → agents → recherche), et il produit un résultat **immédiatement utile à l'utilisateur** — pas une démonstration technique.

**Parcours cible (90 jours)**
1. Je crée un **projet chantier** (nom, commune, phase, documents).
2. Je **dépose les documents** (DQE, BPU, CCTP, plans, comptes rendus, essais) → extraction, indexation, recherche instantanée.
3. L'app **extrait les quantités et les prix** du DQE/BPU, les met en face d'un estimatif et **signale les écarts**.
4. Le **plan et le planning** s'affichent : carte 2D du chantier (MapLibre) + timeline des phases (4D), reliées aux documents.
5. La **veille** (BOAMP, presse locale, Météo-France) remonte dans le centre de notifications avec la source.
6. Un **agent** produit un **compte rendu de réunion** pré-rempli à partir des documents et de la timeline, avec citations — et rien n'est écrit sans validation.
7. Le **registre épistémique** s'applique partout : chaque chiffre affiché dit d'où il vient (page du PDF, date, confiance).

**Ce que ce palier prouve :** Core + bus + recherche + pipeline documentaire + carte + timeline + agents + conformité — c'est-à-dire l'essentiel de la vague 1. Et il est vendable à une entreprise de TP ou à une commune.

## 7. Séquencement proposé (à discuter)

| Vague | Durée | Contenu | Critère de sortie |
|---|---|---|---|
| **V1 — Fondations** | 0–3 mois | Shell installable, Core + modèle canonique, bus/journal, persistance, recherche unifiée, pipeline documentaire, a11y/RGPD, Quality Gate | « Le chantier vivant » (§6) démontré sur des données réelles |
| **V2 — Valeur métier** | 3–9 mois | Module chantier complet (DQE/métrés/NC/OS/DOE), GIS/territoire (données IGN), agents recherche + vérification, SDK de plugins, veille/alertes | Un utilisateur réel travaille dessus une semaine sans revenir aux fichiers Excel |
| **V3 — Élargissement** | 9–24 mois | Simulation, BIM/IFC, 3D avancée, Learning Engine, synchronisation multi-poste, marketplace | Un tiers écrit un module sans toucher au core |

## 8. Décisions que je te recommande de prendre maintenant

| Question (§10 du brief) | Ma recommandation | Pourquoi |
|---|---|---|
| Nom de l'app | Choisir un nom court, distinct de « Cognitorium » (nom du système global) — **« Carré d'As » n'apparaît nulle part dans le dépôt** | Un produit a besoin d'un nom ; l'ambiguïté actuelle ralentit la doc |
| Priorité | **BTP/chantier d'abord** (utilisateur réel, corpus réel, valeur démontrable), territoire ensuite | C'est là que la preuve de valeur est la moins coûteuse |
| Multi-utilisateur | Reporter à la vague 3 ; préparer les données pour (identité locale, pas de données globales implicites) | Éviter la sur-ingénierie immédiate |
| Cloud | **Zéro cloud par défaut, cloud plafonné optionnel** pour les tâches où le local est insuffisant (recherche, gros documents) | Cohérent avec local-first et budget |
| Données de test | **Oui**, anonymiser 10–20 documents et les utiliser comme jeu de test officiel | C'est le meilleur accélérateur du projet |
| GPU | Concevoir pour **6 Go de VRAM** ; documenter ce qui devient possible avec 12–16 Go | Éviter de dépendre d'un achat |
| Ouverture | Garder privé le temps de stabiliser le socle ; décider la licence **avant** d'accepter des contributions externes | La licence conditionne tout le reste (D73) |
| Ambition V1 | **Une tranche verticale parfaite** (chantier) plutôt qu'une couverture large | Un socle prouvé vaut mieux que dix moitiés |

## 9. Hygiène du dépôt (à traiter, sans urgence immédiate)

1. **Corpus de ~100 documents à la racine** : le déplacer vers un dossier dédié (ou un stockage externe + manifeste), pour ne pas alourdir Git définitivement. *(Action à valider : je ne déplace rien sans ton accord.)*
2. **`MANIFEST.json`** : il référence `COGNITORIUM`, `watchtower`… avec des SHA d'août/septembre ; à régénérer.
3. **`data/github_inventory.json`** : snapshot à rafraîchir (le script existe).
4. **Secrets** : confirmer la rotation recommandée par l'audit sécurité.
5. **`Language-decoder`** : décider — lui donner un rôle (ASR/TTS/OCR locaux, comme le suggère l'audit outils) ou l'archiver.
6. **Nommage des dossiers** : `reaserch-engine` (faute de frappe d'origine) est conservé partout ; la corriger maintenant coûte peu, plus tard coûte cher.

---

## 10. Ce qu'il reste à décider ensemble

1. Est-ce que la **cible « produit pour collectivités »** est réelle (elle change RGAA, RGPD, hébergement, prix, et donc la V1) ?
2. Est-ce que je dois **commencer à implémenter** une partie (par exemple l'épinglage du modèle canonique + le bus + la recherche), ou est-ce que tout reste en phase d'analyse jusqu'à la livraison du brief de recherche ?
3. Est-ce que l'**application unifiée doit viser le desktop d'abord** (Windows) ou un fonctionnement dans le navigateur d'abord ?
4. Est-ce qu'on **garde les 9 dépôts séparés** (avec le monorepo comme poste de pilotage) ou est-ce qu'on **fusionne physiquement** par étapes ?
5. Est-ce que le **corpus BTP peut servir de jeu de test officiel** du projet ?
