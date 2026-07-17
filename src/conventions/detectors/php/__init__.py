"""PHP convention detectors package."""

# Import all detector classes to ensure they register
from .architecture import PHPArchitectureDetector
from .base import PHPDetector
from .database import PHPDatabaseDetector
from .index import PHPIndex, make_evidence
from .testing import PHPTestingDetector

__all__ = [
    "PHPIndex",
    "make_evidence",
    "PHPDetector",
    "PHPArchitectureDetector",
    "PHPDatabaseDetector",
    "PHPTestingDetector",
]
