"""Ruby convention detectors package."""

from .base import RubyDetector
from .build import RubyBuildDetector
from .database import RubyDatabaseDetector
from .index import RubyIndex, make_evidence

# Import all detector classes to ensure they register
from .rails_conventions import RubyRailsConventionsDetector
from .testing import RubyTestingDetector

__all__ = [
    "RubyIndex",
    "make_evidence",
    "RubyDetector",
    "RubyBuildDetector",
    "RubyRailsConventionsDetector",
    "RubyDatabaseDetector",
    "RubyTestingDetector",
]
