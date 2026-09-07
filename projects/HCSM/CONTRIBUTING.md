# Contribuer à HCSM

HCSM est un projet de recherche, pas un dépôt de code produit. Toute contribution doit préserver la séparation des couches et le statut épistémique des affirmations.

## Couches (ne pas les mélanger)

```
SCIENTIFIC KNOWLEDGE
        ↓
    EVIDENCE
        ↓
    HCSM MODEL
        ↓
    ONTOLOGY
        ↓
COMPUTATIONAL SPECIFICATION
        ↓
    IMPLEMENTATION
```

- Un résultat empirique publié va dans `scientific/literature/`.
- Une observation ou une mesure va dans le modèle d'évidence, pas dans l'ontologie.
- Une décision de conception logicielle va dans `specs/`, pas dans `docs/`.
- Du code n'entre dans ce dépôt que s'il implémente une spécification déjà écrite.

## Statuts épistémiques

Chaque affirmation importante porte l'un de ces statuts :

| Statut | Signification | Peut être cité comme fait ? |
|---|---|---|
| `ESTABLISHED` | Consensus scientifique large, sources primaires stables | Oui, avec référence |
| `SUPPORTED` | Appuyé par des résultats convergents, encore débattu | Oui, avec nuances |
| `PROPOSED` | Proposition HCSM, pas encore testée | Non, uniquement comme proposition |
| `HYPOTHESIS` | Hypothèse falsifiable du programme de recherche | Non |
| `OPEN QUESTION` | Question ouverte, pas de position prise | Non |

Une pull request qui présente une proposition comme un fait établi sera refusée.

## Comment ajouter du contenu

1. Identifier la couche et le statut.
2. Citer des sources avec DOI quand elles existent.
3. Distinguer explicitement : ce que la science sait d'un construit / ce qui a été mesuré / ce qui est estimé / avec quelle preuve.
4. Ne pas inventer de nouveauté. Si une idée existe déjà (RDoC, ICF, Cognitive Atlas, HPO, digital phenotyping), la ranger dans la matrice de nouveauté (`research/novelty-matrix.md`).
5. Mettre à jour `CHANGELOG.md`.

## Ce que ce dépôt n'accepte pas

- Scores cognitifs présentés comme des mesures directes (`Attention = 73 %`).
- Revendications du type « première intégration cognition + physiologie + neurologie ».
- Exploits, données personnelles, phénotypes individuels réels.
- Implémentation avant spécification.

## Langue

La documentation de recherche est rédigée en français, avec termes techniques anglais conservés (construct, evidence, provenance, latent state). Les identifiants d'ontologie et le schéma de données sont en anglais.
