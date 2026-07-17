"""Kotlin web framework and HTTP routing conventions detector."""

from __future__ import annotations

import re
from typing import Optional

from ..base import DetectorContext, DetectorResult
from ..jvm.build import BuildInfo
from ..registry import DetectorRegistry
from .base import KotlinDetector
from .index import KotlinIndex, make_evidence

# Single-marker-import server frameworks -- one substring is enough signal.
SERVER_IMPORT_SIGNALS: dict[str, tuple[str, ...]] = {
    "http4k": ("org.http4k",),
    "javalin": ("io.javalin",),
    "vertx": ("io.vertx",),
    "micronaut": ("io.micronaut",),
    "quarkus": ("io.quarkus",),
}

# HTTP-client-only libraries -- present alongside or instead of a server framework.
CLIENT_IMPORT_SIGNALS: dict[str, tuple[str, ...]] = {
    "retrofit": ("retrofit2",),
    "ktor-client": ("io.ktor.client",),
}

SPRING_ANNOTATIONS = (
    "RestController", "Controller", "RequestMapping", "GetMapping", "PostMapping",
    "PutMapping", "DeleteMapping", "PatchMapping", "PathVariable", "RequestBody",
    "RequestParam",
)
WEBFLUX_PATTERNS = (r"\bMono\s*<", r"\bFlux\s*<", r"coRouter\s*\{")

KTOR_SERVER_PATTERNS = (
    r"routing\s*\{", r"\broute\s*\(", r"\binstall\s*\(", r"call\.respond", r"call\.receive",
)
KTOR_ROUTE_METHODS = ("get", "post", "put", "delete", "patch")

SPRING_METHOD_ANNOTATIONS: dict[str, str] = {
    "GetMapping": "GET",
    "PostMapping": "POST",
    "PutMapping": "PUT",
    "DeleteMapping": "DELETE",
    "PatchMapping": "PATCH",
}

VALIDATION_ANNOTATIONS = ("Valid", "Validated")
ERROR_HANDLER_ANNOTATIONS = ("ExceptionHandler", "ControllerAdvice", "RestControllerAdvice")
OPENAPI_SIGNALS = ("springdoc", "swagger", "Operation", "ApiResponse")

FRAMEWORK_DISPLAY_NAMES: dict[str, str] = {
    "spring-mvc": "Spring MVC",
    "spring-webflux": "Spring WebFlux",
    "ktor": "Ktor",
    "http4k": "http4k",
    "javalin": "Javalin",
    "vertx": "Vert.x",
    "micronaut": "Micronaut",
    "quarkus": "Quarkus",
    "retrofit": "Retrofit",
    "ktor-client": "Ktor Client",
    "none": "none",
}

# @GetMapping("/users") / @RequestMapping("/api/v1"); `value =` prefix is optional.
SPRING_ROUTE_PATTERN = re.compile(
    r'@(GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping|RequestMapping)'
    r'\s*\(\s*(?:value\s*=\s*)?"([^"]*)"'
)
VERSION_PATTERN = re.compile(r"/v\d+(?:[/.]|$)")

# Priority order used to pick the "primary" framework when several are present.
FRAMEWORK_PRIORITY = (
    "spring-mvc", "spring-webflux", "ktor", "http4k", "javalin",
    "vertx", "micronaut", "quarkus", "retrofit", "ktor-client",
)


class _Signal:
    """Accumulated hit count and example locations for one framework."""

    def __init__(self) -> None:
        self.hits = 0
        self.examples: list[tuple[str, int]] = []

    def add(self, rel_path: str, line: int) -> None:
        self.hits += 1
        if len(self.examples) < 5:
            self.examples.append((rel_path, line))


@DetectorRegistry.register
class KotlinWebDetector(KotlinDetector):
    """Detect Kotlin web framework and HTTP routing conventions."""

    name = "kotlin_web"
    description = "Detects Kotlin web framework and HTTP routing conventions"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect web framework conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        build_info = self.get_build_info(ctx)
        server_signals, client_signals = self._collect_framework_signals(index, build_info)

        if not server_signals and not client_signals:
            return result

        is_client_only = not server_signals
        signals = client_signals if is_client_only else server_signals

        primary = next(
            (fw for fw in FRAMEWORK_PRIORITY if fw in signals),
            next(iter(signals)),
        )
        frameworks = list(signals.keys())

        routes, http_methods, route_locations, route_count = self._extract_routes(
            ctx, index, server_signals
        )
        example_routes = list(dict.fromkeys(path for _method, path in routes))[:20]
        uses_versioning = any(VERSION_PATTERN.search(path) for _method, path in routes)

        suspend_handler_count = sum(
            1
            for file_idx in index.get_files_by_role("api")
            for fn in file_idx.functions
            if fn.is_suspend
        )

        uses_validation, validation_examples = self._detect_validation(index)
        has_error_handler, error_examples = self._detect_error_handling(index)
        patterns = self._detect_extra_patterns(index)

        if uses_validation:
            patterns.append("request validation")
        if has_error_handler:
            patterns.append("centralized error handling")
        if suspend_handler_count:
            patterns.append("suspend handlers")
        if uses_versioning:
            patterns.append("path-based API versioning")

        display_name = FRAMEWORK_DISPLAY_NAMES.get(primary, primary)

        if is_client_only:
            title = f"Web: {display_name} (HTTP client)"
            description = f"Uses {display_name} as an HTTP client; no server-side routing found."
        else:
            title = f"Web: {display_name}"
            if route_count:
                title += f" with {route_count} REST route{'s' if route_count != 1 else ''}"
                prefix = _common_prefix(example_routes)
                if prefix:
                    title += f" under {prefix}"
            description = f"Uses {display_name} for HTTP routing."
            if len(frameworks) > 1:
                others = [FRAMEWORK_DISPLAY_NAMES.get(fw, fw) for fw in frameworks if fw != primary]
                description += f" Also present: {', '.join(others)}."
            if http_methods:
                methods_str = ", ".join(f"{k}: {v}" for k, v in sorted(http_methods.items()))
                description += f" Methods -- {methods_str}."
            if uses_versioning:
                description += " API paths carry an explicit version segment (e.g. /v1)."
            if uses_validation:
                description += " Uses request validation annotations."
            if has_error_handler:
                description += " Has centralized exception handling."
            if suspend_handler_count:
                description += f" {suspend_handler_count} suspend handler function(s)."

        total_hits = sum(s.hits for s in signals.values())
        confidence = 0.35 + min(0.3, 0.02 * total_hits)
        if route_count:
            confidence += 0.15
        if len(frameworks) == 1:
            confidence += 0.05
        confidence = min(0.95, confidence)

        evidence = []
        seen: set[tuple[str, int]] = set()
        combined_examples = (
            list(signals[primary].examples)
            + route_locations
            + validation_examples[:3]
            + error_examples[:3]
        )
        for rel_path, line in combined_examples:
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
            rule_id="kotlin.conventions.web_framework",
            category="api",
            title=title,
            description=description,
            confidence=confidence,
            language="kotlin",
            evidence=evidence,
            stats={
                "framework": primary,
                # CLAUDE.md's tech-stack renderer reads `primary_framework` for
                # web_framework rules.
                "primary_framework": primary,
                "frameworks": frameworks,
                "route_count": route_count,
                "example_routes": example_routes,
                "http_methods": http_methods,
                "uses_versioning": uses_versioning,
                "uses_validation": uses_validation,
                "has_error_handler": has_error_handler,
                "suspend_handler_count": suspend_handler_count,
                "patterns": patterns,
                "is_client_only": is_client_only,
            },
        ))

        # 2. API Routes
        api_routes: list[dict[str, object]] = []
        api_methods: dict[str, int] = {}

        for rel_path, file_idx in index.files.items():
            if file_idx.role == "test":
                continue
            content = "\n".join(file_idx.lines)

            # Spring mapping annotations
            spring_pattern = re.compile(r'@(GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping|RequestMapping)\s*\(\s*(?:value\s*=\s*)?["\']([^"\']+)["\']')
            for match in spring_pattern.finditer(content):
                ann = match.group(1)
                path = match.group(2)
                method = "ANY"
                if ann == "GetMapping":
                    method = "GET"
                elif ann == "PostMapping":
                    method = "POST"
                elif ann == "PutMapping":
                    method = "PUT"
                elif ann == "DeleteMapping":
                    method = "DELETE"
                elif ann == "PatchMapping":
                    method = "PATCH"

                line = content[:match.start()].count("\n") + 1
                api_methods[method] = api_methods.get(method, 0) + 1
                api_routes.append({
                    "method": method,
                    "path": path,
                    "file": rel_path,
                    "line": line,
                })
                if len(api_routes) >= 100:
                    break

            # Ktor routing (e.g. get("/path") or post("/path"))
            ktor_pattern = re.compile(r'\b(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']')
            for match in ktor_pattern.finditer(content):
                method = match.group(1).upper()
                path = match.group(2)
                line = content[:match.start()].count("\n") + 1
                api_methods[method] = api_methods.get(method, 0) + 1
                api_routes.append({
                    "method": method,
                    "path": path,
                    "file": rel_path,
                    "line": line,
                })
                if len(api_routes) >= 100:
                    break

            if len(api_routes) >= 100:
                break

        if api_routes:
            description = (
                f"{len(api_routes)} API routes detected. "
                f"Methods: {', '.join(f'{k}: {v}' for k, v in sorted(api_methods.items()))}."
            )
            result.rules.append(self.make_rule(
                rule_id="kotlin.conventions.api_routes",
                category="api",
                title="API routes",
                description=description,
                confidence=0.85,
                language="kotlin",
                evidence=[],
                stats={
                    "routes": api_routes,
                    "total_routes": len(api_routes),
                    "methods": api_methods,
                },
            ))

        return result

    def _collect_framework_signals(
        self,
        index: KotlinIndex,
        build_info: BuildInfo,
    ) -> tuple[dict[str, _Signal], dict[str, _Signal]]:
        """Gather per-framework hit counts and example locations.

        Returns (server_signals, client_signals). Spring MVC and Spring WebFlux
        share detection (both are driven by the same annotation set) until a
        WebFlux-specific signal (Mono/Flux/coRouter/reactor.core) is seen, at
        which point the accumulated signal is promoted to "spring-webflux".
        """
        server_signals: dict[str, _Signal] = {}
        client_signals: dict[str, _Signal] = {}

        for annotation_name in SPRING_ANNOTATIONS:
            for rel_path, line in index.find_annotation(annotation_name, limit=50):
                server_signals.setdefault("spring-mvc", _Signal()).add(rel_path, line)

        if "spring-mvc" in server_signals:
            is_webflux = index.count_imports_matching("reactor.core") > 0
            for pattern in WEBFLUX_PATTERNS:
                matches = index.search_pattern(pattern, limit=20)
                if matches:
                    is_webflux = True
                    for rel_path, line, _match in matches[:5]:
                        server_signals["spring-mvc"].add(rel_path, line)
            if is_webflux:
                server_signals["spring-webflux"] = server_signals.pop("spring-mvc")

        if build_info.has_dependency("spring-boot-starter-webflux"):
            server_signals.setdefault("spring-webflux", _Signal())
        elif build_info.has_dependency("spring-boot-starter-web"):
            server_signals.setdefault("spring-mvc", _Signal())

        # Ktor's routing DSL verbs are ordinary identifiers: `route(` and
        # `install(` appear in any networking code (okhttp has its own `route(`
        # and calls `Provider.install()`). Only read them as Ktor when Ktor is
        # actually imported or depended on.
        ktor_dependency = build_info.has_dependency("ktor-server")
        if index.count_imports_matching("io.ktor.server") > 0 or ktor_dependency:
            for rel_path, _import_path, line in index.find_imports_matching(
                "io.ktor.server", limit=50
            ):
                server_signals.setdefault("ktor", _Signal()).add(rel_path, line)
            for pattern in KTOR_SERVER_PATTERNS:
                for rel_path, line, _match in index.search_pattern(pattern, limit=20):
                    server_signals.setdefault("ktor", _Signal()).add(rel_path, line)
            if ktor_dependency:
                server_signals.setdefault("ktor", _Signal())

        for name, needles in SERVER_IMPORT_SIGNALS.items():
            for needle in needles:
                for rel_path, _import_path, line in index.find_imports_matching(needle, limit=30):
                    server_signals.setdefault(name, _Signal()).add(rel_path, line)
            if build_info.has_dependency(name):
                server_signals.setdefault(name, _Signal())

        for name, needles in CLIENT_IMPORT_SIGNALS.items():
            for needle in needles:
                for rel_path, _import_path, line in index.find_imports_matching(needle, limit=30):
                    client_signals.setdefault(name, _Signal()).add(rel_path, line)
        if build_info.has_dependency("retrofit2"):
            client_signals.setdefault("retrofit", _Signal())

        return server_signals, client_signals

    def _extract_routes(
        self,
        ctx: DetectorContext,
        index: KotlinIndex,
        server_signals: dict[str, _Signal],
    ) -> tuple[list[tuple[str, str]], dict[str, int], list[tuple[str, int]], int]:
        """Extract (method, path) routes from Spring/Ktor route declarations.

        Returns (routes, http_methods, evidence_locations, route_count). `routes`
        and `http_methods` are capped (they only feed example/breakdown display),
        but `route_count` is tallied across every match so it never saturates on
        large repos -- see the module docstring context around search_pattern.
        """
        routes: list[tuple[str, str]] = []
        http_methods: dict[str, int] = {}
        locations: list[tuple[str, int]] = []
        route_count = 0

        use_spring = "spring-mvc" in server_signals or "spring-webflux" in server_signals
        use_ktor = "ktor" in server_signals
        if not use_spring and not use_ktor:
            return routes, http_methods, locations, route_count

        ktor_route_pattern = re.compile(
            r'\b(' + "|".join(KTOR_ROUTE_METHODS) + r')\s*\(\s*"([^"]*)"'
        )

        for rel_path, file_idx in index.files.items():
            if file_idx.is_test:
                continue
            content = "\n".join(file_idx.lines)

            if use_spring:
                for m in SPRING_ROUTE_PATTERN.finditer(content):
                    annotation, path = m.group(1), m.group(2)
                    if not path:
                        continue
                    route_count += 1
                    line = content[: m.start()].count("\n") + 1
                    method = SPRING_METHOD_ANNOTATIONS.get(annotation)
                    if method:
                        http_methods[method] = http_methods.get(method, 0) + 1
                    if len(routes) < 200:
                        routes.append((method or "ANY", path))
                    if len(locations) < ctx.max_evidence_snippets:
                        locations.append((rel_path, line))

            if use_ktor:
                for m in ktor_route_pattern.finditer(content):
                    method, path = m.group(1).upper(), m.group(2)
                    route_count += 1
                    line = content[: m.start()].count("\n") + 1
                    http_methods[method] = http_methods.get(method, 0) + 1
                    if len(routes) < 200:
                        routes.append((method, path))
                    if len(locations) < ctx.max_evidence_snippets:
                        locations.append((rel_path, line))

        return routes, http_methods, locations, route_count

    def _detect_validation(self, index: KotlinIndex) -> tuple[bool, list[tuple[str, int]]]:
        """Detect request validation annotations (Bean Validation / jakarta / javax)."""
        examples: list[tuple[str, int]] = []
        for annotation_name in VALIDATION_ANNOTATIONS:
            examples.extend(index.find_annotation(annotation_name, limit=10))
        uses_validation = bool(examples) or index.count_imports_matching(".validation.") > 0
        return uses_validation, examples

    def _detect_error_handling(self, index: KotlinIndex) -> tuple[bool, list[tuple[str, int]]]:
        """Detect centralized error-handling constructs."""
        examples: list[tuple[str, int]] = []
        for annotation_name in ERROR_HANDLER_ANNOTATIONS:
            examples.extend(index.find_annotation(annotation_name, limit=10))
        status_pages = index.search_pattern(r"StatusPages", limit=10)
        examples.extend((rel_path, line) for rel_path, line, _match in status_pages)
        return bool(examples), examples

    def _detect_extra_patterns(self, index: KotlinIndex) -> list[str]:
        """Detect serialization wiring and OpenAPI/Swagger documentation signals."""
        patterns: list[str] = []
        if index.search_pattern(r"install\s*\(\s*ContentNegotiation", limit=5):
            patterns.append("ContentNegotiation")
        if index.count_annotation("ResponseBody"):
            patterns.append("@ResponseBody")

        openapi_hits = 0
        for needle in OPENAPI_SIGNALS:
            openapi_hits += index.count_imports_matching(needle)
            openapi_hits += index.count_annotation(needle)
        if openapi_hits:
            patterns.append("OpenAPI/Swagger")

        return patterns


def _common_prefix(paths: list[str]) -> Optional[str]:
    """Return the most common two-segment path prefix, if any repeats."""
    prefix_counts: dict[str, int] = {}
    for path in paths:
        parts = path.strip("/").split("/")
        if not parts or not parts[0]:
            continue
        prefix = "/" + "/".join(parts[:2]) if len(parts) >= 2 else "/" + parts[0]
        prefix_counts[prefix] = prefix_counts.get(prefix, 0) + 1

    if not prefix_counts:
        return None
    best_prefix, best_count = max(prefix_counts.items(), key=lambda kv: kv[1])
    return best_prefix if best_count > 1 else None
