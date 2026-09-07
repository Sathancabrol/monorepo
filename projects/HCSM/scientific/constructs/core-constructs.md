# Construits du noyau v0.1

**Couche :** SCIENTIFIC KNOWLEDGE + pont ONTOLOGY  
**Canon machine :** `ontology/hcsm-v0.1.yaml`

Le noyau est un banc d'essai, pas une carte de l'esprit.

| ID | Rôle | Statut scientifique du *construit* | Statut de son usage HCSM | Alignement prioritaire | Alternatives obligatoires |
|---|---|---|---|---|---|
| `attention` | cognitive_construct | `ESTABLISHED` | `PROPOSED` comme objet T0 | Atlas, RDoC Attention, ICF b140 (close) | fatigue, arousal, motivation, task_difficulty, sleep_pressure |
| `working_memory` | cognitive_construct | `ESTABLISHED` | `PROPOSED` comme objet T0 | Atlas, RDoC WM, ICF b144 (close, imparfait) | attention, fatigue, motivation, task_difficulty |
| `cognitive_control` | cognitive_construct | `ESTABLISHED` | `PROPOSED` comme objet T0 | RDoC Cognitive Control | attention, WM, motivation, fatigue |
| `fatigue` | state_modulator | `SUPPORTED` | `PROPOSED` comme modulateur typé | ICF b1300 (close) | — |
| `arousal` | state_modulator | `ESTABLISHED` | `PROPOSED` comme modulateur typé | RDoC Arousal | — |
| `sleep_pressure` | state_modulator | `SUPPORTED` | `PROPOSED` comme modulateur typé | RDoC Arousal/Regulatory (related) | — |

## Règles d'extension

Un nouveau construit n'entre dans le noyau que s'il a :

1. un alignement externe (`exact` ou `close`) ;
2. au moins une `Measure` `measuredBy` documentée ;
3. des alternatives obligatoires ;
4. une échelle de temps ;
5. une raison *expérimentale* (un test H1–H6 qui en a besoin).

« Ce serait utile dans Cognitorium » n'est pas une raison suffisante.

## Notes de validité

- n-back : ne pas marquer `exact` pour `working_memory` par défaut (validité de construit contestée).
- RT variability : `close` pour attention, non spécifique.
- ICF b144 ≠ working memory.
- Lee & Engle (2026) : le contrôle attentionnel n'est pas la WMC. Ne pas fusionner `attention` et `working_memory` pour simplifier l'interface.
