"""Swift architecture conventions detector."""

from __future__ import annotations

from collections import Counter
from typing import Optional

from ..base import DetectorContext, DetectorResult
from ..registry import DetectorRegistry
from .base import SwiftDetector
from .index import SwiftFileIndex, make_evidence

ARCHITECTURAL_ROLES = ("api", "service", "db", "model")


@DetectorRegistry.register
class SwiftArchitectureDetector(SwiftDetector):
    """Detect Swift project structure, module layout and framework styling."""

    name = "swift_architecture"
    description = "Detects Swift project structure, module layout and framework styling"

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        """Detect Swift architecture conventions."""
        result = DetectorResult()
        index = self.get_index(ctx)

        if not index.files:
            return result

        # 1. Framework detection based on imports and Package.swift.
        swiftui_count = index.count_import("SwiftUI")
        uikit_count = index.count_import("UIKit")
        vapor_count = index.count_import("Vapor") or index.count_dependency("Vapor")

        # Is this a library or an application? A package that vends a .library
        # product is a library even if it also ships a demo app, so the product
        # declaration wins over entry-point heuristics. Without it, any UIKit
        # import made a project a "UIKit Application" -- and nearly every iOS
        # library imports UIKit. Alamofire (a networking library with 3 UIKit
        # imports) was reported as a UIKit Application.
        vends_library = "library" in index.product_types
        vends_executable = "executable" in index.product_types
        app_entry_count = index.count_pattern(
            r"@main\b|@UIApplicationMain\b|@NSApplicationMain\b", exclude_tests=True
        )
        has_package_manifest = (ctx.repo_root / "Package.swift").is_file()

        if vends_library:
            is_application = False
        elif vends_executable or app_entry_count > 0:
            is_application = True
        else:
            # No library product declared. An app built with Xcode has an
            # .xcodeproj and no Package.swift, so the absence of a manifest
            # points at an application rather than a package.
            is_application = not has_package_manifest

        # A UI framework only characterizes the project if it shows up across a
        # real share of it; a handful of incidental imports does not. Scaled to
        # the project rather than a fixed floor, so small projects still work.
        significance = max(1, len(index.files) * 0.1)
        swiftui_primary = swiftui_count >= significance and swiftui_count >= uikit_count
        uikit_primary = uikit_count >= significance and uikit_count > swiftui_count
        vapor_primary = vapor_count >= significance

        if is_application:
            if vapor_primary:
                framework = "Vapor Server Application"
            elif swiftui_primary:
                framework = "SwiftUI Application"
            elif uikit_primary:
                framework = "UIKit Application"
            else:
                framework = "Swift Application"
        else:
            if vapor_primary:
                framework = "Swift Library (Vapor)"
            elif swiftui_primary:
                framework = "Swift Library (SwiftUI)"
            elif uikit_primary:
                framework = "Swift Library (UIKit)"
            else:
                framework = "Swift Package / Library"

        # 2. Structure & Layering
        role_counts = Counter(f.role for f in index.files.values())
        layers = sorted(role for role in role_counts if role in ARCHITECTURAL_ROLES)

        title = f"Architecture: {framework}"
        desc_parts = [
            f"Swift project ({len(index.files)} files) is structured as a {framework}."
        ]
        if layers:
            desc_parts.append(f"Layers detected: {', '.join(layers)}.")

        # Linting styling (SwiftLint)
        has_swiftlint = ctx.repo_root.joinpath(".swiftlint.yml").exists()
        if has_swiftlint:
            desc_parts.append("SwiftLint style rules (.swiftlint.yml) are present.")
        else:
            desc_parts.append("No SwiftLint configuration found.")

        description = " ".join(desc_parts)

        # Build evidence
        evidence = []
        preferred_role_order = ["api", "service", "model", "main"]
        ordered_roles = [r for r in preferred_role_order if r in role_counts]

        for role in ordered_roles:
            if len(evidence) >= ctx.max_evidence_snippets:
                break
            candidate: Optional[SwiftFileIndex] = None
            for file_idx in index.get_files_by_role(role):
                if not file_idx.is_test:
                    candidate = file_idx
                    break
            if candidate:
                ev = make_evidence(index, candidate.relative_path, 1, radius=3)
                if ev:
                    evidence.append(ev)

        stats = {
            "framework": framework,
            "is_application": is_application,
            "product_types": sorted(index.product_types),
            "swiftui_count": swiftui_count,
            "uikit_count": uikit_count,
            "vapor_count": vapor_count,
            "has_swiftlint": has_swiftlint,
            "layers": layers,
            "role_counts": dict(role_counts),
            "file_count": len(index.files),
        }

        result.rules.append(self.make_rule(
            rule_id="swift.conventions.architecture",
            category="architecture",
            title=title,
            description=description,
            confidence=0.8,
            language="swift",
            evidence=evidence,
            stats=stats,
        ))

        return result
