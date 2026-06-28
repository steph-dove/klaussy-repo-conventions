"""Project history detector for decision log and known pitfalls."""

from __future__ import annotations

import subprocess
from pathlib import Path

from ...fs import read_file_safe
from ..base import BaseDetector, DetectorContext, DetectorResult
from ..registry import DetectorRegistry


@DetectorRegistry.register
class HistoryDetector(BaseDetector):
    """Detects decision log items and known pitfalls from changelogs, git history, and CI files."""

    name = "generic_history"
    description = "Detects decision log items and known pitfalls from changelogs, git history, and CI files"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect history, decisions, and pitfalls."""
        result = DetectorResult()
        decisions: list[str] = []
        pitfalls: list[str] = []

        # 1. Scan Git commit logs
        self._scan_git_history(ctx, decisions, pitfalls)

        # 2. Scan Changelog/Release notes files
        self._scan_changelog_files(ctx, decisions, pitfalls)

        # 3. Scan CI configurations
        self._scan_ci_configs(ctx, pitfalls)

        # De-duplicate lists while preserving order
        unique_decisions = list(dict.fromkeys(decisions))
        unique_pitfalls = list(dict.fromkeys(pitfalls))

        # We only output the rule if we actually found something
        if unique_decisions or unique_pitfalls:
            result.rules.append(self.make_rule(
                rule_id="generic.conventions.history",
                category="documentation",
                title="Project history",
                description=f"Detected {len(unique_decisions)} decision log items and {len(unique_pitfalls)} pitfalls.",
                confidence=0.8,
                language="generic",
                evidence=[],
                stats={
                    "detected_decisions": unique_decisions,
                    "detected_pitfalls": unique_pitfalls,
                },
            ))

        return result

    def _scan_git_history(
        self,
        ctx: DetectorContext,
        decisions: list[str],
        pitfalls: list[str],
    ) -> None:
        """Scan git commit history for decisions and pitfalls."""
        try:
            git_result = subprocess.run(
                ["git", "log", "-100", "--format=%s"],
                cwd=ctx.repo_root,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if git_result.returncode != 0:
                return
            commits = git_result.stdout.strip().split("\n")
        except Exception:
            return

        for commit in commits:
            commit_clean = commit.strip()
            if not commit_clean:
                continue

            # Look for breaking changes/decisions
            if "!" in commit_clean.split(":")[0] or any(kw in commit_clean.lower() for kw in ["breaking change", "migration", "migrate to", "deprecated", "removed"]):
                decisions.append(f"Migration/refactor commit: {commit_clean}")

            # Look for pitfalls (CI failure fixes, workarounds, test flakiness, hacks)
            if any(kw in commit_clean.lower() for kw in ["fix ci", "flaky", "flakiness", "timeout", "retry", "workaround", "hack", "bypass"]):
                msg = commit_clean
                for prefix in ["fix:", "chore:", "feat:", "refactor:"]:
                    if msg.lower().startswith(prefix):
                        msg = msg[len(prefix):].strip()
                pitfalls.append(f"CI/test flakiness fix or workaround: {msg}")

    def _scan_changelog_files(
        self,
        ctx: DetectorContext,
        decisions: list[str],
        pitfalls: list[str],
    ) -> None:
        """Scan changelog and history files for decisions and pitfalls."""
        changelog_patterns = ["*changelog*", "*history*", "*releases*", "*release-notes*"]
        found_files: list[Path] = []
        for pattern in changelog_patterns:
            found_files.extend(ctx.repo_root.glob(pattern))
            found_files.extend(ctx.repo_root.glob(pattern.upper()))
            docs_dir = ctx.repo_root / "docs"
            if docs_dir.is_dir():
                found_files.extend(docs_dir.rglob(pattern))
                found_files.extend(docs_dir.rglob(pattern.upper()))

        # De-duplicate files
        found_files = list(set(found_files))

        for file_path in found_files:
            if not file_path.is_file():
                continue
            content = read_file_safe(file_path)
            if not content:
                continue

            lines = content.splitlines()
            for line in lines[:300]:  # Limit scan to first 300 lines (recent releases)
                line_strip = line.strip()
                if not line_strip:
                    continue
                # Look for bullet points with breaking changes / migrations / deprecations
                if line_strip.startswith(("-", "*", "1.")):
                    lower_line = line_strip.lower()
                    if any(kw in lower_line for kw in ["breaking change", "migration", "migrate", "deprecated", "removed"]):
                        cleaned = line_strip.lstrip("-*1. ").strip()
                        decisions.append(f"Changelog breaking change: {cleaned}")
                    if any(kw in lower_line for kw in ["fix flaky", "workaround", "pitfall", "gotcha", "known issue"]):
                        cleaned = line_strip.lstrip("-*1. ").strip()
                        pitfalls.append(f"Changelog noted issue: {cleaned}")

    def _scan_ci_configs(
        self,
        ctx: DetectorContext,
        pitfalls: list[str],
    ) -> None:
        """Scan CI configurations for potential pitfalls."""
        ci_dir = ctx.repo_root / ".github" / "workflows"
        if not ci_dir.is_dir():
            return

        for file_path in ci_dir.glob("*.y*ml"):
            if not file_path.is_file():
                continue
            content = read_file_safe(file_path)
            if not content:
                continue

            if "continue-on-error: true" in content:
                pitfalls.append(f"CI workflow `{file_path.name}` contains steps allowed to fail (`continue-on-error: true`).")
            if "retry" in content.lower():
                pitfalls.append(f"CI workflow `{file_path.name}` uses retry logic for flaky execution steps.")
