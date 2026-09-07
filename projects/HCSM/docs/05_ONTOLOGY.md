# 05 — Ontologie HCSM v0.1

**Statut du document :** `PROPOSED`  
**Couche :** ONTOLOGY  
**Version :** 0.1.0 · 2026-08-25

Spécification machine : `ontology/hcsm-v0.1.yaml`  
Détail des classes : `ontology/entities.md`  
Détail des relations : `ontology/relations.md`  
Espaces de noms : `ontology/namespaces.md`

---

## 1. Principes

1. **HCSM n'est pas une ontologie de la cognition.** C'est une ontologie de l'*état cognitif estimé*. Les construits viennent d'ailleurs (Cognitive Atlas en priorité).
2. **Pas de fusion.** Les identifiants externes sont premiers. Un concept Atlas n'est pas recopié, il est *aligné*.
3. **Trois sous-graphes, une ontologie.** Les classes portent un axe `graph: knowledge | evidence | inference`.
4. **La provenance est une classe, pas une annotation facultative.**
5. **Le refus est une classe.** `Refusal` a le même rang que `ConstructEstimate`.

## 2. Modules

```
hcsm:
  core/           identifiants, statuts, graphes
  knowledge/      construits, théories, tâches, littérature
  evidence/       personne, observation, mesure, contexte, provenance
  inference/      estimation, incertitude, alternatives, refus, projection
  time/           instant, fenêtre, trajectoire
  function/       capacité, activité, participation (alignement ICF)
  align/          ponts Atlas, RDoC, ICF, HPO, CogPO
```

## 3. Classes minimales (v0.1)

### Knowledge

| Classe | Rôle |
|---|---|
| `Construct` | Construit latent (attention, working memory, …) |
| `Subprocess` | Partie d'un construit |
| `Theory` | Cadre théorique qui relie des construits |
| `Task` | Tâche / paradigme de mesure |
| `Measure` | Instrument, score dérivé, feature digitale typée |
| `LiteratureRecord` | Référence qui ancre une définition ou une relation |
| `ExternalConcept` | Proxy d'un identifiant étranger |

### Evidence

| Classe | Rôle |
|---|---|
| `Person` | Sujet d'observation (identifiant opaque) |
| `Observation` | Valeur observée, brute ou dérivée, timestampée |
| `MeasureInstance` | Application d'une `Measure` à une `Person` |
| `ContextRecord` | Situation, tâche en cours, environnement, état déclaré |
| `ProvenanceRecord` | Agent, activité, source, transformation |
| `Signal` | Série temporelle (EEG, HRV, actigraphie) |

### Inference

| Classe | Rôle |
|---|---|
| `ConstructEstimate` | Estimation d'un construit pour une personne dans une fenêtre |
| `Uncertainty` | Représentation de l'incertitude |
| `AlternativeExplanation` | Hypothèse concurrente |
| `Refusal` | Décision de ne pas estimer |
| `FunctionalProjection` | Hypothèse de fonctionnement (ICF) |
| `CognitiveState` | Famille d'estimations / refus à T0 |

### Time / Function

| Classe | Rôle |
|---|---|
| `TimePoint` | Instant T0 |
| `TemporalWindow` | Intervalle d'interprétation |
| `Trajectory` | Suite ordonnée d'`CognitiveState` |
| `CapacityProfile` | Dispositions relativement stables |
| `ActivityLimitation` | Alignement ICF activités |
| `ParticipationRestriction` | Alignement ICF participation |

## 4. Identifiants

```
hcsm:<module>/<class>/<slug>
```

Exemples :

```
hcsm:knowledge/construct/attention
hcsm:knowledge/task/cpt
hcsm:evidence/observation/obs_20260825T094012Z_cpt_omissions
hcsm:inference/estimate/att_pX_t0
hcsm:align/cognitiveatlas/trm_4a3fd79d0b5df   # attention
```

Règles :

- slug ASCII, kebab-case ;
- pas d'information personnelle dans l'IRI ;
- un `ExternalConcept` conserve l'IRI d'origine dans `source_iri` ;
- versionnement : l'ontologie a un IRI de version `hcsm:ontology/0.1.0`.

## 5. Alignements obligatoires en v0.1

Pour tout `Construct` publié dans HCSM v0.1, au moins un alignement doit exister, dans cet ordre de préférence :

1. Cognitive Atlas (`exactMatch` ou `closeMatch`)
2. RDoC construct / domain
3. ICF body function (b1* fonctions mentales) si pertinent
4. HPO si un phénotype observable correspondant existe

Un construit sans aucun alignement est accepté uniquement avec le statut `HYPOTHESIS` et une justification dans `scientific/constructs/`.

## 6. Construits du noyau v0.1

Le noyau est volontairement petit. Il sert à tester l'architecture, pas à cartographier l'esprit.

| Construct HCSM | Alignement prioritaire | Unités d'évidence attendues |
|---|---|---|
| `attention` | Atlas attention ; RDoC Cognitive Systems / Attention | comportement, subjectif, neural, contexte |
| `working_memory` | Atlas working memory ; RDoC Working Memory | comportement, subjectif |
| `cognitive_control` | Atlas cognitive control ; RDoC Cognitive Control | comportement |
| `fatigue` | proche état, pas toujours un construit Atlas | subjectif, physiologique, contexte |
| `arousal` | RDoC Arousal/Regulatory | physiologique, subjectif |
| `sleep_pressure` | contexte / état | subjectif, comportement, physiologique |

`fatigue`, `arousal`, `sleep_pressure` sont des **modulateurs d'état**, pas des construits cognitifs au même titre que l'attention. Ils existent dans l'ontologie pour que les alternatives d'inférence soient typées.

## 7. Ce que l'ontologie interdit

- une `Observation` sous-classe de `Construct` ;
- un `ConstructEstimate` sans `Uncertainty` ni `TemporalWindow` ;
- un `mapsTo` vers un diagnostic DSM/CIM comme s'il s'agissait d'un construit ;
- un niveau `NeurologicalState` parallèle à `Construct`.

## 8. Gouvernance

Toute modification de classe ou de relation :

1. ticket avec statut épistémique ;
2. mise à jour de `ontology/hcsm-v0.1.yaml` (ou version suivante) ;
3. entrée dans `CHANGELOG.md` ;
4. impact sur le schéma (`specs/data-schema.md`).

L'ontologie n'évolue pas par ajout opportuniste de construits « utiles au produit ».
