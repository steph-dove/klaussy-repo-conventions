"""C# testing conventions detector."""

from __future__ import annotations

from typing import Optional

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import CSharpDetector
from .index import make_evidence

FRAMEWORK_PRIORITY = (
    "xunit",
    "nunit",
    "mstest",
    "moq",
    "nsubstitute",
)

RUNNER_FRAMEWORKS = ("xunit", "nunit", "mstest")


@DetectorRegistry.register
class CSharpTestingDetector(CSharpDetector):
    """Detect C# testing frameworks, assertion styles and test organization."""

    name = "csharp_testing"
    description = "Detects C# testing frameworks, assertion styles and test organization"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect testing conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        test_files = index.get_test_files()
        test_file_count = len(test_files)

        patterns: dict[str, dict] = {}
        examples: list[tuple[str, int]] = []

        # xUnit
        xunit_imports = index.count_imports_matching("Xunit")
        xunit_facts = index.count_annotation("Fact") + index.count_annotation("Theory")
        if xunit_imports or xunit_facts:
            patterns["xunit"] = {
                "name": "xUnit",
                "count": xunit_facts or 1,
            }
            fact_sites = index.find_annotation("Fact", limit=2) or index.find_annotation("Theory", limit=2)
            examples.extend(fact_sites)

        # NUnit
        nunit_imports = index.count_imports_matching("NUnit")
        nunit_tests = index.count_annotation("Test") + index.count_annotation("TestCase")
        if nunit_imports or nunit_tests:
            patterns["nunit"] = {
                "name": "NUnit",
                "count": nunit_tests or 1,
            }
            if not examples:
                nunit_sites = index.find_annotation("Test", limit=2)
                examples.extend(nunit_sites)

        # MSTest
        mstest_imports = index.count_imports_matching("Microsoft.VisualStudio.TestTools.UnitTesting")
        mstest_tests = index.count_annotation("TestMethod")
        if mstest_imports or mstest_tests:
            patterns["mstest"] = {
                "name": "MSTest",
                "count": mstest_tests or 1,
            }
            if not examples:
                mstest_sites = index.find_annotation("TestMethod", limit=2)
                examples.extend(mstest_sites)

        # Moq
        moq_imports = index.count_imports_matching("Moq")
        if moq_imports:
            patterns["moq"] = {
                "name": "Moq",
                "count": moq_imports,
            }

        # NSubstitute
        nsubstitute_imports = index.count_imports_matching("NSubstitute")
        if nsubstitute_imports:
            patterns["nsubstitute"] = {
                "name": "NSubstitute",
                "count": nsubstitute_imports,
            }

        if not patterns and not test_file_count:
            return result

        # Determine primary runner
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

        # Compute title and description
        runner_label = patterns[primary_framework]["name"] if primary_framework else "Unit testing"
        title = f"Testing: {runner_label}"

        desc_parts = [
            f"C# codebase includes {test_file_count} test files."
        ]
        active_fws = [v["name"] for v in patterns.values()]
        if active_fws:
            desc_parts.append(f"Uses {', '.join(active_fws)} frameworks.")

        # Naming style checks
        class_naming_counts = {
            "suffix_tests": index.count_pattern(r"\bclass\s+\w+Tests\b"),
            "suffix_test": index.count_pattern(r"\bclass\s+\w+Test\b"),
            "suffix_specs": index.count_pattern(r"\bclass\s+\w+Specs\b"),
            "suffix_spec": index.count_pattern(r"\bclass\s+\w+Spec\b"),
        }
        primary_naming = "unknown"
        if any(class_naming_counts.values()):
            primary_naming = max(class_naming_counts, key=lambda name: class_naming_counts[name])
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
            "class_naming": class_naming_counts,
            "primary_naming": primary_naming,
        }

        result.rules.append(self.make_rule(
            rule_id="csharp.conventions.testing",
            category="testing",
            title=title,
            description=description,
            confidence=0.8,
            language="csharp",
            evidence=evidence,
            stats=stats,
        ))

        return result
