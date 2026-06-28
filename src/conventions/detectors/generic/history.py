"""Project history detector for decision log and known pitfalls."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from ...fs import read_file_safe
from ..base import BaseDetector, DetectorContext, DetectorResult
from ..registry import DetectorRegistry

# A changelog/release-notes heading that names a version, e.g.
# "## 0.27.0 (21st February, 2024)" or "### v1.2.0".
_VERSION_HEADER_RE = re.compile(r"^#{1,6}\s+v?(\d+\.\d+(?:\.\d+)?(?:[.\-][a-z0-9]+)?)\b")
# A date in parentheses on the same heading line, e.g. "(21st February, 2024)".
_DATE_IN_PARENS_RE = re.compile(r"\(([^)]*\b\d{4}\b[^)]*)\)")
# A markdown link: capture the visible text, drop the URL.
_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
# Minimum length (chars) for a cleaned decision/pitfall to be worth recording.
_MIN_ENTRY_LEN = 15
# Cap a single entry so a long paragraph does not bloat the decision log.
_MAX_ENTRY_LEN = 200


def _clean_changelog_text(text: str) -> str:
    """Normalize a changelog bullet into clean prose.

    Converts markdown links to their text, strips emphasis/code markers and
    trailing ellipsis artifacts (the source of mid-sentence ``...*`` fragments).
    """
    text = _MD_LINK_RE.sub(r"\1", text)
    text = text.replace("`", "").replace("**", "").replace("__", "")
    text = text.strip().strip("*").strip()
    # Drop trailing ellipsis ("...", "…") left by truncated changelog prose.
    text = re.sub(r"(?:\.\.\.|…)\s*$", "", text).strip()
    return text


def _first_complete_sentence(text: str) -> str:
    """Return the first complete sentence, length-capped at a word boundary.

    Avoids emitting mid-word fragments: an over-long sentence is cut at the last
    whole word within the cap and terminated with a period.
    """
    match = re.search(r"(.+?[.!?])(?:\s|$)", text)
    sentence = (match.group(1) if match else text).strip()
    if len(sentence) > _MAX_ENTRY_LEN:
        sentence = sentence[:_MAX_ENTRY_LEN].rsplit(" ", 1)[0].rstrip(",;:") + "."
    return sentence


def _format_decision(version: str | None, text: str) -> str:
    """Format a decision-log entry, prefixing the version/date context if known."""
    return f"v{version}: {text}" if version else text


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
            current_version: str | None = None
            for line in lines[:400]:  # Limit scan to recent releases
                line_strip = line.strip()
                if not line_strip:
                    continue

                # Track the version/date heading so entries carry "as of" context.
                if line_strip.startswith("#"):
                    version = self._parse_version_header(line_strip)
                    if version:
                        current_version = version
                    continue

                # Look for bullet points with breaking changes / migrations / deprecations
                if line_strip.startswith(("-", "*", "1.")):
                    lower_line = line_strip.lower()
                    cleaned = _clean_changelog_text(line_strip.lstrip("-*1. ").strip())

                    if any(kw in lower_line for kw in ["breaking change", "migration", "migrate", "deprecated", "removed"]):
                        entry = _first_complete_sentence(cleaned)
                        if len(entry) >= _MIN_ENTRY_LEN:
                            decisions.append(_format_decision(current_version, entry))
                    if any(kw in lower_line for kw in ["fix flaky", "workaround", "pitfall", "gotcha", "known issue"]):
                        entry = _first_complete_sentence(cleaned)
                        if len(entry) >= _MIN_ENTRY_LEN:
                            pitfalls.append(_format_decision(current_version, entry))

    @staticmethod
    def _parse_version_header(line: str) -> str | None:
        """Extract a version (with date, if present) from a changelog heading."""
        match = _VERSION_HEADER_RE.match(line)
        if not match:
            return None
        version = match.group(1)
        date_match = _DATE_IN_PARENS_RE.search(line)
        if date_match:
            return f"{version} ({date_match.group(1).strip()})"
        return version

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
