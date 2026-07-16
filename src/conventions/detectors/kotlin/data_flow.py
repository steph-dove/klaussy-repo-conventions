"""Kotlin data flow / layering conventions detector."""

from __future__ import annotations

import re

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import KotlinDetector
from .index import make_evidence

# Import path segments that indicate a target layer, keyed to the canonical
# layer name used elsewhere in the Kotlin indexer's `role` classification.
LAYER_IMPORT_SEGMENTS: dict[str, str] = {
    ".controller.": "api",
    ".api.": "api",
    ".service.": "service",
    ".domain.": "service",
    ".repository.": "db",
    ".dao.": "db",
    ".model.": "model",
    ".dto.": "model",
    ".entity.": "model",
}

# Layer roles the Kotlin indexer assigns based on conventional package names.
LAYER_ROLES = {"api", "service", "db", "model", "ui"}

# Matches mapping-style function declarations, with or without an extension
# receiver, e.g. `fun toDto(`, `fun User.toEntity(`, `fun UserEntity.toDomain(`.
MAPPING_FUNCTION_PATTERN = re.compile(
    r"fun\s+(?:<[^>]+>\s*)?(?:[\w.<>?,\[\] ]+?\.)?(?:toDto|toEntity|toDomain|toModel)\s*\(",
)


def _constructor_span(lines: list[str], class_line: int, window: int = 25) -> str:
    """Extract the source text spanning a class's primary constructor parameter list.

    Args:
        lines: The file's raw source lines.
        class_line: 1-indexed line where the class declaration starts.
        window: Maximum number of lines to scan looking for the closing paren.

    Returns:
        The joined source text from the class declaration through the closing
        paren of its primary constructor, or an empty string if out of range.
    """
    start_idx = class_line - 1
    if start_idx < 0 or start_idx >= len(lines):
        return ""

    depth = 0
    started = False
    collected: list[str] = []
    end_idx = min(len(lines), start_idx + window)

    for i in range(start_idx, end_idx):
        line = lines[i]
        collected.append(line)
        for ch in line:
            if ch == "(":
                depth += 1
                started = True
            elif ch == ")":
                depth -= 1
        if started and depth <= 0:
            break

    return "\n".join(collected)


@DetectorRegistry.register
class KotlinDataFlowDetector(KotlinDetector):
    """Detects how data flows between layers in a Kotlin codebase."""

    name = "kotlin_data_flow"
    description = "Detects how data flows between layers in a Kotlin codebase"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect layering and data flow conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        non_test_files = index.get_non_test_files()
        if len(non_test_files) < 3:
            return result

        roles_present = {f.role for f in non_test_files}
        if not (roles_present & LAYER_ROLES):
            return result

        # --- Layer dependency edges -------------------------------------
        edge_counts: dict[str, int] = {}
        edge_examples: dict[str, list[tuple[str, int]]] = {}
        violation_examples: list[tuple[str, int]] = []

        for file_idx in non_test_files:
            source_role = file_idx.role
            for import_path, line in file_idx.imports:
                for segment, target_layer in LAYER_IMPORT_SEGMENTS.items():
                    if segment in import_path:
                        edge = f"{source_role}->{target_layer}"
                        edge_counts[edge] = edge_counts.get(edge, 0) + 1
                        edge_examples.setdefault(edge, []).append(
                            (file_idx.relative_path, line)
                        )
                        if source_role == "api" and target_layer == "db":
                            violation_examples.append((file_idx.relative_path, line))
                        break

        layers = sorted(
            (roles_present & LAYER_ROLES)
            | {
                part
                for edge in edge_counts
                for part in edge.split("->")
                if part in LAYER_ROLES
            }
        )

        layer_violations = len(violation_examples)
        follows_layered_flow = (
            edge_counts.get("api->service", 0) > 0
            and edge_counts.get("service->db", 0) > 0
            and layer_violations == 0
        )

        # --- DTO vs entity separation --------------------------------------
        all_classes = index.all_classes()
        model_data_classes = [
            (rel_path, cls)
            for rel_path, cls in all_classes
            if cls.is_data and index.files[rel_path].role == "model"
        ]
        dto_count = len(model_data_classes)

        entity_classes = [
            (rel_path, cls) for rel_path, cls in all_classes if "Entity" in cls.annotations
        ]
        entity_count = len(entity_classes)
        entity_names = {cls.name for _rel_path, cls in entity_classes}

        mutable_dto_count = 0
        for rel_path, cls in model_data_classes:
            file_idx = index.files[rel_path]
            span = _constructor_span(file_idx.lines, cls.line)
            if re.search(r"\bvar\b", span):
                mutable_dto_count += 1

        entity_exposure: list[tuple[str, int]] = []
        if entity_names:
            for file_idx in index.get_files_by_role("api"):
                for fn in file_idx.functions:
                    if fn.return_type and any(
                        re.search(rf"\b{re.escape(name)}\b", fn.return_type)
                        for name in entity_names
                    ):
                        entity_exposure.append((file_idx.relative_path, fn.line))

        # --- Mapping conventions --------------------------------------------
        mapping_matches = index.search_pattern(
            MAPPING_FUNCTION_PATTERN.pattern, limit=50, exclude_tests=True
        )
        mapping_functions = sorted({match.strip() for _rp, _ln, match in mapping_matches})[:10]
        mapstruct_count = index.count_imports_matching("org.mapstruct")
        map_lambda_count = index.count_pattern(r"\.map\s*\{", exclude_tests=True)
        uses_dto_mapping = bool(mapping_functions) or mapstruct_count > 0

        # --- Suspend functions crossing layers -------------------------------
        suspend_crossing_count = sum(
            1
            for f in non_test_files
            if f.role in LAYER_ROLES
            for fn in f.functions
            if fn.is_suspend
        )

        # --- Patterns --------------------------------------------------------
        patterns: list[str] = []
        if edge_counts.get("api->service", 0) > 0:
            patterns.append("api -> service")
        if edge_counts.get("service->db", 0) > 0:
            patterns.append("service -> db")
        if layer_violations:
            patterns.append("api -> db direct (layer violation)")
        if mapping_functions:
            patterns.append("toDto()/toEntity()/toDomain() mapping functions")
        if mapstruct_count:
            patterns.append("MapStruct (org.mapstruct)")
        if map_lambda_count:
            patterns.append(".map { } transformations")
        if dto_count and mutable_dto_count == 0:
            patterns.append("immutable DTOs (val-only constructors)")
        if mutable_dto_count:
            patterns.append("mutable DTOs (var in constructor)")
        if entity_exposure:
            patterns.append("@Entity classes exposed directly from api layer")
        if suspend_crossing_count:
            patterns.append("suspend functions crossing layers")

        total_edges = sum(edge_counts.values())

        # --- Title -------------------------------------------------------------
        canonical_present = [layer for layer in ("api", "service", "db") if layer in layers]
        title = "Data flow: " + " -> ".join(canonical_present or layers or ["main"])
        if uses_dto_mapping:
            title += " with DTO mapping"

        # --- Description ---------------------------------------------------
        description_parts = [
            f"{total_edges} layer-crossing import(s) detected across "
            f"{len(layers)} layer(s) ({', '.join(layers)})."
        ]
        if follows_layered_flow:
            description_parts.append("Follows the canonical api -> service -> db flow.")
        elif edge_counts.get("api->service", 0) or edge_counts.get("service->db", 0):
            description_parts.append(
                "Does not cleanly follow the canonical api -> service -> db flow."
            )
        if layer_violations:
            description_parts.append(
                f"{layer_violations} api file(s)/import(s) reference the db/repository layer "
                "directly, bypassing the service layer."
            )
        if entity_exposure:
            description_parts.append(
                f"{len(entity_exposure)} api-layer site(s) directly expose @Entity-annotated "
                "types instead of DTOs."
            )
        if dto_count:
            if mutable_dto_count:
                description_parts.append(
                    f"{dto_count} DTO/model data class(es), {mutable_dto_count} with mutable "
                    "(var) constructor params."
                )
            else:
                description_parts.append(f"{dto_count} DTO/model data class(es), all immutable.")
        if entity_count:
            description_parts.append(f"{entity_count} @Entity-annotated class(es).")
        if uses_dto_mapping:
            description_parts.append("Uses explicit mapping functions/MapStruct for conversion.")

        description = " ".join(description_parts)

        # --- Confidence ------------------------------------------------------
        confidence = 0.3
        confidence += min(0.3, 0.01 * total_edges)
        if follows_layered_flow:
            confidence += 0.1
        if mapping_functions or mapstruct_count:
            confidence += 0.1
        if dto_count or entity_count:
            confidence += 0.1
        confidence = min(0.9, confidence)

        # --- Evidence ----------------------------------------------------------
        if violation_examples:
            candidate_sites = violation_examples
        else:
            candidate_sites = (
                edge_examples.get("api->service", []) + edge_examples.get("service->db", [])
            )

        evidence = []
        seen: set[tuple[str, int]] = set()
        for rel_path, line in candidate_sites:
            key = (rel_path, line)
            if key in seen:
                continue
            seen.add(key)
            ev = make_evidence(index, rel_path, line, radius=3)
            if ev:
                evidence.append(ev)
            if len(evidence) >= ctx.max_evidence_snippets:
                break

        result.rules.append(
            self.make_rule(
                rule_id="kotlin.conventions.data_flow",
                category="architecture",
                title=title,
                description=description,
                confidence=confidence,
                language="kotlin",
                evidence=evidence,
                stats={
                    "layers": layers,
                    "layer_edges": edge_counts,
                    "follows_layered_flow": follows_layered_flow,
                    "layer_violations": layer_violations,
                    "violation_examples": [
                        f"{rel_path}:{line}" for rel_path, line in violation_examples[:5]
                    ],
                    "uses_dto_mapping": uses_dto_mapping,
                    "mapping_functions": mapping_functions,
                    "dto_count": dto_count,
                    "entity_count": entity_count,
                    "mutable_dto_count": mutable_dto_count,
                    "patterns": patterns,
                    "mapstruct_detected": mapstruct_count > 0,
                    "map_lambda_count": map_lambda_count,
                    "entity_exposure_count": len(entity_exposure),
                    "suspend_crossing_count": suspend_crossing_count,
                },
            )
        )

        return result
