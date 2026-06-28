"""Tests for orchestrator utilities and language detection."""
from __future__ import annotations

from pathlib import Path

from conventions.detectors.orchestrator import detect_languages


class TestLanguageDetection:
    """Tests for auto-detecting languages in a repository."""

    def test_detect_languages_ignores_tests_and_fixtures(self, tmp_repo: Path):
        """Test that language detection ignores files inside test and fixture directories."""
        # 1. Create a Python file in production source folder
        (tmp_repo / "src" / "main.py").write_text("print('hello')\n")

        # 2. Create mock files in test/fixture directories that should be ignored
        (tmp_repo / "tests").mkdir(parents=True, exist_ok=True)
        (tmp_repo / "tests" / "mock.go").write_text("package main\n")

        (tmp_repo / "tests" / "fixtures").mkdir(parents=True, exist_ok=True)
        (tmp_repo / "tests" / "fixtures" / "client.ts").write_text("console.log('hi');\n")

        (tmp_repo / "src" / "fixtures").mkdir(parents=True, exist_ok=True)
        (tmp_repo / "src" / "fixtures" / "api_mock.js").write_text("const express = require('express');\n")

        # Detect languages
        languages = detect_languages(tmp_repo)

        # Python should be detected, but go and node should be ignored
        assert "python" in languages
        assert "go" not in languages
        assert "node" not in languages

    def test_detect_languages_includes_production_files(self, tmp_repo: Path):
        """Test that languages are detected when files reside in non-test directories."""
        # Create a Python file and a Go file in non-test directories
        (tmp_repo / "src" / "main.py").write_text("print('hello')\n")
        (tmp_repo / "src" / "service.go").write_text("package main\n")

        # Detect languages
        languages = detect_languages(tmp_repo)

        # Both python and go should be detected
        assert "python" in languages
        assert "go" in languages
        assert "node" not in languages
