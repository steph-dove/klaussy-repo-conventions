"""Kotlin serialization conventions detector."""

from __future__ import annotations

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import KotlinDetector
from .index import make_evidence

# Library detection signals, in priority order (idiomatic-first). Each entry maps
# a library label to the regex/import/annotation substrings that indicate its use.
LIBRARY_IMPORT_SIGNALS: dict[str, tuple[str, ...]] = {
    "kotlinx.serialization": ("kotlinx.serialization",),
    "Jackson": ("com.fasterxml.jackson",),
    "Moshi": ("com.squareup.moshi",),
    "Gson": ("com.google.gson",),
    "Wire/Protobuf": ("com.squareup.wire",),
}

LIBRARY_ANNOTATION_SIGNALS: dict[str, tuple[str, ...]] = {
    "kotlinx.serialization": ("Serializable", "SerialName"),
    "Jackson": ("JsonProperty",),
    "Moshi": ("JsonClass", "Json"),
    "Gson": ("SerializedName",),
}


class _Detected:
    """Accumulated serialization signal for a single library."""

    def __init__(self) -> None:
        self.hits = 0
        self.examples: list[tuple[str, int]] = []

    def add(self, rel_path: str, line: int) -> None:
        self.hits += 1
        if len(self.examples) < 5:
            self.examples.append((rel_path, line))


@DetectorRegistry.register
class KotlinSerializationDetector(KotlinDetector):
    """Detect Kotlin serialization library and DTO conventions."""

    name = "kotlin_serialization"
    description = "Detects Kotlin serialization library and DTO conventions"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect serialization conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        build_info = self.get_build_info(ctx)
        libraries: dict[str, _Detected] = {}

        # Import-based signals.
        for lib, needles in LIBRARY_IMPORT_SIGNALS.items():
            for needle in needles:
                for rel_path, _import_path, line in index.find_imports_matching(needle, limit=50):
                    libraries.setdefault(lib, _Detected()).add(rel_path, line)

        # Annotation-based signals.
        for lib, annotation_names in LIBRARY_ANNOTATION_SIGNALS.items():
            for annotation_name in annotation_names:
                for rel_path, line in index.find_annotation(annotation_name, limit=50):
                    libraries.setdefault(lib, _Detected()).add(rel_path, line)

        # Free-form pattern signals not captured by import/annotation extraction.
        pattern_signals: dict[str, str] = {
            "kotlinx.serialization": r"Json\s*\.\s*(?:encodeToString|decodeFromString)",
            "Jackson": r"jacksonObjectMapper\s*\(",
            "Wire/Protobuf": r"\bprotobuf\b",
        }
        for lib, pattern in pattern_signals.items():
            for rel_path, line, _match in index.search_pattern(pattern, limit=20):
                libraries.setdefault(lib, _Detected()).add(rel_path, line)

        # Build-file signals.
        if build_info.has_dependency("kotlinx-serialization") or build_info.has_plugin(
            "kotlin.plugin.serialization"
        ):
            libraries.setdefault("kotlinx.serialization", _Detected())
        if build_info.has_dependency("com.fasterxml.jackson"):
            libraries.setdefault("Jackson", _Detected())
        if build_info.has_dependency("com.squareup.moshi"):
            libraries.setdefault("Moshi", _Detected())
        if build_info.has_dependency("com.google.gson"):
            libraries.setdefault("Gson", _Detected())
        if build_info.has_dependency("com.squareup.wire"):
            libraries.setdefault("Wire/Protobuf", _Detected())

        if not libraries:
            return result

        # Jackson without the Kotlin module silently mishandles default values
        # and nullability, so it's worth flagging explicitly.
        jackson_missing_kotlin_module = "Jackson" in libraries and not build_info.has_dependency(
            "jackson-module-kotlin"
        )

        serializable_class_count = index.count_annotation("Serializable")

        all_classes = index.all_classes()
        data_classes = [(rel_path, cls) for rel_path, cls in all_classes if cls.is_data]
        data_class_count = len(data_classes)

        serialization_annotation_names = {
            "Serializable",
            "JsonClass",
            "SerialName",
            "JsonProperty",
            "SerializedName",
            "Json",
        }
        annotated_dto_sites: list[tuple[str, int]] = [
            (rel_path, cls.line)
            for rel_path, cls in data_classes
            if serialization_annotation_names & set(cls.annotations)
        ]
        # Full unlimited count for the description fraction below; `dto_examples`
        # is capped separately since it's only used to gather evidence.
        annotated_dto_count = len(annotated_dto_sites)
        dto_examples = annotated_dto_sites[:5]

        custom_serializer_count = index.count_pattern(
            r"KSerializer\s*<|@Serializer\s*\(|object\s*:\s*KSerializer",
        )

        wire_name_examples = (
            index.find_annotation("SerialName", limit=5)
            + index.find_annotation("JsonProperty", limit=5)
            + index.find_annotation("SerializedName", limit=5)
        )
        uses_wire_name_mapping = len(wire_name_examples) > 0

        json_config_matches = index.search_pattern(
            r"Json\s*\{[^}]*(?:ignoreUnknownKeys|encodeDefaults|explicitNulls)",
            limit=10,
        )

        patterns: list[str] = []
        if serializable_class_count:
            patterns.append("@Serializable")
        if uses_wire_name_mapping:
            patterns.append("explicit wire-name mapping")
        if json_config_matches:
            patterns.append("Json { ... } configuration")
        if custom_serializer_count:
            patterns.append("custom KSerializer")
        if jackson_missing_kotlin_module:
            patterns.append("Jackson without jackson-module-kotlin")

        library_names = list(libraries.keys())
        primary_library = max(libraries.items(), key=lambda kv: kv[1].hits)[0]

        title = f"Serialization: {primary_library}"
        if data_class_count:
            title += f" on {data_class_count} data classes"

        description = f"Uses {primary_library} for serialization."
        if len(library_names) > 1:
            others = [name for name in library_names if name != primary_library]
            description += f" Other libraries present: {', '.join(others)}."
        if serializable_class_count:
            description += f" {serializable_class_count} classes annotated @Serializable."
        if data_class_count:
            description += (
                f" {annotated_dto_count}/{data_class_count} data classes carry a "
                "serialization annotation."
            )
        if uses_wire_name_mapping:
            description += " Uses explicit wire-name mapping (e.g. snake_case wire vs camelCase Kotlin)."
        if custom_serializer_count:
            description += f" {custom_serializer_count} custom serializer(s) defined."
        if jackson_missing_kotlin_module:
            description += (
                " Jackson is used without jackson-module-kotlin; this silently breaks default"
                " values and null-safety for Kotlin data classes."
            )

        # Confidence scales with the amount of corroborating signal found.
        confidence = 0.3
        confidence += min(0.3, 0.05 * sum(d.hits for d in libraries.values()))
        if serializable_class_count:
            confidence += 0.15
        if data_class_count:
            confidence += 0.1
        if len(library_names) == 1:
            confidence += 0.1
        confidence = min(0.95, confidence)

        examples: list[tuple[str, int]] = []
        primary_examples = libraries[primary_library].examples
        examples.extend(primary_examples)
        examples.extend(dto_examples)
        examples.extend((rel_path, line) for rel_path, line, _match in json_config_matches)

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
            rule_id="kotlin.conventions.serialization",
            category="serialization",
            title=title,
            description=description,
            confidence=confidence,
            language="kotlin",
            evidence=evidence,
            stats={
                "libraries": library_names,
                "primary_library": primary_library,
                "serializable_class_count": serializable_class_count,
                "data_class_count": data_class_count,
                "custom_serializer_count": custom_serializer_count,
                "uses_wire_name_mapping": uses_wire_name_mapping,
                "jackson_missing_kotlin_module": jackson_missing_kotlin_module,
                "patterns": patterns,
            },
        ))

        return result
