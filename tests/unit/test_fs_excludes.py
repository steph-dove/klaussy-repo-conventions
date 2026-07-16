"""Tests for filesystem exclude logic (should_exclude / walk_files)."""
from __future__ import annotations

from pathlib import Path

import pytest

from conventions.fs import (
    create_exclude_spec,
    load_gitignore,
    should_exclude,
    walk_files,
)


def touch(root: Path, rel: str) -> Path:
    """Create a real file (with parent dirs) under root and return its path."""
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("x")
    return p


def make_dir(root: Path, rel: str) -> Path:
    """Create a real directory under root and return its path."""
    p = root / rel
    p.mkdir(parents=True, exist_ok=True)
    return p


@pytest.fixture
def repo_root(tmp_path: Path) -> Path:
    """A resolved repo root, so comparisons don't trip on symlinked tmp dirs."""
    return tmp_path.resolve()


class TestShouldExcludeRegression:
    """The regressions that motivated splitting HARD_EXCLUDES into two sets."""

    def test_java_package_root_com_example_not_excluded(self, repo_root: Path):
        """com/example/... is the conventional Java/Kotlin package root."""
        path = touch(repo_root, "src/main/kotlin/com/example/api/App.kt")
        assert should_exclude(path, repo_root) is False

    def test_com_demo_package_not_excluded(self, repo_root: Path):
        path = touch(repo_root, "com/demo/Thing.kt")
        assert should_exclude(path, repo_root) is False

    def test_com_sample_package_not_excluded(self, repo_root: Path):
        path = touch(repo_root, "com/sample/X.kt")
        assert should_exclude(path, repo_root) is False

    def test_com_doc_package_not_excluded(self, repo_root: Path):
        path = touch(repo_root, "com/doc/Y.kt")
        assert should_exclude(path, repo_root) is False

    @pytest.mark.parametrize("parent_name", ["demo", "build", "examples"])
    def test_absolute_path_leak_parent_dir_name_ignored(
        self, tmp_path: Path, parent_name: str
    ):
        """A repo nested under a parent dir with an excluded-looking name must
        not have its entire scan discarded — only the path RELATIVE to
        repo_root is considered.
        """
        repo_root = (tmp_path / "xyz" / parent_name / "myrepo").resolve()
        path = touch(repo_root, "src/app.py")
        assert should_exclude(path, repo_root) is False


class TestShouldExcludeContentExcludes:
    """CONTENT_EXCLUDES apply only at the top level of the repo."""

    @pytest.mark.parametrize(
        "rel",
        [
            "docs/guide.py",
            "examples/demo.py",
            "samples/x.py",
            "tutorials/t.py",
        ],
    )
    def test_top_level_content_dir_file_excluded(self, repo_root: Path, rel: str):
        path = touch(repo_root, rel)
        assert should_exclude(path, repo_root) is True

    @pytest.mark.parametrize("dirname", ["docs", "examples"])
    def test_top_level_content_dir_itself_excluded(self, repo_root: Path, dirname: str):
        """walk_files prunes directories, so should_exclude must return True
        for the directory path itself, not just files inside it."""
        d = make_dir(repo_root, dirname)
        assert should_exclude(d, repo_root) is True

    def test_nested_examples_dir_not_excluded(self, repo_root: Path):
        """Deliberate trade-off: content excludes only match at the top level."""
        path = touch(repo_root, "packages/ui/examples/x.ts")
        assert should_exclude(path, repo_root) is False

    def test_nested_docs_dir_not_excluded(self, repo_root: Path):
        path = touch(repo_root, "src/docs/x.py")
        assert should_exclude(path, repo_root) is False


class TestShouldExcludeStructuralExcludes:
    """STRUCTURAL_EXCLUDES apply at any depth of the relative path."""

    @pytest.mark.parametrize(
        "rel",
        [
            "node_modules/pkg/i.js",
            "src/node_modules/pkg/i.js",
            "build/o.py",
            "src/build/o.py",
            ".git/config",
            "__pycache__/x.pyc",
            ".venv/lib/x.py",
            "site-packages/x.py",
        ],
    )
    def test_structural_exclude_any_depth(self, repo_root: Path, rel: str):
        path = touch(repo_root, rel)
        assert should_exclude(path, repo_root) is True

    @pytest.mark.parametrize(
        "rel",
        [
            "foo.egg-info/x.py",
            "src/foo.egg-info/x.py",
        ],
    )
    def test_egg_info_wildcard_any_depth(self, repo_root: Path, rel: str):
        """Exercises the `*.egg-info` wildcard branch of _matches_exclude."""
        path = touch(repo_root, rel)
        assert should_exclude(path, repo_root) is True


class TestShouldExcludeGitignoreAndCustom:
    def test_custom_exclude_spec_matches(self, repo_root: Path):
        spec = create_exclude_spec(["*.log", "secret_*"])
        matching = touch(repo_root, "app.log")
        nonmatching = touch(repo_root, "app.py")
        assert should_exclude(matching, repo_root, custom_excludes=spec) is True
        assert should_exclude(nonmatching, repo_root, custom_excludes=spec) is False

    def test_custom_exclude_spec_prefix_pattern(self, repo_root: Path):
        spec = create_exclude_spec(["secret_*"])
        matching = touch(repo_root, "secret_config.py")
        nonmatching = touch(repo_root, "normal.py")
        assert should_exclude(matching, repo_root, custom_excludes=spec) is True
        assert should_exclude(nonmatching, repo_root, custom_excludes=spec) is False

    def test_load_gitignore_matches(self, repo_root: Path):
        (repo_root / ".gitignore").write_text("*.secret\n")
        spec = load_gitignore(repo_root)
        assert spec is not None

        matching = touch(repo_root, "config.secret")
        nonmatching = touch(repo_root, "config.py")
        assert should_exclude(matching, repo_root, gitignore_spec=spec) is True
        assert should_exclude(nonmatching, repo_root, gitignore_spec=spec) is False

    def test_load_gitignore_returns_none_when_missing(self, repo_root: Path):
        assert load_gitignore(repo_root) is None


class TestShouldExcludeNormalSource:
    @pytest.mark.parametrize(
        "rel",
        [
            "src/conventions/foo.py",
            "app/main.kt",
            "README.md",
        ],
    )
    def test_normal_source_not_excluded(self, repo_root: Path, rel: str):
        path = touch(repo_root, rel)
        assert should_exclude(path, repo_root) is False


class TestWalkFiles:
    def test_extensions_filter_including_multipart(self, repo_root: Path):
        touch(repo_root, "app/build.gradle.kts")
        touch(repo_root, "app/other.txt")

        result = {p.name for p in walk_files(repo_root, {".gradle.kts"})}
        assert result == {"build.gradle.kts"}

    def test_top_level_examples_excluded_but_nested_com_example_included(
        self, repo_root: Path
    ):
        """End-to-end version of the headline fix."""
        touch(repo_root, "examples/foo.py")
        touch(repo_root, "src/main/kotlin/com/example/App.kt")

        result = {
            str(p.relative_to(repo_root)) for p in walk_files(repo_root, {".py", ".kt"})
        }
        assert "examples/foo.py" not in result
        assert "src/main/kotlin/com/example/App.kt" in result

    def test_node_modules_pruned_at_any_depth(self, repo_root: Path):
        touch(repo_root, "node_modules/pkg/index.js")
        touch(repo_root, "src/node_modules/pkg/index.js")
        touch(repo_root, "src/app.js")

        result = {str(p.relative_to(repo_root)) for p in walk_files(repo_root, {".js"})}
        assert result == {"src/app.js"}

    def test_max_files_caps_results(self, repo_root: Path):
        for i in range(5):
            touch(repo_root, f"file{i}.py")

        result = list(walk_files(repo_root, {".py"}, max_files=2))
        assert len(result) == 2

    def test_exclude_patterns_glob_honored(self, repo_root: Path):
        touch(repo_root, "secret_config.py")
        touch(repo_root, "normal.py")

        result = {
            p.name
            for p in walk_files(repo_root, {".py"}, exclude_patterns=["secret_*.py"])
        }
        assert "secret_config.py" not in result
        assert "normal.py" in result

    def test_respect_gitignore_false_ignores_gitignore(self, repo_root: Path):
        (repo_root / ".gitignore").write_text("ignored.py\n")
        touch(repo_root, "ignored.py")
        touch(repo_root, "normal.py")

        respected = {p.name for p in walk_files(repo_root, {".py"}, respect_gitignore=True)}
        assert "ignored.py" not in respected
        assert "normal.py" in respected

        ignored = {
            p.name for p in walk_files(repo_root, {".py"}, respect_gitignore=False)
        }
        assert "ignored.py" in ignored
        assert "normal.py" in ignored
