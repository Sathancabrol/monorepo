"""Unit tests for HCSM V1 schema + V5 admissibility."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from hcsm_validate.admissibility import assess_admissibility, assess_bundle_requests
from hcsm_validate.ontology import Ontology
from hcsm_validate.schema import validate_bundle, validate_object

CASES = ROOT / "cases"
ONTO = Ontology()


def _load(rel: str) -> dict:
    path = CASES / rel
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    data.pop("_meta", None)
    return data


# ---------------------------------------------------------------------------
# Ontology
# ---------------------------------------------------------------------------


def test_ontology_loads():
    assert ONTO.version == "0.1.0"
    assert ONTO.is_known_construct("hcsm:knowledge/construct/attention")
    assert ONTO.is_known_construct("attention")
    assert not ONTO.is_known_construct("dsm5:ADHD")
    assert "fatigue" in ONTO.mandatory_alternatives("attention")
    assert "task" in ONTO.requires_context("attention")


def test_diagnostic_detection():
    assert Ontology.is_diagnostic_target("dsm5:ADHD")
    assert Ontology.is_diagnostic_target("icd11:6A05")
    assert not Ontology.is_diagnostic_target("hcsm:knowledge/construct/attention")


def test_digital_feature_detection():
    assert Ontology.is_digital_feature_as_construct("screen_time_attention")
    assert not Ontology.is_digital_feature_as_construct(
        "hcsm:knowledge/construct/attention"
    )


# ---------------------------------------------------------------------------
# V1 — valid forms
# ---------------------------------------------------------------------------


def test_valid_construct_estimate():
    obj = _load("valid/construct_estimate_complete.json")
    r = validate_object(obj, ONTO)
    assert r.ok, r.summary()


def test_valid_refusal():
    obj = _load("valid/refusal_no_evidence.json")
    r = validate_object(obj, ONTO)
    assert r.ok, r.summary()


def test_valid_observation():
    obj = _load("valid/observation_only.json")
    r = validate_object(obj, ONTO)
    assert r.ok, r.summary()


def test_valid_functional_projection():
    obj = _load("valid/functional_projection_hypothesis.json")
    r = validate_object(obj, ONTO)
    assert r.ok, r.summary()


def test_valid_mini_scenario_bundle():
    bundle = _load("valid/mini_scenario_attention.json")
    r = validate_bundle(bundle, ONTO)
    assert r.ok, r.summary()


# ---------------------------------------------------------------------------
# V1 — illegal forms
# ---------------------------------------------------------------------------


def test_reject_naked_score():
    obj = _load("invalid/naked_score.json")
    r = validate_object(obj, ONTO)
    assert not r.ok
    assert any(i.code == "V1-NAKED-SCORE" for i in r.issues)


def test_reject_observation_as_construct():
    obj = _load("invalid/observation_as_construct.json")
    r = validate_object(obj, ONTO)
    assert not r.ok
    assert any(i.code == "V1-OBS-ESTIMATE-FIELD" for i in r.issues)


def test_reject_missing_uncertainty():
    obj = _load("invalid/estimate_without_uncertainty.json")
    r = validate_object(obj, ONTO)
    assert not r.ok
    assert any("UNCERTAINTY" in i.code for i in r.issues)


def test_reject_missing_evidence():
    obj = _load("invalid/estimate_without_evidence.json")
    r = validate_object(obj, ONTO)
    assert not r.ok
    assert any("EVIDENCE" in i.code for i in r.issues)


def test_reject_windowless():
    obj = _load("invalid/windowless_t0.json")
    r = validate_object(obj, ONTO)
    assert not r.ok
    assert any(i.code == "V1-WINDOW" for i in r.issues)


def test_reject_refusal_with_value():
    obj = _load("invalid/refusal_with_default_value.json")
    r = validate_object(obj, ONTO)
    assert not r.ok
    assert any(i.code == "V1-REFUSAL-HAS-VALUE" for i in r.issues)


def test_reject_fp_as_fact():
    obj = _load("invalid/functional_projection_as_fact.json")
    r = validate_object(obj, ONTO)
    assert not r.ok
    assert any(i.code == "V1-FP-STATUS" for i in r.issues)


def test_reject_diagnostic_target():
    obj = _load("invalid/diagnostic_target.json")
    r = validate_object(obj, ONTO)
    assert not r.ok
    assert any(i.code == "V1-DIAGNOSTIC-TARGET" for i in r.issues)


def test_reject_digital_as_construct():
    obj = _load("invalid/digital_feature_as_cognition.json")
    r = validate_object(obj, ONTO)
    assert not r.ok
    assert any(i.code == "V1-DIGITAL-AS-CONSTRUCT" for i in r.issues)


def test_reject_pii():
    obj = _load("invalid/pii_in_person.json")
    r = validate_object(obj, ONTO)
    assert not r.ok
    assert any(i.code == "V1-PII" for i in r.issues)


# ---------------------------------------------------------------------------
# V5 — admissibility
# ---------------------------------------------------------------------------


def test_admit_attention():
    bundle = _load("valid/admit_attention_request.json")
    results = assess_bundle_requests(bundle, ONTO)
    assert len(results) == 1
    assert results[0].admissible, results[0].message


def test_refuse_no_construct():
    bundle = _load("invalid/refuse_no_construct.json")
    results = assess_bundle_requests(bundle, ONTO)
    assert len(results) == 1
    assert not results[0].admissible
    assert results[0].refusal_code == "NO_CONSTRUCT"


def test_refuse_no_evidence():
    bundle = _load("invalid/refuse_no_evidence.json")
    results = assess_bundle_requests(bundle, ONTO)
    assert not results[0].admissible
    assert results[0].refusal_code == "NO_EVIDENCE"


def test_refuse_window_undefined():
    bundle = _load("invalid/refuse_window_undefined.json")
    results = assess_bundle_requests(bundle, ONTO)
    assert not results[0].admissible
    assert results[0].refusal_code == "WINDOW_UNDEFINED"


def test_refuse_context_missing():
    bundle = _load("invalid/refuse_context_missing.json")
    results = assess_bundle_requests(bundle, ONTO)
    assert not results[0].admissible
    assert results[0].refusal_code == "CONTEXT_MISSING"


def test_refuse_unresolved_alternatives():
    bundle = _load("invalid/refuse_unresolved_alternatives.json")
    results = assess_bundle_requests(bundle, ONTO)
    assert not results[0].admissible
    assert results[0].refusal_code == "UNRESOLVED_ALTERNATIVES"


def test_refuse_misaligned():
    bundle = _load("invalid/refuse_misaligned_measure.json")
    results = assess_bundle_requests(bundle, ONTO)
    assert not results[0].admissible
    assert results[0].refusal_code == "MISALIGNED_MEASURE"


def test_refuse_provenance_broken():
    bundle = _load("invalid/refuse_provenance_broken.json")
    results = assess_bundle_requests(bundle, ONTO)
    assert not results[0].admissible
    assert results[0].refusal_code == "PROVENANCE_BROKEN"


def test_mini_scenario_attention_admissible_wm_not_in_ce():
    """ConstructEstimate in mini scenario should be admissible under V5."""
    bundle = _load("valid/mini_scenario_attention.json")
    results = assess_bundle_requests(bundle, ONTO)
    # only ConstructEstimate objects are re-checked
    assert any(r.admissible for r in results)
    att = [r for r in results if r.construct_id and "attention" in r.construct_id]
    assert att and att[0].admissible


# ---------------------------------------------------------------------------
# Contract invariants
# ---------------------------------------------------------------------------


def test_refusal_is_not_an_estimate():
    """A Refusal object must never validate if it carries value."""
    bad = {
        "id": "r1",
        "type": "Refusal",
        "insufficient_for": "hcsm:knowledge/construct/attention",
        "about_person": "person:opaque:px",
        "code": "NO_EVIDENCE",
        "message": "x",
        "value": 0.0,
        "has_provenance": {
            "activity_type": "InferenceActivity",
            "started_at": "2026-08-25T00:00:00Z",
            "associated_agent": "agent:x",
        },
    }
    r = validate_object(bad, ONTO)
    assert not r.ok


def test_direct_admissibility_api():
    req = {
        "construct": "hcsm:knowledge/construct/attention",
        "has_window": {"center": "2026-08-25T09:40:00Z", "half_width": 30, "unit": "min"},
        "has_context": {
            "completeness": "declared_unknown",
            "of_person": "person:opaque:px",
        },
        "inferred_from": [
            {
                "type": "Observation",
                "id": "o1",
                "alignment": "exact",
                "quality_flag": "ok",
                "has_provenance": {
                    "activity_type": "MeasureActivity",
                    "started_at": "2026-08-25T09:00:00Z",
                    "associated_agent": "agent:x",
                },
            }
        ],
        "alternatives": [
            {"modulator": "fatigue"},
            {"modulator": "arousal"},
            {"modulator": "motivation"},
            {"modulator": "task_difficulty"},
            {"modulator": "sleep_pressure"},
        ],
        "has_provenance": {
            "activity_type": "InferenceActivity",
            "started_at": "2026-08-25T09:50:00Z",
            "associated_agent": "agent:x",
        },
    }
    result = assess_admissibility(req, ONTO)
    assert result.admissible, result.message
