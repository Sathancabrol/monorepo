# S0 — Racine : dossier de marché/chantier

**Mesuré** : 2026-10-07 · **Méthode** : `ls` + `python3 scripts/audit_s0_map.py` + `docs/DOSSIER-CHANTIER-INDEX.md`
**Verdict** : 224 fichiers à la racine = **220 documents de marché/chantier + 4 fichiers de dépôt**.

## Faits

| Fait | Valeur | Preuve |
|---|---|---|
| Fichiers à la racine | 224 | `python3 scripts/audit_inventory.py --all` → `S0-racine-fichiers-directs` |
| Documents de marché | 220 | `audit/data/S0-mapping.json` (`documents: 220`) |
| Fichiers de dépôt | 4 (`README.md`, `MANIFEST.json`, `requirements.txt`, `.gitignore`) | idem (`repo_files`) |
| Taille cumulée | 225.1 Mo | idem |
| Index existant | `docs/DOSSIER-CHANTIER-INDEX.md` — 220 cités, 0 manquant | contrôle croisé `cited vs files` |
| Extensions | 167 `.pdf`, 17 `.xlsx`, 15 `.xls`, 8 images, 3 `.doc`, 3 `.docx`, 3 `.ppt`, 2 `.rtf` | inventaire |
| Nature | **aucun code** — documentation et données de chantier | inventaire |

## Cartographie canonique (12 familles, 0 orphelin)

| Famille canonique | Fichiers | Taille | Part |
|---|---:|---:|---:|
| Pièces de marché (DCE) | 30 | 27.4 Mo | 12.2 % |
| Devis, prix & budget | 9 | 9.9 Mo | 4.4 % |
| Prescriptions d'exécution (série F) | 30 | 56.9 Mo | 25.3 % |
| Plans & profils | 23 | 18.9 Mo | 8.4 % |
| Suivi de chantier | 29 | 5.7 Mo | 2.5 % |
| Études, essais & qualité | 23 | 14.1 Mo | 6.3 % |
| Signalisation, sécurité & AIPR | 17 | 41.7 Mo | 18.5 % |
| Réseaux, DT/DICT & autorisations | 13 | 4.2 Mo | 1.9 % |
| Ressources humaines & administration | 6 | 7.3 Mo | 3.3 % |
| Références techniques & fournisseurs | 35 | 29.1 Mo | 12.9 % |
| Juridique (recours & litiges) | 2 | 0.2 Mo | 0.1 % |
| Images & vues | 3 | 9.7 Mo | 4.3 % |
| **Total** | **220** | **225.1 Mo** | **100 %** |

Définition des familles : `audit/CATEGORIES.md` §1.1. Reproductible : `python3 scripts/audit_s0_map.py`.

## Constats (à confirmer par lecture quand nécessaire)

1. **Deux projets distincts mélangés à plat** : le dossier couvre au moins « Lotissement la croix Pruniaux (Aurouer) », « Giratoire de Barbazan », « NOE » et des pièces « ARROUER/BARBAZAN » — le nom des fichiers ne permet pas toujours d'attribuer un document à un chantier. `docs/DOSSIER-CHANTIER-INDEX.md` ne tranche pas non plus.
2. **Doublons apparents** (même objet, noms différents) : `CCAP.pdf` vs `04 - CCAP.pdf` vs `Cahier des Clauses Administratives Particulières.pdf` ; `CCTP.pdf`, `05 - CCTP.pdf`, `CCTP LOT1.pdf`, `LOT 2 CCTP.pdf` ; `Acte d'engagement.pdf` vs `03 - Acte d'engagement.pdf` vs `AE.doc` ; `planning BARBAZAN.xls` vs `planning BARBAZAN (Enregistré automatiquement).xls`/`.pdf` ; `PLAN-SITUATION.pdf` vs `Plan de situation.pdf` vs `plan de situation 10000.pdf` ; `ordre de service.pdf` vs `lordre-de-service.pdf` ; `Réglement de consultation.pdf` vs `REGLEMENT-CONSULTATION.pdf`.
3. **Numérotation « 00 → 10 »** (`00 - Cartouche…` à `10 - Récepissés DT`) : série DCE incomplète (pas de 01 visible) — à vérifier.
4. **Séries F incomplètes** : F2, F23–F29, F31, F32, F34–F36, F39, F62-V, F64–F67, F70–F78, F81-II, F82, F85 (30 pièces) — il manque de nombreux numéros de la collection (normal : seules les pièces du marché sont là).
5. **Doublons de format** : `Recours Barbazan.docx` + `Recours Barbazan.pdf` ; `planning BARBAZAN…xls` + `.pdf`.
6. **Contenu potentiellement sensible** : `salaire_minima_hierarchiques_occitanie_2022_0.pdf`, `tableau_reclassement_ETAM.pdf` (grilles salariales), `AIPR CORRECTION.xlsx`/`aipr test complet.xlsx` (réponses QCM), `chantier…` (noms de personnes : « Nathan », « Noé »). Aucun secret technique détecté.
7. **Poids Git** : 225 Mo de binaires dans le dépôt `monorepo` (316 Mo au total côté GitHub) — c'est la cause principale de la taille du dépôt.

## Findings S0

| # | Sévérité | Catégorie | Constat | Preuve | Recommandation |
|---|---|---|---|---|---|
| F-S0-01 | moyen | C6 Données & ressources | 225 Mo de binaires à plat dans la racine, sans arborescence | `ls`, inventaire | ranger par chantier (`chantiers/<nom>/`) ou externaliser |
| F-S0-02 | moyen | C7 Documentation & références | Attribution chantier ambiguë pour une part des 220 fichiers | cartographie S0 | ajouter une colonne « chantier » au `DOSSIER-CHANTIER-INDEX.md` |
| F-S0-03 | faible | C6 Données & ressources | Doublons apparents (≥ 10 paires) | liste ci-dessus §2 | dédupliquer ou marquer « version de travail » |
| F-S0-04 | faible | C9 Sécurité & secrets | Grilles salariales + corrigés AIPR exposés publiquement (repo public) | inventaire | décider : garder (données publiques) ou retirer |
