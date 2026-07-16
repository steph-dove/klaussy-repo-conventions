"""Kotlin documentation conventions detector."""

from __future__ import annotations

import re

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import KotlinDetector
from .index import make_evidence

# KDoc tags worth surfacing, in the order we report them.
KDOC_TAGS = (
    "@param",
    "@return",
    "@throws",
    "@sample",
    "@see",
    "@property",
    "@constructor",
    "@since",
    "@suppress",
)

MODULE_DOC_FILENAMES = ("README.md", "Module.md", "packages.md")


def _has_kdoc(lines: list[str], line: int) -> bool:
    """Check whether the declaration at 1-indexed `line` is preceded by a KDoc block.

    Walks backward from `line - 1`, skipping blank lines and annotation lines,
    then checks whether the line landed on ends a `/** ... */` block comment.
    """
    idx = line - 2  # 0-indexed line immediately above the declaration
    while idx >= 0:
        stripped = lines[idx].strip()
        if not stripped or stripped.startswith("@"):
            idx -= 1
            continue
        break

    if idx < 0:
        return False
    if not lines[idx].rstrip().endswith("*/"):
        return False

    # Walk further back to confirm the block opened with `/**`, not a plain `/*`.
    while idx >= 0:
        stripped = lines[idx].strip()
        if stripped.startswith("/**"):
            return True
        if stripped.startswith("/*"):
            return False
        idx -= 1

    return False


@DetectorRegistry.register
class KotlinDocumentationDetector(KotlinDetector):
    """Detect KDoc coverage and documentation conventions."""

    name = "kotlin_documentation"
    description = "Detects KDoc coverage and documentation conventions"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect documentation conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        public_function_count = 0
        documented_function_count = 0
        public_class_count = 0
        documented_class_count = 0

        documented_examples: list[tuple[str, int]] = []

        for file_idx in index.get_non_test_files():
            lines = file_idx.lines
            for fn in file_idx.functions:
                if not fn.is_public:
                    continue
                public_function_count += 1
                if _has_kdoc(lines, fn.line):
                    documented_function_count += 1
                    documented_examples.append((file_idx.relative_path, fn.line))

            for cls in file_idx.classes:
                if cls.visibility != "public":
                    continue
                public_class_count += 1
                if _has_kdoc(lines, cls.line):
                    documented_class_count += 1
                    documented_examples.append((file_idx.relative_path, cls.line))

        total_public = public_function_count + public_class_count
        if total_public == 0:
            return result

        total_documented = documented_function_count + documented_class_count
        coverage = total_documented / total_public

        build_info = self.get_build_info(ctx)
        uses_dokka = build_info.has_plugin("dokka")

        kdoc_tags: list[str] = []
        for tag in KDOC_TAGS:
            if index.count_pattern(re.escape(tag) + r"\b", exclude_tests=True) > 0:
                kdoc_tags.append(tag)

        todo_count = index.count_pattern(r"//\s*(?:TODO|FIXME)\b", exclude_tests=False)

        has_readme = any(
            (ctx.repo_root / filename).is_file() for filename in MODULE_DOC_FILENAMES
        )

        patterns: list[str] = []
        if kdoc_tags:
            patterns.append("KDoc tags: " + ", ".join(kdoc_tags))
        if uses_dokka:
            patterns.append("Dokka configured")
        if has_readme:
            patterns.append("module-level docs present")
        if todo_count:
            patterns.append(f"{todo_count} TODO/FIXME comment(s)")

        title = f"Documentation: {round(coverage * 100)}% KDoc coverage on public API"
        if uses_dokka:
            title += ", Dokka configured"

        description = (
            f"{total_documented}/{total_public} public declaration(s) have KDoc "
            f"({documented_function_count}/{public_function_count} functions, "
            f"{documented_class_count}/{public_class_count} classes)."
        )
        if uses_dokka:
            description += " Dokka is configured for HTML documentation generation."
        if kdoc_tags:
            description += f" Uses KDoc tags: {', '.join(kdoc_tags)}."
        if has_readme:
            description += " Module-level documentation file present."
        if todo_count:
            description += f" {todo_count} TODO/FIXME comment(s) found in source."

        # Confidence scales with sample size; documentation coverage is directly
        # measured, so a decent sample warrants a high confidence score.
        confidence = 0.9 if total_public >= 10 else 0.5 + 0.04 * total_public

        evidence = []
        for rel_path, line in documented_examples[: ctx.max_evidence_snippets]:
            ev = make_evidence(index, rel_path, line, radius=3)
            if ev:
                evidence.append(ev)

        result.rules.append(self.make_rule(
            rule_id="kotlin.conventions.documentation",
            category="documentation",
            title=title,
            description=description,
            confidence=confidence,
            language="kotlin",
            evidence=evidence,
            stats={
                "coverage": round(coverage, 2),
                "public_function_count": public_function_count,
                "documented_function_count": documented_function_count,
                "public_class_count": public_class_count,
                "documented_class_count": documented_class_count,
                "uses_dokka": uses_dokka,
                "kdoc_tags": kdoc_tags,
                "todo_count": todo_count,
                "has_readme": has_readme,
                "patterns": patterns,
            },
        ))

        return result
