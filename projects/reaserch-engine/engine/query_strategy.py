"""Deterministic query strategy for iterative search.

A research run should not re-ask the same question louder. This module turns the
current epistemic state — covered sub-questions, missing source classes, the fact
that counter-evidence has not been sought yet — into the *next* queries, each
carrying the reason it was generated. The reasons end up in the run report, so a
reader can see why the engine searched what it searched.

Templates are deliberately plain text. An LLM adapter may propose better
queries later, but the baseline must work with no model at all.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
import unicodedata

from .research_strategy import ResearchAction, StrategyState

#: Follow-up families, per language. ``{q}`` is the question and ``{sq}`` a
#: sub-question text.
TEMPLATES = {
    "fr": {
        "define_scope": ("{sq} définition", "définir le périmètre avant de conclure"),
        "state_of_evidence": ("{sq} revue de littérature", "établir l'état des connaissances"),
        "counter_evidence": ("{sq} limites critiques", "chercher activement l'infirmation"),
        "quantify": ("{sq} données chiffrées", "chiffrer plutôt que qualifier"),
        "official_data": ("{sq} données officielles", "remonter à la source institutionnelle"),
        "dataset": ("{sq} jeu de données", "trouver la matière première réutilisable"),
        "field_report": ("{sq} retour de terrain", "ajouter des observations situées"),
        "uncertainty": ("{sq} incertitudes", "cartographier ce qui reste indéterminé"),
    },
    "en": {
        "define_scope": ("{sq} definition", "fix the scope before concluding"),
        "state_of_evidence": ("{sq} literature review", "establish the state of evidence"),
        "counter_evidence": ("{sq} critical limitations", "actively seek disconfirmation"),
        "quantify": ("{sq} quantitative data", "quantify rather than qualify"),
        "official_data": ("{sq} official data", "reach the institutional source"),
        "dataset": ("{sq} dataset", "find reusable raw material"),
        "field_report": ("{sq} field report", "add situated observations"),
        "uncertainty": ("{sq} uncertainty", "map what remains undetermined"),
    },
}

#: Preferred source class -> template family that is most likely to produce it.
SOURCE_CLASS_TEMPLATE = {
    "primary_study": "quantify",
    "systematic_review": "state_of_evidence",
    "meta_analysis": "state_of_evidence",
    "institutional_report": "official_data",
    "academic_book": "state_of_evidence",
    "thesis": "state_of_evidence",
    "secondary_source": "official_data",
    "opinion": "counter_evidence",
    "unverified_web": "official_data",
}

#: The order in which missing coverage is attacked when everything is missing.
FAMILY_PRIORITY = ("define_scope", "state_of_evidence", "quantify",
                   "official_data", "dataset", "counter_evidence",
                   "field_report", "uncertainty")

STOPWORDS = {
    "le", "la", "les", "un", "une", "des", "du", "de", "d", "et", "ou", "que", "qui",
    "quoi", "quel", "quelle", "quels", "quelles", "est", "sont", "pour", "dans", "sur",
    "avec", "sans", "par", "au", "aux", "en", "il", "elle", "on", "ce", "cet", "cette",
    "the", "a", "an", "of", "to", "in", "on", "for", "with", "without", "by", "is",
    "are", "was", "were", "what", "which", "how", "why", "and", "or", "does", "do",
}


@dataclass
class QueryProposal:
    """A query plus the reason it exists (both go into the run report)."""

    query: str
    reason: str
    family: str
    subquestion_id: str | None = None

    def as_dict(self) -> dict:
        return {"query": self.query, "reason": self.reason,
                "family": self.family, "subquestion_id": self.subquestion_id}


@dataclass
class QueryStrategist:
    """Turn question + coverage state into the next round of queries."""

    language: str = "fr"
    max_queries_per_round: int = 3
    template_families: tuple[str, ...] = FAMILY_PRIORITY
    extra_templates: dict = field(default_factory=dict)

    def templates(self) -> dict:
        base = dict(TEMPLATES.get(self.language) or TEMPLATES["en"])
        base.update(self.extra_templates or {})
        return base

    # ── round 0 ──────────────────────────────────────────────────────────────
    def initial_queries(self, question: str, *, subquestions=(), seed_queries=()) -> list[QueryProposal]:
        """Open the investigation: the question itself, then its sub-questions."""
        proposals = [QueryProposal(text, "open the investigation", "question") for text in seed_queries]
        proposals.append(QueryProposal(question.strip(), "verbatim research question", "question"))
        for subquestion in _iter_subquestions(subquestions):
            proposals.append(QueryProposal(
                subquestion["text"], f"planned sub-question {subquestion['id']}", "subquestion",
                subquestion_id=subquestion["id"],
            ))
        return _dedupe(proposals)[:max(1, self.max_queries_per_round)]

    # ── round n ──────────────────────────────────────────────────────────────
    def follow_up(self, *, question: str, round_index: int, tried: set[str],
                  coverage: dict, subquestions=(), source_types=()) -> list[QueryProposal]:
        """Propose the next queries from gaps actually observed in the corpus."""
        templates = self.templates()
        proposals: list[QueryProposal] = []
        uncovered = [subquestion for subquestion in _iter_subquestions(subquestions)
                     if subquestion["id"] in set(coverage.get("uncovered_subquestion_ids") or [])]
        focus = uncovered or _iter_subquestions(subquestions) or [{"id": None, "text": question}]

        # 1. unanswered sub-questions first: they are the stated objectives.
        for subquestion in focus[:2]:
            for family in ("define_scope", "state_of_evidence"):
                proposals.append(self._propose(templates, family, subquestion, question,
                                               "sub-question without any matching evidence"))

        # 2. missing source classes: coverage bias is a methodological defect.
        covered_types = set(coverage.get("source_types") or [])
        for source_type in source_types:
            if source_type in covered_types:
                continue
            family = SOURCE_CLASS_TEMPLATE.get(source_type)
            if not family:
                continue
            proposals.append(self._propose(templates, family, focus[0], question,
                                           f"source class not covered yet: {source_type}",
                                           family_override=family))

        # 3. counter-evidence and uncertainty: always, from round 2 onwards.
        if round_index >= 1:
            proposals.append(self._propose(templates, "counter_evidence", focus[0], question,
                                           "seek disconfirming evidence (Phase 9)"))
        if round_index >= 2:
            proposals.append(self._propose(templates, "uncertainty", focus[0], question,
                                           "characterize what remains unknown"))

        # 4. nothing else left: push the least-covered planned family.
        if not proposals:
            planned = [family for family in self.template_families if family in templates]
            used_families = set(coverage.get("families") or [])
            for family in planned:
                if family not in used_families:
                    proposals.append(self._propose(templates, family, focus[0], question,
                                                   "planned search family not attempted yet"))
                    break

        fresh = _dedupe(proposals, tried=tried)
        return fresh[:max(1, self.max_queries_per_round)]

    # ── strategy bridge ──────────────────────────────────────────────────────
    def actions_from_state(self, state: StrategyState) -> list[ResearchAction]:
        """Reuse the engine's strategy engine to rank *what* to research next."""
        from .research_strategy import ResearchStrategyEngine
        return ResearchStrategyEngine().next_actions(state)

    def _propose(self, templates: dict, family: str, subquestion: dict, question: str,
                 reason: str, *, family_override: str | None = None) -> QueryProposal:
        key = family_override or family
        template = templates.get(key)
        target = subquestion.get("text") or question
        if not template:
            query = f"{target} {key}"
        else:
            pattern, family_reason = template
            query = pattern.format(q=target, sq=target)
            reason = f"{reason} — {family_reason}"
        return QueryProposal(query.strip(), reason, key,
                             subquestion_id=subquestion.get("id"))


def _iter_subquestions(subquestions) -> list[dict]:
    """Accept planner ``SubQuestion`` objects, dicts, or plain strings."""
    normalized = []
    for index, item in enumerate(subquestions or [], start=1):
        if item is None:
            continue
        if isinstance(item, str):
            text = item.strip()
            if text:
                normalized.append({"id": f"sq{index}", "text": text})
            continue
        text = getattr(item, "text", None) or (item.get("text") if isinstance(item, dict) else None)
        if not text:
            continue
        identifier = getattr(item, "id", None) or (item.get("id") if isinstance(item, dict) else None) or f"sq{index}"
        source_types = getattr(item, "source_types", None) or (item.get("source_types") if isinstance(item, dict) else None) or []
        normalized.append({"id": identifier, "text": str(text).strip(), "source_types": list(source_types)})
    return normalized


def _dedupe(proposals: list[QueryProposal], *, tried: set[str] | None = None) -> list[QueryProposal]:
    seen = {normalize_query(query) for query in (tried or set())}
    out: list[QueryProposal] = []
    for proposal in proposals:
        key = normalize_query(proposal.query)
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(proposal)
    return out


def normalize_query(query: str) -> str:
    """Case/accent-insensitive query key, so 'Données' and 'donnees' don't repeat."""
    if not query:
        return ""
    decomposed = unicodedata.normalize("NFKD", query)
    ascii_ish = "".join(char for char in decomposed if not unicodedata.combining(char))
    return " ".join(re.sub(r"[^0-9a-z]+", " ", ascii_ish.casefold()).split())


def significant_terms(text: str) -> set[str]:
    """Content words used for the (deliberately simple) coverage heuristic."""
    return {term for term in normalize_query(text).split() if term not in STOPWORDS and len(term) > 2}


def coverage_of_subquestions(results, subquestions, *, min_overlap: int = 2) -> dict:
    """Report which planned sub-questions the corpus actually addresses.

    The heuristic is transparent on purpose: a sub-question counts as covered
    when at least ``min_overlap`` of its content words appear in one result
    (title + snippet). It is a coverage signal for planning, never a claim of
    completeness.
    """
    subquestions = _iter_subquestions(subquestions)
    haystacks = [
        f"{getattr(result, 'title', '')} {getattr(result, 'snippet', '')}" for result in results
    ]
    covered, uncovered, hits = [], [], {}
    for subquestion in subquestions:
        terms = significant_terms(subquestion["text"])
        matching = sum(
            1 for haystack in haystacks
            if len(terms & significant_terms(haystack)) >= min_overlap
        )
        hits[subquestion["id"]] = matching
        (covered if matching else uncovered).append(subquestion["id"])
    return {
        "covered_subquestion_ids": covered,
        "uncovered_subquestion_ids": uncovered,
        "subquestion_hits": hits,
    }
