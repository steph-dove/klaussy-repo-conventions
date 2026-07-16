"""Kotlin dependency injection conventions detector."""

from __future__ import annotations

import re

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import KotlinDetector
from .index import KotlinClass, KotlinFileIndex, KotlinIndex, make_evidence

# Spring stereotype annotations that mark a class as a container-managed bean.
SPRING_STEREOTYPES = ("Component", "Service", "Repository", "Controller", "RestController", "Configuration")
# Spring wiring annotations that indicate injection points/factories rather than beans.
SPRING_WIRING_ANNOTATIONS = ("Autowired", "Qualifier", "Value", "Bean")

# Hilt-specific annotations (unambiguous: Dagger alone never defines these).
HILT_ONLY_ANNOTATIONS = ("HiltAndroidApp", "AndroidEntryPoint", "HiltViewModel")
# Annotations shared by Dagger and Hilt; disambiguated per-file via imports.
DAGGER_HILT_SHARED_ANNOTATIONS = ("Module", "InstallIn", "Inject", "Provides", "Binds")
DAGGER_ONLY_ANNOTATIONS = ("Component", "Subcomponent")

# Koin DSL declarations. The `(?<![.\w])` guard keeps these off method calls:
# `certificates.single()` is Kotlin's stdlib single(), not a Koin definition.
KOIN_MODULE_RE = r"(?<![.\w])module\s*\{"
KOIN_SINGLE_RE = r"(?<![.\w])single\s*[<({]"
KOIN_FACTORY_RE = r"(?<![.\w])factory\s*[<({]"
KOIN_VIEWMODEL_RE = r"(?<![.\w])viewModel\s*[<({]"
KOIN_BY_INJECT_RE = r"\bby\s+inject\s*\("
KOIN_START_RE = r"(?<![.\w])startKoin\s*\{"

INJECT_CONSTRUCTOR_RE = r"@Inject\s+constructor\s*\("

FIELD_INJECT_PROPERTY_RE = re.compile(r"(?:lateinit\s+var|val|var)\s+\w+\s*:")

# Manual constructor injection: a class whose primary constructor accepts a
# val/var parameter typed as a conventionally-named collaborator, with no DI
# framework annotation involved. Naive single-line heuristic (constructors
# spanning multiple lines are not matched), which is an acceptable trade-off
# for a low-confidence fallback signal.
MANUAL_DI_RE = (
    r"class\s+\w+\s*\([^)]*(?:private\s+)?(?:val|var)\s+\w+\s*:\s*\w*"
    r"(?:Service|Repository|Manager|Client|UseCase|Provider|Factory|Gateway|Dao|Store)\b[^)]*\)"
)


def _file_framework_tags(file_idx: KotlinFileIndex) -> set[str]:
    """Infer which DI frameworks a file's imports point at.

    Hilt modules routinely import Dagger's own `@Module`/`@Provides`/`@Binds`
    directly (there is no Hilt-specific package for them) alongside a
    `dagger.hilt.*` import, so a file is only attributed to plain Dagger when
    it shows no Hilt signal at all — otherwise every Hilt file would also be
    misreported as "also uses Dagger".
    """
    tags: set[str] = set()
    for import_path, _ in file_idx.imports:
        if import_path.startswith("org.springframework"):
            tags.add("spring")
        elif import_path.startswith("org.koin"):
            tags.add("koin")
        elif import_path.startswith("dagger.hilt"):
            tags.add("hilt")
        elif import_path.startswith("dagger"):
            tags.add("dagger")
        elif import_path.startswith("me.tatarka.inject"):
            tags.add("kotlin-inject")
        elif import_path.startswith("org.kodein"):
            tags.add("kodein")
    if "hilt" in tags:
        tags.discard("dagger")
    return tags


def _count_annotation_tagged(
    index: KotlinIndex,
    name: str,
    file_tags: dict[str, set[str]],
    tag: str,
) -> int:
    """Count annotation `name` usages restricted to files tagged with `tag`.

    `find_annotation(limit=N)` would saturate at N on large repos; this scans
    each file's already-parsed (unlimited) annotation list directly instead.
    """
    return sum(
        sum(1 for annotation, _ in file_idx.annotations if annotation == name)
        for rel_path, file_idx in index.files.items()
        if tag in file_tags.get(rel_path, set())
    )


def _constructor_param_text(file_idx: KotlinFileIndex, class_line: int) -> str:
    """Best-effort extraction of a class's primary constructor parameter list."""
    lines = file_idx.lines
    if class_line - 1 >= len(lines) or class_line < 1:
        return ""
    snippet = "\n".join(lines[class_line - 1 : class_line + 4])
    match = re.search(r"class\s+\w+\s*(?:<[^>]+>)?\s*\(([^)]*)\)", snippet, re.DOTALL)
    return match.group(1).strip() if match else ""


def _field_injection_hits(index: KotlinIndex) -> list[tuple[str, int]]:
    """Find @Autowired/@Inject annotations sitting directly on a var/val property.

    Scans forward from the annotation's line, skipping over any other stacked
    annotation lines (e.g. a `@Qualifier` between `@Autowired` and the
    property), until it finds the property declaration or gives up.
    """
    hits: list[tuple[str, int]] = []
    seen: set[tuple[str, int]] = set()
    for annotation_name in ("Autowired", "Inject"):
        # Scan every file's already-parsed (unlimited) annotation list directly
        # rather than `find_annotation(limit=N)`, which would silently cap this
        # count on large repos.
        for rel_path, file_idx in index.files.items():
            lines = file_idx.lines
            for annotation, line in file_idx.annotations:
                if annotation != annotation_name:
                    continue
                idx = max(0, line - 1)
                while idx < len(lines):
                    text = lines[idx]
                    if "constructor(" in text:
                        # The annotation decorates a constructor, not a field —
                        # e.g. `@Inject constructor(private val repo: Repo)` would
                        # otherwise false-positive on the `val repo:` fragment.
                        break
                    if FIELD_INJECT_PROPERTY_RE.search(text):
                        key = (rel_path, line)
                        if key not in seen:
                            seen.add(key)
                            hits.append(key)
                        break
                    stripped = text.strip()
                    if idx > line - 1 and stripped and not stripped.startswith("@"):
                        break
                    idx += 1
    return hits


@DetectorRegistry.register
class KotlinDIDetector(KotlinDetector):
    """Detect Kotlin dependency injection framework and wiring conventions."""

    name = "kotlin_dependency_injection"
    description = "Detects Kotlin dependency injection framework and wiring conventions"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect DI framework usage and injection style."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        build_info = self.get_build_info(ctx)
        file_tags = {rel_path: _file_framework_tags(f) for rel_path, f in index.files.items()}

        def tagged(rel_path: str, tag: str) -> bool:
            return tag in file_tags.get(rel_path, set())

        patterns: list[str] = []
        evidence_sites: list[tuple[str, int]] = []
        field_injection_sites: list[tuple[str, int]] = []

        # --- Spring -----------------------------------------------------------
        spring_import_count = index.count_imports_matching("org.springframework")

        stereotype_counts: dict[str, int] = {}
        spring_stereotype_classes: list[tuple[str, KotlinClass]] = []
        for rel_path, cls in index.all_classes():
            if not tagged(rel_path, "spring"):
                continue
            hit = next((a for a in cls.annotations if a in SPRING_STEREOTYPES), None)
            if hit is None:
                continue
            stereotype_counts[hit] = stereotype_counts.get(hit, 0) + 1
            spring_stereotype_classes.append((rel_path, cls))
            evidence_sites.append((rel_path, cls.line))

        autowired_hits = [
            (r, ln) for r, ln in index.find_annotation("Autowired", limit=200)
        ]
        qualifier_count = sum(
            1 for r, _ in index.find_annotation("Qualifier", limit=200) if tagged(r, "spring")
        )
        value_count = sum(
            1 for r, _ in index.find_annotation("Value", limit=200) if tagged(r, "spring")
        )
        # `bean_hits` is capped small and used only to gather evidence sites; the
        # displayed count comes from the unlimited `bean_count` below.
        bean_hits = [
            (r, ln) for r, ln in index.find_annotation("Bean", limit=10) if tagged(r, "spring")
        ]
        bean_count = _count_annotation_tagged(index, "Bean", file_tags, "spring")

        spring_constructor_classes = [
            (r, cls) for r, cls in spring_stereotype_classes
            if _constructor_param_text(index.files[r], cls.line)
        ]
        spring_field_injected = [(r, ln) for r, ln in autowired_hits if tagged(r, "spring")]

        spring_signal = (
            spring_import_count + sum(stereotype_counts.values())
            + len(spring_field_injected) + qualifier_count + value_count + bean_count
        )
        if spring_signal:
            patterns.append("spring")
            if stereotype_counts:
                patterns.append("spring-stereotypes")
            if bean_count:
                patterns.append("bean-factory-methods")
            evidence_sites.extend(bean_hits[:3])

        # --- Koin ---------------------------------------------------------------
        # Counts below use count_pattern (unlimited) rather than
        # len(search_pattern(..., limit=N)); small-limit searches further down
        # gather a few example sites only.
        # Koin's DSL keywords are ordinary Kotlin words: `single` and `factory`
        # are also stdlib/collection idioms (`certificates.single()`), and
        # `module {` is generic. Attributing them without confirming Koin is
        # actually present flags any codebase that calls `.single()` as using
        # Koin, so the DSL only counts when Koin is imported or depended on.
        koin_import_count = index.count_imports_matching("org.koin")
        koin_present = koin_import_count > 0 or build_info.has_dependency("koin")

        if koin_present:
            koin_module_count = index.count_pattern(KOIN_MODULE_RE, exclude_tests=True)
            koin_single_count = index.count_pattern(KOIN_SINGLE_RE, exclude_tests=True)
            koin_factory_count = index.count_pattern(KOIN_FACTORY_RE, exclude_tests=True)
            koin_viewmodel_count = index.count_pattern(KOIN_VIEWMODEL_RE, exclude_tests=True)
            koin_inject_count = index.count_pattern(KOIN_BY_INJECT_RE, exclude_tests=True)
            koin_start_count = index.count_pattern(KOIN_START_RE, exclude_tests=True)
        else:
            koin_module_count = koin_single_count = koin_factory_count = 0
            koin_viewmodel_count = koin_inject_count = koin_start_count = 0

        koin_component_count = koin_single_count + koin_factory_count + koin_viewmodel_count

        koin_signal = (
            koin_import_count + koin_module_count + koin_component_count
            + koin_inject_count + koin_start_count
        )
        if koin_signal:
            patterns.append("koin")
            koin_module_examples = index.search_pattern(KOIN_MODULE_RE, limit=3, exclude_tests=True)
            koin_start_examples = index.search_pattern(KOIN_START_RE, limit=3, exclude_tests=True)
            evidence_sites.extend(
                (r, ln) for r, ln, _ in (koin_module_examples + koin_start_examples)[:3]
            )

        # --- Hilt / Dagger --------------------------------------------------------
        hilt_import_count = index.count_imports_matching("dagger.hilt")
        # Unlimited: scans imports directly instead of find_imports_matching(limit=N).
        dagger_import_count = sum(
            1
            for rel_path, file_idx in index.files.items()
            if tagged(rel_path, "dagger")
            for imp, _ in file_idx.imports
            if "dagger" in imp and "dagger.hilt" not in imp
        )

        # Unlimited counts via count_annotation / _count_annotation_tagged; small
        # -limit find_annotation calls further down gather example sites only.
        hilt_only_count = sum(index.count_annotation(name) for name in HILT_ONLY_ANNOTATIONS)
        hilt_shared_count = sum(
            _count_annotation_tagged(index, name, file_tags, "hilt")
            for name in DAGGER_HILT_SHARED_ANNOTATIONS
        )
        dagger_shared_count = sum(
            _count_annotation_tagged(index, name, file_tags, "dagger")
            for name in DAGGER_HILT_SHARED_ANNOTATIONS
        )
        dagger_only_count = sum(
            _count_annotation_tagged(index, name, file_tags, "dagger")
            for name in DAGGER_ONLY_ANNOTATIONS
        )

        inject_constructor_count = index.count_pattern(INJECT_CONSTRUCTOR_RE, exclude_tests=True)
        hilt_module_count = _count_annotation_tagged(index, "Module", file_tags, "hilt")
        dagger_module_count = _count_annotation_tagged(index, "Module", file_tags, "dagger")

        hilt_signal = hilt_import_count + hilt_only_count + hilt_shared_count
        dagger_signal = dagger_import_count + dagger_shared_count + dagger_only_count

        if hilt_signal:
            patterns.append("hilt")
            hilt_only_examples = [
                (r, ln)
                for name in HILT_ONLY_ANNOTATIONS
                for r, ln in index.find_annotation(name, limit=3)
            ]
            evidence_sites.extend(hilt_only_examples[:3])
        if dagger_signal:
            patterns.append("dagger")
            dagger_only_examples = [
                (r, ln)
                for name in DAGGER_ONLY_ANNOTATIONS
                for r, ln in index.find_annotation(name, limit=3)
                if tagged(r, "dagger")
            ]
            evidence_sites.extend(dagger_only_examples[:3])
        if inject_constructor_count:
            patterns.append("inject-constructor")
            inject_constructor_examples = index.search_pattern(
                INJECT_CONSTRUCTOR_RE, limit=3, exclude_tests=True
            )
            evidence_sites.extend((r, ln) for r, ln, _ in inject_constructor_examples)

        # --- kotlin-inject / Kodein -----------------------------------------------
        kotlin_inject_import_count = index.count_imports_matching("me.tatarka.inject")
        kodein_import_count = index.count_imports_matching("org.kodein")
        if kotlin_inject_import_count:
            patterns.append("kotlin-inject")
        if kodein_import_count:
            patterns.append("kodein")

        # --- Field injection (anti-pattern) ----------------------------------------
        field_injection_sites = _field_injection_hits(index)
        field_injection_count = len(field_injection_sites)
        if field_injection_count:
            patterns.append("field-injection")

        # --- Manual constructor injection (no framework) -----------------------------
        # Unlimited count; no evidence is gathered from this signal elsewhere.
        manual_signal = index.count_pattern(MANUAL_DI_RE, exclude_tests=True)

        # --- Choose the primary framework by strength of signal ----------------------
        framework_signals: dict[str, int] = {}
        if spring_signal:
            framework_signals["spring"] = spring_signal
        if koin_signal:
            framework_signals["koin"] = koin_signal
        if hilt_signal:
            framework_signals["hilt"] = hilt_signal
        if dagger_signal:
            framework_signals["dagger"] = dagger_signal
        if kotlin_inject_import_count:
            framework_signals["kotlin-inject"] = kotlin_inject_import_count
        if kodein_import_count:
            framework_signals["kodein"] = kodein_import_count

        if not framework_signals:
            if manual_signal:
                framework_signals["manual"] = manual_signal
                patterns.append("manual-constructor-injection")
            elif field_injection_count:
                # No framework identified, but field injection was found on its own
                # (e.g. a bare @Inject with no importable framework signal).
                framework_signals["manual"] = field_injection_count
            else:
                return result

        primary = max(framework_signals, key=lambda k: framework_signals[k])
        frameworks = sorted(framework_signals, key=lambda k: -framework_signals[k])

        # --- Component / module counts for the primary framework ---------------------
        if primary == "spring":
            injected_component_count = sum(stereotype_counts.values())
            constructor_injection_count = len(spring_constructor_classes) + manual_signal
            module_count = stereotype_counts.get("Configuration", 0)
        elif primary == "koin":
            injected_component_count = koin_component_count
            constructor_injection_count = koin_component_count
            module_count = koin_module_count
        elif primary == "hilt":
            injected_component_count = hilt_only_count + inject_constructor_count
            constructor_injection_count = inject_constructor_count
            module_count = hilt_module_count
        elif primary == "dagger":
            injected_component_count = dagger_only_count + inject_constructor_count
            constructor_injection_count = inject_constructor_count
            module_count = dagger_module_count
        elif primary in ("kotlin-inject", "kodein"):
            injected_component_count = framework_signals[primary]
            constructor_injection_count = manual_signal
            module_count = 0
        else:  # manual
            injected_component_count = manual_signal or field_injection_count
            constructor_injection_count = manual_signal
            module_count = 0

        uses_field_injection = field_injection_count > 0

        # --- Title & description ------------------------------------------------------
        framework_labels = {
            "spring": "Spring",
            "koin": "Koin",
            "hilt": "Hilt",
            "dagger": "Dagger",
            "kotlin-inject": "kotlin-inject",
            "kodein": "Kodein",
            "manual": "manual",
        }
        label = framework_labels.get(primary, primary)

        if field_injection_count and field_injection_count >= constructor_injection_count:
            style = "field injection"
        elif constructor_injection_count:
            style = "constructor injection"
        else:
            style = "runtime wiring" if primary == "koin" else "dependency injection"

        if injected_component_count:
            title = f"Dependency injection: {label} {style} across {injected_component_count} component(s)"
        else:
            title = f"Dependency injection: {label} {style}"

        description_parts = [f"Uses {label} for dependency injection."]
        if primary == "spring" and stereotype_counts:
            breakdown = ", ".join(f"{count} @{name}" for name, count in sorted(stereotype_counts.items()))
            description_parts.append(f"Stereotype breakdown: {breakdown}.")
        if module_count:
            noun = "module" if module_count == 1 else "modules"
            description_parts.append(f"Defines {module_count} DI {noun}.")
        if bean_count and primary == "spring":
            description_parts.append(f"Declares {bean_count} @Bean factory method(s).")
        if len(frameworks) > 1:
            others = [framework_labels.get(f, f) for f in frameworks if f != primary]
            description_parts.append(f"Also detected: {', '.join(others)}.")

        if uses_field_injection:
            description_parts.append(
                f"Warning: {field_injection_count} field-injected propert(y/ies) via "
                "@Autowired/@Inject on lateinit/var fields — field injection hides "
                "dependencies, breaks immutability, and makes unit testing harder than "
                "constructor injection. Prefer constructor injection."
            )

        description = " ".join(description_parts)

        # --- Confidence -----------------------------------------------------------
        confidence = 0.35
        confidence += min(0.3, 0.03 * injected_component_count)
        confidence += min(0.15, 0.02 * module_count)
        if primary in ("spring", "hilt", "dagger", "koin"):
            confidence += 0.15
        if manual_signal and primary == "manual":
            confidence -= 0.1  # regex-only heuristic, less reliable
        confidence = min(0.95, max(0.05, confidence))

        # --- Evidence: prefer field-injection sites, then general sites ------------------
        ordered_sites = field_injection_sites + evidence_sites
        evidence = []
        seen: set[tuple[str, int]] = set()
        for rel_path, line in ordered_sites:
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
            rule_id="kotlin.conventions.dependency_injection",
            category="architecture",
            title=title,
            description=description,
            confidence=confidence,
            language="kotlin",
            evidence=evidence,
            stats={
                "framework": primary,
                "frameworks": frameworks,
                "injected_component_count": injected_component_count,
                "constructor_injection_count": constructor_injection_count,
                "field_injection_count": field_injection_count,
                "stereotype_counts": stereotype_counts,
                "module_count": module_count,
                "patterns": patterns,
                "uses_field_injection": uses_field_injection,
            },
        ))

        return result
