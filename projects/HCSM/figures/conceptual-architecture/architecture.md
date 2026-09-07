# Figure 1 — Architecture conceptuelle

**Statut :** `PROPOSED`  
**Message :** HCSM n'est pas une nouvelle science de la cognition. C'est la couche qui relie connaissance, mesure et inférence personnelle.

```mermaid
flowchart TB
  subgraph EXISTING["Science existante"]
    K["Knowledge<br/>Cognitive Atlas · RDoC · HPO · ICF"]
    M["Measurement<br/>tests · EEG · HRV · questionnaires · comportement"]
    F["Function<br/>ICF capacité / performance / participation"]
  end

  subgraph HCSM["HCSM / Cognition Hub"]
    direction TB
    K2["Knowledge"] --> ME["Measurement"]
    ME --> INF["Inference"]
    INF --> T0["State T0"]
    T0 --> CX["Context"]
    CX --> FN["Function"]
    FN --> TR["Trajectory"]
  end

  K --> K2
  M --> ME
  F --> FN
```

## Lecture

- Haut : cadres que HCSM **n'absorbe pas**.
- Bas : chaîne que HCSM **ajoute** comme objet computationnel.
- La flèche critique est `Measurement → Inference`, pas `Measurement → Score`.

## Ce que la figure interdit de lire

- HCSM au-dessus de RDoC comme un remplaçant.
- Function comme un simple export de T0.
