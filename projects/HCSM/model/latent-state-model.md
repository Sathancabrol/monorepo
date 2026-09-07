# Modèle d'état latent — working model v0.1

**Statut :** `PROPOSED`  
**Rôle :** estimateur placeholder compatible avec le contrat, pas une contribution statistique

---

## 1. Intention

Fournir *un* estimateur assez simple pour :

- exercer le contrat (`value`, `uncertainty`, `alternatives`, `refusal`) ;
- être remplacé sans changer l'ontologie ;
- ne pas donner l'illusion d'une fusion multimodale résolue.

## 2. Par voie, puis fusion

Pour un construit \(c\), on partitionne l'évidence selon le canal \(u \in U\) :

\[
\mathcal{E}_{c}
=
\bigsqcup_{u\in U}
\mathcal{E}_{c}^{(u)}
\]

Chaque voie qui a au moins une observation `alignment ∈ {exact, close}` et `quality_flag ≠ unusable` produit une estimation de voie :

\[
\hat\theta^{(u)},\; \sigma^{(u)}
\]

Méthode de voie v0.1 :

- une seule observation standardisée \(z\) : \(\hat\theta^{(u)}=z\), \(\sigma^{(u)}=\sigma_{\mathrm{inst}}\) si connue, sinon \(\sigma^{(u)}=\texttt{unknown}\) et la voie est *indicative*, pas fusionnable numériquement ;
- plusieurs observations de la même mesure : moyenne inverse-variance si \(\sigma_{\mathrm{inst}}\) connue ;
- mesures différentes dans la même voie : on ne fusionne pas en v0.1 ; on garde la plus alignée et on note les autres comme alternatives internes.

## 3. Fusion inter-voies

Seules les voies avec \(\sigma^{(u)}\) numérique entrent dans la fusion.

Prior faible \(\theta \sim \mathcal{N}(\mu_0, \sigma_0^2)\), \(\sigma_0\) large.  
Si un `CapacityProfile` existe, \(\mu_0=\kappa_{c,p}\) et \(\sigma_0\) reste large (l'histoire n'écrase pas T0).

\[
\hat\theta
=
\frac{
\alpha_0\mu_0 + \sum_u \alpha_u \hat\theta^{(u)}
}{
\alpha_0 + \sum_u \alpha_u
},
\qquad
\alpha_u = (\sigma^{(u)})^{-2},
\quad
\alpha_0=\sigma_0^{-2}
\]

\[
\sigma
=
\left(\alpha_0+\sum_u\alpha_u\right)^{-1/2}
\cdot
\gamma_{\mathrm{div}}
\cdot
\gamma_{\mathrm{alt}}
\]

- \(\gamma_{\mathrm{div}} \ge 1\) : inflation si les \(\hat\theta^{(u)}\) divergent au-delà de ce que les \(\sigma^{(u)}\) autorisent ;
- \(\gamma_{\mathrm{alt}} \ge 1\) : inflation si des alternatives ont une plausibilité comparable.

Si moins de une voie fusionnable → `Refusal(NO_EVIDENCE)` ou estimation avec `Uncertainty.kind = unknown` selon la politique du construit. Pour le noyau v0.1 : **refus** plutôt qu'un \(\hat\theta\) orphelin, sauf s'il existe une voie `exact` unique (alors \(\sigma=\texttt{unknown}\) est autorisé).

## 4. Divergence

Soit \(s^2\) la variance empirique des \(\hat\theta^{(u)}\) pondérée. Si \(s^2\) dépasse un seuil préenregistré (à fixer en phase empirique), \(\gamma_{\mathrm{div}}>1\). Au-delà d'un second seuil, `UNRESOLVED_ALTERNATIVES` si deux modulateurs expliquent la divergence.

Les seuils ne sont **pas** fixés dans cette version. Les fixer sans données serait une fausse précision.

## 5. Ce que ce working model ne fait pas

- pas de modèle hiérarchique multi-niveaux ;
- pas de dérive temporelle intra-fenêtre ;
- pas de réseau dynamique sommeil → fatigue → attention (le graphe d'inférence *représente* ces hypothèses, l'estimateur ne les ajuste pas encore) ;
- pas de calibration populationnelle.

Un remplacement (IRT multidimensionnel, état-espace, modèle computationnel) est bienvenu s'il respecte `mathematical-model.md`.
