"""Stable identities for retrieved sources: de-duplication and provenance-safe merging.

Several providers routinely return the same work: Crossref and OpenAlex share
DOIs, SearXNG and OpenAlex can point at the same landing page, and mirrors
repeat the same title. The engine keeps one record per work and records the
merge instead of showing the analyst duplicated evidence.

Identity keys are ordered by reliability: DOI, then canonical URL, then
normalized title. Merging never drops provenance: every provider that carried
the record stays listed in ``metadata["providers"]``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
import unicodedata
from typing import Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

#: Query parameters that never change which document a URL points at.
TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "utm_id", "gclid", "fbclid", "msclkid", "mc_cid", "mc_eid", "igshid",
    "ref", "ref_src", "referrer", "source", "spm", "yclid", "_hsenc",
    "_hsmi", "vero_id", "wickedid", "oly_anon_id", "oly_enc_id", "trk",
}

_DOI_PATH_RE = re.compile(r"^10\.\d{4,9}/\S+$")
_DOI_PREFIXES = ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/",
                 "http://dx.doi.org/", "doi:", "info:doi/")
_TRAILING_JUNK = " \t\r\n.,;:)]}>'\""
#: Short titles ("Home", "Résumé") are too generic to merge on.
MIN_TITLE_LENGTH = 12

#: How informative a source type is. Merging keeps the most specific one so an
#: OpenAlex "primary_study" is not lost behind a generic Crossref placeholder.
SOURCE_TYPE_SPECIFICITY = {
    "": 0, "unknown": 0, "unverified_web": 0,
    "academic_record": 1,
    "secondary_source": 2, "opinion": 2,
    "institutional_report": 3, "academic_book": 3, "thesis": 3,
    "primary_study": 4, "systematic_review": 4, "meta_analysis": 4,
}


def normalize_doi(value: str | None) -> str | None:
    """Return a bare lowercase DOI (``10.1000/xyz``) or ``None``."""
    if not value:
        return None
    cleaned = value.strip().strip("<>").strip()
    low = cleaned.lower()
    for prefix in _DOI_PREFIXES:
        if low.startswith(prefix):
            cleaned = cleaned[len(prefix):]
            break
    cleaned = cleaned.strip().rstrip(_TRAILING_JUNK).lower()
    return cleaned if _DOI_PATH_RE.match(cleaned) else None


def canonical_url(url: str | None) -> str | None:
    """Normalize a URL enough to compare two links to the same document.

    Scheme and host are lowercased, the fragment and tracking parameters are
    removed, the remaining query is sorted, and a trailing slash is dropped.
    """
    if not url or not url.strip():
        return None
    raw = url.strip()
    if "://" not in raw:
        raw = f"https://{raw}"
    parts = urlsplit(raw)
    if not parts.netloc:
        return None
    scheme = (parts.scheme or "https").lower()
    host = parts.netloc.lower().rstrip(".")
    if host.endswith(":80") and scheme == "http":
        host = host[:-3]
    if host.endswith(":443") and scheme == "https":
        host = host[:-4]
    path = parts.path or ""
    if path.endswith("/") and len(path) > 1:
        path = path.rstrip("/")
    query = urlencode(sorted(
        (key, value) for key, value in parse_qsl(parts.query, keep_blank_values=False)
        if key.lower() not in TRACKING_PARAMS
    ))
    return urlunsplit((scheme, host, path, query, ""))


def normalize_title(title: str | None) -> str | None:
    """Normalize a title for comparison, or ``None`` when it is too generic."""
    if not title:
        return None
    decomposed = unicodedata.normalize("NFKD", title)
    ascii_ish = "".join(char for char in decomposed if not unicodedata.combining(char))
    cleaned = re.sub(r"[^0-9a-z]+", " ", ascii_ish.casefold())
    cleaned = " ".join(cleaned.split())
    return cleaned if len(cleaned) >= MIN_TITLE_LENGTH else None


def identity_keys(result) -> list[str]:
    """Candidate identity keys for a result, most reliable first."""
    metadata = getattr(result, "metadata", None) or {}
    keys: list[str] = []
    doi = normalize_doi(metadata.get("doi"))
    if doi:
        keys.append(f"doi:{doi}")
    url = canonical_url(getattr(result, "url", None))
    if url:
        keys.append(f"url:{url}")
    title = normalize_title(getattr(result, "title", None))
    if title:
        keys.append(f"title:{title}")
    return keys


def _provider_of(result) -> str | None:
    metadata = getattr(result, "metadata", None) or {}
    provider = metadata.get("provider")
    return provider if isinstance(provider, str) and provider else None


def _ranks(metadata: dict) -> dict:
    """Best-seen rank per provider, including the record's own rank field."""
    ranks = dict(metadata.get("provider_ranks") or {})
    provider = _provider_of_metadata(metadata)
    rank = metadata.get("rank")
    if provider and isinstance(rank, int) and (provider not in ranks or rank < ranks[provider]):
        ranks[provider] = rank
    return ranks


def _merge_metadata(primary: dict, extra: dict) -> dict:
    merged = dict(primary)
    for key, value in extra.items():
        if key == "providers":
            continue
        if key == "provider_ranks":
            ranks = dict(merged.get("provider_ranks") or {})
            for name, rank in (value or {}).items():
                if name not in ranks or (isinstance(rank, int) and rank < ranks[name]):
                    ranks[name] = rank
            merged["provider_ranks"] = ranks
            continue
        if key == "merged_from":
            merged["merged_from"] = list(dict.fromkeys(list(merged.get("merged_from") or []) + list(value or [])))
            continue
        if key == "enriched_by":
            merged["enriched_by"] = list(dict.fromkeys(list(merged.get("enriched_by") or []) + list(value or [])))
            continue
        current = merged.get(key)
        if current in (None, "", [], {}) and value not in (None, "", [], {}):
            merged[key] = value
        elif key == "citation_count" and isinstance(value, int) and isinstance(current, int):
            merged[key] = max(current, value)
    names = {name for name in [*list(primary.get("providers") or []), *list(extra.get("providers") or []),
                               _provider_of_metadata(primary), _provider_of_metadata(extra)] if name}
    if names:
        merged["providers"] = sorted(names)
    ranks = _ranks(primary)
    for name, rank in _ranks(extra).items():
        if name not in ranks or rank < ranks[name]:
            ranks[name] = rank
    if ranks:
        merged["provider_ranks"] = ranks
    return merged


def _provider_of_metadata(metadata: dict) -> str | None:
    provider = metadata.get("provider")
    return provider if isinstance(provider, str) and provider else None


def merge_into(primary, extra):
    """Fold ``extra`` into ``primary`` without losing provenance.

    The richer snippet wins (full text over an abstraction over a meta
    description), missing fields are filled, and metadata is merged. The
    original ids of both records are kept in ``metadata["merged_from"]``.
    """
    metadata = _merge_metadata(primary.metadata or {}, extra.metadata or {})
    extra_provider = _provider_of(extra)
    if extra_provider:
        metadata.setdefault("provider_ranks", {})
        rank = (extra.metadata or {}).get("rank")
        if isinstance(rank, int):
            current = metadata["provider_ranks"].get(extra_provider)
            if current is None or rank < current:
                metadata["provider_ranks"][extra_provider] = rank
        names = set(metadata.get("providers") or [])
        names.update(name for name in (metadata.get("provider"), extra_provider) if name)
        metadata["providers"] = sorted(names)
    merged_from = list(metadata.get("merged_from") or [])
    for candidate in (primary.id, extra.id):
        if candidate and candidate not in merged_from:
            merged_from.append(candidate)
    metadata["merged_from"] = merged_from

    snippet = primary.snippet or ""
    if len(extra.snippet or "") > len(snippet):
        snippet = extra.snippet
    source_type = primary.source_type
    if (SOURCE_TYPE_SPECIFICITY.get(extra.source_type, 0)
            > SOURCE_TYPE_SPECIFICITY.get(source_type, 0)):
        source_type = extra.source_type
    return type(primary)(
        id=primary.id,
        title=primary.title or extra.title,
        url=primary.url or extra.url,
        snippet=snippet,
        source_type=source_type,
        metadata=metadata,
    )


@dataclass
class MergeOutcome:
    results: list = field(default_factory=list)
    duplicates_merged: int = 0
    #: identity key -> ids of the records that were merged under it
    groups: dict[str, list[str]] = field(default_factory=dict)


def merge_results(results: Iterable) -> MergeOutcome:
    """De-duplicate a result list, preserving first-seen order."""
    outcome = MergeOutcome()
    index: dict[str, int] = {}
    for result in results:
        keys = identity_keys(result)
        position = next((index[key] for key in keys if key in index), None)
        if position is None:
            outcome.results.append(result)
            position = len(outcome.results) - 1
            for key in keys:
                index.setdefault(key, position)
            continue
        keeper = outcome.results[position]
        outcome.results[position] = merge_into(keeper, result)
        outcome.duplicates_merged += 1
        for key in keys:
            index.setdefault(key, position)
        for key in keys:
            outcome.groups.setdefault(key, []).append(keeper.id)
            outcome.groups[key].append(result.id)
    return outcome


def result_to_dict(result) -> dict:
    """JSON-safe projection of a search result (used by reports and dossiers)."""
    return {
        "id": result.id,
        "title": result.title,
        "url": result.url,
        "snippet": result.snippet,
        "source_type": result.source_type,
        "metadata": dict(result.metadata or {}),
    }


def corpus_to_dicts(results: Iterable) -> list[dict]:
    return [result_to_dict(result) for result in results]


def unique_domains(results: Iterable) -> list[str]:
    """Distinct registrable-ish hosts, for coverage reporting."""
    domains = set()
    for result in results:
        url = canonical_url(getattr(result, "url", None))
        if not url:
            continue
        host = urlsplit(url).netloc
        domains.add(host[4:] if host.startswith("www.") else host)
    return sorted(domains)
