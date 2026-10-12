# CARTE — monorepo (Sathancabrol)

> Exemple **rempli** (vérifié dans le dépôt le 2026-10-12) : sert de référence pour
> les autres cartes. Modèle : `CARTE.template.md`.

- **Rôle** : agréger 9 projets dans **un** dépôt navigable, avec explorateur de fichiers,
  lecture Markdown/PDF et aperçus exécutables (iframe), sans casser l'autonomie de chaque projet.
- **Dernière mise à jour de cette carte** : 2026-10-12

## Arborescence utile

```text
monorepo/
├── app/main.py              → FastAPI : pages + API + serveur d'aperçus (/preview/{projet}/{chemin})
│   └── templates/           → base, index, repos, monorepo (drawer + iframe)
├── scripts/github_inventory.py  → inventaire GitHub (stdlib, paginé, snapshot JSON)
├── data/github_inventory.json   → snapshot = cache serveur (le navigateur n'appelle jamais l'API GitHub)
├── docs/                    → dont ce dossier (PARAMETRAGE-HERMES) et synthese-talbot-2026
├── projects/                → les 9 projets (chacun garde son package.json / requirements.txt)
├── MANIFEST.json            → provenance (URL, branche, SHA)
└── requirements.txt         → fastapi, uvicorn, jinja2, python-multipart
```

## Commandes qui marchent

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8123 --reload
# → /            page d'accueil
# → /monorepo    explorateur + aperçus navigables
# → /repos       panorama GitHub + graphe de fusion
# → /health      sonde

python3 scripts/github_inventory.py        # régénère le snapshot (token côté serveur uniquement)

# reconstruire les aperçus Vite (assets relatifs, indispensables pour l'iframe)
for p in animation-chronos proto-cognitorium watchtower; do
  (cd projects/$p && npm ci && npx vite build --base=./)
done
```

## Routes réelles (vérifiées)

| Route | Rôle |
|---|---|
| `GET /` · `/monorepo` · `/repos` | pages HTML |
| `GET /api/fs/list` · `/api/fs/file` | explorateur (traversal `../..` bloqué) |
| `GET /api/github/snapshot` · `/repos` · `/fusion` | données du panorama |
| `POST /api/github/refresh` | régénère le snapshot côté serveur |
| `GET /preview/{projet}[/{chemin}]` | sert une app en iframe same-origin |
| `GET /download/monorepo.bundle` | bundle du dépôt |
| `GET /health` | sonde |

## Les 9 projets

| Projet | Nature | État (source : `projects/watchtower/AUDIT-OUTILS-2026.md`) |
|---|---|---|
| `watchtower` | Vite + CesiumJS, 57 modules maison dans `COGNITORIUM/watchtower-mods` | ⚠️ le dépôt `watchtower` **en ligne** ne contient qu'un README ; les modules vivent dans `COGNITORIUM/` |
| `COGNITORIUM` | `learning/` + `watchtower-mods/` (statique) | actif, briques non packagées |
| `proto-cognitorium` | Vite + React 19 + Three.js + Express (`server.ts` non exécuté dans l'aperçu) | proto, `raw/` non nettoyé |
| `reaserch-engine` | moteur de recherche autonome (question → plan → preuve → synthèse) | v0.1 + tests ; **LLM non branché** |
| `HCSM` | modèle scientifique d'état cognitif | PROPOSED (specs, pas d'implémentation) |
| `ETAT-DE-LART-PSYCHOLOGIE` | état de l'art psycho/cognition + scripts | actif |
| `frontignan` | analyse territoriale + vision 2026-2040 | — |
| `animation-chronos` | animation TypeScript | secondaire |
| `Language-decoder` | README seul | vide |

## Pièges connus

- **Aperçu blanc** : le build Vite doit être fait avec `--base=./` (assets relatifs) ; sinon ouvre
  l'aperçu dans un nouvel onglet pour voir l'erreur console.
- **Token GitHub** : lu depuis `GITHUB_TOKEN` / `GH_TOKEN` côté serveur uniquement ; s'il manque,
  `data/github_inventory.json` reste le cache et l'API renvoie le dernier snapshot.
- **`server.ts` de proto-cognitorium** n'est pas exécuté dans l'iframe (frontend statique seul).
- **Traversal** : toute tentative `../..` renvoie 400 — c'est voulu.
- Les `.env` ne sont jamais commités (déjà dans `.gitignore`).

## Ce qui ne doit pas sortir de la machine

- Tout le **dossier de chantier TP** présent à la racine (DCE, CCAP/CCTP, DQE, BPU, métrés, prix
  fournisseurs, plannings, comptes-rendus de réunion, recours) : documents d'entreprise et données
  de marché. **Jamais** vers un palier gratuit.
- `GITHUB_TOKEN` et tout `.env`.
- Les images de terrain (satellite, streetview) si elles contiennent des tiers identifiables.

## Où sont les décisions

- `docs/` (dont `GITHUB_INVENTORY.md`, `DOSSIER-CHANTIER-INDEX.md`, `docs/synthese-talbot-2026/`).
- `projects/watchtower/audit/` : `REFERENCE.md`, `AUDIT-OUTILS-2026.md`, `CAPACITES-AGENT.md`,
  `COUTS-LICENCES-LEGAL.md`, `REFERENCE.md §1` (phases P0→P10).
- `projects/watchtower/AGENTS.md` : les 9 règles (licences, zéro clé par défaut, code de sortie…).
