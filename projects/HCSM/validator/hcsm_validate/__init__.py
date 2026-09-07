"""HCSM contract validator — form (V1) and admissibility (V5).

Does not estimate cognitive state. Does not replace scientific judgment.
"""

from .ontology import Ontology
from .schema import ValidationResult, validate_bundle, validate_object
from .admissibility import AdmissibilityResult, assess_admissibility

__version__ = "0.1.1"
__all__ = [
    "Ontology",
    "ValidationResult",
    "validate_bundle",
    "validate_object",
    "AdmissibilityResult",
    "assess_admissibility",
    "__version__",
]
