# 🤖 Rendre les agents réellement opérationnels — sans clé, sans installation, puis avec (09/10/2026)

> Question posée : « avant de brancher des clés ou d'installer quoi que ce soit, je veux que la partie agentique soit au moins fonctionnelle : qu'un agent puisse modifier le design de l'app ou aller chercher des données sur internet. »

---

## 1. 🧱 Ce qu'il faut à un agent pour agir : 3 briques

1. **Des mains** = des outils : lire/écrire des fichiers, lancer des commandes, interroger des services, parler à internet.
2. **Un cerveau** = un modèle d'IA qui décide.
3. **Un harnais** = la boucle qui orchestre (le cerveau regarde → choisit un outil → agit → vérifie → recommence), avec des permissions et un journal.

**État actuel du système :**

| Brique | État | Détail |
|---|---|---|
| Mains | ✅ **solides** | les 12 services agent-office testés, tout le monorepo éditable, `registry doctor` comme contrôle |
| Cerveau | ⚠️ **déporté** | le cerveau aujourd'hui = l'agent de cette session Arena (moi). Aucun modèle local/branché |
| Harnais | ⚠️ **humain** | c'est toi qui donnes les missions dans le chat ; pas de boucle autonome |

**Conclusion honnête** : la couche agentique EST fonctionnelle (les mains existent, un cerveau existe, un circuit de validation existe — portes humaines, gates QA, journal), mais elle n'est **ni autonome, ni persistante**. La rendre opérationnelle sans dépenser = formaliser le circuit de mission pour que n'importe quel cerveau (moi maintenant, un outil gratuit ensuite) l'exécute pareil.

**Note technique importante (pour ne pas se raconter d'histoires)** : dans ce sandbox, les commandes shell n'ont accès qu'à GitHub/PyPI/npm ; la recherche et la lecture web passent par les outils de la plateforme. Donc « aller chercher des données sur internet » passe par moi ici, et passera par l'agent directement quand il tournera sur ta machine. C'est une différence de contexte d'exécution, pas de conception.

## 2. 🎯 Ce qu'on met en place maintenant (0 €, 0 installation) : les missions

Un agent devient opérationnel quand il reçoit une **mission** au format standard et qu'il la rend avec sa preuve. Format (hérité de la méthode Jake Van Clief déjà dans nos docs) :

```
Mission M-<numéro> — <agent concerné>
1. OUTCOME   : le résultat visible attendu (une phrase)
2. HOW       : les outils/fichiers autorisés, les étapes
3. TOUCH     : ce qui peut être modifié (chemins), ce qui est interdit
4. HUMAN-CHECK : la porte de validation avant « terminé »
```

- Le registre des missions vit dans `projects/agent-office/agents/missions/` (une mission = un fichier ; statuts : `brouillon → en_cours → gate → terminé`).
- Chaque agent a ses **capacités** déclarées (fiches `agents/*.md`) ; une mission ne peut demander que des capacités de l'agent, dans les chemins autorisés.
- Toute mission terminée laisse une entrée au journal (`update`) : c'est la traçabilité agentique.

**Exemples concrets que ça couvre dès aujourd'hui** :
- « modifier le design de l'app » → mission pour l'agent **Directeur du Registre/Production** : TOUCH = `app/templates/` + `style` uniquement, HOW = lire → éditer → relancer la preview → vérifier, HUMAN-CHECK = ta validation visuelle.
- « aller chercher des données sur internet » → mission pour l'agent **Chercheur** : collecte via les outils de recherche de la session, sortie = note sourcée dans `docs/` + entrée `knowledge`, HUMAN-CHECK = 2 sources minimum par conclusion (règle existante).

## 3. 🪜 Les niveaux suivants (proposés, rien d'installé)

**Niveau 2 — un harnais gratuit sur ta machine (0 €, ~30 min d'installation quand tu le décides)** :
- **Gemini CLI** : agent de code gratuit sur simple compte Google (quota mensuel généreux) ; il sait éditer des fichiers, lancer des commandes, aller sur internet, et il lit nativement les fichiers `AGENTS.md`/`MAP.md` → nos fiches agents le pilotent telles quelles.
- Alternative : **Codex CLI** pointé sur les clés gratuites GitHub Models (déjà dans `CLES-API-GRATUITES.md`).
- À ce stade : « modifie le design de l'app » devient une instruction que tu tapes toi-même sur ta machine, exécutée par un agent qui connaît nos règles.

**Niveau 3 — les clés gratuites + notre propre boucle (0 €, après validation du niveau 2)** :
- un service `runner` dans agent-office (stdlib, zéro dépendance) : `python3 -m agent_office runner --agent chercheur --mission M-007` ; il lit la fiche de l'agent, interroge le modèle via son endpoint OpenAI-compatible (Mistral/GitHub Models/Gemini), exécute des outils **restreints** (chemins autorisés, jamais d'envoi/publication sans porte humaine), journalise tout.
- C'est la version « nous possédons le harnais » — indispensable pour les missions planifiées (veille BOAMP, digests) sans dépendre d'un outil tiers.

**Niveau 4 — l'agent résident 24/7 (après le 1ᵉʳ revenu)** :
- VPS ≤ 6 €/mois + routines planifiées (`routines.yaml`, pattern MAPS) + portail `app/` branché + OmniRoute pour le routage des modèles. Déjà documenté (VPS-AGENT-SQLITE-GRAPH, AGENT-OS veille §6).

## 4. ⚖️ Pourquoi cet ordre

- **Pas de clé d'abord** : sans missions formalisées, une clé ne saurait pas quoi faire proprement ; avec les missions, n'importe quel cerveau s'y branche.
- **Pas d'installation d'abord** : le circuit mission/preuve/journal se valide avec le cerveau actuel (cette session) ; l'installation devient un simple changement de cerveau, sans rien redessiner.
- **Permissions avant puissance** : comme Herald OS et Paf, on définit ce que chaque agent a le droit de toucher AVANT de lui donner plus de force (règles TOUCH + jamais d'action irréversible sans humain).

## 5. ✅ Fait ce tour / proposé

- ✅ Cadre de missions créé : `projects/agent-office/agents/missions/` (README du format + template).
- ✅ Capacités « modifier l'app » et « collecter sur internet » décrites dans les fiches concernées.
- 📌 Proposé : première mission de démonstration au choix — redesign du portail `app/` ou collecte internet structurée (voir discussion).
- 📌 Niveau 2 (Gemini CLI) : prêt à installer quand tu le décideras ; Niveau 3 (runner) : conçu, à construire quand les clés existent.

---
*09/10/2026 — docs/RENDRE-LES-AGENTS-OPERATIONNELS.md*
