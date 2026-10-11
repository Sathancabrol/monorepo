# Matrice de réutilisation — audit transversal 2026-10-11

**Branche d'audit :** `feat/automated-project-audit-2026-10-11`  
**Principe :** inventaire statique fondé sur les chemins/références GitHub consultés. Aucun statut « testé avec succès » n'est attribué sans exécution vérifiable.

## Légende

- **Réutilisable comme base** : architecture ou code candidat ; ne signifie pas prêt à intégrer.
- **Adapter** : logique intéressante, contrat ou interface à normaliser.
- **Bloqué droits** : ne pas redistribuer/porter avant clarification des droits.
- **À tester** : présence de code/tests connue, résultats d'exécution non vérifiés.
- **Archive** : garder comme provenance/historique, pas comme runtime ou source de vérité par défaut.

## Matrice

| Actif / origine | Fonction principale | Valeur potentielle | Risque / statut de preuve | Décision provisoire | Priorité |
|---|---|---|---|---|---|
| `monorepo:feat/gap-driven-audit-2026-10-11` | Découverte de branches, arbres, écarts, index portfolio | Automatise la découverte des angles morts et le suivi des SHA | Arbres limités par exécution ; ne fait pas la revue sémantique ; rapport portfolio paginé différemment | **Réutilisable comme base**, ajouter tests sur fixtures et validation PR isolée | P0 |
| `monorepo:feat/tool-data-catalog-2026-10` | Registre outils/modules et graphe d'intégration | Catalogue partagé, évite les registres concurrents | Divergent de main ; schémas à réconcilier | **Adapter** et fusionner conceptuellement avec le registre créatif | P0 |
| `monorepo:feat/creative-toolchain-registry` | Registre d'outils créatifs, validateur et tests | Exemple de catalogue contrôlé par schéma | Résultats de tests non exécutés ici | **Réutiliser le motif**, pas un deuxième catalogue indépendant | P1 |
| `monorepo:arena/01a08385-monorepo` | Nexus OS, runtime agentique, mémoire JSON, API/UI | Agents, routage modèles, outils/MCP, tâches et mémoire de faits/décisions/leçons | Comparaison statique ; sécurité, permissions et tests non validés | **Candidat runtime**, auditer les capacités et limites avant choix | P0 |
| `monorepo:arena/0034230e-monorepo` | Carré d'As : contrats, admissibilité, cycle de travail, dossiers Markdown | Workflow explicite plan → recherche → production → revue → vérification → mémoire | Recouvrement avec Nexus OS ; divergence Git | **Candidat orchestrateur/contrat**, éviter la fusion en bloc | P0 |
| `monorepo:arena/00f44a26-monorepo/projects/laplace` | Agent Discord, politique, mémoire SQLite | Tests dédiés et contrat Python >=3.11 | Licence déclarée **UNLICENSED** ; dépendances OpenAI/Discord/SQLite | **Bloqué droits** avant portage ou redistribution | P0 |
| `monorepo:arena/0d411b29-monorepo/projects/bone` | Bot/persona, LLM, packs de permissions Discord | Modèle de permissions par capacités et tests dédiés | Licence racine non établie dans la référence consultée ; audit moindre privilège requis | **À auditer**, réutiliser les idées de permission seulement après tests/droits | P2 |
| `ETAT-DE-LART-PSYCHOLOGIE:arena/01a04f7b` (Uranus) | Agent chercheur multi-bases et 11 compétences | Fixtures hors-ligne, normalisation, PRISMA, DOI, déduplication, rapport et tests déclarés | Licence racine non établie ; tests non exécutés ; Trust Factor heuristique | **Candidat de haute valeur** pour Research Engine ; corriger/qualifier les métriques et tester | P0 |
| `Sathancabrol/reaserch-engine:main` | Runs reprenables, EvidenceGraph, checkpoints JSON | Modèle d'épisodes/recherche et liens preuve → affirmation | Deux tests en échec mentionnés dans un audit historique, pas revalidés | **Conserver comme graphe de preuves canonique candidat**, rerun tests | P0 |
| `Language-decoder:arena/01a05471-language-decoder` | Modèle de dynamique humaine, interface/CLI et tests | Temps, rétention/réactivation/transfert, schéma explicite | Tests présents mais non exécutés | **Adapter** comme modèle temporel ; comparer son schéma à HCSM | P1 |
| `HCSM:main` | Schéma/validation de contexte humain et provenance | Contrat commun possible pour contexte, temporalité et incertitude | Pas un moteur d'inférence complet ; tests non exécutés | **Contrat de référence candidat**, tests de compatibilité requis | P0 |
| `proto-cognitorium:arena/01a08342` | Prototype Cognitorium + sondes runtime | Harnais de non-régression et diagnostic des vues/ROME/données | Une sonde force le code de sortie 0 ; README signale des assertions manquantes ; résultats historiques non réexécutés | **Réutiliser après correction du faux-vert** | P0 |
| `watchtower:arena/dec9cd88-watchtower` | Watchtower INTEL, Atlas Thau/Frontignan, veille et chantiers | Données territoriales, import CSV, imprévus TP, tests dédiés | Divergence et provenance/licence des données à contrôler | **Candidat canonique Watchtower/Atlas**, vérifier données et tests | P0 |
| `watchtower:arena/01a072e1-watchtower` | Audit Watchtower, vue territoire, charge mentale, UI volant, parité sources | Documentation approfondie, tests JS, spécification fonctionnelle | 43 commits en avance et 10 en retard ; écart important avec main | **Revue sémantique prioritaire**, sélectionner les apports fichier par fichier | P0 |
| `monorepo:arena/01a08203-monorepo/projects/frontignan` | Atlas Frontignan, communes Thau, graphes, visuels | Données et vues territoriales à réconcilier avec Watchtower | 1 commit en avance, 27 en retard ; fraîcheur/licences de données à vérifier | **Archive/ressource**, pas une source concurrente sans versionnement des données | P1 |
| `COGNITORIUM:watchtower/osint-workbench-v0.1` | Registre sources, observations, dossiers, relations et statuts épistémiques | Bonne base de modèle OSINT et validation humaine | Absent aux chemins `main` vérifiés ; licence/dépendances et portage à auditer | **Prototype à porter sélectivement** dans Watchtower | P0 |
| `monorepo:arena/171a1f38-monorepo` | Audit historique, drift, mémoire et inventaires de branches | Source de décisions passées et de contexte de projet | Snapshots potentiellement périmés | **Archive consultable**, revalider chaque constat | P1 |
| `monorepo:arena/15c77b59-monorepo` | Archives de conversations/outils Carré d'As | Traçabilité des décisions et pistes de travail | Risque de bruit, secrets ou contexte périmé dans les traces brutes | **Archive indexée**, résumé avec provenance avant rappel actif | P1 |
| `monorepo:feat/final-interface-skeleton-2026-10-07` | Shell d'interface et registre des slots | Preview intégrée, UI modulaire | Divergence et recouvrement possible avec l'interface Carré d'As | **Candidat shell**, tester les slots avant choix final | P1 |
| `monorepo:feat/mobile-ar-fastpath-2026-10-11` | Audit gap-driven et dossier HUD mobile | Base de suivi et intégration AR progressive | HUD tiers non testé sur téléphone ; pas de validation runtime | **Conserver comme dossier/branche**, tester séparément l'appareil et le code tiers | P2 |

## Décision d'architecture recommandée à ce stade

### Ne pas fusionner les runtimes prématurément

Faire un prototype de compatibilité autour d'un contrat commun et mesurer les fonctions suivantes pour Nexus OS, Carré d'As et Laplace : permissions, isolation des outils, reprise, persistance, historique, appels MCP, routage LLM, tests et fonctionnement hors-ligne. Laplace reste bloqué par sa déclaration de licence tant que les droits ne sont pas clarifiés.

### Garder un graphe de preuves canonique

Comparer Uranus et Research Engine pour éviter deux bases de publications et deux moteurs de recherche concurrents. Uranus peut fournir les compétences de recherche et la validation de corpus ; Research Engine peut fournir les runs reprenables et le graphe de preuves. Cette division reste une hypothèse à valider par tests d'intégration.

### Mémoire adaptative par adaptateurs

Ne pas construire un nouveau moteur de mémoire maintenant. Relier les stockages existants via un schéma d'adaptation : identifiant stable, type, provenance, date d'observation, période de validité, statut épistémique, liens vers tâche/run/projet, historique de correction et paramètres de rappel. Le decay diminue la priorité, pas la disponibilité de la preuve.

### Règles de validation

- Une branche comparée n'est pas automatiquement revue fichier par fichier.
- Un fichier de test présent ne prouve pas qu'il passe.
- Un score heuristique ne vaut pas probabilité calibrée.
- Le code MIT ne confère pas automatiquement de droits sur les jeux de données tiers.
- Une donnée, une estimation, une hypothèse et une simulation doivent être visuellement distinguées dans les interfaces.

## Tâches bloquantes pour clore l'audit

1. Exécuter les tests/builds dans un clone local ou CI accessible et conserver les logs.
2. Comparer les schémas HCSM / Language-decoder / Carré d'As et définir les adaptateurs.
3. Comparer fichier par fichier les copies OSINT Workbench et Watchtower INTEL.
4. Clarifier les licences d'Uranus, Bone et les données Watchtower/Atlas ; ne pas porter Laplace tant que `UNLICENSED` n'est pas levé.
5. Ajouter des assertions bloquantes aux sondes proto-Cognitorium et tests fixtures du scanner gap-driven.
6. Choisir le runtime après matrice fonctionnelle/testée ; ne pas fusionner toutes les branches.
