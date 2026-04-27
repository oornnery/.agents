# UV Package Manager

Use `uv` for Python dependency, venv, lockfile, Python version, and one-off tool workflows.

## Use When

- creating/syncing Python projects
- adding/removing/upgrading deps
- running project commands
- managing Python versions/venvs
- CI/Docker installs
- migrating from pip/poetry/pip-tools

## Defaults

- Prefer `uv run ...`; do not activate venv manually in agent workflows.
- Prefer `uv sync` over ad hoc installs.
- Commit `uv.lock` for applications.
- Use `--frozen` in CI.
- Use `uvx` for one-off tools not belonging to project deps.

## Essential Commands

```bash
uv --version
uv init
uv sync
uv sync --frozen
uv run python script.py
uv run pytest
uv add httpx
uv add --dev pytest ruff
uv remove httpx
uv lock
uv lock --upgrade-package httpx
uv python install 3.12
uv python pin 3.12
uvx ruff --version
```

## Project Setup

```bash
uv init my-project
cd my-project
uv python pin 3.12
uv add pydantic-settings
uv add --dev pytest ruff ty
uv sync
```

Existing project:

```bash
uv sync
uv run pytest
```

## Dependency Rules

| Task                | Command                         |
| ------------------- | ------------------------------- |
| add runtime dep     | `uv add <pkg>`                  |
| add dev dep         | `uv add --dev <pkg>`            |
| add optional dep    | `uv add --optional <group> <p>` |
| remove dep          | `uv remove <pkg>`               |
| update lock         | `uv lock`                       |
| upgrade one dep     | `uv lock --upgrade-package <p>` |
| export requirements | `uv export -o requirements.txt` |

Avoid mixing `pip install` with `uv` in same project unless repo already does.

## Python and Venvs

```bash
uv python list
uv python install 3.12 3.13
uv python pin 3.12
uv venv
uv venv --python 3.12
```

Agents should run commands through `uv run`, not `source .venv/bin/activate`.

## CI

Use:

```bash
uv sync --frozen
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest -v
```

Cache uv download/cache dirs if CI supports it. Keep install from lockfile deterministic.

## Docker

Pattern:

1. copy `pyproject.toml` + `uv.lock`
2. install uv
3. `uv sync --frozen --no-dev`
4. copy app code
5. run app through venv or `uv run`

Use multi-stage build when final image should not include build tools.

## Workspaces

Use uv workspaces for monorepos with multiple packages. Root `pyproject.toml` owns workspace members; packages keep their own metadata.

## Migration

| From        | First Move                                  |
| ----------- | ------------------------------------------- |
| pip         | keep requirements, run `uv add -r ...`      |
| poetry      | keep `pyproject.toml`, run `uv sync`        |
| pip-tools   | replace compile/sync with `uv lock/sync`    |
| ad hoc venv | add `pyproject.toml`, pin Python, `uv sync` |

Review lockfile diff after migration.

## Troubleshooting

| Problem              | Check/Fix                                  |
| -------------------- | ------------------------------------------ |
| `uv` not found       | install or fix PATH                        |
| wrong Python version | `uv python pin <version>`                  |
| lock out of date     | `uv lock`, then commit `uv.lock`           |
| dependency conflict  | inspect resolver output; relax constraints |
| cache issue          | `uv cache clean`                           |
| offline build        | ensure cache warmed, use `--offline`       |

## Best Practices

- lock application deps
- keep library version ranges reasonable
- pin Python via `.python-version`
- use dependency groups for dev/docs/test extras
- avoid global installs for project tools
- use `uvx` for temporary CLIs
- prefer repo task aliases when available
