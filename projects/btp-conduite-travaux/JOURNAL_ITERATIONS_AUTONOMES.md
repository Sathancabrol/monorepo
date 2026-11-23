# BTP Studio V2 — journal des itérations autonomes

## 2026-11-24, passage 8 — attribution des handlers manquants par module

**Inspection :** branches BTP (`feat/btp-all-modules-workbench-20261123`, `feat/btp-studio-premium-3d-20261123`, `fix/btp-navigation-pages-20261123`), backlog V2, veille GitHub 2026, journal et source du diagnostic. Le diagnostic global des handlers ne permettait pas de savoir quel module contenait un contrôle défaillant.

**Code réellement poussé :**
- [`89374741`](https://github.com/Sathancabrol/monorepo/commit/89374741f65181b205065a12209330ceacc82442) : `assets/diagnostics-v3.js` — attribution des appels inline non résolus au panneau `tab-*` propriétaire ; nombre d'anomalies par module dans le JSON et dans le tableau du diagnostic ; séparation des appels globaux et des appels propres à un module ; étiquette explicite du caractère heuristique des anomalies.
- [`96ef1d22`](https://github.com/Sathancabrol/monorepo/commit/96ef1d2272fbde4c6d93111362a6384b6a37976a) : `tests/diagnostics-module-attribution.test.cjs` — test reproductible simulant deux panneaux et un contrôle global, couvrant l'attribution, le compteur, le statut structurel et l'absence de certification fonctionnelle.

**Vérification :** syntaxe du nouveau `diagnostics-v3.js` compilée dans un moteur JavaScript isolé (`new Function`), six vérifications structurelles de présence du code passées. **Le test Node versionné et les clics dans un navigateur n'ont pas été exécutés ici.** Commande : `cd projects/btp-conduite-travaux && node tests/diagnostics-module-attribution.test.cjs`. Ne pas confondre compilation et recette UI.

**Limites :** l'analyse par expressions régulières des attributs HTML peut générer des faux positifs et ne détecte ni les événements liés par `addEventListener`, ni les erreurs métier. La liste par module ne prouve pas que les fonctions existent ou répondent correctement. Les panneaux hérités ont encore des données de démonstration et des interactions non vérifiées.

**Suite :** exécuter les tests Node et Playwright/Chromium sur l'application réelle ; corriger les fonctions manquantes les plus fréquentes ; réaliser les scénarios création → persistance → export → rechargement pour chaque module, puis le flux DCE → DOE. Ne pas intégrer de dépôt tiers avant preuve de licence et prototype isolé.

**Statut :** V2 incomplète. Aucun merge dans `main`, aucune dépendance payante ajoutée.

---


## 2026-11-23, passage 5 — calculateurs techniques indicatifs raccordés

**Inspection :** branches BTP (branche de travail et deux branches historiques), backlog, journal, veille 2026, `index.html` et `assets/workbench-v3.js`. Les handlers de calcul hydraulique, bassin, réseaux électriques et éclairage public étaient appelés par les contrôles UI sans définition dans le monolithe.

**Code poussé :**
- `dc76da9b9c07b58b7b1f72a29f0b068d2ff309ab` : `assets/technical-calculators-v1.js`, quatre calculateurs indépendants, sans dépendance ni réseau. Manning-Strickler en conduite circulaire partiellement remplie (section et périmètre mouillés), ruissellement brut d'une pluie, chute de tension résistive simplifiée et rapport espacement/hauteur d'éclairage.
- `78fed5d845ccc787b4e24550d362f7969970eb5e` : `tests/technical-calculators-v1.test.cjs`, **10 scénarios Node** versionnés, à exécuter sur PC.
- `448d1c96248bd703c47c62cac7b079d7c41e4097` : raccordement du script au workbench historique, chargement après DOMContentLoaded, sans modification destructive du monolithe.

**Preuves de vérification :** compilation syntaxique JS du module et du test réussie ; **6/6 scénarios exécutés avec succès dans un moteur JavaScript isolé** : conduite pleine (Q cohérent), demi-section circulaire, refus de remplissage >100 %, bassin 562,5 m³ brut pour 2,5 ha × 0,5 × 45 mm, chute de tension résistive monophasée, refus de lux inventés. Les **10 tests Node versionnés ne sont pas déclarés exécutés**. Commande reproductible : `cd projects/btp-conduite-travaux && node tests/technical-calculators-v1.test.cjs`.

**Limites métier :** le bassin affiche un volume **brut de ruissellement**, pas un dimensionnement réglementaire de rétention ; l'ajutage reste non dimensionné faute d'hydrogramme. La chute de tension est une estimation résistive cos φ=1, sans vérification normative, protection ni échauffement. Le ratio hauteur/espacement ne fournit **aucun lux** sans photométrie. L'autocurage n'est **pas déclaré conforme** automatiquement. Valeurs fictives conservées et signalées comme indicatives. Aucun navigateur, aucune caméra, aucune recette métier, aucune fusion dans main.

**À poursuivre :** test réel des quatre sous-vues dans un navigateur, détection des autres handlers orphelins, correction de la navigation technique qui n'affiche actuellement que quatre vues, vérification des calculs contre références métier, puis raccordement aux données de chantier et à la géométrie 3D.

**Statut :** V2 incomplète ; poursuite nécessaire.


## 2026-11-23, passage 4 — registres locaux livraisons et intempéries

**Inspection :** branche de travail et deux branches historiques `feat/btp-studio-premium-3d-20261123`, `fix/btp-navigation-pages-20261123` ; backlog V2, journal, veille GitHub 2026 et source `assets/workbench-v3.js` relus. Les boutons de création/export des registres pointaient vers des fonctions absentes du monolithe.

**Code poussé :**
- `7ba2b27ca07553041d79530c13f9105ca73a42b3` : `assets/legacy-registers-v1.js`, module local sans dépendance ajoutant saisie/validation des bons de livraison et constats d'intempéries, anti-doublon, sauvegarde localStorage, rendu tableau/KPI, export CSV avec échappement des guillemets.
- `8949f6a0f7a295c567802a5681b19218d50f27dd` : chargement du module depuis `assets/workbench-v3.js`, sans remplacement du monolithe historique.
- `db8bc8b630d2cbb98809a2d20eb242507a80c72b` : `tests/legacy-registers-v1.test.cjs`, scénario de non-régression reproductible sans npm.

**Vérification effective :** syntaxe JavaScript du nouveau module et du workbench vérifiée par compilation JS isolée. **7 contrôles exécutés et réussis** sur un DOM simulé : création BL, KPI enrobé 28,40 t, rejet doublon, rejet quantité négative, création intempérie, refus de calcul automatique d'un droit contractuel, invocation des deux exports CSV. Le test Node versionné contient 9 assertions ; **la commande Node n'a pas été exécutée dans cet environnement**. Exécution locale attendue : `cd projects/btp-conduite-travaux && node tests/legacy-registers-v1.test.cjs`.

**Limites / sécurité :** les données enregistrées sont locales au navigateur, non synchronisées avec les projets, et non des preuves validées. Les constats ne donnent **aucun droit automatique** à prolongation de délai ou indemnisation. Le KPI béton reste « Non renseigné » (unités mixtes) et le rendement enrobé « Non calculable sans surface réelle ». Aucune validation en navigateur, aucun test caméra/3D ou test d'impression. Aucun SDK externe ajouté, aucune fusion dans `main`.

**Suite :** vérifier chargement réel du script et les formulaires en navigateur, fiabiliser les calculateurs hydraulique/électrique et la navigation de sous-vues, puis relier les registres au chantier actif avec migration de données versionnée. V2 toujours incomplète.


Ce journal est incrémental, distinct du backlog historique `BTP_STUDIO_V2_ETAT_ET_BACKLOG.md`. Les preuves de calcul ne valent pas recette UI ni validation réglementaire. Ne jamais marquer « terminé » sans tests reproductibles.

## 2026-11-23, passage 3 — validation des calculs du workbench 23 modules

**État inspecté :** branche `feat/btp-all-modules-workbench-20261123`, branches `feat/btp-studio-premium-3d-20261123` et `fix/btp-navigation-pages-20261123` repérées ; backlog historique et veille GitHub 2026 relus. Le monolithe `index.html` comporte 23 panneaux, et `assets/workbench-v3.js` contient la couche d'interaction commune aux 23 modules.

**Correctif réel :** `3523da65d2d594e530cf26b6781781c6b88cca29` modifie `assets/workbench-v3.js`. Auparavant, les valeurs vides ou non numériques étaient silencieusement remplacées par zéro ou les valeurs d'exemple, et une division par zéro affichait un taux trompeur de 0 %. Les calculs rapides affichent désormais « Saisie invalide », « Division par zéro » ou « Résultat hors limites », au lieu de résultats plausibles mais faux. Les zéros valides restent acceptés ; les soldes négatifs calculés restent affichables.

**Tests :** `aa4ff9103ba058b188a5e1edf1697493f6fef9dc` ajoute `tests/workbench-metrics.test.cjs` (13 scénarios). **13/13 scénarios exécutés et réussis** dans un moteur JavaScript isolé en extrayant le bloc `metrics` de la version GitHub après commit. Scénarios : exemples de trois modules, entrée vide, texte, quantité négative, zéro valide, division par zéro, résultat nul, solde négatif, infini en entrée, décimale et débordement numérique. Commande Node reproductible :

```bash
cd projects/btp-conduite-travaux
node tests/workbench-metrics.test.cjs
```

**Limites :** exécution de la commande Node non effectuée ici ; pas de navigateur, donc les interactions DOM, impression et persistance ne sont pas validées. Le correctif vise le calcul rapide pédagogique commun aux 23 modules, **pas** les calculateurs historiques intégrés dans le monolithe, qui doivent encore être audités et corrigés. Les données restent fictives et aucune conformité réglementaire n'est démontrée.

**Suite prioritaire :** inspecter/corriger les handlers UI manquants du monolithe, notamment les calculateurs hydrauliques/électriques et les registres livraisons/intempéries ; réaliser tests navigateur sur l'ensemble des 23 modules, puis intégrer données de tâche, planning, géométrie 3D et exports. Aucun SDK tiers intégré (veille GitHub = benchmark).

**Statut :** V2 incomplète ; poursuite nécessaire.

## 2026-11-23, passage 2 — fiabilité du moteur de tâches

**Base inspectée :** `feat/btp-all-modules-workbench-20261123`; branches repérées `feat/btp-studio-premium-3d-20261123`, `fix/btp-navigation-pages-20261123`. Backlog et veille GitHub 2026 lus. Aucune fusion, aucune dépendance externe ajoutée.

### Modifications poussées

- `2b726f279e8c3e207f024b1f6a08a73e58f8f535` : `assets/project-core-v1.js` refuse désormais quantités vides/nulles/booléennes, effectifs fractionnaires et durées imposées non entières ; tâche à quantité nulle = zéro jour de production sauf durée imposée, avec avertissement ; la base du planning est explicitement `calendar-days`.
- `884d85203a96398520626ffa9b447815a0bd9a61` : ajout de `tests/project-core-v1.test.js` sans npm.
- `92683f9ddc202874183936867c463a82f1f0fae1` : correction de `endInclusive` pour les tâches de durée nulle (valeur `null` au lieu d'une date antérieure au début).
- `825f43973d623349a7d0ba7adacdf33350b3d40f` : ajout d'une assertion de non-régression pour ce cas.

### Vérifications

**18/18 assertions réussies** en exécutant les versions relues depuis GitHub dans un environnement JavaScript isolé avec un adaptateur `assert` équivalent aux méthodes Node utilisées. Couverture : 6 tâches du chantier exemple, 1 830 € de coût théorique, 6 jours calendaires séquentiels, refus de 5 entrées invalides, zéro quantité, durée forcée, successeur d'une tâche nulle, dépendance inconnue, cycle, ID dupliqué. La commande reproductible sur machine disposant de Node est :

```bash
cd projects/btp-conduite-travaux
node tests/project-core-v1.test.js
```

**Limites de preuve :** commande Node non exécutée ici ; aucune session navigateur ni test tactile/visuel/CI. Les données du scénario sont explicitement fictives ; aucun prix ni rendement n'est vérifié contre un marché. Les dates sont des jours **calendaires**, non des jours ouvrés, et n'intègrent pas météo, jours fériés ou horaires. Le modèle n'est pas un planning contractuel.

### État et priorités suivantes

- **Moteur de tâches :** correctifs et tests unitaires ajoutés, pas de recette métier exhaustive.
- **23 modules :** non déclarés fonctionnels ; audit structurel présent mais insuffisant. Examiner les appels UI orphelins dans le monolithe, puis tester chaque parcours avec preuves de navigateur.
- **Priorité P0 suivante :** validation de saisie et cohérence prévu/réalisé/coût ; import/export JSON avec sauvegarde et récupération ; provenance des données ; correction des calculateurs et boutons cassés ; branchement 3D↔tâches↔planning.
- **Veille :** `VEILLE_GITHUB_2026_BTP.md` conservée comme benchmark ; aucun nouveau SDK intégré sans prototype, licence et test matériel.

**Statut :** V2 incomplète, automation à poursuivre.


## 2026-11-23, passage 6 — sécurisation des registres CSV et saisies

**Inspection :** comparaison de `main` avec `feat/btp-all-modules-workbench-20261123` (80 commits d'avance lors de la lecture, 300 fichiers signalés dans la comparaison), branches `feat/btp-studio-premium-3d-20261123` et `fix/btp-navigation-pages-20261123` repérées. Backlog V2, veille 2026, journal et fichiers de réparation V4 relus. Les corrections de navigation des sous-vues techniques et du planning étaient déjà présentes dans `assets/navigation-repairs-v4.js` : elles n'ont **pas** été réécrites.

**Problème confirmé :** `assets/legacy-registers-v1.js` exportait les valeurs saisies en CSV avec simple échappement des guillemets. Un numéro de BL commençant par `=`, `+`, `-` ou `@` pouvait être interprété comme formule à l'ouverture dans un tableur. La validation des dates acceptait des dates calendaires inexistantes via `Date.parse`, et la quantité vide pouvait être convertie en zéro.

**Code poussé :**
- `4ae97b13df99085b6170e540c51d6948d4a671d5` : neutralisation des formules CSV en préfixant une apostrophe dans les cellules suspectes, validation stricte des dates (année bissextile, mois, jour, heure/minute), rejet de quantité vide et borne maximale de saisie (1 000 000 t).
- `a2f9cabb42c245093f7a311d9c8c94f5ea479247` : test Node reproductible `tests/legacy-registers-security.test.cjs` (DOM simulé : rejet date impossible, quantité vide, enregistrement valide, export de cellule à formule neutralisée).

**Vérification effective :** 7 cas calendaires, 5 chaînes de formule CSV, 3 champs ordinaires et 1 compilation JavaScript **réussis** dans un moteur JavaScript isolé sur le texte modifié avant commit. **La commande Node du fichier de test versionné n'a pas été exécutée ici** et **aucun parcours navigateur réel n'a été réalisé**. Pour reproduire : `cd projects/btp-conduite-travaux && node tests/legacy-registers-security.test.cjs`.

**Limites :** le préfixe apostrophe réduit le risque d'exécution de formules lors de l'ouverture CSV dans les tableurs usuels, mais doit être vérifié sur LibreOffice et Excel ; la défense n'est pas une garantie universelle pour tous les importateurs. Les registres restent locaux, manuels et non contractuels. Aucun SDK ajouté, aucune fusion dans `main`.

**À suivre :** exécuter les tests Node et UI dans un navigateur, vérifier le CSV dans un tableur, étendre la protection à tous les exports CSV du monolithe, auditer les 23 modules par scénario complet et vérifier la persistance/import/export de projet. **V2 incomplète.**


## 2026-11-23, passage 7 — diagnostic des commandes UI orphelines

**Inspection :** branche de travail relue, trois branches BTP recensées (`feat/btp-all-modules-workbench-20261123`, `feat/btp-studio-premium-3d-20261123`, `fix/btp-navigation-pages-20261123`). Backlog V2, journal des six passages, veille GitHub 2026 et modules `assets/diagnostics-v3.js`, `assets/navigation-repairs-v4.js`, `assets/legacy-registers-v1.js` inspectés. Aucune reprise à zéro.

**Problème :** le diagnostic existant dénombrait les panneaux et boutons, mais ne détectait pas les noms de fonctions appelées par les attributs `onclick`, `onchange`, `oninput`, `onsubmit`, `onload`, `onmousedown`, `onmouseup` lorsqu'ils étaient absents de `window`. Un bouton présent pouvait donc être présenté comme « connecté » alors que son action échouait.

**Code poussé :** `8883df3cf6148f809ae957e2c23f5b9c9dc0f0d4` — `assets/diagnostics-v3.js`. Ajout d'un inventaire `unresolved_inline_handlers` dans l'export JSON, compteur dans la fenêtre de diagnostic et détail des 50 premières occurrences. Analyse statique sans exécuter les actions ; les appels de propriétés (ex. `Math.max`) sont exclus pour réduire les faux positifs. Aucune modification du monolithe, de la branche principale ou des données métier.

**Tests réellement exécutés :** compilation JavaScript via `new Function`, initialisation sous fenêtre/document simulés, puis cinq scénarios d'attributs inline : fonction absente, fonction `window` absente, fonction globale présente, appel conditionnel absent, méthode d'objet ignorée. Résultat **5/5 scénarios conformes aux attentes**. Aucun navigateur réel, aucun test DOM complet ou CI exécuté. Le diagnostic n'est pas une preuve de fonctionnement métier et peut manquer les appels indirects, fonctions chargées tardivement ou événements ajoutés via JavaScript.

**À suivre :** exécuter ce diagnostic dans un navigateur réel sur les 23 panneaux, trier les faux positifs, réparer les appels orphelins un par un avec tests d'interaction, puis poursuivre les scénarios DCE → DOE et les tests de performance. Veille 2026 conservée, aucun SDK tiers intégré. **V2 incomplète ; poursuivre les itérations.**
