"""C++ architecture conventions detector."""

from __future__ import annotations

import re
from collections import Counter
from typing import Optional

from ...schemas import EvidenceSnippet
from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import CPPDetector
from .index import CPPFileIndex, make_evidence

ARCHITECTURAL_ROLES = ("api", "service", "db", "model")


@DetectorRegistry.register
class CPPArchitectureDetector(CPPDetector):
    """Detect C++ project structure, build systems, and formatting conventions."""

    name = "cpp_architecture"
    description = "Detects C++ project structure, build systems, and formatting conventions"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect C++ architecture conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        # 1. Build System detection
        build_systems = []
        if ctx.repo_root.joinpath("CMakeLists.txt").exists():
            build_systems.append("CMake")
        if ctx.repo_root.joinpath("Makefile").exists() or ctx.repo_root.joinpath("makefile").exists():
            build_systems.append("Make")
        if ctx.repo_root.joinpath("WORKSPACE").exists() or ctx.repo_root.joinpath("BUILD").exists():
            build_systems.append("Bazel")

        build_system = "/".join(build_systems) if build_systems else "Custom / None"

        # 2. Source Layout Style (Header-only vs separated)
        headers = sum(1 for f in index.files.values() if f.is_header)
        sources = len(index.files) - headers
        is_header_only = headers > 0 and sources == 0

        layout = "separated (src/include)"
        if is_header_only:
            layout = "header-only"
        elif headers == 0:
            layout = "flat/sources-only"

        # 3. Code formatting (clang-format)
        has_clang_format = ctx.repo_root.joinpath(".clang-format").exists() or \
                           ctx.repo_root.joinpath("_clang-format").exists()

        role_counts = Counter(f.role for f in index.files.values())
        layers = sorted(role for role in role_counts if role in ARCHITECTURAL_ROLES)

        title = f"Architecture: C++ {layout} via {build_system}"

        truncated = self.scan_was_truncated(index, ctx)
        counts = f"{headers} headers, {sources} sources"
        if truncated:
            desc_parts = [
                f"C++ codebase (at least {len(index.files)} files: {counts}; the scan "
                f"stopped at the {ctx.max_files}-file limit) uses a {layout} layout "
                f"and {build_system} build configuration."
            ]
        else:
            desc_parts = [
                f"C++ codebase ({len(index.files)} files: {counts}) uses a {layout} "
                f"layout and {build_system} build configuration."
            ]

        if layers:
            layer_note = f"Layers detected: {', '.join(layers)}."
            if truncated:
                layer_note = (
                    f"Layers seen in the scanned subset: {', '.join(layers)} "
                    "(the scan was truncated, so others may exist)."
                )
            desc_parts.append(layer_note)
        if has_clang_format:
            desc_parts.append("Clang-Format configuration (.clang-format) is present for consistent styling.")
        else:
            desc_parts.append("No Clang-Format styling rules found.")

        description = " ".join(desc_parts)

        # Build evidence
        evidence: list[EvidenceSnippet] = []
        preferred_role_order = ["api", "service", "model", "main"]
        ordered_roles = [r for r in preferred_role_order if r in role_counts]

        for role in ordered_roles:
            if len(evidence) >= ctx.max_evidence_snippets:
                break
            candidate: Optional[CPPFileIndex] = None
            for file_idx in index.get_files_by_role(role):
                if not file_idx.is_test:
                    candidate = file_idx
                    break
            if candidate:
                ev = make_evidence(index, candidate.relative_path, 1, radius=3)
                if ev:
                    evidence.append(ev)

        stats = {
            "build_system": build_system,
            "layout": layout,
            "is_header_only": is_header_only,
            "has_clang_format": has_clang_format,
            "header_count": headers,
            "source_count": sources,
            "layers": layers,
            "role_counts": dict(role_counts),
            # Files actually scanned, which is the project size only when the
            # scan was not truncated -- hence the companion flag.
            "file_count": len(index.files),
            "scan_truncated": truncated,
        }

        result.rules.append(self.make_rule(
            rule_id="cpp.conventions.architecture",
            category="architecture",
            title=title,
            description=description,
            confidence=0.8,
            language="cpp",
            evidence=evidence,
            stats=stats,
        ))

        # 3. C++ Error Handling
        try_catch_count = index.count_pattern(r"\btry\s*\{", exclude_tests=True)
        throw_count = index.count_pattern(r"\bthrow\b", exclude_tests=True)
        errors_title = "Error Handling: C++ exceptions"
        errors_desc = f"Uses try-catch blocks ({try_catch_count} found) and throws exception blocks ({throw_count} found) for exception/error propagation."

        errors_evidence = []
        if try_catch_count > 0:
            tc_sites = index.search_pattern(r"\btry\s*\{", exclude_tests=True, limit=1)
            if tc_sites:
                ev = make_evidence(index, tc_sites[0][0], tc_sites[0][1], radius=3)
                if ev:
                    errors_evidence.append(ev)

        result.rules.append(self.make_rule(
            rule_id="cpp.conventions.errors",
            category="errors",
            title=errors_title,
            description=errors_desc,
            confidence=0.8,
            language="cpp",
            evidence=errors_evidence,
            stats={
                "try_catch_count": try_catch_count,
                "throw_count": throw_count,
            },
        ))

        # 4. C++ Concurrency
        concurrency_count = index.count_pattern(r'\b(?:std::thread|std::mutex|std::lock_guard|std::unique_lock|std::async)\b', exclude_tests=True)
        concurrency_title = "Concurrency: OS threads"
        concurrency_desc = f"Uses standard library concurrency features ({concurrency_count} thread/mutex primitive instances)."

        result.rules.append(self.make_rule(
            rule_id="cpp.conventions.concurrency",
            category="concurrency",
            title=concurrency_title,
            description=concurrency_desc,
            confidence=0.8,
            language="cpp",
            evidence=[],
            stats={
                "concurrency_count": concurrency_count,
            },
        ))

        # 5. C++ Memory Management / Smart Pointers
        smart_pointer_count = index.count_pattern(r'\b(?:std::unique_ptr|std::shared_ptr|std::make_unique|std::make_shared)\b', exclude_tests=True)
        raw_new_count = index.count_pattern(r'\bnew\b\s+\w+', exclude_tests=True)

        general_title = "Conventions: Memory Management"
        general_desc = f"Uses modern smart pointers ({smart_pointer_count} std::unique_ptr/shared_ptr instances) and {raw_new_count} raw allocations (new)."

        result.rules.append(self.make_rule(
            rule_id="cpp.conventions.general",
            category="style",
            title=general_title,
            description=general_desc,
            confidence=0.8,
            language="cpp",
            evidence=[],
            stats={
                "smart_pointer_count": smart_pointer_count,
                "raw_new_count": raw_new_count,
            },
        ))

        # 6. API Routes
        routes = []
        methods: dict[str, int] = {}

        crowd_route_pattern = re.compile(r'\bCROWD_ROUTE\s*\(\s*\w+\s*,\s*["\']([^"\']+)["\']\s*\)')
        drogon_route_pattern = re.compile(r'\.registerHandler\s*\(\s*["\']([^"\']+)["\']')

        for rel_path, file_idx in index.files.items():
            if file_idx.role == "test":
                continue
            content = "\n".join(file_idx.lines)

            for match in crowd_route_pattern.finditer(content):
                path = match.group(1)
                line = content[:match.start()].count("\n") + 1
                methods["ANY"] = methods.get("ANY", 0) + 1
                routes.append({
                    "method": "ANY",
                    "path": path,
                    "file": rel_path,
                    "line": line,
                })
                if len(routes) >= 100:
                    break

            for match in drogon_route_pattern.finditer(content):
                path = match.group(1)
                line = content[:match.start()].count("\n") + 1
                methods["ANY"] = methods.get("ANY", 0) + 1
                routes.append({
                    "method": "ANY",
                    "path": path,
                    "file": rel_path,
                    "line": line,
                })
                if len(routes) >= 100:
                    break

            if len(routes) >= 100:
                break

        if routes:
            description = (
                f"{len(routes)} API routes detected. "
                f"Methods: {', '.join(f'{k}: {v}' for k, v in sorted(methods.items()))}."
            )
            result.rules.append(self.make_rule(
                rule_id="cpp.conventions.api_routes",
                category="api",
                title="API routes",
                description=description,
                confidence=0.85,
                language="cpp",
                evidence=[],
                stats={
                    "routes": routes,
                    "total_routes": len(routes),
                    "methods": methods,
                },
            ))

        # 7. C++ Database Entities
        db_entities = []
        cpp_model_pattern = re.compile(r'\b(?:struct|class)\s+(\w+)\b[^{]*\{[^}]*\b(?:id|uuid|created_at|updated_at)\b')

        for rel_path, file_idx in index.files.items():
            if file_idx.role == "test":
                continue
            if "model" not in rel_path.lower() and "entity" not in rel_path.lower():
                continue
            content = "\n".join(file_idx.lines)

            for match in cpp_model_pattern.finditer(content):
                db_entities.append({
                    "name": match.group(1),
                    "file": rel_path,
                })

        if db_entities:
            names = [e["name"] for e in db_entities[:10]]
            db_ent_desc = (
                f"{len(db_entities)} database model(s)/struct(s) detected: {', '.join(names)}"
                + ("..." if len(db_entities) > 10 else "") + "."
            )
            result.rules.append(self.make_rule(
                rule_id="cpp.conventions.db_entities",
                category="database",
                title="Database entities",
                description=db_ent_desc,
                confidence=0.8,
                language="cpp",
                evidence=[],
                stats={
                    "entities": db_entities,
                    "entity_count": len(db_entities),
                    "orm": "sqlite_orm" if index.count_pattern("sqlite_orm") else "unknown",
                },
            ))

        return result
