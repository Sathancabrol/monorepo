# 07 — Modèle d'inférence

**Statut du document :** `PROPOSED`  
**Couche :** HCSM MODEL  
**Version :** 0.1.0 · 2026-08-25

Mathématiques : `model/latent-state-model.md`, `model/uncertainty-model.md`.

---

## 1. Rôle

L'inférence est la seule opération qui fait passer d'une observation à un construit. Elle n'est pas une moyenne de scores. Elle n'est pas un classifieur clinique.

```
Knowledge (quoi estimer, avec quelles tâches)
     +
Evidence (quoi a été vu, avec quelle qualité)
     +
Context + History
     ↓
  Inference
     ↓
ConstructEstimate | Refusal
     ↓
FunctionalProjection?   (optionnelle, toujours HYPOTHESIS)
```

## 2. Forme générale

Pour un construit \(c\), une personne \(p\), une fenêtre \(w\) :

\[
(\hat\theta_{c,p,w},\; \sigma_{c,p,w},\; A_{c,p,w})
=
\begin{cases}
\mathrm{estimate}(\mathcal{O}_c, \mathcal{E}_{c,p,w}, \mathcal{X}_{p,w}, \mathcal{H}_p)
  & \text{si admissible} \\
\mathrm{Refusal}(code)
  & \text{sinon}
\end{cases}
\]

- \(\hat\theta\) : estimation latente
- \(\sigma\) : incertitude
- \(A\) : ensemble d'explications alternatives encore actives

## 3. Admissibilité (avant toute estimation)

L'inférence commence par un filtre, pas par un calcul.

1. \(c\) existe dans \(\mathcal{O}\) et n'est pas un diagnostic.
2. Au moins une observation dans \(w\) a `alignment ∈ {exact, close}` avec \(c\).
3. \(w\) est définie (centre et largeur).
4. Le contexte minimal du construit est présent, ou l'absence est déclarée.
5. La chaîne de provenance n'est pas brisée.
6. Les alternatives obligatoires du construit sont instanciées (même à plausibilité inconnue).

Si un item échoue → `Refusal`. Pas de valeur par défaut.

## 4. Familles d'estimateurs acceptables

HCSM n'impose pas *un* estimateur. Il impose un **contrat de sortie**. Familles candidates (`SUPPORTED` comme outils, `PROPOSED` comme usage HCSM) :

| Famille | Usage légitime | Usage illégitime |
|---|---|---|
| IRT / facteur / SEM | plusieurs items d'une même voie | fusionner EEG et Likert dans un facteur unique sans modèle |
| État-espace / Kalman | dynamique intra-individuelle | extrapoler hors fenêtre |
| Modèle computationnel (DDM, RL) | paramètre interprétable | baptiser le paramètre du nom d'un construit Atlas sans alignement |
| Réseau (network psychometrics) | influences entre nœuds d'inférence | remplacer l'ontologie |
| Fusion bayésienne de voies | combiner en déclarant les vraisemblances | cacher les poids |

En v0.1, le working model est une **fusion bayésienne simple par voie**, avec prior faible et possibilité de refus (voir `model/latent-state-model.md`). Ce n'est pas *le* modèle HCSM définitif.

## 5. Alternatives d'explication

Pour `attention`, les alternatives minimales v0.1 sont :

- `fatigue`
- `arousal`
- `motivation`
- `task_difficulty`
- `sleep_pressure`
- `affective_state`

Une alternative n'a pas à être éliminée pour qu'une estimation existe. Elle doit être **nommée**. Si deux alternatives ont une plausibilité comparable et prédisent la même observation, l'incertitude augmente ; elle n'est pas ignorée.

L'inference graph matérialise ces concurrences :

```
sleep_restriction
        │
        ▼
     fatigue
     ↙     ↘
arousal     attention
   │            │
   ▼            ▼
performance ← working memory
```

Les flèches sont des `modulatedBy` / `inferredFrom`, jamais des causalités établies. Statut : `HYPOTHESIS` au niveau de chaque arête, sauf littérature causale explicite.

## 6. Convergence et divergence

- **Convergence** de voies indépendantes : réduit \(\sigma\), ne « prouve » pas le construit.
- **Divergence** : augmente \(\sigma\), peut déclencher `UNRESOLVED_ALTERNATIVES`, peut signaler un mauvais découpage ontologique (question pour le knowledge graph, pas un patch de l'estimateur).

## 7. Histoire

\(\mathcal{H}_{<t}\) entre comme prior ou comme contrainte, jamais comme copie de la dernière estimation.

- une capacité stable peut informer le prior de \(c\) ;
- un état récent hors fenêtre n'est pas collé sur T0 ;
- en v0.1, l'histoire est optionnelle. Un T0 sans histoire est licite. Un T0 qui *n'est* que de l'histoire ne l'est pas.

## 8. Sorties interdites

L'inférence ne produit pas :

- un diagnostic ;
- un percentile marketing sans référence populationnelle déclarée ;
- une valeur sans incertitude ;
- une projection ICF présentée comme un fait.

## 9. Traçabilité de l'inférence

L'inférence est elle-même une activité PROV :

```
wasGeneratedBy(ConstructEstimate, InferenceActivity)
used(InferenceActivity, Observation+)
used(InferenceActivity, OntologyVersion)
used(InferenceActivity, EstimatorVersion)
wasAssociatedWith(InferenceActivity, Agent)
```

Changer d'estimateur change la provenance. Deux estimations de même valeur et de provenances différentes sont deux objets.
