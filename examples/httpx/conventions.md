# Code Conventions Report

*Generated: 2026-06-28 15:42:34*

## Summary

**Description:** The next generation HTTP client.

- **Repository:** `/Users/stephaniedover/projects/klaussy-repo-conventions/httpx_repo`
- **Languages:** python
- **Files scanned:** 60
- **Conventions detected:** 47

## Detected Conventions

| ID | Title | Confidence | Evidence | Docs |
|:---|:------|:----------:|:--------:|:-----|
| `python.conventions.naming` | PEP 8 snake_case naming | 95% | 0 | [docs](https://docs.astral.sh/ruff/) |
| `python.conventions.testing_framework` | pytest-based testing | 95% | 5 | [docs](https://docs.pytest.org/) |
| `python.conventions.typing_coverage` | High type annotation coverage | 95% | 2 | [docs](https://docs.python.org/3/library/typing.html) |
| `python.conventions.string_formatting` | Modern f-string formatting | 94% | 5 | [docs](https://docs.astral.sh/ruff/) |
| `generic.conventions.pr_template` | PR template | 90% | 0 |  |
| `generic.conventions.repo_layout` | Standard repository layout | 90% | 0 | [docs](https://docs.github.com/en/actions) |
| `python.conventions.cli_framework` | CLI framework: Click | 90% | 2 | [docs](https://click.palletsprojects.com/) |
| `python.conventions.context_managers` | Context manager usage | 90% | 5 | [docs](https://docs.python.org/3/library/typing.html) |
| `python.conventions.json_library` | JSON library: stdlib json | 90% | 3 | [docs](https://docs.python.org/3/library/json.html) |
| `python.conventions.type_checker_strictness` | Type checker: mypy (strict mode) | 90% | 0 | [docs](https://mypy.readthedocs.io/) |
| `python.test_conventions.parametrized` | Parametrized tests | 90% | 5 | [docs](https://docs.pytest.org/) |
| `python.conventions.class_style` | Data classes: NamedTuple | 90% | 2 | [docs](https://docs.pydantic.dev/) |
| `python.conventions.linter` | Linters: Ruff, mypy | 90% | 0 | [docs](https://docs.astral.sh/ruff/) |
| `python.conventions.validation_style` | Manual validation (ValueError/TypeError) | 90% | 5 | [docs](https://docs.pydantic.dev/) |
| `python.test_conventions.assertions` | Plain assert statements | 86% | 5 | [docs](https://docs.pytest.org/) |
| `python.test_conventions.fixtures` | pytest fixtures for test setup | 85% | 5 | [docs](https://docs.pytest.org/) |
| `python.conventions.async_http_client` | Async HTTP client: httpx (recommended) | 85% | 1 |  |
| `python.conventions.custom_decorators` | Custom decorator pattern: @click.option | 85% | 5 |  |
| `python.conventions.dependency_health` | Dependency health | 85% | 0 |  |
| `python.conventions.import_aliases` | Python import path (flat-layout) | 85% | 0 |  |
| `python.conventions.import_sorting` | Import sorting: Ruff (isort rules) | 85% | 0 | [docs](https://docs.astral.sh/ruff/) |
| `python.conventions.test_naming` | Test naming: Simple style (test_feature) | 84% | 3 | [docs](https://docs.pytest.org/) |
| `python.data_flow.import_graph` | Import dependency graph | 82% | 5 |  |
| `generic.conventions.history` | Project history | 80% | 0 |  |
| `python.conventions.lock_file` | Lock file: requirements.txt (pinned) | 80% | 0 | [docs](https://docs.astral.sh/uv/) |
| `python.conventions.test_structure` | Single test directory: tests/ | 80% | 0 | [docs](https://docs.pytest.org/) |
| `generic.conventions.ci_platform` | CI/CD: GitHub Actions | 80% | 0 | [docs](https://docs.github.com/en/actions) |
| `generic.conventions.dependency_updates` | Dependency updates: Dependabot | 80% | 0 | [docs](https://docs.github.com/en/code-security/dependabot) |
| `generic.conventions.config_access` | Config access patterns | 77% | 0 |  |
| `python.conventions.logging_library` | Uses Python standard logging | 76% | 2 | [docs](https://docs.python.org/3/library/logging.html) |
| `python.conventions.context_http_client` | HTTP clients with context managers | 75% | 5 |  |
| `generic.conventions.ci_quality` | CI/CD best practices | 70% | 0 | [docs](https://docs.github.com/en/actions) |
| `python.conventions.constant_naming` | lowercase constant naming | 70% | 5 | [docs](https://docs.astral.sh/ruff/) |
| `python.conventions.dependency_management` | Dependency management: pip (requirements.txt) | 70% | 0 | [docs](https://pip.pypa.io/) |
| `python.conventions.docstrings` | Partial docstring coverage | 70% | 4 | [docs](https://docs.astral.sh/ruff/) |
| `python.conventions.enum_usage` | Enum usage: Enum | 70% | 2 | [docs](https://docs.python.org/3/library/enum.html) |
| `python.conventions.env_separation` | Environment config: raw os.environ | 70% | 0 | [docs](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) |
| `python.conventions.exception_chaining` | Limited exception chaining | 70% | 4 | [docs](https://docs.python.org/3/library/typing.html) |
| `python.conventions.import_style` | Absolute imports preferred | 70% | 5 | [docs](https://docs.astral.sh/ruff/) |
| `python.conventions.path_handling` | Mixed path handling (pathlib and os.path) | 70% | 2 | [docs](https://docs.python.org/3/library/pathlib.html) |
| `python.conventions.secrets_access_style` | Configuration via os.environ direct access | 70% | 2 | [docs](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) |
| `python.test_conventions.mocking` | Mocking with pytest monkeypatch fixture | 65% | 3 | [docs](https://docs.python.org/3/library/unittest.mock.html) |
| `generic.conventions.standard_files` | Standard repository files | 60% | 0 | [docs](https://docs.github.com/en/actions) |
| `python.conventions.docstring_style` | Mixed docstring styles | 60% | 2 |  |
| `python.conventions.error_taxonomy` | Mixed exception naming conventions | 60% | 5 | [docs](https://docs.python.org/3/library/typing.html) |
| `python.conventions.timeouts` | Infrequent timeout specification | 60% | 5 | [docs](https://www.python-httpx.org/) |
| `python.conventions.error_wrapper` | Error wrapper pattern: str | 56% | 5 | [docs](https://docs.python.org/3/library/typing.html) |

## Convention Details

### PEP 8 snake_case naming

**ID:** `python.conventions.naming`  
**Category:** style  
**Language:** python  
**Confidence:** 95%
  
**Documentation:** [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)

Function names follow PEP 8 snake_case convention. 267/267 functions use snake_case. Found 23 module-level constants.

**Statistics:**

- snake_case_functions: `267`
- camel_case_functions: `0`
- snake_case_ratio: `1.0`
- module_constants: `23`

---

### pytest-based testing

**ID:** `python.conventions.testing_framework`  
**Category:** testing  
**Language:** python  
**Confidence:** 95%
  
**Documentation:** [https://docs.pytest.org/](https://docs.pytest.org/)

Uses pytest as primary testing framework. Found 196 pytest usages across 32 test files.

**Statistics:**

- framework_counts: `{'pytest': 196}`
- primary_framework: `pytest`
- test_file_count: `32`

**Evidence:**

1. `tests/test_utils.py:3-9`

```
import os
import random

import pytest

import httpx
from httpx._utils import URLPattern, get_environment_proxies
```

2. `tests/conftest.py:5-11`

```
import time
import typing

import pytest
import trustme
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import (
```

3. `tests/test_auth.py:6-12`

```

from urllib.request import parse_keqv_list

import pytest

import httpx

```

---

### High type annotation coverage

**ID:** `python.conventions.typing_coverage`  
**Category:** typing  
**Language:** python  
**Confidence:** 95%
  
**Documentation:** [https://docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html)

Type annotations are commonly used in this codebase. 396/396 functions (100%) have at least one type annotation.

**Statistics:**

- total_functions: `396`
- annotated_functions: `396`
- fully_annotated_functions: `66`
- any_annotation_coverage: `1.0`
- full_annotation_coverage: `0.167`

**Evidence:**

1. `httpx/_decoders.py:32-42`

```
except ImportError:  # pragma: no cover
    zstandard = None  # type: ignore


class ContentDecoder:
    def decode(self, data: bytes) -> bytes:
        raise NotImplementedError()  # pragma: no cover

    def flush(self) -> bytes:
        raise NotImplementedError()  # pragma: no cover
```

2. `httpx/_decoders.py:35-45`

```

class ContentDecoder:
    def decode(self, data: bytes) -> bytes:
        raise NotImplementedError()  # pragma: no cover

    def flush(self) -> bytes:
        raise NotImplementedError()  # pragma: no cover


class IdentityDecoder(ContentDecoder):
```

---

### Modern f-string formatting

**ID:** `python.conventions.string_formatting`  
**Category:** code_style  
**Language:** python  
**Confidence:** 94%
  
**Documentation:** [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)

Uses f-strings consistently for string formatting. 92/95 (97%) use f-strings.

**Statistics:**

- total_formats: `95`
- fstring_count: `92`
- format_method_count: `2`
- percent_count: `1`
- fstring_ratio: `0.968`
- dominant_style: `fstring`

**Evidence:**

1. `httpx/_main.py:120-126`

```
    ]
    method = request.method.decode("ascii")
    target = request.url.target.decode("ascii")
    lines = [f"{method} {target} {version}"] + [
        f"{name.decode('ascii')}: {value.decode('ascii')}" for name, value in headers
    ]
    return "\n".join(lines)
```

2. `httpx/_main.py:121-127`

```
    method = request.method.decode("ascii")
    target = request.url.target.decode("ascii")
    lines = [f"{method} {target} {version}"] + [
        f"{name.decode('ascii')}: {value.decode('ascii')}" for name, value in headers
    ]
    return "\n".join(lines)

```

3. `httpx/_main.py:138-144`

```
        if reason_phrase is None
        else reason_phrase.decode("ascii")
    )
    lines = [f"{version} {status} {reason}"] + [
        f"{name.decode('ascii')}: {value.decode('ascii')}" for name, value in headers
    ]
    return "\n".join(lines)
```

---

### PR template

**ID:** `generic.conventions.pr_template`  
**Category:** git  
**Language:** generic  
**Confidence:** 90%

PR template at .github/pull_request_template.md.

**Statistics:**

- template_path: `.github/pull_request_template.md`
- has_multiple_templates: `False`
- template_count: `0`
- sections: `[]`

---

### Standard repository layout

**ID:** `generic.conventions.repo_layout`  
**Category:** structure  
**Language:** generic  
**Confidence:** 90%
  
**Documentation:** [https://docs.github.com/en/actions](https://docs.github.com/en/actions)

Repository has standard directories: .github (GitHub configuration), docs (documentation), httpx (workspace), scripts (scripts), tests (tests)

**Statistics:**

- found_directories: `['.github', 'docs', 'httpx', 'scripts', 'tests']`
- directory_tree: `{'.github': {'purpose': 'GitHub configuration', 'children': {'CONTRIBUTING.md': {'type': 'file', 'purpose': ''}, 'FUNDING.yml': {'type': 'file', 'purpose': ''}, 'ISSUE_TEMPLATE': {'type': 'dir', 'purpose': '', 'children': {'1-issue.md': {'type': 'file', 'purpose': ''}, 'config.yml': {'type': 'file', 'purpose': ''}}}, 'PULL_REQUEST_TEMPLATE.md': {'type': 'file', 'purpose': ''}, 'dependabot.yml': {'type': 'file', 'purpose': ''}, 'workflows': {'type': 'dir', 'purpose': '', 'children': {'publish.yml': {'type': 'file', 'purpose': ''}, 'test-suite.yml': {'type': 'file', 'purpose': ''}}}}}, 'docs': {'purpose': 'documentation', 'children': {'CNAME': {'type': 'file', 'purpose': ''}, 'advanced': {'type': 'dir', 'purpose': '', 'children': {'authentication.md': {'type': 'file', 'purpose': ''}, 'clients.md': {'type': 'file', 'purpose': ''}, 'event-hooks.md': {'type': 'file', 'purpose': ''}, 'extensions.md': {'type': 'file', 'purpose': ''}, 'proxies.md': {'type': 'file', 'purpose': ''}, 'resource-limits.md': {'type': 'file', 'purpose': ''}, 'ssl.md': {'type': 'file', 'purpose': ''}, 'text-encodings.md': {'type': 'file', 'purpose': ''}, 'timeouts.md': {'type': 'file', 'purpose': ''}, 'transports.md': {'type': 'file', 'purpose': ''}}}, 'api.md': {'type': 'file', 'purpose': ''}, 'async.md': {'type': 'file', 'purpose': ''}, 'code_of_conduct.md': {'type': 'file', 'purpose': ''}, 'compatibility.md': {'type': 'file', 'purpose': ''}, 'contributing.md': {'type': 'file', 'purpose': ''}, 'css': {'type': 'dir', 'purpose': '', 'children': {'custom.css': {'type': 'file', 'purpose': ''}}}, 'environment_variables.md': {'type': 'file', 'purpose': ''}, 'exceptions.md': {'type': 'file', 'purpose': ''}, 'http2.md': {'type': 'file', 'purpose': ''}, 'img': {'type': 'dir', 'purpose': '', 'children': {}}, 'index.md': {'type': 'file', 'purpose': ''}, 'logging.md': {'type': 'file', 'purpose': ''}, 'overrides': {'type': 'dir', 'purpose': '', 'children': {'partials': {'type': 'dir', 'purpose': '', 'children': {'nav.html': {'type': 'file', 'purpose': ''}}}}}, 'quickstart.md': {'type': 'file', 'purpose': ''}, 'third_party_packages.md': {'type': 'file', 'purpose': ''}, 'troubleshooting.md': {'type': 'file', 'purpose': ''}}}, 'httpx': {'purpose': 'source code', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, '__version__.py': {'type': 'file', 'purpose': ''}, '_api.py': {'type': 'file', 'purpose': ''}, '_auth.py': {'type': 'file', 'purpose': ''}, '_client.py': {'type': 'file', 'purpose': ''}, '_config.py': {'type': 'file', 'purpose': ''}, '_content.py': {'type': 'file', 'purpose': ''}, '_decoders.py': {'type': 'file', 'purpose': ''}, '_exceptions.py': {'type': 'file', 'purpose': ''}, '_main.py': {'type': 'file', 'purpose': ''}, '_models.py': {'type': 'file', 'purpose': ''}, '_multipart.py': {'type': 'file', 'purpose': ''}, '_status_codes.py': {'type': 'file', 'purpose': ''}, '_transports': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'asgi.py': {'type': 'file', 'purpose': ''}, 'base.py': {'type': 'file', 'purpose': ''}, 'default.py': {'type': 'file', 'purpose': ''}, 'mock.py': {'type': 'file', 'purpose': ''}, 'wsgi.py': {'type': 'file', 'purpose': ''}}}, '_types.py': {'type': 'file', 'purpose': ''}, '_urlparse.py': {'type': 'file', 'purpose': ''}, '_urls.py': {'type': 'file', 'purpose': ''}, '_utils.py': {'type': 'file', 'purpose': ''}, 'py.typed': {'type': 'file', 'purpose': ''}}}, 'scripts': {'purpose': 'scripts', 'children': {'check': {'type': 'file', 'purpose': ''}, 'clean': {'type': 'file', 'purpose': ''}, 'docs': {'type': 'file', 'purpose': ''}, 'install': {'type': 'file', 'purpose': ''}, 'lint': {'type': 'file', 'purpose': ''}, 'publish': {'type': 'file', 'purpose': ''}, 'sync-version': {'type': 'file', 'purpose': ''}, 'test': {'type': 'file', 'purpose': ''}}}, 'tests': {'purpose': 'tests', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'client': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_async_client.py': {'type': 'file', 'purpose': ''}, 'test_auth.py': {'type': 'file', 'purpose': ''}, 'test_client.py': {'type': 'file', 'purpose': ''}, 'test_cookies.py': {'type': 'file', 'purpose': ''}, 'test_event_hooks.py': {'type': 'file', 'purpose': ''}, 'test_headers.py': {'type': 'file', 'purpose': ''}, 'test_properties.py': {'type': 'file', 'purpose': ''}, 'test_proxies.py': {'type': 'file', 'purpose': ''}, 'test_queryparams.py': {'type': 'file', 'purpose': ''}, 'test_redirects.py': {'type': 'file', 'purpose': ''}}}, 'common.py': {'type': 'file', 'purpose': ''}, 'concurrency.py': {'type': 'file', 'purpose': ''}, 'conftest.py': {'type': 'file', 'purpose': ''}, 'fixtures': {'type': 'dir', 'purpose': '', 'children': {}}, 'models': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_cookies.py': {'type': 'file', 'purpose': ''}, 'test_headers.py': {'type': 'file', 'purpose': ''}, 'test_queryparams.py': {'type': 'file', 'purpose': ''}, 'test_requests.py': {'type': 'file', 'purpose': ''}, 'test_responses.py': {'type': 'file', 'purpose': ''}, 'test_url.py': {'type': 'file', 'purpose': ''}, 'test_whatwg.py': {'type': 'file', 'purpose': ''}, 'whatwg.json': {'type': 'file', 'purpose': ''}}}, 'test_api.py': {'type': 'file', 'purpose': ''}, 'test_asgi.py': {'type': 'file', 'purpose': ''}, 'test_auth.py': {'type': 'file', 'purpose': ''}, 'test_config.py': {'type': 'file', 'purpose': ''}, 'test_content.py': {'type': 'file', 'purpose': ''}, 'test_decoders.py': {'type': 'file', 'purpose': ''}, 'test_exceptions.py': {'type': 'file', 'purpose': ''}, 'test_exported_members.py': {'type': 'file', 'purpose': ''}, 'test_main.py': {'type': 'file', 'purpose': ''}, 'test_multipart.py': {'type': 'file', 'purpose': ''}, 'test_status_codes.py': {'type': 'file', 'purpose': ''}, 'test_timeouts.py': {'type': 'file', 'purpose': ''}, 'test_utils.py': {'type': 'file', 'purpose': ''}, 'test_wsgi.py': {'type': 'file', 'purpose': ''}}}}`
- project_description: `The next generation HTTP client.`

---

### CLI framework: Click

**ID:** `python.conventions.cli_framework`  
**Category:** cli  
**Language:** python  
**Confidence:** 90%
  
**Documentation:** [https://click.palletsprojects.com/](https://click.palletsprojects.com/)

Uses Click for CLI.

**Statistics:**

- frameworks: `['click']`
- primary_framework: `click`
- framework_details: `{'click': {'name': 'Click', 'import_count': 2}}`

**Evidence:**

1. `tests/test_main.py:1-7`

```
import os
import typing

from click.testing import CliRunner

import httpx

```

2. `httpx/_main.py:5-11`

```
import sys
import typing

import click
import pygments.lexers
import pygments.util
import rich.console
```

---

### Context manager usage

**ID:** `python.conventions.context_managers`  
**Category:** resource_management  
**Language:** python  
**Confidence:** 90%
  
**Documentation:** [https://docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html)

Uses context managers for resource management. 24 with statements. Types: http_client (5).

**Statistics:**

- total_with_statements: `24`
- sync_count: `24`
- async_count: `0`
- context_types: `{'http_client': 5}`

**Evidence:**

1. `httpx/_main.py:476-482`

```
        method = "POST" if content or data or files or json else "GET"

    try:
        with Client(proxy=proxy, timeout=timeout, http2=http2, verify=verify) as client:
            with client.stream(
                method,
                url,
```

2. `httpx/_main.py:477-483`

```

    try:
        with Client(proxy=proxy, timeout=timeout, http2=http2, verify=verify) as client:
            with client.stream(
                method,
                url,
                params=list(params),
```

3. `httpx/_api.py:99-105`

```
    <Response [200 OK]>
    ```
    """
    with Client(
        cookies=cookies,
        proxy=proxy,
        verify=verify,
```

---

### JSON library: stdlib json

**ID:** `python.conventions.json_library`  
**Category:** serialization  
**Language:** python  
**Confidence:** 90%
  
**Documentation:** [https://docs.python.org/3/library/json.html](https://docs.python.org/3/library/json.html)

Uses standard library json (21 usages).

**Statistics:**

- json_library_counts: `{'json': 21}`
- primary_library: `json`
- total_usages: `21`

**Evidence:**

1. `httpx/_main.py:1-7`

```
from __future__ import annotations

import functools
import json
import sys
import typing

```

2. `httpx/_content.py:2-8`

```

import inspect
import warnings
from json import dumps as json_dumps
from typing import (
    Any,
    AsyncIterable,
```

3. `httpx/_models.py:3-9`

```
import codecs
import datetime
import email.message
import json as jsonlib
import re
import typing
import urllib.request
```

---

### Type checker: mypy (strict mode)

**ID:** `python.conventions.type_checker_strictness`  
**Category:** tooling  
**Language:** python  
**Confidence:** 90%
  
**Documentation:** [https://mypy.readthedocs.io/](https://mypy.readthedocs.io/)

Uses mypy in strict mode - catches the most type errors.

**Statistics:**

- type_checker: `mypy`
- strictness: `strict`
- strict_options: `['strict mode']`
- config_file: `pyproject.toml`

---

### Parametrized tests

**ID:** `python.test_conventions.parametrized`  
**Category:** testing  
**Language:** python  
**Confidence:** 90%
  
**Documentation:** [https://docs.pytest.org/](https://docs.pytest.org/)

Uses @pytest.mark.parametrize for data-driven tests. Found 44 parametrized test functions.

**Statistics:**

- parametrize_count: `44`

**Evidence:**

1. `tests/test_utils.py:7-17`

```

import httpx
from httpx._utils import URLPattern, get_environment_proxies


@pytest.mark.parametrize(
    "encoding",
    (
        "utf-32",
        "utf-8-sig",
```

2. `tests/test_utils.py:33-43`

```
    response = httpx.Response(200, content=content)
    with pytest.raises(json.decoder.JSONDecodeError):
        response.json()


@pytest.mark.parametrize(
    ("encoding", "expected"),
    (
        ("utf-16-be", "utf-16"),
        ("utf-16-le", "utf-16"),
```

3. `tests/test_utils.py:84-94`

```
            'HTTP Request: GET http://127.0.0.1:8000/ "HTTP/1.1 200 OK"',
        ),
    ]


@pytest.mark.parametrize(
    ["environment", "proxies"],
    [
        ({}, {}),
        ({"HTTP_PROXY": "http://127.0.0.1"}, {"http://": "http://127.0.0.1"}),
```

---

### Data classes: NamedTuple

**ID:** `python.conventions.class_style`  
**Category:** code_style  
**Language:** python  
**Confidence:** 90%
  
**Documentation:** [https://docs.pydantic.dev/](https://docs.pydantic.dev/)

Uses NamedTuple for structured data. 2/2 structured classes use this pattern.

**Statistics:**

- dataclass_count: `0`
- pydantic_count: `0`
- attrs_count: `0`
- namedtuple_count: `2`
- plain_count: `55`
- dominant_style: `namedtuple`

**Evidence:**

1. `httpx/_urlparse.py:153-163`

```
# the stdlib 'ipaddress' module for IP address validation.
IPv4_STYLE_HOSTNAME = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$")
IPv6_STYLE_HOSTNAME = re.compile(r"^\[.*\]$")


class ParseResult(typing.NamedTuple):
    scheme: str
    userinfo: str
    host: str
    port: int | None
```

2. `httpx/_auth.py:338-348`

```

        message = f'Unexpected qop value "{qop!r}" in digest auth'
        raise ProtocolError(message, request=request)


class _DigestAuthChallenge(typing.NamedTuple):
    realm: bytes
    nonce: bytes
    algorithm: str
    opaque: bytes | None
```

---

### Linters: Ruff, mypy

**ID:** `python.conventions.linter`  
**Category:** tooling  
**Language:** python  
**Confidence:** 90%
  
**Documentation:** [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)

Uses Ruff, mypy for code quality.

**Statistics:**

- linters: `['ruff', 'mypy']`
- primary_linter: `ruff`
- linter_details: `{'ruff': {'name': 'Ruff', 'config_file': 'pyproject.toml', 'features': ['custom rules', 'ignores configured']}, 'mypy': {'name': 'mypy', 'config_file': 'pyproject.toml'}}`

---

### Manual validation (ValueError/TypeError)

**ID:** `python.conventions.validation_style`  
**Category:** validation  
**Language:** python  
**Confidence:** 90%
  
**Documentation:** [https://docs.pydantic.dev/](https://docs.pydantic.dev/)

Uses Manual validation (ValueError/TypeError) for input validation. 17/17 (100%) validation patterns use this approach.

**Statistics:**

- validation_counts: `{'manual': 17}`
- dominant_style: `manual`
- dominant_ratio: `1.0`

**Evidence:**

1. `httpx/_urls.py:95-101`

```
            for key, value in kwargs.items():
                if key not in allowed:
                    message = f"{key!r} is an invalid keyword argument for URL()"
                    raise TypeError(message)
                if value is not None and not isinstance(value, allowed[key]):
                    expected = allowed[key].__name__
                    seen = type(value).__name__
```

2. `httpx/_urls.py:100-106`

```
                    expected = allowed[key].__name__
                    seen = type(value).__name__
                    message = f"Argument {key!r} must be {expected} but got {seen}"
                    raise TypeError(message)
                if isinstance(value, bytes):
                    kwargs[key] = value.decode("ascii")

```

3. `httpx/_urls.py:118-124`

```
        elif isinstance(url, URL):
            self._uri_reference = url._uri_reference.copy_with(**kwargs)
        else:
            raise TypeError(
                "Invalid type for url.  Expected str or httpx.URL,"
                f" got {type(url)}: {url!r}"
            )
```

---

### Plain assert statements

**ID:** `python.test_conventions.assertions`  
**Category:** testing  
**Language:** python  
**Confidence:** 86%
  
**Documentation:** [https://docs.pytest.org/](https://docs.pytest.org/)

Uses plain Python assert statements for test assertions. 1268 assert statements. Uses pytest.raises for exception testing (128 usages).

**Statistics:**

- assertion_counts: `{'plain_assert': 1268, 'pytest_raises': 128, 'pytest_warns': 4}`
- style: `plain_assert`

**Evidence:**

1. `tests/test_utils.py:31-37`

```
def test_bad_utf_like_encoding():
    content = b"\x00\x00\x00\x00"
    response = httpx.Response(200, content=content)
    with pytest.raises(json.decoder.JSONDecodeError):
        response.json()


```

2. `tests/test_auth.py:22-28`

```

    # No other requests are made.
    response = httpx.Response(content=b"Hello, world!", status_code=200)
    with pytest.raises(StopIteration):
        flow.send(response)


```

3. `tests/test_auth.py:37-43`

```

    # If a 200 response is returned, then no other requests are made.
    response = httpx.Response(content=b"Hello, world!", status_code=200)
    with pytest.raises(StopIteration):
        flow.send(response)


```

---

### pytest fixtures for test setup

**ID:** `python.test_conventions.fixtures`  
**Category:** testing  
**Language:** python  
**Confidence:** 85%
  
**Documentation:** [https://docs.pytest.org/](https://docs.pytest.org/)

Uses pytest @fixture decorator for test setup. Found 7 fixtures. Uses 1 conftest.py file(s) for shared fixtures.

**Statistics:**

- fixture_counts: `{'pytest_fixture': 7}`
- conftest_files: `1`
- pattern: `pytest_fixture`

**Evidence:**

1. `tests/conftest.py:29-39`

```
    "NO_PROXY",
    "SSLKEYLOGFILE",
}


@pytest.fixture(scope="function", autouse=True)
def clean_environ():
    """Keeps os.environ clean for every test without having to mock os.environ"""
    original_environ = os.environ.copy()
    os.environ.clear()
```

2. `tests/conftest.py:180-190`

```
        {"type": "http.response.start", "status": 301, "headers": [[b"location", b"/"]]}
    )
    await send({"type": "http.response.body"})


@pytest.fixture(scope="session")
def cert_authority():
    return trustme.CA()


```

3. `tests/conftest.py:185-195`

```
@pytest.fixture(scope="session")
def cert_authority():
    return trustme.CA()


@pytest.fixture(scope="session")
def localhost_cert(cert_authority):
    return cert_authority.issue_cert("localhost")


```

---

### Async HTTP client: httpx (recommended)

**ID:** `python.conventions.async_http_client`  
**Category:** async  
**Language:** python  
**Confidence:** 85%

Uses httpx for HTTP requests.

**Statistics:**

- http_client_counts: `{'httpx': 74}`
- primary_client: `httpx`
- quality: `excellent`

**Evidence:**

1. `httpx/_transports/default.py:33-39`

```
if typing.TYPE_CHECKING:
    import ssl  # pragma: no cover

    import httpx  # pragma: no cover

from .._config import DEFAULT_LIMITS, Limits, Proxy, create_ssl_context
from .._exceptions import (
```

---

### Custom decorator pattern: @click.option

**ID:** `python.conventions.custom_decorators`  
**Category:** decorators  
**Language:** python  
**Confidence:** 85%

Uses custom decorator @click.option (17 usages).

**Statistics:**

- top_decorator: `click.option`
- usage_count: `17`
- other_custom_decorators: `[]`

**Evidence:**

1. `httpx/_main.py:310-320`

```
    ctx.exit()


@click.command(add_help_option=False)
@click.argument("url", type=str)
@click.option(
    "--method",
    "-m",
    "method",
    type=str,
```

2. `httpx/_main.py:320-330`

```
    help=(
        "Request method, such as GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD. "
        "[Default: GET, or POST if a request body is included]"
    ),
)
@click.option(
    "--params",
    "-p",
    "params",
    type=(str, str),
```

3. `httpx/_main.py:328-338`

```
    "params",
    type=(str, str),
    multiple=True,
    help="Query parameters to include in the request URL.",
)
@click.option(
    "--content",
    "-c",
    "content",
    type=str,
```

---

### Dependency health

**ID:** `python.conventions.dependency_health`  
**Category:** dependencies  
**Language:** python  
**Confidence:** 85%

Dependency health: 19 deps; pinning: exact (16/19).

**Statistics:**

- total_deps: `19`
- exact_count: `16`
- compatible_count: `0`
- minimum_count: `0`
- unpinned_count: `3`
- pinning_strategy: `exact`
- has_lock_file: `False`

---

### Python import path (flat-layout)

**ID:** `python.conventions.import_aliases`  
**Category:** language  
**Language:** python  
**Confidence:** 85%

Python flat-layout. Import: `httpx`.

**Statistics:**

- layout: `flat`
- package_name: `httpx`

---

### Import sorting: Ruff (isort rules)

**ID:** `python.conventions.import_sorting`  
**Category:** tooling  
**Language:** python  
**Confidence:** 85%
  
**Documentation:** [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)

Uses Ruff (isort rules) for import organization.

**Statistics:**

- sorters: `['ruff']`
- primary_sorter: `ruff`
- sorter_details: `{'ruff': {'name': 'Ruff (isort rules)', 'config_file': 'pyproject.toml', 'has_grouping': False}}`
- has_grouping: `False`
- has_known_first_party: `False`
- has_sections: `False`
- has_force_sort_within_sections: `False`
- profile: `None`

---

### Test naming: Simple style (test_feature)

**ID:** `python.conventions.test_naming`  
**Category:** testing  
**Language:** python  
**Confidence:** 84%
  
**Documentation:** [https://docs.pytest.org/](https://docs.pytest.org/)

Uses Simple style (test_feature) naming. 523/539 (97%) test functions. Uses 2 test classes for grouping.

**Statistics:**

- total_test_functions: `539`
- pattern_counts: `{'simple': 523, 'action_result': 16}`
- test_class_count: `2`
- dominant_pattern: `simple`

**Evidence:**

1. `tests/test_utils.py:22-28`

```
        "utf-32-le",
    ),
)
def test_encoded(encoding):
    content = '{"abc": 123}'.encode(encoding)
    response = httpx.Response(200, content=content)
    assert response.json() == {"abc": 123}
```

2. `tests/test_utils.py:28-34`

```
    assert response.json() == {"abc": 123}


def test_bad_utf_like_encoding():
    content = b"\x00\x00\x00\x00"
    response = httpx.Response(200, content=content)
    with pytest.raises(json.decoder.JSONDecodeError):
```

3. `tests/test_utils.py:44-50`

```
        ("utf-32-le", "utf-32"),
    ),
)
def test_guess_by_bom(encoding, expected):
    content = '\ufeff{"abc": 123}'.encode(encoding)
    response = httpx.Response(200, content=content)
    assert response.json() == {"abc": 123}
```

---

### Import dependency graph

**ID:** `python.data_flow.import_graph`  
**Category:** data_flow  
**Language:** python  
**Confidence:** 82%

Import graph: 60 files, 112 internal imports. 1 dependency clusters. Circular dependencies: 16. httpx/_exceptions.py -> httpx/_models.py; httpx/_models.py -> httpx/_types.py; httpx/_urls.py -> httpx/_utils.py. Most imported: httpx/__init__.py (32 dependents).

**Statistics:**

- total_files: `60`
- total_edges: `112`
- cycle_count: `16`
- cluster_count: `1`
- top_fan_in: `[('httpx/__init__.py', 32), ('httpx/_types.py', 9), ('httpx/_models.py', 8), ('httpx/_exceptions.py', 8), ('httpx/_urls.py', 7)]`
- top_fan_out: `[('httpx/__init__.py', 13), ('httpx/_client.py', 12), ('httpx/_models.py', 8), ('httpx/_api.py', 5), ('httpx/_transports/__init__.py', 5)]`
- core_modules: `[{'path': 'httpx/_types.py', 'dependents': 9, 'responsibility': 'Type definitions for type checking purposes.'}, {'path': 'httpx/_exceptions.py', 'dependents': 8, 'responsibility': 'Our exception hierarchy:'}, {'path': 'httpx/_models.py', 'dependents': 8, 'responsibility': 'models'}, {'path': 'httpx/_urls.py', 'dependents': 7, 'responsibility': 'urls'}, {'path': 'httpx/_utils.py', 'dependents': 6, 'responsibility': 'utils'}, {'path': 'httpx/_transports/base.py', 'dependents': 6, 'responsibility': 'base'}]`

**Evidence:**

1. `httpx/__init__.py:1-4`

```
from .__version__ import __description__, __title__, __version__
from ._api import *
from ._auth import *
from ._client import *
```

2. `httpx/_types.py:1-4`

```
"""
Type definitions for type checking purposes.
"""

```

3. `httpx/_models.py:1-4`

```
from __future__ import annotations

import codecs
import datetime
```

---

### Project history

**ID:** `generic.conventions.history`  
**Category:** documentation  
**Language:** generic  
**Confidence:** 80%

Detected 9 decision log items and 0 pitfalls.

**Statistics:**

- detected_decisions: `['v0.28.0 (28th November, 2024): For users of the standard verify=True or verify=False cases, or verify=<ssl_context> case this should require no changes.', 'v0.28.0 (28th November, 2024): The verify argument as a string argument is now deprecated and will raise warnings.', 'v0.28.0 (28th November, 2024): The cert argument is now deprecated and will raise warnings.', 'v0.28.0 (28th November, 2024): The deprecated proxies argument has now been removed.', 'v0.28.0 (28th November, 2024): The deprecated app argument has now been removed.', 'v0.26.0 (20th December, 2023): The proxy argument was added.', 'v0.26.0 (20th December, 2023): The proxies argument is now deprecated.', 'v0.24.0 (6th April, 2023): The rfc3986 dependancy has been removed.', 'v0.23.2 (2nd January, 2023): Partially revert the API breaking change in 0.23.1, which removed RawURL.']`
- detected_pitfalls: `[]`

---

### Lock file: requirements.txt (pinned)

**ID:** `python.conventions.lock_file`  
**Category:** dependencies  
**Language:** python  
**Confidence:** 80%
  
**Documentation:** [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

Dependencies locked with requirements.txt (pinned).

**Statistics:**

- lock_files: `{'pip_pinned': 'requirements.txt (pinned)'}`
- primary_lock: `pip_pinned`
- quality: `basic`
- has_lock: `True`

---

### Single test directory: tests/

**ID:** `python.conventions.test_structure`  
**Category:** testing  
**Language:** python  
**Confidence:** 80%
  
**Documentation:** [https://docs.pytest.org/](https://docs.pytest.org/)

All tests in 'tests/' directory. 32 test files.

**Statistics:**

- test_file_count: `32`
- test_directories: `{'tests': 32}`
- has_unit: `False`
- has_integration: `False`
- has_e2e: `False`
- structure: `flat`
- categories: `[]`

---

### CI/CD: GitHub Actions

**ID:** `generic.conventions.ci_platform`  
**Category:** ci_cd  
**Language:** generic  
**Confidence:** 80%
  
**Documentation:** [https://docs.github.com/en/actions](https://docs.github.com/en/actions)

Uses GitHub Actions for CI/CD. 2 workflow(s) configured.

**Statistics:**

- platforms: `['github_actions']`
- platform_details: `{'github_actions': {'name': 'GitHub Actions', 'workflow_count': 2, 'files': ['publish.yml', 'test-suite.yml']}}`

---

### Dependency updates: Dependabot

**ID:** `generic.conventions.dependency_updates`  
**Category:** dependencies  
**Language:** generic  
**Confidence:** 80%
  
**Documentation:** [https://docs.github.com/en/code-security/dependabot](https://docs.github.com/en/code-security/dependabot)

Automated dependency updates via Dependabot for pip, github-actions.

**Statistics:**

- tools: `['dependabot']`
- tool_details: `{'dependabot': {'name': 'Dependabot', 'ecosystems': ['pip', 'github-actions']}}`
- primary_tool: `dependabot`

---

### Config access patterns

**ID:** `generic.conventions.config_access`  
**Category:** configuration  
**Language:** generic  
**Confidence:** 77%

Config access: 12 direct env accesses.

**Statistics:**

- access_style: `direct env (python_os_environ)`
- env_access_counts: `{'python_os_environ': 12}`
- libraries: `{}`
- secrets_managers: `{}`
- total_env_accesses: `12`

---

### Uses Python standard logging

**ID:** `python.conventions.logging_library`  
**Category:** logging  
**Language:** python  
**Confidence:** 76%
  
**Documentation:** [https://docs.python.org/3/library/logging.html](https://docs.python.org/3/library/logging.html)

Exclusively uses Python standard logging for logging. Found 3 usages.

**Statistics:**

- library_counts: `{'stdlib_logging': 3}`
- primary_library: `stdlib_logging`
- primary_ratio: `1.0`

**Evidence:**

1. `tests/test_utils.py:1-5`

```
import json
import logging
import os
import random

```

2. `httpx/_client.py:2-8`

```

import datetime
import enum
import logging
import time
import typing
import warnings
```

---

### HTTP clients with context managers

**ID:** `python.conventions.context_http_client`  
**Category:** resource_management  
**Language:** python  
**Confidence:** 75%

Uses context managers for HTTP client lifecycle. 5 usages.

**Statistics:**

- usage_count: `5`
- category: `http_client`

**Evidence:**

1. `httpx/_main.py:476-482`

```
        method = "POST" if content or data or files or json else "GET"

    try:
        with Client(proxy=proxy, timeout=timeout, http2=http2, verify=verify) as client:
            with client.stream(
                method,
                url,
```

2. `httpx/_main.py:477-483`

```

    try:
        with Client(proxy=proxy, timeout=timeout, http2=http2, verify=verify) as client:
            with client.stream(
                method,
                url,
                params=list(params),
```

3. `httpx/_api.py:99-105`

```
    <Response [200 OK]>
    ```
    """
    with Client(
        cookies=cookies,
        proxy=proxy,
        verify=verify,
```

---

### CI/CD best practices

**ID:** `generic.conventions.ci_quality`  
**Category:** ci_cd  
**Language:** generic  
**Confidence:** 70%
  
**Documentation:** [https://docs.github.com/en/actions](https://docs.github.com/en/actions)

CI configuration includes: testing, matrix builds.

**Statistics:**

- has_test_workflow: `True`
- has_lint_workflow: `False`
- has_deploy_workflow: `False`
- has_caching: `False`
- has_matrix: `True`
- features: `['testing', 'matrix builds']`

---

### lowercase constant naming

**ID:** `python.conventions.constant_naming`  
**Category:** naming  
**Language:** python  
**Confidence:** 70%
  
**Documentation:** [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)

Uses lowercase naming for module-level values. 31/44 use lowercase.

**Statistics:**

- all_caps_count: `13`
- lowercase_count: `31`
- all_caps_ratio: `0.295`
- style: `lowercase`

**Evidence:**

1. `httpx/_multipart.py:269-273`

```
        """
        boundary_length = len(self.boundary)
        length = 0

        for field in self.fields:
```

2. `httpx/_content.py:145-149`

```
    body = urlencode(plain_data, doseq=True).encode("utf-8")
    content_length = str(len(body))
    content_type = "application/x-www-form-urlencoded"
    headers = {"Content-Length": content_length, "Content-Type": content_type}
    return headers, ByteStream(body)
```

3. `httpx/_content.py:161-165`

```
    body = text.encode("utf-8")
    content_length = str(len(body))
    content_type = "text/plain; charset=utf-8"
    headers = {"Content-Length": content_length, "Content-Type": content_type}
    return headers, ByteStream(body)
```

---

### Dependency management: pip (requirements.txt)

**ID:** `python.conventions.dependency_management`  
**Category:** dependencies  
**Language:** python  
**Confidence:** 70%
  
**Documentation:** [https://pip.pypa.io/](https://pip.pypa.io/)

Uses pip (requirements.txt) for dependencies.

**Statistics:**

- tools: `['pip']`
- primary_tool: `pip`
- tool_details: `{'pip': {'name': 'pip (requirements.txt)', 'pinned_deps': 15, 'unpinned_deps': 0}}`

---

### Partial docstring coverage

**ID:** `python.conventions.docstrings`  
**Category:** documentation  
**Language:** python  
**Confidence:** 70%
  
**Documentation:** [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)

Some functions have docstrings. Functions: 133/396 (34%).

**Statistics:**

- total_public_functions: `396`
- documented_functions: `133`
- function_doc_ratio: `0.336`
- total_classes: `84`
- documented_classes: `61`
- class_doc_ratio: `0.726`

**Evidence:**

1. `httpx/_decoders.py:203-213`

```
class MultiDecoder(ContentDecoder):
    """
    Handle the case where multiple encodings have been applied.
    """

    def __init__(self, children: typing.Sequence[ContentDecoder]) -> None:
        """
        'children' should be a sequence of decoders in the order in which
        each was applied.
        """
```

2. `httpx/_types.py:94-104`

```
        raise NotImplementedError(
            "The '__iter__' method must be implemented."
        )  # pragma: no cover
        yield b""  # pragma: no cover

    def close(self) -> None:
        """
        Subclasses can override this method to release any network resources
        after a request/response cycle is complete.
        """
```

3. `httpx/_decoders.py:34-40`

```


class ContentDecoder:
    def decode(self, data: bytes) -> bytes:
        raise NotImplementedError()  # pragma: no cover

    def flush(self) -> bytes:
```

---

### Enum usage: Enum

**ID:** `python.conventions.enum_usage`  
**Category:** code_style  
**Language:** python  
**Confidence:** 70%
  
**Documentation:** [https://docs.python.org/3/library/enum.html](https://docs.python.org/3/library/enum.html)

Uses Python enums for categorical values. Found 2 enum class(es). Types: Enum (1), IntEnum (1).

**Statistics:**

- enum_count: `2`
- enum_types: `{'Enum': 1, 'IntEnum': 1}`
- enum_names: `['ClientState', 'codes']`

**Evidence:**

1. `httpx/_client.py:120-130`

```
ACCEPT_ENCODING = ", ".join(
    [key for key in SUPPORTED_DECODERS.keys() if key != "identity"]
)


class ClientState(enum.Enum):
    # UNOPENED:
    #   The client has been instantiated, but has not been used to send a request,
    #   or been opened by entering the context of a `with` block.
    UNOPENED = 1
```

2. `httpx/_status_codes.py:3-13`

```
from enum import IntEnum

__all__ = ["codes"]


class codes(IntEnum):
    """HTTP status codes and reason phrases

    Status codes from the following RFCs are all observed:

```

---

### Environment config: raw os.environ

**ID:** `python.conventions.env_separation`  
**Category:** security  
**Language:** python  
**Confidence:** 70%
  
**Documentation:** [https://docs.pydantic.dev/latest/concepts/pydantic_settings/](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

Uses os.environ/os.getenv directly. Found 2 usages.

**Statistics:**

- approach: `raw_environ`
- has_env_files: `False`
- raw_environ_count: `2`

---

### Limited exception chaining

**ID:** `python.conventions.exception_chaining`  
**Category:** error_handling  
**Language:** python  
**Confidence:** 70%
  
**Documentation:** [https://docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html)

Rarely uses 'raise X from Y'. 16/96 (17%) raises use chaining. Use 'raise X from Y' to preserve context or 'raise X from None' to suppress.

**Statistics:**

- chained_raises: `16`
- unchained_raises: `80`
- bare_raises: `2`
- chaining_ratio: `0.167`

**Evidence:**

1. `httpx/_decoders.py:73-79`

```
            if was_first_attempt:
                self.decompressor = zlib.decompressobj(-zlib.MAX_WBITS)
                return self.decode(data)
            raise DecodingError(str(exc)) from exc

    def flush(self) -> bytes:
        try:
```

2. `httpx/_decoders.py:79-85`

```
        try:
            return self.decompressor.flush()
        except zlib.error as exc:  # pragma: no cover
            raise DecodingError(str(exc)) from exc


class GZipDecoder(ContentDecoder):
```

3. `httpx/_decoders.py:35-41`

```

class ContentDecoder:
    def decode(self, data: bytes) -> bytes:
        raise NotImplementedError()  # pragma: no cover

    def flush(self) -> bytes:
        raise NotImplementedError()  # pragma: no cover
```

---

### Absolute imports preferred

**ID:** `python.conventions.import_style`  
**Category:** code_style  
**Language:** python  
**Confidence:** 70%
  
**Documentation:** [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)

Prefers absolute imports. 87 relative vs 136 absolute imports.

**Statistics:**

- relative_count: `87`
- absolute_count: `136`
- relative_ratio: `0.39`
- style: `absolute`

**Evidence:**

1. `httpx/_decoders.py:11-17`

```
import typing
import zlib

from ._exceptions import DecodingError

# Brotli support is optional
try:
```

2. `httpx/_types.py:22-28`

```
)

if TYPE_CHECKING:  # pragma: no cover
    from ._auth import Auth  # noqa: F401
    from ._config import Proxy, Timeout  # noqa: F401
    from ._models import Cookies, Headers, Request  # noqa: F401
    from ._urls import URL, QueryParams  # noqa: F401
```

3. `httpx/_types.py:23-29`

```

if TYPE_CHECKING:  # pragma: no cover
    from ._auth import Auth  # noqa: F401
    from ._config import Proxy, Timeout  # noqa: F401
    from ._models import Cookies, Headers, Request  # noqa: F401
    from ._urls import URL, QueryParams  # noqa: F401

```

---

### Mixed path handling (pathlib and os.path)

**ID:** `python.conventions.path_handling`  
**Category:** code_style  
**Language:** python  
**Confidence:** 70%
  
**Documentation:** [https://docs.python.org/3/library/pathlib.html](https://docs.python.org/3/library/pathlib.html)

Uses both pathlib (2) and os.path (1). Consider standardizing on pathlib.

**Statistics:**

- pathlib_count: `2`
- ospath_count: `1`
- pathlib_ratio: `0.667`
- style: `mixed`

**Evidence:**

1. `httpx/_multipart.py:5-11`

```
import os
import re
import typing
from pathlib import Path

from ._types import (
    AsyncByteStream,
```

2. `httpx/_multipart.py:142-148`

```
                # all 4 parameters included
                filename, fileobj, content_type, headers = value  # type: ignore
        else:
            filename = Path(str(getattr(value, "name", "upload"))).name
            fileobj = value

        if content_type is None:
```

---

### Configuration via os.environ direct access

**ID:** `python.conventions.secrets_access_style`  
**Category:** security  
**Language:** python  
**Confidence:** 70%
  
**Documentation:** [https://docs.pydantic.dev/latest/concepts/pydantic_settings/](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

Uses os.environ direct access. Found 2 usages.

**Statistics:**

- os_environ: `2`

**Evidence:**

1. `httpx/_config.py:31-37`

```
    import certifi

    if verify is True:
        if trust_env and os.environ.get("SSL_CERT_FILE"):  # pragma: nocover
            ctx = ssl.create_default_context(cafile=os.environ["SSL_CERT_FILE"])
        elif trust_env and os.environ.get("SSL_CERT_DIR"):  # pragma: nocover
            ctx = ssl.create_default_context(capath=os.environ["SSL_CERT_DIR"])
```

2. `httpx/_config.py:33-39`

```
    if verify is True:
        if trust_env and os.environ.get("SSL_CERT_FILE"):  # pragma: nocover
            ctx = ssl.create_default_context(cafile=os.environ["SSL_CERT_FILE"])
        elif trust_env and os.environ.get("SSL_CERT_DIR"):  # pragma: nocover
            ctx = ssl.create_default_context(capath=os.environ["SSL_CERT_DIR"])
        else:
            # Default case...
```

---

### Mocking with pytest monkeypatch fixture

**ID:** `python.test_conventions.mocking`  
**Category:** testing  
**Language:** python  
**Confidence:** 65%
  
**Documentation:** [https://docs.python.org/3/library/unittest.mock.html](https://docs.python.org/3/library/unittest.mock.html)

Uses pytest monkeypatch fixture for test mocking. Found 3 usages.

**Statistics:**

- mock_counts: `{'monkeypatch': 3}`
- primary_pattern: `monkeypatch`

**Evidence:**

1. `tests/test_auth.py:9-19`

```
import pytest

import httpx


def test_basic_auth():
    auth = httpx.BasicAuth(username="user", password="pass")
    request = httpx.Request("GET", "https://www.example.com")

    # The initial request should include a basic auth header.
```

2. `tests/test_config.py:6-16`

```
import pytest

import httpx


def test_load_ssl_config():
    context = httpx.create_ssl_context()
    assert context.verify_mode == ssl.VerifyMode.CERT_REQUIRED
    assert context.check_hostname is True

```

3. `tests/client/test_proxies.py:11-21`

```
    """
    u = httpx.URL(url)
    return httpcore.URL(scheme=u.raw_scheme, host=u.raw_host, port=u.port, target="/")


def test_socks_proxy():
    url = httpx.URL("http://www.example.com")

    for proxy in ("socks5://localhost/", "socks5h://localhost/"):
        client = httpx.Client(proxy=proxy)
```

---

### Standard repository files

**ID:** `generic.conventions.standard_files`  
**Category:** structure  
**Language:** generic  
**Confidence:** 60%
  
**Documentation:** [https://docs.github.com/en/actions](https://docs.github.com/en/actions)

Repository has standard files: README.md, LICENSE.md, CHANGELOG.md, .gitignore

**Statistics:**

- found_files: `['README.md', 'LICENSE.md', 'CHANGELOG.md', '.gitignore']`

---

### Mixed docstring styles

**ID:** `python.conventions.docstring_style`  
**Category:** documentation  
**Language:** python  
**Confidence:** 60%

Docstrings use mixed styles: Google style, Sphinx/reST style.

**Statistics:**

- style_counts: `{'google': 2, 'sphinx': 1}`
- primary_style: `google`
- primary_ratio: `0.667`

**Evidence:**

1. `httpx/_urls.py:161-177`

```
        """
        The URL password as a string, with URL decoding applied.
        For example: "a secret"
        """
        userinfo = self._uri_reference.userinfo
        return unquote(userinfo.partition(":")[2])

    @property
    def host(self) -> str:
        """
```

2. `httpx/_urls.py:188-204`

```
        host: str = self._uri_reference.host

        if host.startswith("xn--"):
            host = idna.decode(host)

        return host

    @property
    def raw_host(self) -> bytes:
        """
```

---

### Mixed exception naming conventions

**ID:** `python.conventions.error_taxonomy`  
**Category:** error_handling  
**Language:** python  
**Confidence:** 60%
  
**Documentation:** [https://docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html)

Exception naming is mixed: 15 *Error, 1 *Exception out of 28 total.

**Statistics:**

- total_custom_exceptions: `28`
- error_suffix_count: `15`
- exception_suffix_count: `1`
- exception_names: `['HTTPError', 'RequestError', 'TransportError', 'TimeoutException', 'ConnectTimeout', 'ReadTimeout', 'WriteTimeout', 'PoolTimeout', 'NetworkError', 'ReadError', 'WriteError', 'ConnectError', 'CloseError', 'ProxyError', 'UnsupportedProtocol', 'ProtocolError', 'LocalProtocolError', 'RemoteProtocolError', 'DecodingError', 'TooManyRedirects']`
- consistency: `0.536`

**Evidence:**

1. `httpx/_exceptions.py:71-77`

```
]


class HTTPError(Exception):
    """
    Base class for `RequestError` and `HTTPStatusError`.

```

2. `httpx/_exceptions.py:104-110`

```
        self._request = request


class RequestError(HTTPError):
    """
    Base class for all exceptions that may occur when issuing a `.request()`.
    """
```

3. `httpx/_exceptions.py:120-126`

```
        self._request = request


class TransportError(RequestError):
    """
    Base class for all exceptions that occur at the level of the Transport API.
    """
```

---

### Infrequent timeout specification

**ID:** `python.conventions.timeouts`  
**Category:** resilience  
**Language:** python  
**Confidence:** 60%
  
**Documentation:** [https://www.python-httpx.org/](https://www.python-httpx.org/)

Timeouts are rarely specified on external calls. Only 52 calls with explicit timeouts.

**Statistics:**

- timeout_indicators: `52`
- no_timeout_indicators: `445`
- timeout_ratio: `0.105`

**Evidence:**

1. `tests/conftest.py:259-265`

```
                return

            try:
                await asyncio.wait_for(self.restart_requested.wait(), timeout=0.1)
            except asyncio.TimeoutError:
                continue

```

2. `tests/test_timeouts.py:7-13`

```
async def test_read_timeout(server):
    timeout = httpx.Timeout(None, read=1e-6)

    async with httpx.AsyncClient(timeout=timeout) as client:
        with pytest.raises(httpx.ReadTimeout):
            await client.get(server.url.copy_with(path="/slow_response"))

```

3. `tests/test_timeouts.py:16-22`

```
async def test_write_timeout(server):
    timeout = httpx.Timeout(None, write=1e-6)

    async with httpx.AsyncClient(timeout=timeout) as client:
        with pytest.raises(httpx.WriteTimeout):
            data = b"*" * 1024 * 1024 * 100
            await client.put(server.url.copy_with(path="/slow_response"), content=data)
```

---

### Error wrapper pattern: str

**ID:** `python.conventions.error_wrapper`  
**Category:** error_handling  
**Language:** python  
**Confidence:** 56%
  
**Documentation:** [https://docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html)

Uses 'str' as a common error handler function. Called in 8/55 (15%) except blocks.

**Statistics:**

- wrapper_function: `str`
- usage_count: `8`
- total_handlers: `55`
- usage_ratio: `0.145`
- other_wrappers: `[]`

**Evidence:**

1. `httpx/_decoders.py:67-77`

```
    def decode(self, data: bytes) -> bytes:
        was_first_attempt = self.first_attempt
        self.first_attempt = False
        try:
            return self.decompressor.decompress(data)
        except zlib.error as exc:
            if was_first_attempt:
                self.decompressor = zlib.decompressobj(-zlib.MAX_WBITS)
                return self.decode(data)
            raise DecodingError(str(exc)) from exc
```

2. `httpx/_decoders.py:76-86`

```
            raise DecodingError(str(exc)) from exc

    def flush(self) -> bytes:
        try:
            return self.decompressor.flush()
        except zlib.error as exc:  # pragma: no cover
            raise DecodingError(str(exc)) from exc


class GZipDecoder(ContentDecoder):
```

3. `httpx/_decoders.py:93-103`

```
        self.decompressor = zlib.decompressobj(zlib.MAX_WBITS | 16)

    def decode(self, data: bytes) -> bytes:
        try:
            return self.decompressor.decompress(data)
        except zlib.error as exc:
            raise DecodingError(str(exc)) from exc

    def flush(self) -> bytes:
        try:
```

---
