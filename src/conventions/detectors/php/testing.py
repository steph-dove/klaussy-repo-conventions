"""PHP testing conventions detector."""

from __future__ import annotations

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import PHPDetector
from .index import make_evidence


@DetectorRegistry.register
class PHPTestingDetector(PHPDetector):
    """Detect PHP testing frameworks and structure."""

    name = "php_testing"
    description = "Detects PHP testing frameworks and structure"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect testing conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        test_files = index.get_test_files()
        test_file_count = len(test_files)

        phpunit_count = index.count_dependency("phpunit/phpunit") or \
                        index.count_pattern(r"extends\s+TestCase\b") or \
                        index.count_pattern(r"extends\s+PHPUnit\\Framework\\TestCase\b")

        pest_count = index.count_dependency("pestphp/pest") or \
                     index.count_pattern(r"\b(?:test|it)\s*\(\s*['\"][^'\"]+['\"]\s*,\s*function\b")

        frameworks = []
        if pest_count > 0:
            frameworks.append("Pest")
        if phpunit_count > 0 or not frameworks:
            # PHPUnit is the fallback standard in PHP
            frameworks.append("PHPUnit")

        if not frameworks and not test_file_count:
            return result

        primary_framework = frameworks[0] if frameworks else "PHPUnit"

        title = f"Testing: {primary_framework}"
        desc_parts = [
            f"PHP codebase includes {test_file_count} test files."
        ]
        if frameworks:
            desc_parts.append(f"Uses {', '.join(frameworks)} for unit testing.")

        description = " ".join(desc_parts)

        # Build evidence
        evidence = []
        if primary_framework == "Pest":
            pest_sites = index.search_pattern(r"\b(?:test|it)\s*\(\s*['\"][^'\"]+['\"]\s*,\s*function\b", limit=2)
            for rel_path, line, _ in pest_sites:
                ev = make_evidence(index, rel_path, line, radius=3)
                if ev:
                    evidence.append(ev)
        else:
            phpunit_sites = index.search_pattern(r"extends\s+TestCase\b", limit=2)
            for rel_path, line, _ in phpunit_sites:
                ev = make_evidence(index, rel_path, line, radius=3)
                if ev:
                    evidence.append(ev)

        stats = {
            "test_file_count": test_file_count,
            "primary_framework": primary_framework,
            "phpunit_count": phpunit_count,
            "pest_count": pest_count,
        }

        result.rules.append(self.make_rule(
            rule_id="php.conventions.testing",
            category="testing",
            title=title,
            description=description,
            confidence=0.8,
            language="php",
            evidence=evidence,
            stats=stats,
        ))

        return result
