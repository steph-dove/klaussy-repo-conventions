"""PHP code indexer using regex-based analysis."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from ...fs import get_relative_path, read_file_safe, walk_files
from ...schemas import EvidenceSnippet


@dataclass
class PHPFileIndex:
    """Index of a single PHP file."""

    path: Path
    relative_path: str
    role: str  # main, test, build, api, service, db, model
    parse_error: Optional[str] = None

    namespace: Optional[str] = None
    uses: list[tuple[str, int]] = field(default_factory=list)  # (use_namespace, line)
    types: list[tuple[str, str, int]] = field(default_factory=list)  # (kind, name, line)

    todo_count: int = 0
    lines: list[str] = field(default_factory=list)

    @property
    def is_test(self) -> bool:
        """Whether this file holds tests."""
        return self.role == "test"


class PHPIndex:
    """
    Index of PHP files in a repository.

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
        self.files: dict[str, PHPFileIndex] = {}
        self.dependencies: set[str] = set()
        self._built = False

    def build(self) -> None:
        """Build the index by scanning all PHP files and composer.json."""
        if self._built:
            return

        # Scan composer.json
        composer_json = self.repo_root / "composer.json"
        if composer_json.exists() and composer_json.is_file():
            self._parse_composer_json(composer_json)

        for file_path in walk_files(
            self.repo_root,
            extensions={".php"},
            max_files=self.max_files,
            exclude_patterns=self.exclude_patterns,
        ):
            file_index = self._index_file(file_path)
            self.files[file_index.relative_path] = file_index

        self._built = True

    def _parse_composer_json(self, path: Path) -> None:
        """Parse composer.json to extract dependencies."""
        content = read_file_safe(path)
        if not content:
            return
        try:
            data = json.loads(content)
            req = data.get("require", {})
            req_dev = data.get("require-dev", {})
            for key in req:
                self.dependencies.add(key)
            for key in req_dev:
                self.dependencies.add(key)
        except Exception:
            pass

    def _index_file(self, file_path: Path) -> PHPFileIndex:
        """Index a single PHP file."""
        relative_path = get_relative_path(file_path, self.repo_root)

        file_index = PHPFileIndex(
            path=file_path,
            relative_path=relative_path,
            role=infer_php_file_role(relative_path),
        )

        content = read_file_safe(file_path)
        if content is None:
            file_index.parse_error = "Could not read file"
            return file_index

        file_index.lines = content.splitlines()

        # Strip comments and strings
        code = strip_comments_and_strings(content)

        file_index.namespace = self._extract_namespace(code)
        file_index.uses = self._extract_uses(code)
        file_index.types = self._extract_types(code)

        file_index.todo_count = len(re.findall(r"//\s*(?:TODO|FIXME)\b", content)) + \
                                len(re.findall(r"/\*\s*(?:TODO|FIXME)\b", content)) + \
                                len(re.findall(r"#\s*(?:TODO|FIXME)\b", content))

        return file_index

    def _extract_namespace(self, code: str) -> Optional[str]:
        """Extract namespace declaration."""
        match = re.search(r"^\s*namespace\s+([^\s;{}]+)\s*;", code, re.MULTILINE)
        return match.group(1) if match else None

    def _extract_uses(self, code: str) -> list[tuple[str, int]]:
        """Extract use imports."""
        uses = []
        # Matches: use App\Models\User;
        pattern = re.compile(r"^\s*use\s+([^\s;{}]+)\s*;", re.MULTILINE)
        for match in pattern.finditer(code):
            line = code[: match.start()].count("\n") + 1
            uses.append((match.group(1), line))
        return uses

    def _extract_types(self, code: str) -> list[tuple[str, str, int]]:
        """Extract classes, interfaces, traits."""
        types = []
        # Matches: class UserController, interface UserRepository, trait Loggable
        pattern = re.compile(r"\b(class|interface|trait)\s+(\w+)\b", re.MULTILINE)
        for match in pattern.finditer(code):
            line = code[: match.start()].count("\n") + 1
            types.append((match.group(1), match.group(2), line))
        return types

    # Query methods
    def count_dependency(self, dep_name: str) -> bool:
        """Check if a composer dependency is present."""
        return dep_name in self.dependencies

    def count_use_matching(self, pattern: str) -> int:
        """Count files importing/using something matching `pattern`."""
        count = 0
        for file_idx in self.files.values():
            if any(pattern in use_path for use_path, _ in file_idx.uses):
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

    def get_test_files(self) -> list[PHPFileIndex]:
        """Get all test files."""
        return [f for f in self.files.values() if f.is_test]

    def get_non_test_files(self) -> list[PHPFileIndex]:
        """Get all non-test files."""
        return [f for f in self.files.values() if not f.is_test]

    def get_files_by_role(self, role: str) -> list[PHPFileIndex]:
        """Get all files with the given role."""
        return [f for f in self.files.values() if f.role == role]


def infer_php_file_role(relative_path: str) -> str:
    """Infer the role of a PHP file from its path."""
    parts = Path(relative_path).parts
    lower_parts = [p.lower() for p in parts]
    filename = Path(relative_path).name

    # Test file detection
    if "test" in lower_parts or "tests" in lower_parts:
        return "test"
    if filename.endswith(("Test.php", "Spec.php")):
        return "test"

    # Content-based roles
    if any(p in ("controller", "controllers", "api", "endpoints", "routes") for p in lower_parts) or filename.endswith("Controller.php"):
        return "api"
    if any(p in ("service", "services", "usecase", "usecases", "domain") for p in lower_parts):
        return "service"
    if any(p in ("repository", "repositories", "db", "database", "migrations") for p in lower_parts):
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

        # Line comment // or #
        if (char == "/" and nxt == "/") or char == "#":
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

        # Double-quoted string literal
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

        # Single-quoted string literal
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
    index: PHPIndex,
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
