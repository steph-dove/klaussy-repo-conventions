"""PHP detector base class."""

from __future__ import annotations

from ..base import BaseDetector, DetectorContext
from .index import PHPIndex


class PHPDetector(BaseDetector):
    """Base class for PHP detectors."""

    languages: set[str] = {"php"}

    def get_index(self, ctx: DetectorContext) -> PHPIndex:
        """Get or create the PHP index."""
        if ctx.cache.get("php_index") is None:
            index = PHPIndex(
                ctx.repo_root,
                max_files=ctx.max_files,
                exclude_patterns=ctx.exclude_patterns,
            )
            index.build()
            ctx.cache["php_index"] = index
        result: PHPIndex = ctx.cache["php_index"]
        return result
