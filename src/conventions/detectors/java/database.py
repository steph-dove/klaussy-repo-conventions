"""Java database and persistence conventions detector."""

from __future__ import annotations

from typing import Optional

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import JavaDetector
from .index import make_evidence

LIBRARY_IMPORT_SIGNALS: dict[str, tuple[str, ...]] = {
    "Spring Data JPA": ("org.springframework.data.jpa", "org.springframework.data.repository"),
    "JPA/Hibernate": ("jakarta.persistence", "javax.persistence", "org.hibernate"),
    "MyBatis": ("org.apache.ibatis", "org.mybatis"),
    "jOOQ": ("org.jooq",),
    "Spring JdbcTemplate": ("org.springframework.jdbc",),
    # Only the JDBC API types imply database access. A bare `java.sql` prefix
    # also catches java.sql.Date/Time/Timestamp, which are plain value types --
    # gson imports them for its date type adapters and is not a database client.
    "JDBC": (
        "java.sql.Connection",
        "java.sql.PreparedStatement",
        "java.sql.Statement",
        "java.sql.ResultSet",
        "java.sql.DriverManager",
        "javax.sql.DataSource",
    ),
    "MongoDB": ("org.springframework.data.mongodb", "com.mongodb"),
    "Redis": ("io.lettuce", "redis.clients.jedis", "org.springframework.data.redis"),
}

LIBRARY_DEPENDENCY_SIGNALS: dict[str, tuple[str, ...]] = {
    "Spring Data JPA": ("spring-boot-starter-data-jpa", "spring-data-jpa"),
    "JPA/Hibernate": ("hibernate-core", "hibernate"),
    "MyBatis": ("mybatis-spring-boot-starter", "mybatis"),
    "jOOQ": ("org.jooq",),
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

REPOSITORY_INTERFACE_PATTERN = (
    r"interface\s+\w+\s+extends\s*(?:JpaRepository|CrudRepository|PagingAndSortingRepository|"
    r"Repository|MongoRepository|ListCrudRepository)\b"
)

_SQL_KEYWORDS = r"(?:SELECT|INSERT|UPDATE|DELETE)"
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
class JavaDatabaseDetector(JavaDetector):
    """Detect Java database access and persistence conventions."""

    name = "java_database"
    description = "Detects Java database access and persistence conventions"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect database conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        build_info = self.get_build_info(ctx)

        # 1. Gather import signals
        library_hits: dict[str, _LibraryHits] = {lib: _LibraryHits() for lib in LIBRARY_IMPORT_SIGNALS}
        for rel_path, file_idx in index.files.items():
            if file_idx.is_test:
                continue
            for import_path, line in file_idx.imports:
                for lib, prefixes in LIBRARY_IMPORT_SIGNALS.items():
                    if any(import_path.startswith(p) for p in prefixes):
                        library_hits[lib].add(rel_path, line)

        # 2. Gather build file signals
        detected_libs: set[str] = set()

        for lib, candidates in LIBRARY_DEPENDENCY_SIGNALS.items():
            if any(build_info.has_dependency(c) for c in candidates):
                detected_libs.add(lib)
        for lib, hits in library_hits.items():
            if hits.hits > 0:
                detected_libs.add(lib)

        # 3. Detect driver/engine
        driver: Optional[str] = None
        for engine, candidates in DRIVER_DEPENDENCY_SIGNALS.items():
            if any(build_info.has_dependency(c) for c in candidates):
                driver = engine
                break

        # 4. Detect migrations
        migration_tool: Optional[str] = None
        for tool, candidates in MIGRATION_DEPENDENCY_SIGNALS.items():
            if any(build_info.has_dependency(c) for c in candidates):
                migration_tool = tool
                break

        # Check for folders conventions
        has_flyway_dir = ctx.repo_root.joinpath("src/main/resources/db/migration").exists() or \
                         ctx.repo_root.joinpath("src/main/resources/db/migrations").exists()
        has_liquibase_dir = ctx.repo_root.joinpath("src/main/resources/db/changelog").exists()

        if has_flyway_dir:
            migration_tool = "Flyway"
        elif has_liquibase_dir:
            migration_tool = "Liquibase"

        # 5. Look for repository patterns and raw SQL concatenation.
        # Counts come from count_pattern -- search_pattern stops at its limit and
        # would silently cap the totals -- while the searches supply evidence.
        repository_count = index.count_pattern(REPOSITORY_INTERFACE_PATTERN, exclude_tests=True)
        raw_sql_concat_count = index.count_pattern(RAW_SQL_CONCAT_PATTERN, exclude_tests=True)
        repo_interfaces = index.search_pattern(REPOSITORY_INTERFACE_PATTERN, exclude_tests=True)
        raw_sql_concats = index.search_pattern(RAW_SQL_CONCAT_PATTERN, exclude_tests=True)

        if not detected_libs and not driver and not migration_tool and not repo_interfaces:
            return result

        # Compute title and description
        libs_list = sorted(detected_libs)
        title_parts = []
        if libs_list:
            title_parts.append("/".join(libs_list))
        if driver:
            title_parts.append(driver.capitalize())
        if migration_tool:
            title_parts.append(migration_tool)

        title = "Database: " + ", ".join(title_parts) if title_parts else "Database: Persistence layer"

        desc_parts = []
        if libs_list:
            desc_parts.append(f"Uses {', '.join(libs_list)} for database access.")
        if driver:
            desc_parts.append(f"Primary database engine is {driver.capitalize()}.")
        if migration_tool:
            desc_parts.append(f"Uses {migration_tool} for database migrations.")
        if repo_interfaces:
            desc_parts.append(f"Detected {repository_count} repository interfaces extending Spring Data interfaces.")
        if raw_sql_concats:
            desc_parts.append(f"Detected {raw_sql_concat_count} occurrences of potential raw SQL concatenation (high SQL-injection risk).")

        description = " ".join(desc_parts)

        # Build evidence
        evidence = []
        # Add repository interface evidence
        for rel_path, line, _ in repo_interfaces[:2]:
            ev = make_evidence(index, rel_path, line, radius=3)
            if ev:
                evidence.append(ev)
        # Add library import evidence
        for lib in libs_list:
            if len(evidence) >= ctx.max_evidence_snippets:
                break
            hits = library_hits.get(lib)
            if hits and hits.examples:
                rel_path, line = hits.examples[0]
                ev = make_evidence(index, rel_path, line, radius=3)
                if ev:
                    evidence.append(ev)

        stats: dict[str, object] = {
            "libraries": libs_list,
            "driver": driver,
            "migration_tool": migration_tool,
            "has_repository_pattern": repository_count > 0,
            "repository_count": repository_count,
            "raw_sql_concat_count": raw_sql_concat_count,
        }


        result.rules.append(self.make_rule(
            rule_id="java.conventions.database",
            category="database",
            title=title,
            description=description,
            confidence=0.8,
            language="java",
            evidence=evidence,
            stats=stats,
        ))

        return result
