"""Integration tests for Kotlin convention detectors."""
from __future__ import annotations

import json
from pathlib import Path

from conventions.detectors.base import DetectorContext
from conventions.detectors.kotlin import (
    KotlinAndroidDetector,
    KotlinArchitectureDetector,
    KotlinCoroutinesDetector,
    KotlinDatabaseDetector,
    KotlinDataFlowDetector,
    KotlinDetector,
    KotlinDIDetector,
    KotlinDocumentationDetector,
    KotlinErrorHandlingDetector,
    KotlinGradleDetector,
    KotlinLoggingDetector,
    KotlinNullSafetyDetector,
    KotlinSerializationDetector,
    KotlinTestingDetector,
    KotlinWebDetector,
)
from conventions.ratings import RATING_RULES, rate_convention

# NOTE: `com/example/...` is silently skipped by fs.should_exclude's
# HARD_EXCLUDES (it matches "example" against any path component), so all
# fixtures below use `com/acme/...` package paths instead.

ALL_KOTLIN_DETECTOR_CLASSES: list[type[KotlinDetector]] = [
    KotlinAndroidDetector,
    KotlinArchitectureDetector,
    KotlinCoroutinesDetector,
    KotlinDatabaseDetector,
    KotlinDataFlowDetector,
    KotlinDIDetector,
    KotlinDocumentationDetector,
    KotlinErrorHandlingDetector,
    KotlinGradleDetector,
    KotlinLoggingDetector,
    KotlinNullSafetyDetector,
    KotlinSerializationDetector,
    KotlinTestingDetector,
    KotlinWebDetector,
]


def _write(path: Path, content: str) -> None:
    """Write `content` to `path`, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _ctx(repo_root: Path) -> DetectorContext:
    return DetectorContext(
        repo_root=repo_root,
        selected_languages={"kotlin"},
        max_files=200,
    )


# ---------------------------------------------------------------------------
# Fixture builders
# ---------------------------------------------------------------------------


def _null_safety_signal_repo(tmp_path: Path) -> Path:
    """Production `!!` plus a test-only `!!`, so the two counters diverge."""
    _write(
        tmp_path / "src/main/kotlin/com/acme/app/UserService.kt",
        """
package com.acme.app

class UserService(private val repository: UserRepository) {
    fun getUser(id: String): User {
        val user = repository.find(id)!!
        return user
    }
}
""",
    )
    _write(
        tmp_path / "src/test/kotlin/com/acme/app/UserServiceTest.kt",
        """
package com.acme.app

import org.junit.jupiter.api.Test

class UserServiceTest {
    @Test
    fun testGetUser() {
        val service = UserService(FakeRepo())
        val user = service.getUser("1")!!
        check(user.id == "1")
    }
}
""",
    )
    return tmp_path


def _null_safety_safe_only_repo(tmp_path: Path) -> Path:
    """No `!!` at all -- only safe calls, elvis, and requireNotNull."""
    _write(
        tmp_path / "src/main/kotlin/com/acme/app/Greeter.kt",
        """
package com.acme.app

class Greeter(private val name: String?) {
    fun greet(): String {
        val safeName = name?.trim()
        val checked = requireNotNull(safeName) { "name required" }
        return checked ?: "anonymous"
    }
}
""",
    )
    return tmp_path


def _no_nullable_signal_repo(tmp_path: Path) -> Path:
    """Plain Kotlin with no null-safety signal of any kind."""
    _write(
        tmp_path / "src/main/kotlin/com/acme/app/Calculator.kt",
        """
package com.acme.app

class Calculator {
    fun add(a: Int, b: Int): Int {
        return a + b
    }

    fun subtract(a: Int, b: Int): Int {
        return a - b
    }
}
""",
    )
    return tmp_path


def _coroutines_signal_repo(tmp_path: Path) -> Path:
    """Suspend functions, Flow/StateFlow, and a GlobalScope anti-pattern."""
    _write(
        tmp_path / "src/main/kotlin/com/acme/app/Repo.kt",
        """
package com.acme.app

import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.StateFlow

class Repo {
    suspend fun fetch(): String {
        return "data"
    }

    fun observe(): Flow<String> = TODO()

    val state: StateFlow<String> get() = TODO()

    fun leak() {
        GlobalScope.launch {
            fetch()
        }
    }
}
""",
    )
    return tmp_path


def _coroutines_runblocking_production_repo(tmp_path: Path) -> Path:
    """`runBlocking` used directly in production (non-test) code."""
    _write(
        tmp_path / "src/main/kotlin/com/acme/app/Bootstrap.kt",
        """
package com.acme.app

import kotlinx.coroutines.runBlocking

class Bootstrap {
    fun start() {
        runBlocking {
            println("starting")
        }
    }
}
""",
    )
    return tmp_path


def _coroutines_runblocking_test_only_repo(tmp_path: Path) -> Path:
    """`runBlocking` used only inside a test file -- must not count as production."""
    _write(
        tmp_path / "src/main/kotlin/com/acme/app/Repo.kt",
        """
package com.acme.app

class Repo {
    suspend fun fetch(): String {
        return "data"
    }
}
""",
    )
    _write(
        tmp_path / "src/test/kotlin/com/acme/app/RepoTest.kt",
        """
package com.acme.app

import kotlinx.coroutines.runBlocking
import org.junit.jupiter.api.Test

class RepoTest {
    @Test
    fun testFetch() {
        runBlocking {
            Repo().fetch()
        }
    }
}
""",
    )
    return tmp_path


def _no_coroutines_repo(tmp_path: Path) -> Path:
    """No coroutine signal of any kind."""
    _write(
        tmp_path / "src/main/kotlin/com/acme/app/Calculator.kt",
        """
package com.acme.app

class Calculator {
    fun add(a: Int, b: Int): Int = a + b
}
""",
    )
    return tmp_path


def _error_handling_repo(tmp_path: Path) -> Path:
    """runCatching, a sealed error hierarchy, an empty catch, and a broad catch."""
    _write(
        tmp_path / "src/main/kotlin/com/acme/app/Errors.kt",
        """
package com.acme.app

sealed class UserError : Exception() {
    data class NotFound(val id: String) : UserError()
    object Invalid : UserError()
}

class Service {
    fun risky(): Result<String> {
        return runCatching {
            "ok"
        }
    }

    fun swallow() {
        try {
            doWork()
        } catch (e: Exception) {
        }
    }

    fun broad() {
        try {
            doWork()
        } catch (e: Exception) {
            log(e)
        }
    }

    private fun doWork(): String = "work"
    private fun log(e: Exception) {}
}
""",
    )
    return tmp_path


def _no_error_handling_repo(tmp_path: Path) -> Path:
    """No try/catch, runCatching, sealed errors, or preconditions."""
    _write(
        tmp_path / "src/main/kotlin/com/acme/app/Calculator.kt",
        """
package com.acme.app

class Calculator {
    fun add(a: Int, b: Int): Int = a + b
}
""",
    )
    return tmp_path


def _testing_repo(tmp_path: Path) -> Path:
    """Kotest StringSpec + MockK + JUnit5, with a backticked test name and runTest."""
    _write(
        tmp_path / "src/main/kotlin/com/acme/app/Service.kt",
        """
package com.acme.app

class Service {
    fun getValue(): String = "x"
    suspend fun getValueAsync(): String = "x"
}
""",
    )
    _write(
        tmp_path / "src/test/kotlin/com/acme/app/ServiceKotestTest.kt",
        """
package com.acme.app

import io.kotest.core.spec.style.StringSpec
import io.mockk.every
import io.mockk.mockk

class ServiceKotestTest : StringSpec({
    "should return value" {
        val service = mockk<Service>()
        every { service.getValue() } returns "x"
    }
})
""",
    )
    _write(
        tmp_path / "src/test/kotlin/com/acme/app/ServiceJUnitTest.kt",
        """
package com.acme.app

import kotlinx.coroutines.test.runTest
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

class ServiceJUnitTest {
    @Test
    fun `does the thing correctly`() {
        assertEquals(1, 1)
    }

    @Test
    fun coroutineTest() = runTest {
        Service().getValueAsync()
    }
}
""",
    )
    return tmp_path


def _no_tests_repo(tmp_path: Path) -> Path:
    """No test files and no test framework signal."""
    _write(
        tmp_path / "src/main/kotlin/com/acme/app/Calculator.kt",
        """
package com.acme.app

class Calculator {
    fun add(a: Int, b: Int): Int = a + b
}
""",
    )
    return tmp_path


def _server_side_kotlin_repo(tmp_path: Path) -> Path:
    """Spring Boot server-side Kotlin: no android/androidx imports, plugin, or manifest."""
    _write(
        tmp_path / "build.gradle.kts",
        """
plugins {
    kotlin("jvm") version "1.9.22"
    id("org.springframework.boot") version "3.2.0"
}
""",
    )
    _write(
        tmp_path / "src/main/kotlin/com/acme/app/UserController.kt",
        """
package com.acme.app

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController

@RestController
class UserController {
    @GetMapping("/users")
    fun getUsers(): List<String> {
        return listOf("alice", "bob")
    }
}
""",
    )
    return tmp_path


def _compose_android_repo(tmp_path: Path) -> Path:
    """A Compose Android app: android plugin + androidx.compose imports."""
    _write(
        tmp_path / "build.gradle.kts",
        """
plugins {
    id("com.android.application")
    kotlin("android") version "1.9.22"
}
""",
    )
    _write(
        tmp_path / "src/main/kotlin/com/acme/app/Greeting.kt",
        """
package com.acme.app

import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun Greeting(name: String) {
    Text(text = "Hello " + name)
}
""",
    )
    return tmp_path


def _android_synthetics_repo(tmp_path: Path) -> Path:
    """An Android project using the deprecated kotlinx.android.synthetic imports."""
    _write(
        tmp_path / "build.gradle.kts",
        """
plugins {
    id("com.android.application")
}
""",
    )
    _write(
        tmp_path / "src/main/kotlin/com/acme/app/MainActivity.kt",
        """
package com.acme.app

import kotlinx.android.synthetic.main.activity_main.textView

class MainActivity {
    fun bind() {
        textView.text = "hello"
    }
}
""",
    )
    return tmp_path


def _gradle_kotlin_dsl_repo(tmp_path: Path) -> Path:
    """A Gradle Kotlin DSL build with a Kotlin version and JVM toolchain."""
    _write(
        tmp_path / "build.gradle.kts",
        """
plugins {
    kotlin("jvm") version "1.9.22"
}

kotlin {
    jvmToolchain(17)
}

dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.0")
}
""",
    )
    _write(
        tmp_path / "src/main/kotlin/com/acme/app/Main.kt",
        """
package com.acme.app

fun main() {
    println("hello")
}
""",
    )
    return tmp_path


def _no_build_files_repo(tmp_path: Path) -> Path:
    """No Gradle/Maven build files at all."""
    _write(
        tmp_path / "src/main/kotlin/com/acme/app/Main.kt",
        """
package com.acme.app

fun main() {
    println("hello")
}
""",
    )
    return tmp_path


def _rich_repo(tmp_path: Path) -> Path:
    """A repo combining null-safety, coroutine, error-handling, testing,
    Gradle, and Compose Android signal so most detectors fire at once."""
    _write(
        tmp_path / "build.gradle.kts",
        """
plugins {
    kotlin("jvm") version "1.9.22"
    id("com.android.application")
}

kotlin {
    jvmToolchain(17)
}

dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
    implementation("io.insert-koin:koin-core:3.5.0")
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.0")
    testImplementation("io.mockk:mockk:1.13.8")
}
""",
    )
    _write(
        tmp_path / "src/main/kotlin/com/acme/app/UserService.kt",
        """
package com.acme.app

import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.flow.Flow

sealed class UserError : Exception() {
    data class NotFound(val id: String) : UserError()
}

class UserService(private val repository: UserRepository) {
    suspend fun fetch(id: String): String {
        val user = repository.find(id)!!
        return user
    }

    fun observe(): Flow<String> = TODO()

    fun risky(): Result<String> = runCatching { "ok" }

    fun swallow() {
        try {
            fetch("1")
        } catch (e: Exception) {
        }
    }

    fun leak() {
        GlobalScope.launch {
            fetch("1")
        }
    }
}

@Composable
fun Greeting(name: String) {
    Text(text = "Hello " + name)
}
""",
    )
    _write(
        tmp_path / "src/test/kotlin/com/acme/app/UserServiceTest.kt",
        """
package com.acme.app

import io.kotest.core.spec.style.StringSpec
import io.mockk.every
import io.mockk.mockk
import org.junit.jupiter.api.Test

class UserServiceKotestTest : StringSpec({
    "should fetch a user" {
        val service = mockk<UserService>()
        every { service.fetch("1") } returns "ok"
    }
})

class UserServiceJUnitTest {
    @Test
    fun `does the thing correctly`() {
        val id = "1"!!
        check(id == "1")
    }
}
""",
    )
    return tmp_path


# ---------------------------------------------------------------------------
# 1. KotlinNullSafetyDetector
# ---------------------------------------------------------------------------


class TestKotlinNullSafetyDetector:
    def test_production_not_null_assertion_fires_rule(self, tmp_path: Path):
        """A `!!` in production code reports not_null_assertions > 0 and fires."""
        repo = _null_safety_signal_repo(tmp_path)
        result = KotlinNullSafetyDetector().detect(_ctx(repo))

        rules = [r for r in result.rules if r.id == "kotlin.conventions.null_safety"]
        assert len(rules) == 1
        stats = rules[0].stats
        assert stats["not_null_assertions"] > 0

    def test_test_file_assertions_counted_separately(self, tmp_path: Path):
        """`!!` in a test file counts toward not_null_assertions_in_tests, not the
        production counter -- this separation is the whole point of the detector."""
        repo = _null_safety_signal_repo(tmp_path)
        result = KotlinNullSafetyDetector().detect(_ctx(repo))

        stats = result.rules[0].stats
        assert stats["not_null_assertions"] == 1
        assert stats["not_null_assertions_in_tests"] == 1

    def test_safe_handling_with_no_assertions_gives_full_safety_ratio(self, tmp_path: Path):
        """`?.`/`?:`/requireNotNull count as safe handling; safety_ratio is 1.0
        when there are no `!!` assertions at all."""
        repo = _null_safety_safe_only_repo(tmp_path)
        result = KotlinNullSafetyDetector().detect(_ctx(repo))

        rules = [r for r in result.rules if r.id == "kotlin.conventions.null_safety"]
        assert len(rules) == 1
        stats = rules[0].stats
        assert stats["not_null_assertions"] == 0
        assert stats["safety_ratio"] == 1.0
        assert stats["safe_calls"] > 0
        assert stats["elvis_operators"] > 0

    def test_no_nullable_signal_emits_no_rule(self, tmp_path: Path):
        """A repo with no nullable signal at all triggers the early return."""
        repo = _no_nullable_signal_repo(tmp_path)
        result = KotlinNullSafetyDetector().detect(_ctx(repo))
        assert result.rules == []


# ---------------------------------------------------------------------------
# 2. KotlinCoroutinesDetector
# ---------------------------------------------------------------------------


class TestKotlinCoroutinesDetector:
    def test_suspend_and_flow_detected(self, tmp_path: Path):
        """Suspend functions are counted and uses_flow is true when Flow/StateFlow
        is present."""
        repo = _coroutines_signal_repo(tmp_path)
        result = KotlinCoroutinesDetector().detect(_ctx(repo))

        rules = [r for r in result.rules if r.id == "kotlin.conventions.coroutines"]
        assert len(rules) == 1
        stats = rules[0].stats
        assert stats["suspend_function_count"] > 0
        assert stats["uses_flow"] is True

    def test_global_scope_surfaced_as_anti_pattern(self, tmp_path: Path):
        """GlobalScope usage is surfaced via global_scope_count > 0."""
        repo = _coroutines_signal_repo(tmp_path)
        result = KotlinCoroutinesDetector().detect(_ctx(repo))
        stats = result.rules[0].stats
        assert stats["global_scope_count"] > 0

    def test_runblocking_in_production_counted(self, tmp_path: Path):
        """runBlocking in production code increments runblocking_in_production."""
        repo = _coroutines_runblocking_production_repo(tmp_path)
        result = KotlinCoroutinesDetector().detect(_ctx(repo))

        rules = [r for r in result.rules if r.id == "kotlin.conventions.coroutines"]
        assert len(rules) == 1
        assert rules[0].stats["runblocking_in_production"] > 0

    def test_runblocking_in_test_file_not_counted_as_production(self, tmp_path: Path):
        """runBlocking used only inside a test file must NOT count toward
        runblocking_in_production."""
        repo = _coroutines_runblocking_test_only_repo(tmp_path)
        result = KotlinCoroutinesDetector().detect(_ctx(repo))

        rules = [r for r in result.rules if r.id == "kotlin.conventions.coroutines"]
        assert len(rules) == 1
        assert rules[0].stats["runblocking_in_production"] == 0

    def test_no_coroutines_emits_no_rule(self, tmp_path: Path):
        """A repo with no coroutine signal at all emits no rule."""
        repo = _no_coroutines_repo(tmp_path)
        result = KotlinCoroutinesDetector().detect(_ctx(repo))
        assert result.rules == []


# ---------------------------------------------------------------------------
# 3. KotlinErrorHandlingDetector
# ---------------------------------------------------------------------------


class TestKotlinErrorHandlingDetector:
    def test_runcatching_and_sealed_hierarchy_detected(self, tmp_path: Path):
        """runCatching is detected and the sealed error hierarchy is captured
        into sealed_error_types."""
        repo = _error_handling_repo(tmp_path)
        result = KotlinErrorHandlingDetector().detect(_ctx(repo))

        rules = [r for r in result.rules if r.id == "kotlin.conventions.error_handling"]
        assert len(rules) == 1
        stats = rules[0].stats
        assert stats["runcatching_count"] > 0
        assert "UserError" in stats["sealed_error_types"]

    def test_empty_and_broad_catch_blocks_flagged(self, tmp_path: Path):
        """An empty catch block and an overly-broad catch are both flagged."""
        repo = _error_handling_repo(tmp_path)
        result = KotlinErrorHandlingDetector().detect(_ctx(repo))

        stats = result.rules[0].stats
        assert stats["empty_catch_count"] > 0
        assert stats["broad_catch_count"] > 0

    def test_no_error_handling_emits_no_rule(self, tmp_path: Path):
        """A repo with no error-handling signal at all emits no rule."""
        repo = _no_error_handling_repo(tmp_path)
        result = KotlinErrorHandlingDetector().detect(_ctx(repo))
        assert result.rules == []


# ---------------------------------------------------------------------------
# 4. KotlinTestingDetector
# ---------------------------------------------------------------------------


class TestKotlinTestingDetector:
    def test_kotest_mockk_junit5_frameworks_detected(self, tmp_path: Path):
        """Kotest StringSpec + MockK + JUnit5 are all detected, with JUnit
        version 5 and MockK usage flagged."""
        repo = _testing_repo(tmp_path)
        result = KotlinTestingDetector().detect(_ctx(repo))

        rules = [r for r in result.rules if r.id == "kotlin.conventions.testing_framework"]
        assert len(rules) == 1
        stats = rules[0].stats
        assert "kotest" in stats["frameworks"]
        assert "mockk" in stats["frameworks"]
        assert "junit5" in stats["frameworks"]
        assert stats["junit_version"] == 5
        assert stats["uses_mockk"] is True

    def test_backtick_test_names_and_coroutine_test_detected(self, tmp_path: Path):
        """Backticked test names are counted, and runTest/coroutine-test support
        is flagged."""
        repo = _testing_repo(tmp_path)
        result = KotlinTestingDetector().detect(_ctx(repo))

        stats = result.rules[0].stats
        assert stats["backtick_test_names"] > 0
        assert stats["uses_coroutine_test"] is True

    def test_no_tests_emits_no_rule(self, tmp_path: Path):
        """A repo with no tests and no test-framework signal emits no rule."""
        repo = _no_tests_repo(tmp_path)
        result = KotlinTestingDetector().detect(_ctx(repo))
        assert result.rules == []


# ---------------------------------------------------------------------------
# 5. KotlinAndroidDetector
# ---------------------------------------------------------------------------


class TestKotlinAndroidDetector:
    def test_server_side_kotlin_emits_no_rule(self, tmp_path: Path):
        """The Android gate is the critical behavior: a server-side Spring Kotlin
        repo with no android/androidx imports, no android plugin, and no
        AndroidManifest.xml must emit NO rule at all."""
        repo = _server_side_kotlin_repo(tmp_path)
        result = KotlinAndroidDetector().detect(_ctx(repo))
        assert result.rules == []

    def test_compose_android_fires_with_compose_toolkit(self, tmp_path: Path):
        """A Compose Android fixture (android plugin + androidx.compose imports)
        fires, with ui_toolkit == compose and composable_count > 0."""
        repo = _compose_android_repo(tmp_path)
        result = KotlinAndroidDetector().detect(_ctx(repo))

        rules = [r for r in result.rules if r.id == "kotlin.conventions.android"]
        assert len(rules) == 1
        stats = rules[0].stats
        assert stats["ui_toolkit"] == "compose"
        assert stats["composable_count"] > 0

    def test_synthetics_import_detected(self, tmp_path: Path):
        """kotlinx.android.synthetic imports mark uses_synthetics True."""
        repo = _android_synthetics_repo(tmp_path)
        result = KotlinAndroidDetector().detect(_ctx(repo))

        rules = [r for r in result.rules if r.id == "kotlin.conventions.android"]
        assert len(rules) == 1
        assert rules[0].stats["uses_synthetics"] is True


# ---------------------------------------------------------------------------
# 6. KotlinGradleDetector
# ---------------------------------------------------------------------------


class TestKotlinGradleDetector:
    def test_gradle_kotlin_dsl_detected(self, tmp_path: Path):
        """A Gradle Kotlin DSL build reports build_system, kotlin_version, and
        jvm_target."""
        repo = _gradle_kotlin_dsl_repo(tmp_path)
        result = KotlinGradleDetector().detect(_ctx(repo))

        rules = [r for r in result.rules if r.id == "kotlin.conventions.build_tools"]
        assert len(rules) == 1
        stats = rules[0].stats
        assert stats["build_system"] == "gradle-kotlin-dsl"
        assert stats["kotlin_version"] == "1.9.22"
        assert stats["jvm_target"] == "17"

    def test_primary_tool_is_gradle(self, tmp_path: Path):
        """primary_tool == 'gradle' -- this is the key CLAUDE.md's tech-stack
        renderer reads."""
        repo = _gradle_kotlin_dsl_repo(tmp_path)
        result = KotlinGradleDetector().detect(_ctx(repo))
        assert result.rules[0].stats["primary_tool"] == "gradle"

    def test_no_build_files_emits_no_rule(self, tmp_path: Path):
        """A repo with no Gradle/Maven build files emits no rule."""
        repo = _no_build_files_repo(tmp_path)
        result = KotlinGradleDetector().detect(_ctx(repo))
        assert result.rules == []


# ---------------------------------------------------------------------------
# Cross-cutting requirements
# ---------------------------------------------------------------------------


class TestCrossCutting:
    def test_all_kotlin_detector_stats_are_json_serializable(self, tmp_path: Path):
        """Every emitted Kotlin rule's stats dict must be JSON-serializable --
        this catches sets/Paths/dataclasses leaking into stats."""
        repo = _rich_repo(tmp_path)
        ctx = _ctx(repo)

        emitted_rule_count = 0
        for detector_cls in ALL_KOTLIN_DETECTOR_CLASSES:
            result = detector_cls().detect(ctx)
            for rule in result.rules:
                emitted_rule_count += 1
                # Raises TypeError if anything non-JSON-serializable (a set,
                # Path, or dataclass instance) leaked into stats.
                json.dumps(rule.stats)

        # Sanity check: the rich fixture should have actually exercised
        # several detectors, not zero.
        assert emitted_rule_count >= 4

    def test_all_emitted_rule_ids_have_rating_rules_and_score(self, tmp_path: Path):
        """Every emitted Kotlin rule id has a RATING_RULES entry, and
        rate_convention() returns a score in 1..5 without raising."""
        repo = _rich_repo(tmp_path)
        ctx = _ctx(repo)

        checked = 0
        for detector_cls in ALL_KOTLIN_DETECTOR_CLASSES:
            result = detector_cls().detect(ctx)
            for rule in result.rules:
                assert rule.id in RATING_RULES, f"{rule.id} missing from RATING_RULES"
                score, reason, suggestion = rate_convention(rule)
                assert 1 <= score <= 5
                assert isinstance(reason, str) and reason
                checked += 1

        assert checked >= 4

    def test_all_kotlin_detectors_are_scoped_to_kotlin(self):
        """Every Kotlin detector declares languages == {'kotlin'}, so none of
        them ever run against a non-Kotlin repo."""
        for detector_cls in ALL_KOTLIN_DETECTOR_CLASSES:
            assert detector_cls.languages == {"kotlin"}, detector_cls.__name__


class TestGenericDslKeywordsAreNotFrameworkEvidence:
    """A framework's DSL only counts when that framework is actually present.

    Regressions found by scanning real repositories:
    - okhttp (zero Koin imports) was reported as using Koin, because Kotlin's
      stdlib `certificates.single()` matches Koin's `single {` definition DSL.
    - okhttp (zero Ktor imports) was reported as "Ktor with 2 REST routes",
      because it has its own `route(` calls and a `Provider.install()` call.
    """

    def test_stdlib_single_and_factory_do_not_imply_koin(self, tmp_path: Path):
        _write(tmp_path / "build.gradle.kts", 'plugins { kotlin("jvm") version "1.9.22" }\n')
        _write(
            tmp_path / "src/main/kotlin/com/acme/Certs.kt",
            """package com.acme

class Certs(private val certificates: List<String>) {
    fun only(): String = certificates.single()
    fun make(): String = Adapter.factory("x")
}
""",
        )
        rules = KotlinDIDetector().detect(_ctx(tmp_path)).rules
        for r in rules:
            assert "koin" not in r.stats["frameworks"], (
                "stdlib .single()/.factory() must not be read as Koin DSL"
            )

    def test_koin_dsl_counts_when_koin_is_imported(self, tmp_path: Path):
        _write(tmp_path / "build.gradle.kts", 'plugins { kotlin("jvm") version "1.9.22" }\n')
        _write(
            tmp_path / "src/main/kotlin/com/acme/Di.kt",
            """package com.acme

import org.koin.dsl.module

val appModule = module {
    single { UserRepository() }
    factory { UserService(get()) }
}
""",
        )
        rules = KotlinDIDetector().detect(_ctx(tmp_path)).rules
        assert rules, "a Koin repo must emit a DI rule"
        assert rules[0].stats["framework"] == "koin"

    def test_route_and_install_do_not_imply_ktor(self, tmp_path: Path):
        _write(tmp_path / "build.gradle.kts", 'plugins { kotlin("jvm") version "1.9.22" }\n')
        _write(
            tmp_path / "src/main/kotlin/com/acme/Net.kt",
            """package com.acme

class Net {
    fun connect() {
        val r = route(address)
        Provider.install()
    }
}
""",
        )
        rules = KotlinWebDetector().detect(_ctx(tmp_path)).rules
        for r in rules:
            assert "ktor" not in r.stats["frameworks"], (
                "a bare route(/install( must not be read as Ktor server routing"
            )

    def test_ktor_detected_when_actually_imported(self, tmp_path: Path):
        _write(tmp_path / "build.gradle.kts", 'plugins { kotlin("jvm") version "1.9.22" }\n')
        _write(
            tmp_path / "src/main/kotlin/com/acme/Server.kt",
            """package com.acme

import io.ktor.server.application.install
import io.ktor.server.routing.get
import io.ktor.server.routing.routing

fun Application.module() {
    routing {
        get("/users") { call.respond("ok") }
    }
}
""",
        )
        rules = KotlinWebDetector().detect(_ctx(tmp_path)).rules
        assert rules, "a Ktor repo must emit a web rule"
        assert rules[0].stats["framework"] == "ktor"

    def test_bare_hilt_import_is_not_hilt_adoption(self, tmp_path: Path):
        """Koin ships one `dagger.hilt.EntryPoints` import; that isn't a Hilt app."""
        _write(
            tmp_path / "build.gradle.kts",
            'plugins { id("com.android.application") }\n',
        )
        _write(
            tmp_path / "src/main/kotlin/com/acme/Interop.kt",
            """package com.acme

import android.util.Log
import dagger.hilt.EntryPoints

class Interop {
    fun go() = Log.d("t", "x")
}
""",
        )
        rules = KotlinAndroidDetector().detect(_ctx(tmp_path)).rules
        for r in rules:
            assert r.stats["uses_hilt"] is False


class TestAndroidTestIsNotMultiplatform:
    """`src/androidTest/` is standard Android, not Kotlin Multiplatform.

    Regression: nowinandroid (an Android-only app) was reported as
    "multiplatform" because androidTest was in MULTIPLATFORM_SOURCE_SETS.
    """

    def test_android_test_source_set_does_not_imply_multiplatform(self, tmp_path: Path):
        _write(tmp_path / "build.gradle.kts", 'plugins { id("com.android.application") }\n')
        for i in range(3):
            _write(
                tmp_path / f"app/src/main/kotlin/com/acme/F{i}.kt",
                f"package com.acme\n\nclass F{i}\n",
            )
        _write(
            tmp_path / "app/src/androidTest/kotlin/com/acme/FTest.kt",
            "package com.acme\n\nclass FTest\n",
        )
        rules = KotlinArchitectureDetector().detect(_ctx(tmp_path)).rules
        assert rules
        assert rules[0].stats["is_multiplatform"] is False
        assert rules[0].stats["structure"] != "multiplatform"

    def test_common_main_does_imply_multiplatform(self, tmp_path: Path):
        _write(tmp_path / "build.gradle.kts", 'plugins { kotlin("multiplatform") }\n')
        for i in range(3):
            _write(
                tmp_path / f"src/commonMain/kotlin/com/acme/F{i}.kt",
                f"package com.acme\n\nclass F{i}\n",
            )
        rules = KotlinArchitectureDetector().detect(_ctx(tmp_path)).rules
        assert rules
        assert rules[0].stats["is_multiplatform"] is True


class TestKotlinDominantPackageRoot:
    """Same dominant-prefix contract as Java: one outlier must not collapse the root."""

    def test_outlier_package_does_not_collapse_root(self, tmp_path: Path):
        _write(tmp_path / "build.gradle.kts", 'plugins { kotlin("jvm") version "1.9.22" }\n')
        for i in range(9):
            _write(
                tmp_path / f"src/main/kotlin/com/acme/app/T{i}.kt",
                f"package com.acme.app\n\nclass T{i}\n",
            )
        _write(
            tmp_path / "fixtures/src/main/kotlin/com/other/demo/Odd.kt",
            "package com.other.demo\n\nclass Odd\n",
        )
        rules = KotlinArchitectureDetector().detect(_ctx(tmp_path)).rules
        assert rules
        assert rules[0].stats["common_package_root"] == "com.acme.app"
