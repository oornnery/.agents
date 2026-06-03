# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!-- Python CLI overlay. Keep CLI details in skills/python-cli. -->

## Project Description

<!-- Who uses the CLI, key workflows, automation expectations -->

## Stack Defaults

- **Python**: 3.12+
- **Package Manager**: uv
- **Simple CLI**: argparse + rich-argparse
- **Command App**: Typer + Rich when multiple commands need richer UX
- **TUI**: Textual only for real interactive terminal apps

## Quick Commands

```bash
uv sync
uv run python -m myapp --help
uv run task check
uv run pytest -v
```

## Validation Entry Points

Use configured commands only:

```bash
uv run task check
uv run ruff format --check .
uv run ruff check .
uv run ty check src
uv run pytest -v
```

## Skill Routing

- Load `skills/python-cli/SKILL.md` for CLI contracts, UX, stdout/stderr, exit codes, and tests.
- Load `skills/python/SKILL.md` for Python implementation details.
- Load `skills/rich/SKILL.md` or `skills/textual/SKILL.md` only when terminal UX needs it.
- Load `skills/verification/SKILL.md` before final checks.
- Load `skills/project-state/SKILL.md` when CLI behavior, safety notes, or next steps need durable state.

## Always-On CLI Rules

- `--help` stays accurate.
- Success uses stdout and exit `0`; errors use stderr and non-zero exit.
- Interactive prompts must be skippable for automation.
- Destructive commands require explicit intent.
- Secrets are never printed.

## Project-Specific Guardrails

<!-- - Preserve machine-readable output shape -->
<!-- - Keep prompts skippable for CI and scripts -->
