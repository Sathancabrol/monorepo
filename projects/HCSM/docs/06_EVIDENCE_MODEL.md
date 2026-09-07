# 06 — Modèle d'évidence

**Statut du document :** `PROPOSED`  
**Couche :** EVIDENCE  
**Version :** 0.1.0 · 2026-08-25

---

## 1. Définition

Une évidence HCSM est une **observation typée, provenancée, contextualisée et temporellement située**, qui *peut* entrer dans une inférence. Ce n'est pas une preuve au sens juridique, ni un résultat statistique.

```
Measure  --instantiated as-->  MeasureInstance  --yields-->  Observation
                                                      │
                                                      ├── ContextRecord
                                                      ├── ProvenanceRecord
                                                      └── TemporalWindow
```

## 2. Types d'évidence (voies)

Alignés sur les unités d'analyse RDoC, restreints à ce que v0.1 peut traiter.

| Voie | Exemples | Qualité typique | Risque typique |
|---|---|---|---|
| `behavioral` | CPT, n-back, RT, erreurs | haute pour la tâche, basse pour le construit | réification de la tâche |
| `subjective` | Likert, EMA, interview | accès à l'expérience | biais de rappel, désirabilité |
| `physiological` | HRV, cortisol, actigraphie | objective, continue | spécificité de construit faible |
| `neural` | EEG, pupillométrie | proche des circuits | coût, labo, N faible |
| `contextual` | sommeil déclaré, charge, lieu | indispensable à l'interprétation | souvent manquant |
| `computational` | paramètres de modèle (RL, drift-diffusion) | théoriquement ancré | dépendance au modèle |
| `digital_passive` | GPS, écran, logs | écologique, dense | validité de construit fragile |

Les voies `genes`, `molecules`, `cells` de RDoC sont **hors v0.1**. Elles peuvent exister plus tard comme voies, jamais comme étages.

## 3. Qualité d'une observation

Chaque `Observation` porte un bloc qualité, même partiel :

| Champ | Sens |
|---|---|
| `raw_value` / `normalized_value` | ne pas écraser le brut |
| `instrument_id` | mesure ontologique |
| `reliability_ref` | fidélité connue de l'instrument, si elle existe |
| `missingness` | donnée manquante, imputée, refusée |
| `quality_flag` | ok / degraded / unusable |
| `alignment` | `measuredBy` du knowledge graph : exact, close, none |

Une observation `alignment: none` peut rester dans l'evidence graph. Elle **ne peut pas** fonder seule un `ConstructEstimate`.

## 4. Multiplicité et non-additivité

Quatre observations d'attention ne font pas automatiquement une meilleure attention. Règles :

1. des observations de la **même voie** et du **même instrument** se combinent (répétitions, fidélité) ;
2. des observations de **voies différentes** se confrontent (convergence / divergence) ;
3. on n'additionne pas un EEG et un Likert ;
4. la taille de `evidence_ids` n'est pas un score de confiance. Quatre mesures mal alignées pèsent moins qu'une mesure bien alignée.

## 5. Features digitales

Une feature extraite d'un smartphone est une `Observation` de voie `digital_passive`. Elle n'est **jamais** un `Construct`.

Interdit :

```
screen_time → attention = low
home_time → anhedonia = high
```

Autorisé :

```
screen_time  [digital_passive, provenance=app_v3, window=T0±30m]
    └── peut entrer comme évidence faible d'un état d'éveil
        └── concurrence : ennui, travail sur écran, insomnie, enfant malade
```

## 6. Données manquantes

Trois statuts, jamais un zéro silencieux :

- `not_collected`
- `collected_unusable`
- `refused_by_person`

Le moteur d'inférence voit ces statuts. Il ne les impute pas en v0.1.

## 7. Lien avec le knowledge graph

Une mesure entre dans HCSM seulement si elle est une instance d'une `Measure` ontologique, elle-même liée à au moins un `Construct` par `measuredBy` ou déclarée `modulatorOf`.

Sinon elle reste hors modèle, éventuellement dans un bac `untyped_observation` qui n'alimente pas l'inférence.

## 8. Mini-contrat pour une observation valide

```
Observation is valid iff
  person_id opaque
  AND timestamp XOR window
  AND measure_id in ontology
  AND provenance.agent AND provenance.activity
  AND raw_value XOR missingness
  AND no construct_id on the observation itself
```
