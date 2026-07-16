"""Kotlin Android UI and lifecycle conventions detector."""

from __future__ import annotations

from typing import Optional

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import KotlinDetector
from .index import KotlinIndex, make_evidence

# Compose runtime idioms that signal active, idiomatic Compose usage (beyond
# just having @Composable functions).
COMPOSE_RUNTIME_PATTERNS: dict[str, str] = {
    "remember {": r"\bremember\s*\{",
    "mutableStateOf(": r"\bmutableStateOf\s*\(",
    "collectAsState()": r"\bcollectAsState(?:WithLifecycle)?\s*\(",
    "LaunchedEffect(": r"\bLaunchedEffect\s*\(",
}

# Legacy View-system idioms.
VIEW_SYSTEM_PATTERNS: dict[str, str] = {
    "findViewById(": r"\bfindViewById\s*(?:<[^>]*>)?\s*\(",
    "ViewBinding inflate": r"\w+Binding\s*\.\s*inflate\s*\(",
}

# Classes extending these Android framework/AndroidX base types are Activities.
_ACTIVITY_PATTERN = r"class\s+\w+\s*:\s*(?:AppCompatActivity|ComponentActivity)\b"
# Fragment and its common subclasses (DialogFragment, BottomSheetDialogFragment, ...).
_FRAGMENT_PATTERN = r"class\s+\w+\s*:\s*\w*Fragment\b"

_GLOBAL_SCOPE_PATTERN = r"\bGlobalScope\b"
_LIVEDATA_PATTERN = r"\bMutableLiveData\b|\bLiveData\s*<"
_STATEFLOW_PATTERN = r"\bMutableStateFlow\b|\bStateFlow\s*<"
_NAV_CONTROLLER_PATTERN = r"\bNavController\b|\bNavHost\b"
_DATABINDING_PATTERN = r"\bDataBindingUtil\b"
_SHARED_PREFS_PATTERN = r"\bSharedPreferences\b"
_LIFECYCLE_SCOPE_PATTERN = r"\blifecycleScope\b"
_REPEAT_ON_LIFECYCLE_PATTERN = r"\brepeatOnLifecycle\s*\("
_VIEW_LIFECYCLE_OWNER_PATTERN = r"\bviewLifecycleOwner\b"


@DetectorRegistry.register
class KotlinAndroidDetector(KotlinDetector):
    """Detect Android UI and lifecycle conventions in Kotlin projects."""

    name = "kotlin_android"
    description = "Detects Android UI and lifecycle conventions in Kotlin projects"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect Android UI toolkit, architecture and lifecycle conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        build_info = self.get_build_info(ctx)

        has_android_plugin = (
            build_info.has_plugin("com.android.application")
            or build_info.has_plugin("com.android.library")
            or build_info.has_plugin("kotlin-android")
            or build_info.has_plugin("kotlin.android")
        )
        android_import_count = index.count_imports_matching(
            "android."
        ) + index.count_imports_matching("androidx.")
        has_manifest = self._has_android_manifest(ctx)

        if not (has_android_plugin or android_import_count > 0 or has_manifest):
            return DetectorResult()

        examples: list[tuple[str, int]] = []

        # -- UI toolkit -----------------------------------------------------
        composable_count = index.count_annotation("Composable")
        preview_count = index.count_annotation("Preview")
        compose_runtime_hits = sum(
            index.count_pattern(pattern) for pattern in COMPOSE_RUNTIME_PATTERNS.values()
        )
        uses_compose = (
            composable_count > 0
            or compose_runtime_hits > 0
            or index.count_imports_matching("androidx.compose") > 0
        )
        if composable_count > 0:
            examples.extend(index.find_annotation("Composable", limit=3))

        material3, material2 = self._detect_material_version(index)
        material_version: Optional[str] = "material3" if material3 else ("material2" if material2 else None)

        find_view_by_id_count = index.count_pattern(VIEW_SYSTEM_PATTERNS["findViewById("])
        view_binding_matches = index.search_pattern(VIEW_SYSTEM_PATTERNS["ViewBinding inflate"], limit=3)
        uses_viewbinding = len(view_binding_matches) > 0
        uses_databinding = (
            index.count_pattern(_DATABINDING_PATTERN) > 0
            or index.count_imports_matching("androidx.databinding") > 0
        )
        uses_synthetics = index.count_imports_matching("kotlinx.android.synthetic") > 0
        synthetic_imports = (
            index.find_imports_matching("kotlinx.android.synthetic", limit=3) if uses_synthetics else []
        )
        examples.extend((rel, line) for rel, _, line in synthetic_imports)

        uses_views = find_view_by_id_count > 0 or uses_viewbinding or uses_databinding or uses_synthetics

        if uses_compose and uses_views:
            ui_toolkit = "hybrid"
        elif uses_compose:
            ui_toolkit = "compose"
        elif uses_views:
            ui_toolkit = "views"
        else:
            ui_toolkit = "unknown"

        if uses_viewbinding:
            examples.extend((rel, line) for rel, line, _ in view_binding_matches)

        # -- Architecture -----------------------------------------------------
        viewmodel_classes = [
            (rel, cls)
            for rel, cls in index.all_classes()
            if cls.name.endswith("ViewModel") and not index.files[rel].is_test
        ]
        viewmodel_count = len(viewmodel_classes)
        if viewmodel_classes:
            examples.append((viewmodel_classes[0][0], viewmodel_classes[0][1].line))

        hilt_viewmodel_count = index.count_annotation("HiltViewModel")
        # A bare `dagger.hilt` import is not adoption -- libraries that merely
        # interoperate with Hilt (Koin ships a single `dagger.hilt.EntryPoints`
        # import) would otherwise be reported as Hilt apps. Require Hilt's own
        # entry-point annotations or a build-level plugin/dependency.
        uses_hilt = (
            hilt_viewmodel_count > 0
            or index.count_annotation("HiltAndroidApp") > 0
            or index.count_annotation("AndroidEntryPoint") > 0
            or build_info.has_plugin("hilt")
            or build_info.has_dependency("hilt")
        )

        stateflow_count = index.count_pattern(_STATEFLOW_PATTERN)
        livedata_count = index.count_pattern(_LIVEDATA_PATTERN)
        if stateflow_count > 0 and livedata_count > 0:
            state_holder = "mixed"
        elif stateflow_count > 0:
            state_holder = "stateflow"
        elif livedata_count > 0:
            state_holder = "livedata"
        else:
            state_holder = "none"

        uses_navigation = (
            index.count_imports_matching("androidx.navigation") > 0
            or index.count_pattern(_NAV_CONTROLLER_PATTERN) > 0
        )

        uses_room = (
            index.count_imports_matching("androidx.room") > 0
            or build_info.has_dependency("androidx.room")
        )
        uses_retrofit = (
            index.count_imports_matching("retrofit2") > 0
            or build_info.has_dependency("retrofit2")
        )

        lifecyclescope_count = index.count_pattern(_LIFECYCLE_SCOPE_PATTERN)
        repeat_on_lifecycle_count = index.count_pattern(_REPEAT_ON_LIFECYCLE_PATTERN)
        view_lifecycle_owner_count = index.count_pattern(_VIEW_LIFECYCLE_OWNER_PATTERN)

        uses_workmanager = (
            index.count_imports_matching("androidx.work") > 0
            or build_info.has_dependency("androidx.work")
        )
        uses_datastore = (
            index.count_imports_matching("androidx.datastore") > 0
            or build_info.has_dependency("androidx.datastore")
        )
        uses_shared_preferences = index.count_pattern(_SHARED_PREFS_PATTERN) > 0

        # Counts via count_pattern; search_pattern only supplies example sites,
        # since its limit would otherwise cap the reported totals.
        activity_count = index.count_pattern(_ACTIVITY_PATTERN, exclude_tests=True)
        fragment_count = index.count_pattern(_FRAGMENT_PATTERN, exclude_tests=True)
        activity_matches = index.search_pattern(_ACTIVITY_PATTERN, limit=1, exclude_tests=True)
        fragment_matches = index.search_pattern(_FRAGMENT_PATTERN, limit=1, exclude_tests=True)
        if activity_matches:
            examples.append((activity_matches[0][0], activity_matches[0][1]))
        if fragment_matches:
            examples.append((fragment_matches[0][0], fragment_matches[0][1]))

        # -- Anti-patterns ------------------------------------------------
        global_scope_matches = index.search_pattern(_GLOBAL_SCOPE_PATTERN, limit=3, exclude_tests=True)
        global_scope_count = len(global_scope_matches)
        if global_scope_matches:
            examples.extend((rel, line) for rel, line, _ in global_scope_matches)

        patterns = _collect_patterns(
            ui_toolkit=ui_toolkit,
            material_version=material_version,
            uses_viewbinding=uses_viewbinding,
            uses_databinding=uses_databinding,
            uses_synthetics=uses_synthetics,
            viewmodel_count=viewmodel_count,
            uses_hilt=uses_hilt,
            state_holder=state_holder,
            uses_navigation=uses_navigation,
            uses_room=uses_room,
            uses_retrofit=uses_retrofit,
            uses_workmanager=uses_workmanager,
            uses_datastore=uses_datastore,
            uses_shared_preferences=uses_shared_preferences,
            global_scope_count=global_scope_count,
        )

        title = _build_title(
            ui_toolkit=ui_toolkit,
            composable_count=composable_count,
            state_holder=state_holder,
            uses_hilt=uses_hilt,
        )
        description = _build_description(
            ui_toolkit=ui_toolkit,
            composable_count=composable_count,
            preview_count=preview_count,
            material_version=material_version,
            uses_viewbinding=uses_viewbinding,
            uses_databinding=uses_databinding,
            uses_synthetics=uses_synthetics,
            viewmodel_count=viewmodel_count,
            uses_hilt=uses_hilt,
            state_holder=state_holder,
            uses_navigation=uses_navigation,
            uses_room=uses_room,
            uses_retrofit=uses_retrofit,
            uses_workmanager=uses_workmanager,
            uses_datastore=uses_datastore,
            uses_shared_preferences=uses_shared_preferences,
            activity_count=activity_count,
            fragment_count=fragment_count,
            lifecyclescope_count=lifecyclescope_count,
            repeat_on_lifecycle_count=repeat_on_lifecycle_count,
            view_lifecycle_owner_count=view_lifecycle_owner_count,
            global_scope_count=global_scope_count,
        )

        confidence = 0.5
        if has_android_plugin:
            confidence += 0.1
        if ui_toolkit != "unknown":
            confidence += 0.1
        if viewmodel_count > 0:
            confidence += 0.05
        if uses_hilt:
            confidence += 0.05
        if uses_navigation:
            confidence += 0.05
        if state_holder != "none":
            confidence += 0.05
        if uses_room or uses_retrofit:
            confidence += 0.05
        confidence = min(0.95, confidence)

        evidence = []
        for rel_path, line in examples[: ctx.max_evidence_snippets]:
            ev = make_evidence(index, rel_path, line, radius=3)
            if ev:
                evidence.append(ev)

        stats: dict[str, object] = {
            "ui_toolkit": ui_toolkit,
            "composable_count": composable_count,
            "activity_count": activity_count,
            "fragment_count": fragment_count,
            "viewmodel_count": viewmodel_count,
            "state_holder": state_holder,
            "uses_navigation": uses_navigation,
            "uses_hilt": uses_hilt,
            "uses_synthetics": uses_synthetics,
            "uses_viewbinding": uses_viewbinding,
            "patterns": patterns,
            "material_version": material_version,
            "preview_count": preview_count,
            "uses_databinding": uses_databinding,
            "stateflow_count": stateflow_count,
            "livedata_count": livedata_count,
            "uses_room": uses_room,
            "uses_retrofit": uses_retrofit,
            "uses_workmanager": uses_workmanager,
            "uses_datastore": uses_datastore,
            "uses_shared_preferences": uses_shared_preferences,
            "lifecyclescope_count": lifecyclescope_count,
            "repeat_on_lifecycle_count": repeat_on_lifecycle_count,
            "global_scope_count": global_scope_count,
        }

        result.rules.append(self.make_rule(
            rule_id="kotlin.conventions.android",
            category="frontend",
            title=title,
            description=description,
            confidence=confidence,
            language="kotlin",
            evidence=evidence,
            stats=stats,
        ))

        return result

    def _has_android_manifest(self, ctx: DetectorContext) -> bool:
        """Check the common locations for an AndroidManifest.xml without a wide glob."""
        common_paths = (
            ctx.repo_root / "src" / "main" / "AndroidManifest.xml",
            ctx.repo_root / "app" / "src" / "main" / "AndroidManifest.xml",
        )
        if any(path.exists() for path in common_paths):
            return True

        # Single-level fallback for other module layouts, e.g. `mobile/src/main/...`.
        return next(ctx.repo_root.glob("*/src/main/AndroidManifest.xml"), None) is not None

    def _detect_material_version(self, index: KotlinIndex) -> tuple[bool, bool]:
        """Check imports for Compose Material3 vs the legacy Material2 package.

        `androidx.compose.material3` is a substring superset of
        `androidx.compose.material.`, so the two are told apart by inspecting
        raw import paths rather than a plain substring count.
        """
        material3 = False
        material2 = False
        for file_idx in index.files.values():
            for import_path, _ in file_idx.imports:
                if import_path.startswith("androidx.compose.material3"):
                    material3 = True
                elif import_path.startswith("androidx.compose.material."):
                    material2 = True
        return material3, material2


def _collect_patterns(
    *,
    ui_toolkit: str,
    material_version: Optional[str],
    uses_viewbinding: bool,
    uses_databinding: bool,
    uses_synthetics: bool,
    viewmodel_count: int,
    uses_hilt: bool,
    state_holder: str,
    uses_navigation: bool,
    uses_room: bool,
    uses_retrofit: bool,
    uses_workmanager: bool,
    uses_datastore: bool,
    uses_shared_preferences: bool,
    global_scope_count: int,
) -> list[str]:
    """Collect short, human-readable pattern tags for the stats block."""
    patterns: list[str] = []
    if ui_toolkit in ("compose", "hybrid"):
        patterns.append("jetpack-compose")
    if material_version:
        patterns.append(material_version)
    if ui_toolkit in ("views", "hybrid"):
        patterns.append("views")
    if uses_viewbinding:
        patterns.append("viewbinding")
    if uses_databinding:
        patterns.append("databinding")
    if uses_synthetics:
        patterns.append("kotlin-synthetics-deprecated")
    if viewmodel_count > 0:
        patterns.append("viewmodel")
    if uses_hilt:
        patterns.append("hilt")
    if state_holder == "stateflow":
        patterns.append("stateflow")
    elif state_holder == "livedata":
        patterns.append("livedata")
    elif state_holder == "mixed":
        patterns.append("stateflow+livedata")
    if uses_navigation:
        patterns.append("navigation")
    if uses_room:
        patterns.append("room")
    if uses_retrofit:
        patterns.append("retrofit")
    if uses_workmanager:
        patterns.append("workmanager")
    if uses_datastore:
        patterns.append("datastore")
    elif uses_shared_preferences:
        patterns.append("shared-preferences")
    if global_scope_count > 0:
        patterns.append("global-scope-in-android")
    return patterns


def _build_title(
    *,
    ui_toolkit: str,
    composable_count: int,
    state_holder: str,
    uses_hilt: bool,
) -> str:
    """Build a rule title summarizing the dominant Android UI toolkit and state approach."""
    if ui_toolkit == "compose":
        noun = "composable" if composable_count == 1 else "composables"
        base = f"Android: Jetpack Compose with {composable_count} {noun}"
    elif ui_toolkit == "hybrid":
        noun = "composable" if composable_count == 1 else "composables"
        base = f"Android: Compose + Views ({composable_count} {noun})"
    elif ui_toolkit == "views":
        base = "Android: Classic Views"
    else:
        base = "Android"

    extras: list[str] = []
    if state_holder == "stateflow":
        extras.append("StateFlow")
    elif state_holder == "livedata":
        extras.append("LiveData")
    elif state_holder == "mixed":
        extras.append("StateFlow + LiveData")
    if uses_hilt:
        extras.append("Hilt")

    if extras:
        base += ", " + " + ".join(extras)
    return base


def _build_description(
    *,
    ui_toolkit: str,
    composable_count: int,
    preview_count: int,
    material_version: Optional[str],
    uses_viewbinding: bool,
    uses_databinding: bool,
    uses_synthetics: bool,
    viewmodel_count: int,
    uses_hilt: bool,
    state_holder: str,
    uses_navigation: bool,
    uses_room: bool,
    uses_retrofit: bool,
    uses_workmanager: bool,
    uses_datastore: bool,
    uses_shared_preferences: bool,
    activity_count: int,
    fragment_count: int,
    lifecyclescope_count: int,
    repeat_on_lifecycle_count: int,
    view_lifecycle_owner_count: int,
    global_scope_count: int,
) -> str:
    """Build a rule description covering UI toolkit, architecture and anti-patterns."""
    parts: list[str] = []

    if ui_toolkit == "compose":
        parts.append(f"Uses Jetpack Compose for UI ({composable_count} @Composable function(s)).")
    elif ui_toolkit == "hybrid":
        parts.append(
            f"Mixes Jetpack Compose ({composable_count} @Composable function(s)) with the classic View system."
        )
    elif ui_toolkit == "views":
        parts.append("Uses the classic Android View system (XML layouts).")

    if preview_count > 0:
        parts.append(f"{preview_count} @Preview composable(s) for design-time rendering.")
    if material_version == "material3":
        parts.append("Uses Material3.")
    elif material_version == "material2":
        parts.append("Uses Material2 (legacy Compose Material).")
    if uses_viewbinding:
        parts.append("Uses ViewBinding.")
    if uses_databinding:
        parts.append("Uses DataBinding.")

    if activity_count > 0 or fragment_count > 0:
        parts.append(f"{activity_count} Activity class(es), {fragment_count} Fragment class(es).")

    if viewmodel_count > 0:
        parts.append(f"{viewmodel_count} ViewModel class(es).")
    if uses_hilt:
        parts.append("Uses Hilt for dependency injection.")
    if state_holder == "stateflow":
        parts.append("Uses StateFlow for UI state (current recommended approach).")
    elif state_holder == "livedata":
        parts.append("Uses LiveData for UI state (older approach; StateFlow is current guidance).")
    elif state_holder == "mixed":
        parts.append("Mixes StateFlow and LiveData for UI state.")
    if uses_navigation:
        parts.append("Uses the Navigation component.")
    if uses_room:
        parts.append("Uses Room for local persistence.")
    if uses_retrofit:
        parts.append("Uses Retrofit for networking.")
    if uses_workmanager:
        parts.append("Uses WorkManager for background work.")
    if uses_datastore:
        parts.append("Uses DataStore for local preferences (current recommended approach).")
    elif uses_shared_preferences:
        parts.append("Uses SharedPreferences (older approach; DataStore is current guidance).")

    lifecycle_notes: list[str] = []
    if lifecyclescope_count > 0:
        lifecycle_notes.append("lifecycleScope")
    if repeat_on_lifecycle_count > 0:
        lifecycle_notes.append("repeatOnLifecycle")
    if view_lifecycle_owner_count > 0:
        lifecycle_notes.append("viewLifecycleOwner")
    if lifecycle_notes:
        parts.append(f"Uses lifecycle-aware APIs: {', '.join(lifecycle_notes)}.")

    anti_pattern_notes: list[str] = []
    if uses_synthetics:
        anti_pattern_notes.append(
            "Uses kotlinx.android.synthetic imports, which are deprecated and were removed "
            "in Kotlin 1.9 -- a migration blocker."
        )
    if global_scope_count > 0:
        noun = "usage" if global_scope_count == 1 else "usages"
        anti_pattern_notes.append(
            f"{global_scope_count} GlobalScope {noun} found in Android code, bypassing "
            "structured concurrency and lifecycle-scoped cancellation."
        )
    if anti_pattern_notes:
        parts.append(" ".join(anti_pattern_notes))

    return " ".join(parts) if parts else "Android project."
