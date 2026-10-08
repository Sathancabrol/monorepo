# 🤖 OUTSIDER — Agents de production (roster)

> Les agents qui fabriquent et maintiennent le monde. Leurs prompts vivent dans `prompts/`, versionnés comme du code.
> Principe : **aucun contenu généré n'entre dans le World State sans passage par CANON-GUARDIAN.**

| Agent | Rôle | Entrées | Sorties | Fichier prompt |
|---|---|---|---|---|
| **CANON-GUARDIAN** | Gardien du canon Supernatural ; valide tout contenu généré ; signale les inventions hors-canon | Contenu candidat + références canon | verdict VALIDÉ / CORRIGÉ / REJETÉ + raison | `prompts/canon-guardian.md` |
| **WORLD-WEAVER** | Génère acteurs & organisations plausibles pour un territoire donné (schémas Société cachée §1-§2) | Région, époque, densité voulue, contraintes | fiches acteurs + organisations au format du World State | `prompts/world-weaver.md` |
| **ECONOMY-WEAVER** | Tisse les chaînes économiques : ressource → producteur → intermédiaire → vendeur → client → utilisation (§3) | Acteurs existants, ressources de la région | chaînes actives, dettes, contrats en cours | `prompts/economy-weaver.md` |
| **PHENOMENON-DIRECTOR** | Décide quoi/où/quand/pourquoi/qui sait/qui réagit (implémentera `docs/PHENOMENON_ENGINE.md`) | World State + tensions actives | journal d'événements + manifestations | 🔜 à écrire avec le moteur |
| **INVESTIGATION-WEAVER** | Cache les chaînes de pistes derrière les événements ; calibre la profondeur découvrable | Événements produits, niveau NG du joueur | réseaux de pistes, fausses pistes, accroches accidentelles | 🔜 phase 2 |
| **NARRATIVE-AUDITOR** | Contrôle de cohérence continue : contradictions, doublons, qualité des rumeurs | Diff du World State | rapport d'anomalies | 🔜 phase 2 |

## Règles communes aux agents
1. Produire au format des schémas de `docs/SOCIETE-SURNATURELLE-CACHEE.md` — pas de texte libre non structuré.
2. Tout élément doit pouvoir produire **une rencontre, une piste ou une ressource** (sinon rejet).
3. Jamais d'invention de société fantastique générique : le surnaturel reste une **couche cachée de la société humaine ordinaire** (RAW 46).
4. Chaque sortie est datée et signée (agent, version du prompt) pour le journal du World State.
