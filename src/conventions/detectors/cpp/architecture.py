"""C++ architecture conventions detector."""

from __future__ import annotations

from collections import Counter
from typing import Optional

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
        evidence = []
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

        return result
