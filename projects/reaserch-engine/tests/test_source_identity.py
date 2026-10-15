from engine.retrieval import SearchResult
from engine.source_identity import (
    canonical_url, identity_keys, merge_into, merge_results, normalize_doi,
    normalize_title, result_to_dict, unique_domains,
)


def test_doi_normalization_covers_the_shapes_providers_return():
    assert normalize_doi("https://doi.org/10.1000/ABC") == "10.1000/abc"
    assert normalize_doi("doi:10.1234/x.y") == "10.1234/x.y"
    assert normalize_doi("  10.1000/xyz.  ") == "10.1000/xyz"
    assert normalize_doi("not-a-doi") is None
    assert normalize_doi(None) is None


def test_canonical_url_drops_tracking_and_normalizes_host_and_query():
    assert canonical_url("HTTPS://Example.ORG:443/Path/?utm_source=nl&b=2&a=1#top") == \
        "https://example.org/Path?a=1&b=2"
    assert canonical_url("example.org") == "https://example.org"
    assert canonical_url("") is None


def test_normalized_title_refuses_generic_short_titles():
    assert normalize_title("Les Effets du Trafic Maritime !") == "les effets du trafic maritime"
    assert normalize_title("Résumé") is None
    assert normalize_title(None) is None


def test_identity_keys_are_ordered_by_reliability():
    result = SearchResult("doi:10.1000/x", "A study of ports",
                          "https://example.org/a/?utm_source=x", "",
                          metadata={"doi": "10.1000/X"})
    keys = identity_keys(result)
    assert keys[0] == "doi:10.1000/x"
    assert keys[1] == "url:https://example.org/a"
    assert keys[2].startswith("title:")


def test_merge_results_folds_duplicates_and_keeps_provenance():
    first = SearchResult("web:a", "Port air quality", "https://example.org/a", "court",
                         "unverified_web", {"provider": "searxng", "rank": 1})
    duplicate = SearchResult("web:b", "Port air quality", "https://example.org/a?utm_source=x",
                             "un extrait nettement plus long et plus utile", "secondary_source",
                             {"provider": "crawl4ai", "rank": 2})
    other = SearchResult("web:c", "Autre sujet", "https://example.org/c", "s", "unverified_web")

    outcome = merge_results([first, duplicate, other])

    assert [result.id for result in outcome.results] == ["web:a", "web:c"]
    assert outcome.duplicates_merged == 1
    merged = outcome.results[0]
    assert merged.snippet == "un extrait nettement plus long et plus utile"
    assert merged.source_type == "secondary_source"
    assert merged.metadata["providers"] == ["crawl4ai", "searxng"]
    assert merged.metadata["provider_ranks"] == {"searxng": 1, "crawl4ai": 2}
    assert merged.metadata["merged_from"] == ["web:a", "web:b"]


def test_merge_into_fills_missing_fields_without_overwriting_present_ones():
    keeper = SearchResult("doi:10.1/x", "Titre", None, "", "academic_record",
                          {"doi": "10.1/x", "venue": "Revue A"})
    completion = SearchResult("doi:10.1/x", "Titre", "https://doi.org/10.1/x", "Résumé long",
                              "primary_study",
                              {"doi": "10.1/x", "venue": "Revue B", "year": 2024, "cited_by_count": 5})

    merged = merge_into(keeper, completion)

    assert merged.metadata["venue"] == "Revue A"       # existing value wins
    assert merged.metadata["year"] == 2024             # missing value filled
    assert merged.url == "https://doi.org/10.1/x"
    assert merged.snippet == "Résumé long"
    assert merged.source_type == "primary_study"


def test_projection_and_domain_listing_are_report_friendly():
    results = [
        SearchResult("a", "T", "https://www.example.org/x", "s", "unverified_web"),
        SearchResult("b", "T2", "https://example.org/y", "s", "unverified_web"),
        SearchResult("c", "T3", None, "s", "unverified_web"),
    ]
    assert unique_domains(results) == ["example.org"]
    projected = result_to_dict(results[0])
    assert set(projected) == {"id", "title", "url", "snippet", "source_type", "metadata"}
