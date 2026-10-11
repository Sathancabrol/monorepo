# Mémoire adaptative, decay et récupération

**Statut :** proposition d'architecture — non implémentée ni validée de bout en bout.
**Objectif :** réduire le contexte actif et le coût de stockage/relecture sans perdre la capacité de retrouver les détails, preuves et décisions d'origine.

## 1. Principe

La mémoire ne doit pas être une accumulation uniforme de texte. Elle transforme les expériences en représentations de plus en plus abstraites, reliées à leurs sources, et réactive les détails quand une tâche les rend nécessaires.

Le decay porte d'abord sur la **saillance et le niveau de détail de la mémoire active**, pas sur la destruction des données sources. Une archive peut être froide, mais reste récupérable selon les règles d'accès et de conservation.

## 2. Couches logiques

1. **Mémoire de session** — contexte temporaire, observations, hypothèses et actions en cours.
2. **Mémoire de travail** — résumés actifs, objectifs, décisions, tâches ouvertes, dépendances et prochaine action.
3. **Mémoire conceptuelle** — concepts abstraits, relations, méthodes réutilisables et modèles de situations.
4. **Mémoire des épisodes** — événements datés : recherche, choix, essais, échecs, résultats, révisions.
5. **Mémoire probante / archive** — sources brutes, fichiers, extraits, données, résultats de tests, versions et historiques.
6. **Index de récupération** — mots-clés, identifiants stables, concepts, relations, dates, chemins, empreintes et liens vers les éléments détaillés.

Ces couches sont des rôles logiques, pas nécessairement six bases séparées.

## 3. Consolidation et abstraction

À la clôture ou au checkpoint d'une tâche : regrouper les observations liées à une même question; séparer faits observés, affirmations de source, inférences, hypothèses et décisions humaines; extraire résultat, règles réutilisables, exceptions et incertitudes; créer un résumé court pointant vers les détails originaux; relier la mémoire aux projets, tâches, concepts, sources et versions; conserver les divergences significatives; éviter les doublons en enrichissant l'entrée existante avec provenance et historique.

L'abstraction doit conserver le chemin de retour : **résumé → concept → tâche/épisode → preuve → source originale**.

## 4. Heuristique de decay

Pour un souvenir m à la date t, estimer une priorité de rappel, par exemple :

`Rappel(m,t) = importance × pertinence_actuelle × confiance × provenance × fraîcheur × besoin_de_rappel`

Ce score est un outil de classement à calibrer, pas une mesure psychologique validée. Une preuve historique importante ne devient pas fausse parce qu'elle est ancienne.

La décroissance peut être représentée par `fraîcheur = exp(-λ × âge)`, avec λ propre au type d'information. À appliquer surtout aux informations volatiles : état d'une branche, disponibilité, prix, météo, statut d'une tâche. Pour une définition stable ou un résultat scientifique historique, l'âge affecte davantage le besoin de revalidation que la valeur historique.

Facteurs de maintien ou réactivation : importance explicitement déclarée par l'utilisateur; réutilisation ou rappel répété; lien à une décision, dépendance ou tâche ouverte; rareté / difficulté à reconstruire; preuve vérifiée, exigence légale ou contrainte de sécurité; contradiction ou incertitude non résolue.

Facteurs de decay : faible pertinence récente; détail redondant déjà consolidé; statut volatil devenu périmé; tâche terminée sans dépendance restante; information facilement recalculable.

**Garde-fous :** ne pas effacer automatiquement les sources primaires ou journaux d'audit; conserver les décisions importantes et leur contexte; ne jamais présenter un souvenir ancien comme état actuel sans revalidation; ne pas apprendre une préférence permanente à partir d'un seul signal ambigu; traiter les données sensibles selon des règles distinctes d'accès, rétention et suppression.

## 5. Récupération rapide

1. Recherche exacte par ID, nom de fichier, URL, commit, tâche ou concept.
2. Recherche lexicale sur titres, tags et résumés.
3. Recherche sémantique / graphe de relations si disponible.
4. Filtrage par projet, temporalité, statut, provenance et permissions.
5. Classement par pertinence, fiabilité, fraîcheur et utilité.
6. Charger d'abord les résumés; ouvrir les détails et sources seulement si nécessaire.
7. Vérifier les faits volatils avant réutilisation.
8. Consigner les souvenirs réellement utilisés et les éventuels faux positifs.

Les résultats doivent inclure identifiant, résumé, date, confiance, provenance et lien vers le détail. Une recherche sans résultat ne prouve pas l'inexistence.

## 6. Boucle d'amélioration de la mémoire

Mesurer le contexte chargé vs utile, le temps de récupération, le taux de bons souvenirs récupérés, les faux positifs et oublis, les faits périmés réutilisés, la qualité des résumés par rapport aux sources, les doublons, le coût de stockage et la capacité à reprendre une tâche interrompue.

Après chaque tâche, conserver les erreurs de récupération et corriger l'index, le résumé ou les liens. Les changements de politique de decay doivent être versionnés et évalués sur un jeu de cas; un agent ne modifie pas silencieusement les règles globales.

## 7. Intégration aux dépôts

- **Nexus OS** : orchestration des opérations de mémoire, récupération, tâches et évaluations.
- **HCSM** : contexte temporel, provenance, incertitude et distinction observation / inférence.
- **Research Engine** : mémoire par exécution de recherche, graphe de preuves, checkpoints, suffisance et conditions d'arrêt.
- **Cognitorium** : abstraction et évolution des concepts, compétences et expériences humaines.
- **Monorepo** : identifiants partagés, registre des recherches, tableaux de bord, KPI et règles de gouvernance.

Ces responsabilités sont une cible. Auditer l'implémentation existante avant de créer des mécanismes redondants.

## 8. Critères d'acceptation minimaux

- Un résumé abstrait permet de retrouver sa preuve source.
- Un état volatil périmé est signalé avant usage.
- Un détail peu actif peut être archivé puis récupéré par ID ou concept.
- Faits, hypothèses, décisions et affirmations de sources restent distincts.
- Une tâche interrompue reprend depuis son dernier checkpoint vérifié.
- Chaque opération de mémoire est traçable et testable.
- Le decay n'efface pas une preuve requise et n'altère pas l'historique.
- Les KPI mesurent qualité du rappel et coût, pas seulement le volume de données.
