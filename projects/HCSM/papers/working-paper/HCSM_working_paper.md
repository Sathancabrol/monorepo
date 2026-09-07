# Relier plutôt que mesurer davantage

## HCSM : un contrat d'inférence pour l'état cognitif humain à T0

**Document de travail · position paper · v0.1.0 · 25 août 2026**  
**Statut global :** `PROPOSED` — aucune hypothèse H1–H6 n'est un résultat.  
**Modèle :** Human Cognitive State Model (HCSM)  
**Système visé :** Cognition Hub  
**Écosystème :** Cognitorium  

> L'enjeu scientifique n'est alors plus simplement de mesurer davantage.  
> Il est de relier correctement ce qui est déjà mesuré.

---

### Résumé

Les cadres contemporains de la cognition et du fonctionnement humain sont riches et, pour l'essentiel, déjà là. Le Cognitive Atlas distingue construits et tâches. RDoC articule un même construit à plusieurs unités d'analyse, avec le développement et l'environnement comme dimensions. L'ICF interdit d'inférer le fonctionnement d'un diagnostic et sépare capacité et performance. HPO formalise des phénotypes observables. La psychométrie estime des états latents avec erreur. L'EMA et le digital phenotyping produisent des observations temporelles in situ.

Ce qui manque n'est pas une énième carte de la cognition, ni « la première intégration » de la psychologie, de la physiologie et de la neurologie — revendication réfutable. Ce qui manque est un **contrat computationnel** précisant ce qui compte comme *état cognitif d'une personne, à un moment, à partir de preuves hétérogènes*.

HCSM propose ce contrat. Un état n'est pas un score. C'est une inférence typée par une ontologie, nourrie seulement d'observations provenancées, située dans une fenêtre et un contexte, accompagnée d'une incertitude et d'explications alternatives, et capable de **refuser** d'estimer. Cognition Hub est le système qui devra instancier ce contrat. Cognitorium peut en consommer les sorties, pas les réécrire.

Trois graphes restent séparés : connaissance, évidence, inférence. Les unités d'analyse sont des voies d'évidence, pas des étages. La projection vers le fonctionnement ICF est toujours une hypothèse.

Le papier déplace la nouveauté, formalise le modèle, borne un noyau de construits, et définit un programme de validation dont l'échec possible est un résultat acceptable.

**Mots-clés :** état cognitif ; ontologie ; évidence ; inférence ; incertitude ; provenance ; RDoC ; ICF ; Cognitive Atlas ; digital phenotyping

---

## 1. Problème

On sait de mieux en mieux *mesurer*. Tests, questionnaires, EEG, HRV, EMA, capteurs passifs : les voies se multiplient. On sait aussi, depuis longtemps, que mesurer n'est pas représenter un construit (Cronbach & Meehl, 1955), qu'un construit n'est pas une personne, et qu'une personne n'est pas son fonctionnement dans la vie (WHO, 2001).

Pourtant la pratique — y compris savante, surtout industrielle — continue de produire des objets du type :

```
Attention = 0.73
```

parfois habillés d'un intervalle, rarement d'un contexte, presque jamais d'une provenance complète, presque jamais d'un droit de ne pas conclure.

Le document de travail « Cognition Hub » identifiait déjà le bon objet : non pas un score, mais une représentation dynamique de l'état cognitif, avec estimation, contexte, temporalité, provenance et incertitude. Il posait aussi, trop tôt, une vitrine intenable : celle d'une intégration inédite des niveaux cognitif, psychologique, physiologique et neurologique.

Cette vitrine est facile à détruire. RDoC fait déjà le travail d'intégration des niveaux comme cadre de *recherche* (Insel et al., 2010 ; Cuthbert & Insel, 2013). L'ICF fait déjà le travail du fonctionnement contextualisé. Le Cognitive Atlas fait déjà le travail du vocabulaire des concepts et des tâches (Poldrack et al., 2011). HPO fait déjà le travail du phénotype observable (Köhler et al., 2024).

La question n'est donc pas : *que manque-t-il à la science de la cognition ?*  
Elle est : *que manque-t-il au moment où ces sciences doivent parler d'une personne, maintenant, avec les preuves qu'on a ?*

## 2. Ce que les cadres existants tiennent — et s'arrêtent de tenir

### 2.1. Knowledge

Le Cognitive Atlas, dans la lignée de Cronbach et Meehl, sépare concepts mentaux et tâches, et relie les seconds aux premiers par des relations du type *measured-by*. C'est le bon graphe de *ce que la science sait*. Il n'a pas à devenir un graphe de personnes.

### 2.2. Niveaux

RDoC organise des construits (attention, working memory, valence, arousal, …) selon des unités d'analyse (du gène à l'auto-évaluation) et refuse le diagnostic comme variable indépendante. Développement et environnement sont des dimensions, pas des notes de bas de page. HCSM en hérite une leçon stricte : « neurologique » n'est pas un étage parallèle à « cognitif ». Un EEG et un temps de réaction sont deux voies, pas deux ontologies.

### 2.3. Function

L'ICF décrit le fonctionnement comme interaction entre fonctions/structures, activités/participation, et facteurs contextuels. On n'infère pas une restriction de participation à partir d'une atteinte, ni une atteinte à partir d'un diagnostic. Capacité et performance ne coïncident pas.

### 2.4. Observation temporelle

EMA (Shiffman, Stone & Hufford, 2008) et digital phenotyping (Onnela & Rauch, 2016) donnent enfin du temps et du dehors-laboratoire. Ils ne donnent pas, à eux seuls, un construit. Une feature de smartphone n'est pas de l'anhédonie. Un temps d'écran n'est pas de l'attention.

### 2.5. Latent

Psychométrie, modèles à état-espace, psychiatrie computationnelle (Montague et al., 2012) estiment déjà ce qui n'est pas observé. Ils le font rarement sous un contrat qui force à la fois une ontologie externe, un contexte, une fenêtre, une provenance et un refus.

### 2.6. Le trou

Les pièces existent. Le **contrat d'assemblage au niveau personne-temps** n'est pas un objet de premier rang. C'est le seul endroit où HCSM revendique quelque chose — et encore : comme proposition, jusqu'à ce qu'une revue de portée montre qu'un cadre équivalent existe déjà.

## 3. Contribution (et non-contribution)

HCSM contribue un contrat, pas une nosologie.

**Revendiqué (`PROPOSED`) :**

1. la séparation computationnelle Knowledge / Evidence / Inference comme condition de représentation d'un état personnel ;
2. l'évidence comme argument de premier rang, au même titre que la capacité, l'état transitoire et le contexte ;
3. le `ConstructEstimate` (valeur, incertitude, preuves, mesures, contexte, fenêtre, référence, provenance, alternatives) comme unité, et le `Refusal` comme unité de même rang ;
4. les unités d'analyse comme voies d'évidence, jusqu'au schéma de données.

**Non revendiqué :**

- être le premier à intégrer plusieurs niveaux ;
- remplacer Atlas, RDoC, ICF, HPO ;
- calculer un état neurologique ;
- produire un score cognitif global ou un diagnostic ;
- avoir validé empiriquement H1–H6.

## 4. Modèle

### 4.1. Définition

\[
\mathrm{CognitiveState}(t)
=
\mathrm{Inference}(\mathrm{Ontology},\; \mathrm{Measurements},\; \mathrm{Context},\; \mathrm{History},\; \mathrm{Evidence})
\]

Pour un construit \(c\) :

\[
State_{c,t}
=
f(Capacity_c,\; State_t,\; Context_t,\; Evidence_t)
\]

\(t\) n'est légal que comme centre d'une fenêtre \(w=(t_0,h)\).

L'état est une application *partielle* des construits vers des estimations ou des refus. Le caractère partiel n'est pas une limitation d'ingénierie.

### 4.2. Trois graphes

Un graphe unique force la confusion des statuts.

- **Knowledge** — construits, sous-processus, théories, tâches, littérature, alignements. Aucune personne.
- **Evidence** — personne opaque, observations, signaux, contexte, provenance. Aucun construit comme valeur.
- **Inference** — estimations, incertitudes, alternatives, refus, projections ICF. Toute arête y est, par défaut, une hypothèse.

Cognition Hub est le moteur qui relie les trois sans les fusionner.

### 4.3. Voies, pas étages

```
                 CONSTRUCT
                    │
    biological  physiological  neural  behavioral  subjective  contextual
                    │
              latent estimation  or  refusal
                    │
           functioning projection?  (HYPOTHESIS)
```

Les voies gènes / molécules / cellules sont hors v0.1. Elles resteraient des voies.

### 4.4. Unité

L'unité n'est pas `Attention = 0.73`. C'est un objet dont l'absence d'incertitude, d'évidence, de fenêtre, de contexte ou de provenance est une erreur de type.

Les alternatives minimales pour l'attention (fatigue, arousal, motivation, difficulté de la tâche, pression de sommeil) doivent être *instanciées*, non nécessairement tranchées. Si elles sont indiscernables, l'incertitude augmente ou l'estimation est refusée.

### 4.5. Working model statistique

Une fusion bayésienne simple par voie, avec inflation d'incertitude en cas de divergence et d'alternatives non départagées, sert de placeholder (`model/latent-state-model.md`). Ce n'est pas la contribution. N'importe quel estimateur qui respecte le contrat peut le remplacer.

## 5. Ontologie v0.1

HCSM n'est pas une ontologie de la cognition. C'est une ontologie de l'état estimé. Les identifiants Atlas, RDoC, ICF, HPO restent premiers. `owl:sameAs` est interdit en v0.1.

Noyau volontairement petit : `attention`, `working_memory`, `cognitive_control`, et les modulateurs `fatigue`, `arousal`, `sleep_pressure`.

Un n-back n'est pas un *exactMatch* de la mémoire de travail. ICF `b144` non plus. Ces écarts sont le genre de chose qu'une super-ontologie « pratique » efface, et qu'HCSM doit conserver.

Le refus a des codes (`NO_EVIDENCE`, `WINDOW_UNDEFINED`, `CONTEXT_MISSING`, `UNRESOLVED_ALTERNATIVES`, `MISALIGNED_MEASURE`, `PROVENANCE_BROKEN`, `NO_CONSTRUCT`). Un pipeline qui a toujours un nombre n'implémente pas HCSM.

## 6. Du T0 au fonctionnement, sans déduction

Une estimation d'attention basse, même riche, ne *devient* pas une restriction de participation. La projection ICF (`b140`, `d160`, …) est une `FunctionalProjection` de statut forcé `HYPOTHESIS`. Cognitorium, s'il relie ces projections à des compétences ou des parcours, lit l'inference graph ; il n'y écrit pas.

## 7. Programme empirique

HCSM n'est pas validé. Cinq niveaux sont définis :

| Niveau | Objet |
|---|---|
| V0 | cohérence conceptuelle et matrice de nouveauté |
| V1 | validateur de forme : les objets illégaux ne passent pas |
| V2 | juges : le format réduit-il la réification ? |
| V3 | fidélité / validité sur le noyau |
| V4 | gain écologique préenregistré vs scores seuls |
| V5 | le refus se déclenche-t-il quand il le doit ? |

Six hypothèses (H1–H6) sont énoncées pour être détruites. En particulier : si tout le gain d'un futur modèle vient d'avoir plus de features, H5 échoue, et HCSM n'a pas de plus-value scientifique.

Aucune donnée personnelle n'accompagne cette version. La prochaine implémentation licite est un validateur, pas une application.

## 8. Limites

Cartographie, pas revue systématique : une antériorité peut faire redescendre la nouveauté. Noyau étroit. Estimateur placeholder. Document source non versé in extenso. Pas d'implémentation. Risque prévisible qu'on extraie `value` et qu'on jette le contrat. Un format plus honnête peut même *augmenter* la confiance injustifiée. Ces limites sont détaillées dans `docs/14_LIMITATIONS.md`.

## 9. Conclusion

On n'avait pas besoin d'une nouvelle carte de l'esprit. On avait besoin d'un endroit où il soit *structurellement coûteux* de prendre une mesure pour un construit, un construit pour une personne, et une personne pour son fonctionnement.

HCSM essaie d'être cet endroit. S'il n'y parvient pas sous les tests qu'il s'impose, il devra se retirer ou se réduire. Ce serait, scientifiquement, une issue propre — et préférable à un tableau de bord.

---

## Références

Voir `papers/references/bibliography.md`.

Citations structurantes : Cronbach & Meehl (1955) ; WHO (2001) ; Insel et al. (2010) ; Poldrack et al. (2011) ; Cuthbert & Insel (2013) ; Shiffman et al. (2008) ; Montague et al. (2012) ; Onnela & Rauch (2016) ; Wilkinson et al. (2016) ; Köhler et al. (2024).
