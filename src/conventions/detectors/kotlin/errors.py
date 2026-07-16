"""Kotlin error handling conventions detector."""

from __future__ import annotations

import re

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import KotlinDetector
from .index import make_evidence

SEALED_ERROR_NAME_RE = r"(Error|Result|Failure|Exception|State)"

EMPTY_CATCH_RE = r"catch\s*\([^)]*\)\s*\{\s*(?://[^\n]*\s*)*\}"
BROAD_CATCH_RE = r"catch\s*\(\s*\w+\s*:\s*(?:Exception|Throwable)\s*\)"


@DetectorRegistry.register
class KotlinErrorHandlingDetector(KotlinDetector):
    """Detect Kotlin error-handling and result-modeling conventions."""

    name = "kotlin_error_handling"
    description = "Detects Kotlin error-handling and result-modeling conventions"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect error handling conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        patterns: list[str] = []
        good_examples: list[tuple[str, int]] = []
        bad_examples: list[tuple[str, int]] = []

        # --- kotlin.Result / runCatching idiom -----------------------------
        # Count unlimited via count_pattern; search_pattern is only used below
        # (with a small limit) to gather a few example sites.
        runcatching_count = index.count_pattern(r"\brunCatching\s*\{", exclude_tests=True)
        getorelse_count = index.count_pattern(r"\.getOrElse\s*\(", exclude_tests=True)
        getornull_count = index.count_pattern(r"\.getOrNull\s*\(", exclude_tests=True)
        getorthrow_count = index.count_pattern(r"\.getOrThrow\s*\(", exclude_tests=True)
        fold_count = index.count_pattern(r"\.fold\s*\(", exclude_tests=True)

        if runcatching_count:
            patterns.append("runCatching")
            runcatching_hits = index.search_pattern(r"\brunCatching\s*\{", limit=3, exclude_tests=True)
            good_examples.extend([(r, ln) for r, ln, _ in runcatching_hits])
        if getorelse_count or getornull_count or getorthrow_count or fold_count:
            patterns.append("result-combinators")

        # --- Result<...> / kotlin.Result return types -----------------------
        result_type_hits = index.search_pattern(
            r"\bResult\s*<|\bkotlin\.Result\b", limit=20, exclude_tests=True
        )
        uses_result_type = bool(result_type_hits) or runcatching_count > 0
        if result_type_hits:
            patterns.append("result-type")
            good_examples.extend([(r, ln) for r, ln, _ in result_type_hits[:2]])

        # --- Arrow (arrow.core) --------------------------------------------
        arrow_import_count = index.count_imports_matching("arrow.core")
        either_hits = index.search_pattern(r"\bEither\s*<", limit=20, exclude_tests=True)
        arrow_either_block_hits = index.search_pattern(r"\beither\s*\{", limit=20, exclude_tests=True)
        uses_arrow = arrow_import_count > 0 or bool(either_hits) or bool(arrow_either_block_hits)
        if uses_arrow:
            patterns.append("arrow-either")
            for r, ln, _ in (either_hits or arrow_either_block_hits)[:3]:
                good_examples.append((r, ln))

        # --- Sealed error hierarchies ----------------------------------------
        sealed_error_classes = [
            (rel_path, cls)
            for rel_path, cls in index.all_classes()
            if cls.is_sealed and re.search(SEALED_ERROR_NAME_RE, cls.name)
        ]
        sealed_error_types = [cls.name for _, cls in sealed_error_classes[:10]]
        if sealed_error_classes:
            patterns.append("sealed-class-results")
            good_examples.extend([(r, cls.line) for r, cls in sealed_error_classes[:3]])

        # --- Custom exceptions -------------------------------------------------
        custom_exception_re = (
            r"class\s+\w+\s*:\s*(?:Exception|RuntimeException|IllegalStateException)\s*\("
        )
        custom_exception_count = index.count_pattern(custom_exception_re, exclude_tests=True)
        if custom_exception_count:
            patterns.append("custom-exceptions")
            custom_exception_hits = index.search_pattern(
                custom_exception_re, limit=2, exclude_tests=True
            )
            good_examples.extend([(r, ln) for r, ln, _ in custom_exception_hits])

        # --- try/catch/finally ---------------------------------------------------
        try_count = index.count_pattern(r"\btry\s*\{", exclude_tests=True)
        catch_count = index.count_pattern(r"\bcatch\s*\(", exclude_tests=True)
        finally_count = index.count_pattern(r"\bfinally\s*\{", exclude_tests=True)
        try_catch_count = try_count + catch_count + finally_count
        if try_catch_count:
            patterns.append("try-catch")

        # --- Anti-patterns -------------------------------------------------------
        empty_catch_count = index.count_pattern(EMPTY_CATCH_RE, exclude_tests=True)
        if empty_catch_count:
            patterns.append("empty-catch")
            empty_catch_hits = index.search_pattern(EMPTY_CATCH_RE, limit=3, exclude_tests=True)
            bad_examples.extend([(r, ln) for r, ln, _ in empty_catch_hits])

        broad_catch_count = index.count_pattern(BROAD_CATCH_RE, exclude_tests=True)
        if broad_catch_count:
            patterns.append("broad-catch")
            broad_catch_hits = index.search_pattern(BROAD_CATCH_RE, limit=3, exclude_tests=True)
            bad_examples.extend([(r, ln) for r, ln, _ in broad_catch_hits])

        print_stack_trace_count = index.count_pattern(r"\.printStackTrace\s*\(", exclude_tests=True)
        if print_stack_trace_count:
            patterns.append("print-stack-trace")

        throw_count = index.count_pattern(r"\bthrow\s+", exclude_tests=True)

        # --- Preconditions -----------------------------------------------------
        require_count = index.count_pattern(r"\brequire\s*\(", exclude_tests=True)
        check_count = index.count_pattern(r"\bcheck\s*\(", exclude_tests=True)
        error_fn_count = index.count_pattern(r"\berror\s*\(", exclude_tests=True)
        if require_count or check_count or error_fn_count:
            patterns.append("preconditions")

        # --- @Throws (Java interop) ----------------------------------------------
        throws_count = index.count_annotation("Throws")
        if throws_count:
            patterns.append("throws-annotation")

        if not patterns:
            return result

        # --- Determine primary style --------------------------------------------
        if sealed_error_classes:
            primary = "sealed-class-results"
        elif uses_arrow:
            primary = "arrow-either"
        elif runcatching_count:
            primary = "runCatching"
        elif custom_exception_count:
            primary = "exceptions"
        elif try_catch_count:
            primary = "try-catch"
        else:
            primary = patterns[0]

        primary_labels = {
            "sealed-class-results": "sealed result types",
            "arrow-either": "Arrow Either",
            "runCatching": "runCatching",
            "exceptions": "custom exceptions",
            "try-catch": "try/catch",
        }
        title_bits = [primary_labels.get(primary, primary)]
        if primary != "runCatching" and runcatching_count:
            title_bits.append("runCatching")
        title = f"Error handling: {' + '.join(title_bits)}"

        description_parts = []
        if sealed_error_classes:
            description_parts.append(
                f"Models expected failures with {len(sealed_error_classes)} sealed error "
                f"hierarchy type(s) ({', '.join(sealed_error_types[:5])})."
            )
        if uses_arrow:
            description_parts.append("Uses Arrow (arrow.core) for functional error handling (Either).")
        if runcatching_count:
            description_parts.append(f"Uses runCatching/Result idioms in {runcatching_count} place(s).")
        if custom_exception_count:
            description_parts.append(f"Defines {custom_exception_count} custom exception type(s).")
        if try_catch_count:
            description_parts.append(f"Uses try/catch/finally {try_catch_count} time(s).")
        if not description_parts:
            description_parts.append("Uses standard Kotlin error-handling idioms.")

        if empty_catch_count:
            description_parts.append(
                f"Warning: {empty_catch_count} empty/swallowed catch block(s) found."
            )
        if broad_catch_count:
            description_parts.append(
                f"Warning: {broad_catch_count} overly broad catch(es) of Exception/Throwable."
            )

        description = " ".join(description_parts)

        # --- Confidence ------------------------------------------------------------
        confidence = 0.4
        confidence += min(0.2, 0.02 * try_catch_count)
        confidence += min(0.15, 0.03 * runcatching_count)
        if sealed_error_classes:
            confidence += 0.2
        if uses_arrow:
            confidence += 0.15
        if custom_exception_count:
            confidence += 0.05
        if empty_catch_count or broad_catch_count:
            confidence += 0.05
        confidence = min(0.95, confidence)

        # --- Evidence: prefer anti-patterns, then good patterns --------------------
        examples = bad_examples + good_examples
        evidence = []
        seen: set[tuple[str, int]] = set()
        for rel_path, line in examples:
            key = (rel_path, line)
            if key in seen:
                continue
            seen.add(key)
            ev = make_evidence(index, rel_path, line, radius=3)
            if ev:
                evidence.append(ev)
            if len(evidence) >= ctx.max_evidence_snippets:
                break

        result.rules.append(self.make_rule(
            rule_id="kotlin.conventions.error_handling",
            category="error_handling",
            title=title,
            description=description,
            confidence=confidence,
            language="kotlin",
            evidence=evidence,
            stats={
                "patterns": patterns,
                "primary": primary,
                "sealed_error_types": sealed_error_types,
                "try_catch_count": try_catch_count,
                "runcatching_count": runcatching_count,
                "custom_exception_count": custom_exception_count,
                "empty_catch_count": empty_catch_count,
                "broad_catch_count": broad_catch_count,
                "uses_arrow": uses_arrow,
                "uses_result_type": uses_result_type,
                "throw_count": throw_count,
                "print_stack_trace_count": print_stack_trace_count,
                "require_check_count": require_count + check_count + error_fn_count,
                "throws_annotation_count": throws_count,
            },
        ))

        return result
