# Uv Reference

Complete uv workflow: project setup, dependency management, dev toolchain,
virtual environments, packaging, and publishing.

## Documentation

- uv Docs: <https://docs.astral.sh/uv/>
- Ruff Docs: <https://docs.astral.sh/ruff/>
- Pyright Docs: <https://microsoft.github.io/pyright/>
- Ty Docs: <https://ty.astral.sh/>
- pytest Docs: <https://docs.pytest.org/>
- taskipy Docs: <https://github.com/taskipy/taskipy>

## Install Uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Required Python Tools

Use `uv tool install` when you want local machine tooling outside a single
project environment:

```bash
uv tool install ruff
uv tool install pyright
uv tool install ty
```

Use `markdown/SKILL.md` for `rumdl` installation, config, and Markdown-specific
lint workflows.

## Project Setup

### Create New Project

```bash
uv init myapp
uv init myapp --lib
uv init myapp --app
cd myapp && uv sync
```

### Project Structure

```text
myapp/
├── pyproject.toml
├── uv.lock
├── .python-version
├── src/
│   └── myapp/
│       └── __init__.py
└── tests/
```

### Python Version Management

```bash
uv python install 3.12
uv python install 3.11 3.12
uv python list
uv python pin 3.12
```

## Dependency Management

### Add Dependencies

```bash
uv add httpx
uv add httpx pydantic rich
uv add "httpx>=0.27"
uv add httpx --optional api
```

### Add Dev Dependencies

```bash
uv add --dev ruff
uv add --dev pytest pytest-cov pytest-asyncio pytest-xdist pytest-mock
uv add --dev ty
uv add --dev taskipy
```

### Remove Dependencies

```bash
uv remove httpx
uv remove --dev ruff
```

### Sync and Lock

```bash
uv sync
uv sync --frozen
uv sync --no-dev
uv lock
uv lock --upgrade
uv lock --upgrade-package httpx
```

### Inspect Dependencies

```bash
uv tree
uv tree --depth 1
uv pip list
uv pip show httpx
```

## Running Commands

### Uv Run

```bash
uv run python script.py
uv run python -m myapp.main
uv run pytest -v
uv run ruff check .
uv run ty check
```

### Run Without Project

```bash
uv run --with httpx python -c "import httpx; print(httpx.get('https://example.com'))"
uvx ruff check .
uvx --from ruff ruff format .
```

## Dev Toolchain

### Standard Dev Stack

```bash
uv add --dev ruff pytest pytest-cov ty taskipy
```

### Formatting and Lint

```bash
uv run ruff format .
uv run ruff format --check .
uv run ruff check .
uv run ruff check . --fix
uv run ruff check . --fix --unsafe-fixes
uv run ruff rule E501
```

### Type Checking

```bash
uv run ty check
uv run ty check src tests
uv run ty check src/myapp/api
```

### Testing

```bash
uv run pytest -v
uv run pytest -v -x
uv run pytest tests/unit/ -v
uv run pytest -k "test_user" -v
uv run pytest -v --cov=src --cov-report=term-missing
```

### Task Runner

Config in `pyproject.toml`:

```toml
[tool.taskipy.tasks]
format = "ruff format ."
lint = "ruff check . --fix"
typecheck = "ty check"
test = "pytest -v"
check = "task format && task lint && task typecheck && task test"
```

```bash
uv run task format
uv run task check
```

## Validation Sequence

Run in order:

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest -v
```

Project-wide validation may still include `uv run rumdl check .`, but the setup
and authoring guidance for that belongs in `markdown/SKILL.md`.

## Virtual Environments

```bash
uv venv
uv venv --python 3.12
uv venv /path/to/venv
source .venv/bin/activate
```

uv auto-discovers `.venv`, so manual activation is usually optional.

## Recommended `pyproject.toml`

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]
fix = true

[tool.ruff.format]
quote-style = "single"

[tool.pyright]
typeCheckingMode = "standard"
reportMissingImports = true

[tool.ty]
strict = true
```

## Building and Publishing

```bash
uv build
uv build --sdist
uv build --wheel
uv publish
uv publish --token $PYPI_TOKEN
```

## Scripts

Run single-file scripts with inline dependencies:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx", "rich"]
# ///

import httpx
from rich import print

response = httpx.get("https://api.example.com/data")
print(response.json())
```

```bash
uv run script.py
```

## Validation Checklist

Use this after bootstrapping local Python tooling:

```bash
ruff --version
pyright --version
ty --version
```

## Guardrails

- Always use `uv` over `pip`.
- Commit `uv.lock` for reproducible installs.
- Use `uv sync --frozen` in CI to catch lockfile drift.
- Use `uv sync --no-dev` for production installs.
- Pin Python version with `.python-version`.
- Use `--dev` for project-local tooling packages.
- Prefer `uv run` over manually activating virtualenvs.
