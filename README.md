# <img src="brand-mark.png" width="32" height="32" align="absmiddle" alt="Klaussy Logo"> klaussy-repo-conventions 🔍

[![PyPI version](https://img.shields.io/pypi/v/klaussy-repo-conventions.svg)](https://pypi.org/project/klaussy-repo-conventions/)
[![Python versions](https://img.shields.io/pypi/pyversions/klaussy-repo-conventions.svg)](https://pypi.org/project/klaussy-repo-conventions/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/steph-dove/klaussy-repo-conventions.svg?style=social)](https://github.com/steph-dove/klaussy-repo-conventions/stargazers)

> **Discover once, align everywhere.** The core conventions discovery and repository mapping engine. It scans codebases for structural styles, rates conventions on a 1-5 scale, traces endpoint-to-store data flows, and compiles a canonical `CLAUDE.md` and rules folder consumed by `klaussy-agents`.

Designed by an ex-GitHub, ex-Twitch, and ex-Microsoft engineer, `klaussy-repo-conventions` is a lightweight, AST-backed static-analysis CLI. It parses file patterns, naming conventions, import trees, and error handling behaviors across multiple programming languages—acting as the single source of truth for downstream AI agent configuration.

---

## ⚡ Quick Start

Analyze your codebase and generate agent-optimized context files in seconds:

```bash
# Install using pipx (recommended)
pipx install klaussy-repo-conventions

# Scan the current directory
conventions discover
```

*This scans the local workspace, auto-detects project languages, and writes detailed convention metrics and ratings into the `.conventions/` directory.*

---

## 🚀 Key Features

*   **🔍 AST-Backed Convention Scan:** Traverses your AST (Python) and code structures (Go, Node, Rust) to detect style patterns, naming strategies, and testing setups.
*   **📊 Multi-Language Analysis:** Deep-dives into Python, Go, Node.js/TypeScript, and Rust, plus cross-language assets (Docker, Kubernetes, GitHub Actions).
*   **🗺️ Architecture Data-Flow Maps:** Computes package dependency graphs, detects circular dependencies (DFS), and traces API endpoints down to their database store layers, generating Mermaid flowcharts directly in `CLAUDE.md`.
*   **🤖 Prescriptive Agent Scoping:** Generates `CLAUDE.md` and path-scoped rules files in `.claude/rules/` with imperative instructions and embedded few-shot code evidence blocks—giving agents the exact models they need to mirror.
*   **📈 Review & Scoring Gate:** Rates each detected convention on a 1-5 scale, listing prioritized improvement suggestions. Ideal for local quality audits and CI/CD validation gates.
*   **🔌 Pluggable Architecture:** Write custom python detectors and rating rule extensions using the plug-in framework.

---

## 🤖 CLAUDE.md & Scoped Rules Generation

`conventions discover` compiles a comprehensive project overview, tech stack, and commands reference directly into `CLAUDE.md`, alongside directory-scoping rules:

```bash
# Generate CLAUDE.md in .claude/ directory
conventions discover --claude

# Or include along with other review formats
conventions discover --format claude
```

### 🧠 Few-Shot Agent Optimization

Path-scoped rule files in `.claude/rules/*.md` and configuration files are optimized specifically for LLM context windows:
*   **Prescriptive Directives:** Observational metrics are converted into imperative instructions (e.g., *"Name functions using snake_case style"*).
*   **Few-Shot Code Examples:** If a convention is detected, the CLI appends the best real-world code snippet from the scanned files, showing the agent exactly how your conventions are implemented.
*   **Token-Optimized Directory Map:** To avoid bloating the main `CLAUDE.md`, the full repository file layout is written to `.claude/directory-map.md` and referenced via a link. It keeps production code folders uncollapsed while collapsing non-essential directories (tests, docs, workflows) to keep token usage optimal.
*   **Dynamic Decision Log & Pitfalls:** Automatically scans git logs, changelogs, release notes, and CI configurations to populate your repository gotchas and architectural decisions, minimizing the need for manual placeholders.

### 🔄 Enhanced via `--init`

Add the `--init` flag to further enrich the generated `CLAUDE.md` using the Claude Code CLI. This pipes the static-analysis output through Claude to populate additional custom gotchas and decision history:

```bash
conventions discover --claude --init
```
*Requires the Claude Code CLI (`npm install -g @anthropic-ai/claude-code`).*

---

## 🌐 Language Support

The engine supports 180+ rules across languages and configurations:

| Language/Platform | Rules | Sample Scanned Patterns |
| :--- | :---: | :--- |
| **Python** | 70+ | typing coverage, docstrings, testing fixtures, stdlib logging, error boundaries, sqlalchemy, context managers, async, dependency injection |
| **Node.js/TypeScript** | 45+ | TypeScript strictness, jest/vitest frameworks, express/fastify api, mongoose, state management, monorepo workspaces, migrations |
| **Go** | 40+ | modules, testimony frameworks, stdlib loggers, channels & goroutines, gRPC structures, wire DI, database configurations |
| **Rust** | 15+ | Cargo configs, tokio async, web frameworks, serialization, macros, unsafe blocks, database ORMs |
| **Generic** | 20+ | GitHub workflows, pre-commit configuration, git hooks, Docker/Kubernetes files, repository layout |

*For the full list of convention IDs, see the [Convention ID Reference](docs/conventions-reference.md).*

---

## 📊 Output Formats & Reports

Scanned results are written to the `.conventions/` folder in multiple formats:

| Format | Output File | Description |
| :--- | :--- | :--- |
| **json** | `conventions.raw.json` | Raw, machine-readable JSON representing all rules, stats, and evidence code blocks. |
| **markdown** | `conventions.md` | Human-readable Markdown summary of all detected rules. |
| **review** | `conventions-review.md` | Audit report with scores (1-5), grouped by rating, with prioritized improvement actions. |
| **html** | `conventions.html` | Interactive dashboard with Light/Dark mode, filtering, search, and expandable evidence code blocks. |
| **sarif** | `conventions.sarif` | Static Analysis Results Interchange Format for GitHub Code Scanning and CI uploads. |

---

## 📈 Rating Scale

Each convention is evaluated and rated on a 1-5 scale:

*   **5 - Excellent:** Best practices followed consistently throughout the codebase.
*   **4 - Good:** Strong alignment with minor improvements possible.
*   **3 - Average:** Room for improvement; inconsistent usage.
*   **2 - Below Average:** Significant improvements needed.
*   **1 - Poor:** Major style or code architecture issues detected.

---

## ⚙️ Configuration

Create a `.conventionsrc.json` configuration file in your repository root to customize behavior:

```json
{
  "languages": ["python", "node"],
  "max_files": 1000,
  "disabled_detectors": ["python_graphql"],
  "disabled_rules": ["python.conventions.graphql"],
  "output_formats": ["json", "markdown", "review", "html"],
  "exclude_patterns": ["**/generated/**", "**/vendor/**"],
  "plugin_paths": ["./custom_rules.py"],
  "min_score": 3.5
}
```

### 🚯 Automatic Exclusions

The CLI respects `.gitignore` rules and automatically excludes:
*   `node_modules/`, `vendor/`, `site-packages/`
*   `venv/`, `.venv/`, `.tox/`, `.nox/`
*   `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`
*   `.git/`, `.svn/`, `.hg/`
*   Build outputs (`build/`, `dist/`, `eggs/`)
*   Examples and docs (`docs/`, `examples/`, `tutorials/`, `demo/`, `samples/`)

---

## 🛡️ CI/CD Integration

Use the CLI as a pull request quality gate. When `min_score` is defined, the scan will fail (exit code 2) if the project-wide average falls below your threshold.

### GitHub Actions Workflow:
```yaml
# .github/workflows/conventions.yml
name: Check Conventions
on: [push, pull_request]

jobs:
  conventions:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install klaussy-repo-conventions
      - run: conventions discover
      - run: cat .conventions/conventions-review.md
```

---

## 🔌 Plugin System

Extend the scanner by creating custom Python detectors and rating rules:

```python
# custom_rules.py
from conventions.detectors.base import BaseDetector, DetectorContext, DetectorResult
from conventions.ratings import RatingRule

class MyCustomDetector(BaseDetector):
    name = "my_custom_detector"
    description = "Detects my custom convention"
    languages = {"python"}

    def detect(self, ctx: DetectorContext) -> DetectorResult:
        result = DetectorResult()
        # Custom detection logic
        return result

# Required exports
DETECTORS = [MyCustomDetector]

# Optional: custom rating rules
RATING_RULES = {
    "custom.my_rule": RatingRule(
        score_func=lambda r: 5 if r.stats.get("metric", 0) > 0.8 else 3,
        reason_func=lambda r, s: f"Custom metric: {r.stats.get('metric', 0):.0%}",
        suggestion_func=lambda r, s: None if s >= 5 else "Improve the custom metric.",
    ),
}
```

Add the plugin path to your `.conventionsrc.json`:
```json
{
  "plugin_paths": ["./custom_rules.py"]
}
```

---

## 🤝 Contributing

Contributions are welcome! To add support for new conventions:
1.  Create a new detector in `src/conventions/detectors/<language>/`
2.  Register it using `@DetectorRegistry.register`
3.  Add rating rules in `src/conventions/ratings.py`
4.  Add tests in `tests/`

---

## ⚖️ License & Governance

*   **License:** MIT
*   **Governance:** `klaussy-repo-conventions` is an open-source project owned and maintained by Dovatech LLC (founded and owned by Stephanie Dover).
