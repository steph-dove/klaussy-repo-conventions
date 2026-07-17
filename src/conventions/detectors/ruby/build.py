"""Ruby build tooling and dependency management conventions detector."""

from __future__ import annotations

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import RubyDetector

# Gems worth surfacing as quality gates in the build.
QUALITY_GEMS = ("rubocop", "standard", "brakeman", "simplecov", "reek")


@DetectorRegistry.register
class RubyBuildDetector(RubyDetector):
    """Detect Ruby dependency management and task-runner conventions."""

    name = "ruby_build"
    description = "Detects Ruby dependency management and task-runner conventions"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect Bundler/Rails build conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        has_gemfile = (ctx.repo_root / "Gemfile").is_file()
        gemspecs = list(ctx.repo_root.glob("*.gemspec"))

        if not has_gemfile and not gemspecs:
            return result

        # Whether this is a Rails app decides how tests are run: `bin/rails test`
        # for an app, `rake test` for a plain gem. Getting this wrong hands a
        # non-Rails gem a `rails test` command that does not exist.
        is_rails = (
            index.count_gem("rails")
            or (ctx.repo_root / "config/application.rb").is_file()
            or (ctx.repo_root / "config/routes.rb").is_file()
        )

        quality_gems = [gem for gem in QUALITY_GEMS if index.count_gem(gem)]
        has_lockfile = (ctx.repo_root / "Gemfile.lock").is_file()
        has_rakefile = (ctx.repo_root / "Rakefile").is_file()
        gem_count = len(index.gems)

        primary_tool = "rails" if is_rails else "bundler"
        project_type = "Rails application" if is_rails else "Ruby gem/library"

        title = f"Build: Bundler ({project_type})"

        description = f"Manages dependencies with Bundler; {gem_count} gem(s) declared in the Gemfile."
        if gemspecs:
            description += f" Packaged as a gem ({gemspecs[0].name})."
        if has_lockfile:
            description += " Gemfile.lock is committed, pinning resolved versions."
        elif not gemspecs:
            description += (
                " No Gemfile.lock is committed; applications should commit it so"
                " deployments resolve the same versions."
            )
        if has_rakefile:
            description += " Rake is used as the task runner."
        if quality_gems:
            description += f" Quality gems: {', '.join(quality_gems)}."

        confidence = 0.6
        if gem_count:
            confidence += 0.2
        if has_lockfile or gemspecs:
            confidence += 0.1
        confidence = min(0.95, confidence)

        result.rules.append(self.make_rule(
            rule_id="ruby.conventions.build_tools",
            category="build",
            title=title,
            description=description,
            confidence=confidence,
            language="ruby",
            # The Gemfile is not a .rb source file, so it is absent from the
            # index and cannot yield evidence snippets.
            evidence=[],
            stats={
                "build_system": "bundler",
                # CLAUDE.md's tech-stack renderer reads `primary_tool` for
                # build_tools rules, and derives build/test commands from it.
                # Rails apps and plain gems run their tests differently.
                "primary_tool": primary_tool,
                "project_type": project_type,
                "is_rails": is_rails,
                "gem_count": gem_count,
                "has_lockfile": has_lockfile,
                "has_rakefile": has_rakefile,
                "is_gem": bool(gemspecs),
                "quality_gems": quality_gems,
            },
        ))

        return result
