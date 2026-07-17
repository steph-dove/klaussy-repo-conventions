"""Ruby detector base class."""

from __future__ import annotations

from ..base import BaseDetector, DetectorContext
from .index import RubyIndex


class RubyDetector(BaseDetector):
    """Base class for Ruby detectors."""

    languages: set[str] = {"ruby"}

    def get_index(self, ctx: DetectorContext) -> RubyIndex:
        """Get or create the Ruby index."""
        if ctx.cache.get("ruby_index") is None:
            index = RubyIndex(
                ctx.repo_root,
                max_files=ctx.max_files,
                exclude_patterns=ctx.exclude_patterns,
            )
            index.build()
            ctx.cache["ruby_index"] = index
        result: RubyIndex = ctx.cache["ruby_index"]
        return result
