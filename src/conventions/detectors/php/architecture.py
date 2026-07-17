"""PHP architecture conventions detector."""

from __future__ import annotations

from collections import Counter
from typing import Optional

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import PHPDetector
from .index import PHPFileIndex, make_evidence

ARCHITECTURAL_ROLES = ("api", "service", "db", "model")


@DetectorRegistry.register
class PHPArchitectureDetector(PHPDetector):
    """Detect PHP project structure, module layout and framework styling."""

    name = "php_architecture"
    description = "Detects PHP project structure, module layout and framework styling"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect PHP architecture conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        # 1. Framework detection based on imports and composer.json
        has_laravel = index.count_dependency("laravel/framework") or \
                      ctx.repo_root.joinpath("artisan").exists() or \
                      ctx.repo_root.joinpath("routes/web.php").exists()

        has_symfony = index.count_dependency("symfony/framework-bundle") or \
                      ctx.repo_root.joinpath("bin/console").exists() or \
                      ctx.repo_root.joinpath("config/bundles.php").exists()

        framework = "PHP Library / Script"
        if has_laravel:
            framework = "Laravel Application"
        elif has_symfony:
            framework = "Symfony Application"

        # 2. Structure & Layering
        role_counts = Counter(f.role for f in index.files.values())
        layers = sorted(role for role in role_counts if role in ARCHITECTURAL_ROLES)

        title = f"Architecture: {framework}"

        # A full index means the walk hit its cap, so the file count is the limit
        # rather than the project size, and the layers below are only those that
        # happened to be reached first. Laravel has 3007 PHP files against a
        # default cap of 2000.
        scanned = len(index.files)
        truncated = scanned >= ctx.max_files

        if truncated:
            desc_parts = [
                f"PHP project (at least {scanned} files; the scan stopped at the "
                f"{ctx.max_files}-file limit) is structured as a {framework}."
            ]
        else:
            desc_parts = [f"PHP project ({scanned} files) is structured as a {framework}."]

        if layers:
            layer_note = f"Layers detected: {', '.join(layers)}."
            if truncated:
                layer_note = (
                    f"Layers seen in the scanned subset: {', '.join(layers)} "
                    "(the scan was truncated, so others may exist)."
                )
            desc_parts.append(layer_note)

        # Linting styling (PHP_CodeSniffer, PHP CS Fixer)
        has_phpcs = ctx.repo_root.joinpath("phpcs.xml").exists() or \
                    ctx.repo_root.joinpath(".php-cs-fixer.dist.php").exists() or \
                    ctx.repo_root.joinpath(".php-cs-fixer.php").exists()

        if has_phpcs:
            desc_parts.append("Code style rules (PHP CS Fixer or PHP_CodeSniffer) are present.")
        else:
            desc_parts.append("No PHP CS Fixer/PHP_CodeSniffer configuration found.")

        description = " ".join(desc_parts)

        # Build evidence
        evidence = []
        preferred_role_order = ["api", "service", "model", "main"]
        ordered_roles = [r for r in preferred_role_order if r in role_counts]

        for role in ordered_roles:
            if len(evidence) >= ctx.max_evidence_snippets:
                break
            candidate: Optional[PHPFileIndex] = None
            for file_idx in index.get_files_by_role(role):
                if not file_idx.is_test:
                    candidate = file_idx
                    break
            if candidate:
                ev = make_evidence(index, candidate.relative_path, 1, radius=3)
                if ev:
                    evidence.append(ev)

        stats = {
            "framework": framework,
            "has_laravel": has_laravel,
            "has_symfony": has_symfony,
            "has_phpcs": has_phpcs,
            "layers": layers,
            "role_counts": dict(role_counts),
            # Files actually scanned, which is the project size only when the
            # scan was not truncated -- hence the companion flag.
            "file_count": scanned,
            "scan_truncated": truncated,
        }

        result.rules.append(self.make_rule(
            rule_id="php.conventions.architecture",
            category="architecture",
            title=title,
            description=description,
            confidence=0.8,
            language="php",
            evidence=evidence,
            stats=stats,
        ))

        return result
