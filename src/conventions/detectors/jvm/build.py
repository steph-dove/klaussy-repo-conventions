"""Gradle and Maven build file parsing shared across JVM languages."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from ...fs import get_relative_path, read_file_safe, walk_files

# Gradle configurations that declare a dependency. Ordered longest-first where
# prefixes overlap so `testImplementation` is not matched as `implementation`.
DEPENDENCY_CONFIGURATIONS = (
    "testImplementation",
    "androidTestImplementation",
    "testRuntimeOnly",
    "testCompileOnly",
    "debugImplementation",
    "releaseImplementation",
    "implementation",
    "compileOnly",
    "runtimeOnly",
    "annotationProcessor",
    "kapt",
    "ksp",
    "api",
)

TEST_CONFIGURATIONS = frozenset({
    "testImplementation",
    "androidTestImplementation",
    "testRuntimeOnly",
    "testCompileOnly",
})


@dataclass
class Dependency:
    """A single declared dependency."""

    group: str
    artifact: str
    version: Optional[str]
    configuration: str
    source_file: str
    line: int

    @property
    def coordinate(self) -> str:
        """The `group:artifact` coordinate, without version."""
        return f"{self.group}:{self.artifact}"

    @property
    def is_test_only(self) -> bool:
        """Whether this dependency is scoped to tests."""
        return self.configuration in TEST_CONFIGURATIONS


@dataclass
class BuildInfo:
    """Parsed view of a repository's JVM build configuration."""

    # gradle-kotlin-dsl, gradle-groovy, maven, or unknown
    build_system: str = "unknown"
    build_files: list[str] = field(default_factory=list)
    dependencies: list[Dependency] = field(default_factory=list)
    plugins: list[tuple[str, int, str]] = field(default_factory=list)  # (id, line, file)
    modules: list[str] = field(default_factory=list)  # settings.gradle include(...)
    kotlin_version: Optional[str] = None
    jvm_target: Optional[str] = None
    uses_version_catalog: bool = False
    catalog_libraries: dict[str, str] = field(default_factory=dict)  # alias -> coordinate

    @property
    def is_multi_module(self) -> bool:
        """Whether the build declares more than one Gradle module."""
        return len(self.modules) > 1

    def has_dependency(self, needle: str) -> bool:
        """Whether any dependency coordinate contains `needle`."""
        return any(needle in d.coordinate for d in self.dependencies)

    def find_dependencies(self, needle: str) -> list[Dependency]:
        """All dependencies whose coordinate contains `needle`."""
        return [d for d in self.dependencies if needle in d.coordinate]

    def has_plugin(self, needle: str) -> bool:
        """Whether any applied plugin id contains `needle`."""
        return any(needle in plugin_id for plugin_id, _, _ in self.plugins)


def parse_build_files(
    repo_root: Path,
    max_files: int = 200,
    exclude_patterns: Optional[list[str]] = None,
) -> BuildInfo:
    """Parse Gradle and Maven build files under `repo_root`.

    Gradle takes precedence when a repository contains both, since Gradle is the
    common case for Kotlin and a `pom.xml` is often a leftover or a submodule.
    """
    info = BuildInfo()
    repo_root = Path(repo_root).resolve()

    gradle_files = list(
        walk_files(
            repo_root,
            extensions={".gradle", ".gradle.kts"},
            max_files=max_files,
            exclude_patterns=exclude_patterns,
        )
    )
    pom_files = list(
        walk_files(
            repo_root,
            extensions={"pom.xml"},
            max_files=max_files,
            exclude_patterns=exclude_patterns,
        )
    )

    if gradle_files:
        _parse_gradle(repo_root, gradle_files, info)
        _parse_version_catalog(repo_root, info)
    elif pom_files:
        _parse_maven(repo_root, pom_files, info)

    return info


def _parse_gradle(repo_root: Path, gradle_files: list[Path], info: BuildInfo) -> None:
    """Populate `info` from Gradle build scripts."""
    has_kts = any(f.name.endswith(".gradle.kts") for f in gradle_files)
    info.build_system = "gradle-kotlin-dsl" if has_kts else "gradle-groovy"

    for file_path in gradle_files:
        content = read_file_safe(file_path)
        if content is None:
            continue

        rel_path = get_relative_path(file_path, repo_root)
        info.build_files.append(rel_path)

        if file_path.name.startswith("settings.gradle"):
            info.modules.extend(_extract_gradle_modules(content))
            continue

        info.dependencies.extend(_extract_gradle_dependencies(content, rel_path))
        info.plugins.extend(_extract_gradle_plugins(content, rel_path))

        if info.kotlin_version is None:
            info.kotlin_version = _extract_kotlin_version(content)
        if info.jvm_target is None:
            info.jvm_target = _extract_jvm_target(content)

        if "libs." in content or "libs.versions.toml" in content:
            info.uses_version_catalog = True


def _extract_gradle_modules(content: str) -> list[str]:
    """Extract module names from settings.gradle include(...) calls."""
    modules = []
    # Matches include(":app", ":core") and include ':app', ':core'
    for match in re.finditer(r"include\s*\(?\s*((?:[\"'][^\"']+[\"']\s*,?\s*)+)\)?", content):
        for quoted in re.finditer(r"[\"']([^\"']+)[\"']", match.group(1)):
            modules.append(quoted.group(1).lstrip(":"))
    return modules


def _extract_gradle_dependencies(content: str, rel_path: str) -> list[Dependency]:
    """Extract dependency declarations from a Gradle build script."""
    dependencies = []
    configs = "|".join(DEPENDENCY_CONFIGURATIONS)

    # implementation("group:artifact:version") / implementation 'group:artifact:version'
    string_notation = re.compile(
        rf"\b({configs})\s*[\(\s]\s*[\"']([^\"':]+):([^\"':]+)(?::([^\"']+))?[\"']"
    )
    for match in string_notation.finditer(content):
        configuration, group, artifact, version = match.groups()
        dependencies.append(
            Dependency(
                group=group,
                artifact=artifact,
                version=version,
                configuration=configuration,
                source_file=rel_path,
                line=content[: match.start()].count("\n") + 1,
            )
        )

    # implementation(kotlin("stdlib")) -- the Kotlin DSL shorthand
    kotlin_notation = re.compile(rf"\b({configs})\s*\(\s*kotlin\s*\(\s*[\"']([^\"']+)[\"']")
    for match in kotlin_notation.finditer(content):
        configuration, artifact = match.groups()
        dependencies.append(
            Dependency(
                group="org.jetbrains.kotlin",
                artifact=f"kotlin-{artifact}",
                version=None,
                configuration=configuration,
                source_file=rel_path,
                line=content[: match.start()].count("\n") + 1,
            )
        )

    return dependencies


def _extract_gradle_plugins(content: str, rel_path: str) -> list[tuple[str, int, str]]:
    """Extract applied plugin ids from a Gradle build script.

    Plugin syntax overlaps with dependency syntax -- `kotlin("jvm")` applies a
    plugin but `implementation(kotlin("stdlib"))` declares a dependency -- so
    the block forms are only read inside `plugins { }`.
    """
    plugins = []

    for block, block_offset in _find_blocks(content, "plugins"):
        # id("org.springframework.boot") / id 'org.springframework.boot'
        for match in re.finditer(r"\bid\s*[\(\s]\s*[\"']([^\"']+)[\"']", block):
            line = content[: block_offset + match.start()].count("\n") + 1
            plugins.append((match.group(1), line, rel_path))

        # kotlin("jvm") / kotlin("plugin.serialization")
        for match in re.finditer(r"\bkotlin\s*\(\s*[\"']([^\"']+)[\"']\s*\)", block):
            line = content[: block_offset + match.start()].count("\n") + 1
            plugins.append((f"kotlin.{match.group(1)}", line, rel_path))

    # apply plugin: 'kotlin-android' -- legacy Groovy form, declared at top level
    for match in re.finditer(r"apply\s+plugin\s*:\s*[\"']([^\"']+)[\"']", content):
        line = content[: match.start()].count("\n") + 1
        plugins.append((match.group(1), line, rel_path))

    return plugins


def _find_blocks(content: str, name: str) -> list[tuple[str, int]]:
    """Find `name { ... }` blocks, returning (block_body, offset_of_body).

    Matches braces so nested blocks are captured whole.
    """
    blocks = []

    for match in re.finditer(rf"\b{re.escape(name)}\s*\{{", content):
        body_start = match.end()
        depth = 1
        i = body_start

        while i < len(content) and depth > 0:
            if content[i] == "{":
                depth += 1
            elif content[i] == "}":
                depth -= 1
            i += 1

        if depth == 0:
            blocks.append((content[body_start : i - 1], body_start))

    return blocks


def _extract_kotlin_version(content: str) -> Optional[str]:
    """Extract the declared Kotlin plugin/language version."""
    patterns = (
        r"kotlin\s*\(\s*[\"'][^\"']+[\"']\s*\)\s*version\s*[\"']([^\"']+)[\"']",
        r"kotlin_version\s*=\s*[\"']([^\"']+)[\"']",
        r"kotlinVersion\s*=\s*[\"']([^\"']+)[\"']",
    )
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    return None


def _extract_jvm_target(content: str) -> Optional[str]:
    """Extract the configured JVM target or toolchain."""
    patterns = (
        r"jvmToolchain\s*\(\s*(\d+)\s*\)",
        r"jvmTarget\s*(?:\.set\s*\(\s*)?=?\s*[\"']?(?:JVM_)?(\d+(?:\.\d+)?)[\"']?",
        r"targetCompatibility\s*=\s*[\"']?(?:JavaVersion\.VERSION_)?(\d+(?:[._]\d+)?)[\"']?",
    )
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1).replace("_", ".")
    return None


def _parse_version_catalog(repo_root: Path, info: BuildInfo) -> None:
    """Parse gradle/libs.versions.toml into `info.catalog_libraries`."""
    catalog_path = repo_root / "gradle" / "libs.versions.toml"
    content = read_file_safe(catalog_path)
    if content is None:
        return

    info.uses_version_catalog = True

    in_libraries = False
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if line.startswith("["):
            in_libraries = line.startswith("[libraries")
            continue
        if not in_libraries or "=" not in line or line.startswith("#"):
            continue

        alias, _, value = line.partition("=")
        alias = alias.strip()

        # module = "group:artifact"  or  group = "g", name = "a"
        module_match = re.search(r"module\s*=\s*[\"']([^\"']+)[\"']", value)
        if module_match:
            info.catalog_libraries[alias] = module_match.group(1)
            continue

        group_match = re.search(r"group\s*=\s*[\"']([^\"']+)[\"']", value)
        name_match = re.search(r"name\s*=\s*[\"']([^\"']+)[\"']", value)
        if group_match and name_match:
            info.catalog_libraries[alias] = f"{group_match.group(1)}:{name_match.group(1)}"
            continue

        # alias = "group:artifact:version"  -- shorthand string form
        shorthand = re.search(r"[\"']([^\"':]+:[^\"':]+)(?::[^\"']+)?[\"']", value)
        if shorthand:
            info.catalog_libraries[alias] = shorthand.group(1)


def _parse_maven(repo_root: Path, pom_files: list[Path], info: BuildInfo) -> None:
    """Populate `info` from Maven POM files."""
    info.build_system = "maven"

    dependency_block = re.compile(r"<dependency>(.*?)</dependency>", re.DOTALL)
    plugin_block = re.compile(r"<plugin>(.*?)</plugin>", re.DOTALL)

    for file_path in pom_files:
        content = read_file_safe(file_path)
        if content is None:
            continue

        rel_path = get_relative_path(file_path, repo_root)
        info.build_files.append(rel_path)

        for match in dependency_block.finditer(content):
            block = match.group(1)
            group = _xml_tag(block, "groupId")
            artifact = _xml_tag(block, "artifactId")
            if not group or not artifact:
                continue
            scope = _xml_tag(block, "scope") or "compile"
            info.dependencies.append(
                Dependency(
                    group=group,
                    artifact=artifact,
                    version=_xml_tag(block, "version"),
                    configuration="testImplementation" if scope == "test" else "implementation",
                    source_file=rel_path,
                    line=content[: match.start()].count("\n") + 1,
                )
            )

        for match in plugin_block.finditer(content):
            artifact = _xml_tag(match.group(1), "artifactId")
            if artifact:
                line = content[: match.start()].count("\n") + 1
                info.plugins.append((artifact, line, rel_path))

        if info.kotlin_version is None:
            info.kotlin_version = _xml_tag(content, "kotlin.version")
        if info.jvm_target is None:
            info.jvm_target = _xml_tag(content, "maven.compiler.target") or _xml_tag(
                content, "java.version"
            )


def _xml_tag(block: str, tag: str) -> Optional[str]:
    """Return the text content of the first `<tag>` in `block`."""
    match = re.search(rf"<{re.escape(tag)}>([^<]*)</{re.escape(tag)}>", block)
    return match.group(1).strip() if match else None
