"""C# build tooling conventions detector."""

from __future__ import annotations

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import CSharpDetector

# Analyzer/quality packages worth surfacing, matched as substrings against the
# PackageReference ids.
QUALITY_PACKAGES = (
    "StyleCop.Analyzers",
    "SonarAnalyzer",
    "Roslynator",
    "Microsoft.CodeAnalysis.NetAnalyzers",
    "coverlet",
)


@DetectorRegistry.register
class CSharpBuildDetector(CSharpDetector):
    """Detect C# build tooling and project configuration conventions."""

    name = "csharp_build"
    description = "Detects C# build tooling, target frameworks and project configuration"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect .NET build conventions."""
        result = DetectorResult()
        build_info = self.get_build_info(ctx)

        if not build_info.modules:
            return result

        quality_packages = sorted(
            {
                pkg
                for pkg in QUALITY_PACKAGES
                if any(pkg.lower() in dep.lower() for dep in build_info.dependencies)
            }
        )

        target_frameworks = build_info.target_frameworks
        project_count = len(build_info.modules)
        dependency_count = len(set(build_info.dependencies))

        title = "Build: .NET"
        if target_frameworks:
            title += f" ({', '.join(target_frameworks[:3])})"

        description = (
            f"Builds with the .NET SDK across {project_count} project(s) "
            f"and {dependency_count} distinct NuGet package(s)."
        )
        if target_frameworks:
            description += f" Targets {', '.join(target_frameworks)}."
        if build_info.nullable_enabled:
            description += (
                f" Nullable reference types are enabled in {build_info.nullable_projects}"
                " project(s)."
            )
        if quality_packages:
            description += f" Analyzer packages: {', '.join(quality_packages)}."
        else:
            description += (
                " No analyzer package detected; consider StyleCop.Analyzers or"
                " Microsoft.CodeAnalysis.NetAnalyzers to enforce style in the build."
            )

        confidence = 0.6
        if target_frameworks:
            confidence += 0.2
        if dependency_count:
            confidence += 0.1
        confidence = min(0.95, confidence)

        result.rules.append(self.make_rule(
            rule_id="csharp.conventions.build_tools",
            category="build",
            title=title,
            description=description,
            confidence=confidence,
            language="csharp",
            # .csproj files are not C# sources, so they are absent from the index
            # and cannot yield evidence snippets.
            evidence=[],
            stats={
                "build_system": "dotnet",
                # CLAUDE.md's tech-stack renderer reads `primary_tool` for
                # build_tools rules, and derives build/test commands from it.
                "primary_tool": "dotnet",
                "target_frameworks": target_frameworks,
                "project_count": project_count,
                "dependency_count": dependency_count,
                "is_multi_module": build_info.is_multi_module,
                "nullable_projects": build_info.nullable_projects,
                "quality_packages": quality_packages,
            },
        ))

        return result
