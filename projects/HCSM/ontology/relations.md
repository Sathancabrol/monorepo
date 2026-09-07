# Relations — HCSM v0.1

**Statut :** `PROPOSED`

## Knowledge

| Relation | Domaine | Portée | Sens |
|---|---|---|---|
| `isA` | Construct, Subprocess, Task | même classe | taxonomie interne, usage minimal |
| `partOf` | Subprocess | Construct | composition |
| `relatedTo` | Construct | Construct | lien théorique non typé, à éviter si une relation fine existe |
| `measuredBy` | Construct | Task ou Measure | héritage Atlas / Cronbach–Meehl |
| `modulatorOf` | Construct (état) | Construct | fatigue module attention |
| `definedBy` | Construct, Task | LiteratureRecord | ancrage |
| `mapsTo` | Construct, Task, Measure | ExternalConcept | alignement |
| `requiresContext` | Construct | dimension de contexte | contrat d'admissibilité |

`isA` interne est volontairement pauvre : on ne reconstruit pas l'Atlas.

## Evidence

| Relation | Domaine | Portée | Sens |
|---|---|---|---|
| `observedOn` | Observation | Person | sujet |
| `producedBy` | Observation | MeasureInstance | instrument |
| `hasContext` | Observation, MeasureInstance | ContextRecord | situation |
| `hasWindow` | Observation, Estimate, State | TemporalWindow | temps |
| `hasProvenance` | presque tout | ProvenanceRecord | PROV |
| `wasDerivedFrom` | Observation, Signal feature | Observation ou Signal | transformation |
| `channelOf` | Observation | voie d'évidence | behavioral, … |

## Inference

| Relation | Domaine | Portée | Sens |
|---|---|---|---|
| `inferredFrom` | ConstructEstimate | Observation+ | évidence utilisée |
| `estimates` | ConstructEstimate | Construct | objet |
| `aboutPerson` | ConstructEstimate, Refusal, CognitiveState | Person | sujet |
| `hasUncertainty` | ConstructEstimate | Uncertainty | obligatoire |
| `competingWith` | AlternativeExplanation | AlternativeExplanation | concurrence |
| `explainsObservation` | AlternativeExplanation | Observation | même donnée, autre lecture |
| `modulatedBy` | ConstructEstimate | AlternativeExplanation ou Construct | influence déclarée, souvent `HYPOTHESIS` |
| `projectsTo` | ConstructEstimate | FunctionalProjection | pont ICF |
| `insufficientFor` | Refusal | Construct | refus |
| `memberOfState` | ConstructEstimate, Refusal | CognitiveState | famille T0 |
| `precedes` | CognitiveState | CognitiveState | trajectoire |

## Interdits

- `Observation estimates Construct`
- `ConstructEstimate isA Observation`
- `Construct mapsTo DiagnosticCode` comme si c'était un *exactMatch*
- toute relation `causes` en v0.1 (trop forte ; utiliser `modulatedBy` + statut)
