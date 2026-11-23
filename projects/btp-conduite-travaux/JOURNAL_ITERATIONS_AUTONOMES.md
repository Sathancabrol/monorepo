# BTP Studio V2 — journal des itérations autonomes

Ce journal est incrémental, distinct du backlog historique `BTP_STUDIO_V2_ETAT_ET_BACKLOG.md`. Les preuves de calcul ne valent pas recette UI ni validation réglementaire. Ne jamais marquer « terminé » sans tests reproductibles.

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
