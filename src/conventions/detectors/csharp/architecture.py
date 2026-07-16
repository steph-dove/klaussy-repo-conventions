"""C# architecture conventions detector."""

from __future__ import annotations

from collections import Counter
from typing import Optional

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import CSharpDetector
from .index import CSharpFileIndex, CSharpIndex, make_evidence

LAYER_WORDS = frozenset({
    "controller", "controllers", "api", "endpoints", "routes", "handlers",
    "service", "services", "usecase", "usecases", "interactor", "repository",
    "repositories", "dao", "db", "database", "context", "persistence",
    "model", "models", "entity", "entities", "dto", "dtos", "schema",
    "ui", "view", "views", "viewmodel", "viewmodels",
})

CLEAN_ARCHITECTURE_WORDS = frozenset({
    "domain", "application", "infrastructure", "adapter", "adapters",
    "port", "ports", "usecase", "usecases",
})

ARCHITECTURAL_ROLES = ("main", "api", "service", "db", "model")


@DetectorRegistry.register
class CSharpArchitectureDetector(CSharpDetector):
    """Detect C# project structure, module layout and layering conventions."""

    name = "csharp_architecture"
    description = "Detects C# project structure, module layout and layering conventions"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect C# architecture conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files or len(index.files) < 2:
            return result

        build_info = self.get_build_info(ctx)

        modules = sorted(set(f.module for f in index.files.values() if f.module) | set(build_info.modules))
        module_count = len(modules)
        is_multi_module = module_count > 1 or build_info.is_multi_module

        structure = "multi-module" if is_multi_module else "single-module"

        role_counts = Counter(f.role for f in index.files.values())
        layers = sorted(role for role in role_counts if role in ARCHITECTURAL_ROLES)

        common_root = self._common_namespace_root(index)
        package_style, style_confidence = self._detect_namespace_style(index, common_root)

        uses_clean_architecture = self._uses_clean_architecture(index)
        framework = self._detect_framework(index)

        confidence = 0.4
        if is_multi_module:
            confidence += 0.1
        if len(layers) >= 3:
            confidence += 0.1
        confidence += style_confidence
        if uses_clean_architecture:
            confidence += 0.1
        if framework != "class library":
            confidence += 0.1
        confidence = min(0.9, confidence)

        title_parts = [structure]
        if package_style != "unknown":
            title_parts.append(package_style)
        if framework != "class library":
            title_parts.append(framework)
        title = "Architecture: " + ", ".join(title_parts)
        if common_root:
            title += f" under {common_root}"

        description_parts = [
            f"C# project with {len(index.files)} files uses a {structure} structure."
        ]
        if layers:
            description_parts.append(f"Layers present: {', '.join(layers)}.")
        if package_style != "unknown":
            description_parts.append(f"Namespace organization is {package_style}.")
        if common_root:
            description_parts.append(f"Common namespace root: {common_root}.")
        if uses_clean_architecture:
            description_parts.append(
                "Uses clean/hexagonal architecture markers (domain, application, "
                "infrastructure, adapter, port, or usecase folders)."
            )
        if framework != "class library":
            description_parts.append(f"Uses {framework}.")
        description = " ".join(description_parts)

        evidence = self._build_evidence(ctx, index, role_counts)

        stats: dict[str, object] = {
            "structure": structure,
            "module_count": module_count,
            "modules": modules[:20],
            "layers": layers,
            "role_counts": dict(role_counts),
            "package_style": package_style,
            "common_namespace_root": common_root,
            "uses_clean_architecture": uses_clean_architecture,
            "framework": framework,
            "file_count": len(index.files),
            "patterns": self._collect_patterns(
                is_multi_module, uses_clean_architecture, framework
            ),
        }

        result.rules.append(self.make_rule(
            rule_id="csharp.conventions.architecture",
            category="architecture",
            title=title,
            description=description,
            confidence=confidence,
            language="csharp",
            evidence=evidence,
            stats=stats,
        ))

        return result

    def _common_namespace_root(self, index: CSharpIndex) -> Optional[str]:
        """Find the common namespace prefix shared across indexed files."""
        namespaces = [f.namespace.split(".") for f in index.files.values() if f.namespace]
        if not namespaces:
            return None

        common: list[str] = []
        for segments in zip(*namespaces):
            first = segments[0]
            if all(s == first for s in segments):
                common.append(first)
            else:
                break

        return ".".join(common) if common else None

    def _detect_namespace_style(
        self,
        index: CSharpIndex,
        common_root: Optional[str],
    ) -> tuple[str, float]:
        """Infer namespace-by-layer vs namespace-by-feature vs flat organization."""
        root_depth = len(common_root.split(".")) if common_root else 0

        layer_at_shallow_depth = 0
        layer_at_deep_depth = 0
        total_with_extra_segments = 0

        for file_idx in index.files.values():
            if not file_idx.namespace:
                continue
            segments = file_idx.namespace.split(".")
            extra = segments[root_depth:]
            if not extra:
                continue
            total_with_extra_segments += 1

            layer_positions = [i for i, seg in enumerate(extra) if seg.lower() in LAYER_WORDS]
            if not layer_positions:
                continue

            first_layer_pos = layer_positions[0]
            if first_layer_pos == 0:
                layer_at_shallow_depth += 1
            else:
                layer_at_deep_depth += 1

        if total_with_extra_segments == 0:
            return "flat", 0.0

        signal_total = layer_at_shallow_depth + layer_at_deep_depth
        if signal_total == 0:
            return "unknown", 0.0

        signal_ratio = signal_total / total_with_extra_segments
        confidence_bonus = min(0.15, signal_ratio * 0.15)

        if layer_at_deep_depth > layer_at_shallow_depth:
            return "package-by-feature", confidence_bonus
        if layer_at_shallow_depth > layer_at_deep_depth:
            return "package-by-layer", confidence_bonus
        return "unknown", 0.0

    def _uses_clean_architecture(self, index: CSharpIndex) -> bool:
        """Check whether packages contain clean/hexagonal architecture markers."""
        marker_packages = 0
        for file_idx in index.files.values():
            if not file_idx.namespace:
                continue
            segments = {seg.lower() for seg in file_idx.namespace.split(".")}
            if segments & CLEAN_ARCHITECTURE_WORDS:
                marker_packages += 1

        return marker_packages >= 2

    def _detect_framework(self, index: CSharpIndex) -> str:
        """Detect ASP.NET Core features (Minimal APIs vs Controllers vs Razor)."""
        has_controllers = index.count_imports_matching("Microsoft.AspNetCore.Mvc") or \
                          len(index.search_pattern(r":\s*Controller(?:Base)?\b")) > 0

        has_minimal_apis = index.count_pattern(r"\.MapGet\s*\(") or \
                           index.count_pattern(r"\.MapPost\s*\(")

        if has_controllers and has_minimal_apis:
            return "ASP.NET Core (mixed APIs)"
        if has_controllers:
            return "ASP.NET Core Web API (Controllers)"
        if has_minimal_apis:
            return "ASP.NET Core Minimal APIs"

        if index.count_imports_matching("Microsoft.AspNetCore"):
            return "ASP.NET Core Web Application"

        return "class library"

    def _collect_patterns(
        self,
        is_multi_module: bool,
        uses_clean_architecture: bool,
        framework: str,
    ) -> list[str]:
        """Collect short, human-readable pattern tags for stats."""
        patterns: list[str] = []
        if is_multi_module:
            patterns.append("multi-module")
        if uses_clean_architecture:
            patterns.append("clean-architecture")
        if framework != "class library":
            patterns.append(framework.lower().replace(" ", "-").replace("(", "").replace(")", ""))
        return patterns

    def _build_evidence(
        self,
        ctx: DetectorContext,
        index: CSharpIndex,
        role_counts: Counter,
    ) -> list:
        """Pick representative evidence files from distinct layers."""
        evidence = []
        seen_roles: set[str] = set()

        preferred_role_order = ["api", "service", "db", "model", "main"]
        ordered_roles = [r for r in preferred_role_order if r in role_counts]

        for role in ordered_roles:
            if len(evidence) >= ctx.max_evidence_snippets:
                break
            if role in seen_roles:
                continue
            seen_roles.add(role)

            candidate: Optional[CSharpFileIndex] = None
            for file_idx in index.get_files_by_role(role):
                if not file_idx.is_test:
                    candidate = file_idx
                    break

            if candidate is None:
                continue

            ev = make_evidence(index, candidate.relative_path, 1, radius=3)
            if ev:
                evidence.append(ev)

        return evidence
