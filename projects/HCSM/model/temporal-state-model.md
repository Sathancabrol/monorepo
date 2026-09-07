# Modèle temporel formel

**Statut :** `PROPOSED`  
**Couche :** HCSM MODEL

---

## 1. Fenêtre

\[
w(t_0,h)
=
[t_0-h,\; t_0+h]
\]

Une observation d'instant \(\tau\) est dans \(w\) ssi \(\tau \in w\).  
Une observation déjà définie sur une sous-fenêtre \(w'\) est dans \(w\) ssi \(w' \subseteq w\). Sinon elle est exclue ou \(w\) est redéfinie (nouvel objet).

## 2. Pas d'extrapolation

Pour tout \(t \notin w\), \(\mathrm{CS}(p,w)\) ne dit rien.  
Pas de hold, pas de LOCF, pas de lissage vers le prochain T0 en v0.1.

## 3. Trajectoire

\[
T_p
=
\big(\mathrm{CS}(p,w_1),\; \ldots,\; \mathrm{CS}(p,w_n)\big)
\quad
\text{avec centres strictement croissants}
\]

Les fenêtres peuvent se chevaucher. Un chevauchement n'autorise pas à fusionner les deux états.  
Les `Refusal` restent des membres. Un trou n'est pas une donnée manquante à imputer ; c'est une absence d'état.

## 4. Capacité

\(\kappa_{c,p}\) vit sur une échelle plus lente. Sa mise à jour (hors v0.1) exigerait plusieurs fenêtres, un modèle explicite, et l'interdiction d'écrire \(\kappa\) dans `ConstructEstimate.value`.

## 5. Constantes de temps

Chaque construit déclare `typicalTimescale`. Utiliser une fenêtre d'un jour pour un construit momentané est légal si déclaré, mais rend les observations non stationnaires plus probables, donc \(\mathcal{U}_{\mathrm{evid}}\) plus grande, donc le refus plus fréquent. C'est le comportement attendu, pas un défaut.
