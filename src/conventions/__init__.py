# Copyright 2026 Dovatech LLC. SPDX-License-Identifier: FSL-1.1-MIT
"""Conventions detection library."""

from .schemas import (
    ConventionRule,
    ConventionsOutput,
    DetectorWarning,
    EvidenceSnippet,
    Language,
    RepoMetadata,
)

__version__ = "1.9.2"

__all__ = [
    "ConventionRule",
    "ConventionsOutput",
    "DetectorWarning",
    "EvidenceSnippet",
    "Language",
    "RepoMetadata",
]
