---
name: python-library
description: Build, review, or validate Python packages and libraries where public API stability, packaging metadata, imports, examples, changelogs, build output, and compatibility matter.
---

# Python Library

Use for Python packages published internally or externally, or any codebase where imports and public APIs are contracts.

## Defaults

- Package manager: uv
- Build backend: existing backend, often hatchling
- Format/lint: Ruff
- Type check: ty and/or pyright when configured
- Tests: pytest
- Docs: load `skills/docs/SKILL.md`
- Final checks: load `skills/verification/SKILL.md`

## Workflow

1. Inspect `pyproject.toml`, package layout, exports, examples, README, tests, and build config.
2. Identify public API: modules, imports, functions, classes, CLI entrypoints, documented examples.
3. Preserve compatibility unless the user explicitly asks for a breaking change.
4. Keep package metadata, dependencies, optional extras, and entrypoints explicit.
5. Verify behavior, imports, packaging, and docs/examples touched by the change.

## Public API Rules

- Treat exported imports as contracts.
- Keep public facade explicit, usually `__init__.py` or `api.py`.
- Deprecate before breaking when practical.
- Avoid surprising import-time side effects.
- Keep examples aligned with real API.
- Do not leak internal module layout into public imports unless intentional.

## Suggested Layout

```text
src/myapp/
├── __init__.py
├── api.py
├── core/
└── integrations/

tests/
├── unit/
├── integration/
└── compatibility/
```

## Verification

- package import path
- public API behavior tests
- README/example commands when touched
- `uv build`
- configured format, lint, type, tests
