"""C++ code indexer using regex-based analysis."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from ...fs import get_relative_path, read_file_safe, walk_files
from ...schemas import EvidenceSnippet

CPP_EXTENSIONS = {".cpp", ".h", ".hpp", ".cc", ".cxx", ".hh", ".hxx"}


@dataclass
class CPPFileIndex:
    """Index of a single C++ file."""

    path: Path
    relative_path: str
    role: str  # main, test, build, api, service, db, model
    parse_error: Optional[str] = None

    includes: list[tuple[str, int]] = field(default_factory=list)  # (include_path, line)
    types: list[tuple[str, str, int]] = field(default_factory=list)  # (kind, name, line)
    namespaces: list[str] = field(default_factory=list)

    todo_count: int = 0
    lines: list[str] = field(default_factory=list)

    @property
    def is_test(self) -> bool:
        """Whether this file holds tests."""
        return self.role == "test"

    @property
    def is_header(self) -> bool:
        """Whether this is a header file."""
        return self.path.suffix in (".h", ".hpp", ".hh", ".hxx")


class CPPIndex:
    """
    Index of C++ files in a repository.

    Uses regex-based analysis (lighter than full AST).
    """

    def __init__(
        self,
        repo_root: Path,
        max_files: int = 1000,
        exclude_patterns: Optional[list[str]] = None,
    ):
        self.repo_root = Path(repo_root).resolve()
        self.max_files = max_files
        self.exclude_patterns = exclude_patterns or []
        self.files: dict[str, CPPFileIndex] = {}
        self.cmake_targets: set[str] = set()
        self._built = False

    def build(self) -> None:
        """Build the index by scanning all C++ files and CMakeLists.txt."""
        if self._built:
            return

        # Scan CMakeLists.txt if present
        cmakelists = self.repo_root / "CMakeLists.txt"
        if cmakelists.exists() and cmakelists.is_file():
            self._parse_cmakelists(cmakelists)

        for file_path in walk_files(
            self.repo_root,
            extensions=CPP_EXTENSIONS,
            max_files=self.max_files,
            exclude_patterns=self.exclude_patterns,
        ):
            if file_path.name == "CMakeLists.txt":
                continue
            file_index = self._index_file(file_path)
            self.files[file_index.relative_path] = file_index

        self._built = True

    def _parse_cmakelists(self, path: Path) -> None:
        """Parse CMakeLists.txt to extract target names or packages."""
        content = read_file_safe(path)
        if not content:
            return
        # Matches: add_executable(my_app ...) or add_library(my_lib ...)
        pattern = re.compile(
            r"\b(?:add_executable|add_library)\s*\(\s*(\w+)",
            re.MULTILINE | re.IGNORECASE,
        )
        for match in pattern.finditer(content):
            self.cmake_targets.add(match.group(1))

    def _index_file(self, file_path: Path) -> CPPFileIndex:
        """Index a single C++ file."""
        relative_path = get_relative_path(file_path, self.repo_root)

        file_index = CPPFileIndex(
            path=file_path,
            relative_path=relative_path,
            role=infer_cpp_file_role(relative_path),
        )

        content = read_file_safe(file_path)
        if content is None:
            file_index.parse_error = "Could not read file"
            return file_index

        file_index.lines = content.splitlines()

        # Strip comments and strings
        code = strip_comments_and_strings(content)

        file_index.includes = self._extract_includes(content)
        file_index.types = self._extract_types(code)
        file_index.namespaces = self._extract_namespaces(code)

        file_index.todo_count = len(re.findall(r"//\s*(?:TODO|FIXME)\b", content)) + \
                                len(re.findall(r"/\*\s*(?:TODO|FIXME)\b", content))

        return file_index

    def _extract_includes(self, code: str) -> list[tuple[str, int]]:
        """Extract include statements."""
        includes = []
        # Matches: #include <vector> or #include "user.h"
        pattern = re.compile(r"^\s*#\s*include\s+([<\"].*?[>\"])", re.MULTILINE)
        for match in pattern.finditer(code):
            line = code[: match.start()].count("\n") + 1
            includes.append((match.group(1), line))
        return includes

    def _extract_types(self, code: str) -> list[tuple[str, str, int]]:
        """Extract classes, structs, enums."""
        types = []
        # Matches: class User, struct Point, enum class Color
        pattern = re.compile(r"\b(class|struct|enum)\s+(?:class\s+)?(\w+)\b", re.MULTILINE)
        for match in pattern.finditer(code):
            line = code[: match.start()].count("\n") + 1
            types.append((match.group(1), match.group(2), line))
        return types

    def _extract_namespaces(self, code: str) -> list[str]:
        """Extract namespaces."""
        # Matches: namespace Acme or namespace Acme::Core
        pattern = re.compile(r"\bnamespace\s+([\w::]+)\b", re.MULTILINE)
        return [match.group(1) for match in pattern.finditer(code)]

    # Query methods
    def count_include(self, include_name: str) -> int:
        """Count files including a specific header file."""
        count = 0
        for file_idx in self.files.values():
            if any(include_name in inc[0] for inc in file_idx.includes):
                count += 1
        return count

    def search_pattern(
        self,
        pattern: str,
        limit: int = 100,
        exclude_tests: bool = False,
    ) -> list[tuple[str, int, str]]:
        """Search for a regex across all files. Returns (file_path, line, match)."""
        results = []
        compiled = re.compile(pattern, re.MULTILINE)

        for rel_path, file_idx in self.files.items():
            if exclude_tests and file_idx.is_test:
                continue

            content = "\n".join(file_idx.lines)
            for match in compiled.finditer(content):
                line = content[: match.start()].count("\n") + 1
                results.append((rel_path, line, match.group(0)))
                if len(results) >= limit:
                    return results

        return results

    def count_pattern(
        self,
        pattern: str,
        exclude_tests: bool = False,
    ) -> int:
        """Count regex occurrences across all files."""
        count = 0
        compiled = re.compile(pattern, re.MULTILINE)

        for file_idx in self.files.values():
            if exclude_tests and file_idx.is_test:
                continue

            content = "\n".join(file_idx.lines)
            count += len(compiled.findall(content))

        return count

    def get_test_files(self) -> list[CPPFileIndex]:
        """Get all test files."""
        return [f for f in self.files.values() if f.is_test]

    def get_non_test_files(self) -> list[CPPFileIndex]:
        """Get all non-test files."""
        return [f for f in self.files.values() if not f.is_test]

    def get_files_by_role(self, role: str) -> list[CPPFileIndex]:
        """Get all files with the given role."""
        return [f for f in self.files.values() if f.role == role]


def infer_cpp_file_role(relative_path: str) -> str:
    """Infer the role of a C++ file from its path."""
    parts = Path(relative_path).parts
    lower_parts = [p.lower() for p in parts]
    filename = Path(relative_path).name

    # Test file detection
    if "test" in lower_parts or "tests" in lower_parts:
        return "test"
    if filename.endswith(("Test.cpp", "Tests.cpp", "test.cpp", "tests.cpp", "Spec.cpp", "Specs.cpp")):
        return "test"

    # Standard roles
    if any(p in ("controller", "controllers", "api") for p in lower_parts):
        return "api"
    if any(p in ("service", "services", "usecase", "domain") for p in lower_parts):
        return "service"
    if any(p in ("repository", "repositories", "db", "database") for p in lower_parts):
        return "db"
    if any(p in ("model", "models", "entity", "entities", "dto") for p in lower_parts):
        return "model"

    return "main"


def strip_comments_and_strings(content: str) -> str:
    """Blank out comments and string literals, preserving offsets."""
    result = list(content)
    length = len(content)
    i = 0

    while i < length:
        char = content[i]
        nxt = content[i + 1] if i + 1 < length else ""

        # Line comment //
        if char == "/" and nxt == "/":
            while i < length and content[i] != "\n":
                result[i] = " "
                i += 1
            continue

        # Block comment /* ... */
        if char == "/" and nxt == "*":
            result[i] = result[i + 1] = " "
            i += 2
            while i < length:
                if content[i] == "*" and i + 1 < length and content[i + 1] == "/":
                    result[i] = result[i + 1] = " "
                    i += 2
                    break
                if content[i] != "\n":
                    result[i] = " "
                i += 1
            continue

        # String literal "..."
        if char == '"':
            result[i] = " "
            i += 1
            while i < length and content[i] != '"':
                if content[i] == "\\" and i + 1 < length:
                    result[i] = " "
                    if content[i + 1] != "\n":
                        result[i + 1] = " "
                    i += 2
                    continue
                if content[i] == "\n":
                    break
                result[i] = " "
                i += 1
            if i < length and content[i] == '"':
                result[i] = " "
                i += 1
            continue

        # Character literal '...'
        if char == "'":
            result[i] = " "
            i += 1
            while i < length and content[i] != "'":
                if content[i] == "\\" and i + 1 < length:
                    result[i] = " "
                    if content[i + 1] != "\n":
                        result[i + 1] = " "
                    i += 2
                    continue
                if content[i] == "\n":
                    break
                result[i] = " "
                i += 1
            if i < length and content[i] == "'":
                result[i] = " "
                i += 1
            continue

        i += 1

    return "".join(result)


def make_evidence(
    index: CPPIndex,
    relative_path: str,
    line: int,
    radius: int = 5,
) -> Optional[EvidenceSnippet]:
    """Create an evidence snippet from the index."""
    file_idx = index.files.get(relative_path)
    if file_idx is None:
        return None

    lines = file_idx.lines
    if not lines or line < 1 or line > len(lines):
        return None

    line_start = max(1, line - radius)
    line_end = min(len(lines), line + radius)

    excerpt_lines = lines[line_start - 1 : line_end]
    excerpt = "\n".join(excerpt_lines)

    return EvidenceSnippet(
        file_path=relative_path,
        line_start=line_start,
        line_end=line_end,
        excerpt=excerpt,
    )
