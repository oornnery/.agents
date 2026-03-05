# Uv Reference

Complete uv workflow: project setup, dependency management, dev toolchain, virtual environments, packaging, and publishing.

## Documentation

- uv Docs: <https://docs.astral.sh/uv/>
- Ruff Docs: <https://docs.astral.sh/ruff/>
- Ty Docs: <https://ty.astral.sh/>
- rumdl Docs: <https://rumdl.com/docs/>
- pytest Docs: <https://docs.pytest.org/>
- taskipy Docs: <https://github.com/taskipy/taskipy>

## Install Uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Project Setup

### Create New Project

```bash
uv init myapp                    # New project
uv init myapp --lib              # Library project
uv init myapp --app              # Application project
cd myapp && uv sync              # Install dependencies
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
uv python install 3.12           # Install a Python version
uv python install 3.11 3.12      # Install multiple versions
uv python list                   # List available versions
uv python pin 3.12               # Pin version for project (.python-version)
```

## Dependency Management

### Add Dependencies

```bash
uv add httpx                     # Runtime dependency
uv add httpx pydantic rich       # Multiple at once
uv add "httpx>=0.27"             # With version constraint
uv add httpx --optional api      # Optional dependency group
```

### Add Dev Dependencies

```bash
uv add --dev ruff                # Dev dependency
uv add --dev pytest pytest-cov pytest-asyncio pytest-xdist pytest-mock
uv add --dev ty                  # Type checker
uv add --dev rumdl               # Markdown linter
uv add --dev taskipy             # Task runner
```

### Remove Dependencies

```bash
uv remove httpx                  # Remove runtime dep
uv remove --dev ruff             # Remove dev dep
```

### Sync and Lock

```bash
uv sync                          # Install from lockfile
uv sync --frozen                 # Fail if lockfile is outdated
uv sync --no-dev                 # Production install (no dev deps)
uv lock                          # Update lockfile without installing
uv lock --upgrade                # Upgrade all deps to latest compatible
uv lock --upgrade-package httpx  # Upgrade specific package
```

### Inspect Dependencies

```bash
uv tree                          # Dependency tree
uv tree --depth 1                # Shallow tree
uv pip list                      # List installed packages
uv pip show httpx                # Package details
```

## Running Commands

### Uv Run

```bash
uv run python script.py          # Run with project env
uv run python -m myapp.main      # Module mode
uv run pytest -v                 # Run dev tools
uv run ruff check .              # Run linter
uv run ty check                  # Run type checker
```

### Run Without Project (Ephemeral)

```bash
uv run --with httpx python -c "import httpx; print(httpx.get('https://example.com'))"
uvx ruff check .                 # Run tool without installing
uvx --from ruff ruff format .    # Explicit package source
```

## Dev Toolchain

### Standard Dev Stack

```bash
uv add --dev ruff pytest pytest-cov ty rumdl taskipy
```

### Formatting and Lint (Ruff)

```bash
uv run ruff format .                      # Format code
uv run ruff format --check .              # Check format (CI)
uv run ruff check .                       # Lint
uv run ruff check . --fix                 # Auto-fix safe issues
uv run ruff check . --fix --unsafe-fixes  # Auto-fix aggressive
uv run ruff rule E501                     # Explain a rule
```

### Type Checking (Ty)

```bash
uv run ty check                  # Check entire project
uv run ty check src tests        # Check specific paths
uv run ty check src/myapp/api    # Check single directory
```

### Markdown Lint (Rumdl)

```bash
uv run rumdl init                # Create .rumdl.toml config
uv run rumdl check .             # Check markdown files
uv run rumdl check --fix .       # Auto-fix markdown issues
uv run rumdl fmt .               # Format markdown files
```

### Testing (Pytest)

```bash
uv run pytest -v                 # Run all tests
uv run pytest -v -x              # Stop on first failure
uv run pytest tests/unit/ -v     # Run specific directory
uv run pytest -k "test_user" -v  # Run by pattern
uv run pytest -v --cov=src --cov-report=term-missing  # With coverage
```

### Task Runner (Taskipy)

Config in `pyproject.toml`:

```toml
[tool.taskipy.tasks]
format = "ruff format ."
lint = "ruff check . --fix"
typecheck = "ty check"
mdlint = "rumdl check ."
test = "pytest -v"
check = "task format && task lint && task mdlint && task typecheck && task test"
```

```bash
uv run task format               # Run single task
uv run task check                # Run full validation
```

## Validation Sequence

Run in order — fail fast on early stages:

```bash
# 1. Format (code)
uv run ruff format --check .

# 2. Lint (code)
uv run ruff check .

# 3. Lint (markdown)
uv run rumdl check .

# 4. Type check
uv run ty check

# 5. Test
uv run pytest -v
```

## Virtual Environments

```bash
uv venv                          # Create .venv in project root
uv venv --python 3.12            # With specific Python version
uv venv /path/to/venv            # Custom location
source .venv/bin/activate         # Activate (optional — uv run handles this)
```

uv auto-discovers `.venv` — you rarely need to activate manually.

## Pyproject.toml

### Complete Project Config

```toml
[project]
name = "myapp"
version = "0.1.0"
description = "Short description"
requires-python = ">=3.12"
readme = "README.md"
license = "MIT"
dependencies = [
    "httpx>=0.27",
    "pydantic>=2.0",
    "rich>=13.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "pytest-asyncio>=0.24",
    "ruff>=0.8",
    "ty>=0.1",
    "rumdl>=0.1",
    "taskipy>=1.13",
]

[project.scripts]
myapp = "myapp.cli:app"

[project.entry-points."myapp.plugins"]
auth = "myapp_auth:plugin"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Ruff Config

```toml
[tool.ruff]
target-version = "py312"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "SIM", "RUF"]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["myapp"]
```

### Pytest Config

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = ["-v", "--strict-markers", "--tb=short"]
markers = [
    "slow: long-running tests",
    "integration: integration-level tests",
]
```

### Coverage Config

```toml
[tool.coverage.run]
source = ["src"]
branch = true
omit = ["*/tests/*", "*/__init__.py"]

[tool.coverage.report]
show_missing = true
skip_covered = false
```

## Building and Publishing

```bash
uv build                         # Build sdist + wheel
uv build --sdist                 # Source distribution only
uv build --wheel                 # Wheel only
uv publish                       # Publish to PyPI
uv publish --token $PYPI_TOKEN   # With explicit token
```

## Scripts (Standalone)

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
uv run script.py                 # Auto-installs deps in ephemeral env
```

## Global Tools

```bash
uv tool install ruff             # Install globally
uv tool install --with ruff-lsp ruff  # With extras
uv tool list                     # List installed tools
uv tool upgrade ruff             # Upgrade tool
uv tool uninstall ruff           # Remove tool
uvx ruff check .                 # Run without installing (ephemeral)
```

## Cache Management

```bash
uv cache clean                   # Clear all caches
uv cache clean httpx             # Clear specific package cache
uv cache dir                     # Show cache directory
```

## Guardrails

- Always use `uv` over `pip` — it handles environments, resolution, and locking.
- Commit `uv.lock` to version control for reproducible installs.
- Use `uv sync --frozen` in CI to catch lockfile drift.
- Use `uv sync --no-dev` for production deployments.
- Pin Python version with `.python-version` file.
- Use `--dev` for all tooling packages (ruff, pytest, ty, rumdl, taskipy).
- Prefer `uv run` over activating virtualenvs.
