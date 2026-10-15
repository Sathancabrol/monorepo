# Search iteration v0.1

A research question is rarely answered by one query. This increment makes the
retrieval layer *iterate*: each round acts on what the previous round revealed,
and the outcome is translated back into the engine's own stopping logic instead
of being decided by the search loop alone.

```text
round 1   question + planned sub-questions
   │      search → merge → enrich
   ▼
coverage  which sub-questions the corpus addresses · which source classes are missing
   │      counter-evidence not sought yet?
   ▼
round 2   queries aimed at the gaps (each carrying its reason)
   │      search → merge → enrich
   ▼
stop      saturation (a round adds nothing new) · max rounds · query/corpus budget · queries exhausted
```

## The loop

`engine/iteration.py` — `IterativeSearch(retriever, strategist=…, max_rounds=3,
results_per_query=10, max_queries=None, max_results_total=None,
min_new_per_round=1, recency_days=None, enrich=True)`.

It accepts any `Retriever`; when the retriever exposes `search_with_report()`
(the federated layer) the per-provider reports and enrichment summaries are
forwarded into the run report, otherwise the loop works with plain results.

Every round is recorded as a `RoundRecord`: queries **with their reason**,
results received, new unique results, corpus size, duplicates merged, per
provider status (ok/error), enrichment summaries.

| Stop reason | Meaning |
|---|---|
| `evidence_saturation` | the round added fewer than `min_new_per_round` new sources |
| `queries_exhausted` | the strategy has no untried query left |
| `max_rounds_reached` | round budget spent |
| `query_budget_exhausted` | `max_queries` distinct queries tried |
| `corpus_budget_exhausted` | `max_results_total` unique sources reached |

## Where the next queries come from

`engine/query_strategy.py` — `QueryStrategist` is deterministic and bilingual
(`fr`/`en`). Families: `define_scope`, `state_of_evidence`, `quantify`,
`official_data`, `dataset`, `counter_evidence`, `field_report`, `uncertainty`.
They are produced from the *observed* state, not from a generic checklist:

1. sub-questions the corpus does not address (`coverage` heuristic below);
2. planned source classes absent from the corpus (mapped to the family most
   likely to produce them, e.g. `institutional_report` → `official_data`);
3. counter-evidence, from round 2 onwards (lifecycle Phase 9);
4. remaining uncertainty, from round 3 onwards;
5. as a last resort, a planned family never attempted.

Queries already tried are suppressed by an accent/case-insensitive key, and each
proposal keeps its reason — the run report reads like a research diary.

**Coverage heuristic (deliberately simple).** A sub-question counts as covered
when ≥ 2 of its content words (stop-words removed) appear in one result's title
or snippet. It is a *planning* signal for choosing the next query. It is never a
claim of completeness, and it never becomes evidence.

**Reusing the strategy engine.** `QueryStrategist.actions_from_state()` exposes
`ResearchStrategyEngine.next_actions()` so an agent can rank *what* to research
next (contradiction > claims > coverage) while this module decides *how* to ask.

## Bridging to the engine's stopping decision

`SearchIterationReport.sufficiency_hints` uses exactly the keys of
`engine.sufficiency.SufficiencyInput`:

```python
{"critical_gaps": n,                      # uncovered sub-questions
 "unsearched_high_value_categories": n,   # planned source classes never seen
 "evidence_saturation": bool,
 "expected_information_gain": float,
 "notes": [...]}
```

`IterativeResearcherAgent` (a drop-in `researcher` for the default pipeline)
publishes the full report as `run.context["search_iteration"]` and writes those
hints into `sufficiency`. The verifier *merges* its own counts into the same
dict, so `Orchestrator` — not the search loop — decides whether to iterate
again. A saturating corpus therefore ends the run through the engine's own
gate (`depth_or_saturation_reached`), with the audit trail to explain why.

```python
from engine.default_pipeline import build_agents
from engine.orchestrator import Orchestrator, ResearchRun

run = ResearchRun("r1", "Quel est l'effet du trafic maritime sur la qualité de l'air à Sète ?")
Orchestrator(build_agents(federated, iterative=True, max_rounds=3)).run(run)
# run.context["search_iteration"], run.context["stopping_decision"]
```

## Command line

```bash
python3 -m engine.cli "ma question"                  # providers from the environment
python3 -m engine.cli "ma question" --rounds 4 --json rapport.json
python3 -m engine.cli "ma question" --language en     # English follow-up queries
python3 -m engine.cli --check                         # probe each provider, exit 1 if none answers
python3 -m engine.cli demo --demo                     # offline fictional corpus
```

`--demo` exercises the whole chain (federation → de-duplication → enrichment →
gap-driven rounds → saturation) with no network and no model. Its corpus is
**fictional** and tagged `demo_fixture`: it demonstrates machinery, never
evidence. An example report is committed as
`docs/examples/recherche-iterative-demo.json`.

Example (fictional corpus, 3 rounds): `apports : [3, 1, 0] (nouveaux par tour)`,
`corpus : 4 sources uniques · 16 doublons fusionnés`,
`arrêt : evidence_saturation`, `critical_gaps=2`.
