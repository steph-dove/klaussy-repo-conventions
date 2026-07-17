"""PHP database and ORM conventions detector."""

from __future__ import annotations

import re

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import PHPDetector
from .index import make_evidence


@DetectorRegistry.register
class PHPDatabaseDetector(PHPDetector):
    """Detect PHP database libraries, migrations, and model structures."""

    name = "php_database"
    description = "Detects PHP database libraries, migrations, and model structures"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect database conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        # 1. ORM/Database library detection
        libs = []
        has_eloquent = index.count_dependency("illuminate/database") or \
                       index.count_use_matching("Illuminate\\Database\\Eloquent") or \
                       ctx.repo_root.joinpath("database/migrations").exists()

        has_doctrine = index.count_dependency("doctrine/orm") or \
                       index.count_use_matching("Doctrine\\ORM")

        if has_eloquent:
            libs.append("Eloquent ORM")
        if has_doctrine:
            libs.append("Doctrine ORM")

        if not libs:
            return result

        # 2. Migrations counting
        laravel_migrations = list(ctx.repo_root.glob("database/migrations/*.php"))
        doctrine_migrations = list(ctx.repo_root.glob("src/Migrations/*.php")) + list(ctx.repo_root.glob("migrations/*.php"))
        migration_count = len(laravel_migrations) + len(doctrine_migrations)

        # 3. Model counting
        # Search for Eloquent models: classes extending Model
        model_count = index.count_pattern(r"\bclass\s+\w+\s+extends\s+Model\b")

        # Compile Title and Description
        libs_str = "/".join(libs)
        title = f"Database: {libs_str}"

        desc_parts = [
            f"Uses {libs_str} for database persistence and Object-Relational Mapping."
        ]
        if migration_count > 0:
            desc_parts.append(f"Detected {migration_count} schema migration file(s).")
        if model_count > 0:
            desc_parts.append(f"Detected {model_count} Eloquent Model class(es).")

        description = " ".join(desc_parts)

        # Build evidence
        evidence = []
        # Find Model declarations
        model_sites = index.search_pattern(r"\bclass\s+\w+\s+extends\s+Model\b", limit=2)
        for rel_path, line, _ in model_sites:
            ev = make_evidence(index, rel_path, line, radius=3)
            if ev:
                evidence.append(ev)

        stats = {
            "libraries": libs,
            "migration_count": migration_count,
            "model_count": model_count,
        }

        result.rules.append(self.make_rule(
            rule_id="php.conventions.database",
            category="database",
            title=title,
            description=description,
            confidence=0.8,
            language="php",
            evidence=evidence,
            stats=stats,
        ))

        # 2. Database Entities
        db_entities = []
        eloquent_pattern = re.compile(r'\bclass\s+(\w+)\s+extends\s+Model\b')
        doctrine_pattern = re.compile(r'#\[ORM\\Entity\]\s*(?:/\*\*.*?\*/\s*)?\b(?:class|interface)\s+(\w+)\b', re.DOTALL)

        for rel_path, file_idx in index.files.items():
            if file_idx.role == "test":
                continue
            content = "\n".join(file_idx.lines)

            for match in eloquent_pattern.finditer(content):
                db_entities.append({
                    "name": match.group(1),
                    "file": rel_path,
                })

            for match in doctrine_pattern.finditer(content):
                db_entities.append({
                    "name": match.group(1),
                    "file": rel_path,
                })

        if db_entities:
            names = [e["name"] for e in db_entities[:10]]
            db_ent_desc = (
                f"{len(db_entities)} database model(s)/table(s) detected: {', '.join(names)}"
                + ("..." if len(db_entities) > 10 else "") + "."
            )
            result.rules.append(self.make_rule(
                rule_id="php.conventions.db_entities",
                category="database",
                title="Database entities",
                description=db_ent_desc,
                confidence=0.9,
                language="php",
                evidence=[],
                stats={
                    "entities": db_entities,
                    "entity_count": len(db_entities),
                    "orm": libs[0] if libs else "eloquent",
                },
            ))

        return result
