# Synchronisation avec le dépôt `Sathancabrol/proto-cognitorium`

**Date :** 2026-10-07 · **Commit de référence du dépôt :** HEAD de `main` (poussé le 2026-09-10)

Le monorepo avait importé ce projet dans une version **antérieure** au 10 septembre.
12 fichiers ont été remis à jour vers la version du dépôt, qui est **plus complète** :

| Fichier | Avant (monorepo) | Après (dépôt) |
|---|---|---|
| `server.ts` | 511 lignes | **1 008 lignes** |
| `src/App.tsx` | 514 | **846** |
| `src/components/OnboardingModal.tsx` | 505 | **780** |
| `src/components/QuickAddNodeModal.tsx` | 536 | **707** |
| `src/components/MetiersGraph.tsx` | 938 | **1 079** |
| `src/components/TemporalNetworkGraph.tsx` | 659 | **724** |
| `src/components/ExperienceDistillerModal.tsx` | 568 | **646** |
| `src/components/ExperimentStudio.tsx` | 493 | **545** |
| `src/components/HorizonsBridge.tsx` | 587 | **619** |
| `src/components/DashboardView.tsx` | 651 | **663** |
| `src/components/Header.tsx` | 277 | **283** |
| `src/types.ts` | 344 | **418** |

Les versions précédentes restent accessibles dans l'historique Git du monorepo (commits antérieurs à cette synchronisation).
Contrôle : `python3 scripts/verif-completude-repos.py --repo proto-cognitorium --no-branches`
