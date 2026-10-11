# Synthèses de discussion — vision « Atlas Frontignan » (2026-10-11)

> Transcription verbatim des deux synthèses transmises le 11/10/2026 (aucune source externe
> citée par les deux synthétiseurs). Elles fondent la spécification Phase 0 de la console
> territoriale Atlas Frontignan : `../atlas-frontignan-2026.json` (schéma `atlas-frontignan-v1`).
>
> Les éléments factuels locaux (PCS 2025, SMBT, PAPI Thau 2026–2031, blocages cévenols) sont
> déjà capturés dans le dataset canonique `data/climat/frontignan-episodes-cevenols/` — ce sont
> ces datasets qui font foi, pas les mentions rapides ci-dessous.

---

## Document 1 — Synthèse « gpt-6-sol-search-max » (sans sources)

La recherche est partie d'un logiciel récent de prévention des inondations aperçu sur Instagram, possiblement lié à l'Asie ou disponible sur GitHub. Le produit exact n'a pas été identifié avec certitude. FastFlood et plusieurs projets de simulation ont été évoqués comme pistes à examiner, pas comme composants déjà retenus.

La discussion a ensuite précisé le véritable objectif : Atlas Frontignan n'est pas un logiciel d'inondation. C'est un outil de visualisation et de décision territoriale, dont l'interface reprend les codes d'un jeu 4X comme Civilization. La version actuelle étant jugée bancale, tu souhaites une version complète en placeholder, avec toutes ses ramifications visibles dès le départ, puis alimentée progressivement selon les besoins et les urgences.

### Expérience recherchée

Une même carte du territoire doit proposer plusieurs modes de vue, comme les lentilles de Civ : territoire, relief et pentes, eau, réseaux pluviaux, inondation, secours, urbanisme, nature, climat, mobilités, économie ou gouvernance. On change de lecture sans changer d'outil. Des couches peuvent aussi se superposer à ces modes.

Autour de la carte, Atlas comprendrait :

- un inspecteur pour comprendre un lieu, un réseau ou un équipement ;
- un arbre ramifié d'actions pour explorer les interventions possibles ;
- des scénarios avant/après et une frise temporelle ;
- des indicateurs transversaux pour voir les effets et arbitrages entre modules.

L'exemple prioritaire discuté relie pentes → écoulement → réseau pluvial → risque d'inondation → moyens de sauvetage. Il illustre la logique d'Atlas, mais ne doit pas réduire le projet à ce seul sujet.

### Méthode de construction

Le principe est de dessiner l'ensemble du produit avant de tout développer : modes, modules, sous-modules, objets cartographiques et actions existent d'abord comme structure navigable. Leur contenu est ensuite ajouté par priorité :

1. rendre l'interface et les modes utilisables ;
2. intégrer les données territoriales jugées urgentes ;
3. approfondir les modules et leurs liens ;
4. ajouter des simulations seulement lorsqu'elles sont fondées et vérifiables.

Point de vigilance essentiel : un placeholder, une donnée réelle, une prévision officielle et un résultat simulé doivent être clairement distingués. Un chiffre ou un « effet avant/après » inventé pour la démonstration ne doit jamais ressembler à une estimation fiable.

En une phrase : Atlas doit devenir une carte stratégique jouable du territoire réel, extensible par modules, où l'on peut explorer différentes vues, comprendre leurs interactions et tester des décisions — l'inondation n'étant qu'une branche parmi d'autres.

---

## Document 2 — Synthèse « grok-4.5-search » (sans sources)

### 1. Point de départ

Recherche d'outils / projets GitHub et logiciels de prévention des risques d'inondation, avec un angle Asie, puis un outil récent vu sur Instagram.

Éléments repérés :

- Projets GitHub (ex. flood-risk-dss Pakistan, autres hors Asie)
- FastFlood Global (Fast Hazard, nov. 2025) : simulations très rapides, résolution fine, tests Bangladesh, interface navigateur — probablement l'outil vu sur Insta
- Moteurs open source utiles : LISEM, LISFLOOD-FP, prototypes QGIS, etc.
- Côté France / Frontignan : PPRI, AZI, Géorisques, données locales

### 2. Besoin réel clarifié

Pas un simple logiciel d'inondation.

Objectif : un équivalent « Atlas » pour Frontignan — outil / jeu / visualisation de type 4X (Civilization, etc.) branché sur un territoire réel :

- carte stratégique interactive
- observation, diagnostic, simulation, décision, suivi
- pas seulement afficher des zones inondables

Précision importante : la prévention inondation n'est qu'un module. Le potentiel est une console de décision territoriale multi-thématiques.

### 3. Vision produit : Atlas

| Dimension | Contenu |
|---|---|
| Métaphore | City-builder / 4X sur données réelles |
| Cœur | Carte unifiée + modes de vue + arbre d'actions + indicateurs |
| Public | Décideurs (élus, techniciens) plus que purs analystes SIG |
| Méthode | Placeholder complet d'abord, remplissage progressif par urgence |

Boucle de jeu :

Observer → Diagnostiquer → Simuler → Décider (actions / travaux) → Suivre les effets

### 4. Modes de vue carte (style Civ)

Lentilles sur le même territoire (un mode actif + overlays) :

| Mode | Rôle |
|---|---|
| Territoire / admin | Limites, PLU, bâti |
| Relief & pentes | MNT, talwegs, bassins versants |
| Cycle de l'eau | Cours d'eau, nappes, Thau, zones humides |
| Réseaux pluviaux | Collecteurs, avaloirs, bassins, points noirs |
| Inondation | PPRI, AZI, scénarios, hauteurs |
| Urgence / secours | PCS, équipes de sauvetage, évacuation, moyens |
| Réseaux techniques | AEP, assainissement, élec… |
| Mobilités, foncier, climat, nature, multi-risques, social, économie, patrimoine, énergie, gouvernance | Modules élargis |
| Scénario | Comparateur avant/après actions |

Overlays : météo, alertes, chantiers, annotations.

### 5. Modules et ramifications

Branches principales :

- **Risques & résilience** : inondation (ruissellement Gardiole + submersion marine), pluvial, incendie, côte, industriel, argiles, multi-risque
- **Pluvial & drainage** : plan des réseaux, pentes, capacités, entretien, noues/bassins, désimperméabilisation
- **Secours & crise** : équipes de sauvetage, PCS, matériel, axes d'évacuation, mode temps réel, RETEX
- **Eau & milieux** : Thau, nappes, qualité, usages
- **Aménagement** : PLU, ZAN, renaturation, mobilités, habitat
- **Nature & climat** : TVB, ICU, littoral, scénarios climatiques
- **Société / éco / gouvernance** : démographie saisonnière, économie locale, compétences, budgets (PAPI, etc.)

Arbre technologique (actions) : chaque action a coût, délai, prérequis, effets multi-modules, preview carte, hook de simulation. Exemples : capteurs, noues, bassins, reprise de collecteurs, renforcement PCS, renaturation, etc.

« Unités » sur la carte : zones, réseaux, ouvrages, bâtiments enjeux, équipes mobiles (sauvetage, curage…), projets « ghost ».

Indicateurs (yields) : risque inondation, performance pluviale, préparation crise, nature, chaleur, budget, acceptabilité, ZAN, conformité réglementaire.

### 6. Spécificités Frontignan

- Double aléa : ruissellement (Gardiole) + submersion marine / lido
- PPRI, AZI, PCS, CatNat
- Enjeux : population permanente + forte saisonnalité (campings, tourisme)
- Contexte : lagune de Thau, AOC Muscat, port, agglo Sète possible plus tard
- Données cibles : IGN, Géorisques, mairie, réseaux pluviaux, MNT/pentes

### 7. Architecture technique (visée)

- Front : carte MapLibre + deck.gl, UI modes / inspecteur / arbre / timeline / yields
- Schéma : modes, modules, actions, layers avec statuts EMPTY → SHELL → DATA → LIVE → SIM
- Simu : stubs d'abord, puis LISEM / approches simples, éventuellement moteurs plus lourds
- FastFlood : référence UX / perf, pas le cœur open source intégrable tel quel (moteur en partie propriétaire ; LISEM plus pertinent en open source)

### 8. Stratégie de construction

- Phase 0 — Shell jouable : 6 modes, faux geojson, actions vides, deltas fake → « feeling 4X »
- Phase 1 — Données urgentes : territoire, pentes, PPRI, PCS, secours, pluvial partiel
- Phase 2 — Modules environnementaux utiles (pluvial complet, côte, perméabilité…)
- Phase 3 — Vraie simulation + comparateur + export élu
- Phase 4 — Élargissement (nature, économie, agglo, crise live…)

Principe : tout déclarer en placeholder, remplir selon besoins et urgence — ne pas tout coder d'un coup.

### 9. Ce qui distingue Atlas d'un SIG

| SIG classique | Atlas |
|---|---|
| Couches pour expert | Carte stratégique pour décideur |
| Thématiques silotées | Indicateurs transverses + actions |
| Statique | Boucle décider → voir l'effet |
| Pas de « jeu » | Arbre techno, unités, scénarios, yields |

### 10. Fil rouge de la conversation

```text
GitHub / Asie / inondation
        ↓
FastFlood (Instagram, récent)
        ↓
Équivalent « Atlas » Frontignan
        ↓
Inondation = un module seulement
        ↓
Outil-jeu 4X multi-vues + multi-modules
        ↓
Placeholder complet (modes Civ, pluvial, pentes,
secours, arbre d'actions) à remplir progressivement
```

### 11. Prochaines étapes possibles (issues de la discussion)

1. Spec JSON complète (modes / modules / actions)
2. Scaffold app carte avec modes switchables
3. Détail d'un mode (ex. Pluvial + Inondation + pentes)
4. Moteur de scores stub
5. Liste des couches Phase 0/1 et sources open data
6. Wrapper / audit LISEM ou autres briques open source

En une phrase :

Atlas est une plateforme stratégique territoriale type 4X pour Frontignan, dont l'inondation, les réseaux pluviaux, les pentes et les équipes de sauvetage sont des modules prioritaires dans un système plus large de vues, d'actions et d'indicateurs, construit d'abord en placeholder complet puis enrichi par urgence.

---

## Notes d'intégration (monorepo)

- **Ce que ces synthèses inspirent** → capturé dans la spec canonique `../atlas-frontignan-2026.json` : 14 modes (dont scénario), 7 modules, 15 actions, 9 indicateurs, 6 types d'« unités », 4 overlays, 5 phases, statuts EMPTY → SHELL → DATA → LIVE → SIM.
- **Ce qui est déjà réel** → les 6 zones de blocage cévenols (dataset `frontignan-cevenols-2026`) et les watchpoints climat Thau (dataset `el-nino-godzilla-2026`) sont branchés en tant que données **DATA** dans la coquille — seule une partie du contenu est donc réellement « placeholder ».
- **Non retenus pour l'instant** : FastFlood (référence UX/perf citée, non vérifiable hors ligne), audit LISEM (Phase 3), MapLibre + deck.gl (cible Phase 3 ; la Phase 0 est volontairement sans dépendance).
