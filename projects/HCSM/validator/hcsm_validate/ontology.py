"""Load and query the HCSM ontology YAML (source of truth)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

# Default: repo_root/ontology/hcsm-v0.1.yaml relative to this package
_DEFAULT_ONTOLOGY = (
    Path(__file__).resolve().parents[2] / "ontology" / "hcsm-v0.1.yaml"
)

# Diagnostic / nosological prefixes and tokens that must never be estimate targets
DIAGNOSTIC_MARKERS = (
    "dsm",
    "dsm5",
    "dsm-5",
    "icd10",
    "icd-10",
    "icd11",
    "icd-11",
    "diagnosis",
    "diagnostic",
    "disorder",
    "adhd",
    "tdah",
    "autism_spectrum",
    "schizophrenia",
    "depression_diagnosis",
)

# Civil / PII field names forbidden on any HCSM object
PII_FIELDS = frozenset(
    {
        "email",
        "full_name",
        "first_name",
        "last_name",
        "surname",
        "given_name",
        "phone",
        "phone_number",
        "address",
        "street",
        "national_id",
        "ssn",
        "social_security",
        "date_of_birth",
        "dob",
        "gps",
        "latitude",
        "longitude",
        "geolocation",
        "medical_record_number",
        "mrn",
    }
)

# Observation must never carry estimation semantics
OBS_FORBIDDEN_FIELDS = frozenset(
    {
        "construct_id",
        "estimates",
        "attention",
        "working_memory",
        "cognitive_control",
        "estimate_status",
        "value_as_construct",
        "latent_value",
        "diagnosed_as",
        "diagnosis",
    }
)

# Digital passive features that must not be labelled as constructs
DIGITAL_FEATURE_MARKERS = (
    "screen_time",
    "screentime",
    "unlock_count",
    "phone_usage",
    "app_usage",
    "click_rate",
    "scroll_speed",
    "steps_as_cognition",
    "digital_phenotype_score",
)


class Ontology:
    """Thin query layer over hcsm-v0.1.yaml."""

    def __init__(self, path: Path | str | None = None) -> None:
        self.path = Path(path) if path else _DEFAULT_ONTOLOGY
        if not self.path.is_file():
            raise FileNotFoundError(f"Ontology not found: {self.path}")
        with self.path.open(encoding="utf-8") as fh:
            self.raw: dict[str, Any] = yaml.safe_load(fh)

        self.version: str = str(self.raw.get("version", "unknown"))
        self.status: str = str(self.raw.get("status", "PROPOSED"))
        self.refusal_codes: list[str] = list(self.raw.get("refusal_codes", []))
        self.evidence_channels: list[str] = list(self.raw.get("evidence_channels", []))
        self.status_vocabulary: list[str] = list(self.raw.get("status_vocabulary", []))
        self.context_dimensions: list[str] = list(self.raw.get("context_dimensions", []))
        self.constructs: dict[str, dict[str, Any]] = dict(self.raw.get("constructs", {}))
        self.tasks_and_measures: dict[str, dict[str, Any]] = dict(
            self.raw.get("tasks_and_measures", {})
        )
        self.classes: dict[str, dict[str, Any]] = dict(self.raw.get("classes", {}))

        # id → construct record
        self._construct_by_id: dict[str, dict[str, Any]] = {}
        for key, rec in self.constructs.items():
            cid = rec.get("id") or f"hcsm:knowledge/construct/{key}"
            self._construct_by_id[cid] = {**rec, "_key": key}
            self._construct_by_id[key] = self._construct_by_id[cid]
            # bare local names
            self._construct_by_id[f"hcsm:construct/{key}"] = self._construct_by_id[cid]

        self._measure_by_id: dict[str, dict[str, Any]] = {}
        for key, rec in self.tasks_and_measures.items():
            mid = rec.get("id") or f"hcsm:knowledge/measure/{key}"
            self._measure_by_id[mid] = {**rec, "_key": key}
            self._measure_by_id[key] = self._measure_by_id[mid]

    def construct(self, construct_id: str | None) -> dict[str, Any] | None:
        if not construct_id:
            return None
        if construct_id in self._construct_by_id:
            return self._construct_by_id[construct_id]
        # suffix match
        for cid, rec in self._construct_by_id.items():
            if cid.endswith("/" + construct_id.split("/")[-1]):
                return rec
        return None

    def is_known_construct(self, construct_id: str | None) -> bool:
        return self.construct(construct_id) is not None

    def mandatory_alternatives(self, construct_id: str | None) -> list[str]:
        rec = self.construct(construct_id)
        if not rec:
            return []
        return list(rec.get("mandatory_alternatives") or [])

    def requires_context(self, construct_id: str | None) -> list[str]:
        rec = self.construct(construct_id)
        if not rec:
            return []
        return list(rec.get("requires_context") or [])

    def measure(self, measure_id: str | None) -> dict[str, Any] | None:
        if not measure_id:
            return None
        if measure_id in self._measure_by_id:
            return self._measure_by_id[measure_id]
        for mid, rec in self._measure_by_id.items():
            if mid.endswith("/" + measure_id.split("/")[-1]):
                return rec
        return None

    @staticmethod
    def is_diagnostic_target(target: str | None) -> bool:
        if not target:
            return False
        t = target.lower().replace(" ", "_")
        return any(m in t for m in DIAGNOSTIC_MARKERS)

    @staticmethod
    def is_digital_feature_as_construct(target: str | None) -> bool:
        if not target:
            return False
        t = target.lower().replace(" ", "_")
        return any(m in t for m in DIGITAL_FEATURE_MARKERS)
