# 11 — Modèle de fonctionnement

**Statut du document :** `PROPOSED` (pont HCSM → ICF)  
**Couche :** HCSM MODEL  
**Version :** 0.1.0 · 2026-08-25

---

## 1. Séparation d'objets

```
ConstructEstimate     ce que l'on infère d'un processus
        ≠
Capacity              ce que la personne peut faire en environnement standard
        ≠
Performance           ce qu'elle fait dans son environnement habituel
        ≠
Participation         son engagement dans des situations de vie
```

L'ICF (`ESTABLISHED`) interdit d'inférer l'un à partir de l'autre par une règle unique. HCSM respecte cette interdiction : une `FunctionalProjection` est toujours une **hypothèse**, jamais une déduction.

## 2. Pont v0.1

Seuls quelques codes ICF sont ouverts, autour du noyau de construits.

| Construct HCSM | ICF candidate | Nature du pont |
|---|---|---|
| `attention` | b140 Attention functions ; d160 Focusing attention | fonction / activité |
| `working_memory` | b144 Memory functions (partiel) | fonction, alignement imparfait |
| `cognitive_control` | b164 Higher-level cognitive functions | fonction |
| `fatigue` | b1300 Energy level ; facteurs personnels | modulateur |
| — | d2 General tasks and demands | activité, projection large |
| — | e2 / e3 / e4 / e5 | environnement, depuis `ContextRecord` |

`working_memory` → `b144` est un `closeMatch` imparfait. Il est documenté comme tel. On n'invente pas un code ICF plus confortable.

## 3. Forme d'une projection

```
FunctionalProjection
  from: ConstructEstimate+
  to:   icf:d160
  kind: activity_limitation_hypothesis
  status: HYPOTHESIS
  requires:
    - context completeness ≥ minimal
    - no Refusal on the source constructs
  does_not_imply:
    - diagnosis
    - participation restriction
    - need for treatment
```

## 4. Capacité vs performance, repris

Un CPT de laboratoire informe davantage la **capacité** dans un environnement standard.  
Une EMA en open space informe davantage la **performance**.

HCSM ne mélange pas les deux sous un même identifiant de fonctionnement. Deux projections distinctes, ou une seule explicitement mixte avec incertitude élargie.

## 5. Cognitorium

Cognitorium consomme des projections de fonctionnement et des trajectoires, pas des scores nus. Le contrat :

- HCSM fournit `CognitiveState` + `FunctionalProjection?` + `Refusal*` ;
- Cognitorium les relie à des compétences, des expériences, des parcours ;
- Cognitorium n'écrit pas dans l'inference graph.

Cette frontière évite qu'un outil d'orientation réécrive un état cognitif pour les besoins de l'interface.

## 6. Interdits

- produire un « score de fonctionnement cognitif global » ;
- traduire automatiquement un état bas en restriction de participation ;
- utiliser HCSM comme justification d'une décision scolaire, médicale ou managériale en v0.1.
