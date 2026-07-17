"""Integration tests for Ruby/Rails convention detectors."""

from __future__ import annotations

from pathlib import Path

from conventions.detectors.base import DetectorContext
from conventions.detectors.ruby import (
    RubyBuildDetector,
    RubyDatabaseDetector,
    RubyIndex,
    RubyRailsConventionsDetector,
    RubyTestingDetector,
)
from conventions.ratings import rate_convention


def _write(path: Path, content: str) -> None:
    """Write `content` to `path`, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _ctx(repo_root: Path) -> DetectorContext:
    return DetectorContext(
        repo_root=repo_root,
        selected_languages={"ruby"},
        max_files=200,
    )


# ---------------------------------------------------------------------------
# Test Indexer
# ---------------------------------------------------------------------------

def test_ruby_indexer(tmp_path: Path):
    _write(
        tmp_path / "Gemfile",
        """
        source 'https://rubygems.org'
        gem 'rails', '~> 7.0.0'
        gem 'rspec-rails'
        """,
    )
    _write(
        tmp_path / "app/models/user.rb",
        """
        class User < ApplicationRecord
          has_many :posts
          belongs_to :tenant

          # TODO: validate emails
          def active?
            true
          end
        end
        """,
    )

    index = RubyIndex(tmp_path)
    index.build()

    assert index.count_gem("rails") is True
    assert index.count_gem("rspec-rails") is True
    assert index.count_gem("devise") is False

    assert len(index.files) == 1
    file_idx = index.files["app/models/user.rb"]
    assert file_idx.class_names == ["User"]
    assert len(file_idx.associations) == 2
    assert file_idx.associations[0][0] == "has_many"
    assert file_idx.associations[0][1] == "posts"
    assert file_idx.todo_count == 1


# ---------------------------------------------------------------------------
# Test Rails Conventions Detector
# ---------------------------------------------------------------------------

def test_ruby_rails_conventions_detector(tmp_path: Path):
    _write(
        tmp_path / "Gemfile",
        "gem 'rails'",
    )
    _write(
        tmp_path / "app/controllers/users_controller.rb",
        "class UsersController < ApplicationController; end",
    )
    _write(
        tmp_path / "app/models/user.rb",
        "class User; end",
    )
    _write(
        tmp_path / ".rubocop.yml",
        "AllCops:\n  NewCops: enable",
    )

    ctx = _ctx(tmp_path)
    detector = RubyRailsConventionsDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.id == "ruby.conventions.rails_structure"
    assert rule.stats["is_rails"] is True
    assert rule.stats["has_rubocop"] is True
    assert "model" in rule.stats["layers"]
    assert "api" in rule.stats["layers"]

    score, _, _ = rate_convention(rule)
    assert score == 5


# ---------------------------------------------------------------------------
# Test Database Detector
# ---------------------------------------------------------------------------

def test_ruby_database_detector(tmp_path: Path):
    _write(
        tmp_path / "Gemfile",
        "gem 'rails'",
    )
    _write(
        tmp_path / "app/models/user.rb",
        """
        class User < ApplicationRecord
          has_many :posts
        end
        """,
    )
    _write(
        tmp_path / "db/migrate/20260716000000_create_users.rb",
        """
        class CreateUsers < ActiveRecord::Migration[7.0]
          def change
            create_table :users do |t|
              t.string :name
            end
          end
        end
        """,
    )

    ctx = _ctx(tmp_path)
    detector = RubyDatabaseDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.id == "ruby.conventions.database"
    assert "ActiveRecord" in rule.stats["libraries"]
    assert rule.stats["migration_count"] == 1
    assert rule.stats["associations_count"] == 1

    score, _, _ = rate_convention(rule)
    assert score == 5


# ---------------------------------------------------------------------------
# Test Testing Detector
# ---------------------------------------------------------------------------

def test_ruby_testing_detector(tmp_path: Path):
    _write(
        tmp_path / "Gemfile",
        "gem 'rspec-rails'",
    )
    _write(
        tmp_path / "spec/models/user_spec.rb",
        """
        require 'rails_helper'
        RSpec.describe User, type: :model do
          it 'is active' do
            expect(User.new.active?).to be_truthy
          end
        end
        """,
    )

    ctx = _ctx(tmp_path)
    detector = RubyTestingDetector()
    result = detector.detect(ctx)

    assert len(result.rules) == 1
    rule = result.rules[0]
    assert rule.stats["test_file_count"] == 1
    assert "RSpec" in rule.stats["frameworks"]
    assert rule.stats["primary_naming"] == "suffix_spec"

    score, _, _ = rate_convention(rule)
    assert score == 3


class TestRubyBuildDetector:
    """Bundler config drives the Test command; Rails vs gem changes the runner."""

    def _gemfile(self, tmp_path: Path, *gems: str) -> None:
        body = "source 'https://rubygems.org'\n" + "".join(f"gem '{g}'\n" for g in gems)
        _write(tmp_path / "Gemfile", body)
        _write(tmp_path / "app/models/user.rb", "class User < ApplicationRecord\nend\n")

    def test_rails_app_uses_the_rails_runner(self, tmp_path: Path):
        self._gemfile(tmp_path, "rails", "minitest")
        _write(tmp_path / "config/routes.rb", "Rails.application.routes.draw do\nend\n")
        rules = RubyBuildDetector().detect(_ctx(tmp_path)).rules
        assert rules
        stats = rules[0].stats
        assert stats["is_rails"] is True
        # `primary_tool` is what the CLAUDE.md renderer reads to pick commands.
        assert stats["primary_tool"] == "rails"

    def test_plain_gem_does_not_use_the_rails_runner(self, tmp_path: Path):
        """Sinatra has no Rails and runs `rake test`; telling it to run
        `rails test` hands it a command that does not exist."""
        self._gemfile(tmp_path, "minitest", "rake")
        _write(tmp_path / "sinatra.gemspec", "Gem::Specification.new do |s|\nend\n")
        rules = RubyBuildDetector().detect(_ctx(tmp_path)).rules
        assert rules
        stats = rules[0].stats
        assert stats["is_rails"] is False
        assert stats["primary_tool"] == "bundler"
        assert stats["is_gem"] is True

    def test_no_gemfile_emits_no_rule(self, tmp_path: Path):
        _write(tmp_path / "lib/thing.rb", "class Thing\nend\n")
        assert RubyBuildDetector().detect(_ctx(tmp_path)).rules == []

    def test_rule_is_rated(self, tmp_path: Path):
        self._gemfile(tmp_path, "rails", "rubocop")
        _write(tmp_path / "Gemfile.lock", "GEM\n  specs:\n")
        rules = RubyBuildDetector().detect(_ctx(tmp_path)).rules
        score, reason, _ = rate_convention(rules[0])
        assert 1 <= score <= 5
        assert "Bundler" in reason


class TestTruncationIsDisclosed:
    """A capped scan must not report the cap as the codebase size.

    Regression: Mastodon has 3219 Ruby files. At the default 2000-file cap the
    entire db/ layer went unseen, yet the rule stated "Ruby codebase (2000
    files)" and listed layers as if complete.
    """

    def test_truncated_scan_is_flagged(self, tmp_path: Path):
        _write(tmp_path / "Gemfile", "source 'https://rubygems.org'\ngem 'rails'\n")
        _write(tmp_path / "config/routes.rb", "Rails.application.routes.draw do\nend\n")
        for i in range(12):
            _write(tmp_path / f"app/models/m{i}.rb", f"class M{i}\nend\n")

        ctx = DetectorContext(repo_root=tmp_path, selected_languages={"ruby"}, max_files=5)
        rules = RubyRailsConventionsDetector().detect(ctx).rules
        assert rules
        stats = rules[0].stats
        assert stats["scan_truncated"] is True
        assert stats["file_count"] == 5
        assert "at least" in rules[0].description
        assert "truncated" in rules[0].description

    def test_complete_scan_is_not_flagged(self, tmp_path: Path):
        _write(tmp_path / "Gemfile", "source 'https://rubygems.org'\ngem 'rails'\n")
        _write(tmp_path / "config/routes.rb", "Rails.application.routes.draw do\nend\n")
        for i in range(3):
            _write(tmp_path / f"app/models/m{i}.rb", f"class M{i}\nend\n")

        ctx = DetectorContext(repo_root=tmp_path, selected_languages={"ruby"}, max_files=200)
        rules = RubyRailsConventionsDetector().detect(ctx).rules
        assert rules
        assert rules[0].stats["scan_truncated"] is False
        assert "at least" not in rules[0].description


class TestRubyDatabaseExposesPrimaryLibrary:
    """The tech-stack renderer reads `primary_library`; without it Database is blank."""

    def test_primary_library_is_set(self, tmp_path: Path):
        _write(tmp_path / "Gemfile", "source 'https://rubygems.org'\ngem 'rails'\n")
        _write(
            tmp_path / "app/models/user.rb",
            "class User < ApplicationRecord\n  has_many :posts\n  belongs_to :team\nend\n",
        )
        _write(tmp_path / "db/migrate/20240101_create_users.rb", "class CreateUsers\nend\n")
        rules = RubyDatabaseDetector().detect(_ctx(tmp_path)).rules
        assert rules
        assert rules[0].stats["primary_library"] == "ActiveRecord"
