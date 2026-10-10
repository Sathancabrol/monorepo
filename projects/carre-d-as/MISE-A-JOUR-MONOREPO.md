# Carré d'As Tutorat — mise à jour des modules (monorepo)

Ce dossier est une copie de travail de **`dojofinancier/app4as`** (commit source `c66eb3a4d745c212ca9c833a335d639087e4f9f9`, branche `main`), importée dans le monorepo comme les autres modules de `projects/`. Le `.git` d'origine et le binaire `stripe.exe` (31 Mo) ne sont pas inclus.

## 1. Comparaison avec les modules externes du monorepo

| Module externe (`projects/…`) | Versions relevées | Décision pour Carré d'As |
|---|---|---|
| `animation-chronos`, `proto-cognitorium` | React `^19.0.1`, Tailwind `^4.1.14`, TypeScript `~5.8.2`, Vite `^6.2.3`, lucide-react `^0.546.0` | Carré d'As est une app **Next.js** (pas Vite). On s'aligne sur **React 19** et **Tailwind 4** (même génération). Vite/Three/Express ne sont pas nécessaires à Carré d'As. |
| `watchtower` | Cesium `^1.124.0`, Vite `^6.0.0` | Sans lien avec Carré d'As (globe 3D). Aucune dépendance commune à aligner. |
| `COGNITORIUM`, `HCSM`, `reaserch-engine`, `Language-decoder`, `ETAT-DE-LART-PSYCHOLOGIE` | pas de `package.json` à la racine (Python / JS statique) | Aucun module npm partagé avec Carré d'As. |

Les copies des modules externes ont été comparées aux dépôts GitHub `Sathancabrol/*` : `proto-cognitorium` a un commit plus récent (2026-09-10) que la copie du monorepo ; non traité ici (hors périmètre Carré d'As).

## 2. Versions Carré d'As : avant → après

Versions « latest » vérifiées sur npm (dist-tag `latest` stable ; les RC/canary de Prisma et TypeScript ont été écartés).

| Type | Paquet | Avant | Après |
|---|---|---|---|
| dep | `next` | ^16.0.8 | ^16.4.0 |
| dep | `react` / `react-dom` | ^19.2.0 | ^19.3.0 |
| dep | `@prisma/client` | ^6.18.0 | ^7.10.0 |
| dep | `@prisma/adapter-pg` (nouveau) | — | ^7.10.0 |
| dep | `pg` (nouveau) | — | ^8.23.1 |
| dep | `stripe` | ^18.0.0 | ^23.0.0 |
| dep | `@stripe/stripe-js` | ^8.1.0 | ^10.0.0 |
| dep | `@stripe/react-stripe-js` | ^5.2.0 | ^7.0.0 |
| dep | `@supabase/supabase-js` | ^2.76.1 | ^2.117.3 |
| dep | `@supabase/ssr` | ^0.6.1 | ^0.12.7 |
| dep | `zod` | ^3.24.1 | ^4.6.5 |
| dep | `@hookform/resolvers` | ^3.10.0 | ^5.9.1 |
| dep | `react-hook-form` | ^7.54.2 | ^7.89.0 |
| dep | `lucide-react` | ^0.469.0 | ^1.55.0 |
| dep | `recharts` | ^3.3.0 | ^3.10.1 |
| dep | `tailwindcss` | ^3.4.17 | ^4.3.3 |
| dep | `tailwind-merge` | ^2.6.0 | ^3.7.0 |
| dep | `tailwindcss-animate` | ^1.0.7 | **retiré** → `tw-animate-css` ^1.4.0 (dev) |
| dep | `autoprefixer` | ^10.4.21 | **retiré** (intégré à Tailwind 4) |
| dep | `@netlify/functions` | ^4.3.0 | ^6.0.2 |
| dep | `date-fns`, `date-fns-tz`, `clsx`, `class-variance-authority`, `postcss`, `@radix-ui/*` | — | dernières 1.x / 4.x / 2.x (patch/minor) |
| dev | `typescript` | ^5.9.3 | ^6.0.3 (voir §4) |
| dev | `prisma` | ^6.18.0 | ^7.10.0 |
| dev | `eslint` / `eslint-config-next` | ^9.18.0 / ^15.1.4 | ^10.12.0 / ^16.4.0 |
| dev | `@types/node` | ^22.18.10 | ^26.6.5 |
| dev | `@types/react` / `@types/react-dom` | ^19.0.0 | ^19.3.0 |
| dev | `@netlify/plugin-nextjs` | ^5.9.4 | ^5.16.2 |
| dev | `@tailwindcss/postcss` (nouveau) | — | ^4.3.3 |
| dev | `dotenv` (nouveau, pour `prisma.config.ts`) | — | ^18.0.7 |

## 3. Adaptations de code (breaking changes traités)

- **Prisma 7** : générateur `prisma-client` (sortie `lib/generated/prisma`, ignorée par Git et régénérée par `npm run prisma:generate`), URL déplacée dans `prisma.config.ts`, `directUrl` retiré du schéma (les migrations utilisent `DIRECT_URL` si défini). Le client utilise l'adaptateur `@prisma/adapter-pg` via la fabrique unique `lib/db-client.ts` (app, fonctions Netlify, seed, scripts).
- **Stripe 23** : `payment_method_types` → `allowed_payment_method_types` (SetupIntent, toujours « carte uniquement ») ; `apiVersion` épinglée à `2026-09-30.endive` (version du SDK 23). ⚠️ Le format des événements webhook peut avoir changé entre `2025-08-27.basil` et cette version : à valider avec un événement de test.
- **Tailwind 4** : `app/globals.css` utilise `@import "tailwindcss"`, `@config` (config JS conservée), `@custom-variant dark` (remplace `darkMode: ["class"]`) et `tw-animate-css`. PostCSS : `@tailwindcss/postcss`. ⚠️ Des valeurs par défaut ont changé en v4 (ex. `ring` 1px au lieu de 3px, `border` en `currentColor`) : vérifier visuellement les formulaires et les boutons focus.
- **Next 16** : `middleware.ts` → `proxy.ts` (même logique : rafraîchissement de session Supabase).
- **Supabase SSR 0.12** : cookies migrés de `get/set/remove` vers `getAll/setAll` (`lib/supabase/server.ts`, `lib/supabase/middleware.ts`).
- **Recharts 3.10** : formateurs de tooltips typés (`Number(value)`, `String(value)`).
- **lucide-react 1.x, Zod 4, @hookform/resolvers 5, @netlify/functions 6** : aucune erreur de compilation après mise à jour (aucun usage de l'API Zod 3 retirée).
- **Lint** : `next lint` n'existe plus → `eslint.config.mjs` (flat config) + script `eslint .`.
- **Netlify** : `NODE_VERSION` passé de `20` à `22` (Prisma 7 exige Node ≥ 20.19 ; Next 16 ≥ 20.9). `engines` mis à jour.

## 4. Choix de version volontaires

- **TypeScript 6.0.3 et non 7.x** : `eslint-config-next` → `typescript-eslint` 8.71 accepte `typescript <6.1.0` seulement. TypeScript 7 casse donc le lint. À remonter dès que `typescript-eslint` supporte TS 7.
- **`@types/node` 26** : typage uniquement ; le runtime Netlify est Node 22.

## 5. Vérifications effectuées (dans le sandbox)

- `tsc --noEmit` : **OK** (exit 0), avec toutes les nouvelles versions.
- `next build --webpack` : **OK** (exit 0). Le build tourne sans base ni Google Fonts (contournements de test, hors dépôt).
- Démarrage `next start` : **OK**, `/connexion` = 200, CSS généré avec les classes du thème et les animations `tw-animate-css`. La page `/` renvoie 500 uniquement parce que la base PostgreSQL n'est pas joignable depuis le sandbox (`Can't reach database server`), ce qui prouve que le client Prisma 7 + adaptateur `pg` est bien branché.
- `npm audit --omit=dev` : **36 vulnérabilités (2 critiques, 30 élevées, 4 modérées) → 4 élevées**. Les 4 restantes sont dans la chaîne du CLI `prisma` (outil de build/dev, pas du runtime). Le correctif proposé par npm est un retour à Prisma 6 : non appliqué.

## 6. Limites et points restants

- **Non testé de bout en bout** : base Supabase, paiements Stripe (SetupIntent, PaymentIntent, webhooks), connexion Supabase, fonctions Netlify planifiées. Le sandbox n'a pas accès à ces services. À valider sur un environnement de préproduction (cartes de test Stripe, webhooks `stripe listen`).
- **ESLint** : 119 erreurs et 39 avertissements, pour l'essentiel des règles de style préexistantes (apostrophes non échappées dans le texte français, dépendances de `useEffect`) rendues visibles par les plugins récents. Non corrigés pour rester dans le périmètre des modules.
- **Prisma 7 en production** : vérifier la connexion via le pooler Supabase (`pgbouncer=true`) et exécuter `npm run prisma:generate` avant le build (déjà prévu dans `netlify.toml`).
- **Build sans réseau** : `next/font/google` (DM Sans) requiert l'accès à Google Fonts au build, comme avant la mise à jour.
