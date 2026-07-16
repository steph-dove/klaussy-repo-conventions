"""Java logging conventions detector."""

from __future__ import annotations

from typing import Optional

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import JavaDetector
from .index import make_evidence

FRAMEWORK_LABELS = {
    "slf4j": "SLF4J",
    "logback": "Logback",
    "log4j2": "Log4j2",
    "java.util.logging": "java.util.logging",
}

FRAMEWORK_PRIORITY = (
    "slf4j",
    "logback",
    "log4j2",
    "java.util.logging",
)


@DetectorRegistry.register
class JavaLoggingDetector(JavaDetector):
    """Detect Java logging framework and raw print call conventions."""

    name = "java_logging"
    description = "Detects Java logging framework and raw print call conventions"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect logging conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        build_info = self.get_build_info(ctx)

        frameworks: dict[str, int] = {}
        examples: list[tuple[str, int]] = []

        # SLF4J (including Lombok @Slf4j)
        slf4j_imports = index.count_imports_matching("org.slf4j")
        slf4j_declares = index.search_pattern(
            r"\bLoggerFactory\.getLogger\(", limit=10, exclude_tests=True
        )
        lombok_slf4j = index.count_annotation("Slf4j")
        slf4j_dep = build_info.has_dependency("slf4j") or build_info.has_dependency("spring-boot-starter-logging")

        if slf4j_imports or slf4j_declares or lombok_slf4j or slf4j_dep:
            frameworks["slf4j"] = slf4j_imports + len(slf4j_declares) + lombok_slf4j
            if slf4j_declares:
                examples.extend([(r, ln) for r, ln, _ in slf4j_declares[:2]])
            elif lombok_slf4j > 0:
                lombok_sites = index.find_annotation("Slf4j", limit=2)
                examples.extend(lombok_sites)

        # Logback
        logback_imports = index.count_imports_matching("ch.qos.logback")
        logback_dep = build_info.has_dependency("logback")
        if logback_imports or logback_dep:
            frameworks["logback"] = logback_imports + (1 if logback_dep else 0)

        # Log4j2
        log4j2_imports = index.count_imports_matching("org.apache.logging.log4j")
        log4j2_dep = build_info.has_dependency("log4j")
        if log4j2_imports or log4j2_dep:
            frameworks["log4j2"] = log4j2_imports + (1 if log4j2_dep else 0)

        # java.util.logging
        jul_imports = index.count_imports_matching("java.util.logging")
        jul_declares = index.search_pattern(
            r"\bLogger\.getLogger\(", limit=10, exclude_tests=True
        )
        if jul_imports or jul_declares:
            frameworks["java.util.logging"] = jul_imports + len(jul_declares)

        # Find raw print calls
        # Count via count_pattern; search_pattern stops at its limit, so len(...)
        # would report exactly the limit for any repo that exceeds it.
        print_call_count = index.count_pattern(r"\bSystem\.(?:out|err)\.print", exclude_tests=True)
        print_calls = index.search_pattern(r"\bSystem\.(?:out|err)\.print", exclude_tests=True, limit=5)

        # Determine primary framework
        primary: Optional[str] = None
        for fw in FRAMEWORK_PRIORITY:
            if frameworks.get(fw, 0) > 0:
                primary = fw
                break

        if primary is None and not print_call_count:
            return result

        # Compute title and description
        title_parts = []
        if primary:
            title_parts.append(FRAMEWORK_LABELS[primary])
        if lombok_slf4j > 0:
            title_parts.append("Lombok @Slf4j")
        if print_call_count:
            title_parts.append("System.out (raw print calls)")

        title = "Logging: " + ", ".join(title_parts) if title_parts else "Logging: Print statements"

        desc_parts = []
        if primary:
            desc_parts.append(f"Uses {FRAMEWORK_LABELS[primary]} for logging.")
        if lombok_slf4j > 0:
            desc_parts.append("Uses Lombok @Slf4j annotation to generate loggers automatically.")
        if print_calls:
            desc_parts.append(f"Detected {print_call_count} raw console print statements (System.out.println/print) in source code (non-test files).")

        description = " ".join(desc_parts)

        # Build evidence
        evidence = []
        # Add logger declares / Lombok annotations first
        for rel_path, line in examples[:2]:
            ev = make_evidence(index, rel_path, line, radius=3)
            if ev:
                evidence.append(ev)
        # Add print call evidence if empty
        if not evidence and print_calls:
            for rel_path, line, _ in print_calls[:2]:
                ev = make_evidence(index, rel_path, line, radius=3)
                if ev:
                    evidence.append(ev)

        stats = {
            "primary_framework": primary,
            "has_lombok_slf4j": lombok_slf4j > 0,
            "lombok_slf4j_count": lombok_slf4j,
            "raw_print_count": print_call_count,
            "frameworks": list(frameworks.keys()),
        }


        result.rules.append(self.make_rule(
            rule_id="java.conventions.logging",
            category="logging",
            title=title,
            description=description,
            confidence=0.8,
            language="java",
            evidence=evidence,
            stats=stats,
        ))

        return result
