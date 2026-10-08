---
provenance: interview-mined
dimension: infrastructure
status: partial
last_updated: 2026-10-08
source: docs/LIFE-HUB.md, HARDWARE-LIFE-HUB.md, app/, projects/
---

# Current State — Infrastructure

## Ce qui existe
- **Monorepo git-first** (Sathancabrol/monorepo) : `app/` FastAPI (port 8123), `docs/` (13 docs de décision), `projects/` (mail-organizer, life-hub, outsider, + dormants).
- **Connecteurs actifs** : Gmail, Google Calendar, Google Drive, Notion, Linear (côté Arena).
- **Vie du code** : branche de travail Arena, commits poussés, docs = source de vérité des décisions.
- **Matériel** : TODO (interview) — machine actuelle, pas encore de serveur maison.

## Ce qui est décidé mais pas encore construit
- Routeur IA L1 (`docs/SYSTEME-COMBINE-IA.md`) — endpoint OpenAI-compatible unique.
- UI mobiGlas L4 (`docs/UI-MOBIGLAS.md`) — PWA à 9 tuiles.
- Serveur maison N150 (`docs/HARDWARE-LIFE-HUB.md`) — achat non effectué.
- USER/ instancié (ce fichier en fait partie) — interview à compléter.

## Lacunes honnêtes
- Aucune sauvegarde hors-site formalisée du monorepo (GitHub = seul exemplaire).
- Pas de serveur 24/7 : tout dépend des sessions.
