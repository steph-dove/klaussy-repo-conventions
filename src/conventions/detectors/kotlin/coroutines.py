"""Kotlin coroutines and structured-concurrency conventions detector."""

from __future__ import annotations

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import KotlinDetector
from .index import KotlinIndex, make_evidence

# Flow is the idiomatic reactive/asynchronous stream type in kotlinx.coroutines.
FLOW_PATTERNS: dict[str, str] = {
    "Flow<": r"\bFlow\s*<",
    "StateFlow": r"\bStateFlow\b",
    "SharedFlow": r"\bSharedFlow\b",
    "MutableStateFlow": r"\bMutableStateFlow\b",
    "flow {": r"\bflow\s*\{",
    ".collect {": r"\.collect\s*\{",
    "flowOn(": r"\bflowOn\s*\(",
    ".stateIn(": r"\.stateIn\s*\(",
    ".shareIn(": r"\.shareIn\s*\(",
}

CHANNEL_PATTERNS: dict[str, str] = {
    "Channel<": r"\bChannel\s*<",
    "produce {": r"\bproduce\s*\{",
    ".consumeEach": r"\.consumeEach\b",
}

BUILDER_PATTERNS: dict[str, str] = {
    "launch {": r"\blaunch\s*\{",
    "async {": r"\basync\s*\{",
    "runBlocking {": r"\brunBlocking\b",
    "withContext(": r"\bwithContext\s*\(",
    "coroutineScope {": r"\bcoroutineScope\s*\{",
    "supervisorScope {": r"\bsupervisorScope\s*\{",
}

DISPATCHER_PATTERNS: dict[str, str] = {
    "Dispatchers.IO": r"\bDispatchers\.IO\b",
    "Dispatchers.Default": r"\bDispatchers\.Default\b",
    "Dispatchers.Main": r"\bDispatchers\.Main\b",
    "Dispatchers.Unconfined": r"\bDispatchers\.Unconfined\b",
}

SCOPE_PATTERNS: dict[str, str] = {
    "CoroutineScope(": r"\bCoroutineScope\s*\(",
    "viewModelScope": r"\bviewModelScope\b",
    "lifecycleScope": r"\blifecycleScope\b",
    "GlobalScope": r"\bGlobalScope\b",
}

# Regex used specifically for surfacing runBlocking in production (non-test) code.
_RUNBLOCKING_PATTERN = r"\brunBlocking\b"

# Regex used specifically for surfacing hardcoded Dispatchers at call sites.
_HARDCODED_DISPATCHER_PATTERN = r"Dispatchers\.(?:IO|Default|Main|Unconfined)"


@DetectorRegistry.register
class KotlinCoroutinesDetector(KotlinDetector):
    """Detect Kotlin coroutine and structured-concurrency conventions."""

    name = "kotlin_coroutines"
    description = "Detects Kotlin coroutine and structured-concurrency conventions"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect coroutine usage, Flow/channel idioms, and concurrency anti-patterns."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        build_info = self.get_build_info(ctx)

        has_coroutines_import = index.count_imports_matching("kotlinx.coroutines") > 0
        has_coroutines_dependency = build_info.has_dependency("kotlinx-coroutines")

        all_functions = index.all_functions()
        suspend_function_count = sum(1 for _, fn in all_functions if fn.is_suspend)
        total_functions = len(all_functions)
        suspend_share = suspend_function_count / total_functions if total_functions else 0.0

        flow_counts, flow_examples = _match_patterns(index, FLOW_PATTERNS)
        channel_counts, channel_examples = _match_patterns(index, CHANNEL_PATTERNS)
        builder_counts, builder_examples = _match_patterns(index, BUILDER_PATTERNS)
        dispatcher_counts, dispatcher_examples = _match_patterns(index, DISPATCHER_PATTERNS)
        scope_counts, scope_examples = _match_patterns(index, SCOPE_PATTERNS)

        flow_usage = sum(flow_counts.values())
        channel_usage = sum(channel_counts.values())
        uses_flow = flow_usage > 0

        has_any_signal = (
            has_coroutines_import
            or has_coroutines_dependency
            or suspend_function_count > 0
            or flow_usage > 0
            or channel_usage > 0
            or sum(builder_counts.values()) > 0
            or sum(dispatcher_counts.values()) > 0
            or sum(scope_counts.values()) > 0
        )
        if not has_any_signal:
            return result

        patterns: list[str] = [
            key
            for counts in (flow_counts, channel_counts, builder_counts, dispatcher_counts, scope_counts)
            for key, count in counts.items()
            if count > 0
        ]
        dispatchers = [key for key, count in dispatcher_counts.items() if count > 0]

        uses_structured_concurrency = (
            builder_counts.get("coroutineScope {", 0) > 0 or builder_counts.get("supervisorScope {", 0) > 0
        )

        # Anti-patterns worth surfacing.
        global_scope_count = scope_counts.get("GlobalScope", 0)
        runblocking_in_production = index.count_pattern(
            _RUNBLOCKING_PATTERN, exclude_tests=True, exclude_imports=True
        )
        hardcoded_dispatcher_sites = index.count_pattern(
            _HARDCODED_DISPATCHER_PATTERN, exclude_tests=True, exclude_imports=True
        )

        title = _build_title(suspend_function_count, uses_flow, channel_usage)
        description = _build_description(
            has_coroutines_dependency or has_coroutines_import,
            suspend_function_count,
            total_functions,
            uses_flow,
            channel_usage,
            uses_structured_concurrency,
            global_scope_count,
            runblocking_in_production,
            hardcoded_dispatcher_sites,
        )

        confidence = 0.5
        if has_coroutines_dependency:
            confidence += 0.1
        if suspend_function_count > 0:
            confidence += 0.1
        if uses_flow:
            confidence += 0.1
        if uses_structured_concurrency:
            confidence += 0.1
        if patterns:
            confidence += 0.05
        confidence = min(0.95, confidence)

        # Evidence: prefer anti-pattern sites, otherwise fall back to representative usage.
        evidence_sources: list[tuple[str, int]] = list(scope_examples.get("GlobalScope", []))
        if runblocking_in_production > 0:
            evidence_sources.extend(
                (rel, line)
                for rel, line, _ in index.search_pattern(
                    _RUNBLOCKING_PATTERN,
                    limit=ctx.max_evidence_snippets,
                    exclude_tests=True,
                    exclude_imports=True,
                )
            )
        if not evidence_sources:
            for examples in (flow_examples, builder_examples, channel_examples, scope_examples, dispatcher_examples):
                for sites in examples.values():
                    evidence_sources.extend(sites)
                    if len(evidence_sources) >= ctx.max_evidence_snippets:
                        break
                if len(evidence_sources) >= ctx.max_evidence_snippets:
                    break

        evidence = []
        for rel_path, line in evidence_sources[: ctx.max_evidence_snippets]:
            ev = make_evidence(index, rel_path, line, radius=3)
            if ev:
                evidence.append(ev)

        result.rules.append(self.make_rule(
            rule_id="kotlin.conventions.coroutines",
            category="concurrency",
            title=title,
            description=description,
            confidence=confidence,
            language="kotlin",
            evidence=evidence,
            stats={
                "suspend_function_count": suspend_function_count,
                "flow_usage": flow_usage,
                "channel_usage": channel_usage,
                "patterns": patterns,
                "dispatchers": dispatchers,
                "global_scope_count": global_scope_count,
                "runblocking_in_production": runblocking_in_production,
                "uses_structured_concurrency": uses_structured_concurrency,
                "uses_flow": uses_flow,
                "total_functions": total_functions,
                "suspend_share": round(suspend_share, 3),
                "hardcoded_dispatcher_sites": hardcoded_dispatcher_sites,
            },
        ))

        return result


def _match_patterns(
    index: KotlinIndex,
    patterns: dict[str, str],
    example_limit: int = 3,
) -> tuple[dict[str, int], dict[str, list[tuple[str, int]]]]:
    """Search `patterns` against the index, returning per-key counts and example sites.

    Import lines are excluded throughout: these patterns match coroutine symbols,
    and `import kotlinx.coroutines.GlobalScope` is not a usage of GlobalScope.
    """
    counts: dict[str, int] = {}
    examples: dict[str, list[tuple[str, int]]] = {}
    for key, regex in patterns.items():
        count = index.count_pattern(regex, exclude_imports=True)
        counts[key] = count
        matches = (
            index.search_pattern(regex, limit=example_limit, exclude_imports=True)
            if count
            else []
        )
        examples[key] = [(rel, line) for rel, line, _ in matches]
    return counts, examples


def _build_title(suspend_function_count: int, uses_flow: bool, channel_usage: int) -> str:
    """Build a rule title summarizing the dominant coroutine idioms in use."""
    parts: list[str] = []
    if suspend_function_count > 0:
        noun = "function" if suspend_function_count == 1 else "functions"
        parts.append(f"{suspend_function_count} suspend {noun}")
    if uses_flow:
        parts.append("Flow-based streams")
    elif channel_usage > 0:
        parts.append("channel-based streams")
    if not parts:
        parts.append("structured concurrency")
    return "Coroutines: " + ", ".join(parts)


def _build_description(
    uses_coroutines: bool,
    suspend_function_count: int,
    total_functions: int,
    uses_flow: bool,
    channel_usage: int,
    uses_structured_concurrency: bool,
    global_scope_count: int,
    runblocking_in_production: int,
    hardcoded_dispatcher_sites: int,
) -> str:
    """Build a rule description covering usage and any anti-patterns found."""
    parts: list[str] = []
    if uses_coroutines:
        parts.append("Uses kotlinx.coroutines.")
    if suspend_function_count > 0:
        parts.append(
            f"{suspend_function_count} of {total_functions} function(s) are suspend."
        )
    if uses_flow:
        parts.append("Uses Flow for reactive/asynchronous streams.")
    if channel_usage > 0:
        parts.append(f"{channel_usage} channel-based usage(s).")
    if uses_structured_concurrency:
        parts.append("Uses coroutineScope/supervisorScope for structured concurrency.")

    anti_pattern_notes: list[str] = []
    if global_scope_count > 0:
        noun = "usage" if global_scope_count == 1 else "usages"
        verb = "bypasses" if global_scope_count == 1 else "bypass"
        anti_pattern_notes.append(f"{global_scope_count} GlobalScope {noun} {verb} structured concurrency.")
    if runblocking_in_production > 0:
        noun = "site" if runblocking_in_production == 1 else "sites"
        verb = "blocks" if runblocking_in_production == 1 else "block"
        anti_pattern_notes.append(
            f"{runblocking_in_production} runBlocking {noun} in production code {verb} the calling thread."
        )
    if hardcoded_dispatcher_sites > 0:
        noun = "site" if hardcoded_dispatcher_sites == 1 else "sites"
        verb = "hardcodes" if hardcoded_dispatcher_sites == 1 else "hardcode"
        anti_pattern_notes.append(
            f"{hardcoded_dispatcher_sites} call {noun} {verb} Dispatchers directly instead of an "
            "injected dispatcher, hurting testability."
        )
    if anti_pattern_notes:
        parts.append(" ".join(anti_pattern_notes))

    return " ".join(parts) if parts else "Uses Kotlin coroutines."
