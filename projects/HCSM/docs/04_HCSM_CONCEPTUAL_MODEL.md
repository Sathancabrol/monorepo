# 04 — Modèle conceptuel HCSM

**Statut du document :** `PROPOSED`  
**Couche :** HCSM MODEL  
**Version :** 0.1.0 · 2026-08-25

Formalisation mathématique : `model/mathematical-model.md`.  
Figures : `figures/`.

---

## 1. Définition

HCSM représente l'état cognitif d'une personne au temps \(t\) comme le résultat d'une inférence, et non comme une mesure.

\[
\mathrm{CognitiveState}(t) = \mathrm{Inference}\big(\mathcal{O},\; \mathcal{M}_{t},\; \mathcal{X}_{t},\; \mathcal{H}_{<t},\; \mathcal{E}_{t}\big)
\]

| Symbole | Nom | Graphe | Question |
|---|---|---|---|
| \(\mathcal{O}\) | Ontologie des construits | Knowledge | Qu'existe-t-il à estimer ? |
| \(\mathcal{M}_{t}\) | Mesures disponibles | Evidence | Qu'a-t-on observé ? |
| \(\mathcal{X}_{t}\) | Contexte | Evidence | Dans quelles conditions ? |
| \(\mathcal{H}_{<t}\) | Histoire utile | Temporal | Que sait-on déjà de cette personne ? |
| \(\mathcal{E}_{t}\) | Évidence structurée | Evidence | Quelle force, quelle provenance ? |
| Inference | Moteur | Inference | Que peut-on conclure, ou refuser de conclure ? |

Un `CognitiveState` est une *famille* de `ConstructEstimate`, pas un vecteur anonyme de scores.

## 2. Quatre arguments d'un construit

Pour un construit \(c\) :

\[
State_{c,t} = f(Capacity_{c},\; State_{t},\; Context_{t},\; Evidence_{t})
\]

| Argument | Sens | Ce qu'il n'est pas |
|---|---|---|
| **Capacity** | Disposition relativement stable (trait, compétence, réserve) | Un score de test unique |
| **State** | Fluctuation transitoire (fatigue, arousal, humeur, charge) | La capacité |
| **Context** | Situation, tâche, environnement, contraintes | Un simple label |
| **Evidence** | Observations qui autorisent l'estimation | Le construit lui-même |

Séparer Capacity et State est `SUPPORTED` (psychométrie état–trait, ICF capacité vs performance).  
Ajouter Evidence comme argument de premier rang est `PROPOSED`.

Sans Evidence, le modèle retombe sur un score habillé. Avec Evidence, le modèle peut renvoyer « non estimable ».

## 3. Trois graphes superposés

HCSM n'est pas un graphe unique. Un graphe unique force la confusion des statuts.

### 3.1. Knowledge graph — ce que la science sait

Nœuds typiques : `Construct`, `Subprocess`, `Theory`, `Task`, `Paradigm`, `LiteratureRecord`, `ExternalConcept` (Atlas, RDoC, ICF, HPO).

Relations typiques : `isA`, `partOf`, `relatedTo`, `measuredBy`, `definedBy`, `mapsTo`.

Règle : aucun nœud du knowledge graph n'est une personne. Aucune arête n'exprime un état.

### 3.2. Evidence graph — ce qui a été observé

Nœuds typiques : `Person` (identifiant non identifiant au sens clinique de ce dépôt), `Observation`, `MeasureInstance`, `Signal`, `SelfReport`, `ContextRecord`, `ProvenanceRecord`.

Relations typiques : `observedOn`, `producedBy`, `hasContext`, `derivedFrom`, `hasAgent`, `hasTimestamp`.

Règle : une observation n'est jamais un construit. `CPT_omission_rate = 0.18` n'est pas `Attention`.

### 3.3. Inference graph — ce que l'on peut conclure

Nœuds typiques : `ConstructEstimate`, `LatentState`, `AlternativeExplanation`, `FunctionalProjection`, `Refusal`.

Relations typiques : `inferredFrom`, `competingWith`, `modulatedBy`, `projectsTo`, `insufficientFor`.

Règle : toute estimation cite au moins une observation, une fenêtre, une incertitude. Toute estimation peut être mise en concurrence.

### 3.4. Le moteur

Cognition Hub, quand il existera, est le moteur qui :

1. ancre un construit dans \(\mathcal{O}\) ;
2. collecte \(\mathcal{M}_{t}\) et \(\mathcal{X}_{t}\) dans l'evidence graph ;
3. produit ou refuse un nœud du inference graph ;
4. projette, si légitime, vers un fonctionnement ICF ;
5. archive la provenance de l'inférence elle-même (l'inférence est une activité PROV).

## 4. Unités d'analyse comme voies d'évidence

Héritage RDoC, réinterprété (`PROPOSED`) :

```
                 CONSTRUCT (knowledge)
                         │
     biological  physiological  neural  behavioral  subjective  contextual
         │            │           │          │           │           │
         └────────────┴───── evidence ───────┴───────────┴───────────┘
                                   │
                           latent estimation
                                   │
                              functioning
```

Conséquences :

- il n'y a pas d'« état neurologique » parallèle à l'« état cognitif » ;
- une voie peut être vide : le modèle n'impute pas ;
- la convergence entre voies augmente la confiance, elle ne crée pas le construit ;
- une divergence entre voies est un signal (mesure mauvaise, contexte non partagé, construit mal découpé), pas un bug.

## 5. Objet `ConstructEstimate`

Schéma canonique (détail : `specs/data-schema.md`) :

```text
ConstructEstimate
├── construct_id          hcsm:construct/attention
├── person_id             opaque
├── value                 0.73          # latente, jamais brute
├── scale                 latent_z | unit_interval | model_param
├── uncertainty           {type: sd, value: 0.12}
├── evidence_ids          [obs:1, obs:2, obs:3, obs:4]
├── measure_ids           [cpt, rt_var, self_report, ema]
├── context_id            ctx:sleep_restriction+high_workload
├── temporal_window       {center: T0, half_width: 30min}
├── population_reference  ref:adults_18_40_norm_v0
├── provenance            prov:...
├── alternative_explanations
│     ├── fatigue
│     ├── arousal
│     ├── motivation
│     └── task_difficulty
├── status                estimated | refused
└── epistemic_tag         PROPOSED
```

Un objet sans `uncertainty`, sans `evidence_ids` ou sans `temporal_window` est **invalide**.

## 6. Refus d'estimer

Le modèle produit un nœud `Refusal` lorsque l'une des conditions suivantes est vraie :

| Code | Condition |
|---|---|
| `NO_CONSTRUCT` | identifiant hors ontologie ou ambigu |
| `NO_EVIDENCE` | aucune observation dans la fenêtre |
| `WINDOW_UNDEFINED` | T0 ou largeur absents |
| `CONTEXT_MISSING` | contexte requis par le construit non renseigné |
| `UNRESOLVED_ALTERNATIVES` | explications concurrentes non départageables et de même plausibilité |
| `MISALIGNED_MEASURE` | la tâche ne *measure-by* pas le construit dans le knowledge graph |
| `PROVENANCE_BROKEN` | chaîne PROV incomplète |

Le refus est un résultat scientifique. Il est plus fidèle qu'un 0.50 par défaut.

## 7. De l'état au fonctionnement

L'état HCSM n'est pas le fonctionnement. La projection :

```
ConstructEstimate+  ×  Context  ×  Capacity  →  FunctionalProjection
```

suit la logique ICF : on ne déduit pas une restriction de participation d'une estimation d'attention. On formule une *hypothèse de fonctionnement* (`HYPOTHESIS` au niveau de chaque projection), testable par des indicateurs d'activité et de participation.

## 8. Ce que le modèle refuse d'être

- un facteur g cognitif unique ;
- un classifieur diagnostique ;
- un tableau de bord de « niveaux » empilés ;
- un agrégat de features digitales étiqueté avec des noms de construits.

## 9. Mini-scénario (illustratif, non empirique)

Personne P, T0 = 09:40, fenêtre ±30 min.

Evidence :

- omissions CPT élevées ;
- variabilité des temps de réaction élevée ;
- self-report « je n'arrive pas à me concentrer » ;
- EMA sommeil = 4 h 20 ;
- contexte : deadline, open space.

Inférence légitime :

- `attention` estimée basse, incertitude large ;
- alternatives actives : fatigue, charge, motivation, difficulté de la tâche ;
- `working_memory` **refusée** (pas de mesure alignée dans la fenêtre) ;
- projection ICF `d160 Focusing attention` : hypothèse de limitation d'activité, pas un fait.

Inférence illégitime, que HCSM doit rendre inexprimable :

- `Attention = 27 %` ;
- `TDAH probable` ;
- `état neurologique dégradé`.
