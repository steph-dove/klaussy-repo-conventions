"""Java coding style and language conventions detector."""

from __future__ import annotations

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import JavaDetector
from .index import make_evidence


@DetectorRegistry.register
class JavaConventionsDetector(JavaDetector):
    """Detect Java-specific coding conventions (Records, Lombok, Streams, Optionals)."""

    name = "java_conventions"
    description = "Detects Java-specific coding conventions (Records, Lombok, Streams, Optionals)"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect coding conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        # 1. Lombok vs Java Records
        #
        # Lombok's annotation names are not unique to Lombok -- Spring's
        # @Value (property injection) is far more common than Lombok's @Value
        # in a Spring codebase -- so only attribute them when Lombok is actually
        # imported or declared as a dependency.
        build_info = self.get_build_info(ctx)
        uses_lombok = (
            index.count_imports_matching("lombok") > 0 or build_info.has_dependency("lombok")
        )
        if uses_lombok:
            lombok_data = index.count_annotation("Data")
            lombok_value = index.count_annotation("Value")
            lombok_builder = index.count_annotation("Builder")
            lombok_getter_setter = (
                index.count_annotation("Getter") + index.count_annotation("Setter")
            )
            lombok_count = lombok_data + lombok_value + lombok_builder + lombok_getter_setter
        else:
            lombok_data = lombok_value = lombok_builder = lombok_getter_setter = 0
            lombok_count = 0

        # count_pattern, not len(search_pattern(...)): the latter stops at its
        # limit and would cap the record count.
        records_count = index.count_pattern(r"\brecord\s+\w+\s*\(", exclude_tests=True)

        # Determine primary data class convention
        data_class_style = "standard classes (POJOs)"
        if lombok_count > 0 and lombok_count >= records_count:
            data_class_style = "Lombok annotations"
        elif records_count > 0 and records_count >= lombok_count:
            data_class_style = "Java Records"

        # 2. Streams & Lambdas vs traditional loops
        stream_count = sum(f.stream_count for f in index.files.values())
        lambda_count = sum(f.lambda_count for f in index.files.values())
        for_loops = index.count_pattern(r"\bfor\s*\(", exclude_tests=True)
        while_loops = index.count_pattern(r"\bwhile\s*\(", exclude_tests=True)
        loops_count = for_loops + while_loops

        fp_style = "traditional loops"
        if stream_count > 0 or lambda_count > 0:
            if (stream_count + lambda_count) > loops_count:
                fp_style = "functional (Streams & Lambdas)"
            else:
                fp_style = "hybrid (mixed loops and Streams)"

        # 3. Optional vs null checks
        optional_count = sum(f.optional_count for f in index.files.values())
        null_checks = index.count_pattern(r"==\s*null\b", exclude_tests=True) + index.count_pattern(r"!=\s*null\b", exclude_tests=True)

        null_safety_style = "standard null checks (== null)"
        if optional_count > 0:
            if optional_count > null_checks:
                null_safety_style = "Optional wrapper type"
            else:
                null_safety_style = "mixed (Optional & null checks)"

        # Compile Title and Description
        title = f"Conventions: {data_class_style}, {fp_style} processing, {null_safety_style}"

        desc_parts = []
        if lombok_count > 0:
            desc_parts.append(f"Uses Lombok annotations ({lombok_count} annotations found) to boilerplate getters, setters, builders, and data classes.")
        if records_count > 0:
            desc_parts.append(f"Uses native Java Records ({records_count} records found) for lightweight data structures.")
        if lombok_count == 0 and records_count == 0:
            desc_parts.append("Uses standard POJO patterns (manually generated getters/setters/constructors) for data structures.")

        if stream_count > 0:
            desc_parts.append(f"Utilizes Java Stream API ({stream_count} stream operations) and lambdas ({lambda_count} arrows) for data manipulation.")
        else:
            desc_parts.append("Uses traditional imperative loops for collection traversal.")

        if optional_count > 0:
            desc_parts.append(f"Uses java.util.Optional ({optional_count} instances) to manage null values.")

        description = " ".join(desc_parts)

        # Build evidence
        evidence = []
        # Add Record evidence
        if records_count > 0:
            records = index.search_pattern(r"\brecord\s+\w+\s*\(", exclude_tests=True, limit=1)
            if records:
                ev = make_evidence(index, records[0][0], records[0][1], radius=3)
                if ev:
                    evidence.append(ev)
        # Add Lombok evidence
        if lombok_count > 0 and len(evidence) < ctx.max_evidence_snippets:
            lombok_sites = index.find_annotation("Data", limit=1) or index.find_annotation("Value", limit=1)
            if lombok_sites:
                ev = make_evidence(index, lombok_sites[0][0], lombok_sites[0][1], radius=3)
                if ev:
                    evidence.append(ev)
        # Add Stream evidence
        if stream_count > 0 and len(evidence) < ctx.max_evidence_snippets:
            streams = index.search_pattern(r"\.stream\b", exclude_tests=True, limit=1)
            if streams:
                ev = make_evidence(index, streams[0][0], streams[0][1], radius=3)
                if ev:
                    evidence.append(ev)

        stats = {
            "lombok_count": lombok_count,
            "records_count": records_count,
            "data_class_style": data_class_style,
            "stream_count": stream_count,
            "lambda_count": lambda_count,
            "loop_count": loops_count,
            "fp_style": fp_style,
            "optional_count": optional_count,
            "null_check_count": null_checks,
            "null_safety_style": null_safety_style,
        }

        result.rules.append(self.make_rule(
            rule_id="java.conventions.general",
            category="style",
            title=title,
            description=description,
            confidence=0.8,
            language="java",
            evidence=evidence,
            stats=stats,
        ))

        # 4. Error Handling
        try_catch_count = index.count_pattern(r"\btry\s*\{", exclude_tests=True)
        custom_exceptions_count = index.count_pattern(r"class\s+\w+Exception\s+extends\s+(?:Exception|RuntimeException)\b", exclude_tests=True)

        errors_title = "Error Handling: Standard exceptions"
        if custom_exceptions_count > 0:
            errors_title = "Error Handling: Custom Exception taxonomy"

        errors_desc = f"Uses try-catch blocks ({try_catch_count} found) and declares {custom_exceptions_count} custom Exception classes."
        errors_evidence = []
        if try_catch_count > 0:
            tc_sites = index.search_pattern(r"\btry\s*\{", exclude_tests=True, limit=1)
            if tc_sites:
                ev = make_evidence(index, tc_sites[0][0], tc_sites[0][1], radius=3)
                if ev:
                    errors_evidence.append(ev)

        result.rules.append(self.make_rule(
            rule_id="java.conventions.errors",
            category="errors",
            title=errors_title,
            description=errors_desc,
            confidence=0.8,
            language="java",
            evidence=errors_evidence,
            stats={
                "try_catch_count": try_catch_count,
                "custom_exceptions_count": custom_exceptions_count,
            },
        ))

        # 5. Security & Secrets
        has_raw_sql_usage = index.count_pattern(r'\b(?:createNativeQuery|createSQLQuery|jdbcTemplate\.query)\b', exclude_tests=True) > 0
        security_title = "Security: Secure settings"
        if has_raw_sql_usage:
            security_title = "Security: Raw SQL injection risk"

        security_desc = "Checks for secure configurations."
        if has_raw_sql_usage:
            security_desc += " Warning: Detected raw native SQL query API usage (e.g. createNativeQuery / jdbcTemplate.query)."

        result.rules.append(self.make_rule(
            rule_id="java.conventions.security",
            category="security",
            title=security_title,
            description=security_desc,
            confidence=0.8,
            language="java",
            evidence=[],
            stats={
                "has_raw_sql_usage": has_raw_sql_usage,
            },
        ))

        # 6. Concurrency
        concurrency_primitives_count = index.count_pattern(r'\b(?:synchronized|ReentrantLock|CompletableFuture|ExecutorService)\b', exclude_tests=True)
        concurrency_title = "Concurrency: JVM Threads"
        concurrency_desc = f"Uses standard JVM concurrency or asynchronous structures ({concurrency_primitives_count} primitives like synchronized/CompletableFuture)."

        result.rules.append(self.make_rule(
            rule_id="java.conventions.concurrency",
            category="concurrency",
            title=concurrency_title,
            description=concurrency_desc,
            confidence=0.8,
            language="java",
            evidence=[],
            stats={
                "concurrency_primitives_count": concurrency_primitives_count,
            },
        ))

        return result
