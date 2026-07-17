"""Swift code indexer using regex-based analysis."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from ...fs import get_relative_path, read_file_safe, walk_files
from ...schemas import EvidenceSnippet


@dataclass
class SwiftFileIndex:
    """Index of a single Swift file."""

    path: Path
    relative_path: str
    role: str  # main, test, build, api, service, db, model
    parse_error: Optional[str] = None

    imports: list[tuple[str, int]] = field(default_factory=list)  # (module_name, line)
    types: list[tuple[str, str, int]] = field(default_factory=list)  # (kind, name, line)
    async_count: int = 0
    await_count: int = 0
    todo_count: int = 0
    lines: list[str] = field(default_factory=list)

    @property
    def is_test(self) -> bool:
        """Whether this file holds tests."""
        return self.role == "test"


class SwiftIndex:
    """
    Index of Swift files in a repository.

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
        self.files: dict[str, SwiftFileIndex] = {}
        self.dependencies: set[str] = set()
        # Product kinds declared in Package.swift: "library" and/or "executable".
        self.product_types: set[str] = set()
        self._built = False

    def build(self) -> None:
        """Build the index by scanning all Swift files and Package.swift."""
        if self._built:
            return

        # Scan Package.swift for Swift Package Manager dependencies
        package_swift = self.repo_root / "Package.swift"
        if package_swift.exists() and package_swift.is_file():
            self._parse_package_swift(package_swift)

        for file_path in walk_files(
            self.repo_root,
            extensions={".swift"},
            max_files=self.max_files,
            exclude_patterns=self.exclude_patterns,
        ):
            if file_path.name == "Package.swift":
                continue
            file_index = self._index_file(file_path)
            self.files[file_index.relative_path] = file_index

        self._built = True

    def _parse_package_swift(self, path: Path) -> None:
        """Parse Package.swift for dependencies and the products it vends."""
        content = read_file_safe(path)
        if not content:
            return
        # Matches dependencies like: .package(url: "...", ...) or package(name: "...", ...)
        pattern = re.compile(
            r"\.package\s*\(\s*(?:url|path|name)\s*:\s*['\"]([^'\"]+)['\"]",
            re.MULTILINE,
        )
        for match in pattern.finditer(content):
            dep_path = match.group(1)
            # Extract last segment as dependency name (e.g. Vapor from https://github.com/vapor/vapor.git)
            dep_name = dep_path.split("/")[-1].replace(".git", "")
            self.dependencies.add(dep_name)

        # The products a package vends say what it *is*. A package declaring a
        # .library product is a library even when it also ships a demo app or an
        # executable dev tool, and nearly every iOS library imports UIKit -- so
        # UIKit imports alone must not make it an "application".
        if re.search(r"\.library\s*\(", content):
            self.product_types.add("library")
        if re.search(r"\.executable(?:Target)?\s*\(", content):
            self.product_types.add("executable")

    def _index_file(self, file_path: Path) -> SwiftFileIndex:
        """Index a single Swift file."""
        relative_path = get_relative_path(file_path, self.repo_root)

        file_index = SwiftFileIndex(
            path=file_path,
            relative_path=relative_path,
            role=infer_swift_file_role(relative_path),
        )

        content = read_file_safe(file_path)
        if content is None:
            file_index.parse_error = "Could not read file"
            return file_index

        file_index.lines = content.splitlines()

        # Strip comments and strings
        code = strip_comments_and_strings(content)

        file_index.imports = self._extract_imports(code)
        file_index.types = self._extract_types(code)

        # Count async/await keywords
        file_index.async_count = len(re.findall(r"\basync\b", code))
        file_index.await_count = len(re.findall(r"\bawait\b", code))
        file_index.todo_count = len(re.findall(r"//\s*(?:TODO|FIXME)\b", content))

        return file_index

    def _extract_imports(self, code: str) -> list[tuple[str, int]]:
        """Extract import statements."""
        imports = []
        # Matches: import Vapor or import struct Vapor.Application
        pattern = re.compile(r"^\s*import\s+(?:(?:class|struct|enum|protocol|let|var)\s+)?([\w.]+)", re.MULTILINE)
        for match in pattern.finditer(code):
            line = code[: match.start()].count("\n") + 1
            imports.append((match.group(1), line))
        return imports

    def _extract_types(self, code: str) -> list[tuple[str, str, int]]:
        """Extract type declarations (class, struct, enum, protocol, actor)."""
        types = []
        # Matches: struct User, class UserService, actor DBClient, protocol Repository, enum State
        pattern = re.compile(r"\b(struct|class|enum|protocol|actor)\s+(\w+)\b", re.MULTILINE)
        for match in pattern.finditer(code):
            line = code[: match.start()].count("\n") + 1
            types.append((match.group(1), match.group(2), line))
        return types

    # Query methods
    def count_import(self, module_name: str) -> int:
        """Count files importing a specific module."""
        count = 0
        for file_idx in self.files.values():
            if any(imp[0] == module_name for imp in file_idx.imports):
                count += 1
        return count

    def count_dependency(self, dep_name: str) -> bool:
        """Check if a dependency is present in Package.swift."""
        return any(dep_name.lower() in d.lower() for d in self.dependencies)

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

    def get_test_files(self) -> list[SwiftFileIndex]:
        """Get all test files."""
        return [f for f in self.files.values() if f.is_test]

    def get_non_test_files(self) -> list[SwiftFileIndex]:
        """Get all non-test files."""
        return [f for f in self.files.values() if not f.is_test]

    def get_files_by_role(self, role: str) -> list[SwiftFileIndex]:
        """Get all files with the given role."""
        return [f for f in self.files.values() if f.role == role]


def infer_swift_file_role(relative_path: str) -> str:
    """Infer the role of a Swift file from its path."""
    parts = Path(relative_path).parts
    lower_parts = [p.lower() for p in parts]
    filename = Path(relative_path).name

    # Test file detection
    if "test" in lower_parts or "tests" in lower_parts:
        return "test"
    if filename.endswith(("Test.swift", "Tests.swift", "Spec.swift", "Specs.swift")):
        return "test"

    # Content-based roles
    if any(p in ("controller", "controllers", "api", "endpoints", "routes") for p in lower_parts) or filename.endswith("Controller.swift"):
        return "api"
    if any(p in ("service", "services", "usecase", "usecases", "domain") for p in lower_parts):
        return "service"
    if any(p in ("repository", "repositories", "db", "database", "persistence") for p in lower_parts):
        return "db"
    if any(p in ("model", "models", "entity", "entities", "dto", "dtos") for p in lower_parts):
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

        # Line comment
        if char == "/" and nxt == "/":
            while i < length and content[i] != "\n":
                result[i] = " "
                i += 1
            continue

        # Block comment
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

        # Multiline string (triple double quotes)
        if char == '"' and nxt == '"' and i + 2 < length and content[i + 2] == '"':
            result[i] = result[i + 1] = result[i + 2] = " "
            i += 3
            while i < length:
                if content[i] == '"' and i + 2 < length and content[i + 1] == '"' and content[i + 2] == '"':
                    result[i] = result[i + 1] = result[i + 2] = " "
                    i += 3
                    break
                if content[i] != "\n":
                    result[i] = " "
                i += 1
            continue

        # Regular string literal
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

        i += 1

    return "".join(result)


def make_evidence(
    index: SwiftIndex,
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
