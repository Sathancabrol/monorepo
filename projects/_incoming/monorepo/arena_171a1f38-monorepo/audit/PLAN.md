# PLAN — Audit complet du monorepo Sathancabrol

**Audit** : `audit-2026-10` · **Démarré** : 2026-10-07 · **Mode** : agent autonome itératif
**Livrable principal** : `audit/AUDIT-2026-10.md` (tableaux complets) + ce dossier de mémoire
**Règle d'or** : aucune affirmation sans preuve locale (fichier + ligne) ou preuve GitHub (API). Toute preuve est horodatée et marquée `vérifié` / `déclaré` / `inféré` (cf. `CATEGORIES.md` §4).

---

## 1. Objectif

Produire **l'état des lieux réel** (pas déclaré) des projets du dépôt `Sathancabrol/monorepo` :
ce qui existe, ce qui fonctionne, ce qui manque, ce qui diverge, ce qui est en risque.
Public cible : le propriétaire du dépôt, pour décider des suites (consolider, archiver, câbler).

## 2. Périmètre (exhaustif)

| # | Périmètre | Contenu |
|---|---|---|
| S0 | Racine du dépôt | dossier de marché/chantier (~220 fichiers : PDF, XLS/DOC, plans, images), `README.md`, `MANIFEST.json`, `requirements.txt` |
| S1 | Infra monorepo | `app/` (FastAPI + templates), `scripts/` (inventaire GitHub, publication), `data/` (snapshot JSON), `docs/` (index chantier, inventaire, synthèse Talbot) |
| S2 | 9 projets locaux | `projects/COGNITORIUM`, `proto-cognitorium`, `HCSM`, `reaserch-engine`, `ETAT-DE-LART-PSYCHOLOGIE`, `watchtower`, `animation-chronos`, `Language-decoder`, `frontignan` |
| S3 | Réel GitHub | 9 dépôts (`Sathancabrol/*`) : SHA réels, branches, PR, issues, dates, écart avec les copies locales |
| S4 | Documents externes | connecteurs (Google Drive/Docs, Notion, Linear, Gmail) : documents de ressources et de suivi liés aux projets |

**Hors périmètre** : modification du code des projets audités. L'audit est en lecture seule ; seuls `audit/`, `scripts/audit_memory.py` et (si demandé) `docs/` sont écrits.

## 3. Méthode

1. **Preuve d'abord** : chaque ligne de tableau a une source (`chemin:ligne`, sortie de commande, ou réponse API GitHub).
2. **Double passe** : passe locale (fichiers) puis passe distante (GitHub) ; tout écart est un *finding*.
3. **Taxonomie figée** : noms de catégories définis dans `CATEGORIES.md`, réutilisés à l'identique partout.
4. **Mémoire instrumentée** : chaque étape écrit dans `audit/state.json` + `audit/JOURNAL.jsonl` via `scripts/audit_memory.py` (aucun re-scan inutile, tokens minimaux).
5. **Rejouable** : toute commande d'inventaire est consignée dans `audit/notes/` pour être relancée à l'identique.
6. **Arrêt sur preuve** : si une donnée n'est pas vérifiable, elle est marquée `inconnu` plutôt que devinée.

## 4. Processus (phases, critères de sortie)

| Phase | Nom | Travail | Critère de sortie |
|---|---|---|---|
| P0 | Cadrage & plan | périmètre, méthode, taxonomie, livrables | `PLAN.md` + `CATEGORIES.md` écrits |
| P1 | Mémoire & instrumentation | `state.json`, `MEMORY.md`, `JOURNAL.jsonl`, `graph.json`, CLI `audit_memory.py` | `audit_memory.py check` = OK |
| P2 | Inventaire factuel | comptages/tailles/LOC/langages : racine, infra, 9 projets ; vérif des 220 docs | notes `notes/S0-racine.md`, `notes/S1-infra.md`, `notes/S2-inventaire.md` |
| P3 | Audit par projet | 9 fiches projet : identité, structure, stack, fonctionnalités, données, docs, tests, sécurité, exécution, dette | 9 notes `notes/P-<projet>.md` + projets `done` dans `state.json` |
| P4 | Audit transversal | doublons, câblage, dépendances croisées, secrets, tests/CI, données volumineuses, doc coverage, naming | note `notes/S4-transverse.md` |
| P5 | Audit externe | GitHub réel (SHA, branches, PR, issues, drift) + connecteurs (Drive/Notion/Linear/Gmail) | note `notes/S3-github.md`, `notes/S4-externe.md` |
| P6 | Synthèse & tableaux | tableaux complets (une section par catégorie), synthèse par projet, notation maturité/risque, recommandations | `audit/AUDIT-2026-10.md` + `audit/AUDIT-2026-10.csv` |
| P7 | Contrôle qualité & publication | vérif croisée des chiffres, `check`, commit, push branche, PR | PR ouverte, journal à jour |

**Reprise après interruption** : lire `audit/MEMORY.md` puis `python3 scripts/audit_memory.py status` et `next`. Les phases non `done` dans `state.json` indiquent où reprendre. Ne jamais refaire une phase `done` : relire la note correspondante.

## 5. Outils utilisés

- **bash** : comptages (`find`, `du`, `wc`, `grep`), analyse de manifests, scan secrets/TODO.
- **Python stdlib** : parsing JSON/YAML-léger, statistiques, génération des tableaux.
- **`gh` CLI** : état réel GitHub (repos, branches, PR, issues, commits, contenus de branches non fusionnées).
- **`scripts/github_inventory.py`** : snapshot existant (cache serveur) — comparé au réel.
- **Connecteurs** : Google Drive/Docs (documents sources), Notion (pages projet), Linear (suivi), Gmail (pièces jointes/reçus) — uniquement pour retrouver des documents de ressources, jamais pour publier.
- **Serveur local** (`uvicorn app.main:app`) : vérification fonctionnelle des previews monorepo (à défaut, inspection statique).

## 6. Livrables

| Livrable | Chemin | Statut |
|---|---|---|
| Plan de processus | `audit/PLAN.md` | ✅ |
| Taxonomie canonique | `audit/CATEGORIES.md` | ✅ |
| Mémoire machine | `audit/state.json` | ✅ |
| Index mémoire | `audit/MEMORY.md` (généré) | ✅ |
| Journal | `audit/JOURNAL.jsonl` | ✅ |
| Graphe de connaissances | `audit/graph.json` (généré) | ✅ |
| Notes par périmètre | `audit/notes/*.md` | ✅ (14 notes : S0–S4 + 9 projets) |
| Audit externe (connecteurs) | `audit/notes/S4-externe.md` | ✅ |
| **Audit complet (tableaux)** | `audit/AUDIT-2026-10.md` | ✅ (13 sections) |
| Données tabulaires | `audit/AUDIT-2026-10.csv` | ✅ (9 lignes × 13 colonnes) |

## 7. Risques de l'audit lui-même

| Risque | Mitigation |
|---|---|
| Copie locale ≠ GitHub (dérive) | P5 compare SHA/tree ; tout écart listé comme finding |
| Fichiers volumineux non lisibles (XLS, PDF scannés) | métadonnées + extraction texte si possible ; sinon marqué `déclaré` |
| Faux positifs « secrets » | vérification contextuelle (exemples, placeholders, .env.example) |
| Coût tokens | mémoire compacte, `grep` ciblés, aucune relecture intégrale de doc déjà résumée |
| Scope flou (« tout ») | périmètre S0–S4 explicite, hors-périmètre assumé |

## 8. Discipline de mémoire (obligatoire à chaque itération)

```bash
python3 scripts/audit_memory.py status                 # où j'en suis
python3 scripts/audit_memory.py set phase.current P3   # avancer
python3 scripts/audit_memory.py fact HCSM files 86     # consigner un fait
python3 scripts/audit_memory.py log "P3 HCSM terminé" --tag P3
python3 scripts/audit_memory.py render                 # régénérer MEMORY.md + graph.json
```

Règle : **une phase n'est `done` que si sa note existe** ; un projet n'est `done` que si ses 12 catégories sont renseignées (ou marquées `n/a` avec motif).
