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

| Rule                     | Scope                                             |
| ------------------------ | ------------------------------------------------- |
| `rules/python.md`        | Python style, anti-gold-plating, comments         |
| `rules/git.md`           | Git safety, production protection, worktrees      |
| `rules/documentation.md` | Markdown and documentation standards              |
| `rules/safety.md`        | Reversibility, blast radius, production safety    |

## Commands

Procedural workflows in `commands/`. Invoke when performing a task.

| Command                | When to use                                      |
| ---------------------- | ------------------------------------------------ |
| `commands/commit.md`   | Commit changes with logical commits              |
| `commands/refactor.md` | Deep audit, clean code, SOLID, 3-agent simplify  |
| `commands/review.md`   | Code review with 4 specialized reviewer agents   |
| `commands/verify.md`   | Adversarial verification — try to break the code |
| `commands/debug.md`    | Systematic debugging workflow                    |
| `commands/setup.md`    | Project onboarding and env verification          |
| `commands/plan.md`     | Planning with SDD, SPEC.md, ARCH.md, DDD, ADRs   |

## Skills

On-demand knowledge modules in `skills/`. Load the relevant skill
when working in its domain.

### Language and Runtime

| Skill             | When to use                                           |
| ----------------- | ----------------------------------------------------- |
| `python/SKILL.md` | General Python code, conventions, async, architecture |
| `uv/SKILL.md`     | uv, ruff, ty, pre-commit, packaging                   |
| `typer/SKILL.md`  | CLI applications                                      |

### Web and API

| Skill                        | When to use                                           |
| ---------------------------- | ----------------------------------------------------- |
| `fastapi/SKILL.md`           | FastAPI APIs, routes, dependencies                    |
| `httpx/SKILL.md`             | HTTP client patterns (sync/async)                     |
| `api-design/SKILL.md`        | REST conventions, OpenAPI, BFF, pagination, errors    |
| `jx/SKILL.md`                | Jinja server-rendered components (JX)                 |

### Frontend

| Skill                        | When to use                                           |
| ---------------------------- | ----------------------------------------------------- |
| `frontend/SKILL.md`          | Frontend bootstrap, JS/TS tooling, Tailwind, Basecoat |
| `design-system/SKILL.md`     | Design tokens, Figma workflow, component docs, a11y   |

### Data and Validation

| Skill                        | When to use                                           |
| ---------------------------- | ----------------------------------------------------- |
| `pydantic/SKILL.md`          | Data validation, serialization, settings              |

### Testing and Quality

| Skill                        | When to use                                           |
| ---------------------------- | ----------------------------------------------------- |
| `testing/SKILL.md`           | Test pyramid, pytest, coverage, mocking, BDD          |
| `tdd/SKILL.md`               | TDD cycle, red-green-refactor, test-first workflow    |

### Architecture and Design

| Skill                        | When to use                                           |
| ---------------------------- | ----------------------------------------------------- |
| `architecture/SKILL.md`      | DDD, Clean Architecture, Onion, SOLID, Clean Code     |
| `rca/SKILL.md`               | Root cause analysis, 5 Whys, postmortems              |

### DevOps and Tools

| Skill                        | When to use                                           |
| ---------------------------- | ----------------------------------------------------- |
| `git/SKILL.md`               | Git workflows, branching, PRs, bisect, worktrees      |
| `graphite/SKILL.md`          | Stacked PRs, incremental review, PR management        |
| `cicd/SKILL.md`              | CI/CD, releases, tags, containers, publishing         |
| `rtk/SKILL.md`               | RTK setup, custom filters, token optimization         |

### Documentation and Output

| Skill                        | When to use                                           |
| ---------------------------- | ----------------------------------------------------- |
| `markdown/SKILL.md`          | Markdown writing, structure, rumdl lint               |
| `documentation/SKILL.md`     | ADRs, changelogs, README, docstrings, auto-gen docs   |
| `rich/SKILL.md`              | Console output, tables, progress bars                 |

### Agent Development

| Skill                        | When to use                                           |
| ---------------------------- | ----------------------------------------------------- |
| `building-agents/SKILL.md`   | Building tool-using LLM agents, ReAct loop, harnesses |

Each skill has a `SKILL.md` entrypoint. Some have `references/` folders
with detailed submodules. Load these on demand — not all at once.
