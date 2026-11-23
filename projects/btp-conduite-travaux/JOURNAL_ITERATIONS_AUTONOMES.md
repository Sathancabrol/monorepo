# BTP Studio V2 — journal des itérations autonomes

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
