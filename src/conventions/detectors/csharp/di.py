"""C# dependency injection conventions detector."""

from __future__ import annotations

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import CSharpDetector
from .index import make_evidence

# A C# 12 primary constructor: `public sealed class UserService(IUserRepo repo)`.
#
# Anchored to the start of a line and using [ \t] rather than \s throughout: \s
# matches newlines, so a bare `class` at the end of one line followed by any
# `Method(args)` call on the next satisfied the old pattern. That reported
# Newtonsoft.Json -- which predates primary constructors -- as using them.
PRIMARY_CONSTRUCTOR_PATTERN = (
    r"^[ \t]*(?:(?:public|internal|protected|private|sealed|abstract|static|partial)[ \t]+)*"
    r"class[ \t]+\w+(?:<[^>]*>)?[ \t]*\([^)]"
)

# ASP.NET Core / Generic Host bootstrap. These wire up Microsoft.Extensions.
# DependencyInjection implicitly, so they count as DI on their own.
HOST_BOOTSTRAP_PATTERN = (
    r"\bWebApplication\.CreateBuilder\b"
    r"|\bHost\.CreateDefaultBuilder\b"
    r"|\bHostApplicationBuilder\b"
    r"|\bbuilder\.Services\b"
    r"|\bIServiceCollection\b"
)


@DetectorRegistry.register
class CSharpDIDetector(CSharpDetector):
    """Detect C# dependency injection frameworks and conventions."""

    name = "csharp_di"
    description = "Detects C# dependency injection frameworks and conventions"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect dependency injection conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        build_info = self.get_build_info(ctx)

        # 1. Framework detection based on imports and dependencies
        di_frameworks: set[str] = set()

        # Test-only signals are excluded throughout: a container referenced purely
        # by the test suite is not the project's DI convention.
        ms_di_imports = index.count_imports_matching(
            "Microsoft.Extensions.DependencyInjection", exclude_tests=True
        )
        ms_di_calls = index.count_pattern(r"\.Add(?:Transient|Scoped|Singleton)\b", exclude_tests=True)
        autofac_imports = index.count_imports_matching("Autofac", exclude_tests=True)
        ninject_imports = index.count_imports_matching("Ninject", exclude_tests=True)

        deps = set(build_info.production_dependencies)
        if ms_di_imports > 0 or ms_di_calls > 0 or any("Microsoft.Extensions.DependencyInjection" in d for d in deps):
            di_frameworks.add("Microsoft.Extensions.DependencyInjection")
        if autofac_imports > 0 or any("Autofac" in d for d in deps):
            di_frameworks.add("Autofac")
        if ninject_imports > 0 or any("Ninject" in d for d in deps):
            di_frameworks.add("Ninject")

        if not di_frameworks:
            # ASP.NET Core and the Generic Host wire up Microsoft.Extensions.
            # DependencyInjection implicitly, so their bootstrap counts as DI even
            # without an explicit using. The presence of a Program.cs does not:
            # every console app has one, which reported Newtonsoft.Json (whose only
            # Program.cs belongs to a test console) as using MS DI.
            if index.count_pattern(HOST_BOOTSTRAP_PATTERN, exclude_tests=True):
                di_frameworks.add("Microsoft.Extensions.DependencyInjection")
            else:
                return result

        # 2. Injection styles detection
        # Field Injection: rare in C#, but check for [Inject] attributes on properties or fields
        inject_attr_count = index.count_annotation("Inject")

        # Constructor Injection: The absolute standard in C#
        # C# constructors match class names, we can check constructor signatures
        constructor_inject_count = 0
        for file_idx in index.files.values():
            if file_idx.is_test:
                continue
            for cls in file_idx.classes:
                # Find methods inside class with the same name (constructors)
                ctor_methods = [f for f in file_idx.functions if f.name == cls.name]
                if ctor_methods:
                    constructor_inject_count += 1

        primary_style = "constructor"
        if inject_attr_count > constructor_inject_count:
            primary_style = "field/property"

        # C# 12 primary constructors: `public class UserService(IUserRepository repo)`.
        # Counted via count_pattern (search_pattern stops at its limit), and only
        # treated as the primary style when they actually outnumber the classic
        # forms -- a single primary constructor is not a codebase-wide convention.
        primary_constructors = index.count_pattern(PRIMARY_CONSTRUCTOR_PATTERN, exclude_tests=True)

        if primary_constructors > max(constructor_inject_count, inject_attr_count):
            primary_style = "primary constructor"

        # 3. Compile title, description and stats
        frameworks_str = "/".join(sorted(di_frameworks))
        title = f"Dependency Injection: {frameworks_str} ({primary_style} injection)"

        desc_parts = [f"Uses {frameworks_str} for dependency injection."]
        if primary_style == "primary constructor":
            desc_parts.append("Utilizes C# 12 primary constructor injection extensively.")
        else:
            desc_parts.append("Constructor injection is preferred and used consistently.")

        if ms_di_calls > 0:
            desc_parts.append(f"Found {ms_di_calls} service lifetime registrations (Transient/Scoped/Singleton).")

        description = " ".join(desc_parts)

        # Build evidence
        evidence = []
        if ms_di_calls > 0:
            sites = index.search_pattern(r"\.Add(?:Transient|Scoped|Singleton)\b", exclude_tests=True, limit=2)
            for rel_path, line, _ in sites:
                ev = make_evidence(index, rel_path, line, radius=3)
                if ev:
                    evidence.append(ev)

        stats = {
            "frameworks": list(di_frameworks),
            "primary_style": primary_style,
            "ms_di_calls": ms_di_calls,
            "primary_constructor_count": primary_constructors,
            "inject_attribute_count": inject_attr_count,
        }

        result.rules.append(self.make_rule(
            rule_id="csharp.conventions.di",
            category="dependency_injection",
            title=title,
            description=description,
            confidence=0.8,
            language="csharp",
            evidence=evidence,
            stats=stats,
        ))

        return result
