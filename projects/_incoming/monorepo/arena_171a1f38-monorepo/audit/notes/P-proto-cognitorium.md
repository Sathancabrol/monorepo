# P — `proto-cognitorium`

**Audit** : fait (2026-10-07) · **Risque global** : élevé · **Maturité** : M3 `alpha` (local M2 — périmé)
**Résumé** : le « Core applicatif » de la vision Cognitorium — app React 19 + serveur Express + Gemini. Code le plus riche en fonctionnalités ; **copie locale en retard de 25 fichiers sur `main`**, tous liés à l'authentification/onboarding arrivés le 2026-09-10.

## C1 — Identité & provenance

| Fait | Valeur | Preuve |
|---|---|---|
| Dépôt | `Sathancabrol/proto-cognitorium`, public | `gh repo list` |
| Créé / dernier push | 2026-08-24 / **2026-09-10** | idem |
| SHA `main` réel | `74e301e4` — `feat(auth): implement onboarding and authentication flow` | `gh api` |
| SHA de référence local | `05058b39` (MANIFEST) | `MANIFEST.json` |
| Licence | **aucune** | `find` |
| PR | 6 fusionnées (toutes ≤ 2026-08-26) ; **le commit du 10/09 n'a pas de PR** (push direct, audit de branche) | `gh pr list`, `docs/AUDIT_2026-09-10…md` |

## C2 — Dépôt, branches & synchronisation

- **Dérive confirmée** : local 161 fichiers / distant 184 ; **+25 fichiers distants**, 12 fichiers modifiés (`audit/data/drift.json`).
  Fichiers manquants localement : `src/components/auth/*` (9 fichiers, dont `CognitoriumObsidianGraph.tsx` 1 287 lignes), `AccountLoginGate.tsx`, `MultiProjectsView.tsx`, `TargetedCvView.tsx`, `cv/*`, `data/cognitiveBiasesData.ts`, `types/authTypes.ts`.
- Branche de travail : `arena/01a08342` — **+5 commits** (2026-09-10) : `tools/audit/*` (5 sondes) + 3 rapports `docs/AUDIT_2026-09-*.md` + `docs/TRACEABILITE.csv`.
- 6 autres branches = mortes (0 commit d'avance, jusqu'à −54 de retard).

## C3 — Structure & volumétrie

| Mesure | Local | Distant `main` |
|---|---:|---:|
| Fichiers | 161 | 184 |
| Taille | 73.8 Mo | 94 Mo (diskUsage GitHub) |
| LOC-code | 53 334 | **67 787** lignes `src/` + `server.ts` (audit branche) |
| Composants `.tsx` | — | **52** |
| `raw/` | 61 fichiers, **64 Mo** | idem |

## C4 — Stack & dépendances

- React 19.0.1 · Vite 6.2.3 · TypeScript 5.8 · Express 4.21 · `@google/genai` 2.4 · three 0.185 · Tailwind 4.1 · motion · canvas-confetti · lucide-react.
- **Deux lockfiles** (`bun.lock` + `package-lock.json`) — source de vérité ambiguë.
- Scripts : `dev` (tsx server.ts), `build` (vite build + esbuild serveur), `start`, `lint` (tsc --noEmit).

## C5 — Fonctionnalités & modules

- Graphe 5 niveaux (Expérience → Tâche → Compétence → Cognition → Matching), échelle épistémique, courbe d'oubli (Ebbinghaus), moteur ROME (1 911 fiches, 17 920 compétences — `src/data/romeData.ts`, 5.5 Mo), extraction CV par IA, modes graphe/arbre/tableau/timeline, atlas de psychologie, laboratoire d'expériences, 10 biais cognitifs, profils réels (4).
- **Nouveau sur `main` (non-local)** : parcours d'authentification/onboarding complet (9 composants `auth/`), gestion multi-projets, CV ciblé, gestionnaire de profils.
- `server.ts` : proxy IA (Gemini) — clé côté serveur.

## C6 — Données & ressources

- `raw/` = 61 fichiers, **64 Mo** : `slide carte représentation.pptx` (21.8 Mo), `Manuel_exploitation.pdf`, `Cabrol.Rapport de stage.pdf`, `Soutenance-fin-de-stage-FINAL.pdf`, guides SeQuelec/terrassement…
- `src/data/romeData.ts` : **5.5 Mo** embarqués dans le bundle (déjà noté comme dette).

## C7 — Documentation & références

- Local : `docs/ANALYSE_VERSIONS.md`, `ANALYSE_RAW.md`, `CONSOLIDATION.md` (3 fichiers, 57 docs comptés incluent les .md de `raw`).
- Distant : 5 docs supplémentaires (3 audits datés 08/09/10-09, roadmap, traçabilité).
- **Les audits de branche sont une source d'état réelle** (`docs/AUDIT_2026-09-10_main_74e301e.md` : 45 anomalies relevées, `tsc` 0 erreur, build 7 026 kB).

## C8 — Tests & qualité

- **0 test dans le dépôt** (toutes branches) ; `lint` = `tsc --noEmit` (0 erreur au 10/09).
- Outillage d'audit non fusionné : `tools/audit/content-audit.mjs`, `data-audit.mjs`, `interaction-probe.mjs`, `rome-diagnostic.mjs`, `runtime-probe.mjs`.

## C9 — Sécurité & secrets

- 1 « nom sensible » détecté par l'inventaire (`package-lock.json` — faux positif de règle).
- **Antécédent documenté** : `raw/identifiants_cognitorium*.json` a existé puis a été purgé → recommander rotation (cf. `COGNITORIUM/docs/audits/internal/001-audit-global.md` §10).
- Clé Gemini via `.env` (`.env.example` présent dans les autres projets, pas ici) — à vérifier au déploiement.

## C10 — Exécution & déploiement

- `npm run dev` → tsx `server.ts` (Express + Vite middleware) ; `npm run build` → `dist/` (front) + `dist/server.cjs`.
- Preview monorepo : `dist/index.html` (build committée, 73.8 Mo avec `raw/`).
- Le rebuild exige `npm ci` (node_modules absents) + `GEMINI_API_KEY` pour les fonctions IA.

## C11 — Dette technique & risques

1. **Copie locale périmée** (25 fichiers manquants dont tout le module auth) → l'audit local ne reflète pas le produit.
2. `raw/` 64 Mo + `romeData.ts` 5.5 Mo dans Git → dépôt 94 Mo, bundle lourd.
3. Deux lockfiles ; aucun test ; pas de CI ; pas de PR sur le dernier `main`.
4. 45 anomalies ouvertes listées par l'audit de branche (non reprises dans `main`).
5. Dépendance dure à Gemini (pas d'abstraction LLM — ADR-008 ouverte).

## C12 — Maturité & complétude

**M3 `alpha`** pour `main` distant (app fonctionnelle, auth, build OK, mais 0 test) ; **M2 `prototype`** pour la copie locale (périmée).
**Prochaine étape** : resynchroniser la copie locale, fusionner la branche d'audit (outils de sondes), écrire les premiers tests, sortir `raw/`.

## Findings

| # | Sévérité | Catégorie | Constat | Preuve | Recommandation |
|---|---|---|---|---|---|
| F-PC-01 | élevé | C2 | copie locale en retard de 25 fichiers / 12 modifiés vs `main` | `audit/data/drift.json` | resynchroniser |
| F-PC-02 | élevé | C6 | 64 Mo de `raw/` + 5.5 Mo de données ROME dans Git | inventaire | LFS / hors dépôt / lazy-load |
| F-PC-03 | moyen | C8 | 0 test, 0 CI ; sondes d'audit non fusionnées | `tools/audit/` (branche) | fusionner + brancher en CI |
| F-PC-04 | moyen | C4 | deux lockfiles concurrents | `bun.lock`, `package-lock.json` | choisir un gestionnaire |
| F-PC-05 | moyen | C9 | antécédent de secrets en clair (purgé) | doc interne COGNITORIUM | rotation + `.gitignore` renforcé |
