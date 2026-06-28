# Agent-Context Output Improvement Plan

> Working plan to make klaussy's generated agent-context files (`CLAUDE.md`,
> `.claude/rules/`, reports) more correct and more useful to coding agents.
> This is a living checklist — update status as steps land so work can resume
> after an interruption.

## Context / motivation

klaussy scans a target repo and emits agent-context files. Review of the
`examples/fastapi` and `examples/httpx` outputs surfaced a core flaw: the
generated `CLAUDE.md` **conflates "how the code currently is" (descriptive) with
"how an agent should write code" (prescriptive).** Detected anti-patterns and
false positives land in the "Conventions" section — the exact place an agent
reads to learn what to imitate.

Evidence: `examples/httpx/CLAUDE.md` lists
`Password hashing: hashlib (not recommended)` under **Conventions**. It is both
(a) a false positive (httpx uses `hashlib` for HTTP Digest auth, not passwords)
and (b) an anti-pattern presented as something to mirror.

The scoring layer (`src/conventions/ratings.py`, public API
`rate_convention(rule) -> (score:int 1-5, reason, suggestion)` and
`get_score_label(score)`) already grades every convention, but
`src/conventions/outputs/claude.py` never uses it to gate or rank what lands in
`CLAUDE.md`.

## Plan (multi-part)

### 1. Score-gate Conventions + add "Anti-patterns present" section  ✅ DONE
- In `_build_conventions_section` (`claude.py:~870`), rate each project-wide
  rule via `rate_convention`. Keep score >= 3 in **Conventions (mirror these)**.
- Add a new `_build_antipatterns_section` for score <= 2 rules, rendered as
  **Anti-patterns present (do not imitate; fix on touch)**, including each
  rule's actionable `suggestion`.
- Wire the new section into `generate_claude_md` right after Conventions.
- Update the top-of-file docstring (currently says "filtering by signal quality
  rather than score") to reflect that score now gates Conventions vs Anti-patterns.
- Tests + regenerate `examples/` to confirm the hashlib line moves out of
  Conventions.

### 2. Fix the false-positive class (domain guards on detectors)  ✅ DONE
- Root-cause the `password_hashing` detector: it flags any `hashlib` use.
  Add a domain guard (only flag when near auth/password/user context).
- Audit sibling pattern-only detectors for the same over-matching failure mode.

**Root cause:** the old gate counted generic tokens (`hash`, `verify`,
`authenticate`, `login`) in function names, which collide with httpx's SSL
`verify=`, HTTP `Auth`, and `__hash__`; combined with `hashlib` (used for
*digest auth*), httpx tripped the gate and got a CRITICAL "weak password
hashing" claim.

**Fix (`detectors/python/security.py`):** replaced the loose gate. Dedicated
libs (argon2/bcrypt/passlib) are reported on sight; a bare `hashlib` import is
only reported as weak password hashing when an explicit password-*storage*
function exists (`_PASSWORD_STORAGE_FUNC_RE` matches `set_password`,
`hash_password`, `check_password`, `password_hash`, etc., and excludes
digest/SSL helpers). Trades a little recall for precision — correct for a
high-stakes security claim. 3 new tests in
`tests/detectors/test_python_security.py` (httpx-like → not flagged; real
password storage → weak; bcrypt → good). 332 total pass, ruff clean.

**Sibling audit:** most detectors match on *library import names*
(kafka/passlib/dynaconf) — high precision, no action. Residual generic-token
matchers to tighten later (lower stakes; step-1 score-gating already mitigates):
`resilience.py:170` (`get`/`post`/`request` vs call names — highest residual
risk), `api_schema.py:299` (`response`/`result`/`wrapper` vs class names),
`architecture.py:235` (`session`/`engine`/`model`).

**Examples:** regenerated from source (see workflow below). `password_hashing`/
`hashlib` is now gone from every example file — verified end-to-end against real
httpx source. httpx `CLAUDE.md` is net -1 line vs baseline (the bogus hashlib
convention removed); it now has no Anti-patterns section because, with the false
positive suppressed, httpx genuinely has no <=2-scoring conventions.

### 3. Raise Decision Log fidelity (or omit)  ✅ DONE
- `examples/httpx/CLAUDE.md:43` is a truncated mid-sentence changelog fragment.
- Parse version + date, dedupe, require complete sentences; drop low-quality
  entries instead of emitting broken markdown.

**Fix (`detectors/generic/history.py`):** the changelog scanner now (a) tracks
the nearest `## <version> (date)` heading and prefixes each entry with
`v<version> (date): ` for "as of" context; (b) cleans markdown — links
`[txt](url)` → `txt`, strips emphasis/backticks and trailing `...`/`…`/`*`
artifacts; (c) keeps only the first complete sentence, length-capped at a word
boundary (no mid-word cuts); (d) drops entries shorter than 15 chars. Added
`_clean_changelog_text`, `_first_complete_sentence`, `_format_decision`,
`_parse_version_header`. Updated `test_history.py` assertions to the new format
and added `test_changelog_decision_fidelity`. 333 tests pass, ruff clean.

**Result on real data:** httpx decisions went from
`Changelog breaking change: ...deprecated...*` (mid-sentence, no version) to
`v0.28.0 (28th November, 2024): The deprecated proxies argument has now been
removed.` fastapi dropped `PR [#..](url) by [@..](url)` link noise →
`v0.137.0 (2026-06-14): 🔥 Remove slim package stub, deprecated for a while.`

**Known limitation:** the scanner still selects whichever bullet matches a
keyword, so an explanatory sub-bullet can be chosen over the true decision
headline (httpx's first entry is prose). Perfect changelog-structure awareness
is out of scope; fidelity goal (complete sentence + version/date + clean
markdown) is met.

### 4. Emit an Architecture summary for library/CLI repos  ✅ DONE
- `_build_architecture_section` only fires when API routes exist, so libraries
  (httpx) get no architecture summary — only the raw directory map.
- Derive a "core modules + responsibilities / public API surface / entry points"
  map from the already-computed `import_graph` stats.

**Two root causes fixed:**
1. The import-graph rule was being path-bucketed (its evidence sits under one
   package dir, e.g. `httpx/**/*.py`) and dropped from CLAUDE.md. Added
   `_ALWAYS_PROJECT_WIDE_SUFFIXES` (import_graph, endpoint_chains,
   service_dependencies, api_routes, monorepo, db_entities) so whole-repo
   structural artifacts always render in the root CLAUDE.md.
2. There was no core-module map at all.

**Implementation:**
- `index.py`: capture `FileIndex.module_docstring` via `ast.get_docstring`.
- `data_flow.py`: `_build_core_modules` ranks the most-depended-upon modules,
  counting **production importers only** (via the deduped `adj`) so test/script
  fan-in doesn't masquerade as centrality; excludes `__init__.py` facades and
  test/docs/script modules (`_NONPROD_DIRS`). `_module_responsibility` takes the
  first sentence of the module docstring, falling back to a humanized filename.
- `claude.py`: `_build_core_modules_lines` renders a `### Core Modules`
  subsection; import-graph `### Key Patterns` now shows the circular-dep count
  even without cycle examples.
- Tests: `test_core_modules_with_responsibilities` (detector, incl. docstring +
  fallback + facade exclusion), `test_core_modules_section_for_library`
  (rendering + project-wide bucketing). 335 pass, ruff clean.

**Result:** httpx (a library, no API routes) now gets an Architecture section —
`httpx/_types.py — Type definitions… (9 dependents)`, `_exceptions.py — Our
exception hierarchy:`, etc. fastapi's map is now production-only (`exceptions`,
`openapi/models`, `types`, `datastructures`…); the earlier `testclient.py` (436
dependents, all from tests), `tests/utils.py`, and `scripts/*` pollution is gone.

**Deferred:** public API surface / entry points (`__all__`, console_scripts)
were in scope but not implemented — core-modules map delivers the core value;
note this as a future enhancement.

### 5. Improve Known Pitfalls recall  ✅ DONE
- httpx produced zero pitfalls despite it being a headline feature.
- Derive pitfalls from: low-score (1-2) conventions, CI `continue-on-error`,
  circular deps (already detected), in addition to changelog scraping.

**Implementation (`claude.py`):** added `_collect_pitfalls(output)` aggregating
from multiple sources and de-duplicating: (a) **circular import dependencies**
from the import graph's `cycle_count` (new — the highest-recall win), and (b)
the history detector's findings (flaky CI / `continue-on-error`, changelog
gotchas, workarounds). Cap raised 5→7. Circular deps were moved out of the
Architecture/Key Patterns render into Known Pitfalls (no duplication).

**Scope decision:** low-score (1-2) conventions are deliberately **excluded**
here — step 1 already surfaces them in the dedicated "Anti-patterns Present"
section, so routing them into pitfalls too would double-report. Known Pitfalls
now covers *structural/process* gotchas; Anti-patterns covers *code-style*
conventions. Complementary, non-overlapping.

**Result:** httpx went from **zero** pitfalls to
`16 circular import dependencies detected — watch import order…`. fastapi now
aggregates `20 circular import dependencies…` + `pre-commit.yml contains steps
allowed to fail (continue-on-error: true)`. Tests:
`test_known_pitfalls_aggregates_multiple_sources`,
`test_known_pitfalls_placeholder_when_none`. 337 pass, ruff clean.

## Regenerating examples

`scripts/regen-examples.sh` clones the latest httpx + fastapi, runs the scanner
with all formats, and copies artifacts into `examples/<name>/`. Decision: track
**latest upstream** (so per-step diffs may include upstream drift; in practice
both repos are stable and drift is mostly the `Generated:` timestamp lines).
**Run this after every step** so examples reflect the current code. The source
repos are not vendored — the script clones into `<name>_repo/` and cleans up.

## Status log
- 2026-06-28: Plan created. Starting step 1.
- 2026-06-28: Step 1 complete. `claude.py` now rates each project-wide
  convention via `rate_convention`; score >= 3 stays under **Conventions**,
  score <= 2 moves to a new **Anti-patterns Present** section (with the rule's
  fix suggestion). Added `_select_project_wide_conventions` helper +
  `_build_antipatterns_section`, wired after Conventions in `generate_claude_md`,
  updated the module docstring, added 2 tests (68 in test_claude_output, 329
  total pass), ruff clean. Regenerated `examples/httpx/CLAUDE.md` (hashlib line
  moved to anti-patterns); `examples/fastapi/CLAUDE.md` unchanged (no low
  scorers in its convention set). Next: step 2.
- 2026-06-28: Step 2 complete. Added a domain guard to the `password_hashing`
  detector so `hashlib` is only flagged as weak password hashing with an
  explicit password-storage function present (httpx digest-auth no longer
  misreported). Audited siblings (see step 2 notes). 332 tests pass, ruff clean.
  Next: step 3 (Decision Log fidelity).
- 2026-06-28: Added `scripts/regen-examples.sh` (clone-latest workflow) and
  regenerated examples from real httpx/fastapi source. Confirms steps 1+2 on
  real data: hashlib false positive gone everywhere; httpx CLAUDE.md net -1 line
  vs baseline; fastapi diff is timestamp-only. Will re-run regen after each
  subsequent step.
- 2026-06-28: Step 3 complete. Rewrote the changelog scanner in
  `history.py` for decision-log fidelity (version/date context, markdown
  cleanup, first-sentence extraction, quality gate). 333 tests pass, ruff clean.
  Regenerated examples: httpx/fastapi decision logs now carry `v<version>
  (date):` prefixes with no truncated/`...*`/link artifacts. Next: step 4
  (architecture summary for library/CLI repos).
- 2026-06-28: Step 4 complete. Added a Core Modules architecture map (module
  docstrings + production-only fan-in) and made structural artifacts
  project-wide so libraries/CLIs get an Architecture section. 335 tests pass,
  ruff clean. Regenerated examples: httpx now has an Architecture section;
  fastapi's core modules are production-only (test/script pollution removed).
  Next: step 5 (Known Pitfalls recall).
- 2026-06-28: Step 5 complete. Known Pitfalls now aggregates circular
  dependencies (import graph) + history findings, deduped; low-score conventions
  intentionally excluded (covered by Anti-patterns Present). 337 tests pass, ruff
  clean. Regenerated examples: httpx pitfalls went 0 → 1 (circular deps); fastapi
  shows circular deps + flaky CI. **All 5 plan steps done.**
