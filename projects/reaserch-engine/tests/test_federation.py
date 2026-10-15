from engine.federation import FederatedRetriever
from engine.retrieval import SearchRequest, SearchResult


def result(identifier, *, provider=None, snippet="extrait", url=None, **metadata):
    data = dict(metadata)
    if provider:
        data["provider"] = provider
    return SearchResult(identifier, f"Titre {identifier}", url or f"https://example.org/{identifier}",
                        snippet, "unverified_web", data)


class RecordingRetriever:
    def __init__(self, name, results=(), error=None):
        self.name = name
        self.results = list(results)
        self.error = error
        self.requests = []

    def search(self, request):
        self.requests.append(request)
        if self.error:
            raise self.error
        return self.results[:request.max_results]

    def diagnostics(self):
        return {"provider": self.name, "returned": len(self.results)}


def test_a_dead_provider_does_not_kill_the_round():
    alive = RecordingRetriever("alive", [result("a", provider="alive")])
    dead = RecordingRetriever("dead", error=RuntimeError("connection refused"))
    federated = FederatedRetriever({"alive": alive, "dead": dead})

    search = federated.search_with_report(SearchRequest("q"))

    assert [item.id for item in search.results] == ["a"]
    assert search.failed_providers == ["dead"]
    report = {entry.name: entry for entry in search.providers}
    assert report["alive"].ok and report["alive"].returned == 1
    assert report["dead"].error.startswith("RuntimeError: connection refused")
    assert len(report) == 2


def test_duplicates_across_providers_are_merged_once_with_full_provenance():
    shared_title = "Rapport annuel de surveillance"
    first = SearchResult("web:https://example.org/r", shared_title, "https://example.org/r",
                         "court", "unverified_web", {"provider": "searxng", "rank": 1})
    mirror = SearchResult("web:https://example.net/r", shared_title,
                          "https://example.net/r?utm_source=nl", "un extrait plus riche",
                          "unverified_web", {"provider": "mirror", "rank": 1})
    federated = FederatedRetriever({
        "searxng": RecordingRetriever("searxng", [first]),
        "mirror": RecordingRetriever("mirror", [mirror]),
    })

    search = federated.search_with_report(SearchRequest("q"))

    # The two providers point at different hosts but carry the same normalized
    # title, so the corpus keeps one record listing both providers.
    assert len(search.results) == 1
    assert search.corpus_size == 1
    assert search.results[0].metadata["providers"] == ["mirror", "searxng"]
    assert federated.search(SearchRequest("q")) is not None
    assert federated.last_report.corpus_size == 1


def test_interleaving_is_deterministic_and_weightable():
    a = RecordingRetriever("alpha", [result("a1", provider="alpha"), result("a2", provider="alpha")])
    b = RecordingRetriever("beta", [result("b1", provider="beta"), result("b2", provider="beta")])

    plain = FederatedRetriever({"alpha": a, "beta": b})
    assert [item.id for item in plain.search(SearchRequest("q"))] == ["a1", "b1", "a2", "b2"]

    weighted = FederatedRetriever({"alpha": a, "beta": b}, weights={"beta": 5.0})
    assert [item.id for item in weighted.search(SearchRequest("q"))] == ["b1", "a1", "b2", "a2"]


def test_per_provider_caps_and_final_truncation():
    provider = RecordingRetriever("alpha", [result(f"r{index}", provider="alpha") for index in range(5)])
    federated = FederatedRetriever({"alpha": provider}, per_provider_max=3)

    search = federated.search_with_report(SearchRequest("q", max_results=2))

    assert provider.requests[0].max_results == 3     # asked for more than returned…
    assert len(search.results) == 2                  # …then the caller's limit applies
    assert search.corpus_size == 3                   # the merged corpus keeps the extra material


def test_enrichers_run_over_the_merged_corpus_and_report_themselves():
    class Enricher:
        name = "fake-enricher"

        def __init__(self):
            self.last_enrichment = {}

        def enrich(self, results):
            for item in results:
                item.metadata["enriched_by"] = ["fake-enricher"]
            self.last_enrichment = {"provider": self.name, "enriched": len(results)}
            return results

    class Broken:
        name = "broken"

        def enrich(self, results):
            raise RuntimeError("enrichment exploded")

    federated = FederatedRetriever(
        {"alpha": RecordingRetriever("alpha", [result("a1", provider="alpha")])},
        enrichers=[Enricher(), Broken()])

    search = federated.search_with_report(SearchRequest("q"))

    assert search.results[0].metadata["enriched_by"] == ["fake-enricher"]
    assert search.enrichment[0] == {"provider": "fake-enricher", "enriched": 1}
    assert search.enrichment[1]["provider"] == "broken"
    assert "enrichment exploded" in search.enrichment[1]["error"]


def test_enrichment_can_be_disabled_per_search():
    class Enricher:
        name = "fake-enricher"
        last_enrichment: dict = {}

        def enrich(self, results):
            raise AssertionError("enricher must not run")

    federated = FederatedRetriever(
        {"alpha": RecordingRetriever("alpha", [result("a1", provider="alpha")])},
        enrichers=[Enricher()])

    search = federated.search_with_report(SearchRequest("q"), enrich=False)

    assert [item.id for item in search.results] == ["a1"]
    assert search.enrichment == []


def test_accepts_retrieval_provider_objects_too():
    from engine.providers import RetrievalProvider

    provider = RetrievalProvider(name="wrapped", retriever=RecordingRetriever("wrapped", [result("w", provider="wrapped")]))
    federated = FederatedRetriever([provider])
    assert federated.provider_names() == ["wrapped"]
    assert [item.id for item in federated.search(SearchRequest("q"))] == ["w"]
