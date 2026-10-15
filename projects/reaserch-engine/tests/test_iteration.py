import json

from engine.federation import FederatedRetriever
from engine.iteration import IterativeSearch, sufficiency_hints
from engine.query_strategy import QueryProposal, QueryStrategist, normalize_query
from engine.retrieval import SearchRequest, SearchResult


def doc(identifier, title, *, source_type="unverified_web", provider="index", metadata=None):
    return SearchResult(identifier, title, f"https://example.org/{identifier}", f"{title} — extrait",
                        source_type, {"provider": provider, **(metadata or {})})


class KeywordProvider:
    """Returns canned documents when a keyword appears in the query."""

    def __init__(self, name, mapping):
        self.name = name
        self.mapping = [(normalize_query(keyword), results) for keyword, results in mapping.items()]
        self.queries: list[str] = []

    def search(self, request):
        self.queries.append(request.query)
        query = normalize_query(request.query)
        out = []
        for keyword, results in self.mapping:
            if keyword and keyword in query:
                for result in results:
                    out.append(SearchResult(result.id, result.title, result.url, result.snippet,
                                            result.source_type, {**result.metadata, "provider": self.name}))
        return out[:request.max_results]

    def diagnostics(self):
        return {"provider": self.name, "returned": 0}


class ScriptedStrategist:
    """Prescribes the queries of round 1, 2, 3… so the loop can be tested alone."""

    def __init__(self, plan):
        self.plan = plan
        self.follow_ups = 0

    def initial_queries(self, question, *, subquestions=(), seed_queries=()):
        return [QueryProposal(query, "scripted round 1", "scripted") for query in self.plan[0]]

    def follow_up(self, *, round_index, **kwargs):
        self.follow_ups += 1
        if round_index < len(self.plan):
            return [QueryProposal(query, f"scripted round {round_index + 1}", "scripted")
                    for query in self.plan[round_index]]
        return []

    def actions_from_state(self, state):  # pragma: no cover - parity with QueryStrategist
        return []


def test_rounds_add_new_material_and_report_their_yield():
    provider = KeywordProvider("index", {
        "trafic": [doc("web:a", "Trafic maritime et qualité de l'air")],
        "definition": [doc("web:b", "Définition des périmètres portuaires")],
        "limites": [doc("doi:10.1/x", "Limites méthodologiques", source_type="primary_study",
                        metadata={"doi": "10.1/x"})],
    })
    search = IterativeSearch(FederatedRetriever({"index": provider}),
                            strategist=ScriptedStrategist([["trafic maritime"],
                                                           ["trafic maritime définition"],
                                                           ["trafic maritime limites"]]),
                            max_rounds=3)

    report = search.run("trafic maritime")

    assert [result.id for result in report.corpus] == ["web:a", "web:b", "doi:10.1/x"]
    assert report.metrics["new_results_per_round"] == [1, 1, 1]
    assert report.metrics["duplicates_merged"] == 2   # 'trafic' legitimately recurs
    assert report.stop_reason == "max_rounds_reached"
    assert len(report.rounds) == 3
    assert report.rounds[1].queries[0].reason == "scripted round 2"


def test_saturation_stops_the_loop_before_the_round_budget():
    provider = KeywordProvider("index", {"trafic": [doc("web:a", "Trafic maritime")]})
    search = IterativeSearch(FederatedRetriever({"index": provider}),
                             strategist=ScriptedStrategist([["trafic"], ["trafic"], ["trafic"]]),
                             max_rounds=3)

    report = search.run("trafic maritime")

    assert report.stop_reason == "evidence_saturation"
    assert len(report.rounds) == 2
    assert report.rounds[-1].results_new == 0
    assert report.sufficiency_hints["evidence_saturation"] is True


def test_the_strategy_can_exhaust_its_queries():
    provider = KeywordProvider("index", {"trafic": [doc("web:a", "Trafic maritime")]})
    search = IterativeSearch(FederatedRetriever({"index": provider}),
                             strategist=ScriptedStrategist([["trafic"]]), max_rounds=4)

    report = search.run("trafic maritime")

    assert report.stop_reason == "queries_exhausted"
    assert len(report.rounds) == 1


def test_query_and_corpus_budgets_are_enforced():
    provider = KeywordProvider("index", {
        "trafic": [doc("web:a", "Trafic maritime")],
        "definition": [doc("web:b", "Définition des périmètres")],
    })
    plan = [["trafic"], ["trafic définition"]]

    by_queries = IterativeSearch(FederatedRetriever({"index": provider}),
                                 strategist=ScriptedStrategist(plan), max_rounds=3, max_queries=1).run("trafic")
    assert by_queries.stop_reason == "query_budget_exhausted"
    assert len(by_queries.rounds) == 1

    by_corpus = IterativeSearch(FederatedRetriever({"index": provider}),
                                strategist=ScriptedStrategist(plan), max_rounds=3,
                                max_results_total=1).run("trafic")
    assert by_corpus.stop_reason == "corpus_budget_exhausted"
    assert len(by_corpus.corpus) == 1


def test_gap_signals_map_onto_the_engine_sufficiency_input():
    provider = KeywordProvider("index", {"trafic": [doc("web:a", "Trafic maritime")]})
    search = IterativeSearch(FederatedRetriever({"index": provider}),
                             strategist=ScriptedStrategist([["trafic"]]), max_rounds=1)

    report = search.run("trafic maritime",
                        subquestions=[{"id": "sq1", "text": "navires émissions inventaires"}],
                        source_types=["systematic_review"])

    assert report.coverage["uncovered_subquestion_ids"] == ["sq1"]
    assert report.coverage["missing_source_types"] == ["systematic_review"]
    hints = report.sufficiency_hints
    assert hints["critical_gaps"] == 1
    assert hints["unsearched_high_value_categories"] == 1
    assert hints["evidence_saturation"] is False

    from engine.sufficiency import SufficiencyInput
    assert SufficiencyInput(**hints).critical_gaps == 1     # keys are accepted as-is
    assert sufficiency_hints(report) == hints


def test_plain_protocol_retrievers_work_without_the_federation_layer():
    provider = KeywordProvider("index", {"trafic": [doc("web:a", "Trafic maritime")]})
    report = IterativeSearch(provider, strategist=ScriptedStrategist([["trafic"], ["trafic"]]),
                             max_rounds=2).run("trafic")

    assert [result.id for result in report.corpus] == ["web:a"]
    assert report.rounds[0].providers == []          # no federation report to forward
    assert report.stop_reason == "evidence_saturation"


def test_enrichment_flag_reaches_the_federation():
    class Enricher:
        name = "fake"

        def __init__(self):
            self.last_enrichment = {}

        def enrich(self, results):
            for item in results:
                item.metadata["enriched_by"] = ["fake"]
                item.metadata["providers"] = sorted(set(list(item.metadata.get("providers") or []) + ["fake"]))
            self.last_enrichment = {"provider": self.name, "enriched": len(results)}
            return results

    provider = KeywordProvider("index", {"trafic": [doc("web:a", "Trafic maritime")]})
    plan = [["trafic"], ["trafic"]]

    with_enrichment = IterativeSearch(FederatedRetriever({"index": provider}, enrichers=[Enricher()]),
                                      strategist=ScriptedStrategist(plan), max_rounds=1).run("trafic")
    assert with_enrichment.corpus[0].metadata["enriched_by"] == ["fake"]
    assert with_enrichment.rounds[0].enrichment == [{"provider": "fake", "enriched": 1}]

    without = IterativeSearch(FederatedRetriever({"index": provider}, enrichers=[Enricher()]),
                              strategist=ScriptedStrategist(plan), max_rounds=1, enrich=False).run("trafic")
    assert "enriched_by" not in without.corpus[0].metadata


def test_report_is_json_safe_and_self_describing():
    provider = KeywordProvider("index", {"trafic": [doc("web:a", "Trafic maritime")]})
    report = IterativeSearch(FederatedRetriever({"index": provider}),
                             strategist=QueryStrategist(language="fr", max_queries_per_round=1),
                             max_rounds=2).run("trafic maritime")

    payload = json.loads(json.dumps(report.as_dict(), ensure_ascii=False))

    assert payload["question"] == "trafic maritime"
    assert payload["rounds"][0]["queries"][0]["reason"]
    assert payload["corpus"][0]["id"] == "web:a"
    assert payload["metrics"]["sources_by_provider"] == {"index": 1}
    assert payload["metrics"]["sources_by_type"] == {"unverified_web": 1}
    assert payload["sufficiency_hints"]["notes"]
    assert isinstance(payload["rounds"][0]["providers"], list)


def test_recency_and_source_hints_are_forwarded_to_providers():
    seen = []

    class Recorder:
        name = "recorder"

        def search(self, request):
            seen.append(request)
            return [doc("web:a", "Trafic")]

        def search_with_report(self, request, *, enrich=True):
            seen.append(request)
            from engine.federation import FederatedSearch
            return FederatedSearch(query=request.query, results=[doc("web:a", "Trafic")])

    IterativeSearch(Recorder(), strategist=ScriptedStrategist([["trafic"]]),
                    max_rounds=1, results_per_query=4, recency_days=30).run("trafic")

    assert seen[0].max_results == 4 and seen[0].recency_days == 30
    assert isinstance(seen[0], SearchRequest)
