"""Tests for the Python security detector's password-hashing domain guard."""
from __future__ import annotations

from pathlib import Path

from conventions.detectors.base import DetectorContext
from conventions.detectors.python.security import (
    PythonSecurityConventionsDetector,
)


def _password_rule(repo: Path):
    """Run the security detector and return the password_hashing rule, if any."""
    ctx = DetectorContext(
        repo_root=repo,
        selected_languages={"python"},
        max_files=100,
    )
    result = PythonSecurityConventionsDetector().detect(ctx)
    for rule in result.rules:
        if rule.id == "python.conventions.password_hashing":
            return rule
    return None


def test_http_digest_auth_not_flagged(tmp_path: Path):
    """An HTTP client using hashlib for digest auth is not password hashing.

    This mirrors httpx: hashlib is imported for digest auth, and there are
    generic auth/verify/hash symbols, but no password-storage function.
    """
    src = tmp_path / "src"
    src.mkdir()
    (src / "_auth.py").write_text(
        '''"""HTTP auth helpers."""
import hashlib


class BasicAuth:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class DigestAuth:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def build_digest_header(self, nonce, realm):
        return hashlib.md5(f"{self.username}:{realm}".encode()).hexdigest()


def verify(cert):
    """SSL verification (collides with the old loose gate)."""
    return cert is not None
'''
    )

    assert _password_rule(tmp_path) is None


def test_hashlib_password_storage_flagged_weak(tmp_path: Path):
    """Real password storage with hashlib is flagged as weak."""
    src = tmp_path / "src"
    src.mkdir()
    (src / "users.py").write_text(
        '''"""User model with password storage."""
import hashlib


class User:
    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()
'''
    )

    rule = _password_rule(tmp_path)
    assert rule is not None
    assert rule.stats["quality"] == "weak"
    assert rule.stats["primary_library"] == "hashlib"


def test_dedicated_lib_flagged_without_password_function(tmp_path: Path):
    """A dedicated password lib is reported on sight, no password fn required."""
    src = tmp_path / "src"
    src.mkdir()
    (src / "auth.py").write_text(
        '''"""Auth module using a dedicated hashing lib."""
import bcrypt


def make_hash(value):
    return bcrypt.hashpw(value, bcrypt.gensalt())
'''
    )

    rule = _password_rule(tmp_path)
    assert rule is not None
    assert rule.stats["quality"] == "good"
