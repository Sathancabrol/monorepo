# Architecture modulaire du monorepo

Le monorepo devient le shell d'integration. Les projets sources restent autonomes et exposent progressivement leurs capacites via des contrats communs.

## Couches

- `apps/` : interfaces et shells
- `core/` : contrats, registre, provenance, evenements
- `modules/` : capacites fonctionnelles
- `adapters/` : ponts vers les projets existants
- `data/` : donnees brutes, normalisees et registres
- `projects/` : projets sources/importes, conserves tels quels pendant la migration

## Flux

`SOURCE -> ADAPTER -> CANONICAL DATA -> CAPABILITY -> MODULE -> UI / AGENT`

## Modules cibles

GIS, Territoire, Chantier BTP/TP, Recherche/Preuves, Cognition/Connaissance, Learning Engine, Temporal/Chronos, Agents/Orchestration, Language Decoder.

## Regle de migration

1. Referencer l'existant.
2. Ajouter un adaptateur.
3. Normaliser les donnees.
4. Extraire uniquement le code reellement partage.
5. Remplacer progressivement les anciennes integrations.

Aucun gros deplacement de code n'est effectue dans cette etape : l'objectif est de stabiliser l'architecture avant de migrer les briques.