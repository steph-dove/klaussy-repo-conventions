"""PHP architecture conventions detector."""

from __future__ import annotations

import re
from collections import Counter
from typing import Optional

from ...schemas import EvidenceSnippet
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
        truncated = self.scan_was_truncated(index, ctx)

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
        evidence: list[EvidenceSnippet] = []
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

        # 2. PHP Build Tools / Composer
        has_composer = ctx.repo_root.joinpath("composer.json").exists()
        dep_count = len(index.dependencies)
        build_title = "Build: Composer"
        build_desc = f"Uses Composer package manager with {dep_count} dependencies declared in composer.json."

        result.rules.append(self.make_rule(
            rule_id="php.conventions.build_tools",
            category="build",
            title=build_title,
            description=build_desc,
            confidence=0.8,
            language="php",
            evidence=[],
            stats={
                "has_composer": has_composer,
                "dependency_count": dep_count,
            },
        ))

        # 3. PHP Error Handling
        try_catch_count = index.count_pattern(r"\btry\s*\{", exclude_tests=True)
        errors_title = "Error Handling: PHP exceptions"
        errors_desc = f"Uses structured try-catch blocks ({try_catch_count} found) for exception handling."

        errors_evidence = []
        if try_catch_count > 0:
            tc_sites = index.search_pattern(r"\btry\s*\{", exclude_tests=True, limit=1)
            if tc_sites:
                ev = make_evidence(index, tc_sites[0][0], tc_sites[0][1], radius=3)
                if ev:
                    errors_evidence.append(ev)

        result.rules.append(self.make_rule(
            rule_id="php.conventions.errors",
            category="errors",
            title=errors_title,
            description=errors_desc,
            confidence=0.8,
            language="php",
            evidence=errors_evidence,
            stats={
                "try_catch_count": try_catch_count,
            },
        ))

        # 4. PHP Logging
        log_count = index.count_pattern(r'\b(?:Log::(?:info|error|warn|debug|write)|logger\s*\(|error_log\s*\()\b', exclude_tests=True)
        logging_title = "Logging: Monolog / PSR-3"
        logging_desc = f"Uses PSR-3 compatible logging facades ({log_count} statements found)."

        result.rules.append(self.make_rule(
            rule_id="php.conventions.logging",
            category="logging",
            title=logging_title,
            description=logging_desc,
            confidence=0.8,
            language="php",
            evidence=[],
            stats={
                "logger_count": log_count,
            },
        ))

        # 5. API Routes
        routes = []
        methods: dict[str, int] = {}

        laravel_route_pattern = re.compile(r'Route::(get|post|put|delete|patch|any)\s*\(\s*["\']([^"\']+)["\']')
        symfony_route_pattern = re.compile(r'#\[Route\(\s*["\']([^"\']+)["\'](?:,\s*name:\s*["\'][^"\']+["\'])?(?:,\s*methods:\s*\[([^\]]+)\])?\s*\)\]')

        for rel_path, file_idx in index.files.items():
            if file_idx.role == "test":
                continue
            content = "\n".join(file_idx.lines)

            for match in laravel_route_pattern.finditer(content):
                method = match.group(1).upper()
                path = match.group(2)
                line = content[:match.start()].count("\n") + 1
                methods[method] = methods.get(method, 0) + 1
                routes.append({
                    "method": method,
                    "path": path,
                    "file": rel_path,
                    "line": line,
                })
                if len(routes) >= 100:
                    break

            for match in symfony_route_pattern.finditer(content):
                path = match.group(1)
                method_raw = match.group(2) if match.lastindex is not None and match.lastindex >= 2 and match.group(2) else "ANY"
                parsed_methods = []
                if method_raw != "ANY":
                    for m in re.findall(r'["\'](\w+)["\']', method_raw):
                        parsed_methods.append(m.upper())
                if not parsed_methods:
                    parsed_methods = ["ANY"]

                line = content[:match.start()].count("\n") + 1
                for method in parsed_methods:
                    methods[method] = methods.get(method, 0) + 1
                    routes.append({
                        "method": method,
                        "path": path,
                        "file": rel_path,
                        "line": line,
                    })
                if len(routes) >= 100:
                    break

            if len(routes) >= 100:
                break

        if routes:
            description = (
                f"{len(routes)} API routes detected. "
                f"Methods: {', '.join(f'{k}: {v}' for k, v in sorted(methods.items()))}."
            )
            result.rules.append(self.make_rule(
                rule_id="php.conventions.api_routes",
                category="api",
                title="API routes",
                description=description,
                confidence=0.85,
                language="php",
                evidence=[],
                stats={
                    "routes": routes,
                    "total_routes": len(routes),
                    "methods": methods,
                },
            ))

        return result
