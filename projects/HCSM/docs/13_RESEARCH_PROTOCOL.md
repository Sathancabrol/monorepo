# 13 — Protocole de recherche

**Statut du document :** protocole de travail, à préenregistrer avant toute collecte  
**Couche :** SCIENTIFIC KNOWLEDGE  
**Version :** 0.1.0 · 2026-08-25

Ce n'est pas encore un protocole OSF figé. Toute collecte réelle exigera une version datée, un préenregistrement, et un avis éthique.

---

## 1. Objectif

Tester si HCSM améliore la *liaison* entre connaissances, mesures et inférences individuelles, par rapport aux scores multimodaux et aux cadres existants utilisés séparément.

## 2. Phases

### Phase A — Critique et formalisation (cette version)

- audit du document source ;
- état de l'art et matrice de nouveauté ;
- ontologie v0.1, modèle mathématique, schéma ;
- validateur de forme (V1).

Livrable : ce dépôt.

### Phase B — Revue systématique ciblée

Question : *Quels modèles computationnels d'état cognitif individuel multimodal existent-ils, et comment traitent-ils ontologie, incertitude, contexte, provenance ?*

- bases : PsycINFO, PubMed, Scopus, Web of Science, IEEE Xplore ;
- période : 2010–2026 (digital phenotyping, RDoC mature, computational psychiatry) ;
- type : revue de portée PRISMA-ScR, pas une méta-analyse d'efficacité ;
- extraction : construits, unités d'analyse, présence/absence de (ontologie, incertitude, contexte, provenance, refus, fonctionnement) ;
- lien avec le corpus [ETAT-DE-LART-PSYCHOLOGIE](https://github.com/Sathancabrol/ETAT-DE-LART-PSYCHOLOGIE) sans le dupliquer.

### Phase C — Étude de juges (V2, H1 H2 H4)

- participants : chercheurs en psychologie / neurosciences / psychométrie (N cible à fixer au préenregistrement, ordre de grandeur 30–60) ;
- devis : intra-sujet, ordre contrebalancé, matériaux identiques, formats (score nu vs `ConstructEstimate`) ;
- critères : erreurs de réification, calibration de la confiance, identification des alternatives ;
- préenregistrement OSF obligatoire ;
- pas de données cliniques de patients requises.

### Phase D — Étude empirique noyau (V3 V4 V5)

Hors de cette version. Conditions minimales pour l'ouvrir :

- construits limités à `attention`, `working_memory`, `fatigue` ;
- mesures alignées Atlas / tâches établies + EMA contexte/sommeil ;
- critère écologique préenregistré (performance de tâche quotidienne ou ICF d160 opérationnalisé) ;
- plan de refus testé sur sous-ensembles amputés ;
- éthique, consentement, minimisation, pas de diagnostic en sortie.

## 3. Critères d'inclusion / exclusion (phase B, esquisse)

**Inclus :** cadres ou systèmes qui estiment un état ou un profil cognitif / psychologique individuel à partir d'au moins deux voies, ou qui proposent une ontologie computationnelle de l'état.

**Exclus :** papiers de taxonomie pure sans individu ; classifieurs diagnostiques sans construit ; applications wellness sans modèle.

## 4. Biais et limites anticipés

- biais de familiarité des juges avec les tableaux de bord (phase C) ;
- WEIRD si phase D trop locale ;
- risque de *researcher allegiance* : les auteurs du modèle évaluent le modèle — prévoir des juges externes et des critères figés ;
- tentation d'élargir le noyau de construits avant d'avoir V2.

## 5. Éthique

HCSM v0.1 ne collecte rien.  
Dès la phase D : pas d'usage décisionnel, pas de feedback diagnostique aux participants, droit de retrait, pas de réidentification, séparation stricte evidence graph / identité civile.

## 6. Livrables scientifiques

1. Working paper de position (ce dépôt).  
2. Revue de portée (phase B).  
3. Étude de juges (phase C).  
4. Ontologie versionnée + validateur.  
5. Si et seulement si C est positif : protocole de phase D.

## 7. Ce qui arrête le programme

- V2 négatif (le format n'aide pas, ou nuit) ;
- impossibilité d'aligner le noyau sans déformer Atlas / ICF ;
- dérive vers un produit de scoring.

Un arrêt est un résultat. Il se documente dans `CHANGELOG.md` et `docs/14_LIMITATIONS.md`.
