# P — `animation-chronos`

**Audit** : fait (2026-10-07) · **Risque global** : faible · **Maturité** : M2 `prototype`
**Résumé** : expérience visuelle React/Vite (« Ferrofluid Consciousness Vessel ») — 20 fichiers source, 9 composants, 6 images générées. Aucun README, aucun test, aucun rattachement documenté à la vision.

## C1 — Identité & provenance

| Fait | Valeur | Preuve |
|---|---|---|
| Dépôt | `Sathancabrol/animation-chronos`, public | `gh repo list` |
| Créé / dernier push | 2026-09-02 / 2026-09-02 | idem |
| SHA `main` | `38c57a36` — `feat: initialize ferrofluid consciousness vessel` | `gh api` |
| Licence | **aucune** | `find` |
| Branches | 1 seule | `branches.json` |

## C2 — Dépôt, branches & synchronisation

- Écart local/distant limité à 2 fichiers de configuration : `package-lock.json` (local seulement) et `public/assets/aistudio/.gitignore` (distant seulement) — pas de travail perdu.

## C3 — Structure & volumétrie

| Mesure | Valeur |
|---|---|
| Fichiers / taille | 30 / 3.8 Mo (dont `dist/` committé) |
| LOC-code / données-doc | 2 583 / 4 362 (dont `stages.ts` et images) |
| `src/` | 20 fichiers : 9 composants (`ChronosBubble`, `VesselStage`, `InspectionLens`, `MonographDrawer`, `ProgressiveDiscoveryBar`…), `stages.ts`, 6 images |
| Docs | **0** (aucun README) |

## C4 — Stack & dépendances

- React 19 · Vite 6 · TypeScript 5.8 · motion · lucide-react · Tailwind 4 · Express + dotenv · `@google/genai` 2.4.
- `package.json` : `"name": "react-example"`, `"version": "0.0.0"` — **métadonnées non personnalisées** (artefact Google AI Studio).
- `.env.example` : `GEMINI_API_KEY` (injectée par AI Studio).

## C5 — Fonctionnalités & modules

- Narration progressive : barre de découverte, séquence de transitions, lentille d'inspection, tiroir monograph.
- `metadata.json` : « Photorealistic 3D scientific-art visualization of an organic ovoid glass vessel containing black ferrofluid suspended in microgravity near an event horizon » ; capacité déclarée : `MAJOR_CAPABILITY_SERVER_SIDE_GEMINI_API`.

## C6 — Données & ressources

- 6 images JPG générées (≈ 3 Mo) dans `src/assets/images` + `dist/assets`.
- Aucune donnée métier.

## C7 — Documentation & références

- **Aucune documentation** : ni README, ni description d'intention (le lien avec la vision Cognitorium n'est documenté qu'ailleurs, dans `COGNITORIUM/docs/etat-des-lieux/07-animation-chronos.md`).

## C8 — Tests & qualité

- **0 test**, 0 CI ; `lint` = `tsc --noEmit` (déclaré).

## C9 — Sécurité & secrets

- Aucun secret. `.env.example` avec placeholder (faux positif du scan).

## C10 — Exécution & déploiement

- `npm run dev` (Vite, port 3000, `--host 0.0.0.0`) · `npm run build` → `dist/` committé, `--base=./`.
- Preview monorepo fonctionnelle (`dist/index.html`).

## C11 — Dette technique & risques

1. **Projet orphelin documentairement** : aucun README, aucune intention écrite, pas de rattachement à la vision (« à archivier ou rattacher », déjà noté dans `09-synthese.md`).
2. `package.json` générique AI Studio (`react-example`).
3. ~3 Mo d'images dans Git ; `dist/` committé.

## C12 — Maturité & complétude

**M2 `prototype`** — visuel soigné, exécutable, mais sans documentation, tests ni usage cible défini.
**Prochaine étape** : écrire un README d'intention (ou archiver, décision MA).

## Findings

| # | Sévérité | Catégorie | Constat | Preuve | Recommandation |
|---|---|---|---|---|---|
| F-AC-01 | moyen | C7 | 0 documentation, 0 README dans un dépôt public | `ls` | README d'intention ou archivage |
| F-AC-02 | faible | C4 | `package.json` non renommé (`react-example`) | `package.json` | personnaliser |
| F-AC-03 | info | C8 | 0 test / 0 CI | inventaire | — (projet visuel) |
