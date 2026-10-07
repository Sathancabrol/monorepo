# Interfaces — analyse des concept arts et 3 propositions

**Statut :** `PROPOSED` — à valider avant toute implémentation.
**Date :** 7 octobre 2026 · **Sources :** 9 concept arts trouvés dans le dépôt (`projects/COGNITORIUM/*.png`, `projects/proto-cognitorium/src/assets/images/cognitorium_ui_concept_*.jpg`, `projects/proto-cognitorium/raw/html ghierarchi.png`) + le **Cahier des charges de référence v1.0 du 24 août 2026** (`projects/proto-cognitorium/raw/Cognitorium_Cahier_des_charges_reference_v1.0.docx`) + les images Drive du dossier `1qY33R9SNVw4Wl-iSgAtPLR2TzI226CVT`.
**Maquettes cliquables :** `maquettes/v1-le-carre.html` · `maquettes/v2-l-atelier.html` · `maquettes/v3-l-arbre.html` (ouvrir `maquettes/index.html`).

---

## 1. Ce que disent tes concept arts (analyse, image par image)

| # | Image | Ce qu'elle montre | Ce qu'elle vaut |
|---|---|---|---|
| 1 | `cognitorium_ui_concept_…jpg` | Tableau de bord **en anglais** : 4 tuiles de jauges (« Interactive cognitive vitality » 77 %, « Memory decay » 60 %, « skill half-life » 75 %), graphe constellation au centre, suggestions ROME à droite, barre de commandes, onglets (Dashboard, Skill Map, Career Paths, Insights, Network) | **La maquette la plus proche d'un vrai produit** : grille de cartes, hiérarchie claire. À reprendre pour le tableau de bord |
| 2 | `generated-image.png` / `gen_0727_1855` | Écran d'accueil : cerveau-arbre lumineux au centre, rail gauche (Accueil, Cognition, Éducation, Formations, Métiers, Univers, Analyses, IA, Paramètres), carte « Explorer mon potentiel » | **Belle vitrine**, mais c'est une **image d'ambiance**, pas une interface : aucun élément ne dit ce qu'on peut faire réellement |
| 3 | `gen_0730_0123` | « **Ecosystem Hub** » : Cognitorium au centre, connecteurs (LinkedIn ✓, GitHub ✓, France Travail, ESCO/ROME, LMS, Google Drive ✗, Notion ✗, Universités, Open Badges, Entreprise RH), import/export, « confiance : élevé », explorateur d'API (12 actives / 4 inactives), assistant IA, journal d'audit | **La vue la plus utile et la plus sous-estimée** : c'est exactement le panneau « Comptes & sources » du point 7 de tes demandes. À garder tel quel comme écran |
| 4 | `gen_0801_2244` | « **Tri-View** » : 3 colonnes (Mon parcours/arbre de compétences · Comment je pense/profil + radar · Où puis-je aller/graphe) + frise basse Arbre → Profil → Réseau → Possibilités → Projets de vie | **Excellente pédagogie** : trois questions, trois vues, une frise. À reprendre comme **mode découverte** |
| 5 | `gen_0801_2245` | « **Cognitive Map** » : corps anatomique, biais cognitifs, Learning Loop, graphe personnel, patterns de décision, coach IA | **Trop chargé** pour un écran principal ; utile en « mode expert » |
| 6 | `gen_0801_2250` | Planche de **12 vues** (jumeau, arbre, graphe, compétences, avenir, décisions, apprentissage, réseau social, impact territorial, simulation de vie, coach, dashboard) | **C'est la meilleure carte de navigation jamais produite pour ce projet** — mais telle quelle, c'est un poster, pas un menu |
| 7 | `telechargement1` | Arbre de compétences + **axe de vie** (Naissance → Sagesse), panneau « Profil cognitif » (87/76/82/91/74 %), « Potentiel détecté », « Compétences manquantes », « Parcours recommandé » | **L'axe de vie est une idée forte** : c'est la timeline du projet. À reprendre |
| 8 | `gen_0730_0550` | « Vision 2050 : Atlas des Compétences Humaines » : globe lumineux, cartes d'intention, rail d'icônes, barre d'état « Base de données : 1,8 M nœuds · Connexion locale · v3.1.1 · FPS · Mode IA » | **La barre d'état est un bon modèle** (état local, volume, mode, performances). Le message est émotionnel, pas opérationnel |
| 9 | `raw/html ghierarchi.png` | Comparaison des **5 hiérarchies concurrentes** dans tes maquettes, et celle retenue par le proto : **Expérience → Tâche → Compétence → Cognition → Matching** | **Le document le plus précieux des 9** : il tranche le modèle. À intégrer au Core |

### ADN commun (ce qui revient dans presque toutes les images)

1. **Fond sombre spatial** (bleu nuit / cyan / violet), halo lumineux, sensation de profondeur.
2. **Rail vertical à gauche** avec icône **+ libellé** (jamais l'icône seule).
3. **Barre haute** : titre + recherche globale + état (Sync / Mode IA / Notifications / Profil).
4. **Barre d'état en bas** : volume de données, mode local, version, performances.
5. **Cartes flottantes en verre** (glassmorphism) portant chacune un concept.
6. **Un motif central fort** : arbre, cerveau, constellation, globe.
7. **Des jauges et radars** pour les indicateurs personnels.
8. **Deux niveaux de lecture** : novice (cartes) / expert (graphe, scores, décay).

### Divergences à trancher

| Sujet | Option A (images 1, 2, 5) | Option B (images 3, 7, 9) | Ce que je recommande |
|---|---|---|---|
| Densité | Vide, contemplatif | Dense, fonctionnel | **Deux densités** : confort (défaut) / dense (tableaux, chantier) |
| Objet central | L'humain (cerveau, corps) | Le travail (hub, hiérarchie, graphe) | **Le projet** — avec l'humain en filigrane |
| Navigation | Par vues (12 vues) | Par objets (nœuds, liens) | **Par portes** (4) puis par vues dans le contexte |
| Vocabulaire | « potentiel », « jumeau cognitif », « Vision 2050 » | « nœuds », « API actives », « journal d'audit » | **Traduire** : la poésie pour l'accueil, la précision dans les panneaux |
| Langue | mélange FR/EN | FR | **FR d'abord**, EN en option |

### Le risque n°1 de ces maquettes

Elles promettent **plus que ce qu'un logiciel peut tenir** : « 1,8 M nœuds », « jumeau cognitif numérique », « simulation de vie ». C'est un problème de confiance : le cahier des charges lui-même impose (UX-09) de **ne pas créer de fausse précision**. Les trois propositions ci-dessous retirent les promesses et gardent l'esthétique.

---

## 2. Les principes hérités du cahier des charges (à respecter dans les 3 versions)

| Réf. | Exigence | Application concrète |
|---|---|---|
| UX-01 | **Simplicité en surface → profondeur à la demande** | un premier écran compréhensible sans explication ; le reste accessible en 1 clic |
| UX-02 | Première utilisation guidée | écran d'entrée unique, 3 chemins (exemple / import / guidé) |
| UX-03 | Profil construit progressivement | ne jamais demander tout, jamais de formulaire-mur |
| UX-04 | Toute proposition IA est validable | boutons **Accepter / Modifier / Refuser** systématiques |
| UX-05 | Les preuves sont accessibles | pastille de provenance sur chaque donnée |
| UX-07 | Débutant et expert, densités différentes | bascule confort / dense |
| UX-08 | Les recommandations expliquent leur raisonnement | « pourquoi » toujours présent |
| UX-09 | Pas de fausse précision | jamais un score nu ; intervalle + statut + source |
| UX-10 | **Le graphe n'est pas l'unique porte d'entrée** | navigation par portes et recherche ; le graphe est une vue |
| §14 | Chaîne fonctionnelle : **Portail → Onboarding → Collecteurs → Distillation IA → Validation → Core → Référentiels → Matching → Représentations → Recommandations** | c'est l'ordre de construction (voir `05-REPONSES-AUX-QUESTIONS.md` §2) |

---

## 3. Les trois propositions

> Les trois partagent : fond sombre, rail à gauche, barre haute, barre d'état, palette Ctrl+K, panneau de provenance, marqueurs de certitude ✅ 📅 🔮 ⚠️, et l'indicateur « modules installés ». **Elles diffèrent par ce qui est au centre.**

### V1 — « LE CARRÉ » — la simplicité assumée

**Idée :** l'accueil **est** le produit. Quatre portes, une recherche, des reprises. Rien d'autre.

```
┌──────────────────────────────────────────────────────────────┐
│ ⬢ CARRÉ D'AS   [Projet ▾]   ⌕ Rechercher (Ctrl+K)      🔔 ⚙ │
├──────┬───────────────────────────────────────────────────────┤
│ rail │   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │
│      │   │ PROJETS │ │  CARTE  │ │DOCUMENTS│ │ AGENTS  │    │
│ ⌂ 🏗 🗺 │   │ 12      │ │         │ │ 154     │ │ 22      │    │
│ 📄 ⬢ ⚙ │   └─────────┘ └─────────┘ └─────────┘ └─────────┘    │
│      │   Reprendre · activité · à traiter · alertes          │
└──────┴───────────────────────────────────────────────────────┘
        Barre d'état : dossier local · 154 documents · hors ligne
```

- **Pour** : charge mentale minimale (R5) ; un débutant comprend en 5 secondes ; s'adapte à une mairie, une association, un artisan.
- **Contre** : peu impressionnant en démonstration ; les usages intensifs demandent plus de raccourcis (compensé par le Ctrl+K).
- **Pour qui** : l'utilisateur final non technique ; c'est la **porte d'entrée par défaut**.

### V2 — « L'ATELIER » — le poste de travail métier

**Idée :** le **projet** est le conteneur. À l'intérieur, tout est à portée : documents, prix, planning, carte, 3D, qualité, journal. Panneaux latéraux pour les détails et la provenance, dock en bas pour les outils, palette au clavier.

```
┌──────────────────────────────────────────────────────────────┐
│ ⬢ CHANTIER BARBAZAN — giratoire · phase 3      ⌕ Ctrl+K  🔔 ⚙│
├──────┬────────────────────────────────────────────────────────┤
│ rail │ Documents · Prix · Planning · Carte · 3D · Qualité · …│
│      ├──────────────────────────────┬─────────────────────────┤
│      │                              │  DÉTAILS                │
│      │        ZONE DE TRAVAIL       │  provenance ✅ page 12  │
│      │        (tableau / carte)     │  écart −4 200 €         │
│      │                              │  ──────────────         │
│      │                              │  ACTIVITÉ / AGENTS      │
├──────┴──────────────────────────────┴─────────────────────────┤
│ DOCK  [2D] [Bâti 3D] [Calques] [DQE/BPU] [Métrés] [⏺ Journal]  │
└──────────────────────────────────────────────────────────────┘
```

- **Pour** : productivité réelle ; c'est là que vit le module BTP ; réutilise la « barre unique de fonctions » validée par tes tests Watchtower ; le mode dense est naturel.
- **Contre** : demande d'apprendre 5 zones ; peut intimider un débutant (atténué par V1 comme accueil).
- **Pour qui** : le conducteur de travaux, l'usage quotidien, les 154 documents.

### V3 — « L'ARBRE » — la carte cognitive (fidèle à tes concept arts)

**Idée :** on navigue **dans une représentation** : l'arbre de compétences, le graphe de connaissances et l'axe de vie sont l'interface principale ; les objets (documents, chantiers) apparaissent en cartes contextuelles.

```
┌──────────────────────────────────────────────────────────────┐
│ ⬢ CARRÉ D'AS — Niveau : Personne ▾         ⌕ Ctrl+K      🔔 ⚙│
├──────┬──────────────────────────────────┬────────────────────┤
│ rail │         ARBRE / GRAPHE           │  FICHE (au clic)   │
│      │      ✦ arbre de compétences      │  Compétence        │
│      │     ╱   │   ╲   (zoom sémantique)│  provenance ✅      │
│      │  savoir expérience projets       │  preuves (3)       │
│      │    ▼ axe de vie : période active  │  à réactiver 🔮     │
├──────┴──────────────────────────────────┴────────────────────┤
│ ○ Fin  ○ Vue métier  ○ Timeline  ○ Tableau  ○ Graphe          │
└──────────────────────────────────────────────────────────────┘
```

- **Pour** : identité forte, mémorable, pédagogique ; correspond à ce que tes images donnent envie d'acheter ; excellent en démonstration et pour la formation.
- **Contre** : ⚠️ risque d'inverse de UX-10 (le graphe comme unique porte d'entrée) ; performance et accessibilité (canvas) ; CANVAS difficile pour les lecteurs d'écran → **exiger un mode liste équivalent**.
- **Pour qui** : la découverte, l'éducation, le récit, et… la démonstration à une association ou un financeur.

---

## 4. Comparaison directe

| Critère (pondération indicative) | V1 Le Carré | V2 L'Atelier | V3 L'Arbre |
|---|---|---|---|
| Compréhension immédiate (×3) | ★★★★★ | ★★★☆☆ | ★★★☆☆ |
| Efficacité en usage intensif (×3) | ★★☆☆☆ | ★★★★★ | ★★★☆☆ |
| Fidélité à tes concept arts (×2) | ★★☆☆☆ | ★★★☆☆ | ★★★★★ |
| Charge mentale réduite (×2) | ★★★★★ | ★★★☆☆ | ★★☆☆☆ |
| Accessibilité (RGAA/WCAG) (×2) | ★★★★★ | ★★★★☆ | ★★☆☆☆ |
| Performance sur GTX 1060 (×2) | ★★★★★ | ★★★★☆ | ★★★☆☆ |
| Effort de construction (×2) | ★★★★★ (le moins) | ★★★☆☆ | ★★☆☆☆ |
| Potentiel de démonstration (×1) | ★★★☆☆ | ★★★☆☆ | ★★★★★ |
| **Total pondéré** | **3,9 / 5** | **3,7 / 5** | **3,3 / 5** |

## 5. Ma recommandation

> **V1 comme accueil par défaut + V2 comme espace de travail**, et **V3 comme module d'exploration** (pas comme shell).

C'est-à-dire : on entre dans Carré d'As par **quatre portes** (V1). Dès qu'un projet est ouvert, l'interface devient **l'Atelier** (V2) — c'est là que vivent 154 documents, les prix, la carte et le chantier. L'**Arbre** (V3) reste accessible en un clic comme vue d'exploration et de démonstration, avec un mode liste équivalent pour l'accessibilité et pour les machines modestes.

Trois raisons :
1. le cahier des charges l'impose presque (UX-01 : simplicité en surface ; UX-07 : deux densités ; UX-10 : le graphe n'est pas l'unique porte) ;
2. c'est le seul scénario compatible avec la machine cible (globe/graphe = coût GPU ; 2D/tableaux = léger) ;
3. ça n'abandonne rien de tes images : l'esthétique (sombre, lumineuse, arbre/cerveau/constellation), le rail, la barre d'état, l'Ecosystem Hub, l'axe de vie — tout est réutilisé quelque part.

## 6. Ce que je retire de tes concept arts (et pourquoi)

| Retiré | Raison |
|---|---|
| « 1,8 M nœuds », « Vision 2050 », « jumeau cognitif » en page d'accueil | promesse non tenue = perte de confiance (UX-09) |
| Corps anatomique central | joli mais mystifiant : on n'analyse pas le corps ; risque de perception « diagnostic » (interdit §7.4 du cahier des charges) |
| Scores nus (87 %, 76 %, 82 %) | remplacer par **intervalle + statut + source** (« disponibilité estimée : forte · confirmée · 3 preuves ») |
| 12 vues au même niveau | elles deviennent : 4 portes → vues contextuelles → mode expert |
| Mélange FR/EN | FR par défaut, EN en option (i18n prévu dès le départ) |
| Icônes seules dans le rail | libellé toujours visible (règle d'affordance A1) |

## 7. Ce qu'il te reste à valider (3 questions)

1. **Accueil : V1, V2 ou V3 ?** (ma recommandation : V1 en accueil + V2 au travail + V3 en exploration)
2. **Densité par défaut** : confort (V1) ou dense (V2) ?
3. **Mode démonstration** : veux-tu un « mode présentation » plein écran (issu de V3) pour montrer le projet à une association, une mairie ou un financeur ?

Une fois ces 3 points tranchés, je fige la maquette retenue en **design system** (tokens, composants, règles d'affordance) et elle devient la référence des modules.
