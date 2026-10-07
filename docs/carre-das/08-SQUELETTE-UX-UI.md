# Le squelette d'interface — Carré d'As, portail des modules

**Statut :** `FAIT` (squelette fonctionnel, à habiller) · **Date :** 7 octobre 2026
**Ouvrir :** double-cliquer sur `shell/index.html` — ou `python3 -m http.server 8000 --directory shell`
**Fichiers :** `shell/` (code) · `shell/README.md` (mode d'emploi) · `docs/carre-das/07-INVENTAIRE-FONCTIONNALITES.md` (le contenu)

---

## 1. L'idée, telle que tu l'as formulée

> « Carré d'As doit être un **triomphe vers les fonctionnalités de chaque module** ; tout intégré en **HTML squelette UX/UI**, servant de **template** ; navigation **simple, qualitative, luxueuse, pure** ; **open source, modulable** ; avec un **guidage IA, voix et visuel** (style JARVIS). Et **il ne faut pas perdre de fonctionnalités.** »

Le squelette répond point par point :

| Ta demande | Ce qui est livré |
|---|---|
| Un portail vers **chaque** module | **8 portes** → **14 modules** → **104 fonctionnalités**, toutes navigables |
| HTML squelette qui sert de **template** | `shell/index.html` + `tokens.css` (design system) + `shell.css` + 4 modules JS, **zéro dépendance** |
| Navigation simple et **luxueuse** | Un seul rail, une palette `Ctrl+K`, une zone de travail, des emplacements réservés lisibles |
| **Open source, modulable** | Ajouter un module = une entrée dans `shell/tools/gen-registry.py` + un `#slot-<id>` |
| **Guidage IA, voix, visuel** | Assistant : orbe à 4 états, parole, écoute, guidage réel (« ouvre le BTP »), modèle local optionnel |
| **« un morceau dans un repo »** | Sons d'interface synthétisés hors ligne + pack **uisfx** (CC0/MIT, personnalité « scifi ») en option |
| **Ne perdre aucune fonctionnalité** | Registre exhaustif, **104/104 fonctionnalités adossées à une source réelle** (contrôle automatique) |

---

## 2. Le design system vient de **ton** prototype, pas d'internet

En explorant `raw`, j'ai retrouvé **`projects/proto-cognitorium/raw/noeud neurono.html`** (48 Ko, autonome, titré « COGNITORIUM — Prototype ») : c'est **la référence d'interface d'origine**, avec ses variables CSS, ses onglets, sa session N-back et — détail précieux — un bouton **« Vue liste accessible »**.

J'ai repris **exactement** sa palette et sa typographie, sans rien réinventer :

| Rôle | Valeur | Sens dans le projet |
|---|---|---|
| `--void` | `#050508` | le fond : ce qui n'est pas encore connu |
| `--bg-elev` / `--bg-panel` | `#0A0A12` / `#1A1A2E` | surfaces, panneaux |
| `--plasticity` | **`#00E5CC`** | ce qui se construit (accent principal) |
| `--transfer` | **`#9B59B6`** | ce qui circule d'un domaine à l'autre (arêtes-pont) |
| `--alert` | `#FF3366` | ce qui doit être vérifié |
| Textes | `#E8E8F0` / `#8A8AA8` / `#4A4A6A` | trois niveaux de lecture |
| Polices | **Inter** + **JetBrains Mono** | la mono sert au factuel : sources, valeurs, identifiants |

Ajouts du squelette (rien de contradictoire) : échelle de rythme, ombres, **densités** (confort/dense), **contraste élevé**, **mouvement réduit**, et la **grille de vérité** ✅ établi · 📅 planifié · 🔮 hypothèse · ⚠️ alerte.

---

## 3. La structure (et pourquoi elle est ainsi)

```
┌──────────────────────────────────────────────────────────────────────┐
│ 🃏 Carré d'As   Portail   ⌕ Chercher… Ctrl+K        🛡  ⚙  🔔       │  barre haute
├──────────┬───────────────────────────────────────────────────────────┤
│ Accueil  │  Titre de la vue + sous-titre                             │
│ Projets  │  Onglets du module (ses fonctionnalités)                  │  zone de travail
│ Documents│  ┌─────────────────────────────────────────────────────┐  │
│ Carte    │  │  EMPLACEMENT RÉSERVÉ DU MODULE (#slot-<id>)         │  │
│ Agents   │  │  contrat · identifiant · point de montage · statut  │  │
│ Explorer │  └─────────────────────────────────────────────────────┘  │
│ Assistant│                                                           │
│ Système  │                                                           │
├──────────┴───────────────────────────────────────────────────────────┤
│ 14 modules · 104 fonctionnalités · assistant prêt · local, hors ligne │  barre d'état
└──────────────────────────────────────────────────────────────────────┘
        🛡 Assistant (orbe + voix + guidage)      ⌘K palette de commandes
```

- **Le rail ne contient que des portes**, pas des fonctionnalités : l'accès reste simple (règle R1).
- **La palette `Ctrl+K`** cherche dans les 104 fonctionnalités et dans les modules, au clavier (règle « toute action en moins de 300 ms »).
- **La barre d'état dit toujours la vérité** : local, hors ligne, nombre de modules, état de l'assistant.
- **Chaque emplacement réservé affiche le contrat** : identifiant, point de montage, statut, palier, **et la source dans le dépôt**. Un module non branché n'est jamais déguisé en module qui marche.

---

## 4. Les 14 modules (et le décompte de leurs fonctionnalités)

| Porte | Modules | Fonctions |
|---|---|---|
| **Accueil** | Command Center | 7 |
| **Projets** | Projets & chantiers · BTP — conduite de travaux | 6 + 11 |
| **Documents** | Documents | 7 |
| **Carte** | Carte & territoire | 8 |
| **Agents** | Agents & automatisation · Langage & notes | 9 + 5 |
| **Explorer** | Cognition & profil · Graphe & arbre · Métiers & passerelles · Référentiels & fiches · Apprentissage | 8 + 9 + 6 + 7 + 4 |
| **Assistant** | Assistant JARVIS | 7 |
| **Système** | Système & modules | 10 |

**Statuts** : 62 disponibles · 24 à porter depuis les branches · 18 à construire.
Chaque fonctionnalité porte **son palier** (V1 / V1.5 / V2) et **sa source**.

**Contrôle automatique** (deux garde-fous, rejouables) :

```bash
python3 shell/tools/check-sources.py          # 104/104 fonctionnalités adossées à une source réelle
python3 shell/tools/gen-registry.py           # regénère data/modules.json + assets/registry.js
python3 scripts/verif-completude-repos.py     # rien ne manque dans le monorepo (dépôts + branches)
```

---

## 5. L'assistant : ce qu'il fait vraiment (et ce qu'il ne fait pas)

| Capacité | État | Détail |
|---|---|---|
| Ouvrir un module | ✅ | « ouvre le BTP », « va sur la carte », « montre moi les documents » |
| Chercher une fonctionnalité | ✅ | « cherche métrés », « où est la décroissance », « cherche 3D » |
| Expliquer | ✅ | « explique la synchronisation », « c'est quoi le contrat de module » |
| Faire le point | ✅ | « où en est le projet » → 14 modules, 104 fonctions, 62 / 24 / 18 |
| Se taire | ✅ | « silence » |
| Parler | ✅ | synthèse vocale du système, voix française si disponible, **désactivable** |
| Écouter | ✅ si Chrome/Edge | reconnaissance vocale du navigateur ; **ailleurs, l'écrit fonctionne toujours** |
| Voir | ✅ | orbe à 4 états (repos · écoute · réflexion · parole) + ondes animées |
| Utiliser un modèle local | ✅ optionnel | adresse Ollama dans **Système** ; **si rien ne répond, il le dit** et reste en mode règles |
| Inventer des fonctionnalités | ❌ jamais | il ne répond que sur le registre ; les phrases sont construites à partir des données réelles |

**Inscription dans l'écosystème** : la référence est **`adewaskar/jarvis`** (MIT, ★395) — assistant navigateur avec visage holographique, mot de réveil, *barge-in*, mode dégradé. Nous en reprenons **les principes** (mode sans clé, états explicites, micro optionnel), pas le code Three.js : notre orbe est en CSS pur, pour rester léger sur une GTX 1060.

---

## 6. Les sons : « un morceau dans un repo »

Deux couches, dans cet ordre :

1. **Par défaut, synthèse locale** (`shell/assets/sounds.js`, Web Audio) : `boot`, `open`, `close`, `tick`, `confirm`, `cancel`, `error`, `ping`, `sweep`. Aucun fichier, aucune licence, **fonctionne hors ligne**. Le `boot` s'entend à l'ouverture (léger balayage 220 → 660 Hz).
2. **Option, un vrai pack libre** : **uisfx** (`romainsimon/uisfx`) — **code MIT, audio CC0**, 936 sons, 78 gestes sémantiques, 12 personnalités, dont **« scifi »** : *« clean holographic pings and restrained digital shimmer »*. Alternative : **soundcn** (700+ sons CC0, installation par la CLI shadcn).

```bash
mkdir -p shell/assets/sfx/scifi
# y déposer open.mp3, close.mp3, tick.mp3, confirm.mp3, cancel.mp3, error.mp3, ping.mp3, sweep.mp3, boot.mp3
```
```js
CarreSounds.loadPack("scifi");   // mémorisé ; si les fichiers manquent, la synthèse reprend la main
```

Règle du projet respectée : **l'audio n'est jamais le seul canal** — tout son a un équivalent visuel, et tout est coupable en un clic.

---

## 7. Brancher un module (le contrat, en 3 gestes)

```html
<!-- 1. dans index.html, l'emplacement existe déjà -->
<section id="slot-btp" data-module="btp"></section>

<!-- 2. le module s'y monte, en respectant le contrat -->
<script type="module" src="modules/btp/index.js"></script>
```
```python
# 3. ses fonctionnalités se déclarent ICI (source de vérité), puis :
#    python3 shell/tools/gen-registry.py
{"n": "Métrés & quantités", "d": "Contrôle de cohérence, écarts, révision",
 "s": "dispo", "src": "projects/proto-cognitorium/raw/métré.xlsx", "p": "V1"}
```

Le rail, la palette, les filtres, l'assistant et la barre d'état se mettent à jour **tout seuls**.
Contrat complet : `docs/carre-das/01-CONTRAT-MODULE.md` (permissions « rien par défaut », activation à chaud ≤ 300 ms, défaillance isolée, événements, `owns`/`reads`).

---

## 8. Accessibilité (règle non négociable)

- Navigation **100 % clavier** (`Alt+1…8`, `Ctrl+K`, `/`, `Échap`), `:focus-visible` partout ;
- `aria-current`, `aria-pressed`, `role="tablist"`, `aria-live` sur les zones qui changent ;
- **densité** confort/dense, **contraste élevé**, **mouvement réduit** (respect de `prefers-reduced-motion`) ;
- le prototype d'origine prévoyait déjà une **« Vue liste accessible »** : c'est repris comme **règle** — tout graphe ou arbre aura son équivalent textuel (RGAA, et règle UX-10 du cahier des charges) ;
- **impression** propre (le mode présentation peut sortir en PDF, comme le deck de Frontignan).

---

## 9. Ce que la fouille de `raw` a rapporté (au passage)

| Trouvaille | Ce que c'est | Usage |
|---|---|---|
| **`noeud neurono.html`** (48 Ko) | **le prototype d'origine** : design system Void/Plasticity/Transfer, zoom sémantique à 5 niveaux, statut épistémique (Établi/Modèle/Spéculatif), session N-back, trajectoire avec incertitude, vue liste accessible | **le design system du squelette** (§2) |
| **`01a0389d-….patch`** (951 Ko, 73 fichiers) | un lot de travail **jamais appliqué** : `bias_cards.py` (239 l.), `concept_details.py` (495 l.), `experiment_templates.py` (77 l.), `lab_endpoints.py` (75 l.), `scientific_articles.py` (257 l.) | **137 Ko de code récupérés** → `projects/_incoming/ETAT-DE-LART-PSYCHOLOGIE/…/app/` |
| **`slide carte représentation.pptx`** (22,9 Mo) | **50 diapositives, 186 médias** : captations d'interface, avatars, produits | matière visuelle (non retenue comme maquette : ce sont des images décoratives) |
| **~15 fichiers HTML** dans les branches | interfaces Flask et prototypes (`app/templates/*.html`, atlas Frontignan, deck 18 slides, OSINT Workbench) | sources d'écrans réels, toutes conservées |

**Honnêteté sur ce qui est irrécupérable** : le patch cite **20 illustrations JPG** (`bias_*.jpg`, `diagram_*.jpg`, `exp_*.jpg`, `real_*.jpg`, `schema_*.jpg`) et un `cognitorium-complete.zip` — **leurs octets ne sont pas dans le patch** (diff sans `--binary`) et n'existent dans **aucune** branche des 9 dépôts. Ils sont donc **à régénérer**. Ce n'est pas une perte de fonctionnalité (le code des fiches existe), c'est une perte d'illustrations, et c'est dit.

---

## 10. Ce qui reste à faire

| # | Chose | Où |
|---|---|---|
| 1 | **Brancher le premier module réel** (le corpus BTP : 154 documents) dans `#slot-btp` | P1–P3 du plan |
| 2 | Choisir la forme définitive (les 3 maquettes `maquettes/` vs ce portail) et **figer** le design system | toi |
| 3 | Porter **NEXUS·OS** (22 agents, 147 tests) en module Agents | V1.5 |
| 4 | Persistance (Core), puis installeur Windows | P1 puis P4 |
| 5 | Charger le pack **uisfx « scifi »** si tu veux les vrais sons | 5 minutes |
