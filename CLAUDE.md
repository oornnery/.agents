# CLAUDE.md

Project instructions for AI coding agents (Claude, Codex, Copilot, etc.).

## Stack

- **Language**: Python 3.12+
- **Package manager**: uv
- **Linter/Formatter**: ruff
- **Type checker**: ty
- **Test runner**: pytest
- **Markdown lint**: rumdl

## Quick Commands

```bash
uv sync                          # Install deps from lockfile
uv run ruff format .             # Format
uv run ruff check . --fix        # Lint
uv run ty check                  # Type check
uv run pytest -v                 # Test
uv run rumdl check .             # Markdown lint
```

## Validation (run in order, fail fast)

```bash
uv run ruff format --check .
uv run ruff check .
uv run rumdl check .
uv run ty check
uv run pytest -v
```

## Skills

On-demand knowledge modules in `.agents/skills/`. Load the relevant skill
when working in its domain.

| Skill                  | When to use                              |
| ---------------------- | ---------------------------------------- |
| `python/SKILL.md`      | General Python code, conventions, async  |
| `fastapi/SKILL.md`     | FastAPI APIs, routes, dependencies       |
| `jx/SKILL.md`          | Jinja server-rendered components (JX)    |

Each skill has a `references/` folder with detailed submodules (httpx,
pydantic, pytest, rich, typer, uv, streaming, dependencies, etc.).
Load these on demand — not all at once.

## Conventions

- Use `pathlib` over `os.path`
- f-strings only
- `snake_case` functions/variables, `PascalCase` classes, `UPPER_SNAKE` constants
- Type all public functions
- Use `Annotated` style for FastAPI parameters and dependencies
- `logging` for app logs, `rich` for CLI output — never `print`
- Pydantic `BaseModel` for validation, `dataclass` for plain data
- IO at edges only — services and domain must be pure
- Prefer `uv` over direct `pip` workflows
- Never commit code that fails `ruff check`
