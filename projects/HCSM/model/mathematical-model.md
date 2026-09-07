# Modèle mathématique HCSM

**Statut :** `PROPOSED` · working model v0.1  
**Couche :** HCSM MODEL  
**Date :** 2026-08-25

Ce n'est pas *le* modèle statistique définitif. C'est le contrat formel que tout estimateur compatible HCSM doit respecter.

Documents liés : `latent-state-model.md`, `uncertainty-model.md`, `temporal-state-model.md`.

---

## 1. Objets

Soit :

- \(\mathcal{C}\) l'ensemble des construits de l'ontologie ;
- \(p\) une personne (identifiant opaque) ;
- \(w = (t_0, h)\) une fenêtre de centre \(t_0\) et de demi-largeur \(h\) ;
- \(\mathcal{O}\) l'ontologie versionnée ;
- \(\mathcal{M}_{p,w}\) les instances de mesure dans \(w\) ;
- \(\mathcal{X}_{p,w}\) le contexte ;
- \(\mathcal{H}_{p,<t_0}\) l'histoire strictement antérieure ;
- \(\mathcal{E}_{p,w}\) l'évidence structurée (observations + provenance + qualité).

L'état cognitif est une application partielle :

\[
\mathrm{CS}(p,w) :
\mathcal{C} \;\rightharpoonup\;
\big(\hat\theta_{c},\, \sigma_{c},\, A_{c}\big)
\;\cup\;
\{\mathrm{Refusal}(c,k)\}
\]

Pas un vecteur de \(\mathbb{R}^{|\mathcal{C}|}\). Le caractère partiel est essentiel : le refus est dans le codomaine.

## 2. Définition opérationnelle

\[
\mathrm{CognitiveState}(p,t_0,h)
=
\mathrm{Inference}\big(\mathcal{O},\, \mathcal{M}_{p,w},\, \mathcal{X}_{p,w},\, \mathcal{H}_{p,<t_0},\, \mathcal{E}_{p,w}\big)
\]

`Inference` n'est pas une fonction numérique unique. C'est une procédure qui, pour chaque \(c \in \mathcal{C}\) demandé :

1. évalue l'admissibilité \(A(c,p,w) \in \{0,1\}\) ;
2. si \(A=0\), retourne \(\mathrm{Refusal}(c,k)\) ;
3. si \(A=1\), retourne \((\hat\theta_c, \sigma_c, A_c)\).

## 3. Admissibilité

\[
A(c,p,w)=1
\iff
\begin{aligned}[t]
& c \in \mathcal{O}
\;\wedge\;
\mathrm{role}(c)\neq\mathrm{diagnosis} \\
&\wedge\; \exists\, o\in\mathcal{E}_{c,p,w}:\; \mathrm{align}(o,c)\in\{\mathrm{exact},\mathrm{close}\} \\
&\wedge\; w \text{ est définie} \\
&\wedge\; \mathrm{context\_ok}(c,\mathcal{X}_{p,w}) \\
&\wedge\; \mathrm{prov\_ok}(\mathcal{E}_{c,p,w}) \\
&\wedge\; \mathrm{alts\_instantiated}(c)
\end{aligned}
\]

`context_ok` est vrai si les dimensions `requiresContext` sont présentes ou `declared_unknown`.  
`alts_instantiated` exige que les `mandatoryAlternatives` existent comme nœuds, pas qu'elles soient tranchées.

## 4. Factorisation conceptuelle

\[
\theta_{c,p,w}
=
f_c\!\left(
\kappa_{c,p},\;
s_{p,w},\;
x_{p,w},\;
e_{c,p,w}
\right)
\]

| Symbole | Nom | Échelle typique |
|---|---|---|
| \(\kappa_{c,p}\) | capacité (disposition) | lente |
| \(s_{p,w}\) | état transitoire (fatigue, arousal, …) | fenêtre |
| \(x_{p,w}\) | contexte | fenêtre |
| \(e_{c,p,w}\) | évidence utile à \(c\) | fenêtre |

\(f_c\) n'est pas spécifiée universellement. Contraintes :

- si \(e=\emptyset\), \(f_c\) n'est pas évaluée (refus) ;
- \(\kappa\) n'est pas identifiée à partir d'une seule fenêtre ;
- \(s\) et \(x\) sont distincts (nuit courte ≠ fatigue, même si la première informe la seconde).

## 5. Sortie canonique

Un estimateur compatible expose au minimum :

\[
\big(\hat\theta,\; \sigma,\; A,\; \mathcal{E}^{\mathrm{used}},\; \pi,\; k_{\mathrm{estimator}}\big)
\]

- \(A\) : alternatives actives ;
- \(\mathcal{E}^{\mathrm{used}}\) : observations effectivement utilisées ;
- \(\pi\) : enregistrement de provenance de l'activité d'inférence ;
- \(k_{\mathrm{estimator}}\) : identifiant de version de l'estimateur.

Deux sorties égales en \(\hat\theta\) et distinctes en \(k_{\mathrm{estimator}}\) sont deux objets.

## 6. Comparabilité

\((\hat\theta,w,x)\) et \((\hat\theta',w',x')\) sont comparables seulement si :

\[
c=c',\;
\mathrm{compatible}(h,h'),\;
\mathrm{noncontradict}(x,x'),\;
k=k' \;\text{ou écart déclaré},\;
\mathcal{O}=\mathcal{O}'
\]

Pas de distance euclidienne par défaut sur un vecteur d'états.

## 7. Ce que le formalisme refuse

- \(\mathrm{Attention}_p = 0.73 \in \mathbb{R}\) comme objet terminal ;
- une norme \(\|\mathrm{CS}\|\) comme « score cognitif global » ;
- l'identification \(\theta_{c} \equiv m\) pour une mesure \(m\).
