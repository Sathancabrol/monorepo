---
provenance: interview-mined
instantiated: 2026-10-08
method: WORKFLOW/Interview.md — étape 5 « External sources » appliquée au monorepo entier
status: PARTIEL — les champs minés sont sourcés, le reste est marqué TODO
---

# USER — instance réelle de Nathan

> Instancié le 2026-10-08 pendant la Phase 2 du Life Hub, en **minant le monorepo** (docs/, projects/, MANIFEST.json, historique de session) plutôt qu'en repartant de zéro. Chaque fait ci-dessous a une source dans le repo ; tout le reste est `TODO (interview)`.
> Le template d'origine reste intact dans `../template/USER/` — cette instance est l'arbre vivant.

## Ce qui est rempli (miné, sourcé)
- `BASICINFO.md` — identité, lieu, timezone, langue, devises, emails
- `ABOUTME.md` — profil, centres d'intérêt, valeurs de travail
- `PROJECTS.md` — inventaire des projets du monorepo
- `GEAR.md` — matériel actuel + plan d'achat (issu de `docs/HARDWARE-LIFE-HUB.md`)
- `TECHSTACKPREFERENCES.md` — préférences techniques établies pendant la session
- `TELOS/CURRENT_STATE/` — INFRASTRUCTURE, CREATIVE, SNAPSHOT
- `CONFIG/LIFEOS_CONFIG.toml` — bloc `[principal]` rempli

## Ce qui attend l'interview (rien n'est inventé)
- `CONFIG/LIFEOS_CONFIG.toml` → `[da]` : **nom de l'assistant** + voix (étape 1 du workflow)
- `TELOS/MISSION.md` + `TELOS/IDEAL_STATE/` — cap de vie et état idéal (étape 4)
- `FINANCES/` — comptes, revenus, enveloppes (aucune donnée dans le repo)
- `HEALTH/` — non abordé
- `CONTACTS.md` — personnes qui comptent
- `TELOS/CURRENT_STATE/RELATIONSHIPS.md`, `RHYTHMS.md`, `FREEDOM.md`

## Règle
Jamais d'invention : un champ vide reste vide avec `TODO (interview)`. Toute mise à jour garde le frontmatter `last_updated` à jour.
