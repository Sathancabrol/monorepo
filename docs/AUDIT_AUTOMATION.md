# Automated project audit

## Purpose

Maintain one repeatable audit workflow across the project ecosystem so each audit updates shared inventory, KPIs, a gap queue, roadmap actions and history instead of creating an isolated report.

## Workflow

- Portfolio configuration: data/audit/portfolio.json
- Default-branch signals: scripts/project_audit/audit_portfolio.py
- Gap-driven branch discovery and instruction-file discovery: scripts/project_audit/audit_gaps.py
- Cross-project rules and session protocol: docs/CROSS_PROJECT_AUTOMATION_STANDARD.md and AGENTS.md
- Initial rules inventory with source SHAs and explicit gaps: docs/PROJECT_RULES_INVENTORY.md
- Workflow: .github/workflows/project-audit.yml
- Reports: reports/project-audit/latest.json, latest.md, index.html, history.jsonl, branch-index.json, gaps.json, gaps.md
- Trigger: daily at 06:17 UTC, manual dispatch, or relevant audit-code/config changes on main.
- Scope: all paginated branches for configured repositories; new, changed, or unreviewed branch trees are prioritized in bounded batches. Relevant paths include agent instructions, handoffs, policies, standards, decisions, roadmaps, tests and workflows.
- Validation: Python syntax and portfolio JSON are checked before an audit run.
- Rule inventory: finding a rule file is only discovery. Its contents, scope, SHA, conflicts and downstream applicability still require review.
- Safety: read-only inspection of source repositories; generated reports only are committed to this monorepo. No source project code is changed by the audit.

## Gap-driven rule

When an answer depends on an unknown fact, the unknown becomes a follow-up audit item. Search prior audit notes and generated reports, enumerate all repositories and branches, inspect relevant file contents, compare candidate branches, and record evidence before declaring a feature missing. If evidence is still incomplete, leave the exact question and relevant paths in the queue. Do not stop at main or a previously inspected branch.

The gap scanner persists branch names and SHAs. New branches, changed SHAs, failed tree reads and content reviews that remain pending are visible in the queue. Tree inspection discovers relevant files; it does not count as semantic review. Closing a content gap requires a dated finding with repository, branch, path, SHA, confidence, and next action.

## Cross-project work-cycle standard

The shared session cycle is RECALL → DISCOVER → PLAN → EXECUTE → VERIFY → DELIVER → HANDOFF. The canonical policy is docs/CROSS_PROJECT_AUTOMATION_STANDARD.md. Root AGENTS.md requires agents to read the handoff, recover valid memory and prior evidence, search before asking the user, run relevant checks, and update the handoff and append-only journal.

Rule discovery must include AGENTS.md, CLAUDE.md, GEMINI.md, CONTRIBUTING.md, nested instructions, workflows, test/build scripts, security/licence policies, project decisions, roadmaps, and generated deliverable conventions. Every finding must be scoped to its repository, branch, path and SHA. Conflicting rules must be recorded rather than silently resolved.

The user should only be interrupted for genuinely missing information, a consequential product decision, an unavailable permission/credential, or an action that requires approval. Research, repository inspection, branch comparison, routine validation and report preparation should be done autonomously when tools and permissions allow. A scheduled GitHub workflow is not proof of a continuously running agent; actual background execution requires a working runner and verified workflow run.

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
- [x] Expand path discovery to agent instructions, policies, standards, handoffs and decision records.
- [x] Create an initial, source-linked rules inventory for the currently inspected default-branch documents.
- [ ] Audit the contents and scope of discovered rule files across every relevant repository and branch.
- [ ] Read queued file contents and record semantic findings.
- [ ] Resolve the configured repository paths that returned 404 for proto-cognitorium and animation-chronos.
- [ ] Detect rule conflicts and produce a repository-scoped rules registry with source SHA and freshness.
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
- [ ] Automate session-start context recovery and session-end handoff updates in the agent runner.
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

## Verification status after automation-standard update

- Python syntax validation is now part of the workflow definition, but has not yet been executed on this branch.
- The cross-project standard and expanded rule-path discovery have been committed to the feature branch, not merged into main.
- JEV has not been identified in the configured repositories by the code searches run so far; confirm the exact name or location before making claims about that system.
- No semantic all-branch rule audit, full CI run, or local runtime verification is claimed yet.
