"""Swift testing conventions detector."""

from __future__ import annotations

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import SwiftDetector
from .index import make_evidence


@DetectorRegistry.register
class SwiftTestingDetector(SwiftDetector):
    """Detect Swift testing frameworks and organization."""

    name = "swift_testing"
    description = "Detects Swift testing frameworks and organization"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect testing conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        test_files = index.get_test_files()
        test_file_count = len(test_files)

        xctest_count = index.count_import("XCTest") or index.count_pattern(r":\s*XCTestCase\b")
        swift_testing_count = index.count_import("Testing") or index.count_pattern(r"@Test\b")

        # Pick the primary framework by weight of use, not by a fixed order.
        # Alamofire imports XCTest in 31 files and swift-testing in 5; listing
        # swift-testing first reported it as the primary framework regardless.
        # A tie favours swift-testing, which is the direction Apple is moving.
        framework_counts = {
            "swift-testing": swift_testing_count,
            "XCTest": xctest_count,
        }
        frameworks = [name for name, count in framework_counts.items() if count > 0]

        if not frameworks and not test_file_count:
            return result

        primary_framework = (
            max(frameworks, key=lambda name: framework_counts[name])
            if frameworks
            else "XCTest"
        )

        title = f"Testing: {primary_framework}"
        desc_parts = [
            f"Swift codebase includes {test_file_count} test files."
        ]
        if frameworks:
            desc_parts.append(f"Uses {', '.join(frameworks)} for unit testing.")

        description = " ".join(desc_parts)

        # Build evidence
        evidence = []
        if primary_framework == "swift-testing":
            test_sites = index.search_pattern(r"@Test\b", limit=2)
            for rel_path, line, _ in test_sites:
                ev = make_evidence(index, rel_path, line, radius=3)
                if ev:
                    evidence.append(ev)
        else:
            xctest_sites = index.search_pattern(r":\s*XCTestCase\b", limit=2)
            for rel_path, line, _ in xctest_sites:
                ev = make_evidence(index, rel_path, line, radius=3)
                if ev:
                    evidence.append(ev)

        stats = {
            "test_file_count": test_file_count,
            "primary_framework": primary_framework,
            "xctest_count": xctest_count,
            "swift_testing_count": swift_testing_count,
        }

        result.rules.append(self.make_rule(
            rule_id="swift.conventions.testing",
            category="testing",
            title=title,
            description=description,
            confidence=0.8,
            language="swift",
            evidence=evidence,
            stats=stats,
        ))

        return result
