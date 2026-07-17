"""Integration tests for Swift convention detectors."""

from __future__ import annotations

from pathlib import Path

from conventions.detectors.base import DetectorContext
from conventions.detectors.swift import (
    SwiftArchitectureDetector,
    SwiftIndex,
    SwiftTestingDetector,
)
from conventions.ratings import rate_convention


def _write(path: Path, content: str) -> None:
    """Write `content` to `path`, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _ctx(repo_root: Path) -> DetectorContext:
    return DetectorContext(
        repo_root=repo_root,
        selected_languages={"swift"},
        max_files=200,
    )


# ---------------------------------------------------------------------------
# Test Indexer
# ---------------------------------------------------------------------------

def test_swift_indexer(tmp_path: Path):
    _write(
        tmp_path / "Package.swift",
        """
        // swift-tools-version: 5.9
        import PackageDescription
        let package = Package(
            name: "MyProject",
            dependencies: [
                .package(url: "https://github.com/vapor/vapor.git", from: "4.0.0")
            ]
        )
        """,
    )
    _write(
        tmp_path / "Sources/App/Controllers/UserController.swift",
        """
        import Vapor
        import SwiftUI

        struct UserController {
            func fetch() async -> String {
                // TODO: load from DB
                await Task.sleep(1_000_000)
                return "user"
            }
        }
        """,
    )

    index = SwiftIndex(tmp_path)
    index.build()

    assert index.count_dependency("Vapor") is True
    assert index.count_import("Vapor") == 1
    assert index.count_import("SwiftUI") == 1

    assert len(index.files) == 1
    file_idx = index.files["Sources/App/Controllers/UserController.swift"]
    assert file_idx.types == [("struct", "UserController", 5)]
    assert file_idx.async_count == 1
    assert file_idx.await_count == 1
    assert file_idx.todo_count == 1


# ---------------------------------------------------------------------------
# Test Architecture Detector
# ---------------------------------------------------------------------------

def test_swift_architecture_detector(tmp_path: Path):
    _write(
        tmp_path / "Sources/App/Controllers/UserController.swift",
        """
        import Vapor
        struct UserController {}
        """,
    )
    _write(
        tmp_path / ".swiftlint.yml",
        "disabled_rules:\n  - trailing_whitespace",
    )

    ctx = _ctx(tmp_path)
    detector = SwiftArchitectureDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.id == "swift.conventions.architecture"
    assert rule.stats["framework"] == "Vapor Server Application"
    assert rule.stats["has_swiftlint"] is True

    score, _, _ = rate_convention(rule)
    assert score == 5


# ---------------------------------------------------------------------------
# Test Testing Detector
# ---------------------------------------------------------------------------

def test_swift_testing_detector(tmp_path: Path):
    _write(
        tmp_path / "Tests/AppTests/UserTests.swift",
        """
        import Testing
        @testable import App

        @Test func testFetch() async {
            #expect(true)
        }
        """,
    )

    ctx = _ctx(tmp_path)
    detector = SwiftTestingDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.stats["test_file_count"] == 1
    assert rule.stats["primary_framework"] == "swift-testing"

    score, _, _ = rate_convention(rule)
    assert score == 3


class TestLibraryVersusApplication:
    """A package that vends a library is a library, however much UIKit it imports.

    Regression: any UIKit import made a project a "UIKit Application", so
    Alamofire (a networking library with 3 incidental UIKit imports) and
    Kingfisher (a UIKit image library) were both reported as applications.
    """

    def _library_package(self, tmp_path: Path, ui_import: str, file_count: int = 12) -> Path:
        _write(
            tmp_path / "Package.swift",
            'let package = Package(\n'
            '    name: "MyLib",\n'
            '    products: [.library(name: "MyLib", targets: ["MyLib"])]\n'
            ')\n',
        )
        for i in range(file_count):
            _write(
                tmp_path / f"Sources/MyLib/F{i}.swift",
                f"import {ui_import}\n\nstruct F{i} {{}}\n",
            )
        return tmp_path

    def test_uikit_library_is_not_an_application(self, tmp_path: Path):
        repo = self._library_package(tmp_path, "UIKit")
        rules = SwiftArchitectureDetector().detect(_ctx(repo)).rules
        assert rules
        stats = rules[0].stats
        assert stats["is_application"] is False
        assert stats["framework"] == "Swift Library (UIKit)"

    def test_incidental_uikit_does_not_characterize_a_library(self, tmp_path: Path):
        """Alamofire imports UIKit in 3 of ~97 files; that is not a UIKit project."""
        _write(
            tmp_path / "Package.swift",
            'let package = Package(name: "Net", products: [.library(name: "Net", targets: ["Net"])])\n',
        )
        for i in range(30):
            _write(tmp_path / f"Sources/Net/F{i}.swift", f"import Foundation\n\nstruct F{i} {{}}\n")
        _write(tmp_path / "Sources/Net/Image.swift", "import UIKit\n\nstruct Image {}\n")

        rules = SwiftArchitectureDetector().detect(_ctx(tmp_path)).rules
        assert rules
        assert rules[0].stats["framework"] == "Swift Package / Library"

    def test_xcode_app_without_a_manifest_is_an_application(self, tmp_path: Path):
        """A real iOS app has an .xcodeproj and no Package.swift."""
        for i in range(12):
            _write(
                tmp_path / f"MyApp/Views/V{i}.swift",
                f"import UIKit\n\nclass V{i}: UIViewController {{}}\n",
            )
        _write(
            tmp_path / "MyApp/AppDelegate.swift",
            "import UIKit\n\n@UIApplicationMain\nclass AppDelegate: UIResponder {}\n",
        )
        rules = SwiftArchitectureDetector().detect(_ctx(tmp_path)).rules
        assert rules
        assert rules[0].stats["is_application"] is True
        assert rules[0].stats["framework"] == "UIKit Application"

    def test_executable_package_is_an_application(self, tmp_path: Path):
        _write(
            tmp_path / "Package.swift",
            'let package = Package(\n'
            '    name: "Server",\n'
            '    products: [.executable(name: "Server", targets: ["Server"])]\n'
            ')\n',
        )
        for i in range(12):
            _write(tmp_path / f"Sources/Server/R{i}.swift", f"import Vapor\n\nstruct R{i} {{}}\n")
        rules = SwiftArchitectureDetector().detect(_ctx(tmp_path)).rules
        assert rules
        assert rules[0].stats["is_application"] is True
        assert rules[0].stats["framework"] == "Vapor Server Application"


class TestPrimaryTestFrameworkFollowsUsage:
    """The primary test framework is the one actually used most.

    Regression: the frameworks list was built swift-testing-first and the primary
    was taken as frameworks[0], so Alamofire -- 31 files importing XCTest against
    5 importing swift-testing -- was reported as a swift-testing project.
    """

    def _repo(self, tmp_path: Path, xctest_files: int, swift_testing_files: int) -> Path:
        for i in range(xctest_files):
            _write(
                tmp_path / f"Tests/AppTests/XC{i}Tests.swift",
                f"import XCTest\n\nclass XC{i}Tests: XCTestCase {{}}\n",
            )
        for i in range(swift_testing_files):
            _write(
                tmp_path / f"Tests/AppTests/ST{i}Tests.swift",
                f"import Testing\n\n@Test func st{i}() {{}}\n",
            )
        return tmp_path

    def test_xctest_majority_wins(self, tmp_path: Path):
        repo = self._repo(tmp_path, xctest_files=31, swift_testing_files=5)
        rules = SwiftTestingDetector().detect(_ctx(repo)).rules
        assert rules
        assert rules[0].stats["primary_framework"] == "XCTest"

    def test_swift_testing_majority_wins(self, tmp_path: Path):
        repo = self._repo(tmp_path, xctest_files=2, swift_testing_files=20)
        rules = SwiftTestingDetector().detect(_ctx(repo)).rules
        assert rules
        assert rules[0].stats["primary_framework"] == "swift-testing"
