"""Tests for generic history detector."""
from __future__ import annotations

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

        # Assert decisions were parsed, with version context from the headings.
        decisions = rule.stats["detected_decisions"]
        assert "Migration/refactor commit: feat!: migrate to new configuration structure" in decisions
        assert "v1.2.0: breaking change: migrated database schema to postgresql v16" in decisions
        assert "v1.2.0: deprecated: old endpoint /v1/users is deprecated" in decisions

        # Assert pitfalls were parsed
        pitfalls = rule.stats["detected_pitfalls"]
        assert "CI/test flakiness fix or workaround: fix ci builds: retry linting step" in pitfalls
        assert "v1.1.0: fix flaky test by adding retry logic" in pitfalls
        assert "CI workflow `ci.yml` contains steps allowed to fail (`continue-on-error: true`)." in pitfalls
        assert "CI workflow `ci.yml` uses retry logic for flaky execution steps." in pitfalls


def test_changelog_decision_fidelity(tmp_path: Path):
    """Truncated, link-laden changelog prose becomes a clean, versioned entry."""
    changelog = """# Changelog

## 0.27.0 (21st February, 2024)

- The deprecated `verify=<ssl_context>` string cases have been removed and require migration...*
- The deprecated `proxies` argument has now been removed. See PR [#3005](https://github.com/encode/httpx/pull/3005) for details.
"""
    (tmp_path / "CHANGELOG.md").write_text(changelog)

    ctx = DetectorContext(repo_root=tmp_path, selected_languages=set())
    mock_run_result = MagicMock(returncode=0, stdout="")
    with patch("subprocess.run", return_value=mock_run_result):
        rule = HistoryDetector().detect(ctx).rules[0]

    decisions = rule.stats["detected_decisions"]

    # Every entry carries version (and date) context.
    assert all(d.startswith("v0.27.0 (21st February, 2024): ") for d in decisions)
    # No truncated mid-sentence markdown artifacts survive.
    assert not any(d.rstrip().endswith(("...", "*", "…")) for d in decisions)
    # Markdown links are reduced to their visible text (no raw URLs).
    assert not any("http" in d or "](" in d for d in decisions)
    # The first complete sentence is kept, not a fragment.
    assert "v0.27.0 (21st February, 2024): The deprecated proxies argument has now been removed." in decisions
