# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!-- UV inline script overlay. Keep script details in skills/uv-script. -->

## Project Description

<!-- What script does, who runs it, side effects, repeatability expectations -->

## Stack Defaults

- **Python**: 3.12+
- **Runner**: uv
- **Packaging Style**: single-file script with inline metadata

## Quick Commands

```bash
uv run script.py
uv run --with pytest pytest -v
```

## Validation Entry Points

- run script with representative happy-path arguments
- run a representative failure path
- add or run lightweight tests when script is reused or critical

## Skill Routing

- Load `skills/uv-script/SKILL.md` for inline metadata, script safety, and representative runs.
- Load `skills/python/SKILL.md` for Python implementation details.
- Load `skills/verification/SKILL.md` for check selection.
- Load `skills/project-state/SKILL.md` only when script behavior, safety notes, or follow-ups need durable state.

## Always-On Script Rules

- Inline dependencies stay inside script metadata when the script is truly standalone.
- Side effects must be visible and repeatable or explicitly guarded.
- Do not silently overwrite files.
- Secrets stay outside the script.
- Promote to a package once multiple modules, commands, or shared logic appear.

## Project-Specific Guardrails

<!-- - Keep operational scripts deterministic -->
<!-- - Do not silently overwrite files -->
