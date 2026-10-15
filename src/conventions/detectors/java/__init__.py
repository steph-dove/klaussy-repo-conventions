# Copyright 2026 Dovatech LLC. SPDX-License-Identifier: FSL-1.1-MIT
"""Java convention detectors package."""

# Import all detector classes to ensure they register
from .architecture import JavaArchitectureDetector
from .base import JavaDetector
from .build import JavaBuildDetector
from .conventions import JavaConventionsDetector
from .database import JavaDatabaseDetector
from .di import JavaDIDetector
from .index import JavaIndex, make_evidence
from .logging import JavaLoggingDetector
from .testing import JavaTestingDetector

__all__ = [
    "JavaIndex",
    "make_evidence",
    "JavaDetector",
    "JavaArchitectureDetector",
    "JavaBuildDetector",
    "JavaDatabaseDetector",
    "JavaDIDetector",
    "JavaLoggingDetector",
    "JavaTestingDetector",
    "JavaConventionsDetector",
]
