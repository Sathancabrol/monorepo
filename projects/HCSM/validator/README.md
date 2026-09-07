# Validateur HCSM v0.1

**Couche :** IMPLEMENTATION (contrat seulement)  
**Statut :** `PROPOSED`  
**Version :** 0.1.1

Ce module **n'estime rien**. Il lit des objets JSON (ou un bundle) et décide :

1. **V1 — forme** : l'objet est-il licite au regard de `ontology/hcsm-v0.1.yaml` et de `specs/data-schema.md` ?
2. **V5 — admissibilité** : l'inférence est-elle autorisée, ou faut-il un `Refusal` ?

```
Knowledge → Measurement → Inference → State T0
                              ↑
                     ce validateur agit ICI
                     (avant toute estimation numérique)
```

## Installation

```bash
cd validator
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
# Valider un fichier
python validate.py cases/valid/mini_scenario_attention.json

# Tous les cas (attendus pass / fail / admit / refuse)
python validate.py --all

# Admissibilité seule (V5)
python validate.py --admit cases/valid/mini_scenario_attention.json

# Tests unitaires
python -m pytest tests/ -q
```

Code de sortie : `0` si conforme à l'attendu, `1` sinon.

## Ce qui est rejeté (V1)

| Interdit | Code |
|---|---|
| Score nu (`Attention = 0.73`) | `V1-NAKED-SCORE` |
| Observation portant un champ d'estimation | `V1-OBS-ESTIMATE-FIELD` |
| `ConstructEstimate` sans incertitude / fenêtre / preuves / provenance / contexte | `V1-CE-*` |
| `Refusal` avec une `value` | `V1-REFUSAL-HAS-VALUE` |
| `FunctionalProjection.status ≠ HYPOTHESIS` | `V1-FP-STATUS` |
| Cible diagnostique | `V1-DIAGNOSTIC-TARGET` |
| Feature digitale présentée comme construit | `V1-DIGITAL-AS-CONSTRUCT` |
| Identifiant civil | `V1-PII` |
| T0 / fenêtre mal formée | `V1-WINDOW` |

## Ce qui déclenche un refus (V5)

| Code | Condition |
|---|---|
| `NO_CONSTRUCT` | construit hors ontologie ou rôle diagnostic |
| `NO_EVIDENCE` | aucune observation `exact`/`close` dans la fenêtre |
| `WINDOW_UNDEFINED` | centre ou demi-largeur absents |
| `CONTEXT_MISSING` | contexte requis absent et non déclaré |
| `UNRESOLVED_ALTERNATIVES` | alternatives obligatoires non instanciées |
| `MISALIGNED_MEASURE` | mesure sans alignement sur le construit |
| `PROVENANCE_BROKEN` | chaîne PROV absente ou incomplète |

## Structure

```
validator/
├── README.md
├── requirements.txt
├── validate.py                 # point d'entrée CLI
├── hcsm_validate/
│   ├── __init__.py
│   ├── ontology.py             # charge hcsm-v0.1.yaml
│   ├── schema.py               # validation de forme (V1)
│   ├── admissibility.py        # filtre d'inférence (V5)
│   └── cli.py
├── cases/
│   ├── valid/                  # doivent passer
│   └── invalid/                # doivent échouer (ou produire Refusal)
└── tests/
    └── test_validator.py
```

## Ce que ce module n'est pas

- pas un estimateur bayésien ;
- pas une API réseau ;
- pas un lecteur de capteurs ;
- pas un outil clinique.

Un objet qui **passe** est bien formé. Il n'est pas pour autant **vrai**.
