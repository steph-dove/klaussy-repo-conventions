"""Kotlin Gradle build tooling conventions detector."""

from __future__ import annotations

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import KotlinDetector
from .index import make_evidence

# Notable plugins worth surfacing, keyed by the substring matched against
# `BuildInfo.plugins` ids via `has_plugin`.
NOTABLE_PLUGINS = (
    "detekt",
    "ktlint",
    "spotless",
    "dokka",
    "shadow",
    "org.springframework.boot",
    "com.android.application",
    "com.android.library",
    "kotlin.kapt",
    "com.google.devtools.ksp",
)

BUILD_SYSTEM_LABELS = {
    "gradle-kotlin-dsl": "Gradle Kotlin DSL",
    "gradle-groovy": "Gradle Groovy DSL",
    "maven": "Maven",
}


@DetectorRegistry.register
class KotlinGradleDetector(KotlinDetector):
    """Detect Kotlin build tooling, Gradle configuration and dependency conventions."""

    name = "kotlin_gradle"
    description = "Detects Kotlin build tooling, Gradle configuration and dependency conventions"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect Gradle/Maven build conventions."""
        result = DetectorResult()
        build_info = self.get_build_info(ctx)

        if build_info.build_system == "unknown" or not build_info.build_files:
            return result

        index = self.get_index(ctx)

        plugins = [p for p in NOTABLE_PLUGINS if build_info.has_plugin(p)]

        dependency_count = len(build_info.dependencies)
        test_dependency_count = sum(1 for d in build_info.dependencies if d.is_test_only)

        build_system_label = BUILD_SYSTEM_LABELS.get(build_info.build_system, build_info.build_system)

        title_parts = [f"Build: {build_system_label}"]
        if build_info.kotlin_version:
            title_parts.append(f"Kotlin {build_info.kotlin_version}")
        if build_info.jvm_target:
            title_parts.append(f"JVM {build_info.jvm_target}")
        title = ", ".join(title_parts)

        description = f"Uses {build_system_label} with {dependency_count} declared dependencies"
        if test_dependency_count:
            description += f" ({test_dependency_count} test-only)"
        description += "."

        if build_info.is_multi_module:
            description += f" Multi-module project with {len(build_info.modules)} modules."

        if build_info.uses_version_catalog:
            description += " Uses a Gradle version catalog for dependency management."

        if plugins:
            description += f" Notable plugins: {', '.join(plugins)}."

        if "kotlin.kapt" in plugins and "com.google.devtools.ksp" not in plugins:
            description += " Uses kapt without KSP; KSP is the modern, faster replacement for kapt."

        # Confidence scales with how much build signal was actually recovered.
        confidence = 0.5
        if build_info.kotlin_version:
            confidence += 0.15
        if build_info.jvm_target:
            confidence += 0.1
        if dependency_count:
            confidence += 0.15
        if plugins:
            confidence += 0.1

        evidence = []
        for plugin_id, line, source_file in build_info.plugins:
            if plugin_id not in plugins:
                continue
            if source_file not in index.files:
                continue
            ev = make_evidence(index, source_file, line, radius=3)
            if ev:
                evidence.append(ev)
            if len(evidence) >= ctx.max_evidence_snippets:
                break

        result.rules.append(self.make_rule(
            rule_id="kotlin.conventions.build_tools",
            category="build",
            title=title,
            description=description,
            confidence=confidence,
            language="kotlin",
            evidence=evidence,
            stats={
                "build_system": build_info.build_system,
                # CLAUDE.md's tech-stack renderer reads `primary_tool` for build_tools rules.
                "primary_tool": "maven" if build_info.build_system == "maven" else "gradle",
                "kotlin_version": build_info.kotlin_version,
                "jvm_target": build_info.jvm_target,
                "uses_version_catalog": build_info.uses_version_catalog,
                "module_count": len(build_info.modules),
                "dependency_count": dependency_count,
                "plugins": plugins,
                "is_multi_module": build_info.is_multi_module,
            },
        ))

        return result
