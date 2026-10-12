# Audit ciblé de l'automatisation — 12 octobre 2026

## Périmètre et preuve

- Dépôt : `Sathancabrol/monorepo`.
- Base examinée : `origin/feat/gap-driven-audit-2026-10-11`, SHA `370801b`.
- Vérification distante : les branches `feat/gap-driven-audit-2026-10-11`, `feat/automated-project-audit-2026-10-11` et `audit/convergence-2026-10-10` existent encore sur GitHub aux SHA observés localement.
- Méthode : revue statique des scripts, du workflow, du handoff et des documents d'automatisation. Aucun test, build ou workflow n'a été exécuté.

## Observations

1. Le workflow imposait `ref: main` au checkout. Un lancement manuel depuis la branche d'audit aurait donc vérifié le code de `main`, pas le code sélectionné dans l'interface GitHub Actions.
2. En cas d'échec de lecture des métadonnées d'un dépôt, le scanner omettait toutes ses branches du nouvel index.
3. En cas d'échec de pagination de la liste des branches, les branches connues mais non retournées pouvaient être marquées `not_listed_now`, ce qui confondait indisponibilité de l'API et disparition réelle.
4. L'audit reste un inventaire statique : la présence d'un test, d'un workflow ou d'un fichier source ne prouve ni exécution ni fonctionnement.

## Décisions appliquées

- Laisser `actions/checkout` utiliser la ref de l'événement pour les lancements manuels et les pushes.
- Interdire la publication automatique des rapports lorsque la ref n'est pas `refs/heads/main`.
- Préserver les entrées précédentes avec les états `metadata_error` ou `branch_list_error` lors d'un échec GitHub, et maintenir ces états dans la file des écarts à examiner.
- Paginer l'audit portefeuille, rendre son état complet ou incomplet visible et enregistrer la ref ainsi que le SHA fournis par GitHub Actions.

## Limites et suite

Au moment de cette revue, les changements ne sont ni fusionnés dans `main` ni déployés. La compilation Python, la validation JSON, sept tests unitaires et le contrôle statique du diff réussissent localement. Une exécution manuelle du workflow sur la branche publiée reste nécessaire avant intégration.

La branche `feat/automated-project-audit-2026-10-11` conserve quatre audits métier absents de la branche gap-driven. Ils n'ont pas été copiés ni modifiés ici afin d'éviter une fusion implicite; leur branche et leurs chemins sont enregistrés dans la todo pour une intégration ultérieure avec revue de provenance.
