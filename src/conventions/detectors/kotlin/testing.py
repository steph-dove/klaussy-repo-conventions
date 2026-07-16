"""Kotlin testing conventions detector."""

from __future__ import annotations

import re

from ..base import DetectorContext, DetectorResult
from ..jvm.junit import count_assertion_style, detect_junit, find_test_class_naming
from ..registry import DetectorRegistry
from .base import KotlinDetector
from .index import make_evidence

# Kotest spec base classes, detected via their supertype declaration, e.g.
# `class FooTest : StringSpec({ ... })`.
KOTEST_SPEC_STYLES = (
    "StringSpec",
    "FunSpec",
    "BehaviorSpec",
    "DescribeSpec",
    "ShouldSpec",
    "WordSpec",
)

# Idiomatic Kotlin backtick-quoted test method names, e.g. fun `does the thing`().
BACKTICK_TEST_NAME_PATTERN = r"fun\s+`[^`]+`\s*\("

# Test-runner-ish frameworks, in the order they should be preferred when
# picking a single "primary" framework and when building the frameworks list.
FRAMEWORK_PRIORITY = (
    "junit5",
    "junit4",
    "kotest",
    "kotlin_test",
    "mockk",
    "mockito",
    "turbine",
    "coroutine_test",
    "assertj",
    "truth",
    "hamcrest",
    "strikt",
    "testcontainers",
)

# The subset of frameworks that represent a "test runner" rather than an
# assertion or mocking library, used to pick the primary framework.
RUNNER_FRAMEWORKS = ("kotest", "junit5", "junit4", "kotlin_test")


@DetectorRegistry.register
class KotlinTestingDetector(KotlinDetector):
    """Detect Kotlin testing frameworks, assertion styles and test organization."""

    name = "kotlin_testing"
    description = "Detects Kotlin testing frameworks, assertion styles and test organization"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect testing conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        junit_info = detect_junit(index)
        assertion_counts = count_assertion_style(index)
        class_naming = find_test_class_naming(index)

        test_files = index.get_test_files()
        non_test_files = index.get_non_test_files()
        test_file_count = len(test_files)

        patterns: dict[str, dict] = {}
        examples: list[tuple[str, int]] = []

        # JUnit (reused from the shared JVM detector)
        if junit_info.is_present:
            key = f"junit{junit_info.major_version}"
            patterns[key] = {
                "name": f"JUnit {junit_info.major_version}",
                "count": junit_info.test_method_count,
            }
            examples.extend(junit_info.examples[:3])

        # Kotest, including spec style detection
        kotest_import_count = index.count_imports_matching("io.kotest")
        spec_style_counts: dict[str, int] = {}
        spec_examples: list[tuple[str, int]] = []
        for style in KOTEST_SPEC_STYLES:
            # Unlimited count via count_pattern; search_pattern (small limit) is
            # only used to grab one example site per style.
            style_count = index.count_pattern(rf":\s*{style}\s*\(")
            if style_count:
                spec_style_counts[style] = style_count
                matches = index.search_pattern(rf":\s*{style}\s*\(", limit=1)
                spec_examples.extend([(r, ln) for r, ln, _ in matches])
        if kotest_import_count or spec_style_counts:
            patterns["kotest"] = {
                "name": "Kotest",
                "count": kotest_import_count or sum(spec_style_counts.values()),
            }
            examples.extend(spec_examples[:3])

        # MockK (idiomatic Kotlin mocking) vs Mockito (Java-ish alternative)
        mockk_signals = (
            index.count_imports_matching("io.mockk")
            + index.count_pattern(r"\bmockk<")
            + index.count_pattern(r"\bevery\s*\{")
            + index.count_pattern(r"\bcoEvery\s*\{")
            + index.count_pattern(r"\bverify\s*\{")
        )
        if mockk_signals:
            patterns["mockk"] = {"name": "MockK", "count": mockk_signals}
            mockk_matches = index.search_pattern(r"\bevery\s*\{", limit=5)
            examples.extend([(r, ln) for r, ln, _ in mockk_matches[:2]])

        mockito_count = index.count_imports_matching("org.mockito")
        if mockito_count:
            patterns["mockito"] = {"name": "Mockito", "count": mockito_count}

        # kotlin.test assertions
        kotlin_test_count = index.count_imports_matching("kotlin.test")
        if kotlin_test_count:
            patterns["kotlin_test"] = {"name": "kotlin.test", "count": kotlin_test_count}

        # Turbine (Flow testing)
        turbine_count = index.count_imports_matching("app.cash.turbine")
        if turbine_count:
            patterns["turbine"] = {"name": "Turbine (Flow testing)", "count": turbine_count}

        # Coroutine test support
        run_blocking_in_tests = 0
        for file_idx in test_files:
            content = "\n".join(file_idx.lines)
            run_blocking_in_tests += len(re.findall(r"\brunBlocking\s*\{", content))

        coroutine_test_signals = (
            index.count_imports_matching("kotlinx.coroutines.test")
            + index.count_pattern(r"\brunTest\s*\{")
            + index.count_pattern(r"\bTestDispatcher\b")
            + run_blocking_in_tests
        )
        uses_coroutine_test = coroutine_test_signals > 0
        if coroutine_test_signals:
            patterns["coroutine_test"] = {
                "name": "Coroutine test support (kotlinx-coroutines-test)",
                "count": coroutine_test_signals,
            }

        # Other assertion libraries
        assertj_count = index.count_imports_matching("org.assertj")
        if assertj_count:
            patterns["assertj"] = {"name": "AssertJ", "count": assertj_count}

        truth_count = index.count_imports_matching("com.google.common.truth")
        if truth_count:
            patterns["truth"] = {"name": "Truth", "count": truth_count}

        hamcrest_count = index.count_imports_matching("org.hamcrest")
        if hamcrest_count:
            patterns["hamcrest"] = {"name": "Hamcrest", "count": hamcrest_count}

        strikt_count = index.count_imports_matching("strikt.api")
        if strikt_count:
            patterns["strikt"] = {"name": "Strikt", "count": strikt_count}

        # Testcontainers
        testcontainers_count = index.count_imports_matching("org.testcontainers")
        if testcontainers_count:
            patterns["testcontainers"] = {"name": "Testcontainers", "count": testcontainers_count}

        # Backticked test names (idiomatic Kotlin)
        # Unlimited count via count_pattern -- this also backstops `total_tests`
        # below when JUnit isn't present, so it must not saturate on big repos.
        backtick_count = index.count_pattern(BACKTICK_TEST_NAME_PATTERN)
        if backtick_count:
            patterns["backtick_test_names"] = {
                "name": "Backticked test names",
                "count": backtick_count,
            }
            backtick_matches = index.search_pattern(BACKTICK_TEST_NAME_PATTERN, limit=2)
            examples.extend([(r, ln) for r, ln, _ in backtick_matches])

        if class_naming:
            patterns["test_class_naming"] = {
                "name": "Test class naming",
                "count": sum(class_naming.values()),
            }

        if not patterns:
            return result

        frameworks = [key for key in FRAMEWORK_PRIORITY if key in patterns]

        runner_candidates = {
            key: patterns[key]["count"] for key in RUNNER_FRAMEWORKS if key in patterns
        }
        if runner_candidates:
            primary_framework = max(runner_candidates, key=lambda k: runner_candidates[k])
        elif frameworks:
            primary_framework = frameworks[0]
        else:
            primary_framework = "unspecified"

        total_tests = junit_info.test_method_count
        if total_tests == 0:
            total_tests = backtick_count

        non_test_file_count = len(non_test_files)
        test_to_source_ratio = float(test_file_count) / max(1, non_test_file_count)

        # Title, e.g. "Testing: 42 tests with Kotest + MockK"
        if primary_framework in patterns:
            label_parts = [patterns[primary_framework]["name"]]
            if "mockk" in patterns and primary_framework != "mockk":
                label_parts.append("MockK")
            elif "mockito" in patterns and primary_framework != "mockito":
                label_parts.append("Mockito")
            title = f"Testing: {total_tests} tests with {' + '.join(label_parts)}"
        elif total_tests:
            title = f"Testing: {total_tests} tests"
        else:
            title = "Testing conventions detected"

        description = f"Found {test_file_count} test file(s)"
        if non_test_file_count:
            description += f" against {non_test_file_count} non-test file(s)"
        description += "."

        if junit_info.is_present:
            description += f" Uses JUnit {junit_info.major_version}"
            if junit_info.uses_parameterized:
                description += " with parameterized tests"
            description += "."

        if "kotest" in patterns:
            styles = ", ".join(sorted(spec_style_counts)) if spec_style_counts else ""
            description += f" Uses Kotest{f' ({styles})' if styles else ''} for spec-style testing."

        if "mockk" in patterns:
            description += " Uses MockK for mocking."
        elif "mockito" in patterns:
            description += " Uses Mockito for mocking."

        if uses_coroutine_test:
            description += " Has coroutine test support (kotlinx-coroutines-test)."

        if backtick_count:
            description += f" Uses backticked test names ({backtick_count} found), the idiomatic Kotlin style."

        if turbine_count:
            description += " Uses Turbine for Flow testing."

        if testcontainers_count:
            description += " Uses Testcontainers for integration tests."

        confidence = 0.4
        if junit_info.is_present:
            confidence += 0.2
        if "kotest" in patterns:
            confidence += 0.15
        if "mockk" in patterns or "mockito" in patterns:
            confidence += 0.1
        if backtick_count:
            confidence += 0.05
        if test_file_count:
            confidence += 0.05
        confidence = min(0.95, confidence)

        evidence = []
        for rel_path, line in examples[: ctx.max_evidence_snippets]:
            ev = make_evidence(index, rel_path, line, radius=3)
            if ev:
                evidence.append(ev)

        result.rules.append(self.make_rule(
            rule_id="kotlin.conventions.testing_framework",
            category="testing",
            title=title,
            description=description,
            confidence=confidence,
            language="kotlin",
            evidence=evidence,
            stats={
                "test_file_count": test_file_count,
                "non_test_file_count": non_test_file_count,
                "total_tests": total_tests,
                "frameworks": frameworks,
                "primary_framework": primary_framework,
                "patterns": list(patterns.keys()),
                "pattern_details": patterns,
                "junit_version": junit_info.major_version,
                "junit_test_method_count": junit_info.test_method_count,
                "junit_annotation_counts": junit_info.annotation_counts,
                "uses_display_name": junit_info.uses_display_name,
                "uses_nested": junit_info.uses_nested,
                "uses_parameterized": junit_info.uses_parameterized,
                "uses_mockk": "mockk" in patterns,
                "uses_coroutine_test": uses_coroutine_test,
                "backtick_test_names": backtick_count,
                "test_to_source_ratio": test_to_source_ratio,
                "kotest_spec_styles": spec_style_counts,
                "assertion_style_counts": assertion_counts,
                "test_class_naming": class_naming,
            },
        ))

        return result
