"""Ruby database and ActiveRecord conventions detector."""

from __future__ import annotations

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import RubyDetector
from .index import make_evidence


@DetectorRegistry.register
class RubyDatabaseDetector(RubyDetector):
    """Detect Ruby database libraries, migrations, and model associations."""

    name = "ruby_database"
    description = "Detects Ruby database libraries, migrations, and model associations"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect database conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        # 1. ORM detection
        libs = []
        if index.count_gem("activerecord") or index.count_gem("rails"):
            libs.append("ActiveRecord")
        if index.count_gem("sequel"):
            libs.append("Sequel")
        if index.count_gem("rom"):
            libs.append("ROM")

        # Fallback to file structure checks
        has_migrations_dir = ctx.repo_root.joinpath("db/migrate").exists()
        if not libs and has_migrations_dir:
            libs.append("ActiveRecord")

        if not libs:
            return result

        # 2. Migration counting
        migration_files = list(ctx.repo_root.glob("db/migrate/*.rb"))
        migration_count = len(migration_files)

        # 3. Model associations counting
        associations_count = sum(len(f.associations) for f in index.files.values())

        # Compile Title and Description
        libs_str = "/".join(libs)
        title = f"Database: {libs_str}"

        desc_parts = [
            f"Uses {libs_str} for database persistence and Object-Relational Mapping."
        ]
        if migration_count > 0:
            desc_parts.append(f"Detected {migration_count} schema migration file(s) under `db/migrate/`.")
        if associations_count > 0:
            desc_parts.append(f"Parsed {associations_count} ActiveRelation association definition(s) (has_many, belongs_to, etc.) in model files.")

        description = " ".join(desc_parts)

        # Build evidence
        evidence = []
        # Find association evidence
        assoc_sites = index.search_pattern(r"\b(?:has_many|belongs_to|has_one|has_and_belongs_to_many)\b", limit=2)
        for rel_path, line, _ in assoc_sites:
            ev = make_evidence(index, rel_path, line, radius=3)
            if ev:
                evidence.append(ev)

        stats = {
            "libraries": libs,
            # CLAUDE.md's tech-stack renderer reads `primary_library` for
            # database rules; without it the Database line renders empty.
            "primary_library": libs[0] if libs else None,
            "migration_count": migration_count,
            "associations_count": associations_count,
        }

        result.rules.append(self.make_rule(
            rule_id="ruby.conventions.database",
            category="database",
            title=title,
            description=description,
            confidence=0.8,
            language="ruby",
            evidence=evidence,
            stats=stats,
        ))

        return result
