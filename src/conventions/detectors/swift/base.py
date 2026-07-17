"""Swift detector base class."""

from __future__ import annotations

from ..base import BaseDetector, DetectorContext
from .index import SwiftIndex


class SwiftDetector(BaseDetector):
    """Base class for Swift detectors."""

    languages: set[str] = {"swift"}

    def get_index(self, ctx: DetectorContext) -> SwiftIndex:
        """Get or create the Swift index."""
        if ctx.cache.get("swift_index") is None:
            index = SwiftIndex(
                ctx.repo_root,
                max_files=ctx.max_files,
                exclude_patterns=ctx.exclude_patterns,
            )
            index.build()
            ctx.cache["swift_index"] = index
        result: SwiftIndex = ctx.cache["swift_index"]
        return result
