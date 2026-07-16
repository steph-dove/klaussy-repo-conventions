"""Kotlin logging conventions detector."""

from __future__ import annotations

import re

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import KotlinDetector
from .index import make_evidence

LOG_LEVELS = ("trace", "debug", "info", "warn", "error")

# Human-readable framework labels, keyed by the internal signal key used below.
FRAMEWORK_LABELS = {
    "kotlin-logging": "kotlin-logging",
    "slf4j": "SLF4J",
    "logback": "Logback",
    "log4j2": "Log4j2",
    "timber": "Timber",
    "android.util.Log": "android.util.Log",
    "ktor": "Ktor call.application.log",
    "napier": "Napier",
    "kermit": "Kermit",
}

# Priority order used to pick the "primary" framework when several are present.
FRAMEWORK_PRIORITY = (
    "kotlin-logging",
    "slf4j",
    "logback",
    "log4j2",
    "timber",
    "android.util.Log",
    "ktor",
    "napier",
    "kermit",
)


@DetectorRegistry.register
class KotlinLoggingDetector(KotlinDetector):
    """Detect Kotlin logging framework and structured logging conventions."""

    name = "kotlin_logging"
    description = "Detects Kotlin logging framework and structured logging conventions"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect logging conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        build_info = self.get_build_info(ctx)

        frameworks: dict[str, int] = {}
        examples: list[tuple[str, int]] = []

        # -- kotlin-logging (the idiomatic Kotlin wrapper) ------------------
        kl_imports = index.count_imports_matching("io.github.oshai.kotlinlogging")
        kl_imports += index.count_imports_matching("mu.KotlinLogging")
        kl_declares = index.search_pattern(
            r"\bval\s+\w+\s*=\s*KotlinLogging\.logger\s*\{", limit=10, exclude_tests=True
        )
        kl_dep = build_info.has_dependency("kotlin-logging") or build_info.has_dependency(
            "io.github.oshai"
        )
        if kl_imports or kl_declares or kl_dep:
            frameworks["kotlin-logging"] = kl_imports + len(kl_declares)
            examples.extend([(r, ln) for r, ln, _ in kl_declares[:2]])

        # -- SLF4J ------------------------------------------------------------
        slf4j_imports = index.count_imports_matching("org.slf4j")
        slf4j_declares = index.search_pattern(
            r"\bval\s+\w+\s*=\s*LoggerFactory\.getLogger\(", limit=10, exclude_tests=True
        )
        slf4j_dep = build_info.has_dependency("slf4j")
        if slf4j_imports or slf4j_declares or slf4j_dep:
            frameworks["slf4j"] = slf4j_imports + len(slf4j_declares)
            if not examples:
                examples.extend([(r, ln) for r, ln, _ in slf4j_declares[:2]])

        # -- Logback / Log4j2 backends -----------------------------------
        logback_imports = index.count_imports_matching("ch.qos.logback")
        logback_dep = build_info.has_dependency("logback")
        if logback_imports or logback_dep:
            frameworks["logback"] = logback_imports

        log4j2_imports = index.count_imports_matching("org.apache.logging.log4j")
        log4j2_dep = build_info.has_dependency("log4j")
        if log4j2_imports or log4j2_dep:
            frameworks["log4j2"] = log4j2_imports

        # -- Timber (Android) --------------------------------------------
        timber_imports = index.count_imports_matching("timber.log.Timber")
        timber_calls = index.count_pattern(r"\bTimber\.(?:v|d|i|w|e|wtf)\s*\(", exclude_tests=True)
        timber_dep = build_info.has_dependency("timber")
        if timber_imports or timber_calls or timber_dep:
            frameworks["timber"] = timber_imports + timber_calls

        # -- Raw android.util.Log -----------------------------------------
        android_log_imports = index.count_imports_matching("android.util.Log")
        android_log_calls = index.count_pattern(r"\bLog\.(?:v|d|i|w|e)\s*\(", exclude_tests=True)
        if android_log_imports or android_log_calls:
            frameworks["android.util.Log"] = android_log_imports + android_log_calls

        # -- Ktor's call.application.log -----------------------------------
        ktor_calls = index.count_pattern(
            r"\bcall\.application\.log\b|\bapplication\.log\.(?:trace|debug|info|warn|error)\s*\(",
            exclude_tests=True,
        )
        if ktor_calls:
            frameworks["ktor"] = ktor_calls

        # -- Multiplatform loggers: Napier, Kermit --------------------------
        napier_imports = index.count_imports_matching("io.github.aakira.napier")
        napier_calls = index.count_pattern(r"\bNapier\.(?:v|d|i|w|e)\s*\(", exclude_tests=True)
        napier_dep = build_info.has_dependency("napier")
        if napier_imports or napier_calls or napier_dep:
            frameworks["napier"] = napier_imports + napier_calls

        kermit_imports = index.count_imports_matching("co.touchlab.kermit")
        kermit_dep = build_info.has_dependency("kermit")
        if kermit_imports or kermit_dep:
            frameworks["kermit"] = kermit_imports

        # -- Logger call sites: lazy lambda vs eager string ------------------
        lazy_logging_count = index.count_pattern(
            r"\b(?:logger|log)\.(?:trace|debug|info|warn|error)\s*\{", exclude_tests=True
        )
        eager_logging_count = index.count_pattern(
            r"\b(?:logger|log)\.(?:trace|debug|info|warn|error)\s*\(", exclude_tests=True
        )
        logger_call_count = lazy_logging_count + eager_logging_count

        levels: list[str] = []
        for level in LOG_LEVELS:
            level_count = index.count_pattern(
                rf"\b(?:logger|log)\.{level}\s*[({{]", exclude_tests=True
            )
            if level_count:
                levels.append(level)

        # -- Structured logging / MDC ---------------------------------------
        mdc_count = index.count_pattern(r"\bMDC\.(?:put|remove|clear)\s*\(", exclude_tests=True)
        logging_context_count = index.count_pattern(r"\bwithLoggingContext\s*\(", exclude_tests=True)
        uses_structured_logging = (mdc_count + logging_context_count) > 0

        # -- println/print() in production code (anti-pattern) --------------
        # search_pattern's limit doesn't support role filtering, so the unlimited
        # count is computed directly here rather than via count_pattern; a small
        # separate search_pattern call below gathers a couple of example sites.
        println_pattern = re.compile(r"\b(?:println|print)\s*\(")
        println_in_production = sum(
            len(println_pattern.findall("\n".join(f.lines)))
            for f in index.files.values()
            if not f.is_test and f.role != "build"
        )
        if println_in_production and len(examples) < ctx.max_evidence_snippets:
            println_matches = index.search_pattern(
                r"\b(?:println|print)\s*\(", limit=10, exclude_tests=True
            )
            println_matches = [
                (rel_path, line, matched)
                for rel_path, line, matched in println_matches
                if index.files[rel_path].role != "build"
            ]
            examples.extend([(r, ln) for r, ln, _ in println_matches[:2]])

        if not frameworks and not println_in_production:
            return result

        # -- Companion-object logger holder idiom ----------------------------
        companion_holder_count = index.count_pattern(
            r"companion object\s*\{[\s\S]{0,300}?\bval\s+\w*[Ll]og(?:ger)?\s*=",
            exclude_tests=True,
        )

        patterns: list[str] = []
        if kl_declares:
            patterns.append("KotlinLogging.logger {} declaration")
        if slf4j_declares:
            patterns.append("LoggerFactory.getLogger() declaration")
        if companion_holder_count:
            patterns.append("companion object logger holder")
        if lazy_logging_count:
            patterns.append("lazy lambda logging")
        if eager_logging_count:
            patterns.append("eager string logging")
        if uses_structured_logging:
            patterns.append("structured logging / MDC context")
        if println_in_production:
            patterns.append("println in production code (anti-pattern)")

        # -- Determine primary framework -------------------------------------
        primary = "none"
        for candidate in FRAMEWORK_PRIORITY:
            if candidate in frameworks:
                primary = candidate
                break

        if primary == "slf4j":
            backend = "logback" if "logback" in frameworks else ("log4j2" if "log4j2" in frameworks else None)
            framework_label = FRAMEWORK_LABELS["slf4j"] + (
                f" + {FRAMEWORK_LABELS[backend]}" if backend else ""
            )
        elif primary != "none":
            framework_label = FRAMEWORK_LABELS[primary]
        else:
            framework_label = "println" if println_in_production else "unknown"

        # -- Title -------------------------------------------------------------
        if primary == "kotlin-logging":
            style = "lazy lambda messages" if lazy_logging_count >= eager_logging_count else "eager string messages"
            title = f"Logging: {framework_label} with {style}"
        elif primary == "none":
            title = "Logging: println in production code" if println_in_production else "Logging: no framework detected"
        else:
            title = f"Logging: {framework_label}"

        # -- Description ---------------------------------------------------
        description_parts: list[str] = []
        if frameworks:
            call_suffix = f" ({logger_call_count} call site(s))" if logger_call_count else ""
            description_parts.append(f"Uses {framework_label} for logging{call_suffix}.")
        else:
            description_parts.append("No structured logging framework detected.")

        if lazy_logging_count and eager_logging_count:
            description_parts.append(
                f"{lazy_logging_count} lazy lambda log call(s) vs {eager_logging_count} eager call(s)."
            )
        if eager_logging_count > lazy_logging_count and eager_logging_count > 0:
            description_parts.append(
                "Eager string logging dominates; prefer lazy lambda logging "
                '(`logger.info { "..." }`) to avoid building messages when the level is disabled.'
            )

        if println_in_production:
            description_parts.append(
                f"Found {println_in_production} println()/print() call(s) in production code; "
                "prefer the logging framework over raw console output."
            )

        if uses_structured_logging:
            description_parts.append("Uses structured logging context (MDC / withLoggingContext).")

        description = " ".join(description_parts)

        # -- Confidence ----------------------------------------------------
        confidence = 0.3
        if frameworks:
            confidence += 0.35
            if len(frameworks) > 1:
                confidence += 0.05
        if logger_call_count >= 5:
            confidence += 0.1
        if logger_call_count >= 20:
            confidence += 0.05
        if uses_structured_logging:
            confidence += 0.05
        if println_in_production and not frameworks:
            confidence += 0.1
        confidence = min(confidence, 0.95)

        evidence = []
        for rel_path, line in examples[: ctx.max_evidence_snippets]:
            ev = make_evidence(index, rel_path, line, radius=3)
            if ev:
                evidence.append(ev)

        result.rules.append(
            self.make_rule(
                rule_id="kotlin.conventions.logging_library",
                category="logging",
                title=title,
                description=description,
                confidence=confidence,
                language="kotlin",
                evidence=evidence,
                stats={
                    "frameworks": list(frameworks.keys()),
                    "primary_framework": primary,
                    # CLAUDE.md's tech-stack renderer reads `primary_library` for
                    # logging_library rules.
                    "primary_library": primary,
                    "logger_call_count": logger_call_count,
                    "lazy_logging_count": lazy_logging_count,
                    "eager_logging_count": eager_logging_count,
                    "println_in_production": println_in_production,
                    "levels": levels,
                    "uses_structured_logging": uses_structured_logging,
                    "patterns": patterns,
                },
            )
        )

        return result
