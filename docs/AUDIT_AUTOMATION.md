# Automated project audit

## Purpose

Maintain one repeatable audit workflow across the project ecosystem so each audit updates shared inventory, KPIs, a gap queue, roadmap actions and history instead of creating an isolated report.

## Workflow

- Portfolio configuration: data/audit/portfolio.json
- Default-branch signals: scripts/project_audit/audit_portfolio.py
- Gap-driven branch discovery: scripts/project_audit/audit_gaps.py
- Workflow: .github/workflows/project-audit.yml
- Reports: reports/project-audit/latest.json, latest.md, index.html, history.jsonl, branch-index.json, gaps.json, gaps.md
- Trigger: daily at 06:17 UTC, manual dispatch, or relevant audit-code/config changes on main.
- Scope: all paginated branches for configured repositories; new, changed, or unreviewed branch trees are prioritized in bounded batches.
- Safety: read-only inspection of source repositories; generated reports only are committed to this monorepo. No source project code is changed by the audit.

## Gap-driven rule

When an answer depends on an unknown fact, the unknown becomes a follow-up audit item. Search prior audit notes and generated reports, enumerate all repositories and branches, inspect relevant file contents, compare candidate branches, and record evidence before declaring a feature missing. If evidence is still incomplete, leave the exact question and relevant paths in the queue. Do not stop at main or a previously inspected branch.

The gap scanner persists branch names and SHAs. New branches, changed SHAs, failed tree reads and content reviews that remain pending are visible in the queue. Tree inspection discovers relevant files; it does not count as semantic review. Closing a content gap requires a dated finding with repository, branch, path, SHA, confidence, and next action.

## KPI definitions

| KPI | Formula | What it means | What it does not mean |
|---|---|---|---|
| Repository audit coverage | Repositories with readable metadata / configured repositories | Portfolio metadata coverage | Functional completeness |
| Branch inventory coverage | Current branches indexed / branches returned by GitHub | Branch discovery coverage | File-content review |
| Branch tree coverage | Current branch SHAs with successful tree reads / current branch SHAs | Tree-inspection coverage | Code correctness |
| Content review coverage | Current branch SHAs with dated file-level findings / current branch SHAs | Evidence review coverage | Runtime health |
| Documentation signal coverage | Repos with docs or Markdown / repos with readable trees | Documentation exists | Documentation is correct |
| Test signal coverage | Repos with test-like files / repos with readable trees | Test files may exist | Tests pass |
| CI signal coverage | Repos with workflow files / repos with readable trees | Workflow files exist | CI is green |
| Unresolved evidence gaps | Branches with pending/error review | Remaining audit work | Repository is broken |
| Runtime verification | Reproducible tests/builds/runs recorded against a SHA | Verified execution evidence | General product readiness |

Never combine these into a single misleading completion percentage. Targets are governance goals, not current quality scores.

## Automatic next actions

- stale activity;
- missing documentation/test/CI signals;
- large branch inventory;
- missing or changed branches;
- tree-read errors or truncated trees;
- unresolved content reviews;
- stale evidence whose source SHA has changed.

These are review prompts, not automatic deletion, merges, or code changes.

## Current phases

### Phase 1 — Portfolio inventory and KPI snapshot
- [x] Configure the repository portfolio and focus branches.
- [x] Generate JSON, Markdown and HTML dashboard.
- [x] Record KPI history.
- [x] Schedule daily/manual audit.
- [ ] Verify workflow execution on GitHub Actions.

### Phase 2 — Branch and module reconciliation
- [x] Enumerate branches with pagination and persist branch SHAs.
- [x] Queue new, changed and previously uninspected branch trees.
- [x] Inspect branch trees in bounded batches and preserve relevant evidence paths.
- [ ] Read queued file contents and record semantic findings.
- [ ] Compare each relevant branch against its default branch and other candidate branches.
- [ ] Identify duplicate modules using manifest/path signatures and hashes where practical.
- [ ] Track divergence and create stable roadmap items with evidence links.

### Phase 3 — Evidence-backed functional audit
- [ ] Run repository-native tests/builds in isolated CI jobs.
- [ ] Record exact command, commit SHA, environment, exit code, duration and artifacts.
- [ ] Separate static presence, test execution, passing tests, build/preview, and human acceptance.
- Never infer "working" from README text alone.

### Phase 4 — Shared roadmap and dashboard
- [ ] Use stable requirement IDs across Watchtower, Atlas, BTP, Cognitorium, Nexus and monorepo.
- [ ] Link requirements to repository, path, branch/SHA, issue/PR, dependencies, priority, KPI, evidence and acceptance test.
- [ ] Calculate progress from verified acceptance criteria.
- [ ] Detect regressions, stale evidence and blockers.
- [ ] Expose the dashboard in the existing monorepo interface.

### Phase 5 — Continuity agent and research
- [x] Document continuity-agent architecture and guardrails in docs/AGENT_CONTINUITY.md.
- [ ] Audit Nexus OS, Research Engine and HCSM code/tests before reusing components.
- [ ] Implement a persistent task queue with stable IDs, dependencies, resumable state and append-only journal.
- [ ] Connect issues, PRs, commits and CI results to working memory.
- [ ] Add background research with deduplication, provenance, freshness and quotas.
- [ ] Add an isolated runner for tests and branch-based changes.
- [ ] Add agent-control UI and quality KPIs.
- [ ] Keep merges, deletion, deployment and costly actions behind human approval.

## Operational notes

- Public GitHub API access is rate-limited; use a least-privilege GH_AUDIT_TOKEN secret when required.
- The gap scanner paginates branch listing and caps tree inspections per run (default 15); unprocessed branches remain queued.
- GitHub Actions schedules may start later than the requested minute.
- Reports are committed to main; report paths must not trigger an infinite workflow loop.
- Workflow execution and local runtime have not yet been verified by this document.
