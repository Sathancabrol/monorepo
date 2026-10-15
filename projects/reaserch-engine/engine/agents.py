"""Reference agent contracts for Research Engine v0.1.

Agents are deliberately thin orchestration components. A production LLM
adapter should implement these contracts while returning structured data.
"""

from dataclasses import dataclass, fields
from typing import Any, Protocol

from .iteration import DEFAULT_MAX_ROUNDS, DEFAULT_RESULTS_PER_QUERY
from .sufficiency import SufficiencyInput

#: Keys the orchestrator's stopping decision understands.
SUFFICIENCY_KEYS = frozenset(field.name for field in fields(SufficiencyInput))


@dataclass
class AgentContext:
    run_id: str
    question: str
    state: dict[str, Any]


class Agent(Protocol):
    name: str

    def execute(self, context: AgentContext) -> dict[str, Any]: ...


class PlannerAgent:
    name = "planner"

    def execute(self, context: AgentContext) -> dict[str, Any]:
        return {"research_plan": {"question": context.question, "subquestions": []}}


class ResearcherAgent:
    name = "researcher"

    def __init__(self, retriever):
        self.retriever = retriever

    def execute(self, context: AgentContext) -> dict[str, Any]:
        from .retrieval import SearchRequest
        queries = context.state.get("queries", [context.question])
        results = []
        for query in queries:
            results.extend(self.retriever.search(SearchRequest(query=query)))
        return {"search_results": results}


class IterativeResearcherAgent:
    """Researcher that iterates: search → coverage → re-query gaps → enrich.

    Drop-in replacement for :class:`ResearcherAgent` when a retriever can answer
    more than one round (see :mod:`engine.iteration`). It publishes the whole
    iteration report for the dossier and translates the outcome into the keys
    ``SufficiencyInput`` understands, so the orchestrator — not the search loop —
    decides whether another cycle is worth it.
    """

    name = "researcher"

    def __init__(self, retriever, *, strategist=None, max_rounds: int = DEFAULT_MAX_ROUNDS,
                 results_per_query: int = DEFAULT_RESULTS_PER_QUERY,
                 language: str = "fr", max_queries: int | None = None,
                 enrich: bool = True):
        from .query_strategy import QueryStrategist
        from .iteration import IterativeSearch

        self.strategist = strategist or QueryStrategist(language=language)
        self._search = IterativeSearch
        self.retriever = retriever
        self.options = {"max_rounds": max_rounds, "results_per_query": results_per_query,
                        "max_queries": max_queries, "enrich": enrich}

    def execute(self, context: AgentContext) -> dict[str, Any]:
        state = context.state
        question = context.question or state.get("question", "")
        plan = state.get("research_plan") or {}
        subquestions = plan.get("subquestions") if isinstance(plan, dict) else getattr(plan, "subquestions", [])
        source_types = list(state.get("source_types") or [])
        for subquestion in subquestions or []:
            source_types.extend(getattr(subquestion, "source_types", None)
                                or (subquestion.get("source_types") if isinstance(subquestion, dict) else []) or [])
        search = self._search(self.retriever, strategist=self.strategist, **self.options)
        report = search.run(
            question,
            subquestions=subquestions or (),
            source_types=list(dict.fromkeys(source_types)),
            seed_queries=state.get("queries") or (),
        )
        hints = report.sufficiency_hints
        # Only keys the stopping decision understands may reach the orchestrator:
        # an unknown key would make SufficiencyInput(**...) raise mid-run.
        result = {
            "search_results": report.corpus,
            "search_iteration": report.as_dict(),
            "sufficiency": {key: value for key, value in hints.items() if key in SUFFICIENCY_KEYS},
            "critical_gaps": hints["critical_gaps"],
            "unsearched_high_value_categories": hints["unsearched_high_value_categories"],
            "evidence_saturation": hints["evidence_saturation"],
        }
        return result


class EvidenceAnalystAgent:
    name = "evidence_analyst"

    def execute(self, context: AgentContext) -> dict[str, Any]:
        from .run_builder import RunBuilder

        graph = context.state.get("evidence_graph")
        builder = RunBuilder(graph)
        records = []
        for result in context.state.get("search_results", []):
            records.append(builder.add_source_result(result))
        # Claim drafts are optional structured agent output. Keeping them
        # separate from final claims prevents the core from inventing claims.
        for draft in context.state.get("claim_drafts", []):
            if isinstance(draft, dict) and {"id", "text"} <= draft.keys():
                builder.add_claim(
                    draft["id"], draft["text"], draft.get("evidence_ids", ()),
                    draft.get("importance", 1), draft.get("direction", "supports"),
                )
        return {
            "evidence": records,
            "evidence_analysis": {"status": "complete", "records": records},
            "evidence_graph_snapshot": builder.snapshot(),
        }


class ContradictionAnalystAgent:
    name = "contradiction_analyst"

    def execute(self, context: AgentContext) -> dict[str, Any]:
        from .run_builder import RunBuilder

        builder = RunBuilder(context.state.get("evidence_graph"))
        contradictions = context.state.get("contradictions", [])
        for item in contradictions:
            if isinstance(item, dict) and {"id", "claim_ids"} <= item.keys():
                data = {key: value for key, value in item.items() if key not in {"id", "claim_ids"}}
                builder.add_contradiction(item["id"], item["claim_ids"], **data)
        return {"contradictions": contradictions, "evidence_graph_snapshot": builder.snapshot()}


class SynthesizerAgent:
    name = "synthesizer"

    def execute(self, context: AgentContext) -> dict[str, Any]:
        from .run_builder import RunBuilder

        synthesis = {"status": "draft", "based_on": context.state.get("claims", [])}
        builder = RunBuilder(context.state.get("evidence_graph"))
        # A provider may explicitly return a conclusion draft. It is only added
        # when a claim provenance list accompanies it.
        draft = context.state.get("conclusion_draft")
        if isinstance(draft, dict) and {"id", "text"} <= draft.keys():
            builder.add_conclusion(draft["id"], draft["text"], draft.get("claim_ids", ()),
                                   draft.get("contradiction_ids", ()))
            synthesis["conclusion_id"] = draft["id"]
        return {"synthesis": synthesis, "evidence_graph_snapshot": builder.snapshot()}


class VerifierAgent:
    name = "verifier"

    def execute(self, context: AgentContext) -> dict[str, Any]:
        from .graph_assessment import assess_evidence_graph

        graph = context.state.get("evidence_graph")
        assessment = assess_evidence_graph(graph) if graph is not None else {}
        # Merge instead of replacing: a retrieval agent may already have recorded
        # coverage gaps, and the stopping decision needs both views.
        sufficiency = dict(context.state.get("sufficiency") or {})
        sufficiency.update({
            "weak_critical_claims": assessment.get("weak_critical_claims", 0),
            "unresolved_major_contradictions": assessment.get("unresolved_major_contradictions", 0),
        })
        return {
            "verification": {"critical_issues": 0, "graph_assessment": assessment},
            "sufficiency": sufficiency,
        }


class NextActionAgent:
    name = "next_action"

    def execute(self, context: AgentContext) -> dict[str, Any]:
        from .actions import next_best_action
        return {"next_action": next_best_action(context.state)}
