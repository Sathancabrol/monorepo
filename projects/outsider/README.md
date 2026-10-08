# 🎮 OUTSIDER — RPG d'enquête dans l'univers Supernatural

> Chantier game design & world simulation · ouvert le 2026-10-08 · monorepo, branche `arena/93b54a79-monorepo`
> ⚖️ **Statut IP** : projet de travail basé sur l'univers *Supernatural* (Warner Bros.). Aucune exploitation commerciale sans droits — ce repo contient le design, pas de contenu de marque redistribué.

## Le pitch
Un jeu d'**enquête** dans l'Amérique de Supernatural : le surnaturel n'est pas un monde à part, c'est **une couche cachée de la société humaine** — marchés noirs, services occultes, trafics d'objets, alliances monstres/humains. Le joueur n'est pas le centre du monde : **le monde tourne sans lui**, il arrive au milieu d'histoires déjà commencées. Et la vraie progression n'est pas la puissance — c'est **la connaissance** (NG+ = reconnaître plus vite).

## Les 5 piliers (non négociables)
1. **Canon d'abord** — pas de « société des monstres » façon RPG fantasy inventée. Supernatural *montre déjà* réseaux, marchés, alliances : on part du substrat canonique, on le systématise. (RAW 46)
2. **Règle générale** — *tout ce qui existe dans le canon et qui peut être systématisé doit devenir potentiellement systémique.*
3. **Le monde sans le joueur** — sorcière vend objet → vampire achète → rituel → cadavre → police → rumeur → chasseur entend → le joueur arrive. La simulation produit les histoires ; le scénario les récolte.
4. **La connaissance est la progression** — 1ʳᵉ vie « C'est quoi ce truc ? » → NG+ « Je connais ce symbole » → NG+++ « Je sais pourquoi ils le vendent ».
5. **Émergence sur script** — une grande partie du contenu existe dans le World Simulation, prête à produire rencontres, enquêtes et ramifications ; pas tout en quêtes main.

## Structure du chantier
```
projects/outsider/
├── README.md                      ← ici : vision, piliers, roadmap
├── docs/
│   ├── GDD-INDEX.md               ← table des matières du game design
│   ├── raw/
│   │   └── RAW-46-economie-societe-surnaturelle.md   ← règle fondatrice
│   ├── SOCIETE-SURNATURELLE-CACHEE.md                ← système formalisé
│   ├── PHENOMENON_ENGINE.md       ← NEXT : qui décide quoi, où, quand
│   └── WORLD_STATE.md             ← NEXT : la source de vérité unique
└── agents/
    ├── README.md                  ← roster des agents de production
    └── prompts/                   ← prompts versionnés (canon, world, éco…)
```

## Roadmap de production
| Phase | Contenu | Statut |
|---|---|---|
| **0. Fondation** | RAW 46 + formalisation Société surnaturelle cachée + roster d'agents | ✅ fait |
| **1. Moteurs** | `PHENOMENON_ENGINE.md` (événements) + `WORLD_STATE.md` (persistance) | 🔜 next |
| **2. Boucle d'enquête** | Chaînes d'indices, fausses pistes, découvertes hors-quête, Carré d'As | ⏳ |
| **3. Progression** | Système de connaissance NG+/NG+++, reconnaissance de patterns | ⏳ |
| **4. Prototype** | Génération d'une ville test (acteurs, organisations, économie locale) | ⏳ |

## Conventions de travail (façon studio)
- Les **règles** sont numérotées `RAW-nn` et jamais réécrites : une règle changée = nouvelle règle + note d'obsolescence.
- Chaque doc de système répond à : *qu'est-ce qui existe ? qui le produit ? qui le consomme ? comment le joueur tombe dessus ?*
- Les **agents de production** (génération de monde) sont promptés dans `agents/prompts/`, versionnés comme du code ; tout contenu généré passe par **CANON-GUARDIAN** avant d'entrer dans le World State.
- Rien n'est « lore décoratif » : si un élément ne peut ni produire une rencontre, ni une piste, ni une ressource — il n'entre pas dans la simulation.
