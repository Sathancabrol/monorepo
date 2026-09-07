# Feuille de route d'implémentation

**Couche :** COMPUTATIONAL SPECIFICATION  
**Statut :** `PROPOSED`  
**Règle :** pas d'implémentation avant que la couche correspondante soit écrite.

```
SCIENTIFIC KNOWLEDGE
        ↓
    EVIDENCE
        ↓
    HCSM MODEL
        ↓
    ONTOLOGY
        ↓
COMPUTATIONAL SPECIFICATION     ← nous sommes ici pour le logiciel
        ↓
    IMPLEMENTATION              ← Cognition Hub, plus tard
```

## Phase 0 — ce dépôt (fait)

- position, audit, état de l'art, gap ;
- modèle à trois graphes ;
- ontologie v0.1 + schéma ;
- working paper de position ;
- protocole de validation.

## Phase 1 — validateur V1 (**fait** · v0.1.1)

- lire `hcsm-v0.1.yaml` + JSON d'exemples ;
- rejeter les objets interdits ;
- jeux de cas synthétiques pour V5 (refus).
- **Livré :** `validator/` — CLI, schéma V1, admissibilité V5, 23 cas, 29 tests.

Pas d'UI. Pas de capteurs. Pas de personnes réelles.

```bash
cd validator && pip install -r requirements.txt
python validate.py --all
python -m pytest tests/ -q
```

## Phase 2 — moteur d'inférence placeholder (**prochaine**)

- working model `model/latent-state-model.md` ;
- uniquement données synthétiques ;
- traces PROV.

## Phase 3 — étude de juges (hors code produit)

- matériaux V2 ;
- préenregistrement OSF ;
- pas de « démo produit ».

## Phase 4 — revue de portée

- corpus des modèles d'état individuel ;
- mise à jour de la matrice de nouveauté ;
- éventuellement abaisser des `proposition` en `héritage`.

## Phase 5 — seulement si V2 n'échoue pas

- protocole éthique phase D ;
- acquisition minimale attention / WM / fatigue ;
- comparaison préenregistrée vs scores seuls.

## Hors route, volontairement

- application wellness ;
- plugin RH ;
- diagnostic ;
- graphe D3 « état du cerveau » temps réel ;
- expansion encyclopédique de l'ontologie.

## Lien Cognitorium

Cognitorium peut *lire* des `CognitiveState` à partir de la phase 5, pas avant, et seulement en lecture. Il n'implémente pas HCSM.
