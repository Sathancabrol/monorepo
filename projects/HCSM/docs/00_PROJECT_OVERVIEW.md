# 00 — Vue d'ensemble du projet

**Statut du document :** `PROPOSED`  
**Couche :** SCIENTIFIC KNOWLEDGE / HCSM MODEL  
**Version :** 0.1.0 · 2026-08-25

---

## 1. Objet

HCSM (Human Cognitive State Model) est un cadre scientifique pour représenter l'état cognitif d'une personne à un instant T0 comme un **objet latent, multimodal, contextualisé, temporel et evidential**.

Il répond à une question précise :

> Comment relier, sans les confondre, (i) ce que la science sait d'un construit cognitif, (ii) ce qui a été mesuré chez une personne, et (iii) ce que l'on peut inférer sur son état, son fonctionnement et sa trajectoire ?

Cette question n'est pas « comment obtenir un meilleur score d'attention ». Elle est « comment ne pas prendre une mesure pour un état, ni un état pour une capacité, ni une capacité pour un fonctionnement ».

## 2. Trois noms, trois objets

Le document source « Cognition Hub » mélangeait parfois le système, le modèle et l'écosystème. HCSM les sépare.

```
Cognitorium
  architecture globale
  connaissances · compétences · expériences · trajectoires
        │
        │  consomme
        ▼
  Cognition Hub
  système computationnel
  graphes · API · provenance · interfaces
        │
        │  instancie
        ▼
     HCSM
  modèle scientifique
  ontologie · évidence · inférence · T0 · incertitude
```

- **HCSM** fixe ce qui est représentable, ce qui est estimable, et sous quelles hypothèses.
- **Cognition Hub** est l'implémentation de ce modèle (hors phase actuelle).
- **Cognitorium** reste le cadre plus large dans lequel un état HCSM devient une ressource pour l'orientation, l'apprentissage ou le suivi.

## 3. Périmètre de la version 0.1

Inclus :

- positionnement scientifique et déplacement de la nouveauté ;
- état de l'art et cartographie des antériorités ;
- modèle conceptuel à trois graphes ;
- ontologie v0.1 (classes, relations, identifiants, provenance) ;
- modèle mathématique de l'état à T0 ;
- modèles d'évidence, d'inférence, de temps, d'incertitude, de contexte et de fonctionnement ;
- cadre de validation et protocole de recherche ;
- spécification computationnelle (schéma, API conceptuelle, roadmap).

Exclus (volontairement) :

- implémentation logicielle ;
- recueil de données personnelles ;
- usage clinique ou décisionnel ;
- prétention à une nosologie nouvelle ;
- figures « produit » ou tableau de bord psychologique.

## 4. Unité fondamentale

L'unité n'est pas un scalaire. C'est un **ConstructEstimate** :

| Champ | Rôle |
|---|---|
| `construct` | Construit ontologique (ex. attention) |
| `value` | Estimation latente, jamais une mesure brute |
| `uncertainty` | Dispersion, intervalle, ou distribution |
| `evidence` | Observations qui portent l'estimation |
| `measures` | Instruments / tâches / capteurs |
| `context` | État, charge, sommeil, environnement, tâche |
| `temporal_window` | Fenêtre sur laquelle l'estimation est définie |
| `population_reference` | Norme ou modèle de référence, s'il existe |
| `provenance` | Qui a mesuré, comment, quand, avec quel traitement |
| `alternative_explanations` | Hypothèses concurrentes non éliminées |

`Attention = 0.73` n'est pas une sortie légitime de HCSM. C'est une composante d'un objet plus large, et seulement si les autres champs sont renseignés.

## 5. Architecture en couches

```
SCIENTIFIC KNOWLEDGE     ce que la littérature établit sur les construits
        ↓
    EVIDENCE             ce qui a été observé, avec qualité et provenance
        ↓
    HCSM MODEL           comment on infère un état à partir de l'évidence
        ↓
    ONTOLOGY             vocabulaire formel des entités et relations
        ↓
COMPUTATIONAL SPEC       schéma, API, contraintes d'implémentation
        ↓
    IMPLEMENTATION       Cognition Hub (phase ultérieure)
```

Une implémentation qui calcule un score sans passer par l'ontologie, l'évidence et l'incertitude n'instancie pas HCSM.

## 6. Hypothèses de travail (à tester, pas à croire)

Ces énoncés sont des `HYPOTHESIS`, pas des résultats.

- **H1** — Un état cognitif personnel n'est pas réductible à un profil de scores, même multimodal.
- **H2** — La séparation Knowledge / Evidence / Inference réduit les erreurs de réification (prendre une mesure pour un construit, un construit pour une personne).
- **H3** — L'ajout explicite du contexte et de la fenêtre temporelle améliore la validité écologique des estimations par rapport à un agrégat de tests.
- **H4** — Un graphe d'inférence avec explications alternatives est plus fidèle scientifiquement qu'un score unique, même moins « actionnable ».
- **H5** — HCSM apporte une plus-value mesurable par rapport à l'usage séparé de RDoC, ICF et Cognitive Atlas, précisément sur la liaison personne-niveau (état T0), pas sur la taxonomie des construits.
- **H6** — La qualité de l'inférence est limitée par la qualité et la couverture de l'évidence ; le modèle doit refuser d'estimer plutôt que d'inventer.

Le programme qui les teste est dans `docs/12_VALIDATION_FRAMEWORK.md` et `docs/13_RESEARCH_PROTOCOL.md`.

## 7. Public

HCSM s'adresse d'abord à :

- chercheurs en psychologie, neurosciences, psychométrie, psychiatrie computationnelle ;
- concepteurs d'ontologies et de knowledge graphs biomédicaux ;
- équipes qui construisent des outils de phénotypage numérique et veulent éviter la réification des scores.

Il ne s'adresse pas, en v0.1, aux patients, aux prescripteurs, ni aux systèmes de décision automatique.

## 8. Documents liés

- Position : `docs/01_SCIENTIFIC_POSITION.md`
- Antériorités : `docs/02_STATE_OF_THE_ART.md`, `research/novelty-matrix.md`
- Audit du document source : `research/scientific-audit.md`
- Modèle : `docs/04_HCSM_CONCEPTUAL_MODEL.md`
- Working paper : `papers/working-paper/HCSM_working_paper.md`
