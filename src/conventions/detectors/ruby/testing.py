"""Ruby testing conventions detector."""

from __future__ import annotations

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import RubyDetector
from .index import make_evidence


@DetectorRegistry.register
class RubyTestingDetector(RubyDetector):
    """Detect Ruby testing frameworks, assertion styles and test organization."""

    name = "ruby_testing"
    description = "Detects Ruby testing frameworks, assertion styles and test organization"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect testing conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        test_files = index.get_test_files()
        test_file_count = len(test_files)

        frameworks = []
        if index.count_gem("rspec") or index.count_gem("rspec-rails") or ctx.repo_root.joinpath("spec").exists():
            frameworks.append("RSpec")
        if index.count_gem("minitest") or ctx.repo_root.joinpath("test").exists():
            # If spec exists, RSpec is usually preferred, but Minitest could be the default Rails test setup
            if not frameworks:
                frameworks.append("Minitest")

        if not frameworks and not test_file_count:
            return result

        primary_framework = frameworks[0] if frameworks else "Minitest"

        # Check for spec vs unit test naming
        spec_naming_count = len([f for f in test_files if f.relative_path.endswith("_spec.rb")])
        test_naming_count = len([f for f in test_files if f.relative_path.endswith("_test.rb")])

        primary_naming = "suffix_spec" if spec_naming_count >= test_naming_count else "suffix_test"

        title = f"Testing: {primary_framework}"

        desc_parts = [
            f"Ruby codebase includes {test_file_count} test files."
        ]
        if frameworks:
            noun = "framework" if len(frameworks) == 1 else "frameworks"
            desc_parts.append(f"Uses the {', '.join(frameworks)} {noun}.")
        desc_parts.append(f"Test files are organized with a {primary_naming.replace('_', ' ')} convention.")

        description = " ".join(desc_parts)

        # Build evidence
        evidence = []
        if primary_framework == "RSpec":
            rspec_sites = index.search_pattern(r"\bdescribe\s+['\"].*['\"]\s+do\b", limit=2)
            for rel_path, line, _ in rspec_sites:
                ev = make_evidence(index, rel_path, line, radius=3)
                if ev:
                    evidence.append(ev)
        else:
            test_sites = index.search_pattern(r"\bclass\s+\w+Test\s*<\s*ActiveSupport::TestCase\b", limit=2)
            for rel_path, line, _ in test_sites:
                ev = make_evidence(index, rel_path, line, radius=3)
                if ev:
                    evidence.append(ev)

        stats = {
            "test_file_count": test_file_count,
            "frameworks": frameworks,
            "primary_framework": primary_framework,
            "primary_naming": primary_naming,
            "spec_naming_count": spec_naming_count,
            "test_naming_count": test_naming_count,
        }

        result.rules.append(self.make_rule(
            rule_id="ruby.conventions.testing",
            category="testing",
            title=title,
            description=description,
            confidence=0.8,
            language="ruby",
            evidence=evidence,
            stats=stats,
        ))

        return result
