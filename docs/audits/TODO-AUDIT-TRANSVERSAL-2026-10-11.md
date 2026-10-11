# TODO — Audit transversal Watchtower / Cognitorium / Nexus OS / Carré d'As / BTP

**Ouvert le :** 2026-10-11  
**Branche de travail :** `feat/automated-project-audit-2026-10-11`  
**Objectif :** réutiliser le code existant avant toute réécriture, rechercher automatiquement les branches non auditées, documenter les preuves et ne jamais déclarer les tests réussis sans les avoir exécutés.

## Périmètre suivi

Watchtower, proto-Cognitorium, COGNITORIUM/CLE/watchtower-mods, HCSM, reaserch-engine, ETAT-DE-LART-PSYCHOLOGIE, animation-chronos, Language-decoder, monorepo, Nexus OS, Carré d'As, BTP, Atlas Frontignan/Thau et simulateur cognitif.

## Checklist

### A. Inventaire et branches

- [x] Recenser les arbres `main` des dépôts principaux.
- [x] Inventorier les capacités et doublons visibles dans les fichiers consultés.
- [x] Terminer la pagination de recherche des branches pour les 9 dépôts ciblés.
- [x] Faire un premier passage sur les branches prioritaires : Nexus OS, Carré d'As, BTP, Watchtower INTEL, Language-decoder, OSINT Workbench, audit de convergence, catalogue outils et squelette d'interface.
- [x] Comparer les références de Nexus OS, Carré d'As, gap-driven audit, catalogue d'outils, BTP, Watchtower INTEL et Language-decoder à leurs références `main` ; résultats détaillés dans [l'addendum de comparaisons](DELTA-COMPARAISONS-BRANCHES-2026-10-11.md).
- [x] Confirmer par diff GitHub que `watchtower/osint-workbench-v0.1` contient une spécification et des modules OSINT additionnels.
- [ ] Finir l'examen sémantique des branches pertinentes restantes, y compris les autres branches de proto-Cognitorium et des dépôts de recherche.
- [ ] Comparer fichier par fichier les copies `watchtower-mods` dans Watchtower, COGNITORIUM et le monorepo ; consigner les différences exactes et les SHA.
- [ ] Examiner les branches non prioritaires restantes avec le protocole gap-driven et consigner pourquoi chaque branche est ignorée ou retenue.
- [x] Retrouver les modules Nexus OS, BTP, Atlas/Watchtower INTEL et Language-decoder dans les branches, sans les déclarer intégrés ou validés.
- [x] Définir une gouvernance provisoire : Watchtower comme application canonique, OSINT Workbench comme prototype à porter sélectivement, copies monorepo comme archive.

### B. Architecture, réutilisation et risques

- [x] Rédiger l'audit initial Watchtower / proto-Cognitorium / Cognitorium / HCSM / Research Engine.
- [x] Étendre l'inventaire à ETAT-DE-LART-PSYCHOLOGIE, animation-chronos, Language-decoder et Frontignan.
- [x] Inspecter statiquement les mécanismes de persistance Nexus Memory, Research Engine checkpoints, Watchtower context, proto decay et Language-decoder dynamics.
- [x] Repérer les options local-first et les dépendances API/cloud dans les principaux manifestes/README.
- [x] Proposer la convergence via adaptateurs, fiches Markdown et provenance plutôt que créer un nouveau moteur de mémoire.
- [x] Définir un contrat commun minimal à confronter à Carré d'As, HCSM et Language-decoder.
- [ ] Compléter une matrice exhaustive dépendances/licences/tests/coût d'intégration par module.
- [ ] Vérifier les permissions, le traitement des secrets, la sandbox et les appels externes du runtime Nexus OS et de Carré d'As.
- [ ] Confirmer les licences des codes, dépendances, documents et jeux de données avant portage ; la licence du code ne vaut pas automatiquement pour les données tierces.
- [ ] Décider du runtime d'agents canonique après comparaison fonctionnelle et tests, sans fusionner Nexus OS et Carré d'As à l'aveugle.
- [ ] Valider les différences entre les versions des modules et des contrats avant toute fusion.

### C. Mémoire adaptative, decay et recherche

- [x] Définir le modèle de fiche Markdown et ses liens vers sources, preuves, résultats et historique dans `templates/research/RECHERCHE.md`.
- [x] Définir les champs communs : identité, provenance, validité temporelle, statut épistémique, validation humaine et références croisées.
- [x] Définir les couches mémoire : contexte actif, épisodes/runs, fiches de recherche, concepts, index de rappel, consolidation et boucle qualité.
- [x] Spécifier un decay qui baisse la priorité de rappel sans supprimer la preuve source et qui permet la réactivation.
- [x] Définir les scénarios d'acceptation : reprise, paraphrase, contradiction, decay/récupération, provenance, correction humaine et minimisation.
- [ ] Comparer les schémas Carré d'As, HCSM et Language-decoder champ par champ ; choisir un contrat de référence ou documenter les adaptateurs.
- [ ] Implémenter les fixtures et tests d'intégration du contrat commun.
- [ ] Mesurer précision@k, rappel@k, affirmations sans preuve, perte de provenance, doublons après reprise, correction et coût de rappel.
- [ ] Vérifier concrètement la reprise d'un run Research Engine et l'export/indexation/rappel d'une fiche Markdown.

### D. Exécution et validation

- [x] Vérifier la présence des scripts/tests dans les branches ciblées sans confondre présence et exécution.
- [x] Consigner que les résultats CI disponibles pour le commit de l'audit ne montrent aucun workflow associé.
- [x] Noter que l'audit de convergence historique rapporte deux tests Research Engine à revérifier ; ce signal est historique et non confirmé actuellement.
- [ ] Exécuter les tests/builds de Watchtower, Research Engine, HCSM, proto-Cognitorium, Language-decoder, Nexus OS et Carré d'As.
- [ ] Archiver les commandes, versions d'environnement, logs et résultats (pass/fail/skip).
- [ ] Exécuter les tests d'intégration et vérifier les interfaces de convergence.
- [ ] Publier le bilan final séparant : réutilisable maintenant, à adapter, à tester, à différer, bloqué par licence ou par accès.

## État après la passe de comparaison du 2026-10-11

- [x] Comparaisons ciblées documentées : [DELTA-COMPARAISONS-BRANCHES-2026-10-11.md](DELTA-COMPARAISONS-BRANCHES-2026-10-11.md).
- [x] Confirmé : les branches Carré d'As et Nexus OS sont divergentes par rapport à `main`, avec des responsabilités qui se recoupent ; pas de fusion en bloc.
- [x] Confirmé : la branche BTP comprend un corpus et des registres de traçabilité ; protéger les documents et vérifier leurs droits/provenance.
- [x] Confirmé : Watchtower INTEL contient des modules et tests territoriaux additionnels.
- [x] Confirmé : Language-decoder dispose d'une branche avec code et tests, même si `main` est minimal.
- [ ] Non terminé : lecture de toutes les branches, comparaison exhaustive des copies, tests d'exécution et intégration.
- [ ] Aucun test n'est déclaré réussi dans ce rapport sans exécution vérifiable.

## Critère de fin

L'audit ne peut être déclaré terminé que lorsque les branches pertinentes sont examinées ou explicitement classées hors périmètre, les décisions sont sourcées, les tests exécutables sont rapportés avec leurs logs, les restrictions de licence sont distinguées, et les actions impossibles à exécuter sont identifiées. L'audit n'implique pas de fusionner tous les projets ni de les déclarer prêts pour la production.
