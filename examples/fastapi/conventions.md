# Code Conventions Report

*Generated: 2026-06-28 12:36:48*

## Summary

**Description:** FastAPI framework, high performance, easy to learn, fast to code, ready for production

- **Repository:** `/Users/stephaniedover/projects/klaussy-repo-conventions/fastapi_repo`
- **Languages:** python
- **Files scanned:** 668
- **Conventions detected:** 65

## Detected Conventions

| ID | Title | Confidence | Evidence | Docs |
|:---|:------|:----------:|:--------:|:-----|
| `python.conventions.dependency_management` | Dependency management: uv | 95% | 0 | [docs](https://docs.astral.sh/uv/) |
| `python.conventions.import_sorting` | Import organization: Ruff with grouping | 95% | 0 | [docs](https://docs.astral.sh/ruff/) |
| `python.conventions.lock_file` | Lock file: uv.lock | 95% | 0 | [docs](https://docs.astral.sh/uv/) |
| `python.conventions.naming` | PEP 8 snake_case naming | 95% | 0 | [docs](https://docs.astral.sh/ruff/) |
| `python.conventions.testing_framework` | pytest-based testing | 95% | 5 | [docs](https://docs.pytest.org/) |
| `python.conventions.typing_coverage` | High type annotation coverage | 95% | 4 | [docs](https://docs.python.org/3/library/typing.html) |
| `python.conventions.string_formatting` | Modern f-string formatting | 95% | 5 | [docs](https://docs.astral.sh/ruff/) |
| `python.conventions.path_handling` | Modern pathlib for path handling | 92% | 5 | [docs](https://docs.python.org/3/library/pathlib.html) |
| `generic.conventions.ci_quality` | CI/CD best practices | 90% | 0 | [docs](https://docs.github.com/en/actions) |
| `generic.conventions.repo_layout` | Standard repository layout | 90% | 0 | [docs](https://docs.github.com/en/actions) |
| `generic.conventions.runtime_prerequisites` | Runtime prerequisites | 90% | 0 |  |
| `python.conventions.api_routes` | API routes | 90% | 0 |  |
| `python.conventions.cli_framework` | CLI framework: Typer | 90% | 5 | [docs](https://typer.tiangolo.com/) |
| `python.conventions.context_managers` | Context manager usage | 90% | 4 | [docs](https://docs.python.org/3/library/typing.html) |
| `python.conventions.data_class_style` | Data class style: Pydantic for API + dataclasses for internal | 90% | 5 | [docs](https://docs.pydantic.dev/) |
| `python.conventions.decorator_caching` | Caching decorator pattern | 90% | 5 | [docs](https://docs.python.org/3/library/typing.html) |
| `python.conventions.json_library` | JSON library: mixed | 90% | 4 | [docs](https://docs.python.org/3/library/json.html) |
| `python.conventions.type_checker_strictness` | Type checker: mypy (strict mode) | 90% | 0 | [docs](https://mypy.readthedocs.io/) |
| `python.data_flow.import_graph` | Import dependency graph | 90% | 5 |  |
| `python.test_conventions.fixtures` | pytest fixtures for test setup | 90% | 5 | [docs](https://docs.pytest.org/) |
| `python.test_conventions.mocking` | Mocking with pytest monkeypatch fixture | 90% | 5 | [docs](https://docs.python.org/3/library/unittest.mock.html) |
| `python.test_conventions.parametrized` | Parametrized tests | 90% | 5 | [docs](https://docs.pytest.org/) |
| `python.conventions.linter` | Linters: Ruff, mypy | 90% | 0 | [docs](https://docs.astral.sh/ruff/) |
| `python.conventions.logging_library` | Uses Python standard logging | 90% | 5 | [docs](https://docs.python.org/3/library/logging.html) |
| `python.test_conventions.assertions` | Plain assert statements | 89% | 5 | [docs](https://docs.pytest.org/) |
| `generic.conventions.config_access` | Config access patterns | 88% | 0 |  |
| `python.conventions.api_versioning` | URL-based API versioning | 85% | 5 | [docs](https://fastapi.tiangolo.com/) |
| `python.conventions.async_http_client` | Async HTTP client: httpx (recommended) | 85% | 5 |  |
| `python.conventions.auth_pattern` | OAuth2 authentication | 85% | 5 | [docs](https://pyjwt.readthedocs.io/) |
| `python.conventions.db_session_lifecycle` | FastAPI-style session dependency injection | 85% | 1 | [docs](https://docs.sqlalchemy.org/) |
| `python.conventions.dependency_health` | Dependency health | 85% | 0 |  |
| `python.conventions.env_separation` | Environment separation: Pydantic Settings | 85% | 5 | [docs](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) |
| `python.conventions.import_aliases` | Python import path (flat-layout) | 85% | 0 |  |
| `python.conventions.secrets_access_style` | Structured configuration with Pydantic Settings | 85% | 5 | [docs](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) |
| `python.conventions.class_style` | Data classes: Pydantic models | 85% | 5 | [docs](https://docs.pydantic.dev/) |
| `python.conventions.test_naming` | Test naming: Simple style (test_feature) | 84% | 3 | [docs](https://docs.pytest.org/) |
| `python.conventions.schema_library` | Primary schema library: Pydantic | 84% | 5 | [docs](https://docs.pydantic.dev/) |
| `python.conventions.api_framework` | Primary API framework: FastAPI | 83% | 5 | [docs](https://fastapi.tiangolo.com/) |
| `generic.conventions.history` | Project history | 80% | 0 |  |
| `python.conventions.caching` | Caching: functools.lru_cache | 80% | 2 | [docs](https://redis.io/docs/) |
| `python.conventions.enum_usage` | Enum usage: Enum | 80% | 4 | [docs](https://docs.python.org/3/library/enum.html) |
| `python.conventions.pagination_pattern` | Cursor-based pagination | 80% | 0 | [docs](https://fastapi.tiangolo.com/) |
| `generic.conventions.ci_platform` | CI/CD: GitHub Actions | 80% | 0 | [docs](https://docs.github.com/en/actions) |
| `generic.conventions.dependency_updates` | Dependency updates: Dependabot | 80% | 0 | [docs](https://docs.github.com/en/code-security/dependabot) |
| `generic.conventions.git_hooks` | Git hooks: pre-commit | 80% | 0 | [docs](https://pre-commit.com/) |
| `python.conventions.background_jobs` | Background jobs with FastAPI BackgroundTasks | 72% | 4 | [docs](https://fastapi.tiangolo.com/) |
| `python.conventions.constant_naming` | lowercase constant naming | 70% | 5 | [docs](https://docs.astral.sh/ruff/) |
| `python.conventions.context_file_io` | File I/O with context managers | 70% | 4 |  |
| `python.conventions.custom_decorators` | Custom decorator pattern: @deprecated | 70% | 4 |  |
| `python.conventions.error_handling_boundary` | HTTP errors raised in service layer | 70% | 5 | [docs](https://fastapi.tiangolo.com/) |
| `python.conventions.exception_chaining` | Limited exception chaining | 70% | 4 | [docs](https://docs.python.org/3/library/typing.html) |
| `python.conventions.exception_handlers` | Semi-centralized exception handling | 70% | 5 | [docs](https://fastapi.tiangolo.com/) |
| `python.conventions.import_style` | Absolute imports preferred | 70% | 5 | [docs](https://docs.astral.sh/ruff/) |
| `python.conventions.openapi_docs` | OpenAPI with FastAPI (default) | 70% | 0 | [docs](https://swagger.io/specification/) |
| `python.conventions.response_envelope` | Response envelope classes | 70% | 5 | [docs](https://docs.pydantic.dev/) |
| `python.conventions.test_structure` | Distributed test files | 70% | 0 | [docs](https://docs.pytest.org/) |
| `python.conventions.validation_style` | Mixed validation approaches | 70% | 5 | [docs](https://docs.pydantic.dev/) |
| `generic.conventions.standard_files` | Standard repository files | 60% | 0 | [docs](https://docs.github.com/en/actions) |
| `python.conventions.db_connection_pooling` | Default connection pooling | 60% | 0 | [docs](https://docs.sqlalchemy.org/) |
| `python.conventions.docstrings` | Low docstring coverage | 60% | 4 | [docs](https://docs.astral.sh/ruff/) |
| `python.conventions.error_taxonomy` | Mixed exception naming conventions | 60% | 5 | [docs](https://docs.python.org/3/library/typing.html) |
| `python.conventions.pre_commit_hooks` | Pre-commit hooks configured | 60% | 0 | [docs](https://pre-commit.com/) |
| `python.conventions.timeouts` | Infrequent timeout specification | 60% | 5 | [docs](https://www.python-httpx.org/) |
| `python.conventions.error_wrapper` | Error wrapper pattern: time.sleep | 57% | 5 | [docs](https://docs.python.org/3/library/typing.html) |
| `python.conventions.health_checks` | Health check functions | 50% | 1 | [docs](https://fastapi.tiangolo.com/) |

## Convention Details

### Dependency management: uv

**ID:** `python.conventions.dependency_management`  
**Category:** dependencies  
**Language:** python  
**Confidence:** 95%
  
**Documentation:** [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

Uses uv with lock file for dependencies.

**Statistics:**

- tools: `['uv']`
- primary_tool: `uv`
- tool_details: `{'uv': {'name': 'uv', 'has_lock': True}}`

---

### Import organization: Ruff with grouping

**ID:** `python.conventions.import_sorting`  
**Category:** tooling  
**Language:** python  
**Confidence:** 95%
  
**Documentation:** [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)

Uses Ruff isort rules with proper import grouping. Has first-party package configuration.

**Statistics:**

- sorters: `['ruff']`
- primary_sorter: `ruff`
- sorter_details: `{'ruff': {'name': 'Ruff (isort rules)', 'config_file': 'pyproject.toml', 'has_grouping': True}}`
- has_grouping: `True`
- has_known_first_party: `True`
- has_sections: `False`
- has_force_sort_within_sections: `False`
- profile: `None`

---

### Lock file: uv.lock

**ID:** `python.conventions.lock_file`  
**Category:** dependencies  
**Language:** python  
**Confidence:** 95%
  
**Documentation:** [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

Dependencies locked with uv.lock.

**Statistics:**

- lock_files: `{'uv': 'uv.lock'}`
- primary_lock: `uv`
- quality: `modern`
- has_lock: `True`

---

### PEP 8 snake_case naming

**ID:** `python.conventions.naming`  
**Category:** style  
**Language:** python  
**Confidence:** 95%
  
**Documentation:** [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)

Function names follow PEP 8 snake_case convention. 363/363 functions use snake_case. Found 28 module-level constants.

**Statistics:**

- snake_case_functions: `363`
- camel_case_functions: `0`
- snake_case_ratio: `1.0`
- module_constants: `28`

---

### pytest-based testing

**ID:** `python.conventions.testing_framework`  
**Category:** testing  
**Language:** python  
**Confidence:** 95%
  
**Documentation:** [https://docs.pytest.org/](https://docs.pytest.org/)

Uses pytest as primary testing framework. Found 942 pytest usages across 496 test files.

**Statistics:**

- framework_counts: `{'pytest': 942, 'unittest': 1}`
- primary_framework: `pytest`
- test_file_count: `496`

**Evidence:**

1. `tests/test_datastructures.py:2-8`

```
from pathlib import Path
from typing import cast

import pytest
from fastapi import FastAPI, UploadFile
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.testclient import TestClient
```

2. `tests/test_union_body_discriminator_annotated.py:2-8`

```

from typing import Annotated

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
```

3. `tests/test_computed_fields.py:1-4`

```
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
```

---

### High type annotation coverage

**ID:** `python.conventions.typing_coverage`  
**Category:** typing  
**Language:** python  
**Confidence:** 95%
  
**Documentation:** [https://docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html)

Type annotations are commonly used in this codebase. 434/438 functions (99%) have at least one type annotation.

**Statistics:**

- total_functions: `438`
- annotated_functions: `434`
- fully_annotated_functions: `243`
- any_annotation_coverage: `0.991`
- full_annotation_coverage: `0.555`

**Evidence:**

1. `fastapi/params.py:24-34`

```


class Param(FieldInfo):  # type: ignore[misc]  # ty: ignore[subclass-of-final-class]
    in_: ParamTypes

    def __init__(
        self,
        default: Any = Undefined,
        *,
        default_factory: Callable[[], Any] | None = _Unset,
```

2. `fastapi/params.py:128-138`

```

        use_kwargs = {k: v for k, v in kwargs.items() if v is not _Unset}

        super().__init__(**use_kwargs)  # ty: ignore[invalid-argument-type]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.default})"


class Path(Param):  # type: ignore[misc]
```

3. `scripts/translation_fixer.py:22-32`

```

cli = typer.Typer()


@cli.callback()
def callback():
    pass


def iter_all_lang_paths(lang_path_root: Path) -> Iterable[Path]:
```

---

### Modern f-string formatting

**ID:** `python.conventions.string_formatting`  
**Category:** code_style  
**Language:** python  
**Confidence:** 95%
  
**Documentation:** [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)

Uses f-strings consistently for string formatting. 273/274 (100%) use f-strings.

**Statistics:**

- total_formats: `274`
- fstring_count: `273`
- format_method_count: `1`
- percent_count: `0`
- fstring_ratio: `0.996`
- dominant_style: `fstring`

**Evidence:**

1. `fastapi/params.py:131-137`

```
        super().__init__(**use_kwargs)  # ty: ignore[invalid-argument-type]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.default})"


class Path(Param):  # type: ignore[misc]
```

2. `fastapi/params.py:575-581`

```
        super().__init__(**use_kwargs)  # ty: ignore[invalid-argument-type]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.default})"


class Form(Body):  # type: ignore[misc]
```

3. `fastapi/applications.py:1128-1134`

```
                    oauth2_redirect_url = root_path + oauth2_redirect_url
                return get_swagger_ui_html(
                    openapi_url=openapi_url,
                    title=f"{self.title} - Swagger UI",
                    oauth2_redirect_url=oauth2_redirect_url,
                    init_oauth=self.swagger_ui_init_oauth,
                    swagger_ui_parameters=self.swagger_ui_parameters,
```

---

### Modern pathlib for path handling

**ID:** `python.conventions.path_handling`  
**Category:** code_style  
**Language:** python  
**Confidence:** 92%
  
**Documentation:** [https://docs.python.org/3/library/pathlib.html](https://docs.python.org/3/library/pathlib.html)

Uses pathlib consistently for file paths. 64/70 (91%) use pathlib.

**Statistics:**

- pathlib_count: `64`
- ospath_count: `6`
- pathlib_ratio: `0.914`
- style: `pathlib`

**Evidence:**

1. `fastapi/__init__.py:15-21`

```
from .param_functions import File as File
from .param_functions import Form as Form
from .param_functions import Header as Header
from .param_functions import Path as Path
from .param_functions import Query as Query
from .param_functions import Security as Security
from .requests import Request as Request
```

2. `fastapi/encoders.py:12-18`

```
    IPv6Interface,
    IPv6Network,
)
from pathlib import Path, PurePath
from re import Pattern
from types import GeneratorType
from typing import Annotated, Any
```

3. `scripts/contributors.py:3-9`

```
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
```

---

### CI/CD best practices

**ID:** `generic.conventions.ci_quality`  
**Category:** ci_cd  
**Language:** generic  
**Confidence:** 90%
  
**Documentation:** [https://docs.github.com/en/actions](https://docs.github.com/en/actions)

CI configuration includes: testing, deployment, caching, matrix builds.

**Statistics:**

- has_test_workflow: `True`
- has_lint_workflow: `False`
- has_deploy_workflow: `True`
- has_caching: `True`
- has_matrix: `True`
- features: `['testing', 'deployment', 'caching', 'matrix builds']`

---

### Standard repository layout

**ID:** `generic.conventions.repo_layout`  
**Category:** structure  
**Language:** generic  
**Confidence:** 90%
  
**Documentation:** [https://docs.github.com/en/actions](https://docs.github.com/en/actions)

Repository has standard directories: .github (GitHub configuration), docs (documentation), fastapi (workspace), scripts (scripts), tests (tests)

**Statistics:**

- found_directories: `['.github', 'docs', 'fastapi', 'scripts', 'tests']`
- directory_tree: `{'.github': {'purpose': 'GitHub configuration', 'children': {'DISCUSSION_TEMPLATE': {'type': 'dir', 'purpose': '', 'children': {'questions.yml': {'type': 'file', 'purpose': ''}, 'translations.yml': {'type': 'file', 'purpose': ''}}}, 'ISSUE_TEMPLATE': {'type': 'dir', 'purpose': '', 'children': {'config.yml': {'type': 'file', 'purpose': ''}, 'privileged.yml': {'type': 'file', 'purpose': ''}}}, 'dependabot.yml': {'type': 'file', 'purpose': ''}, 'labeler.yml': {'type': 'file', 'purpose': ''}, 'workflows': {'type': 'dir', 'purpose': '', 'children': {'add-to-project.yml': {'type': 'file', 'purpose': ''}, 'build-docs.yml': {'type': 'file', 'purpose': ''}, 'contributors.yml': {'type': 'file', 'purpose': ''}, 'create-draft-release.yml': {'type': 'file', 'purpose': ''}, 'deploy-docs.yml': {'type': 'file', 'purpose': ''}, 'detect-conflicts.yml': {'type': 'file', 'purpose': ''}, 'guard-dependencies.yml': {'type': 'file', 'purpose': ''}, 'issue-manager.yml': {'type': 'file', 'purpose': ''}, 'label-approved.yml': {'type': 'file', 'purpose': ''}, 'labeler.yml': {'type': 'file', 'purpose': ''}, 'latest-changes.yml': {'type': 'file', 'purpose': ''}, 'notify-translations.yml': {'type': 'file', 'purpose': ''}, 'people.yml': {'type': 'file', 'purpose': ''}, 'pre-commit.yml': {'type': 'file', 'purpose': ''}, 'prepare-release.yml': {'type': 'file', 'purpose': ''}, 'publish.yml': {'type': 'file', 'purpose': ''}, 'smokeshow.yml': {'type': 'file', 'purpose': ''}, 'sponsors.yml': {'type': 'file', 'purpose': ''}, 'test-redistribute.yml': {'type': 'file', 'purpose': ''}, 'test.yml': {'type': 'file', 'purpose': ''}, 'topic-repos.yml': {'type': 'file', 'purpose': ''}, 'translate.yml': {'type': 'file', 'purpose': ''}, 'zizmor.yml': {'type': 'file', 'purpose': ''}}}}}, 'docs': {'purpose': 'documentation', 'children': {'de': {'type': 'dir', 'purpose': '', 'children': {'docs': {'type': 'dir', 'purpose': '', 'children': {'_llm-test.md': {'type': 'file', 'purpose': ''}, 'about': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'advanced': {'type': 'dir', 'purpose': '', 'children': {'additional-responses.md': {'type': 'file', 'purpose': ''}, 'additional-status-codes.md': {'type': 'file', 'purpose': ''}, 'advanced-dependencies.md': {'type': 'file', 'purpose': ''}, 'advanced-python-types.md': {'type': 'file', 'purpose': ''}, 'async-tests.md': {'type': 'file', 'purpose': ''}, 'behind-a-proxy.md': {'type': 'file', 'purpose': ''}, 'custom-response.md': {'type': 'file', 'purpose': ''}, 'dataclasses.md': {'type': 'file', 'purpose': ''}, 'events.md': {'type': 'file', 'purpose': ''}, 'generate-clients.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'json-base64-bytes.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'openapi-callbacks.md': {'type': 'file', 'purpose': ''}, 'openapi-webhooks.md': {'type': 'file', 'purpose': ''}, 'path-operation-advanced-configuration.md': {'type': 'file', 'purpose': ''}, 'response-change-status-code.md': {'type': 'file', 'purpose': ''}, 'response-cookies.md': {'type': 'file', 'purpose': ''}, 'response-directly.md': {'type': 'file', 'purpose': ''}, 'response-headers.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'http-basic-auth.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-scopes.md': {'type': 'file', 'purpose': ''}}}, 'settings.md': {'type': 'file', 'purpose': ''}, 'stream-data.md': {'type': 'file', 'purpose': ''}, 'strict-content-type.md': {'type': 'file', 'purpose': ''}, 'sub-applications.md': {'type': 'file', 'purpose': ''}, 'templates.md': {'type': 'file', 'purpose': ''}, 'testing-dependencies.md': {'type': 'file', 'purpose': ''}, 'testing-events.md': {'type': 'file', 'purpose': ''}, 'testing-websockets.md': {'type': 'file', 'purpose': ''}, 'using-request-directly.md': {'type': 'file', 'purpose': ''}, 'websockets.md': {'type': 'file', 'purpose': ''}, 'wsgi.md': {'type': 'file', 'purpose': ''}}}, 'alternatives.md': {'type': 'file', 'purpose': ''}, 'async.md': {'type': 'file', 'purpose': ''}, 'benchmarks.md': {'type': 'file', 'purpose': ''}, 'deployment': {'type': 'dir', 'purpose': '', 'children': {'cloud.md': {'type': 'file', 'purpose': ''}, 'concepts.md': {'type': 'file', 'purpose': ''}, 'docker.md': {'type': 'file', 'purpose': ''}, 'fastapicloud.md': {'type': 'file', 'purpose': ''}, 'https.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'manually.md': {'type': 'file', 'purpose': ''}, 'server-workers.md': {'type': 'file', 'purpose': ''}, 'versions.md': {'type': 'file', 'purpose': ''}}}, 'editor-support.md': {'type': 'file', 'purpose': ''}, 'environment-variables.md': {'type': 'file', 'purpose': ''}, 'fastapi-cli.md': {'type': 'file', 'purpose': ''}, 'features.md': {'type': 'file', 'purpose': ''}, 'help-fastapi.md': {'type': 'file', 'purpose': ''}, 'history-design-future.md': {'type': 'file', 'purpose': ''}, 'how-to': {'type': 'dir', 'purpose': '', 'children': {'authentication-error-status-code.md': {'type': 'file', 'purpose': ''}, 'conditional-openapi.md': {'type': 'file', 'purpose': ''}, 'configure-swagger-ui.md': {'type': 'file', 'purpose': ''}, 'custom-docs-ui-assets.md': {'type': 'file', 'purpose': ''}, 'custom-request-and-route.md': {'type': 'file', 'purpose': ''}, 'extending-openapi.md': {'type': 'file', 'purpose': ''}, 'general.md': {'type': 'file', 'purpose': ''}, 'graphql.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'migrate-from-pydantic-v1-to-pydantic-v2.md': {'type': 'file', 'purpose': ''}, 'separate-openapi-schemas.md': {'type': 'file', 'purpose': ''}, 'testing-database.md': {'type': 'file', 'purpose': ''}}}, 'index.md': {'type': 'file', 'purpose': ''}, 'learn': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'project-generation.md': {'type': 'file', 'purpose': ''}, 'python-types.md': {'type': 'file', 'purpose': ''}, 'resources': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'translation-banner.md': {'type': 'file', 'purpose': ''}, 'tutorial': {'type': 'dir', 'purpose': '', 'children': {'background-tasks.md': {'type': 'file', 'purpose': ''}, 'bigger-applications.md': {'type': 'file', 'purpose': ''}, 'body-fields.md': {'type': 'file', 'purpose': ''}, 'body-multiple-params.md': {'type': 'file', 'purpose': ''}, 'body-nested-models.md': {'type': 'file', 'purpose': ''}, 'body-updates.md': {'type': 'file', 'purpose': ''}, 'body.md': {'type': 'file', 'purpose': ''}, 'cookie-param-models.md': {'type': 'file', 'purpose': ''}, 'cookie-params.md': {'type': 'file', 'purpose': ''}, 'cors.md': {'type': 'file', 'purpose': ''}, 'debugging.md': {'type': 'file', 'purpose': ''}, 'dependencies': {'type': 'dir', 'purpose': '', 'children': {'classes-as-dependencies.md': {'type': 'file', 'purpose': ''}, 'dependencies-in-path-operation-decorators.md': {'type': 'file', 'purpose': ''}, 'dependencies-with-yield.md': {'type': 'file', 'purpose': ''}, 'global-dependencies.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'sub-dependencies.md': {'type': 'file', 'purpose': ''}}}, 'encoder.md': {'type': 'file', 'purpose': ''}, 'extra-data-types.md': {'type': 'file', 'purpose': ''}, 'extra-models.md': {'type': 'file', 'purpose': ''}, 'first-steps.md': {'type': 'file', 'purpose': ''}, 'handling-errors.md': {'type': 'file', 'purpose': ''}, 'header-param-models.md': {'type': 'file', 'purpose': ''}, 'header-params.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'metadata.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'path-operation-configuration.md': {'type': 'file', 'purpose': ''}, 'path-params-numeric-validations.md': {'type': 'file', 'purpose': ''}, 'path-params.md': {'type': 'file', 'purpose': ''}, 'query-param-models.md': {'type': 'file', 'purpose': ''}, 'query-params-str-validations.md': {'type': 'file', 'purpose': ''}, 'query-params.md': {'type': 'file', 'purpose': ''}, 'request-files.md': {'type': 'file', 'purpose': ''}, 'request-form-models.md': {'type': 'file', 'purpose': ''}, 'request-forms-and-files.md': {'type': 'file', 'purpose': ''}, 'request-forms.md': {'type': 'file', 'purpose': ''}, 'response-model.md': {'type': 'file', 'purpose': ''}, 'response-status-code.md': {'type': 'file', 'purpose': ''}, 'schema-extra-example.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'first-steps.md': {'type': 'file', 'purpose': ''}, 'get-current-user.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-jwt.md': {'type': 'file', 'purpose': ''}, 'simple-oauth2.md': {'type': 'file', 'purpose': ''}}}, 'server-sent-events.md': {'type': 'file', 'purpose': ''}, 'sql-databases.md': {'type': 'file', 'purpose': ''}, 'static-files.md': {'type': 'file', 'purpose': ''}, 'stream-json-lines.md': {'type': 'file', 'purpose': ''}, 'testing.md': {'type': 'file', 'purpose': ''}}}, 'virtual-environments.md': {'type': 'file', 'purpose': ''}}}, 'llm-prompt.md': {'type': 'file', 'purpose': ''}}}, 'en': {'type': 'dir', 'purpose': '', 'children': {'data': {'type': 'dir', 'purpose': '', 'children': {'contributors.yml': {'type': 'file', 'purpose': ''}, 'github_sponsors.yml': {'type': 'file', 'purpose': ''}, 'members.yml': {'type': 'file', 'purpose': ''}, 'people.yml': {'type': 'file', 'purpose': ''}, 'skip_users.yml': {'type': 'file', 'purpose': ''}, 'sponsors.yml': {'type': 'file', 'purpose': ''}, 'sponsors_badge.yml': {'type': 'file', 'purpose': ''}, 'topic_repos.yml': {'type': 'file', 'purpose': ''}, 'translation_reviewers.yml': {'type': 'file', 'purpose': ''}, 'translators.yml': {'type': 'file', 'purpose': ''}}}, 'docs': {'type': 'dir', 'purpose': '', 'children': {'_llm-test.md': {'type': 'file', 'purpose': ''}, 'about': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'advanced': {'type': 'dir', 'purpose': '', 'children': {'additional-responses.md': {'type': 'file', 'purpose': ''}, 'additional-status-codes.md': {'type': 'file', 'purpose': ''}, 'advanced-dependencies.md': {'type': 'file', 'purpose': ''}, 'advanced-python-types.md': {'type': 'file', 'purpose': ''}, 'async-tests.md': {'type': 'file', 'purpose': ''}, 'behind-a-proxy.md': {'type': 'file', 'purpose': ''}, 'custom-response.md': {'type': 'file', 'purpose': ''}, 'dataclasses.md': {'type': 'file', 'purpose': ''}, 'events.md': {'type': 'file', 'purpose': ''}, 'generate-clients.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'json-base64-bytes.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'openapi-callbacks.md': {'type': 'file', 'purpose': ''}, 'openapi-webhooks.md': {'type': 'file', 'purpose': ''}, 'path-operation-advanced-configuration.md': {'type': 'file', 'purpose': ''}, 'response-change-status-code.md': {'type': 'file', 'purpose': ''}, 'response-cookies.md': {'type': 'file', 'purpose': ''}, 'response-directly.md': {'type': 'file', 'purpose': ''}, 'response-headers.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'http-basic-auth.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-scopes.md': {'type': 'file', 'purpose': ''}}}, 'settings.md': {'type': 'file', 'purpose': ''}, 'stream-data.md': {'type': 'file', 'purpose': ''}, 'strict-content-type.md': {'type': 'file', 'purpose': ''}, 'sub-applications.md': {'type': 'file', 'purpose': ''}, 'templates.md': {'type': 'file', 'purpose': ''}, 'testing-dependencies.md': {'type': 'file', 'purpose': ''}, 'testing-events.md': {'type': 'file', 'purpose': ''}, 'testing-websockets.md': {'type': 'file', 'purpose': ''}, 'using-request-directly.md': {'type': 'file', 'purpose': ''}, 'websockets.md': {'type': 'file', 'purpose': ''}, 'wsgi.md': {'type': 'file', 'purpose': ''}}}, 'alternatives.md': {'type': 'file', 'purpose': ''}, 'async.md': {'type': 'file', 'purpose': ''}, 'benchmarks.md': {'type': 'file', 'purpose': ''}, 'contributing.md': {'type': 'file', 'purpose': ''}, 'css': {'type': 'dir', 'purpose': '', 'children': {'custom.css': {'type': 'file', 'purpose': ''}, 'termynal.css': {'type': 'file', 'purpose': ''}}}, 'deployment': {'type': 'dir', 'purpose': '', 'children': {'cloud.md': {'type': 'file', 'purpose': ''}, 'concepts.md': {'type': 'file', 'purpose': ''}, 'docker.md': {'type': 'file', 'purpose': ''}, 'fastapicloud.md': {'type': 'file', 'purpose': ''}, 'https.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'manually.md': {'type': 'file', 'purpose': ''}, 'server-workers.md': {'type': 'file', 'purpose': ''}, 'versions.md': {'type': 'file', 'purpose': ''}}}, 'editor-support.md': {'type': 'file', 'purpose': ''}, 'environment-variables.md': {'type': 'file', 'purpose': ''}, 'external-links.md': {'type': 'file', 'purpose': ''}, 'fastapi-cli.md': {'type': 'file', 'purpose': ''}, 'fastapi-people.md': {'type': 'file', 'purpose': ''}, 'features.md': {'type': 'file', 'purpose': ''}, 'help-fastapi.md': {'type': 'file', 'purpose': ''}, 'history-design-future.md': {'type': 'file', 'purpose': ''}, 'how-to': {'type': 'dir', 'purpose': '', 'children': {'authentication-error-status-code.md': {'type': 'file', 'purpose': ''}, 'conditional-openapi.md': {'type': 'file', 'purpose': ''}, 'configure-swagger-ui.md': {'type': 'file', 'purpose': ''}, 'custom-docs-ui-assets.md': {'type': 'file', 'purpose': ''}, 'custom-request-and-route.md': {'type': 'file', 'purpose': ''}, 'extending-openapi.md': {'type': 'file', 'purpose': ''}, 'general.md': {'type': 'file', 'purpose': ''}, 'graphql.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'migrate-from-pydantic-v1-to-pydantic-v2.md': {'type': 'file', 'purpose': ''}, 'separate-openapi-schemas.md': {'type': 'file', 'purpose': ''}, 'testing-database.md': {'type': 'file', 'purpose': ''}}}, 'img': {'type': 'dir', 'purpose': '', 'children': {'async': {'type': 'dir', 'purpose': '', 'children': {'concurrent-burgers': {'type': 'dir', 'purpose': '', 'children': {}}, 'parallel-burgers': {'type': 'dir', 'purpose': '', 'children': {}}}}, 'deployment': {'type': 'dir', 'purpose': '', 'children': {'concepts': {'type': 'dir', 'purpose': '', 'children': {}}, 'deta': {'type': 'dir', 'purpose': '', 'children': {}}, 'https': {'type': 'dir', 'purpose': '', 'children': {}}}}, 'index': {'type': 'dir', 'purpose': '', 'children': {}}, 'logo-margin': {'type': 'dir', 'purpose': '', 'children': {}}, 'logos': {'type': 'dir', 'purpose': '', 'children': {}}, 'python-types': {'type': 'dir', 'purpose': '', 'children': {}}, 'sponsors': {'type': 'dir', 'purpose': '', 'children': {}}, 'tutorial': {'type': 'dir', 'purpose': '', 'children': {'additional-responses': {'type': 'dir', 'purpose': '', 'children': {}}, 'async-sql-databases': {'type': 'dir', 'purpose': '', 'children': {}}, 'behind-a-proxy': {'type': 'dir', 'purpose': '', 'children': {}}, 'bigger-applications': {'type': 'dir', 'purpose': '', 'children': {}}, 'body': {'type': 'dir', 'purpose': '', 'children': {}}, 'body-fields': {'type': 'dir', 'purpose': '', 'children': {}}, 'body-nested-models': {'type': 'dir', 'purpose': '', 'children': {}}, 'cookie-param-models': {'type': 'dir', 'purpose': '', 'children': {}}, 'custom-response': {'type': 'dir', 'purpose': '', 'children': {}}, 'dataclasses': {'type': 'dir', 'purpose': '', 'children': {}}, 'debugging': {'type': 'dir', 'purpose': '', 'children': {}}, 'dependencies': {'type': 'dir', 'purpose': '', 'children': {}}, 'extending-openapi': {'type': 'dir', 'purpose': '', 'children': {}}, 'generate-clients': {'type': 'dir', 'purpose': '', 'children': {}}, 'graphql': {'type': 'dir', 'purpose': '', 'children': {}}, 'header-param-models': {'type': 'dir', 'purpose': '', 'children': {}}, 'json-base64-bytes': {'type': 'dir', 'purpose': '', 'children': {}}, 'metadata': {'type': 'dir', 'purpose': '', 'children': {}}, 'openapi-callbacks': {'type': 'dir', 'purpose': '', 'children': {}}, 'openapi-webhooks': {'type': 'dir', 'purpose': '', 'children': {}}, 'path-operation-advanced-configuration': {'type': 'dir', 'purpose': '', 'children': {}}, 'path-operation-configuration': {'type': 'dir', 'purpose': '', 'children': {}}, 'path-params': {'type': 'dir', 'purpose': '', 'children': {}}, 'query-param-models': {'type': 'dir', 'purpose': '', 'children': {}}, 'query-params-str-validations': {'type': 'dir', 'purpose': '', 'children': {}}, 'request-form-models': {'type': 'dir', 'purpose': '', 'children': {}}, 'response-model': {'type': 'dir', 'purpose': '', 'children': {}}, 'response-status-code': {'type': 'dir', 'purpose': '', 'children': {}}, 'security': {'type': 'dir', 'purpose': '', 'children': {}}, 'separate-openapi-schemas': {'type': 'dir', 'purpose': '', 'children': {}}, 'sql-databases': {'type': 'dir', 'purpose': '', 'children': {}}, 'sub-applications': {'type': 'dir', 'purpose': '', 'children': {}}, 'websockets': {'type': 'dir', 'purpose': '', 'children': {}}}}}}, 'index.md': {'type': 'file', 'purpose': ''}, 'js': {'type': 'dir', 'purpose': '', 'children': {'custom.js': {'type': 'file', 'purpose': ''}, 'init_kapa_widget.js': {'type': 'file', 'purpose': ''}, 'termynal.js': {'type': 'file', 'purpose': ''}}}, 'learn': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'management.md': {'type': 'file', 'purpose': ''}, 'newsletter.md': {'type': 'file', 'purpose': ''}, 'project-generation.md': {'type': 'file', 'purpose': ''}, 'python-types.md': {'type': 'file', 'purpose': ''}, 'reference': {'type': 'dir', 'purpose': '', 'children': {'apirouter.md': {'type': 'file', 'purpose': ''}, 'background.md': {'type': 'file', 'purpose': ''}, 'dependencies.md': {'type': 'file', 'purpose': ''}, 'encoders.md': {'type': 'file', 'purpose': ''}, 'exceptions.md': {'type': 'file', 'purpose': ''}, 'fastapi.md': {'type': 'file', 'purpose': ''}, 'httpconnection.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'openapi': {'type': 'dir', 'purpose': '', 'children': {'docs.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'models.md': {'type': 'file', 'purpose': ''}}}, 'parameters.md': {'type': 'file', 'purpose': ''}, 'request.md': {'type': 'file', 'purpose': ''}, 'response.md': {'type': 'file', 'purpose': ''}, 'responses.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'staticfiles.md': {'type': 'file', 'purpose': ''}, 'status.md': {'type': 'file', 'purpose': ''}, 'templating.md': {'type': 'file', 'purpose': ''}, 'testclient.md': {'type': 'file', 'purpose': ''}, 'uploadfile.md': {'type': 'file', 'purpose': ''}, 'websockets.md': {'type': 'file', 'purpose': ''}}}, 'release-notes.md': {'type': 'file', 'purpose': ''}, 'resources': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'translation-banner.md': {'type': 'file', 'purpose': ''}, 'translations.md': {'type': 'file', 'purpose': ''}, 'tutorial': {'type': 'dir', 'purpose': '', 'children': {'background-tasks.md': {'type': 'file', 'purpose': ''}, 'bigger-applications.md': {'type': 'file', 'purpose': ''}, 'body-fields.md': {'type': 'file', 'purpose': ''}, 'body-multiple-params.md': {'type': 'file', 'purpose': ''}, 'body-nested-models.md': {'type': 'file', 'purpose': ''}, 'body-updates.md': {'type': 'file', 'purpose': ''}, 'body.md': {'type': 'file', 'purpose': ''}, 'cookie-param-models.md': {'type': 'file', 'purpose': ''}, 'cookie-params.md': {'type': 'file', 'purpose': ''}, 'cors.md': {'type': 'file', 'purpose': ''}, 'debugging.md': {'type': 'file', 'purpose': ''}, 'dependencies': {'type': 'dir', 'purpose': '', 'children': {'classes-as-dependencies.md': {'type': 'file', 'purpose': ''}, 'dependencies-in-path-operation-decorators.md': {'type': 'file', 'purpose': ''}, 'dependencies-with-yield.md': {'type': 'file', 'purpose': ''}, 'global-dependencies.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'sub-dependencies.md': {'type': 'file', 'purpose': ''}}}, 'encoder.md': {'type': 'file', 'purpose': ''}, 'extra-data-types.md': {'type': 'file', 'purpose': ''}, 'extra-models.md': {'type': 'file', 'purpose': ''}, 'first-steps.md': {'type': 'file', 'purpose': ''}, 'frontend.md': {'type': 'file', 'purpose': ''}, 'handling-errors.md': {'type': 'file', 'purpose': ''}, 'header-param-models.md': {'type': 'file', 'purpose': ''}, 'header-params.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'metadata.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'path-operation-configuration.md': {'type': 'file', 'purpose': ''}, 'path-params-numeric-validations.md': {'type': 'file', 'purpose': ''}, 'path-params.md': {'type': 'file', 'purpose': ''}, 'query-param-models.md': {'type': 'file', 'purpose': ''}, 'query-params-str-validations.md': {'type': 'file', 'purpose': ''}, 'query-params.md': {'type': 'file', 'purpose': ''}, 'request-files.md': {'type': 'file', 'purpose': ''}, 'request-form-models.md': {'type': 'file', 'purpose': ''}, 'request-forms-and-files.md': {'type': 'file', 'purpose': ''}, 'request-forms.md': {'type': 'file', 'purpose': ''}, 'response-model.md': {'type': 'file', 'purpose': ''}, 'response-status-code.md': {'type': 'file', 'purpose': ''}, 'schema-extra-example.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'first-steps.md': {'type': 'file', 'purpose': ''}, 'get-current-user.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-jwt.md': {'type': 'file', 'purpose': ''}, 'simple-oauth2.md': {'type': 'file', 'purpose': ''}}}, 'server-sent-events.md': {'type': 'file', 'purpose': ''}, 'sql-databases.md': {'type': 'file', 'purpose': ''}, 'static-files.md': {'type': 'file', 'purpose': ''}, 'stream-json-lines.md': {'type': 'file', 'purpose': ''}, 'testing.md': {'type': 'file', 'purpose': ''}}}, 'virtual-environments.md': {'type': 'file', 'purpose': ''}}}, 'mkdocs.yml': {'type': 'file', 'purpose': ''}, 'overrides': {'type': 'dir', 'purpose': '', 'children': {'main.html': {'type': 'file', 'purpose': ''}, 'partials': {'type': 'dir', 'purpose': '', 'children': {'banner-sponsors.html': {'type': 'file', 'purpose': ''}, 'copyright.html': {'type': 'file', 'purpose': ''}}}}}}}, 'es': {'type': 'dir', 'purpose': '', 'children': {'docs': {'type': 'dir', 'purpose': '', 'children': {'_llm-test.md': {'type': 'file', 'purpose': ''}, 'about': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'advanced': {'type': 'dir', 'purpose': '', 'children': {'additional-responses.md': {'type': 'file', 'purpose': ''}, 'additional-status-codes.md': {'type': 'file', 'purpose': ''}, 'advanced-dependencies.md': {'type': 'file', 'purpose': ''}, 'advanced-python-types.md': {'type': 'file', 'purpose': ''}, 'async-tests.md': {'type': 'file', 'purpose': ''}, 'behind-a-proxy.md': {'type': 'file', 'purpose': ''}, 'custom-response.md': {'type': 'file', 'purpose': ''}, 'dataclasses.md': {'type': 'file', 'purpose': ''}, 'events.md': {'type': 'file', 'purpose': ''}, 'generate-clients.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'json-base64-bytes.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'openapi-callbacks.md': {'type': 'file', 'purpose': ''}, 'openapi-webhooks.md': {'type': 'file', 'purpose': ''}, 'path-operation-advanced-configuration.md': {'type': 'file', 'purpose': ''}, 'response-change-status-code.md': {'type': 'file', 'purpose': ''}, 'response-cookies.md': {'type': 'file', 'purpose': ''}, 'response-directly.md': {'type': 'file', 'purpose': ''}, 'response-headers.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'http-basic-auth.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-scopes.md': {'type': 'file', 'purpose': ''}}}, 'settings.md': {'type': 'file', 'purpose': ''}, 'stream-data.md': {'type': 'file', 'purpose': ''}, 'strict-content-type.md': {'type': 'file', 'purpose': ''}, 'sub-applications.md': {'type': 'file', 'purpose': ''}, 'templates.md': {'type': 'file', 'purpose': ''}, 'testing-dependencies.md': {'type': 'file', 'purpose': ''}, 'testing-events.md': {'type': 'file', 'purpose': ''}, 'testing-websockets.md': {'type': 'file', 'purpose': ''}, 'using-request-directly.md': {'type': 'file', 'purpose': ''}, 'websockets.md': {'type': 'file', 'purpose': ''}, 'wsgi.md': {'type': 'file', 'purpose': ''}}}, 'alternatives.md': {'type': 'file', 'purpose': ''}, 'async.md': {'type': 'file', 'purpose': ''}, 'benchmarks.md': {'type': 'file', 'purpose': ''}, 'deployment': {'type': 'dir', 'purpose': '', 'children': {'cloud.md': {'type': 'file', 'purpose': ''}, 'concepts.md': {'type': 'file', 'purpose': ''}, 'docker.md': {'type': 'file', 'purpose': ''}, 'fastapicloud.md': {'type': 'file', 'purpose': ''}, 'https.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'manually.md': {'type': 'file', 'purpose': ''}, 'server-workers.md': {'type': 'file', 'purpose': ''}, 'versions.md': {'type': 'file', 'purpose': ''}}}, 'editor-support.md': {'type': 'file', 'purpose': ''}, 'environment-variables.md': {'type': 'file', 'purpose': ''}, 'fastapi-cli.md': {'type': 'file', 'purpose': ''}, 'features.md': {'type': 'file', 'purpose': ''}, 'help-fastapi.md': {'type': 'file', 'purpose': ''}, 'history-design-future.md': {'type': 'file', 'purpose': ''}, 'how-to': {'type': 'dir', 'purpose': '', 'children': {'authentication-error-status-code.md': {'type': 'file', 'purpose': ''}, 'conditional-openapi.md': {'type': 'file', 'purpose': ''}, 'configure-swagger-ui.md': {'type': 'file', 'purpose': ''}, 'custom-docs-ui-assets.md': {'type': 'file', 'purpose': ''}, 'custom-request-and-route.md': {'type': 'file', 'purpose': ''}, 'extending-openapi.md': {'type': 'file', 'purpose': ''}, 'general.md': {'type': 'file', 'purpose': ''}, 'graphql.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'migrate-from-pydantic-v1-to-pydantic-v2.md': {'type': 'file', 'purpose': ''}, 'separate-openapi-schemas.md': {'type': 'file', 'purpose': ''}, 'testing-database.md': {'type': 'file', 'purpose': ''}}}, 'index.md': {'type': 'file', 'purpose': ''}, 'learn': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'project-generation.md': {'type': 'file', 'purpose': ''}, 'python-types.md': {'type': 'file', 'purpose': ''}, 'resources': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'translation-banner.md': {'type': 'file', 'purpose': ''}, 'tutorial': {'type': 'dir', 'purpose': '', 'children': {'background-tasks.md': {'type': 'file', 'purpose': ''}, 'bigger-applications.md': {'type': 'file', 'purpose': ''}, 'body-fields.md': {'type': 'file', 'purpose': ''}, 'body-multiple-params.md': {'type': 'file', 'purpose': ''}, 'body-nested-models.md': {'type': 'file', 'purpose': ''}, 'body-updates.md': {'type': 'file', 'purpose': ''}, 'body.md': {'type': 'file', 'purpose': ''}, 'cookie-param-models.md': {'type': 'file', 'purpose': ''}, 'cookie-params.md': {'type': 'file', 'purpose': ''}, 'cors.md': {'type': 'file', 'purpose': ''}, 'debugging.md': {'type': 'file', 'purpose': ''}, 'dependencies': {'type': 'dir', 'purpose': '', 'children': {'classes-as-dependencies.md': {'type': 'file', 'purpose': ''}, 'dependencies-in-path-operation-decorators.md': {'type': 'file', 'purpose': ''}, 'dependencies-with-yield.md': {'type': 'file', 'purpose': ''}, 'global-dependencies.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'sub-dependencies.md': {'type': 'file', 'purpose': ''}}}, 'encoder.md': {'type': 'file', 'purpose': ''}, 'extra-data-types.md': {'type': 'file', 'purpose': ''}, 'extra-models.md': {'type': 'file', 'purpose': ''}, 'first-steps.md': {'type': 'file', 'purpose': ''}, 'handling-errors.md': {'type': 'file', 'purpose': ''}, 'header-param-models.md': {'type': 'file', 'purpose': ''}, 'header-params.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'metadata.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'path-operation-configuration.md': {'type': 'file', 'purpose': ''}, 'path-params-numeric-validations.md': {'type': 'file', 'purpose': ''}, 'path-params.md': {'type': 'file', 'purpose': ''}, 'query-param-models.md': {'type': 'file', 'purpose': ''}, 'query-params-str-validations.md': {'type': 'file', 'purpose': ''}, 'query-params.md': {'type': 'file', 'purpose': ''}, 'request-files.md': {'type': 'file', 'purpose': ''}, 'request-form-models.md': {'type': 'file', 'purpose': ''}, 'request-forms-and-files.md': {'type': 'file', 'purpose': ''}, 'request-forms.md': {'type': 'file', 'purpose': ''}, 'response-model.md': {'type': 'file', 'purpose': ''}, 'response-status-code.md': {'type': 'file', 'purpose': ''}, 'schema-extra-example.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'first-steps.md': {'type': 'file', 'purpose': ''}, 'get-current-user.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-jwt.md': {'type': 'file', 'purpose': ''}, 'simple-oauth2.md': {'type': 'file', 'purpose': ''}}}, 'server-sent-events.md': {'type': 'file', 'purpose': ''}, 'sql-databases.md': {'type': 'file', 'purpose': ''}, 'static-files.md': {'type': 'file', 'purpose': ''}, 'stream-json-lines.md': {'type': 'file', 'purpose': ''}, 'testing.md': {'type': 'file', 'purpose': ''}}}, 'virtual-environments.md': {'type': 'file', 'purpose': ''}}}, 'llm-prompt.md': {'type': 'file', 'purpose': ''}}}, 'fr': {'type': 'dir', 'purpose': '', 'children': {'docs': {'type': 'dir', 'purpose': '', 'children': {'_llm-test.md': {'type': 'file', 'purpose': ''}, 'about': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'advanced': {'type': 'dir', 'purpose': '', 'children': {'additional-responses.md': {'type': 'file', 'purpose': ''}, 'additional-status-codes.md': {'type': 'file', 'purpose': ''}, 'advanced-dependencies.md': {'type': 'file', 'purpose': ''}, 'advanced-python-types.md': {'type': 'file', 'purpose': ''}, 'async-tests.md': {'type': 'file', 'purpose': ''}, 'behind-a-proxy.md': {'type': 'file', 'purpose': ''}, 'custom-response.md': {'type': 'file', 'purpose': ''}, 'dataclasses.md': {'type': 'file', 'purpose': ''}, 'events.md': {'type': 'file', 'purpose': ''}, 'generate-clients.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'json-base64-bytes.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'openapi-callbacks.md': {'type': 'file', 'purpose': ''}, 'openapi-webhooks.md': {'type': 'file', 'purpose': ''}, 'path-operation-advanced-configuration.md': {'type': 'file', 'purpose': ''}, 'response-change-status-code.md': {'type': 'file', 'purpose': ''}, 'response-cookies.md': {'type': 'file', 'purpose': ''}, 'response-directly.md': {'type': 'file', 'purpose': ''}, 'response-headers.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'http-basic-auth.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-scopes.md': {'type': 'file', 'purpose': ''}}}, 'settings.md': {'type': 'file', 'purpose': ''}, 'stream-data.md': {'type': 'file', 'purpose': ''}, 'strict-content-type.md': {'type': 'file', 'purpose': ''}, 'sub-applications.md': {'type': 'file', 'purpose': ''}, 'templates.md': {'type': 'file', 'purpose': ''}, 'testing-dependencies.md': {'type': 'file', 'purpose': ''}, 'testing-events.md': {'type': 'file', 'purpose': ''}, 'testing-websockets.md': {'type': 'file', 'purpose': ''}, 'using-request-directly.md': {'type': 'file', 'purpose': ''}, 'websockets.md': {'type': 'file', 'purpose': ''}, 'wsgi.md': {'type': 'file', 'purpose': ''}}}, 'alternatives.md': {'type': 'file', 'purpose': ''}, 'async.md': {'type': 'file', 'purpose': ''}, 'benchmarks.md': {'type': 'file', 'purpose': ''}, 'deployment': {'type': 'dir', 'purpose': '', 'children': {'cloud.md': {'type': 'file', 'purpose': ''}, 'concepts.md': {'type': 'file', 'purpose': ''}, 'docker.md': {'type': 'file', 'purpose': ''}, 'fastapicloud.md': {'type': 'file', 'purpose': ''}, 'https.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'manually.md': {'type': 'file', 'purpose': ''}, 'server-workers.md': {'type': 'file', 'purpose': ''}, 'versions.md': {'type': 'file', 'purpose': ''}}}, 'editor-support.md': {'type': 'file', 'purpose': ''}, 'environment-variables.md': {'type': 'file', 'purpose': ''}, 'fastapi-cli.md': {'type': 'file', 'purpose': ''}, 'features.md': {'type': 'file', 'purpose': ''}, 'help-fastapi.md': {'type': 'file', 'purpose': ''}, 'history-design-future.md': {'type': 'file', 'purpose': ''}, 'how-to': {'type': 'dir', 'purpose': '', 'children': {'authentication-error-status-code.md': {'type': 'file', 'purpose': ''}, 'conditional-openapi.md': {'type': 'file', 'purpose': ''}, 'configure-swagger-ui.md': {'type': 'file', 'purpose': ''}, 'custom-docs-ui-assets.md': {'type': 'file', 'purpose': ''}, 'custom-request-and-route.md': {'type': 'file', 'purpose': ''}, 'extending-openapi.md': {'type': 'file', 'purpose': ''}, 'general.md': {'type': 'file', 'purpose': ''}, 'graphql.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'migrate-from-pydantic-v1-to-pydantic-v2.md': {'type': 'file', 'purpose': ''}, 'separate-openapi-schemas.md': {'type': 'file', 'purpose': ''}, 'testing-database.md': {'type': 'file', 'purpose': ''}}}, 'index.md': {'type': 'file', 'purpose': ''}, 'learn': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'project-generation.md': {'type': 'file', 'purpose': ''}, 'python-types.md': {'type': 'file', 'purpose': ''}, 'resources': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'translation-banner.md': {'type': 'file', 'purpose': ''}, 'tutorial': {'type': 'dir', 'purpose': '', 'children': {'background-tasks.md': {'type': 'file', 'purpose': ''}, 'bigger-applications.md': {'type': 'file', 'purpose': ''}, 'body-fields.md': {'type': 'file', 'purpose': ''}, 'body-multiple-params.md': {'type': 'file', 'purpose': ''}, 'body-nested-models.md': {'type': 'file', 'purpose': ''}, 'body-updates.md': {'type': 'file', 'purpose': ''}, 'body.md': {'type': 'file', 'purpose': ''}, 'cookie-param-models.md': {'type': 'file', 'purpose': ''}, 'cookie-params.md': {'type': 'file', 'purpose': ''}, 'cors.md': {'type': 'file', 'purpose': ''}, 'debugging.md': {'type': 'file', 'purpose': ''}, 'dependencies': {'type': 'dir', 'purpose': '', 'children': {'classes-as-dependencies.md': {'type': 'file', 'purpose': ''}, 'dependencies-in-path-operation-decorators.md': {'type': 'file', 'purpose': ''}, 'dependencies-with-yield.md': {'type': 'file', 'purpose': ''}, 'global-dependencies.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'sub-dependencies.md': {'type': 'file', 'purpose': ''}}}, 'encoder.md': {'type': 'file', 'purpose': ''}, 'extra-data-types.md': {'type': 'file', 'purpose': ''}, 'extra-models.md': {'type': 'file', 'purpose': ''}, 'first-steps.md': {'type': 'file', 'purpose': ''}, 'handling-errors.md': {'type': 'file', 'purpose': ''}, 'header-param-models.md': {'type': 'file', 'purpose': ''}, 'header-params.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'metadata.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'path-operation-configuration.md': {'type': 'file', 'purpose': ''}, 'path-params-numeric-validations.md': {'type': 'file', 'purpose': ''}, 'path-params.md': {'type': 'file', 'purpose': ''}, 'query-param-models.md': {'type': 'file', 'purpose': ''}, 'query-params-str-validations.md': {'type': 'file', 'purpose': ''}, 'query-params.md': {'type': 'file', 'purpose': ''}, 'request-files.md': {'type': 'file', 'purpose': ''}, 'request-form-models.md': {'type': 'file', 'purpose': ''}, 'request-forms-and-files.md': {'type': 'file', 'purpose': ''}, 'request-forms.md': {'type': 'file', 'purpose': ''}, 'response-model.md': {'type': 'file', 'purpose': ''}, 'response-status-code.md': {'type': 'file', 'purpose': ''}, 'schema-extra-example.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'first-steps.md': {'type': 'file', 'purpose': ''}, 'get-current-user.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-jwt.md': {'type': 'file', 'purpose': ''}, 'simple-oauth2.md': {'type': 'file', 'purpose': ''}}}, 'server-sent-events.md': {'type': 'file', 'purpose': ''}, 'sql-databases.md': {'type': 'file', 'purpose': ''}, 'static-files.md': {'type': 'file', 'purpose': ''}, 'stream-json-lines.md': {'type': 'file', 'purpose': ''}, 'testing.md': {'type': 'file', 'purpose': ''}}}, 'virtual-environments.md': {'type': 'file', 'purpose': ''}}}, 'llm-prompt.md': {'type': 'file', 'purpose': ''}}}, 'hi': {'type': 'dir', 'purpose': '', 'children': {'docs': {'type': 'dir', 'purpose': '', 'children': {'_llm-test.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'translation-banner.md': {'type': 'file', 'purpose': ''}}}, 'llm-prompt.md': {'type': 'file', 'purpose': ''}, 'mkdocs.yml': {'type': 'file', 'purpose': ''}}}, 'ja': {'type': 'dir', 'purpose': '', 'children': {'docs': {'type': 'dir', 'purpose': '', 'children': {'_llm-test.md': {'type': 'file', 'purpose': ''}, 'about': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'advanced': {'type': 'dir', 'purpose': '', 'children': {'additional-responses.md': {'type': 'file', 'purpose': ''}, 'additional-status-codes.md': {'type': 'file', 'purpose': ''}, 'advanced-dependencies.md': {'type': 'file', 'purpose': ''}, 'advanced-python-types.md': {'type': 'file', 'purpose': ''}, 'async-tests.md': {'type': 'file', 'purpose': ''}, 'behind-a-proxy.md': {'type': 'file', 'purpose': ''}, 'custom-response.md': {'type': 'file', 'purpose': ''}, 'dataclasses.md': {'type': 'file', 'purpose': ''}, 'events.md': {'type': 'file', 'purpose': ''}, 'generate-clients.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'json-base64-bytes.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'openapi-callbacks.md': {'type': 'file', 'purpose': ''}, 'openapi-webhooks.md': {'type': 'file', 'purpose': ''}, 'path-operation-advanced-configuration.md': {'type': 'file', 'purpose': ''}, 'response-change-status-code.md': {'type': 'file', 'purpose': ''}, 'response-cookies.md': {'type': 'file', 'purpose': ''}, 'response-directly.md': {'type': 'file', 'purpose': ''}, 'response-headers.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'http-basic-auth.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-scopes.md': {'type': 'file', 'purpose': ''}}}, 'settings.md': {'type': 'file', 'purpose': ''}, 'stream-data.md': {'type': 'file', 'purpose': ''}, 'strict-content-type.md': {'type': 'file', 'purpose': ''}, 'sub-applications.md': {'type': 'file', 'purpose': ''}, 'templates.md': {'type': 'file', 'purpose': ''}, 'testing-dependencies.md': {'type': 'file', 'purpose': ''}, 'testing-events.md': {'type': 'file', 'purpose': ''}, 'testing-websockets.md': {'type': 'file', 'purpose': ''}, 'using-request-directly.md': {'type': 'file', 'purpose': ''}, 'websockets.md': {'type': 'file', 'purpose': ''}, 'wsgi.md': {'type': 'file', 'purpose': ''}}}, 'alternatives.md': {'type': 'file', 'purpose': ''}, 'async.md': {'type': 'file', 'purpose': ''}, 'benchmarks.md': {'type': 'file', 'purpose': ''}, 'deployment': {'type': 'dir', 'purpose': '', 'children': {'cloud.md': {'type': 'file', 'purpose': ''}, 'concepts.md': {'type': 'file', 'purpose': ''}, 'docker.md': {'type': 'file', 'purpose': ''}, 'fastapicloud.md': {'type': 'file', 'purpose': ''}, 'https.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'manually.md': {'type': 'file', 'purpose': ''}, 'server-workers.md': {'type': 'file', 'purpose': ''}, 'versions.md': {'type': 'file', 'purpose': ''}}}, 'editor-support.md': {'type': 'file', 'purpose': ''}, 'environment-variables.md': {'type': 'file', 'purpose': ''}, 'fastapi-cli.md': {'type': 'file', 'purpose': ''}, 'features.md': {'type': 'file', 'purpose': ''}, 'help-fastapi.md': {'type': 'file', 'purpose': ''}, 'history-design-future.md': {'type': 'file', 'purpose': ''}, 'how-to': {'type': 'dir', 'purpose': '', 'children': {'authentication-error-status-code.md': {'type': 'file', 'purpose': ''}, 'conditional-openapi.md': {'type': 'file', 'purpose': ''}, 'configure-swagger-ui.md': {'type': 'file', 'purpose': ''}, 'custom-docs-ui-assets.md': {'type': 'file', 'purpose': ''}, 'custom-request-and-route.md': {'type': 'file', 'purpose': ''}, 'extending-openapi.md': {'type': 'file', 'purpose': ''}, 'general.md': {'type': 'file', 'purpose': ''}, 'graphql.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'migrate-from-pydantic-v1-to-pydantic-v2.md': {'type': 'file', 'purpose': ''}, 'separate-openapi-schemas.md': {'type': 'file', 'purpose': ''}, 'testing-database.md': {'type': 'file', 'purpose': ''}}}, 'index.md': {'type': 'file', 'purpose': ''}, 'learn': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'project-generation.md': {'type': 'file', 'purpose': ''}, 'python-types.md': {'type': 'file', 'purpose': ''}, 'resources': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'translation-banner.md': {'type': 'file', 'purpose': ''}, 'tutorial': {'type': 'dir', 'purpose': '', 'children': {'background-tasks.md': {'type': 'file', 'purpose': ''}, 'bigger-applications.md': {'type': 'file', 'purpose': ''}, 'body-fields.md': {'type': 'file', 'purpose': ''}, 'body-multiple-params.md': {'type': 'file', 'purpose': ''}, 'body-nested-models.md': {'type': 'file', 'purpose': ''}, 'body-updates.md': {'type': 'file', 'purpose': ''}, 'body.md': {'type': 'file', 'purpose': ''}, 'cookie-param-models.md': {'type': 'file', 'purpose': ''}, 'cookie-params.md': {'type': 'file', 'purpose': ''}, 'cors.md': {'type': 'file', 'purpose': ''}, 'debugging.md': {'type': 'file', 'purpose': ''}, 'dependencies': {'type': 'dir', 'purpose': '', 'children': {'classes-as-dependencies.md': {'type': 'file', 'purpose': ''}, 'dependencies-in-path-operation-decorators.md': {'type': 'file', 'purpose': ''}, 'dependencies-with-yield.md': {'type': 'file', 'purpose': ''}, 'global-dependencies.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'sub-dependencies.md': {'type': 'file', 'purpose': ''}}}, 'encoder.md': {'type': 'file', 'purpose': ''}, 'extra-data-types.md': {'type': 'file', 'purpose': ''}, 'extra-models.md': {'type': 'file', 'purpose': ''}, 'first-steps.md': {'type': 'file', 'purpose': ''}, 'handling-errors.md': {'type': 'file', 'purpose': ''}, 'header-param-models.md': {'type': 'file', 'purpose': ''}, 'header-params.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'metadata.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'path-operation-configuration.md': {'type': 'file', 'purpose': ''}, 'path-params-numeric-validations.md': {'type': 'file', 'purpose': ''}, 'path-params.md': {'type': 'file', 'purpose': ''}, 'query-param-models.md': {'type': 'file', 'purpose': ''}, 'query-params-str-validations.md': {'type': 'file', 'purpose': ''}, 'query-params.md': {'type': 'file', 'purpose': ''}, 'request-files.md': {'type': 'file', 'purpose': ''}, 'request-form-models.md': {'type': 'file', 'purpose': ''}, 'request-forms-and-files.md': {'type': 'file', 'purpose': ''}, 'request-forms.md': {'type': 'file', 'purpose': ''}, 'response-model.md': {'type': 'file', 'purpose': ''}, 'response-status-code.md': {'type': 'file', 'purpose': ''}, 'schema-extra-example.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'first-steps.md': {'type': 'file', 'purpose': ''}, 'get-current-user.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-jwt.md': {'type': 'file', 'purpose': ''}, 'simple-oauth2.md': {'type': 'file', 'purpose': ''}}}, 'server-sent-events.md': {'type': 'file', 'purpose': ''}, 'sql-databases.md': {'type': 'file', 'purpose': ''}, 'static-files.md': {'type': 'file', 'purpose': ''}, 'stream-json-lines.md': {'type': 'file', 'purpose': ''}, 'testing.md': {'type': 'file', 'purpose': ''}}}, 'virtual-environments.md': {'type': 'file', 'purpose': ''}}}, 'llm-prompt.md': {'type': 'file', 'purpose': ''}}}, 'ko': {'type': 'dir', 'purpose': '', 'children': {'docs': {'type': 'dir', 'purpose': '', 'children': {'_llm-test.md': {'type': 'file', 'purpose': ''}, 'about': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'advanced': {'type': 'dir', 'purpose': '', 'children': {'additional-responses.md': {'type': 'file', 'purpose': ''}, 'additional-status-codes.md': {'type': 'file', 'purpose': ''}, 'advanced-dependencies.md': {'type': 'file', 'purpose': ''}, 'advanced-python-types.md': {'type': 'file', 'purpose': ''}, 'async-tests.md': {'type': 'file', 'purpose': ''}, 'behind-a-proxy.md': {'type': 'file', 'purpose': ''}, 'custom-response.md': {'type': 'file', 'purpose': ''}, 'dataclasses.md': {'type': 'file', 'purpose': ''}, 'events.md': {'type': 'file', 'purpose': ''}, 'generate-clients.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'json-base64-bytes.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'openapi-callbacks.md': {'type': 'file', 'purpose': ''}, 'openapi-webhooks.md': {'type': 'file', 'purpose': ''}, 'path-operation-advanced-configuration.md': {'type': 'file', 'purpose': ''}, 'response-change-status-code.md': {'type': 'file', 'purpose': ''}, 'response-cookies.md': {'type': 'file', 'purpose': ''}, 'response-directly.md': {'type': 'file', 'purpose': ''}, 'response-headers.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'http-basic-auth.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-scopes.md': {'type': 'file', 'purpose': ''}}}, 'settings.md': {'type': 'file', 'purpose': ''}, 'stream-data.md': {'type': 'file', 'purpose': ''}, 'strict-content-type.md': {'type': 'file', 'purpose': ''}, 'sub-applications.md': {'type': 'file', 'purpose': ''}, 'templates.md': {'type': 'file', 'purpose': ''}, 'testing-dependencies.md': {'type': 'file', 'purpose': ''}, 'testing-events.md': {'type': 'file', 'purpose': ''}, 'testing-websockets.md': {'type': 'file', 'purpose': ''}, 'using-request-directly.md': {'type': 'file', 'purpose': ''}, 'websockets.md': {'type': 'file', 'purpose': ''}, 'wsgi.md': {'type': 'file', 'purpose': ''}}}, 'alternatives.md': {'type': 'file', 'purpose': ''}, 'async.md': {'type': 'file', 'purpose': ''}, 'benchmarks.md': {'type': 'file', 'purpose': ''}, 'deployment': {'type': 'dir', 'purpose': '', 'children': {'cloud.md': {'type': 'file', 'purpose': ''}, 'concepts.md': {'type': 'file', 'purpose': ''}, 'docker.md': {'type': 'file', 'purpose': ''}, 'fastapicloud.md': {'type': 'file', 'purpose': ''}, 'https.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'manually.md': {'type': 'file', 'purpose': ''}, 'server-workers.md': {'type': 'file', 'purpose': ''}, 'versions.md': {'type': 'file', 'purpose': ''}}}, 'editor-support.md': {'type': 'file', 'purpose': ''}, 'environment-variables.md': {'type': 'file', 'purpose': ''}, 'fastapi-cli.md': {'type': 'file', 'purpose': ''}, 'features.md': {'type': 'file', 'purpose': ''}, 'help-fastapi.md': {'type': 'file', 'purpose': ''}, 'history-design-future.md': {'type': 'file', 'purpose': ''}, 'how-to': {'type': 'dir', 'purpose': '', 'children': {'authentication-error-status-code.md': {'type': 'file', 'purpose': ''}, 'conditional-openapi.md': {'type': 'file', 'purpose': ''}, 'configure-swagger-ui.md': {'type': 'file', 'purpose': ''}, 'custom-docs-ui-assets.md': {'type': 'file', 'purpose': ''}, 'custom-request-and-route.md': {'type': 'file', 'purpose': ''}, 'extending-openapi.md': {'type': 'file', 'purpose': ''}, 'general.md': {'type': 'file', 'purpose': ''}, 'graphql.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'migrate-from-pydantic-v1-to-pydantic-v2.md': {'type': 'file', 'purpose': ''}, 'separate-openapi-schemas.md': {'type': 'file', 'purpose': ''}, 'testing-database.md': {'type': 'file', 'purpose': ''}}}, 'index.md': {'type': 'file', 'purpose': ''}, 'learn': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'project-generation.md': {'type': 'file', 'purpose': ''}, 'python-types.md': {'type': 'file', 'purpose': ''}, 'resources': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'translation-banner.md': {'type': 'file', 'purpose': ''}, 'tutorial': {'type': 'dir', 'purpose': '', 'children': {'background-tasks.md': {'type': 'file', 'purpose': ''}, 'bigger-applications.md': {'type': 'file', 'purpose': ''}, 'body-fields.md': {'type': 'file', 'purpose': ''}, 'body-multiple-params.md': {'type': 'file', 'purpose': ''}, 'body-nested-models.md': {'type': 'file', 'purpose': ''}, 'body-updates.md': {'type': 'file', 'purpose': ''}, 'body.md': {'type': 'file', 'purpose': ''}, 'cookie-param-models.md': {'type': 'file', 'purpose': ''}, 'cookie-params.md': {'type': 'file', 'purpose': ''}, 'cors.md': {'type': 'file', 'purpose': ''}, 'debugging.md': {'type': 'file', 'purpose': ''}, 'dependencies': {'type': 'dir', 'purpose': '', 'children': {'classes-as-dependencies.md': {'type': 'file', 'purpose': ''}, 'dependencies-in-path-operation-decorators.md': {'type': 'file', 'purpose': ''}, 'dependencies-with-yield.md': {'type': 'file', 'purpose': ''}, 'global-dependencies.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'sub-dependencies.md': {'type': 'file', 'purpose': ''}}}, 'encoder.md': {'type': 'file', 'purpose': ''}, 'extra-data-types.md': {'type': 'file', 'purpose': ''}, 'extra-models.md': {'type': 'file', 'purpose': ''}, 'first-steps.md': {'type': 'file', 'purpose': ''}, 'handling-errors.md': {'type': 'file', 'purpose': ''}, 'header-param-models.md': {'type': 'file', 'purpose': ''}, 'header-params.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'metadata.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'path-operation-configuration.md': {'type': 'file', 'purpose': ''}, 'path-params-numeric-validations.md': {'type': 'file', 'purpose': ''}, 'path-params.md': {'type': 'file', 'purpose': ''}, 'query-param-models.md': {'type': 'file', 'purpose': ''}, 'query-params-str-validations.md': {'type': 'file', 'purpose': ''}, 'query-params.md': {'type': 'file', 'purpose': ''}, 'request-files.md': {'type': 'file', 'purpose': ''}, 'request-form-models.md': {'type': 'file', 'purpose': ''}, 'request-forms-and-files.md': {'type': 'file', 'purpose': ''}, 'request-forms.md': {'type': 'file', 'purpose': ''}, 'response-model.md': {'type': 'file', 'purpose': ''}, 'response-status-code.md': {'type': 'file', 'purpose': ''}, 'schema-extra-example.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'first-steps.md': {'type': 'file', 'purpose': ''}, 'get-current-user.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-jwt.md': {'type': 'file', 'purpose': ''}, 'simple-oauth2.md': {'type': 'file', 'purpose': ''}}}, 'server-sent-events.md': {'type': 'file', 'purpose': ''}, 'sql-databases.md': {'type': 'file', 'purpose': ''}, 'static-files.md': {'type': 'file', 'purpose': ''}, 'stream-json-lines.md': {'type': 'file', 'purpose': ''}, 'testing.md': {'type': 'file', 'purpose': ''}}}, 'virtual-environments.md': {'type': 'file', 'purpose': ''}}}, 'llm-prompt.md': {'type': 'file', 'purpose': ''}}}, 'language_names.yml': {'type': 'file', 'purpose': ''}, 'missing-translation.md': {'type': 'file', 'purpose': ''}, 'pt': {'type': 'dir', 'purpose': '', 'children': {'docs': {'type': 'dir', 'purpose': '', 'children': {'_llm-test.md': {'type': 'file', 'purpose': ''}, 'about': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'advanced': {'type': 'dir', 'purpose': '', 'children': {'additional-responses.md': {'type': 'file', 'purpose': ''}, 'additional-status-codes.md': {'type': 'file', 'purpose': ''}, 'advanced-dependencies.md': {'type': 'file', 'purpose': ''}, 'advanced-python-types.md': {'type': 'file', 'purpose': ''}, 'async-tests.md': {'type': 'file', 'purpose': ''}, 'behind-a-proxy.md': {'type': 'file', 'purpose': ''}, 'custom-response.md': {'type': 'file', 'purpose': ''}, 'dataclasses.md': {'type': 'file', 'purpose': ''}, 'events.md': {'type': 'file', 'purpose': ''}, 'generate-clients.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'json-base64-bytes.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'openapi-callbacks.md': {'type': 'file', 'purpose': ''}, 'openapi-webhooks.md': {'type': 'file', 'purpose': ''}, 'path-operation-advanced-configuration.md': {'type': 'file', 'purpose': ''}, 'response-change-status-code.md': {'type': 'file', 'purpose': ''}, 'response-cookies.md': {'type': 'file', 'purpose': ''}, 'response-directly.md': {'type': 'file', 'purpose': ''}, 'response-headers.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'http-basic-auth.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-scopes.md': {'type': 'file', 'purpose': ''}}}, 'settings.md': {'type': 'file', 'purpose': ''}, 'stream-data.md': {'type': 'file', 'purpose': ''}, 'strict-content-type.md': {'type': 'file', 'purpose': ''}, 'sub-applications.md': {'type': 'file', 'purpose': ''}, 'templates.md': {'type': 'file', 'purpose': ''}, 'testing-dependencies.md': {'type': 'file', 'purpose': ''}, 'testing-events.md': {'type': 'file', 'purpose': ''}, 'testing-websockets.md': {'type': 'file', 'purpose': ''}, 'using-request-directly.md': {'type': 'file', 'purpose': ''}, 'websockets.md': {'type': 'file', 'purpose': ''}, 'wsgi.md': {'type': 'file', 'purpose': ''}}}, 'alternatives.md': {'type': 'file', 'purpose': ''}, 'async.md': {'type': 'file', 'purpose': ''}, 'benchmarks.md': {'type': 'file', 'purpose': ''}, 'deployment': {'type': 'dir', 'purpose': '', 'children': {'cloud.md': {'type': 'file', 'purpose': ''}, 'concepts.md': {'type': 'file', 'purpose': ''}, 'docker.md': {'type': 'file', 'purpose': ''}, 'fastapicloud.md': {'type': 'file', 'purpose': ''}, 'https.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'manually.md': {'type': 'file', 'purpose': ''}, 'server-workers.md': {'type': 'file', 'purpose': ''}, 'versions.md': {'type': 'file', 'purpose': ''}}}, 'editor-support.md': {'type': 'file', 'purpose': ''}, 'environment-variables.md': {'type': 'file', 'purpose': ''}, 'fastapi-cli.md': {'type': 'file', 'purpose': ''}, 'features.md': {'type': 'file', 'purpose': ''}, 'help-fastapi.md': {'type': 'file', 'purpose': ''}, 'history-design-future.md': {'type': 'file', 'purpose': ''}, 'how-to': {'type': 'dir', 'purpose': '', 'children': {'authentication-error-status-code.md': {'type': 'file', 'purpose': ''}, 'conditional-openapi.md': {'type': 'file', 'purpose': ''}, 'configure-swagger-ui.md': {'type': 'file', 'purpose': ''}, 'custom-docs-ui-assets.md': {'type': 'file', 'purpose': ''}, 'custom-request-and-route.md': {'type': 'file', 'purpose': ''}, 'extending-openapi.md': {'type': 'file', 'purpose': ''}, 'general.md': {'type': 'file', 'purpose': ''}, 'graphql.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'migrate-from-pydantic-v1-to-pydantic-v2.md': {'type': 'file', 'purpose': ''}, 'separate-openapi-schemas.md': {'type': 'file', 'purpose': ''}, 'testing-database.md': {'type': 'file', 'purpose': ''}}}, 'index.md': {'type': 'file', 'purpose': ''}, 'learn': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'project-generation.md': {'type': 'file', 'purpose': ''}, 'python-types.md': {'type': 'file', 'purpose': ''}, 'resources': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'translation-banner.md': {'type': 'file', 'purpose': ''}, 'tutorial': {'type': 'dir', 'purpose': '', 'children': {'background-tasks.md': {'type': 'file', 'purpose': ''}, 'bigger-applications.md': {'type': 'file', 'purpose': ''}, 'body-fields.md': {'type': 'file', 'purpose': ''}, 'body-multiple-params.md': {'type': 'file', 'purpose': ''}, 'body-nested-models.md': {'type': 'file', 'purpose': ''}, 'body-updates.md': {'type': 'file', 'purpose': ''}, 'body.md': {'type': 'file', 'purpose': ''}, 'cookie-param-models.md': {'type': 'file', 'purpose': ''}, 'cookie-params.md': {'type': 'file', 'purpose': ''}, 'cors.md': {'type': 'file', 'purpose': ''}, 'debugging.md': {'type': 'file', 'purpose': ''}, 'dependencies': {'type': 'dir', 'purpose': '', 'children': {'classes-as-dependencies.md': {'type': 'file', 'purpose': ''}, 'dependencies-in-path-operation-decorators.md': {'type': 'file', 'purpose': ''}, 'dependencies-with-yield.md': {'type': 'file', 'purpose': ''}, 'global-dependencies.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'sub-dependencies.md': {'type': 'file', 'purpose': ''}}}, 'encoder.md': {'type': 'file', 'purpose': ''}, 'extra-data-types.md': {'type': 'file', 'purpose': ''}, 'extra-models.md': {'type': 'file', 'purpose': ''}, 'first-steps.md': {'type': 'file', 'purpose': ''}, 'handling-errors.md': {'type': 'file', 'purpose': ''}, 'header-param-models.md': {'type': 'file', 'purpose': ''}, 'header-params.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'metadata.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'path-operation-configuration.md': {'type': 'file', 'purpose': ''}, 'path-params-numeric-validations.md': {'type': 'file', 'purpose': ''}, 'path-params.md': {'type': 'file', 'purpose': ''}, 'query-param-models.md': {'type': 'file', 'purpose': ''}, 'query-params-str-validations.md': {'type': 'file', 'purpose': ''}, 'query-params.md': {'type': 'file', 'purpose': ''}, 'request-files.md': {'type': 'file', 'purpose': ''}, 'request-form-models.md': {'type': 'file', 'purpose': ''}, 'request-forms-and-files.md': {'type': 'file', 'purpose': ''}, 'request-forms.md': {'type': 'file', 'purpose': ''}, 'response-model.md': {'type': 'file', 'purpose': ''}, 'response-status-code.md': {'type': 'file', 'purpose': ''}, 'schema-extra-example.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'first-steps.md': {'type': 'file', 'purpose': ''}, 'get-current-user.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-jwt.md': {'type': 'file', 'purpose': ''}, 'simple-oauth2.md': {'type': 'file', 'purpose': ''}}}, 'server-sent-events.md': {'type': 'file', 'purpose': ''}, 'sql-databases.md': {'type': 'file', 'purpose': ''}, 'static-files.md': {'type': 'file', 'purpose': ''}, 'stream-json-lines.md': {'type': 'file', 'purpose': ''}, 'testing.md': {'type': 'file', 'purpose': ''}}}, 'virtual-environments.md': {'type': 'file', 'purpose': ''}}}, 'llm-prompt.md': {'type': 'file', 'purpose': ''}}}, 'ru': {'type': 'dir', 'purpose': '', 'children': {'docs': {'type': 'dir', 'purpose': '', 'children': {'_llm-test.md': {'type': 'file', 'purpose': ''}, 'about': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'advanced': {'type': 'dir', 'purpose': '', 'children': {'additional-responses.md': {'type': 'file', 'purpose': ''}, 'additional-status-codes.md': {'type': 'file', 'purpose': ''}, 'advanced-dependencies.md': {'type': 'file', 'purpose': ''}, 'advanced-python-types.md': {'type': 'file', 'purpose': ''}, 'async-tests.md': {'type': 'file', 'purpose': ''}, 'behind-a-proxy.md': {'type': 'file', 'purpose': ''}, 'custom-response.md': {'type': 'file', 'purpose': ''}, 'dataclasses.md': {'type': 'file', 'purpose': ''}, 'events.md': {'type': 'file', 'purpose': ''}, 'generate-clients.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'json-base64-bytes.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'openapi-callbacks.md': {'type': 'file', 'purpose': ''}, 'openapi-webhooks.md': {'type': 'file', 'purpose': ''}, 'path-operation-advanced-configuration.md': {'type': 'file', 'purpose': ''}, 'response-change-status-code.md': {'type': 'file', 'purpose': ''}, 'response-cookies.md': {'type': 'file', 'purpose': ''}, 'response-directly.md': {'type': 'file', 'purpose': ''}, 'response-headers.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'http-basic-auth.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-scopes.md': {'type': 'file', 'purpose': ''}}}, 'settings.md': {'type': 'file', 'purpose': ''}, 'stream-data.md': {'type': 'file', 'purpose': ''}, 'strict-content-type.md': {'type': 'file', 'purpose': ''}, 'sub-applications.md': {'type': 'file', 'purpose': ''}, 'templates.md': {'type': 'file', 'purpose': ''}, 'testing-dependencies.md': {'type': 'file', 'purpose': ''}, 'testing-events.md': {'type': 'file', 'purpose': ''}, 'testing-websockets.md': {'type': 'file', 'purpose': ''}, 'using-request-directly.md': {'type': 'file', 'purpose': ''}, 'websockets.md': {'type': 'file', 'purpose': ''}, 'wsgi.md': {'type': 'file', 'purpose': ''}}}, 'alternatives.md': {'type': 'file', 'purpose': ''}, 'async.md': {'type': 'file', 'purpose': ''}, 'benchmarks.md': {'type': 'file', 'purpose': ''}, 'deployment': {'type': 'dir', 'purpose': '', 'children': {'cloud.md': {'type': 'file', 'purpose': ''}, 'concepts.md': {'type': 'file', 'purpose': ''}, 'docker.md': {'type': 'file', 'purpose': ''}, 'fastapicloud.md': {'type': 'file', 'purpose': ''}, 'https.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'manually.md': {'type': 'file', 'purpose': ''}, 'server-workers.md': {'type': 'file', 'purpose': ''}, 'versions.md': {'type': 'file', 'purpose': ''}}}, 'editor-support.md': {'type': 'file', 'purpose': ''}, 'environment-variables.md': {'type': 'file', 'purpose': ''}, 'fastapi-cli.md': {'type': 'file', 'purpose': ''}, 'features.md': {'type': 'file', 'purpose': ''}, 'help-fastapi.md': {'type': 'file', 'purpose': ''}, 'history-design-future.md': {'type': 'file', 'purpose': ''}, 'how-to': {'type': 'dir', 'purpose': '', 'children': {'authentication-error-status-code.md': {'type': 'file', 'purpose': ''}, 'conditional-openapi.md': {'type': 'file', 'purpose': ''}, 'configure-swagger-ui.md': {'type': 'file', 'purpose': ''}, 'custom-docs-ui-assets.md': {'type': 'file', 'purpose': ''}, 'custom-request-and-route.md': {'type': 'file', 'purpose': ''}, 'extending-openapi.md': {'type': 'file', 'purpose': ''}, 'general.md': {'type': 'file', 'purpose': ''}, 'graphql.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'migrate-from-pydantic-v1-to-pydantic-v2.md': {'type': 'file', 'purpose': ''}, 'separate-openapi-schemas.md': {'type': 'file', 'purpose': ''}, 'testing-database.md': {'type': 'file', 'purpose': ''}}}, 'index.md': {'type': 'file', 'purpose': ''}, 'learn': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'project-generation.md': {'type': 'file', 'purpose': ''}, 'python-types.md': {'type': 'file', 'purpose': ''}, 'resources': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'translation-banner.md': {'type': 'file', 'purpose': ''}, 'tutorial': {'type': 'dir', 'purpose': '', 'children': {'background-tasks.md': {'type': 'file', 'purpose': ''}, 'bigger-applications.md': {'type': 'file', 'purpose': ''}, 'body-fields.md': {'type': 'file', 'purpose': ''}, 'body-multiple-params.md': {'type': 'file', 'purpose': ''}, 'body-nested-models.md': {'type': 'file', 'purpose': ''}, 'body-updates.md': {'type': 'file', 'purpose': ''}, 'body.md': {'type': 'file', 'purpose': ''}, 'cookie-param-models.md': {'type': 'file', 'purpose': ''}, 'cookie-params.md': {'type': 'file', 'purpose': ''}, 'cors.md': {'type': 'file', 'purpose': ''}, 'debugging.md': {'type': 'file', 'purpose': ''}, 'dependencies': {'type': 'dir', 'purpose': '', 'children': {'classes-as-dependencies.md': {'type': 'file', 'purpose': ''}, 'dependencies-in-path-operation-decorators.md': {'type': 'file', 'purpose': ''}, 'dependencies-with-yield.md': {'type': 'file', 'purpose': ''}, 'global-dependencies.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'sub-dependencies.md': {'type': 'file', 'purpose': ''}}}, 'encoder.md': {'type': 'file', 'purpose': ''}, 'extra-data-types.md': {'type': 'file', 'purpose': ''}, 'extra-models.md': {'type': 'file', 'purpose': ''}, 'first-steps.md': {'type': 'file', 'purpose': ''}, 'handling-errors.md': {'type': 'file', 'purpose': ''}, 'header-param-models.md': {'type': 'file', 'purpose': ''}, 'header-params.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'metadata.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'path-operation-configuration.md': {'type': 'file', 'purpose': ''}, 'path-params-numeric-validations.md': {'type': 'file', 'purpose': ''}, 'path-params.md': {'type': 'file', 'purpose': ''}, 'query-param-models.md': {'type': 'file', 'purpose': ''}, 'query-params-str-validations.md': {'type': 'file', 'purpose': ''}, 'query-params.md': {'type': 'file', 'purpose': ''}, 'request-files.md': {'type': 'file', 'purpose': ''}, 'request-form-models.md': {'type': 'file', 'purpose': ''}, 'request-forms-and-files.md': {'type': 'file', 'purpose': ''}, 'request-forms.md': {'type': 'file', 'purpose': ''}, 'response-model.md': {'type': 'file', 'purpose': ''}, 'response-status-code.md': {'type': 'file', 'purpose': ''}, 'schema-extra-example.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'first-steps.md': {'type': 'file', 'purpose': ''}, 'get-current-user.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-jwt.md': {'type': 'file', 'purpose': ''}, 'simple-oauth2.md': {'type': 'file', 'purpose': ''}}}, 'server-sent-events.md': {'type': 'file', 'purpose': ''}, 'sql-databases.md': {'type': 'file', 'purpose': ''}, 'static-files.md': {'type': 'file', 'purpose': ''}, 'stream-json-lines.md': {'type': 'file', 'purpose': ''}, 'testing.md': {'type': 'file', 'purpose': ''}}}, 'virtual-environments.md': {'type': 'file', 'purpose': ''}}}, 'llm-prompt.md': {'type': 'file', 'purpose': ''}}}, 'tr': {'type': 'dir', 'purpose': '', 'children': {'docs': {'type': 'dir', 'purpose': '', 'children': {'_llm-test.md': {'type': 'file', 'purpose': ''}, 'about': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'advanced': {'type': 'dir', 'purpose': '', 'children': {'additional-responses.md': {'type': 'file', 'purpose': ''}, 'additional-status-codes.md': {'type': 'file', 'purpose': ''}, 'advanced-dependencies.md': {'type': 'file', 'purpose': ''}, 'advanced-python-types.md': {'type': 'file', 'purpose': ''}, 'async-tests.md': {'type': 'file', 'purpose': ''}, 'behind-a-proxy.md': {'type': 'file', 'purpose': ''}, 'custom-response.md': {'type': 'file', 'purpose': ''}, 'dataclasses.md': {'type': 'file', 'purpose': ''}, 'events.md': {'type': 'file', 'purpose': ''}, 'generate-clients.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'json-base64-bytes.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'openapi-callbacks.md': {'type': 'file', 'purpose': ''}, 'openapi-webhooks.md': {'type': 'file', 'purpose': ''}, 'path-operation-advanced-configuration.md': {'type': 'file', 'purpose': ''}, 'response-change-status-code.md': {'type': 'file', 'purpose': ''}, 'response-cookies.md': {'type': 'file', 'purpose': ''}, 'response-directly.md': {'type': 'file', 'purpose': ''}, 'response-headers.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'http-basic-auth.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-scopes.md': {'type': 'file', 'purpose': ''}}}, 'settings.md': {'type': 'file', 'purpose': ''}, 'stream-data.md': {'type': 'file', 'purpose': ''}, 'strict-content-type.md': {'type': 'file', 'purpose': ''}, 'sub-applications.md': {'type': 'file', 'purpose': ''}, 'templates.md': {'type': 'file', 'purpose': ''}, 'testing-dependencies.md': {'type': 'file', 'purpose': ''}, 'testing-events.md': {'type': 'file', 'purpose': ''}, 'testing-websockets.md': {'type': 'file', 'purpose': ''}, 'using-request-directly.md': {'type': 'file', 'purpose': ''}, 'websockets.md': {'type': 'file', 'purpose': ''}, 'wsgi.md': {'type': 'file', 'purpose': ''}}}, 'alternatives.md': {'type': 'file', 'purpose': ''}, 'async.md': {'type': 'file', 'purpose': ''}, 'benchmarks.md': {'type': 'file', 'purpose': ''}, 'deployment': {'type': 'dir', 'purpose': '', 'children': {'cloud.md': {'type': 'file', 'purpose': ''}, 'concepts.md': {'type': 'file', 'purpose': ''}, 'docker.md': {'type': 'file', 'purpose': ''}, 'fastapicloud.md': {'type': 'file', 'purpose': ''}, 'https.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'manually.md': {'type': 'file', 'purpose': ''}, 'server-workers.md': {'type': 'file', 'purpose': ''}, 'versions.md': {'type': 'file', 'purpose': ''}}}, 'editor-support.md': {'type': 'file', 'purpose': ''}, 'environment-variables.md': {'type': 'file', 'purpose': ''}, 'fastapi-cli.md': {'type': 'file', 'purpose': ''}, 'features.md': {'type': 'file', 'purpose': ''}, 'help-fastapi.md': {'type': 'file', 'purpose': ''}, 'history-design-future.md': {'type': 'file', 'purpose': ''}, 'how-to': {'type': 'dir', 'purpose': '', 'children': {'authentication-error-status-code.md': {'type': 'file', 'purpose': ''}, 'conditional-openapi.md': {'type': 'file', 'purpose': ''}, 'configure-swagger-ui.md': {'type': 'file', 'purpose': ''}, 'custom-docs-ui-assets.md': {'type': 'file', 'purpose': ''}, 'custom-request-and-route.md': {'type': 'file', 'purpose': ''}, 'extending-openapi.md': {'type': 'file', 'purpose': ''}, 'general.md': {'type': 'file', 'purpose': ''}, 'graphql.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'migrate-from-pydantic-v1-to-pydantic-v2.md': {'type': 'file', 'purpose': ''}, 'separate-openapi-schemas.md': {'type': 'file', 'purpose': ''}, 'testing-database.md': {'type': 'file', 'purpose': ''}}}, 'index.md': {'type': 'file', 'purpose': ''}, 'learn': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'project-generation.md': {'type': 'file', 'purpose': ''}, 'python-types.md': {'type': 'file', 'purpose': ''}, 'resources': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'translation-banner.md': {'type': 'file', 'purpose': ''}, 'tutorial': {'type': 'dir', 'purpose': '', 'children': {'background-tasks.md': {'type': 'file', 'purpose': ''}, 'bigger-applications.md': {'type': 'file', 'purpose': ''}, 'body-fields.md': {'type': 'file', 'purpose': ''}, 'body-multiple-params.md': {'type': 'file', 'purpose': ''}, 'body-nested-models.md': {'type': 'file', 'purpose': ''}, 'body-updates.md': {'type': 'file', 'purpose': ''}, 'body.md': {'type': 'file', 'purpose': ''}, 'cookie-param-models.md': {'type': 'file', 'purpose': ''}, 'cookie-params.md': {'type': 'file', 'purpose': ''}, 'cors.md': {'type': 'file', 'purpose': ''}, 'debugging.md': {'type': 'file', 'purpose': ''}, 'dependencies': {'type': 'dir', 'purpose': '', 'children': {'classes-as-dependencies.md': {'type': 'file', 'purpose': ''}, 'dependencies-in-path-operation-decorators.md': {'type': 'file', 'purpose': ''}, 'dependencies-with-yield.md': {'type': 'file', 'purpose': ''}, 'global-dependencies.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'sub-dependencies.md': {'type': 'file', 'purpose': ''}}}, 'encoder.md': {'type': 'file', 'purpose': ''}, 'extra-data-types.md': {'type': 'file', 'purpose': ''}, 'extra-models.md': {'type': 'file', 'purpose': ''}, 'first-steps.md': {'type': 'file', 'purpose': ''}, 'handling-errors.md': {'type': 'file', 'purpose': ''}, 'header-param-models.md': {'type': 'file', 'purpose': ''}, 'header-params.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'metadata.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'path-operation-configuration.md': {'type': 'file', 'purpose': ''}, 'path-params-numeric-validations.md': {'type': 'file', 'purpose': ''}, 'path-params.md': {'type': 'file', 'purpose': ''}, 'query-param-models.md': {'type': 'file', 'purpose': ''}, 'query-params-str-validations.md': {'type': 'file', 'purpose': ''}, 'query-params.md': {'type': 'file', 'purpose': ''}, 'request-files.md': {'type': 'file', 'purpose': ''}, 'request-form-models.md': {'type': 'file', 'purpose': ''}, 'request-forms-and-files.md': {'type': 'file', 'purpose': ''}, 'request-forms.md': {'type': 'file', 'purpose': ''}, 'response-model.md': {'type': 'file', 'purpose': ''}, 'response-status-code.md': {'type': 'file', 'purpose': ''}, 'schema-extra-example.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'first-steps.md': {'type': 'file', 'purpose': ''}, 'get-current-user.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-jwt.md': {'type': 'file', 'purpose': ''}, 'simple-oauth2.md': {'type': 'file', 'purpose': ''}}}, 'server-sent-events.md': {'type': 'file', 'purpose': ''}, 'sql-databases.md': {'type': 'file', 'purpose': ''}, 'static-files.md': {'type': 'file', 'purpose': ''}, 'stream-json-lines.md': {'type': 'file', 'purpose': ''}, 'testing.md': {'type': 'file', 'purpose': ''}}}, 'virtual-environments.md': {'type': 'file', 'purpose': ''}}}, 'llm-prompt.md': {'type': 'file', 'purpose': ''}}}, 'uk': {'type': 'dir', 'purpose': '', 'children': {'docs': {'type': 'dir', 'purpose': '', 'children': {'_llm-test.md': {'type': 'file', 'purpose': ''}, 'about': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'advanced': {'type': 'dir', 'purpose': '', 'children': {'additional-responses.md': {'type': 'file', 'purpose': ''}, 'additional-status-codes.md': {'type': 'file', 'purpose': ''}, 'advanced-dependencies.md': {'type': 'file', 'purpose': ''}, 'advanced-python-types.md': {'type': 'file', 'purpose': ''}, 'async-tests.md': {'type': 'file', 'purpose': ''}, 'behind-a-proxy.md': {'type': 'file', 'purpose': ''}, 'custom-response.md': {'type': 'file', 'purpose': ''}, 'dataclasses.md': {'type': 'file', 'purpose': ''}, 'events.md': {'type': 'file', 'purpose': ''}, 'generate-clients.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'json-base64-bytes.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'openapi-callbacks.md': {'type': 'file', 'purpose': ''}, 'openapi-webhooks.md': {'type': 'file', 'purpose': ''}, 'path-operation-advanced-configuration.md': {'type': 'file', 'purpose': ''}, 'response-change-status-code.md': {'type': 'file', 'purpose': ''}, 'response-cookies.md': {'type': 'file', 'purpose': ''}, 'response-directly.md': {'type': 'file', 'purpose': ''}, 'response-headers.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'http-basic-auth.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-scopes.md': {'type': 'file', 'purpose': ''}}}, 'settings.md': {'type': 'file', 'purpose': ''}, 'stream-data.md': {'type': 'file', 'purpose': ''}, 'strict-content-type.md': {'type': 'file', 'purpose': ''}, 'sub-applications.md': {'type': 'file', 'purpose': ''}, 'templates.md': {'type': 'file', 'purpose': ''}, 'testing-dependencies.md': {'type': 'file', 'purpose': ''}, 'testing-events.md': {'type': 'file', 'purpose': ''}, 'testing-websockets.md': {'type': 'file', 'purpose': ''}, 'using-request-directly.md': {'type': 'file', 'purpose': ''}, 'websockets.md': {'type': 'file', 'purpose': ''}, 'wsgi.md': {'type': 'file', 'purpose': ''}}}, 'alternatives.md': {'type': 'file', 'purpose': ''}, 'async.md': {'type': 'file', 'purpose': ''}, 'benchmarks.md': {'type': 'file', 'purpose': ''}, 'deployment': {'type': 'dir', 'purpose': '', 'children': {'cloud.md': {'type': 'file', 'purpose': ''}, 'concepts.md': {'type': 'file', 'purpose': ''}, 'docker.md': {'type': 'file', 'purpose': ''}, 'fastapicloud.md': {'type': 'file', 'purpose': ''}, 'https.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'manually.md': {'type': 'file', 'purpose': ''}, 'server-workers.md': {'type': 'file', 'purpose': ''}, 'versions.md': {'type': 'file', 'purpose': ''}}}, 'editor-support.md': {'type': 'file', 'purpose': ''}, 'environment-variables.md': {'type': 'file', 'purpose': ''}, 'fastapi-cli.md': {'type': 'file', 'purpose': ''}, 'features.md': {'type': 'file', 'purpose': ''}, 'help-fastapi.md': {'type': 'file', 'purpose': ''}, 'history-design-future.md': {'type': 'file', 'purpose': ''}, 'how-to': {'type': 'dir', 'purpose': '', 'children': {'authentication-error-status-code.md': {'type': 'file', 'purpose': ''}, 'conditional-openapi.md': {'type': 'file', 'purpose': ''}, 'configure-swagger-ui.md': {'type': 'file', 'purpose': ''}, 'custom-docs-ui-assets.md': {'type': 'file', 'purpose': ''}, 'custom-request-and-route.md': {'type': 'file', 'purpose': ''}, 'extending-openapi.md': {'type': 'file', 'purpose': ''}, 'general.md': {'type': 'file', 'purpose': ''}, 'graphql.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'migrate-from-pydantic-v1-to-pydantic-v2.md': {'type': 'file', 'purpose': ''}, 'separate-openapi-schemas.md': {'type': 'file', 'purpose': ''}, 'testing-database.md': {'type': 'file', 'purpose': ''}}}, 'index.md': {'type': 'file', 'purpose': ''}, 'learn': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'project-generation.md': {'type': 'file', 'purpose': ''}, 'python-types.md': {'type': 'file', 'purpose': ''}, 'resources': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'translation-banner.md': {'type': 'file', 'purpose': ''}, 'tutorial': {'type': 'dir', 'purpose': '', 'children': {'background-tasks.md': {'type': 'file', 'purpose': ''}, 'bigger-applications.md': {'type': 'file', 'purpose': ''}, 'body-fields.md': {'type': 'file', 'purpose': ''}, 'body-multiple-params.md': {'type': 'file', 'purpose': ''}, 'body-nested-models.md': {'type': 'file', 'purpose': ''}, 'body-updates.md': {'type': 'file', 'purpose': ''}, 'body.md': {'type': 'file', 'purpose': ''}, 'cookie-param-models.md': {'type': 'file', 'purpose': ''}, 'cookie-params.md': {'type': 'file', 'purpose': ''}, 'cors.md': {'type': 'file', 'purpose': ''}, 'debugging.md': {'type': 'file', 'purpose': ''}, 'dependencies': {'type': 'dir', 'purpose': '', 'children': {'classes-as-dependencies.md': {'type': 'file', 'purpose': ''}, 'dependencies-in-path-operation-decorators.md': {'type': 'file', 'purpose': ''}, 'dependencies-with-yield.md': {'type': 'file', 'purpose': ''}, 'global-dependencies.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'sub-dependencies.md': {'type': 'file', 'purpose': ''}}}, 'encoder.md': {'type': 'file', 'purpose': ''}, 'extra-data-types.md': {'type': 'file', 'purpose': ''}, 'extra-models.md': {'type': 'file', 'purpose': ''}, 'first-steps.md': {'type': 'file', 'purpose': ''}, 'handling-errors.md': {'type': 'file', 'purpose': ''}, 'header-param-models.md': {'type': 'file', 'purpose': ''}, 'header-params.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'metadata.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'path-operation-configuration.md': {'type': 'file', 'purpose': ''}, 'path-params-numeric-validations.md': {'type': 'file', 'purpose': ''}, 'path-params.md': {'type': 'file', 'purpose': ''}, 'query-param-models.md': {'type': 'file', 'purpose': ''}, 'query-params-str-validations.md': {'type': 'file', 'purpose': ''}, 'query-params.md': {'type': 'file', 'purpose': ''}, 'request-files.md': {'type': 'file', 'purpose': ''}, 'request-form-models.md': {'type': 'file', 'purpose': ''}, 'request-forms-and-files.md': {'type': 'file', 'purpose': ''}, 'request-forms.md': {'type': 'file', 'purpose': ''}, 'response-model.md': {'type': 'file', 'purpose': ''}, 'response-status-code.md': {'type': 'file', 'purpose': ''}, 'schema-extra-example.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'first-steps.md': {'type': 'file', 'purpose': ''}, 'get-current-user.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-jwt.md': {'type': 'file', 'purpose': ''}, 'simple-oauth2.md': {'type': 'file', 'purpose': ''}}}, 'server-sent-events.md': {'type': 'file', 'purpose': ''}, 'sql-databases.md': {'type': 'file', 'purpose': ''}, 'static-files.md': {'type': 'file', 'purpose': ''}, 'stream-json-lines.md': {'type': 'file', 'purpose': ''}, 'testing.md': {'type': 'file', 'purpose': ''}}}, 'virtual-environments.md': {'type': 'file', 'purpose': ''}}}, 'llm-prompt.md': {'type': 'file', 'purpose': ''}}}, 'zh': {'type': 'dir', 'purpose': '', 'children': {'docs': {'type': 'dir', 'purpose': '', 'children': {'_llm-test.md': {'type': 'file', 'purpose': ''}, 'about': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'advanced': {'type': 'dir', 'purpose': '', 'children': {'additional-responses.md': {'type': 'file', 'purpose': ''}, 'additional-status-codes.md': {'type': 'file', 'purpose': ''}, 'advanced-dependencies.md': {'type': 'file', 'purpose': ''}, 'advanced-python-types.md': {'type': 'file', 'purpose': ''}, 'async-tests.md': {'type': 'file', 'purpose': ''}, 'behind-a-proxy.md': {'type': 'file', 'purpose': ''}, 'custom-response.md': {'type': 'file', 'purpose': ''}, 'dataclasses.md': {'type': 'file', 'purpose': ''}, 'events.md': {'type': 'file', 'purpose': ''}, 'generate-clients.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'json-base64-bytes.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'openapi-callbacks.md': {'type': 'file', 'purpose': ''}, 'openapi-webhooks.md': {'type': 'file', 'purpose': ''}, 'path-operation-advanced-configuration.md': {'type': 'file', 'purpose': ''}, 'response-change-status-code.md': {'type': 'file', 'purpose': ''}, 'response-cookies.md': {'type': 'file', 'purpose': ''}, 'response-directly.md': {'type': 'file', 'purpose': ''}, 'response-headers.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'http-basic-auth.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-scopes.md': {'type': 'file', 'purpose': ''}}}, 'settings.md': {'type': 'file', 'purpose': ''}, 'stream-data.md': {'type': 'file', 'purpose': ''}, 'strict-content-type.md': {'type': 'file', 'purpose': ''}, 'sub-applications.md': {'type': 'file', 'purpose': ''}, 'templates.md': {'type': 'file', 'purpose': ''}, 'testing-dependencies.md': {'type': 'file', 'purpose': ''}, 'testing-events.md': {'type': 'file', 'purpose': ''}, 'testing-websockets.md': {'type': 'file', 'purpose': ''}, 'using-request-directly.md': {'type': 'file', 'purpose': ''}, 'websockets.md': {'type': 'file', 'purpose': ''}, 'wsgi.md': {'type': 'file', 'purpose': ''}}}, 'alternatives.md': {'type': 'file', 'purpose': ''}, 'async.md': {'type': 'file', 'purpose': ''}, 'benchmarks.md': {'type': 'file', 'purpose': ''}, 'deployment': {'type': 'dir', 'purpose': '', 'children': {'cloud.md': {'type': 'file', 'purpose': ''}, 'concepts.md': {'type': 'file', 'purpose': ''}, 'docker.md': {'type': 'file', 'purpose': ''}, 'fastapicloud.md': {'type': 'file', 'purpose': ''}, 'https.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'manually.md': {'type': 'file', 'purpose': ''}, 'server-workers.md': {'type': 'file', 'purpose': ''}, 'versions.md': {'type': 'file', 'purpose': ''}}}, 'editor-support.md': {'type': 'file', 'purpose': ''}, 'environment-variables.md': {'type': 'file', 'purpose': ''}, 'fastapi-cli.md': {'type': 'file', 'purpose': ''}, 'features.md': {'type': 'file', 'purpose': ''}, 'help-fastapi.md': {'type': 'file', 'purpose': ''}, 'history-design-future.md': {'type': 'file', 'purpose': ''}, 'how-to': {'type': 'dir', 'purpose': '', 'children': {'authentication-error-status-code.md': {'type': 'file', 'purpose': ''}, 'conditional-openapi.md': {'type': 'file', 'purpose': ''}, 'configure-swagger-ui.md': {'type': 'file', 'purpose': ''}, 'custom-docs-ui-assets.md': {'type': 'file', 'purpose': ''}, 'custom-request-and-route.md': {'type': 'file', 'purpose': ''}, 'extending-openapi.md': {'type': 'file', 'purpose': ''}, 'general.md': {'type': 'file', 'purpose': ''}, 'graphql.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'migrate-from-pydantic-v1-to-pydantic-v2.md': {'type': 'file', 'purpose': ''}, 'separate-openapi-schemas.md': {'type': 'file', 'purpose': ''}, 'testing-database.md': {'type': 'file', 'purpose': ''}}}, 'index.md': {'type': 'file', 'purpose': ''}, 'learn': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'project-generation.md': {'type': 'file', 'purpose': ''}, 'python-types.md': {'type': 'file', 'purpose': ''}, 'resources': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'translation-banner.md': {'type': 'file', 'purpose': ''}, 'tutorial': {'type': 'dir', 'purpose': '', 'children': {'background-tasks.md': {'type': 'file', 'purpose': ''}, 'bigger-applications.md': {'type': 'file', 'purpose': ''}, 'body-fields.md': {'type': 'file', 'purpose': ''}, 'body-multiple-params.md': {'type': 'file', 'purpose': ''}, 'body-nested-models.md': {'type': 'file', 'purpose': ''}, 'body-updates.md': {'type': 'file', 'purpose': ''}, 'body.md': {'type': 'file', 'purpose': ''}, 'cookie-param-models.md': {'type': 'file', 'purpose': ''}, 'cookie-params.md': {'type': 'file', 'purpose': ''}, 'cors.md': {'type': 'file', 'purpose': ''}, 'debugging.md': {'type': 'file', 'purpose': ''}, 'dependencies': {'type': 'dir', 'purpose': '', 'children': {'classes-as-dependencies.md': {'type': 'file', 'purpose': ''}, 'dependencies-in-path-operation-decorators.md': {'type': 'file', 'purpose': ''}, 'dependencies-with-yield.md': {'type': 'file', 'purpose': ''}, 'global-dependencies.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'sub-dependencies.md': {'type': 'file', 'purpose': ''}}}, 'encoder.md': {'type': 'file', 'purpose': ''}, 'extra-data-types.md': {'type': 'file', 'purpose': ''}, 'extra-models.md': {'type': 'file', 'purpose': ''}, 'first-steps.md': {'type': 'file', 'purpose': ''}, 'handling-errors.md': {'type': 'file', 'purpose': ''}, 'header-param-models.md': {'type': 'file', 'purpose': ''}, 'header-params.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'metadata.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'path-operation-configuration.md': {'type': 'file', 'purpose': ''}, 'path-params-numeric-validations.md': {'type': 'file', 'purpose': ''}, 'path-params.md': {'type': 'file', 'purpose': ''}, 'query-param-models.md': {'type': 'file', 'purpose': ''}, 'query-params-str-validations.md': {'type': 'file', 'purpose': ''}, 'query-params.md': {'type': 'file', 'purpose': ''}, 'request-files.md': {'type': 'file', 'purpose': ''}, 'request-form-models.md': {'type': 'file', 'purpose': ''}, 'request-forms-and-files.md': {'type': 'file', 'purpose': ''}, 'request-forms.md': {'type': 'file', 'purpose': ''}, 'response-model.md': {'type': 'file', 'purpose': ''}, 'response-status-code.md': {'type': 'file', 'purpose': ''}, 'schema-extra-example.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'first-steps.md': {'type': 'file', 'purpose': ''}, 'get-current-user.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-jwt.md': {'type': 'file', 'purpose': ''}, 'simple-oauth2.md': {'type': 'file', 'purpose': ''}}}, 'server-sent-events.md': {'type': 'file', 'purpose': ''}, 'sql-databases.md': {'type': 'file', 'purpose': ''}, 'static-files.md': {'type': 'file', 'purpose': ''}, 'stream-json-lines.md': {'type': 'file', 'purpose': ''}, 'testing.md': {'type': 'file', 'purpose': ''}}}, 'virtual-environments.md': {'type': 'file', 'purpose': ''}}}, 'llm-prompt.md': {'type': 'file', 'purpose': ''}}}, 'zh-hant': {'type': 'dir', 'purpose': '', 'children': {'docs': {'type': 'dir', 'purpose': '', 'children': {'_llm-test.md': {'type': 'file', 'purpose': ''}, 'about': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'advanced': {'type': 'dir', 'purpose': '', 'children': {'additional-responses.md': {'type': 'file', 'purpose': ''}, 'additional-status-codes.md': {'type': 'file', 'purpose': ''}, 'advanced-dependencies.md': {'type': 'file', 'purpose': ''}, 'advanced-python-types.md': {'type': 'file', 'purpose': ''}, 'async-tests.md': {'type': 'file', 'purpose': ''}, 'behind-a-proxy.md': {'type': 'file', 'purpose': ''}, 'custom-response.md': {'type': 'file', 'purpose': ''}, 'dataclasses.md': {'type': 'file', 'purpose': ''}, 'events.md': {'type': 'file', 'purpose': ''}, 'generate-clients.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'json-base64-bytes.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'openapi-callbacks.md': {'type': 'file', 'purpose': ''}, 'openapi-webhooks.md': {'type': 'file', 'purpose': ''}, 'path-operation-advanced-configuration.md': {'type': 'file', 'purpose': ''}, 'response-change-status-code.md': {'type': 'file', 'purpose': ''}, 'response-cookies.md': {'type': 'file', 'purpose': ''}, 'response-directly.md': {'type': 'file', 'purpose': ''}, 'response-headers.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'http-basic-auth.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-scopes.md': {'type': 'file', 'purpose': ''}}}, 'settings.md': {'type': 'file', 'purpose': ''}, 'stream-data.md': {'type': 'file', 'purpose': ''}, 'strict-content-type.md': {'type': 'file', 'purpose': ''}, 'sub-applications.md': {'type': 'file', 'purpose': ''}, 'templates.md': {'type': 'file', 'purpose': ''}, 'testing-dependencies.md': {'type': 'file', 'purpose': ''}, 'testing-events.md': {'type': 'file', 'purpose': ''}, 'testing-websockets.md': {'type': 'file', 'purpose': ''}, 'using-request-directly.md': {'type': 'file', 'purpose': ''}, 'websockets.md': {'type': 'file', 'purpose': ''}, 'wsgi.md': {'type': 'file', 'purpose': ''}}}, 'alternatives.md': {'type': 'file', 'purpose': ''}, 'async.md': {'type': 'file', 'purpose': ''}, 'benchmarks.md': {'type': 'file', 'purpose': ''}, 'deployment': {'type': 'dir', 'purpose': '', 'children': {'cloud.md': {'type': 'file', 'purpose': ''}, 'concepts.md': {'type': 'file', 'purpose': ''}, 'docker.md': {'type': 'file', 'purpose': ''}, 'fastapicloud.md': {'type': 'file', 'purpose': ''}, 'https.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'manually.md': {'type': 'file', 'purpose': ''}, 'server-workers.md': {'type': 'file', 'purpose': ''}, 'versions.md': {'type': 'file', 'purpose': ''}}}, 'editor-support.md': {'type': 'file', 'purpose': ''}, 'environment-variables.md': {'type': 'file', 'purpose': ''}, 'fastapi-cli.md': {'type': 'file', 'purpose': ''}, 'features.md': {'type': 'file', 'purpose': ''}, 'help-fastapi.md': {'type': 'file', 'purpose': ''}, 'history-design-future.md': {'type': 'file', 'purpose': ''}, 'how-to': {'type': 'dir', 'purpose': '', 'children': {'authentication-error-status-code.md': {'type': 'file', 'purpose': ''}, 'conditional-openapi.md': {'type': 'file', 'purpose': ''}, 'configure-swagger-ui.md': {'type': 'file', 'purpose': ''}, 'custom-docs-ui-assets.md': {'type': 'file', 'purpose': ''}, 'custom-request-and-route.md': {'type': 'file', 'purpose': ''}, 'extending-openapi.md': {'type': 'file', 'purpose': ''}, 'general.md': {'type': 'file', 'purpose': ''}, 'graphql.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'migrate-from-pydantic-v1-to-pydantic-v2.md': {'type': 'file', 'purpose': ''}, 'separate-openapi-schemas.md': {'type': 'file', 'purpose': ''}, 'testing-database.md': {'type': 'file', 'purpose': ''}}}, 'index.md': {'type': 'file', 'purpose': ''}, 'learn': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'project-generation.md': {'type': 'file', 'purpose': ''}, 'python-types.md': {'type': 'file', 'purpose': ''}, 'resources': {'type': 'dir', 'purpose': '', 'children': {'index.md': {'type': 'file', 'purpose': ''}}}, 'translation-banner.md': {'type': 'file', 'purpose': ''}, 'tutorial': {'type': 'dir', 'purpose': '', 'children': {'background-tasks.md': {'type': 'file', 'purpose': ''}, 'bigger-applications.md': {'type': 'file', 'purpose': ''}, 'body-fields.md': {'type': 'file', 'purpose': ''}, 'body-multiple-params.md': {'type': 'file', 'purpose': ''}, 'body-nested-models.md': {'type': 'file', 'purpose': ''}, 'body-updates.md': {'type': 'file', 'purpose': ''}, 'body.md': {'type': 'file', 'purpose': ''}, 'cookie-param-models.md': {'type': 'file', 'purpose': ''}, 'cookie-params.md': {'type': 'file', 'purpose': ''}, 'cors.md': {'type': 'file', 'purpose': ''}, 'debugging.md': {'type': 'file', 'purpose': ''}, 'dependencies': {'type': 'dir', 'purpose': '', 'children': {'classes-as-dependencies.md': {'type': 'file', 'purpose': ''}, 'dependencies-in-path-operation-decorators.md': {'type': 'file', 'purpose': ''}, 'dependencies-with-yield.md': {'type': 'file', 'purpose': ''}, 'global-dependencies.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'sub-dependencies.md': {'type': 'file', 'purpose': ''}}}, 'encoder.md': {'type': 'file', 'purpose': ''}, 'extra-data-types.md': {'type': 'file', 'purpose': ''}, 'extra-models.md': {'type': 'file', 'purpose': ''}, 'first-steps.md': {'type': 'file', 'purpose': ''}, 'handling-errors.md': {'type': 'file', 'purpose': ''}, 'header-param-models.md': {'type': 'file', 'purpose': ''}, 'header-params.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'metadata.md': {'type': 'file', 'purpose': ''}, 'middleware.md': {'type': 'file', 'purpose': ''}, 'path-operation-configuration.md': {'type': 'file', 'purpose': ''}, 'path-params-numeric-validations.md': {'type': 'file', 'purpose': ''}, 'path-params.md': {'type': 'file', 'purpose': ''}, 'query-param-models.md': {'type': 'file', 'purpose': ''}, 'query-params-str-validations.md': {'type': 'file', 'purpose': ''}, 'query-params.md': {'type': 'file', 'purpose': ''}, 'request-files.md': {'type': 'file', 'purpose': ''}, 'request-form-models.md': {'type': 'file', 'purpose': ''}, 'request-forms-and-files.md': {'type': 'file', 'purpose': ''}, 'request-forms.md': {'type': 'file', 'purpose': ''}, 'response-model.md': {'type': 'file', 'purpose': ''}, 'response-status-code.md': {'type': 'file', 'purpose': ''}, 'schema-extra-example.md': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'first-steps.md': {'type': 'file', 'purpose': ''}, 'get-current-user.md': {'type': 'file', 'purpose': ''}, 'index.md': {'type': 'file', 'purpose': ''}, 'oauth2-jwt.md': {'type': 'file', 'purpose': ''}, 'simple-oauth2.md': {'type': 'file', 'purpose': ''}}}, 'server-sent-events.md': {'type': 'file', 'purpose': ''}, 'sql-databases.md': {'type': 'file', 'purpose': ''}, 'static-files.md': {'type': 'file', 'purpose': ''}, 'stream-json-lines.md': {'type': 'file', 'purpose': ''}, 'testing.md': {'type': 'file', 'purpose': ''}}}, 'virtual-environments.md': {'type': 'file', 'purpose': ''}}}, 'llm-prompt.md': {'type': 'file', 'purpose': ''}}}}}, 'fastapi': {'purpose': 'source code', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, '__main__.py': {'type': 'file', 'purpose': ''}, '_compat': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'shared.py': {'type': 'file', 'purpose': ''}, 'v2.py': {'type': 'file', 'purpose': ''}}}, 'applications.py': {'type': 'file', 'purpose': ''}, 'background.py': {'type': 'file', 'purpose': ''}, 'cli.py': {'type': 'file', 'purpose': ''}, 'concurrency.py': {'type': 'file', 'purpose': ''}, 'datastructures.py': {'type': 'file', 'purpose': ''}, 'dependencies': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'models.py': {'type': 'file', 'purpose': ''}, 'utils.py': {'type': 'file', 'purpose': ''}}}, 'encoders.py': {'type': 'file', 'purpose': ''}, 'exception_handlers.py': {'type': 'file', 'purpose': ''}, 'exceptions.py': {'type': 'file', 'purpose': ''}, 'logger.py': {'type': 'file', 'purpose': ''}, 'middleware': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'asyncexitstack.py': {'type': 'file', 'purpose': ''}, 'cors.py': {'type': 'file', 'purpose': ''}, 'gzip.py': {'type': 'file', 'purpose': ''}, 'httpsredirect.py': {'type': 'file', 'purpose': ''}, 'trustedhost.py': {'type': 'file', 'purpose': ''}, 'wsgi.py': {'type': 'file', 'purpose': ''}}}, 'openapi': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'constants.py': {'type': 'file', 'purpose': ''}, 'docs.py': {'type': 'file', 'purpose': ''}, 'models.py': {'type': 'file', 'purpose': ''}, 'utils.py': {'type': 'file', 'purpose': ''}}}, 'param_functions.py': {'type': 'file', 'purpose': ''}, 'params.py': {'type': 'file', 'purpose': ''}, 'py.typed': {'type': 'file', 'purpose': ''}, 'requests.py': {'type': 'file', 'purpose': ''}, 'responses.py': {'type': 'file', 'purpose': ''}, 'routing.py': {'type': 'file', 'purpose': ''}, 'security': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'api_key.py': {'type': 'file', 'purpose': ''}, 'base.py': {'type': 'file', 'purpose': ''}, 'http.py': {'type': 'file', 'purpose': ''}, 'oauth2.py': {'type': 'file', 'purpose': ''}, 'open_id_connect_url.py': {'type': 'file', 'purpose': ''}, 'utils.py': {'type': 'file', 'purpose': ''}}}, 'sse.py': {'type': 'file', 'purpose': ''}, 'staticfiles.py': {'type': 'file', 'purpose': ''}, 'templating.py': {'type': 'file', 'purpose': ''}, 'testclient.py': {'type': 'file', 'purpose': ''}, 'types.py': {'type': 'file', 'purpose': ''}, 'utils.py': {'type': 'file', 'purpose': ''}, 'websockets.py': {'type': 'file', 'purpose': ''}}}, 'scripts': {'purpose': 'scripts', 'children': {'add_latest_release_date.py': {'type': 'file', 'purpose': ''}, 'contributors.py': {'type': 'file', 'purpose': ''}, 'deploy_docs_status.py': {'type': 'file', 'purpose': ''}, 'doc_parsing_utils.py': {'type': 'file', 'purpose': ''}, 'docs.py': {'type': 'file', 'purpose': ''}, 'format.sh': {'type': 'file', 'purpose': ''}, 'general-llm-prompt.md': {'type': 'file', 'purpose': ''}, 'label_approved.py': {'type': 'file', 'purpose': ''}, 'lint.sh': {'type': 'file', 'purpose': ''}, 'notify_translations.py': {'type': 'file', 'purpose': ''}, 'people.py': {'type': 'file', 'purpose': ''}, 'playwright': {'type': 'dir', 'purpose': '', 'children': {'cookie_param_models': {'type': 'dir', 'purpose': '', 'children': {'image01.py': {'type': 'file', 'purpose': ''}}}, 'header_param_models': {'type': 'dir', 'purpose': '', 'children': {'image01.py': {'type': 'file', 'purpose': ''}}}, 'json_base64_bytes': {'type': 'dir', 'purpose': '', 'children': {'image01.py': {'type': 'file', 'purpose': ''}}}, 'query_param_models': {'type': 'dir', 'purpose': '', 'children': {'image01.py': {'type': 'file', 'purpose': ''}}}, 'request_form_models': {'type': 'dir', 'purpose': '', 'children': {'image01.py': {'type': 'file', 'purpose': ''}}}, 'separate_openapi_schemas': {'type': 'dir', 'purpose': '', 'children': {'image01.py': {'type': 'file', 'purpose': ''}, 'image02.py': {'type': 'file', 'purpose': ''}, 'image03.py': {'type': 'file', 'purpose': ''}, 'image04.py': {'type': 'file', 'purpose': ''}, 'image05.py': {'type': 'file', 'purpose': ''}}}, 'sql_databases': {'type': 'dir', 'purpose': '', 'children': {'image01.py': {'type': 'file', 'purpose': ''}, 'image02.py': {'type': 'file', 'purpose': ''}}}}}, 'prepare_release.py': {'type': 'file', 'purpose': ''}, 'sponsors.py': {'type': 'file', 'purpose': ''}, 'test-cov-html.sh': {'type': 'file', 'purpose': ''}, 'test-cov.sh': {'type': 'file', 'purpose': ''}, 'test.sh': {'type': 'file', 'purpose': ''}, 'tests': {'type': 'dir', 'purpose': '', 'children': {'test_translation_fixer': {'type': 'dir', 'purpose': '', 'children': {'conftest.py': {'type': 'file', 'purpose': ''}, 'test_code_blocks': {'type': 'dir', 'purpose': '', 'children': {'data': {'type': 'dir', 'purpose': '', 'children': {'en_doc.md': {'type': 'file', 'purpose': ''}, 'translated_doc_lines_number_gt.md': {'type': 'file', 'purpose': ''}, 'translated_doc_lines_number_lt.md': {'type': 'file', 'purpose': ''}, 'translated_doc_mermaid_not_translated.md': {'type': 'file', 'purpose': ''}, 'translated_doc_mermaid_translated.md': {'type': 'file', 'purpose': ''}, 'translated_doc_number_gt.md': {'type': 'file', 'purpose': ''}, 'translated_doc_number_lt.md': {'type': 'file', 'purpose': ''}, 'translated_doc_wrong_lang_code.md': {'type': 'file', 'purpose': ''}, 'translated_doc_wrong_lang_code_2.md': {'type': 'file', 'purpose': ''}}}, 'test_code_blocks_lines_number_mismatch.py': {'type': 'file', 'purpose': ''}, 'test_code_blocks_mermaid.py': {'type': 'file', 'purpose': ''}, 'test_code_blocks_number_mismatch.py': {'type': 'file', 'purpose': ''}, 'test_code_blocks_wrong_lang_code.py': {'type': 'file', 'purpose': ''}}}, 'test_code_includes': {'type': 'dir', 'purpose': '', 'children': {'data': {'type': 'dir', 'purpose': '', 'children': {'en_doc.md': {'type': 'file', 'purpose': ''}, 'translated_doc_number_gt.md': {'type': 'file', 'purpose': ''}, 'translated_doc_number_lt.md': {'type': 'file', 'purpose': ''}}}, 'test_number_mismatch.py': {'type': 'file', 'purpose': ''}}}, 'test_complex_doc': {'type': 'dir', 'purpose': '', 'children': {'data': {'type': 'dir', 'purpose': '', 'children': {'en_doc.md': {'type': 'file', 'purpose': ''}, 'translated_doc.md': {'type': 'file', 'purpose': ''}, 'translated_doc_expected.md': {'type': 'file', 'purpose': ''}}}, 'test_compex_doc.py': {'type': 'file', 'purpose': ''}}}, 'test_header_permalinks': {'type': 'dir', 'purpose': '', 'children': {'data': {'type': 'dir', 'purpose': '', 'children': {'en_doc.md': {'type': 'file', 'purpose': ''}, 'translated_doc_level_mismatch_1.md': {'type': 'file', 'purpose': ''}, 'translated_doc_level_mismatch_2.md': {'type': 'file', 'purpose': ''}, 'translated_doc_number_gt.md': {'type': 'file', 'purpose': ''}, 'translated_doc_number_lt.md': {'type': 'file', 'purpose': ''}}}, 'test_header_level_mismatch.py': {'type': 'file', 'purpose': ''}, 'test_header_number_mismatch.py': {'type': 'file', 'purpose': ''}}}, 'test_html_links': {'type': 'dir', 'purpose': '', 'children': {'data': {'type': 'dir', 'purpose': '', 'children': {'en_doc.md': {'type': 'file', 'purpose': ''}, 'translated_doc_number_gt.md': {'type': 'file', 'purpose': ''}, 'translated_doc_number_lt.md': {'type': 'file', 'purpose': ''}}}, 'test_html_links_number_mismatch.py': {'type': 'file', 'purpose': ''}}}, 'test_markdown_links': {'type': 'dir', 'purpose': '', 'children': {'data': {'type': 'dir', 'purpose': '', 'children': {'en_doc.md': {'type': 'file', 'purpose': ''}, 'translated_doc.md': {'type': 'file', 'purpose': ''}, 'translated_doc_number_gt.md': {'type': 'file', 'purpose': ''}, 'translated_doc_number_lt.md': {'type': 'file', 'purpose': ''}}}, 'test_mkd_links_number_mismatch.py': {'type': 'file', 'purpose': ''}}}}}}}, 'topic_repos.py': {'type': 'file', 'purpose': ''}, 'translate.py': {'type': 'file', 'purpose': ''}, 'translation_fixer.py': {'type': 'file', 'purpose': ''}}}, 'tests': {'purpose': 'tests', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'benchmarks': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_general_performance.py': {'type': 'file', 'purpose': ''}}}, 'forward_reference_type.py': {'type': 'file', 'purpose': ''}, 'main.py': {'type': 'file', 'purpose': ''}, 'test_additional_properties.py': {'type': 'file', 'purpose': ''}, 'test_additional_properties_bool.py': {'type': 'file', 'purpose': ''}, 'test_additional_response_extra.py': {'type': 'file', 'purpose': ''}, 'test_additional_responses_bad.py': {'type': 'file', 'purpose': ''}, 'test_additional_responses_custom_model_in_callback.py': {'type': 'file', 'purpose': ''}, 'test_additional_responses_custom_validationerror.py': {'type': 'file', 'purpose': ''}, 'test_additional_responses_default_validationerror.py': {'type': 'file', 'purpose': ''}, 'test_additional_responses_response_class.py': {'type': 'file', 'purpose': ''}, 'test_additional_responses_router.py': {'type': 'file', 'purpose': ''}, 'test_additional_responses_union_duplicate_anyof.py': {'type': 'file', 'purpose': ''}, 'test_allow_inf_nan_in_enforcing.py': {'type': 'file', 'purpose': ''}, 'test_ambiguous_params.py': {'type': 'file', 'purpose': ''}, 'test_annotated.py': {'type': 'file', 'purpose': ''}, 'test_application.py': {'type': 'file', 'purpose': ''}, 'test_arbitrary_types.py': {'type': 'file', 'purpose': ''}, 'test_callable_endpoint.py': {'type': 'file', 'purpose': ''}, 'test_compat.py': {'type': 'file', 'purpose': ''}, 'test_computed_fields.py': {'type': 'file', 'purpose': ''}, 'test_custom_middleware_exception.py': {'type': 'file', 'purpose': ''}, 'test_custom_route_class.py': {'type': 'file', 'purpose': ''}, 'test_custom_schema_fields.py': {'type': 'file', 'purpose': ''}, 'test_custom_swagger_ui_redirect.py': {'type': 'file', 'purpose': ''}, 'test_datastructures.py': {'type': 'file', 'purpose': ''}, 'test_datetime_custom_encoder.py': {'type': 'file', 'purpose': ''}, 'test_default_response_class.py': {'type': 'file', 'purpose': ''}, 'test_default_response_class_router.py': {'type': 'file', 'purpose': ''}, 'test_dependencies_utils.py': {'type': 'file', 'purpose': ''}, 'test_dependency_after_yield_raise.py': {'type': 'file', 'purpose': ''}, 'test_dependency_after_yield_streaming.py': {'type': 'file', 'purpose': ''}, 'test_dependency_after_yield_websockets.py': {'type': 'file', 'purpose': ''}, 'test_dependency_cache.py': {'type': 'file', 'purpose': ''}, 'test_dependency_class.py': {'type': 'file', 'purpose': ''}, 'test_dependency_contextmanager.py': {'type': 'file', 'purpose': ''}, 'test_dependency_contextvars.py': {'type': 'file', 'purpose': ''}, 'test_dependency_duplicates.py': {'type': 'file', 'purpose': ''}, 'test_dependency_overrides.py': {'type': 'file', 'purpose': ''}, 'test_dependency_paramless.py': {'type': 'file', 'purpose': ''}, 'test_dependency_partial.py': {'type': 'file', 'purpose': ''}, 'test_dependency_pep695.py': {'type': 'file', 'purpose': ''}, 'test_dependency_security_overrides.py': {'type': 'file', 'purpose': ''}, 'test_dependency_wrapped.py': {'type': 'file', 'purpose': ''}, 'test_dependency_yield_except_httpexception.py': {'type': 'file', 'purpose': ''}, 'test_dependency_yield_scope.py': {'type': 'file', 'purpose': ''}, 'test_dependency_yield_scope_websockets.py': {'type': 'file', 'purpose': ''}, 'test_depends_hashable.py': {'type': 'file', 'purpose': ''}, 'test_deprecated_openapi_prefix.py': {'type': 'file', 'purpose': ''}, 'test_deprecated_responses.py': {'type': 'file', 'purpose': ''}, 'test_dump_json_fast_path.py': {'type': 'file', 'purpose': ''}, 'test_duplicate_models_openapi.py': {'type': 'file', 'purpose': ''}, 'test_empty_router.py': {'type': 'file', 'purpose': ''}, 'test_enforce_once_required_parameter.py': {'type': 'file', 'purpose': ''}, 'test_exception_handlers.py': {'type': 'file', 'purpose': ''}, 'test_extra_routes.py': {'type': 'file', 'purpose': ''}, 'test_fastapi_cli.py': {'type': 'file', 'purpose': ''}, 'test_file_and_form_order_issue_9116.py': {'type': 'file', 'purpose': ''}, 'test_filter_pydantic_sub_model_pv2.py': {'type': 'file', 'purpose': ''}, 'test_form_default.py': {'type': 'file', 'purpose': ''}, 'test_forms_from_non_typing_sequences.py': {'type': 'file', 'purpose': ''}, 'test_forms_single_model.py': {'type': 'file', 'purpose': ''}, 'test_forms_single_param.py': {'type': 'file', 'purpose': ''}, 'test_frontend.py': {'type': 'file', 'purpose': ''}, 'test_generate_unique_id_function.py': {'type': 'file', 'purpose': ''}, 'test_generic_parameterless_depends.py': {'type': 'file', 'purpose': ''}, 'test_get_model_definitions_formfeed_escape.py': {'type': 'file', 'purpose': ''}, 'test_get_request_body.py': {'type': 'file', 'purpose': ''}, 'test_http_connection_injection.py': {'type': 'file', 'purpose': ''}, 'test_include_route.py': {'type': 'file', 'purpose': ''}, 'test_include_router_defaults_overrides.py': {'type': 'file', 'purpose': ''}, 'test_infer_param_optionality.py': {'type': 'file', 'purpose': ''}, 'test_inherited_custom_class.py': {'type': 'file', 'purpose': ''}, 'test_invalid_path_param.py': {'type': 'file', 'purpose': ''}, 'test_invalid_sequence_param.py': {'type': 'file', 'purpose': ''}, 'test_json_type.py': {'type': 'file', 'purpose': ''}, 'test_jsonable_encoder.py': {'type': 'file', 'purpose': ''}, 'test_list_bytes_file_order_preserved_issue_14811.py': {'type': 'file', 'purpose': ''}, 'test_local_docs.py': {'type': 'file', 'purpose': ''}, 'test_modules_same_name_body': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'app': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'a.py': {'type': 'file', 'purpose': ''}, 'b.py': {'type': 'file', 'purpose': ''}, 'main.py': {'type': 'file', 'purpose': ''}}}, 'test_main.py': {'type': 'file', 'purpose': ''}}}, 'test_multi_body_errors.py': {'type': 'file', 'purpose': ''}, 'test_multi_query_errors.py': {'type': 'file', 'purpose': ''}, 'test_multipart_installation.py': {'type': 'file', 'purpose': ''}, 'test_no_schema_split.py': {'type': 'file', 'purpose': ''}, 'test_no_swagger_ui_redirect.py': {'type': 'file', 'purpose': ''}, 'test_openapi_cache_root_path.py': {'type': 'file', 'purpose': ''}, 'test_openapi_examples.py': {'type': 'file', 'purpose': ''}, 'test_openapi_model_description_trim_on_formfeed.py': {'type': 'file', 'purpose': ''}, 'test_openapi_query_parameter_extension.py': {'type': 'file', 'purpose': ''}, 'test_openapi_route_extensions.py': {'type': 'file', 'purpose': ''}, 'test_openapi_schema_type.py': {'type': 'file', 'purpose': ''}, 'test_openapi_separate_input_output_schemas.py': {'type': 'file', 'purpose': ''}, 'test_openapi_servers.py': {'type': 'file', 'purpose': ''}, 'test_operations_signatures.py': {'type': 'file', 'purpose': ''}, 'test_optional_file_list.py': {'type': 'file', 'purpose': ''}, 'test_orjson_response_class.py': {'type': 'file', 'purpose': ''}, 'test_param_class.py': {'type': 'file', 'purpose': ''}, 'test_param_in_path_and_dependency.py': {'type': 'file', 'purpose': ''}, 'test_param_include_in_schema.py': {'type': 'file', 'purpose': ''}, 'test_params_repr.py': {'type': 'file', 'purpose': ''}, 'test_path.py': {'type': 'file', 'purpose': ''}, 'test_prepare_release.py': {'type': 'file', 'purpose': ''}, 'test_put_no_body.py': {'type': 'file', 'purpose': ''}, 'test_pydantic_v1_error.py': {'type': 'file', 'purpose': ''}, 'test_pydanticv2_dataclasses_uuid_stringified_annotations.py': {'type': 'file', 'purpose': ''}, 'test_query.py': {'type': 'file', 'purpose': ''}, 'test_query_cookie_header_model_extra_params.py': {'type': 'file', 'purpose': ''}, 'test_read_with_orm_mode.py': {'type': 'file', 'purpose': ''}, 'test_regex_deprecated_body.py': {'type': 'file', 'purpose': ''}, 'test_regex_deprecated_params.py': {'type': 'file', 'purpose': ''}, 'test_repeated_cookie_headers.py': {'type': 'file', 'purpose': ''}, 'test_repeated_dependency_schema.py': {'type': 'file', 'purpose': ''}, 'test_repeated_parameter_alias.py': {'type': 'file', 'purpose': ''}, 'test_request_body_parameters_media_type.py': {'type': 'file', 'purpose': ''}, 'test_request_param_model_by_alias.py': {'type': 'file', 'purpose': ''}, 'test_request_params': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_body': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_list.py': {'type': 'file', 'purpose': ''}, 'test_optional_list.py': {'type': 'file', 'purpose': ''}, 'test_optional_str.py': {'type': 'file', 'purpose': ''}, 'test_required_str.py': {'type': 'file', 'purpose': ''}, 'utils.py': {'type': 'file', 'purpose': ''}}}, 'test_cookie': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_list.py': {'type': 'file', 'purpose': ''}, 'test_optional_list.py': {'type': 'file', 'purpose': ''}, 'test_optional_str.py': {'type': 'file', 'purpose': ''}, 'test_required_str.py': {'type': 'file', 'purpose': ''}}}, 'test_file': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_list.py': {'type': 'file', 'purpose': ''}, 'test_optional.py': {'type': 'file', 'purpose': ''}, 'test_optional_list.py': {'type': 'file', 'purpose': ''}, 'test_required.py': {'type': 'file', 'purpose': ''}, 'utils.py': {'type': 'file', 'purpose': ''}}}, 'test_form': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_list.py': {'type': 'file', 'purpose': ''}, 'test_optional_list.py': {'type': 'file', 'purpose': ''}, 'test_optional_str.py': {'type': 'file', 'purpose': ''}, 'test_required_str.py': {'type': 'file', 'purpose': ''}, 'utils.py': {'type': 'file', 'purpose': ''}}}, 'test_header': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_list.py': {'type': 'file', 'purpose': ''}, 'test_optional_list.py': {'type': 'file', 'purpose': ''}, 'test_optional_str.py': {'type': 'file', 'purpose': ''}, 'test_required_str.py': {'type': 'file', 'purpose': ''}}}, 'test_path': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_list.py': {'type': 'file', 'purpose': ''}, 'test_optional_list.py': {'type': 'file', 'purpose': ''}, 'test_optional_str.py': {'type': 'file', 'purpose': ''}, 'test_required_str.py': {'type': 'file', 'purpose': ''}}}, 'test_query': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_list.py': {'type': 'file', 'purpose': ''}, 'test_optional_list.py': {'type': 'file', 'purpose': ''}, 'test_optional_str.py': {'type': 'file', 'purpose': ''}, 'test_required_str.py': {'type': 'file', 'purpose': ''}}}}}, 'test_required_noneable.py': {'type': 'file', 'purpose': ''}, 'test_response_by_alias.py': {'type': 'file', 'purpose': ''}, 'test_response_change_status_code.py': {'type': 'file', 'purpose': ''}, 'test_response_class_no_mediatype.py': {'type': 'file', 'purpose': ''}, 'test_response_code_no_body.py': {'type': 'file', 'purpose': ''}, 'test_response_dependency.py': {'type': 'file', 'purpose': ''}, 'test_response_model_as_return_annotation.py': {'type': 'file', 'purpose': ''}, 'test_response_model_data_filter.py': {'type': 'file', 'purpose': ''}, 'test_response_model_data_filter_no_inheritance.py': {'type': 'file', 'purpose': ''}, 'test_response_model_default_factory.py': {'type': 'file', 'purpose': ''}, 'test_response_model_include_exclude.py': {'type': 'file', 'purpose': ''}, 'test_response_model_invalid.py': {'type': 'file', 'purpose': ''}, 'test_response_model_sub_types.py': {'type': 'file', 'purpose': ''}, 'test_response_set_response_code_empty.py': {'type': 'file', 'purpose': ''}, 'test_return_none_stringified_annotations.py': {'type': 'file', 'purpose': ''}, 'test_route_scope.py': {'type': 'file', 'purpose': ''}, 'test_router_circular_import.py': {'type': 'file', 'purpose': ''}, 'test_router_events.py': {'type': 'file', 'purpose': ''}, 'test_router_include_context.py': {'type': 'file', 'purpose': ''}, 'test_router_prefix_with_template.py': {'type': 'file', 'purpose': ''}, 'test_router_redirect_slashes.py': {'type': 'file', 'purpose': ''}, 'test_schema_compat_pydantic_v2.py': {'type': 'file', 'purpose': ''}, 'test_schema_extra_examples.py': {'type': 'file', 'purpose': ''}, 'test_schema_ref_pydantic_v2.py': {'type': 'file', 'purpose': ''}, 'test_security_api_key_cookie.py': {'type': 'file', 'purpose': ''}, 'test_security_api_key_cookie_description.py': {'type': 'file', 'purpose': ''}, 'test_security_api_key_cookie_optional.py': {'type': 'file', 'purpose': ''}, 'test_security_api_key_header.py': {'type': 'file', 'purpose': ''}, 'test_security_api_key_header_description.py': {'type': 'file', 'purpose': ''}, 'test_security_api_key_header_optional.py': {'type': 'file', 'purpose': ''}, 'test_security_api_key_query.py': {'type': 'file', 'purpose': ''}, 'test_security_api_key_query_description.py': {'type': 'file', 'purpose': ''}, 'test_security_api_key_query_optional.py': {'type': 'file', 'purpose': ''}, 'test_security_http_base.py': {'type': 'file', 'purpose': ''}, 'test_security_http_base_description.py': {'type': 'file', 'purpose': ''}, 'test_security_http_base_optional.py': {'type': 'file', 'purpose': ''}, 'test_security_http_basic_optional.py': {'type': 'file', 'purpose': ''}, 'test_security_http_basic_realm.py': {'type': 'file', 'purpose': ''}, 'test_security_http_basic_realm_description.py': {'type': 'file', 'purpose': ''}, 'test_security_http_bearer.py': {'type': 'file', 'purpose': ''}, 'test_security_http_bearer_description.py': {'type': 'file', 'purpose': ''}, 'test_security_http_bearer_optional.py': {'type': 'file', 'purpose': ''}, 'test_security_http_digest.py': {'type': 'file', 'purpose': ''}, 'test_security_http_digest_description.py': {'type': 'file', 'purpose': ''}, 'test_security_http_digest_optional.py': {'type': 'file', 'purpose': ''}, 'test_security_oauth2.py': {'type': 'file', 'purpose': ''}, 'test_security_oauth2_authorization_code_bearer.py': {'type': 'file', 'purpose': ''}, 'test_security_oauth2_authorization_code_bearer_description.py': {'type': 'file', 'purpose': ''}, 'test_security_oauth2_authorization_code_bearer_scopes_openapi.py': {'type': 'file', 'purpose': ''}, 'test_security_oauth2_authorization_code_bearer_scopes_openapi_simple.py': {'type': 'file', 'purpose': ''}, 'test_security_oauth2_optional.py': {'type': 'file', 'purpose': ''}, 'test_security_oauth2_optional_description.py': {'type': 'file', 'purpose': ''}, 'test_security_oauth2_password_bearer_optional.py': {'type': 'file', 'purpose': ''}, 'test_security_oauth2_password_bearer_optional_description.py': {'type': 'file', 'purpose': ''}, 'test_security_openid_connect.py': {'type': 'file', 'purpose': ''}, 'test_security_openid_connect_description.py': {'type': 'file', 'purpose': ''}, 'test_security_openid_connect_optional.py': {'type': 'file', 'purpose': ''}, 'test_security_scopes.py': {'type': 'file', 'purpose': ''}, 'test_security_scopes_dont_propagate.py': {'type': 'file', 'purpose': ''}, 'test_security_scopes_sub_dependency.py': {'type': 'file', 'purpose': ''}, 'test_serialize_response.py': {'type': 'file', 'purpose': ''}, 'test_serialize_response_dataclass.py': {'type': 'file', 'purpose': ''}, 'test_serialize_response_model.py': {'type': 'file', 'purpose': ''}, 'test_skip_defaults.py': {'type': 'file', 'purpose': ''}, 'test_sse.py': {'type': 'file', 'purpose': ''}, 'test_starlette_exception.py': {'type': 'file', 'purpose': ''}, 'test_starlette_urlconvertors.py': {'type': 'file', 'purpose': ''}, 'test_stream_bare_type.py': {'type': 'file', 'purpose': ''}, 'test_stream_cancellation.py': {'type': 'file', 'purpose': ''}, 'test_stream_json_validation_error.py': {'type': 'file', 'purpose': ''}, 'test_strict_content_type_app_level.py': {'type': 'file', 'purpose': ''}, 'test_strict_content_type_nested.py': {'type': 'file', 'purpose': ''}, 'test_strict_content_type_router_level.py': {'type': 'file', 'purpose': ''}, 'test_stringified_annotation_dependency.py': {'type': 'file', 'purpose': ''}, 'test_stringified_annotation_dependency_py314.py': {'type': 'file', 'purpose': ''}, 'test_stringified_annotations_simple.py': {'type': 'file', 'purpose': ''}, 'test_sub_callbacks.py': {'type': 'file', 'purpose': ''}, 'test_swagger_ui_escape.py': {'type': 'file', 'purpose': ''}, 'test_swagger_ui_init_oauth.py': {'type': 'file', 'purpose': ''}, 'test_top_level_security_scheme_in_openapi.py': {'type': 'file', 'purpose': ''}, 'test_tuples.py': {'type': 'file', 'purpose': ''}, 'test_tutorial': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_additional_responses': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}}}, 'test_additional_status_codes': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_advanced_middleware': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}}}, 'test_async_tests': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_main_a.py': {'type': 'file', 'purpose': ''}}}, 'test_authentication_error_status_code': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_background_tasks': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}}}, 'test_behind_a_proxy': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001_01.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}}}, 'test_bigger_applications': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_main.py': {'type': 'file', 'purpose': ''}}}, 'test_body': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}}}, 'test_body_fields': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_body_multiple_params': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}, 'test_tutorial005.py': {'type': 'file', 'purpose': ''}}}, 'test_body_nested_models': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001_tutorial002_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}, 'test_tutorial005.py': {'type': 'file', 'purpose': ''}, 'test_tutorial006.py': {'type': 'file', 'purpose': ''}, 'test_tutorial007.py': {'type': 'file', 'purpose': ''}, 'test_tutorial008.py': {'type': 'file', 'purpose': ''}, 'test_tutorial009.py': {'type': 'file', 'purpose': ''}}}, 'test_body_updates': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}}}, 'test_conditional_openapi': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_configure_swagger_ui': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}}}, 'test_cookie_param_models': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}}}, 'test_cookie_params': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_cors': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_custom_docs_ui': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}}}, 'test_custom_request_and_route': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}}}, 'test_custom_response': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001b.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002_tutorial003_tutorial004.py': {'type': 'file', 'purpose': ''}, 'test_tutorial005.py': {'type': 'file', 'purpose': ''}, 'test_tutorial006.py': {'type': 'file', 'purpose': ''}, 'test_tutorial006b.py': {'type': 'file', 'purpose': ''}, 'test_tutorial006c.py': {'type': 'file', 'purpose': ''}, 'test_tutorial007.py': {'type': 'file', 'purpose': ''}, 'test_tutorial008.py': {'type': 'file', 'purpose': ''}, 'test_tutorial009.py': {'type': 'file', 'purpose': ''}, 'test_tutorial009b.py': {'type': 'file', 'purpose': ''}, 'test_tutorial009c.py': {'type': 'file', 'purpose': ''}, 'test_tutorial010.py': {'type': 'file', 'purpose': ''}}}, 'test_dataclasses': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}}}, 'test_debugging': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_dependencies': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001_tutorial001_02.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002_tutorial003_tutorial004.py': {'type': 'file', 'purpose': ''}, 'test_tutorial005.py': {'type': 'file', 'purpose': ''}, 'test_tutorial006.py': {'type': 'file', 'purpose': ''}, 'test_tutorial007.py': {'type': 'file', 'purpose': ''}, 'test_tutorial008.py': {'type': 'file', 'purpose': ''}, 'test_tutorial008b.py': {'type': 'file', 'purpose': ''}, 'test_tutorial008c.py': {'type': 'file', 'purpose': ''}, 'test_tutorial008d.py': {'type': 'file', 'purpose': ''}, 'test_tutorial008e.py': {'type': 'file', 'purpose': ''}, 'test_tutorial010.py': {'type': 'file', 'purpose': ''}, 'test_tutorial011.py': {'type': 'file', 'purpose': ''}, 'test_tutorial012.py': {'type': 'file', 'purpose': ''}}}, 'test_encoder': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_events': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}}}, 'test_extending_openapi': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_extra_data_types': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_extra_models': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}, 'test_tutorial005.py': {'type': 'file', 'purpose': ''}}}, 'test_first_steps': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001_tutorial002_tutorial003.py': {'type': 'file', 'purpose': ''}}}, 'test_generate_clients': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}}}, 'test_graphql': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_handling_errors': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}, 'test_tutorial005.py': {'type': 'file', 'purpose': ''}, 'test_tutorial006.py': {'type': 'file', 'purpose': ''}}}, 'test_header_param_models': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}}}, 'test_header_params': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}}}, 'test_json_base64_bytes': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_metadata': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001_1.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}}}, 'test_middleware': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_openapi_callbacks': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_openapi_webhooks': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_path_operation_advanced_configurations': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}, 'test_tutorial005.py': {'type': 'file', 'purpose': ''}, 'test_tutorial006.py': {'type': 'file', 'purpose': ''}, 'test_tutorial007.py': {'type': 'file', 'purpose': ''}}}, 'test_path_operation_configurations': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002b.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003_tutorial004.py': {'type': 'file', 'purpose': ''}, 'test_tutorial005.py': {'type': 'file', 'purpose': ''}, 'test_tutorial006.py': {'type': 'file', 'purpose': ''}}}, 'test_path_params': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003b.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}, 'test_tutorial005.py': {'type': 'file', 'purpose': ''}}}, 'test_path_params_numeric_validations': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}, 'test_tutorial005.py': {'type': 'file', 'purpose': ''}, 'test_tutorial006.py': {'type': 'file', 'purpose': ''}}}, 'test_python_types': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}, 'test_tutorial005.py': {'type': 'file', 'purpose': ''}, 'test_tutorial006.py': {'type': 'file', 'purpose': ''}, 'test_tutorial007.py': {'type': 'file', 'purpose': ''}, 'test_tutorial008.py': {'type': 'file', 'purpose': ''}, 'test_tutorial008b.py': {'type': 'file', 'purpose': ''}, 'test_tutorial009_tutorial009b.py': {'type': 'file', 'purpose': ''}, 'test_tutorial010.py': {'type': 'file', 'purpose': ''}, 'test_tutorial011.py': {'type': 'file', 'purpose': ''}, 'test_tutorial013.py': {'type': 'file', 'purpose': ''}}}, 'test_query_param_models': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}}}, 'test_query_params': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}, 'test_tutorial005.py': {'type': 'file', 'purpose': ''}, 'test_tutorial006.py': {'type': 'file', 'purpose': ''}}}, 'test_query_params_str_validations': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}, 'test_tutorial005.py': {'type': 'file', 'purpose': ''}, 'test_tutorial006.py': {'type': 'file', 'purpose': ''}, 'test_tutorial006c.py': {'type': 'file', 'purpose': ''}, 'test_tutorial007.py': {'type': 'file', 'purpose': ''}, 'test_tutorial008.py': {'type': 'file', 'purpose': ''}, 'test_tutorial009.py': {'type': 'file', 'purpose': ''}, 'test_tutorial010.py': {'type': 'file', 'purpose': ''}, 'test_tutorial011.py': {'type': 'file', 'purpose': ''}, 'test_tutorial012.py': {'type': 'file', 'purpose': ''}, 'test_tutorial013.py': {'type': 'file', 'purpose': ''}, 'test_tutorial014.py': {'type': 'file', 'purpose': ''}, 'test_tutorial015.py': {'type': 'file', 'purpose': ''}}}, 'test_request_files': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001_02.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001_03.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}}}, 'test_request_form_models': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}}}, 'test_request_forms': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_request_forms_and_files': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_response_change_status_code': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_response_cookies': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}}}, 'test_response_directly': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}}}, 'test_response_headers': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}}}, 'test_response_model': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001_tutorial001_01.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003_01.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003_02.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003_03.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003_04.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003_05.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}, 'test_tutorial005.py': {'type': 'file', 'purpose': ''}, 'test_tutorial006.py': {'type': 'file', 'purpose': ''}}}, 'test_response_status_code': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001_tutorial002.py': {'type': 'file', 'purpose': ''}}}, 'test_schema_extra_example': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}, 'test_tutorial005.py': {'type': 'file', 'purpose': ''}}}, 'test_security': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}, 'test_tutorial005.py': {'type': 'file', 'purpose': ''}, 'test_tutorial006.py': {'type': 'file', 'purpose': ''}, 'test_tutorial007.py': {'type': 'file', 'purpose': ''}}}, 'test_separate_openapi_schemas': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}}}, 'test_server_sent_events': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}, 'test_tutorial005.py': {'type': 'file', 'purpose': ''}}}, 'test_settings': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_app01.py': {'type': 'file', 'purpose': ''}, 'test_app02.py': {'type': 'file', 'purpose': ''}, 'test_app03.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_sql_databases': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}}}, 'test_static_files': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_stream_data': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}}}, 'test_stream_json_lines': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_strict_content_type': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_sub_applications': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_templates': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_testing': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_main_a.py': {'type': 'file', 'purpose': ''}, 'test_main_b.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}, 'test_tutorial004.py': {'type': 'file', 'purpose': ''}}}, 'test_testing_dependencies': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_using_request_directly': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}, 'test_websockets': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}, 'test_tutorial002.py': {'type': 'file', 'purpose': ''}, 'test_tutorial003.py': {'type': 'file', 'purpose': ''}}}, 'test_wsgi': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'test_tutorial001.py': {'type': 'file', 'purpose': ''}}}}}, 'test_typing_python39.py': {'type': 'file', 'purpose': ''}, 'test_union_body.py': {'type': 'file', 'purpose': ''}, 'test_union_body_discriminator.py': {'type': 'file', 'purpose': ''}, 'test_union_body_discriminator_annotated.py': {'type': 'file', 'purpose': ''}, 'test_union_forms.py': {'type': 'file', 'purpose': ''}, 'test_union_inherited_body.py': {'type': 'file', 'purpose': ''}, 'test_validate_response.py': {'type': 'file', 'purpose': ''}, 'test_validate_response_dataclass.py': {'type': 'file', 'purpose': ''}, 'test_validate_response_recursive': {'type': 'dir', 'purpose': '', 'children': {'__init__.py': {'type': 'file', 'purpose': ''}, 'app.py': {'type': 'file', 'purpose': ''}, 'test_validate_response_recursive.py': {'type': 'file', 'purpose': ''}}}, 'test_validation_error_context.py': {'type': 'file', 'purpose': ''}, 'test_webhooks_security.py': {'type': 'file', 'purpose': ''}, 'test_wrapped_method_forward_reference.py': {'type': 'file', 'purpose': ''}, 'test_ws_dependencies.py': {'type': 'file', 'purpose': ''}, 'test_ws_router.py': {'type': 'file', 'purpose': ''}, 'utils.py': {'type': 'file', 'purpose': ''}}}}`
- project_description: `FastAPI framework, high performance, easy to learn, fast to code, ready for production`

---

### Runtime prerequisites

**ID:** `generic.conventions.runtime_prerequisites`  
**Category:** environment  
**Language:** generic  
**Confidence:** 90%

Runtime prerequisites: python 3.11.

**Statistics:**

- tools: `[{'name': 'python', 'version': '3.11', 'source': '.python-version'}]`

---

### API routes

**ID:** `python.conventions.api_routes`  
**Category:** api  
**Language:** python  
**Confidence:** 90%

29 API routes detected. Methods: DELETE: 2, GET: 16, PATCH: 2, POST: 7, PUT: 2.

**Statistics:**

- routes: `[{'method': 'GET', 'path': '/users/', 'file': 'fastapi/applications.py', 'line': 229}, {'method': 'GET', 'path': '/items/', 'file': 'fastapi/applications.py', 'line': 230}, {'method': 'GET', 'path': '/items/', 'file': 'fastapi/applications.py', 'line': 387}, {'method': 'GET', 'path': '/items/', 'file': 'fastapi/applications.py', 'line': 1982}, {'method': 'PUT', 'path': '/items/{item_id}', 'file': 'fastapi/applications.py', 'line': 2360}, {'method': 'POST', 'path': '/items/', 'file': 'fastapi/applications.py', 'line': 2738}, {'method': 'DELETE', 'path': '/items/{item_id}', 'file': 'fastapi/applications.py', 'line': 3111}, {'method': 'PATCH', 'path': '/items/', 'file': 'fastapi/applications.py', 'line': 4235}, {'method': 'POST', 'path': '/send-notification/{email}', 'file': 'fastapi/background.py', 'line': 33}, {'method': 'GET', 'path': '/users/', 'file': 'fastapi/routing.py', 'line': 2079}, {'method': 'GET', 'path': '/items/', 'file': 'fastapi/routing.py', 'line': 3449}, {'method': 'PUT', 'path': '/items/{item_id}', 'file': 'fastapi/routing.py', 'line': 3831}, {'method': 'POST', 'path': '/items/', 'file': 'fastapi/routing.py', 'line': 4213}, {'method': 'DELETE', 'path': '/items/{item_id}', 'file': 'fastapi/routing.py', 'line': 4590}, {'method': 'PATCH', 'path': '/items/', 'file': 'fastapi/routing.py', 'line': 5731}, {'method': 'GET', 'path': '/items/{item_id}', 'file': 'fastapi/exceptions.py', 'line': 37}, {'method': 'GET', 'path': '/items/{item_id}', 'file': 'fastapi/param_functions.py', 'line': 317}, {'method': 'GET', 'path': '/items/', 'file': 'fastapi/param_functions.py', 'line': 2364}, {'method': 'GET', 'path': '/users/me/items/', 'file': 'fastapi/param_functions.py', 'line': 2453}, {'method': 'POST', 'path': '/files/', 'file': 'fastapi/datastructures.py', 'line': 44}, {'method': 'POST', 'path': '/uploadfile/', 'file': 'fastapi/datastructures.py', 'line': 49}, {'method': 'POST', 'path': '/login', 'file': 'fastapi/security/oauth2.py', 'line': 39}, {'method': 'POST', 'path': '/login', 'file': 'fastapi/security/oauth2.py', 'line': 193}, {'method': 'GET', 'path': '/items/', 'file': 'fastapi/security/api_key.py', 'line': 81}, {'method': 'GET', 'path': '/items/', 'file': 'fastapi/security/api_key.py', 'line': 173}, {'method': 'GET', 'path': '/items/', 'file': 'fastapi/security/api_key.py', 'line': 261}, {'method': 'GET', 'path': '/users/me', 'file': 'fastapi/security/http.py', 'line': 134}, {'method': 'GET', 'path': '/users/me', 'file': 'fastapi/security/http.py', 'line': 246}, {'method': 'GET', 'path': '/users/me', 'file': 'fastapi/security/http.py', 'line': 349}]`
- total_routes: `29`
- methods: `{'GET': 16, 'PUT': 2, 'POST': 7, 'DELETE': 2, 'PATCH': 2}`
- path_prefixes: `['/items', '/items/{item_id}', '/users/me', '/users', '/login']`

---

### CLI framework: Typer

**ID:** `python.conventions.cli_framework`  
**Category:** cli  
**Language:** python  
**Confidence:** 90%
  
**Documentation:** [https://typer.tiangolo.com/](https://typer.tiangolo.com/)

Uses Typer for CLI.

**Statistics:**

- frameworks: `['typer']`
- primary_framework: `typer`
- framework_details: `{'typer': {'name': 'Typer', 'import_count': 16}}`

**Evidence:**

1. `tests/test_prepare_release.py:2-8`

```
from pathlib import Path

import pytest
from typer.testing import CliRunner

from scripts.prepare_release import (
    RELEASE_NOTES_HEADER,
```

2. `scripts/translate.py:8-14`

```
from typing import Annotated

import git
import typer
import yaml
from doc_parsing_utils import check_translation
from github import Github
```

3. `scripts/translation_fixer.py:3-9`

```
from pathlib import Path
from typing import Annotated

import typer

from scripts.doc_parsing_utils import check_translation

```

---

### Context manager usage

**ID:** `python.conventions.context_managers`  
**Category:** resource_management  
**Language:** python  
**Confidence:** 90%
  
**Documentation:** [https://docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html)

Uses context managers for resource management. 33 with statements (22 sync, 11 async). Types: file_io (4).

**Statistics:**

- total_with_statements: `33`
- sync_count: `22`
- async_count: `11`
- context_types: `{'file_io': 4}`

**Evidence:**

1. `scripts/docs.py:853-859`

```
    in_code_block4 = False
    permalinks = set()

    with path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
```

2. `scripts/docs.py:893-899`

```

        updated_lines.append(line)

    with path.open("w", encoding="utf-8") as f:
        f.writelines(updated_lines)


```

3. `scripts/add_latest_release_date.py:9-15`

```


def main() -> None:
    with open(RELEASE_NOTES_FILE) as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
```

---

### Data class style: Pydantic for API + dataclasses for internal

**ID:** `python.conventions.data_class_style`  
**Category:** api  
**Language:** python  
**Confidence:** 90%
  
**Documentation:** [https://docs.pydantic.dev/](https://docs.pydantic.dev/)

Uses Pydantic for API schemas (63) and dataclasses for internal DTOs (10). Good separation.

**Statistics:**

- primary_style: `pydantic`
- style_counts: `{'dataclass': 10, 'pydantic': 63}`
- has_validation: `True`

**Evidence:**

1. `fastapi/sse.py:47-57`

```
    if v is not None and "\0" in v:
        raise ValueError("SSE 'id' must not contain null characters")
    return _check_single_line(v, "id")


class ServerSentEvent(BaseModel):
    """Represents a single Server-Sent Event.

    When `yield`ed from a *path operation function* that uses
    `response_class=EventSourceResponse`, each `ServerSentEvent` is encoded
```

2. `fastapi/security/http.py:11-21`

```
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED


class HTTPBasicCredentials(BaseModel):
    """
    The HTTP Basic credentials given as the result of using `HTTPBasic` in a
    dependency.

```

3. `fastapi/security/http.py:24-34`

```

    username: Annotated[str, Doc("The HTTP Basic username.")]
    password: Annotated[str, Doc("The HTTP Basic password.")]


class HTTPAuthorizationCredentials(BaseModel):
    """
    The HTTP authorization credentials in the result of using `HTTPBearer` or
    `HTTPDigest` in a dependency.

```

---

### Caching decorator pattern

**ID:** `python.conventions.decorator_caching`  
**Category:** decorators  
**Language:** python  
**Confidence:** 90%
  
**Documentation:** [https://docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html)

Uses caching decorators for memoization. Found 12 usages.

**Statistics:**

- usage_count: `12`
- top_decorator: `cached_property`
- category: `caching`

**Evidence:**

1. `fastapi/dependencies/models.py:48-58`

```
    parent_oauth_scopes: list[str] | None = None
    use_cache: bool = True
    path: str | None = None
    scope: Literal["function", "request"] | None = None

    @cached_property
    def oauth_scopes(self) -> list[str]:
        scopes = self.parent_oauth_scopes.copy() if self.parent_oauth_scopes else []
        # This doesn't use a set to preserve order, just in case
        for scope in self.own_oauth_scopes or []:
```

2. `fastapi/dependencies/models.py:57-67`

```
        for scope in self.own_oauth_scopes or []:
            if scope not in scopes:
                scopes.append(scope)
        return scopes

    @cached_property
    def cache_key(self) -> DependencyCacheKey:
        scopes_for_cache = (
            tuple(sorted(set(self.oauth_scopes or []))) if self._uses_scopes else ()
        )
```

3. `fastapi/dependencies/models.py:68-78`

```
            self.call,
            scopes_for_cache,
            self.computed_scope or "",
        )

    @cached_property
    def _uses_scopes(self) -> bool:
        if self.own_oauth_scopes:
            return True
        if self.security_scopes_param_name is not None:
```

---

### JSON library: mixed

**ID:** `python.conventions.json_library`  
**Category:** serialization  
**Language:** python  
**Confidence:** 90%
  
**Documentation:** [https://docs.python.org/3/library/json.html](https://docs.python.org/3/library/json.html)

Uses both stdlib json and orjson. Consider standardizing on orjson.

**Statistics:**

- json_library_counts: `{'json': 43, 'orjson': 2, 'ujson': 2}`
- primary_library: `json`
- total_usages: `47`

**Evidence:**

1. `fastapi/routing.py:4-10`

```
import errno
import functools
import inspect
import json
import os
import stat
import types
```

2. `fastapi/openapi/docs.py:1-4`

```
import json
from typing import Annotated, Any

from annotated_doc import Doc
```

3. `scripts/translate.py:1-4`

```
import json
import secrets
import subprocess
from collections.abc import Iterable
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

### Import dependency graph

**ID:** `python.data_flow.import_graph`  
**Category:** data_flow  
**Language:** python  
**Confidence:** 90%

Import graph: 668 files, 1012 internal imports. 3 dependency clusters. Circular dependencies: 20. fastapi/__init__.py -> fastapi/applications.py; fastapi/_compat/__init__.py -> fastapi/_compat/v2.py; fastapi/routing.py -> fastapi/utils.py. Most imported: fastapi/testclient.py (436 dependents).

**Statistics:**

- total_files: `668`
- total_edges: `1012`
- cycle_count: `20`
- cluster_count: `3`
- top_fan_in: `[('fastapi/testclient.py', 436), ('fastapi/__init__.py', 239), ('fastapi/exceptions.py', 35), ('tests/utils.py', 34), ('fastapi/security/__init__.py', 34)]`
- top_fan_out: `[('fastapi/openapi/utils.py', 14), ('fastapi/applications.py', 11), ('fastapi/routing.py', 10), ('fastapi/dependencies/utils.py', 10), ('fastapi/__init__.py', 9)]`

**Evidence:**

1. `fastapi/testclient.py:1-1`

```
from starlette.testclient import TestClient as TestClient  # noqa
```

2. `fastapi/__init__.py:1-4`

```
"""FastAPI framework, high performance, easy to learn, fast to code, ready for production"""

__version__ = "0.138.1"

```

3. `fastapi/exceptions.py:1-4`

```
from collections.abc import Mapping, Sequence
from typing import Annotated, Any, TypedDict

from annotated_doc import Doc
```

---

### pytest fixtures for test setup

**ID:** `python.test_conventions.fixtures`  
**Category:** testing  
**Language:** python  
**Confidence:** 90%
  
**Documentation:** [https://docs.pytest.org/](https://docs.pytest.org/)

Uses pytest @fixture decorator for test setup. Found 199 fixtures. Uses 1 conftest.py file(s) for shared fixtures.

**Statistics:**

- fixture_counts: `{'pytest_fixture': 199}`
- conftest_files: `1`
- pattern: `pytest_fixture`

**Evidence:**

1. `tests/test_union_body_discriminator_annotated.py:7-17`

```
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel


@pytest.fixture(name="client")
def client_fixture() -> TestClient:
    from fastapi import Body
    from pydantic import Discriminator, Tag

```

2. `tests/test_computed_fields.py:2-12`

```
from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


@pytest.fixture(name="client")
def get_client(request):
    separate_input_output_schemas = request.param
    app = FastAPI(separate_input_output_schemas=separate_input_output_schemas)

```

3. `tests/test_schema_ref_pydantic_v2.py:5-15`

```
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, ConfigDict, Field


@pytest.fixture(name="client")
def get_client():
    app = FastAPI()

    class ModelWithRef(BaseModel):
```

---

### Mocking with pytest monkeypatch fixture

**ID:** `python.test_conventions.mocking`  
**Category:** testing  
**Language:** python  
**Confidence:** 90%
  
**Documentation:** [https://docs.python.org/3/library/unittest.mock.html](https://docs.python.org/3/library/unittest.mock.html)

Uses pytest monkeypatch fixture for test mocking. Found 14 usages. Also uses: unittest.mock / Mock, @patch decorator.

**Statistics:**

- mock_counts: `{'monkeypatch': 14, 'unittest_mock': 14, 'patch_decorator': 1}`
- primary_pattern: `monkeypatch`

**Evidence:**

1. `tests/test_frontend.py:15-25`

```
def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def test_frontend_exact_prefix_path_serves_index(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app")
    app = FastAPI()
    app.frontend("/app", directory=dist)
```

2. `tests/test_prepare_release.py:27-37`

```
        ("0.136.3", "major", "1.0.0"),
        ("0.136.3", "minor", "0.137.0"),
        ("0.136.3", "patch", "0.136.4"),
    ],
)
def test_bump_version(current_version: str, bump: BumpType, new_version: str) -> None:
    assert bump_version(current_version, bump) == new_version


def test_update_version_file() -> None:
```

3. `tests/test_sse.py:103-113`

```
def client_fixture():
    with TestClient(app) as c:
        yield c


def test_async_generator_with_model(client: TestClient):
    response = client.get("/items/stream")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    assert response.headers["cache-control"] == "no-cache"
```

---

### Parametrized tests

**ID:** `python.test_conventions.parametrized`  
**Category:** testing  
**Language:** python  
**Confidence:** 90%
  
**Documentation:** [https://docs.pytest.org/](https://docs.pytest.org/)

Uses @pytest.mark.parametrize for data-driven tests. Found 453 parametrized test functions.

**Statistics:**

- parametrize_count: `453`

**Evidence:**

1. `tests/test_computed_fields.py:30-40`

```

    client = TestClient(app)
    return client


@pytest.mark.parametrize("client", [True, False], indirect=True)
@pytest.mark.parametrize("path", ["/", "/responses"])
def test_get(client: TestClient, path: str):
    response = client.get(path)
    assert response.status_code == 200, response.text
```

2. `tests/test_computed_fields.py:31-41`

```
    client = TestClient(app)
    return client


@pytest.mark.parametrize("client", [True, False], indirect=True)
@pytest.mark.parametrize("path", ["/", "/responses"])
def test_get(client: TestClient, path: str):
    response = client.get(path)
    assert response.status_code == 200, response.text
    assert response.json() == {"width": 3, "length": 4, "area": 12}
```

3. `tests/test_computed_fields.py:38-48`

```
    response = client.get(path)
    assert response.status_code == 200, response.text
    assert response.json() == {"width": 3, "length": 4, "area": 12}


@pytest.mark.parametrize("client", [True, False], indirect=True)
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
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

### Uses Python standard logging

**ID:** `python.conventions.logging_library`  
**Category:** logging  
**Language:** python  
**Confidence:** 90%
  
**Documentation:** [https://docs.python.org/3/library/logging.html](https://docs.python.org/3/library/logging.html)

Exclusively uses Python standard logging for logging. Found 10 usages.

**Statistics:**

- library_counts: `{'stdlib_logging': 10}`
- primary_library: `stdlib_logging`
- primary_ratio: `1.0`

**Evidence:**

1. `fastapi/logger.py:1-3`

```
import logging

logger = logging.getLogger("fastapi")
```

2. `scripts/contributors.py:1-4`

```
import logging
import secrets
import subprocess
from collections import Counter
```

3. `scripts/label_approved.py:1-4`

```
import logging
from typing import Literal

from github import Github
```

---

### Plain assert statements

**ID:** `python.test_conventions.assertions`  
**Category:** testing  
**Language:** python  
**Confidence:** 89%
  
**Documentation:** [https://docs.pytest.org/](https://docs.pytest.org/)

Uses plain Python assert statements for test assertions. 4592 assert statements. Uses pytest.raises for exception testing (121 usages).

**Statistics:**

- assertion_counts: `{'plain_assert': 4592, 'pytest_raises': 121, 'pytest_warns': 17}`
- style: `plain_assert`

**Evidence:**

1. `tests/test_datastructures.py:9-15`

```


def test_upload_file_invalid_pydantic_v2():
    with pytest.raises(ValueError):
        UploadFile._validate("not a Starlette UploadFile", {})


```

2. `tests/test_openapi_schema_type.py:20-24`

```

def test_invalid_type_value() -> None:
    """Test that Schema raises ValueError for invalid type values."""
    with pytest.raises(ValueError, match="2 validation errors for Schema"):
        Schema(type=True)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
```

3. `tests/test_response_model_invalid.py:8-14`

```


def test_invalid_response_model_raises():
    with pytest.raises(FastAPIError):
        app = FastAPI()

        @app.get("/", response_model=NonPydanticModel)
```

---

### Config access patterns

**ID:** `generic.conventions.config_access`  
**Category:** configuration  
**Language:** generic  
**Confidence:** 88%

Config access: 2 direct env accesses; libraries: pydantic_settings.

**Statistics:**

- access_style: `library (pydantic_settings)`
- env_access_counts: `{'python_os_environ': 2}`
- libraries: `{'pydantic_settings': 21}`
- secrets_managers: `{}`
- total_env_accesses: `2`

---

### URL-based API versioning

**ID:** `python.conventions.api_versioning`  
**Category:** api  
**Language:** python  
**Confidence:** 85%
  
**Documentation:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

Uses URL path versioning (e.g., /v1/, /api/v2/). Found 2 versioned routes.

**Statistics:**

- versioning_patterns: `{'url_versioning': 2, 'header_versioning': 5, 'router_prefix': 15}`
- primary_pattern: `url_versioning`

**Evidence:**

1. `fastapi/applications.py:214-220`

```
                ```python
                from fastapi import FastAPI

                app = FastAPI(openapi_url="/api/v1/openapi.json")
                ```
                """
            ),
```

2. `fastapi/applications.py:652-658`

```
                ```python
                from fastapi import FastAPI

                app = FastAPI(root_path="/api/v1")
                ```
                """
            ),
```

3. `fastapi/applications.py:890-896`

```
        self.separate_input_output_schemas = separate_input_output_schemas
        self.openapi_external_docs = openapi_external_docs
        self.extra = extra
        self.openapi_version: Annotated[
            str,
            Doc(
                """
```

---

### Async HTTP client: httpx (recommended)

**ID:** `python.conventions.async_http_client`  
**Category:** async  
**Language:** python  
**Confidence:** 85%

Uses httpx for HTTP requests.

**Statistics:**

- http_client_counts: `{'requests': 1, 'httpx': 11}`
- primary_client: `httpx`
- quality: `excellent`

**Evidence:**

1. `scripts/contributors.py:6-12`

```
from pathlib import Path
from typing import Any

import httpx
import yaml
from github import Github
from pydantic import BaseModel, SecretStr
```

2. `scripts/notify_translations.py:5-11`

```
from pathlib import Path
from typing import Any, cast

import httpx
from github import Github
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings
```

3. `scripts/sponsors.py:5-11`

```
from pathlib import Path
from typing import Any

import httpx
import yaml
from github import Github
from pydantic import BaseModel, SecretStr
```

---

### OAuth2 authentication

**ID:** `python.conventions.auth_pattern`  
**Category:** security  
**Language:** python  
**Confidence:** 85%
  
**Documentation:** [https://pyjwt.readthedocs.io/](https://pyjwt.readthedocs.io/)

Uses OAuth2 for authentication. OAuth2 usages: 13.

**Statistics:**

- oauth2: `13`
- dependency_auth: `23`

**Evidence:**

1. `tests/test_dependency_paramless.py:1-9`

```
from typing import Annotated

from fastapi import FastAPI, HTTPException, Security
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)
from fastapi.testclient import TestClient

```

2. `tests/test_security_oauth2_password_bearer_optional_description.py:1-7`

```
from fastapi import FastAPI, Security
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

app = FastAPI()

```

3. `tests/test_dependency_paramless.py:1-9`

```
from typing import Annotated

from fastapi import FastAPI, HTTPException, Security
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)
from fastapi.testclient import TestClient

```

---

### FastAPI-style session dependency injection

**ID:** `python.conventions.db_session_lifecycle`  
**Category:** database  
**Language:** python  
**Confidence:** 85%
  
**Documentation:** [https://docs.sqlalchemy.org/](https://docs.sqlalchemy.org/)

Uses get_db() dependency pattern with Depends() for session lifecycle. Found 1 get_db definitions.

**Statistics:**

- get_db: `1`
- Depends_injection: `202`

**Evidence:**

1. `tests/test_security_scopes.py:10-20`

```
    return {"count": 0}


@pytest.fixture(name="app")
def app_fixture(call_counter: dict[str, int]):
    def get_db():
        call_counter["count"] += 1
        return f"db_{call_counter['count']}"

    def get_user(db: Annotated[str, Depends(get_db)]):
```

---

### Dependency health

**ID:** `python.conventions.dependency_health`  
**Category:** dependencies  
**Language:** python  
**Confidence:** 85%

Dependency health: 5 deps; pinning: minimum (5/5); lock file present.

**Statistics:**

- total_deps: `5`
- exact_count: `0`
- compatible_count: `0`
- minimum_count: `5`
- unpinned_count: `0`
- pinning_strategy: `minimum`
- has_lock_file: `True`

---

### Environment separation: Pydantic Settings

**ID:** `python.conventions.env_separation`  
**Category:** security  
**Language:** python  
**Confidence:** 85%
  
**Documentation:** [https://docs.pydantic.dev/latest/concepts/pydantic_settings/](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

Uses Pydantic Settings for structured configuration.

**Statistics:**

- approach: `pydantic_settings`
- has_env_files: `False`
- raw_environ_count: `0`

**Evidence:**

1. `scripts/contributors.py:10-16`

```
import yaml
from github import Github
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings

github_graphql_url = "https://api.github.com/graphql"

```

2. `scripts/label_approved.py:4-10`

```
from github import Github
from github.PullRequestReview import PullRequestReview
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings


class LabelSettings(BaseModel):
```

3. `scripts/notify_translations.py:8-14`

```
import httpx
from github import Github
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings

awaiting_label = "awaiting-review"
lang_all_label = "lang-all"
```

---

### Python import path (flat-layout)

**ID:** `python.conventions.import_aliases`  
**Category:** language  
**Language:** python  
**Confidence:** 85%

Python flat-layout. Import: `fastapi`.

**Statistics:**

- layout: `flat`
- package_name: `fastapi`

---

### Structured configuration with Pydantic Settings

**ID:** `python.conventions.secrets_access_style`  
**Category:** security  
**Language:** python  
**Confidence:** 85%
  
**Documentation:** [https://docs.pydantic.dev/latest/concepts/pydantic_settings/](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

Uses Pydantic BaseSettings for configuration management. Found 16 Settings usages.

**Statistics:**

- pydantic_settings: `16`

**Evidence:**

1. `scripts/contributors.py:237-243`

```

def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = Settings()  # ty: ignore[missing-argument]
    logging.info(f"Using config: {settings.model_dump_json()}")
    g = Github(settings.github_token.get_secret_value())
    repo = g.get_repo(settings.github_repository)
```

2. `scripts/label_approved.py:12-18`

```
    number: int


default_config = {"approved-2": LabelSettings(await_label="awaiting-review", number=2)}


class Settings(BaseSettings):
```

3. `scripts/label_approved.py:22-28`

```
    config: dict[str, LabelSettings] | Literal[""] = default_config


settings = Settings()  # ty: ignore[missing-argument]
if settings.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
```

---

### Data classes: Pydantic models

**ID:** `python.conventions.class_style`  
**Category:** code_style  
**Language:** python  
**Confidence:** 85%
  
**Documentation:** [https://docs.pydantic.dev/](https://docs.pydantic.dev/)

Uses Pydantic models for structured data. 85/103 structured classes use this pattern.

**Statistics:**

- dataclass_count: `10`
- pydantic_count: `85`
- attrs_count: `0`
- namedtuple_count: `8`
- plain_count: `70`
- dominant_style: `pydantic`

**Evidence:**

1. `fastapi/sse.py:47-57`

```
    if v is not None and "\0" in v:
        raise ValueError("SSE 'id' must not contain null characters")
    return _check_single_line(v, "id")


class ServerSentEvent(BaseModel):
    """Represents a single Server-Sent Event.

    When `yield`ed from a *path operation function* that uses
    `response_class=EventSourceResponse`, each `ServerSentEvent` is encoded
```

2. `fastapi/security/http.py:11-21`

```
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED


class HTTPBasicCredentials(BaseModel):
    """
    The HTTP Basic credentials given as the result of using `HTTPBasic` in a
    dependency.

```

3. `fastapi/security/http.py:24-34`

```

    username: Annotated[str, Doc("The HTTP Basic username.")]
    password: Annotated[str, Doc("The HTTP Basic password.")]


class HTTPAuthorizationCredentials(BaseModel):
    """
    The HTTP authorization credentials in the result of using `HTTPBearer` or
    `HTTPDigest` in a dependency.

```

---

### Test naming: Simple style (test_feature)

**ID:** `python.conventions.test_naming`  
**Category:** testing  
**Language:** python  
**Confidence:** 84%
  
**Documentation:** [https://docs.pytest.org/](https://docs.pytest.org/)

Uses Simple style (test_feature) naming. 2196/2253 (97%) test functions.

**Statistics:**

- total_test_functions: `2253`
- pattern_counts: `{'simple': 2196, 'action_result': 57}`
- test_class_count: `0`
- dominant_pattern: `simple`

**Evidence:**

1. `tests/test_datastructures.py:8-14`

```
from fastapi.testclient import TestClient


def test_upload_file_invalid_pydantic_v2():
    with pytest.raises(ValueError):
        UploadFile._validate("not a Starlette UploadFile", {})

```

2. `tests/test_datastructures.py:13-19`

```
        UploadFile._validate("not a Starlette UploadFile", {})


def test_default_placeholder_equals():
    placeholder_1 = cast(DefaultPlaceholder, Default("a"))
    placeholder_2 = cast(DefaultPlaceholder, Default("a"))
    assert placeholder_1 == placeholder_2
```

3. `tests/test_datastructures.py:20-26`

```
    assert placeholder_1.value == placeholder_2.value


def test_default_placeholder_bool():
    placeholder_a = Default("a")
    placeholder_b = Default("")
    assert placeholder_a
```

---

### Primary schema library: Pydantic

**ID:** `python.conventions.schema_library`  
**Category:** api  
**Language:** python  
**Confidence:** 84%
  
**Documentation:** [https://docs.pydantic.dev/](https://docs.pydantic.dev/)

Uses Pydantic as primary schema library (447/459 usages). Also uses: dataclasses.

**Statistics:**

- library_counts: `{'pydantic': 447, 'dataclasses': 12}`
- primary_library: `pydantic`

**Evidence:**

1. `tests/test_multi_body_errors.py:4-10`

```
from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, condecimal

app = FastAPI()

```

2. `tests/test_json_type.py:3-9`

```

from fastapi import Cookie, FastAPI, Form, Header, Query
from fastapi.testclient import TestClient
from pydantic import Json

app = FastAPI()

```

3. `tests/test_union_body_discriminator_annotated.py:6-12`

```
from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel


@pytest.fixture(name="client")
```

---

### Primary API framework: FastAPI

**ID:** `python.conventions.api_framework`  
**Category:** api  
**Language:** python  
**Confidence:** 83%
  
**Documentation:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

Uses FastAPI as primary framework (1740/1839 usages). Also uses: Starlette.

**Statistics:**

- framework_counts: `{'fastapi': 1740, 'starlette': 99}`
- primary_framework: `fastapi`

**Evidence:**

1. `tests/test_datastructures.py:3-9`

```
from typing import cast

import pytest
from fastapi import FastAPI, UploadFile
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.testclient import TestClient

```

2. `tests/test_datastructures.py:4-10`

```

import pytest
from fastapi import FastAPI, UploadFile
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.testclient import TestClient


```

3. `tests/test_datastructures.py:5-11`

```
import pytest
from fastapi import FastAPI, UploadFile
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.testclient import TestClient


def test_upload_file_invalid_pydantic_v2():
```

---

### Project history

**ID:** `generic.conventions.history`  
**Category:** documentation  
**Language:** generic  
**Confidence:** 80%

Detected 2 decision log items and 1 pitfalls.

**Statistics:**

- detected_decisions: `['Changelog breaking change: 🔥 Remove slim package stub, deprecated for a while. PR [#15649](https://github.com/fastapi/fastapi/pull/15649) by [@tiangolo](https://github.com/tiangolo).', 'Changelog breaking change: 🔧 Migrate docs from MkDocs to Zensical. PR [#15563](https://github.com/fastapi/fastapi/pull/15563) by [@tiangolo](https://github.com/tiangolo).']`
- detected_pitfalls: `['CI workflow `pre-commit.yml` contains steps allowed to fail (`continue-on-error: true`).']`

---

### Caching: functools.lru_cache

**ID:** `python.conventions.caching`  
**Category:** performance  
**Language:** python  
**Confidence:** 80%
  
**Documentation:** [https://redis.io/docs/](https://redis.io/docs/)

Uses functools.lru_cache for caching.

**Statistics:**

- caching_methods: `['lru_cache']`
- primary_method: `lru_cache`
- method_details: `{'lru_cache': {'name': 'functools.lru_cache', 'count': 2}}`

**Evidence:**

1. `fastapi/_compat/v2.py:411-417`

```


@lru_cache
def get_cached_model_fields(model: type[BaseModel]) -> list[ModelField]:
    return get_model_fields(model)


```

2. `scripts/translate.py:34-40`

```


@lru_cache
def get_langs() -> dict[str, str]:
    return yaml.safe_load(Path("docs/language_names.yml").read_text(encoding="utf-8"))


```

---

### Enum usage: Enum

**ID:** `python.conventions.enum_usage`  
**Category:** code_style  
**Language:** python  
**Confidence:** 80%
  
**Documentation:** [https://docs.python.org/3/library/enum.html](https://docs.python.org/3/library/enum.html)

Uses Python enums for categorical values. Found 4 enum class(es).

**Statistics:**

- enum_count: `4`
- enum_types: `{'Enum': 4}`
- enum_names: `['ParamTypes', 'ParameterInType', 'SecuritySchemeType', 'APIKeyIn']`

**Evidence:**

1. `fastapi/params.py:14-24`

```
    Undefined,
)
from .datastructures import _Unset


class ParamTypes(Enum):
    query = "query"
    header = "header"
    path = "path"
    cookie = "cookie"
```

2. `fastapi/openapi/models.py:216-226`

```
    externalValue: AnyUrl | None

    __pydantic_config__ = {"extra": "allow"}  # type: ignore[misc]  # ty: ignore[invalid-typed-dict-statement]


class ParameterInType(Enum):
    query = "query"
    header = "header"
    path = "path"
    cookie = "cookie"
```

3. `fastapi/openapi/models.py:316-326`

```
    trace: Operation | None = None
    servers: list[Server] | None = None
    parameters: list[Parameter | Reference] | None = None


class SecuritySchemeType(Enum):
    apiKey = "apiKey"
    http = "http"
    oauth2 = "oauth2"
    openIdConnect = "openIdConnect"
```

---

### Cursor-based pagination

**ID:** `python.conventions.pagination_pattern`  
**Category:** api  
**Language:** python  
**Confidence:** 80%
  
**Documentation:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

Uses cursor-based pagination. 8 cursor/after/before usages.

**Statistics:**

- offset_count: `0`
- cursor_count: `8`
- page_count: `0`
- pattern: `cursor`

---

### CI/CD: GitHub Actions

**ID:** `generic.conventions.ci_platform`  
**Category:** ci_cd  
**Language:** generic  
**Confidence:** 80%
  
**Documentation:** [https://docs.github.com/en/actions](https://docs.github.com/en/actions)

Uses GitHub Actions for CI/CD. 23 workflow(s) configured.

**Statistics:**

- platforms: `['github_actions']`
- platform_details: `{'github_actions': {'name': 'GitHub Actions', 'workflow_count': 23, 'files': ['guard-dependencies.yml', 'smokeshow.yml', 'issue-manager.yml', 'deploy-docs.yml', 'publish.yml']}}`

---

### Dependency updates: Dependabot

**ID:** `generic.conventions.dependency_updates`  
**Category:** dependencies  
**Language:** generic  
**Confidence:** 80%
  
**Documentation:** [https://docs.github.com/en/code-security/dependabot](https://docs.github.com/en/code-security/dependabot)

Automated dependency updates via Dependabot for github-actions.

**Statistics:**

- tools: `['dependabot']`
- tool_details: `{'dependabot': {'name': 'Dependabot', 'ecosystems': ['github-actions']}}`
- primary_tool: `dependabot`

---

### Git hooks: pre-commit

**ID:** `generic.conventions.git_hooks`  
**Category:** git  
**Language:** generic  
**Confidence:** 80%
  
**Documentation:** [https://pre-commit.com/](https://pre-commit.com/)

Uses pre-commit for Git hooks. Configured: whitespace, file validation, formatting, linting.

**Statistics:**

- hooks_tools: `['pre-commit']`
- hooks_configured: `['whitespace', 'file validation', 'formatting', 'linting']`
- hook_tool: `pre-commit`
- has_pre_commit: `True`
- has_husky: `False`
- has_lefthook: `False`

---

### Background jobs with FastAPI BackgroundTasks

**ID:** `python.conventions.background_jobs`  
**Category:** concurrency  
**Language:** python  
**Confidence:** 72%
  
**Documentation:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

Uses FastAPI BackgroundTasks for background task processing. Found 4 usages.

**Statistics:**

- job_library_counts: `{'fastapi_background': 4}`
- primary_library: `fastapi_background`
- task_decorators: `0`

**Evidence:**

1. `fastapi/background.py:1-10`

```
from collections.abc import Callable
from typing import Annotated, Any

from annotated_doc import Doc
from starlette.background import BackgroundTasks as StarletteBackgroundTasks
from typing_extensions import ParamSpec

P = ParamSpec("P")


```

2. `fastapi/__init__.py:3-13`

```
__version__ = "0.138.1"

from starlette import status as status

from .applications import FastAPI as FastAPI
from .background import BackgroundTasks as BackgroundTasks
from .datastructures import UploadFile as UploadFile
from .exceptions import HTTPException as HTTPException
from .exceptions import WebSocketException as WebSocketException
from .param_functions import Body as Body
```

3. `fastapi/dependencies/utils.py:47-57`

```
    lenient_issubclass,
    sequence_types,
    serialize_sequence_value,
    value_is_sequence,
)
from fastapi.background import BackgroundTasks
from fastapi.concurrency import (
    asynccontextmanager,
    contextmanager_in_threadpool,
)
```

---

### lowercase constant naming

**ID:** `python.conventions.constant_naming`  
**Category:** naming  
**Language:** python  
**Confidence:** 70%
  
**Documentation:** [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)

Uses lowercase naming for module-level values. 106/115 use lowercase.

**Statistics:**

- all_caps_count: `9`
- lowercase_count: `106`
- all_caps_ratio: `0.078`
- style: `lowercase`

**Evidence:**

1. `fastapi/params.py:18-22`

```

class ParamTypes(Enum):
    query = "query"
    header = "header"
    path = "path"
```

2. `fastapi/params.py:19-23`

```
class ParamTypes(Enum):
    query = "query"
    header = "header"
    path = "path"
    cookie = "cookie"
```

3. `fastapi/params.py:20-24`

```
    query = "query"
    header = "header"
    path = "path"
    cookie = "cookie"

```

---

### File I/O with context managers

**ID:** `python.conventions.context_file_io`  
**Category:** resource_management  
**Language:** python  
**Confidence:** 70%

Uses context managers for file operations. 4 usages ensure proper file cleanup.

**Statistics:**

- usage_count: `4`
- category: `file_io`

**Evidence:**

1. `scripts/docs.py:853-859`

```
    in_code_block4 = False
    permalinks = set()

    with path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
```

2. `scripts/docs.py:893-899`

```

        updated_lines.append(line)

    with path.open("w", encoding="utf-8") as f:
        f.writelines(updated_lines)


```

3. `scripts/add_latest_release_date.py:9-15`

```


def main() -> None:
    with open(RELEASE_NOTES_FILE) as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
```

---

### Custom decorator pattern: @deprecated

**ID:** `python.conventions.custom_decorators`  
**Category:** decorators  
**Language:** python  
**Confidence:** 70%

Uses custom decorator @deprecated (4 usages). Also uses: @asynccontextmanager.

**Statistics:**

- top_decorator: `deprecated`
- usage_count: `4`
- other_custom_decorators: `['asynccontextmanager']`

**Evidence:**

1. `fastapi/responses.py:34-44`

```
    orjson = cast(_OrjsonModule, importlib.import_module("orjson"))
except ModuleNotFoundError:  # pragma: nocover
    orjson = None  # type: ignore[assignment]


@deprecated(
    "UJSONResponse is deprecated, FastAPI now serializes data directly to JSON "
    "bytes via Pydantic when a return type or response model is set, which is "
    "faster and doesn't need a custom response class. Read more in the FastAPI "
    "docs: https://fastapi.tiangolo.com/advanced/custom-response/#orjson-or-response-model "
```

2. `fastapi/responses.py:64-74`

```
    def render(self, content: Any) -> bytes:
        assert ujson is not None, "ujson must be installed to use UJSONResponse"
        return ujson.dumps(content, ensure_ascii=False).encode("utf-8")


@deprecated(
    "ORJSONResponse is deprecated, FastAPI now serializes data directly to JSON "
    "bytes via Pydantic when a return type or response model is set, which is "
    "faster and doesn't need a custom response class. Read more in the FastAPI "
    "docs: https://fastapi.tiangolo.com/advanced/custom-response/#orjson-or-response-model "
```

3. `fastapi/applications.py:4643-4653`

```
            self.router.add_websocket_route(path, func, name=name)
            return func

        return decorator

    @deprecated(
        """
        on_event is deprecated, use lifespan event handlers instead.

        Read more about it in the
```

---

### HTTP errors raised in service layer

**ID:** `python.conventions.error_handling_boundary`  
**Category:** error_handling  
**Language:** python  
**Confidence:** 70%
  
**Documentation:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

HTTPException is frequently raised outside the API layer. Service: 0, API: 0, Other: 23.

**Statistics:**

- total_http_exceptions: `23`
- by_role: `{'test': 11, 'other': 12}`
- api_ratio: `0.0`

**Evidence:**

1. `tests/test_starlette_exception.py:9-19`

```


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "Some custom header"},
        )
```

2. `tests/test_starlette_exception.py:19-29`

```
    return {"item": items[item_id]}


@app.get("/http-no-body-statuscode-exception")
async def no_body_status_code_exception():
    raise HTTPException(status_code=204)


@app.get("/http-no-body-statuscode-with-detail-exception")
async def no_body_status_code_with_detail_exception():
```

3. `tests/test_starlette_exception.py:24-34`

```
    raise HTTPException(status_code=204)


@app.get("/http-no-body-statuscode-with-detail-exception")
async def no_body_status_code_with_detail_exception():
    raise HTTPException(status_code=204, detail="I should just disappear!")


@app.get("/starlette-items/{item_id}")
async def read_starlette_item(item_id: str):
```

---

### Limited exception chaining

**ID:** `python.conventions.exception_chaining`  
**Category:** error_handling  
**Language:** python  
**Confidence:** 70%
  
**Documentation:** [https://docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html)

Rarely uses 'raise X from Y'. 10/94 (11%) raises use chaining. Use 'raise X from Y' to preserve context or 'raise X from None' to suppress.

**Statistics:**

- chained_raises: `10`
- unchained_raises: `84`
- bare_raises: `2`
- chaining_ratio: `0.106`

**Evidence:**

1. `fastapi/encoders.py:350-356`

```
            data = vars(obj)
        except Exception as e:
            errors.append(e)
            raise ValueError(errors) from e
    return jsonable_encoder(
        data,
        include=include,
```

2. `fastapi/utils.py:72-78`

```
    try:
        return v2.ModelField(mode=mode, name=name, field_info=field_info)
    except PydanticSchemaGenerationError:
        raise fastapi.exceptions.FastAPIError(
            _invalid_args_message.format(type_=type_)
        ) from None

```

3. `fastapi/concurrency.py:34-40`

```
            )
        )
        if not ok:
            raise e
    else:
        await anyio.to_thread.run_sync(
            cm.__exit__, None, None, None, limiter=exit_limiter
```

---

### Semi-centralized exception handling

**ID:** `python.conventions.exception_handlers`  
**Category:** error_handling  
**Language:** python  
**Confidence:** 70%
  
**Documentation:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

Exception handlers are spread across 2 modules. Total handlers: 17.

**Statistics:**

- total_handlers: `17`
- decorator_handlers: `6`
- call_handlers: `11`
- handler_files: `['tests/test_validation_error_context.py', 'fastapi/applications.py']`

**Evidence:**

1. `tests/test_validation_error_context.py:27-37`

```
captured_exception = ExceptionCapture()

app.mount(path="/sub", app=sub_app)


@app.exception_handler(RequestValidationError)
@sub_app.exception_handler(RequestValidationError)
async def request_validation_handler(request: Request, exc: RequestValidationError):
    captured_exception.capture(exc)
    raise exc
```

2. `tests/test_validation_error_context.py:28-38`

```

app.mount(path="/sub", app=sub_app)


@app.exception_handler(RequestValidationError)
@sub_app.exception_handler(RequestValidationError)
async def request_validation_handler(request: Request, exc: RequestValidationError):
    captured_exception.capture(exc)
    raise exc

```

3. `tests/test_validation_error_context.py:34-44`

```
async def request_validation_handler(request: Request, exc: RequestValidationError):
    captured_exception.capture(exc)
    raise exc


@app.exception_handler(ResponseValidationError)
@sub_app.exception_handler(ResponseValidationError)
async def response_validation_handler(_: Request, exc: ResponseValidationError):
    captured_exception.capture(exc)
    raise exc
```

---

### Absolute imports preferred

**ID:** `python.conventions.import_style`  
**Category:** code_style  
**Language:** python  
**Confidence:** 70%
  
**Documentation:** [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)

Prefers absolute imports. 70 relative vs 510 absolute imports.

**Statistics:**

- relative_count: `70`
- absolute_count: `510`
- relative_ratio: `0.121`
- style: `absolute`

**Evidence:**

1. `fastapi/params.py:10-16`

```
from pydantic.fields import FieldInfo
from typing_extensions import deprecated

from ._compat import (
    Undefined,
)
from .datastructures import _Unset
```

2. `fastapi/params.py:13-19`

```
from ._compat import (
    Undefined,
)
from .datastructures import _Unset


class ParamTypes(Enum):
```

3. `fastapi/__init__.py:4-10`

```

from starlette import status as status

from .applications import FastAPI as FastAPI
from .background import BackgroundTasks as BackgroundTasks
from .datastructures import UploadFile as UploadFile
from .exceptions import HTTPException as HTTPException
```

---

### OpenAPI with FastAPI (default)

**ID:** `python.conventions.openapi_docs`  
**Category:** api  
**Language:** python  
**Confidence:** 70%
  
**Documentation:** [https://swagger.io/specification/](https://swagger.io/specification/)

Uses FastAPI's built-in OpenAPI documentation at /docs and /redoc.

**Statistics:**

- openapi_indicators: `{'fastapi_builtin': 1}`
- primary_tool: `fastapi_builtin`

---

### Response envelope classes

**ID:** `python.conventions.response_envelope`  
**Category:** api  
**Language:** python  
**Confidence:** 70%
  
**Documentation:** [https://docs.pydantic.dev/](https://docs.pydantic.dev/)

Uses response envelope classes (5 found).

**Statistics:**

- envelope_classes: `5`
- field_counts: `{'errors': 4, 'message': 2}`
- pattern: `class_based`

**Evidence:**

1. `fastapi/responses.py:43-53`

```
    "docs: https://fastapi.tiangolo.com/advanced/custom-response/#orjson-or-response-model "
    "and https://fastapi.tiangolo.com/tutorial/response-model/",
    category=FastAPIDeprecationWarning,
    stacklevel=2,
)
class UJSONResponse(JSONResponse):
    """JSON response using the ujson library to serialize data to JSON.

    **Deprecated**: `UJSONResponse` is deprecated. FastAPI now serializes data
    directly to JSON bytes via Pydantic when a return type or response model is
```

2. `fastapi/responses.py:73-83`

```
    "docs: https://fastapi.tiangolo.com/advanced/custom-response/#orjson-or-response-model "
    "and https://fastapi.tiangolo.com/tutorial/response-model/",
    category=FastAPIDeprecationWarning,
    stacklevel=2,
)
class ORJSONResponse(JSONResponse):
    """JSON response using the orjson library to serialize data to JSON.

    **Deprecated**: `ORJSONResponse` is deprecated. FastAPI now serializes data
    directly to JSON bytes via Pydantic when a return type or response model is
```

3. `scripts/contributors.py:102-112`

```

class PRsRepository(BaseModel):
    pullRequests: PullRequests


class PRsResponseData(BaseModel):
    repository: PRsRepository


class PRsResponse(BaseModel):
```

---

### Distributed test files

**ID:** `python.conventions.test_structure`  
**Category:** testing  
**Language:** python  
**Confidence:** 70%
  
**Documentation:** [https://docs.pytest.org/](https://docs.pytest.org/)

Test files spread across 2 directories. 496 total test files.

**Statistics:**

- test_file_count: `496`
- test_directories: `{'tests': 485, 'scripts': 11}`
- has_unit: `False`
- has_integration: `False`
- has_e2e: `False`
- structure: `distributed`
- categories: `[]`

---

### Mixed validation approaches

**ID:** `python.conventions.validation_style`  
**Category:** validation  
**Language:** python  
**Confidence:** 70%
  
**Documentation:** [https://docs.pydantic.dev/](https://docs.pydantic.dev/)

Uses multiple validation approaches: Pydantic validation, Manual validation (ValueError/TypeError), Decorator-based validation.

**Statistics:**

- validation_counts: `{'pydantic': 17, 'decorator': 1, 'manual': 14}`
- dominant_style: `pydantic`
- dominant_ratio: `0.531`

**Evidence:**

1. `fastapi/encoders.py:21-27`

```
from annotated_doc import Doc
from fastapi.exceptions import PydanticV1NotSupportedError
from fastapi.types import IncEx
from pydantic import BaseModel
from pydantic.networks import AnyUrl, NameEmail
from pydantic.types import SecretBytes, SecretStr
from pydantic_core import PydanticUndefinedType
```

2. `fastapi/types.py:3-9`

```
from enum import Enum
from typing import Any, TypeVar, Union

from pydantic import BaseModel
from pydantic.main import IncEx as IncEx

DecoratedCallable = TypeVar("DecoratedCallable", bound=Callable[..., Any])
```

3. `fastapi/sse.py:1-7`

```
from typing import Annotated, Any

from annotated_doc import Doc
from pydantic import AfterValidator, BaseModel, Field, model_validator
from starlette.responses import StreamingResponse

# Canonical SSE event schema matching the OpenAPI 3.2 spec
```

---

### Standard repository files

**ID:** `generic.conventions.standard_files`  
**Category:** structure  
**Language:** generic  
**Confidence:** 60%
  
**Documentation:** [https://docs.github.com/en/actions](https://docs.github.com/en/actions)

Repository has standard files: README.md, LICENSE, .gitignore, .pre-commit-config.yaml

**Statistics:**

- found_files: `['README.md', 'LICENSE', '.gitignore', '.pre-commit-config.yaml']`

---

### Default connection pooling

**ID:** `python.conventions.db_connection_pooling`  
**Category:** database  
**Language:** python  
**Confidence:** 60%
  
**Documentation:** [https://docs.sqlalchemy.org/](https://docs.sqlalchemy.org/)

Uses default SQLAlchemy connection pooling without explicit configuration.

**Statistics:**

- default_pool: `2`

---

### Low docstring coverage

**ID:** `python.conventions.docstrings`  
**Category:** documentation  
**Language:** python  
**Confidence:** 60%
  
**Documentation:** [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)

Few functions have docstrings. Only 82/438 (19%).

**Statistics:**

- total_public_functions: `438`
- documented_functions: `82`
- function_doc_ratio: `0.187`
- total_classes: `174`
- documented_classes: `31`
- class_doc_ratio: `0.178`

**Evidence:**

1. `fastapi/applications.py:1065-1075`

```
        app = self.router
        for cls, args, kwargs in reversed(middleware):
            app = cls(app, *args, **kwargs)
        return app

    def openapi(self) -> dict[str, Any]:
        """
        Generate the OpenAPI schema of the application. This is called by FastAPI
        internally.

```

2. `fastapi/applications.py:1217-1227`

```
            name=name,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    def frontend(
        self,
        path: Annotated[
            str,
            Doc(
```

3. `fastapi/params.py:26-32`

```
class Param(FieldInfo):  # type: ignore[misc]  # ty: ignore[subclass-of-final-class]
    in_: ParamTypes

    def __init__(
        self,
        default: Any = Undefined,
        *,
```

---

### Mixed exception naming conventions

**ID:** `python.conventions.error_taxonomy`  
**Category:** error_handling  
**Language:** python  
**Confidence:** 60%
  
**Documentation:** [https://docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html)

Exception naming is mixed: 11 *Error, 3 *Exception out of 14 total.

**Statistics:**

- total_custom_exceptions: `14`
- error_suffix_count: `11`
- exception_suffix_count: `3`
- exception_names: `['CustomError', 'AsyncDependencyError', 'SyncDependencyError', 'OtherDependencyError', 'CustomError', 'HTTPException', 'WebSocketException', 'FastAPIError', 'DependencyScopeError', 'ValidationException', 'RequestValidationError', 'WebSocketRequestValidationError', 'ResponseValidationError', 'PydanticV1NotSupportedError']`
- consistency: `0.786`

**Evidence:**

1. `tests/test_ws_router.py:95-101`

```
    pass  # pragma: no cover


class CustomError(Exception):
    pass


```

2. `tests/test_dependency_contextmanager.py:24-30`

```
    return state


class AsyncDependencyError(Exception):
    pass


```

3. `tests/test_dependency_contextmanager.py:28-34`

```
    pass


class SyncDependencyError(Exception):
    pass


```

---

### Pre-commit hooks configured

**ID:** `python.conventions.pre_commit_hooks`  
**Category:** tooling  
**Language:** python  
**Confidence:** 60%
  
**Documentation:** [https://pre-commit.com/](https://pre-commit.com/)

Pre-commit is configured with 18 hooks.

**Statistics:**

- has_pre_commit: `True`
- hooks: `['check-added-large-files', 'check-toml', 'check-yaml', 'end-of-file-fixer', 'trailing-whitespace', 'typos', 'local-ruff-check', 'local-ruff-format', 'local-mypy', 'local-ty', 'add-permalinks-pages', 'generate-readme', 'render-banner-sponsors', 'update-languages', 'ensure-non-translated', 'fix-translations', 'add-release-date', 'zizmor']`
- has_ruff: `False`
- has_mypy: `False`
- has_pyright: `False`
- has_type_checker: `False`
- has_black: `False`
- has_flake8: `False`
- has_isort: `False`

---

### Infrequent timeout specification

**ID:** `python.conventions.timeouts`  
**Category:** resilience  
**Language:** python  
**Confidence:** 60%
  
**Documentation:** [https://www.python-httpx.org/](https://www.python-httpx.org/)

Timeouts are rarely specified on external calls. Only 6 calls with explicit timeouts.

**Statistics:**

- timeout_indicators: `6`
- no_timeout_indicators: `275`
- timeout_ratio: `0.021`

**Evidence:**

1. `tests/test_stream_cancellation.py:77-83`

```

async def test_raw_stream_cancellation() -> None:
    """Raw streaming endpoint should be cancellable within a reasonable time."""
    cancelled = await _run_asgi_and_cancel(app, "/stream-raw", timeout=3.0)
    # The key assertion: we reached this line at all (didn't hang).
    # cancelled will be True because the infinite generator was interrupted.
    assert cancelled
```

2. `tests/test_stream_cancellation.py:85-89`

```

async def test_jsonl_stream_cancellation() -> None:
    """JSONL streaming endpoint should be cancellable within a reasonable time."""
    cancelled = await _run_asgi_and_cancel(app, "/stream-jsonl", timeout=3.0)
    assert cancelled
```

3. `scripts/contributors.py:126-132`

```
) -> dict[str, Any]:
    headers = {"Authorization": f"token {settings.github_token.get_secret_value()}"}
    variables = {"after": after}
    response = httpx.post(
        github_graphql_url,
        headers=headers,
        timeout=settings.httpx_timeout,
```

---

### Error wrapper pattern: time.sleep

**ID:** `python.conventions.error_wrapper`  
**Category:** error_handling  
**Language:** python  
**Confidence:** 57%
  
**Documentation:** [https://docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html)

Uses 'time.sleep' as a common error handler function. Called in 7/40 (18%) except blocks.

**Statistics:**

- wrapper_function: `time.sleep`
- usage_count: `7`
- total_handlers: `40`
- usage_ratio: `0.175`
- other_wrappers: `[]`

**Evidence:**

1. `scripts/playwright/cookie_param_models/image01.py:28-38`

```
)
try:
    for _ in range(3):
        try:
            response = httpx.get("http://localhost:8000/docs")
        except httpx.ConnectError:
            time.sleep(1)
            break
    with sync_playwright() as playwright:
        run(playwright)
```

2. `scripts/playwright/sql_databases/image01.py:26-36`

```
)
try:
    for _ in range(3):
        try:
            response = httpx.get("http://localhost:8000/docs")
        except httpx.ConnectError:
            time.sleep(1)
            break
    with sync_playwright() as playwright:
        run(playwright)
```

3. `scripts/playwright/sql_databases/image02.py:26-36`

```
)
try:
    for _ in range(3):
        try:
            response = httpx.get("http://localhost:8000/docs")
        except httpx.ConnectError:
            time.sleep(1)
            break
    with sync_playwright() as playwright:
        run(playwright)
```

---

### Health check functions

**ID:** `python.conventions.health_checks`  
**Category:** resilience  
**Language:** python  
**Confidence:** 50%
  
**Documentation:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

Has 1 health-related function(s) but no clear endpoints.

**Statistics:**

- health_endpoint_count: `0`
- health_function_count: `1`
- has_readiness: `False`
- has_liveness: `True`

**Evidence:**

1. `scripts/docs.py:458-464`

```


@app.command()
def live() -> None:
    """
    Serve the English docs with livereload from the source files.
    """
```

---
