"""Web, scholarly and page-reading retrievers for the Research Engine.

Three adapters sit behind the existing :class:`engine.retrieval.Retriever`
protocol, so the engine core still performs no network I/O on its own:

- :class:`SearxngRetriever` — discovery through a self-hosted SearXNG instance
  (``format=json``), keyless, no query ever leaves the machine unless the
  operator configures upstream engines.
- :class:`OpenAlexRetriever` — scholarly discovery over the public OpenAlex
  Works API, plus ``enrich`` which completes a corpus with abstracts, authors,
  venues and citation counts from DOIs already present.
- :class:`Crawl4AiRetriever` — a *page reader*, not a discovery engine: it turns
  a URL into markdown through a local Crawl4AI server, and ``enrich`` upgrades
  discovery snippets into full text.

Every adapter takes an injectable transport (``http_get``/``http_post``) and
never calls the network at import or construction time. Transport, payload and
configuration problems are raised as :class:`engine.retrieval.RetrievalError`
so a caller (or the federation layer) can fail soft per provider.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
from typing import Callable, Iterable
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .retrieval import RetrievalError, SearchRequest, SearchResult
from .source_identity import canonical_url, merge_into, normalize_doi

USER_AGENT = "ResearchEngine/0.2 (+local research assistant)"

#: SearXNG ``time_range`` buckets, from a day count.
TIME_RANGES = ((1, "day"), (7, "week"), (31, "month"), (365, "year"))

#: OpenAlex work types mapped onto the engine's source taxonomy. Anything not
#: listed stays ``academic_record``: the engine never upgrades a record to
#: primary evidence from a venue name alone.
OPENALEX_SOURCE_TYPES = {
    "article": "primary_study",
    "preprint": "primary_study",
    "dataset": "institutional_report",
    "report": "institutional_report",
    "dissertation": "thesis",
    "book": "academic_book",
    "book-chapter": "academic_book",
    "review": "secondary_source",
    "editorial": "opinion",
    "letter": "opinion",
    "erratum": "academic_record",
    "retraction": "academic_record",
}


def _iso_now(clock: Callable[[], datetime] | None = None) -> str:
    moment = clock() if clock else datetime.now(timezone.utc)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc).isoformat(timespec="seconds")


def default_http_get(url: str, *, timeout: float = 15.0) -> dict:
    """Minimal JSON GET used when no transport is injected."""
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urlopen(request, timeout=timeout) as response:  # nosec B310: operator-selected endpoint
            raw = response.read().decode("utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001 - normalized into a provider error
        raise RetrievalError(f"GET {url} failed: {exc}") from exc
    try:
        return json.loads(raw)
    except ValueError as exc:
        raise RetrievalError(f"GET {url} returned non-JSON payload: {exc}") from exc


def default_http_post(url: str, payload: dict, *, timeout: float = 60.0) -> dict:
    """Minimal JSON POST used when no transport is injected."""
    body = json.dumps(payload).encode("utf-8")
    request = Request(url, data=body, method="POST",
                      headers={"User-Agent": USER_AGENT, "Content-Type": "application/json",
                               "Accept": "application/json"})
    try:
        with urlopen(request, timeout=timeout) as response:  # nosec B310: operator-selected endpoint
            raw = response.read().decode("utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001 - normalized into a provider error
        raise RetrievalError(f"POST {url} failed: {exc}") from exc
    try:
        return json.loads(raw)
    except ValueError as exc:
        raise RetrievalError(f"POST {url} returned non-JSON payload: {exc}") from exc


def time_range_for(days: int | None) -> str | None:
    if not days or days <= 0:
        return None
    for threshold, value in TIME_RANGES:
        if days <= threshold:
            return value
    return None


def web_result_id(url: str) -> str | None:
    canonical = canonical_url(url)
    return f"web:{canonical}" if canonical else None


@dataclass
class _ProviderDiagnostics:
    """Small, JSON-safe diagnostics block attached to each search call."""

    def __init__(self, **values):
        self.values = values

    def as_dict(self) -> dict:
        return dict(self.values)


class SearxngRetriever:
    """Discovery over a self-hosted SearXNG instance (JSON output required).

    The ``format=json`` output format must be enabled in ``settings.yml``
    (``search.formats: [html, json]``); without it SearXNG answers HTML and this
    adapter raises :class:`RetrievalError` instead of pretending to have no
    results — an empty corpus and a broken provider are different states.
    """

    name = "searxng"

    def __init__(self, base_url: str = "http://127.0.0.1:8080", *,
                 http_get: Callable[[str], dict] | None = None,
                 language: str | None = "fr",
                 categories: Iterable[str] | None = None,
                 engines: Iterable[str] | None = None,
                 time_range: str | None = None,
                 safesearch: int = 0,
                 endpoint_path: str = "/search"):
        self.base_url = (base_url or "").rstrip("/")
        self.endpoint_path = endpoint_path if endpoint_path.startswith("/") else f"/{endpoint_path}"
        self.http_get = http_get or default_http_get
        self.language = language
        self.categories = list(categories or [])
        self.engines = list(engines or [])
        self.time_range = time_range
        self.safesearch = safesearch
        self.last_diagnostics: dict = {}

    def build_url(self, request: SearchRequest) -> str:
        params = {
            "q": request.query,
            "format": "json",
            "pageno": 1,
            "safesearch": self.safesearch,
        }
        if self.language:
            params["language"] = self.language
        if self.categories:
            params["categories"] = ",".join(self.categories)
        if self.engines:
            params["engines"] = ",".join(self.engines)
        time_range = self.time_range or time_range_for(request.recency_days)
        if time_range:
            params["time_range"] = time_range
        return f"{self.base_url}{self.endpoint_path}?{urlencode(params)}"

    def search(self, request: SearchRequest) -> list[SearchResult]:
        if not self.base_url:
            raise RetrievalError("searxng: no base_url configured")
        url = self.build_url(request)
        payload = self.http_get(url)
        if not isinstance(payload, dict):
            raise RetrievalError(f"searxng: unexpected payload type {type(payload).__name__}")
        if "results" not in payload:
            raise RetrievalError("searxng: payload has no 'results' key (is format=json enabled?)")

        results: list[SearchResult] = []
        skipped = 0
        for position, item in enumerate(payload.get("results") or [], start=1):
            if not isinstance(item, dict):
                skipped += 1
                continue
            result_id = web_result_id(item.get("url") or "")
            if not result_id:
                skipped += 1
                continue
            engines = item.get("engines") or ([item["engine"]] if item.get("engine") else [])
            results.append(SearchResult(
                id=result_id,
                title=(item.get("title") or item.get("url") or "").strip(),
                url=canonical_url(item.get("url")),
                snippet=(item.get("content") or "").strip(),
                source_type="unverified_web",
                metadata={
                    "provider": self.name,
                    "rank": position,
                    "query": request.query,
                    "engines": [str(name) for name in engines],
                    "category": item.get("category"),
                    "score": item.get("score"),
                    "published": item.get("publishedDate"),
                },
            ))
        self.last_diagnostics = {
            "provider": self.name,
            "query": request.query,
            "returned": len(results),
            "skipped": skipped,
            "unresponsive_engines": _normalize_unresponsive(payload.get("unresponsive_engines")),
            "answer_count": len(payload.get("answers") or []),
            "suggestion_count": len(payload.get("suggestions") or []),
        }
        limit = request.max_results or len(results)
        return results[:limit]

    def diagnostics(self) -> dict:
        return dict(self.last_diagnostics)


def _normalize_unresponsive(value) -> list[dict]:
    """SearXNG reports dead engines as pairs, dicts or plain strings."""
    normalized = []
    for entry in value or []:
        if isinstance(entry, (list, tuple)) and entry:
            normalized.append({"engine": str(entry[0]), "reason": str(entry[1]) if len(entry) > 1 else ""})
        elif isinstance(entry, dict):
            normalized.append({"engine": str(entry.get("engine", "")), "reason": str(entry.get("reason", ""))})
        elif isinstance(entry, str):
            normalized.append({"engine": entry, "reason": ""})
    return normalized


class OpenAlexRetriever:
    """Scholarly discovery and corpus enrichment over the OpenAlex Works API.

    OpenAlex is keyless. Supplying ``mailto`` only joins the polite pool.
    ``search`` is bounded discovery; ``enrich`` is the data-completion step that
    turns a thin DOI reference (from Crossref, SearXNG or a bibliography) into a
    record carrying abstract, authors, venue, year and citation count.
    """

    name = "openalex"
    endpoint = "https://api.openalex.org/works"
    #: OpenAlex caps OR filters; staying at 25 keeps requests comfortably valid.
    max_doi_batch = 25
    max_per_page = 200

    def __init__(self, mailto: str | None = None, *,
                 http_get: Callable[[str], dict] | None = None,
                 endpoint: str | None = None,
                 filter: str | None = None,
                 sort: str | None = None,
                 per_page: int = 25,
                 max_doi_batch: int | None = None,
                 max_abstract_chars: int = 1200,
                 today: Callable[[], date] | None = None):
        self.mailto = mailto
        self.http_get = http_get or default_http_get
        self.endpoint = endpoint or self.endpoint
        self.filter = filter
        self.sort = sort
        self.per_page = max(1, min(per_page, self.max_per_page))
        self.max_doi_batch = max(1, min(max_doi_batch or self.max_doi_batch, 50))
        self.max_abstract_chars = max_abstract_chars
        self.today = today or date.today
        self.last_diagnostics: dict = {}
        self.last_enrichment: dict = {}

    # ── discovery ────────────────────────────────────────────────────────────
    def build_url(self, request: SearchRequest) -> str:
        params: dict[str, str] = {
            "search": request.query,
            "per-page": str(min(request.max_results or self.per_page, self.max_per_page)),
        }
        if self.mailto:
            params["mailto"] = self.mailto
        filters = [self.filter] if self.filter else []
        if request.recency_days and request.recency_days > 0:
            since = self.today() - timedelta(days=request.recency_days)
            filters.append(f"from_publication_date:{since.isoformat()}")
        if filters:
            params["filter"] = ",".join(filters)
        if self.sort:
            params["sort"] = self.sort
        return f"{self.endpoint}?{urlencode(params)}"

    def search(self, request: SearchRequest) -> list[SearchResult]:
        url = self.build_url(request)
        payload = self.http_get(url)
        items = _openalex_items(payload, url)
        results = [self._to_result(item, request, rank) for rank, item in enumerate(items, start=1)]
        results = [result for result in results if result is not None]
        self.last_diagnostics = {
            "provider": self.name,
            "query": request.query,
            "returned": len(results),
            "url": url,
        }
        limit = request.max_results or len(results)
        return results[:limit]

    def _to_result(self, item: dict, request: SearchRequest, rank: int) -> SearchResult | None:
        doi = normalize_doi(item.get("doi"))
        openalex_id = item.get("id")
        if doi:
            result_id = f"doi:{doi}"
            url = f"https://doi.org/{doi}"
        elif openalex_id:
            result_id = f"openalex:{str(openalex_id).rsplit('/', 1)[-1]}"
            url = openalex_id
        else:
            return None
        location = item.get("primary_location") or {}
        source = (location.get("source") or {}) if isinstance(location, dict) else {}
        best_oa = item.get("best_oa_location") or {}
        item_type = (item.get("type") or "").lower()
        abstract = reconstruct_abstract(item.get("abstract_inverted_index"),
                                        max_chars=self.max_abstract_chars)
        metadata = {
            "provider": self.name,
            "rank": rank,
            "query": request.query,
            "doi": doi,
            "openalex_id": openalex_id,
            "authors": _authors(item.get("authorships")),
            "venue": source.get("display_name"),
            "venue_type": source.get("type"),
            "year": item.get("publication_year"),
            "publication_date": item.get("publication_date"),
            "cited_by_count": item.get("cited_by_count"),
            "openalex_type": item_type or None,
            "type_crossref": item.get("type_crossref"),
            "is_oa": item.get("is_oa") if item.get("is_oa") is not None else (item.get("open_access") or {}).get("is_oa"),
            "open_access_url": (best_oa or {}).get("pdf_url") or (best_oa or {}).get("landing_page_url"),
            "language": item.get("language"),
            "retracted": bool(item.get("is_retracted")),
            "peer_reviewed": None,  # never inferred from a venue name
        }
        if item.get("abstract_inverted_index") is None and abstract:
            metadata["abstract_source"] = "provider_text"
        return SearchResult(
            id=result_id,
            title=(item.get("title") or item.get("display_name") or doi or "").strip(),
            url=canonical_url(url),
            snippet=abstract,
            source_type=OPENALEX_SOURCE_TYPES.get(item_type, "academic_record"),
            metadata=metadata,
        )

    # ── enrichment ───────────────────────────────────────────────────────────
    def enrich(self, results: Iterable, *, only_missing: bool = True) -> list:
        """Complete records that carry a DOI but miss abstract/author metadata.

        Existing values always win; only empty fields are filled, and every
        record keeps a trace of who enriched it (``metadata["enriched_by"]``).
        """
        results = list(results)
        targets = [(position, result) for position, result in enumerate(results)
                   if _enrichment_target(result, only_missing=only_missing)]
        self.last_enrichment = {"provider": self.name, "candidates": len(targets), "matched": 0, "batches": 0}
        if not targets:
            return results

        by_doi: dict[str, list[int]] = {}
        for position, result in targets:
            doi = normalize_doi((result.metadata or {}).get("doi"))
            if doi:
                by_doi.setdefault(doi, []).append(position)
        if not by_doi:
            return results

        records: dict[str, dict] = {}
        dois = sorted(by_doi)
        for start in range(0, len(dois), self.max_doi_batch):
            batch = dois[start:start + self.max_doi_batch]
            params = {"filter": "doi:" + "|".join(batch), "per-page": str(len(batch))}
            if self.mailto:
                params["mailto"] = self.mailto
            url = f"{self.endpoint}?{urlencode(params)}"
            payload = self.http_get(url)
            items = _openalex_items(payload, url)
            self.last_enrichment["batches"] += 1
            for item in items:
                doi = normalize_doi(item.get("doi"))
                if doi:
                    records[doi] = item

        if not records:
            return results
        enriched = list(results)
        for doi, positions in by_doi.items():
            item = records.get(doi)
            if not item:
                continue
            completion = self._to_result(item, SearchRequest(query="", max_results=1), rank=0)
            if completion is None:
                continue
            for position in positions:
                enriched[position] = _apply_enrichment(enriched[position], completion)
            self.last_enrichment["matched"] += len(positions)
        return enriched


def _enrichment_target(result, *, only_missing: bool) -> bool:
    metadata = getattr(result, "metadata", None) or {}
    if not normalize_doi(metadata.get("doi")):
        return False
    if not only_missing:
        return True
    missing = not (result.snippet or "").strip() or not metadata.get("authors") or not metadata.get("venue")
    return missing and "openalex" not in (metadata.get("enriched_by") or [])


def _apply_enrichment(result, completion) -> object:
    """Fill empty fields of ``result`` from ``completion`` without overwriting.

    The merge keeps the original identifier, the richer snippet and every value
    already present; the record simply gains what was missing.
    """
    merged = merge_into(result, completion)
    metadata = dict(merged.metadata)
    metadata["enriched_by"] = sorted(set(list((result.metadata or {}).get("enriched_by") or []) + [OpenAlexRetriever.name]))
    metadata["providers"] = sorted(set(list(metadata.get("providers") or []) + [OpenAlexRetriever.name]))
    merged.metadata = metadata
    return merged


def _openalex_items(payload, url: str) -> list[dict]:
    if not isinstance(payload, dict):
        raise RetrievalError(f"openalex: unexpected payload type {type(payload).__name__}")
    items = payload.get("results")
    if items is None:
        raise RetrievalError(f"openalex: payload has no 'results' key ({url})")
    if not isinstance(items, list):
        raise RetrievalError("openalex: 'results' is not a list")
    return [item for item in items if isinstance(item, dict)]


def _authors(authorships) -> list[str]:
    names = []
    for entry in authorships or []:
        if not isinstance(entry, dict):
            continue
        author = entry.get("author") or {}
        name = author.get("display_name") or " ".join(
            part for part in [author.get("given_name"), author.get("family_name")] if part)
        if name:
            names.append(name)
    return names[:20]


def reconstruct_abstract(inverted_index, *, max_chars: int = 1200) -> str:
    """Rebuild readable text from OpenAlex ``abstract_inverted_index``.

    The index maps tokens to positions, so gaps (words OpenAlex removed for
    copyright) become single spaces rather than a joined wall of text. Tokens
    whose positions are unusable are skipped instead of failing the record.
    """
    if isinstance(inverted_index, str):
        return inverted_index.strip()[:max_chars]
    if not isinstance(inverted_index, dict) or not inverted_index:
        return ""
    positioned: list[tuple[int, str]] = []
    for token, positions in inverted_index.items():
        if not isinstance(positions, (list, tuple)):
            continue
        for position in positions:
            if isinstance(position, int) and position >= 0:
                positioned.append((position, str(token)))
    if not positioned:
        return ""
    positioned.sort(key=lambda pair: pair[0])
    text = " ".join(token for _, token in positioned)
    return " ".join(text.split())[:max_chars]


class Crawl4AiRetriever:
    """Page reader over a local Crawl4AI server (``POST /crawl``).

    This adapter does not discover anything: it turns given URLs into markdown
    so the evidence extractor works on documents instead of search snippets.
    ``search`` reads ``request.metadata["urls"]``; ``enrich`` upgrades the first
    N eligible results of a discovered corpus.
    """

    name = "crawl4ai"
    #: A fetched page is a document; turning it into evidence is a later phase.
    page_source_type = "secondary_source"

    def __init__(self, base_url: str = "http://127.0.0.1:11235", *,
                 http_post: Callable[[str, dict], dict] | None = None,
                 path: str = "/crawl",
                 markdown_variant: str = "fit",
                 max_chars: int = 20000,
                 timeout_ms: int = 20000,
                 clock: Callable[[], datetime] | None = None):
        self.base_url = (base_url or "").rstrip("/")
        self.path = path if path.startswith("/") else f"/{path}"
        self.http_post = http_post or default_http_post
        self.markdown_variant = markdown_variant
        self.max_chars = max_chars
        self.timeout_ms = timeout_ms
        self.clock = clock
        self.last_diagnostics: dict = {}
        self.last_enrichment: dict = {}

    def _post(self, urls: list[str]) -> dict:
        payload = {"urls": list(urls), "crawler_config": {"cache_mode": "bypass"}}
        return self.http_post(self.url, payload)

    @property
    def url(self) -> str:
        return f"{self.base_url}{self.path}"

    def fetch(self, url: str) -> SearchResult:
        """Read one page and return it as a markdown-backed result."""
        if not self.base_url:
            raise RetrievalError("crawl4ai: no base_url configured")
        payload = self._post([url])
        markdown, title = extract_markdown(payload, variant=self.markdown_variant)
        if not markdown:
            raise RetrievalError(f"crawl4ai: no markdown returned for {url}")
        result_id = web_result_id(url)
        if not result_id:
            raise RetrievalError(f"crawl4ai: unusable url {url!r}")
        truncated = len(markdown) > self.max_chars
        return SearchResult(
            id=result_id,
            title=(title or _first_heading(markdown) or url).strip(),
            url=canonical_url(url),
            snippet=markdown[:self.max_chars],
            source_type=self.page_source_type,
            metadata={
                "provider": self.name,
                "fetched_at": _iso_now(self.clock),
                "markdown_variant": self.markdown_variant,
                "content_chars": len(markdown),
                "content_sha256": hashlib.sha256(markdown.encode("utf-8")).hexdigest(),
                "truncated": truncated,
                "full_text": True,
            },
        )

    def search(self, request: SearchRequest) -> list[SearchResult]:
        urls = list((request.metadata or {}).get("urls") or [])
        if not urls and (request.metadata or {}).get("url"):
            urls = [request.metadata["url"]]
        if not urls:
            self.last_diagnostics = {"provider": self.name, "urls": 0,
                                     "note": "page reader: needs request.metadata['urls']"}
            return []
        results, errors = [], []
        for url in urls[:max(1, request.max_results)]:
            try:
                results.append(self.fetch(url))
            except RetrievalError as exc:
                errors.append({"url": url, "error": str(exc)})
        self.last_diagnostics = {"provider": self.name, "urls": len(urls),
                                 "returned": len(results), "errors": errors}
        return results

    def enrich(self, results: Iterable, *, limit: int = 3,
               source_types: Iterable[str] = ("unverified_web",),
               max_chars: int | None = None) -> list:
        """Replace discovery snippets with the page's full markdown text."""
        results = list(results)
        eligible = [position for position, result in enumerate(results)
                    if getattr(result, "url", None)
                    and result.source_type in set(source_types)
                    and not (result.metadata or {}).get("full_text")]
        self.last_enrichment = {"provider": self.name, "candidates": len(eligible),
                                "enriched": 0, "errors": []}
        enriched = list(results)
        for position in eligible[:max(0, limit)]:
            result = enriched[position]
            try:
                page = self.fetch(result.url)
            except RetrievalError as exc:
                self.last_enrichment["errors"].append({"url": result.url, "error": str(exc)})
                continue
            if max_chars:
                page.snippet = page.snippet[:max_chars]
            merged = merge_into(result, page)
            metadata = dict(merged.metadata)
            metadata["full_text"] = True
            metadata["enriched_by"] = sorted(set(list(metadata.get("enriched_by") or []) + [self.name]))
            metadata["providers"] = sorted(set(list(metadata.get("providers") or []) + [self.name]))
            for key in ("fetched_at", "content_sha256", "content_chars", "truncated", "markdown_variant"):
                if page.metadata.get(key) is not None:
                    metadata.setdefault(key, page.metadata[key])
            merged.metadata = metadata
            if merged.source_type in ("", "unknown", "unverified_web"):
                merged.source_type = self.page_source_type
            enriched[position] = merged
            self.last_enrichment["enriched"] += 1
        return enriched

    def diagnostics(self) -> dict:
        return dict(self.last_diagnostics)


def _first_heading(markdown: str) -> str | None:
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            if heading:
                return heading
        elif stripped:
            break
    return None


def extract_markdown(payload, *, variant: str = "fit") -> tuple[str, str | None]:
    """Pull markdown and a title out of the Crawl4AI response shapes.

    Handles the batch ``/crawl`` envelope (``results[0].markdown`` as raw text or
    as ``{raw_markdown, fit_markdown}``), the single-page ``/md`` shape
    (``{"markdown": "..."}``) and the flat ``fit_markdown``/``raw_markdown``
    variants. Returns ``("", None)`` when nothing usable is present.
    """
    if not isinstance(payload, dict):
        return "", None
    title = None
    if isinstance(payload.get("metadata"), dict):
        title = payload["metadata"].get("title")
    containers = []
    results = payload.get("results")
    if isinstance(results, list) and results and isinstance(results[0], dict):
        containers.append(results[0])
        result_metadata = results[0].get("metadata")
        if isinstance(result_metadata, dict) and result_metadata.get("title"):
            title = result_metadata["title"]
    containers.append(payload)

    for container in containers:
        markdown = container.get("markdown")
        if isinstance(markdown, str) and markdown.strip():
            return markdown, title
        if isinstance(markdown, dict):
            for key in _variant_keys(variant):
                value = markdown.get(key)
                if isinstance(value, str) and value.strip():
                    return value, title
        for key in ("fit_markdown", "raw_markdown", "cleaned_html", "html"):
            value = container.get(key)
            if isinstance(value, str) and value.strip():
                return value, title
    return "", title


def _variant_keys(variant: str) -> tuple[str, ...]:
    if variant == "raw":
        return ("raw_markdown", "fit_markdown")
    return ("fit_markdown", "raw_markdown")
