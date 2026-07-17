"""C++ testing conventions detector."""

from __future__ import annotations

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import CPPDetector
from .index import make_evidence


@DetectorRegistry.register
class CPPTestingDetector(CPPDetector):
    """Detect C++ testing frameworks and test configurations."""

    name = "cpp_testing"
    description = "Detects C++ testing frameworks and test configurations"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect testing conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        test_files = index.get_test_files()
        test_file_count = len(test_files)

        # 1. Framework detection based on headers or test macros
        gtest_count = index.count_include("gtest/gtest") or index.count_pattern(r"\b(?:TEST|TEST_F|TEST_P)\s*\(")
        catch_count = index.count_include("catch") or index.count_pattern(r"\bTEST_CASE\s*\(\s*\"[^\"]+\"")
        doctest_count = index.count_include("doctest")

        # Pick the primary framework by weight of use, not by a fixed order.
        # Listing Google Test first reported nlohmann/json -- 158 Catch2 hits
        # against a single gtest one -- as a Google Test project. And defaulting
        # to "Google Test" when nothing at all was found claimed a framework on
        # no evidence: redis reported Google Test with all three counts at zero.
        framework_counts = {
            "Google Test": gtest_count,
            "Catch2": catch_count,
            "doctest": doctest_count,
        }
        frameworks = [name for name, count in framework_counts.items() if count > 0]

        if not frameworks and not test_file_count:
            return result

        primary_framework = (
            max(frameworks, key=lambda name: framework_counts[name]) if frameworks else None
        )

        title = (
            f"Testing: {primary_framework}"
            if primary_framework
            else f"Testing: {test_file_count} test files"
        )
        desc_parts = [
            f"C++ codebase includes {test_file_count} test files."
        ]
        if frameworks:
            desc_parts.append(f"Uses {', '.join(frameworks)} for unit testing.")
        else:
            desc_parts.append("No unit-testing framework was identified.")

        description = " ".join(desc_parts)

        # Build evidence
        evidence = []
        if primary_framework == "Google Test":
            gtest_sites = index.search_pattern(r"\b(?:TEST|TEST_F|TEST_P)\s*\(", limit=2)
            for rel_path, line, _ in gtest_sites:
                ev = make_evidence(index, rel_path, line, radius=3)
                if ev:
                    evidence.append(ev)
        else:
            catch_sites = index.search_pattern(r"\bTEST_CASE\s*\(", limit=2)
            for rel_path, line, _ in catch_sites:
                ev = make_evidence(index, rel_path, line, radius=3)
                if ev:
                    evidence.append(ev)

        stats = {
            "test_file_count": test_file_count,
            "primary_framework": primary_framework,
            "gtest_count": gtest_count,
            "catch_count": catch_count,
            "doctest_count": doctest_count,
        }

        result.rules.append(self.make_rule(
            rule_id="cpp.conventions.testing",
            category="testing",
            title=title,
            description=description,
            confidence=0.8,
            language="cpp",
            evidence=evidence,
            stats=stats,
        ))

        return result
