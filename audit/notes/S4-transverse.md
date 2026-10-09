# S4 — Audit transverse (les 9 projets ensemble)

**Mesuré** : 2026-10-07 · **Sources** : `audit/data/inventory.json`, `drift.json`, `branches-all.json` + scans ciblés

## 1. Doublons & dispersions (mesurés)

| Doublon | Preuve | Portée |
|---|---|---|
| **Code Watchtower en 2 exemplaires** | `projects/COGNITORIUM/watchtower-mods/` (62 fichiers) : **62/62 noms de fichiers existent aussi dans `projects/watchtower/`** | ~100 % de recouvrement → une seule source de vérité à choisir |
| **3 bases de connaissances « cognition »** | `proto-cognitorium/src/data/{psychologyAtlas,psyRefLibrary,psyRefSources}.ts` · `ETAT-DE-LART/data/nodes_etat_art_psychologie.csv` · `HCSM/ontology/hcsm-v0.1.yaml` | ADR-009 toujours ouverte (décision non prise) |
| **2 représentations de l'état cognitif** | HCSM (validateur V1/V5) vs `intelTwin` (watchtower) vs `capacity_cognitive` (proto) | aucune ne consomme l'autre |
| **Audits dispersés** | 7 fichiers `docs/audits/*` (COGNITORIUM) + 5 `audit/*` (watchtower) + 5 rapports sur branches + ce dossier | pas de registre central avant `audit/` |
| **Frontignan en 3 formats** | `.md`, `.html`, deck `index.html` + atlas sur branche | maintenance multiple |
| **Dossier DCE en double dans le monorepo** | racine (220 fichiers) **et** `projects/btp-conduite-travaux/documents_sources/` (154 fichiers, branche `01a08449`) | à dédupliquer lors de la fusion |

## 2. Câblage / intégration

**Constat : aucun câblage de code entre les projets.** Recherche de références croisées : `HCSM`, `reaserch-engine`, `Language-decoder` ne sont cités que dans la **documentation** de `COGNITORIUM` (et par eux-mêmes). Aucun import, aucune dépendance déclarée, aucun appel d'API inter-projets.
→ La « fusion » réalisée dans `projects/` est **physique (copie)** et **visuelle (preview)**, pas **logique** — conforme à ce que dit le README, mais c'est la limite structurante de l'écosystème.

## 3. Sécurité globale

| Contrôle | Résultat | Preuve |
|---|---|---|
| Clés/API secrets en clair (`sk-`, `ghp_`, `AIza`, `xox`, clés privées) | **0** | `grep -rInE` sur tout le dépôt |
| Fichiers `.env` réels | **0** | `find -name .env` |
| Modèles `.env.example` | 4 (animation-chronos, proto, watchtower ×2) | `find` |
| Antécédent | `proto-cognitorium/raw/identifiants_cognitorium*.json` purgé (rotation recommandée) | doc interne COGNITORIUM |
| Données sensibles publiques | grilles salariales + corrigés AIPR à la racine d'un dépôt **public** | inventaire S0 |
| Clés utilisateur | stockées en `localStorage` (watchtower, proto) | README/docs |

## 4. Données lourdes & poids Git

| Poste | Taille | Où |
|---|---:|---|
| Dossier de chantier | 225.1 Mo (220 fichiers) | racine (committé) |
| `raw/` proto-cognitorium | 64 Mo (61 fichiers) | committé |
| Images/figures (frontignan, COGNITORIUM, watchtower) | ~35 Mo | committé |
| `dist/` + assets Cesium | ~10 Mo | committé (choix assumé) |
| **Dépôt `monorepo` total** | **317 Mo** | GitHub |
| 2ᵉ copie du dossier de chantier | ~150 Mo | branche `01a08449` |

## 5. Tests & CI (global)

| Indicateur | Valeur | Détail |
|---|---:|---|
| Fichiers de test | **221** | watchtower 208 · reaserch-engine 12 · HCSM 1 |
| Projets avec tests | **3 / 9** | — |
| Projets sans aucun test | **6 / 9** | COGNITORIUM, proto, ETAT-DE-LART, animation-chronos, Language-decoder, frontignan |
| CI | **1 / 9** | `watchtower/.github/workflows/ci.yml` (27 runs, matrix Node 24/26 + Windows) |
| Dernier résultat mesuré | watchtower : 1344/1454 ok sans deps (109 échecs = `ERR_MODULE_NOT_FOUND`) · HCSM 29/29 + 23/23 cas · reaserch-engine **2 rouges** | exécuté le 2026-10-07 |
| TODO/FIXME | 10 | 8 dans `scripts/github_inventory.py`, 2 dans COGNITORIUM |

## 6. Documentation, sources & références

- **237 fichiers de documentation** dans les projets (dont 57 proto, 53 COGNITORIUM, 52 HCSM, 35 watchtower, 20 ETAT-DE-LART) + 7 dans `docs/` + 224 à la racine.
- Bonnes pratiques de sourçage **locales** : `frontignan` (249 sources datées + balises ✅/📅/🔮/⚠️), synthèse Talbot (registre ✅/⚠️/❌, 12 corrections), watchtower (`REFERENCE.md` 193 Ko, 86 outils), HCSM (positionnement vs RDoC/ICF).
- **Mais aucun registre de sources commun** : chaque projet réinvente sa méthode de traçabilité → cohérent avec le besoin d'un « registre de claims » (proposé par l'audit watchtower V5).

## 7. Nommage & conventions (à corriger)

| Problème | Exemple | Impact |
|---|---|---|
| Faute d'orthographe de dépôt | `reaserch-engine` | recherche, liens, image publique |
| Comptage faux dans les docs | « 8 dépôts » alors que 9 projets existent (+`frontignan`) | documents d'état des lieux |
| Titres incohérents | `Language-decoder` vs « Language Decoder » vs « décodeur de langage » | navigation |
| Doublons de nommage de fichiers | `CCAP.pdf` / `04 - CCAP.pdf` / `Cahier des Clauses Administratives Particulières.pdf` | ambiguïté juridique |
| Typos dans les noms de fichiers | `BORUDRE P1.pdf`, `glisière.pdf`, `Réglement…` | scripts, recherche |
| Dossiers racine `12 catégories` (index) vs `12 familles` (cet audit) | deux taxonomies cohabitent | à unifier (fait ici : familles canoniques) |

## 8. Licences & légal

| Projet | Licence | Note |
|---|---|---|
| `watchtower` | MIT — © Bilawal Sidhu | **fork** de `gods-eye-view` ; attribution à clarifier en tête de README |
| `HCSM` | LICENSE + CITATION.cff | exemplaire |
| `Language-decoder` | CC-BY-4.0 (branche seulement) | à rapatrier dans `main` |
| 6 autres | **aucune** | usage public sans licence = « tous droits réservés » implicite |

## 9. Versions & dépendances

- Trois apps React 19 + Vite 6 homogènes (`animation-chronos`, `proto-cognitorium`, `watchtower`) ; pas de monorepo de dépendances (pas de workspace) — volumétrie npm non factorisée (3 `node_modules` potentiels).
- **Incohérence lockfiles** : `proto-cognitorium` a `bun.lock` **et** `package-lock.json` ; `COGNITORIUM/watchtower-mods` n'en a aucun.
- Python sans manifeste pour `reaserch-engine`, `ETAT-DE-LART`, `frontignan` ; seul `HCSM/validator/requirements.txt` existe.

## 10. Mémoire & persistance (l'axe « mémoire » de la vision)

| Projet | Persistance | Preuve |
|---|---|---|
| proto-cognitorium | `localStorage` | ADR-002 |
| COGNITORIUM/learning | `localStorage` (événements de session) | README |
| reaserch-engine | `JsonRunStore` (JSON atomique par run) | `engine/persistence.py` |
| ETAT-DE-LART | SQLite | `app/database.py` |
| watchtower | 39 clés `watchtower.*.v1` en localStorage | audit de branche |
| **Décision actée** | ADR-007 : PostgreSQL + pgvector + Apache AGE + PostGIS | `docs/audits/external/003` |

→ La mémoire reste **éclatée** : 5 mécanismes, aucun partagé. ADR-007 tranche la cible mais rien n'est implémenté.

## 11. Findings transverses

| # | Sévérité | Catégorie | Constat | Preuve | Recommandation |
|---|---|---|---|---|---|
| F-TR-01 | **critique** | C2 | 153 commits non fusionnés sur 15 branches (5 actives le jour de l'audit) | `branches-all.json` | plan de fusion séquencé |
| F-TR-02 | élevé | C11 | aucun câblage logique entre projets (docs seulement) | grep références croisées | définir 2-3 interfaces prioritaires (HCSM↔proto, reaserch↔dossier) |
| F-TR-03 | élevé | C6 | 225 Mo + 64 Mo de données dans Git, dossier de chantier en double | inventaire | LFS/externalisation + dédup |
| F-TR-04 | élevé | C8 | 6 projets sans test, 1 CI pour 9 dépôts | inventaire + API | CI minimale partout (lint/build), tests sur proto & learning |
| F-TR-05 | moyen | C1 | 6 projets sans licence | `find` | décider licence par projet |
| F-TR-06 | moyen | C7 | nommage incohérent (`reaserch-engine`, « 8 dépôts ») | inspection | corriger docs + renommer dépôt |
| F-TR-07 | moyen | C6 | 3 bases de connaissances + 2 représentations cognitives | docs + grep | fermer ADR-009 |
| F-TR-08 | faible | C10 | lockfiles incohérents (bun + npm, ou aucun) | `find` | standardiser npm |
| F-TR-09 | faible | C8 | 10 TODO/FIXME dont 8 dans l'inventaire GitHub | inventaire | traiter ou convertir en issues |
