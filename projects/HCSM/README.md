# HCSM — Human Cognitive State Model

**Version 0.1.1** · 25 août 2026 · statut global : `PROPOSED`  
Cadre scientifique pour une représentation multidimensionnelle, contextualisée, temporelle et evidentiale de l'état cognitif humain à T0.

> L'enjeu scientifique n'est plus simplement de mesurer davantage.  
> Il est de **relier correctement ce qui est déjà mesuré**.

---

## Ce que HCSM est — et n'est pas

| Objet | Rôle | Couche |
|---|---|---|
| **HCSM** | Modèle scientifique de l'état cognitif humain | MODEL |
| **Cognition Hub** | Système computationnel qui instancie HCSM | SPEC / IMPLEMENTATION |
| **Cognitorium** | Architecture globale des connaissances, compétences, expériences et trajectoires | ECOSYSTEM |

HCSM n'est **pas** :

- un score cognitif unique, ni un QI 2.0 ;
- « la première plateforme à intégrer cognition + psychologie + physiologie + neurologie » — cette revendication est **réfutable** et n'est pas portée ici ;
- une nouvelle nosologie, ni un substitut de [RDoC](https://www.nimh.nih.gov/research/research-funded-by-nimh/rdoc), de l'[ICF](https://www.who.int/standards/classifications/international-classification-of-functioning-disability-and-health), du [Cognitive Atlas](https://www.cognitiveatlas.org/) ou de [HPO](https://hpo.jax.org/) ;
- un moteur de diagnostic clinique.

HCSM est une **couche d'intégration computationnelle** entre des mondes déjà existants :

```
RDoC          → logique d'intégration des unités d'analyse
ICF           → fonctionnement contextualisé (fonction ↔ activité ↔ participation ↔ environnement)
Cognitive Atlas → représentation des concepts et des tâches
HPO           → phénotypes observables, hiérarchie sémantique
Psychométrie  → construits latents, validité, incertitude de mesure
Digital phenotyping / EMA → observations temporelles in situ
        │
        ▼
     HCSM
  Knowledge → Measurement → Inference → State T0 → Context → Function → Trajectory
```

**Statut :** `PROPOSED` — le modèle est formulé pour être critiqué, pas pour être adopté comme fait.

---

## Thèse

L'objet scientifique n'est pas un score. C'est un **état latent estimé**, pour une personne, à un instant T0, sur un ensemble de construits, à partir de preuves hétérogènes, dans un contexte, avec une provenance et une incertitude explicites.

On ne calcule pas :

```
Attention = 0.73
```

On estime :

```
CONSTRUCT              Attention
ESTIMATION             0.73
UNCERTAINTY            ± 0.12
EVIDENCE               4 observations
MEASURES               CPT · RT variability · self-report · EMA
CONTEXT                sleep restriction · high workload
TEMPORAL WINDOW        T0 ± 30 min
POPULATION REFERENCE   ...
PROVENANCE             ...
ALTERNATIVE EXPLANATIONS   fatigue · arousal · motivation · task difficulty
```

Formellement :

```
CognitiveState(t) = Inference(Ontology, Measurements, Context, History, Evidence)
```

Cette formule distingue six choses que le document source mélangeait encore trop souvent :

1. ce qui existe dans l'ontologie (connaissance) ;
2. ce qui a été mesuré (observation) ;
3. ce qui est estimé (inférence) ;
4. avec quel niveau de preuve (évidence) ;
5. dans quel contexte ;
6. à quel moment.

---

## Trois graphes, un moteur

HCSM ne produit pas « une carte de la cognition ». Il superpose trois graphes que Cognition Hub relie.

```
Graphe 1 — Knowledge          Graphe 2 — Evidence           Graphe 3 — Inference
Attention                     Person                        Sleep restriction
 ├── definition                ├── Test                          │
 ├── subprocesses              ├── Questionnaire                 ▼
 ├── theories                  ├── HRV / EEG                  Fatigue
 ├── related constructs        ├── Sleep                     ↙       ↘
 ├── tasks                     └── Context              arousal    attention
 └── literature                     └── workload           │            │
                                                           ▼            ▼
                                                    performance ← working memory
```

- **Knowledge graph** : ce que la science sait d'un construit. Aligné sur Cognitive Atlas, RDoC, ICF, HPO.
- **Evidence graph** : ce qui a été observé chez une personne, avec provenance.
- **Inference graph** : ce que l'on peut inférer, sous quelles hypothèses, avec quelles explications alternatives.

Le moteur ne confond pas ce que la science sait d'une fonction avec ce que l'on peut inférer sur une personne.

---

## Comment lire ce dépôt

Les couches ne se mélangent pas.

```
SCIENTIFIC KNOWLEDGE          scientific/  docs/02  docs/03
        ↓
    EVIDENCE                  docs/06  scientific/measures
        ↓
    HCSM MODEL                docs/04  docs/07–11  model/
        ↓
    ONTOLOGY                  ontology/  docs/05
        ↓
COMPUTATIONAL SPECIFICATION   specs/
        ↓
    IMPLEMENTATION            (hors de ce dépôt, phase ultérieure)
```

Chaque affirmation importante porte un statut :

`ESTABLISHED` · `SUPPORTED` · `PROPOSED` · `HYPOTHESIS` · `OPEN QUESTION`

Voir `CONTRIBUTING.md`.

### Carte du dépôt

```
HCSM/
├── README.md
├── docs/
│   ├── 00_PROJECT_OVERVIEW.md
│   ├── 01_SCIENTIFIC_POSITION.md
│   ├── 02_STATE_OF_THE_ART.md
│   ├── 03_RESEARCH_GAP.md
│   ├── 04_HCSM_CONCEPTUAL_MODEL.md
│   ├── 05_ONTOLOGY.md
│   ├── 06_EVIDENCE_MODEL.md
│   ├── 07_INFERENCE_MODEL.md
│   ├── 08_TEMPORAL_MODEL.md
│   ├── 09_UNCERTAINTY_AND_PROVENANCE.md
│   ├── 10_CONTEXT_MODEL.md
│   ├── 11_FUNCTIONING_MODEL.md
│   ├── 12_VALIDATION_FRAMEWORK.md
│   ├── 13_RESEARCH_PROTOCOL.md
│   └── 14_LIMITATIONS.md
├── scientific/          literature, models, hypotheses, constructs, measures
├── ontology/            entités, relations, namespaces, hcsm-v0.1.yaml
├── model/               modèle mathématique, état latent, incertitude, temps
├── figures/             architecture, graphes, T0, trajectoire
├── papers/              working paper + bibliographie
├── research/            audit, novelty matrix, questions ouvertes
├── specs/               schéma de données, API, roadmap
└── validator/           contrat exécutable V1 (forme) + V5 (admissibilité)
```

### Validateur (phase 1 — fait)

Le contrat n'est plus seulement documenté : il est exécutable.

```bash
cd validator
pip install -r requirements.txt
python validate.py --all          # 23 cas synthétiques
python -m pytest tests/ -q        # tests unitaires
```

Ce module **n'estime rien**. Il rejette les objets illégaux et décide si une inférence est admissible ou doit produire un `Refusal`. Voir `validator/README.md`.

### Parcours recommandé

1. Position et audit — `docs/01_SCIENTIFIC_POSITION.md`, `research/scientific-audit.md`
2. Antériorités — `docs/02_STATE_OF_THE_ART.md`, `research/novelty-matrix.md`
3. Modèle — `docs/04_HCSM_CONCEPTUAL_MODEL.md`, `model/mathematical-model.md`
4. Ontologie — `ontology/README.md`, `ontology/hcsm-v0.1.yaml`
5. Validation — `docs/12_VALIDATION_FRAMEWORK.md`, `docs/13_RESEARCH_PROTOCOL.md`
6. Contrat exécutable — `validator/README.md`
7. Working paper — `papers/working-paper/HCSM_working_paper.md`

---

## Relation avec les autres dépôts

| Dépôt | Rôle par rapport à HCSM |
|---|---|
| [Sathancabrol/ETAT-DE-LART-PSYCHOLOGIE](https://github.com/Sathancabrol/ETAT-DE-LART-PSYCHOLOGIE) | Cartographie critique 2020–2026, taxonomie des construits, protocole PRISMA. Alimente le knowledge graph. |
| [Sathancabrol/COGNITORIUM](https://github.com/Sathancabrol/COGNITORIUM) | Outils de visualisation et architecture globale connaissances / compétences / trajectoires. HCSM en est le moteur d'état cognitif. |

---

## Licence et citation

Documentation sous [CC-BY 4.0](LICENSE).  
Les statuts `PROPOSED` et `HYPOTHESIS` doivent être conservés en cas de réutilisation.

```
HCSM contributors (2026). HCSM — Human Cognitive State Model (v0.1.0).
https://github.com/Sathancabrol/HCSM
```
