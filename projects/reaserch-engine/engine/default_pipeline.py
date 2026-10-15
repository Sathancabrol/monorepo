"""Build the reference v0.1 pipeline from injectable components."""

from .agents import (
    PlannerAgent, ResearcherAgent, IterativeResearcherAgent, EvidenceAnalystAgent,
    ContradictionAnalystAgent, SynthesizerAgent, VerifierAgent, NextActionAgent,
)
from .agents import AgentContext


def build_agents(retriever, *, iterative: bool = False, max_rounds: int = 3,
                 results_per_query: int = 10, strategist=None, language: str = "fr",
                 max_queries: int | None = None):
    """Assemble the reference pipeline.

    ``iterative=True`` swaps the single-shot researcher for one that re-queries
    the gaps between rounds and enriches the corpus (see ``engine.iteration``).
    """
    if iterative:
        researcher = IterativeResearcherAgent(
            retriever, strategist=strategist, max_rounds=max_rounds,
            results_per_query=results_per_query, language=language, max_queries=max_queries,
        )
    else:
        researcher = ResearcherAgent(retriever)
    instances = [
        PlannerAgent(),
        researcher,
        EvidenceAnalystAgent(),
        ContradictionAnalystAgent(),
        SynthesizerAgent(),
        VerifierAgent(),
        NextActionAgent(),
    ]
    def invoke(execute):
        def wrapped(state):
            return execute(AgentContext(
                run_id=state.get("run_id", "unknown"),
                question=state.get("question", ""),
                state=state,
            ))
        return wrapped

    return {agent.name: invoke(agent.execute) for agent in instances}
