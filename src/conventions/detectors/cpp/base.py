"""C++ detector base class."""

from __future__ import annotations

from ..base import BaseDetector, DetectorContext
from .index import CPPIndex


class CPPDetector(BaseDetector):
    """Base class for C++ detectors."""

    languages: set[str] = {"cpp"}

    def get_index(self, ctx: DetectorContext) -> CPPIndex:
        """Get or create the C++ index."""
        if ctx.cache.get("cpp_index") is None:
            index = CPPIndex(
                ctx.repo_root,
                max_files=ctx.max_files,
                exclude_patterns=ctx.exclude_patterns,
            )
            index.build()
            ctx.cache["cpp_index"] = index
        result: CPPIndex = ctx.cache["cpp_index"]
        return result
