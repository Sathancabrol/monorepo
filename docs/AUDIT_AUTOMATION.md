# Automated project audit

## Purpose

Maintain one repeatable audit workflow across the project ecosystem so that a new audit updates a shared inventory, KPI snapshot, action list and historical series rather than creating an isolated report.

## Current first iteration

- Portfolio configuration: `data/audit/portfolio.json`
- Collector and deterministic rules: `scripts/project_audit/audit_portfolio.py`
- Scheduled workflow: `.github/workflows/project-audit.yml`
- Generated outputs: `reports/project-audit/latest.json`, `latest.md`, `index.html`, `history.jsonl`
- Trigger: daily at 06:17 UTC, manual dispatch, or relevant changes to audit configuration/code on `main`.
- Scope: GitHub metadata, default branch file tree, selected branch existence/tree, documentation/test/CI/source signals, last repository push, and deterministic next-action suggestions.
- Safety: read-only inspection of project repositories; only generated reports are committed to this monorepo. No application code is modified by the audit.

## KPI definitions

| KPI | Formula | What it means | What it does not mean |
|---|---|---|---|
| Audit coverage | Successfully read repository metadata / configured repositories | Portfolio inventory coverage | Functional completeness |
| Documentation signal coverage | Audited repos with docs/ or Markdown files / repos with readable default tree | Documentation exists | Documentation is correct or current |
| Test signal coverage | Audited repos with test-like files / repos with readable default tree | Test files may exist | Tests pass or cover important paths |
| CI signal coverage | Audited repos with GitHub Actions workflow files / repos with readable default tree | CI workflow files exist | CI is enabled or green |
| Source signal | Count of repos with source-like files | Code is present | The app builds or runs |
| Audit errors | Count of repos with metadata/tree/branch errors | Data gaps to resolve | Repository is broken |
| Runtime verification | Always false in this initial implementation | Runtime testing is still outstanding | No runtime verification is claimed |

The initial targets in the portfolio file are governance targets, not current scores. A 100% file-signal KPI must never be interpreted as 100% product readiness.

## Auto-generated next actions

Rules currently create reminders for:
- stale last push (30+ days);
- missing documentation signal;
- missing test-file signal;
- missing CI workflow signal;
- 10+ branches;
- inaccessible metadata, branch listing or tree.

These are prompts for review, not automatic deletion, merges or code changes.

## Planned evolution

### Phase 1 — Portfolio inventory and KPI snapshot
- [x] Configure portfolio repositories and focus branches.
- [x] Generate JSON, Markdown and HTML dashboard.
- [x] Record KPI history.
- [x] Schedule daily/manual audit.
- [ ] Verify workflow execution on GitHub Actions.

### Phase 2 — Branch and module reconciliation
- Compare each configured branch to its default branch.
- Identify duplicate modules using manifest/path signatures and file hashes where practical.
- Track branch age, divergence, uncommitted work (where a local runner is available), and merge/archive recommendations.
- Create roadmap items with stable IDs and evidence links.

### Phase 3 — Evidence-backed functional audit
- Run repository-native test commands in isolated CI jobs.
- Record exact command, commit SHA, environment, exit code, duration and artifact links.
- Distinguish static presence, tests executed, tests passed, preview/build passed, and human-validated acceptance.
- Never infer "working" from README text alone.

### Phase 4 — Shared roadmap and dashboard
- Use stable requirement IDs across Watchtower, Atlas, BTP, Cognitorium, Nexus and the monorepo.
- Link each roadmap item to repository, path, issue/PR, dependencies, priority, KPI, evidence and acceptance test.
- Calculate progress from verified acceptance criteria, not optimistic labels.
- Detect regressions and stale evidence, and highlight blocked work.
- Expose the dashboard in the monorepo's existing interface skeleton.

### Phase 5 — Agent de continuité et recherche de fond
- [x] Documenter l'architecture cible et les garde-fous dans `docs/AGENT_CONTINUITY.md`.
- [ ] Auditer Nexus OS, Research Engine et HCSM au niveau code/tests avant de réutiliser leurs composants.
- [ ] Implémenter une file persistante de tâches avec IDs stables, dépendances, état de reprise et journal append-only.
- [ ] Connecter les issues, PR, commits et résultats CI à la mémoire de travail.
- [ ] Ajouter la recherche de fond liée aux besoins, avec déduplication, provenance, fraîcheur et quotas.
- [ ] Ajouter un runner isolé pour tests et modifications sur branche dédiée.
- [ ] Ajouter l'interface de pilotage et les KPI de qualité de l'agent.
- [ ] Garder fusion, suppression, déploiement et actions coûteuses sous approbation humaine.

## Operational notes

- Public repositories can be inspected using the unauthenticated GitHub API, but rate limits apply.
- For private repositories, configure a least-privilege repository-scoped secret named `GH_AUDIT_TOKEN`; never commit a token to the portfolio config or reports.
- The first version caps branch enumeration at 100 per repository.
- GitHub Actions schedules may start later than the requested minute.
- Audit reports are committed to `main`; the workflow ignores report paths as push triggers, preventing an infinite run loop.
- Review the workflow permissions and organization policies before enabling it in a production repository.
