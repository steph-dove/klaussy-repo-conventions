"""Integration tests for C# convention detectors."""

from __future__ import annotations

from pathlib import Path

from conventions.detectors.base import DetectorContext
from conventions.detectors.csharp import (
    CSharpArchitectureDetector,
    CSharpBuildDetector,
    CSharpConventionsDetector,
    CSharpDatabaseDetector,
    CSharpDIDetector,
    CSharpIndex,
    CSharpLoggingDetector,
    CSharpTestingDetector,
)
from conventions.ratings import rate_convention


def _write(path: Path, content: str) -> None:
    """Write `content` to `path`, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _ctx(repo_root: Path) -> DetectorContext:
    return DetectorContext(
        repo_root=repo_root,
        selected_languages={"csharp"},
        max_files=200,
    )


# ---------------------------------------------------------------------------
# Test Indexer
# ---------------------------------------------------------------------------

def test_csharp_indexer(tmp_path: Path):
    _write(
        tmp_path / "src/UserService.cs",
        """
        #nullable enable
        namespace Acme.App.Services;

        using System;
        using System.Collections.Generic;

        [ServiceAttribute]
        public class UserService {
            private readonly IUserRepository _repo;

            public UserService(IUserRepository repo) {
                _repo = repo;
            }

            public async Task<List<User>> GetUsersAsync() {
                // TODO: paginate
                var list = await _repo.FindAllAsync();
                return list.Where(u => u.IsActive).ToList();
            }
        }
        """,
    )

    index = CSharpIndex(tmp_path)
    index.build()

    assert len(index.files) == 1
    file_idx = index.files["src/UserService.cs"]
    assert file_idx.namespace == "Acme.App.Services"
    assert len(file_idx.usings) == 2
    assert file_idx.usings[0][0] == "System"
    assert len(file_idx.classes) == 1
    assert file_idx.classes[0].name == "UserService"
    assert file_idx.classes[0].kind == "class"
    assert file_idx.classes[0].attributes == ["ServiceAttribute"]
    assert len(file_idx.functions) == 2
    assert file_idx.functions[0].name == "UserService"
    assert file_idx.functions[1].name == "GetUsersAsync"
    assert file_idx.async_count == 1
    assert file_idx.await_count == 1
    assert file_idx.linq_count > 0
    assert file_idx.nullable_enabled is True
    assert file_idx.todo_count == 1


# ---------------------------------------------------------------------------
# Test Architecture Detector
# ---------------------------------------------------------------------------

def test_csharp_architecture_detector(tmp_path: Path):
    _write(
        tmp_path / "src/Controllers/UserController.cs",
        """
        namespace Acme.App.Controllers;
        using Microsoft.AspNetCore.Mvc;
        [ApiController]
        public class UserController : ControllerBase {}
        """,
    )
    _write(
        tmp_path / "src/Services/UserService.cs",
        """
        namespace Acme.App.Services;
        public class UserService {}
        """,
    )

    ctx = _ctx(tmp_path)
    detector = CSharpArchitectureDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.id == "csharp.conventions.architecture"
    assert rule.stats["structure"] == "single-module"
    assert "service" in rule.stats["layers"]
    assert "api" in rule.stats["layers"]
    assert rule.stats["package_style"] == "package-by-layer"
    assert rule.stats["framework"] == "ASP.NET Core Web API (Controllers)"

    score, _, _ = rate_convention(rule)
    assert score >= 4


# ---------------------------------------------------------------------------
# Test Database Detector
# ---------------------------------------------------------------------------

def test_csharp_database_detector(tmp_path: Path):
    _write(
        tmp_path / "src/Db/AppDbContext.cs",
        """
        namespace Acme.App.Db;
        using Microsoft.EntityFrameworkCore;
        public class AppDbContext : DbContext {}
        """,
    )
    _write(
        tmp_path / "src/Db/Migrations/20260716_Init.cs",
        """
        namespace Acme.App.Db.Migrations;
        using Microsoft.EntityFrameworkCore.Migrations;
        [Migration("20260716_Init")]
        public class Init : Migration {}
        """,
    )

    ctx = _ctx(tmp_path)
    detector = CSharpDatabaseDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.id == "csharp.conventions.database"
    assert "Entity Framework Core" in rule.stats["libraries"]
    assert rule.stats["dbcontext_count"] == 1
    assert rule.stats["migration_count"] == 1

    score, _, _ = rate_convention(rule)
    assert score == 5


def test_csharp_database_sql_warning(tmp_path: Path):
    _write(
        tmp_path / "src/Db/UserDao.cs",
        """
        namespace Acme.App.Db;
        public class UserDao {
            public string FindUser(string name) {
                var query = "SELECT * FROM Users WHERE Name = '" + name + "'";
                return query;
            }
        }
        """,
    )

    ctx = _ctx(tmp_path)
    detector = CSharpDatabaseDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.stats["raw_sql_concat_count"] == 1
    # The finding rides on the rule, not the detector-failure channel.
    assert "SQL concatenation" in rule.description
    assert result.warnings == []

    score, _, _ = rate_convention(rule)
    assert score == 2


# ---------------------------------------------------------------------------
# Test DI Detector
# ---------------------------------------------------------------------------

def test_csharp_di_detector(tmp_path: Path):
    _write(
        tmp_path / "src/Program.cs",
        """
        var builder = WebApplication.CreateBuilder(args);
        builder.Services.AddScoped<IUserService, UserService>();
        """,
    )

    ctx = _ctx(tmp_path)
    detector = CSharpDIDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert "Microsoft.Extensions.DependencyInjection" in rule.stats["frameworks"]
    assert rule.stats["ms_di_calls"] == 1

    score, _, _ = rate_convention(rule)
    assert score == 5


# ---------------------------------------------------------------------------
# Test Logging Detector
# ---------------------------------------------------------------------------

def test_csharp_logging_detector(tmp_path: Path):
    _write(
        tmp_path / "src/Service.cs",
        """
        namespace Acme.App;
        using Microsoft.Extensions.Logging;
        public class Service {
            private readonly ILogger<Service> _logger;
            public Service(ILogger<Service> logger) {
                _logger = logger;
            }
            public void Do() {
                _logger.LogInformation("Done");
            }
        }
        """,
    )

    ctx = _ctx(tmp_path)
    detector = CSharpLoggingDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.stats["primary_framework"] == "microsoft_logging"
    assert rule.stats["raw_print_count"] == 0

    score, _, _ = rate_convention(rule)
    assert score == 5


def test_csharp_logging_raw_print(tmp_path: Path):
    _write(
        tmp_path / "src/Service.cs",
        """
        namespace Acme.App;
        using Microsoft.Extensions.Logging;
        public class Service {
            public void Do() {
                Console.WriteLine("Done");
            }
        }
        """,
    )

    ctx = _ctx(tmp_path)
    detector = CSharpLoggingDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.stats["raw_print_count"] == 1
    assert "console output" in rule.description
    assert result.warnings == []

    score, _, _ = rate_convention(rule)
    assert score == 3


# ---------------------------------------------------------------------------
# Test Testing Detector
# ---------------------------------------------------------------------------

def test_csharp_testing_detector(tmp_path: Path):
    _write(
        tmp_path / "tests/ServiceTests.cs",
        """
        namespace Acme.App.Tests;
        using Xunit;
        public class ServiceTests {
            [Fact]
            public void TestOne() {
                Assert.True(true);
            }
        }
        """,
    )

    ctx = _ctx(tmp_path)
    detector = CSharpTestingDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.stats["test_file_count"] == 1
    assert "xUnit" in rule.stats["frameworks"]
    assert rule.stats["primary_naming"] == "suffix_tests"

    score, _, _ = rate_convention(rule)
    assert score == 3


# ---------------------------------------------------------------------------
# Test Conventions Detector
# ---------------------------------------------------------------------------

def test_csharp_conventions_detector(tmp_path: Path):
    _write(
        tmp_path / "src/Processor.cs",
        """
        #nullable enable
        namespace Acme.App;
        using System.Linq;
        public class Processor {
            public async Task Process() {
                var list = new List<string>();
                var active = list.Where(x => x != null).ToList();
                await Task.CompletedTask;
            }
        }
        """,
    )

    ctx = _ctx(tmp_path)
    detector = CSharpConventionsDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 4
    rule = result.rules[0]
    assert rule.id == "csharp.conventions.general"
    assert rule.stats["nullable_style"] == "enabled (standard)"
    assert rule.stats["async_style"] == "asynchronous (async/await)"
    assert rule.stats["linq_style"] == "LINQ processing"

    score, _, _ = rate_convention(rule)
    assert score == 5


_CSPROJ_NULLABLE = """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.Extensions.DependencyInjection" Version="8.0.0" />
  </ItemGroup>
</Project>
"""

_CSPROJ_TEST_ONLY = """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Autofac" Version="8.0.0" />
    <PackageReference Include="xunit" Version="2.9.0" />
  </ItemGroup>
</Project>
"""


class TestNullableIsReadFromTheProject:
    """Nullable reference types are a project-wide setting since .NET 6.

    Regression: only per-file `#nullable enable` directives were read, so
    eShopOnWeb -- which sets <Nullable>enable</Nullable> in every csproj --
    was reported as having nullable "disabled".
    """

    def test_csproj_nullable_enable_is_detected(self, tmp_path: Path):
        _write(tmp_path / "src/App/App.csproj", _CSPROJ_NULLABLE)
        _write(
            tmp_path / "src/App/Service.cs",
            "namespace App;\n\npublic class Service\n{\n    public string? Name { get; set; }\n}\n",
        )
        rules = CSharpConventionsDetector().detect(_ctx(tmp_path)).rules
        assert rules
        assert rules[0].stats["nullable_style"] == "enabled (project-wide)"

    def test_directory_build_props_nullable_is_detected(self, tmp_path: Path):
        """A repo can enable nullable once in Directory.Build.props."""
        _write(
            tmp_path / "Directory.Build.props",
            "<Project>\n  <PropertyGroup>\n    <Nullable>enable</Nullable>\n"
            "  </PropertyGroup>\n</Project>\n",
        )
        _write(
            tmp_path / "src/App/App.csproj",
            '<Project Sdk="Microsoft.NET.Sdk">\n  <PropertyGroup>\n'
            "    <TargetFramework>net8.0</TargetFramework>\n  </PropertyGroup>\n</Project>\n",
        )
        _write(tmp_path / "src/App/Service.cs", "namespace App;\n\npublic class Service {}\n")
        rules = CSharpConventionsDetector().detect(_ctx(tmp_path)).rules
        assert rules
        assert rules[0].stats["nullable_style"] == "enabled (project-wide)"

    def test_no_nullable_declaration_reports_disabled(self, tmp_path: Path):
        _write(
            tmp_path / "src/App/App.csproj",
            '<Project Sdk="Microsoft.NET.Sdk">\n  <PropertyGroup>\n'
            "    <TargetFramework>net472</TargetFramework>\n  </PropertyGroup>\n</Project>\n",
        )
        _write(tmp_path / "src/App/Service.cs", "namespace App;\n\npublic class Service {}\n")
        rules = CSharpConventionsDetector().detect(_ctx(tmp_path)).rules
        assert rules
        assert rules[0].stats["nullable_style"] == "disabled"


class TestTestOnlySignalsAreNotConventions:
    """A package used only by the test suite is not the project's convention."""

    def test_test_project_autofac_is_not_the_di_framework(self, tmp_path: Path):
        """Newtonsoft.Json references Autofac only from its test project, to demo
        DI in a documentation sample. That does not make Autofac its DI container."""
        _write(tmp_path / "src/MyLib/MyLib.csproj", _CSPROJ_NULLABLE)
        _write(
            tmp_path / "src/MyLib/Parser.cs",
            "namespace MyLib;\n\npublic class Parser\n{\n    public void Go() {}\n}\n",
        )
        _write(tmp_path / "src/MyLib.Tests/MyLib.Tests.csproj", _CSPROJ_TEST_ONLY)
        _write(
            tmp_path / "src/MyLib.Tests/DiSample.cs",
            "using Autofac;\n\nnamespace MyLib.Tests;\n\npublic class DiSample\n{\n"
            "    private readonly ILogger _logger;\n}\n",
        )
        rules = CSharpDIDetector().detect(_ctx(tmp_path)).rules
        for r in rules:
            assert "Autofac" not in r.stats["frameworks"], (
                "a container referenced only by the test project is not the DI convention"
            )

    def test_dotnet_test_project_directory_is_classified_as_test(self):
        from conventions.detectors.csharp.index import infer_csharp_file_role

        # .NET names test projects after the project under test.
        assert infer_csharp_file_role("Src/Newtonsoft.Json.Tests/Foo.cs") == "test"
        assert infer_csharp_file_role("src/MyApp.UnitTests/Bar.cs") == "test"
        assert infer_csharp_file_role("src/MyApp.IntegrationTests/Baz.cs") == "test"
        # ...but a directory that merely ends in "test" is not one.
        assert infer_csharp_file_role("src/latest/Thing.cs") == "main"
        assert infer_csharp_file_role("src/Contest/Entry.cs") == "main"


class TestPrimaryConstructorDetection:
    """C# 12 primary constructors, without matching across lines.

    Regression: the pattern used \\s+ (which spans newlines), so a bare `class`
    at the end of one line followed by any `Method(args)` call on the next
    matched. Newtonsoft.Json, which predates primary constructors, was reported
    as using them.
    """

    def test_class_followed_by_call_on_next_line_is_not_a_primary_constructor(self, tmp_path: Path):
        _write(tmp_path / "src/App/App.csproj", _CSPROJ_NULLABLE)
        _write(
            tmp_path / "src/App/Reflect.cs",
            """namespace App;

public class Reflect
{
    public void Go()
    {
        // returns the base class
        GetChildPrivateFields(fieldInfos, targetType, bindingAttr);
    }
}
""",
        )
        rules = CSharpDIDetector().detect(_ctx(tmp_path)).rules
        for r in rules:
            assert r.stats["primary_constructor_count"] == 0

    def test_real_primary_constructor_is_detected(self, tmp_path: Path):
        _write(tmp_path / "src/App/App.csproj", _CSPROJ_NULLABLE)
        _write(
            tmp_path / "src/App/UserService.cs",
            "namespace App;\n\npublic sealed class UserService(IUserRepository repo)\n{\n"
            "    public void Go() {}\n}\n",
        )
        rules = CSharpDIDetector().detect(_ctx(tmp_path)).rules
        assert rules
        assert rules[0].stats["primary_constructor_count"] == 1


class TestCSharpBuildDetector:
    """The .NET build rule drives the Build/Test commands in CLAUDE.md."""

    def test_build_rule_reports_dotnet(self, tmp_path: Path):
        _write(tmp_path / "src/App/App.csproj", _CSPROJ_NULLABLE)
        _write(tmp_path / "src/App/Service.cs", "namespace App;\n\npublic class Service {}\n")
        rules = CSharpBuildDetector().detect(_ctx(tmp_path)).rules
        assert rules
        stats = rules[0].stats
        # `primary_tool` is what the CLAUDE.md renderer reads to pick commands.
        assert stats["primary_tool"] == "dotnet"
        assert "net8.0" in stats["target_frameworks"]
        assert stats["nullable_projects"] == 1

    def test_no_projects_emits_no_rule(self, tmp_path: Path):
        _write(tmp_path / "src/App/Service.cs", "namespace App;\n\npublic class Service {}\n")
        assert CSharpBuildDetector().detect(_ctx(tmp_path)).rules == []

    def test_rule_is_rated(self, tmp_path: Path):
        _write(tmp_path / "src/App/App.csproj", _CSPROJ_NULLABLE)
        _write(tmp_path / "src/App/Service.cs", "namespace App;\n\npublic class Service {}\n")
        rules = CSharpBuildDetector().detect(_ctx(tmp_path)).rules
        score, reason, _ = rate_convention(rules[0])
        assert 1 <= score <= 5
        assert ".NET" in reason
