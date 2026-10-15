from engine.agents import AgentContext, IterativeResearcherAgent
from engine.default_pipeline import build_agents
from engine.federation import FederatedRetriever
from engine.orchestrator import Orchestrator, ResearchRun
from engine.query_strategy import normalize_query
from engine.retrieval import SearchResult


def doc(identifier, title, *, source_type="unverified_web"):
    return SearchResult(identifier, title, f"https://example.org/{identifier}", f"{title} — extrait",
                        source_type, {"provider": "index"})


class KeywordProvider:
    def __init__(self, mapping):
        self.name = "index"
        self.mapping = [(normalize_query(key), items) for key, items in mapping.items()]

    def search(self, request):
        query = normalize_query(request.query)
        out = []
        for keyword, items in self.mapping:
            if keyword and keyword in query:
                for item in items:
                    out.append(SearchResult(item.id, item.title, item.url, item.snippet,
                                            item.source_type, {**item.metadata, "provider": self.name}))
        return out[:request.max_results]

    def diagnostics(self):
        return {"provider": self.name, "returned": 0}


def build_retriever(*, extra_documents: bool = False):
    mapping = {"trafic": [doc("web:a", "Trafic maritime et qualité de l'air")]}
    if extra_documents:
        mapping["definition"] = [doc("web:b", "Définition des périmètres portuaires")]
    return FederatedRetriever({"index": KeywordProvider(mapping)})


def test_iterative_researcher_publishes_the_report_and_keeps_the_verifier_signals():
    """A saturating corpus must stop the run *through* the engine's own gates."""
    run = ResearchRun("run-iter", "trafic maritime")
    run.context["queries"] = ["trafic maritime"]

    completed = Orchestrator(build_agents(build_retriever(), iterative=True, max_rounds=2),
                             max_iterations=3).run(run)

    iteration = completed.context["search_iteration"]
    assert len(iteration["rounds"]) == 2 and iteration["stop_reason"] == "evidence_saturation"
    assert iteration["metrics"]["corpus_size"] == 1

    sufficiency = completed.context["sufficiency"]
    assert {"critical_gaps", "evidence_saturation"} <= set(sufficiency)          # from the search loop
    assert {"weak_critical_claims", "unresolved_major_contradictions"} <= set(sufficiency)  # verifier merged in
    assert sufficiency["evidence_saturation"] is True

    sources = {node["id"] for node in completed.context["evidence_graph_snapshot"]["nodes"]
               if node["kind"] == "source"}
    assert "web:a" in sources                                # the enriched corpus reached the graph
    assert completed.context["stopping_decision"]["decision"] == "stop"
    assert completed.context["stopping_decision"]["reason"] == "depth_or_saturation_reached"


def test_the_flag_off_keeps_the_single_shot_researcher():
    run = ResearchRun("run-plain", "trafic maritime")
    run.context["queries"] = ["trafic maritime"]

    completed = Orchestrator(build_agents(build_retriever(extra_documents=True)),
                             max_iterations=1).run(run)

    assert "search_iteration" not in completed.context
    assert completed.context["search_results"]


def test_agent_uses_the_planner_subquestions_and_reports_gaps():
    agent = IterativeResearcherAgent(build_retriever(), max_rounds=1)
    context = AgentContext(run_id="r", question="trafic maritime", state={
        "research_plan": {"subquestions": [
            {"id": "sq1", "text": "trafic maritime", "source_types": ["primary_study"]},
            {"id": "sq2", "text": "inventaires portuaires officiels"},
        ]},
    })

    result = agent.execute(context)

    assert result["search_results"]
    assert isinstance(result["critical_gaps"], int) and result["critical_gaps"] >= 1
    assert result["unsearched_high_value_categories"] >= 1        # primary_study never appeared
    assert result["sufficiency"]["evidence_saturation"] in (True, False)
    queries = [query["query"] for round_ in result["search_iteration"]["rounds"] for query in round_["queries"]]
    assert any("inventaires portuaires officiels" in query for query in queries)


def test_a_corpus_that_saturates_tells_the_engine_to_stop():
    """When three rounds add nothing, the loop says so and the engine stops."""
    class ExhaustedRetriever:
        name = "exhausted"

        def search(self, request):
            return []

        def search_with_report(self, request, *, enrich=True):
            from engine.federation import FederatedSearch
            return FederatedSearch(query=request.query, results=[], providers=[])

    run = ResearchRun("run-empty", "question sans aucune source")
    completed = Orchestrator(build_agents(ExhaustedRetriever(), iterative=True, max_rounds=2),
                             max_iterations=3).run(run)

    assert completed.context["sufficiency"]["evidence_saturation"] is True
    assert completed.context["stopping_decision"]["decision"] == "stop"
    assert completed.context["stopping_decision"]["reason"] == "depth_or_saturation_reached"


def test_only_known_sufficiency_keys_are_published():
    """The orchestrator builds SufficiencyInput(**context['sufficiency']):
    an unknown key would crash a run, so the agent filters them."""
    from engine.agents import SUFFICIENCY_KEYS

    agent = IterativeResearcherAgent(build_retriever(), max_rounds=1)
    context = AgentContext(run_id="r", question="trafic maritime", state={})
    result = agent.execute(context)

    assert set(result["sufficiency"]) <= SUFFICIENCY_KEYS
    from engine.sufficiency import SufficiencyInput
    assert SufficiencyInput(**result["sufficiency"]) is not None
    assert {"critical_gaps", "evidence_saturation"} <= set(result["sufficiency"])
