"""Unit and integration tests for the Kotlin index detector.

NOTE: fixtures deliberately use `com/acme/...` (never `com/example/...`) because
`src/conventions/fs.py` HARD_EXCLUDES matches "example"/"examples"/"demo"/"docs"/
"sample"/"samples" against ANY path component, which would silently drop fixture
files using the conventional `com/example` package path.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from conventions.detectors.kotlin.index import (
    KotlinIndex,
    infer_kotlin_file_role,
    infer_module,
    infer_source_set,
    make_evidence,
    strip_comments_and_strings,
)

# ----------------------------------------------------------------------
# strip_comments_and_strings
# ----------------------------------------------------------------------


class TestStripCommentsAndStrings:
    """Direct unit tests for the comment/string stripper."""

    def test_line_comment_blanked(self):
        content = "val x = 1 // class Fake\nval y = 2\n"
        stripped = strip_comments_and_strings(content)

        assert "Fake" not in stripped
        assert "class" not in stripped
        assert "val x = 1" in stripped
        assert "val y = 2" in stripped
        assert len(stripped) == len(content)
        assert stripped.count("\n") == content.count("\n")

    def test_block_comment_blanked(self):
        content = "val a = 1\n/* class Fake */\nval b = 2\n"
        stripped = strip_comments_and_strings(content)

        assert "Fake" not in stripped
        assert "class" not in stripped
        assert "val a = 1" in stripped
        assert "val b = 2" in stripped
        assert len(stripped) == len(content)
        assert stripped.count("\n") == content.count("\n")

    def test_nested_block_comment_blanked(self):
        # Kotlin block comments nest; the inner `/* ... */` closes but the
        # outer comment continues until its own matching `*/`.
        content = '/* a /* nested class Fake */ still c */ class Real\n'
        stripped = strip_comments_and_strings(content)

        assert "Fake" not in stripped
        assert "still" not in stripped
        assert "class Real" in stripped
        assert len(stripped) == len(content)
        assert stripped.count("\n") == content.count("\n")

    def test_raw_string_blanked(self):
        content = 'val s = """class NotAClass"""\nval t = 2\n'
        stripped = strip_comments_and_strings(content)

        assert "NotAClass" not in stripped
        assert "class" not in stripped
        assert "val s =" in stripped
        assert "val t = 2" in stripped
        assert len(stripped) == len(content)
        assert stripped.count("\n") == content.count("\n")

    def test_regular_string_blanked(self):
        content = 'val s = "class NotAClass"\nval t = 2\n'
        stripped = strip_comments_and_strings(content)

        assert "NotAClass" not in stripped
        assert "class" not in stripped
        assert "val s =" in stripped
        assert "val t = 2" in stripped
        assert len(stripped) == len(content)
        assert stripped.count("\n") == content.count("\n")

    def test_escaped_quote_in_string_does_not_terminate_early(self):
        content = 'val s = "a \\" b"\nval real = 1\n'
        stripped = strip_comments_and_strings(content)
        lines = stripped.splitlines()

        # The whole string (including the escaped quote) is blanked, and
        # parsing correctly resumes as real code on the next line.
        assert lines[0].rstrip() == "val s ="
        assert lines[1] == "val real = 1"
        assert len(stripped) == len(content)
        assert stripped.count("\n") == content.count("\n")

    def test_length_and_newlines_preserved_for_mixed_content(self):
        content = (
            "package com.acme\n"
            "// leading comment with class Fake\n"
            "/* block\n"
            "spanning\n"
            "lines with \"quotes\" and 'chars' */\n"
            'val s = "esc \\" ape"\n'
            'val t = """raw class Fake"""\n'
            "class Real\n"
        )
        stripped = strip_comments_and_strings(content)

        assert len(stripped) == len(content)
        assert stripped.count("\n") == content.count("\n")
        assert "class Real" in stripped
        assert "Fake" not in stripped


# ----------------------------------------------------------------------
# infer_kotlin_file_role / infer_source_set / infer_module (pure functions)
# ----------------------------------------------------------------------


class TestInferRoleSourceSetModule:
    """Pure-function tests; no filesystem needed."""

    def test_main_api_role(self):
        path = "src/main/kotlin/com/acme/api/Foo.kt"
        assert infer_kotlin_file_role(path) == "api"
        assert infer_source_set(path) == "main"
        assert infer_module(path) is None

    def test_module_above_src(self):
        path = "app/src/main/kotlin/com/acme/Foo.kt"
        assert infer_module(path) == "app"

    def test_test_source_set_role(self):
        path = "src/test/kotlin/com/acme/FooTest.kt"
        assert infer_kotlin_file_role(path) == "test"
        assert infer_source_set(path) == "test"

    def test_android_test_role(self):
        path = "src/androidTest/kotlin/com/acme/FooTest.kt"
        assert infer_kotlin_file_role(path) == "androidTest"
        assert infer_source_set(path) == "androidTest"

    def test_build_gradle_kts_role(self):
        assert infer_kotlin_file_role("build.gradle.kts") == "build"
        assert infer_kotlin_file_role("settings.gradle.kts") == "build"

    def test_service_dir_role(self):
        assert infer_kotlin_file_role("src/main/kotlin/com/acme/service/UserService.kt") == "service"

    def test_db_dir_role(self):
        assert infer_kotlin_file_role("src/main/kotlin/com/acme/db/UserDao.kt") == "db"

    def test_model_dir_role(self):
        assert infer_kotlin_file_role("src/main/kotlin/com/acme/model/User.kt") == "model"

    def test_ui_dir_role(self):
        assert infer_kotlin_file_role("src/main/kotlin/com/acme/ui/MainActivity.kt") == "ui"

    def test_test_suffix_outside_test_dir_is_still_test(self):
        path = "src/main/kotlin/com/acme/FooTest.kt"
        assert infer_source_set(path) == "main"
        assert infer_kotlin_file_role(path) == "test"

    def test_no_src_segment_no_module_no_source_set(self):
        path = "scripts/Tool.kt"
        assert infer_source_set(path) is None
        assert infer_module(path) is None


# ----------------------------------------------------------------------
# Declaration extraction (single-file fixture exercising the stripped `code`
# path: functions, classes, properties, annotations, counters).
# ----------------------------------------------------------------------


@pytest.fixture
def decl_repo(tmp_path: Path):
    """A single Kotlin file covering the declaration-extraction surface.

    Returns (repo_root, relative_path, expected_lines) where expected_lines
    maps a descriptive key to the 1-indexed line number of that declaration,
    computed from the same list used to build the file (no hand counting).
    """
    lines: list[str] = []
    expected: dict[str, int] = {}

    def add(text: str, key: str | None = None) -> None:
        if key is not None:
            expected[key] = len(lines) + 1
        lines.append(text)

    add("package com.acme.api")
    add("")
    # A block comment containing declarations that must NOT be extracted,
    # since they sit at true line-start and would match the anchored
    # regexes if the comment weren't stripped first.
    add("/*")
    add("class HiddenClass")
    add("fun hiddenFunction() {")
    add("}")
    add("import com.acme.fake.Hidden")
    add("@FakeAnnotation")
    add("*/")
    add("")
    add("import com.acme.model.User", key="import_user")
    add("import com.acme.util.Logger", key="import_logger")
    add("")
    add("// class OneLineHiddenClass")
    add('private val commentedString = "class StringClassNotReal"', key="commented_string_prop")
    add("")
    add("@RestController", key="rest_controller_annotation")
    add("class UserController {", key="user_controller")
    add("    fun publicMethod(): String {", key="public_method")
    add('        return "ok"')
    add("    }")
    add("")
    add("    private fun privateMethod() {", key="private_method")
    add("    }")
    add("")
    add("    internal suspend fun fetchUser(id: Int): User? {", key="fetch_user")
    add("        return null")
    add("    }")
    add("}")
    add("")
    add("fun String.toSlug(): String {", key="to_slug")
    add("    return this.lowercase()")
    add("}")
    add("")
    add("data class UserDto(val id: Int, val name: String)", key="user_dto")
    add("")
    add("sealed class Result", key="result_class")
    add("")
    add("interface Repository {", key="repository")
    add("    fun find(id: Int): User?", key="find_fn")
    add("}")
    add("")
    add("enum class Status {", key="status_enum")
    add("    ACTIVE, INACTIVE")
    add("}")
    add("")
    add("object Singleton", key="singleton")
    add("")
    add("class NullableOps {", key="nullable_ops")
    add("    val a: String? = null", key="prop_a")
    add('    var b: String = "x"', key="prop_b")
    add("    lateinit var c: String", key="prop_c")
    add("")
    add("    fun process() {", key="process_fn")
    add("        val x = a!!", key="prop_x")
    add("        val y = a?.length", key="prop_y")
    add('        val z = a ?: "default"', key="prop_z")
    add("    }")
    add("}")

    content = "\n".join(lines) + "\n"

    src_dir = tmp_path / "src" / "main" / "kotlin" / "com" / "acme" / "api"
    src_dir.mkdir(parents=True)
    file_path = src_dir / "UserController.kt"
    file_path.write_text(content)

    relative_path = "src/main/kotlin/com/acme/api/UserController.kt"
    return tmp_path, relative_path, expected


class TestDeclarationExtraction:
    def _build(self, repo_root: Path, relative_path: str):
        index = KotlinIndex(repo_root)
        index.build()
        return index.files[relative_path]

    def test_package_extracted(self, decl_repo):
        repo_root, relative_path, _ = decl_repo
        file_idx = self._build(repo_root, relative_path)
        assert file_idx.package == "com.acme.api"

    def test_imports_extracted_with_correct_lines(self, decl_repo):
        repo_root, relative_path, expected = decl_repo
        file_idx = self._build(repo_root, relative_path)

        imports = dict((path, line) for path, line in file_idx.imports)
        # Imports preceded by blank or comment-blanked lines must still report
        # the line the `import` keyword is actually on.
        assert imports == {
            "com.acme.model.User": expected["import_user"],
            "com.acme.util.Logger": expected["import_logger"],
        }
        # The commented-out import must not leak through.
        assert "com.acme.fake.Hidden" not in imports

    def test_hidden_declarations_in_comments_and_strings_not_extracted(self, decl_repo):
        repo_root, relative_path, _ = decl_repo
        file_idx = self._build(repo_root, relative_path)

        function_names = {fn.name for fn in file_idx.functions}
        class_names = {cls.name for cls in file_idx.classes}
        annotation_names = {name for name, _ in file_idx.annotations}

        assert "hiddenFunction" not in function_names
        assert "HiddenClass" not in class_names
        assert "OneLineHiddenClass" not in class_names
        assert "StringClassNotReal" not in class_names
        assert "FakeAnnotation" not in annotation_names

    def test_functions_extracted(self, decl_repo):
        repo_root, relative_path, expected = decl_repo
        file_idx = self._build(repo_root, relative_path)

        by_name = {fn.name: fn for fn in file_idx.functions}
        assert set(by_name) == {
            "publicMethod",
            "privateMethod",
            "fetchUser",
            "toSlug",
            "find",
            "process",
        }

        public_method = by_name["publicMethod"]
        assert public_method.visibility == "public"
        assert public_method.is_public is True
        assert public_method.line == expected["public_method"]
        assert public_method.return_type == "String"
        assert public_method.is_suspend is False
        assert public_method.is_extension is False

        private_method = by_name["privateMethod"]
        assert private_method.visibility == "private"
        assert private_method.is_public is False
        assert private_method.line == expected["private_method"]

        fetch_user = by_name["fetchUser"]
        assert fetch_user.visibility == "internal"
        assert fetch_user.is_suspend is True
        assert fetch_user.return_type == "User?"
        assert fetch_user.line == expected["fetch_user"]

        to_slug = by_name["toSlug"]
        assert to_slug.is_extension is True
        assert to_slug.visibility == "public"
        assert to_slug.return_type == "String"
        assert to_slug.line == expected["to_slug"]

    def test_classes_extracted_with_correct_kinds(self, decl_repo):
        repo_root, relative_path, expected = decl_repo
        file_idx = self._build(repo_root, relative_path)

        by_name = {cls.name: cls for cls in file_idx.classes}
        assert set(by_name) == {
            "UserController",
            "UserDto",
            "Result",
            "Repository",
            "Status",
            "Singleton",
            "NullableOps",
        }

        assert by_name["UserController"].kind == "class"
        assert by_name["UserController"].line == expected["user_controller"]
        assert by_name["UserDto"].kind == "data class"
        assert by_name["UserDto"].is_data is True
        assert by_name["UserDto"].is_sealed is False
        assert by_name["Result"].kind == "sealed class"
        assert by_name["Result"].is_sealed is True
        assert by_name["Result"].is_data is False
        assert by_name["Repository"].kind == "interface"
        assert by_name["Status"].kind == "enum class"
        assert by_name["Singleton"].kind == "object"
        assert by_name["NullableOps"].kind == "class"

    def test_class_annotations_from_preceding_lines(self, decl_repo):
        repo_root, relative_path, _ = decl_repo
        file_idx = self._build(repo_root, relative_path)

        by_name = {cls.name: cls for cls in file_idx.classes}
        assert by_name["UserController"].annotations == ["RestController"]
        # No annotation directly precedes these declarations.
        assert by_name["Repository"].annotations == []
        assert by_name["UserDto"].annotations == []

    def test_file_level_annotation_usage_recorded(self, decl_repo):
        repo_root, relative_path, expected = decl_repo
        file_idx = self._build(repo_root, relative_path)

        annotations = dict(file_idx.annotations)
        assert annotations["RestController"] == expected["rest_controller_annotation"]

    def test_properties_extracted_with_is_var_flag(self, decl_repo):
        repo_root, relative_path, _ = decl_repo
        file_idx = self._build(repo_root, relative_path)

        by_name = {name: is_var for name, _line, is_var in file_idx.properties}
        assert by_name == {
            "commentedString": False,
            "a": False,
            "b": True,
            "c": True,
            "x": False,
            "y": False,
            "z": False,
        }
        assert len(file_idx.properties) == 7

    def test_counters(self, decl_repo):
        repo_root, relative_path, _ = decl_repo
        file_idx = self._build(repo_root, relative_path)

        assert file_idx.suspend_count == 1
        assert file_idx.not_null_assertion_count == 1
        assert file_idx.safe_call_count == 1
        assert file_idx.elvis_count == 1
        assert file_idx.lateinit_count == 1


# ----------------------------------------------------------------------
# Query helpers, roles-via-build, make_evidence
# ----------------------------------------------------------------------


@pytest.fixture
def query_repo(tmp_path: Path):
    """A small multi-file repo exercising query helpers, roles, and modules."""
    expected: dict[str, int] = {}

    # File A: main/service source, with one import shared with file B and
    # one import unique to it, plus an annotation usage.
    a_lines: list[str] = []

    def add_a(text: str, key: str | None = None) -> None:
        if key is not None:
            expected[key] = len(a_lines) + 1
        a_lines.append(text)

    add_a("package com.acme.service")
    add_a("")
    add_a("import com.acme.model.User", key="a_import_user")
    add_a("import com.acme.util.Logger", key="a_import_logger")
    add_a("")
    add_a("class UserService {", key="a_class")
    add_a('    @Deprecated("use v2")', key="a_deprecated")
    add_a("    fun getUser(id: Int): User {", key="a_fun")
    add_a('        Logger.log("fetching")')
    add_a("        return User(id)")
    add_a("    }")
    add_a("}")

    a_dir = tmp_path / "src" / "main" / "kotlin" / "com" / "acme" / "service"
    a_dir.mkdir(parents=True)
    a_path = a_dir / "UserService.kt"
    a_path.write_text("\n".join(a_lines) + "\n")
    a_rel = "src/main/kotlin/com/acme/service/UserService.kt"

    # File B: test source.
    b_content = (
        "package com.acme.service\n"
        "\n"
        "import com.acme.testutil.Fixtures\n"
        "\n"
        "class UserServiceTest {\n"
        "    fun testGetUser() {\n"
        "        val service = UserService()\n"
        "    }\n"
        "}\n"
    )
    b_dir = tmp_path / "src" / "test" / "kotlin" / "com" / "acme" / "service"
    b_dir.mkdir(parents=True)
    b_path = b_dir / "UserServiceTest.kt"
    b_path.write_text(b_content)
    b_rel = "src/test/kotlin/com/acme/service/UserServiceTest.kt"

    # File C: lives under an "app" module, no matching role keyword -> "main".
    c_content = "package com.acme\n\nclass App\n"
    c_dir = tmp_path / "app" / "src" / "main" / "kotlin" / "com" / "acme"
    c_dir.mkdir(parents=True)
    c_path = c_dir / "App.kt"
    c_path.write_text(c_content)
    c_rel = "app/src/main/kotlin/com/acme/App.kt"

    # File D: a build script at repo root.
    d_content = 'plugins {\n    id("org.jetbrains.kotlin.jvm")\n}\n'
    d_path = tmp_path / "build.gradle.kts"
    d_path.write_text(d_content)
    d_rel = "build.gradle.kts"

    return tmp_path, {
        "a": a_rel,
        "b": b_rel,
        "c": c_rel,
        "d": d_rel,
    }, expected


class TestQueryHelpersAndRoles:
    def _build(self, repo_root: Path) -> KotlinIndex:
        index = KotlinIndex(repo_root)
        index.build()
        return index

    def test_roles_inferred_through_build(self, query_repo):
        repo_root, rel, _ = query_repo
        index = self._build(repo_root)

        assert index.files[rel["a"]].role == "service"
        assert index.files[rel["b"]].role == "test"
        assert index.files[rel["c"]].role == "main"
        assert index.files[rel["d"]].role == "build"

    def test_modules(self, query_repo):
        repo_root, rel, _ = query_repo
        index = self._build(repo_root)

        assert index.files[rel["a"]].module is None
        assert index.files[rel["c"]].module == "app"
        assert index.modules == {"app"}

    def test_find_imports_matching(self, query_repo):
        repo_root, rel, expected = query_repo
        index = self._build(repo_root)

        results = index.find_imports_matching("com.acme.model")
        assert results == [(rel["a"], "com.acme.model.User", expected["a_import_user"])]

    def test_count_imports_matching(self, query_repo):
        repo_root, rel, _ = query_repo
        index = self._build(repo_root)

        # Only file A imports something under com.acme.model.
        assert index.count_imports_matching("com.acme.model") == 1
        # Files A and B each import something under com.acme (as a file count,
        # not an import count).
        assert index.count_imports_matching("com.acme") == 2

    def test_search_pattern_exclude_tests(self, query_repo):
        repo_root, rel, _ = query_repo
        index = self._build(repo_root)

        all_results = index.search_pattern(r"class \w+", exclude_tests=False)
        matched_files = {r[0] for r in all_results}
        assert rel["a"] in matched_files
        assert rel["b"] in matched_files
        assert rel["c"] in matched_files

        non_test_results = index.search_pattern(r"class \w+", exclude_tests=True)
        matched_files_no_test = {r[0] for r in non_test_results}
        assert rel["b"] not in matched_files_no_test
        assert rel["a"] in matched_files_no_test
        assert rel["c"] in matched_files_no_test

    def test_count_pattern_exclude_tests(self, query_repo):
        repo_root, rel, _ = query_repo
        index = self._build(repo_root)

        assert index.count_pattern(r"\bfun\b", exclude_tests=True) == 1
        assert index.count_pattern(r"\bfun\b", exclude_tests=False) == 2

    def test_find_and_count_annotation(self, query_repo):
        repo_root, rel, expected = query_repo
        index = self._build(repo_root)

        results = index.find_annotation("Deprecated")
        assert results == [(rel["a"], expected["a_deprecated"])]
        assert index.count_annotation("Deprecated") == 1
        assert index.count_annotation("NoSuchAnnotation") == 0

    def test_get_test_and_non_test_files(self, query_repo):
        repo_root, rel, _ = query_repo
        index = self._build(repo_root)

        test_paths = {f.relative_path for f in index.get_test_files()}
        non_test_paths = {f.relative_path for f in index.get_non_test_files()}

        assert test_paths == {rel["b"]}
        assert non_test_paths == {rel["a"], rel["c"], rel["d"]}

    def test_get_files_by_role_and_script_files(self, query_repo):
        repo_root, rel, _ = query_repo
        index = self._build(repo_root)

        service_files = [f.relative_path for f in index.get_files_by_role("service")]
        assert service_files == [rel["a"]]

        script_files = [f.relative_path for f in index.get_script_files()]
        assert script_files == [rel["d"]]

    def test_all_functions_and_all_classes(self, query_repo):
        repo_root, rel, _ = query_repo
        index = self._build(repo_root)

        functions = index.all_functions()
        function_names = {(path, fn.name) for path, fn in functions}
        assert function_names == {
            (rel["a"], "getUser"),
            (rel["b"], "testGetUser"),
        }

        classes = index.all_classes()
        class_names = {(path, cls.name) for path, cls in classes}
        assert class_names == {
            (rel["a"], "UserService"),
            (rel["b"], "UserServiceTest"),
            (rel["c"], "App"),
        }

    def test_make_evidence_valid(self, query_repo):
        repo_root, rel, expected = query_repo
        index = self._build(repo_root)

        line = expected["a_fun"]
        evidence = make_evidence(index, rel["a"], line, radius=1)

        assert evidence is not None
        assert evidence.file_path == rel["a"]
        assert evidence.line_start == line - 1
        assert evidence.line_end == line + 1
        assert "fun getUser" in evidence.excerpt

    def test_make_evidence_unknown_path_returns_none(self, query_repo):
        repo_root, _, _ = query_repo
        index = self._build(repo_root)

        assert make_evidence(index, "no/such/File.kt", 1) is None

    def test_make_evidence_out_of_range_line_returns_none(self, query_repo):
        repo_root, rel, _ = query_repo
        index = self._build(repo_root)

        assert make_evidence(index, rel["a"], 0) is None
        assert make_evidence(index, rel["a"], 10_000) is None


# ----------------------------------------------------------------------
# Edge cases
# ----------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_repo_has_no_files(self, tmp_path: Path):
        index = KotlinIndex(tmp_path)
        index.build()
        assert index.files == {}

    def test_file_with_no_package_or_imports_does_not_crash(self, tmp_path: Path):
        src_dir = tmp_path / "src" / "main" / "kotlin" / "com" / "acme"
        src_dir.mkdir(parents=True)
        (src_dir / "Bare.kt").write_text("class Foo\n")

        index = KotlinIndex(tmp_path)
        index.build()

        file_idx = index.files["src/main/kotlin/com/acme/Bare.kt"]
        assert file_idx.package is None
        assert file_idx.imports == []
        assert file_idx.parse_error is None
        assert [c.name for c in file_idx.classes] == ["Foo"]

    def test_build_is_idempotent(self, tmp_path: Path):
        src_dir = tmp_path / "src" / "main" / "kotlin" / "com" / "acme"
        src_dir.mkdir(parents=True)
        (src_dir / "Foo.kt").write_text("package com.acme\n\nclass Foo\n")

        index = KotlinIndex(tmp_path)
        index.build()
        first_count = len(index.files)
        first_function_count = len(index.all_functions())
        first_class_count = len(index.all_classes())

        index.build()

        assert len(index.files) == first_count
        assert len(index.all_functions()) == first_function_count
        assert len(index.all_classes()) == first_class_count
