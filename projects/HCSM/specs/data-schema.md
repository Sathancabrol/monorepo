# Schéma de données — concept v0.1

**Couche :** COMPUTATIONAL SPECIFICATION  
**Statut :** `PROPOSED`  
**Source de vérité sémantique :** `ontology/hcsm-v0.1.yaml`

Ce schéma n'est pas une API. Il fixe les objets qu'une implémentation doit pouvoir sérialiser. JSON ci-dessous = exemple normatif.

---

## ConstructEstimate (objet terminal légitime)

```json
{
  "id": "hcsm:inference/estimate/att_px_t0",
  "type": "ConstructEstimate",
  "status": "PROPOSED",
  "estimates": "hcsm:knowledge/construct/attention",
  "about_person": "person:opaque:px",
  "value": 0.73,
  "scale": "unit_interval",
  "uncertainty": {
    "kind": "sd",
    "value": 0.12,
    "measurement_component": null,
    "evidence_component": 0.08,
    "inference_component": 0.09
  },
  "inferred_from": [
    "obs:cpt_omissions",
    "obs:rt_var",
    "obs:ema_focus",
    "obs:self_report"
  ],
  "measures": [
    "hcsm:knowledge/task/cpt",
    "hcsm:knowledge/measure/rt_variability",
    "hcsm:knowledge/measure/ema_focus"
  ],
  "has_context": "ctx:px_t0",
  "has_window": {
    "center": "2026-08-25T09:40:00Z",
    "half_width": 30,
    "unit": "min"
  },
  "population_reference": null,
  "alternatives": [
    {"modulator": "hcsm:knowledge/construct/fatigue", "plausibility": null},
    {"modulator": "hcsm:knowledge/construct/arousal", "plausibility": null},
    {"modulator": "motivation", "plausibility": null},
    {"modulator": "task_difficulty", "plausibility": null}
  ],
  "has_provenance": "prov:inf_att_px_t0",
  "estimate_status": "estimated"
}
```

## Refusal

```json
{
  "id": "hcsm:inference/refusal/wm_px_t0",
  "type": "Refusal",
  "insufficient_for": "hcsm:knowledge/construct/working_memory",
  "about_person": "person:opaque:px",
  "code": "NO_EVIDENCE",
  "message": "No observation with alignment exact|close for working_memory in window.",
  "has_window": {
    "center": "2026-08-25T09:40:00Z",
    "half_width": 30,
    "unit": "min"
  },
  "has_provenance": "prov:inf_wm_px_t0"
}
```

## Observation (jamais un construit)

```json
{
  "id": "obs:cpt_omissions",
  "type": "Observation",
  "observed_on": "person:opaque:px",
  "produced_by": "mi:cpt_px_t0",
  "channel": "behavioral",
  "raw_value": 0.18,
  "quality_flag": "ok",
  "alignment": "close",
  "has_context": "ctx:px_t0",
  "has_provenance": "prov:meas_cpt_px_t0"
}
```

Champ interdit : `construct_id`, `estimates`, `attention`.

## Validateur (contrat V1) — **implémenté**

Un objet est rejeté si :

1. `type = ConstructEstimate` et manque `uncertainty` ou `has_window` ou `inferred_from` ou `has_provenance` ou `has_context` ;
2. une `Observation` porte un champ d'estimation ;
3. `FunctionalProjection.status ≠ HYPOTHESIS` ;
4. la cible d'une estimation est un code diagnostique ;
5. `value` est présent sur un `Refusal` ;
6. score nu (`Attention = 0.73`) ;
7. feature digitale présentée comme construit ;
8. identifiant civil (PII) ;
9. fenêtre T0 sans `half_width` / `unit`.

**Implémentation :** `validator/` (V1 forme + V5 admissibilité).

```bash
python validator/validate.py cases/valid/mini_scenario_attention.json
python validator/validate.py --all
```

## Données personnelles

Aucun champ civil. Pas de géolocalisation précise. Pas de dossier clinique. Les exemples utilisent `person:opaque:px`.
