# CLAUDE.md

Project instructions for AI coding agents (Claude, Codex, Copilot, etc.).

All CLI commands go through RTK for token optimization (handled by hook).

## Stack

- **Language**: Python 3.12+
- **Package manager**: uv
- **Linter/Formatter**: ruff
- **Type checker**: ty
- **Test runner**: pytest
- **Markdown lint**: rumdl
- **Token optimizer**: rtk

## Quick Commands

```bash
uv sync                          # Install deps from lockfile
uv run ruff format .             # Format
uv run ruff check . --fix        # Lint
uv run ty check                  # Type check
uv run pytest -v                 # Test
uv run rumdl check .             # Markdown lint
rtk gain                         # Show token savings
```

## Validation (run in order, fail fast)

```bash
uv run ruff format --check .
uv run ruff check .
uv run rumdl check .
uv run ty check
uv run pytest -v
```

## Rules

Always-on conventions in `rules/`. Automatically loaded by Claude Code.

| Rule                       | Scope                                |
| -------------------------- | ------------------------------------ |
| `rules/python.md`          | Python style and conventions         |
| `rules/git.md`             | Git safety rules                     |
| `rules/documentation.md`   | Markdown and documentation standards |

## Commands

Procedural workflows in `commands/`. Invoke when performing a task.

| Command                | When to use                                  |
| ---------------------- | -------------------------------------------- |
| `commands/commit.md`   | Commit changes with logical commits          |
| `commands/refactor.md` | Deep audit, clean code, SOLID, security      |
| `commands/review.md`   | Code review of changes or PRs                |
| `commands/debug.md`    | Systematic debugging workflow                |
| `commands/setup.md`    | Project onboarding and env verification      |
| `commands/plan.md`     | Planning with SDD, SPEC.md, ARCH.md, mermaid |

## Skills

On-demand knowledge modules in `skills/`. Load the relevant skill
when working in its domain.

| Skill               | When to use                                           |
| ------------------- | ----------------------------------------------------- |
| `python/SKILL.md`   | General Python code, conventions, async, architecture |
| `fastapi/SKILL.md`  | FastAPI APIs, routes, dependencies                    |
| `jx/SKILL.md`       | Jinja server-rendered components (JX)                 |
| `frontend/SKILL.md` | Frontend bootstrap, JS/TS tooling, Tailwind, Basecoat |
| `markdown/SKILL.md` | Markdown writing, structure, rumdl lint               |
| `rtk/SKILL.md`      | RTK setup, custom filters, token optimization         |
| `pydantic/SKILL.md` | Data validation, serialization, settings              |
| `httpx/SKILL.md`    | HTTP client patterns (sync/async)                     |
| `testing/SKILL.md`  | Testing strategy, pytest, coverage, mocking           |
| `rich/SKILL.md`     | Console output, tables, progress bars                 |
| `typer/SKILL.md`    | CLI applications                                      |
| `uv/SKILL.md`       | uv, ruff, ty, pre-commit, packaging                   |
| `git/SKILL.md`      | Git workflows, branching, PRs, bisect                 |
| `cicd/SKILL.md`     | CI/CD, releases, tags, containers, publishing         |

Each skill has a `SKILL.md` entrypoint. Some have `references/` folders
with detailed submodules. Load these on demand — not all at once.
