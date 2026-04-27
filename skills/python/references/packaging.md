# Python Packaging

Modern Python packaging guidance for libraries, CLIs, distribution, and publishing.

## Use When

- creating package layout
- writing `pyproject.toml`
- adding CLI entrypoints
- building wheels/sdists
- publishing to PyPI/private index
- testing installability
- packaging data files

## Defaults

- use `src/` layout for real packages
- use `pyproject.toml`
- keep build backend simple (`hatchling` or `setuptools`)
- define CLI entrypoints in `[project.scripts]`
- include typed package marker when public typed API matters
- test install in clean env before publishing

## Layouts

Recommended:

```text
project/
├── pyproject.toml
├── README.md
├── src/my_package/
│   ├── __init__.py
│   └── py.typed
└── tests/
```

Flat layout only for tiny/internal packages.

## Minimal `pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-package"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[project.scripts]
my-cli = "my_package.cli:main"
```

## Metadata Checklist

- name
- version or dynamic version config
- description
- README
- license
- authors/maintainers
- Python requirement
- dependencies
- optional dependency groups
- classifiers when publishing publicly
- URLs for docs/source/issues

## Versioning

- libraries: semantic versioning
- apps/internal tools: simple monotonic version OK
- git-derived versions: use `setuptools-scm` or backend equivalent
- expose `__version__` only if callers need runtime introspection

## CLI

Use simple `argparse` by default. Add Click/Typer only if UX needs nested commands, rich options, or shell completion.

Entry contract:

- parse args
- call small application function
- return exit code
- keep side effects at boundary

## Build and Check

```bash
uv add --dev build twine
uv run python -m build
uv run twine check dist/*
```

Artifacts:

- wheel: install target
- sdist: source distribution

## Publish

Safe flow:

1. build
2. `twine check`
3. publish to TestPyPI/private staging
4. install in clean env
5. smoke test import + CLI
6. publish prod

Use trusted publishing/OIDC in CI where possible. Do not store long-lived PyPI tokens in repo.

## Data Files

- prefer `importlib.resources`
- include data via backend config
- keep package data small
- avoid relying on current working directory

## Namespace Packages

Use only when several distributions intentionally share namespace. Prefer normal package otherwise.

## Native Extensions

Reach for C/Rust only for stable hot paths with measured need. Document build requirements and wheel strategy.

## Install Testing

```bash
uv venv /tmp/pkg-test
uv pip install dist/*.whl
uv run python -c "import my_package"
uv run my-cli --help
```

## README Template

Keep public README concise:

- what it is
- install
- quick start
- main features
- docs link
- dev/test commands
- license

## Common Patterns

| Need              | Pattern                                   |
| ----------------- | ----------------------------------------- |
| private index     | configure source/index outside code       |
| multi-arch wheels | CI matrix + cibuildwheel                  |
| optional features | `[project.optional-dependencies]`         |
| console script    | `[project.scripts]`                       |
| typed package     | include `py.typed`                        |
| monorepo packages | workspace/tooling config at repo root     |

## Publish Checklist

- [ ] clean working tree or intentional release commit
- [ ] version bumped/tagged
- [ ] changelog/release notes updated if used
- [ ] tests/lint/type pass
- [ ] wheel and sdist build
- [ ] `twine check` passes
- [ ] clean-env import works
- [ ] CLI smoke test works
- [ ] credentials handled by trusted publishing or secret manager
