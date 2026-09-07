# Ontologie HCSM v0.1

**Statut :** `PROPOSED`  
**IRI de version :** `https://github.com/Sathancabrol/HCSM/ontology/0.1.0`  
**Fichier canonique :** [`hcsm-v0.1.yaml`](hcsm-v0.1.yaml)

HCSM n'est pas une ontologie de la cognition. C'est une ontologie de **l'état cognitif estimé** : construits alignés, observations, estimations, refus, contexte, temps, provenance, projections de fonctionnement.

## Fichiers

| Fichier | Contenu |
|---|---|
| `hcsm-v0.1.yaml` | Spécification machine (classes, propriétés, contraintes, alignements) |
| `entities.md` | Classes, en langage naturel |
| `relations.md` | Propriétés d'objet et de donnée |
| `namespaces.md` | Préfixes et IRI externes |

## Axe `graph`

Chaque classe est assignée à un graphe :

- `knowledge` — ce que la science sait
- `evidence` — ce qui a été observé
- `inference` — ce qui est conclu ou refusé
- `cross` — temps, identifiants, provenance (utilisés par plusieurs graphes)

Une instance ne change pas de graphe. Un pont se fait par une relation typée, jamais par sous-classement trans-graphe.

## Règle d'or

```
Observation  ⊄  Construct
ConstructEstimate  requires  Uncertainty  ∧  TemporalWindow  ∧  evidence
Diagnosis  ∉  HCSM
NeurologicalState  ∉  HCSM
```

## Versions

Le fichier s'appelle `v0.1` à dessein. Un ajout de construit du noyau, une relation nouvelle ou un changement de contrainte majeure ⇒ `v0.2`.
