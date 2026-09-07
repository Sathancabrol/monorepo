"""V1 — structural validation of HCSM objects.

Rejects illegal forms. Does not assess scientific truth.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .ontology import OBS_FORBIDDEN_FIELDS, PII_FIELDS, Ontology

# Types recognized in a bundle
KNOWN_TYPES = frozenset(
    {
        "ConstructEstimate",
        "Refusal",
        "Observation",
        "MeasureInstance",
        "ContextRecord",
        "ProvenanceRecord",
        "CognitiveState",
        "FunctionalProjection",
        "TemporalWindow",
        "Uncertainty",
        "AlternativeExplanation",
        "Person",
        "Agent",
        "Signal",
        "CapacityProfile",
        "Trajectory",
        "Construct",
        "Bundle",  # container
    }
)

REFUSAL_CODES = frozenset(
    {
        "NO_CONSTRUCT",
        "NO_EVIDENCE",
        "WINDOW_UNDEFINED",
        "CONTEXT_MISSING",
        "UNRESOLVED_ALTERNATIVES",
        "MISALIGNED_MEASURE",
        "PROVENANCE_BROKEN",
    }
)

VALID_CHANNELS = frozenset(
    {
        "behavioral",
        "subjective",
        "physiological",
        "neural",
        "contextual",
        "computational",
        "digital_passive",
    }
)

VALID_SCALES = frozenset({"latent_z", "unit_interval", "model_param"})
VALID_ALIGNMENTS = frozenset({"exact", "close", "none"})
VALID_QUALITY = frozenset({"ok", "degraded", "unusable"})
VALID_UNCERTAINTY_KINDS = frozenset(
    {"sd", "variance", "credible_interval", "discrete", "unknown"}
)
VALID_WINDOW_UNITS = frozenset({"s", "min", "h", "day"})
STATUS_VOCAB = frozenset(
    {"ESTABLISHED", "SUPPORTED", "PROPOSED", "HYPOTHESIS", "OPEN_QUESTION"}
)


@dataclass
class Issue:
    code: str
    message: str
    path: str = ""

    def __str__(self) -> str:
        loc = f" @ {self.path}" if self.path else ""
        return f"[{self.code}]{loc} {self.message}"


@dataclass
class ValidationResult:
    ok: bool
    issues: list[Issue] = field(default_factory=list)
    object_type: str | None = None
    object_id: str | None = None

    def add(self, code: str, message: str, path: str = "") -> None:
        self.issues.append(Issue(code, message, path))
        self.ok = False

    def merge(self, other: ValidationResult, prefix: str = "") -> None:
        for iss in other.issues:
            p = f"{prefix}.{iss.path}" if prefix and iss.path else (prefix or iss.path)
            self.issues.append(Issue(iss.code, iss.message, p))
            if not other.ok:
                self.ok = False
        if not other.ok:
            self.ok = False

    def summary(self) -> str:
        if self.ok:
            return "OK"
        return "; ".join(str(i) for i in self.issues)


def _is_blank(v: Any) -> bool:
    return v is None or v == "" or v == [] or v == {}


def _check_pii(obj: dict[str, Any], result: ValidationResult, path: str = "") -> None:
    for key in obj:
        lk = key.lower()
        if lk in PII_FIELDS or any(p in lk for p in ("email", "surname", "geolocation")):
            result.add(
                "V1-PII",
                f"Forbidden civil/PII field '{key}'. Use opaque person identifiers only.",
                path or key,
            )
        val = obj[key]
        if isinstance(val, dict):
            _check_pii(val, result, f"{path}.{key}" if path else key)
        elif isinstance(val, list):
            for i, item in enumerate(val):
                if isinstance(item, dict):
                    _check_pii(item, result, f"{path}.{key}[{i}]" if path else f"{key}[{i}]")


def _validate_window(
    window: Any, result: ValidationResult, path: str = "has_window"
) -> None:
    if _is_blank(window):
        result.add("V1-WINDOW", "Temporal window is missing.", path)
        return
    if isinstance(window, str):
        # reference id — structural OK at V1 (resolved in bundle if present)
        return
    if not isinstance(window, dict):
        result.add("V1-WINDOW", "Window must be an object or reference id.", path)
        return
    center = window.get("center") or window.get("timestamp")
    if _is_blank(center):
        # nested TimePoint
        if isinstance(window.get("center"), dict):
            center = window["center"].get("timestamp")
        if _is_blank(center):
            result.add("V1-WINDOW", "Window center/timestamp is required.", f"{path}.center")
    half = window.get("half_width")
    if half is None:
        result.add("V1-WINDOW", "Window half_width is required.", f"{path}.half_width")
    elif not isinstance(half, (int, float)) or half < 0:
        result.add(
            "V1-WINDOW",
            "half_width must be a non-negative number.",
            f"{path}.half_width",
        )
    unit = window.get("unit")
    if unit is None:
        result.add("V1-WINDOW", "Window unit is required.", f"{path}.unit")
    elif unit not in VALID_WINDOW_UNITS:
        result.add(
            "V1-WINDOW",
            f"Invalid unit '{unit}'. Expected one of {sorted(VALID_WINDOW_UNITS)}.",
            f"{path}.unit",
        )


def _validate_uncertainty(
    unc: Any, result: ValidationResult, path: str = "uncertainty"
) -> None:
    if _is_blank(unc):
        result.add(
            "V1-CE-UNCERTAINTY",
            "ConstructEstimate requires uncertainty (or has_uncertainty).",
            path,
        )
        return
    if isinstance(unc, str):
        return
    if not isinstance(unc, dict):
        result.add("V1-CE-UNCERTAINTY", "uncertainty must be an object.", path)
        return
    kind = unc.get("kind")
    if kind not in VALID_UNCERTAINTY_KINDS:
        result.add(
            "V1-CE-UNCERTAINTY",
            f"uncertainty.kind must be one of {sorted(VALID_UNCERTAINTY_KINDS)}.",
            f"{path}.kind",
        )
    if kind in {"sd", "variance"} and unc.get("value") is None and kind != "unknown":
        # allow unknown without value
        if kind != "unknown":
            result.add(
                "V1-CE-UNCERTAINTY",
                f"uncertainty.kind={kind} requires a numeric value.",
                f"{path}.value",
            )
    if kind == "credible_interval":
        if unc.get("lower") is None or unc.get("upper") is None:
            result.add(
                "V1-CE-UNCERTAINTY",
                "credible_interval requires lower and upper.",
                path,
            )


def _validate_provenance_ref(
    prov: Any, result: ValidationResult, path: str = "has_provenance", required: bool = True
) -> None:
    if _is_blank(prov):
        if required:
            result.add("V1-PROVENANCE", "Provenance is required.", path)
        return
    if isinstance(prov, str):
        return
    if not isinstance(prov, dict):
        result.add("V1-PROVENANCE", "Provenance must be an object or reference id.", path)
        return
    if _is_blank(prov.get("id")) and _is_blank(prov.get("activity_type")):
        result.add(
            "V1-PROVENANCE",
            "Inline provenance needs id or activity_type.",
            path,
        )
    agent = prov.get("associated_agent")
    if required and _is_blank(agent):
        result.add(
            "V1-PROVENANCE",
            "Provenance requires associated_agent.",
            f"{path}.associated_agent",
        )
    at = prov.get("activity_type")
    if at and at not in {"MeasureActivity", "PreprocessActivity", "InferenceActivity"}:
        result.add(
            "V1-PROVENANCE",
            f"Unknown activity_type '{at}'.",
            f"{path}.activity_type",
        )
    if _is_blank(prov.get("started_at")) and required:
        result.add("V1-PROVENANCE", "Provenance requires started_at.", f"{path}.started_at")


def validate_construct_estimate(
    obj: dict[str, Any], onto: Ontology, path: str = ""
) -> ValidationResult:
    r = ValidationResult(ok=True, object_type="ConstructEstimate", object_id=obj.get("id"))
    p = path

    if _is_blank(obj.get("id")):
        r.add("V1-CE-ID", "ConstructEstimate.id is required.", f"{p}id")

    target = obj.get("estimates") or obj.get("construct_id")
    if _is_blank(target):
        r.add("V1-CE-TARGET", "estimates (construct id) is required.", f"{p}estimates")
    else:
        if Ontology.is_diagnostic_target(str(target)):
            r.add(
                "V1-DIAGNOSTIC-TARGET",
                f"ConstructEstimate cannot target diagnostic code '{target}'.",
                f"{p}estimates",
            )
        if Ontology.is_digital_feature_as_construct(str(target)):
            r.add(
                "V1-DIGITAL-AS-CONSTRUCT",
                f"Digital feature '{target}' cannot be labelled as a cognitive construct.",
                f"{p}estimates",
            )

    if obj.get("value") is None:
        r.add("V1-CE-VALUE", "ConstructEstimate.value is required.", f"{p}value")
    elif not isinstance(obj.get("value"), (int, float)):
        r.add("V1-CE-VALUE", "value must be numeric.", f"{p}value")

    scale = obj.get("scale")
    if scale not in VALID_SCALES:
        r.add(
            "V1-CE-SCALE",
            f"scale must be one of {sorted(VALID_SCALES)}.",
            f"{p}scale",
        )

    # uncertainty: accept uncertainty or has_uncertainty
    unc = obj.get("uncertainty") if "uncertainty" in obj else obj.get("has_uncertainty")
    if "uncertainty" not in obj and "has_uncertainty" not in obj:
        r.add(
            "V1-CE-UNCERTAINTY",
            "Missing uncertainty / has_uncertainty.",
            f"{p}uncertainty",
        )
    else:
        _validate_uncertainty(unc, r, f"{p}uncertainty")

    inferred = obj.get("inferred_from")
    if _is_blank(inferred):
        r.add(
            "V1-CE-EVIDENCE",
            "inferred_from must list at least one observation.",
            f"{p}inferred_from",
        )
    elif not isinstance(inferred, list) or len(inferred) < 1:
        r.add(
            "V1-CE-EVIDENCE",
            "inferred_from must be a non-empty list.",
            f"{p}inferred_from",
        )

    if "has_window" not in obj and "temporal_window" not in obj:
        r.add("V1-CE-WINDOW", "has_window is required.", f"{p}has_window")
    else:
        _validate_window(
            obj.get("has_window") or obj.get("temporal_window"),
            r,
            f"{p}has_window",
        )

    if _is_blank(obj.get("has_context")) and _is_blank(obj.get("context_id")):
        r.add("V1-CE-CONTEXT", "has_context is required.", f"{p}has_context")

    if _is_blank(obj.get("has_provenance")) and _is_blank(obj.get("provenance")):
        r.add("V1-CE-PROVENANCE", "has_provenance is required.", f"{p}has_provenance")
    else:
        _validate_provenance_ref(
            obj.get("has_provenance") or obj.get("provenance"),
            r,
            f"{p}has_provenance",
            required=True,
        )

    if _is_blank(obj.get("about_person")) and _is_blank(obj.get("person_id")):
        r.add("V1-CE-PERSON", "about_person is required.", f"{p}about_person")

    est_status = obj.get("estimate_status")
    if est_status is not None and est_status != "estimated":
        r.add(
            "V1-CE-STATUS",
            "estimate_status must be 'estimated' (use Refusal otherwise).",
            f"{p}estimate_status",
        )

    # naked score pattern: only value + construct-like key, missing contract fields
    # (already covered above)

    # alternatives should be present as list (may be empty only if construct has none)
    alts = obj.get("alternatives")
    if alts is not None and not isinstance(alts, list):
        r.add("V1-CE-ALTS", "alternatives must be a list.", f"{p}alternatives")

    status = obj.get("status")
    if status is not None and status not in STATUS_VOCAB:
        r.add(
            "V1-STATUS",
            f"status must be one of {sorted(STATUS_VOCAB)}.",
            f"{p}status",
        )

    _check_pii(obj, r, p.rstrip("."))
    return r


def validate_refusal(
    obj: dict[str, Any], onto: Ontology, path: str = ""
) -> ValidationResult:
    r = ValidationResult(ok=True, object_type="Refusal", object_id=obj.get("id"))
    p = path

    if _is_blank(obj.get("id")):
        r.add("V1-REF-ID", "Refusal.id is required.", f"{p}id")

    if obj.get("value") is not None:
        r.add(
            "V1-REFUSAL-HAS-VALUE",
            "Refusal must not carry a numeric value (no default score).",
            f"{p}value",
        )

    if "uncertainty" in obj or "has_uncertainty" in obj:
        r.add(
            "V1-REFUSAL-HAS-VALUE",
            "Refusal must not carry uncertainty as if it were an estimate.",
            f"{p}uncertainty",
        )

    code = obj.get("code")
    known = set(onto.refusal_codes) | REFUSAL_CODES
    if code not in known:
        r.add(
            "V1-REF-CODE",
            f"Unknown refusal code '{code}'. Expected one of {sorted(known)}.",
            f"{p}code",
        )

    if _is_blank(obj.get("insufficient_for")) and _is_blank(obj.get("construct_id")):
        r.add(
            "V1-REF-TARGET",
            "insufficient_for (construct) is required.",
            f"{p}insufficient_for",
        )

    if _is_blank(obj.get("message")):
        r.add("V1-REF-MSG", "Refusal.message is required.", f"{p}message")

    if _is_blank(obj.get("about_person")) and _is_blank(obj.get("person_id")):
        r.add("V1-REF-PERSON", "about_person is required.", f"{p}about_person")

    if _is_blank(obj.get("has_provenance")) and _is_blank(obj.get("provenance")):
        r.add("V1-REF-PROVENANCE", "has_provenance is required.", f"{p}has_provenance")
    else:
        _validate_provenance_ref(
            obj.get("has_provenance") or obj.get("provenance"),
            r,
            f"{p}has_provenance",
            required=True,
        )

    # window optional on refusal except when code is not WINDOW_UNDEFINED
    if "has_window" in obj and obj.get("has_window") is not None:
        _validate_window(obj.get("has_window"), r, f"{p}has_window")

    _check_pii(obj, r, p.rstrip("."))
    return r


def validate_observation(
    obj: dict[str, Any], onto: Ontology, path: str = ""
) -> ValidationResult:
    r = ValidationResult(ok=True, object_type="Observation", object_id=obj.get("id"))
    p = path

    if _is_blank(obj.get("id")):
        r.add("V1-OBS-ID", "Observation.id is required.", f"{p}id")

    for forbidden in OBS_FORBIDDEN_FIELDS:
        if forbidden in obj and obj[forbidden] is not None:
            r.add(
                "V1-OBS-ESTIMATE-FIELD",
                f"Observation must not carry estimation field '{forbidden}'. "
                "An observation is not a construct.",
                f"{p}{forbidden}",
            )

    # also catch attention=0.73 style keys
    for key in obj:
        lk = key.lower()
        if lk in {"attention", "working_memory", "iq", "cognitive_score"}:
            r.add(
                "V1-OBS-ESTIMATE-FIELD",
                f"Observation field '{key}' looks like a construct label.",
                f"{p}{key}",
            )

    if _is_blank(obj.get("observed_on")) and _is_blank(obj.get("person_id")):
        r.add("V1-OBS-PERSON", "observed_on is required.", f"{p}observed_on")

    if _is_blank(obj.get("produced_by")):
        r.add("V1-OBS-SOURCE", "produced_by (MeasureInstance) is required.", f"{p}produced_by")

    ch = obj.get("channel")
    if ch not in VALID_CHANNELS:
        r.add(
            "V1-OBS-CHANNEL",
            f"channel must be one of {sorted(VALID_CHANNELS)}.",
            f"{p}channel",
        )

    qf = obj.get("quality_flag")
    if qf not in VALID_QUALITY:
        r.add(
            "V1-OBS-QUALITY",
            f"quality_flag must be one of {sorted(VALID_QUALITY)}.",
            f"{p}quality_flag",
        )

    al = obj.get("alignment")
    if al not in VALID_ALIGNMENTS:
        r.add(
            "V1-OBS-ALIGN",
            f"alignment must be one of {sorted(VALID_ALIGNMENTS)}.",
            f"{p}alignment",
        )

    # raw_value XOR missingness
    has_raw = obj.get("raw_value") is not None or obj.get("normalized_value") is not None
    has_miss = obj.get("missingness") is not None
    if not has_raw and not has_miss:
        r.add(
            "V1-OBS-VALUE",
            "Observation needs raw_value/normalized_value or missingness.",
            f"{p}raw_value",
        )

    if _is_blank(obj.get("has_provenance")) and _is_blank(obj.get("provenance")):
        r.add("V1-OBS-PROVENANCE", "has_provenance is required.", f"{p}has_provenance")

    _check_pii(obj, r, p.rstrip("."))
    return r


def validate_functional_projection(
    obj: dict[str, Any], onto: Ontology, path: str = ""
) -> ValidationResult:
    r = ValidationResult(
        ok=True, object_type="FunctionalProjection", object_id=obj.get("id")
    )
    p = path
    status = obj.get("status")
    if status != "HYPOTHESIS":
        r.add(
            "V1-FP-STATUS",
            f"FunctionalProjection.status must be HYPOTHESIS, got '{status}'.",
            f"{p}status",
        )
    if _is_blank(obj.get("from_estimates")):
        r.add(
            "V1-FP-FROM",
            "from_estimates must reference at least one ConstructEstimate.",
            f"{p}from_estimates",
        )
    if _is_blank(obj.get("maps_to")):
        r.add("V1-FP-MAPS", "maps_to (e.g. ICF code) is required.", f"{p}maps_to")
    _check_pii(obj, r, p.rstrip("."))
    return r


def validate_cognitive_state(
    obj: dict[str, Any], onto: Ontology, path: str = ""
) -> ValidationResult:
    r = ValidationResult(ok=True, object_type="CognitiveState", object_id=obj.get("id"))
    p = path
    if _is_blank(obj.get("about_person")):
        r.add("V1-CS-PERSON", "about_person is required.", f"{p}about_person")
    if "has_window" not in obj:
        r.add("V1-CS-WINDOW", "has_window is required.", f"{p}has_window")
    else:
        _validate_window(obj.get("has_window"), r, f"{p}has_window")
    members = obj.get("members")
    if _is_blank(members) or not isinstance(members, list) or len(members) < 1:
        r.add(
            "V1-CS-MEMBERS",
            "members must contain at least one ConstructEstimate or Refusal.",
            f"{p}members",
        )
    else:
        for i, m in enumerate(members):
            if isinstance(m, dict):
                sub = validate_object(m, onto, path=f"{p}members[{i}].")
                r.merge(sub)
    if _is_blank(obj.get("has_provenance")):
        r.add("V1-CS-PROVENANCE", "has_provenance is required.", f"{p}has_provenance")
    _check_pii(obj, r, p.rstrip("."))
    return r


def validate_naked_score(
    obj: dict[str, Any], path: str = ""
) -> ValidationResult | None:
    """Detect bare score objects that lack HCSM contract fields."""
    # Explicit type
    t = obj.get("type")
    if t in KNOWN_TYPES and t != "Bundle":
        return None
    # Heuristic: has a numeric value and a construct-like label, missing contract
    keys = set(obj.keys())
    constructish = any(
        k in obj
        for k in (
            "attention",
            "Attention",
            "score",
            "cognitive_score",
            "construct",
            "metric",
        )
    )
    has_value = isinstance(obj.get("value"), (int, float)) or isinstance(
        obj.get("score"), (int, float)
    )
    missing_contract = not any(
        k in keys
        for k in (
            "uncertainty",
            "has_uncertainty",
            "inferred_from",
            "has_provenance",
            "has_window",
        )
    )
    if (constructish or t in {None, "Score", "CognitiveScore", "Metric"}) and has_value and missing_contract:
        r = ValidationResult(ok=False, object_type=t or "Score", object_id=obj.get("id"))
        r.add(
            "V1-NAKED-SCORE",
            "Naked score rejected. HCSM requires ConstructEstimate with "
            "uncertainty, evidence, window, context, and provenance — "
            "not Attention = 0.73.",
            path or "value",
        )
        return r
    return None


def validate_object(
    obj: dict[str, Any],
    onto: Ontology | None = None,
    path: str = "",
) -> ValidationResult:
    """Validate a single HCSM object (or naked score)."""
    if onto is None:
        onto = Ontology()

    if not isinstance(obj, dict):
        r = ValidationResult(ok=False)
        r.add("V1-TYPE", "Object must be a JSON object.", path)
        return r

    # Bundle container
    if obj.get("type") == "Bundle" or ("objects" in obj and obj.get("type") is None and "hcsm_bundle" in obj):
        return validate_bundle(obj, onto)

    if "objects" in obj and isinstance(obj.get("objects"), list) and obj.get("type") in {
        None,
        "Bundle",
        "hcsm_bundle",
    }:
        return validate_bundle(obj, onto)

    naked = validate_naked_score(obj, path)
    if naked is not None:
        return naked

    t = obj.get("type")
    if t is None:
        r = ValidationResult(ok=False, object_id=obj.get("id"))
        r.add(
            "V1-TYPE",
            "Missing type. Expected ConstructEstimate, Refusal, Observation, …",
            f"{path}type",
        )
        return r

    dispatch = {
        "ConstructEstimate": validate_construct_estimate,
        "Refusal": validate_refusal,
        "Observation": validate_observation,
        "FunctionalProjection": validate_functional_projection,
        "CognitiveState": validate_cognitive_state,
    }
    if t in dispatch:
        return dispatch[t](obj, onto, path)

    # Light validation for supporting types
    r = ValidationResult(ok=True, object_type=t, object_id=obj.get("id"))
    if t not in KNOWN_TYPES:
        r.add("V1-TYPE", f"Unknown type '{t}'.", f"{path}type")
    if t == "TemporalWindow":
        _validate_window(obj, r, path.rstrip(".") or "window")
    if t == "ProvenanceRecord":
        _validate_provenance_ref(obj, r, path.rstrip(".") or "provenance", required=True)
    if t == "ContextRecord":
        if _is_blank(obj.get("of_person")):
            r.add("V1-CTX-PERSON", "of_person is required.", f"{path}of_person")
        if "has_window" in obj:
            _validate_window(obj.get("has_window"), r, f"{path}has_window")
        comp = obj.get("completeness")
        if comp not in {"full", "partial", "declared_unknown", None}:
            r.add(
                "V1-CTX-COMPLETENESS",
                f"Invalid completeness '{comp}'.",
                f"{path}completeness",
            )
        if comp is None:
            r.add(
                "V1-CTX-COMPLETENESS",
                "completeness is required.",
                f"{path}completeness",
            )
    _check_pii(obj, r, path.rstrip("."))
    return r


def validate_bundle(
    bundle: dict[str, Any],
    onto: Ontology | None = None,
) -> ValidationResult:
    """Validate a list of objects, optionally under key 'objects'."""
    if onto is None:
        onto = Ontology()

    r = ValidationResult(ok=True, object_type="Bundle", object_id=bundle.get("id"))

    if isinstance(bundle.get("objects"), list):
        objects = bundle["objects"]
    elif isinstance(bundle, list):  # type: ignore[unreachable]
        objects = bundle
    else:
        # single object wrapped
        if bundle.get("type") and bundle.get("type") != "Bundle":
            return validate_object(bundle, onto)
        r.add("V1-BUNDLE-EMPTY", "Bundle has no 'objects' list.", "objects")
        return r

    if len(objects) == 0:
        r.add("V1-BUNDLE-EMPTY", "Bundle objects list is empty.", "objects")
        return r

    for i, obj in enumerate(objects):
        if not isinstance(obj, dict):
            r.add("V1-TYPE", "Bundle item must be an object.", f"objects[{i}]")
            continue
        sub = validate_object(obj, onto, path=f"objects[{i}].")
        r.merge(sub)
        if not sub.ok:
            r.ok = False

    if r.issues:
        r.ok = all(False for _ in r.issues if True) and len(r.issues) == 0
        # fix: ok is False if any issues
        r.ok = len(r.issues) == 0

    return r
