"""Java detector base class."""

from __future__ import annotations

from ..base import BaseDetector, DetectorContext
from ..jvm.build import BuildInfo, parse_build_files
from .index import JavaIndex


class JavaDetector(BaseDetector):
    """Base class for Java detectors."""

    languages: set[str] = {"java"}

    def get_index(self, ctx: DetectorContext) -> JavaIndex:
        """Get or create the Java index."""
        if ctx.cache.get("java_index") is None:
            index = JavaIndex(
                ctx.repo_root,
                max_files=ctx.max_files,
                exclude_patterns=ctx.exclude_patterns,
            )
            index.build()
            ctx.cache["java_index"] = index
        result: JavaIndex = ctx.cache["java_index"]
        return result

    def get_build_info(self, ctx: DetectorContext) -> BuildInfo:
        """Get or create the parsed Gradle/Maven build info."""
        if ctx.cache.get("jvm_build_info") is None:
            ctx.cache["jvm_build_info"] = parse_build_files(
                ctx.repo_root,
                exclude_patterns=ctx.exclude_patterns,
            )
        result: BuildInfo = ctx.cache["jvm_build_info"]
        return result
