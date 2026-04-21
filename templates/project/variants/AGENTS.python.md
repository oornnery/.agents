# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!--
Python project overlay.
Use for Python applications, services, packages, or internal tools that need
project-specific stack, commands, layout, and validation entrypoints.
-->

## Project Description

<!-- Brief description of what this Python project does and its main constraints -->

## Stack

- **Python**: 3.12+
- **Package Manager**: uv
- **Lint and Format**: Ruff
- **Type Check**: ty
- **Tests**: pytest
- **Validation**: Pydantic
- **HTTP Client**: HTTPX
<!-- - **Persistence**: SQLModel / SQLAlchemy / PostgreSQL -->

## Quick Commands

```bash
uv sync                          # Install dependencies
uv run python -m myapp           # Start the app entrypoint
uv run task check                # Run full validation
uv run pytest -v                 # Run the test suite
```

## Validation Entry Points

```bash
uv run ruff format --check .
uv run ruff check .
uv run rumdl check .
uv run ty check src
uv run pytest -v
```

If the project exposes task aliases, prefer them when they map cleanly to the
real commands.

## Python Onboarding Focus

- treat `pyproject.toml` as the primary source of truth
- identify the real app entrypoint, package root, and test layout before editing
- inspect how config is loaded and where environment-specific behavior lives
- confirm whether the project is app-first, library-first, CLI-first, or mixed
- inspect recent commits to understand current momentum and local conventions

## Toolchain Verification

```bash
uv --version
ruff --version
ty --version
python --version
```

## Layout

```text
src/myapp/
├── core/            # reusable business logic and shared rules
├── services/        # orchestration and feature workflows
├── models/          # data models and typed structures
├── database/        # persistence, sessions, repositories, queries
├── api/             # HTTP entrypoints when present
├── cli/             # CLI entrypoints when present
└── views/           # templates or rendering adapters when present

tests/
├── unit/
├── integration/
└── e2e/
```

## Python-Specific Defaults

- keep IO at the edges and core logic easy to test
- prefer explicit types on public functions and boundaries
- validate external input at boundaries, not in internal helpers
- use `pathlib`, `logging`, and parameterized queries
- prefer sync code by default; use async only when the full path benefits from it
- keep modules focused and package boundaries obvious

## Preferred Libraries

- use `Pydantic` for validated external data, typed settings, and explicit
  contracts
- use `HTTPX` for sync and async HTTP work instead of older HTTP clients
- use `Parsel` when the project needs HTML or XML extraction
- use `Polars` when the project needs dataframe-style analytics or tabular data
  processing
- use `SQLModel` when the project benefits from typed SQLAlchemy-based models
  and schema-like ergonomics for persistence

## Toolchain and Package Rules

- use `uv` as the single package and environment workflow
- add runtime dependencies with `uv add` and development dependencies with
  `uv add --dev`
- use `uv run` for project commands and `uvx` for one-off tools outside the
  project environment
- keep `pyproject.toml` and `uv.lock` as the source of truth for installs
- prefer task aliases only when they stay readable and map cleanly to the real
  commands
- keep packaging metadata, entrypoints, and dependency groups explicit when the
  project ships a library or CLI

## UV Inline Scripts

For true single-file scripts, prefer inline metadata over a full package layout
when the script is small and standalone.

Use this pattern:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx>=0.27",
#   "rich>=13.0",
# ]
# ///
```

Optional shebang:

```python
#!/usr/bin/env -S uv run
```

Promote the script to a real project once it grows multiple modules, multiple
commands, or shared reusable logic.

## Structure and Boundary Rules

- keep package boundaries obvious and module responsibilities focused
- keep public imports deliberate; use `__all__` when a module exposes a public
  surface
- keep routes, CLI entrypoints, jobs, and adapters thin
- move reusable logic into `core/` or `services/`
- keep schemas, settings, and persisted models separate when their shapes differ
- do not leak ORM, transport, or framework types into reusable logic unless the
  project is intentionally framework-bound
- prefer absolute imports when they improve clarity

## Pythonic Defaults

- prefer small, well-named functions over class-heavy designs
- use dataclasses or Pydantic models when structure matters; use plain classes only when behavior justifies them
- prefer explicit return types at boundaries
- use `Enum` for fixed sets instead of free-form strings
- keep imports clean and absolute when practical
- use context managers for files, connections, and temporary resources
- raise specific exceptions that are useful to callers

## Typing and Data Modeling Rules

- type public functions, boundary contracts, and important internal helpers
- use `Protocol` for structural boundaries and lightweight interfaces
- use `TypedDict` when dict keys are known and still need mapping semantics
- use dataclasses for plain internal data and Pydantic models for validated
  external shapes
- contain `Any`, unchecked casts, and untyped third-party surfaces at the edge
- prefer narrowing, helper types, and explicit conversion over informal
  assumptions
- use `Annotated` or semantic wrappers when raw primitives become ambiguous

## Data, Config, and Runtime Rules

- keep settings and secrets outside the codebase
- make config loading explicit and typed
- keep schema models separate from persistence models when the shapes differ
- treat file system, subprocess, database, and network calls as edge concerns
- default to sync code unless async clearly improves the end-to-end path

## Validation, Error, and Design Rules

- validate external input at boundaries only, then pass typed values inward
- keep validation, parsing, and normalization close to the edge
- raise exceptions that match the real failure and help the caller react
- make partial failure behavior explicit in batch, retry, or streaming flows
- prefer composition over inheritance-heavy designs
- introduce abstractions only when duplication is real and repeating
- avoid god modules, hidden global state, flag-argument APIs, and convenience
  wrappers that hide side effects
- keep retry, timeout, and backoff policy centralized instead of scattering it
  through business logic

## Async, Job, and Resource Rules

- default to sync code; switch to async only when the full path benefits from it
- if async is needed, keep the call path async end-to-end
- keep background jobs idempotent and explicit about ownership, retries, and
  lifecycle
- use context managers for files, connections, and temporary resources
- make cleanup, cancellation, and timeout behavior visible
- treat streaming responses and long-lived resources as explicit lifetime
  problems, not incidental details

## Logging and Error Handling

- use `logging` for application logs and structured context
- avoid `print` except for intentional CLI output
- log enough to debug failures without leaking secrets or full payloads
- fail loudly and specifically instead of hiding broken states

## Observability, Performance, and Testing Rules

- keep logging structured and consistent across services, jobs, and handlers
- add metrics or traces when the project needs operational visibility, but keep
  the instrumentation at the edges
- profile and measure before optimizing; do not optimize by guesswork
- treat database round-trips, repeated parsing, large object copies, and
  unbounded loops as first suspects
- test behavior, edge cases, error paths, and historical regressions
- keep many focused unit tests, a smaller set of integration tests, and only a
  few end-to-end tests
- mock external boundaries, not the logic under test

## Python Review Focus

- look for hidden IO inside reusable logic
- look for weak or missing boundary validation
- look for ORM, transport, or framework types leaking into shared code
- look for uncontained `Any`, unchecked casts, or type-eroding helpers
- look for retries, timeouts, cleanup, and partial failure behavior hidden in
  business code
- look for tests that overfit implementation details instead of behavior

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

| Symptom                 | Check                                      |
| ----------------------- | ------------------------------------------ |
| `TypeError`             | wrong type passed; check function signature|
| `AttributeError`        | missing attribute; check object type       |
| `ImportError`           | missing dependency or circular import      |
| `KeyError`              | missing dict key; check input data shape   |
| `TimeoutError`          | slow I/O or infinite loop                  |
| validation failure      | model or schema mismatch; check payload    |
| flaky test              | shared state, timing, or ordering issue    |
| works locally, fails CI | env difference: deps, Python version, or OS|

## When the Project Includes FastAPI

- use `Annotated` for request parameters and dependencies
- keep routes thin and move orchestration into `services/` or `core/`
- use explicit return types or `response_model` for public handlers
- prefer `def` instead of `async def` when the internals block
- do not run blocking file, database, or network work inside async handlers
- keep auth, validation, uploads, callbacks, and error shapes explicit at the
  edge

## Python Checklist

### Project Setup

- [ ] `pyproject.toml` is the source of truth
- [ ] dependencies and dev dependencies are explicit
- [ ] validation entrypoints are clear
- [ ] config and secrets stay out of source code

### Code Structure

- [ ] core logic stays reusable and testable
- [ ] services orchestrate workflows without hiding side effects
- [ ] models and schemas are explicit
- [ ] database and external IO stay at the edges
- [ ] package boundaries and public imports stay intentional

### Quality Gates

- [ ] `ruff format --check`
- [ ] `ruff check`
- [ ] `rumdl check`
- [ ] `ty check`
- [ ] `pytest`

### Correctness and Safety

- [ ] boundary validation is explicit
- [ ] file paths and external input are validated
- [ ] parameterized queries are used
- [ ] retries, timeouts, and cleanup behavior are explicit
- [ ] logging is structured and useful
- [ ] errors are specific and actionable

### Testing

- [ ] unit tests cover core logic
- [ ] integration tests cover database and external systems
- [ ] regression tests protect historical failures
- [ ] fixtures stay focused and maintainable
- [ ] performance-sensitive paths are measured before optimization

## Testing Focus

<!-- - business rules -->
<!-- - validation and error paths -->
<!-- - external integration boundaries -->
<!-- - regression tests for known failure modes -->

## Environment Variables

<!-- | Variable | Description | Required | -->
<!-- |----------|-------------|----------| -->

## Project-Specific Guardrails

<!-- - Keep public imports stable -->
<!-- - Do not bypass typed settings -->
<!-- - Avoid framework-specific logic in `core/` -->
