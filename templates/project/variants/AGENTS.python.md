# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!--
Python project overlay.
Use for Python apps, services, packages, internal tools needing
project-specific stack, commands, layout, valid entrypoints.
-->

## Project Description

<!-- Brief description of what this Python project does and its main constraints -->

## Stack

- **Python**: 3.12+
- **Package Manager**: uv
- **Lint and Format**: Ruff
- **Type Check**: ty
- **Tests**: pytest
- **Valid**: Pydantic
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

Prefer task aliases when they map cleanly to real commands.

## Python Onboarding Focus

- `pyproject.toml` = source of truth
- identify app entrypoint, package root, test layout before editing
- inspect config loading, env-specific behavior location
- confirm project type: app-first, library-first, CLI-first, or mixed
- inspect recent commits for momentum and local conventions

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

- IO at edges, core logic testable
- explicit types on public fns and boundaries
- validate external input at boundaries, not internal helpers
- use `pathlib`, `logging`, parameterized queries
- sync by default; async only when full path benefits
- focused modules, obvious package boundaries

## Preferred Libraries

- `Pydantic` for validated external data, typed settings, explicit contracts
- `HTTPX` for sync/async HTTP over older clients
- `Parsel` for HTML/XML extraction
- `Polars` for dataframe-style analytics or tabular data processing
- `SQLModel` for typed SQLAlchemy-based models and schema-like persistence ergonomics

## Toolchain and Package Rules

- `uv` as single package/env workflow
- `uv add` for runtime deps, `uv add --dev` for dev deps
- `uv run` for project commands, `uvx` for one-off tools outside project
- `pyproject.toml` and `uv.lock` = source of truth for installs
- task aliases only when readable and map cleanly to real commands
- packaging metadata, entrypoints, dep groups explicit when shipping library or CLI

## UV Inline Scripts

For single-file scripts, prefer inline metadata over full package layout when script is small and standalone.

Pattern:

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

Promote to real project once it grows multiple modules, commands, or shared logic.

## Structure and Boundary Rules

- obvious package boundaries, focused module responsibilities
- deliberate public imports; use `__all__` for public surface
- routes, CLI entrypoints, jobs, adapters stay thin
- reusable logic in `core/` or `services/`
- schemas, settings, persisted models separate when shapes differ
- no ORM, transport, or framework types in reusable logic unless intentionally framework-bound
- absolute imports when they improve clarity

## Pythonic Defaults

- small well-named fns over class-heavy designs
- dataclasses or Pydantic models when structure matters; plain classes only when behavior justifies
- explicit return types at boundaries
- `Enum` for fixed sets, not free-form strings
- clean absolute imports when practical
- context managers for files, connections, temp resources
- raise specific exceptions useful to callers

## Typing and Data Modeling Rules

- type public fns, boundary contracts, important internal helpers
- `Protocol` for structural boundaries and lightweight interfaces
- `TypedDict` when dict keys known and need mapping semantics
- dataclasses for plain internal data, Pydantic for validated external shapes
- contain `Any`, unchecked casts, untyped third-party surfaces at edge
- prefer narrowing, helper types, explicit conversion over informal assumptions
- `Annotated` or semantic wrappers when raw primitives become ambiguous

## Data, Config, and Runtime Rules

- settings and secrets outside codebase
- config loading explicit and typed
- schema models separate from persistence models when shapes differ
- filesystem, subprocess, database, network = edge concerns
- sync by default; async only when end-to-end path clearly benefits

## Validation, Error, and Design Rules

- validate external input at boundaries only, pass typed values inward
- valid, parsing, normalization close to edge
- raise exceptions matching real failure, helping caller react
- partial failure behavior explicit in batch, retry, streaming flows
- composition over inheritance-heavy designs
- abstractions only when duplication is real and repeating
- avoid god modules, hidden global state, flag-arg APIs, convenience wrappers hiding side effects
- retry, timeout, backoff policy centralized, not scattered through business logic

## Async, Job, and Resource Rules

- sync by default; async only when full path benefits
- if async needed, keep call path async end-to-end
- background jobs idempotent, explicit on ownership, retries, lifecycle
- context managers for files, connections, temp resources
- cleanup, cancellation, timeout behavior visible
- streaming responses and long-lived resources = explicit lifetime problems

## Logging and Error Handling

- `logging` for app logs and structured context
- `print` only for intentional CLI output
- log enough to debug failures, no secret or payload leaks
- fail loudly and specifically, never hide broken states

## Observability, Performance, and Testing Rules

- structured consistent logging across services, jobs, handlers
- metrics/traces when project needs operational visibility; instrumentation at edges
- profile and measure before optimizing; no guesswork optimization
- DB round-trips, repeated parsing, large object copies, unbounded loops = first suspects
- test behavior, edge cases, error paths, historical regressions
- many focused unit tests, smaller integration set, few e2e tests
- mock external boundaries, not logic under test

## Python Review Focus

- hidden IO inside reusable logic
- weak or missing boundary valid
- ORM, transport, framework types leaking into shared code
- uncontained `Any`, unchecked casts, type-eroding helpers
- retries, timeouts, cleanup, partial failure hidden in business code
- tests overfitting impl details over behavior

## Common Build Fixes

| Tool        | Error Pattern             | Fix                                  |
| ----------- | ------------------------- | ------------------------------------ |
| ruff format | file would be reformatted | `uv run ruff format <file>`          |
| ruff check  | import unused             | remove import                        |
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
| `TimeoutError`          | slow I/O or infinite loop                   |
| valid failure           | model or schema mismatch; check payload     |
| flaky test              | shared state, timing, or ordering issue     |
| works locally, fails CI | env difference: deps, Python version, or OS |

## When the Project Includes FastAPI

- `Annotated` for request parameters and dependencies
- routes thin, orchestration in `services/` or `core/`
- explicit return types or `response_model` for public handlers
- `def` over `async def` when internals block
- no blocking file, database, or network work inside async handlers
- auth, valid, uploads, callbacks, error shapes explicit at edge

## Python Checklist

### Project Setup

- [ ] `pyproject.toml` is source of truth
- [ ] dependencies and dev dependencies explicit
- [ ] valid entrypoints clear
- [ ] config and secrets stay out of source code

### Code Structure

- [ ] core logic reusable and testable
- [ ] services orchestrate workflows without hiding side effects
- [ ] models and schemas explicit
- [ ] database and external IO at edges
- [ ] package boundaries and public imports intentional

### Quality Gates

- [ ] `ruff format --check`
- [ ] `ruff check`
- [ ] `rumdl check`
- [ ] `ty check`
- [ ] `pytest`

### Correctness and Safety

- [ ] boundary valid explicit
- [ ] file paths and external input validated
- [ ] parameterized queries used
- [ ] retries, timeouts, cleanup behavior explicit
- [ ] logging structured and useful
- [ ] errors specific and actionable

### Testing

- [ ] unit tests cover core logic
- [ ] integration tests cover database and external systems
- [ ] regression tests protect historical failures
- [ ] fixtures focused and maintainable
- [ ] performance-sensitive paths measured before optimization

## Testing Focus

<!-- - business rules -->
<!-- - valid and error paths -->
<!-- - external integration boundaries -->
<!-- - regression tests for known failure modes -->

## Environment Variables

<!-- | Variable | Description | Required | -->
<!-- |----------|-------------|----------| -->

## Project-Specific Guardrails

<!-- - Keep public imports stable -->
<!-- - Do not bypass typed settings -->
<!-- - Avoid framework-specific logic in `core/` -->
