# 🌍 WORLD_STATE — prochaine structure à formaliser

> Statut : **NEXT** (décidé le 08/10/2026) · Dépend de : `SOCIETE-SURNATURELLE-CACHEE.md`
> Rôle prévu : **la source de vérité unique** du monde — ce que tout le reste lit et écrit.

## Ce qu'il devra contenir
```
WORLD_STATE
├── ACTEURS        (schéma §1 de la Société cachée)
├── ORGANISATIONS  (schéma §2)
├── ÉCONOMIE       (chaînes ressource→client actives, §3)
├── RELATIONS      (graphes datés et évolutifs, §4)
├── TERRITOIRES    (zones, contrôles, chevauchements)
├── ÉVÉNEMENTS     (journal produit par le PHENOMENON_ENGINE)
├── SAVOIRS        (qui sait quoi — joueur inclus)
└── HISTORIQUE     (ce qui s'est passé, pour la cohérence NG+)
```

## Questions à trancher
1. **Format** : graphe de fichiers (git-first, lisible par les agents de génération — même philosophie que le Life Hub) vs base embarquée.
2. **Qui écrit** : uniquement les moteurs (Phenomenon Engine, agents de génération) ; les scénarios *lisent* et *proposent*.
3. **Qui lit** : moteurs, scénarios, dialogues, UI d'enquête.
4. **Cohérence** : toute écriture passe par validation **CANON-GUARDIAN** (cf. `../agents/README.md`).
5. **NG+** : ce qui persiste entre les vies — les *connaissances du joueur* (RAW 46 §5) vs l'état du monde (reset ? dérive ?).

## Convention déjà actée
Chaque mutation du World State est **journalisée** (quoi, quand, par quel moteur, à partir de quelle cause) — c'est la condition pour que « le joueur arrive au milieu d'une histoire déjà commencée » reste compréhensible et debuggable.
