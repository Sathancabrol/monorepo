# 08 — Modèle temporel

**Statut du document :** `PROPOSED`  
**Couche :** HCSM MODEL  
**Version :** 0.1.0 · 2026-08-25

Détail formel : `model/temporal-state-model.md`.

---

## 1. T0 n'est pas un point magique

T0 est un **centre de fenêtre**, pas un instant métaphysique où l'état « vraiment » se révèle. Toute estimation HCSM est définie sur une `TemporalWindow`.

```
         |← half_width →|← half_width →|
    ─────[──────────────T0──────────────]─────
              temporal window w(T0, h)
```

Sans \(h\), T0 est illégal.

## 2. Échelles de temps

Les construits n'ont pas la même constante de temps. Les imposer à une même fenêtre est une erreur.

| Échelle | Exemples | Fenêtre typique | Statut |
|---|---|---|---|
| momentanée | attention soutenue, arousal | minutes | `SUPPORTED` |
| circadienne / quotidienne | sommeil, fatigue, humeur | heures–jour | `SUPPORTED` |
| épisodique | charge de travail, stress aigu | jours–semaines | `SUPPORTED` |
| dispositionnelle | capacité, réserve, trait | mois–années | `ESTABLISHED` (état–trait) |

v0.1 estime principalement les échelles momentanée et quotidienne. Les dispositions entrent comme `CapacityProfile`, pas comme état T0.

## 3. Règles de fenêtre

1. La fenêtre d'un `ConstructEstimate` doit couvrir les timestamps de toutes les observations utilisées.
2. Si les observations s'étalent au-delà de la fenêtre déclarée, soit on élargit la fenêtre (et on change l'objet), soit on exclut l'observation.
3. On n'extrapole pas hors fenêtre en v0.1.
4. Une observation ponctuelle (un CPT de 12 minutes) peut fonder une fenêtre courte. Elle ne fonde pas une journée.

## 4. Capacité, état, trajectoire

```
CapacityProfile     lent, peu d'updates
      │
      │  prior
      ▼
CognitiveState(t)   fenêtre courte
      │
      │  suite ordonnée
      ▼
Trajectory          objet distinct, pas un lissage cosmétique
```

Une trajectoire est une suite de `CognitiveState` dont les fenêtres sont déclarées. Ce n'est pas une courbe lissée de scores. Deux états successifs peuvent contenir des `Refusal`. Un trou n'est pas interpolé en v0.1.

## 5. Ce que le temporel interdit

- agréger un test de 2022 et une EMA de ce matin sous le même T0 ;
- appeler « état actuel » une norme de population ;
- dériver une pente de trajectoire à partir de deux points de voies différentes.

## 6. Lien avec EMA et digital phenotyping

EMA et capteurs donnent naturellement des séries. HCSM ne les avale pas comme une série d'états. Il les avale comme des `Observation`, puis tranche des fenêtres. La densité des capteurs n'autorise pas, à elle seule, une fenêtre plus étroite que la validité de construit de la feature.
