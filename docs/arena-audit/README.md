# Dossier d'audit — à donner à ArenaAI

**Objet :** faire auditer, comparer et réorganiser Carré d'As par un agent de recherche disposant d'un accès web/GitHub.
**Date :** 8 octobre 2026 · **État du dépôt :** branche `arena/0034230e-monorepo`, 9 projets, 13 branches rapatriées, 2 157 fichiers vérifiés, 0 manquant.

---

## Ce qu'il faut transmettre

| Fichier | Rôle | Indispensable |
|---|---|---|
| `00-MISSION-ARENAAI.md` | **le brief** : contexte, état vérifié, protocole de recherche, grille d'évaluation, contraintes, format de sortie | ✅ oui |
| `01-TABLEAU-DOMAINES.md` | **93 domaines** : existant, à auditer, à construire, priorité, candidats vérifiés, risques de licence, fiche art | ✅ oui |
| `02-CONCEPT-ART-ET-PROMPTS.md` | direction artistique + **20 fiches de concept art** et leurs prompts d'image | ✅ oui |
| `03-LICENCES-VERIFIEES.md` | **97 dépôts** contrôlés (licence, étoiles, activité, risque) + les 5 pièges à ne pas reproduire | ✅ oui |
| `data/domaines.json` | les 93 domaines en JSON, pour un traitement automatique | recommandé |
| `data/licences-2026-10-08.tsv` | la matrice de licences en tableau | optionnel |

**Phrase d'accompagnement suggérée :**

> Voici le dossier d'audit de Carré d'As. Lis `00-MISSION-ARENAAI.md` en entier avant de commencer.
> Tu dois produire, pour chacun des 93 domaines de `01-TABLEAU-DOMAINES.md`, un bloc JSON au format indiqué dans la mission,
> avec au moins deux preuves URL par domaine, une licence SPDX vérifiée par l'API GitHub, un budget de ressources,
> un mode d'intégration et un plan de sortie. Compare systématiquement avec ce que le dépôt contient déjà
> (`docs/carre-das/00→08`, `docs/recherche/`, `projects/_incoming/`) et n'oublie aucune des **104 fonctionnalités**
> du registre `shell/data/modules.json`. Termine par l'architecture cible, le plan de migration et les 4 planches d'images
> décrites dans `02-CONCEPT-ART-ET-PROMPTS.md`.

---

## Ce que ce dossier a déjà fait à ta place (ne pas refaire)

- **Vérification de 97 dépôts** par l'API GitHub le 08/10/2026 : licence réelle (fichier lu quand GitHub répondait `NOASSERTION`),
  étoiles, date de dernière publication, archivage. **Cinq pièges** en sont sortis : `mapbox-gl-js` (propriétaire),
  `FalkorDB` (SSPL), `gaussian-splatting` INRIA (non-commercial), `tldraw` (licence maison), `ODM/WebODM` (AGPL).
- **Correction de noms** de ton tableau : « GeoLibre » **existe** (`opengeos/GeoLibre`, MIT, ★7 871),
  « OpenClaw » **existe** (★391 640), « Alethe » **existe** (`Kc1t/alethe-agents`), « Gods-Eye-View » **existe**
  (MIT, ★49 027), « Argos » **introuvable**, « Mapbox » **à remplacer par MapLibre**.
- **Rapprochement** de ton nouveau tableau (~80 domaines) avec la matrice existante (`docs/recherche/02` : 85 domaines)
  → **93 domaines** après ajout de 8 manquants (D86 synchronisation 2D↔3D↔temps, D87 Language Decoder,
  D88 conformité chantier, D89 registre d'outils, D90 registre de compétences, D91 mises à jour, D92 collaboration, D93 santé des briques).
- **Reconstitution textuelle** de ta planche de concept art, pour qu'un agent qui ne voit pas l'image puisse l'utiliser.

## Rejouer / mettre à jour

```bash
python3 scripts/gen-dossier-arena.py     # régénère les tableaux, le JSON et la matrice de licences
python3 shell/tools/check-sources.py     # 104/104 fonctionnalités adossées à un fichier réel
python3 shell/tools/gen-registry.py      # régénère le registre du shell
python3 scripts/verif-completude-repos.py # 2 157 fichiers examinés, 0 manquant
```
