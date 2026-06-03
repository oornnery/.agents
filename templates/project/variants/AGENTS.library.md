# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!-- Python library overlay. Keep package/API details in skills/python-library. -->

## Project Description

<!-- Library purpose, target users, public API expectations -->

## Stack Defaults

- **Python**: 3.12+
- **Package Manager**: uv
- **Build Backend**: existing backend, often hatchling
- **Lint and Format**: Ruff
- **Type Check**: ty and/or pyright when configured
- **Tests**: pytest

## Quick Commands

```bash
uv sync
uv run task check
uv run pytest -v
uv build
```

## Validation Entry Points

Use configured commands only:

```bash
uv run task check
uv run ruff format --check .
uv run ruff check .
uv run ty check src
uv run pytest -v
uv build
```

## Skill Routing

- Load `skills/python-library/SKILL.md` for public API, packaging, imports, examples, and build output.
- Load `skills/python/SKILL.md` for Python implementation details.
- Load `skills/docs/SKILL.md` when README, examples, changelog, or API docs change.
- Load `skills/verification/SKILL.md` before final checks and package build validation.
- Load `skills/project-state/SKILL.md` when public API decisions, release status, or next steps need durable state.

## Always-On Library Rules

- Public imports and documented APIs are contracts.
- Avoid breaking changes unless explicitly requested.
- Keep examples aligned with real behavior.
- Avoid import-time side effects.
- Verify build output before release/publish work.

## Project-Specific Guardrails

<!-- - Maintain backward compatibility within minor versions -->
<!-- - Keep import paths stable -->
