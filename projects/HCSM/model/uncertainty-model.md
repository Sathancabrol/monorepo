# Modèle d'incertitude

**Statut :** `PROPOSED`  
**Couche :** HCSM MODEL

---

## 1. Trois composantes

\[
\mathcal{U}
=
\{\mathcal{U}_{\mathrm{meas}},\;
\mathcal{U}_{\mathrm{evid}},\;
\mathcal{U}_{\mathrm{inf}}\}
\]

On peut résumer, on ne doit pas écraser.

| Composante | Contenu | Défaut honnête |
|---|---|---|
| mesure | fidélité d'instrument, erreur de scoring | `unknown` |
| évidence | couverture des voies, qualité, missingness | élargit \(\sigma\) ou refus |
| inférence | modèle, hyperparamètres, alternatives | \(\gamma_{\mathrm{alt}}\), provenance de l'estimateur |

## 2. Représentations

```
kind: sd | variance | credible_interval | discrete | unknown
```

Règles :

- `sd` / `variance` : même échelle que `value` ;
- `credible_interval` : `lower`, `upper`, niveau déclaré (défaut 0.95) ;
- `discrete` : table `{state: mass}` ; masse totale ≤ 1 (le reste est `unallocated`, pas caché) ;
- `unknown` : légitime ; interdit de la remplacer par 0.

## 3. Interdits

- pastille unique de confiance ;
- `1 - p` d'un classifieur baptisé incertitude d'état ;
- intervalle construit a posteriori pour « faire scientifique ».

## 4. Propagation minimale

Si une observation utilisée a `quality_flag = degraded`, \(\mathcal{U}_{\mathrm{evid}}\) augmente.  
Si une alternative obligatoire a `plausibility = unknown`, \(\mathcal{U}_{\mathrm{inf}}\) n'est pas inférieure à celle d'une estimation sans alternative : on n'est pas plus sûr parce qu'on a oublié de quantifier.

## 5. Calibration

Aucune calibration n'est revendiquée en v0.1. Un intervalle n'est pas un intervalle de prédiction empirique tant qu'une phase D n'a pas été menée.
