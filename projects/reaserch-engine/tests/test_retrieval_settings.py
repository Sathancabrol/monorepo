import json

from engine.settings import (
    DEFAULT_CRAWL4AI_URL, DEFAULT_SEARXNG_URL, RetrievalSettings,
    build_federated, build_registry, build_retrievers,
)


def test_defaults_are_local_keyless_and_fully_enabled():
    settings = RetrievalSettings.from_env({})

    assert settings.searxng_url == DEFAULT_SEARXNG_URL
    assert settings.crawl4ai_url == DEFAULT_CRAWL4AI_URL
    assert settings.openalex_mailto is None and settings.crossref_mailto is None
    assert (settings.enable_searxng, settings.enable_crawl4ai,
            settings.enable_openalex, settings.enable_crossref) == (True, True, True, True)
    assert list(build_retrievers(settings)) == ["searxng", "openalex", "crossref", "crawl4ai"]


def test_a_provider_can_be_turned_off_by_an_empty_url_or_an_explicit_flag():
    by_url = RetrievalSettings.from_env({"SEARXNG_BASE_URL": ""})
    assert by_url.searxng_url is None and by_url.enable_searxng is False
    assert "searxng" not in build_retrievers(by_url)

    by_flag = RetrievalSettings.from_env({"CRAWL4AI_DISABLED": "1", "OPENALEX_DISABLED": "true"})
    assert by_flag.enable_crawl4ai is False and by_flag.enable_openalex is False
    assert list(build_retrievers(by_flag)) == ["searxng", "crossref"]


def test_aliases_numbers_and_lists_are_read_from_the_environment():
    settings = RetrievalSettings.from_env({
        "SEARCH_BASE_URL": "http://localhost:9999",
        "RESEARCH_MAX_ROUNDS": "5",
        "RESEARCH_RESULTS_PER_QUERY": "12",
        "SEARXNG_CATEGORIES": "general, news",
        "SEARXNG_ENGINES": "duckduckgo,mojeek",
        "RESEARCH_LANGUAGE": "en",
        "OPENALEX_MAILTO": "research@example.org",
    })

    assert settings.searxng_url == "http://localhost:9999"
    assert (settings.max_rounds, settings.results_per_query) == (5, 12)
    assert settings.searxng_categories == ["general", "news"]
    assert settings.searxng_engines == ["duckduckgo", "mojeek"]
    assert settings.language == "en" and settings.openalex_mailto == "research@example.org"


def test_malformed_numbers_fall_back_instead_of_crashing():
    settings = RetrievalSettings.from_env({"RESEARCH_MAX_ROUNDS": "beaucoup", "RESEARCH_RESULTS_PER_QUERY": ""})
    assert settings.max_rounds == 3 and settings.results_per_query == 10


def test_reported_settings_never_leak_contact_addresses():
    settings = RetrievalSettings.from_env({"OPENALEX_MAILTO": "moi@example.org",
                                          "CROSSREF_MAILTO": "moi@example.org"})
    payload = json.dumps(settings.as_dict(), ensure_ascii=False)
    assert "moi@example.org" not in payload
    assert settings.as_dict()["polite_pool_configured"] is True


def test_the_page_reader_is_an_enricher_not_a_discovery_provider():
    federation = build_federated(RetrievalSettings.from_env({}),
                                http_get=lambda url: {"results": []},
                                http_post=lambda url, body: {"results": [{"markdown": "# ok"}]})

    assert federation.provider_names() == ["searxng", "openalex", "crossref"]
    assert [getattr(enricher, "name", "?") for enricher in federation.enrichers] == ["openalex", "crawl4ai"]


def test_registry_exposes_the_configured_retrievers():
    registry = build_registry(RetrievalSettings.from_env({"SEARXNG_BASE_URL": "",
                                                         "CRAWL4AI_BASE_URL": ""}))
    assert registry.names() == ["openalex", "crossref"]
    assert len(registry) == 2 and "openalex" in registry
    assert registry.get("crossref").retriever.__class__.__name__ == "CrossrefRetriever"


def test_disabling_everything_yields_an_empty_federation_that_still_runs():
    settings = RetrievalSettings(enable_searxng=False, enable_crawl4ai=False,
                                 enable_openalex=False, enable_crossref=False)
    federation = build_federated(settings)
    assert federation.provider_names() == []
    assert federation.enrichers == []

    from engine.iteration import IterativeSearch
    report = IterativeSearch(federation, max_rounds=1).run("question sans fournisseur")
    assert report.corpus == []
    assert report.stop_reason in {"evidence_saturation", "queries_exhausted", "max_rounds_reached"}
