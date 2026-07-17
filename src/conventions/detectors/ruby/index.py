"""Ruby code indexer using regex-based analysis."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from ...fs import get_relative_path, read_file_safe, walk_files
from ...schemas import EvidenceSnippet


@dataclass
class RubyFileIndex:
    """Index of a single Ruby file."""

    path: Path
    relative_path: str
    role: str  # main, test, build, api, service, db, model
    parse_error: Optional[str] = None

    class_names: list[str] = field(default_factory=list)
    module_names: list[str] = field(default_factory=list)
    requires: list[tuple[str, int]] = field(default_factory=list)  # (require_path, line)
    associations: list[tuple[str, str, int]] = field(default_factory=list)  # (type, target, line)

    todo_count: int = 0
    lines: list[str] = field(default_factory=list)

    @property
    def is_test(self) -> bool:
        """Whether this file holds tests."""
        return self.role == "test"


class RubyIndex:
    """
    Index of Ruby files in a repository.

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
        self.files: dict[str, RubyFileIndex] = {}
        self.gems: set[str] = set()
        self._built = False

    def build(self) -> None:
        """Build the index by scanning all Ruby files and Gemfile."""
        if self._built:
            return

        # Scan Gemfile
        gemfile_path = self.repo_root / "Gemfile"
        if gemfile_path.exists() and gemfile_path.is_file():
            self._parse_gemfile(gemfile_path)

        for file_path in walk_files(
            self.repo_root,
            extensions={".rb"},
            max_files=self.max_files,
            exclude_patterns=self.exclude_patterns,
        ):
            file_index = self._index_file(file_path)
            self.files[file_index.relative_path] = file_index

        self._built = True

    def _parse_gemfile(self, path: Path) -> None:
        """Parse Gemfile to extract declared gems."""
        content = read_file_safe(path)
        if not content:
            return
        # Matches: gem 'rails', gem "rspec-rails"
        pattern = re.compile(r"^\s*gem\s+['\"]([^'\"]+)['\"]", re.MULTILINE)
        for match in pattern.finditer(content):
            self.gems.add(match.group(1))

    def _index_file(self, file_path: Path) -> RubyFileIndex:
        """Index a single Ruby file."""
        relative_path = get_relative_path(file_path, self.repo_root)

        file_index = RubyFileIndex(
            path=file_path,
            relative_path=relative_path,
            role=infer_ruby_file_role(relative_path),
        )

        content = read_file_safe(file_path)
        if content is None:
            file_index.parse_error = "Could not read file"
            return file_index

        file_index.lines = content.splitlines()

        # Strip comments and strings
        code = strip_comments_and_strings(content)

        file_index.class_names = self._extract_classes(code)
        file_index.module_names = self._extract_modules(code)
        file_index.requires = self._extract_requires(code)
        file_index.associations = self._extract_associations(code)

        file_index.todo_count = len(re.findall(r"#\s*(?:TODO|FIXME)\b", content))

        return file_index

    def _extract_classes(self, code: str) -> list[str]:
        """Extract class declarations."""
        # Matches: class User or class Admin::User
        pattern = re.compile(r"^\s*class\s+([\w::]+)", re.MULTILINE)
        return [match.group(1) for match in pattern.finditer(code)]

    def _extract_modules(self, code: str) -> list[str]:
        """Extract module declarations."""
        # Matches: module Services
        pattern = re.compile(r"^\s*module\s+([\w::]+)", re.MULTILINE)
        return [match.group(1) for match in pattern.finditer(code)]

    def _extract_requires(self, code: str) -> list[tuple[str, int]]:
        """Extract require/require_relative statements."""
        requires = []
        # Matches: require 'rails' or require_relative 'lib/foo'
        pattern = re.compile(r"^\s*(?:require|require_relative)\s+['\"]([^'\"]+)['\"]", re.MULTILINE)
        for match in pattern.finditer(code):
            line = code[: match.start()].count("\n") + 1
            requires.append((match.group(1), line))
        return requires

    def _extract_associations(self, code: str) -> list[tuple[str, str, int]]:
        """Extract ActiveRecord associations (has_many, belongs_to, etc.)."""
        associations = []
        # Matches: has_many :posts or belongs_to :user
        pattern = re.compile(
            r"\b(has_many|belongs_to|has_one|has_and_belongs_to_many)\s+:(\w+)",
            re.MULTILINE,
        )
        for match in pattern.finditer(code):
            line = code[: match.start()].count("\n") + 1
            associations.append((match.group(1), match.group(2), line))
        return associations

    # Query methods
    def count_gem(self, gem_name: str) -> bool:
        """Check if a gem is present in the Gemfile."""
        return gem_name in self.gems

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

    def get_test_files(self) -> list[RubyFileIndex]:
        """Get all test files."""
        return [f for f in self.files.values() if f.is_test]

    def get_non_test_files(self) -> list[RubyFileIndex]:
        """Get all non-test files."""
        return [f for f in self.files.values() if not f.is_test]

    def get_files_by_role(self, role: str) -> list[RubyFileIndex]:
        """Get all files with the given role."""
        return [f for f in self.files.values() if f.role == role]


def infer_ruby_file_role(relative_path: str) -> str:
    """Infer the role of a Ruby file from its path."""
    parts = Path(relative_path).parts
    lower_parts = [p.lower() for p in parts]
    filename = Path(relative_path).name

    # Test file detection
    if "spec" in lower_parts or "test" in lower_parts:
        return "test"
    if filename.endswith(("_spec.rb", "_test.rb")):
        return "test"

    # Content-based roles (standard Rails conventions)
    if any(p in ("controller", "controllers") for p in lower_parts) or filename.endswith("_controller.rb"):
        return "api"
    if any(p in ("service", "services", "usecase", "usecases", "domain") for p in lower_parts):
        return "service"
    if any(p in ("repository", "repositories", "db", "database") for p in lower_parts) or "migrate" in lower_parts:
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

        # Line comment
        if char == "#":
            while i < length and content[i] != "\n":
                result[i] = " "
                i += 1
            continue

        # Regular string or char literal
        if char in ('"', "'"):
            quote = char
            result[i] = " "
            i += 1
            while i < length and content[i] != quote:
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
            if i < length and content[i] == quote:
                result[i] = " "
                i += 1
            continue

        i += 1

    return "".join(result)


def make_evidence(
    index: RubyIndex,
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
