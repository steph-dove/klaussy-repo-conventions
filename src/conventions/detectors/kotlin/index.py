"""Kotlin code indexer using regex-based analysis."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from ...fs import get_relative_path, read_file_safe, walk_files
from ...schemas import EvidenceSnippet

# Class-like declaration kinds, longest-first so `data class` wins over `class`.
CLASS_KINDS = (
    "annotation class",
    "value class",
    "inline class",
    "sealed interface",
    "sealed class",
    "data object",
    "data class",
    "enum class",
    "companion object",
    "interface",
    "object",
    "class",
)

VISIBILITY_MODIFIERS = ("public", "private", "protected", "internal")


@dataclass
class KotlinFileIndex:
    """Index of a single Kotlin file."""

    path: Path
    relative_path: str
    role: str  # main, test, androidTest, build, api, service, db, model, ui
    parse_error: Optional[str] = None

    package: Optional[str] = None
    source_set: Optional[str] = None  # main, test, commonMain, jvmMain, ...
    module: Optional[str] = None  # Gradle module this file belongs to

    # Extracted declarations
    imports: list[tuple[str, int]] = field(default_factory=list)  # (import_path, line)
    functions: list["KotlinFunction"] = field(default_factory=list)
    classes: list["KotlinClass"] = field(default_factory=list)
    annotations: list[tuple[str, int]] = field(default_factory=list)  # (name, line)
    properties: list[tuple[str, int, bool]] = field(default_factory=list)  # (name, line, is_var)

    # Cheap counters used by several detectors
    suspend_count: int = 0
    flow_count: int = 0
    not_null_assertion_count: int = 0  # `!!`
    safe_call_count: int = 0  # `?.`
    elvis_count: int = 0  # `?:`
    lateinit_count: int = 0

    lines: list[str] = field(default_factory=list)

    @property
    def is_test(self) -> bool:
        """Whether this file holds tests."""
        return self.role in ("test", "androidTest")


@dataclass
class KotlinFunction:
    """A function declaration."""

    name: str
    line: int
    visibility: str  # public, private, protected, internal
    is_suspend: bool = False
    is_inline: bool = False
    is_extension: bool = False
    return_type: Optional[str] = None

    @property
    def is_public(self) -> bool:
        """Kotlin declarations are public by default."""
        return self.visibility == "public"


@dataclass
class KotlinClass:
    """A class-like declaration (class, object, interface, enum, ...)."""

    name: str
    line: int
    kind: str  # class, data class, sealed class, object, interface, enum class, ...
    visibility: str
    annotations: list[str] = field(default_factory=list)

    @property
    def is_data(self) -> bool:
        """Whether this is a data class or data object."""
        return self.kind.startswith("data ")

    @property
    def is_sealed(self) -> bool:
        """Whether this is a sealed class or sealed interface."""
        return self.kind.startswith("sealed ")


class KotlinIndex:
    """
    Index of Kotlin files in a repository.

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
        self.files: dict[str, KotlinFileIndex] = {}
        self._built = False

    def build(self) -> None:
        """Build the index by scanning all Kotlin files."""
        if self._built:
            return

        for file_path in walk_files(
            self.repo_root,
            extensions={".kt", ".kts"},
            max_files=self.max_files,
            exclude_patterns=self.exclude_patterns,
        ):
            file_index = self._index_file(file_path)
            self.files[file_index.relative_path] = file_index

        self._built = True

    def _index_file(self, file_path: Path) -> KotlinFileIndex:
        """Index a single Kotlin file."""
        relative_path = get_relative_path(file_path, self.repo_root)

        file_index = KotlinFileIndex(
            path=file_path,
            relative_path=relative_path,
            role=infer_kotlin_file_role(relative_path),
            source_set=infer_source_set(relative_path),
            module=infer_module(relative_path),
        )

        content = read_file_safe(file_path)
        if content is None:
            file_index.parse_error = "Could not read file"
            return file_index

        file_index.lines = content.splitlines()

        # Strip comments and string literals before structural extraction so that
        # commented-out code and string contents don't register as declarations.
        code = strip_comments_and_strings(content)

        file_index.package = self._extract_package(code)
        file_index.imports = self._extract_imports(code)
        file_index.functions = self._extract_functions(code)
        file_index.classes = self._extract_classes(code)
        file_index.annotations = self._extract_annotations(code)
        file_index.properties = self._extract_properties(code)

        file_index.suspend_count = len(re.findall(r"\bsuspend\b", code))
        file_index.flow_count = len(re.findall(r"\bFlow\s*<", code))
        file_index.not_null_assertion_count = len(re.findall(r"!!", code))
        file_index.safe_call_count = len(re.findall(r"\?\.", code))
        file_index.elvis_count = len(re.findall(r"\?:", code))
        file_index.lateinit_count = len(re.findall(r"\blateinit\b", code))

        return file_index

    def _extract_package(self, code: str) -> Optional[str]:
        """Extract the package declaration."""
        # Leading whitespace is matched with [ \t]* rather than \s*: \s also
        # matches newlines, which would drag the match start back onto a
        # preceding blank line and report the wrong line number.
        match = re.search(r"^[ \t]*package\s+([\w.]+)", code, re.MULTILINE)
        return match.group(1) if match else None

    def _extract_imports(self, code: str) -> list[tuple[str, int]]:
        """Extract import statements."""
        imports = []
        for match in re.finditer(r"^[ \t]*import\s+([\w.*]+)", code, re.MULTILINE):
            line = code[: match.start()].count("\n") + 1
            imports.append((match.group(1), line))
        return imports

    def _extract_functions(self, code: str) -> list[KotlinFunction]:
        """Extract function declarations."""
        functions = []
        pattern = re.compile(
            r"^[ \t]*"
            r"((?:(?:public|private|protected|internal|open|override|abstract|final|"
            r"suspend|inline|operator|infix|tailrec|external|expect|actual)\s+)*)"
            r"fun\s+(?:<[^>]+>\s*)?"
            r"(?:([\w.<>?, \[\]]+?)\.)?"  # receiver type for extension functions
            r"(\w+)\s*\(",
            re.MULTILINE,
        )

        for match in pattern.finditer(code):
            modifiers = match.group(1) or ""
            receiver = match.group(2)
            name = match.group(3)
            line = code[: match.start()].count("\n") + 1

            functions.append(
                KotlinFunction(
                    name=name,
                    line=line,
                    visibility=_extract_visibility(modifiers),
                    is_suspend="suspend" in modifiers,
                    is_inline="inline" in modifiers,
                    is_extension=receiver is not None,
                    return_type=_extract_return_type(code, match.end()),
                )
            )
        return functions

    def _extract_classes(self, code: str) -> list[KotlinClass]:
        """Extract class-like declarations."""
        classes = []
        kinds = "|".join(re.escape(k) for k in CLASS_KINDS)
        pattern = re.compile(
            r"^[ \t]*"
            r"((?:(?:public|private|protected|internal|open|abstract|final|inner|"
            r"expect|actual)\s+)*)"
            rf"({kinds})\s+(\w+)",
            re.MULTILINE,
        )

        for match in pattern.finditer(code):
            modifiers = match.group(1) or ""
            kind = match.group(2)
            name = match.group(3)
            line = code[: match.start()].count("\n") + 1

            classes.append(
                KotlinClass(
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

    def _extract_properties(self, code: str) -> list[tuple[str, int, bool]]:
        """Extract val/var property declarations."""
        properties = []
        pattern = re.compile(
            r"^[ \t]*"
            r"(?:(?:public|private|protected|internal|open|override|abstract|final|"
            r"const|lateinit)\s+)*"
            r"(val|var)\s+(\w+)",
            re.MULTILINE,
        )
        for match in pattern.finditer(code):
            line = code[: match.start()].count("\n") + 1
            properties.append((match.group(2), line, match.group(1) == "var"))
        return properties

    # ------------------------------------------------------------------
    # Query helpers (mirrors the Go/Rust index surface)
    # ------------------------------------------------------------------

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
        """Search for a regex across all files. Returns (file_path, line, match).

        Set `exclude_imports` when counting usage of a symbol: an `import
        kotlinx.coroutines.GlobalScope` line otherwise reads as a call site.
        """
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
        """Count regex occurrences across all files.

        Set `exclude_imports` when counting usage of a symbol; see
        :meth:`search_pattern`.
        """
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

    def get_test_files(self) -> list[KotlinFileIndex]:
        """Get all test files."""
        return [f for f in self.files.values() if f.is_test]

    def get_non_test_files(self) -> list[KotlinFileIndex]:
        """Get all non-test files."""
        return [f for f in self.files.values() if not f.is_test]

    def get_files_by_role(self, role: str) -> list[KotlinFileIndex]:
        """Get all files with the given role."""
        return [f for f in self.files.values() if f.role == role]

    def get_script_files(self) -> list[KotlinFileIndex]:
        """Get all .kts script files (build scripts and the like)."""
        return [f for f in self.files.values() if f.relative_path.endswith(".kts")]

    def all_functions(self) -> list[tuple[str, KotlinFunction]]:
        """All functions across the repo as (file_path, function)."""
        return [(rel, fn) for rel, f in self.files.items() for fn in f.functions]

    def all_classes(self) -> list[tuple[str, KotlinClass]]:
        """All class-like declarations across the repo as (file_path, class)."""
        return [(rel, cls) for rel, f in self.files.items() for cls in f.classes]

    @property
    def modules(self) -> set[str]:
        """Gradle modules that contain Kotlin sources."""
        return {f.module for f in self.files.values() if f.module}


def _is_import_line(lines: list[str], line: int) -> bool:
    """Whether the 1-indexed `line` is an import or package declaration."""
    if line < 1 or line > len(lines):
        return False
    stripped = lines[line - 1].lstrip()
    return stripped.startswith(("import ", "package "))


def strip_comments_and_strings(content: str) -> str:
    """Blank out comments and string literals, preserving line/column offsets.

    Replacing rather than deleting keeps every byte offset stable, so line
    numbers computed against the stripped text still point at the real source.
    """
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

        # Block comment (Kotlin allows nesting)
        if char == "/" and nxt == "*":
            depth = 0
            while i < length:
                if content[i] == "/" and i + 1 < length and content[i + 1] == "*":
                    depth += 1
                    result[i] = result[i + 1] = " "
                    i += 2
                    continue
                if content[i] == "*" and i + 1 < length and content[i + 1] == "/":
                    depth -= 1
                    result[i] = result[i + 1] = " "
                    i += 2
                    if depth == 0:
                        break
                    continue
                if content[i] != "\n":
                    result[i] = " "
                i += 1
            continue

        # Raw string
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
                    break  # unterminated literal; don't run past the line
                result[i] = " "
                i += 1
            if i < length and content[i] == quote:
                result[i] = " "
                i += 1
            continue

        i += 1

    return "".join(result)


def _extract_visibility(modifiers: str) -> str:
    """Extract the visibility modifier, defaulting to Kotlin's implicit public."""
    for modifier in VISIBILITY_MODIFIERS:
        if re.search(rf"\b{modifier}\b", modifiers):
            return modifier
    return "public"


def _extract_return_type(code: str, params_start: int) -> Optional[str]:
    """Extract a function's declared return type by scanning past its parameters."""
    depth = 0
    i = params_start - 1

    while i < len(code):
        char = code[i]
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                break
        i += 1

    if i >= len(code):
        return None

    match = re.match(r"\s*:\s*([\w.<>?, \[\]]+)", code[i + 1 :])
    return match.group(1).strip() if match else None


def _annotations_above(code: str, decl_start: int) -> list[str]:
    """Collect annotations on the lines immediately preceding a declaration."""
    preceding = code[:decl_start].splitlines()
    annotations = []

    for line in reversed(preceding):
        stripped = line.strip()
        if not stripped:
            continue
        if not stripped.startswith("@"):
            break
        annotations.extend(re.findall(r"@(\w+)", stripped))

    return list(reversed(annotations))


def infer_source_set(relative_path: str) -> Optional[str]:
    """Infer the Gradle source set from a path like `src/main/kotlin/...`."""
    parts = Path(relative_path).parts
    for i, part in enumerate(parts):
        if part == "src" and i + 1 < len(parts):
            return parts[i + 1]
    return None


def infer_module(relative_path: str) -> Optional[str]:
    """Infer the Gradle module (the path segment above `src/`)."""
    parts = Path(relative_path).parts
    for i, part in enumerate(parts):
        if part == "src" and i > 0:
            return parts[i - 1]
    return None


def infer_kotlin_file_role(relative_path: str) -> str:
    """Infer the role of a Kotlin file from its path."""
    parts = Path(relative_path).parts
    lower_parts = [p.lower() for p in parts]
    filename = Path(relative_path).name
    source_set = infer_source_set(relative_path)

    # Build scripts
    if filename.endswith(".gradle.kts") or filename in ("settings.gradle.kts", "build.gradle.kts"):
        return "build"
    if source_set == "buildSrc" or "buildSrc" in parts:
        return "build"

    # Test source sets take precedence over content-based roles
    if source_set == "androidTest" or "androidtest" in lower_parts:
        return "androidTest"
    if source_set in ("test", "testFixtures") or "test" in lower_parts:
        return "test"
    if filename.endswith(("Test.kt", "Tests.kt", "Spec.kt", "IT.kt")):
        return "test"

    # Content-based roles, keyed on conventional package/directory names
    if any(p in ("controller", "controllers", "api", "routes", "routing", "handlers",
                 "endpoints", "resources") for p in lower_parts):
        return "api"
    if any(p in ("service", "services", "usecase", "usecases", "interactor",
                 "interactors", "domain") for p in lower_parts):
        return "service"
    if any(p in ("repository", "repositories", "dao", "db", "database", "store",
                 "stores", "persistence", "datasource") for p in lower_parts):
        return "db"
    if any(p in ("model", "models", "entity", "entities", "dto", "dtos", "schema") for p in lower_parts):
        return "model"
    if any(p in ("ui", "screen", "screens", "compose", "view", "views", "widget",
                 "widgets", "activity", "fragment") for p in lower_parts):
        return "ui"

    return "main"


def make_evidence(
    index: KotlinIndex,
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
