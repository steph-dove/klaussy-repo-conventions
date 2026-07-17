"""Base class for Rust convention detectors."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import BaseDetector, DetectorContext

if TYPE_CHECKING:
    from .index import RustIndex


class RustDetector(BaseDetector):
    """Base class for Rust-specific detectors."""

    # `languages` (plural) is the attribute BaseDetector.should_run gates on; a
    # singular `language` was silently ignored, leaving these detectors with the
    # inherited empty set, which means "language-agnostic -- always run". Every
    # Rust detector was building a RustIndex for every repository scanned.
    languages: set[str] = {"rust"}

    def get_index(self, ctx: DetectorContext) -> "RustIndex":
        """Get or create the Rust index from context."""
        from .index import RustIndex

        cache_key = "rust_index"
        if cache_key not in ctx.cache:
            index = RustIndex(ctx.repo_root)
            index.build()
            ctx.cache[cache_key] = index
        result: RustIndex = ctx.cache[cache_key]
        return result
