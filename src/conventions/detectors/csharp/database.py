"""C# database and persistence conventions detector."""

from __future__ import annotations

import re

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import CSharpDetector
from .index import make_evidence

LIBRARY_IMPORT_SIGNALS: dict[str, tuple[str, ...]] = {
    "Entity Framework Core": ("Microsoft.EntityFrameworkCore",),
    "Dapper": ("Dapper",),
    "NHibernate": ("NHibernate",),
    "FluentMigrator": ("FluentMigrator",),
    "DbUp": ("DbUp",),
}

LIBRARY_DEPENDENCY_SIGNALS: dict[str, tuple[str, ...]] = {
    "Entity Framework Core": ("Microsoft.EntityFrameworkCore",),
    "Dapper": ("Dapper",),
    "NHibernate": ("NHibernate",),
    "FluentMigrator": ("FluentMigrator",),
    "DbUp": ("dbup",),
}

DB_CONTEXT_PATTERN = r":\s*DbContext\b"
EF_MIGRATION_PATTERN = r"\[Migration\(\"[^\"]+\"\)\]"
_SQL_KEYWORDS = r"(?:SELECT|INSERT|UPDATE|DELETE)"
RAW_SQL_CONCAT_PATTERN = '(?i)"' + _SQL_KEYWORDS + r'\b[^"\n]*"\s*\+'


@DetectorRegistry.register
class CSharpDatabaseDetector(CSharpDetector):
    """Detect C# database access and persistence conventions."""

    name = "csharp_database"
    description = "Detects C# database access and persistence conventions"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect database conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        build_info = self.get_build_info(ctx)

        # 1. Gather import signals
        detected_libs: set[str] = set()
        for rel_path, file_idx in index.files.items():
            if file_idx.is_test:
                continue
            for using_path, _ in file_idx.usings:
                for lib, prefixes in LIBRARY_IMPORT_SIGNALS.items():
                    if any(using_path.startswith(p) for p in prefixes):
                        detected_libs.add(lib)

        # 2. Gather build dependencies
        deps = set(build_info.dependencies)
        for lib, candidates in LIBRARY_DEPENDENCY_SIGNALS.items():
            if any(any(c in d for d in deps) for c in candidates):
                detected_libs.add(lib)

        # 3. Specific pattern detection
        db_contexts = index.search_pattern(DB_CONTEXT_PATTERN, exclude_tests=True)
        ef_migrations = index.search_pattern(EF_MIGRATION_PATTERN, exclude_tests=True)
        raw_sql_concats = index.search_pattern(RAW_SQL_CONCAT_PATTERN, exclude_tests=True)

        if db_contexts or ef_migrations:
            detected_libs.add("Entity Framework Core")

        if not detected_libs and not db_contexts and not ef_migrations and not raw_sql_concats:
            return result

        # 4. Compile Title and Description
        libs_list = sorted(detected_libs)
        title = "Database: " + "/".join(libs_list) if libs_list else "Database: Persistence layer"

        desc_parts = []
        if libs_list:
            desc_parts.append(f"Uses {', '.join(libs_list)} for database access.")
        if db_contexts:
            desc_parts.append(f"Detected {len(db_contexts)} DbContext class declaration(s).")
        if ef_migrations:
            desc_parts.append(f"Detected Entity Framework Core database migrations ({len(ef_migrations)} migration files).")
        if raw_sql_concats:
            desc_parts.append(f"Detected {len(raw_sql_concats)} occurrences of potential raw SQL concatenation (high SQL-injection risk).")

        description = " ".join(desc_parts)

        # Build evidence
        evidence = []
        # Add DbContext evidence
        for rel_path, line, _ in db_contexts[:2]:
            ev = make_evidence(index, rel_path, line, radius=3)
            if ev:
                evidence.append(ev)
        # Add migration evidence
        if len(evidence) < ctx.max_evidence_snippets:
            for rel_path, line, _ in ef_migrations[:1]:
                ev = make_evidence(index, rel_path, line, radius=3)
                if ev:
                    evidence.append(ev)

        stats = {
            "libraries": libs_list,
            "has_ef_core": "Entity Framework Core" in detected_libs,
            "dbcontext_count": len(db_contexts),
            "migration_count": len(ef_migrations),
            "raw_sql_concat_count": len(raw_sql_concats),
        }


        result.rules.append(self.make_rule(
            rule_id="csharp.conventions.database",
            category="database",
            title=title,
            description=description,
            confidence=0.8,
            language="csharp",
            evidence=evidence,
            stats=stats,
        ))

        # 2. Database Entities
        db_entities = []
        dbset_pattern = re.compile(r'DbSet<\s*(\w+)\s*>')
        for rel_path, file_idx in index.files.items():
            if file_idx.role == "test":
                continue
            content = "\n".join(file_idx.lines)
            for match in dbset_pattern.finditer(content):
                entity_name = match.group(1)
                db_entities.append({
                    "name": entity_name,
                    "file": rel_path,
                })

        if db_entities:
            names = [e["name"] for e in db_entities[:10]]
            db_ent_desc = (
                f"{len(db_entities)} database model(s)/table(s) detected: {', '.join(names)}"
                + ("..." if len(db_entities) > 10 else "") + "."
            )
            result.rules.append(self.make_rule(
                rule_id="csharp.conventions.db_entities",
                category="database",
                title="Database entities",
                description=db_ent_desc,
                confidence=0.9,
                language="csharp",
                evidence=[],
                stats={
                    "entities": db_entities,
                    "entity_count": len(db_entities),
                    "orm": "efcore" if "Entity Framework Core" in detected_libs else "unknown",
                },
            ))

        return result
