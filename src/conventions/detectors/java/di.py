"""Java dependency injection conventions detector."""

from __future__ import annotations

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import JavaDetector
from .index import make_evidence

SPRING_STEREOTYPES = ("Component", "Service", "Repository", "Controller", "RestController", "Configuration")


@DetectorRegistry.register
class JavaDIDetector(JavaDetector):
    """Detect Java dependency injection frameworks and conventions."""

    name = "java_di"
    description = "Detects Java dependency injection frameworks and conventions"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect dependency injection conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        build_info = self.get_build_info(ctx)

        # 1. Framework detection based on imports and dependencies
        di_frameworks: set[str] = set()

        spring_imports = index.count_imports_matching("org.springframework")
        jakarta_inject_imports = index.count_imports_matching("jakarta.inject") or index.count_imports_matching("javax.inject")
        guice_imports = index.count_imports_matching("com.google.inject")
        dagger_imports = index.count_imports_matching("dagger")

        if spring_imports > 0 or build_info.has_dependency("spring"):
            di_frameworks.add("Spring DI")
        # Match the JSR-330 coordinates precisely: `has_dependency` is a substring
        # test, so a needle of "inject" also matches unrelated artifacts such as
        # com.google.testparameterinjector:test-parameter-injector.
        if (
            jakarta_inject_imports > 0
            or build_info.has_dependency("javax.inject")
            or build_info.has_dependency("jakarta.inject")
            or build_info.has_dependency("cdi-api")
        ):
            di_frameworks.add("CDI (JSR-330)")
        if guice_imports > 0 or build_info.has_dependency("guice"):
            di_frameworks.add("Guice")
        if dagger_imports > 0 or build_info.has_dependency("dagger"):
            di_frameworks.add("Dagger")

        if not di_frameworks:
            return result

        # 2. Injection styles detection
        # Field Injection: @Autowired / @Inject on fields (no parenthesis parameters, followed by field definition)
        field_inject_patterns = [
            r"@(Autowired|Inject)\s+(?:private|protected|public)?\s+\w+\s+\w+;",
            r"@(Autowired|Inject)\s*\n\s*(?:private|protected|public)?\s+\w+\s+\w+;"
        ]
        field_inject_hits = sum(index.count_pattern(p, exclude_tests=True) for p in field_inject_patterns)

        # Constructor Injection: Constructor annotated with @Inject/@Autowired, or Spring class with final fields and a constructor
        constructor_inject_annotated = index.count_pattern(r"@Autowired\s+(?:public|private|protected)?\s+\w+\s*\(", exclude_tests=True) + \
                                      index.count_pattern(r"@Inject\s+(?:public|private|protected)?\s+\w+\s*\(", exclude_tests=True)

        # Setter Injection: @Autowired / @Inject on methods
        setter_inject_patterns = [
            r"@(Autowired|Inject)\s+(?:public|protected|private)?\s+void\s+set\w+\(",
            r"@(Autowired|Inject)\s*\n\s*(?:public|protected|private)?\s+void\s+set\w+\("
        ]
        setter_inject_hits = sum(index.count_pattern(p, exclude_tests=True) for p in setter_inject_patterns)

        # Infer primary injection style
        total_signals = field_inject_hits + constructor_inject_annotated + setter_inject_hits
        primary_style = "constructor"

        if total_signals > 0:
            if field_inject_hits > constructor_inject_annotated and field_inject_hits > setter_inject_hits:
                primary_style = "field"
            elif setter_inject_hits > constructor_inject_annotated and setter_inject_hits > field_inject_hits:
                primary_style = "setter"
        else:
            # Check for Lombok @RequiredArgsConstructor which generates constructor injection implicitly for final fields
            lombok_constructor_injects = index.count_annotation("RequiredArgsConstructor") + index.count_annotation("AllArgsConstructor")
            if lombok_constructor_injects > 0:
                primary_style = "constructor (Lombok)"

        # 3. Compile title, description and stats
        frameworks_str = "/".join(sorted(di_frameworks))
        title = f"Dependency Injection: {frameworks_str} ({primary_style} injection)"

        desc_parts = [f"Uses {frameworks_str} as the primary dependency injection framework."]
        if primary_style.startswith("constructor"):
            desc_parts.append("Constructor injection is preferred and used consistently.")
        elif primary_style == "field":
            desc_parts.append("Field injection (using @Autowired/@Inject directly on variables) is commonly used.")
        elif primary_style == "setter":
            desc_parts.append("Setter injection is used for wiring dependencies.")

        if field_inject_hits > 0 and primary_style.startswith("constructor"):
            desc_parts.append(f"Found {field_inject_hits} instances of field injection (potential mixed style).")

        description = " ".join(desc_parts)

        # Build evidence
        evidence = []
        # Find some autowired/inject lines
        for pattern in field_inject_patterns + setter_inject_patterns:
            sites = index.search_pattern(pattern, exclude_tests=True, limit=2)
            for rel_path, line, _ in sites:
                ev = make_evidence(index, rel_path, line, radius=3)
                if ev:
                    evidence.append(ev)
            if len(evidence) >= ctx.max_evidence_snippets:
                break

        stats = {
            "frameworks": list(di_frameworks),
            "primary_style": primary_style,
            "field_injection_count": field_inject_hits,
            "setter_injection_count": setter_inject_hits,
            "constructor_annotation_count": constructor_inject_annotated,
        }

        result.rules.append(self.make_rule(
            rule_id="java.conventions.di",
            category="dependency_injection",
            title=title,
            description=description,
            confidence=0.8,
            language="java",
            evidence=evidence,
            stats=stats,
        ))

        return result
