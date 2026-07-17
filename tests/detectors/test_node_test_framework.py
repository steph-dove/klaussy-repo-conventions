"""Tests for Node.js test-framework detection."""
from __future__ import annotations

from pathlib import Path

from conventions.detectors.base import DetectorContext
from conventions.detectors.node.index import NodeIndex


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _ctx(repo_root: Path) -> DetectorContext:
    return DetectorContext(repo_root=repo_root, selected_languages={"node"}, max_files=200)


class TestPackageImportsAreNotSubstrings:
    """Package detection must not match arbitrary substrings of a module path.

    Regression: test-framework detection used a substring test, so Mastodon's
    `mastodon/components/avatar` imports counted as the `ava` framework. The
    counts were also capped at 10, so phantom ava (10) outvoted real vitest (2)
    and every Rails app with an app/javascript frontend was told to run
    `npx ava`.
    """

    def _repo(self, tmp_path: Path) -> Path:
        _write(tmp_path / "package.json", '{"name": "app", "devDependencies": {"vitest": "^2.0.0"}}')
        # Many imports of an "avatar" component -- the trap.
        for i in range(12):
            _write(
                tmp_path / f"app/javascript/features/f{i}.jsx",
                "import { Avatar } from 'app/components/avatar';\n"
                "export const F = () => <Avatar />;\n",
            )
        _write(
            tmp_path / "app/javascript/features/f0.test.js",
            "import { describe, it } from 'vitest';\n\ndescribe('f', () => it('works', () => {}));\n",
        )
        return tmp_path

    def test_avatar_imports_are_not_the_ava_framework(self, tmp_path: Path):
        repo = self._repo(tmp_path)
        index = NodeIndex(repo, max_files=200)
        index.build()

        # The substring test is what created the phantom hits...
        assert index.find_imports_matching("ava"), "fixture should contain 'avatar' imports"
        # ...and package matching must reject every one of them.
        assert index.find_package_imports("ava") == []

    def test_package_import_matches_package_and_subpath(self, tmp_path: Path):
        _write(tmp_path / "package.json", '{"name": "app"}')
        _write(
            tmp_path / "src/a.js",
            "import test from 'ava';\nimport helper from 'ava/helpers';\n"
            "import { Avatar } from './components/avatar';\n",
        )
        index = NodeIndex(tmp_path, max_files=200)
        index.build()

        modules = {m for _, m, _ in index.find_package_imports("ava")}
        assert modules == {"ava", "ava/helpers"}

    def test_scoped_package_matches(self, tmp_path: Path):
        _write(tmp_path / "package.json", '{"name": "app"}')
        _write(tmp_path / "src/a.js", "import { jest } from '@jest/globals';\n")
        index = NodeIndex(tmp_path, max_files=200)
        index.build()

        modules = {m for _, m, _ in index.find_package_imports("@jest")}
        assert modules == {"@jest/globals"}

    def test_real_framework_wins_over_lookalike_imports(self, tmp_path: Path):
        """End-to-end: the repo uses vitest and has many `avatar` imports."""
        from conventions.detectors.node.conventions import NodeConventionsDetector

        repo = self._repo(tmp_path)
        rules = NodeConventionsDetector().detect(_ctx(repo)).rules
        testing = [r for r in rules if r.id.endswith("testing_framework")]
        for rule in testing:
            assert rule.stats["primary_library"] == "vitest"
            assert "ava" not in rule.stats["test_library_counts"]
