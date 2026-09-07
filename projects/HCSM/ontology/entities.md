# Entités — HCSM v0.1

**Statut :** `PROPOSED`

Les identifiants ci-dessous sont des slugs locaux. Le fichier canonique reste `hcsm-v0.1.yaml`.

---

## Cross-cutting

### `Entity`
Racine. Champs communs : `id`, `label`, `description`, `status` (`ESTABLISHED|SUPPORTED|PROPOSED|HYPOTHESIS|OPEN QUESTION`), `version`.

### `ProvenanceRecord` · graph: `cross`
Profil PROV-O : `entity`, `activity`, `agent`, `started_at`, `ended_at`, `derived_from[]`, `used[]`.

### `TimePoint` · graph: `cross`
Instant avec fuseau. Centre potentiel d'une fenêtre.

### `TemporalWindow` · graph: `cross`
`center`, `half_width`, `unit` (`s|min|h|day`). Obligatoire sur toute estimation.

---

## Knowledge

### `Construct`
Construit latent. N'est pas une tâche, pas une personne, pas un diagnostic.  
Alignements : Atlas, RDoC, éventuellement ICF / HPO.  
`requiresContext[]`, `mandatoryAlternatives[]`, `typicalTimescale`.

### `Subprocess`
`partOf` un `Construct`. Ex. attention sélective, soutenue, divisée.

### `Theory`
Cadre qui relie des construits (ex. Baddeley working memory). Statut épistémique obligatoire.

### `Task`
Paradigme expérimental ou clinique (CPT, Stroop, n-back). Alignement CogPO / Atlas task souhaité.

### `Measure`
Instrument ou score dérivé, y compris feature digitale typée. Toujours liée à une `Task` ou déclarée `modulatorOf`.

### `LiteratureRecord`
DOI, citation, rôle (`defines`, `supports`, `challenges`).

### `ExternalConcept`
Proxy : `source`, `source_iri`, `match` (`exact|close|related`).

---

## Evidence

### `Person`
Identifiant opaque. Pas de données civiles dans HCSM.

### `Observation`
Valeur observée. Interdiction : champ `construct_id`.  
`measure_id`, `raw_value?`, `normalized_value?`, `missingness?`, `channel`, `quality_flag`, `alignment`, `timestamp` ou `window`.

### `MeasureInstance`
Application d'une `Measure` à une `Person`. Groupe éventuellement plusieurs `Observation` (items).

### `Signal`
Série temporelle (EEG, HRV, actigraphie). Les features extraites deviennent des `Observation` dérivées, avec `wasDerivedFrom`.

### `ContextRecord`
Dimensions : `task`, `environment`, `somatic`, `occupational`, `social`, `temporal_structure`, `motivational`.  
`completeness`: `full|partial|declared_unknown`.

---

## Inference

### `CognitiveState`
Famille, pour une personne et une fenêtre, de `ConstructEstimate` et de `Refusal`.

### `ConstructEstimate`
Voir contrat dans `docs/04`. Invalide sans incertitude, évidence, fenêtre, provenance.

### `Uncertainty`
`kind`: `sd|variance|credible_interval|discrete|unknown`.  
Composantes optionnelles : `measurement`, `evidence`, `inference`.

### `AlternativeExplanation`
`target_construct`, `modulator` (fatigue, arousal, …), `plausibility?`.

### `Refusal`
`code` ∈ {`NO_CONSTRUCT`,`NO_EVIDENCE`,`WINDOW_UNDEFINED`,`CONTEXT_MISSING`,`UNRESOLVED_ALTERNATIVES`,`MISALIGNED_MEASURE`,`PROVENANCE_BROKEN`}.  
`message`, `blocking_items[]`.

### `FunctionalProjection`
Pont vers ICF. `status` forcé à `HYPOTHESIS`. `does_not_imply[]`.

### `CapacityProfile`
Dispositions lentes. N'est pas un état T0. Peut informer un prior.

### `Trajectory`
Suite ordonnée de `CognitiveState`. Pas d'interpolation implicite.

---

## Function (alignement ICF)

### `ActivityLimitation`
Projection côté activités.

### `ParticipationRestriction`
Projection côté participation. Jamais déduite automatiquement d'une limitation d'activité.

Les deux classes existent pour typer les projections. Elles ne recréent pas l'ICF.
