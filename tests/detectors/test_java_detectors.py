"""Integration tests for Java convention detectors."""

from __future__ import annotations

from pathlib import Path

from conventions.detectors.base import DetectorContext
from conventions.detectors.java import (
    JavaArchitectureDetector,
    JavaBuildDetector,
    JavaConventionsDetector,
    JavaDatabaseDetector,
    JavaDIDetector,
    JavaIndex,
    JavaLoggingDetector,
    JavaTestingDetector,
)
from conventions.ratings import rate_convention


def _write(path: Path, content: str) -> None:
    """Write `content` to `path`, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _ctx(repo_root: Path) -> DetectorContext:
    return DetectorContext(
        repo_root=repo_root,
        selected_languages={"java"},
        max_files=200,
    )


# ---------------------------------------------------------------------------
# Test Indexer
# ---------------------------------------------------------------------------

def test_java_indexer(tmp_path: Path):
    _write(
        tmp_path / "src/main/java/com/acme/app/UserService.java",
        """
        package com.acme.app;

        import org.springframework.stereotype.Service;
        import java.util.List;

        /**
         * This is a service.
         */
        @Service
        public class UserService {
            private final UserRepository repo;

            // Constructor
            public UserService(UserRepository repo) {
                this.repo = repo;
            }

            public List<User> getUsers() {
                // TODO: add pagination
                return repo.findAll();
            }
        }
        """,
    )

    index = JavaIndex(tmp_path)
    index.build()

    assert len(index.files) == 1
    file_idx = index.files["src/main/java/com/acme/app/UserService.java"]
    assert file_idx.package == "com.acme.app"
    assert len(file_idx.imports) == 2
    assert file_idx.imports[0][0] == "org.springframework.stereotype.Service"
    assert len(file_idx.classes) == 1
    assert file_idx.classes[0].name == "UserService"
    assert file_idx.classes[0].kind == "class"
    assert file_idx.classes[0].annotations == ["Service"]
    assert len(file_idx.functions) == 2
    assert file_idx.functions[0].name == "UserService"
    assert file_idx.functions[1].name == "getUsers"
    assert file_idx.todo_count == 1


# ---------------------------------------------------------------------------
# Test Architecture Detector
# ---------------------------------------------------------------------------

def test_java_architecture_detector(tmp_path: Path):
    _write(
        tmp_path / "src/main/java/com/acme/app/controller/UserController.java",
        """
        package com.acme.app.controller;
        import org.springframework.web.bind.annotation.RestController;
        @RestController
        public class UserController {}
        """,
    )
    _write(
        tmp_path / "src/main/java/com/acme/app/service/UserService.java",
        """
        package com.acme.app.service;
        import org.springframework.stereotype.Service;
        @Service
        public class UserService {}
        """,
    )

    ctx = _ctx(tmp_path)
    detector = JavaArchitectureDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.id == "java.conventions.architecture"
    assert rule.stats["structure"] == "single-module"
    assert "service" in rule.stats["layers"]
    assert "api" in rule.stats["layers"]
    assert rule.stats["package_style"] == "package-by-layer"
    assert rule.stats["framework"] == "Spring Boot"

    score, _, _ = rate_convention(rule)
    assert score >= 4


# ---------------------------------------------------------------------------
# Test Database Detector
# ---------------------------------------------------------------------------

def test_java_database_detector(tmp_path: Path):
    # Standard JPA / Hibernate setup
    _write(
        tmp_path / "src/main/java/com/acme/app/db/UserRepository.java",
        """
        package com.acme.app.db;
        import jakarta.persistence.Entity;
        import org.springframework.data.jpa.repository.JpaRepository;
        public interface UserRepository extends JpaRepository<User, Long> {}
        """,
    )
    # Flyway migration resource directory
    (tmp_path / "src/main/resources/db/migration").mkdir(parents=True)
    _write(tmp_path / "src/main/resources/db/migration/V1__init.sql", "CREATE TABLE users;")

    ctx = _ctx(tmp_path)
    detector = JavaDatabaseDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.id == "java.conventions.database"
    assert "Spring Data JPA" in rule.stats["libraries"]
    assert rule.stats["migration_tool"] == "Flyway"
    assert rule.stats["repository_count"] == 1
    assert rule.stats["raw_sql_concat_count"] == 0

    score, _, _ = rate_convention(rule)
    assert score == 5


def test_java_database_sql_injection_warning(tmp_path: Path):
    _write(
        tmp_path / "src/main/java/com/acme/app/db/UserDao.java",
        """
        package com.acme.app.db;
        import java.sql.Connection;
        public class UserDao {
            public void findUser(String name, Connection conn) {
                String sql = "SELECT * FROM users WHERE name = '" + name + "'";
                conn.createStatement().execute(sql);
            }
        }
        """,
    )

    ctx = _ctx(tmp_path)
    detector = JavaDatabaseDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.stats["raw_sql_concat_count"] == 1
    # The finding rides on the rule, not the detector-failure channel.
    assert "SQL concatenation" in rule.description
    assert result.warnings == []

    score, _, _ = rate_convention(rule)
    assert score == 2


# ---------------------------------------------------------------------------
# Test DI Detector
# ---------------------------------------------------------------------------

def test_java_di_detector_constructor(tmp_path: Path):
    _write(
        tmp_path / "src/main/java/com/acme/app/service/UserService.java",
        """
        package com.acme.app.service;
        import org.springframework.beans.factory.annotation.Autowired;
        public class UserService {
            private final Repo repo;
            @Autowired
            public UserService(Repo repo) {
                this.repo = repo;
            }
        }
        """,
    )

    ctx = _ctx(tmp_path)
    detector = JavaDIDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.id == "java.conventions.di"
    assert "Spring DI" in rule.stats["frameworks"]
    assert rule.stats["primary_style"] == "constructor"

    score, _, _ = rate_convention(rule)
    assert score == 5


def test_java_di_detector_field(tmp_path: Path):
    _write(
        tmp_path / "src/main/java/com/acme/app/service/UserService.java",
        """
        package com.acme.app.service;
        import org.springframework.beans.factory.annotation.Autowired;
        public class UserService {
            @Autowired
            private Repo repo;
        }
        """,
    )

    ctx = _ctx(tmp_path)
    detector = JavaDIDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.stats["primary_style"] == "field"

    score, _, _ = rate_convention(rule)
    assert score == 3


# ---------------------------------------------------------------------------
# Test Logging Detector
# ---------------------------------------------------------------------------

def test_java_logging_detector_slf4j(tmp_path: Path):
    _write(
        tmp_path / "src/main/java/com/acme/app/Service.java",
        """
        package com.acme.app;
        import org.slf4j.Logger;
        import org.slf4j.LoggerFactory;
        public class Service {
            private static final Logger log = LoggerFactory.getLogger(Service.class);
            public void doWork() {
                log.info("working");
            }
        }
        """,
    )

    ctx = _ctx(tmp_path)
    detector = JavaLoggingDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.id == "java.conventions.logging"
    assert rule.stats["primary_framework"] == "slf4j"
    assert rule.stats["raw_print_count"] == 0

    score, _, _ = rate_convention(rule)
    assert score == 5


def test_java_logging_detector_raw_print(tmp_path: Path):
    _write(
        tmp_path / "src/main/java/com/acme/app/Service.java",
        """
        package com.acme.app;
        import org.slf4j.Logger;
        public class Service {
            public void doWork() {
                System.out.println("working");
            }
        }
        """,
    )

    ctx = _ctx(tmp_path)
    detector = JavaLoggingDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.stats["raw_print_count"] == 1
    assert "console print" in rule.description
    assert result.warnings == []

    score, _, _ = rate_convention(rule)
    assert score == 3


# ---------------------------------------------------------------------------
# Test Testing Detector
# ---------------------------------------------------------------------------

def test_java_testing_detector(tmp_path: Path):
    _write(
        tmp_path / "src/test/java/com/acme/app/ServiceTest.java",
        """
        package com.acme.app;
        import org.junit.jupiter.api.Test;
        import static org.assertj.core.api.Assertions.assertThat;
        public class ServiceTest {
            @Test
            public void testOne() {
                assertThat(1).isEqualTo(1);
            }
        }
        """,
    )

    ctx = _ctx(tmp_path)
    detector = JavaTestingDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.id == "java.conventions.testing"
    assert rule.stats["test_file_count"] == 1
    assert "JUnit 5" in rule.stats["frameworks"]
    assert "AssertJ" in rule.stats["frameworks"]
    assert rule.stats["primary_naming"] == "suffix_test"

    score, _, _ = rate_convention(rule)
    assert score == 3  # < 3 files is Average


# ---------------------------------------------------------------------------
# Test Conventions Detector
# ---------------------------------------------------------------------------

def test_java_conventions_detector(tmp_path: Path):
    _write(
        tmp_path / "src/main/java/com/acme/app/User.java",
        """
        package com.acme.app;
        import lombok.Data;
        @Data
        public class User {
            private String name;
        }
        """,
    )
    _write(
        tmp_path / "src/main/java/com/acme/app/Processor.java",
        """
        package com.acme.app;
        import java.util.List;
        import java.util.Optional;
        public class Processor {
            public Optional<String> process(List<String> items) {
                return items.stream()
                    .filter(i -> i != null)
                    .map(String::toUpperCase)
                    .findFirst();
            }
        }
        """,
    )

    ctx = _ctx(tmp_path)
    detector = JavaConventionsDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 4
    rule = result.rules[0]
    assert rule.id == "java.conventions.general"
    assert rule.stats["data_class_style"] == "Lombok annotations"
    assert rule.stats["fp_style"] == "functional (Streams & Lambdas)"
    assert rule.stats["null_safety_style"] == "Optional wrapper type"

    score, _, _ = rate_convention(rule)
    assert score == 5


# ---------------------------------------------------------------------------
# Regression: detectors must survive a real build file
# ---------------------------------------------------------------------------

_POM_WITH_DEPS = """<project>
  <groupId>com.acme</groupId>
  <artifactId>app</artifactId>
  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-data-jpa</artifactId>
      <version>3.2.0</version>
    </dependency>
    <dependency>
      <groupId>org.postgresql</groupId>
      <artifactId>postgresql</artifactId>
      <version>42.7.1</version>
    </dependency>
    <dependency>
      <groupId>com.google.testparameterinjector</groupId>
      <artifactId>test-parameter-injector</artifactId>
      <version>1.15</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
</project>
"""


class TestDetectorsWithBuildFile:
    """Every Java detector must run against a repo that declares dependencies.

    Regression: java_di and java_database did `set(build_info.dependencies)`.
    Dependency is an unhashable dataclass, so both crashed on any repo with a
    build file -- every real project. The fixtures here previously had no
    pom.xml/build.gradle at all, so `set([])` never raised and the suite stayed
    green while the detectors failed on Spring PetClinic.
    """

    def _repo(self, tmp_path: Path) -> Path:
        _write(tmp_path / "pom.xml", _POM_WITH_DEPS)
        _write(
            tmp_path / "src/main/java/com/acme/app/UserRepository.java",
            """package com.acme.app;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
}
""",
        )
        return tmp_path

    def test_no_detector_raises_with_dependencies_present(self, tmp_path: Path):
        repo = self._repo(tmp_path)
        ctx = _ctx(repo)
        for detector_cls in (
            JavaArchitectureDetector,
            JavaConventionsDetector,
            JavaDatabaseDetector,
            JavaDIDetector,
            JavaLoggingDetector,
            JavaTestingDetector,
        ):
            # Must not raise.
            detector_cls().detect(ctx)

    def test_database_reads_dependencies(self, tmp_path: Path):
        repo = self._repo(tmp_path)
        rules = JavaDatabaseDetector().detect(_ctx(repo)).rules
        assert rules
        stats = rules[0].stats
        assert "Spring Data JPA" in stats["libraries"]
        assert stats["driver"] == "postgresql"

    def test_di_reads_dependencies(self, tmp_path: Path):
        repo = self._repo(tmp_path)
        rules = JavaDIDetector().detect(_ctx(repo)).rules
        assert rules
        assert "Spring DI" in rules[0].stats["frameworks"]


class TestSignalsAreNotOverBroad:
    """Framework signals must not fire on incidental names.

    Both regressions were found by scanning real repositories.
    """

    def test_test_parameter_injector_is_not_cdi(self, tmp_path: Path):
        """`has_dependency` is a substring test: "inject" matched
        com.google.testparameterinjector:test-parameter-injector, so gson (which
        uses no DI at all) was reported as using CDI/JSR-330."""
        _write(tmp_path / "pom.xml", _POM_WITH_DEPS)
        _write(
            tmp_path / "src/main/java/com/acme/app/Plain.java",
            "package com.acme.app;\n\npublic class Plain {}\n",
        )
        rules = JavaDIDetector().detect(_ctx(tmp_path)).rules
        for r in rules:
            assert "CDI (JSR-330)" not in r.stats["frameworks"]

    def test_java_sql_date_types_are_not_jdbc(self, tmp_path: Path):
        """java.sql.Timestamp/Time are value types, not database access. gson
        imports them for its date adapters and was reported as a JDBC client."""
        _write(
            tmp_path / "src/main/java/com/acme/app/SqlTimeAdapter.java",
            """package com.acme.app;

import java.sql.Time;
import java.sql.Timestamp;

public class SqlTimeAdapter {
    private Timestamp ts;
    private Time t;
}
""",
        )
        rules = JavaDatabaseDetector().detect(_ctx(tmp_path)).rules
        for r in rules:
            assert "JDBC" not in r.stats["libraries"]

    def test_spring_value_annotation_is_not_lombok(self, tmp_path: Path):
        """Spring's @Value (property injection) is not Lombok's @Value.
        Spring PetClinic uses no Lombok but was reported as using it."""
        _write(
            tmp_path / "src/main/java/com/acme/app/Config.java",
            """package com.acme.app;

import org.springframework.beans.factory.annotation.Value;

public class Config {
    @Value("${app.name}")
    private String name;
}
""",
        )
        rules = JavaConventionsDetector().detect(_ctx(tmp_path)).rules
        for r in rules:
            assert r.stats.get("data_class_style") != "Lombok annotations"

    def test_lombok_detected_when_actually_imported(self, tmp_path: Path):
        _write(
            tmp_path / "src/main/java/com/acme/app/User.java",
            """package com.acme.app;

import lombok.Data;

@Data
public class User {
    private String name;
}
""",
        )
        rules = JavaConventionsDetector().detect(_ctx(tmp_path)).rules
        assert rules
        assert rules[0].stats.get("data_class_style") == "Lombok annotations"


class TestJavaBuildDetector:
    """Java build tooling drives the Build/Test commands in CLAUDE.md."""

    def test_maven_build_detected(self, tmp_path: Path):
        _write(tmp_path / "pom.xml", _POM_WITH_DEPS)
        rules = JavaBuildDetector().detect(_ctx(tmp_path)).rules
        assert rules
        stats = rules[0].stats
        assert stats["build_system"] == "maven"
        # `primary_tool` is what the CLAUDE.md renderer reads to pick commands.
        assert stats["primary_tool"] == "maven"
        assert stats["dependency_count"] == 3
        assert stats["test_dependency_count"] == 1

    def test_gradle_build_detected(self, tmp_path: Path):
        _write(
            tmp_path / "build.gradle.kts",
            'plugins {\n    id("java")\n    id("jacoco")\n}\n'
            "java { toolchain { languageVersion = 17 } }\n"
            'dependencies {\n    implementation("com.acme:lib:1.0")\n}\n',
        )
        rules = JavaBuildDetector().detect(_ctx(tmp_path)).rules
        assert rules
        stats = rules[0].stats
        assert stats["primary_tool"] == "gradle"
        assert "jacoco" in stats["quality_plugins"]

    def test_no_build_file_emits_no_rule(self, tmp_path: Path):
        _write(
            tmp_path / "src/main/java/com/acme/app/A.java",
            "package com.acme.app;\n\npublic class A {}\n",
        )
        assert JavaBuildDetector().detect(_ctx(tmp_path)).rules == []

    def test_rule_is_rated(self, tmp_path: Path):
        _write(tmp_path / "pom.xml", _POM_WITH_DEPS)
        rules = JavaBuildDetector().detect(_ctx(tmp_path)).rules
        score, reason, _suggestion = rate_convention(rules[0])
        assert 1 <= score <= 5
        assert "maven" in reason


class TestDominantPackageRoot:
    """The package root must survive an outlier package.

    Regression: a strict common prefix collapsed gson's root to "com", because
    18 of its files sit under com.example (JPMS/native-image test modules)
    against 241 under com.google.gson.
    """

    def test_outlier_package_does_not_collapse_root(self, tmp_path: Path):
        for i in range(9):
            _write(
                tmp_path / f"src/main/java/com/acme/gson/T{i}.java",
                f"package com.acme.gson;\n\npublic class T{i} {{}}\n",
            )
        # A single outlier module under a different root.
        _write(
            tmp_path / "test-jpms/src/main/java/com/other/demo/Odd.java",
            "package com.other.demo;\n\npublic class Odd {}\n",
        )
        rules = JavaArchitectureDetector().detect(_ctx(tmp_path)).rules
        assert rules
        assert rules[0].stats["common_package_root"] == "com.acme.gson"

    def test_genuinely_split_roots_stop_early(self, tmp_path: Path):
        """With no dominant root, the prefix stops rather than inventing one."""
        for i in range(5):
            _write(
                tmp_path / f"src/main/java/com/acme/alpha/A{i}.java",
                f"package com.acme.alpha;\n\npublic class A{i} {{}}\n",
            )
        for i in range(5):
            _write(
                tmp_path / f"src/main/java/com/acme/beta/B{i}.java",
                f"package com.acme.beta;\n\npublic class B{i} {{}}\n",
            )
        rules = JavaArchitectureDetector().detect(_ctx(tmp_path)).rules
        assert rules
        assert rules[0].stats["common_package_root"] == "com.acme"
