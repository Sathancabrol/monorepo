# Journal incrémental BTP Studio V2

## 2026-11-23 — calculs de métrés isolés

Branche : `feat/btp-all-modules-workbench-20261123`. Base inspectée : `ff2ef6327a7e2ccc8e0a8739c5a7086064efed1e`. Branches V2 et historique conservées ; aucun merge.

Ajouts : `assets/metres-v1.cjs` (fonctions pures sans dépendance) et `tests/metres-v1.test.cjs` (5 scénarios). Terrassement, tranchée trapézoïdale, chaussée multicouche, durée de production/installation/aléas ; rejet des entrées numériques non finies ou négatives.

Preuve de calcul : exécution Node 22.16.0 de la suite équivalente dans un environnement isolé : **5/5 réussis**, 0 échec. Résultats : 30 m³ ; tranchée 4 m / 3 m² / 60 m³ ; couches 25/12/6 m³ ; durée 5 + 1 + 2 = 8 jours. **Limite** : test local sur copie équivalente, pas encore une exécution CI du commit GitHub. Aucun parcours navigateur vérifié dans cette passe. Le moteur n'est pas encore branché à l'interface : ne pas déclarer la fonctionnalité UI terminée.

Suite : exécuter `npm test` sur la branche complète, brancher les métrés aux fiches/atelier, tester les conversions d'unités, arrondis, exports et provenance réelle/simulation. Vérifier les 23 parcours UI et l'intégrité des imports avant toute déclaration de complétion.
