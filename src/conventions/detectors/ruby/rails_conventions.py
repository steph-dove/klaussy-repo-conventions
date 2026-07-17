"""Ruby and Rails architecture conventions detector."""

from __future__ import annotations

import re
from collections import Counter
from typing import Optional

from ...fs import read_file_safe
from ...schemas import EvidenceSnippet
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
        truncated = self.scan_was_truncated(index, ctx)

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
        evidence: list[EvidenceSnippet] = []
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

        # 2. Build Tools / Bundler
        has_gemfile = ctx.repo_root.joinpath("Gemfile").exists()
        gem_count = len(index.gems)
        build_title = "Build: Bundler"
        build_desc = f"Uses Bundler package manager with {gem_count} gems declared in Gemfile."

        result.rules.append(self.make_rule(
            rule_id="ruby.conventions.build_tools",
            category="build",
            title=build_title,
            description=build_desc,
            confidence=0.8,
            language="ruby",
            evidence=[],
            stats={
                "has_gemfile": has_gemfile,
                "gem_count": gem_count,
            },
        ))

        # 3. Error Handling
        rescue_count = index.count_pattern(r"\brescue\b", exclude_tests=True)
        errors_title = "Error Handling: Standard rescue"
        errors_desc = f"Uses begin-rescue blocks ({rescue_count} found) for exception handling."

        errors_evidence = []
        if rescue_count > 0:
            rescue_sites = index.search_pattern(r"\brescue\b", exclude_tests=True, limit=1)
            if rescue_sites:
                ev = make_evidence(index, rescue_sites[0][0], rescue_sites[0][1], radius=3)
                if ev:
                    errors_evidence.append(ev)

        result.rules.append(self.make_rule(
            rule_id="ruby.conventions.errors",
            category="errors",
            title=errors_title,
            description=errors_desc,
            confidence=0.8,
            language="ruby",
            evidence=errors_evidence,
            stats={
                "rescue_count": rescue_count,
            },
        ))

        # 4. Security & SQL Injection
        has_raw_sql_usage = index.count_pattern(r'\b(?:find_by_sql|connection\.execute)\b', exclude_tests=True) > 0
        security_title = "Security: Secure settings"
        if has_raw_sql_usage:
            security_title = "Security: Raw SQL injection risk"

        security_desc = "Checks for secure Rails settings."
        if has_raw_sql_usage:
            security_desc += " Warning: Detected raw SQL query API usage (e.g. find_by_sql)."

        result.rules.append(self.make_rule(
            rule_id="ruby.conventions.security",
            category="security",
            title=security_title,
            description=security_desc,
            confidence=0.8,
            language="ruby",
            evidence=[],
            stats={
                "has_raw_sql_usage": has_raw_sql_usage,
            },
        ))

        # 5. Logging
        logger_count = index.count_pattern(r'\b(?:logger\.(?:info|error|warn|debug)|Rails\.logger)\b', exclude_tests=True)
        logging_title = "Logging: Rails logger"
        logging_desc = f"Uses Rails logger for application events ({logger_count} statements found)."

        result.rules.append(self.make_rule(
            rule_id="ruby.conventions.logging",
            category="logging",
            title=logging_title,
            description=logging_desc,
            confidence=0.8,
            language="ruby",
            evidence=[],
            stats={
                "logger_count": logger_count,
            },
        ))

        # 6. API Routes
        routes = []
        methods: dict[str, int] = {}
        routes_file = ctx.repo_root.joinpath("config/routes.rb")
        if routes_file.exists():
            content = read_file_safe(routes_file)
            if content:
                route_pattern = re.compile(r'\b(get|post|put|delete|patch)\s+["\']([^"\']+)["\']')
                for match in route_pattern.finditer(content):
                    method = match.group(1).upper()
                    path = match.group(2)
                    line = content[:match.start()].count("\n") + 1
                    methods[method] = methods.get(method, 0) + 1
                    routes.append({
                        "method": method,
                        "path": path,
                        "file": "config/routes.rb",
                        "line": line,
                    })

                res_pattern = re.compile(r'\bresources\s+:(\w+)')
                for match in res_pattern.finditer(content):
                    res_name = match.group(1)
                    line = content[:match.start()].count("\n") + 1
                    for m in ("GET", "POST", "PUT", "DELETE"):
                        methods[m] = methods.get(m, 0) + 1
                    routes.append({
                        "method": "ANY",
                        "path": f"/{res_name}",
                        "file": "config/routes.rb",
                        "line": line,
                    })

        if routes:
            description = (
                f"{len(routes)} API routes detected. "
                f"Methods: {', '.join(f'{k}: {v}' for k, v in sorted(methods.items()))}."
            )
            result.rules.append(self.make_rule(
                rule_id="ruby.conventions.api_routes",
                category="api",
                title="API routes",
                description=description,
                confidence=0.85,
                language="ruby",
                evidence=[],
                stats={
                    "routes": routes,
                    "total_routes": len(routes),
                    "methods": methods,
                },
            ))

        return result
