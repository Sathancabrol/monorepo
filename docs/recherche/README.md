# Dossier de recherche — à remettre à un agent (ArenaAI ou autre)

**Objet :** préparer la **réorganisation complète de l'application** en confiant à un agent de recherche une mission cadrée : chercher sources, outils et systèmes existants, les vérifier, les comparer à ce que le projet possède déjà, et produire des décisions.

## Contenu

| Fichier | Rôle | À qui |
|---|---|---|
| **`00-BRIEF-ARENA-RECHERCHE.md`** | **LE FICHIER À DONNER.** Brief auto-suffisant : vision, état réel des 9 dépôts, acquis à ne pas refaire, matrice de 80 domaines, 10 chantiers P0 détaillés, méthode de recherche, format de sortie imposé, règles de conduite | L'agent de recherche |
| `01-PROMPT-A-COLLER.md` | Prompt prêt à coller (version courte si l'agent a le dépôt, version longue sinon) + comment vérifier que le travail est bien fait | L'utilisateur |
| `02-MATRICE-DOMAINES.csv` | Le tableau : 80 domaines (`D01`→`D80`), priorités P0→P3, existant, questions de recherche, pistes à vérifier, décision attendue, critère de succès | Outil de pilotage / agent |
| `03-ENRICHISSEMENTS-ET-ARBITRAGES.md` | Analyse de la discussion initiale : ce qui est solide, les 7 corrections à apporter, les 12 domaines manquants, ce qu'il faudrait prendre pour le monorepo, ce qui est écarté, le premier palier démontrable | L'utilisateur (décision) |

## Utilisation en trois étapes

1. Ouvrir une session avec accès **web + GitHub**, ouvrir le dépôt `Sathancabrol/monorepo`.
2. Coller le prompt de `01-PROMPT-A-COLLER.md`.
3. Vérifier la sortie avec les trois signaux en fin de `01-PROMPT-A-COLLER.md` (contredit le brief quand il a tort · écrit « inconnu » · produit des décisions et des écartés).

## Rappel — ce que ce dossier n'est pas

- Ce n'est pas une liste d'outils validée : les « pistes à vérifier » sont des points de départ issus de connaissances générales, **à confirmer par l'agent** (licence, activité, performance, licence, coût).
- Ce n'est pas une décision : les arbitrages de `03-…` sont des **propositions** argumentées.
- Ce n'est pas figé : toute information contredite par le dépôt doit être corrigée dans le dépôt.

*Créé le 2026-10-07. Vérifications en ligne effectuées à cette date via l'API GitHub (`gh api`) pour une trentaine de projets cités (licence, étoiles, dernier commit, archivage).*
