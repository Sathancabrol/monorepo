# API conceptuelle — Cognition Hub

**Couche :** COMPUTATIONAL SPECIFICATION  
**Statut :** `PROPOSED` · pas d'implémentation  
**Date :** 2026-08-25

Cognition Hub est le système qui instancie HCSM. L'API ci-dessous décrit des *ressources*, pas des routes définitives.

---

## Ressources

| Ressource | Graphe | Mutabilité |
|---|---|---|
| `/constructs` | knowledge | versionnée avec l'ontologie |
| `/measures` `/tasks` | knowledge | versionnée |
| `/people/{opaque}` | evidence | création hors bande, pas de GET identifiant |
| `/observations` | evidence | append-only |
| `/contexts` | evidence | append-only |
| `/states` | inference | produite par inférence, jamais PATCH de `value` |
| `/estimates` | inference | idem |
| `/refusals` | inference | idem |
| `/trajectories` | inference | vue sur `/states` |
| `/projections` | inference | toujours `HYPOTHESIS` |

Append-only : on n'efface pas une observation ; on en ajoute une qui la déprécie, avec provenance.

## Opérations

### `POST /infer`

Entrée : `person`, `window`, `constructs[]` (sous-ensemble du noyau), `ontology_version`, `estimator_version`.

Sortie : `CognitiveState` = liste d'`ConstructEstimate` et de `Refusal`.

Interdit en sortie : un scalaire nu, un diagnostic, un score global.

### `POST /observations`

Entrée : objet conforme au schéma, `alignment` calculé côté serveur à partir du knowledge graph, pas fourni par le client comme vérité.

### `GET /states/{id}`

Retourne l'état et sa provenance. Ne retourne pas d'identité civile.

## Non-objectifs d'API

- streaming d'« état cognitif temps réel » ;
- endpoint `/iq` ou `/diagnosis` ;
- correction automatique d'un score par le sommeil ;
- écriture depuis Cognitorium dans l'inference graph.

## Auth et éthique (rappel)

Hors v0.1. Toute implémentation future : minimisation, consentement, pas de décision automatique, journal d'accès.
