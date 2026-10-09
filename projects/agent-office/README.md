# 🏢 agent-office — la boîte à outils de l'entreprise d'IA

> **Objectif** : que l'agent (Laplace) effectue un maximum de bureautique — mail, budget, marketing, recherche, prospection, planning, facturation — avec des outils **zéro dépendance** (stdlib Python 3.9+), testés, invocables en CLI et découvrables via un registre.
> Convention héritée de `projects/mail-organizer` : rien à installer, jamais de suppression de données, sorties dans `out/` (ignoré par Git).

## 🚀 Démarrage

```bash
cd projects/agent-office
python3 -m agent_office registry list     # que sait faire l'entreprise ?
python3 -m agent_office registry doctor   # auto-test de tous les services
python3 -m agent_office budget report     # budget réel (seedé depuis USER/FINANCES)
```

## 🧰 Les services

| Service | Commande | Fait quoi |
|---|---|---|
| 💰 **budget** | `budget report` / `budget add ...` | suivi mensuel, totaux LOCK/MOVE, alerte déficit |
| 🧾 **invoices** | `invoices devis/facture ...` | devis & factures conformes (mention franchise TVA art. 293 B CGI), HTML + texte |
| 📣 **marketing** | `marketing onepager/sequence/post --offer O1` | one-pager HTML, séquence de prospection 3 touches, posts — sur les offres O1/O2/O3 réelles |
| 🎯 **prospects** | `prospects list/next/add/move` | mini-CRM pipeline (cible→gagné), relances dues |
| 🔎 **research** | `research brief/cite/watch` | briefs de recherche, registre de citations, veille — s'articule avec `reaserch-engine` |
| 📬 **mail** | `mail digest [--demo]` | digest IMAP lecture seule des non-lus groupés par expéditeur (jamais de suppression) |
| 📅 **planning** | `planning week/add/ics` | agenda hebdo + export `.ics` importable dans Google Calendar |
| ⚔️ **arena** | `arena battle/page/vote/elo/judge` | confrontation de modèles : duels en aveugle + ELO + grille ChatEval (voir `docs/SYSTEMES-CONFRONTATION-MODELES.md`) |
| 🔄 **update** | `update journal/lessons/changelog/check` | auto-mise à jour du système : journal des évolutions, leçons (Reflexion), changelog auto, garde-fou (voir `docs/AUTO-MAJ-SYSTEME-AGENTIQUE.md`) |
| 🗂 **registry** | `registry list/build/doctor` | registre des capacités (`tools.json`) + auto-tests |

Tous : `python3 -m agent_office <service> --help`.

## 📁 Structure

```
agent_office/     ← les modules (un par service)
data/             ← budget_transactions.csv (réel), prospects.json, tasks.json, citations.json
tools.json        ← registre généré (registry build)
tests/            ← unittest
out/              ← productions générées (ignoré Git)
```

## 🏗 Lien avec le reste

- Architecture « entreprise d'IA » : `docs/AGENT-ENTREPRISE.md` (s'appuie sur les audits `SYSTEME-COMBINE-IA.md`, `BENCHMARK-HARNESS-2026.md`, `AUDIT-ACTIFS-COMPLET.md`).
- Les offres O1/O2/O3 vendues par le marketing sont celles de `USER/TELOS/MISSION.md`.
- Le budget seedé = les vrais chiffres de `USER/FINANCES/BUDGET-MENSUEL.md`.
