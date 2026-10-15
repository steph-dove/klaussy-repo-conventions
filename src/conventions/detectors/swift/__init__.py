# Copyright 2026 Dovatech LLC. SPDX-License-Identifier: FSL-1.1-MIT
"""Swift convention detectors package."""

# Import all detector classes to ensure they register
from .architecture import SwiftArchitectureDetector
from .base import SwiftDetector
from .index import SwiftIndex, make_evidence
from .testing import SwiftTestingDetector

__all__ = [
    "SwiftIndex",
    "make_evidence",
    "SwiftDetector",
    "SwiftArchitectureDetector",
    "SwiftTestingDetector",
]
