# L'Orchestrateur et le Système Solaire — conception

**Date** : 9 octobre 2026 · **Référence** : le système `cosmos/` du projet
ETAT-DE-LART-PSYCHOLOGIE (SOL ☉ · Laplace ✳ · Uranus ♅ · Vénus ♀ — 5 177 lignes,
documenté dans `docs/COSMOS.md`), que nous avons retrouvé et dont nous nous
inspirons **sans recopier**.

**La règle d'or** : *on ne parle pas aux agents. On parle au patron.*

---

## 1. Pourquoi un seul interlocuteur (style JARVIS)

Tu parles à **un seul être** : l'Orchestrateur. Comme JARVIS, comme un
chef de projet, comme un DGS. Tu ne choisis pas qui fait quoi — c'est son
métier. Tu demandes, il analyse, il délègue, il rend compte.

| Sans patron (actuel) | Avec patron (cible) |
|---|---|
| Tu choisis l'agent dans une liste | Tu parles au patron, il choisit |
| Tu vois un résultat | Tu vois **qui a travaillé, comment, et ce qu'il a créé** |
| Un agent seul, livré à lui-même | Un patron qui **surveille**, **corrige**, **consolide** |
| Pas de mémoire de la délégation | Chaque délégation est **journalisée** et visible |

**Conséquence** : le chat n'expose plus le routage. L'utilisateur écrit,
le patron répond. Dans sa réponse, il dit quel agent a travaillé —
mais il ne l'a pas choisi, c'est le patron qui l'a fait.

---

## 2. La structure — un système solaire

Métaphore empruntée à ton système `cosmos/` : **chaque rôle est un astre**,
choisi pour sa symbolique et sa tâche.

```
                         ☉ SOL — LE PATRON
                    (orchestrateur, unique interlocuteur)
                    /                          \
              orbite intérieure              orbite extérieure
        les agents les plus sollicités      les spécialistes rares
        (rédacteur, chef de projet,         (juriste, archiviste,
         analyste, OSINT…)                  monteur, coach…)
                    \                          /
              ✦ sous-agents créés à la volée
                (lunes qui naissent autour
                 de leur planète mère)
```

### La sémantique orbitale

| Élément | Signification |
|---|---|
| **☉ Le soleil (SOL)** | Le patron. Au centre. Tout passe par lui. |
| **🪐 Les planètes** | Les 22 agents. Plus proche du soleil = plus sollicité. |
| **🛰️ Les satellites de tâche** | Les tâches en cours. Tournent autour de l'agent qui les exécute. |
| **☾ Les lunes** | Les **sous-agents créés à la volée** pour une tâche spécifique. |
| **✦ Les étoiles** | La mémoire, les connaissances produites. |

### Ce qu'on voit quand ça travaille

1. Tu parles au patron (le soleil **pulse** — il réfléchit)
2. Le patron délègue → la planète de l'agent choisi **s'active** (halo, rotation accélérée)
3. L'agent exécute → des **satellites de tâche** apparaissent autour de sa planète et tournent
4. Si la tâche dépasse ses compétences → une **lune naît** (sous-agent spécialisé créé à la volée)
5. Le patron rend compte → le soleil **brille** (résultat prêt), le document est proposé

**Règle visuelle** : *un agent qui travaille tourne. Un agent au repos est
immobile.* On voit le travail, pas seulement le résultat.

---

## 3. Le flux d'une interaction (tout passe par le patron)

```
VOUS ──► ☉ SOL (analyse la demande, approuve, décompose)
            │
            ├─► délègue à l'agent compétent (déterministe : mots-clés)
            │       │
            │       ├─► l'agent exécute les 6 phases
            │       │      (plan → recherche → production → revue
            │       │       → vérification → mémoire)
            │       │
            │       └─► si hors périmètre : crée un SOUS-AGENT
            │              spécialisé (parent + domaine + tâche)
            │
            └─► consolide, rend compte, propose le document
```

### Le patron a 4 responsabilités (comme SOL dans cosmos/)

| Responsabilité | Ce que ça fait concrètement |
|---|---|
| **Analyser** | Comprend la demande, détecte le domaine, les livrables attendus |
| **Déléguer** | Choisit l'agent (routage déterministe), ou crée un sous-agent |
| **Surveiller** | Suit les phases, détecte les blocages, peut réorienter |
| **Rendre compte** | Répond à l'utilisateur : qui a travaillé, ce qui a été produit, ce qui bloque |

---

## 4. Les sous-agents — création à la volée

Quand une tâche dépasse le périmètre des 22 agents (domaine trop spécifique,
compétence manquante), le patron **crée un sous-agent** :

```
parent : l'agent le plus proche du domaine
nom    : dérivé de la tâche (ex: « Expert foncier — Frange Sud »)
rôle   : la spécialité exacte
tâche  : ce qu'il doit faire
créé_pour : la demande qui a déclenché la création
```

- Un sous-agent est **un vrai agent** : il a un id, un parent, un rôle, il
  exécute les 6 phases, il est journalisé.
- Il apparaît dans la visualisation comme **une lune** autour de sa planète mère.
- Il est **réutilisable** : la prochaine fois que le patron retombe sur ce
  domaine, il le retrouve et le réactive plutôt que d'en recréer un.
- Il est **traçable** : on sait toujours pourquoi il existe.

**Règle** : *le patron ne délègue jamais dans le vide. S'il ne trouve pas,
il crée — et il le dit.*

---

## 5. Ce qu'on implémente dans Carré d'As

| Pièce | Fichier | Rôle |
|---|---|---|
| Le patron | `modules/agents/orchestrateur.py` | Analyse, délègue, surveille, rend compte, crée des sous-agents |
| Le registre des sous-agents | collection `sousagents` | Persistance, réutilisation, traçabilité |
| L'état live du système | `GET /api/agents/systeme` | Qui travaille, quelles tâches, quels sous-agents |
| Le chat | `modules/chat` modifié | Un seul interlocuteur : le patron |
| La vue | `Système solaire` (dans l'app) | Soleil, planètes, satellites de tâche, lunes, animation |
| Les événements | `broadcast('agents', …)` | La visu se met à jour en direct |

### La vue « Système solaire » (2D, zéro dépendance)

- Rendu **SVG + requestAnimationFrame** (comme la constellation, pas de Three.js :
  un poste de mairie doit tenir, et l'app doit rester offline)
- **Soleil fixe au centre** (halo pulsant quand le patron réfléchit)
- **Planètes en orbite** : 22 agents, rayon d'orbite = fréquence d'utilisation
- **Rotation** : les planètes tournent ; un agent **au travail** tourne plus vite + halo
- **Satellites de tâche** : apparaissent autour de l'agent qui exécute, disparaissent à la fin
- **Lunes** : les sous-agents, avec animation de naissance
- **Clic planète** → fiche agent (rôle, tâches en cours, sous-agents, historique)
- **Clic soleil** → ouvre le chat (tu parles au patron)
- **Live** : polling toutes les 2 s sur `/api/agents/systeme`

---

## 6. Ce qu'on ne fait PAS (et pourquoi)

| On ne fait pas | Pourquoi |
|---|---|
| Pas de Three.js / WebGL | L'app doit tourner offline sur un poste de mairie d'entrée de gamme |
| Pas de choix d'agent dans le chat | C'est le patron qui choisit — c'est toute la différence avec un sélecteur |
| Pas de sous-agent sans parent | Tout sous-agent a une planète mère — la traçabilité avant tout |
| Pas de sous-agent recréé à chaque fois | On réutilise — la mémoire du système, c'est son capital |
| Pas de LLM obligatoire | Le patron fonctionne sans clé, sans réseau — déterministe |

---

## 7. Références

- `projects/_incoming/ETAT-DE-LART-PSYCHOLOGIE/.../docs/COSMOS.md` — le système
  solaire original (SOL · Laplace · Uranus · Vénus), carte, flux, structure
  entreprise (chaque département = un astre)
- `projects/_incoming/ETAT-DE-LART-PSYCHOLOGIE/.../cosmos/sol.py` — orchestrateur
  (approbation, intégrité, interface)
- `projects/_incoming/ETAT-DE-LART-PSYCHOLOGIE/.../cosmos/bodies.py` — 12 corps,
  8 planètes, rôles et symboles
- `projects/_incoming/ETAT-DE-LART-PSYCHOLOGIE/.../cosmos/laplace.py` — l'interlocuteur
  principal (remplace SOL en façade)
- `projects/_incoming/ETAT-DE-LART-PSYCHOLOGIE/.../cosmos/metatron.py` — création
  de sous-agents (suggestion de spécification selon la mission)
- `projects/watchtower/src/systemeSolaire.js` — système solaire réaliste (JPL)
  autour de la Terre — preuve qu'un rendu orbital vanilla tient
