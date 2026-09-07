# Figure 3 — Objet Cognitive State à T0

**Statut :** `PROPOSED`  
**Message :** l'unité n'est pas un scalaire.

```mermaid
block-beta
  columns 2
  a["CONSTRUCT<br/>Attention"]:1
  b["ESTIMATION<br/>0.73"]:1
  c["UNCERTAINTY<br/>± 0.12"]:1
  d["EVIDENCE<br/>4 observations"]:1
  e["MEASURES<br/>CPT · RT var · self-report · EMA"]:1
  f["CONTEXT<br/>sleep restriction · high workload"]:1
  g["TEMPORAL WINDOW<br/>T0 ± 30 min"]:1
  h["POPULATION REFERENCE<br/>declared or none"]:1
  i["PROVENANCE<br/>agent · activity · versions"]:1
  j["ALTERNATIVE EXPLANATIONS<br/>fatigue · arousal · motivation · difficulty"]:1
```

Forme carte (lisible hors rendu block) :

```
┌──────────────────────────────────────────────┐
│  ConstructEstimate                           │
│  construct:     attention                    │
│  value:         0.73     scale: unit_interval│
│  uncertainty:   sd = 0.12                    │
│  window:        T0 ± 30 min                  │
│  evidence:      4 observations               │
│  measures:      CPT, RT var, self-report, EMA│
│  context:       sleep restriction, workload  │
│  reference:     declared or absent           │
│  provenance:    complete                     │
│  alternatives:  fatigue, arousal,            │
│                 motivation, task difficulty  │
│  status:        estimated                    │
└──────────────────────────────────────────────┘
```

Un objet auquel il manque une ligne du cadre est **invalide**, pas « partiel mais publiable ».
