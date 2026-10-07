# P — `COGNITORIUM`

**Audit** : fait (2026-10-07) · **Risque global** : moyen · **Maturité** : M2 `prototype`
**Résumé** : dépôt vitrine + gouvernance documentaire (53 docs) + 2 briques de code : `learning/` (PoC CLE, 206 lignes) et `watchtower-mods/` (fork Cesium, 37 k lignes).

## C1 — Identité & provenance

| Fait | Valeur | Preuve |
|---|---|---|
| Dépôt | `Sathancabrol/COGNITORIUM`, public | `gh repo list` |
| Créé / dernier push | 2026-08-02 / 2026-09-07 | idem |
| SHA `main` réel | `5348d4cb` (2026-09-06) | `gh api` |
| SHA de référence local | `cbf65391` (MANIFEST) | `MANIFEST.json` |
| Licence | **aucune** | `find` racine |
| Branches | 4 (dont `watchtower/osint-workbench-v0.1` en avant) | `gh api branches` |

## C2 — Dépôt, branches & synchronisation

- **Copie locale = `main` distant** : 131 fichiers des deux côtés, 0 écart (`audit/data/drift.json`).
- **Travail non fusionné** : `watchtower/osint-workbench-v0.1` — **+13 commits**, 143 fichiers, 22.94 Mo, dernier commit 2026-09-07 : `watchtower-mods/docs/OSINT-*.md` + `src/osint/*.js` (workbench OSINT).

## C3 — Structure & volumétrie

| Mesure | Valeur |
|---|---|
| Fichiers / taille | 131 / 22.9 Mo |
| LOC-code / LOC-données-doc | 27 691 / 2 291 |
| `docs/` | 2 886 lignes Markdown (53 fichiers) |
| `learning/` | 206 lignes (JS/HTML/CSS) |
| `watchtower-mods/` | 37 106 lignes — dont `vite.config.js` de **7 821 lignes** (343 Ko) |
| Images générées | 10+ PNG/JPG non nommés (« Generated Image … », « Gemini_Generated_Image … ») |

## C4 — Stack & dépendances

- Pas de `package.json` à la racine ; `learning/` = JS vanilla ; `watchtower-mods/` = Vite + CesiumJS (config custom 343 Ko : proxys OpenSky, CelesTrak, Overpass, GBFS, CCTV, adsb.lol, AIS, TomTom, NASA FIRMS…).
- Aucun lockfile dans la copie locale de `watchtower-mods`.

## C5 — Fonctionnalités & modules

| Module | État | Preuve |
|---|---|---|
| `docs/constitution/` (vision → ADR-001..) | complet, v1 sept. 2026 | 10 fichiers |
| `docs/etat-des-lieux/` | complet (8 dépôts + synthèse) | 10 fichiers |
| `docs/audits/` (interne, externe, sécurité, coûts) | complet | 7 fichiers |
| `docs/agents/` | 13 fiches d'agents (orchestrateur, coding, gis, learning…) | `docs/agents/` |
| `learning/` CLE PoC | 2 parcours (« argent », turboréacteur) ; 1 seul implémenté (`money-poc.js`, 10.8 Ko) | `learning/` |
| `watchtower-mods/` | fork God's Eye View — globe Cesium, chantier, fiche lieu, intelTwin, voix FR/EN, capture HUD (voir `README.md`, 38 Ko) | `watchtower-mods/` |

## C6 — Données & ressources

- Aucun `raw/`, aucune donnée métier ; **10+ images générées** (Gemini/Canva) pèsent l'essentiel des 22.9 Mo avec `watchtower-mods` (README 38 Ko, index.html 55 Ko, vite.config 343 Ko).

## C7 — Documentation & références

- 53 fichiers Markdown : gouvernance (10), état des lieux (10), audits (7), agents (13), architecture (4), +
- Références externes : dépôt upstream God's Eye View, sources FR (SOURCES-FR.md).

## C8 — Tests & qualité

- **0 test**, 0 CI, 0 lint. Aucun script de vérification.

## C9 — Sécurité & secrets

- Scan : 0 secret, 0 `.env`, 0 fichier d'identifiants (le fichier historique `identifiants_cognitorium*.json` a été purgé — cf. `docs/audits/internal/001-audit-global.md` §10).
- Les clés optionnelles (Google Maps, Cesium ion) restent côté navigateur (localStorage) — usage documenté.

## C10 — Exécution & déploiement

- Lancement : `python -m http.server 8000` → `learning/` (README).
- Preview monorepo : `learning/index.html` (détecté par `app/main.py::detect_preview_entry`).
- `watchtower-mods/` n'a **pas de build committée** dans ce dépôt (le build vit dans le dépôt `watchtower`).

## C11 — Dette technique & risques

1. **Double vie du fork** : `watchtower-mods/` (ici) vs dépôt `watchtower` (583 fichiers) — deux copies du même code, dérive possible (déjà constatée : `main` watchtower n'a ni import CSV ni base INTEL).
2. `vite.config.js` de 7 821 lignes = point de fragilité unique (15+ proxys dans un seul fichier).
3. Images non nommées dans Git (22 Mo).
4. Gouvernance très en avance sur le code (53 docs pour 2 PoC) → risque de « documentation-théâtre ».

## C12 — Maturité & complétude

**M2 `prototype`** — la couche documentaire est M4, la couche code est M2 (PoC sans tests ni build reproductible).
**Prochaine étape** : trancher le sort du fork (fusionner `watchtower` et ce module), sortir les images du dépôt, formaliser `learning/`.

## Findings

| # | Sévérité | Catégorie | Constat | Preuve | Recommandation |
|---|---|---|---|---|---|
| F-CG-01 | élevé | C2 | 13 commits OSINT non fusionnés (dont `src/osint/*`) | `audit/data/branches.json` | fusionner ou abandonner explicitement |
| F-CG-02 | moyen | C11 | fork Cesium dupliqué entre 2 dépôts | `watchtower-mods/` vs `projects/watchtower/` | définir la source de vérité (ADR) |
| F-CG-03 | moyen | C6 | 10+ images ~20 Mo dans Git | inventaire | sortir du dépôt |
| F-CG-04 | faible | C9 | clés API utilisateur en localStorage (par design) | `watchtower-mods/README.md` | documenter le risque XSS |
