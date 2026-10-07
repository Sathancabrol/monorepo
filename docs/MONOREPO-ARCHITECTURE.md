# Architecture cible du monorepo

## Objectif

Le monorepo devient un **shell d'intégration modulaire** : les projets historiques restent autonomes, mais leurs capacités sont exposées par des contrats communs.

Le principe n'est plus :

`projet → copie de code → UI`

mais :

`source → adapter → contrat → capacité → module → UI / agent`

## Couches

```
apps/
  shell/                 Interface unifiée (FastAPI/Jinja aujourd'hui)

core/
  contracts/             Schémas canoniques et contrats d'échange
  registry/              Registre des modules/capacités
  events/                Événements inter-modules
  provenance/            Source, licence, confiance, temporalité

modules/
  gis/                   Cartographie, couches, 3D, géospatial
  territory/             Territoire, population, acteurs, projets
  chantier/              BTP/TP, documents, tâches, planning, risques
  research/              Recherche, sources, preuves, claims
  cognition/             HCSM, connaissances, compétences
  learning/              Learning Engine, simulations pédagogiques
  temporal/              Chronos, chronologie, phasage
  agents/                Orchestration et agents spécialisés
  language/              Décodage / extraction linguistique

adapters/
  watchtower/
  cognitorium/
  research-engine/
  hcsm/
  frontignan/
  chronos/
  chantier-corpus/

data/
  raw/                    Sources brutes, idéalement hors Git si sensibles
  normalized/             Données normalisées
  indexes/                Index/recherches
  registries/              Catalogues machine-readable

projects/
  ...                     Projets sources/importés conservés tels quels
```

## Règle de migration

On ne déplace pas tout le code d'un coup.

### Phase A — maintenant
Créer les contrats, manifestes et adaptateurs logiques. Aucun doublon de code.

### Phase B
Extraire les fonctions réellement partagées dans `modules/` ou `core/`.

### Phase C
Remplacer progressivement les anciennes UI par les modules communs.

### Phase D
Les projets sources deviennent des références/versionnées, pas des copies concurrentes.

## Contrat d'un module

Chaque module expose :

- identité et version
- domaine
- source de référence
- capacités
- entrées
- sorties
- événements produits/consommés
- dépendances
- statut
- licence/provenance
- point d'intégration

Un module peut être :
- **embedded** : exécuté dans le shell
- **service** : API/processus séparé
- **library** : bibliothèque partagée
- **adapter** : pont vers un projet existant
- **external** : outil externe référencé

## Flux de données canonique

```
SOURCE
  ↓
ADAPTER
  ↓
CANONICAL RECORD
  ↓
CAPABILITY
  ↓
MODULE
  ├──→ MAP
  ├──→ GRAPH
  ├──→ DOSSIER
  ├──→ SIMULATION
  └──→ AGENT
```

## Exemple transversal

```
CCTP
 ↓
chantier adapter
 ↓
Document / Task / Constraint
 ↓
GIS ─────────────→ localisation
 ↓
Research ────────→ preuve/source
 ↓
Cognition ───────→ compétence
 ↓
Learning ────────→ scénario d'entraînement
 ↓
Temporal ────────→ planning / chronologie
 ↓
Agent ───────────→ orchestration
```

## Ce que le shell doit savoir

Le shell ne doit pas connaître le code interne de Watchtower, Cognitorium ou Research Engine.

Il doit seulement savoir :

1. quels modules sont disponibles ;
2. quelles capacités ils exposent ;
3. quels contrats ils acceptent ;
4. comment les appeler ;
5. quelles données ils produisent ;
6. d'où viennent ces données.

Cela rend l'ensemble remplaçable et extensible.
