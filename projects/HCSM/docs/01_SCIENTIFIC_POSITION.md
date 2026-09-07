# 01 — Position scientifique

**Statut du document :** `PROPOSED`  
**Couche :** SCIENTIFIC KNOWLEDGE  
**Version :** 0.1.0 · 2026-08-25

Ce document fixe ce que HCSM revendique, ce qu'il refuse de revendiquer, et pourquoi le document source « Cognition Hub » devait être repositionné.

---

## 1. Diagnostic du document source

Le document « COGNITION HUB — Vers une représentation multidimensionnelle et dynamique de l'état cognitif humain à T0 » pose une thèse forte et globalement juste :

> le véritable objet n'est pas un score cognitif, mais une ontologie dynamique de l'état cognitif humain, avec estimation, contexte, temporalité, provenance et incertitude.

Cette thèse est **conservée**. Ce qui ne l'est pas, c'est la manière dont la nouveauté y était parfois formulée.

### Ce qui était déjà là, et qu'il ne faut plus présenter comme nouveau

| Formulation à risque dans le document source | Pourquoi elle est réfutable | Cadre déjà existant |
|---|---|---|
| Première intégration cognition + psychologie + physiologie + neurologie | RDoC intègre déjà des construits à travers gènes, molécules, cellules, circuits, physiologie, comportement, auto-évaluations | RDoC (Insel et al., 2010 ; Cuthbert & Insel, 2013) |
| Fonctionnement humain nécessairement contextualisé | C'est le cœur de l'ICF : fonction ↔ activité ↔ participation ↔ environnement | ICF (WHO, 2001) |
| Carte des concepts et des tâches cognitives | C'est l'objet du Cognitive Atlas (concepts vs tasks, relations *measured-by*) | Poldrack et al., 2011 |
| Phénotypes cognitifs formalisés | HPO organise déjà des phénotypes observables, y compris comportementaux | Köhler et al., 2024 |
| Mesure continue in situ | Digital phenotyping et EMA le font depuis plus d'une décennie | Onnela & Rauch, 2016 ; Shiffman et al., 2008 |

Le document source **reconnaissait déjà** ces filiations. Il ne les utilisait pas assez pour borner sa propre contribution. Résultat : des phrases qui sonnent comme une fondation alors qu'elles décrivent un héritage.

L'audit affirmation par affirmation est dans `research/scientific-audit.md`.

## 2. Ce que HCSM ne revendique pas

HCSM ne revendique **pas** :

1. d'être le premier cadre à penser la cognition à plusieurs niveaux d'analyse ;
2. d'être une ontologie cognitive plus complète que le Cognitive Atlas ;
3. d'être une nosologie alternative à RDoC ou au DSM/CIM ;
4. de calculer un état neurologique comme niveau parallèle au cognitif ;
5. de produire un score unique d'état cognitif actionnable cliniquement ;
6. de résoudre le problème de validité écologique par la seule multiplication des capteurs.

Ces non-revendications sont des contraintes scientifiques, pas de la modestie rhétorique. Une revue les testera en premier.

## 3. Là où se trouve réellement la contribution

Il faut distinguer quatre objets que la littérature traite souvent séparément :

```
SCIENCE EXISTANTE
       │
       ├── Knowledge          ontologies, théories, construits
       │     Cognitive Atlas · RDoC · HPO · ICF
       │
       ├── Measurement        tests, EEG, HRV, questionnaires, comportement
       │
       └── Function           fonctionnement humain contextualisé (ICF)
                 │
                 ▼
            HCSM / Cognition Hub
       Knowledge → Measurement → Inference → State T0
                 → Context → Function → Trajectory
```

La séparation **Knowledge → Measurement → Inference → Function** est la contribution conceptuelle principale (`PROPOSED`).

Elle résout un problème que ni RDoC, ni l'ICF, ni le Cognitive Atlas ne traitent comme objet computationnel de premier rang :

> ne pas confondre ce que la science sait sur une fonction avec ce que l'on peut réellement inférer sur une personne, à un moment donné, à partir des preuves disponibles.

RDoC organise la *recherche* sur des construits.  
L'ICF organise le *fonctionnement* dans un contexte.  
Le Cognitive Atlas organise les *concepts et les tâches*.  
HCSM organise l'*inférence personnelle temporelle* qui relie les trois.

C'est une couche, pas un remplacement.

## 4. Déplacement du modèle conceptuel

### 4.1. Ce que le document source proposait

```
Capacity × State × Context
```

Cette factorisation est utile (`SUPPORTED` comme intuition, `PROPOSED` comme modèle). Elle manque une dimension sans laquelle elle redevient un score habillé :

```
Evidence
```

### 4.2. Formulation retenue

Au niveau d'un construit \(c\) au temps \(t\) :

\[
State_{c,t} = f(Capacity_c,\; State_t,\; Context_t,\; Evidence_t)
\]

Au niveau de la personne :

\[
\mathrm{CognitiveState}(t) = \mathrm{Inference}(\mathrm{Ontology},\; \mathrm{Measurements},\; \mathrm{Context},\; \mathrm{History},\; \mathrm{Evidence})
\]

Cette seconde formule est la définition opérationnelle de HCSM (`PROPOSED`).

Elle force six distinctions :

| Objet | Question | Graphe |
|---|---|---|
| Ontologie | Qu'est-ce que l'attention, pour la science ? | Knowledge |
| Mesure | Qu'a-t-on observé ? | Evidence |
| Estimation | Que peut-on en conclure ? | Inference |
| Preuve | Avec quelle force, quelles sources ? | Evidence + Inference |
| Contexte | Dans quelles conditions ? | Evidence + Inference |
| Temps | Sur quelle fenêtre ? | Temporal model |

## 5. Correction de l'« état neurologique »

Le document source proposait une pile :

```
biologique → physiologique → psychologique → cognitif → neurologique → comportement → environnement
```

Cette pile est conceptuellement instable. « Neurologique » n'est pas un niveau parallèle à « cognitif ». Un même construit (attention, mémoire de travail, valence négative) peut être étudié à plusieurs *unités d'analyse*. C'est exactement l'apport de RDoC (`ESTABLISHED`).

Architecture retenue :

```
                    COGNITIVE CONSTRUCT
                           │
     ┌─────────────────────┼─────────────────────┐
     ▼                     ▼                     ▼
 BIOLOGICAL          PHYSIOLOGICAL            NEURAL
  EVIDENCE             EVIDENCE              EVIDENCE
     │                     │                     │
     └─────────────────────┼─────────────────────┘
                           ▼
                    BEHAVIORAL DATA
                           │
                           ▼
                    SUBJECTIVE DATA
                           │
                           ▼
                    CONTEXTUAL DATA
                           │
                           ▼
                  LATENT ESTIMATION
                           │
                           ▼
                     FUNCTIONING
```

Les unités d'analyse sont des **voies d'évidence**, pas des étages ontologiques indépendants. Un EEG n'est pas « plus neurologique » qu'un temps de réaction : les deux parlent, différemment, du même construit, avec des biais différents.

## 6. Phrase centrale

Le document source contient déjà la phrase qui doit porter le papier :

> « L'enjeu scientifique n'est alors plus simplement de mesurer davantage. Il est de relier correctement ce qui est déjà mesuré. »

HCSM se juge à cette phrase. S'il n'améliore pas la *liaison* entre connaissances, mesures, inférences et fonctionnement, il n'a pas de contribution, même avec une belle ontologie.

## 7. Critère de nouveauté admissible

Une idée n'est originale ici que si elle satisfait les trois conditions suivantes :

1. elle n'est pas déjà un objet de premier rang dans RDoC, ICF, Cognitive Atlas, HPO, ou les cadres de digital phenotyping ;
2. elle porte sur la *liaison computationnelle* entre ces cadres, au niveau d'une personne et d'un temps T0 ;
3. elle est formulée de façon falsifiable (voir H1–H6 dans `docs/00_PROJECT_OVERVIEW.md`).

La matrice complète est dans `research/novelty-matrix.md`.

## 8. Conséquence pour l'écriture scientifique

- Toute phrase du type « pour la première fois » est interdite tant que la matrice de nouveauté ne l'autorise pas.
- Toute sortie numérique est un `ConstructEstimate`, jamais un score nu.
- Toute référence à un niveau « neurologique » indépendant est remplacée par une unité d'analyse.
- Toute filiation (RDoC, ICF, Atlas, HPO) est citée avant la proposition HCSM correspondante.
