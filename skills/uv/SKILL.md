---
name: uv
description: Python package management with uv -- project setup, deps, dev toolchain, venvs, publishing. Load when managing Python projects or dependencies.
---

# Uv

Package management and dev toolchain. See [uv docs](https://docs.astral.sh/uv/).

## Install

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Project Setup

```bash
uv init myapp                        # Create project
uv init myapp --lib                  # Library layout
uv sync                              # Install deps from lockfile
```

## Dependency Management

```bash
uv add httpx pydantic rich           # Add deps
uv add --dev ruff pytest ty taskipy  # Add dev deps
uv remove httpx                      # Remove dep
uv sync --frozen                     # Reproducible install (CI)
uv sync --no-dev                     # Production install
uv lock --upgrade                    # Upgrade all
uv tree --depth 1                    # Inspect deps
```

## Running Commands

```bash
uv run python script.py
uv run pytest -v
uv run ruff check .
uvx ruff check .                     # Run without project
```

## Dev Toolchain

```bash
uv run ruff format .                 # Format
uv run ruff format --check .         # Format check
uv run ruff check . --fix            # Lint + fix
uv run ty check                      # Type check
uv run pytest -v                     # Test
```

## Task Runner

Config in `pyproject.toml`:

```toml
[tool.taskipy.tasks]
format = "ruff format ."
lint = "ruff check . --fix"
typecheck = "ty check"
test = "pytest -v"
check = "task format && task lint && task typecheck && task test"
```

## Recommended `pyproject.toml`

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]
fix = true

[tool.ty.rules]
possibly-unbound-attribute = "warn"
```

## Building and Publishing

```bash
uv build
uv publish --token $PYPI_TOKEN
```

## Inline Script Dependencies

```python
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx", "rich"]
# ///
```

## Pre-Commit

```bash
uv add --dev pre-commit
uv run pre-commit install
```

See `markdown/SKILL.md` for rumdl configuration.

## Guardrails

- Always use `uv` over `pip`.
- Commit `uv.lock` for reproducible installs.
- Use `uv sync --frozen` in CI to catch lockfile drift.
- Pin Python version with `.python-version`.
- Use `--dev` for project-local tooling packages.
- Prefer `uv run` over manually activating virtualenvs.
