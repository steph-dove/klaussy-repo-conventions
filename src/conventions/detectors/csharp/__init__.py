"""C# convention detectors package."""

# Import all detector classes to ensure they register
from .architecture import CSharpArchitectureDetector
from .base import CSharpDetector
from .build import CSharpBuildDetector
from .conventions import CSharpConventionsDetector
from .database import CSharpDatabaseDetector
from .di import CSharpDIDetector
from .index import CSharpIndex, make_evidence
from .logging import CSharpLoggingDetector
from .testing import CSharpTestingDetector

__all__ = [
    "CSharpIndex",
    "make_evidence",
    "CSharpDetector",
    "CSharpArchitectureDetector",
    "CSharpBuildDetector",
    "CSharpDatabaseDetector",
    "CSharpDIDetector",
    "CSharpLoggingDetector",
    "CSharpTestingDetector",
    "CSharpConventionsDetector",
]
