"""Federated retrieval: fan-out, per-provider isolation, de-duplication, enrichment.

One research question is rarely answered by one provider. This layer runs every
configured provider, keeps the run alive when one of them is down, merges the
duplicates they return, and records what happened per provider so the run stays
auditable.

Order is deterministic: providers are interleaved round-robin (weighted, then
alphabetical), and de-duplication keeps the first record it meets while folding
the later copies into it. Two runs on the same corpus therefore produce the same
list — a prerequisite for reproducible research.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .providers import RetrievalProvider
from .retrieval import SearchRequest
from .source_identity import MergeOutcome, corpus_to_dicts, merge_results


@dataclass
class ProviderReport:
    """What one provider did during one federated search."""

    name: str
    returned: int = 0
    skipped: int = 0
    error: str | None = None
    diagnostics: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.error is None

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "returned": self.returned,
            "skipped": self.skipped,
            "ok": self.ok,
            "error": self.error,
            "diagnostics": self.diagnostics,
        }


@dataclass
class FederatedSearch:
    """Result of one federated search, including its own audit trail."""

    query: str
    results: list = field(default_factory=list)
    corpus_size: int = 0
    duplicates_merged: int = 0
    providers: list[ProviderReport] = field(default_factory=list)
    enrichment: list[dict] = field(default_factory=list)
    merge_groups: dict[str, list[str]] = field(default_factory=dict)

    @property
    def failed_providers(self) -> list[str]:
        return [report.name for report in self.providers if not report.ok]

    def as_dict(self) -> dict:
        return {
            "query": self.query,
            "corpus_size": self.corpus_size,
            "returned": len(self.results),
            "duplicates_merged": self.duplicates_merged,
            "providers": [report.as_dict() for report in self.providers],
            "failed_providers": self.failed_providers,
            "enrichment": self.enrichment,
            "merge_groups": {key: ids for key, ids in self.merge_groups.items()},
        }


class FederatedRetriever:
    """A ``Retriever`` that combines several providers behind one interface.

    ``search_with_report`` returns the corpus **and** the audit trail;
    ``search`` keeps the protocol signature and stores the same report on
    ``last_report`` for callers that only need the list.
    """

    def __init__(self, providers: Iterable, *,
                 weights: dict[str, float] | None = None,
                 per_provider_max: int | None = None,
                 interleave: bool = True,
                 enrichers: Iterable | None = None,
                 clock=None):
        self.providers: dict[str, object] = _normalize_providers(providers)
        self.weights = dict(weights or {})
        self.per_provider_max = per_provider_max
        self.interleave = interleave
        self.enrichers = list(enrichers or [])
        self.clock = clock
        self.last_report: FederatedSearch | None = None

    # ── public API ───────────────────────────────────────────────────────────
    def provider_names(self) -> list[str]:
        return list(self.providers)

    def search(self, request: SearchRequest) -> list:
        return self.search_with_report(request).results

    def search_with_report(self, request: SearchRequest, *, enrich: bool = True) -> FederatedSearch:
        reports: list[ProviderReport] = []
        gathered: list[tuple[str, list]] = []
        for name, retriever in self.providers.items():
            report, results = self._run_provider(name, retriever, request)
            reports.append(report)
            if results:
                gathered.append((name, results))

        ordered = self._interleave(gathered) if self.interleave else [item for _, batch in gathered for item in batch]
        merge: MergeOutcome = merge_results(ordered)
        search = FederatedSearch(
            query=request.query,
            results=merge.results,
            corpus_size=len(merge.results),
            duplicates_merged=merge.duplicates_merged,
            providers=reports,
            merge_groups=merge.groups,
        )
        if enrich:
            search.results = self._enrich(search.results, search)
        limit = request.max_results or len(search.results)
        search.results = search.results[:limit]
        self.last_report = search
        return search

    # ── internals ────────────────────────────────────────────────────────────
    def _run_provider(self, name: str, retriever, request: SearchRequest) -> tuple[ProviderReport, list]:
        report = ProviderReport(name=name)
        provider_request = _request_for(request, self.per_provider_max)
        try:
            results = list(retriever.search(provider_request) or [])
        except Exception as exc:  # noqa: BLE001 - a dead provider must not kill the run
            report.error = f"{type(exc).__name__}: {exc}"
            return report, []
        report.returned = len(results)
        diagnostics = getattr(retriever, "diagnostics", None)
        if callable(diagnostics):
            try:
                report.diagnostics = dict(diagnostics() or {})
            except Exception:  # noqa: BLE001 - diagnostics are optional
                report.diagnostics = {}
        report.skipped = int(report.diagnostics.get("skipped") or 0)
        for position, result in enumerate(results, start=1):
            metadata = dict(getattr(result, "metadata", None) or {})
            metadata.setdefault("provider", name)
            metadata.setdefault("rank", position)
            names = set(metadata.get("providers") or [])
            names.add(name)
            metadata["providers"] = sorted(names)
            result.metadata = metadata
        return report, results

    def _interleave(self, batches: list[tuple[str, list]]) -> list:
        order = sorted(range(len(batches)),
                       key=lambda index: (-self.weights.get(batches[index][0], 0.0), batches[index][0]))
        ordered: list = []
        for depth in range(max((len(batch) for _, batch in batches), default=0)):
            for index in order:
                name, batch = batches[index]
                if depth < len(batch):
                    ordered.append(batch[depth])
        return ordered

    def _enrich(self, results: list, search: FederatedSearch) -> list:
        for enricher in self.enrichers:
            try:
                results = list(enricher.enrich(results) or [])
            except Exception as exc:  # noqa: BLE001 - enrichment is best-effort
                search.enrichment.append({"provider": getattr(enricher, "name", type(enricher).__name__),
                                          "error": f"{type(exc).__name__}: {exc}"})
                continue
            summary = getattr(enricher, "last_enrichment", None)
            if isinstance(summary, dict):
                search.enrichment.append(dict(summary))
        return results

    def corpus(self) -> list[dict]:
        """JSON-safe view of the last corpus (for reports and dossiers)."""
        return corpus_to_dicts(self.last_report.results) if self.last_report else []


def _normalize_providers(providers: Iterable) -> dict[str, object]:
    if isinstance(providers, dict):
        return dict(providers)
    normalized: dict[str, object] = {}
    for entry in providers:
        if isinstance(entry, RetrievalProvider):
            normalized[entry.name] = entry.retriever
            continue
        try:
            name, retriever = entry  # (name, retriever) pairs
        except (TypeError, ValueError) as exc:
            raise TypeError("providers must be a mapping or (name, retriever) pairs") from exc
        normalized[str(name)] = retriever
    return normalized


def _request_for(request: SearchRequest, cap: int | None) -> SearchRequest:
    if not cap:
        return request
    return SearchRequest(
        query=request.query,
        subquestion_id=request.subquestion_id,
        source_types=list(request.source_types),
        max_results=cap,
        recency_days=request.recency_days,
        metadata=dict(request.metadata or {}),
    )
