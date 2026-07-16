"""Shared JVM helpers for language detectors (Kotlin, and Java in future).

This package holds parsing utilities common to JVM languages -- build file
parsing (Gradle/Maven) and JUnit test conventions. It intentionally contains
no registered detectors: language packages such as `detectors/kotlin` own the
detectors and call into these helpers.
"""

from .build import (
    BuildInfo,
    Dependency,
    parse_build_files,
)
from .junit import (
    JUnitInfo,
    detect_junit,
)

__all__ = [
    "BuildInfo",
    "Dependency",
    "parse_build_files",
    "JUnitInfo",
    "detect_junit",
]
