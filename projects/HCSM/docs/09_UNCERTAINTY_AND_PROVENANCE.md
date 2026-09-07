# 09 — Incertitude et provenance

**Statut du document :** `PROPOSED` (contrat HCSM), s'appuie sur PROV-O et FAIR (`ESTABLISHED`)  
**Couche :** HCSM MODEL  
**Version :** 0.1.0 · 2026-08-25

---

## 1. Pourquoi les deux vont ensemble

Une incertitude sans provenance est un intervalle décoratif.  
Une provenance sans incertitude est une traçabilité de score nu.

HCSM tient les deux comme constitutives de `ConstructEstimate`. L'absence de l'une invalide l'objet.

## 2. Incertitude — trois sources, un objet

| Source | Origine | Traitement v0.1 |
|---|---|---|
| de mesure | bruit d'instrument, fidélité | reportée depuis la `Measure` si connue, sinon `unknown` |
| d'évidence | couverture, voies manquantes, qualité | élargit \(\sigma\) ou déclenche `Refusal` |
| d'inférence | modèle, alternatives non départagées | explicite dans \(A\) et dans la provenance de l'estimateur |

On ne les fusionne pas en un unique « indice de confiance » marketing. On peut *résumer* \(\sigma\), on ne détruit pas les composantes.

Représentations acceptées :

- écart-type ou variance sur l'échelle latente ;
- intervalle de crédibilité ;
- distribution discrète sur un petit ensemble d'états ;
- `unknown` — valeur légitime, plus honnête qu'un ±0.00.

Représentations refusées :

- pastille verte / orange / rouge sans définition ;
- pourcentage de confiance sans calibration ;
- absence de champ.

Détail : `model/uncertainty-model.md`.

## 3. Provenance — profil PROV-O

Profil minimal, compatible [PROV-O](https://www.w3.org/TR/prov-o/) :

```
Entity        Observation, ConstructEstimate, OntologyVersion, Dataset
Activity      MeasureActivity, PreprocessActivity, InferenceActivity
Agent         Person(operator), SoftwareAgent(estimator, app), Organization
```

Relations utilisées :

- `wasGeneratedBy`
- `used`
- `wasDerivedFrom`
- `wasAttributedTo` / `wasAssociatedWith`
- `startedAtTime` / `endedAtTime`

Une estimation doit pouvoir répondre à :

1. Quelles observations ?  
2. Quelles transformations ?  
3. Quelle version d'ontologie ?  
4. Quel estimateur, quels hyperparamètres ?  
5. Quel agent ?  
6. Quand ?

Si l'une de ces réponses manque, `PROVENANCE_BROKEN`.

## 4. FAIR appliqué à l'état cognitif

Wilkinson et al. (2016), interprétés pour HCSM :

| Principe | Application |
|---|---|
| Findable | IRI stables `hcsm:...`, métadonnées de fenêtre et de construit |
| Accessible | protocole déclaré ; données personnelles hors de ce dépôt |
| Interoperable | alignements Atlas / RDoC / ICF / HPO, PROV-O, schéma YAML/JSON |
| Reusable | licence CC-BY pour le modèle ; statuts épistémiques conservés |

FAIR ne s'applique pas aux données individuelles dans ce dépôt : il n'y en a pas. Il s'applique au **modèle**, à l'**ontologie** et aux **jeux synthétiques** de validation.

## 5. Incertitude des alternatives

Chaque `AlternativeExplanation` peut porter une plausibilité dans \([0,1]\) ou `unknown`. La somme n'a pas à valoir 1 : les alternatives ne forment pas une partition exhaustive du monde. Elles forment l'ensemble des hypothèses que le modèle refuse d'oublier.

## 6. Versionnement

Changer :

- une définition de construit,
- un `measuredBy`,
- un estimateur,
- une largeur de fenêtre par défaut,

crée une **nouvelle activité**, donc potentiellement une nouvelle estimation, même si `value` ne change pas. On ne réécrit pas l'histoire.
