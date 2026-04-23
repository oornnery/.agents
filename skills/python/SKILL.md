---
name: python
description: Python guidance for project onboarding, uv, typing, testing, async, configuration, packaging, observability, resilience, resource management, FastAPI conventions, and common debug and build-fix patterns. Load when writing, reviewing, debugging, or maintaining Python code.
---

# Python

## Reference Map

Core guidance here for default workflow. Load only the ref that matches the task. Each ref is self-contained.

### Project and Toolchain

- `references/uv.md` -- dependency management, environments, Python installs,
  lockfiles, and advanced `uv` workflows
- `references/structure.md` -- module layout, package boundaries, and
  public API structure
- `references/config.md` -- environment variables, typed settings,
  secrets, and config loading
- `references/packaging.md` -- build metadata, packaging layouts, publishing,
  and advanced packaging patterns

### Implementation and Correctness

- `references/style.md` -- formatting, linting, naming, docstrings, and
  style defaults
- `references/types.md` -- type hints, generics, protocols, narrowing,
  and checker guidance
- `references/errors.md` -- boundary validation, exception design, and
  partial failure handling
- `references/design.md` -- KISS, SRP, composition, layering, and
  dependency injection
- `references/anti-patterns.md` -- review checklist for common Python mistakes

### Runtime Behavior

- `references/async.md` -- asyncio, concurrency, cancellation, and
  non-blocking IO
- `references/jobs.md` -- workers, queues, idempotency, and job
  orchestration
- `references/resources.md` -- context managers, cleanup, streaming,
  and lifetime control
- `references/resilience.md` -- retries, backoff, timeouts, and fault-tolerance
  patterns
- `references/observability.md` -- structured logging, metrics, tracing, and
  production diagnostics, instrumentation, and logging bridges
- `references/perf.md` -- profiling, benchmarking, and optimization
  techniques

### Testing

- `references/tests.md` -- pytest patterns, fixtures, mocking, coverage, and
  advanced testing workflows

## Assets

Small real project shapes:

- `assets/project/pyproject.toml` -- repo-aligned Python toolchain config
- `assets/project/src/myapp/main.py` -- a small application entrypoint
- `assets/project/src/myapp/settings.py` -- typed settings example
- `assets/project/tests/test_main.py` -- a matching test module
- `assets/project/scripts/report.py` -- a standalone `uv` script example

## Policy

Keep this file lean and policy-level.

- Here: onboarding, stack defaults, validation order, core defaults, debug workflow, build-fix order, review cues, FastAPI defaults.
- Refs: tool-specific setup, long examples, advanced variants, framework-specific patterns.
- Load one focused ref over growing this file.
- Guidance for one theme goes in that theme's ref.

## Project Onboarding

Detect a Python project:

```bash
ls pyproject.toml 2>/dev/null
```

For this stack, `pyproject.toml` usually means a `uv`-managed Python project.

Before editing:

1. verify toolchain
2. identify validation entrypoints
3. inspect layout, config, test setup
4. check momentum: `git log --oneline -10`

Check validation entrypoints in this order:

1. task aliases in `pyproject.toml`
2. direct `uv run` commands
3. project README or scripts
4. CI config if still unclear

Primary refs: `references/uv.md`, `references/structure.md`,
`references/config.md`, and `references/packaging.md`.

## Map the Project

Before changing: repo layout, architecture style, config loading, test location, recent commits.

## Default Stack

- language: Python 3.12+
- package manager: `uv`
- linter and formatter: `ruff`
- type checker: `ty`
- test runner: `pytest`
- markdown lint: `rumdl`
- token optimizer: `rtk`

## Validation Order

Validate in order and fail fast:

```bash
uv run ruff format --check .
uv run ruff check .
uv run rumdl check .
uv run ty check
uv run pytest -v
```

If the project exposes task aliases, prefer them:

```bash
uv run task lint
uv run task fmt
uv run task test
uv run task test-cov
```

Primary refs: `references/style.md`, `references/types.md`, and
`references/tests.md`.

## Toolchain Verification

```bash
uv --version
ruff --version
ty --version
python --version
```

## Install Dependencies

Use the native package manager:

```bash
uv sync
```

## Core Defaults

Keep these as the default stance before loading deeper refs:

- use `uv`, `uv run`, and `uv add`; avoid direct `pip` workflows -- see
  `references/uv.md`
- format with `ruff`, keep naming boring and descriptive, and prefer
  `pathlib`, f-strings, and absolute imports -- see
  `references/style.md`
- type public APIs, use `Protocol` at boundaries, and keep `Any` contained --
  see `references/types.md`
- externalize config and secrets with typed settings loaded explicitly at
  startup -- see `references/config.md`
- validate external input at system boundaries and convert raw strings or
  payloads into typed domain values early -- see
  `references/errors.md`
- keep IO at the edges, avoid leaking ORM or transport types, and prefer
  composition and focused modules over clever abstractions -- see
  `references/design.md` and `references/structure.md`
- default to sync code unless there is real concurrent I/O pressure; when async
  is needed, keep the call path async end-to-end -- see `references/async.md`
- centralize retries, timeouts, and resource cleanup instead of scattering them
  through business code -- see `references/resilience.md`,
  `references/resources.md`, and `references/anti-patterns.md`
- make background work idempotent and explicit about job state, retries, and
  ownership boundaries -- see `references/jobs.md`
- keep observability structured and separate from core business logic -- see
  `references/observability.md`
- test behavior, isolate boundaries, and prefer clear unit and integration
  coverage over framework-heavy tests -- see `references/tests.md`
- use `references/perf.md` only after measuring a real bottleneck; do
  not optimize by guesswork

## Build-Fix Workflow

Fix failures in this order:

1. formatting
2. lint
3. markdown
4. typing
5. tests

After each fix, re-run the failing check.
Stop and report if the fix requires architectural change.

Primary refs: `references/style.md`, `references/types.md`,
`references/tests.md`, and `references/uv.md`.

## Common Build Fixes

| Tool        | Error Pattern             | Fix                                  |
| ----------- | ------------------------- | ------------------------------------ |
| ruff format | file would be reformatted | `uv run ruff format <file>`          |
| ruff check  | import unused             | remove the import                    |
| ruff check  | missing type annotation   | add annotation                       |
| ty          | incompatible type         | fix type or add cast                 |
| ty          | module not found          | add dependency or fix import path    |
| pytest      | assertion error           | fix logic or update expected value   |
| pytest      | import error              | fix module path or add `__init__.py` |
| pytest      | fixture not found         | add `conftest.py`                    |

## Common Debug Patterns

| Symptom                 | Check                                       |
| ----------------------- | ------------------------------------------- |
| `TypeError`             | wrong type passed; check function signature |
| `AttributeError`        | missing attribute; check object type        |
| `ImportError`           | missing dependency or circular import       |
| `KeyError`              | missing dict key; check input data shape    |
| `TimeoutError`          | slow IO or infinite loop                    |
| `ValidationError`       | Pydantic model mismatch; check payload      |
| flaky test              | shared state, timing, or ordering issue     |
| works locally, fails CI | env difference: deps, Python version, or OS |

## Debugging Workflow

1. reproduce the failure exactly
2. record environment details
3. read the traceback from the bottom up
4. inspect recent changes with `git log --oneline -10` and `git diff`
5. isolate the failure boundary
6. if regression is suspected, use `git bisect`
7. confirm the fix with the failing test or command
8. remove temporary debug statements and `breakpoint()` calls

Rules:

- do not guess before reproducing
- fix the root cause, not only the symptom
- prefer one hypothesis at a time
- do not add broad `try/except` to silence errors
- do not change tests to match broken behavior
- do not mix bug fixes with refactoring

Primary refs: `references/observability.md`, `references/perf.md`,
`references/async.md`, and `references/anti-patterns.md`.

## FastAPI Conventions

Keep this section short and framework-adjacent. For async, validation, typing,
and observability details, load `references/async.md`, `references/errors.md`,
`references/types.md`, and
`references/observability.md`.

- prefer `Annotated` for `Path`, `Query`, `Header`, and `Depends`
- create reusable dependency aliases when they simplify repeated signatures
- do not use ellipsis `...` for required FastAPI or Pydantic fields
- prefer explicit return types or `response_model` to validate and filter output
- use router-level `prefix`, `tags`, and shared dependencies on the router itself
- default to `def` rather than `async def` when internals may block
- do not run blocking code inside async handlers
- prefer HTTPX over Requests
- do not use deprecated `ORJSONResponse` or `UJSONResponse` shortcuts as a performance crutch
- do not use Pydantic `RootModel` when a normal typed structure is enough

## Review Focus

When reviewing Python changes, prioritize:

- correctness: edge cases, error paths, race conditions
- security: boundary validation, secrets, injection, auth checks
- performance: blocking in async paths, N+1 queries, unbounded loops
- maintainability: SRP, dead code, magic values, noisy comments
- convention adherence: naming, style, and existing project patterns

Skip trivial style feedback already enforced by tooling.

## Refactoring Rules

- preserve external behavior
- do not sneak in feature work
- do not rewrite stable code just because it looks old
- reduce complexity only where readability or maintenance clearly improve
- keep one logical change at a time

## Workflow Cues

- if the work is mostly API contract shape, pair this with `design`
- if the work is mostly architecture and boundaries, pair this with `arch`
- if the work is test-first or failure-diagnosis focused, pair this with `quality`
