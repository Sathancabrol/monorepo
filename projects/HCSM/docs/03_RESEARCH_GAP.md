# 03 — Lacune de recherche

**Statut du document :** `PROPOSED` (lecture), s'appuie sur des constats `SUPPORTED`  
**Couche :** SCIENTIFIC KNOWLEDGE  
**Version :** 0.1.0 · 2026-08-25

---

## 1. Ce qui n'est pas une lacune

Les formulations suivantes sont des faux gaps. Elles décrivent des champs déjà peuplés.

- « On n'a pas encore intégré cognition, physiologie et neurologie. » — RDoC le fait comme cadre de recherche.
- « On n'a pas encore d'ontologie des processus cognitifs. » — Cognitive Atlas, CogPO.
- « On n'a pas encore de modèle du fonctionnement dans le contexte. » — ICF.
- « On n'a pas encore de phénotype formel. » — HPO.
- « On n'a pas encore de données temporelles in situ. » — EMA, digital phenotyping.
- « On n'a pas encore de variable latente. » — un siècle de psychométrie.

Présenter HCSM comme la réponse à l'un de ces faux gaps le rend trivialement réfutable.

## 2. La lacune réelle

Les cadres existent. Ils ne se parlent pas au niveau où une décision scientifique (ou, plus tard, une décision d'accompagnement) a lieu : **une personne, un moment, un ensemble de preuves hétérogènes**.

```
         DONNÉES
            │
  ┌─────────┼─────────┐
  ▼         ▼         ▼
psycho-   physio-   comporte-
métrie    logie     ment
  │         │         │
  └─────────┼─────────┘
            ▼
   fragmented evidence
            ▼
     ? couche manquante ?
            ▼
    structured inference
            ▼
      HUMAN STATE T0
            ▼
       FUNCTIONING
            ▼
       TRAJECTORY
```

La couche manquante n'est pas une énième taxonomie. C'est un **contrat d'inférence** :

1. typé par une ontologie de construits (knowledge) ;
2. nourri uniquement par des observations provenancées (evidence) ;
3. produisant des estimations avec incertitude et explications alternatives (inference) ;
4. situées dans un contexte et une fenêtre temporelle ;
5. projetables vers un fonctionnement ICF, pas vers un diagnostic.

## 3. Cinq décalages concrets

### 3.1. Réification de la mesure — `SUPPORTED`

On publie et on industrialise `Attention = 73 %` à partir d'un CPT, d'un questionnaire ou d'une feature smartphone. Le construit, l'instrument, l'état et la personne s'effondrent en un scalaire. Cronbach & Meehl l'interdisent depuis 1955 ; la pratique continue.

HCSM rend cette réification *structurellement coûteuse* : un `ConstructEstimate` incomplet n'est pas un résultat.

### 3.2. Confusion connaissance / personne — `SUPPORTED`

Le Cognitive Atlas dit ce qu'est l'attention pour la science. Un test dit ce qu'une personne a fait un mardi matin. Rien, dans les cadres existants, n'empêche de coller la définition scientifique sur le résultat individuel comme s'ils avaient le même statut.

HCSM force le passage par l'inférence, donc par l'incertitude et les alternatives.

### 3.3. Niveaux empilés au lieu de voies d'évidence — `SUPPORTED`

« État neurologique » à côté de « état cognitif » reproduit une pile que RDoC a précisément défaite. Un EEG et un temps de réaction ne sont pas deux étages ; ce sont deux preuves d'un même construit, de qualités différentes.

### 3.4. Contexte comme métadonnée, pas comme argument — `SUPPORTED`

L'ICF met le contexte au centre du fonctionnement. Les pipelines de digital phenotyping le mettent souvent en colonne annexe. Un état d'attention sous restriction de sommeil n'est pas le même objet qu'un état d'attention après une nuit normale. S'ils reçoivent le même identifiant, le modèle ment.

### 3.5. Absence de refus d'estimer — `PROPOSED` comme norme HCSM

Les systèmes de scores produisent toujours un nombre. Un cadre scientifique doit pouvoir dire : *évidence insuffisante, fenêtre mal définie, explications alternatives non départagées — pas d'estimation*.

Ce refus est une feature, pas une limite d'implémentation.

## 4. Ce que combler la lacune ne signifie pas

Combler la lacune ne signifie pas fusionner RDoC, ICF et Cognitive Atlas dans une super-ontologie. Une fusion abusive perdrait :

- la vocation de recherche de RDoC ;
- la vocation fonctionnelle de l'ICF ;
- la vocation conceptuelle de l'Atlas.

HCSM est un **alignement opérationnel**, pas une unification théorique. Les identifiants externes restent premiers. Les identifiants HCSM sont des ponts.

## 5. Critère de succès scientifique

HCSM réussit si, et seulement si, on peut montrer empiriquement au moins l'un des points suivants (`HYPOTHESIS`, voir validation) :

1. des juges experts font moins d'erreurs de réification avec un `ConstructEstimate` qu'avec un score nu ;
2. l'ajout de contexte + fenêtre temporelle + alternatives améliore une prédiction de fonctionnement (ICF performance) au-delà des scores seuls ;
3. le système refuse d'estimer dans des cas où un pipeline de scores produit un faux positif d'état ;
4. l'alignement Atlas / RDoC / ICF / HPO est opérationnel sans perte sémantique majeure sur un sous-ensemble de construits (attention, mémoire de travail, fatigue).

Si aucun de ces tests ne passe, HCSM reste une architecture conceptuelle utile à la discussion, pas une contribution empirique.

## 6. Périmètre volontairement étroit pour T0

La v0.1 se concentre sur **T0** : une coupe. La trajectoire est spécifiée (docs/08) mais n'est pas l'objet de la première validation. Étendre trop tôt à la dynamique reviendrait à empiler une originalité non testée sur une originalité non testée.
