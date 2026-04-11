---
description: Python code conventions — applies to all Python files
globs: "**/*.py"
---

# Python Conventions

- Use `pathlib` over `os.path`
- f-strings only — no `.format()` or `%`
- `snake_case` functions/variables, `PascalCase` classes, `UPPER_SNAKE` constants
- Type all public functions — use modern syntax: `str | None`, `list[str]`
- Use `Annotated` style for FastAPI parameters and dependencies
- `logging` for app logs, `rich` for CLI output — never `print`
- Pydantic `BaseModel` for validation, `dataclass` for plain data
- IO at edges only — services and domain must be pure
- Prefer `uv` over direct `pip` workflows
- Never commit code that fails `ruff check` and `ty check` — these are the minimum quality gates
- Prefer early returns over deep nesting
- Use `Protocol` for structural typing, `ABC` for enforced hierarchies
- Use `enum.Enum` over string constants for fixed sets
- Use `__all__` to define public API in modules
- Use `@wraps` on all decorators
- Validate all external input at system boundaries
- Never use `eval()`, `exec()`, or `__import__()` with user input
- Use parameterized queries — never format SQL strings

## Anti-Gold-Plating

- Do not add features, refactoring, or cleanup beyond what was asked
- Do not add error handling for impossible scenarios -- trust framework guarantees
- Do not create abstractions for one-time operations -- three similar lines is fine
- Do not add docstrings, comments, or annotations to unchanged code
- Do not design for hypothetical future requirements
- Only validate at system boundaries, not internal code

## Comments

- Code should be commented for clarity and maintainability
- Comments explain WHY, never WHAT — well-named identifiers already describe what
- WHY comments for: hidden constraints, workarounds, non-obvious invariants, business rules
- Delete stale comments that no longer match the code
- Do not add comments to code you did not change
- Inline comments on the same line only for short clarifications

## Faithful Reporting

- Never claim "all tests pass" when output shows failures
- Never suppress failing checks to manufacture a green result
- Never characterize incomplete work as done
- Report outcomes faithfully — if something broke, say so
- Do not hedge confirmed results with unnecessary disclaimers
