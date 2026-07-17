"""C# coding style and language conventions detector."""

from __future__ import annotations

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import CSharpDetector
from .index import make_evidence


@DetectorRegistry.register
class CSharpConventionsDetector(CSharpDetector):
    """Detect C#-specific coding conventions (async/await, LINQ, nullable types)."""

    name = "csharp_conventions"
    description = "Detects C#-specific coding conventions (async/await, LINQ, nullable types)"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect coding conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        # 1. Nullable Reference Types.
        #
        # Since .NET 6 these are enabled project-wide via <Nullable>enable</Nullable>
        # in the .csproj (or Directory.Build.props); per-file `#nullable enable`
        # directives are the older, incremental-adoption route. Reading only the
        # directives reported eShopOnWeb -- which enables it in every project --
        # as having nullable "disabled".
        build_info = self.get_build_info(ctx)
        files_with_nullable = sum(1 for f in index.files.values() if f.nullable_enabled)
        nullable_ratio = files_with_nullable / len(index.files) if index.files else 0.0

        if build_info.nullable_enabled:
            nullable_style = "enabled (project-wide)"
        elif nullable_ratio > 0.8:
            nullable_style = "enabled (standard)"
        elif nullable_ratio > 0.0:
            nullable_style = "mixed (partially enabled)"
        else:
            nullable_style = "disabled"

        # 2. Async/Await usage
        async_count = sum(f.async_count for f in index.files.values())
        await_count = sum(f.await_count for f in index.files.values())

        async_style = "synchronous"
        if async_count > 0 or await_count > 0:
            async_style = "asynchronous (async/await)"

        # 3. LINQ usage
        linq_count = sum(f.linq_count for f in index.files.values())

        linq_style = "standard loops"
        if linq_count > 0:
            linq_style = "LINQ processing"

        # Compile Title and Description
        title = f"Conventions: Nullable types {nullable_style}, {async_style}, {linq_style}"

        desc_parts = []
        if nullable_ratio > 0.0:
            desc_parts.append(f"C# Nullable Reference Types feature is {nullable_style} ({files_with_nullable} file(s) with #nullable enable).")
        else:
            desc_parts.append("C# Nullable Reference Types feature is disabled or not declared.")

        if async_count > 0:
            desc_parts.append(f"Uses async/await pattern extensively ({async_count} async declarations, {await_count} awaits).")
        else:
            desc_parts.append("Codebase is primarily synchronous.")

        if linq_count > 0:
            desc_parts.append(f"Utilizes LINQ (Language Integrated Query) for list filtering and transformation ({linq_count} LINQ operations).")

        description = " ".join(desc_parts)

        # Build evidence
        evidence = []
        # Add nullable or async evidence
        if async_count > 0:
            async_methods = index.search_pattern(r"\basync\s+[\w.<>]+\s+\w+\s*\(", exclude_tests=True, limit=1)
            if async_methods:
                ev = make_evidence(index, async_methods[0][0], async_methods[0][1], radius=3)
                if ev:
                    evidence.append(ev)
        if len(evidence) < ctx.max_evidence_snippets:
            linq_calls = index.search_pattern(r"\.\w+\s*\(.*\)\s*\.\w+\s*\(", exclude_tests=True, limit=1)
            if linq_calls:
                ev = make_evidence(index, linq_calls[0][0], linq_calls[0][1], radius=3)
                if ev:
                    evidence.append(ev)

        stats = {
            "nullable_ratio": nullable_ratio,
            "files_with_nullable": files_with_nullable,
            "nullable_style": nullable_style,
            "async_count": async_count,
            "await_count": await_count,
            "async_style": async_style,
            "linq_count": linq_count,
            "linq_style": linq_style,
        }

        result.rules.append(self.make_rule(
            rule_id="csharp.conventions.general",
            category="style",
            title=title,
            description=description,
            confidence=0.8,
            language="csharp",
            evidence=evidence,
            stats=stats,
        ))

        # 4. Error Handling
        try_catch_count = index.count_pattern(r"\btry\s*\{", exclude_tests=True)
        custom_exceptions_count = index.count_pattern(r"class\s+\w+Exception\s*:\s*(?:Exception|RuntimeException)\b", exclude_tests=True)

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
            rule_id="csharp.conventions.errors",
            category="errors",
            title=errors_title,
            description=errors_desc,
            confidence=0.8,
            language="csharp",
            evidence=errors_evidence,
            stats={
                "try_catch_count": try_catch_count,
                "custom_exceptions_count": custom_exceptions_count,
            },
        ))

        # 5. Security & Secrets
        has_raw_sql_usage = index.count_pattern(r'\b(?:ExecuteSqlRaw|FromSqlRaw|FromSqlInterpolated)\b', exclude_tests=True) > 0
        connection_string_count = index.count_pattern(r'\bConnectionString\b', exclude_tests=True)

        security_title = "Security: Secure settings"
        if has_raw_sql_usage:
            security_title = "Security: Raw SQL injection risk"

        security_desc = f"Checks for secure configurations. Found {connection_string_count} connection string references."
        if has_raw_sql_usage:
            security_desc += " Warning: Detected raw SQL query API usage (e.g. FromSqlRaw/ExecuteSqlRaw)."

        result.rules.append(self.make_rule(
            rule_id="csharp.conventions.security",
            category="security",
            title=security_title,
            description=security_desc,
            confidence=0.8,
            language="csharp",
            evidence=[],
            stats={
                "has_raw_sql_usage": has_raw_sql_usage,
                "connection_string_count": connection_string_count,
            },
        ))

        # 6. Concurrency
        concurrency_primitives_count = index.count_pattern(r'\b(?:SemaphoreSlim|Monitor|Mutex|lock\s*\(|Task\.Run)\b', exclude_tests=True)
        concurrency_title = "Concurrency: Tasks & Threads"
        concurrency_desc = f"Uses async tasks and {concurrency_primitives_count} explicit synchronization/concurrency primitives (e.g. lock, SemaphoreSlim)."

        result.rules.append(self.make_rule(
            rule_id="csharp.conventions.concurrency",
            category="concurrency",
            title=concurrency_title,
            description=concurrency_desc,
            confidence=0.8,
            language="csharp",
            evidence=[],
            stats={
                "concurrency_primitives_count": concurrency_primitives_count,
            },
        ))

        return result
