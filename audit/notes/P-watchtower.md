# P — `watchtower` (God's Eye View / WATCHTOWER)

**Audit** : fait (2026-10-07) · **Risque global** : moyen · **Maturité** : **M3 `alpha`** (le plus avancé du monorepo)
**Résumé** : tour de veille géospatiale CesiumJS (fork « God's Eye View »), 583 fichiers, **190 453 lignes de code**, **208 fichiers de test**, **seule CI du monorepo**, registre de 86 outils, 43 commits d'audit + une PR #3 ouverte (carte stratégique + base INTEL).

## C1 — Identité & provenance

| Fait | Valeur | Preuve |
|---|---|---|
| Dépôt | `Sathancabrol/watchtower`, public | `gh repo list` |
| Créé / dernier push | 2026-09-01 / **2026-10-07 09:32** | idem |
| SHA `main` | `d44ef7c4` (2026-09-07) | `gh api` |
| Licence | **MIT** — `Copyright (c) 2026 Bilawal Sidhu` : **c'est un fork** de `bilawalsidhu/gods-eye-view`, non marqué « fork » sur GitHub | `LICENSE` |
| Version | 0.1.1 (`package.json`), CHANGELOG à jour | `CHANGELOG.md` |
| Branches | 5 — **2 avec travail non fusionné** | `branches.json` |

## C2 — Dépôt, branches & synchronisation

| Branche | Avance | Contenu | État |
|---|---:|---|---|
| `arena/dec9cd88-watchtower` | +7 / 623 fichiers | **PR #3 ouverte** : carte stratégique, import CSV (7 types), base INTEL territoriale, veille, lacunes, sources | **CI verte** (5 runs récents « success ») |
| `arena/01a072e1-watchtower` | **+43** / 650 fichiers | 43 commits : docs/audit + UI (volant, carte 2D, panneau FIL, niveaux INTEL) | non fusionnée, 10 commits de retard |
| 3 autres | 0 | mortes / déjà fusionnées | supprimables |

- Copie locale = `main` (583 fichiers, 0 écart) → **INTEL, import CSV et 43 commits sont absents de la copie monorepo**.

## C3 — Structure & volumétrie

| Mesure | Valeur |
|---|---|
| Fichiers / taille | 583 / 22.8 Mo (dont `src/` 446 fichiers, 16.1 Mo) |
| LOC-code | **190 453** (dont ~30 000 de tests) |
| Tests | **208 fichiers** `*.test.mjs` |
| Documents | 35 Markdown (`docs/` 11, `audit/` 5, racine 10) + `audit/reference/` |
| Données locales | 19 fichiers (`dams`, `datacenters`, `natural_earth`, `neighborhoods`, câbles sous-marins) |
| Scripts | 59 (`qa-*.mjs`, `pinokio-*`, `dev-*`) + `tools/` (6, dont rendu Cesium headless) |

## C4 — Stack & dépendances

- **CesiumJS 1.124** + vite-plugin-cesium, Vite 6, `@mapbox/vector-tile`, `pbf`, `satellite.js`, `mgrs`, `egm96-universal` ; dev : `puppeteer`, `sharp`, `ws`.
- Scripts npm : `doctor`, `dev`, `dev:secure`, `build`, `preview`, `test`, `test:track`, `qa:map-source-tray`.
- CI : `.github/workflows/ci.yml` — matrix Node 24.14/26, `npm ci`, `doctor`, `npm test`, build + job **Windows onboarding** (Pinokio).

## C5 — Fonctionnalités & modules

- Mesuré sur la branche INTEL (07/10) : **29 docks**, **29 calques 3D**, **7 vues INTEL**, 102 modules de données, 105 modules de code, 29 sources déclarées (`src/tracabilite.js`, 6 familles), 39 clés localStorage `watchtower.*.v1`.
- Capacités vérifiées : navigation France → parcelle, bâti 3D + cadastre IGN + Panoramax, interrogation en direct (Géorisques, recherche-entreprises, GDELT, Open-Meteo, USGS, EONET, AIS, OpenSky), fonctionnement hors réseau sur le classeur territorial, import CSV avec traçabilité, export JSON/CSV (`tools/exporter-intel.mjs`), régénération reproductible des bases (SHA-256), 81 fiches d'imprévus TP.
- `docs/CURRENT-STATE.md` : journal de comportement runtime très détaillé (premières-règles, politiques d'affichage, clés absentes).

## C6 — Données & ressources

- Bases locales versionnées (dams/datacenters/regions/marine/câbles), fixtures voix (`scripts/fixtures/voice/*.wav`), `public/models` (glb).
- Bases territoriales générées : dossier Frontignan, atlas de Thau, veille officielle (branches).
- Attention : `dist/` cesium assets committés (comportement voulu pour preview).

## C7 — Documentation & références

- `audit/REFERENCE.md` (**193 Ko**) + `REGISTRE-OUTILS.json`/`.tsv` : **86 outils** en 12 catégories (55-56 copiables libres, 68 sans clé, 12 avec compte gratuit, 2 payants), `doctor.py`, `cherche.py`, `generate-reference.py`.
- `AGENTS.md` généré (mode d'emploi du repo), `CAPACITES-AGENT.md` (25 tâches cotées), `COUTS-LICENCES-LEGAL.md`, `RND-PROPOSITIONS-2026.md`, `DATA_SOURCES.md`, `SECURITY.md`, `TESTING.md`, `ROADMAP.md` (itération 21).
- Règle éditoriale forte : sources datées, licences vérifiées sur le fichier LICENSE, « zéro clé par défaut ».

## C8 — Tests & qualité

**Vérifié le 2026-10-07** (sans `node_modules`, Node v22.22.3) :

```
node scripts/run-unit-tests.mjs → 1454 sous-tests | 1344 pass | 109 fail | 1 skip
```

Analyse des 109 échecs : **tous `ERR_MODULE_NOT_FOUND`** (`cesium`, `egm96-universal`, `vite`…) — conséquence de l'absence de `npm ci`, **pas des bugs**. La branche auditée revendique `3 255 tests (3 254 ok, 1 skip)` avec dépendances installées ; la CI GitHub de la PR #3 est **verte**.

## C9 — Sécurité & secrets

- `SECURITY.md` : modèle explicite (client local-first sur données **publiques**, pas un service durci) + canal de divulgation privé.
- Aucun secret committé (scan : seuls `.env.example` ressortent — faux positifs).
- Règle projet : `.env` en 600, pas de binding `0.0.0.0`, `ALLOW_FRAMING=1` réservé aux previews.
- Ancienne mention : `npm run dev` bloque les tuiles OSM qui refusent l'app (documenté).

## C10 — Exécution & déploiement

```bash
npm ci && npm run dev        # dev server Vite (port 4173 par défaut)
npm run doctor -- --json     # état réel de la machine (exit 1 si socle incomplet)
npm test                     # 208 fichiers de test
npm run build                # dist/ (assets relatifs, committé pour la preview)
```

- Installation 1-clic via **Pinokio** (`pinokio/*`, scripts Node, job CI Windows).
- Preview monorepo : `dist/index.html` fonctionnelle.

## C11 — Dette technique & risques

1. **Main en retard sur les branches** : la PR #3 (INTEL/CSV) attend depuis le 06/10 ; `arena/01a072e1` (+43 commits) n'a pas de PR.
2. Licence MIT d'un **fork** : l'attribution upstream est dans `LICENSE` mais le README ne dit pas clairement « fork de gods-eye-view ».
3. `src/ui.js` = 10 310 lignes (plus gros fichier) ; module monolithique.
4. `dist/` + assets Cesium committés (poids, dérive build/source).
5. Dépendance aux services tiers gratuits (régression de quota = premier risque) — déjà identifié dans `AGENTS.md` §9.

## C12 — Maturité & complétude

**M3 `alpha`** — exécutable, testée (208 fichiers), CI verte, docs d'exploitation complètes ; pas encore M4 (deux branches divergentes, pas de release, attribution fork à clarifier).

## Findings

| # | Sévérité | Catégorie | Constat | Preuve | Recommandation |
|---|---|---|---|---|---|
| F-WT-01 | élevé | C2 | PR #3 (INTEL + import CSV) ouverte, CI verte, non fusionnée depuis 1 jour ; +43 commits sur `01a072e1` sans PR | `gh pr list`, `gh run list` | fusionner la PR #3, ouvrir une PR pour `01a072e1` |
| F-WT-02 | moyen | C1 | fork MIT attribué mais non déclaré dans le README | `LICENSE` vs `README.md` | mention « fork de … » |
| F-WT-03 | moyen | C3 | `src/ui.js` 10 310 lignes | `wc -l` | découper par domaine |
| F-WT-04 | faible | C10 | `dist/` + assets Cesium committés | inventaire | reconstruire en CI, ne plus committer |
| F-WT-05 | info | C8 | 109 échecs de tests en local par dépendances absentes | run mesuré | documenter `npm ci` obligatoire |
