---
name: python
description: Python guidance for project onboarding, uv, typing, testing, async, configuration, packaging, observability, resilience, resource management, FastAPI conventions, and common debug/build-fix patterns. Load when writing, reviewing, debugging, or maintaining Python code.
---

# Python

Policy-level Python guidance. Load one focused ref for deep detail; keep this file as router + defaults.

## Reference Map

| Need                    | Ref                                      |
| ----------------------- | ---------------------------------------- |
| uv, deps, venv, Python  | `references/uv.md`                       |
| package/module layout   | `references/structure.md`                |
| env/settings/secrets    | `references/config.md`                   |
| packaging/publishing    | `references/packaging.md`                |
| style/ruff/naming       | `references/style.md`                    |
| typing/protocols        | `references/types.md`                    |
| validation/exceptions   | `references/errors.md`                   |
| design/SRP/composition  | `references/design.md`                   |
| anti-pattern review     | `references/anti-patterns.md`            |
| asyncio/concurrency     | `references/async.md`                    |
| jobs/workers/queues     | `references/jobs.md`                     |
| resources/cleanup       | `references/resources.md`                |
| retries/timeouts        | `references/resilience.md`               |
| logs/metrics/tracing    | `references/observability.md`            |
| profiling/perf          | `references/perf.md`                     |
| pytest/testing          | `references/tests.md`                    |

## Assets

- `assets/project/pyproject.toml`
- `assets/project/src/myapp/main.py`
- `assets/project/src/myapp/settings.py`
- `assets/project/tests/test_main.py`
- `assets/project/scripts/report.py`

## Onboarding

Detect:

```bash
ls pyproject.toml 2>/dev/null
```

Before edit:

1. verify tools
2. find validation entrypoints
3. inspect layout/config/tests
4. check momentum: `git log --oneline -10`

Validation discovery order:

1. task aliases in `pyproject.toml`
2. direct `uv run ...`
3. README/scripts
4. CI config

## Default Stack

- Python 3.12+
- `uv`
- `ruff`
- `ty`
- `pytest`
- `rumdl`
- `rtk`

## Validation

```bash
uv run ruff format --check .
uv run ruff check .
uv run rumdl check .
uv run ty check
uv run pytest -v
```

Prefer task aliases when repo defines them:

```bash
uv run task lint
uv run task fmt
uv run task test
uv run task test-cov
```

Verify tools:

```bash
uv --version
ruff --version
ty --version
python --version
```

Install deps:

```bash
uv sync
```

## Core Defaults

- use `uv`, `uv run`, `uv add`; avoid direct `pip`
- format with `ruff`
- prefer `pathlib`, f-strings, absolute imports
- type public APIs; use `Protocol` at boundaries; contain `Any`
- externalize config/secrets with typed settings loaded at startup
- validate external input at boundaries; convert raw payloads early
- keep IO at edges; avoid leaking ORM/transport types
- prefer composition/focused modules over clever abstractions
- default sync unless real concurrent I/O pressure exists
- keep async path async end-to-end when used
- centralize retries, timeouts, cleanup
- make background jobs idempotent and explicit about state/ownership
- keep observability structured and outside core business logic
- test behavior and boundaries; avoid framework-heavy tests when simple tests suffice
- optimize only after measuring bottleneck

## Build-Fix

Order:

1. format
2. lint
3. markdown
4. typing
5. tests

After each fix, rerun failing check. Stop/report if fix needs architecture change.

Common fixes:

| Tool   | Signal                   | Fix                                  |
| ------ | ------------------------ | ------------------------------------ |
| ruff   | formatting/import/style  | format or remove/fix code            |
| ty     | type/import mismatch     | fix type, import path, or dependency |
| pytest | assertion/import/fixture | fix logic, path, or fixture          |

## Debug

1. reproduce exactly
2. record env
3. read traceback bottom-up
4. inspect `git log --oneline -10` and `git diff`
5. isolate boundary
6. use `git bisect` if regression likely
7. confirm fix with failing test/command
8. remove temp debug/breakpoints

Rules: do not guess first; fix root cause; one hypothesis at time; do not silence with broad `try/except`; do not change tests to match bug.

## FastAPI Cues

- use `Annotated` for `Path`, `Query`, `Header`, `Depends`
- reusable dependency aliases only when repeated signatures simplify
- no ellipsis `...` for required FastAPI/Pydantic fields
- explicit return type or `response_model`
- router-level `prefix`, `tags`, dependencies
- default `def` if internals may block
- no blocking code inside async handlers
- prefer HTTPX over Requests
- no deprecated `ORJSONResponse`/`UJSONResponse` performance crutch
- no `RootModel` when normal typed structure is enough

## Review Focus

- correctness: edge cases, error paths, races
- security: boundary validation, secrets, injection, auth
- performance: blocking async, N+1, unbounded loops
- maintainability: SRP, dead code, magic values, noisy comments
- conventions: naming, style, project patterns

Skip style already enforced by tools.

## Refactoring

- preserve behavior
- no hidden feature work
- do not rewrite stable code just because old
- reduce complexity only with clear maintenance gain
- one logical change at time

## Workflow Cues

- API contract shape -> pair `design`
- architecture/boundaries -> pair `arch`
- test-first or failure diagnosis -> pair `quality`
