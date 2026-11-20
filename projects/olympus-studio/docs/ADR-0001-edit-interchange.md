# ADR-0001 — Format d'échange EDIT indépendant des moteurs

Date : 2026-11-14. Statut : **provisoire, décision d'architecture locale** ; benchmark Windows non réalisé. Issue #12.

## Décision
Conserver le moteur séquentiel EDIT actuel pour le MVP et **ne pas forker** FreeCut, OpenReelio ou Velorn avant essais reproductibles. Ajouter un manifeste d'échange JSON versionné et sans chemins locaux : `src/edit-interchange.js`, testé par `tests/edit-interchange.test.mjs`. Il expose l'ordre, les plages temporelles, les IDs de médias partagés, les titres et la piste audio. Ce n'est **pas** un importeur FreeCut/OpenReelio/Velorn, ni un standard EDL/OTIO. La fonction n'est pas encore branchée à l'interface.

## Vérification amont (GitHub API, 14/11/2026)
| Projet | Licence déclarée par API GitHub | Description amont | Limite |
|---|---|---|---|
| [FreeCut](https://github.com/walterlow/freecut) | MIT | Éditeur vidéo dans navigateur, multi-pistes, keyframes, export | Pas de test d'API/format ni de performance |
| [OpenReelio](https://github.com/openreelio/openreelio) | MIT | Éditeur piloté par prompts, version pré-alpha (<0.5.0) | Contrat d'intégration et stabilité non validés |
| [Velorn](https://github.com/VelornLabs/velorn) | GPL-3.0 | Éditeur vidéo avec workflows génératifs et agents locaux | Obligations de redistribution à analyser avant intégration |

Les identifiants SPDX sont ceux **déclarés par l'API des dépôts**, pas une revue juridique des dépendances transitives ou fichiers individuels. Aucun code tiers copié.

## Contrat initial
- `schema: olympus.edit.interchange.v1`, `timeUnit: seconds`, `duration`, `segments[]`, `soundtrack`.
- Chaque segment : `clipId`, `assetId`, `kind`, `timelineStart`, `duration`, `sourceIn`, `title`.
- Les deux moitiés d'un split gardent le même `assetId` mais ont des `clipId` différents.
- Pas de Blob, URI arbitraire, secret, chemin disque ou appel réseau. Les assets restent dans LIBRARY/Portable; l'échange des octets et les droits d'usage sont des opérations distinctes.
- Pas de conversion implicite de fps/timebase : les secondes flottantes suffisent à ce MVP, mais un futur adaptateur frame-accurate doit déclarer sa timebase et ses arrondis.

## Benchmark encore requis
Épingler SHA/version de chaque candidat, analyser licence complète + dépendances, relever format de projet et APIs documentées, mesurer import/coupe/audio/sous-titres/export avec **la même fixture**, puis CPU/RAM/VRAM sous GTX 1060 et 1650. Choisir cœur/fallback seulement après ces preuves. Aucune affirmation de compatibilité ou de performance aujourd'hui.
