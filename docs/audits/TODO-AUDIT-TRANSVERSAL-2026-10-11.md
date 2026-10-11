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
- [x] Parcourir les pages de résultats de branches jusqu'à épuisement pour les 9 dépôts accessibles ciblés (pagination terminée).
- [x] Comparer un premier lot de branches prioritaires : Nexus OS, Carré d'As, BTP, Watchtower INTEL, Language-decoder, OSINT workbench, audit convergence, catalogue outils et squelette d'interface.\n- [ ] Finir l'examen sémantique de toutes les branches pertinentes et relancer les compares avant toute fusion.
- [x] Retrouver les chemins de Nexus OS, BTP, Atlas/Watchtower INTEL et Language-decoder dans les branches prioritaires et documenter leurs capacités.\n- [ ] Compléter la recherche exhaustive sur toutes les branches et archives qui restent non examinées.
- [x] Proposer une règle de gouvernance : dépôt Watchtower pour l'application, branche OSINT comme prototype à porter sélectivement, copies monorepo comme archive.\n- [ ] Comparer fichier par fichier les copies `watchtower-mods` et enregistrer les écarts exacts.

### B. Audit technique de réutilisation
- [x] Rédiger l'audit initial Watchtower / proto-Cognitorium / Cognitorium / HCSM / Research Engine.
- [x] Étendre l'inventaire à l'état de l'art, animation-chronos, Language-decoder et Frontignan.
- [x] Inspecter statiquement les principales briques de persistance (Nexus Memory, Research Engine checkpoints, Watchtower context, proto decay, Language-decoder dynamics).\n- [ ] Exécuter les scripts de tests/build de chaque moteur et enregistrer les logs.
- [x] Repérer les dépendances cloud/API et les options local-first dans les manifestes et README principaux.\n- [ ] Confirmer les dépendances et les comportements en exécution.
- [x] Créer la matrice EXISTANT / À RÉUTILISER / À ADAPTER / À DIFFÉRER avec chemins et preuves statiques.\n- [ ] Compléter pour chaque entrée les dépendances, licences, statut de tests et estimation de coût d'intégration.
- [x] Proposer le contrat minimal commun et identifier `carredas/core/canonical.py`, HCSM et Language-decoder comme schémas à comparer.\n- [ ] Valider le schéma par des fixtures et tests d'intégration.

### C. Mémoire adaptative et fiches de recherche
- [x] Spécifier le modèle de fiche Markdown et les liens vers sources/preuves/résultats/historique dans `templates/research/RECHERCHE.md` et le rapport d'audit.
- [x] Proposer les champs d'identité, provenance, validité temporelle, statut épistémique et validation humaine.\n- [ ] Implémenter et tester le schéma commun.
- [x] Définir les couches de mémoire et le principe de decay sans suppression de la preuve source.
- [x] Définir la boucle d'amélioration après chaque tâche et le stockage des leçons.
- [x] Définir les scénarios d'acceptation pour reprise, rappel par paraphrase, contradiction, decay/récupération, provenance, correction humaine et minimisation.

### D. Vérification et compte rendu
- [ ] Exécuter les suites de tests/build. Les outils GitHub consultés ne montrent aucun workflow associé au commit de l'audit et aucun environnement local n'est disponible dans cette session.
- [x] Marquer explicitement les tests non exécutés : présence du code ≠ exécution ≠ succès ; l'audit historique rapporte deux tests rouges Research Engine à revérifier.
- [x] Mettre à jour l'audit avec les découvertes de branches, les contrats de convergence, le benchmark et les limites.
- [ ] Publier le bilan final après le dernier passage sur les branches et la vérification des tests.

## Critère de fin

Le travail est terminé quand les inventaires/rapports sont commités sur la branche, les décisions sont fondées sur les fichiers/branches examinés, les tests exécutables sont rapportés sans extrapolation, et toute action impossible à exécuter à distance est clairement signalée. « Terminé » ne signifie pas que tous les projets sont fusionnés, réécrits ou validés en production.
