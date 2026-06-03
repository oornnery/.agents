# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!--
Python project overlay.
Use for Python apps, services, packages, CLIs, scripts, and internal tools.
Keep web/API specifics in AGENTS.fastapi.md.
-->

## Project Description

<!-- Brief description of what this Python project does and its main constraints -->

## Stack Defaults

- **Python**: 3.12+
- **Package Manager**: uv
- **Lint and Format**: Ruff
- **Type Check**: ty and/or pyright
- **Tests**: pytest
- **Validation**: Pydantic at external boundaries
- **HTTP Client**: HTTPX when outbound HTTP is needed
<!-- - **Persistence**: SQLModel / SQLAlchemy / PostgreSQL -->

## Quick Commands

```bash
uv sync
uv run python -m myapp
uv run task check
uv run pytest -v
```

## Validation Entry Points

Prefer repo task aliases when they exist and map cleanly to real commands.

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check src
uv run pyright
uv run pytest -v
```

Run only installed/configured tools. Do not add pyright, ty, task, rumdl, pre-commit, or bandit just because this template mentions them.

## Python Discovery

- Treat `pyproject.toml` and `uv.lock` as source of truth
- Identify project type before editing: app, library, CLI, script, service, or mixed
- Find package root, entrypoints, config loading, test layout, and task aliases
- Inspect nearby modules and tests before adding new structure
- Prefer existing dependency, typing, logging, and error patterns over new ones

## Package and Tooling Rules

- Use `uv sync`, `uv add`, `uv add --dev`, and `uv run`
- Use `uvx` only for one-off tools outside the project
- Do not mix `pip`, `poetry`, `pipenv`, `conda`, or manual venv workflows into a uv project
- Add dependencies only when the standard library or existing deps do not solve the request cleanly
- Keep package metadata, dependency groups, and entrypoints explicit when shipping a library or CLI

## Layout Defaults

```text
src/myapp/
├── core/       # business rules, pure logic, shared policies
├── services/   # orchestration and workflows
├── models/     # typed data structures and domain objects
├── database/   # sessions, repositories, queries, migrations
├── api/        # HTTP entrypoints when present
├── cli/        # CLI entrypoints when present
└── views/      # templates/rendering adapters when present

tests/
├── unit/
├── integration/
└── e2e/
```

Match the repo's actual layout over this example.

## Python Design Rules

- Keep IO at edges; keep core logic testable without filesystem, network, database, or subprocess calls
- Use small functions and focused modules before classes
- Use dataclasses for plain internal data; Pydantic for validated external shapes
- Keep routes, commands, jobs, and adapters thin
- Separate schemas, settings, persisted models, and domain objects when their shapes differ
- Do not leak ORM, transport, or framework types into reusable logic unless intentionally framework-bound
- Use `pathlib`, context managers, `logging`, and parameterized queries
- Prefer sync by default; use async only when the full call path benefits

## Typing Rules

- Type public functions, boundary contracts, and important internal helpers
- Contain `Any`, unchecked casts, and untyped third-party values at the edge
- Use `Protocol` for lightweight structural boundaries
- Use `TypedDict` when dict keys are known and mapping semantics matter
- Use `Enum` or literals for fixed sets, not free-form strings
- Prefer narrowing, explicit conversion, and helper types over informal assumptions
- Use `Annotated` or semantic wrappers when raw primitives become ambiguous

## Validation and Error Rules

- Validate external input at boundaries, then pass typed values inward
- Keep parsing, normalization, and validation close to the edge
- Raise specific exceptions that help callers react
- Do not add broad `except Exception` handling to hide broken states
- Make partial failure behavior explicit in batch, retry, streaming, and migration flows
- Centralize retry, timeout, and backoff policy instead of scattering it through business logic

## Runtime and Resource Rules

- Settings and secrets stay outside source code
- Config loading must be explicit and typed
- Background jobs must state ownership, idempotency, retries, and lifecycle
- Cleanup, cancellation, timeout, and streaming lifetimes must be visible
- Use bounded caches; never introduce unbounded cache keys casually

## Testing Rules

- Test behavior, business rules, edge cases, error paths, and historical regressions
- Prefer many focused unit tests, fewer integration tests, and only critical e2e tests
- Mock external boundaries, not logic under test
- Add regression tests for bugs when feasible
- Avoid tests that only assert constants, implementation details, or "returns something"

## Performance Rules

- Profile before optimizing; never optimize from vibes
- First suspects: bad algorithm, N+1 queries, repeated parsing, large object copies, unbounded loops
- Stream or iterate large inputs instead of materializing when possible
- Use comprehensions, joins, dict/set lookups, and bounded caches where they keep code clear
- Reach for multiprocessing, async, vectorization, or native extensions only after measuring the bottleneck

## Review Focus

- hidden IO inside reusable logic
- weak or missing boundary validation
- ORM, transport, or framework types leaking into shared code
- uncontained `Any`, unchecked casts, type-eroding helpers
- broad exception handling hiding real failures
- retries, timeouts, cleanup, or partial failure hidden in business code
- tests overfitting implementation details instead of intent

## UV Inline Scripts

For small standalone scripts, prefer inline metadata over a full package layout.

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx>=0.27",
#   "rich>=13.0",
# ]
# ///
```

Promote to a real project once it grows multiple modules, commands, or shared logic.

## Project-Specific Guardrails

<!-- - Keep public imports stable -->
<!-- - Do not bypass typed settings -->
<!-- - Avoid framework-specific logic in core/ -->
