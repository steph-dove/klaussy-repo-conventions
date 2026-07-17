"""Integration tests for PHP/Laravel/Symfony convention detectors."""

from __future__ import annotations

from pathlib import Path

from conventions.detectors.base import DetectorContext
from conventions.detectors.php import (
    PHPArchitectureDetector,
    PHPDatabaseDetector,
    PHPIndex,
    PHPTestingDetector,
)
from conventions.ratings import rate_convention


def _write(path: Path, content: str) -> None:
    """Write `content` to `path`, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _ctx(repo_root: Path) -> DetectorContext:
    return DetectorContext(
        repo_root=repo_root,
        selected_languages={"php"},
        max_files=200,
    )


# ---------------------------------------------------------------------------
# Test Indexer
# ---------------------------------------------------------------------------

def test_php_indexer(tmp_path: Path):
    _write(
        tmp_path / "composer.json",
        """
        {
            "require": {
                "laravel/framework": "^10.0"
            },
            "require-dev": {
                "phpunit/phpunit": "^10.0"
            }
        }
        """,
    )
    _write(
        tmp_path / "app/Services/UserService.php",
        """<?php
        namespace App\\Services;

        use App\\Repositories\\UserRepositoryInterface;

        class UserService implements UserServiceInterface {
            // TODO: check roles
            public function create() {}
        }
        """,
    )

    index = PHPIndex(tmp_path)
    index.build()

    assert index.count_dependency("laravel/framework") is True
    assert index.count_dependency("phpunit/phpunit") is True
    assert index.count_dependency("doctrine/orm") is False

    assert len(index.files) == 1
    file_idx = index.files["app/Services/UserService.php"]
    assert file_idx.namespace == "App\\Services"
    assert len(file_idx.uses) == 1
    assert file_idx.uses[0][0] == "App\\Repositories\\UserRepositoryInterface"
    assert file_idx.types == [("class", "UserService", 6)]
    assert file_idx.todo_count == 1


# ---------------------------------------------------------------------------
# Test Architecture Detector
# ---------------------------------------------------------------------------

def test_php_architecture_detector(tmp_path: Path):
    _write(
        tmp_path / "composer.json",
        '{"require": {"laravel/framework": "^10.0"}}',
    )
    _write(
        tmp_path / "app/Http/Controllers/UserController.php",
        "<?php namespace App\\Http\\Controllers; class UserController {}",
    )
    _write(
        tmp_path / ".php-cs-fixer.dist.php",
        "<?php return new PhpCsFixer\\Config();",
    )

    ctx = _ctx(tmp_path)
    detector = PHPArchitectureDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.id == "php.conventions.architecture"
    assert rule.stats["framework"] == "Laravel Application"
    assert rule.stats["has_phpcs"] is True

    score, _, _ = rate_convention(rule)
    assert score == 5


# ---------------------------------------------------------------------------
# Test Database Detector
# ---------------------------------------------------------------------------

def test_php_database_detector(tmp_path: Path):
    _write(
        tmp_path / "app/Models/User.php",
        "<?php namespace App\\Models; use Illuminate\\Database\\Eloquent\\Model; class User extends Model {}",
    )
    _write(
        tmp_path / "database/migrations/2026_07_16_000000_create_users_table.php",
        "<?php use Illuminate\\Database\\Migrations\\Migration; class CreateUsersTable extends Migration {}",
    )

    ctx = _ctx(tmp_path)
    detector = PHPDatabaseDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.id == "php.conventions.database"
    assert "Eloquent ORM" in rule.stats["libraries"]
    assert rule.stats["migration_count"] == 1
    assert rule.stats["model_count"] == 1

    score, _, _ = rate_convention(rule)
    assert score == 5


# ---------------------------------------------------------------------------
# Test Testing Detector
# ---------------------------------------------------------------------------

def test_php_testing_detector(tmp_path: Path):
    _write(
        tmp_path / "tests/Feature/UserTest.php",
        """<?php
        namespace Tests\\Feature;
        use Tests\\TestCase;
        class UserTest extends TestCase {
            public function test_example() {
                $this->assertTrue(true);
            }
        }
        """,
    )

    ctx = _ctx(tmp_path)
    detector = PHPTestingDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.stats["test_file_count"] == 1
    assert rule.stats["primary_framework"] == "PHPUnit"

    score, _, _ = rate_convention(rule)
    assert score == 3


class TestPHPTruncationIsDisclosed:
    """A capped scan must not report the cap as the project size.

    Regression: Laravel has ~3000 PHP files. At the default 2000-file cap the
    rule stated "PHP project (2000 files)" and listed its layers as if the scan
    were complete, with nothing indicating the walk had stopped early.
    """

    def _repo(self, tmp_path: Path, file_count: int) -> Path:
        _write(tmp_path / "composer.json", '{"name": "acme/app", "require": {}}')
        for i in range(file_count):
            _write(
                tmp_path / f"src/Service/S{i}.php",
                f"<?php\nnamespace Acme\\Service;\n\nclass S{i} {{}}\n",
            )
        return tmp_path

    def test_truncated_scan_is_flagged(self, tmp_path: Path):
        repo = self._repo(tmp_path, 12)
        ctx = DetectorContext(repo_root=repo, selected_languages={"php"}, max_files=5)
        rules = PHPArchitectureDetector().detect(ctx).rules
        assert rules
        stats = rules[0].stats
        assert stats["scan_truncated"] is True
        assert stats["file_count"] == 5
        assert "at least" in rules[0].description
        assert "truncated" in rules[0].description

    def test_complete_scan_is_not_flagged(self, tmp_path: Path):
        repo = self._repo(tmp_path, 4)
        ctx = DetectorContext(repo_root=repo, selected_languages={"php"}, max_files=200)
        rules = PHPArchitectureDetector().detect(ctx).rules
        assert rules
        assert rules[0].stats["scan_truncated"] is False
        assert rules[0].stats["file_count"] == 4
        assert "at least" not in rules[0].description


class TestFrameworkVersusLibrary:
    """A framework's own repository is a library, not an application.

    laravel/framework has no artisan and no routes/web.php -- those belong to
    apps built on it -- so it is correctly reported as a library, the same way
    Vapor's repository is a Swift library rather than a Vapor application.
    """

    def test_laravel_app_is_detected(self, tmp_path: Path):
        _write(tmp_path / "composer.json", '{"require": {"laravel/framework": "^11.0"}}')
        _write(tmp_path / "artisan", "#!/usr/bin/env php\n")
        _write(tmp_path / "routes/web.php", "<?php\nRoute::get('/', fn () => view('welcome'));\n")
        _write(tmp_path / "app/Models/User.php", "<?php\nnamespace App\\Models;\n\nclass User {}\n")

        rules = PHPArchitectureDetector().detect(_ctx(tmp_path)).rules
        assert rules
        assert rules[0].stats["has_laravel"] is True
        assert rules[0].stats["framework"] == "Laravel Application"

    def test_symfony_app_is_detected(self, tmp_path: Path):
        _write(tmp_path / "composer.json", '{"require": {"symfony/framework-bundle": "^7.0"}}')
        _write(tmp_path / "bin/console", "#!/usr/bin/env php\n")
        _write(tmp_path / "config/bundles.php", "<?php\nreturn [];\n")
        _write(tmp_path / "src/Controller/HomeController.php", "<?php\nclass HomeController {}\n")

        rules = PHPArchitectureDetector().detect(_ctx(tmp_path)).rules
        assert rules
        assert rules[0].stats["has_symfony"] is True
        assert rules[0].stats["framework"] == "Symfony Application"

    def test_plain_library_is_not_an_application(self, tmp_path: Path):
        _write(tmp_path / "composer.json", '{"name": "guzzlehttp/guzzle", "require": {}}')
        _write(tmp_path / "src/Client.php", "<?php\nnamespace GuzzleHttp;\n\nclass Client {}\n")

        rules = PHPArchitectureDetector().detect(_ctx(tmp_path)).rules
        assert rules
        assert rules[0].stats["has_laravel"] is False
        assert rules[0].stats["has_symfony"] is False
        assert rules[0].stats["framework"] == "PHP Library / Script"
