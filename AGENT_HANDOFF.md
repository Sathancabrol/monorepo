# Agent handoff — monorepo

> **Règle :** tout agent qui commence ici doit lire ce fichier en premier, puis les instructions du dépôt et l'état réel du code. À la fin de chaque session, il met à jour ce fichier pour que le prochain agent reprenne sans repartir de zéro.

## État de passation

- **Dernière mise à jour du handoff :** 2026-10-11
- **Dernier audit de code complet :** non confirmé
- **État d'exécution / tests :** non vérifié dans cette passation
- **Projet :** Poste de pilotage, archive et intégration des projets
- **Priorité portefeuille :** P0
- **État :** initialisation du handoff; ne pas interpréter ce fichier comme la preuve qu'un audit a été exécuté.

## Résumé du dernier état connu

L'existence du dépôt a été vérifiée; le README a été consulté lorsqu'il était disponible. Le code, les tests et les previews n'ont pas été intégralement exécutés dans cette passation. Lire les audits et décisions existants avant de refaire du travail.

## Instruction au prochain agent

Lire docs/AGENT_CONTINUITY.md et docs/AUDIT_AUTOMATION.md. Valider le script d'audit, puis intégrer une file persistante de tâches, la recherche ciblée, les preuves, les résultats CI et la vue roadmap. Ne pas déclarer l'agent opérationnel avant exécution vérifiée.

### Procédure obligatoire

1. Lire ce fichier, le README, les instructions locales (par exemple `AGENTS.md`, `CONTRIBUTING.md`) et les derniers audits/notes de décision disponibles.
2. Examiner le statut Git, les commits récents, les branches pertinentes, les PR/issues et les résultats CI accessibles.
3. Reconstituer ce qui est fait, en cours, bloqué, proposé et réellement vérifié. La présence de code ou de documentation ne prouve pas qu'une fonctionnalité fonctionne.
4. Identifier le besoin prioritaire à partir de la demande utilisateur la plus récente, des objectifs du projet, des dépendances et des preuves. Si le besoin est ambigu, faire un audit ciblé plutôt qu'une refonte arbitraire.
5. Faire une seule unité de travail utile et limitée. Préserver les modifications existantes; travailler sur une branche dédiée si une modification de code est nécessaire.
6. Exécuter les vérifications pertinentes et consigner les commandes, le commit testé et les résultats. Si rien n'a été exécuté, le dire explicitement.
7. Mettre à jour ce fichier avant de terminer : état, audit, tests, décisions, blocages et prochaine action. Ajouter une entrée au journal sans effacer les incertitudes précédentes.

## Prochaine action

- [ ] Lire les audits et décisions antérieurs.
- [ ] Établir l'état réel du code et des tests.
- [ ] Choisir et justifier la prochaine tâche prioritaire.
- [ ] Mettre à jour ce handoff avec preuves et résultats.

## Journal des sessions

### 2026-10-11 — Initialisation du handoff
- Ajout d'un point d'entrée commun pour les agents.
- Aucun audit complet ni test d'exécution n'est revendiqué.
- Prochaine étape : lire les documents du projet et produire un état vérifié.

## Format des mises à jour futures

À chaque session, ajouter : date; besoin traité; fichiers/branches/commits touchés; périmètre de l'audit; commandes de tests et résultats; décisions, sources et incertitudes; blocages/approbations; prochaine action et critère de réussite.

## Garde-fous

- Ne jamais inventer un résultat d'audit, un test réussi ou un état de déploiement.
- Ne pas supprimer ou écraser du travail existant sans comparaison et autorisation.
- Ne pas fusionner, déployer, publier, supprimer de branche ou engager une dépense sans autorisation explicite.
- Séparer les faits observés, les hypothèses et les recommandations.
- Pour la recherche externe, conserver URL, date, provenance et lien avec le besoin; respecter les licences et limites d'accès.


## Nouvelle orientation utilisateur — mémoire adaptative et recherches itératives (2026-10-11)

Documents préparés sur cette branche :
- `docs/MEMOIRE_ADAPTATIVE_ET_DECAY.md` : couches logiques de mémoire, consolidation, abstraction, decay, récupération rapide, métriques et critères d'acceptation.
- `templates/research/RECHERCHE.md` : gabarit humain/IA par question de recherche, avec état de processus, sources, preuves, réponse provisoire, boucle d'amélioration et consolidation mémoire.

Ces documents sont des propositions d'architecture, pas la preuve d'une implémentation opérationnelle.

### Prochaine action recommandée
1. Auditer les mécanismes réels déjà présents dans Nexus OS, HCSM et Research Engine avant de développer des doublons.
2. Faire un mapping explicite entre les capacités existantes et le modèle de mémoire adaptative.
3. Choisir un prototype vertical minimal : une recherche possède un dossier et un `RECHERCHE.md`, des checkpoints persistants, des preuves sourcées et une boucle d'évaluation.
4. Tester récupération après interruption, détection d'information périmée, retour du résumé vers la preuve originale et mesure du contexte chargé.
5. Ne pas implémenter le decay destructif; commencer par un score de rappel, une abstraction versionnée et une archive réversible.

### Critère de réussite
Un agent qui reprend une recherche doit retrouver la bonne question, son état vérifié, les preuves et la prochaine action depuis le dossier de recherche, sans charger toutes les données historiques ni recommencer l'audit global.


## Session 2026-10-11 — Automatisation transversale

- Ajout de `docs/CROSS_PROJECT_AUTOMATION_STANDARD.md` : cycle RECALL → DISCOVER → PLAN → EXECUTE → VERIFY → DELIVER → HANDOFF, règles d'entrée de session, inventaire des consignes, gestion des conflits, niveaux d'autonomie et preuves attendues.
- Mise à jour de `AGENTS.md` : récupération du contexte et des audits valides, recherche avant question, tests et mise à jour du handoff.
- Mise à jour de `scripts/project_audit/audit_gaps.py` : découverte prioritaire des fichiers de consignes, politiques, standards, handoffs et décisions.
- Mise à jour de `.github/workflows/project-audit.yml` : validation syntaxique Python et JSON avant exécution de l'audit.
- Mise à jour de `docs/AUDIT_AUTOMATION.md` : étapes de revue des règles et de continuité.
- Statut : changements sur la branche `feat/gap-driven-audit-2026-10-11`, non fusionnés. Le workflow et les tests n'ont pas encore été exécutés; aucune validation d'exécution n'est revendiquée.
- Recherche GitHub sur les dépôts configurés : aucun résultat identifié pour « JEV ». Le système visé reste à identifier, sans supposer ce que l'acronyme signifie.

### Prochaine action
1. Exécuter la validation syntaxique et les tests sur la branche, corriger les erreurs éventuelles.
2. Lire et comparer les consignes effectives sur les dépôts/branches prioritaires et produire un registre avec source, SHA, portée, conflit et statut de revue.
3. Auditer Nexus OS, Research Engine et HCSM avant de développer une file de tâches persistante ou un agent de continuité.
4. Vérifier les permissions et l'exécution GitHub Actions avant toute fusion.


### Complément de session — règles de plusieurs projets
- Ajout de `docs/PROJECT_RULES_INVENTORY.md`, avec sources et SHA pour les premières règles vérifiées de Watchtower, Research Engine, HCSM, État de l'art psychologie, COGNITORIUM et Language-decoder.
- Découverte importante : `proto-cognitorium` et `animation-chronos` ont `AGENTS.md` et `AGENT_HANDOFF.md` sur `chore/agent-handoff-2026-10-11`, même si `README.md` n'a pas été trouvé sur `main`. Cela confirme qu'il faut examiner les branches non principales avant de conclure qu'une règle ou un projet manque.
- Ajout de `tests/test_project_audit_gaps.py` : tests prévus pour pagination, erreur API et JSON d'état invalide. Le workflow est configuré pour les exécuter, mais ils n'ont pas encore été exécutés dans cette session.
- Le workflow inclut maintenant py_compile, validation JSON et tests unitaires avant le scan; aucune exécution CI réussie n'est revendiquée.

## Session 2026-10-12 — Durcissement ciblé de l'audit

- Besoin traité : confronter l'audit récent à l'état Git actuel et corriger rapidement les risques de faux état.
- Branche locale : `codex/audit-hardening-2026-10-12`, basée sur `origin/feat/gap-driven-audit-2026-10-11` au SHA `370801b`.
- Le lancement manuel du workflow vérifie désormais la ref sélectionnée; la publication des rapports reste limitée à `main`.
- Les erreurs de métadonnées ou de pagination GitHub conservent le dernier inventaire connu avec un état d'erreur explicite, au lieu d'effacer des branches ou de les marquer implicitement absentes.
- L'audit portefeuille pagine désormais toutes les branches et expose dans ses sorties humaines la complétude de l'inventaire, les erreurs partielles et la ref/SHA génératrice.
- Vérifications effectuées : revue statique du diff, statut Git, SHA local, `git ls-remote` des branches d'audit GitHub, compilation Python, validation JSON, `git diff --check` et 7 tests unitaires réussis.
- Commande automatisée : `python -m py_compile ...`, `python -m json.tool ...`, puis `python -m unittest discover -s tests -p 'test_project_audit*.py' -v`.
- Incident corrigé pendant la vérification : le test de pagination cherchait naïvement `page=1`, qui correspondait aussi à `per_page=100` et bouclait; il analyse maintenant le paramètre d'URL.
- Build applicatif : non exécuté car hors périmètre des scripts d'audit.
- Publication contrôlée : commits `f6d0dc0` et `d78a3bc` poussés uniquement sur `codex/audit-hardening-2026-10-12`.
- Validation distante : GitHub Actions `Project portfolio audit`, exécution `38191715595`, terminée avec succès sur `d78a3bc`.
- Vérification de non-régression Git : `main` reste à `a18938d`; les branches `feat/gap-driven-audit-2026-10-11` (`370801b`) et `feat/automated-project-audit-2026-10-11` (`d97f4b4`) sont inchangées.
- Prochaine action : revue humaine du diff et des permissions `contents: write`; aucune PR ni fusion n'a été créée.
