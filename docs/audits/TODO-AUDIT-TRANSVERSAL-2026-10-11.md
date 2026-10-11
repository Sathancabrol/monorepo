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
- [x] Vérifier les chemins OSINT Workbench sur les références `main` : absent aux deux chemins testés, présent sur la branche prototype COGNITORIUM ; ce constat ne couvre pas toutes les branches.
- [x] Confirmer par diff GitHub que `watchtower/osint-workbench-v0.1` contient une spécification et des modules OSINT additionnels.
- [ ] Finir l'examen sémantique des branches pertinentes restantes, y compris les autres branches de proto-Cognitorium et des dépôts de recherche.
- [x] Comparer un nouveau lot de branches monorepo : Bone, Laplace, Atlas Frontignan, proto-Cognitorium, archive Carré d'As, archive d'audit, registre créatif et HUD mobile.
- [x] Comparer les branches Watchtower restantes et plusieurs variantes de ETAT-DE-LART-PSYCHOLOGIE ; relever l'agent de recherche Uranus, les outils d'inventaire et les variantes d'application cognitive.
- [ ] Comparer fichier par fichier les copies `watchtower-mods` dans Watchtower, COGNITORIUM et le monorepo ; consigner les différences exactes et les SHA.
- [ ] Examiner les branches non prioritaires restantes avec le protocole gap-driven et consigner pourquoi chaque branche est ignorée ou retenue.
- [x] Lire les scripts `audit_gaps.py` et `audit_portfolio.py` ainsi que le workflow ; consigner le budget de 15 arbres par exécution, la limite de 100 branches du rapport portefeuille et l'absence de revue sémantique automatique dans l'addendum.
- [ ] Ajouter/valider des tests du scanner sur fixtures et un déclencheur de validation PR, sans publier automatiquement depuis une PR vers `main`.
- [x] Lire les sondes d'audit de `proto-cognitorium:arena/01a08342-proto-cognitorium` : le README signale l'absence d'assertions runtime ; le script de sonde force un code de sortie 0, donc il faut corriger ce faux-vert potentiel avant de compter sur la CI.
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
- [x] Définir les axes comparatifs nécessaires pour les runtimes Nexus OS / Carré d'As / Laplace et les moteurs de recherche Uranus / Research Engine ; la matrice reste à remplir avec preuves détaillées.
- [ ] Vérifier les permissions, le traitement des secrets, la sandbox et les appels externes du runtime Nexus OS et de Carré d'As.
- [ ] Confirmer les licences des codes, dépendances, documents et jeux de données avant portage ; la licence du code ne vaut pas automatiquement pour les données tierces.
- [x] Repérer `UNLICENSED` dans Laplace et l'absence de fichier `LICENSE` à la racine des références consultées pour Bone/Uranus ; bloquer le portage/redistribution de Laplace et clarifier les droits des autres avant réutilisation.
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
- [x] Revoir statiquement le calcul Trust Factor d'Uranus : garder le score explicitement heuristique, dissocier taille d'échantillon et réplication, et tester les collisions du dédoublonnage DOI/titre.
- [ ] Vérifier concrètement la reprise d'un run Research Engine et l'export/indexation/rappel d'une fiche Markdown.

### D. Exécution et validation

- [x] Vérifier la présence des scripts/tests dans les branches ciblées sans confondre présence et exécution.
- [x] Consigner que les résultats CI disponibles pour le commit de l'audit ne montrent aucun workflow associé.
- [x] Noter que l'audit de convergence historique rapporte deux tests Research Engine à revérifier ; ce signal est historique et non confirmé actuellement.
- [ ] Exécuter les tests/builds de Watchtower, Research Engine, HCSM, proto-Cognitorium, Language-decoder, Nexus OS et Carré d'As.
- [x] Recontrôler les statuts GitHub du dernier commit d'audit : aucun workflow associé et aucun statut combiné visible ; l'exécution CI n'est pas confirmée.
- [x] Tenter l'accès Git en lecture seule depuis l'environnement d'exécution : `git ls-remote` échoue car `github.com` n'est pas résolu dans cet environnement ; aucun clone local ni lancement de tests n'est donc possible ici.
- [ ] Archiver les commandes, versions d'environnement, logs et résultats (pass/fail/skip).
- [x] Repérer que les tests Uranus écrivent des runs dans `output/agent_runs` ; recommander l'isolation des artefacts de test.
- [ ] Exécuter les tests d'intégration et vérifier les interfaces de convergence.
- [ ] Publier le bilan final séparant : réutilisable maintenant, à adapter, à tester, à différer, bloqué par licence ou par accès.
- [x] Consigner dans l'addendum les nouvelles branches à haute valeur et les décisions de convergence provisoires.

## État après les passes de comparaison du 2026-10-11

- [x] Comparaisons ciblées documentées : [DELTA-COMPARAISONS-BRANCHES-2026-10-11.md](DELTA-COMPARAISONS-BRANCHES-2026-10-11.md).
- [x] Confirmé : les branches Carré d'As et Nexus OS sont divergentes par rapport à `main`, avec des responsabilités qui se recoupent ; pas de fusion en bloc.
- [x] Confirmé : la branche BTP comprend un corpus et des registres de traçabilité ; protéger les documents et vérifier leurs droits/provenance.
- [x] Confirmé : Watchtower INTEL contient des modules et tests territoriaux additionnels.
- [x] Confirmé : Language-decoder dispose d'une branche avec code et tests, même si `main` est minimal.
- [x] Confirmé : ETAT-DE-LART-PSYCHOLOGIE a une branche de 38 commits en avance contenant un agent de recherche à compétences modulaires et des tests déclarés.
- [x] Confirmé : les branches Watchtower INTEL, Atlas Frontignan et les archives d'audit contiennent des deltas significatifs à comparer avant portage.
- [x] Confirmé : Laplace et Bone sont des candidats supplémentaires à auditer ; leurs présences dans l'archive ne prouvent ni leur maturité ni leur sécurité.
- [ ] Non terminé : lecture de toutes les branches, comparaison exhaustive des copies, tests d'exécution et intégration.
- [ ] Aucun test n'est déclaré réussi dans ce rapport sans exécution vérifiable.

## Critère de fin

L'audit ne peut être déclaré terminé que lorsque les branches pertinentes sont examinées ou explicitement classées hors périmètre, les décisions sont sourcées, les tests exécutables sont rapportés avec leurs logs, les restrictions de licence sont distinguées, et les actions impossibles à exécuter sont identifiées. L'audit n'implique pas de fusionner tous les projets ni de les déclarer prêts pour la production.
