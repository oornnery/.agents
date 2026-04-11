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

| Rule                     | Scope                                                |
| ------------------------ | ---------------------------------------------------- |
| `rules/python.md`        | Python style, anti-gold-plating, comments            |
| `rules/git.md`           | Git safety, production protection, worktrees         |
| `rules/documentation.md` | Markdown and documentation standards                 |
| `rules/safety.md`        | Reversibility, blast radius, production safety       |
| `rules/output.md`        | Response style, anti-hallucination, token efficiency |
| `rules/uv.md`            | uv over pip, uv run, uvx, lockfile conventions       |

## Commands

Procedural workflows in `commands/`. Invoke when performing a task.

| Command                | When to use                                       |
| ---------------------- | ------------------------------------------------- |
| `commands/commit.md`   | Commit changes with logical commits               |
| `commands/refactor.md` | Deep audit, clean code, SOLID, 3-agent simplify   |
| `commands/review.md`   | Code review with 4 specialized reviewer agents    |
| `commands/verify.md`   | Adversarial verification -- try to break the code |
| `commands/debug.md`    | Systematic debugging workflow                     |
| `commands/setup.md`    | Project onboarding and env verification           |
| `commands/plan.md`     | Planning with SDD, SPEC.md, ARCH.md, DDD, ADRs    |

## Skills

On-demand knowledge modules in `skills/`. Load the relevant skill
when working in its domain. Each has a `SKILL.md` entrypoint and
optional `references/` submodules.

| Category              | Skills                                                       |
| --------------------- | ------------------------------------------------------------ |
| Language and Runtime  | `python`, `uv`, `typer`                                      |
| Web and API           | `fastapi`, `httpx`, `api-design`, `jx`                       |
| Frontend              | `frontend`, `design-system`                                  |
| Data and Validation   | `pydantic`                                                   |
| Testing and Quality   | `testing`, `tdd`                                             |
| Architecture          | `architecture`, `rca`                                        |
| DevOps and Tools      | `git`, `graphite`, `cicd`, `rtk`                             |
| Documentation         | `markdown`, `documentation`, `rich`                          |
| Agent Development     | `building-agents`                                            |
