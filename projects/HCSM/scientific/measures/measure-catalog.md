# Catalogue de mesures v0.1

**Couche :** EVIDENCE / KNOWLEDGE  
**Statut :** `PROPOSED` comme catalogue HCSM · les instruments cités sont établis par ailleurs

| Measure / Task | Canal | Construit ou modulateur | Alignement max v0.1 | Caveat |
|---|---|---|---|---|
| CPT (omissions, commissions) | behavioral | attention | close | tâche ≠ construit |
| RT variability | behavioral | attention | close | non spécifique |
| n-back | behavioral | working_memory | close, jamais exact par défaut | validité contestée |
| antisaccade / Stroop / flanker | behavioral | cognitive_control / attention | close | selon contraste |
| EMA focus | subjective | attention | close | auto-rapport |
| EMA sleep hours | subjective | sleep_pressure, fatigue | related / close | déclaration ≠ sommeil |
| questionnaire d'état (focus, fatigue) | subjective | selon items | close | désirabilité |
| HRV (RMSSD fenêtre) | physiological | arousal (faible), fatigue (faible) | related | spécificité basse |
| actigraphie | physiological / digital_passive | sleep_pressure | close pour sommeil, pas pour cognition | |
| EEG (feature déclarée) | neural | selon paradigme | close seulement si paradigme aligné | hors première empirie |
| paramètre DDM / RL | computational | selon modèle | related | paramètre ≠ construit Atlas |
| screen time / GPS | digital_passive | aucun construit du noyau | none | interdites comme mesure d'attention |

Toute mesure `alignment: none` peut être stockée. Elle ne fonde pas seule un `ConstructEstimate`.
