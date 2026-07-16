"""C# logging conventions detector."""

from __future__ import annotations

from typing import Optional

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import CSharpDetector
from .index import make_evidence

FRAMEWORK_LABELS = {
    "microsoft_logging": "Microsoft.Extensions.Logging",
    "serilog": "Serilog",
    "nlog": "NLog",
    "log4net": "log4net",
}

FRAMEWORK_PRIORITY = (
    "serilog",
    "microsoft_logging",
    "nlog",
    "log4net",
)


@DetectorRegistry.register
class CSharpLoggingDetector(CSharpDetector):
    """Detect C# logging framework and raw print call conventions."""

    name = "csharp_logging"
    description = "Detects C# logging framework and raw print call conventions"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect logging conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        frameworks: dict[str, int] = {}
        examples: list[tuple[str, int]] = []

        build_info = self.get_build_info(ctx)

        # Microsoft.Extensions.Logging.
        #
        # `ILogger` is an ordinary interface name that projects define for
        # themselves -- Newtonsoft.Json declares one in a documentation sample --
        # so it only counts as Microsoft.Extensions.Logging when that package is
        # actually imported or referenced.
        ms_logging_imports = index.count_imports_matching(
            "Microsoft.Extensions.Logging", exclude_tests=True
        )
        ms_logging_referenced = any(
            "Microsoft.Extensions.Logging" in dep for dep in build_info.production_dependencies
        )
        if ms_logging_imports or ms_logging_referenced:
            ms_logging_usages = index.count_pattern(r"\bILogger\b", exclude_tests=True)
            frameworks["microsoft_logging"] = ms_logging_imports + ms_logging_usages
            ms_logger_declares = index.search_pattern(
                r"\bILogger<\w+>", limit=2, exclude_tests=True
            )
            examples.extend([(r, ln) for r, ln, _ in ms_logger_declares])

        # Serilog
        serilog_imports = index.count_imports_matching("Serilog", exclude_tests=True)
        serilog_usages = index.count_pattern(
            r"\bLog\.Logger\b", exclude_tests=True
        ) + index.count_pattern(r"\bLoggerConfiguration\b", exclude_tests=True)
        if serilog_imports or serilog_usages:
            frameworks["serilog"] = serilog_imports + serilog_usages
            if not examples:
                serilog_sites = index.search_pattern(r"\bLog\.Logger\b", limit=2)
                examples.extend([(r, ln) for r, ln, _ in serilog_sites])

        # NLog
        nlog_imports = index.count_imports_matching("NLog", exclude_tests=True)
        if nlog_imports:
            frameworks["nlog"] = nlog_imports

        # log4net
        log4net_imports = index.count_imports_matching("log4net", exclude_tests=True)
        if log4net_imports:
            frameworks["log4net"] = log4net_imports

        # Raw console prints. The count comes from count_pattern: search_pattern
        # stops at its limit, so len(...) would report exactly the limit for any
        # repo that exceeds it.
        print_call_count = index.count_pattern(r"\bConsole\.Write(?:Line)?\b", exclude_tests=True)
        print_calls = index.search_pattern(r"\bConsole\.Write(?:Line)?\b", exclude_tests=True, limit=5)

        # Primary framework selection
        primary: Optional[str] = None
        for fw in FRAMEWORK_PRIORITY:
            if frameworks.get(fw, 0) > 0:
                primary = fw
                break

        if primary is None and not print_call_count:
            return result

        # Compile Title and Description
        title_parts = []
        if primary:
            title_parts.append(FRAMEWORK_LABELS[primary])
        if print_call_count:
            title_parts.append("Console.WriteLine")

        title = "Logging: " + ", ".join(title_parts) if title_parts else "Logging: Console output"

        desc_parts = []
        if primary:
            desc_parts.append(f"Uses {FRAMEWORK_LABELS[primary]} for application logging.")
        if print_call_count:
            desc_parts.append(f"Detected {print_call_count} console output statement(s) (Console.WriteLine) in production code.")

        description = " ".join(desc_parts)

        # Build evidence
        evidence = []
        for rel_path, line in examples[:2]:
            ev = make_evidence(index, rel_path, line, radius=3)
            if ev:
                evidence.append(ev)
        if not evidence and print_calls:
            for rel_path, line, _ in print_calls[:2]:
                ev = make_evidence(index, rel_path, line, radius=3)
                if ev:
                    evidence.append(ev)

        stats = {
            "primary_framework": primary,
            "raw_print_count": print_call_count,
            "frameworks": list(frameworks.keys()),
        }


        result.rules.append(self.make_rule(
            rule_id="csharp.conventions.logging",
            category="logging",
            title=title,
            description=description,
            confidence=0.8,
            language="csharp",
            evidence=evidence,
            stats=stats,
        ))

        return result
