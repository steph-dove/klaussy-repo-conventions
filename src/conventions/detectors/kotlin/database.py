"""Kotlin database and persistence conventions detector."""

from __future__ import annotations

from typing import Optional

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import KotlinDetector
from .index import make_evidence

# Import substrings that identify each database library. These are specific enough
# to disambiguate libraries that share annotation names: Room's @Entity/@Dao/@Query
# come from `androidx.room`, while Spring Data JPA's/JPA-Hibernate's same-named
# annotations come from `org.springframework.data.jpa`/`jakarta.persistence`/
# `javax.persistence`/`org.hibernate` -- matching on the import alone is enough to
# attribute usage to the right library without guessing from annotation names.
LIBRARY_IMPORT_SIGNALS: dict[str, tuple[str, ...]] = {
    "Exposed": ("org.jetbrains.exposed",),
    "Spring Data JPA": ("org.springframework.data.jpa",),
    "JPA/Hibernate": ("jakarta.persistence", "javax.persistence", "org.hibernate"),
    "Room": ("androidx.room",),
    "jOOQ": ("org.jooq",),
    "JDBI": ("org.jdbi",),
    "Ktorm": ("org.ktorm",),
    "SQLDelight": ("app.cash.sqldelight", "com.squareup.sqldelight"),
    "R2DBC": ("io.r2dbc",),
    "Spring JdbcTemplate": ("org.springframework.jdbc",),
    "MongoDB": ("org.springframework.data.mongodb", "com.mongodb"),
    "Redis": ("io.lettuce", "redis.clients.jedis", "org.springframework.data.redis"),
}

# Build-file (Gradle/Maven coordinate) signals. These corroborate import-based
# detection, or stand in for it when a dependency is declared but not yet imported.
LIBRARY_DEPENDENCY_SIGNALS: dict[str, tuple[str, ...]] = {
    "Exposed": ("org.jetbrains.exposed",),
    "Spring Data JPA": ("spring-boot-starter-data-jpa", "spring-data-jpa"),
    "JPA/Hibernate": ("hibernate-core", "hibernate"),
    "Room": ("androidx.room",),
    "jOOQ": ("org.jooq",),
    "JDBI": ("org.jdbi",),
    "Ktorm": ("org.ktorm",),
    "SQLDelight": ("app.cash.sqldelight", "com.squareup.sqldelight"),
    "R2DBC": ("r2dbc",),
    "Spring JdbcTemplate": ("spring-boot-starter-jdbc", "spring-jdbc"),
    "MongoDB": ("spring-boot-starter-data-mongodb", "mongodb-driver", "spring-data-mongodb"),
    "Redis": ("lettuce-core", "jedis", "spring-boot-starter-data-redis", "spring-data-redis"),
}

DRIVER_DEPENDENCY_SIGNALS: dict[str, tuple[str, ...]] = {
    "postgresql": ("org.postgresql",),
    "mysql": ("mysql-connector", "com.mysql"),
    "h2": ("com.h2database",),
    "sqlite": ("org.xerial", "sqlite-jdbc"),
}

MIGRATION_DEPENDENCY_SIGNALS: dict[str, tuple[str, ...]] = {
    "Flyway": ("org.flywaydb",),
    "Liquibase": ("liquibase",),
}

# A handful of libraries read better in a title with a qualifier than as a bare name.
TITLE_LABELS: dict[str, str] = {
    "Exposed": "Exposed DSL",
}

REPOSITORY_INTERFACE_PATTERN = (
    r"interface\s+\w+\s*:\s*(?:JpaRepository|CrudRepository|PagingAndSortingRepository|"
    r"ReactiveCrudRepository|CoroutineCrudRepository)\b"
)
EXPOSED_TABLE_PATTERN = r"object\s+\w+\s*:\s*(?:Table|IntIdTable|UUIDTable|LongIdTable)\b"
EXPOSED_TRANSACTION_PATTERN = r"\btransaction\s*\{"
EXPOSED_SUSPENDED_TRANSACTION_PATTERN = r"\bnewSuspendedTransaction\s*\{"

# Conservative SQL-injection-shaped anti-pattern: a string literal that *starts* with
# a SQL verb and later contains Kotlin interpolation (`$name` / `${expr}`), or is
# concatenated with `+`. Interpolation must be followed by an identifier char or `{`
# so native bind placeholders like `$1` (not valid Kotlin interpolation) aren't flagged.
_SQL_KEYWORDS = r"(?:SELECT|INSERT|UPDATE|DELETE)"
RAW_SQL_INTERPOLATION_PATTERN = '(?i)"' + _SQL_KEYWORDS + r'\b[^"\n]*\$(?:\{|[A-Za-z_])'
RAW_SQL_CONCAT_PATTERN = '(?i)"' + _SQL_KEYWORDS + r'\b[^"\n]*"\s*\+'


class _LibraryHits:
    """Accumulated signal (hit count + example sites) for a single database library."""

    def __init__(self) -> None:
        self.hits = 0
        self.examples: list[tuple[str, int]] = []

    def add(self, rel_path: str, line: int) -> None:
        """Record one occurrence, keeping a handful of example sites."""
        self.hits += 1
        if len(self.examples) < 5:
            self.examples.append((rel_path, line))


@DetectorRegistry.register
class KotlinDatabaseDetector(KotlinDetector):
    """Detect Kotlin database access and persistence conventions."""

    name = "kotlin_database"
    description = "Detects Kotlin database access and persistence conventions"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect database/ORM library usage, entities, repositories, and anti-patterns."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        build_info = self.get_build_info(ctx)
        libraries: dict[str, _LibraryHits] = {}

        # Import-based signals -- also the mechanism that disambiguates Room from
        # Spring Data JPA / JPA-Hibernate for the annotation names they share.
        for lib, needles in LIBRARY_IMPORT_SIGNALS.items():
            for needle in needles:
                for rel_path, _import_path, line in index.find_imports_matching(needle, limit=50):
                    libraries.setdefault(lib, _LibraryHits()).add(rel_path, line)

        # Build-file signals corroborate, or stand in for, import-based detection.
        for lib, needles in LIBRARY_DEPENDENCY_SIGNALS.items():
            if any(build_info.has_dependency(n) for n in needles):
                libraries.setdefault(lib, _LibraryHits())

        if not libraries:
            return result

        all_classes = index.all_classes()

        # Entities: JPA/Room @Entity-annotated classes plus Exposed table objects.
        # The table count comes from count_pattern: len(search_pattern(limit=N))
        # would silently cap the reported total at N.
        entity_classes = [(rel, cls) for rel, cls in all_classes if "Entity" in cls.annotations]
        exposed_table_count = (
            index.count_pattern(EXPOSED_TABLE_PATTERN) if "Exposed" in libraries else 0
        )
        exposed_table_matches = (
            index.search_pattern(EXPOSED_TABLE_PATTERN, limit=ctx.max_evidence_snippets)
            if "Exposed" in libraries
            else []
        )
        entity_count = len(entity_classes) + exposed_table_count

        # Repositories/DAOs: @Repository/@Dao-annotated classes plus interfaces
        # extending a Spring Data repository base type. Keyed by site to dedupe a
        # declaration that happens to match both signals.
        repo_sites: dict[tuple[str, int], None] = {}
        for rel, cls in all_classes:
            if "Repository" in cls.annotations or "Dao" in cls.annotations:
                repo_sites.setdefault((rel, cls.line), None)
        for rel, line, _match in index.search_pattern(REPOSITORY_INTERFACE_PATTERN, limit=100):
            repo_sites.setdefault((rel, line), None)
        repository_count = len(repo_sites)

        # Transaction management.
        transactional_count = index.count_annotation("Transactional")
        exposed_tx_count = (
            index.count_pattern(EXPOSED_TRANSACTION_PATTERN) if "Exposed" in libraries else 0
        )
        exposed_suspended_tx_count = (
            index.count_pattern(EXPOSED_SUSPENDED_TRANSACTION_PATTERN) if "Exposed" in libraries else 0
        )
        tx_parts: list[str] = []
        if transactional_count:
            tx_parts.append("@Transactional")
        if exposed_tx_count:
            tx_parts.append("Exposed transaction {}")
        if exposed_suspended_tx_count:
            tx_parts.append("Exposed newSuspendedTransaction {}")
        transaction_pattern: Optional[str] = ", ".join(tx_parts) if tx_parts else None

        # Suspend (coroutine-based) repository functions.
        repo_files = {rel for rel, _ in repo_sites} | {f.relative_path for f in index.get_files_by_role("db")}
        suspend_repository_count = sum(
            1 for rel, fn in index.all_functions() if fn.is_suspend and rel in repo_files
        )

        # Anti-pattern: raw SQL built via string interpolation or `+` concatenation.
        raw_sql_interp_matches = index.search_pattern(
            RAW_SQL_INTERPOLATION_PATTERN, limit=ctx.max_evidence_snippets, exclude_tests=True
        )
        raw_sql_concat_matches = index.search_pattern(
            RAW_SQL_CONCAT_PATTERN, limit=ctx.max_evidence_snippets, exclude_tests=True
        )
        raw_sql_interpolation_count = index.count_pattern(
            RAW_SQL_INTERPOLATION_PATTERN, exclude_tests=True
        ) + index.count_pattern(RAW_SQL_CONCAT_PATTERN, exclude_tests=True)

        # N+1 risk, lightweight: only worth mentioning when JPA/Hibernate is present.
        jpa_present = "Spring Data JPA" in libraries or "JPA/Hibernate" in libraries
        eager_fetch_count = index.count_pattern(r"FetchType\.EAGER") if jpa_present else 0

        # Migrations.
        migration_tool: Optional[str] = None
        uses_migrations = False
        for candidate in (
            ctx.repo_root / "src" / "main" / "resources" / "db" / "migration",
            ctx.repo_root / "db" / "migration",
        ):
            if candidate.is_dir() and list(candidate.glob("V*__*.sql")):
                migration_tool = "Flyway"
                uses_migrations = True
                break
        if migration_tool is None:
            for lib, needles in MIGRATION_DEPENDENCY_SIGNALS.items():
                if any(build_info.has_dependency(n) for n in needles):
                    migration_tool = lib
                    uses_migrations = True
                    break

        # Drivers.
        drivers = [
            name
            for name, needles in DRIVER_DEPENDENCY_SIGNALS.items()
            if any(build_info.has_dependency(n) for n in needles)
        ]

        library_names = list(libraries.keys())
        primary_library = max(libraries.items(), key=lambda kv: kv[1].hits)[0]
        primary_label = TITLE_LABELS.get(primary_library, primary_library)

        patterns: list[str] = []
        if exposed_table_matches:
            patterns.append("Exposed Table objects")
        if exposed_tx_count:
            patterns.append("Exposed transaction {}")
        if exposed_suspended_tx_count:
            patterns.append("Exposed newSuspendedTransaction {}")
        if transactional_count:
            patterns.append("@Transactional")
        if repository_count:
            patterns.append("Repository/DAO pattern")
        if suspend_repository_count:
            patterns.append("suspend repository functions")
        if uses_migrations and migration_tool:
            patterns.append(f"{migration_tool} migrations")
        if eager_fetch_count:
            patterns.append("FetchType.EAGER (N+1 risk)")
        if raw_sql_interpolation_count:
            patterns.append("raw SQL string interpolation (possible injection)")

        title = f"Database: {primary_label}"
        if entity_count:
            singular, plural = (
                ("table", "tables") if primary_library == "Exposed" else ("entity", "entities")
            )
            noun = singular if entity_count == 1 else plural
            title += f" with {entity_count} {noun}"
        if uses_migrations and migration_tool:
            title += f", {migration_tool} migrations"

        description_parts: list[str] = [f"Uses {primary_label} for database access."]
        others = [name for name in library_names if name != primary_library]
        if others:
            description_parts.append(f"Also present: {', '.join(others)}.")
        if entity_count:
            description_parts.append(f"{entity_count} entity/table declaration(s) detected.")
        if repository_count:
            description_parts.append(f"{repository_count} repository/DAO declaration(s).")
        if transaction_pattern:
            description_parts.append(f"Transaction management via {transaction_pattern}.")
        if suspend_repository_count:
            description_parts.append(
                f"{suspend_repository_count} suspend repository function(s) (coroutine-based data access)."
            )
        if uses_migrations and migration_tool:
            description_parts.append(f"Uses {migration_tool} for schema migrations.")
        if drivers:
            description_parts.append(f"Database driver(s): {', '.join(drivers)}.")
        if eager_fetch_count:
            description_parts.append(
                f"{eager_fetch_count} FetchType.EAGER usage(s) risk N+1 query problems."
            )
        if raw_sql_interpolation_count:
            description_parts.append(
                f"WARNING: {raw_sql_interpolation_count} site(s) build SQL via string interpolation "
                "or `+` concatenation instead of parameterized queries -- a possible SQL injection risk."
            )

        description = " ".join(description_parts)

        # Confidence scales with the amount of corroborating signal found.
        confidence = 0.3
        confidence += min(0.3, 0.05 * sum(hits.hits for hits in libraries.values()))
        if entity_count:
            confidence += 0.15
        if repository_count:
            confidence += 0.1
        if len(library_names) == 1:
            confidence += 0.1
        if uses_migrations:
            confidence += 0.05
        confidence = min(0.95, confidence)

        # Evidence: lead with the raw-SQL anti-pattern sites since they're the most
        # actionable finding, then fall back to representative library/entity usage.
        evidence_sources: list[tuple[str, int]] = [
            (rel, line) for rel, line, _match in raw_sql_interp_matches
        ] + [(rel, line) for rel, line, _match in raw_sql_concat_matches]
        evidence_sources.extend(libraries[primary_library].examples)
        evidence_sources.extend(list(repo_sites.keys())[:5])
        evidence_sources.extend((rel, cls.line) for rel, cls in entity_classes[:5])

        evidence = []
        seen: set[tuple[str, int]] = set()
        for rel_path, line in evidence_sources:
            key = (rel_path, line)
            if key in seen:
                continue
            seen.add(key)
            ev = make_evidence(index, rel_path, line, radius=3)
            if ev:
                evidence.append(ev)
            if len(evidence) >= ctx.max_evidence_snippets:
                break

        result.rules.append(self.make_rule(
            rule_id="kotlin.conventions.db_library",
            category="database",
            title=title,
            description=description,
            confidence=confidence,
            language="kotlin",
            evidence=evidence,
            stats={
                "libraries": library_names,
                "primary_library": primary_library,
                "entity_count": entity_count,
                "repository_count": repository_count,
                "uses_migrations": uses_migrations,
                "migration_tool": migration_tool,
                "transaction_pattern": transaction_pattern,
                "suspend_repository_count": suspend_repository_count,
                "raw_sql_interpolation_count": raw_sql_interpolation_count,
                "patterns": patterns,
                "drivers": drivers,
            },
        ))

        return result
