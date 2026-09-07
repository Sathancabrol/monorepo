"""V5 — admissibility filter before any numeric estimation.

Returns whether Inference may produce a ConstructEstimate, or must Refusal.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .ontology import Ontology


@dataclass
class AdmissibilityResult:
    admissible: bool
    refusal_code: str | None = None
    message: str = ""
    construct_id: str | None = None
    checks: list[dict[str, Any]] = field(default_factory=list)

    def as_refusal_stub(
        self,
        *,
        person_id: str = "person:opaque:px",
        window: dict[str, Any] | None = None,
        provenance_id: str = "prov:refusal_auto",
    ) -> dict[str, Any]:
        """Build a minimal Refusal object (still needs V1 validation of provenance detail)."""
        return {
            "id": f"hcsm:inference/refusal/auto_{self.refusal_code or 'UNKNOWN'}",
            "type": "Refusal",
            "insufficient_for": self.construct_id,
            "about_person": person_id,
            "code": self.refusal_code or "NO_EVIDENCE",
            "message": self.message,
            "has_window": window,
            "has_provenance": provenance_id,
        }


def _index_bundle(objects: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    idx: dict[str, dict[str, Any]] = {}
    for o in objects:
        oid = o.get("id")
        if oid:
            idx[str(oid)] = o
    return idx


def _resolve(ref: Any, index: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    if isinstance(ref, dict):
        return ref
    if isinstance(ref, str) and ref in index:
        return index[ref]
    return None


def _window_defined(window: Any, index: dict[str, dict[str, Any]]) -> bool:
    w = _resolve(window, index) if not isinstance(window, dict) else window
    if not isinstance(w, dict):
        return False
    center = w.get("center") or w.get("timestamp")
    if isinstance(center, dict):
        center = center.get("timestamp")
    half = w.get("half_width")
    unit = w.get("unit")
    return (
        center not in (None, "")
        and half is not None
        and isinstance(half, (int, float))
        and half >= 0
        and unit in {"s", "min", "h", "day"}
    )


def _prov_ok(prov: Any, index: dict[str, dict[str, Any]]) -> bool:
    if prov in (None, "", []):
        return False
    if isinstance(prov, str):
        rec = index.get(prov)
        if rec is None:
            # dangling ref — broken
            return False
        prov = rec
    if not isinstance(prov, dict):
        return False
    if not prov.get("associated_agent") and not (
        isinstance(prov.get("associated_agent"), str) and prov.get("associated_agent")
    ):
        # allow agent as nested or string id present in index or inline
        agent = prov.get("associated_agent")
        if not agent:
            return False
    agent = prov.get("associated_agent")
    if isinstance(agent, str) and agent not in index and not agent.startswith("agent:"):
        # string agent ids like agent:hcsm_validator are OK by convention
        if ":" not in str(agent):
            return False
    if not prov.get("started_at") and prov.get("activity_type") is None and not prov.get("id"):
        return False
    if isinstance(prov, dict) and prov.get("id") and prov.get("id") in index:
        full = index[prov["id"]]
        return bool(full.get("associated_agent") or full.get("started_at"))
    # inline or string ref with agent-like id
    if isinstance(prov, str):
        return True  # already checked membership
    return bool(prov.get("associated_agent")) and bool(
        prov.get("started_at") or prov.get("activity_type")
    )


def _collect_observations(
    request: dict[str, Any],
    index: dict[str, dict[str, Any]],
    objects: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Observations relevant to the request."""
    explicit = request.get("observations") or request.get("inferred_from") or []
    obs: list[dict[str, Any]] = []
    for ref in explicit:
        o = _resolve(ref, index)
        if o and o.get("type") == "Observation":
            obs.append(o)
        elif isinstance(ref, dict) and (
            ref.get("type") == "Observation" or "raw_value" in ref or "alignment" in ref
        ):
            obs.append(ref)
    if obs:
        return obs
    # fall back: all observations in bundle
    return [o for o in objects if o.get("type") == "Observation"]


def _alt_names(alts: list[Any]) -> set[str]:
    names: set[str] = set()
    for a in alts:
        if isinstance(a, str):
            names.add(a.split("/")[-1].lower())
        elif isinstance(a, dict):
            for key in ("modulator", "id", "label", "name"):
                if a.get(key):
                    names.add(str(a[key]).split("/")[-1].lower())
                    break
    return names


def assess_admissibility(
    request: dict[str, Any],
    onto: Ontology | None = None,
    *,
    bundle: dict[str, Any] | list[dict[str, Any]] | None = None,
) -> AdmissibilityResult:
    """Evaluate A(c,p,w) for a construct estimation request.

    ``request`` fields (all optional except construct):
      - construct / estimates / construct_id
      - has_window
      - has_context / context
      - observations / inferred_from
      - alternatives
      - has_provenance
      - about_person
      - measures (optional measure ids claimed)
    """
    if onto is None:
        onto = Ontology()

    objects: list[dict[str, Any]] = []
    if bundle is not None:
        if isinstance(bundle, list):
            objects = bundle
        elif isinstance(bundle, dict):
            if isinstance(bundle.get("objects"), list):
                objects = bundle["objects"]
            else:
                objects = [bundle]
    # also include nested objects from request
    if isinstance(request.get("objects"), list):
        objects = list(objects) + request["objects"]

    index = _index_bundle(objects)

    construct_id = (
        request.get("construct")
        or request.get("estimates")
        or request.get("construct_id")
        or request.get("insufficient_for")
    )
    checks: list[dict[str, Any]] = []

    def fail(code: str, message: str) -> AdmissibilityResult:
        checks.append({"check": code, "pass": False, "detail": message})
        return AdmissibilityResult(
            admissible=False,
            refusal_code=code,
            message=message,
            construct_id=str(construct_id) if construct_id else None,
            checks=checks,
        )

    def ok_check(name: str, detail: str = "") -> None:
        checks.append({"check": name, "pass": True, "detail": detail})

    # 1. Construct exists and is not diagnostic
    if not construct_id:
        return fail("NO_CONSTRUCT", "No construct identifier provided.")

    cid = str(construct_id)
    if Ontology.is_diagnostic_target(cid):
        return fail(
            "NO_CONSTRUCT",
            f"Target '{cid}' is diagnostic / nosological — out of HCSM scope.",
        )

    rec = onto.construct(cid)
    if rec is None and not cid.startswith("hcsm:knowledge/construct/"):
        # try local name
        rec = onto.construct(cid.split("/")[-1])
    if rec is None:
        return fail(
            "NO_CONSTRUCT",
            f"Construct '{cid}' is not in ontology v{onto.version}.",
        )
    ok_check("NO_CONSTRUCT", f"known construct {rec.get('id', cid)}")

    # 2. Window defined
    window = request.get("has_window") or request.get("window") or request.get("temporal_window")
    if not _window_defined(window, index):
        return fail(
            "WINDOW_UNDEFINED",
            "Temporal window must have center, half_width ≥ 0, and unit.",
        )
    ok_check("WINDOW_UNDEFINED", "window defined")

    # 3. Evidence with alignment exact|close
    observations = _collect_observations(request, index, objects)
    usable = [
        o
        for o in observations
        if o.get("alignment") in {"exact", "close"}
        and o.get("quality_flag") != "unusable"
    ]
    if not usable:
        # check misalignment specifically
        if observations and all(o.get("alignment") == "none" for o in observations):
            return fail(
                "MISALIGNED_MEASURE",
                "Observations exist but alignment is 'none' for all — "
                "measure does not support this construct in the knowledge graph.",
            )
        return fail(
            "NO_EVIDENCE",
            "No observation with alignment exact|close in window for this construct.",
        )
    ok_check("NO_EVIDENCE", f"{len(usable)} usable observation(s)")

    # 3b. Optional: claimed measures must not be pure digital-as-construct
    for m in request.get("measures") or []:
        if Ontology.is_digital_feature_as_construct(str(m)):
            return fail(
                "MISALIGNED_MEASURE",
                f"Digital feature '{m}' cannot serve as aligned measure of a construct.",
            )

    # 4. Context
    ctx = request.get("has_context") or request.get("context") or request.get("context_id")
    ctx_obj = _resolve(ctx, index) if not isinstance(ctx, dict) else ctx
    required_dims = onto.requires_context(rec.get("id") or cid)
    if required_dims:
        if ctx_obj is None and isinstance(ctx, str) and ctx:
            # opaque ref not in bundle — treat as present but unknown completeness
            ok_check("CONTEXT_MISSING", f"context ref '{ctx}' (unresolved, assumed declared)")
        elif ctx_obj is None:
            return fail(
                "CONTEXT_MISSING",
                f"Construct requires context dimensions {required_dims}; none provided.",
            )
        else:
            completeness = ctx_obj.get("completeness")
            if completeness == "declared_unknown":
                ok_check("CONTEXT_MISSING", "context declared_unknown")
            else:
                missing = []
                for dim in required_dims:
                    if _is_missing_dim(ctx_obj, dim):
                        missing.append(dim)
                if missing and completeness != "declared_unknown":
                    return fail(
                        "CONTEXT_MISSING",
                        f"Required context dimensions missing: {missing}.",
                    )
                ok_check("CONTEXT_MISSING", "required dimensions present or partial OK")
    else:
        ok_check("CONTEXT_MISSING", "no required context dimensions")

    # 5. Provenance
    prov = request.get("has_provenance") or request.get("provenance")
    # also require usable observations to have provenance
    obs_prov_ok = all(
        _prov_ok(o.get("has_provenance") or o.get("provenance"), index) for o in usable
    )
    if not _prov_ok(prov, index) or not obs_prov_ok:
        return fail(
            "PROVENANCE_BROKEN",
            "Provenance chain incomplete for inference activity or observations.",
        )
    ok_check("PROVENANCE_BROKEN", "provenance chain present")

    # 6. Mandatory alternatives instantiated
    mandatory = onto.mandatory_alternatives(rec.get("id") or cid)
    alts = request.get("alternatives") or []
    if mandatory:
        names = _alt_names(alts)
        missing_alts = []
        for m in mandatory:
            token = m.split("/")[-1].lower()
            if token not in names and m.lower() not in names:
                # also accept full iri endings
                if not any(token in n for n in names):
                    missing_alts.append(m)
        if missing_alts:
            return fail(
                "UNRESOLVED_ALTERNATIVES",
                "Mandatory alternatives not instantiated (must be named even if "
                f"plausibility unknown): {missing_alts}.",
            )
        ok_check("UNRESOLVED_ALTERNATIVES", f"{len(names)} alternatives named")
    else:
        ok_check("UNRESOLVED_ALTERNATIVES", "no mandatory alternatives")

    return AdmissibilityResult(
        admissible=True,
        refusal_code=None,
        message="Admissible for estimation under HCSM v0.1 contract.",
        construct_id=str(rec.get("id") or cid),
        checks=checks,
    )


def _is_missing_dim(ctx: dict[str, Any], dim: str) -> bool:
    val = ctx.get(dim)
    if val is None:
        return True
    if val == {} or val == [] or val == "":
        return True
    if isinstance(val, dict) and val.get("status") == "missing":
        return True
    return False


def assess_bundle_requests(
    bundle: dict[str, Any],
    onto: Ontology | None = None,
) -> list[AdmissibilityResult]:
    """Run admissibility for each 'inference_request' in a bundle, or for each CE target."""
    if onto is None:
        onto = Ontology()
    objects = bundle.get("objects") if isinstance(bundle, dict) else bundle
    if not isinstance(objects, list):
        objects = []
    results: list[AdmissibilityResult] = []

    requests = [
        o
        for o in objects
        if isinstance(o, dict) and o.get("type") in {"InferenceRequest", "inference_request"}
    ]
    if not requests and isinstance(bundle, dict):
        top = bundle.get("inference_requests") or bundle.get("requests")
        if isinstance(top, list):
            requests = top

    if requests:
        for req in requests:
            results.append(assess_admissibility(req, onto, bundle=bundle))
        return results

    # If bundle already contains ConstructEstimates, re-check their admissibility inputs
    for o in objects:
        if isinstance(o, dict) and o.get("type") == "ConstructEstimate":
            req = {
                "construct": o.get("estimates") or o.get("construct_id"),
                "has_window": o.get("has_window"),
                "has_context": o.get("has_context"),
                "inferred_from": o.get("inferred_from"),
                "alternatives": o.get("alternatives"),
                "has_provenance": o.get("has_provenance"),
                "about_person": o.get("about_person"),
                "measures": o.get("measures"),
            }
            results.append(assess_admissibility(req, onto, bundle=bundle))
    return results
