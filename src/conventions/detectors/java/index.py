"""Java code indexer using regex-based analysis."""

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
    "enum",
    "@interface",
)

VISIBILITY_MODIFIERS = ("public", "private", "protected")


@dataclass
class JavaFileIndex:
    """Index of a single Java file."""

    path: Path
    relative_path: str
    role: str  # main, test, build, api, service, db, model
    parse_error: Optional[str] = None

    package: Optional[str] = None
    source_set: Optional[str] = None  # main, test, etc.
    module: Optional[str] = None  # Gradle/Maven module this file belongs to

    # Extracted declarations
    imports: list[tuple[str, int]] = field(default_factory=list)  # (import_path, line)
    functions: list["JavaFunction"] = field(default_factory=list)
    classes: list["JavaClass"] = field(default_factory=list)
    annotations: list[tuple[str, int]] = field(default_factory=list)  # (name, line)

    # Cheap counters
    stream_count: int = 0
    optional_count: int = 0
    lambda_count: int = 0  # -> count
    todo_count: int = 0  # TODO/FIXME count

    lines: list[str] = field(default_factory=list)

    @property
    def is_test(self) -> bool:
        """Whether this file holds tests."""
        return self.role == "test"


@dataclass
class JavaFunction:
    """A Java method declaration."""

    name: str
    line: int
    visibility: str  # public, private, protected, package-private
    is_static: bool = False
    is_final: bool = False
    return_type: Optional[str] = None

    @property
    def is_public(self) -> bool:
        """Whether this is a public function."""
        return self.visibility == "public"


@dataclass
class JavaClass:
    """A class-like declaration (class, interface, record, enum, annotation)."""

    name: str
    line: int
    kind: str  # class, interface, record, enum, @interface
    visibility: str
    annotations: list[str] = field(default_factory=list)


class JavaIndex:
    """
    Index of Java files in a repository.

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
        self.files: dict[str, JavaFileIndex] = {}
        self._built = False

    def build(self) -> None:
        """Build the index by scanning all Java files."""
        if self._built:
            return

        for file_path in walk_files(
            self.repo_root,
            extensions={".java"},
            max_files=self.max_files,
            exclude_patterns=self.exclude_patterns,
        ):
            file_index = self._index_file(file_path)
            self.files[file_index.relative_path] = file_index

        self._built = True

    def _index_file(self, file_path: Path) -> JavaFileIndex:
        """Index a single Java file."""
        relative_path = get_relative_path(file_path, self.repo_root)

        file_index = JavaFileIndex(
            path=file_path,
            relative_path=relative_path,
            role=infer_java_file_role(relative_path),
            source_set=infer_source_set(relative_path),
            module=infer_module(relative_path),
        )

        content = read_file_safe(file_path)
        if content is None:
            file_index.parse_error = "Could not read file"
            return file_index

        file_index.lines = content.splitlines()

        # Strip comments and strings
        code = strip_comments_and_strings(content)

        file_index.package = self._extract_package(code)
        file_index.imports = self._extract_imports(code)
        file_index.functions = self._extract_functions(code)
        file_index.classes = self._extract_classes(code)
        file_index.annotations = self._extract_annotations(code)

        # Cheap counters
        file_index.stream_count = len(re.findall(r"\.stream\b", code))
        file_index.optional_count = len(re.findall(r"\bOptional\b", code))
        file_index.lambda_count = len(re.findall(r"->", code))
        file_index.todo_count = len(re.findall(r"//\s*(?:TODO|FIXME)\b", content)) + len(re.findall(r"/\*\s*(?:TODO|FIXME)\b", content))

        return file_index

    def _extract_package(self, code: str) -> Optional[str]:
        """Extract package declaration."""
        match = re.search(r"^[ \t]*package\s+([\w.]+)", code, re.MULTILINE)
        return match.group(1) if match else None

    def _extract_imports(self, code: str) -> list[tuple[str, int]]:
        """Extract import statements."""
        imports = []
        for match in re.finditer(r"^[ \t]*import\s+(?:static\s+)?([\w.*]+)", code, re.MULTILINE):
            line = code[: match.start()].count("\n") + 1
            imports.append((match.group(1), line))
        return imports

    def _extract_functions(self, code: str) -> list[JavaFunction]:
        """Extract function declarations."""
        functions = []
        # Match methods: visibility modifiers, optional static/final/abstract, optional return type, name, parameters
        pattern = re.compile(
            r"^[ \t]*"
            r"((?:(?:public|private|protected|static|final|abstract|synchronized|default)\s+)+)"
            r"(?:([\w.<>?, \[\]]+?)\s+)?"  # return type (optional for constructors)
            r"(\w+)\s*\(",
            re.MULTILINE,
        )

        for match in pattern.finditer(code):
            modifiers = match.group(1) or ""
            return_type = match.group(2)
            name = match.group(3)
            # Skip common non-method keywords that can trigger false positives
            if name in ("class", "interface", "record", "enum", "new", "return", "throw", "extends", "implements", "if", "for", "while", "switch"):
                continue

            line = code[: match.start()].count("\n") + 1

            functions.append(
                JavaFunction(
                    name=name,
                    line=line,
                    visibility=_extract_visibility(modifiers),
                    is_static="static" in modifiers,
                    is_final="final" in modifiers,
                    return_type=return_type,
                )
            )
        return functions

    def _extract_classes(self, code: str) -> list[JavaClass]:
        """Extract class-like declarations."""
        classes = []
        kinds = "|".join(re.escape(k) for k in CLASS_KINDS)
        pattern = re.compile(
            r"^[ \t]*"
            r"((?:(?:public|private|protected|static|final|abstract)\s+)*)"
            rf"({kinds})\s+(\w+)",
            re.MULTILINE,
        )

        for match in pattern.finditer(code):
            modifiers = match.group(1) or ""
            kind = match.group(2)
            name = match.group(3)
            line = code[: match.start()].count("\n") + 1

            classes.append(
                JavaClass(
                    name=name,
                    line=line,
                    kind=kind,
                    visibility=_extract_visibility(modifiers),
                    annotations=_annotations_above(code, match.start()),
                )
            )
        return classes

    def _extract_annotations(self, code: str) -> list[tuple[str, int]]:
        """Extract annotation usages."""
        annotations = []
        for match in re.finditer(r"@(\w+)", code):
            line = code[: match.start()].count("\n") + 1
            annotations.append((match.group(1), line))
        return annotations

    # Query methods
    def find_imports_matching(
        self,
        pattern: str,
        limit: int = 50,
    ) -> list[tuple[str, str, int]]:
        """Find imports containing `pattern`. Returns (file_path, import_path, line)."""
        results = []
        for rel_path, file_idx in self.files.items():
            for import_path, line in file_idx.imports:
                if pattern in import_path:
                    results.append((rel_path, import_path, line))
                    if len(results) >= limit:
                        return results
        return results

    def count_imports_matching(self, pattern: str) -> int:
        """Count files importing something matching `pattern`."""
        count = 0
        for file_idx in self.files.values():
            if any(pattern in import_path for import_path, _ in file_idx.imports):
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
                if exclude_imports and _is_import_line(file_idx.lines, line):
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
                if not _is_import_line(file_idx.lines, line):
                    count += 1

        return count

    def find_annotation(
        self,
        name: str,
        limit: int = 50,
    ) -> list[tuple[str, int]]:
        """Find usages of annotation `name`. Returns (file_path, line)."""
        results = []
        for rel_path, file_idx in self.files.items():
            for annotation, line in file_idx.annotations:
                if annotation == name:
                    results.append((rel_path, line))
                    if len(results) >= limit:
                        return results
        return results

    def count_annotation(self, name: str) -> int:
        """Count usages of annotation `name` across all files."""
        return sum(
            sum(1 for annotation, _ in f.annotations if annotation == name)
            for f in self.files.values()
        )

    def get_test_files(self) -> list[JavaFileIndex]:
        """Get all test files."""
        return [f for f in self.files.values() if f.is_test]

    def get_non_test_files(self) -> list[JavaFileIndex]:
        """Get all non-test files."""
        return [f for f in self.files.values() if not f.is_test]

    def get_files_by_role(self, role: str) -> list[JavaFileIndex]:
        """Get all files with the given role."""
        return [f for f in self.files.values() if f.role == role]


def infer_source_set(relative_path: str) -> Optional[str]:
    """Infer the source set from path like `src/main/java/...`."""
    parts = Path(relative_path).parts
    for i, part in enumerate(parts):
        if part == "src" and i + 1 < len(parts):
            return parts[i + 1]
    return None


def infer_module(relative_path: str) -> Optional[str]:
    """Infer the Maven/Gradle module (the path segment above `src/`)."""
    parts = Path(relative_path).parts
    for i, part in enumerate(parts):
        if part == "src" and i > 0:
            return parts[i - 1]
    return None


def infer_java_file_role(relative_path: str) -> str:
    """Infer the role of a Java file from its path."""
    parts = Path(relative_path).parts
    lower_parts = [p.lower() for p in parts]
    filename = Path(relative_path).name
    source_set = infer_source_set(relative_path)

    # Test source sets take precedence
    if source_set in ("test", "testFixtures") or "test" in lower_parts:
        return "test"
    if filename.endswith(("Test.java", "Tests.java", "IT.java", "TestCase.java")):
        return "test"

    # Content-based roles
    if any(p in ("controller", "controllers", "api", "routes", "routing", "endpoints", "resources") for p in lower_parts):
        return "api"
    if any(p in ("service", "services", "usecase", "usecases", "domain") for p in lower_parts):
        return "service"
    if any(p in ("repository", "repositories", "dao", "db", "database", "persistence", "datasource") for p in lower_parts):
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

        # Java 15+ Text Blocks """
        if content.startswith('"""', i):
            result[i] = result[i + 1] = result[i + 2] = " "
            i += 3
            while i < length and not content.startswith('"""', i):
                if content[i] != "\n":
                    result[i] = " "
                i += 1
            if i < length:
                result[i] = result[i + 1] = result[i + 2] = " "
                i += 3
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
    return "package-private"


def _is_import_line(lines: list[str], line_1_indexed: int) -> bool:
    """Check if the given line is an import statement."""
    if line_1_indexed < 1 or line_1_indexed > len(lines):
        return False
    stripped = lines[line_1_indexed - 1].strip()
    return stripped.startswith(("import ", "package "))


def _annotations_above(code: str, index: int) -> list[str]:
    """Find annotations placed directly above the declaration at `index`."""
    chunk = code[max(0, index - 400) : index]
    annotations = []

    # Simple scanner moving backwards
    lines = chunk.splitlines()
    for line in reversed(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("@"):
            match = re.search(r"@(\w+)", stripped)
            if match:
                annotations.append(match.group(1))
            continue
        # If we see any non-blank line that doesn't start with @, stop scanning
        break

    return list(reversed(annotations))


def make_evidence(
    index: JavaIndex,
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
