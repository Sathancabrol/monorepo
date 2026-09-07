# 12 — Cadre de validation

**Statut du document :** `PROPOSED`  
**Couche :** SCIENTIFIC KNOWLEDGE / HCSM MODEL  
**Version :** 0.1.0 · 2026-08-25

HCSM n'est pas validé. Ce document dit comment on saurait qu'il l'est, et comment on saurait qu'il ne l'est pas.

---

## 1. Ce que « valider HCSM » ne veut pas dire

- obtenir une AUC élevée pour prédire un diagnostic ;
- corréler un vecteur HCSM avec un QI ou un PHQ-9 ;
- convaincre des utilisateurs qu'un tableau de bord est « riche » ;
- aligner 200 construits sur le Cognitive Atlas.

Ces succès-là peuvent arriver sans que la contribution (relier sans réifier) soit réelle.

## 2. Niveaux de validation

| Niveau | Question | Critère de réussite | Critère d'échec |
|---|---|---|---|
| V0 Conceptuel | Les distinctions tiennent-elles face à l'audit ? | revue par pairs internes, matrice de nouveauté stable | contradiction avec RDoC/ICF/Atlas non assumée |
| V1 Forme | L'ontologie et le schéma rejettent-ils les objets illégaux ? | 100 % des cas d'interdiction testés | un `Attention=0.73` nu passe le validateur |
| V2 Juges | Le format `ConstructEstimate` réduit-il la réification ? | moins d'erreurs qu'avec un score nu | pas de différence, ou plus de confusion |
| V3 Psychométrique | Les estimations sont-elles fidèles, convergentes, divergentes là où il faut ? | fidélité / validité argumentée sur le noyau | estimateur instable ou non aligné |
| V4 Écologique | Contexte + fenêtre améliorent-ils une prédiction de performance ICF ? | gain vs scores seuls, préenregistré | pas de gain, ou gain dû à la fuite de données |
| V5 Refus | Le système refuse-t-il quand il le doit ? | sensibilité/spécificité du refus sur cas construits | toujours une valeur, ou refus capricieux |

V0 et V1 sont le périmètre immédiat de ce dépôt.  
V2–V5 sont le programme empirique (`docs/13_RESEARCH_PROTOCOL.md`).

## 3. Hypothèses et tests

Reprise de H1–H6, opérationnalisées.

### H1 — Non-réductibilité au profil de scores

**Test V2.** Matériel : mêmes données présentées (a) comme scores nus, (b) comme `ConstructEstimate`. Tâche : juges (chercheurs / cliniciens chercheurs) identifient ce qui est mesuré, estimé, encore ouvert.  
**Succès :** moins de collages mesure = construit dans (b).  
**Échec :** pas d'effet, ou (b) augmente la confiance injustifiée.

### H2 — Séparation Knowledge / Evidence / Inference

**Test V1 + V2.** Le validateur refuse les objets trans-graphes illégaux. Les juges attribuent correctement un item à son graphe.  
**Succès :** κ élevé sur l'attribution de graphe.  
**Échec :** les trois graphes ne sont pas discriminables en pratique.

### H3 — Contexte et fenêtre

**Test V4.** Prédiction d'un indicateur de performance (ex. d160 en situation réelle, ou tâche écologique) à partir de (a) scores, (b) scores + contexte/fenêtre, (c) HCSM complet.  
**Succès :** (c) > (b) > (a) sur métrique préenregistrée, sans fuite.  
**Échec :** (c) ≤ (a).

### H4 — Alternatives

**Test V2 / V5.** Cas où fatigue et attention sont indiscernables.  
**Succès :** HCSM maintient les deux alternatives ou refuse ; les juges ne choisissent pas un « vainqueur » fictif.  
**Échec :** le modèle « départage » sans évidence.

### H5 — Plus-value vs cadres séparés

**Test V4.** Comparer HCSM à : Atlas seul (pas d'état), RDoC seul (pas d'individu T0), ICF seul (pas d'état latent), scores multimodaux seuls.  
**Succès :** gain spécifique sur la liaison personne-temps, pas sur la taxonomie.  
**Échec :** tout le gain vient d'avoir plus de features.

### H6 — Refus plutôt qu'invention

**Test V5.** Jeux de cas : évidence nulle, fenêtre absente, mesure non alignée, provenance cassée.  
**Succès :** `Refusal` correct ; zéro valeur inventée.  
**Échec :** un nombre sort.

## 4. Jeux de données

En v0.1, **pas de données personnelles dans ce dépôt**.

Autorisés :

- cas synthétiques (voir `research/` plus tard) ;
- données publiques déjà consenties, citées, non recopiées ici si licence douteuse ;
- protocoles d'acquisition futurs, préenregistrés.

Interdits :

- logs réels, EEG identifiants, traces smartphone nominatives.

## 5. Ce qui serait une validation-spectacle

- une démo Cognitorium colorée ;
- une heatmap d'« état cognitif » temps réel ;
- un communiqué « IA de la cognition ».

Aucune de ces choses n'entre dans V0–V5.
