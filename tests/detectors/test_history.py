"""Tests for generic history detector."""
from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from conventions.detectors.base import DetectorContext
from conventions.detectors.generic.history import HistoryDetector


@pytest.fixture
def mock_repo_with_history(tmp_path: Path) -> Path:
    """Create a temporary repository with workflows and changelog."""
    # Write a changelog
    changelog = """# Changelog

## 1.2.0
- feat: add new feature
- breaking change: migrated database schema to postgresql v16
- deprecated: old endpoint /v1/users is deprecated

## 1.1.0
- fix: resolved issue with authentication flakiness
- fix flaky test by adding retry logic
"""
    (tmp_path / "CHANGELOG.md").write_text(changelog)

    # Write a GitHub workflow with flakiness gotchas
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    ci_workflow = """name: CI
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Run Tests
        run: pytest
        continue-on-error: true
      - name: Deploy
        run: retry deploy.sh
"""
    (workflows / "ci.yml").write_text(ci_workflow)
    return tmp_path


def test_history_detector(mock_repo_with_history: Path):
    """Test HistoryDetector correctly parses changelogs, git history, and CI workflows."""
    ctx = DetectorContext(
        repo_root=mock_repo_with_history,
        selected_languages=set(),
    )

    # Mock subprocess.run to return sample commit logs
    mock_run_result = MagicMock()
    mock_run_result.returncode = 0
    mock_run_result.stdout = """feat!: migrate to new configuration structure
fix ci builds: retry linting step
chore: refactor auth logic
"""

    with patch("subprocess.run", return_value=mock_run_result) as mock_run:
        result = HistoryDetector().detect(ctx)

        # Assert git log was called with right arguments
        mock_run.assert_called_once_with(
            ["git", "log", "-100", "--format=%s"],
            cwd=mock_repo_with_history,
            capture_output=True,
            text=True,
            timeout=5,
        )

        assert len(result.rules) == 1
        rule = result.rules[0]
        assert rule.id == "generic.conventions.history"

        # Assert decisions were parsed
        decisions = rule.stats["detected_decisions"]
        assert "Migration/refactor commit: feat!: migrate to new configuration structure" in decisions
        assert "Changelog breaking change: breaking change: migrated database schema to postgresql v16" in decisions
        assert "Changelog breaking change: deprecated: old endpoint /v1/users is deprecated" in decisions

        # Assert pitfalls were parsed
        pitfalls = rule.stats["detected_pitfalls"]
        assert "CI/test flakiness fix or workaround: fix ci builds: retry linting step" in pitfalls
        assert "Changelog noted issue: fix flaky test by adding retry logic" in pitfalls
        assert "CI workflow `ci.yml` contains steps allowed to fail (`continue-on-error: true`)." in pitfalls
        assert "CI workflow `ci.yml` uses retry logic for flaky execution steps." in pitfalls
