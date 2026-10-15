from engine.planner import SubQuestion
from engine.query_strategy import (
    QueryStrategist, coverage_of_subquestions, normalize_query, significant_terms,
)

SUBQUESTIONS = [
    {"id": "sq1", "text": "Que mesurent les capteurs du port", "source_types": ["institutional_report"]},
    {"id": "sq2", "text": "Quelles preuves relient les navires aux particules"},
]


def test_initial_queries_open_with_the_question_then_the_subquestions():
    strategist = QueryStrategist(language="fr", max_queries_per_round=6)
    proposals = strategist.initial_queries("Effet du trafic maritime", subquestions=SUBQUESTIONS)

    assert [proposal.family for proposal in proposals] == ["question", "subquestion", "subquestion"]
    assert proposals[0].query == "Effet du trafic maritime"
    assert proposals[1].subquestion_id == "sq1"


def test_follow_up_targets_uncovered_subquestions_and_missing_source_classes():
    strategist = QueryStrategist(language="fr", max_queries_per_round=6)
    proposals = strategist.follow_up(
        question="Effet du trafic maritime",
        round_index=1,
        tried=set(),
        coverage={"uncovered_subquestion_ids": ["sq1"], "source_types": ["unverified_web"]},
        subquestions=SUBQUESTIONS,
        source_types=["institutional_report"],
    )
    families = [proposal.family for proposal in proposals]

    assert families == ["define_scope", "state_of_evidence", "official_data", "counter_evidence"]
    assert proposals[0].subquestion_id == "sq1"
    assert any("source class not covered yet: institutional_report" in proposal.reason
               for proposal in proposals)
    assert any("confirmer" in proposal.reason or "désinformation" in proposal.reason
               or "infirmation" in proposal.reason for proposal in proposals)


def test_follow_up_never_repeats_a_query_already_tried():
    strategist = QueryStrategist(language="fr", max_queries_per_round=6)
    first = strategist.follow_up(question="Q", round_index=1, tried=set(),
                                 coverage={}, subquestions=[], source_types=[])
    tried = {proposal.query for proposal in first}
    second = strategist.follow_up(question="Q", round_index=1, tried=tried,
                                  coverage={}, subquestions=[], source_types=[])

    assert tried.isdisjoint({proposal.query for proposal in second})


def test_english_templates_and_planner_objects_are_supported():
    strategist = QueryStrategist(language="en", max_queries_per_round=3)
    proposals = strategist.follow_up(
        question="Shipping and air quality",
        round_index=1,
        tried=set(),
        coverage={},
        subquestions=[SubQuestion("sq9", "What do harbour sensors measure?", "define_scope")],
        source_types=[],
    )

    assert proposals[0].query == "What do harbour sensors measure? definition"
    assert any(proposal.query.endswith("critical limitations") for proposal in proposals)


def test_coverage_heuristic_reports_what_the_corpus_does_not_address():
    class Doc:
        title = "Mesures des capteurs du port de Sète"
        snippet = "Les capteurs mesurent les particules fines."

    coverage = coverage_of_subquestions([Doc()], SUBQUESTIONS)

    assert coverage["covered_subquestion_ids"] == ["sq1"]
    assert coverage["uncovered_subquestion_ids"] == ["sq2"]
    assert coverage["subquestion_hits"] == {"sq1": 1, "sq2": 0}


def test_query_normalization_and_stopwords_are_shared_with_the_loop():
    assert normalize_query("Données  Officielles !") == "donnees officielles"
    assert significant_terms("Quel est l'effet du trafic maritime") == {"effet", "trafic", "maritime"}
