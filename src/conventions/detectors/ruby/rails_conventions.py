"""Ruby and Rails architecture conventions detector."""

from __future__ import annotations

from collections import Counter
from typing import Optional

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import RubyDetector
from .index import RubyFileIndex, make_evidence

ARCHITECTURAL_ROLES = ("api", "service", "db", "model")


@DetectorRegistry.register
class RubyRailsConventionsDetector(RubyDetector):
    """Detect Ruby on Rails project structure and architectural patterns."""

    name = "ruby_rails_conventions"
    description = "Detects Ruby on Rails project structure and architectural patterns"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect Ruby/Rails architecture conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        is_rails = index.count_gem("rails") or \
                   (ctx.repo_root / "config/application.rb").exists() or \
                   (ctx.repo_root / "config/routes.rb").exists()

        structure = "Rails Application" if is_rails else "Ruby Library/Script"

        role_counts = Counter(f.role for f in index.files.values())
        layers = sorted(role for role in role_counts if role in ARCHITECTURAL_ROLES)

        has_rubocop = (ctx.repo_root / ".rubocop.yml").exists()

        confidence = 0.8 if is_rails else 0.5
        title = f"Architecture: {structure}"

        # A full index means the walk hit its cap, so the file count is the limit
        # rather than the codebase size, and the layers below are only those that
        # happened to be reached first.
        scanned = len(index.files)
        truncated = scanned >= ctx.max_files

        if truncated:
            desc_parts = [
                f"Ruby codebase (at least {scanned} files; the scan stopped at the "
                f"{ctx.max_files}-file limit) follows a {structure} layout."
            ]
        else:
            desc_parts = [f"Ruby codebase ({scanned} files) follows a {structure} layout."]

        if is_rails:
            desc_parts.append("Standard Rails Model-View-Controller (MVC) directory structure is present.")
        if layers:
            layer_note = f"Layers present: {', '.join(layers)}."
            if truncated:
                layer_note = (
                    f"Layers seen in the scanned subset: {', '.join(layers)} "
                    "(the scan was truncated, so others may exist)."
                )
            desc_parts.append(layer_note)
        if has_rubocop:
            desc_parts.append("RuboCop configuration (.rubocop.yml) is present for code style enforcement.")
        else:
            desc_parts.append("No RuboCop configuration found.")

        description = " ".join(desc_parts)

        # Build evidence
        evidence = []
        preferred_role_order = ["api", "model", "db", "main"]
        ordered_roles = [r for r in preferred_role_order if r in role_counts]

        for role in ordered_roles:
            if len(evidence) >= ctx.max_evidence_snippets:
                break
            candidate: Optional[RubyFileIndex] = None
            for file_idx in index.get_files_by_role(role):
                if not file_idx.is_test:
                    candidate = file_idx
                    break
            if candidate:
                ev = make_evidence(index, candidate.relative_path, 1, radius=3)
                if ev:
                    evidence.append(ev)

        stats = {
            "structure": structure,
            "is_rails": is_rails,
            "has_rubocop": has_rubocop,
            "layers": layers,
            "role_counts": dict(role_counts),
            # Files actually scanned, which is the codebase size only when the
            # scan was not truncated -- hence the companion flag.
            "file_count": scanned,
            "scan_truncated": truncated,
        }

        result.rules.append(self.make_rule(
            rule_id="ruby.conventions.rails_structure",
            category="architecture",
            title=title,
            description=description,
            confidence=confidence,
            language="ruby",
            evidence=evidence,
            stats=stats,
        ))

        return result
