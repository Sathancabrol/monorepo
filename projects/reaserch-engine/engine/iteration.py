"""Iterative search: search → measure coverage → re-query the gaps → enrich.

The engine's own design principle is *autonomous iteration*: a search round is
only useful if the next round can act on what the previous one revealed. This
module implements that loop around any retriever and returns a JSON-safe report
that also feeds the engine's stopping logic:

    round 1  question + sub-questions
    round 2  gaps: uncovered sub-questions, missing source classes, counter-evidence
    round 3  remaining uncertainty, dataset/institutional angles
    stop     saturation (a round finds nothing new) | max rounds | no query left

Enrichment is not an afterthought: each round ends by running the retriever's
enrichers (OpenAlex completion, Crawl4AI full text) over the merged corpus, which
is what turns a list of snippets into usable data.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .query_strategy import QueryProposal, QueryStrategist, coverage_of_subquestions, normalize_query
from .retrieval import SearchRequest
from .source_identity import corpus_to_dicts, merge_results, unique_domains

DEFAULT_MAX_ROUNDS = 3
DEFAULT_RESULTS_PER_QUERY = 10


@dataclass
class RoundRecord:
    """One search round: what was asked, at what cost, and what it added."""

    index: int
    queries: list[QueryProposal] = field(default_factory=list)
    results_new: int = 0
    results_returned: int = 0
    corpus_size: int = 0
    duplicates_merged: int = 0
    providers: list[dict] = field(default_factory=list)
    failed_providers: list[str] = field(default_factory=list)
    enrichment: list[dict] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def queries_text(self) -> list[str]:
        return [proposal.query for proposal in self.queries]

    def as_dict(self) -> dict:
        return {
            "index": self.index,
            "queries": [proposal.as_dict() for proposal in self.queries],
            "results_new": self.results_new,
            "results_returned": self.results_returned,
            "corpus_size": self.corpus_size,
            "duplicates_merged": self.duplicates_merged,
            "providers": self.providers,
            "failed_providers": self.failed_providers,
            "enrichment": self.enrichment,
            "notes": self.notes,
        }


@dataclass
class SearchIterationReport:
    """Audit-ready account of an iterative search."""

    question: str
    rounds: list[RoundRecord] = field(default_factory=list)
    corpus: list = field(default_factory=list)
    stop_reason: str = "unknown"
    stop_detail: str = ""
    queries_tried: list[str] = field(default_factory=list)
    coverage: dict = field(default_factory=dict)
    metrics: dict = field(default_factory=dict)
    sufficiency_hints: dict = field(default_factory=dict)

    def add_round(self, record: RoundRecord) -> None:
        self.rounds.append(record)

    def as_dict(self) -> dict:
        """JSON-safe report; safe to persist with ``JsonRunStore``."""
        return {
            "question": self.question,
            "stop_reason": self.stop_reason,
            "stop_detail": self.stop_detail,
            "rounds": [record.as_dict() for record in self.rounds],
            "queries_tried": list(self.queries_tried),
            "coverage": dict(self.coverage),
            "metrics": dict(self.metrics),
            "sufficiency_hints": dict(self.sufficiency_hints),
            "corpus": corpus_to_dicts(self.corpus),
        }


class IterativeSearch:
    """Run successive search rounds until the corpus stops growing."""

    def __init__(self, retriever, *,
                 strategist: QueryStrategist | None = None,
                 max_rounds: int = DEFAULT_MAX_ROUNDS,
                 results_per_query: int = DEFAULT_RESULTS_PER_QUERY,
                 max_queries: int | None = None,
                 max_results_total: int | None = None,
                 min_new_per_round: int = 1,
                 recency_days: int | None = None,
                 enrich: bool = True):
        self.retriever = retriever
        self.strategist = strategist or QueryStrategist()
        self.max_rounds = max(1, max_rounds)
        self.results_per_query = max(1, results_per_query)
        self.max_queries = max_queries
        self.max_results_total = max_results_total
        self.min_new_per_round = max(0, min_new_per_round)
        self.recency_days = recency_days
        self.enrich = enrich

    # ── public API ───────────────────────────────────────────────────────────
    def run(self, question: str, *, subquestions=(), source_types=(), seed_queries=()) -> SearchIterationReport:
        report = SearchIterationReport(question=question)
        corpus: list = []
        tried: set[str] = set()
        source_types = list(source_types)
        queries = self.strategist.initial_queries(
            question, subquestions=subquestions, seed_queries=seed_queries)

        for round_index in range(self.max_rounds):
            if not queries:
                report.stop_reason = "queries_exhausted"
                report.stop_detail = "the strategy has no new query to propose"
                break
            record = self._run_round(round_index + 1, queries, report, corpus)
            report.add_round(record)
            tried.update(normalize_query(proposal.query) for proposal in queries)

            if record.results_new < self.min_new_per_round:
                report.stop_reason = "evidence_saturation"
                report.stop_detail = (
                    f"round {record.index} added {record.results_new} new result(s) "
                    f"below the threshold of {self.min_new_per_round}"
                )
                break
            if self.max_queries is not None and len(tried) >= self.max_queries:
                report.stop_reason = "query_budget_exhausted"
                report.stop_detail = f"{len(tried)} distinct queries tried"
                break
            if self.max_results_total is not None and len(corpus) >= self.max_results_total:
                report.stop_reason = "corpus_budget_exhausted"
                report.stop_detail = f"corpus reached {len(corpus)} results"
                break

            coverage = self._coverage(corpus, subquestions, source_types, report.rounds)
            queries = self.strategist.follow_up(
                question=question, round_index=round_index + 1, tried=tried,
                coverage=coverage, subquestions=subquestions, source_types=source_types,
            )
        else:
            report.stop_reason = "max_rounds_reached"
            report.stop_detail = f"{self.max_rounds} rounds completed"

        report.corpus = corpus
        report.queries_tried = sorted(tried)
        report.coverage = self._coverage(corpus, subquestions, source_types, report.rounds)
        report.metrics = self._metrics(corpus, report)
        report.sufficiency_hints = sufficiency_hints(report)
        return report

    # ── internals ────────────────────────────────────────────────────────────
    def _run_round(self, index: int, queries: list[QueryProposal],
                   report: SearchIterationReport, corpus: list) -> RoundRecord:
        record = RoundRecord(index=index, queries=list(queries))
        before = {result.id for result in corpus}
        gathered: list = []
        for proposal in queries:
            request = SearchRequest(
                query=proposal.query,
                subquestion_id=proposal.subquestion_id,
                max_results=self.results_per_query,
                recency_days=self.recency_days,
            )
            results, providers, enrichment = self._search_once(request)
            record.providers.extend(providers)
            record.enrichment.extend(enrichment)
            gathered.extend(results)
            for provider in providers:
                if not provider.get("ok", True) and provider.get("name") not in record.failed_providers:
                    record.failed_providers.append(provider.get("name", "?"))
            if self.max_results_total is not None and len(before) + len(gathered) >= self.max_results_total:
                record.notes.append("corpus budget reached mid-round")
                break

        merge = merge_results([*corpus, *gathered])
        corpus.clear()
        corpus.extend(merge.results)
        record.duplicates_merged = merge.duplicates_merged
        record.corpus_size = len(corpus)
        record.results_returned = len(gathered)
        record.results_new = len({result.id for result in corpus} - before)
        if not gathered:
            record.notes.append("no result returned by any provider this round")
        return record

    def _search_once(self, request: SearchRequest):
        """Use the federated API when available, else the plain protocol."""
        search_with_report = getattr(self.retriever, "search_with_report", None)
        if callable(search_with_report):
            federated = search_with_report(request, enrich=self.enrich)
            return (list(federated.results),
                    [provider.as_dict() for provider in federated.providers],
                    list(federated.enrichment))
        results = list(self.retriever.search(request) or [])
        return results, [], []

    def _coverage(self, corpus, subquestions, source_types, rounds) -> dict:
        coverage = coverage_of_subquestions(corpus, subquestions)
        covered_types = sorted({result.source_type for result in corpus})
        coverage["source_types"] = covered_types
        coverage["missing_source_types"] = [item for item in source_types if item not in covered_types]
        coverage["domains"] = unique_domains(corpus)
        coverage["families"] = sorted({proposal.family for record in rounds for proposal in record.queries})
        return coverage

    def _metrics(self, corpus, report: SearchIterationReport) -> dict:
        by_provider: dict[str, int] = {}
        for result in corpus:
            for name in ((result.metadata or {}).get("providers") or [None]):
                if name:
                    by_provider[name] = by_provider.get(name, 0) + 1
        rounds_used = len(report.rounds)
        yields = [record.results_new for record in report.rounds]
        return {
            "rounds_used": rounds_used,
            "corpus_size": len(corpus),
            "unique_domains": len(unique_domains(corpus)),
            "sources_by_provider": by_provider,
            "sources_by_type": _count_by(corpus, "source_type"),
            "new_results_per_round": yields,
            "yield_last_round": yields[-1] if yields else 0,
            "duplicates_merged": sum(record.duplicates_merged for record in report.rounds),
            "full_text_sources": sum(1 for result in corpus if (result.metadata or {}).get("full_text")),
            "enriched_sources": sum(1 for result in corpus if (result.metadata or {}).get("enriched_by")),
        }


def _count_by(results, attribute: str) -> dict:
    counts: dict[str, int] = {}
    for result in results:
        key = str(getattr(result, attribute, None) or "unknown")
        counts[key] = counts.get(key, 0) + 1
    return counts


def sufficiency_hints(report: SearchIterationReport) -> dict:
    """Translate the iteration outcome into the engine's stopping vocabulary.

    These keys map onto ``engine.sufficiency.SufficiencyInput`` so an agent can
    let the orchestrator decide whether to iterate again, instead of the search
    loop deciding alone.
    """
    hints = {
        "critical_gaps": len(report.coverage.get("uncovered_subquestion_ids") or []),
        "unsearched_high_value_categories": len(report.coverage.get("missing_source_types") or []),
        "evidence_saturation": report.stop_reason == "evidence_saturation",
        "expected_information_gain": float(
            report.metrics.get("yield_last_round") or 0) / max(1, report.metrics.get("corpus_size") or 1),
        "notes": [
            f"stop_reason={report.stop_reason}",
            f"rounds={report.metrics.get('rounds_used', 0)}",
            f"corpus={report.metrics.get('corpus_size', 0)}",
        ],
    }
    if report.stop_reason == "query_budget_exhausted":
        hints["research_cost"] = 1.0
    return hints
