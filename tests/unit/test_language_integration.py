"""Every registered language must be exposed through all its integration points.

Adding a language means more than writing detectors: it has to be accepted by
CLI validation, offered in the HTML filter, and declared in the SARIF report.
Kotlin, Java, C#, Ruby and Swift each shipped detectors while missing some or
all of these, so the language would work on auto-detect yet be rejected by
`--languages <lang>`. These tests derive the expected set from the detector
registry, so a new language fails here until it is wired up everywhere.
"""
from __future__ import annotations

import re
from pathlib import Path

from conventions.detectors.registry import DetectorRegistry, register_all_detectors

SRC = Path(__file__).resolve().parents[2] / "src" / "conventions"


def _registered_languages() -> set[str]:
    """Languages claimed by at least one registered detector."""
    register_all_detectors()
    languages: set[str] = set()
    for detector_class in DetectorRegistry.get_all():
        languages |= set(detector_class.languages or set())
    return languages


def test_registry_reports_languages():
    """Guard the guard: the helper must actually find languages."""
    languages = _registered_languages()
    assert {"python", "go", "node", "rust", "kotlin", "java", "csharp", "ruby", "swift"} <= languages


def test_cli_accepts_every_registered_language():
    source = (SRC / "cli.py").read_text()
    match = re.search(r"valid_langs = \{([^}]*)\}", source)
    assert match, "could not locate valid_langs in cli.py"
    valid = set(re.findall(r'"([a-z#+]+)"', match.group(1)))

    missing = _registered_languages() - valid
    assert not missing, (
        f"languages have detectors but are rejected by `--languages`: {sorted(missing)}"
    )


def test_sarif_declares_every_registered_language():
    source = (SRC / "outputs" / "sarif.py").read_text()
    match = re.search(r'"supportedLanguages":\s*\[([^\]]*)\]', source)
    assert match, "could not locate supportedLanguages in sarif.py"
    declared = set(re.findall(r'"([a-z#+]+)"', match.group(1)))

    missing = _registered_languages() - declared
    assert not missing, f"languages missing from SARIF supportedLanguages: {sorted(missing)}"


def test_html_filter_offers_every_registered_language():
    source = (SRC / "outputs" / "html.py").read_text()
    offered = set(re.findall(r'<option value="([a-z#+]+)">', source))

    missing = _registered_languages() - offered
    assert not missing, f"languages missing from the HTML language filter: {sorted(missing)}"
