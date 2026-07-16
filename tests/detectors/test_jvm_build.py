"""Tests for JVM build file parsing and JUnit convention detection."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from conventions.detectors.jvm.build import BuildInfo, Dependency, parse_build_files
from conventions.detectors.jvm.junit import detect_junit, find_test_class_naming

# NOTE: fixtures deliberately avoid "com/example/..." style package paths.
# src/conventions/fs.py HARD_EXCLUDES matches "example"/"examples"/"demo"/
# "docs"/"sample"/"samples"/"build"/"dist" against ANY path component, so a
# repo containing a "com/example" directory would be silently skipped by
# should_exclude. We use "com/acme" instead.


# ---------------------------------------------------------------------------
# Gradle Kotlin DSL
# ---------------------------------------------------------------------------


@pytest.fixture
def gradle_kts_repo(tmp_path: Path) -> Path:
    """A Gradle Kotlin DSL repo with plugins, kotlin block, and dependencies."""
    (tmp_path / "build.gradle.kts").write_text(
        "plugins {\n"
        '    kotlin("jvm") version "1.9.22"\n'
        '    id("org.springframework.boot") version "3.2.0"\n'
        "}\n"
        "\n"
        "kotlin {\n"
        "    jvmToolchain(17)\n"
        "}\n"
        "\n"
        "dependencies {\n"
        '    implementation("com.acme:my-lib:1.0.0")\n'
        '    testImplementation("org.junit.jupiter:junit-jupiter:5.10.0")\n'
        "    implementation(kotlin(\"stdlib\"))\n"
        "}\n"
    )
    return tmp_path


class TestGradleKotlinDsl:
    """Tests for parsing build.gradle.kts (Gradle Kotlin DSL)."""

    def test_build_system_is_gradle_kotlin_dsl(self, gradle_kts_repo: Path):
        info = parse_build_files(gradle_kts_repo)
        assert info.build_system == "gradle-kotlin-dsl"

    def test_kotlin_version_extracted(self, gradle_kts_repo: Path):
        info = parse_build_files(gradle_kts_repo)
        assert info.kotlin_version == "1.9.22"

    def test_jvm_target_extracted_from_toolchain(self, gradle_kts_repo: Path):
        info = parse_build_files(gradle_kts_repo)
        assert info.jvm_target == "17"

    def test_implementation_dependency_parsed(self, gradle_kts_repo: Path):
        info = parse_build_files(gradle_kts_repo)
        matches = [d for d in info.dependencies if d.artifact == "my-lib"]
        assert len(matches) == 1
        dep = matches[0]
        assert dep.group == "com.acme"
        assert dep.version == "1.0.0"
        assert dep.configuration == "implementation"
        assert dep.is_test_only is False

    def test_test_implementation_dependency_is_test_only(self, gradle_kts_repo: Path):
        info = parse_build_files(gradle_kts_repo)
        matches = [d for d in info.dependencies if d.artifact == "junit-jupiter"]
        assert len(matches) == 1
        dep = matches[0]
        assert dep.group == "org.junit.jupiter"
        assert dep.configuration == "testImplementation"
        assert dep.is_test_only is True

    def test_kotlin_stdlib_shorthand_maps_to_kotlin_group(self, gradle_kts_repo: Path):
        info = parse_build_files(gradle_kts_repo)
        matches = [d for d in info.dependencies if d.artifact == "kotlin-stdlib"]
        assert len(matches) == 1
        dep = matches[0]
        assert dep.group == "org.jetbrains.kotlin"
        assert dep.configuration == "implementation"


# ---------------------------------------------------------------------------
# Gradle Groovy DSL
# ---------------------------------------------------------------------------


@pytest.fixture
def gradle_groovy_repo(tmp_path: Path) -> Path:
    """A Gradle Groovy DSL repo with a legacy `apply plugin` and a dependency."""
    (tmp_path / "build.gradle").write_text(
        "apply plugin: 'kotlin-android'\n"
        "\n"
        "dependencies {\n"
        "    implementation 'com.acme:util:2.3.4'\n"
        "}\n"
    )
    return tmp_path


class TestGradleGroovyDsl:
    """Tests for parsing build.gradle (Gradle Groovy DSL)."""

    def test_build_system_is_gradle_groovy(self, gradle_groovy_repo: Path):
        info = parse_build_files(gradle_groovy_repo)
        assert info.build_system == "gradle-groovy"

    def test_single_quoted_dependency_parsed(self, gradle_groovy_repo: Path):
        info = parse_build_files(gradle_groovy_repo)
        matches = [d for d in info.dependencies if d.artifact == "util"]
        assert len(matches) == 1
        dep = matches[0]
        assert dep.group == "com.acme"
        assert dep.version == "2.3.4"
        assert dep.configuration == "implementation"

    def test_apply_plugin_syntax_is_picked_up(self, gradle_groovy_repo: Path):
        info = parse_build_files(gradle_groovy_repo)
        assert info.has_plugin("kotlin-android")


# ---------------------------------------------------------------------------
# Regression: plugin extraction must be scoped to plugins { } block
# ---------------------------------------------------------------------------


class TestPluginScopingRegression:
    """`kotlin("stdlib")` as a dependency must not be misread as an applied plugin."""

    def test_stdlib_dependency_not_misread_as_plugin(self, tmp_path: Path):
        (tmp_path / "build.gradle.kts").write_text(
            "plugins {\n"
            '    kotlin("jvm") version "1.9.22"\n'
            "}\n"
            "\n"
            "dependencies {\n"
            '    implementation(kotlin("stdlib"))\n'
            "}\n"
        )
        info = parse_build_files(tmp_path)

        plugin_ids = [p[0] for p in info.plugins]
        assert "kotlin.jvm" in plugin_ids
        assert "kotlin.stdlib" not in plugin_ids

        # The dependency itself must still be recorded.
        assert info.has_dependency("kotlin-stdlib")


# ---------------------------------------------------------------------------
# _find_blocks brace matching across nested blocks
# ---------------------------------------------------------------------------


class TestNestedBraces:
    """The plugins { } block must be found correctly alongside other nested blocks."""

    def test_plugins_block_found_amid_other_nested_blocks(self, tmp_path: Path):
        (tmp_path / "build.gradle.kts").write_text(
            "android {\n"
            "    buildFeatures {\n"
            "        compose = true\n"
            "    }\n"
            "}\n"
            "\n"
            "plugins {\n"
            '    id("com.acme.plugin")\n'
            '    kotlin("jvm") version "1.9.22"\n'
            "}\n"
            "\n"
            "kotlin {\n"
            "    jvmToolchain(17)\n"
            "}\n"
        )
        info = parse_build_files(tmp_path)

        plugin_ids = [p[0] for p in info.plugins]
        assert "com.acme.plugin" in plugin_ids
        assert "kotlin.jvm" in plugin_ids
        # A plugin id must not leak in from the unrelated `android` block.
        assert not any("compose" in pid for pid in plugin_ids)
        assert info.jvm_target == "17"


# ---------------------------------------------------------------------------
# settings.gradle.kts
# ---------------------------------------------------------------------------


class TestSettingsGradle:
    """Tests for module discovery via settings.gradle.kts include(...)."""

    def test_multi_module_include(self, tmp_path: Path):
        (tmp_path / "settings.gradle.kts").write_text(
            'rootProject.name = "myapp"\n'
            'include(":app", ":core")\n'
        )
        info = parse_build_files(tmp_path)
        assert info.modules == ["app", "core"]
        assert info.is_multi_module is True

    def test_single_module_include(self, tmp_path: Path):
        (tmp_path / "settings.gradle.kts").write_text(
            'rootProject.name = "myapp"\n'
            'include(":app")\n'
        )
        info = parse_build_files(tmp_path)
        assert info.modules == ["app"]
        assert info.is_multi_module is False


# ---------------------------------------------------------------------------
# Version catalog: gradle/libs.versions.toml
# ---------------------------------------------------------------------------


@pytest.fixture
def version_catalog_repo(tmp_path: Path) -> Path:
    """A Gradle repo using a version catalog with all three library forms."""
    (tmp_path / "build.gradle.kts").write_text(
        "plugins {\n"
        '    kotlin("jvm") version "1.9.22"\n'
        "}\n"
        "\n"
        "dependencies {\n"
        "    implementation(libs.kotlin.stdlib)\n"
        "}\n"
    )
    gradle_dir = tmp_path / "gradle"
    gradle_dir.mkdir()
    (gradle_dir / "libs.versions.toml").write_text(
        "[versions]\n"
        'kotlin = "1.9.22"\n'
        "\n"
        "[libraries]\n"
        'kotlin-stdlib = { module = "org.jetbrains.kotlin:kotlin-stdlib" }\n'
        'junit-jupiter = { group = "org.junit.jupiter", name = "junit-jupiter" }\n'
        'coroutines = "org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3"\n'
        "\n"
        "[plugins]\n"
        'kotlin-jvm = { id = "org.jetbrains.kotlin.jvm", version.ref = "kotlin" }\n'
    )
    return tmp_path


class TestVersionCatalog:
    """Tests for gradle/libs.versions.toml parsing."""

    def test_uses_version_catalog_flag(self, version_catalog_repo: Path):
        info = parse_build_files(version_catalog_repo)
        assert info.uses_version_catalog is True

    def test_module_form_parsed(self, version_catalog_repo: Path):
        info = parse_build_files(version_catalog_repo)
        assert info.catalog_libraries["kotlin-stdlib"] == "org.jetbrains.kotlin:kotlin-stdlib"

    def test_group_and_name_form_parsed(self, version_catalog_repo: Path):
        info = parse_build_files(version_catalog_repo)
        assert info.catalog_libraries["junit-jupiter"] == "org.junit.jupiter:junit-jupiter"

    def test_shorthand_string_form_parsed(self, version_catalog_repo: Path):
        info = parse_build_files(version_catalog_repo)
        assert (
            info.catalog_libraries["coroutines"]
            == "org.jetbrains.kotlinx:kotlinx-coroutines-core"
        )

    def test_versions_and_plugins_sections_not_parsed_as_libraries(
        self, version_catalog_repo: Path
    ):
        info = parse_build_files(version_catalog_repo)
        assert "kotlin" not in info.catalog_libraries
        assert "kotlin-jvm" not in info.catalog_libraries
        assert len(info.catalog_libraries) == 3


# ---------------------------------------------------------------------------
# Maven
# ---------------------------------------------------------------------------


@pytest.fixture
def maven_repo(tmp_path: Path) -> Path:
    """A Maven repo with a compile-scope dep, a test-scope dep, and a plugin."""
    (tmp_path / "pom.xml").write_text(
        "<project>\n"
        "  <dependencies>\n"
        "    <dependency>\n"
        "      <groupId>com.acme</groupId>\n"
        "      <artifactId>core-lib</artifactId>\n"
        "      <version>1.2.3</version>\n"
        "    </dependency>\n"
        "    <dependency>\n"
        "      <groupId>org.junit.jupiter</groupId>\n"
        "      <artifactId>junit-jupiter</artifactId>\n"
        "      <version>5.10.0</version>\n"
        "      <scope>test</scope>\n"
        "    </dependency>\n"
        "  </dependencies>\n"
        "  <build>\n"
        "    <plugins>\n"
        "      <plugin>\n"
        "        <groupId>org.apache.maven.plugins</groupId>\n"
        "        <artifactId>maven-compiler-plugin</artifactId>\n"
        "        <version>3.11.0</version>\n"
        "      </plugin>\n"
        "    </plugins>\n"
        "  </build>\n"
        "  <properties>\n"
        "    <maven.compiler.target>17</maven.compiler.target>\n"
        "  </properties>\n"
        "</project>\n"
    )
    return tmp_path


class TestMaven:
    """Tests for parsing pom.xml."""

    def test_build_system_is_maven(self, maven_repo: Path):
        info = parse_build_files(maven_repo)
        assert info.build_system == "maven"

    def test_compile_scope_dependency(self, maven_repo: Path):
        info = parse_build_files(maven_repo)
        matches = [d for d in info.dependencies if d.artifact == "core-lib"]
        assert len(matches) == 1
        dep = matches[0]
        assert dep.group == "com.acme"
        assert dep.version == "1.2.3"
        assert dep.configuration == "implementation"
        assert dep.is_test_only is False

    def test_test_scope_dependency_maps_to_test_implementation(self, maven_repo: Path):
        info = parse_build_files(maven_repo)
        matches = [d for d in info.dependencies if d.artifact == "junit-jupiter"]
        assert len(matches) == 1
        dep = matches[0]
        assert dep.configuration == "testImplementation"
        assert dep.is_test_only is True

    def test_plugin_artifact_id_extracted(self, maven_repo: Path):
        info = parse_build_files(maven_repo)
        assert info.has_plugin("maven-compiler-plugin")

    def test_jvm_target_from_compiler_target_property(self, maven_repo: Path):
        info = parse_build_files(maven_repo)
        assert info.jvm_target == "17"


# ---------------------------------------------------------------------------
# Precedence: Gradle wins when both Gradle and Maven files exist
# ---------------------------------------------------------------------------


class TestPrecedence:
    """Gradle build files take precedence over a coexisting pom.xml."""

    def test_gradle_wins_over_maven(self, tmp_path: Path):
        (tmp_path / "build.gradle.kts").write_text(
            "plugins {\n"
            '    kotlin("jvm") version "1.9.22"\n'
            "}\n"
        )
        (tmp_path / "pom.xml").write_text(
            "<project>\n"
            "  <dependencies>\n"
            "    <dependency>\n"
            "      <groupId>com.acme</groupId>\n"
            "      <artifactId>core-lib</artifactId>\n"
            "      <version>1.2.3</version>\n"
            "    </dependency>\n"
            "  </dependencies>\n"
            "</project>\n"
        )
        info = parse_build_files(tmp_path)
        assert info.build_system.startswith("gradle")
        assert info.has_plugin("kotlin.jvm")
        # Maven-only dependency must not have been parsed.
        assert not info.has_dependency("core-lib")


# ---------------------------------------------------------------------------
# Empty repo
# ---------------------------------------------------------------------------


class TestEmptyRepo:
    """No build files present must not raise and yields an 'unknown' result."""

    def test_no_build_files(self, tmp_path: Path):
        (tmp_path / "README.md").write_text("# Empty repo\n")
        info = parse_build_files(tmp_path)
        assert info.build_system == "unknown"
        assert info.build_files == []
        assert info.dependencies == []
        assert info.plugins == []
        assert info.modules == []
        assert info.is_multi_module is False


# ---------------------------------------------------------------------------
# BuildInfo helper methods
# ---------------------------------------------------------------------------


class TestBuildInfoHelpers:
    """Tests for BuildInfo/Dependency convenience methods."""

    def test_has_dependency_is_substring_match(self):
        dep = Dependency(
            group="org.jetbrains.kotlinx",
            artifact="kotlinx-coroutines-core",
            version="1.7.3",
            configuration="implementation",
            source_file="build.gradle.kts",
            line=1,
        )
        info = BuildInfo(dependencies=[dep])
        assert info.has_dependency("kotlinx-coroutines")
        assert not info.has_dependency("nonexistent-lib")

    def test_find_dependencies_filters_by_substring(self):
        acme_dep = Dependency(
            group="com.acme",
            artifact="core",
            version="1.0",
            configuration="implementation",
            source_file="build.gradle.kts",
            line=1,
        )
        other_dep = Dependency(
            group="org.other",
            artifact="thing",
            version="2.0",
            configuration="implementation",
            source_file="build.gradle.kts",
            line=2,
        )
        info = BuildInfo(dependencies=[acme_dep, other_dep])
        found = info.find_dependencies("acme")
        assert found == [acme_dep]

    def test_has_plugin_is_substring_match(self):
        info = BuildInfo(plugins=[("org.springframework.boot", 3, "build.gradle.kts")])
        assert info.has_plugin("springframework")
        assert not info.has_plugin("android")

    def test_dependency_coordinate(self):
        dep = Dependency(
            group="com.acme",
            artifact="core",
            version="1.0",
            configuration="implementation",
            source_file="build.gradle.kts",
            line=1,
        )
        assert dep.coordinate == "com.acme:core"


# ---------------------------------------------------------------------------
# detect_junit
# ---------------------------------------------------------------------------


class FakeIndex:
    """Minimal stand-in for a language index, sufficient for detect_junit."""

    def __init__(self, imports: list[str], annotation_counts: dict[str, int]):
        self.imports = imports
        self.annotation_counts = annotation_counts

    def count_imports_matching(self, pattern: str) -> int:
        return sum(1 for imp in self.imports if pattern in imp)

    def _name_for(self, pattern: str) -> str:
        match = re.search(r"@(\w+)", pattern)
        return match.group(1) if match else pattern

    def search_pattern(
        self, pattern: str, limit: int = 100, exclude_tests: bool = False
    ) -> list[tuple[str, int, str]]:
        name = self._name_for(pattern)
        count = self.annotation_counts.get(name, 0)
        # Truncates at `limit`, exactly like the real index -- which is why
        # counts must come from count_pattern instead.
        return [(f"Foo{i}.kt", i + 1, f"@{name}") for i in range(min(count, limit))]

    def count_pattern(self, pattern: str, exclude_tests: bool = False) -> int:
        # Unbounded, like the real index.
        return self.annotation_counts.get(self._name_for(pattern), 0)


class TestDetectJunit:
    """Tests for JUnit version and annotation-usage detection."""

    def test_junit5_detected_from_jupiter_imports(self):
        idx = FakeIndex(
            imports=["org.junit.jupiter.api.Test", "org.junit.jupiter.api.BeforeEach"],
            annotation_counts={"Test": 3, "BeforeEach": 1},
        )
        info = detect_junit(idx)
        assert info.major_version == 5
        assert info.is_present is True

    def test_junit4_detected_with_corroborating_annotation(self):
        idx = FakeIndex(
            imports=["org.junit.Test", "org.junit.Before"],
            annotation_counts={"Test": 2, "Before": 1},
        )
        info = detect_junit(idx)
        assert info.major_version == 4

    def test_jupiter_only_imports_not_misread_as_junit4(self):
        # "org.junit." is a string prefix of "org.junit.jupiter.", so a naive
        # substring check against JUNIT4_IMPORT would also match jupiter-only
        # imports. Confirm the stub really does substring-match here, and that
        # detect_junit still correctly prioritizes the JUnit 5 check.
        idx = FakeIndex(
            imports=["org.junit.jupiter.api.Test"],
            annotation_counts={"Test": 4},
        )
        assert idx.count_imports_matching("org.junit.") > 0
        info = detect_junit(idx)
        assert info.major_version == 5

    def test_parameterized_test_pushes_to_5_without_imports(self):
        idx = FakeIndex(imports=[], annotation_counts={"Test": 1, "ParameterizedTest": 2})
        info = detect_junit(idx)
        assert info.major_version == 5
        assert info.uses_parameterized is True

    def test_nested_pushes_to_5_without_imports(self):
        idx = FakeIndex(imports=[], annotation_counts={"Test": 1, "Nested": 1})
        info = detect_junit(idx)
        assert info.major_version == 5
        assert info.uses_nested is True

    def test_bare_test_with_no_imports_defaults_to_5(self):
        idx = FakeIndex(imports=[], annotation_counts={"Test": 1})
        info = detect_junit(idx)
        assert info.major_version == 5

    def test_no_annotations_means_absent(self):
        idx = FakeIndex(imports=[], annotation_counts={})
        info = detect_junit(idx)
        assert info.major_version is None
        assert info.is_present is False

    def test_test_method_count_and_examples_capped_at_three(self):
        idx = FakeIndex(imports=[], annotation_counts={"Test": 5})
        info = detect_junit(idx)
        assert info.test_method_count == 5
        assert len(info.examples) == 3

    def test_display_name_and_5_only_flags(self):
        idx = FakeIndex(
            imports=["org.junit.jupiter.api.Test"],
            annotation_counts={
                "Test": 2,
                "DisplayName": 1,
                "Nested": 1,
                "ParameterizedTest": 1,
            },
        )
        info = detect_junit(idx)
        assert info.major_version == 5
        assert info.uses_nested is True
        assert info.uses_parameterized is True
        assert info.uses_display_name is True


class TestJunitCountsAreNotCapped:
    """Counts must not saturate at a search limit.

    Regression: detect_junit derived counts from len(search_pattern(limit=100)),
    so every repo with more than 100 tests reported exactly 100. Real-world
    okhttp has ~2800 @Test occurrences and was reported as 100.
    """

    def test_test_count_exceeds_any_search_limit(self):
        idx = FakeIndex(
            imports=["org.junit.jupiter.api.Test"],
            annotation_counts={"Test": 2817},
        )
        info = detect_junit(idx)
        assert info.test_method_count == 2817
        assert info.annotation_counts["Test"] == 2817

    def test_examples_stay_capped_while_count_does_not(self):
        """Evidence stays bounded even though the count is complete."""
        idx = FakeIndex(
            imports=["org.junit.jupiter.api.Test"],
            annotation_counts={"Test": 500},
        )
        info = detect_junit(idx, example_limit=3)
        assert info.test_method_count == 500
        assert len(info.examples) == 3

    def test_class_naming_counts_not_capped(self):
        idx = FakeIndex(imports=[], annotation_counts={})
        idx.annotation_counts[r"\bclass\s+\w+Test\b"] = 300
        counts = find_test_class_naming(idx)
        assert counts["suffix_test"] == 300
