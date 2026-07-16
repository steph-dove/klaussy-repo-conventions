"""Kotlin null-safety conventions detector."""

from __future__ import annotations

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import KotlinDetector
from .index import make_evidence

# Annotations that signal Java interop, where nullability is a documentation
# convention rather than something the Kotlin compiler enforces.
PLATFORM_TYPE_ANNOTATIONS = ("Nullable", "NotNull", "NonNull")


@DetectorRegistry.register
class KotlinNullSafetyDetector(KotlinDetector):
    """Detect Kotlin null-safety conventions and unsafe nullable handling."""

    name = "kotlin_null_safety"
    description = "Detects Kotlin null-safety conventions and unsafe nullable handling"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect null-safety conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        not_null_assertions = sum(
            f.not_null_assertion_count for f in index.get_non_test_files()
        )
        not_null_assertions_in_tests = sum(
            f.not_null_assertion_count for f in index.get_test_files()
        )
        safe_calls = sum(f.safe_call_count for f in index.files.values())
        elvis_operators = sum(f.elvis_count for f in index.files.values())
        lateinit_count = sum(f.lateinit_count for f in index.files.values())

        nullable_return_count = sum(
            1
            for _, fn in index.all_functions()
            if fn.return_type is not None and fn.return_type.strip().endswith("?")
        )

        require_not_null_count = index.count_pattern(
            r"\b(?:requireNotNull|checkNotNull)\s*\("
        )

        safe_call_let_count = index.count_pattern(r"\?\.\s*let\s*\{")

        platform_type_annotation_count = sum(
            index.count_annotation(name) for name in PLATFORM_TYPE_ANNOTATIONS
        )

        files_with_assertions = sum(
            1 for f in index.get_non_test_files() if f.not_null_assertion_count > 0
        )

        has_signal = (
            not_null_assertions > 0
            or not_null_assertions_in_tests > 0
            or safe_calls > 0
            or elvis_operators > 0
            or lateinit_count > 0
            or nullable_return_count > 0
        )
        if not has_signal:
            return result

        safe_signal = safe_calls + elvis_operators + require_not_null_count
        if not_null_assertions == 0:
            safety_ratio = 1.0
        else:
            safety_ratio = safe_signal / (safe_signal + not_null_assertions)

        patterns: list[str] = []
        if not_null_assertions > 0 or not_null_assertions_in_tests > 0:
            patterns.append("not_null_assertion")
        if safe_calls > 0:
            patterns.append("safe_call")
        if elvis_operators > 0:
            patterns.append("elvis_operator")
        if lateinit_count > 0:
            patterns.append("lateinit")
        if nullable_return_count > 0:
            patterns.append("nullable_return")
        if require_not_null_count > 0:
            patterns.append("require_not_null")
        if safe_call_let_count > 0:
            patterns.append("safe_call_let")
        if platform_type_annotation_count > 0:
            patterns.append("platform_type_annotation")

        # Title
        if not_null_assertions == 0:
            title = "Null safety: idiomatic, no `!!` assertions in production code"
        else:
            if safety_ratio >= 0.7:
                qualifier = "idiomatic elsewhere"
            elif safety_ratio >= 0.4:
                qualifier = "mixed practice"
            else:
                qualifier = "frequently bypassed"
            assertion_plural = "s" if not_null_assertions != 1 else ""
            file_plural = "s" if files_with_assertions != 1 else ""
            title = (
                f"Null safety: {not_null_assertions} `!!` assertion{assertion_plural} "
                f"across {files_with_assertions} file{file_plural}, {qualifier}"
            )

        # Description
        if not_null_assertions > 0:
            description = (
                f"Production code uses the `!!` not-null assertion "
                f"{not_null_assertions} time(s) across {files_with_assertions} file(s)."
            )
        else:
            description = "Production code has no `!!` not-null assertions."

        if not_null_assertions_in_tests > 0:
            description += (
                f" Tests use `!!` {not_null_assertions_in_tests} time(s) "
                "(more acceptable in test code)."
            )

        if safe_calls > 0 or elvis_operators > 0:
            description += (
                f" Uses safe calls (`?.`) {safe_calls} time(s) and the elvis "
                f"operator (`?:`) {elvis_operators} time(s)."
            )

        if lateinit_count > 0:
            description += (
                f" {lateinit_count} `lateinit var` declaration(s) defer null "
                "checks to runtime."
            )

        if nullable_return_count > 0:
            description += (
                f" {nullable_return_count} function(s) declare nullable return types."
            )

        if require_not_null_count > 0:
            description += (
                f" Uses `requireNotNull`/`checkNotNull` {require_not_null_count} "
                "time(s) as an explicit alternative to `!!`."
            )

        if platform_type_annotation_count > 0:
            description += (
                f" {platform_type_annotation_count} @Nullable/@NotNull/@NonNull "
                "annotation(s) indicate Java interop where nullability is not "
                "enforced by the Kotlin compiler."
            )

        if not_null_assertions >= 5 or (not_null_assertions > 0 and safety_ratio < 0.5):
            description += (
                " Consider replacing `!!` with safe calls (`?.`), the elvis "
                "operator (`?:`), or explicit `requireNotNull`/`checkNotNull` "
                "checks to preserve compile-time null safety."
            )

        signal_total = (
            not_null_assertions
            + not_null_assertions_in_tests
            + safe_calls
            + elvis_operators
            + lateinit_count
            + nullable_return_count
            + require_not_null_count
        )
        confidence = min(0.95, 0.55 + signal_total * 0.01)

        # Evidence: prefer `!!` sites in production code, the actionable finding.
        if not_null_assertions > 0:
            sites = index.search_pattern(r"!!", limit=50, exclude_tests=True)
        else:
            sites = index.search_pattern(r"\?\.", limit=20, exclude_tests=True)

        evidence = []
        for rel_path, line, _ in sites:
            ev = make_evidence(index, rel_path, line, radius=3)
            if ev:
                evidence.append(ev)
            if len(evidence) >= ctx.max_evidence_snippets:
                break

        result.rules.append(self.make_rule(
            rule_id="kotlin.conventions.null_safety",
            category="type_safety",
            title=title,
            description=description,
            confidence=confidence,
            language="kotlin",
            evidence=evidence,
            stats={
                "not_null_assertions": not_null_assertions,
                "not_null_assertions_in_tests": not_null_assertions_in_tests,
                "safe_calls": safe_calls,
                "elvis_operators": elvis_operators,
                "lateinit_count": lateinit_count,
                "nullable_return_count": nullable_return_count,
                "require_not_null_count": require_not_null_count,
                "safety_ratio": safety_ratio,
                "patterns": patterns,
                "files_with_assertions": files_with_assertions,
                "safe_call_let_count": safe_call_let_count,
                "platform_type_annotation_count": platform_type_annotation_count,
            },
        ))

        return result
