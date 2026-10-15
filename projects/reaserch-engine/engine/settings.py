"""Environment-driven wiring for the retrieval layer.

The engine stays usable with **zero configuration and zero keys**:

- ``searxng`` — a local SearXNG instance (``http://127.0.0.1:8080`` by default,
  the address used by the Watchtower audit stack);
- ``crawl4ai`` — a local Crawl4AI server (``http://127.0.0.1:11235``), used as a
  page *reader* / enricher, never as a discovery provider;
- ``openalex`` / ``crossref`` — public scholarly APIs, keyless.

Nothing is registered twice and nothing is called at import time. A provider is
skipped when its URL is explicitly emptied (``SEARXNG_BASE_URL=``) or when its
``*_DISABLED`` flag is set, so an operator can run the engine with only, say,
OpenAlex and no local containers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import os
from typing import Callable, Mapping

from .federation import FederatedRetriever
from .iteration import DEFAULT_MAX_ROUNDS, DEFAULT_RESULTS_PER_QUERY
from .providers import ProviderRegistry
from .retrieval import CrossrefRetriever
from .web_retrieval import Crawl4AiRetriever, OpenAlexRetriever, SearxngRetriever

DEFAULT_SEARXNG_URL = "http://127.0.0.1:8080"
DEFAULT_CRAWL4AI_URL = "http://127.0.0.1:11235"

_TRUTHY = {"1", "true", "yes", "on", "oui", "vrai"}
_FALSY = {"0", "false", "no", "off", "non", "faux", ""}


def _flag(env: Mapping[str, str], name: str, *, default: bool) -> bool:
    raw = env.get(name)
    if raw is None:
        return default
    value = raw.strip().lower()
    if value in _TRUTHY:
        return True
    if value in _FALSY:
        return False
    return default


def _int(env: Mapping[str, str], name: str, *, default: int) -> int:
    raw = env.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        return int(float(raw))
    except ValueError:
        return default


def _text(env: Mapping[str, str], *names: str, default: str | None = None) -> str | None:
    """First set-and-non-empty variable among ``names`` (empty string = unset)."""
    for name in names:
        if name in env:
            return (env.get(name) or "").strip() or None
    return default


def _url(env: Mapping[str, str], *names: str, default: str) -> str | None:
    """First non-empty environment URL among ``names`` (empty string disables)."""
    for name in names:
        if name in env:
            return (env.get(name) or "").strip() or None
    return default


@dataclass
class RetrievalSettings:
    """Resolved retrieval configuration (one place to read, one place to test)."""

    searxng_url: str | None = DEFAULT_SEARXNG_URL
    crawl4ai_url: str | None = DEFAULT_CRAWL4AI_URL
    openalex_mailto: str | None = None
    crossref_mailto: str | None = None
    language: str = "fr"
    search_language: str | None = "fr"
    enable_searxng: bool = True
    enable_crawl4ai: bool = True
    enable_openalex: bool = True
    enable_crossref: bool = True
    max_rounds: int = DEFAULT_MAX_ROUNDS
    results_per_query: int = DEFAULT_RESULTS_PER_QUERY
    crawl4ai_enrich_limit: int = 3
    crawl4ai_max_chars: int = 20000
    searxng_categories: list[str] = field(default_factory=list)
    searxng_engines: list[str] = field(default_factory=list)

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "RetrievalSettings":
        source = os.environ if env is None else env
        settings = cls(
            searxng_url=_url(source, "SEARXNG_BASE_URL", "SEARCH_BASE_URL", default=DEFAULT_SEARXNG_URL),
            crawl4ai_url=_url(source, "CRAWL4AI_BASE_URL", "CRAWL4AI_URL", default=DEFAULT_CRAWL4AI_URL),
            openalex_mailto=_text(source, "OPENALEX_MAILTO"),
            crossref_mailto=_text(source, "CROSSREF_MAILTO", "RESEARCH_CONTACT_EMAIL"),
            language=(_text(source, "RESEARCH_LANGUAGE") or "fr"),
            search_language=_text(source, "SEARXNG_LANGUAGE", default="fr"),
            enable_searxng=not _flag(source, "SEARXNG_DISABLED", default=False),
            enable_crawl4ai=not _flag(source, "CRAWL4AI_DISABLED", default=False),
            enable_openalex=not _flag(source, "OPENALEX_DISABLED", default=False),
            enable_crossref=not _flag(source, "CROSSREF_DISABLED", default=False),
            max_rounds=_int(source, "RESEARCH_MAX_ROUNDS", default=DEFAULT_MAX_ROUNDS),
            results_per_query=_int(source, "RESEARCH_RESULTS_PER_QUERY", default=DEFAULT_RESULTS_PER_QUERY),
            crawl4ai_enrich_limit=_int(source, "RESEARCH_CRAWL4AI_ENRICH_LIMIT", default=3),
            crawl4ai_max_chars=_int(source, "CRAWL4AI_MAX_CHARS", default=20000),
            searxng_categories=_csv(source.get("SEARXNG_CATEGORIES")),
            searxng_engines=_csv(source.get("SEARXNG_ENGINES")),
        )
        if settings.searxng_url is None:
            settings.enable_searxng = False
        if settings.crawl4ai_url is None:
            settings.enable_crawl4ai = False
        return settings

    def as_dict(self) -> dict:
        """Redacted view for reports: no mailto, no credentials."""
        return {
            "searxng": self.searxng_url if self.enable_searxng else None,
            "crawl4ai": self.crawl4ai_url if self.enable_crawl4ai else None,
            "openalex": self.enable_openalex,
            "crossref": self.enable_crossref,
            "polite_pool_configured": bool(self.openalex_mailto or self.crossref_mailto),
            "language": self.language,
            "search_language": self.search_language,
            "max_rounds": self.max_rounds,
            "results_per_query": self.results_per_query,
        }


def _csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def build_retrievers(settings: RetrievalSettings, *,
                     http_get: Callable[[str], dict] | None = None,
                     http_post: Callable[[str, dict], dict] | None = None,
                     clock=None) -> dict:
    """Instantiate the providers the settings enable (no network at build time)."""
    retrievers: dict = {}
    if settings.enable_searxng and settings.searxng_url:
        retrievers["searxng"] = SearxngRetriever(
            settings.searxng_url, http_get=http_get, language=settings.search_language,
            categories=settings.searxng_categories, engines=settings.searxng_engines,
        )
    if settings.enable_openalex:
        retrievers["openalex"] = OpenAlexRetriever(settings.openalex_mailto, http_get=http_get)
    if settings.enable_crossref:
        retrievers["crossref"] = CrossrefRetriever(settings.crossref_mailto, http_get=http_get)
    if settings.enable_crawl4ai and settings.crawl4ai_url:
        retrievers["crawl4ai"] = Crawl4AiRetriever(
            settings.crawl4ai_url, http_post=http_post,
            max_chars=settings.crawl4ai_max_chars, clock=clock,
        )
    return retrievers


def build_registry(settings: RetrievalSettings | None = None, **kwargs) -> ProviderRegistry:
    settings = settings or RetrievalSettings.from_env()
    registry = ProviderRegistry()
    for name, retriever in build_retrievers(settings, **kwargs).items():
        registry.register_retriever(name, retriever)
    return registry


def build_federated(settings: RetrievalSettings | None = None, *,
                    weights: dict[str, float] | None = None,
                    http_get=None, http_post=None, clock=None) -> FederatedRetriever:
    """Discovery federation + enrichment chain, ready to hand to the loop.

    ``crawl4ai`` is deliberately **not** a discovery provider (it cannot answer a
    query on its own); it joins as an enricher that replaces snippets with full
    page text. OpenAlex doubles as discovery and DOI-completion enricher.
    """
    settings = settings or RetrievalSettings.from_env()
    retrievers = build_retrievers(settings, http_get=http_get, http_post=http_post, clock=clock)
    discovery = {name: retriever for name, retriever in retrievers.items() if name != "crawl4ai"}
    enrichers = []
    if settings.enable_openalex and "openalex" in retrievers:
        enrichers.append(retrievers["openalex"])
    if settings.enable_crawl4ai and "crawl4ai" in retrievers:
        enrichers.append(_LimitedEnricher(retrievers["crawl4ai"], limit=settings.crawl4ai_enrich_limit))
    return FederatedRetriever(discovery, weights=weights, enrichers=enrichers, clock=clock)


class _LimitedEnricher:
    """Binds an enrich limit without changing the retriever's public defaults."""

    def __init__(self, retriever, *, limit: int):
        self.retriever = retriever
        self.limit = max(1, limit)
        self.name = getattr(retriever, "name", type(retriever).__name__)
        self.last_enrichment: dict = {}

    def enrich(self, results):
        enriched = self.retriever.enrich(results, limit=self.limit)
        self.last_enrichment = getattr(self.retriever, "last_enrichment", {})
        return enriched
