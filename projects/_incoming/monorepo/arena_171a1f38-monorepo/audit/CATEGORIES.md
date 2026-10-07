# CATEGORIES — Taxonomie canonique de l'audit

> **Autorité de nommage.** Toute table produite par cet audit utilise exactement ces noms.
> Un slug = un concept, sans synonyme. Toute ambiguïté se règle ici, pas dans les tableaux.
> Version : 2026-10-07 · Réf. : `audit/PLAN.md`

---

## 1. Périmètres (`scope`)

| Slug | Nom d'affichage exact | Définition | Volume attendu |
|---|---|---|---|
| `S0-racine` | Racine — dossier de marché/chantier | Fichiers non-code à la racine du dépôt (PDF, XLS/DOC, plans, images) | ~220 fichiers |
| `S1-infra` | Infra monorepo | `app/`, `scripts/`, `data/`, `docs/`, `MANIFEST.json`, `requirements.txt` | ~15 fichiers |
| `S2-projets` | Projets locaux | Les 9 dossiers de `projects/` | 9 projets |
| `S3-github` | Réel GitHub | État des 9 dépôts sur github.com/Sathancabrol (SHA, branches, PR, issues) | 9 dépôts |
| `S4-externe` | Documents externes | Contenus des connecteurs (Drive, Docs, Notion, Linear, Gmail) rattachables aux projets | à inventorier |

## 2. Projets — noms canoniques (casse exacte, à ne jamais altérer)

| Nom canonique | Dépôt GitHub | Alias toléré en prose | Note de nommage |
|---|---|---|---|
| `COGNITORIUM` | oui | — | majuscules obligatoires |
| `proto-cognitorium` | oui | proto | minuscules avec tiret |
| `HCSM` | oui | — | acronyme, majuscules |
| `reaserch-engine` | oui | research-engine (⚠️ *incorrect*) | **faute d'orthographe d'origine conservée** ; le nom réel du dépôt fait foi |
| `ETAT-DE-LART-PSYCHOLOGIE` | oui | ETAT-DE-LART (raccourci) | tirets, majuscules |
| `watchtower` | oui | — | minuscules |
| `animation-chronos` | oui | — | minuscules avec tiret |
| `Language-decoder` | oui | — | L majuscule, tiret |
| `frontignan` | **non** | — | projet local uniquement, absent de GitHub (à dater/documenter) |
| `monorepo` | oui | — | conteneur ; exclu des vues « projet » |

Règle : dans les tableaux, un nom de projet est un **code** (`backticks`), jamais traduit ni reformaté.

## 3. Catégories d'audit (`AUDIT-2026-10.md`)

Les 12 catégories ci-dessous structurent chaque fiche projet et les tableaux transverses.
**Ordre canonique** : de `C1` à `C12`, toujours respecté.

| # | Slug | Nom d'affichage exact | Ce qui est audité | Preuves types |
|---|---|---|---|---|
| C1 | `identite` | Identité & provenance | nom, URL, création, description, licence, propriétaire, SHA de référence | `MANIFEST.json`, API GitHub, LICENSE |
| C2 | `git-sync` | Dépôt, branches & synchronisation | branche par défaut, nb de branches, PR (ouvertes/fusionnées), issues, écart copie locale ↔ distant | `gh api`, `gh pr list`, SHA local |
| C3 | `structure` | Structure & volumétrie | nb de fichiers par type, taille, LOC, langages, arborescence | `find`, `du`, `wc -l`, `tokei`-like maison |
| C4 | `stack` | Stack & dépendances | manifests (package.json, requirements…), frameworks, versions, lockfiles | `package.json`, `bun.lock`, etc. |
| C5 | `fonctionnalites` | Fonctionnalités & modules | modules livrés, écrans/endpoints, ce qui marche vs stub | `src/`, `engine/`, `app/` |
| C6 | `donnees` | Données & ressources | datasets, `raw/`, fixtures, assets, images, volumétrie Git | `raw/`, `data/`, `public/`, `assets/` |
| C7 | `documentation` | Documentation & références | README, docs/, sources/citations, glossaires, index | `*.md`, CSV de sources |
| C8 | `tests-qualite` | Tests & qualité | fichiers de test, couverture, linters, CI, scripts de vérification | `tests/`, `*.test.*`, workflows |
| C9 | `securite` | Sécurité & secrets | secrets en clair, `.env`, `.gitignore`, données personnelles, dépendances à risque | `grep`, `.gitignore`, historique |
| C10 | `execution` | Exécution & déploiement | build, `dist/`, commandes de lancement, prévisualisation, portabilité | `dist/`, scripts, `vite.config` |
| C11 | `dette-risques` | Dette technique & risques | TODO/FIXME, code mort, duplications, dépendances figées, risques projet | `grep TODO`, comparaisons |
| C12 | `maturite` | Maturité & complétude | note de maturité + justification + prochaine étape | synthèse (échelle §5) |

### 3.1 Sous-catégories autorisées (précision)

Uniquement si un tableau l'exige ; le nom est `Nom catégorie / précision` :
`Données & ressources / brutes (raw)`, `Données & ressources / référentiels`,
`Documentation & références / sources citées`, `Tests & qualité / CI`,
`Tests & qualité / couverture`, `Sécurité & secrets / identifiants`,
`Exécution & déploiement / build`, `Exécution & déploiement / preview`.

## 4. Statuts et échelles (vocabulaire contrôlé)

**Statut d'audit** (`status`) : `à-faire` · `en-cours` · `fait` · `vérifié` · `bloqué`
**Confiance de preuve** : `vérifié` (constaté dans un fichier/une réponse API) · `déclaré` (affirmé par un doc du repo) · `inféré` (déduit, dit comme tel) · `inconnu`
**Risque** : `critique` · `élevé` · `moyen` · `faible` · `info`

### 5. Échelle de maturité (exacte, ordre croissant)

| Note | Nom | Définition opérationnelle |
|---|---|---|
| M0 | `vide` | rien d'exécutable, seulement un README ou des assets |
| M1 | `ébauche` | intentions écrites + fichiers épars, aucun run possible |
| M2 | `prototype` | exécutable localement, données factices, pas de tests |
| M3 | `alpha` | exécutable, fonctionnalités principales réelles, tests partiels |
| M4 | `bêta` | utilisable au quotidien, tests significatifs, docs à jour |
| M5 | `production` | CI, versionnage, sécurité, exploitation documentés |
| MA | `archive` | figé volontairement, conservé pour référence |

## 6. Règles de rédaction des tableaux

1. Une ligne = une entité (projet, fichier, finding). Jamais deux entités par ligne.
2. Chiffres : unités explicites (`fichiers`, `Mo`, `lignes`), séparateur décimal virgule en prose, point en données machine.
3. Un finding = `sévérité` + `catégorie (C1–C12)` + `preuve` + `recommandation`.
4. Colonne « Preuve » : chemin relatif + ligne, ou commande, ou endpoint API. Jamais « vu dans le repo ».
5. Les catégories vides sont écrites `n/a` avec motif, jamais supprimées.
6. Toute ligne non vérifiée porte `(déclaré)` ou `(inféré)`.
7. Les noms de fichiers sont cités **exactement** (accents et espaces compris).
