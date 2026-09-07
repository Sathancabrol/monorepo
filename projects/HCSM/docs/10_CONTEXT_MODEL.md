# 10 — Modèle de contexte

**Statut du document :** `PROPOSED`  
**Couche :** HCSM MODEL  
**Version :** 0.1.0 · 2026-08-25

---

## 1. Le contexte n'est pas une métadonnée

Dans l'ICF (`ESTABLISHED`), le fonctionnement est une interaction entre condition de santé et facteurs contextuels. HCSM reprend cette exigence au niveau de l'état cognitif : un `ConstructEstimate` sans contexte n'est comparable ni à un autre moment, ni à une autre personne.

```
même construit + même valeur + contextes différents
        ≠
même état
```

## 2. Dimensions de contexte v0.1

| Dimension | Exemples | Source typique |
|---|---|---|
| `task` | nature, difficulté, enjeu, durée | protocole, app |
| `environment` | bruit, open space, labo, domicile | déclaration, capteur |
| `somatic` | sommeil, douleur, substances, maladie aiguë | EMA, wearable |
| `occupational` | charge, deadline, interruption | déclaration, calendrier |
| `social` | présence d'autrui, évaluation sociale | déclaration, GPS approximatif |
| `temporal_structure` | heure circadienne, jour de semaine | horloge |
| `motivational` | consigne, récompense, contrainte | protocole |

Toutes les dimensions n'ont pas à être remplies. Celles **requises** par un construit le sont dans l'ontologie (`requiresContext`).

Pour `attention` v0.1, le contexte minimal est : `task` + une dimension parmi `somatic` ou `occupational`. Sinon `CONTEXT_MISSING` ou contexte explicitement `declared_unknown`.

## 3. Contexte vs état vs capacité

| Objet | Bouge à quelle vitesse | Exemple |
|---|---|---|
| Capacity | lent | réserve, compétence CPT entraînée |
| State | rapide | fatigue, arousal |
| Context | externe ou situationnel | deadline, nuit courte, open space |

La nuit courte est un **contexte** (fait) qui peut fonder une **alternative** `sleep_pressure` (hypothèse) qui module un **état** `attention` (estimation). Ces trois objets ne fusionnent pas.

## 4. Encodage

Un `ContextRecord` est une observation comme une autre : typé, timestampé, provenancé. Il n'est pas un tag libre.

```
ContextRecord
  person_id
  window
  dimensions:
    task: {id: cpt, difficulty: standard, duration_min: 12}
    somatic: {sleep_hours: 4.3, source: ema}
    occupational: {workload: high, source: self_report}
  completeness: partial
  provenance: ...
```

## 5. Comparabilité

Deux estimations ne sont comparables que si :

- même construit ;
- fenêtres de largeur compatible ;
- contextes non contradictoires sur les dimensions requises ;
- estimateur et ontologie de mêmes versions, ou écart déclaré.

Comparer l'attention d'un CPT de laboratoire bien reposé à une EMA de lundi matin en restriction de sommeil, sans déclarer l'écart, est une erreur de modèle.

## 6. Ce que le contexte n'autorise pas

- « corriger » un score d'attention pour le sommeil par une règle opaque ;
- inférer un trait à partir d'un contexte unique ;
- traiter le lieu GPS comme un contexte psychologique (maison ≠ sécurité).
