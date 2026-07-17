"""Integration tests for C++ convention detectors."""

from __future__ import annotations

from pathlib import Path

from conventions.detectors.base import DetectorContext
from conventions.detectors.cpp import (
    CPPArchitectureDetector,
    CPPIndex,
    CPPTestingDetector,
)
from conventions.ratings import rate_convention


def _write(path: Path, content: str) -> None:
    """Write `content` to `path`, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _ctx(repo_root: Path) -> DetectorContext:
    return DetectorContext(
        repo_root=repo_root,
        selected_languages={"cpp"},
        max_files=200,
    )


# ---------------------------------------------------------------------------
# Test Indexer
# ---------------------------------------------------------------------------

def test_cpp_indexer(tmp_path: Path):
    _write(
        tmp_path / "CMakeLists.txt",
        """
        cmake_minimum_required(VERSION 3.15)
        project(MyProject)
        add_executable(my_app main.cpp)
        add_library(my_lib lib.cpp)
        """,
    )
    _write(
        tmp_path / "src/UserService.cpp",
        """
        #include "UserService.h"
        #include <vector>
        #include <string>

        namespace Acme::App {
            class UserService {
                // TODO: load config
                void fetch() {}
            };
        }
        """,
    )

    index = CPPIndex(tmp_path)
    index.build()

    assert "my_app" in index.cmake_targets
    assert "my_lib" in index.cmake_targets

    assert len(index.files) == 1
    file_idx = index.files["src/UserService.cpp"]
    assert file_idx.includes[0][0] == '"UserService.h"'
    assert file_idx.includes[1][0] == "<vector>"
    assert file_idx.types == [("class", "UserService", 7)]
    assert file_idx.namespaces == ["Acme::App"]
    assert file_idx.todo_count == 1


# ---------------------------------------------------------------------------
# Test Architecture Detector
# ---------------------------------------------------------------------------

def test_cpp_architecture_detector(tmp_path: Path):
    _write(
        tmp_path / "CMakeLists.txt",
        "add_executable(app main.cpp)",
    )
    _write(
        tmp_path / "include/app.h",
        "class App {};",
    )
    _write(
        tmp_path / "src/app.cpp",
        '#include "app.h"',
    )
    _write(
        tmp_path / ".clang-format",
        "BasedOnStyle: LLVM",
    )

    ctx = _ctx(tmp_path)
    detector = CPPArchitectureDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.id == "cpp.conventions.architecture"
    assert rule.stats["build_system"] == "CMake"
    assert rule.stats["layout"] == "separated (src/include)"
    assert rule.stats["has_clang_format"] is True

    score, _, _ = rate_convention(rule)
    assert score == 5


# ---------------------------------------------------------------------------
# Test Testing Detector
# ---------------------------------------------------------------------------

def test_cpp_testing_detector(tmp_path: Path):
    _write(
        tmp_path / "tests/app_test.cpp",
        """
        #include <gtest/gtest.h>
        TEST(AppTest, Simple) {
            EXPECT_TRUE(true);
        }
        """,
    )

    ctx = _ctx(tmp_path)
    detector = CPPTestingDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.stats["test_file_count"] == 1
    assert rule.stats["primary_framework"] == "Google Test"

    score, _, _ = rate_convention(rule)
    assert score == 3


class TestHeaderExtensionDoesNotEstablishCpp:
    """`.h` is equally a C, C++ and Objective-C header, so it cannot claim C++.

    Regression: including .h in language detection reported every pure C project
    as C++. redis -- whose only C++ files are vendored under deps/ -- was read as
    a 319-file "C++ codebase" of 312 headers and 7 sources.
    """

    def _repo(self, tmp_path: Path, files: dict[str, str]) -> Path:
        for rel, body in files.items():
            _write(tmp_path / rel, body)
        return tmp_path

    def test_pure_c_project_is_not_cpp(self, tmp_path: Path):
        from conventions.detectors.orchestrator import detect_languages

        repo = self._repo(tmp_path, {
            "src/server.c": "#include <stdio.h>\nint main(){return 0;}\n",
            "src/server.h": "#ifndef SERVER_H\n#define SERVER_H\n#endif\n",
            "Makefile": "all:\n\tcc src/server.c\n",
        })
        assert "cpp" not in detect_languages(repo)

    def test_objective_c_project_is_not_cpp(self, tmp_path: Path):
        from conventions.detectors.orchestrator import detect_languages

        repo = self._repo(tmp_path, {
            "App/main.m": "int main(){return 0;}\n",
            "App/App.h": "#import <Foundation/Foundation.h>\n",
        })
        assert "cpp" not in detect_languages(repo)

    def test_unambiguous_extensions_still_detect_cpp(self, tmp_path: Path):
        from conventions.detectors.orchestrator import detect_languages

        for rel, body in (
            ("src/a.cpp", "int main(){return 0;}\n"),
            ("src/b.cc", "int f(){return 1;}\n"),
            ("include/lib.hpp", "#pragma once\ntemplate<class T> struct S {};\n"),
        ):
            repo = self._repo(Path(str(tmp_path / rel.replace('/', '_'))), {rel: body})
            assert "cpp" in detect_languages(repo), rel

    def test_headers_are_still_indexed_once_cpp_is_established(self, tmp_path: Path):
        """.h must not *claim* C++, but a C++ project's .h headers still count."""
        repo = self._repo(tmp_path, {
            "src/app.cpp": '#include "app.h"\nint main(){return 0;}\n',
            "src/app.h": "#pragma once\nclass App {};\n",
        })
        index = CPPIndex(repo, max_files=100)
        index.build()
        assert "src/app.h" in index.files
        assert "src/app.cpp" in index.files


class TestPrimaryTestFrameworkFollowsUsage:
    """The primary framework is the one used most, and is never invented.

    Regressions: the list was built Google-Test-first and the primary taken as
    frameworks[0], so nlohmann/json -- 158 Catch2 hits against a single gtest
    one -- was reported as a Google Test project. And the fallback claimed
    "Google Test" when no framework was found at all: redis reported it with all
    three counts at zero.
    """

    def _tests(self, tmp_path: Path, gtest: int, catch: int) -> Path:
        _write(tmp_path / "CMakeLists.txt", "project(app)\n")
        _write(tmp_path / "src/app.cpp", "int main(){return 0;}\n")
        for i in range(gtest):
            _write(
                tmp_path / f"test/g{i}_test.cpp",
                f'#include <gtest/gtest.h>\n\nTEST(S, c{i}) {{}}\n',
            )
        for i in range(catch):
            _write(
                tmp_path / f"test/c{i}_test.cpp",
                f'#include <catch2/catch.hpp>\n\nTEST_CASE("c{i}") {{}}\n',
            )
        return tmp_path

    def test_catch2_majority_wins_over_a_single_gtest_hit(self, tmp_path: Path):
        repo = self._tests(tmp_path, gtest=1, catch=20)
        rules = CPPTestingDetector().detect(_ctx(repo)).rules
        assert rules
        assert rules[0].stats["primary_framework"] == "Catch2"

    def test_gtest_majority_wins(self, tmp_path: Path):
        repo = self._tests(tmp_path, gtest=12, catch=0)
        rules = CPPTestingDetector().detect(_ctx(repo)).rules
        assert rules
        assert rules[0].stats["primary_framework"] == "Google Test"

    def test_no_framework_is_not_invented(self, tmp_path: Path):
        """Test files with no recognizable framework must not claim one."""
        _write(tmp_path / "src/app.cpp", "int main(){return 0;}\n")
        _write(tmp_path / "test/basic_test.cpp", "int check(){return 1;}\n")
        rules = CPPTestingDetector().detect(_ctx(tmp_path)).rules
        for r in rules:
            assert r.stats["primary_framework"] is None
            assert "Google Test" not in r.title
