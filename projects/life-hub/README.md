# 🏠 LIFE-HUB — adoption LifeOS (Phase 1)

> **Décision actée le 2026-10-08** : LifeOS est adopté comme socle du Life Hub (voir `docs/LIFE-HUB.md`, renforcé par `docs/BENCHMARK-HARNESS-2026.md` — aucun challenger ne couvre budget+planning+mails+mémoire+dashboard).
> **Upstream** : [danielmiessler/LifeOS](https://github.com/danielmiessler/LifeOS) (MIT) · commit figé **`5e2f2e8c`** (2026-09-03) · version `7.40.4`
> Attribution : voir [`NOTICE`](NOTICE).

## ⚠️ Constat d'audit au moment de l'adoption
Le repo upstream a **évolué depuis l'audit initial** (`docs/LIFE-HUB.md` §7) : LifeOS est désormais un **harnais d'installation** — `install/` contient les templates (USER, LIFEOS, agents, commands, ~60 hooks, dizaines de skills), et PULSE/TOOLS vivent dans l'arborescence `install/LIFEOS/` (PULSE = 7,9 Mo, TOOLS = 2,9 Mo, ~770 fichiers). L'adoption est donc **sélective et traçable**, pas un vendage complet.

## 📦 Ce qui est adopté maintenant (950 Ko, 142 fichiers)
| Dossier | Origine upstream | Rôle |
|---|---|---|
| `template/USER/` | `install/USER/` | **Le coffre de données personnel** — format complet : ABOUTME, BASICINFO, CONTACTS, **FINANCES/** (schémas yaml inclus), **TELOS/** (CURRENT_STATE ↔ IDEAL_STATE : santé, argent, relations, rythmes, création, liberté, infrastructure), DIGITAL_ASSISTANT (mémoire IA), CONFIG |
| `core/ALGORITHM/` | `install/LIFEOS/ALGORITHM/` | La boucle « état actuel → état idéal » (v8.20.2, guides d'éval) |
| `core/ATLAS/` | `install/LIFEOS/ATLAS/` | Inventaire de ce qu'on possède (actifs, comptes, matériel) — rejoindra `docs/HARDWARE-LIFE-HUB.md` |
| `core/RULES/` | `install/LIFEOS/RULES/` | Règles de fonctionnement du système |
| `core/LIFEOS_SYSTEM_PROMPT.md` | idem | Le prompt-maître du harnais |
| `WORKFLOW/` | `Workflows/` | Interview (remplir USER/), Setup, Update, Uninstall |

## 🚫 Ce qui n'est PAS copié (et pourquoi)
| Partie | Taille | Verdict |
|---|---|---|
| `install/LIFEOS/PULSE/` (dashboard Next.js) | 7,9 Mo | Phase 2 — en concurrence avec notre propre UI [`UI-MOBIGLAS.md`](../../docs/UI-MOBIGLAS.md) : on évaluera PULSE vs construction mince dans `app/` avant d'embarquer 8 Mo |
| `install/LIFEOS/TOOLS/` (gmail.ts, DASchedule…) | 2,9 Mo | Phase 2 — à piocher à l'unité (gmail, planning) quand les ponts monorepo seront posés |
| `install/hooks/` (~60 hooks) + `install/skills/` (dizaines) | ~17 Mo | Cherry-pick plus tard ; candidats déjà repérés : SystemsThinking, RootCauseAnalysis, Telos, Vitals, ThreatModel |
| `install/LIFEOS/DOCUMENTATION/` | 1,4 Mo | Consultable en ligne : [docs.ourlifeos.ai](https://docs.ourlifeos.ai) |

## 🗺️ Phases (rappel, détail dans `docs/LIFE-HUB.md` §5)
- **Phase 1 ✅ (ce commit)** : adoption sélective + NOTICE + traçabilité upstream.
- **Phase 2** : instancier `USER/` réel via le workflow **Interview** (données perso réelles — à faire en séance), adapter au contexte FR/Linux, premiers ponts (mail-organizer, connecteurs Google).
- **Phase 3** : arbitrage dashboard (PULSE vs UI mobiGlas maison) + router L1 de `docs/SYSTEME-COMBINE-IA.md`.
- **Phase 4+** : skills cherry-pickées, Cortex/mémoire, revue hebdo auto.

## 🔒 Règle de licence
MIT → copie autorisée **avec attribution** (NOTICE conservé à chaque mise à jour upstream). Les fichiers copiés restent sous licence MIT de leurs auteurs ; nos adaptations maison sont clairement séparées (rien n'est modifié dans `template/` et `core/` — l'adaptation vivra dans `USER/` instancié et dans `app/`).
