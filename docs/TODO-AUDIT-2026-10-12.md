# Todo — consolidation de l'audit portefeuille

Branche de travail : `codex/audit-hardening-2026-10-12`
Base : `origin/feat/gap-driven-audit-2026-10-11` au SHA `370801b`

## P0 — fiabilité des états

- [x] Faire valider au lancement manuel la ref réellement sélectionnée.
- [x] Restreindre la publication automatique des rapports à `main`.
- [x] Préserver le dernier inventaire connu lors d'une erreur de métadonnées GitHub.
- [x] Distinguer une erreur de liste de branches d'une branche réellement disparue.
- [x] Paginer l'inventaire des branches dans l'audit portefeuille.
- [x] Ne pas déclarer absente une branche non retrouvée lorsque l'inventaire est incomplet.
- [x] Exécuter les validations locales automatisées : compilation Python, JSON, 7 tests unitaires et contrôle du diff réussis le 12 octobre 2026.
- [ ] Vérifier l'exécution GitHub Actions déclenchée automatiquement par le push de la branche, sans publication vers `main`.

## P1 — qualité des preuves

- [x] Ajouter aux rapports la ref et le SHA du code d'audit fournis par GitHub Actions; signaler explicitement une exécution locale non enregistrée.
- [x] Rendre visible l'état complet/incomplet de la pagination dans les rapports Markdown et HTML.
- [x] Rendre la ref, le SHA et le détail des erreurs partielles directement visibles dans les rapports Markdown et HTML.
- [x] Ajouter des tests de régression pour la conservation de l'ancien index dans `audit_gaps.py`.
- [x] Empêcher un arbre GitHub tronqué d'alimenter de faux KPI de couverture.
- [ ] Vérifier les permissions minimales du workflow avant proposition de fusion.

## P2 — intégration

- [x] Comparer cette branche avec `feat/automated-project-audit-2026-10-11` et référencer les quatre audits métier qui restent conservés sur cette branche distante : `AUDIT-REUTILISATION-WATCHTOWER-COGNITORIUM-2026-10-11.md`, `DELTA-COMPARAISONS-BRANCHES-2026-10-11.md`, `MATRICE-REUTILISATION-TRANSVERSALE-2026-10-11.md` et `TODO-AUDIT-TRANSVERSAL-2026-10-11.md`.
- [ ] Préparer un diff de fusion minimal, sans intégrer les propositions WorldTwin ou mémoire sur mesure non demandées.
- [x] Mettre à jour le handoff avec les résultats réellement exécutés.
- [ ] Demander validation humaine avant commit, push, PR ou fusion.

## Critère de sortie

Le workflow lancé sur une branche doit vérifier cette branche, ne jamais publier hors de `main`, conserver un état antérieur en cas d'indisponibilité GitHub, paginer toutes les branches et distinguer explicitement inconnu, absent et erreur. Aucun statut « vérifié » ne doit être produit sans exécution enregistrée.
