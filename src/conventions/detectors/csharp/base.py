"""C# detector base class."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

from ..base import BaseDetector, DetectorContext
from .index import CSharpIndex


@dataclass
class CSharpBuildInfo:
    """Parsed C# build info (from .csproj/.sln files)."""

    dependencies: list[str] = field(default_factory=list)
    # Packages referenced by non-test projects only. Use this when deciding what
    # the project itself uses: Newtonsoft.Json's test project references Autofac
    # purely to demo DI in a documentation sample, which does not make Autofac a
    # convention of the library.
    production_dependencies: list[str] = field(default_factory=list)
    modules: list[str] = field(default_factory=list)
    is_multi_module: bool = False
    # Projects declaring <Nullable>enable</Nullable>. Since .NET 6 this is how
    # nullable reference types are turned on -- project-wide, not with per-file
    # `#nullable enable` directives.
    nullable_projects: int = 0
    target_frameworks: list[str] = field(default_factory=list)

    @property
    def nullable_enabled(self) -> bool:
        """Whether any project enables nullable reference types."""
        return self.nullable_projects > 0


class CSharpDetector(BaseDetector):
    """Base class for C# detectors."""

    languages: set[str] = {"csharp"}

    def get_index(self, ctx: DetectorContext) -> CSharpIndex:
        """Get or create the C# index."""
        if ctx.cache.get("csharp_index") is None:
            index = CSharpIndex(
                ctx.repo_root,
                max_files=ctx.max_files,
                exclude_patterns=ctx.exclude_patterns,
            )
            index.build()
            ctx.cache["csharp_index"] = index
        result: CSharpIndex = ctx.cache["csharp_index"]
        return result

    def get_build_info(self, ctx: DetectorContext) -> CSharpBuildInfo:
        """Get or create the parsed C# build info."""
        if ctx.cache.get("csharp_build_info") is None:
            ctx.cache["csharp_build_info"] = self._parse_build_info(ctx)
        result: CSharpBuildInfo = ctx.cache["csharp_build_info"]
        return result

    def _parse_build_info(self, ctx: DetectorContext) -> CSharpBuildInfo:
        """Parse all .csproj files to gather NuGet dependencies and projects."""
        from ...fs import walk_files
        from .index import _is_test_dir

        dependencies = []
        production_dependencies = []
        modules = []
        nullable_projects = 0
        target_frameworks: list[str] = []

        # Directory.Build.props applies its properties to every project beneath
        # it, so a repo can enable nullable there once instead of per-project.
        build_props = list(
            walk_files(
                ctx.repo_root,
                {"Directory.Build.props"},
                exclude_patterns=ctx.exclude_patterns,
            )
        )

        csproj_files = list(walk_files(ctx.repo_root, {".csproj"}, exclude_patterns=ctx.exclude_patterns))
        for proj_path in csproj_files + build_props:
            is_project = proj_path.suffix == ".csproj"
            if is_project:
                modules.append(proj_path.stem)
            # .NET names test projects after the project under test
            # (Newtonsoft.Json.Tests), so the stem is the reliable signal.
            is_test_project = is_project and _is_test_dir(proj_path.stem)
            try:
                content = proj_path.read_text(encoding="utf-8")
                # Remove XML namespaces to simplify element querying
                content_clean = re.sub(r' xmlns="[^"]+"', '', content, count=1)
                root = ET.fromstring(content_clean)
                for pkg in root.findall(".//PackageReference"):
                    inc = pkg.get("Include")
                    if inc:
                        dependencies.append(inc)
                        if not is_test_project:
                            production_dependencies.append(inc)

                # <Nullable>enable</Nullable> is the modern, project-wide switch
                # for nullable reference types; `annotations` enables them too.
                nullable_el = root.find(".//Nullable")
                if nullable_el is not None and (nullable_el.text or "").strip().lower() in (
                    "enable",
                    "annotations",
                ):
                    nullable_projects += 1

                for tfm_tag in ("TargetFramework", "TargetFrameworks"):
                    tfm_el = root.find(f".//{tfm_tag}")
                    if tfm_el is not None and tfm_el.text:
                        target_frameworks.extend(
                            t.strip() for t in tfm_el.text.split(";") if t.strip()
                        )
            except Exception:
                pass

        return CSharpBuildInfo(
            dependencies=dependencies,
            production_dependencies=production_dependencies,
            modules=modules,
            is_multi_module=len(modules) > 1,
            nullable_projects=nullable_projects,
            target_frameworks=sorted(set(target_frameworks)),
        )
