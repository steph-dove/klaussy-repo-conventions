"""JUnit test convention detection shared across JVM languages."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional, Protocol

# JUnit 5 lives under org.junit.jupiter; JUnit 4 under plain org.junit.
JUNIT5_IMPORT = "org.junit.jupiter"
JUNIT4_IMPORT = "org.junit."

# Annotations that mark a test method, mapped to the JUnit major version that
# introduced them. Used to disambiguate JUnit 4 from 5 when imports are absent.
TEST_ANNOTATIONS = {
    "Test": None,  # present in both 4 and 5
    "ParameterizedTest": 5,
    "RepeatedTest": 5,
    "TestFactory": 5,
    "TestTemplate": 5,
    "Nested": 5,
    "BeforeEach": 5,
    "AfterEach": 5,
    "BeforeAll": 5,
    "AfterAll": 5,
    "Before": 4,
    "After": 4,
    "BeforeClass": 4,
    "AfterClass": 4,
}


class _Index(Protocol):
    """The subset of a language index that JUnit detection needs."""

    def count_imports_matching(self, pattern: str) -> int: ...

    def search_pattern(
        self, pattern: str, limit: int = ..., exclude_tests: bool = ...
    ) -> list[tuple[str, int, str]]: ...

    def count_pattern(self, pattern: str, exclude_tests: bool = ...) -> int: ...


@dataclass
class JUnitInfo:
    """Detected JUnit usage in a repository."""

    # 5, 4, or None when no JUnit usage is found
    major_version: Optional[int] = None
    test_method_count: int = 0
    annotation_counts: dict[str, int] = field(default_factory=dict)
    examples: list[tuple[str, int]] = field(default_factory=list)  # (rel_path, line)
    uses_display_name: bool = False
    uses_nested: bool = False
    uses_parameterized: bool = False

    @property
    def is_present(self) -> bool:
        """Whether any JUnit usage was detected."""
        return self.major_version is not None


def detect_junit(index: _Index, example_limit: int = 3) -> JUnitInfo:
    """Detect JUnit version and test-annotation usage via a language index."""
    info = JUnitInfo()

    for annotation, introduced_in in TEST_ANNOTATIONS.items():
        # Counts come from count_pattern, never len(search_pattern(...)):
        # search_pattern stops at its limit, which would silently cap the
        # reported test count at that limit for any sizable repository.
        count = index.count_pattern(rf"@{annotation}\b")
        if not count:
            continue

        info.annotation_counts[annotation] = count

        if annotation == "Test":
            info.test_method_count = count
            info.examples.extend(
                (rel_path, line)
                for rel_path, line, _ in index.search_pattern(
                    rf"@{annotation}\b", limit=example_limit
                )
            )
        if introduced_in == 5:
            info.uses_nested = info.uses_nested or annotation == "Nested"
            info.uses_parameterized = info.uses_parameterized or annotation == "ParameterizedTest"

    if not info.annotation_counts:
        return info

    info.uses_display_name = bool(index.search_pattern(r"@DisplayName\b", limit=1))
    info.major_version = _infer_major_version(index, info)

    return info


def _infer_major_version(index: _Index, info: JUnitInfo) -> int:
    """Infer the JUnit major version from imports, falling back to annotations."""
    if index.count_imports_matching(JUNIT5_IMPORT) > 0:
        return 5

    junit4_only = {a for a, v in TEST_ANNOTATIONS.items() if v == 4}
    if index.count_imports_matching(JUNIT4_IMPORT) > 0:
        # `org.junit.` is a prefix of `org.junit.jupiter.`, so only treat this as
        # JUnit 4 when a 4-exclusive annotation corroborates it.
        if info.annotation_counts.keys() & junit4_only:
            return 4

    junit5_only = {a for a, v in TEST_ANNOTATIONS.items() if v == 5}
    if info.annotation_counts.keys() & junit5_only:
        return 5
    if info.annotation_counts.keys() & junit4_only:
        return 4

    # Only a bare @Test with no distinguishing import or annotation. JUnit 5 is
    # the modern default, so prefer it over guessing 4.
    return 5


def count_assertion_style(index: _Index) -> dict[str, int]:
    """Count assertion styles, to distinguish JUnit/Kotest/AssertJ/Truth usage."""
    styles = {
        "junit_assertions": r"\bassert(?:Equals|True|False|Null|NotNull|Throws)\s*\(",
        "kotlin_test_assertions": r"\bassert(?:Equals|True|False|Null|NotNull|Fails)\s*\(",
        "assertj": r"\bassertThat\s*\(",
        "truth": r"\bassertWithMessage\s*\(",
        "kotest_matchers": r"\bshould(?:Be|NotBe|Contain|Throw|HaveSize)\b",
    }
    return {name: index.count_pattern(pattern) for name, pattern in styles.items()}


def find_test_class_naming(index: _Index) -> dict[str, int]:
    """Count test class naming conventions (FooTest vs TestFoo vs FooSpec)."""
    conventions = {
        "suffix_test": r"\bclass\s+\w+Test\b",
        "suffix_tests": r"\bclass\s+\w+Tests\b",
        "suffix_spec": r"\bclass\s+\w+Spec\b",
        "suffix_it": r"\bclass\s+\w+IT\b",
        "prefix_test": r"\bclass\s+Test[A-Z]\w*\b",
    }
    counts = {}
    for name, pattern in conventions.items():
        count = index.count_pattern(pattern)
        if count:
            counts[name] = count
    return counts


def strip_annotation_args(annotation: str) -> str:
    """Normalize `@Foo(bar = 1)` to `Foo` for grouping."""
    return re.sub(r"\s*\(.*\)\s*$", "", annotation.lstrip("@")).strip()
