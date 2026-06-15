# Python Project Template

## Overview

A minimal, opinionated Python project skeleton built around [uv](https://docs.astral.sh/uv/), [Ruff](https://docs.astral.sh/ruff/), [ty](https://docs.astral.sh/ty/), and [pytest](https://docs.pytest.org/). It ships with a FastAPI entrypoint, pre-configured linting, type checking, test coverage, and GitHub Actions workflows. The goal is to clone, rename, and start writing code with zero toolchain setup.

## Quick Start

1. Copy this template into a new project directory.
2. Rename the `src/myapp` package to your project name.
3. Update `name` in `pyproject.toml` to match.
4. Run the init script to pin Python, install dependencies, and set up the environment:

```bash
bash scripts/init.sh
```

This pins Python 3.13, syncs the lockfile, installs dev tools (ruff, ty, pyright, bandit, pytest, pre-commit, taskipy), and adds runtime libraries (rich, httpx, python-dotenv).

## Project Structure

```
.
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── .rumdl.toml
├── README.md
├── pyproject.toml
├── ruff.toml
├── ty.toml
├── scripts/
│   └── init.sh
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── main.py
│       └── routes.py
├── tests/
│   ├── conftest.py
│   └── test_app.py
├── docker/
│   ├── .dockerignore
│   ├── Dockerfile
│   └── compose.yml
└── .github/
    ├── ci.yml
    ├── container.yml
    └── publish.yml
```

| Path | Purpose |
|------|---------|
| `src/myapp/` | Application source code. Rename `myapp` to your package name. |
| `tests/` | pytest suite with shared fixtures in `conftest.py`. |
| `scripts/init.sh` | One-time environment setup script. |
| `pyproject.toml` | Project metadata, dependencies, and tool configuration. |
| `ruff.toml` | Ruff formatter and linter settings. |
| `ty.toml` | ty type checker configuration. |
| `.rumdl.toml` | Markdown linting rules. |
| `.pre-commit-config.yaml` | Pre-commit hooks for ruff, trailing whitespace, YAML checks, and local type checking. |
| `docker/Dockerfile` | Multi-stage Docker image using uv and Python 3.12 slim. |
| `docker/compose.yml` | Docker Compose placeholder. |
| `.github/ci.yml` | Pull request and push validation workflow. |
| `.github/publish.yml` | PyPI publish workflow triggered on version tags. |

## Available Commands

All tasks are defined in `pyproject.toml` under `[tool.taskipy.tasks]` and run via `task <name>`.

| Task | Description |
|------|-------------|
| `fmt` | Format all Python files with `ruff format .` |
| `lint` | Lint and auto-fix with `ruff check . --fix` |
| `type` | Type-check with `ty check src` and `pyright` |
| `test` | Run the test suite with `pytest -v` |
| `mdlint` | Lint Markdown files with `rumdl check .` |
| `mdfmt` | Format Markdown files with `rumdl fmt .` |
| `sec` | Run security scan with `bandit -r src` |
| `check` | Full validation flow: `fmt → lint → type → mdlint → test` |

Run the full validation flow before committing:

```bash
task check
```

## Configuration

### Python version

Set in `pyproject.toml` under `requires-python` and in `scripts/init.sh` via `uv python pin`.

### Ruff

Settings live in `ruff.toml` and `pyproject.toml`. The selected rule set covers pycodestyle, pyflakes, isort, pyupgrade, bugbear, pytest style, type-checking imports, pathlib, perflint, logging, and bandit security checks.

### Type checking

`ty.toml` configures the ty checker with strict rules for `src/` and relaxed warnings for `tests/`. `pyproject.toml` also sets `pyright` to strict mode.

### pytest

Configured in `pyproject.toml` with coverage tracking for `src/`, branch coverage enabled, and markers for `slow`, `integration`, and `e2e` tests.

### Pre-commit

Install hooks after running `init.sh`:

```bash
uv run pre-commit install
```

Hooks run ruff check/format, trailing whitespace cleanup, YAML validation, and local `ty check` and `rumdl check` passes.

## Docker Usage

Build the image from the project root:

```bash
docker build -f docker/Dockerfile -t myapp:latest .
```

The Dockerfile copies `pyproject.toml` and `uv.lock` first for layer caching, then installs production dependencies with `uv sync --frozen --no-dev`, and finally copies `src/`. The default command starts the FastAPI app on port 8000. Update the module path in the `CMD` instruction if you renamed `myapp`.

## CI/CD Setup

### Validation workflow (`.github/ci.yml`)

Runs on every pull request and push to `main` or `dev`:

1. Checkout code
2. Install uv
3. Sync dependencies with `uv sync --frozen`
4. Run `ruff format --check .`
5. Run `ruff check .`
6. Run `rumdl check .`
7. Run `ty check`
8. Run `pyright`
9. Run `pytest -v --cov=src --cov-report=term-missing`

### Publish workflow (`.github/publish.yml`)

Triggered on pushes to tags matching `v*`. Builds the package with `uv build` and publishes to PyPI using `uv publish`.

Set the `PYPI_TOKEN` repository secret before cutting your first release.
