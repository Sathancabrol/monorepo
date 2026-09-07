# Figure 2 — Unités d'analyse comme voies d'évidence

**Statut :** `PROPOSED` (réinterprétation de RDoC, `ESTABLISHED`)  
**Message :** il n'y a pas d'étage « neurologique » parallèle au cognitif.

```mermaid
flowchart TB
  C["COGNITIVE CONSTRUCT<br/>knowledge graph"]
  C --> B["BIOLOGICAL evidence"]
  C --> P["PHYSIOLOGICAL evidence"]
  C --> N["NEURAL evidence"]
  B --> BEH
  P --> BEH
  N --> BEH["BEHAVIORAL data"]
  BEH --> SUB["SUBJECTIVE data"]
  SUB --> CTX["CONTEXTUAL data"]
  CTX --> LAT["LATENT ESTIMATION<br/>inference graph"]
  LAT --> FUN["FUNCTIONING<br/>ICF projection, always HYPOTHESIS"]
```

Les voies biologiques moléculaires / cellulaires sont hors v0.1 mais restent des *voies*, pas des niveaux ontologiques.

Variante compacte utilisée dans le working paper :

```mermaid
flowchart LR
  C[Construct] --> E1[behavioral]
  C --> E2[subjective]
  C --> E3[physiological]
  C --> E4[neural]
  C --> E5[contextual]
  E1 --> L[ConstructEstimate or Refusal]
  E2 --> L
  E3 --> L
  E4 --> L
  E5 --> L
  L --> F[FunctionalProjection?]
```
