# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!--
Python library overlay.
Use for packages published internally or externally where public API stability,
packaging, versioning, and usage documentation need stronger emphasis.
-->

## Project Description

<!-- Brief description of the library, target users, and supported use cases -->

## Stack

- **Python**: 3.12+
- **Build Backend**: hatchling
- **Package Manager**: uv
- **Lint and Format**: Ruff
- **Type Check**: ty
- **Tests**: pytest

## Quick Commands

```bash
uv sync
uv run pytest -v
uv run task check
uv build
```

## Validation Entry Points

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check src
uv run pytest -v
uv build
```

## Public API Rules

- treat exported modules, classes, functions, and CLI entrypoints as contracts
- define intended public API explicitly
- deprecate before breaking when practical
- keep examples and README usage aligned with the actual package surface
- avoid leaking internal module layout into public imports unless intentional

## Typing, Docs, and Compatibility

- type public functions and important data structures
- keep examples runnable and close to real usage
- make deprecations explicit before breaking
- avoid surprising import-time side effects

## Packaging Defaults

- keep metadata, dependencies, and entrypoints explicit in `pyproject.toml`
- verify build output before publishing
- treat README and changelog as part of the public surface

## Layout

```text
src/myapp/
├── __init__.py       # stable exports
├── api.py            # optional public facade
├── core/             # internal implementation
└── integrations/     # optional adapters or provider bindings

tests/
├── unit/
├── integration/
└── compatibility/
```

## Packaging and Release Notes

- keep `pyproject.toml` as the source of truth for metadata and dependencies
- ensure `README.md` reflects actual installation and usage
- verify build artifacts before publishing
- use changelog categories consistently for public releases

## Library Checklist

### Public Surface

- [ ] intended public imports are explicit
- [ ] examples match the real API
- [ ] breaking changes are obvious and documented
- [ ] import-time side effects are avoided

### Packaging

- [ ] metadata is complete in `pyproject.toml`
- [ ] build output is verified before publish
- [ ] versioning and changelog policy are clear

### Verification

- [ ] public API behavior is tested
- [ ] package import and build paths are tested
- [ ] compatibility or regression cases are covered

## Testing Focus

<!-- - public API behavior -->
<!-- - import and packaging correctness -->
<!-- - compatibility or regression coverage -->
<!-- - usage examples that should keep working -->

## Environment Variables

<!-- Include only if the library genuinely depends on env-driven behavior -->

## Project-Specific Guardrails

<!-- - Maintain backward compatibility within minor versions -->
<!-- - Keep import paths stable -->
<!-- - Do not add hidden side effects at import time -->
