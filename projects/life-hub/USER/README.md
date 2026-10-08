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

## Ajouté à l'interview du 08/10 (soir)
- **DA nommé : Laplace** (`CONFIG/LIFEOS_CONFIG.toml`)
- **Budget réel importé** depuis le tableur de Nathan : `FINANCES/BUDGET-MENSUEL.md` (charges 1 088,61 € · revenus 977,10 € France travail · déficit structurel −111,51 €)
- **MONEY** : état monétaire honnête + actifs monétisables : `TELOS/CURRENT_STATE/MONEY.md`
- **MISSION v2** : exploration par hypothèses testées (M1-M3) + pistes de revenu classées (A-D), révisions à J+30 : `TELOS/MISSION.md`

## Ce qui attend encore l'interview (rien n'est inventé)
- `TELOS/IDEAL_STATE/` — à construire une fois que les tests M1-M3 auront donné des données
- `FINANCES/` — comptes bancaires, échéance des droits France Travail, statut micro-entreprise
- `HEALTH/` — non abordé
- `CONTACTS.md` — personnes qui comptent
- `TELOS/CURRENT_STATE/RELATIONSHIPS.md`, `RHYTHMS.md`, `FREEDOM.md`

## Règle
Jamais d'invention : un champ vide reste vide avec `TODO (interview)`. Toute mise à jour garde le frontmatter `last_updated` à jour.
