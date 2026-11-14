# OLYMPUS Studio — charge de travail et cadence autonome

Dernière modification : 13 novembre 2026. **Il s'agit d'ordres de grandeur de complexité, pas de promesses de délai.** Le temps réel d'une session automatique varie selon les outils, accès, CI et limites d'exécution. Une reprise toutes les heures **ne signifie pas** une heure de développement à chaque passage.

## Cadence effective

- Tâche ChatGPT `6af632ef3df88191a7ef46e372054ac4` : **toutes les heures**, zone `Europe/Paris`, à partir du 13/11/2026 à 04:00 locale.
- Chaque run lit l'état GitHub et le checkpoint, traite la plus haute priorité non terminée, **enchaîne une autre tranche testable pendant le même run** si le contexte et les ressources le permettent, puis écrit un checkpoint atomique.
- Aucun déclenchement récursif illimité : le calendrier horaire prend le relais. Si une session n'a pas terminé un travail, la suivante reprend l'état enregistré.
- GitHub Actions lance les tests après chaque push : **cela ne développe pas de code sans agent**.
- Ne pas effectuer d'édition concurrente sur le même fichier sans relire son SHA et le dernier commit; aucun merge vers `main`.

## Taille des tâches (estimation relative)

Échelle : **S** = courte, **M** = intermédiaire, **L** = importante, **XL** = chantier majeur avec plusieurs incréments et dépendances. Cette échelle indique l'effort d'ingénierie relatif, **pas une durée de livraison**.

| ID | Taille | Motif principal | Limite ou condition |
|---|---|---|---|
| A01 | M | Audio de EDIT : débogage pipeline réel et synchronisation | Validation A/V par fichier réel |
| A02 | M | E2E IndexedDB, import portable, reprise après fermeture | Origine HTTP + navigateur exploitable |
| A03 | S–M | Fixture codec/dérive et analyse FFprobe | Capture WebM réellement produite |
| A04 | M | Undo/redo non destructif avec commandes | État cohérent scènes et audio |
| A05 | M | Benchmark FreeCut, OpenReelio, ADR et licences | Vérifier versions/licences exactes |
| A06 | XL | ASR français/anglais, choix de source, SRT et erreurs | Modèle local et CPU |
| A07 | L | Flux XR horodaté, gestes, intégration X-Ray | Fixtures + webcam ensuite |
| A08 | M | Import contrôlé des sorties ComfyUI | ComfyUI réel pour recette |
| A09 | L | Gouvernance d'actions et intégration Chronos | Permissions explicites |
| A10 | L–XL | Vue Watchtower/Cesium, contrat de scène et mémoire | 3D réelle sur matériel |
| A11 | XL | Avatar VRM, suivi pose, animations et profil faible GPU | Licence de modèles et performances |
| A12 | L | Packaging Windows/offline, diagnostic, sécurité | Installation réelle |
| W01–W03 | L | Recette réelle de LIVE, GPU, 3D, stabilité | Accès Windows indispensable |

**Plus grand risque de sous-estimation** : intégration de plusieurs moteurs (A/V temps réel, animations 3D, traitements IA locaux), sécurité/licences et différences Windows vs Linux.

## Format du checkpoint à chaque run

Sous `docs/HANDOFF.md` écrire :
- Commit/branche vérifiés en début de run et dernier commit écrit, fichier(s) changés.
- Tâche `READY / IN_PROGRESS / BLOCKED / DONE` et critère(s) d'acceptation déjà prouvés.
- Résultats des tests : syntaxe, Node, navigateur, Windows réel, lien CI au dernier commit.
- Difficultés, erreurs et solutions tentées sans secrets; ce qu'il reste à vérifier.
- **Première action exacte de la session suivante**, avec sa taille relative, sans dépendre de l'utilisateur.

## Complétion

Le périmètre global dépasse le scaffold actuel. Une interface de 12 espaces **ne prouve pas** que les 12 moteurs sont actifs. Ne pas clôturer le projet sans tests vidéo/audio réels, OBS, ComfyUI, XR, Watchtower, licences, packaging et recette Windows.

Si l'utilisateur veut une exécution réellement ininterrompue, il faudra un agent permanent sur une machine/runner autorisé et disponible (par exemple son écosystème Hermes/Chronos), avec gestion de budget, secrets, reprise et arrêt. **Ce runner n'est pas en place via cette automatisation**.
