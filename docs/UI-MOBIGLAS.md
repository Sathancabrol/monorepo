# 🪟 UI « MOBIGLAS » — le système de présentation du Life Hub (inspiré SF)

> **Date** : 2026-10-08 · **Commande** : « un système de présentation pour visualiser tout ce qu'on veut, en raccourcis comme un téléphone mais clean, comme la mobiGlas de Star Citizen ; idem pour le HUD et la gestion des options à l'écran. Regarder les jeux et films SF pour inspiration. »
> **Livrable** : le cahier des charges de la couche L4 (`SYSTEME-COMBINE-IA.md`) + l'habillage du dashboard PULSE (`LIFE-HUB.md`) — pensé dès maintenant pour finir sur des lunettes IA (`LUNETTES-IA-ETUDE.md`).

---

## 1. 🎭 Le genre « gestion/création d'IA » (la famille SillyTavern)

État de l'art 2026 des harness de personnages/agents ([comparatifs](https://www.promptquorum.com/power-local-llm/sillytavern-vs-agnai-vs-risuai-roleplay)) :

| Harness | ★ | Ce qu'il apporte au genre | Licence |
|---|---|---|---|
| **[SillyTavern](https://github.com/SillyTavern/SillyTavern)** | 34 211 | Le plus profond : cartes v1/v2/v3, **personas multiples**, **lorebooks/world info** (scan récursif), group chats, écosystème d'extensions massif | AGPL ⚠️ service seulement |
| **[Agnai](https://agnai.chat/)** | — | Léger, tourne sur petites machines ; **mode serveur multi-utilisateurs** (le différenciateur) | open source |
| **[RisuAI](https://risuai.net/)** | — | Présentation visual-novel (sprites, embranchements), le plus simple, mobile-first | open source |
| **[Backyard AI](https://backyard.ai/)** | — | Turnkey : les modèles tournent dedans, zéro config | fermé |

**Les 2 standards de fait à adopter (sans copier de code AGPL)** :
1. **Le format de carte Tavern v2** pour nos `USER/PERSONAS/*.md` — des milliers de cartes existent déjà, et ça permet de tester nos personas dans SillyTavern avant même d'avoir notre UI.
2. **L'endpoint OpenAI-compatible** comme seule prise : tous ces frontends se branchent sur n'importe quel backend Ollama/vLLM/API. Notre routeur L1 devient donc utilisable par SillyTavern/RisuAI en l'état — interop gratuite.

## 2. 🎬 La bibliothèque SF — ce qu'on vole à chaque référence

| Référence | Le principe à voler | La leçon inverse (l'erreur à ne pas faire) |
|---|---|---|
| **Star Citizen — mobiGlas** ([design notes officielles RSI](https://robertsspaceindustries.com/en/comm-link/engineering/14466-Design-Notes-MobiGlas)) | **Remplacer TOUS les menus par un seul appareil perso** : home screen à **widgets customisables** + apps dédiées, tout repose sur une **grille**, le téléphone compagnon EST la mobiGlas (mêmes fonctions PC↔mobile) | Les UI de film « ne sont pas faites pour un utilisateur normal » (dixit CIG) → la beauté SF doit passer l'épreuve de l'usage |
| **Dead Space** ([analyses](https://www.gamedeveloper.com/design/game-ui-discoveries-what-players-want)) | **UI diégétique** : l'info vit sur l'objet (santé sur la colonne, ammo sur l'arme) → zéro écran superposé, immersion totale | Leur carte holographique 3D a **échoué** → ils ont ajouté un « locator » projeté au sol. Morale : la fonction bat toujours le style |
| **Iron Man — JARVIS** | **L'interface est un personnage** : contexte ambiant, voix, elle anticipe. Le HUD ne s'affiche que quand il sert | Trop d'hologrammes tue l'hologramme : Stark a aussi un atelier « établi » classique |
| **Minority Report** | Gestes + panneaux transparents : l'idée de **manipuler l'information physiquement** (drag & drop spatial) | Les gestes fatiguent — le film a inspiré les écrans tactiles, pas les interfaces gestuelles réelles |
| **Her** | [Wired : *Her* influencera l'UI plus que Minority Report](https://www.provideocoalition.com/user-interfaces-in-the-movies-and-beyond/) → **voix d'abord, écran minimal**, chaleur, personnalité de l'OS | — |
| **Fallout — Pip-Boy** | Tous les menus dans **un seul appareil au poignet** ; l'app compagnon réelle synchronise jeu↔téléphone (preuve que poignet↔téléphone marche) | Le style rétro ne doit pas coûter de la lisibilité |
| **Mass Effect — omni-tool** | **Un seul outil universel** : scanner, comms, fabrication, tout part du même objet | — |
| **Cyberpunk 2077** ([critique UX](https://interfaceingame.com/articles/cyberpunk-2077-ux-ui-critique/)) | Leur carte/boussole diégétiques réussies | **L'overload de marqueurs = l'échec documenté** : icônes partout = plus rien ne se voit. Chaque raccourci doit *mériter* sa place |
| **Star Trek — LCARS** | Panneaux **codés par couleur = zones fonctionnelles** lisibles en un coup d'œil ; frameworks CSS réels existent : [joernweissenborn/lcars](https://github.com/joernweissenborn/lcars) (370★ MIT), louh/lcars (GPL) | LCARS est un mur de contrôle de vaisseau — trop dense pour la vie quotidienne |
| **Blade Runner 2049** | Profondeur tactile, rétro-futurisme sobre | — |
| **Dashboards « JARVIS » open source existants** | [mpolden/jarvis2](https://github.com/mpolden/jarvis2) (MIT, Flask), jarvis-hermes-dashboard (MIT, voix + mission control d'agents) | Ce sont des démos 0★-5k★ : des idées d'ambiance, pas des fondations |

## 3. 📐 Le design system retenu — « MobiGlas » en 3 surfaces

### Principes globaux (synthèse SF)
1. **Règle des 2 secondes** : chaque écran doit répondre à « quoi de neuf ? / qu'est-ce que je peux faire ? » en 2 s (mobiGlas : « glance at your wrist, not scroll through menus »).
2. **Diégétique** : l'info vit sur ce qu'elle concerne (le budget sur la carte budget, l'état du serveur sur sa tuile) — pas de panneau flottant générique (Dead Space).
3. **Chaque raccourci mérite sa place** : home = 8-12 tuiles max, le reste se cherche (anti-Cyberpunk).
4. **Le mouvement est du sens** : une animation = un message (arrivée, urgence, fin), jamais de la déco (JARVIS/MR).
5. **L'interface est un personnage** : la voix/persona active (couche L3) est visible partout, discrètement (Her).
6. **Un accent, un fond** : sombre, une seule couleur d'accent par contexte (LCARS modernisé), pas d'arc-en-ciel.
7. **Grille partout** : tout l'écran repose sur la même grille (design notes mobiGlas).

### Surface A — LE POIGNET / HOME (« mobiGlas »)
PWA téléphone + page d'accueil desktop. Une grille de **tuiles-widgets customisables**, chacune = un module du monorepo, chacune diégétique (chiffre clé + tendance + 1 action) :

| Tuile | Donnée affichée | Action rapide |
|---|---|---|
| 📰 Brief (Hugo-style) | 3 titres du jour | ouvrir le brief complet |
| ✉️ Mail | inbox restant, alertes filtres | « tout archiver » |
| 💶 Budget | solde + alerte enveloppe | saisie langage naturel (« courses 45 ») |
| 📅 Agenda | prochain événement + trajet | créer/déplacer |
| 🤖 IA | persona active, agents en cours, coût du jour | changer de persona / parler |
| 🎯 Tracker | prédictions en approche d'échéance (PROSPECTIVE-TRACKER) | marquer résolue |
| 🏠 Serveur | état mini-PC, disques, Ollama | redémarrer |
| 🌡️ Climat/énergie | météo Sète + prix énergie | — |
| 🔍 Recherche | UNE barre, cherche dans USER/ + docs/ + mail | aller au résultat |

### Surface B — LE HUD (couche ambiante, par-dessus la vie)
Le HUD n'est **pas** un dashboard de plus : c'est la couche « ce qui demande ton attention maintenant », en 3 niveaux :
- **N1 ambient** : lisible sans interaction — barre fine : prochaine échéance, serveur OK/⚠, persona active. (C'est exactement ce qui finira sur les **lunettes IA** : 1-3 lignes, jamais de menu.)
- **N2 notification** : cartes empilées, triées par le routeur d'importance (pas de flood — anti-Cyberpunk), chacune avec 2 actions max.
- **N3 briefing** : le matin = le « Today » d'Amethyst version mobiGlas : agenda, dettes, prédictions du tracker, signal Shenzhen en cours.
- Mode « **lunettes** » : le même N1 rendu en texte 3 lignes pour micro-display (Frame/DIY ESP32 de `LUNETTES-IA-ETUDE.md`) — le HUD est conçu dès le départ pour cette cible.

### Surface C — LES OPTIONS (gestion à l'écran, façon LCARS)
Une vue dédiée, **pas** un menu éparpillé : panneaux codés par couleur = zones (LCARS), chaque zone = un fichier/une décision du monorepo :
- **IA & modèles** (orange) : routeur L1 — fournisseur actif, fallbacks, budget de clés, modèle local Ollama, persona par défaut.
- **Vie privée** (rouge) : ce qui reste local vs cloud, par module — l'interrupteur le plus important du système (leçon GobboNet : « entirely local, entirely private » comme argument nº1).
- **Modules** (bleu) : activer/désactiver tuiles et hooks (mail-organizer, tracker, n8n…).
- **Apparence** (violet) : thème, accent, densité — dont un thème « LCARS » et un thème « mobiGlas » en clin d'œil.

## 4. 🛠️ Implémentation (ce qu'on construit, ce qu'on emprunte)

| Élément | Choix |
|---|---|
| Écrans | PWA unique servie par `app/` (FastAPI) — même codebase téléphone/desktop, comme la mobiGlas « companion app = la mobiGlas » |
| Grille/tuiles | CSS grid maison + pattern widget (PULSE en a déjà) |
| Ambiance SF | emprunts `lcars` CSS (MIT) pour la vue options ; sobre : 1 accent, pas d'holo-kitsch |
| HUD N1 lunettes | rendu texte 3 lignes → API `/api/life/hud.txt` (consommable par Frame/ESP32 plus tard) |
| Personas à l'écran | cartes Tavern v2 dans `USER/PERSONAS/` (interop SillyTavern testable aujourd'hui) |
| À NE PAS faire | installer un dashboard SF tout fait (jarvis2 & co = démos), refaire SillyTavern, surcharger de tuiles |

**Ordre** : ① home 9 tuiles + recherche → ② vue options LCARS → ③ HUD N1/N2 → ④ thème lunettes. Chaque étape reste utilisable seule.

---

## 📚 Sources
[RSI — Design Notes mobiGlas](https://robertsspaceindustries.com/en/comm-link/engineering/14466-Design-Notes-MobiGlas) · [HUDS+GUIS — Star Citizen UI revisited](https://www.hudsandguis.com/home/star-citizen-revisited-part-2) · [PC Gamer — mobiGlas widgets](https://www.pcgamer.com/star-citizen-video-show-off-smartwatch-style-ui-called-mobiglas/) · [Gamasutra — Game UI Discoveries (Dead Space)](https://www.gamedeveloper.com/design/game-ui-discoveries-what-players-want) · [In/β — Dead Space UI lessons](https://medium.com/inbeta/dead-space-ui-design-lessons-for-vr-39aa9e976ca8) · [punchev — diegetic vs non-diegetic](https://punchev.com/blog/diegetic-vs-non-diegetic-game-ui) · [Interface in Game — Cyberpunk 2077 UX critique](https://interfaceingame.com/articles/cyberpunk-2077-ux-ui-critique/) · [TV Tropes — Diegetic Interface (Pip-Boy)](https://tvtropes.org/pmwiki/pmwiki.php/Main/DiegeticInterface) · [ProVideo Coalition — UI in the movies (Her, Minority Report)](https://www.provideocoalition.com/user-interfaces-in-the-movies-and-beyond/) · [liistudio — sci-fi UI lessons](https://liistudio.com/sci-fi-ui-design-inspired-by-films/) · [promptquorum — SillyTavern vs Agnai vs RisuAI](https://www.promptquorum.com/power-local-llm/sillytavern-vs-agnai-vs-risuai-roleplay) · GitHub : lcars (MIT 370★), jarvis2 (MIT), SillyTavern (AGPL), RisuAI, Agnai
