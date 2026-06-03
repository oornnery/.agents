# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!-- Python overlay. Keep detailed Python guidance in skills/python. -->

## Project Description

<!-- What this Python project does, main constraints, critical boundaries -->

## Stack Defaults

- **Python**: 3.12+
- **Package Manager**: uv
- **Lint and Format**: Ruff
- **Type Check**: ty and/or pyright when configured
- **Tests**: pytest
- **Validation**: Pydantic at external boundaries
- **HTTP Client**: HTTPX when outbound HTTP is needed

## Quick Commands

```bash
uv sync
uv run python -m myapp
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
uv run pyright
uv run pytest -v
uv run task sec
uv run bandit -r src
uv run pip-audit
```

Do not add tools only because this template lists them.

## Skill Routing

- Load `skills/python/SKILL.md` for Python implementation, typing, testing, packaging, async, config, errors, performance, or uv details.
- Load `skills/verification/SKILL.md` before final validation or check repair.
- Load `skills/project-state/SKILL.md` when work changes scope, decisions, memory, validation, or next steps.
- Load `skills/security/SKILL.md` when work touches trust boundaries.

## Always-On Python Rules

- Treat `pyproject.toml` and lockfiles as source of truth.
- Use `uv` workflows; do not mix package managers.
- Keep IO at edges and core logic testable.
- Validate external input at boundaries, then pass typed values inward.
- Keep settings and secrets outside source code.
- Prefer existing repo layout and conventions over template examples.

## Project-Specific Guardrails

<!-- - Keep public imports stable -->
<!-- - Do not bypass typed settings -->
<!-- - Avoid framework-specific logic in core/ -->
