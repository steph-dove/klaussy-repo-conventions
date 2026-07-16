"""Kotlin convention detectors package."""

from .android import KotlinAndroidDetector
from .architecture import KotlinArchitectureDetector
from .base import KotlinDetector
from .coroutines import KotlinCoroutinesDetector
from .data_flow import KotlinDataFlowDetector
from .database import KotlinDatabaseDetector
from .documentation import KotlinDocumentationDetector
from .errors import KotlinErrorHandlingDetector

# Import all detector classes to ensure they register
from .gradle import KotlinGradleDetector
from .index import KotlinIndex, make_evidence
from .logging import KotlinLoggingDetector
from .null_safety import KotlinNullSafetyDetector
from .serialization import KotlinSerializationDetector
from .spring_di import KotlinDIDetector
from .testing import KotlinTestingDetector
from .web import KotlinWebDetector

__all__ = [
    "KotlinIndex",
    "make_evidence",
    "KotlinDetector",
    "KotlinGradleDetector",
    "KotlinTestingDetector",
    "KotlinCoroutinesDetector",
    "KotlinNullSafetyDetector",
    "KotlinErrorHandlingDetector",
    "KotlinLoggingDetector",
    "KotlinSerializationDetector",
    "KotlinDIDetector",
    "KotlinWebDetector",
    "KotlinDatabaseDetector",
    "KotlinDocumentationDetector",
    "KotlinArchitectureDetector",
    "KotlinDataFlowDetector",
    "KotlinAndroidDetector",
]
