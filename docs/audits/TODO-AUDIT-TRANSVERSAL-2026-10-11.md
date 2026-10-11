# TODO — Audit transversal Watchtower / proto-Cognitorium / Cognitorium et écosystème

**Ouvert le :** 2026-10-11  
**Branche de travail :** `feat/automated-project-audit-2026-10-11`  
**Objectif :** terminer un audit fondé sur les dépôts, les branches, les preuves de code et les tests accessibles. Ne pas déclarer « terminé » les actions qui nécessitent un clone local ou une exécution qui n'a pas eu lieu.

## Périmètre

- Watchtower
- proto-Cognitorium
- COGNITORIUM / CLE / watchtower-mods
- HCSM
- reaserch-engine
- ETAT-DE-LART-PSYCHOLOGIE
- animation-chronos
- Language-decoder
- monorepo et ses projets copiés
- rechercher explicitement Atlas, Nexus OS, BTP, simulateur cognitif et autres prototypes dans les branches et l'archive

## Checklist

### A. Inventaire des dépôts et des branches
- [x] Recenser les arbres de fichiers `main` des dépôts principaux.
- [x] Faire un premier inventaire des capacités et doublons visibles dans le code.
- [x] Documenter les restrictions de licence de Watchtower et de ses données.
- [ ] Parcourir les pages de résultats de branches jusqu'à épuisement pour chaque dépôt.
- [ ] Comparer les branches non-main pertinentes aux versions main (commits/fichiers distinctifs), en distinguant les branches de travail automatisées `arena/*`.
- [ ] Rechercher Atlas, Nexus OS, BTP et simulateur dans toutes les branches/archives et produire un tableau des chemins trouvés.
- [ ] Déterminer la source canonique des copies `watchtower-mods` et documenter les écarts.

### B. Audit technique de réutilisation
- [x] Rédiger l'audit initial Watchtower / proto-Cognitorium / Cognitorium / HCSM / Research Engine.
- [x] Étendre l'inventaire à l'état de l'art, animation-chronos, Language-decoder et Frontignan.
- [ ] Vérifier les scripts de tests/build et les contrats de persistance de chaque moteur.
- [ ] Contrôler les dépendances cloud/API et les possibilités local-first.
- [ ] Créer la matrice finale EXISTANT / À RÉUTILISER / À ADAPTER / MANQUANT / À ÉCARTER avec chemin, preuve, dépendance, licence, test et coût d'intégration.
- [ ] Définir les contrats d'échange minimaux entre Watchtower, Cognitorium, HCSM et Research Engine.

### C. Mémoire adaptative et fiches de recherche
- [ ] Spécifier la fiche Markdown de recherche minimale et ses liens vers sources, preuves, claims, contradictions et artefacts.
- [ ] Définir l'identité stable des souvenirs/épisodes, leur provenance, validité temporelle, confiance et statut de validation humaine.
- [ ] Définir les couches mémoire (travail, épisode, concept, archive) et le decay sans suppression des preuves sources.
- [ ] Définir la boucle d'amélioration après chaque tâche : résultat, écart, correction, leçon, consolidation.
- [ ] Définir un benchmark minimal de rappel, reprise après interruption, contradiction et traçabilité.

### D. Vérification et compte rendu
- [ ] Vérifier les suites de tests/build accessibles et exécuter celles qui peuvent être exécutées via CI ou environnement disponible.
- [ ] Marquer explicitement les tests non exécutables depuis les outils distants.
- [ ] Mettre à jour l'audit avec les preuves et limites restantes.
- [ ] Publier un résumé final ici avec les tâches terminées, les décisions et les blocages restants.

## Critère de fin

Le travail est terminé quand les inventaires/rapports sont commités sur la branche, les décisions sont fondées sur les fichiers/branches examinés, les tests exécutables sont rapportés sans extrapolation, et toute action impossible à exécuter à distance est clairement signalée. « Terminé » ne signifie pas que tous les projets sont fusionnés, réécrits ou validés en production.
