# Gap-driven audit protocol

## Rule

When an answer depends on an unknown fact, do not guess and do not stop at the default branch. Turn the unknown into an audit question and search existing evidence first.

## Required sequence

1. State the unknown precisely.
2. Read existing audit memory and reports first: audit/MEMORY.md, audit/state.json, audit/JOURNAL.jsonl, audit/PLAN.md, audit/notes/, docs/AUDIT_AUTOMATION.md, interface registries, manifests, and generated reports when present. Reuse facts only while their source SHA and date remain valid.
3. Enumerate repositories, all paginated branches, relevant pull requests, commits, audit documents, and file paths. Include arena branches, feature branches, audit branches, and branch names referenced by prior audits.
4. Prioritize branches mentioned by prior audits, branches with new or changed SHAs, and branches whose names or paths match the unknown feature.
5. Inspect file contents, not just names. Record repository, branch, path, SHA, date, finding, confidence, impact, dependency, next action, and acceptance test.
6. Compare candidate branches with the default branch and each other before deciding what to preserve or integrate. Do not discard work merely because a branch is old or divergent.
7. Update the shared inventory, KPI snapshot, roadmap, and audit memory. If uncertainty remains, queue the exact missing evidence.
8. Do not label a feature missing while a relevant branch or document remains uninspected.
9. Verify runtime separately. Static presence, build, test execution, passing tests, and human acceptance are distinct states.

## Automated first pass

scripts/project_audit/audit_gaps.py enumerates all configured repositories' branches with pagination, compares SHAs with a persistent index, prioritizes new/changed/unreviewed branches, inspects trees in bounded batches, and writes:

- reports/project-audit/branch-index.json: persistent branch index keyed by repository and branch;
- reports/project-audit/gaps.json: machine-readable evidence queue;
- reports/project-audit/gaps.md: readable queue with evidence paths.

The bounded batch prevents one run from exhausting the API budget. Remaining branches stay queued for later runs. The scanner intentionally does not claim that files have been semantically reviewed or that an app runs.

## KPIs

- Branch inventory coverage: branches indexed / branches returned by GitHub.
- Branch tree audit coverage: current branch SHAs with successfully inspected trees / current branch SHAs.
- Content review coverage: branch SHAs with dated findings backed by file contents / current branch SHAs.
- Unresolved evidence gaps: count of branches with pending or failed review.
- Stale evidence: findings whose source SHA no longer matches the current branch SHA.
- Runtime verification coverage: modules with reproducible run/test records / modules claimed as operational.

Never collapse these into a single misleading completion score.
