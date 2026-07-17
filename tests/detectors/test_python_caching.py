"""Tests for the Python caching detector."""
from __future__ import annotations

from pathlib import Path

from conventions.detectors.base import DetectorContext
from conventions.detectors.python.caching import PythonCachingDetector


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _ctx(repo_root: Path) -> DetectorContext:
    return DetectorContext(repo_root=repo_root, selected_languages={"python"}, max_files=200)


class TestCacheLibraryImportsAreUnpackedCorrectly:
    """Regression: the detector crashed on any project importing a cache library.

    `PythonIndex.find_imports_matching` returns (rel_path, ImportInfo) tuples,
    but the detector read them as objects (`f.file_path`), raising
    AttributeError: 'tuple' object has no attribute 'file_path'. The
    orchestrator swallowed it into a warning, so the caching rule silently
    vanished for every project using redis, cachetools, aiocache or diskcache.
    """

    def _repo(self, tmp_path: Path, module: str) -> Path:
        _write(
            tmp_path / "app/cache.py",
            f"import {module}\n\n\ndef get_client():\n    return {module}\n",
        )
        return tmp_path

    def test_redis_import_does_not_raise(self, tmp_path: Path):
        result = PythonCachingDetector().detect(_ctx(self._repo(tmp_path, "redis")))
        assert result.rules
        assert "redis" in result.rules[0].stats["caching_methods"]
        assert result.rules[0].stats["primary_method"] == "redis"

    def test_cachetools_import_does_not_raise(self, tmp_path: Path):
        result = PythonCachingDetector().detect(_ctx(self._repo(tmp_path, "cachetools")))
        assert result.rules
        assert "cachetools" in result.rules[0].stats["caching_methods"]

    def test_diskcache_import_does_not_raise(self, tmp_path: Path):
        result = PythonCachingDetector().detect(_ctx(self._repo(tmp_path, "diskcache")))
        assert result.rules

    def test_aiocache_import_does_not_raise(self, tmp_path: Path):
        result = PythonCachingDetector().detect(_ctx(self._repo(tmp_path, "aiocache")))
        assert result.rules
