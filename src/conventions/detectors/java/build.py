"""Java build tooling conventions detector."""

from __future__ import annotations

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import JavaDetector

# Notable plugins worth surfacing, matched as substrings against the plugin ids
# in `BuildInfo.plugins`. Maven plugins are recorded by artifactId
# (maven-compiler-plugin), Gradle plugins by id (com.diffplug.spotless).
NOTABLE_PLUGINS = (
    "checkstyle",
    "spotbugs",
    "pmd",
    "jacoco",
    "spotless",
    "errorprone",
    "shade",
    "org.springframework.boot",
    "spring-boot-maven-plugin",
)

# Quality gates: static analysis or coverage enforcement in the build.
QUALITY_PLUGINS = ("checkstyle", "spotbugs", "pmd", "errorprone", "spotless", "jacoco")

BUILD_SYSTEM_LABELS = {
    "gradle-kotlin-dsl": "Gradle Kotlin DSL",
    "gradle-groovy": "Gradle Groovy DSL",
    "maven": "Maven",
}


@DetectorRegistry.register
class JavaBuildDetector(JavaDetector):
    """Detect Java build tooling and dependency management conventions."""

    name = "java_build"
    description = "Detects Java build tooling, dependency management and build plugins"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect Gradle/Maven build conventions."""
        result = DetectorResult()
        build_info = self.get_build_info(ctx)

        if build_info.build_system == "unknown" or not build_info.build_files:
            return result

        plugins = [p for p in NOTABLE_PLUGINS if build_info.has_plugin(p)]
        quality_plugins = [p for p in plugins if p in QUALITY_PLUGINS]

        dependency_count = len(build_info.dependencies)
        test_dependency_count = sum(1 for d in build_info.dependencies if d.is_test_only)

        build_system_label = BUILD_SYSTEM_LABELS.get(
            build_info.build_system, build_info.build_system
        )

        title_parts = [f"Build: {build_system_label}"]
        if build_info.jvm_target:
            title_parts.append(f"Java {build_info.jvm_target}")
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

        if not quality_plugins:
            description += (
                " No static-analysis or coverage plugin detected; consider Checkstyle,"
                " SpotBugs or JaCoCo to enforce quality in the build."
            )

        # Confidence scales with how much build signal was actually recovered.
        confidence = 0.5
        if build_info.jvm_target:
            confidence += 0.15
        if dependency_count:
            confidence += 0.15
        if plugins:
            confidence += 0.1
        confidence = min(0.95, confidence)

        result.rules.append(self.make_rule(
            rule_id="java.conventions.build_tools",
            category="build",
            title=title,
            description=description,
            confidence=confidence,
            language="java",
            # Build files (pom.xml, *.gradle) are not Java sources, so they are
            # absent from the index and cannot yield evidence snippets.
            evidence=[],
            stats={
                "build_system": build_info.build_system,
                # CLAUDE.md's tech-stack renderer reads `primary_tool` for
                # build_tools rules, and derives build/test commands from it.
                "primary_tool": "maven" if build_info.build_system == "maven" else "gradle",
                "java_version": build_info.jvm_target,
                "jvm_target": build_info.jvm_target,
                "uses_version_catalog": build_info.uses_version_catalog,
                "module_count": len(build_info.modules),
                "dependency_count": dependency_count,
                "test_dependency_count": test_dependency_count,
                "plugins": plugins,
                "quality_plugins": quality_plugins,
                "is_multi_module": build_info.is_multi_module,
            },
        ))

        return result
