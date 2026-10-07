# UI Carré d'As — principes, inspirations, structure

**Statut :** `PROPOSED` — proposition de conception, à discuter.
**Exigence utilisateur :** *interface simple et affordante, point d'accès aux fonctionnalités des modules.*
**Sources :** tes branches (dont l'audit UI et les principes de charge mentale de Watchtower) + recherche en ligne du 2026-10-07 (sources citées).

---

## 1. Les cinq règles non négociables

### R1 — Un point d'accès, quatre portes
L'accueil de Carré d'As ne présente pas 12 catégories ni 100 modules : il présente **quatre grandes portes** et une barre de recherche.

```
                    ┌───────────────────────────────────────┐
                    │        ⌕  Que voulez-vous faire ?      │   ← Ctrl+K partout
                    └───────────────────────────────────────┘
      ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
      │  🏗 PROJETS  │  │  🗺 CARTE    │  │  📄 DOCUMENTS│  │  ⬢ AGENTS    │
      │  chantiers,  │  │  territoire, │  │  DCE, plans, │  │  recherche,  │
      │  étude de    │  │  réseaux,    │  │  rapports,   │  │  rédaction,  │
      │  prix, suivi │  │  phasage     │  │  index       │  │  analyse     │
      └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
      ┌────────────────────────────────────────────────────────────────────┐
      │  Reprendre :  DQE Barbazan · CR n°7 · Plan phase 3   |  Activité  │
      └────────────────────────────────────────────────────────────────────┘
```

Les modules **enrichissent** cet accueil (cartes, résumés, alertes) sans jamais le remplacer. Un module désactivé fait disparaître sa porte, pas la cohérence.

### R2 — Rien n'est perdu
> Règle héritée de `AUDIT-UI.md` (branche Watchtower) : *« Aucune fonction ne peut plus être "perdue" silencieusement : si elle est injoignable, elle le dit. »*

Conséquences :
- toute fonction déclarée par un module est atteignable depuis le Ctrl+K **et** depuis la navigation ;
- si un module est désactivé ou en échec, l'entrée reste visible avec un état explicite (« module désactivé », « n'a pas démarré — voir Diagnostic ») ;
- aucun menu imbriqué de plus de 2 niveaux.

### R3 — Chaque action répond
Aucun bouton muet. Toute action produit un retour dans **300 ms** : soit le résultat, soit un état de chargement avec progression, soit un refus explicite et actionnable.

### R4 — La vérité est visible
> Modèle issu du hub INTEL (branche Watchtower) : *« Aucun fait n'est affiché sans dire ce qu'il vaut. »*

Chaque donnée affichée porte sa provenance et son niveau de certitude :

| Marque | Sens |
|---|---|
| ✅ **engagé** | contractualisé, mesuré, officiel (avec source) |
| 📅 **annoncé** | déclaré par un acteur, non contractualisé |
| 🔮 **tendance** | projection, inférence (préfixe `~` dans le texte) |
| ⚠️ **incertain** | donnée manquante, contradictoire ou non vérifiée |

Garde-fou à coder (déjà conçu dans la branche) : **un fait sans source ne peut pas être marqué « engagé »** — la règle est appliquée par le logiciel, pas par la discipline.

### R5 — Réduire la charge extrinsèque, jamais la complexité métier
> Base solide, sourcée dans `CHARGE-MENTALE.md` : théorie de la charge cognitive (Sweller) — *la seule charge qu'une interface peut réduire est l'extrinsèque*.

Traduction : on simplifie la **présentation** (nombre d'éléments, hiérarchie, vocabulaire), jamais la rigueur du fond. Pour mesurer, la variante **RTLX** (moyenne simple des 6 dimensions NASA-TLX, sans les 15 comparaisons par paires) est utilisable en test utilisateur léger.

---

## 2. Inspirations issues de tes branches (le meilleur est déjà là)

| Inspiration | Où | Ce qu'on en garde | Ce qu'on adapte |
|---|---|---|---|
| **Barre unique de fonctions** (24 fonctions, 4 catégories : Vues, Données, Navigation, Modes) | `docs/AUDIT-UI.md` + `src/barreFonctions.js` | le principe : **une seule barre**, tout est visible, catégories explicites, cases translucides, poignée pour replier | réduire à ~8 fonctions principales + « plus » (24 est trop pour un non-initié) |
| **Le volant** (contrôle radial : bascules d'affichage, méduses, anneau céleste) | `docs/VOLANT.md` | le contrôle **radial contextuel** comme second mode d'accès, mémorisable par la position | réservé aux vues (carte, 3D), pas à la navigation générale |
| **Bascule 2D ↔ 3D franche** | `docs/CARTE-2D.md` | **un seul moteur actif** ; état de caméra transféré ; pas d'affichage simultané | mesure citée dans le doc : Cesium **21 357 ms** de *total blocking time* contre **3 ms** pour MapLibre + deck.gl (étude FOSS4G 2025, arXiv 2602.23660 — à re-vérifier) → **2D par défaut**, 3D à la demande |
| **Planchers de lisibilité** (`src/lisibilite.js`) | `AUDIT-UI.md` | **des planchers, pas des tailles fixes** : panneaux ≥ 300 px, boutons fermer/modifier **28×28 px**, barres de titre ≥ 34 px | à intégrer au design system, pas en correctif transversal |
| **Repli sans clé = Plan IGN** | `VOLANT.md` | une application sans compte doit être **belle et lisible** dès le premier lancement (rues nommées, bâti, limites) | devient la règle par défaut de Carré d'As |
| **Grille de certitude** ✅📅🔮⚠️ | `docs/INTEL-TERRITOIRE.md` | **le langage de vérité** de toute l'application | étendu à toutes les données (documents, prix, planning, agents) |
| **« Chaque étape doit payer deux fois »** | `docs/ARCHITECTURE-MODULE.md` | un chantier technique doit servir **l'app autonome maintenant** et la fusion ensuite | règle d'arbitrage pour tous les chantiers V1 |
| **Le panneau FIL / niveaux INTEL** | branche `01a072e1` | filtrage et exploration progressive des données | généralisé en « filtres » transversaux |
| **Charge mentale : ne pas ajouter de capteurs inutiles** | `CHARGE-MENTALE.md` | la mesure (rPPG, émotions) n'est **pas** un objectif de la V1 | si mesure un jour : RTLX + consentement explicite |

## 3. Inspirations extérieures (vérifiées le 2026-10-07)

| Référence | Ce que c'est | Ce qu'on en prend |
|---|---|---|
| **PowerToys 0.98 — Command Palette Dock** (2026) | Microsoft a transformé la palette de commandes en **dock persistant** : positionnable sur n'importe quel bord, extensions épinglables, mêmes extensions que la palette, personnalisation d'apparence | le modèle exact de la V1 : **la palette (Ctrl+K) et le dock sont les deux faces d'une même architecture d'extensions**. Un module qui publie une commande peut aussi publier une tuile de dock |
| **Linear** | onboarding par étapes, palette de commandes, clavier d'abord, densité maîtrisée | le soin de l'**onboarding** et la sensation de vitesse |
| **Obsidian** | coffre local, plugins communautaires, palette, liens profonds | **le modèle de coffre** (dossier de données local) et la découverte de modules par un panneau « extensions » |
| **Raycast** | lanceur : actions contextuelles, extensions, historique | le Ctrl+K de Carré d'As : actions, pas seulement recherche |
| **Milanote / Craft** | tableaux, cartes, blocs modulaires, typographie | la **carte-objet** comme représentation standard d'un élément (chantier, document, lieu) |
| **Dropbox Dash** | recherche universelle + palette | la recherche qui trouve **partout** (documents, entités, événements, modules) |
| **Blender / QGIS** | espaces de travail, panneaux déplaçables, modes | la **notion d'espace de travail** (« Étude », « Chantier », « Carte »), mais sans en imposer la complexité |
| **PowerToys Command Palette (dock)** · [windowsforum](https://windowsforum.com/threads/powertoys-0-98-command-palette-dock-a-modular-second-taskbar-for-windows.407336/) · [xda](https://www.xda-developers.com/microsoft-powertoys-dock-keeps-my-app-workflow-one-keystroke-away/) · [grauberg](https://grauberg.co/resources/great-ui-websites) | | |

> ⚠️ **Prudence sur les sources d'inspiration** : la plupart des articles « UI inspiration 2026 » sont des contenus marketing sans méthode. Les deux seules sources réellement structurantes ici sont **le modèle d'extensions du dock PowerToys** (documenté par Microsoft et la presse technique) et **tes propres documents d'audit UI**. Le reste sert d'illustration, pas de justification.

## 4. Structure du shell

```
┌────────────────────────────────────────────────────────────────────────────┐
│  ⬢ CARRÉ D'AS      [ Projets ▾ ]   ⌕ Rechercher ou exécuter (Ctrl+K)    🔔 ⚙ │  ← barre haute
├──────────┬─────────────────────────────────────────────────────────────────┤
│          │                                                                 │
│  RAIL    │                        ZONE DE TRAVAIL                          │
│  (icônes │    (une vue à la fois : carte, tableau, document, 3D, graphe)   │
│   + noms)│                                                                 │
│          │  ┌──────────────────────────┐  ┌────────────────────────┐      │
│ ○ Accueil│  │  PANNEAU CONTEXTUEL      │  │  PANNEAU CONTEXTUEL    │      │
│ ○ Projets│  │  (détails, filtres,      │  │  (activité, agents,    │      │
│ ○ Carte  │  │   propriétés)            │  │   provenance)          │      │
│ ○ Docs   │  └──────────────────────────┘  └────────────────────────┘      │
│ ○ Agents │                                                                 │
│ ──────── │                                                                 │
│ ○ Système│                                                                 │
├──────────┴─────────────────────────────────────────────────────────────────┤
│  DOCK : [Carte 2D] [Bâti 3D] [Calques] [Prix] [Planning] [Qualité] [⏺ Journal] │  ← dock
└────────────────────────────────────────────────────────────────────────────┘
```

| Élément | Rôle | Règle |
|---|---|---|
| **Barre haute** | identité, projet courant, recherche/palette, notifications, paramètres | toujours visible ; jamais utilisée pour des commandes de module |
| **Rail** | navigation principale | ≤ 8 entrées ; libellés visibles (pas d'icônes seules) |
| **Zone de travail** | la vue active | une seule vue à la fois (pas d'onglets imbriqués) ; plein écran possible |
| **Panneaux contextuels** | détails, filtres, provenance | redimensionnables, mémorisés, **repliables** ; jamais bloquants |
| **Dock** | actions rapides du contexte + tuiles d'extensions | alimenté par les modules ; même source que la palette |
| **Palette (Ctrl+K)** | toutes les commandes + recherche universelle | première classe, pas un gadget : c'est l'API utilisateur de l'application |

## 5. Les écrans de la V1

| Écran | Contenu | Inspiration |
|---|---|---|
| **Accueil** | 4 portes, « reprendre », activité récente, état du système, notifications | accueil Linear + cartes Milanote |
| **Projets / Chantier** | liste des chantiers, fiche chantier : documents, prix, planning, qualité, carte, journal | dashboard BTP existant (branche `01a08449`) |
| **Carte** | 2D par défaut (Plan IGN sans clé), couches, entités, bâti 3D à la demande, phasage | Watchtower + `CARTE-2D.md` |
| **Documents** | dépôt par glisser-déposer, index, lecteur, extraction, provenance page | Dropbox Dash (recherche) + Obsidian (coffre) |
| **Agents** | chat, plans visibles, coût, journal des actions, approbations | NEXUS·OS + transparence d'agent |
| **Système** | comptes (Google/OneDrive/local), dossier de données, sauvegardes, modules installés, diagnostic, licences | dossier « Extensions » d'Obsidian + panneau système |

**Écran vide = écran qui apprend.** Chaque zone vide explique la prochaine action utile (« Déposez un DQE ici », « Ajoutez un lieu », « Demandez une recherche ») et propose un exemple réel du corpus — jamais un écran blanc.

## 6. Règles d'affordance (concrètes, vérifiables)

| # | Règle | Vérification en revue |
|---|---|---|
| A1 | Libellés de boutons = **verbe + objet** (« Extraire les prix », pas « OK ») | aucune étiquette vide de sens |
| A2 | Une action destructrice est **distincte visuellement** (couleur, confirmation) et jamais à côté d'une action fréquente | 0 destruction sans confirmation |
| A3 | Tout élément cliquable a un **état survol / focus / actif / désactivé** visible | test clavier complet |
| A4 | Les zones cliquables font ≥ **32×32 px** (28×28 minimum, comme la règle Watchtower) | audit automatisé |
| A5 | Un état vide n'est **jamais un cul-de-sac** | chaque écran vide propose une action |
| A6 | Le chargement d'un travail long est **segmenté et annulable** | > 2 s ⇒ progression + annulation |
| A7 | Les erreurs disent **quoi faire**, pas seulement ce qui a échoué | message + action de reprise |
| A8 | La provenance est toujours accessible à **un clic** de la donnée | audit par échantillonnage |
| A9 | Le clavier atteint **toutes** les fonctions (Tab, raccourcis, palette) | test : souris débranchée |
| A10 | Aucun élément de plus de 2 niveaux de profondeur (menu, panneau, accordéon) | revue de structure |

## 7. Design system (direction)

| Élément | Direction | Justification |
|---|---|---|
| **Thème** | clair par défaut, sombre disponible ; contrastes AA mini | usage terrain (chantier, plein soleil) + accessibilité |
| **Typographie** | une famille lisible avec chiffres tabulaires (données, prix, métrés) | lisibilité des tableaux métier |
| **Densité** | deux modes : « confort » (défaut) et « dense » (tableaux, cartes de données) | besoins contradictoires : novice vs conducteur de travaux |
| **Couleurs** | 4 couleurs de certitude (✅📅🔮⚠️) + 1 couleur d'accent + états sémantiques | langage visuel unique dans toute l'app |
| **Cartes** | composant standard : titre, 3 indicateurs, action principale, provenance | cohérence de l'accueil aux modules |
| **Icônes** | un seul jeu, avec libellé adjacent systématique | évite l'ambiguïté pictographique |
| **Mouvement** | transitions courtes (120-200 ms), respect de `prefers-reduced-motion` | accessibilité + sensation de vitesse |

## 8. Accessibilité (obligation ou pas, c'est la bonne pratique)

- Cible **WCAG 2.2 niveau AA** ; méthode **RGAA 4.1** pour l'audit (RGAA 5 attendu fin 2026 → à réévaluer).
- Rappel juridique exact : **une association à but non lucratif est hors du champ du RGAA**, *sauf* si elle fournit des services essentiels au public, des services destinés aux personnes handicapées, ou si elle est majoritairement financée/créée/administrée par des personnes publiques — auquel cas elle est dans le champ de l'article 47. Si Carré d'As est utilisé **par** des collectivités, l'accessibilité devient une exigence de fait.
- Tests automatisés (axe-core) dans la Quality Gate + un parcours clavier de bout en bout dans les tests d'intégration.
- Les **cartes** bénéficient d'une exemption partielle dans le RGAA, à condition que les informations essentielles (localisation, itinéraire) soient fournies sous forme accessible — à prévoir dès la conception (liste textuelle des entités affichées).

## 9. Ce qu'il faut éviter (anti-patterns déjà rencontrés)

| Anti-pattern | Où il a fait mal | Règle |
|---|---|---|
| Fonctions accessibles seulement par un ancien bouton supprimé | Watchtower (`AUDIT-UI.md` §2) | R2 + test automatisé de présence des entrées |
| Bloc d'information centré « dans l'axe du regard » | Watchtower (pastilles) | jamais d'information critique au centre ; elle pousse le contenu |
| Deux moteurs de rendu simultanés | carte 2D/3D | un seul moteur actif |
| Tailles fixes qui cassent un panneau déjà correct | lisibilité | des planchers, pas des tailles |
| Modules qui se déclarent en global (`window.*`) | 57 modules Watchtower | contrat + registre |
| Clés API dans le client | constat C4 (R&D) | coffre OS + proxy local |
| Écran vide muet | partout | R3 + A5 |
| Icônes sans libellés | habitude fréquente | libellé adjacent systématique |

## 10. Ce qui doit être mesuré (V1)

| Indicateur | Seuil |
|---|---|
| Temps pour accomplir « créer un projet + déposer un document + le retrouver » | < 2 minutes |
| Temps d'ouverture de l'application (à froid) | < 3 s |
| Latence de la palette (Ctrl+K) | < 100 ms |
| Fonctions atteignables au clavier | 100 % |
| Écrans vides sans action proposée | 0 |
| Actions sans retour visible | 0 |
| Erreurs critiques d'accessibilité (axe-core) | 0 |
