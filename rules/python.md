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
- Never commit code that fails `ruff check`
- Prefer early returns over deep nesting
- Use `Protocol` for structural typing, `ABC` for enforced hierarchies
- Use `enum.Enum` over string constants for fixed sets
- Use `__all__` to define public API in modules
- Use `@wraps` on all decorators
- Validate all external input at system boundaries
- Never use `eval()`, `exec()`, or `__import__()` with user input
- Use parameterized queries — never format SQL strings
