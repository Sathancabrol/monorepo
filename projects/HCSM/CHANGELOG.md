# Changelog

Toutes les modifications notables de HCSM sont documentées ici.
Format inspiré de [Keep a Changelog](https://keepachangelog.com/).
Le versionnage suit SemVer pour le modèle et l'ontologie, indépendamment du code.

## [0.1.1] — 2026-08-25

### Added

- **Validateur V1** (`validator/`) : contrat de forme exécutable sur JSON.
  - Rejette scores nus, observations-comme-construits, projections ICF non-HYPOTHESIS,
    cibles diagnostiques, features digitales étiquetées cognition, PII, fenêtres mal formées,
    `ConstructEstimate` incomplets, `Refusal` avec valeur par défaut.
- **Admissibilité V5** : filtre pré-estimation (`NO_CONSTRUCT`, `NO_EVIDENCE`,
  `WINDOW_UNDEFINED`, `CONTEXT_MISSING`, `UNRESOLVED_ALTERNATIVES`, `MISALIGNED_MEASURE`,
  `PROVENANCE_BROKEN`).
- 23 cas synthétiques (valides / invalides / refus) + 29 tests unitaires.
- Mini-scénario docs/04 exécutable : attention estimable, working memory refusée.
- CLI : `python validator/validate.py --all`.

### Not added (volontaire)

- Aucun estimateur numérique (phase 2).
- Aucune UI, capteur, donnée réelle, API réseau.

---

## [0.1.0] — 2026-08-25

### Added

- Positionnement scientifique v2 : déplacement de la revendication de nouveauté.
- Distinction des objets : HCSM (modèle), Cognition Hub (système), Cognitorium (architecture globale).
- Vocabulaire de statut épistémique : `ESTABLISHED · SUPPORTED · PROPOSED · HYPOTHESIS · OPEN QUESTION`.
- Séparation des couches : Scientific Knowledge → Evidence → HCSM Model → Ontology → Computational Specification → Implementation.
- Documentation scientifique (`docs/00` à `docs/14`).
- Audit scientifique du document source Cognition Hub.
- État de l'art et matrice de nouveauté (Cognitive Atlas, RDoC, ICF, HPO, psychométrie, digital phenotyping).
- Modèle conceptuel HCSM : Knowledge / Evidence / Inference graphs.
- Ontologie v0.1 (`ontology/hcsm-v0.1.yaml`) : entités, relations, identifiants, provenance.
- Modèle mathématique de l'état cognitif à T0, incertitude et temporalité.
- Cadre de validation et protocole de recherche.
- Figures scientifiques (architecture, graphes, T0, trajectoire).
- Schéma de données, concept d'API et feuille de route d'implémentation.
- Working paper de position.

### Changed

- Unité fondamentale : plus un score `Attention = 0.73`, mais un objet d'estimation avec incertitude, preuves, contexte, fenêtre temporelle, référence populationnelle, provenance et explications alternatives.
- Architecture des niveaux : les unités d'analyse (biologique, physiologique, neurale, comportementale, subjective, contextuelle) ne sont plus des étages indépendants, mais des voies d'évidence d'un même construit.
- Formule conceptuelle : `CognitiveState(t) = Inference(Ontology, Measurements, Context, History, Evidence)`.

### Not claimed

- HCSM n'est pas « la première plateforme à intégrer cognition + psychologie + physiologie + neurologie ».
- HCSM n'est pas une nouvelle nosologie, ni un substitut de RDoC, ICF, Cognitive Atlas ou HPO.
