# 🗺 CARTE DU MONOREPO — chaque fait a une seule maison

> Fichier panneau-indicateur (pattern MAPS, voir `docs/AGENT-OS-ET-AGENCY-VEILLE.md` §6). Il ne contient aucun fait : seulement où les trouver. Maximum 2 sauts pour atteindre n'importe quel document.

## Zones de travail
- **Mission, cap, offres** → `projects/life-hub/USER/TELOS/MISSION.md` puis `docs/SYNTHESE-GLOBALE-09-10.md` (état des lieux) et `docs/FRONTIGNAN-THAU-AGGLO-STRATEGIE.md` (stratégie locale).
- **Budget & finances** → `projects/life-hub/USER/FINANCES/BUDGET-MENSUEL.md` (réel) ; outil `projects/agent-office` service `budget`.
- **Entreprise d'IA (organisation)** → `docs/AGENT-ENTREPRISE.md` (organigramme 12 services) puis `projects/agent-office/agents/` (fiches par département).
- **Boîte à outils agent-office** → `projects/agent-office/README.md` puis `projects/agent-office/registry.py` + `tools.json`.
- **Mémoire & graphe de connaissances** → `projects/agent-office/agent_office/knowledge.py` + `docs/VPS-AGENT-SQLITE-GRAPH.md`.
- **Veille & benchmarks** → `docs/AGENT-OS-ET-AGENCY-VEILLE.md` (agent OS, GPU, MAPS), `docs/VEILLE-AUGMA-GEO-MARCHES-PUBLICS.md`, `docs/CLES-API-GRATUITES.md`, `docs/ETUDE-MARCHE-BASSIN-DE-THAU.md`.
- **Confrontation de modèles & auto-mise à jour** → `docs/SYSTEMES-CONFRONTATION-MODELES.md` + `docs/AUTO-MAJ-SYSTEME-AGENTIQUE.md`.
- **Internet & marketing & réseaux** → `docs/INTERNET-ET-MARKETING-AGENTIQUE.md` + service `social`.
- **Projets & livrables** → `projects/` (frontignan = deck O2, proto-cognitorium = moteur O1, life-hub, mail-organizer…) ; inventaire détaillé : `projects/life-hub/USER/PROJECTS.md`.
- **Portail & apps** → `app/` (FastAPI + Jinja).
- **Planning & échéances** → `projects/agent-office/data/tasks.json` (via `planning week`).
- **Règles permanentes** → `projects/life-hub/USER/` (README, ABOUTME — contraintes utilisateur : jamais de suppression, français, épargne) + `docs/AGENT-ENTREPRISE.md` §2 (règles d'or).

## Règles de la carte
1. Chaque fait a **une seule maison** — rien n'est écrit deux fois.
2. Ce fichier pointe vers les zones, les zones pointent vers les documents, les documents contiennent les faits.
3. Si un document déménage, mettre à jour cette carte dans le même commit.
