# Matrice de nouveauté

**Statut :** provisoire jusqu'à la revue de portée (phase B)  
**Règle :** une ligne `originale` qui tombe après une antériorité non citée est une erreur, pas une découverte.

Légende de la colonne HCSM :

- `héritage` — déjà un objet de premier rang ailleurs ; HCSM aligne
- `assemblage` — pièces existantes, combinaison peut-être originale
- `proposition` — objet de premier rang dans HCSM, à défendre
- `non revendiqué` — explicitement hors contribution

| Idée | Antériorité principale | Statut ailleurs | Statut HCSM | Commentaire |
|---|---|---|---|---|
| Distinguer construit et tâche | Cronbach & Meehl 1955 ; Cognitive Atlas 2011 | `ESTABLISHED` | héritage | |
| Matrice construits × unités d'analyse | RDoC 2010– | `ESTABLISHED` | héritage | |
| Développement + environnement comme dimensions | RDoC ; Casey et al. 2014 | `ESTABLISHED` | héritage | |
| Fonctionnement = interaction personne × contexte | ICF 2001 | `ESTABLISHED` | héritage | |
| Capacité ≠ performance | ICF | `ESTABLISHED` | héritage | |
| Phénotype observable formel | HPO | `ESTABLISHED` | héritage | |
| État latent + erreur de mesure | psychométrie, IRT, SEM | `ESTABLISHED` | héritage | |
| État vs trait | psychométrie classique | `ESTABLISHED` | héritage | |
| EMA / expérience momentanée | Shiffman et al. 2008 | `ESTABLISHED` | héritage | |
| Digital phenotyping | Onnela & Rauch 2016 ; Torous | `SUPPORTED` | héritage | canal, pas construit |
| Phénotype computationnel | Montague et al. 2012 ; Huys et al. 2016 | `SUPPORTED` | héritage | mesure dérivée |
| Réseaux de symptômes | Borsboom | `SUPPORTED` | héritage | famille d'inférence |
| Provenance formelle | PROV-O, FAIR | `ESTABLISHED` | héritage | rendue constitutive |
| Knowledge graph de la cognition | Atlas, CogPO, travaux Poldrack & Yarkoni | `ESTABLISHED` | héritage | |
| Fusion multimodale prédictive | littérature digital health | `SUPPORTED` | non revendiqué | prédire un score ≠ estimer un état |
| Intégration « première » multi-niveaux | — | déjà RDoC | non revendiqué | |
| Séparation computationnelle Knowledge / Evidence / Inference pour un état personnel T0 | pièces séparées, pas un contrat unique identifié ici | — | **proposition** | cœur |
| Evidence comme argument de premier rang de l'état | implicite en Bayes, rarement ontologisée | — | **proposition** | |
| `ConstructEstimate` comme unité (valeur + σ + alternatives + fenêtre + contexte + provenance) | pièces séparées | — | **assemblage** / **proposition** | l'originalité est le contrat, pas chaque champ |
| Refus d'estimer comme objet de même rang | rare dans les pipelines de scoring | — | **proposition** | |
| Unités d'analyse = voies d'évidence, pas étages | lecture RDoC | RDoC le permet | **assemblage** | utile si tenu jusqu'au schéma |
| Trois graphes superposés + moteur | KG + EMA + modèles latents existent séparément | — | **assemblage** | originalité conditionnelle à l'implémentation du contrat |
| Pont Atlas × RDoC × ICF × personne-temps | alignements 2 à 2 existent | partiel | **assemblage** | pas une super-ontologie |
| Projection ICF toujours hypothétique | esprit ICF | `ESTABLISHED` comme interdiction de déduire | héritage opérationnalisé | |
| Vocabulaire de statut épistémique dans le modèle | science ouverte, GRADE | `SUPPORTED` | héritage appliqué | |

## Lecture honnête

HCSM n'introduit presque aucun *concept* nouveau.  
Il introduit un **contrat** : ce qui compte comme état cognitif individuel représentable, et ce qui n'en est pas un.

Si la phase B trouve un cadre qui a déjà ce contrat (ontologie + évidence personnelle + inférence avec refus + contexte + fenêtre + provenance + pont fonctionnement, comme objets de premier rang), la colonne « proposition » redescend en « héritage » et la contribution se restreint encore.

C'est le résultat acceptable, et préférable à une originalité fictive.
