# Module Chantier (BTP / TP) — spécification de la brique forte

**Statut :** `PROPOSED` — spécification fonctionnelle et technique, aucune implémentation.
**Exigence utilisateur :** *« le module BTP doit devenir une partie puissante : modélisation 3D, moteur desktop, carte, stats, mise à jour avec compte Google ou autre. »*
**Base existante :** branche `monorepo/arena/01a08449` — `projects/btp-conduite-travaux/` (154 documents, 7 rapports, 28 sous-détails de prix, matrice de traçabilité, dashboard) + Watchtower (carte, chantier, phasage 4D) + corpus réel à la racine du dépôt.

---

## 1. Ce qui existe déjà (et ne doit pas être refait)

| Actif | Contenu vérifié | Réutilisation |
|---|---|---|
| `documents_sources/` | **154 documents** classés en 7 familles : DCE et marchés publics, préparation et étude de prix, réglementation DICT/AIPR/sécurité, suivi d'exécution et comptes rendus, DOE et réception, management RH/formation, plans et cartographie — dans des dossiers par chantier (Barbazan, Saint-Nicolas-de-la-Grave, Pruniaux) | **le jeu de test officiel** du module et du pipeline documentaire |
| `rapports/` (7 rapports) | synthèse état de l'art + in-situ · marchés/DCE/cadre juridique · étude de prix et sous-détails · technique voirie-réseaux-terrassement · anti-endommagement DICT/AIPR · pilotage in-situ (CR, aléas, litiges) · réception/DOE/BIM/Lean · schéma directeur de la chaîne chantier | la **connaissance métier** encodée : c'est la base d'un assistant utile |
| `data/` | inventaire JSON avec **SHA-256** par document, version CSV pour export, synthèse chantiers et **barèmes des sous-détails de prix**, matrice de confrontation théorie/état de l'art/in-situ | socle de données + **déduplication et intégrité par empreinte** |
| `index.html` (dashboard) | comparateur dynamique, catalogue des **28 sous-détails de prix** avec simulateur déboursé sec/marge, explorateur des 154 documents, lecteur des 7 rapports | prototype de l'UI du module (à refaire avec le design system) |
| Watchtower (chantier) | phasage 4D, GPS des engins, sous-sol OSM, prospection BOAMP, fiche lieu, import KML/GeoJSON | la **couche carte** du module |

**Conséquence :** le module BTP de la V1 est un travail d'**industrialisation** (schéma, UI, flux), pas de création de contenu.

---

## 2. Les sept piliers du module

### Pilier 1 — Documents et DCE
- Dépôt par glisser-déposer (dossier complet ou fichier), **arborescence reconnue automatiquement** (les 7 familles existent déjà).
- Ingestion : PDF, XLS/XLSX, DOC/DOCX, images, plans scannés. Extraction : texte, tableaux chiffrés, métrés, références de prix, dates, acteurs.
- Indexation instantanée + recherche dans le contenu (« trouve tous les prix enrobés »).
- **Chaque chiffre extrait porte sa provenance** : document, page, zone. Un chiffre sans provenance n'est pas affiché comme un fait.
- Détection des doublons par empreinte (SHA-256 du corpus existant) et des versions successives d'un même document.

### Pilier 2 — Étude de prix, DQE, BPU, métrés
- Import DQE/BPU/DETAIL-ESTIMATIF, normalisation, rapprochement ligne à ligne.
- **Comparateur** : DQE ↔ BPU ↔ devis entreprise ↔ réalisé, avec écarts expliqués (quantité, prix unitaire, oubli, doublon).
- **28 sous-détails de prix** déjà modélisés : déboursé sec, frais, marge, simulateur de variantes.
- Métrés issus des plans (assistés), cohérence quantités ↔ plans ↔ terrain.
- Références externes : indices INSEE BT01, base de prix, révision de prix (à brancher, cf. dossier recherche D63).

### Pilier 3 — Suivi de chantier
- Planning et phasage (frise, dépendances, chemin critique simple), rattaché au phasage 4D de la carte.
- Comptes rendus de réunion : saisie assistée, **génération pré-remplie** depuis les documents et le journal (validation humaine obligatoire).
- Non-conformités et essais (fiches existantes dans le corpus : plaque, double-anneau, hydraulique) avec photos, mesures, décisions.
- Ordres de service, avenants, arrêtés de circulation, autorisations de voirie, **DICT/DT et AIPR** : suivi des obligations et des échéances.
- Journal de chantier : événements datés et géolocalisés (météo, aléas, livraisons, incidents) — c'est aussi la matière première de la timeline.
- Situations et facturation : suivi des avancements et des montants (v1.1).

### Pilier 4 — Carte
- **2D par défaut** (Plan IGN sans clé — règle adoptée pour toute l'application), couches OSM, cadastre, satellite.
- Couche chantier : emprise, installations, réseaux (existants/projetés), servitudes, DICT, signalisation, accès.
- Phasage temporel : chaque phase s'affiche sur la carte (le « 4D » de Watchtower).
- Entités géolocalisées (engins, dépôts, points de contrôle) sans dépendre d'un service payant.
- Import/export : GeoJSON, KML, DXF (lecture), export pour QGIS.

### Pilier 5 — 3D et modélisation (le sujet sensible)
> ⚠️ **Décision de principe : Carré d'As assemble, visualise, mesure et pilote. Il ne réécrit pas un modeleur.**
> Écrire un modeleur B-rep concurrent de FreeCAD/Revit est un projet de plusieurs années (principe P3 de la constitution : on ne réimplémente pas ce qui existe).

**Trois paliers, dans cet ordre :**

| Palier | V1 | Ce que ça donne | Brique technique |
|---|---|---|---|
| **1. Voir et mesurer** | ✅ V1 | ouvrir un modèle (IFC, glTF/GLB, OBJ, STEP simplifié), un nuage de points (LAS/LAZ/COPC) et une orthophoto ; mesurer, couper, annoter, comparer à un plan | visionneuse web : **web-ifc** / **xeokit** pour l'IFC, **three.js** pour glTF, **Potree** pour les nuages ; globe **Cesium** pour le contexte global (à la demande) |
| **2. Assembler et comparer** | ⏳ V1.5 | assembler maquette + terrain + plan, positionner, comparer deux états (avant/après, théorique/réalisé), détecter les écarts, exporter une vue | **CloudCompare** (GPL, piloté en local) pour les nuages, **IfcOpenShell** (LGPL) pour lire IFC et extraire les quantités, **PDAL** pour le traitement |
| **3. Modéliser et produire** | ⏳ V2+ | pièces paramétriques simples, implantation VRD, scan→maquette, orthophoto de chantier | **FreeCAD/BIM** ou **Blender** pilotés par l'app ; noyau paramétrique embarquable (**OCCT** via replicad) pour les pièces simples ; **OpenDroneMap** pour la photogrammétrie ; **Cloud2BIM** (pipeline open source scan→IFC, arXiv 2503.11498) à évaluer |

**Pilotage d'outils externes :** l'application détecte, lance et surveille les outils installés (FreeCAD, Blender, CloudCompare, ODM, QGIS) via une file de travaux locale avec progression, journal et reprise. C'est ce qui donne une « puissance desktop » immédiate sans développer un moteur.

**Contraintes machine (GTX 1060, 6 Go VRAM, 16 Go RAM) — à dire honnêtement :**
- visionneuses 3D web et nuages de points : **oui**, avec budget mémoire strict et chargement progressif (COPC/LOD) ;
- photogrammétrie (OpenDroneMap) : **possible mais lent** (heures, CPU et RAM) → traitement nocturne ou machine dédiée, jamais bloquant ;
- rendu photoréaliste temps réel, jumeau complet d'un quartier : **non** sur cette machine ;
- le mode 2D/3D doit rester **exclusif** (un seul moteur actif à la fois) — mesure de référence dans `docs/CARTE-2D.md`.

**Formats d'échange à supporter** (c'est ce qui évite l'enfermement) : IFC (BIM), DXF/DWG (plans, lecture), LandXML/GeoJSON (VRD), LAS/LAZ/COPC/E57 (nuages), GeoTIFF/COG (ortho), STEP/IGES (CAO, lecture), glTF (diffusion).

### Pilier 6 — Statistiques
- Tableaux de bord du chantier : avancement, délais, écarts de prix, qualité (NC/essais), sécurité (incidents, AIPR), météo.
- Comparaisons entre chantiers et entre variantes (déboursé sec, marge, durée).
- Analyse du corpus : quels postes coûtent, quels aléas reviennent, quels documents manquent.
- Visualisations : graphiques simples et lisibles (barres, courbes, écarts), tableaux exportables ; pas de « dataviz » décorative.
- Chaque indicateur affiche **sa méthode de calcul** et sa provenance (règle R4 de l'UI).

### Pilier 7 — Synchronisation et comptes
Objectif : *« mise à jour avec compte Google ou autre »*, sans jamais rendre le compte obligatoire.

| Fournisseur | Usage | Points techniques |
|---|---|---|
| **Aucun compte** (défaut) | dossier local + disque externe / NAS | toujours supporté ; c'est le mode de référence |
| **Google** | sauvegarde et continuité des données de l'app + partage de fichiers choisis | `drive.appdata` (dossier applicatif **masqué**, horodaté, non listable par l'utilisateur) pour l'état de l'app ; `drive.file` pour les **fichiers que l'utilisateur choisit** explicitement. Ces deux scopes sont **non sensibles**, ce qui évite un processus de vérification lourd ; jetons dans le **coffre Windows**, jamais dans le code ; `access_type=offline` pour le jeton de rafraîchissement (révocable par l'utilisateur, 6 mois d'inactivité) |
| **OneDrive / Microsoft** | même usage | Microsoft Graph, modèle équivalent, derrière la **même interface** |
| **WebDAV / Nextcloud / NAS** | même usage, auto-hébergé | le plus souverain ; à supporter en priorité pour les collectivités |
| **Dossier partagé d'équipe** | plusieurs postes sur un même projet | manifeste + verrous + empreintes (SHA-256 déjà présentes dans l'inventaire) ; conflits signalés, **jamais écrasés en silence** |

**Règles de synchronisation (non négociables) :**
1. Le **local est la vérité primaire** ; le cloud est une copie.
2. **Rien ne part sans action de l'utilisateur** (aucune télémétrie, aucun envoi implicite).
3. Un conflit est **présenté**, pas tranché en silence : « deux versions de ce DQE, voici les différences ».
4. Les documents sont **dédupliqués par empreinte** (pas de double envoi, pas de doublon).
5. La restauration complète doit être possible **sans l'application** (export lisible).
6. Les données personnelles (CV, noms, coordonnées présentes dans les marchés) sont **identifiées** et exclues par défaut de toute synchronisation non consentie.

---

## 3. Modèle de données du module (proposition)

Socle commun (cœur) : `project`, `document`, `place`, `organization`, `person`, `event`, `task`, `agent`, `user`.

Entités propres au module (`owns`) :

```
chantier        ── lot, phase, intervenant, marché, montant, délai
lot             ── poste, quantité, unité, prix_unitaire, sous_detail_prix
metre           ── ligne, quantité, unité, origine (plan|terrain|calcul), preuve
prix_unitaire   ── déboursé_sec, frais, marge, ressources, temps_unitaire
marche          ── type, montant, délai, pièces, cadre juridique (CCAP/CCTP/BPU)
non_conformite  ── gravité, description, photo, décision, statut, coût
essai           ── type (plaque, double-anneau, hydraulique…), valeur, seuil, conformité
reseau          ── nature (AEP, EU, EP, élec, télécom), statut (existant, projeté), géométrie
danger          ── DICT/DT, AIPR, servitude, emprise, échéance
```

Règles : chaque entité porte provenance, confiance, statut épistémique et licence ; les quantités et les prix portent **toujours** leur origine et leur unité ; les documents sont liés par empreinte.

---

## 4. Intégrations du module

| Vers | Ce que le module consomme / produit |
|---|---|
| **Documents** | consomme `document.indexed` ; produit `chantier.piece.identifiee` |
| **Carte** | publie les entités géographiques du chantier ; consomme les couches de fond |
| **Agents** | expose des outils (« extraire un DQE », « résumer un CR », « vérifier un écart ») via MCP ; reçoit des propositions à valider |
| **Temporal** | publie les événements de chantier pour la timeline/4D |
| **Recherche** | alimente l'index global ; interrogeable par entité, document, montant |
| **Cognition** (v1.1) | relie les compétences requises aux personnes et aux tâches |
| **Système** | sync, sauvegardes, licences, mises à jour du module |

---

## 5. Feuille de route du module

| Étape | Contenu | Critère de sortie |
|---|---|---|
| **B1** | Reprise du corpus dans le schéma canonique (154 documents, inventaire, SHA-256, 28 SDP) | l'inventaire existant est intégralement retrouvé dans le module |
| **B2** | Ingestion + index + recherche dans le contenu (texte et tableaux) | « trouve ce prix » répond en < 1 s sur le corpus, avec provenance |
| **B3** | Étude de prix : comparateur DQE ↔ BPU ↔ devis ↔ réalisé, simulateur SDP | un DQE réel produit un tableau d'écarts expliqué |
| **B4** | Suivi : planning, CR, NC, essais, DICT/AIPR, journal | un chantier suivi une semaine **sans revenir à Excel** |
| **B5** | Carte : emprise, réseaux, phasage, entités | le chantier s'affiche et se raconte sur la carte |
| **B6** | 3D palier 1 : visionneuses (IFC, glTF, nuages, ortho) + mesures | un plan et un nuage s'ouvrent, se mesurent, s'annoter |
| **B7** | Sync : Google + OneDrive + WebDAV/NAS + dossier partagé | deux postes se synchronisent **sans perte** (test de conflit documenté) |
| **B8** | Stats : tableaux de bord + export | 5 indicateurs fiables, méthode affichée |
| **B9+** | 3D paliers 2-3, scan→maquette, photogrammétrie, situations/facturation | décidé après usage réel de B1-B8 |

---

## 6. Risques propres au module

| Risque | Parade |
|---|---|
| **Promettre un modeleur** | message clair : on assemble et on pilote ; palier 3 seulement si besoin réel |
| **Responsabilité des calculs** | aucun calcul de sécurité sans avertissement et validation par un professionnel ; les notes de calcul restent hors périmètre V1 |
| **Licences des outils pilotés** (CloudCompare GPL, IfcOpenShell LGPL, ODM AGPL) | **pilotage** (processus séparé) et non liaison ; matrice de licences avant distribution |
| **Données personnelles dans les marchés** (noms, adresses, CV) | identification et exclusion des exports/sync non consentis ; politique de données |
| **Machine cible** | 2D par défaut, 3D à la demande, budgets mémoire mesurés, traitements lourds en tâche de fond |
| **Documents clients confidentiels** | chiffrement local optionnel, aucun envoi automatique, journal des accès |
| **Divergence avec l'usage réel** | boucle de retour hebdomadaire avec le conducteur de travaux (rituel D80 du dossier recherche) |

---

## 7. Question ouverte à trancher

> **Quel est le premier chantier réel que le module doit accompagner de bout en bout ?**
> Le corpus contient trois candidats : **Barbazan** (giratoire, phasage, plans, CR), **Pruniaux** (lotissement, DCE, préparation), **Saint-Nicolas-de-la-Grave**. C'est ce choix qui décidera de l'ordre exact de B2 → B5.

Sources externes vérifiées le 2026-10-07 : `ifcopenshell` (LGPL-3.0, actif), CloudCompare (GPL, référence des nuages de points), Potree (rendu web de nuages, utilisé notamment par des viewers commerciaux), Cloud2BIM (pipeline open source scan→IFC, arXiv 2503.11498, 2025), FreeCAD/BIM (open source, IFC natif), Google Drive `appDataFolder` + scopes `drive.appdata`/`drive.file` (non sensibles).
