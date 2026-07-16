"""Java testing conventions detector."""

from __future__ import annotations

from typing import Optional

from ..base import DetectorContext, DetectorResult
from ..jvm.junit import count_assertion_style, detect_junit, find_test_class_naming
from ..registry import DetectorRegistry
from .base import JavaDetector
from .index import make_evidence

FRAMEWORK_PRIORITY = (
    "junit5",
    "junit4",
    "testng",
    "mockito",
    "assertj",
    "hamcrest",
    "testcontainers",
)

RUNNER_FRAMEWORKS = ("junit5", "junit4", "testng")


@DetectorRegistry.register
class JavaTestingDetector(JavaDetector):
    """Detect Java testing frameworks, assertion styles and test organization."""

    name = "java_testing"
    description = "Detects Java testing frameworks, assertion styles and test organization"

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
        test_file_count = len(test_files)

        patterns: dict[str, dict] = {}
        examples: list[tuple[str, int]] = []

        # JUnit 4 vs 5
        if junit_info.is_present:
            key = f"junit{junit_info.major_version}"
            patterns[key] = {
                "name": f"JUnit {junit_info.major_version}",
                "count": junit_info.test_method_count,
            }
            examples.extend(junit_info.examples[:3])

        # TestNG
        testng_imports = index.count_imports_matching("org.testng")
        testng_tests = index.count_pattern(r"@org\.testng\.annotations\.Test\b") + index.count_pattern(r"@Test\b") * (1 if testng_imports else 0)
        if testng_imports or testng_tests:
            patterns["testng"] = {
                "name": "TestNG",
                "count": testng_tests or 1,
            }
            if not examples:
                testng_sites = index.search_pattern(r"@Test\b", limit=3)
                examples.extend([(r, ln) for r, ln, _ in testng_sites])

        # Mockito
        mockito_imports = index.count_imports_matching("org.mockito")
        if mockito_imports > 0:
            patterns["mockito"] = {
                "name": "Mockito",
                "count": mockito_imports,
            }

        # AssertJ
        assertj_imports = index.count_imports_matching("org.assertj")
        assertj_calls = assertion_counts.get("assertj", 0)
        if assertj_imports or assertj_calls:
            patterns["assertj"] = {
                "name": "AssertJ",
                "count": assertj_calls or assertj_imports,
            }

        # Hamcrest
        hamcrest_imports = index.count_imports_matching("org.hamcrest")
        if hamcrest_imports:
            patterns["hamcrest"] = {
                "name": "Hamcrest",
                "count": hamcrest_imports,
            }

        # Testcontainers
        testcontainers_imports = index.count_imports_matching("org.testcontainers")
        if testcontainers_imports:
            patterns["testcontainers"] = {
                "name": "Testcontainers",
                "count": testcontainers_imports,
            }

        if not patterns and not test_file_count:
            return result

        # Primary runner/framework
        primary_runner: Optional[str] = None
        for fw in FRAMEWORK_PRIORITY:
            if fw in RUNNER_FRAMEWORKS and fw in patterns:
                primary_runner = fw
                break

        primary_library: Optional[str] = None
        for fw in FRAMEWORK_PRIORITY:
            if fw in patterns:
                primary_library = fw
                break

        primary_framework = primary_runner or primary_library

        # Test naming style
        primary_naming = "unknown"
        if class_naming:
            primary_naming = max(class_naming, key=class_naming.get)

        # Assertion style
        primary_assertion = "junit"
        max_assert = 0
        for style, count in assertion_counts.items():
            if count > max_assert:
                max_assert = count
                primary_assertion = style.replace("_assertions", "")

        # Compute title
        runner_label = patterns[primary_framework]["name"] if primary_framework else "Unit testing"
        style_labels = []
        if primary_naming != "unknown":
            style_labels.append(primary_naming.replace("_", " "))
        if primary_assertion != "junit":
            style_labels.append(f"{primary_assertion} assertions")

        title = f"Testing: {runner_label}"
        if style_labels:
            title += f" ({', '.join(style_labels)})"

        # Description
        desc_parts = [
            f"Java codebase includes {test_file_count} test files."
        ]
        active_fws = [v["name"] for v in patterns.values()]
        if active_fws:
            desc_parts.append(f"Uses {', '.join(active_fws)} frameworks.")
        if primary_naming != "unknown":
            desc_parts.append(f"Test classes are primarily named with a {primary_naming.replace('_', ' ')} convention.")

        description = " ".join(desc_parts)

        # Build evidence
        evidence = []
        for rel_path, line in examples[:ctx.max_evidence_snippets]:
            ev = make_evidence(index, rel_path, line, radius=3)
            if ev:
                evidence.append(ev)

        stats = {
            "test_file_count": test_file_count,
            "frameworks": active_fws,
            "primary_framework": primary_framework,
            "class_naming": class_naming,
            "primary_naming": primary_naming,
            "assertion_counts": assertion_counts,
            "primary_assertion": primary_assertion,
            "junit_info": {
                "version": junit_info.major_version,
                "has_parameterized": junit_info.uses_parameterized,
                "has_nested": junit_info.uses_nested,
                "has_display_name": junit_info.uses_display_name,
            } if junit_info.is_present else None,
        }

        result.rules.append(self.make_rule(
            rule_id="java.conventions.testing",
            category="testing",
            title=title,
            description=description,
            confidence=0.8,
            language="java",
            evidence=evidence,
            stats=stats,
        ))

        return result
