from datetime import date, datetime, timezone
from urllib.parse import unquote

import pytest

from engine.retrieval import RetrievalError, SearchRequest, SearchResult
from engine.web_retrieval import (
    Crawl4AiRetriever, OpenAlexRetriever, SearxngRetriever, extract_markdown,
    reconstruct_abstract, time_range_for,
)


# ── SearXNG ──────────────────────────────────────────────────────────────────
def test_searxng_maps_results_and_reports_diagnostics():
    observed = []

    def fake_get(url):
        observed.append(url)
        return {
            "results": [
                {"url": "https://example.org/a?utm_source=x", "title": "A", "content": "Extrait A",
                 "engines": ["duckduckgo"], "score": 1.5, "category": "general"},
                {"title": "sans url"},
                "not-a-dict",
            ],
            "unresponsive_engines": [["google", "too many requests"], "qwant"],
            "answers": [],
            "suggestions": ["autre requête"],
        }

    retriever = SearxngRetriever(http_get=fake_get, language="fr")
    results = retriever.search(SearchRequest("trafic maritime Sète", max_results=5))

    assert "format=json" in observed[0] and "language=fr" in observed[0]
    assert [result.id for result in results] == ["web:https://example.org/a"]
    assert results[0].url == "https://example.org/a"
    assert results[0].source_type == "unverified_web"
    assert results[0].metadata["engines"] == ["duckduckgo"]
    diagnostics = retriever.diagnostics()
    assert diagnostics["skipped"] == 2
    assert diagnostics["unresponsive_engines"] == [
        {"engine": "google", "reason": "too many requests"}, {"engine": "qwant", "reason": ""}]


def test_searxng_sends_time_range_and_respects_max_results():
    observed = []

    def fake_get(url):
        observed.append(url)
        return {"results": [{"url": f"https://example.org/{index}", "title": str(index)}
                            for index in range(5)]}

    retriever = SearxngRetriever(http_get=fake_get)
    results = retriever.search(SearchRequest("q", max_results=2, recency_days=3))

    assert "time_range=week" in observed[0]
    assert len(results) == 2
    assert time_range_for(1) == "day" and time_range_for(400) is None


def test_searxng_refuses_to_confuse_a_broken_payload_with_an_empty_result():
    with pytest.raises(RetrievalError, match="format=json"):
        SearxngRetriever(http_get=lambda url: {"number_of_results": 0}).search(SearchRequest("q"))
    with pytest.raises(RetrievalError):
        SearxngRetriever(http_get=lambda url: ["nope"]).search(SearchRequest("q"))


# ── OpenAlex ─────────────────────────────────────────────────────────────────
OPENALEX_ITEM = {
    "id": "https://openalex.org/W123",
    "doi": "https://doi.org/10.1000/ABC",
    "title": "Shipping emissions in ports",
    "type": "article",
    "publication_year": 2024,
    "publication_date": "2024-05-02",
    "cited_by_count": 12,
    "is_oa": True,
    "language": "en",
    "type_crossref": "journal-article",
    "primary_location": {"source": {"display_name": "Journal of Ports", "type": "journal"}},
    "best_oa_location": {"pdf_url": "https://example.org/paper.pdf"},
    "authorships": [{"author": {"display_name": "Ada Demo"}}],
    "abstract_inverted_index": {"Port": [0], "emissions": [1], "matter.": [3]},
}


def test_openalex_maps_a_work_without_network():
    observed = []

    def fake_get(url):
        observed.append(url)
        return {"results": [OPENALEX_ITEM, {"title": "sans identifiant"}]}

    retriever = OpenAlexRetriever(mailto="research@example.test", http_get=fake_get,
                                 today=lambda: date(2026, 10, 15))
    results = retriever.search(SearchRequest("shipping emissions", max_results=10, recency_days=30))

    assert "mailto=research%40example.test" in observed[0]
    assert "from_publication_date%3A2026-09-15" in observed[0]
    assert len(results) == 1
    result = results[0]
    assert result.id == "doi:10.1000/abc"
    assert result.source_type == "primary_study"
    assert result.snippet == "Port emissions matter."
    assert result.metadata["doi"] == "10.1000/abc"
    assert result.metadata["authors"] == ["Ada Demo"]
    assert result.metadata["venue"] == "Journal of Ports"
    assert result.metadata["cited_by_count"] == 12
    assert result.metadata["peer_reviewed"] is None  # never inferred from the venue
    assert result.metadata["open_access_url"] == "https://example.org/paper.pdf"


def test_openalex_maps_reviews_and_retractions_to_the_engine_taxonomy():
    payload = {"results": [
        {**OPENALEX_ITEM, "doi": "10.1000/rev", "type": "review"},
        {**OPENALEX_ITEM, "doi": "10.1000/ret", "type": "article", "is_retracted": True},
        {**OPENALEX_ITEM, "doi": "10.1000/thesis", "type": "dissertation"},
    ]}
    results = OpenAlexRetriever(http_get=lambda url: payload).search(SearchRequest("q"))
    assert [result.source_type for result in results] == ["secondary_source", "primary_study", "thesis"]
    assert results[1].metadata["retracted"] is True


def test_openalex_without_doi_falls_back_to_its_own_id():
    payload = {"results": [{"id": "https://openalex.org/W9", "doi": None, "title": "T", "type": "dataset"}]}
    result = OpenAlexRetriever(http_get=lambda url: payload).search(SearchRequest("q"))[0]
    assert result.id == "openalex:W9"
    assert result.source_type == "institutional_report"


def test_openalex_payload_without_results_is_an_error_not_an_empty_corpus():
    with pytest.raises(RetrievalError, match="results"):
        OpenAlexRetriever(http_get=lambda url: {"meta": {}}).search(SearchRequest("q"))


def test_abstract_reconstruction_respects_gaps_and_gives_up_gracefully():
    assert reconstruct_abstract({"Les": [0], "ports": [1], "mesurent.": [4]}) == "Les ports mesurent."
    assert reconstruct_abstract("texte déjà propre") == "texte déjà propre"
    assert reconstruct_abstract(None) == ""
    assert reconstruct_abstract({"seul": []}) == ""
    assert reconstruct_abstract({"mot": [0]}, max_chars=2) == "mo"


def test_openalex_enrichment_completes_records_from_their_dois():
    calls = []

    def fake_get(url):
        calls.append(url)
        return {"results": [OPENALEX_ITEM]}

    retriever = OpenAlexRetriever(http_get=fake_get)
    thin = SearchResult("doi:10.1000/abc", "Shipping emissions in ports", "https://doi.org/10.1000/abc",
                        "", "academic_record", {"doi": "10.1000/abc", "provider": "crossref"})
    complete = SearchResult("doi:10.1000/other", "Déjà complet", "https://doi.org/10.1000/other",
                            "Résumé existant", "primary_study",
                            {"doi": "10.1000/other", "authors": ["X"], "venue": "Y",
                             "enriched_by": ["openalex"]})

    enriched = retriever.enrich([thin, complete])

    assert len(calls) == 1 and "filter=doi%3A10.1000%2Fabc" in calls[0]
    assert enriched[0].snippet == "Port emissions matter."
    assert enriched[0].metadata["authors"] == ["Ada Demo"]
    assert enriched[0].metadata["enriched_by"] == ["openalex"]
    assert enriched[0].metadata["providers"] == ["crossref", "openalex"]
    assert enriched[1].snippet == "Résumé existant"
    assert retriever.last_enrichment == {"provider": "openalex", "candidates": 1, "matched": 1, "batches": 1}


def test_openalex_enrichment_batches_beyond_the_api_limit():
    calls = []

    def fake_get(url):
        calls.append(url)
        requested = unquote(url.split("filter=")[1].split("&")[0]).removeprefix("doi:")
        return {"results": [{**OPENALEX_ITEM, "doi": f"https://doi.org/{requested}"}]}

    retriever = OpenAlexRetriever(http_get=fake_get, max_doi_batch=1)
    results = [SearchResult(f"doi:10.1000/{index}", f"T{index}", None, "", "academic_record",
                            {"doi": f"10.1000/{index}"}) for index in range(3)]
    enriched = retriever.enrich(results)
    assert len(calls) == 3                              # one DOI per batch, three batches
    assert retriever.last_enrichment == {"provider": "openalex", "candidates": 3, "matched": 3, "batches": 3}
    assert all("enriched_by" in result.metadata for result in enriched)
    assert [result.snippet for result in enriched] == ["Port emissions matter."] * 3


def test_openalex_enrichment_is_a_no_op_without_dois():
    retriever = OpenAlexRetriever(http_get=lambda url: pytest.fail("no call expected"))
    results = [SearchResult("web:https://example.org/a", "T", "https://example.org/a", "s", "unverified_web")]
    assert retriever.enrich(results) == results
    assert retriever.last_enrichment["batches"] == 0


# ── Crawl4AI ─────────────────────────────────────────────────────────────────
def _clock():
    return datetime(2026, 10, 15, 12, 0, tzinfo=timezone.utc)


def test_crawl4ai_fetch_turns_a_page_into_traceable_markdown():
    payload = {"success": True, "results": [{
        "url": "https://example.org/a",
        "markdown": {"raw_markdown": "# Titre\n\nTexte brut.", "fit_markdown": "# Titre\n\nTexte filtré."},
        "metadata": {"title": "Titre"},
    }]}
    retriever = Crawl4AiRetriever(http_post=lambda url, body: payload, clock=_clock)

    result = retriever.fetch("https://example.org/a?utm_source=x")

    assert result.id == "web:https://example.org/a"
    assert result.title == "Titre"
    assert result.snippet == "# Titre\n\nTexte filtré."
    assert result.source_type == "secondary_source"
    assert result.metadata["full_text"] is True
    assert result.metadata["fetched_at"] == "2026-10-15T12:00:00+00:00"
    assert len(result.metadata["content_sha256"]) == 64
    assert result.metadata["truncated"] is False


def test_crawl4ai_accepts_the_single_page_and_flat_payload_shapes():
    assert extract_markdown({"markdown": "# Seul"})[0] == "# Seul"
    assert extract_markdown({"fit_markdown": "depuis un flat"})[0] == "depuis un flat"
    assert extract_markdown({"results": [{"markdown": "texte"}]}, variant="raw")[0] == "texte"
    assert extract_markdown({"results": [{}]}) == ("", None)


def test_crawl4ai_truncates_long_pages_and_refuses_empty_ones():
    long_markdown = "# T\n\n" + ("ligne " * 5000)
    retriever = Crawl4AiRetriever(http_post=lambda url, body: {"results": [{"markdown": long_markdown}]},
                                  max_chars=100, clock=_clock)
    result = retriever.fetch("https://example.org/long")
    assert result.metadata["truncated"] is True and len(result.snippet) == 100
    assert result.metadata["content_chars"] > 100

    with pytest.raises(RetrievalError, match="no markdown"):
        Crawl4AiRetriever(http_post=lambda url, body: {"results": []}).fetch("https://example.org/x")


def test_crawl4ai_search_needs_urls_and_isolates_per_url_errors():
    calls = []

    def fake_post(url, body):
        calls.append(body["urls"][0])
        if "casse" in body["urls"][0]:
            raise RetrievalError("boom")
        return {"results": [{"markdown": "# OK"}]}

    retriever = Crawl4AiRetriever(http_post=fake_post, clock=_clock)
    assert retriever.search(SearchRequest("q")) == []
    assert retriever.diagnostics()["note"].startswith("page reader")

    results = retriever.search(SearchRequest("q", metadata={"urls": [
        "https://example.org/ok", "https://example.org/casse"]}))
    assert [result.id for result in results] == ["web:https://example.org/ok"]
    assert retriever.diagnostics()["errors"][0]["url"] == "https://example.org/casse"


def test_crawl4ai_enrichment_replaces_snippets_and_keeps_going_after_a_failure():
    def fake_post(url, body):
        if "dead" in body["urls"][0]:
            raise RetrievalError("boom")
        return {"results": [{"markdown": "# Page\n\nCorps complet."}]}

    retriever = Crawl4AiRetriever(http_post=fake_post, clock=_clock)
    results = [
        SearchResult("web:https://example.org/live", "T", "https://example.org/live", "extrait",
                     "unverified_web", {"provider": "searxng"}),
        SearchResult("web:https://example.org/dead", "T2", "https://example.org/dead", "extrait",
                     "unverified_web", {"provider": "searxng"}),
        SearchResult("web:https://example.org/page-ok", "T3", "https://example.org/page-ok", "extrait",
                     "unverified_web", {"provider": "searxng"}),
    ]

    enriched = retriever.enrich(results, limit=3)

    assert enriched[0].metadata["full_text"] is True
    assert "Corps complet." in enriched[0].snippet
    assert enriched[0].source_type == "secondary_source"
    assert enriched[1].metadata.get("full_text") is None      # failure left it untouched
    assert retriever.last_enrichment["enriched"] == 2
    assert retriever.last_enrichment["errors"][0]["url"] == "https://example.org/dead"


def test_crawl4ai_skips_documents_that_already_carry_full_text():
    retriever = Crawl4AiRetriever(http_post=lambda url, body: pytest.fail("no call expected"))
    results = [SearchResult("web:x", "T", "https://example.org/x", "déjà complet",
                            "secondary_source", {"full_text": True})]
    assert retriever.enrich(results) == results
