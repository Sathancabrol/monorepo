# Concept art & prompts pour IA — Carré d'As

> **À quoi sert ce document.** Le tableau (`01-TABLEAU-DOMAINES.md`) dit *ce que le logiciel doit faire*.
> Celui-ci dit **à quoi il doit ressembler et ce qu'il doit montrer**, sous une forme directement exploitable
> par une IA de génération d'images, puis par une IA de génération d'interface.
>
> **Règle d'or :** ces images ne sont pas des maquettes à copier pixel par pixel. Ce sont des **directions** :
> elles servent à fixer une ambiance, une hiérarchie de lecture et des repères d'interface. Le seul document
> qui fait autorité pour les couleurs et les composants reste **`shell/assets/tokens.css`** (design system repris
> du prototype d'origine). Toute image qui contredit ces valeurs est une **illustration**, pas une spécification.

---

## 1. Direction artistique globale

**Formule :** *« OS de connaissance + centre de commandement + laboratoire scientifique + jeu de stratégie sérieux. »*

| Ce qu'on veut | Ce qu'on refuse |
|---|---|
| Sombre graphite / bleu nuit, verre sombre maîtrisé | Le cyberpunk décoratif, les néons gratuits |
| Cartographie **réaliste** (satellite, IGN, OSM), pas d'hologramme cliché | Les écrans bleus « film de SF » illisibles |
| Accents lumineux **très** sobres, réservés au signal | Le dégradé partout, le bruit visuel |
| Typographie technique, **données réellement lisibles** | Les fausses données, la fausse précision |
| Profondeur 2D/3D assumée, densité maîtrisée | Le vide « design » qui cache l'information |
| Inspirations : centres opérationnels, logiciels scientifiques, outils professionnels, jeux 4X | Les copies de dashboard SaaS génériques |

**Palette imposée (celle du prototype d'origine) :**

| Rôle | Hex | Sens |
|---|---|---|
| Vide / fond | `#050508` | ce qui n'est pas encore connu |
| Surface élevée | `#0A0A12` | panneaux, barres |
| Panneau | `#1A1A2E` | cartes, fiches, onglets |
| Texte | `#E8E8F0` / `#8A8AA8` / `#4A4A6A` | trois niveaux de lecture |
| **Plasticité (accent)** | **`#00E5CC`** | ce qui se construit, la sélection active |
| **Transfert** | **`#9B59B6`** | ce qui circule d'un domaine à l'autre, les ponts |
| Alerte | `#FF3366` | ce qui doit être vérifié |
| Établi / planifié / hypothèse | ✅ / 📅 / 🔮 | grille de vérité épistémique |

**Typographie :** Inter (textes, interfaces) + JetBrains Mono (sources, identifiants, valeurs, code).

**Interdits transverses :** pas de texte illisible en petit, pas de mots inventés à l'écran, pas de faux indicateurs
qui ne veulent rien dire, pas d'anglais décoratif, pas de logo Carré d'As déformé, **pas de fausse précision**.

---

## 2. Ta planche de référence, reconstituée pour l'IA

L'image fournie le 08/10/2026 n'est pas joignable par un agent qui lit ce fichier : voici sa **description exacte**,
à recopier dans un prompt de vision globale si besoin.

> **Titre :** « CARRÉ D'AS — OS DE CONNAISSANCE ET D'ACTION ». Sous-titre : « Observer · Comprendre · Décider · Agir · Prévoir ».
> **Colonne gauche :** un **diagramme en anneau** — au centre trois briques (Context Engine, Event Bus, Knowledge Graph),
> autour sept capacités reliées par des liens : Territory/Atlas, Projects BTP/Planning, Watchtower OSINT/Intel,
> Cognitorium Compétences/Métiers, Chronos Timeline, Simulation Scénarios, Nexus Agents IA ; légende : Données / Événements / Agents / Contextes.
> **Sous ce diagramme :** « Principes fondateurs » (Local first, Ouvert, Extensible, Sécurisé, Sécable) et une **pile technique** en couches :
> UI (Panneaux · Vues · Widgets · Layouts) → Core Engine (Context Engine, Event Bus, Entity Registry, Permission) →
> Services (Data, Search, Agent, File) → Storage (SQLite/DuckDB, Filesystem, Graph DB, Cache) → Externe (Tauri, Rust,
> SQLite, plugins Tauri, Extism, MCP, WebAssembly, Wasmtime, MapLibre, DuckDB, llama.cpp, Syncthing, Docker).
> **Au centre, une grille de 12 vignettes de concept art** : 1. Command Center · 2. Territory/Atlas · 3. Watchtower ·
> 4. Chronos · 5. Entity Dossier · 6. Knowledge Graph · 7. Nexus – Agents · 8. Repo Intelligence · 9. BTP Command ·
> 10. Digital Twin · 11. Cognitorium · 12. Learning Engine — chacune avec une capture d'interface sombre et une légende courte.
> **En bas :** « 2D ↔ 3D ↔ Temps », « Vue stratégique (Strategic View) », « Style visuel » (nuancier + icônes de types de vues :
> cartes, graphes, timelines, tableaux, 3D, terminal) et le mot d'ordre « Connaissance connectée, décision éclairée, action maîtrisée ».
> **Une correction de fond :** la pile cite à la fois **Extism** et **Wasmtime** (Extism *utilise* Wasmtime : une seule ligne suffit),
> et cite **Docker**, ce qui contredit la règle « installable sans Docker » — Docker reste un outil de développement, hors produit.

---

## 3. Les quatre types d'images

| Type | Objectif | Nombre | Public |
|---|---|---|---|
| **01 — Vision globale** | montrer le système entier (anneau + couches + principes) | 1 | décideur, lecteur pressé |
| **02 — Concept art de module** | donner une identité visuelle à chaque module | 12 + 8 | équipe, futur design |
| **03 — UI fonctionnelle** | montrer concrètement écrans, panneaux, interactions | 6 | développement |
| **04 — Architecture système** | montrer comment les briques communiquent | 1 + 3 coupes | architecture |

---

## 4. Le gabarit de prompt (à respecter pour chaque image)

```
RÔLE          : architecte produit et directeur artistique du poste de travail « Carré d'As »
CONTEXTE      : application locale, sombre, modulaire, pour la connaissance et l'action ; hors ligne ; PC modeste
OBJECTIF      : <ce que l'image doit montrer, en une phrase>
UTILISATEUR   : <qui regarde cet écran : opérateur, chef de chantier, chercheur, décideur associatif>
DONNÉES VISIBLES : <des données crédibles et lisibles, jamais de faux indicateurs inventés>
STRUCTURE UI  : <zones de l'écran, panneaux, barres, onglets, proportions>
INTERACTIONS  : <ce qu'on comprend pouvoir faire : survoler, sélectionner, filtrer, comparer, ouvrir une fiche>
STYLE         : sombre `#050508`/`#0A0A12`/`#1A1A2E`, accent `#00E5CC`, transfert `#9B59B6`, alerte `#FF3366`,
                Inter + JetBrains Mono, verre sombre maîtrisé, profondeur 2D/3D, cartographie réaliste
CONTRAINTES   : densité maîtrisée, hiérarchie de lecture nette, texte lisible, pas de néon gratuit,
                écran 16:9 de poste de travail, cohérent avec les autres planches
INTERDITS     : cyberpunk décoratif, hologramme cliché, données fausses, anglais décoratif, logo déformé, esthétique SaaS générique
```

---

## 5. Les douze fiches principales (type 02)

### art-01 · Command Center — *accueil · domaine D27*
**Concept** : le poste de commandement — on voit tout le système d'un coup d'œil.
**Description visuelle** : vue centrale sombre ; au centre, la carte du territoire active ; autour, des panneaux
translucides : projets en cours, agents actifs, derniers événements, alertes ; une timeline horizontale en bas.
**Éléments UI** : navigation globale, carte miniature, timeline, agents actifs, événements, ressources, alertes.
**Prompt assemblé** : « Écran d'accueil d'un poste de commandement logiciel sombre et sobre : au centre une carte
cartographique réaliste d'un territoire, autour des panneaux de verre sombre montrant des projets, des agents en
cours d'exécution, un flux d'événements horodatés et quelques alertes ; une frise temporelle horizontale en bas ;
palette graphite `#050508`/`#1A1A2E` avec un accent cyan `#00E5CC` réservé à la sélection ; typographie technique ;
aucun néon gratuit ; rendu photoréaliste d'interface, 16:9. »

### art-02 · Territory / Atlas — *module `carte` · domaines D48→D50*
**Concept** : la carte stratégique de territoire, du monde au bâtiment.
**Description visuelle** : vue satellite/2D d'un littoral méditerranéen (Sète, Thau) avec zoom progressif visible
(france → région → agglo → commune → quartier → bâtiment) ; un panneau de couches activables à gauche ; valeurs mesurées.
**Éléments UI** : niveaux de zoom, couches (bâti, réseaux, risques, environnement, population), opacité, dates, échelle, coordonnées.
**Prompt assemblé** : « Interface de système d'information géographique : carte réaliste d'une côte méditerranéenne
française, panneau de couches à gauche avec cases à cocher (bâti, réseaux, risques inondation, espaces verts), barre
d'échelle et coordonnées en bas à droite, curseur de zoom multi-échelle indiquant monde → région → commune → bâtiment ;
tons sombres graphite, accent cyan discret ; données cartographiques lisibles ; pas d'hologramme. »

### art-03 · Watchtower — *module `agents` (OSINT) · D39, D40*
**Concept** : la salle de renseignement — sources, dossiers, alertes, liens.
**Description visuelle** : carte du monde + panneau de **sources** avec dates et niveaux de confiance, liste de dossiers
entités, flux d'alertes ; des liens fins relient événements et lieux.
**Éléments UI** : OSINT, sources, relations, timeline, alertes, dossiers, filtres par fiabilité.
**Prompt assemblé** : « Poste d'analyse de renseignement en sources ouvertes : grande carte du monde à gauche,
à droite un registre de sources datées avec niveau de confiance (✅ établi, 📅 planifié, 🔮 hypothèse), une liste de
dossiers et un flux d'alertes ; traits de liaison fins entre lieux et événements ; esthétique centre opérationnel
sobre, sombre, lisible ; aucune donnée inventée présentée comme réelle. »

### art-04 · Chronos — *module `carte` (timeline) · D51*
**Concept** : la frise temporelle immersive, multi-échelle.
**Description visuelle** : timeline horizontale occupant la largeur, graduée en heures → jours → décennies ; des
événements empilés par nature (chantier, veille, cognition, territoire), avec un curseur de rejeu.
**Éléments UI** : échelles, empilements, filtres, curseur de rejeu, densité, comparaison de périodes.
**Prompt assemblé** : « Frise chronologique professionnelle horizontale à plusieurs échelles (de la seconde à la
décennie) : événements empilés par catégories colorées discrètement, curseur de rejeu, zooms ; fond graphite très
sombre, texte monospace pour les dates ; impression de densité maîtrisée et de lisibilité scientifique. »

### art-05 · Dossier d'entité universel — *D09, D44*
**Concept** : la fiche 360° d'une entité (personne, lieu, entreprise, chantier, document).
**Description visuelle** : à gauche, une identité (nom, type, aliases, identifiants) ; au centre, une carte et une
timeline intégrées ; à droite, relations, sources avec dates, documents liés, indices de confiance.
**Éléments UI** : identité, relations, sources, événements, documents, géolocalisation, niveau de preuve.
**Prompt assemblé** : « Dossier numérique augmenté d'une entité : panneau d'identité à gauche, carte et frise
temporelle au centre, à droite une liste de sources numérotées avec dates et citations, et un graphe de relations ;
chaque information est reliée à sa source ; esthétique sobre type outil d'enquête professionnel, sombre, dense mais clair. »

### art-06 · Knowledge Graph — *module `graphe` · D05*
**Concept** : le réseau de connaissances en 2D/3D.
**Description visuelle** : graphe de nœuds typés (personnes, lieux, projets, compétences, documents, événements) ;
arêtes colorées : grises = structure, **violettes `#9B59B6` = ponts entre domaines** ; panneau de filtres et de provenance.
**Éléments UI** : nœuds, relations, provenance, confiance, filtres, focus, chemins, vue liste accessible.
**Prompt assemblé** : « Visualisation de graphe de connaissances : nœuds circulaires typés par couleur discrète,
arêtes fines, quelques arêtes violettes `#9B59B6` reliant des communautés distinctes, panneau latéral de filtres et
de provenance ; fond `#050508` presque noir ; sensation d'exploration savante, pas de décoration. »

### art-07 · Nexus — Agents — *module `agents` · D29→D35*
**Concept** : le centre de contrôle des agents.
**Description visuelle** : plusieurs agents spécialisés autour d'un espace de travail partagé ; pour chacun : tâche en
cours, outils autorisés, permissions, mémoire, journal ; un agent « vérificateur » distinct qui contrôle un producteur.
**Éléments UI** : agents, tâches, outils, permissions, mémoire, journaux, verrous, budget de ressources.
**Prompt assemblé** : « Salle de contrôle d'agents logiciels : plusieurs cartes d'agents alignées, chacune avec sa
tâche, ses outils et ses permissions, une barre de progression, un journal défilant ; un agent annoté « vérification »
examine le travail d'un autre ; interface technique sombre, accent cyan pour l'état actif, rouge `#FF3366` pour ce qui
nécessite attention ; aucune fioriture. »

### art-08 · Repo Intelligence — *D24 (archéologie Git)*
**Concept** : un dépôt Git vu comme une civilisation, avec son histoire.
**Description visuelle** : arbre de branches volumétrique, commits en strates, PR et issues en annotations, courbe
d'activité sur 12 mois, forks comme ramifications.
**Éléments UI** : arbre Git, branches, commits, PR, issues, fichiers, dépendances, activité, licences.
**Prompt assemblé** : « Visualisation archéologique d'un dépôt de code : arbre de branches en volume, strates de
commits, annotations de pull requests et d'issues, courbe d'activité mensuelle, ramifications de forks ; rendu
technique sombre, lisible, inspiré des outils de développement professionnels ; une légende claire des licences. »

### art-09 · BTP Command — *module `btp` · D56→D63, D82, D88*
**Concept** : le centre de contrôle chantier.
**Description visuelle** : maquette 3D du chantier à gauche, planning (Gantt) en bas, coûts et métrés à droite,
sécurité et incidents en encart, météo et logistique en bandeau.
**Éléments UI** : BIM 4D/5D, planning, coûts, sécurité, matériel, incidents, conformité DT/DICT, documents.
**Prompt assemblé** : « Poste de conduite de chantier : maquette BIM 3D d'un bâtiment en construction à gauche,
diagramme de Gantt en bas, panneaux de coûts, métrés et quantités à droite, encart sécurité et conformité, bandeau
météo et livraisons ; ambiance chantier professionnelle, sombre, très lisible en plein jour ; données réalistes,
pas de science-fiction. »

### art-10 · Digital Twin — *D52*
**Concept** : le même ouvrage, réel / modèle / historique.
**Description visuelle** : vue triple synchronisée : photo réelle, maquette BIM, coupe historique avec curseur temporel.
**Éléments UI** : réel ↔ BIM ↔ GIS ↔ historique, capteurs, dates, écarts, alertes.
**Prompt assemblé** : « Jumeau numérique : trois vues synchronisées du même site en construction — photographie
réelle, modèle 3D et vue historique à une date antérieure ; une frise relie les trois ; quelques mesures et capteurs ;
esthétique ingénierie sobre, sombre, précise. »

### art-11 · Cognitorium — *module `cognition` · D41→D43*
**Concept** : l'arbre cognitif vivant d'une personne.
**Description visuelle** : constellation de compétences (nœuds) reliée à des **preuves** (documents, expériences,
réalisations) ; probabilités affichées avec honnêteté ; évolution dans le temps ; passerelles vers des métiers.
**Éléments UI** : compétences, preuves, confiance, évolution, métiers, écarts, recommandations.
**Prompt assemblé** : « Arbre cognitif vivant : constellation de compétences reliées à des preuves (documents,
projets, expériences) ; chaque nœud affiche un niveau de confiance honnête ; des chemins se dessinent vers des
métiers cibles ; tons sombres, accents cyan et violet, sensation d'outil de réflexion, pas de gamification enfantine. »

### art-12 · Learning Engine — *D43*
**Concept** : le laboratoire d'apprentissage — agir d'abord, comprendre ensuite.
**Description visuelle** : une situation interactive (scénario) à gauche ; conséquence simulée au centre ; le concept
apparaît ensuite à droite, avec la trace du raisonnement et un transfert vers un autre contexte.
**Éléments UI** : choix → conséquence → concept → transfert, progression, hypothèses, rétroaction.
**Prompt assemblé** : « Laboratoire d'apprentissage par situation : à gauche un scénario manipulable, au centre le
résultat d'une décision avec ses conséquences chiffrées, à droite le concept expliqué et sa réutilisation dans un
autre contexte ; interface sobre, pédagogique, sombre ; pas de bulles d'aide envahissantes. »

---

## 6. Les huit fiches complémentaires (type 02)

| Fiche | Domaine | Concept | Prompt assemblé (court) |
|---|---|---|---|
| **art-13** | D60, D61 | **Drone / LiDAR — poste de pilotage** | « Poste de télédétection : vue terrain, trajectoire de vol planifiée, nuage de points coloré par altitude, orthophoto en incrustation, mesures de volume ; esthétique topographique sombre et précise. » |
| **art-14** | D45 | **Research Lab — mur de preuves scientifiques** | « Espace de recherche : articles reliés à des hypothèses et à des expériences, citations numérotées, niveaux de preuve, graphe de citations ; sobre, dense, lisible comme une revue scientifique. » |
| **art-15** | D64→D68 | **Simulation Lab — monde simulé** | « Monde simulé manipulable : agents, ressources, flux et contraintes représentés sur une carte, panneau de paramètres, résultats comparés à la réalité ; rendu d'ingénierie, pas de jeu vidéo. » |
| **art-16** | D67 | **Strategic View — vue stratégique** | « Carte territoriale type grand strategy alimentée par des données réelles : infrastructures, ressources, économie, risques, influence ; icônes sobres, curseur temporel projetant 2030-2050. » |
| **art-17** | D58, D59, D82 | **Atelier 3D / CAD** | « Atelier de conception : modèle paramétrique au centre, mesures et contraintes visibles, IFC/BIM, préparation de fabrication ; fond neutre sombre, outillage technique discret. » |
| **art-18** | D44, D18 | **Sources & preuves** | « Mur des preuves : chaque affirmation reliée à une source datée avec niveau de confiance et citation ; vue tableau + vue graphe ; rigueur documentaire, aucune affirmation orpheline. » |
| **art-19** | D01, D27, D02 | **System Map — vue “god mode”** | « Schéma d'architecture complet : modules, agents, données, événements, APIs, frontières de permissions ; diagramme technique net, flèches lisibles, légende des contrats. » |
| **art-20** | D24, D75, D93 | **OSS Archaeology — bibliothèque technologique** | « Mur de projets open source comparés : étoiles, activité, licence, architecture, benchmarks ; chaque brique a une fiche santé et un plan de remplacement. » |

---

## 7. Les six écrans de type 03 (UI fonctionnelle)

| # | Écran | Contenu attendu |
|---|---|---|
| 1 | **Accueil / portail** | 8 portes, recherche, état du système, derniers événements — c'est le `shell/index.html` actuel |
| 2 | **Module BTP** | onglets, maquette, planning, coûts, sécurité, documents, conformité |
| 3 | **Carte + timeline + dossier** | la synchronisation D86 : une sélection met tout à jour |
| 4 | **Espace agents** | file de tâches, agents, permissions, journaux, vérification |
| 5 | **Fiche entité 360°** | identité, relations, sources, documents, carte, frise |
| 6 | **Système & modules** | installation, ressources (ECO/STANDARD/PERFORMANCE), mises à jour, diagnostics, licences |

## 8. Les quatre planches de type 04 (architecture)

| # | Planche | Ce qu'elle doit montrer |
|---|---|---|
| 1 | **Vue d'ensemble** | les 10 briques transversales et les capacités branchées dessus |
| 2 | **Coupe « données »** | du fichier brut → entité → événement → graphe → fiche, avec la provenance |
| 3 | **Coupe « agents »** | requête → orchestrateur → outils → vérification → réponse sourcée |
| 4 | **Coupe « ressources »** | ce qui tourne en permanence / à la demande / jamais, par profil ECO/STANDARD/PERFORMANCE |

---

## 9. Comment juger une image produite (et la refuser)

- **Refusée** si l'on ne peut pas dire *quoi* est sélectionné et *pourquoi* (hiérarchie absente).
- **Refusée** si les données affichées sont des faux indicateurs absurdes (règle UX-09 : jamais de fausse précision).
- **Refusée** si l'accent cyan est partout : il doit rester rare pour rester signifiant.
- **Refusée** si elle ne pourrait pas être implémentée en HTML/CSS/SVG avec un canvas WebGL raisonnable.
- **Acceptée** si un opérateur comprend en trois secondes : *où je suis, ce qui a changé, ce qu'on me demande*.
