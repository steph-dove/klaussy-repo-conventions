"""C# / .NET code indexer using regex-based analysis."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from ...fs import get_relative_path, read_file_safe, walk_files
from ...schemas import EvidenceSnippet

CLASS_KINDS = (
    "class",
    "interface",
    "record",
    "struct",
)

VISIBILITY_MODIFIERS = ("public", "private", "protected", "internal")


@dataclass
class CSharpFileIndex:
    """Index of a single C# file."""

    path: Path
    relative_path: str
    role: str  # main, test, build, api, service, db, model
    parse_error: Optional[str] = None

    namespace: Optional[str] = None
    module: Optional[str] = None  # The .csproj module this file belongs to

    # Extracted declarations
    usings: list[tuple[str, int]] = field(default_factory=list)  # (using_namespace, line)
    functions: list["CSharpFunction"] = field(default_factory=list)
    classes: list["CSharpClass"] = field(default_factory=list)
    attributes: list[tuple[str, int]] = field(default_factory=list)  # (name, line)

    # Cheap counters
    async_count: int = 0
    await_count: int = 0
    linq_count: int = 0  # usage of LINQ extension methods or query expressions
    nullable_enabled: bool = False
    todo_count: int = 0

    lines: list[str] = field(default_factory=list)

    @property
    def is_test(self) -> bool:
        """Whether this file holds tests."""
        return self.role == "test"


@dataclass
class CSharpFunction:
    """A C# method declaration."""

    name: str
    line: int
    visibility: str  # public, private, protected, internal, private-protected, etc.
    is_static: bool = False
    is_async: bool = False
    return_type: Optional[str] = None

    @property
    def is_public(self) -> bool:
        """Whether this is a public function."""
        return self.visibility == "public"


@dataclass
class CSharpClass:
    """A class-like declaration (class, interface, record, struct)."""

    name: str
    line: int
    kind: str  # class, interface, record, struct
    visibility: str
    attributes: list[str] = field(default_factory=list)
    base_types: list[str] = field(default_factory=list)


class CSharpIndex:
    """
    Index of C# files in a repository.

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
        self.files: dict[str, CSharpFileIndex] = {}
        self._built = False

    def build(self) -> None:
        """Build the index by scanning all C# files."""
        if self._built:
            return

        for file_path in walk_files(
            self.repo_root,
            extensions={".cs"},
            max_files=self.max_files,
            exclude_patterns=self.exclude_patterns,
        ):
            file_index = self._index_file(file_path)
            self.files[file_index.relative_path] = file_index

        self._built = True

    def _index_file(self, file_path: Path) -> CSharpFileIndex:
        """Index a single C# file."""
        relative_path = get_relative_path(file_path, self.repo_root)

        file_index = CSharpFileIndex(
            path=file_path,
            relative_path=relative_path,
            role=infer_csharp_file_role(relative_path),
            module=infer_csproj_module(relative_path),
        )

        content = read_file_safe(file_path)
        if content is None:
            file_index.parse_error = "Could not read file"
            return file_index

        file_index.lines = content.splitlines()

        # Check for #nullable enable
        file_index.nullable_enabled = "#nullable enable" in content

        # Strip comments and strings
        code = strip_comments_and_strings(content)

        file_index.namespace = self._extract_namespace(code)
        file_index.usings = self._extract_usings(code)
        file_index.functions = self._extract_functions(code)
        file_index.classes = self._extract_classes(code)
        file_index.attributes = self._extract_attributes(code)

        # Cheap counters
        file_index.async_count = len(re.findall(r"\basync\b", code))
        file_index.await_count = len(re.findall(r"\bawait\b", code))
        file_index.linq_count = len(re.findall(r"\.Select\b|\.Where\b|\.ToList\b|\.FirstOrDefault\b|from\s+\w+\s+in\b", code))
        file_index.todo_count = len(re.findall(r"//\s*(?:TODO|FIXME)\b", content)) + len(re.findall(r"/\*\s*(?:TODO|FIXME)\b", content))

        return file_index

    def _extract_namespace(self, code: str) -> Optional[str]:
        """Extract namespace declaration (both block and file-scoped)."""
        match = re.search(r"^[ \t]*namespace\s+([\w.]+);?", code, re.MULTILINE)
        return match.group(1) if match else None

    def _extract_usings(self, code: str) -> list[tuple[str, int]]:
        """Extract using directives."""
        usings = []
        # Matches: using System; or using static System.Math;
        for match in re.finditer(r"^[ \t]*using\s+(?:static\s+)?([\w.]+);", code, re.MULTILINE):
            line = code[: match.start()].count("\n") + 1
            usings.append((match.group(1), line))
        return usings

    def _extract_functions(self, code: str) -> list[CSharpFunction]:
        """Extract C# method declarations."""
        functions = []
        # Match methods: modifiers, optional async, optional return type, name, parameters
        pattern = re.compile(
            r"^[ \t]*"
            r"((?:(?:public|private|protected|internal|static|async|override|virtual|abstract|sealed|partial)\s+)+)"
            r"(?:([\w.<>?, \[\]]+?)\s+)?"  # return type (optional for constructors)
            r"(\w+)\s*\(",
            re.MULTILINE,
        )

        for match in pattern.finditer(code):
            modifiers = match.group(1) or ""
            return_type = match.group(2)
            name = match.group(3)
            if name in ("class", "interface", "record", "struct", "namespace", "using", "new", "return", "throw", "if", "for", "foreach", "while", "switch"):
                continue

            line = code[: match.start()].count("\n") + 1

            functions.append(
                CSharpFunction(
                    name=name,
                    line=line,
                    visibility=_extract_visibility(modifiers),
                    is_static="static" in modifiers,
                    is_async="async" in modifiers,
                    return_type=return_type,
                )
            )
        return functions

    def _extract_classes(self, code: str) -> list[CSharpClass]:
        """Extract class-like declarations."""
        classes = []
        kinds = "|".join(re.escape(k) for k in CLASS_KINDS)
        # Matches public class Foo : IBar, QBaz
        pattern = re.compile(
            r"^[ \t]*"
            r"((?:(?:public|private|protected|internal|static|sealed|abstract|partial)\s+)*)"
            rf"({kinds})\s+(\w+)"
            r"(?:\s*:\s*([\w.<>?,\s]+))?",
            re.MULTILINE,
        )

        for match in pattern.finditer(code):
            modifiers = match.group(1) or ""
            kind = match.group(2)
            name = match.group(3)
            base_types_str = match.group(4) or ""
            line = code[: match.start()].count("\n") + 1

            base_types = [t.strip() for t in base_types_str.split(",") if t.strip()]

            classes.append(
                CSharpClass(
                    name=name,
                    line=line,
                    kind=kind,
                    visibility=_extract_visibility(modifiers),
                    attributes=_attributes_above(code, match.start()),
                    base_types=base_types,
                )
            )
        return classes

    def _extract_attributes(self, code: str) -> list[tuple[str, int]]:
        """Extract attribute usages [AttributeName]."""
        attributes = []
        # Simple attribute matching: [HttpGet] or [Route("api/users")]
        # Exclude common square brackets in code like arrays or LINQ
        for match in re.finditer(r"^[ \t]*\[(\w+)(?:\([^\]]*\))?\]", code, re.MULTILINE):
            line = code[: match.start()].count("\n") + 1
            attributes.append((match.group(1), line))
        return attributes

    # Query methods
    def find_imports_matching(
        self,
        pattern: str,
        limit: int = 50,
    ) -> list[tuple[str, str, int]]:
        """Find usings containing `pattern`. Returns (file_path, using_namespace, line)."""
        results = []
        for rel_path, file_idx in self.files.items():
            for using_path, line in file_idx.usings:
                if pattern in using_path:
                    results.append((rel_path, using_path, line))
                    if len(results) >= limit:
                        return results
        return results

    def count_imports_matching(self, pattern: str, exclude_tests: bool = False) -> int:
        """Count files importing/using something matching `pattern`.

        Set `exclude_tests` when deciding what the *project* uses: a library
        referenced only by the test suite is not a production convention.
        """
        count = 0
        for file_idx in self.files.values():
            if exclude_tests and file_idx.is_test:
                continue
            if any(pattern in using_path for using_path, _ in file_idx.usings):
                count += 1
        return count

    def search_pattern(
        self,
        pattern: str,
        limit: int = 100,
        exclude_tests: bool = False,
        exclude_imports: bool = False,
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
                if exclude_imports and _is_using_line(file_idx.lines, line):
                    continue
                results.append((rel_path, line, match.group(0)))
                if len(results) >= limit:
                    return results

        return results

    def count_pattern(
        self,
        pattern: str,
        exclude_tests: bool = False,
        exclude_imports: bool = False,
    ) -> int:
        """Count regex occurrences across all files."""
        count = 0
        compiled = re.compile(pattern, re.MULTILINE)

        for file_idx in self.files.values():
            if exclude_tests and file_idx.is_test:
                continue

            content = "\n".join(file_idx.lines)
            if not exclude_imports:
                count += len(compiled.findall(content))
                continue

            for match in compiled.finditer(content):
                line = content[: match.start()].count("\n") + 1
                if not _is_using_line(file_idx.lines, line):
                    count += 1

        return count

    def find_annotation(
        self,
        name: str,
        limit: int = 50,
    ) -> list[tuple[str, int]]:
        """Find usages of attribute `name`. Returns (file_path, line)."""
        results = []
        for rel_path, file_idx in self.files.items():
            for attr, line in file_idx.attributes:
                if attr == name:
                    results.append((rel_path, line))
                    if len(results) >= limit:
                        return results
        return results

    def count_annotation(self, name: str) -> int:
        """Count usages of attribute `name` across all files."""
        return sum(
            sum(1 for attr, _ in f.attributes if attr == name)
            for f in self.files.values()
        )

    def get_test_files(self) -> list[CSharpFileIndex]:
        """Get all test files."""
        return [f for f in self.files.values() if f.is_test]

    def get_non_test_files(self) -> list[CSharpFileIndex]:
        """Get all non-test files."""
        return [f for f in self.files.values() if not f.is_test]

    def get_files_by_role(self, role: str) -> list[CSharpFileIndex]:
        """Get all files with the given role."""
        return [f for f in self.files.values() if f.role == role]


def infer_csproj_module(relative_path: str) -> Optional[str]:
    """Infer the project module name from path."""
    path = Path(relative_path)
    # Search upwards from file path for a directory containing a .csproj file
    current = path.parent
    while current and current != Path("."):
        csproj_files = list(current.glob("*.csproj"))
        if csproj_files:
            return csproj_files[0].stem
        if current.parent == current:
            break
        current = current.parent
    return None


# Dotted name segments that mark a directory as holding tests. .NET names test
# projects after the project under test -- `Newtonsoft.Json.Tests`,
# `MyApp.UnitTests` -- so an exact "tests" path component is not enough.
_TEST_DIR_SEGMENTS = frozenset({
    "test",
    "tests",
    "testing",
    "unittest",
    "unittests",
    "integrationtest",
    "integrationtests",
    "functionaltest",
    "functionaltests",
    "spec",
    "specs",
    "benchmark",
    "benchmarks",
})


def _is_test_dir(part: str) -> bool:
    """Whether a path component names a test project or directory.

    Matches on dotted segments rather than a suffix, so `Newtonsoft.Json.Tests`
    counts while `latest` (which ends in "test") does not.
    """
    return any(segment in _TEST_DIR_SEGMENTS for segment in part.lower().split("."))


def infer_csharp_file_role(relative_path: str) -> str:
    """Infer the role of a C# file from its path."""
    parts = Path(relative_path).parts
    lower_parts = [p.lower() for p in parts]
    filename = Path(relative_path).name

    # Test file detection
    if any(_is_test_dir(p) for p in parts):
        return "test"
    if filename.endswith(("Test.cs", "Tests.cs", "Spec.cs", "Specs.cs")):
        return "test"

    # Content-based roles
    if any(p in ("controller", "controllers", "api", "endpoints", "routes") for p in lower_parts):
        return "api"
    if any(p in ("service", "services", "usecase", "usecases", "domain") for p in lower_parts):
        return "service"
    if any(p in ("repository", "repositories", "dao", "db", "database", "context", "persistence") for p in lower_parts):
        return "db"
    if any(p in ("model", "models", "entity", "entities", "dto", "dtos", "schema") for p in lower_parts):
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

        # Interpolated/verbatim string $@"..." or @$"..." or @"..."
        if (char == "@" and nxt == '"') or (char == "$" and nxt == "@") or (char == "@" and nxt == "$"):
            result[i] = result[i + 1] = " "
            i += 2
            while i < length:
                if content[i] == '"':
                    # In verbatim strings, "" represents a single double-quote
                    if i + 1 < length and content[i + 1] == '"':
                        result[i] = result[i + 1] = " "
                        i += 2
                        continue
                    else:
                        result[i] = " "
                        i += 1
                        break
                if content[i] != "\n":
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


def _extract_visibility(modifiers: str) -> str:
    """Extract visibility modifier."""
    for modifier in VISIBILITY_MODIFIERS:
        if re.search(rf"\b{modifier}\b", modifiers):
            return modifier
    return "private"


def _is_using_line(lines: list[str], line_1_indexed: int) -> bool:
    """Check if the given line is a using statement."""
    if line_1_indexed < 1 or line_1_indexed > len(lines):
        return False
    stripped = lines[line_1_indexed - 1].strip()
    return stripped.startswith("using ")


def _attributes_above(code: str, index: int) -> list[str]:
    """Find C# attributes placed directly above the declaration at `index`."""
    chunk = code[max(0, index - 400) : index]
    attributes = []

    lines = chunk.splitlines()
    for line in reversed(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("[") and stripped.endswith("]"):
            match = re.search(r"\[(\w+)", stripped)
            if match:
                attributes.append(match.group(1))
            continue
        break

    return list(reversed(attributes))


def make_evidence(
    index: CSharpIndex,
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
