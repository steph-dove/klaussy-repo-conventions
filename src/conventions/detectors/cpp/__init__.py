# Copyright 2026 Dovatech LLC. SPDX-License-Identifier: FSL-1.1-MIT
"""C++ convention detectors package."""

# Import all detector classes to ensure they register
from .architecture import CPPArchitectureDetector
from .base import CPPDetector
from .index import CPPIndex, make_evidence
from .testing import CPPTestingDetector

__all__ = [
    "CPPIndex",
    "make_evidence",
    "CPPDetector",
    "CPPArchitectureDetector",
    "CPPTestingDetector",
]
