# Conventions Review Report

*Generated: 2026-06-28 12:36:48*

## Score Legend

| Score | Rating |
|:-----:|:-------|
| 5 | Excellent |
| 4 | Good |
| 3 | Average |
| 2 | Below Average |
| 1 | Poor |

## Summary

- **Conventions Reviewed:** 65
- **Average Score:** 3.6/5 (Good)
- **Excellent (5):** 15
- **Good (4):** 17
- **Average (3):** 27
- **Below Average (2):** 3
- **Poor (1):** 3

## Scores Overview

| Convention | Score | Rating |
|:-----------|:-----:|:-------|
| Dependency updates: Dependabot | 5/5 | Excellent |
| Git hooks: pre-commit | 5/5 | Excellent |
| Primary API framework: FastAPI | 5/5 | Excellent |
| Async HTTP client: httpx (recommended) | 5/5 | Excellent |
| CLI framework: Typer | 5/5 | Excellent |
| Data class style: Pydantic for API + dataclasses for internal | 5/5 | Excellent |
| Dependency management: uv | 5/5 | Excellent |
| Import organization: Ruff with grouping | 5/5 | Excellent |
| Linters: Ruff, mypy | 5/5 | Excellent |
| Lock file: uv.lock | 5/5 | Excellent |
| PEP 8 snake_case naming | 5/5 | Excellent |
| Structured configuration with Pydantic Settings | 5/5 | Excellent |
| pytest-based testing | 5/5 | Excellent |
| Type checker: mypy (strict mode) | 5/5 | Excellent |
| High type annotation coverage | 5/5 | Excellent |
| CI/CD best practices | 4/5 | Good |
| Standard repository layout | 4/5 | Good |
| Runtime prerequisites | 4/5 | Good |
| API routes | 4/5 | Good |
| OAuth2 authentication | 4/5 | Good |
| Caching: functools.lru_cache | 4/5 | Good |
| Context manager usage | 4/5 | Good |
| Caching decorator pattern | 4/5 | Good |
| Environment separation: Pydantic Settings | 4/5 | Good |
| Semi-centralized exception handling | 4/5 | Good |
| OpenAPI with FastAPI (default) | 4/5 | Good |
| Modern pathlib for path handling | 4/5 | Good |
| Primary schema library: Pydantic | 4/5 | Good |
| Import dependency graph | 4/5 | Good |
| pytest fixtures for test setup | 4/5 | Good |
| Mocking with pytest monkeypatch fixture | 4/5 | Good |
| Parametrized tests | 4/5 | Good |
| CI/CD: GitHub Actions | 3/5 | Average |
| Config access patterns | 3/5 | Average |
| Project history | 3/5 | Average |
| URL-based API versioning | 3/5 | Average |
| Background jobs with FastAPI BackgroundTasks | 3/5 | Average |
| Data classes: Pydantic models | 3/5 | Average |
| lowercase constant naming | 3/5 | Average |
| File I/O with context managers | 3/5 | Average |
| Custom decorator pattern: @deprecated | 3/5 | Average |
| Default connection pooling | 3/5 | Average |
| FastAPI-style session dependency injection | 3/5 | Average |
| Dependency health | 3/5 | Average |
| Enum usage: Enum | 3/5 | Average |
| Mixed exception naming conventions | 3/5 | Average |
| Error wrapper pattern: time.sleep | 3/5 | Average |
| Python import path (flat-layout) | 3/5 | Average |
| Absolute imports preferred | 3/5 | Average |
| JSON library: mixed | 3/5 | Average |
| Uses Python standard logging | 3/5 | Average |
| Cursor-based pagination | 3/5 | Average |
| Pre-commit hooks configured | 3/5 | Average |
| Response envelope classes | 3/5 | Average |
| Modern f-string formatting | 3/5 | Average |
| Test naming: Simple style (test_feature) | 3/5 | Average |
| Distributed test files | 3/5 | Average |
| Mixed validation approaches | 3/5 | Average |
| Plain assert statements | 3/5 | Average |
| Standard repository files | 2/5 | Below Average |
| Limited exception chaining | 2/5 | Below Average |
| Health check functions | 2/5 | Below Average |
| Low docstring coverage | 1/5 | Poor |
| HTTP errors raised in service layer | 1/5 | Poor |
| Infrequent timeout specification | 1/5 | Poor |

## Detailed Reviews

### Excellent (5/5)

#### Dependency updates: Dependabot

**ID:** `generic.conventions.dependency_updates`  
**Score:** 5/5 (Excellent)

**Assessment:** Dependency updates: dependabot

---

#### Git hooks: pre-commit

**ID:** `generic.conventions.git_hooks`  
**Score:** 5/5 (Excellent)

**Assessment:** Git hooks: pre-commit

---

#### Primary API framework: FastAPI

**ID:** `python.conventions.api_framework`  
**Score:** 5/5 (Excellent)

**Assessment:** Uses FastAPI as primary API framework

---

#### Async HTTP client: httpx (recommended)

**ID:** `python.conventions.async_http_client`  
**Score:** 5/5 (Excellent)

**Assessment:** Uses httpx for HTTP requests

---

#### CLI framework: Typer

**ID:** `python.conventions.cli_framework`  
**Score:** 5/5 (Excellent)

**Assessment:** CLI framework: typer

---

#### Data class style: Pydantic for API + dataclasses for internal

**ID:** `python.conventions.data_class_style`  
**Score:** 5/5 (Excellent)

**Assessment:** Data class style: Pydantic

---

#### Dependency management: uv

**ID:** `python.conventions.dependency_management`  
**Score:** 5/5 (Excellent)

**Assessment:** Dependencies: uv

---

#### Import organization: Ruff with grouping

**ID:** `python.conventions.import_sorting`  
**Score:** 5/5 (Excellent)

**Assessment:** Import sorting: ruff with grouping

---

#### Linters: Ruff, mypy

**ID:** `python.conventions.linter`  
**Score:** 5/5 (Excellent)

**Assessment:** Linters: Ruff, mypy

---

#### Lock file: uv.lock

**ID:** `python.conventions.lock_file`  
**Score:** 5/5 (Excellent)

**Assessment:** Lock file: uv.lock

---

#### PEP 8 snake_case naming

**ID:** `python.conventions.naming`  
**Score:** 5/5 (Excellent)

**Assessment:** PEP 8 snake_case compliance is 100%

---

#### Structured configuration with Pydantic Settings

**ID:** `python.conventions.secrets_access_style`  
**Score:** 5/5 (Excellent)

**Assessment:** Uses Pydantic Settings for configuration (os.environ: 0 direct accesses)

---

#### pytest-based testing

**ID:** `python.conventions.testing_framework`  
**Score:** 5/5 (Excellent)

**Assessment:** Uses pytest with 496 test file(s)

---

#### Type checker: mypy (strict mode)

**ID:** `python.conventions.type_checker_strictness`  
**Score:** 5/5 (Excellent)

**Assessment:** mypy in strict mode

---

#### High type annotation coverage

**ID:** `python.conventions.typing_coverage`  
**Score:** 5/5 (Excellent)

**Assessment:** Type annotation coverage is 99%

---

### Good (4/5)

#### CI/CD best practices

**ID:** `generic.conventions.ci_quality`  
**Score:** 4/5 (Good)

**Assessment:** Convention detected with 90% confidence

---

#### Standard repository layout

**ID:** `generic.conventions.repo_layout`  
**Score:** 4/5 (Good)

**Assessment:** Convention detected with 90% confidence

---

#### Runtime prerequisites

**ID:** `generic.conventions.runtime_prerequisites`  
**Score:** 4/5 (Good)

**Assessment:** Convention detected with 90% confidence

---

#### API routes

**ID:** `python.conventions.api_routes`  
**Score:** 4/5 (Good)

**Assessment:** Convention detected with 90% confidence

---

#### OAuth2 authentication

**ID:** `python.conventions.auth_pattern`  
**Score:** 4/5 (Good)

**Assessment:** Authentication uses OAuth2, dependency injection

**Suggestion:** Use a dedicated password hashing library (passlib or bcrypt) for secure credential storage.

---

#### Caching: functools.lru_cache

**ID:** `python.conventions.caching`  
**Score:** 4/5 (Good)

**Assessment:** Caching with functools.lru_cache

**Suggestion:** Consider Redis for distributed caching in production environments.

---

#### Context manager usage

**ID:** `python.conventions.context_managers`  
**Score:** 4/5 (Good)

**Assessment:** Convention detected with 90% confidence

---

#### Caching decorator pattern

**ID:** `python.conventions.decorator_caching`  
**Score:** 4/5 (Good)

**Assessment:** Convention detected with 90% confidence

---

#### Environment separation: Pydantic Settings

**ID:** `python.conventions.env_separation`  
**Score:** 4/5 (Good)

**Assessment:** Config: Pydantic Settings

---

#### Semi-centralized exception handling

**ID:** `python.conventions.exception_handlers`  
**Score:** 4/5 (Good)

**Assessment:** Exception handlers spread across 2 module(s) (17 handlers)

**Suggestion:** Consider centralizing exception handlers for easier maintenance.

---

#### OpenAPI with FastAPI (default)

**ID:** `python.conventions.openapi_docs`  
**Score:** 4/5 (Good)

**Assessment:** OpenAPI docs via FastAPI (default)

**Suggestion:** Customize OpenAPI metadata with tags, descriptions, and examples for better docs.

---

#### Modern pathlib for path handling

**ID:** `python.conventions.path_handling`  
**Score:** 4/5 (Good)

**Assessment:** Convention detected with 92% confidence

---

#### Primary schema library: Pydantic

**ID:** `python.conventions.schema_library`  
**Score:** 4/5 (Good)

**Assessment:** Uses Pydantic for schema validation

**Suggestion:** Ensure consistent schema library usage across the codebase.

---

#### Import dependency graph

**ID:** `python.data_flow.import_graph`  
**Score:** 4/5 (Good)

**Assessment:** Convention detected with 90% confidence

---

#### pytest fixtures for test setup

**ID:** `python.test_conventions.fixtures`  
**Score:** 4/5 (Good)

**Assessment:** Convention detected with 90% confidence

---

#### Mocking with pytest monkeypatch fixture

**ID:** `python.test_conventions.mocking`  
**Score:** 4/5 (Good)

**Assessment:** Convention detected with 90% confidence

---

#### Parametrized tests

**ID:** `python.test_conventions.parametrized`  
**Score:** 4/5 (Good)

**Assessment:** Convention detected with 90% confidence

---

### Average (3/5)

#### CI/CD: GitHub Actions

**ID:** `generic.conventions.ci_platform`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 80% confidence

**Suggestion:** Add automated testing, linting, and deployment steps to your CI/CD pipeline.

---

#### Config access patterns

**ID:** `generic.conventions.config_access`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 88% confidence

**Suggestion:** Review this convention and consider industry best practices for improvement.

---

#### Project history

**ID:** `generic.conventions.history`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 80% confidence

**Suggestion:** Add docstrings to public functions and classes explaining purpose and parameters.

---

#### URL-based API versioning

**ID:** `python.conventions.api_versioning`  
**Score:** 3/5 (Average)

**Assessment:** URL-based API versioning (2 versioned routes)

**Suggestion:** Apply consistent versioning across all API routes.

---

#### Background jobs with FastAPI BackgroundTasks

**ID:** `python.conventions.background_jobs`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 72% confidence

**Suggestion:** Use appropriate synchronization primitives and handle async errors properly.

---

#### Data classes: Pydantic models

**ID:** `python.conventions.class_style`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 85% confidence

**Suggestion:** Review this convention and consider industry best practices for improvement.

---

#### lowercase constant naming

**ID:** `python.conventions.constant_naming`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 70% confidence

**Suggestion:** Review this convention and consider industry best practices for improvement.

---

#### File I/O with context managers

**ID:** `python.conventions.context_file_io`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 70% confidence

**Suggestion:** Review this convention and consider industry best practices for improvement.

---

#### Custom decorator pattern: @deprecated

**ID:** `python.conventions.custom_decorators`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 70% confidence

**Suggestion:** Review this convention and consider industry best practices for improvement.

---

#### Default connection pooling

**ID:** `python.conventions.db_connection_pooling`  
**Score:** 3/5 (Average)

**Assessment:** Uses default connection pooling

**Suggestion:** Configure pool_size, max_overflow, and pool_pre_ping for production reliability.

---

#### FastAPI-style session dependency injection

**ID:** `python.conventions.db_session_lifecycle`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 85% confidence

**Suggestion:** Review this convention and consider industry best practices for improvement.

---

#### Dependency health

**ID:** `python.conventions.dependency_health`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 85% confidence

**Suggestion:** Add automated testing, linting, and deployment steps to your CI/CD pipeline.

---

#### Enum usage: Enum

**ID:** `python.conventions.enum_usage`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 80% confidence

**Suggestion:** Review this convention and consider industry best practices for improvement.

---

#### Mixed exception naming conventions

**ID:** `python.conventions.error_taxonomy`  
**Score:** 3/5 (Average)

**Assessment:** Exception naming is 79% consistent across 14 custom exceptions

**Suggestion:** Standardize exception naming to use *Error suffix consistently.

---

#### Error wrapper pattern: time.sleep

**ID:** `python.conventions.error_wrapper`  
**Score:** 3/5 (Average)

**Assessment:** Error wrapper 'time.sleep' used in 7/40 handlers (18%)

**Suggestion:** Consider using 'time.sleep' more consistently across all exception handlers.

---

#### Python import path (flat-layout)

**ID:** `python.conventions.import_aliases`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 85% confidence

**Suggestion:** Review this convention and consider industry best practices for improvement.

---

#### Absolute imports preferred

**ID:** `python.conventions.import_style`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 70% confidence

**Suggestion:** Review this convention and consider industry best practices for improvement.

---

#### JSON library: mixed

**ID:** `python.conventions.json_library`  
**Score:** 3/5 (Average)

**Assessment:** Uses stdlib json (47 usages)

**Suggestion:** Consider orjson for 10x faster JSON serialization with minimal API changes.

---

#### Uses Python standard logging

**ID:** `python.conventions.logging_library`  
**Score:** 3/5 (Average)

**Assessment:** Uses stdlib logging as primary logging library

**Suggestion:** Consider adopting structlog or Loguru for structured logging with better context propagation.

---

#### Cursor-based pagination

**ID:** `python.conventions.pagination_pattern`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 80% confidence

**Suggestion:** Review this convention and consider industry best practices for improvement.

---

#### Pre-commit hooks configured

**ID:** `python.conventions.pre_commit_hooks`  
**Score:** 3/5 (Average)

**Assessment:** 18 pre-commit hooks configured

**Suggestion:** Add ruff to pre-commit for fast linting and formatting.

---

#### Response envelope classes

**ID:** `python.conventions.response_envelope`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 70% confidence

**Suggestion:** Review this convention and consider industry best practices for improvement.

---

#### Modern f-string formatting

**ID:** `python.conventions.string_formatting`  
**Score:** 3/5 (Average)

**Assessment:** f-string usage: 0%

**Suggestion:** Prefer f-strings for readability and performance over .format() or %.

---

#### Test naming: Simple style (test_feature)

**ID:** `python.conventions.test_naming`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 84% confidence

**Suggestion:** Add more test cases and increase coverage of edge cases and error paths.

---

#### Distributed test files

**ID:** `python.conventions.test_structure`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 70% confidence

**Suggestion:** Add more test cases and increase coverage of edge cases and error paths.

---

#### Mixed validation approaches

**ID:** `python.conventions.validation_style`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 70% confidence

**Suggestion:** Review this convention and consider industry best practices for improvement.

---

#### Plain assert statements

**ID:** `python.test_conventions.assertions`  
**Score:** 3/5 (Average)

**Assessment:** Convention detected with 89% confidence

**Suggestion:** Add more test cases and increase coverage of edge cases and error paths.

---

### Below Average (2/5)

#### Standard repository files

**ID:** `generic.conventions.standard_files`  
**Score:** 2/5 (Below Average)

**Assessment:** Convention detected with 60% confidence

**Suggestion:** Review this convention and consider industry best practices for improvement.

---

#### Limited exception chaining

**ID:** `python.conventions.exception_chaining`  
**Score:** 2/5 (Below Average)

**Assessment:** Exception chaining: 11%

**Suggestion:** Use 'raise X from Y' for context or 'raise X from None' to suppress chain.

---

#### Health check functions

**ID:** `python.conventions.health_checks`  
**Score:** 2/5 (Below Average)

**Assessment:** Health checks: liveness

**Suggestion:** Add a /ready endpoint to signal when the service is ready to accept traffic.

---

### Poor (1/5)

#### Low docstring coverage

**ID:** `python.conventions.docstrings`  
**Score:** 1/5 (Poor)

**Assessment:** Docstring coverage is 19% of public functions

**Suggestion:** Add docstrings to public functions and classes. Focus on explaining the 'why' and documenting parameters/return values.

---

#### HTTP errors raised in service layer

**ID:** `python.conventions.error_handling_boundary`  
**Score:** 1/5 (Poor)

**Assessment:** HTTPException raised in API layer 0% of the time

**Suggestion:** Ensure HTTP errors are raised only at the API boundary layer.

---

#### Infrequent timeout specification

**ID:** `python.conventions.timeouts`  
**Score:** 1/5 (Poor)

**Assessment:** Timeout coverage is 2% (6 with, 275 without)

**Suggestion:** Add explicit timeouts to HTTP client calls. Found 275 calls without timeouts.

---

## Improvement Priorities

Conventions sorted by priority (lowest scores first):

1. **Low docstring coverage** (Score: 1/5)
   - Add docstrings to public functions and classes. Focus on explaining the 'why' and documenting parameters/return values.

2. **HTTP errors raised in service layer** (Score: 1/5)
   - Ensure HTTP errors are raised only at the API boundary layer.

3. **Infrequent timeout specification** (Score: 1/5)
   - Add explicit timeouts to HTTP client calls. Found 275 calls without timeouts.

4. **Standard repository files** (Score: 2/5)
   - Review this convention and consider industry best practices for improvement.

5. **Limited exception chaining** (Score: 2/5)
   - Use 'raise X from Y' for context or 'raise X from None' to suppress chain.

6. **Health check functions** (Score: 2/5)
   - Add a /ready endpoint to signal when the service is ready to accept traffic.

7. **CI/CD: GitHub Actions** (Score: 3/5)
   - Add automated testing, linting, and deployment steps to your CI/CD pipeline.

8. **Config access patterns** (Score: 3/5)
   - Review this convention and consider industry best practices for improvement.

9. **Project history** (Score: 3/5)
   - Add docstrings to public functions and classes explaining purpose and parameters.

10. **URL-based API versioning** (Score: 3/5)
   - Apply consistent versioning across all API routes.

11. **Background jobs with FastAPI BackgroundTasks** (Score: 3/5)
   - Use appropriate synchronization primitives and handle async errors properly.

12. **Data classes: Pydantic models** (Score: 3/5)
   - Review this convention and consider industry best practices for improvement.

13. **lowercase constant naming** (Score: 3/5)
   - Review this convention and consider industry best practices for improvement.

14. **File I/O with context managers** (Score: 3/5)
   - Review this convention and consider industry best practices for improvement.

15. **Custom decorator pattern: @deprecated** (Score: 3/5)
   - Review this convention and consider industry best practices for improvement.

16. **Default connection pooling** (Score: 3/5)
   - Configure pool_size, max_overflow, and pool_pre_ping for production reliability.

17. **FastAPI-style session dependency injection** (Score: 3/5)
   - Review this convention and consider industry best practices for improvement.

18. **Dependency health** (Score: 3/5)
   - Add automated testing, linting, and deployment steps to your CI/CD pipeline.

19. **Enum usage: Enum** (Score: 3/5)
   - Review this convention and consider industry best practices for improvement.

20. **Mixed exception naming conventions** (Score: 3/5)
   - Standardize exception naming to use *Error suffix consistently.

21. **Error wrapper pattern: time.sleep** (Score: 3/5)
   - Consider using 'time.sleep' more consistently across all exception handlers.

22. **Python import path (flat-layout)** (Score: 3/5)
   - Review this convention and consider industry best practices for improvement.

23. **Absolute imports preferred** (Score: 3/5)
   - Review this convention and consider industry best practices for improvement.

24. **JSON library: mixed** (Score: 3/5)
   - Consider orjson for 10x faster JSON serialization with minimal API changes.

25. **Uses Python standard logging** (Score: 3/5)
   - Consider adopting structlog or Loguru for structured logging with better context propagation.

26. **Cursor-based pagination** (Score: 3/5)
   - Review this convention and consider industry best practices for improvement.

27. **Pre-commit hooks configured** (Score: 3/5)
   - Add ruff to pre-commit for fast linting and formatting.

28. **Response envelope classes** (Score: 3/5)
   - Review this convention and consider industry best practices for improvement.

29. **Modern f-string formatting** (Score: 3/5)
   - Prefer f-strings for readability and performance over .format() or %.

30. **Test naming: Simple style (test_feature)** (Score: 3/5)
   - Add more test cases and increase coverage of edge cases and error paths.

31. **Distributed test files** (Score: 3/5)
   - Add more test cases and increase coverage of edge cases and error paths.

32. **Mixed validation approaches** (Score: 3/5)
   - Review this convention and consider industry best practices for improvement.

33. **Plain assert statements** (Score: 3/5)
   - Add more test cases and increase coverage of edge cases and error paths.

34. **OAuth2 authentication** (Score: 4/5)
   - Use a dedicated password hashing library (passlib or bcrypt) for secure credential storage.

35. **Caching: functools.lru_cache** (Score: 4/5)
   - Consider Redis for distributed caching in production environments.

36. **Semi-centralized exception handling** (Score: 4/5)
   - Consider centralizing exception handlers for easier maintenance.

37. **OpenAPI with FastAPI (default)** (Score: 4/5)
   - Customize OpenAPI metadata with tags, descriptions, and examples for better docs.

38. **Primary schema library: Pydantic** (Score: 4/5)
   - Ensure consistent schema library usage across the codebase.
