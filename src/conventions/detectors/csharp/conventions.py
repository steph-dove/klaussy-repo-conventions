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

        return result
