---
name: debug
description: Systematic debugging workflow for isolating and fixing bugs. Use when the user reports a bug, error, or unexpected behavior.
---

# Debug

Systematically isolate and fix bugs. Do not guess — follow the evidence.

## Process

### 1. Reproduce

Before anything else, reproduce the issue:

- Get the exact error message, traceback, or unexpected output.
- Understand the expected behavior vs actual behavior.
- Identify the minimal steps to trigger the issue.
- Note the environment: Python version, OS, dependencies.

```bash
# Run the failing command or test
uv run pytest tests/path/to/failing_test.py -v --tb=long
```

### 2. Isolate

Narrow down the source:

- **Read the traceback** — start from the bottom (the actual error).
- **Check recent changes**: `git log --oneline -10` and `git diff HEAD~5`.
- **Binary search**: if the bug is a regression, use `git bisect`.
- **Narrow the module**: comment out or mock components to find the boundary.

```bash
# Find when the bug was introduced
git bisect start
git bisect bad HEAD
git bisect good <known-good-commit>
# Then test at each step
```

### 3. Hypothesize and Verify

Form a hypothesis about the root cause, then verify it:

- Add targeted `logging.debug()` or `print()` statements (temporary).
- Use `breakpoint()` (Python 3.7+) for interactive debugging.
- Check assumptions: types, values, state at the point of failure.
- Verify with a minimal reproduction test.

```python
# Quick hypothesis check
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("value at this point: %r", suspicious_variable)
```

### 4. Fix

Apply the minimal fix:

- Fix the root cause, not the symptom.
- Do not change unrelated code in the same fix.
- Add a test that would have caught the bug.
- Run the full validation suite to check for regressions.

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest -v
```

### 5. Clean Up

- Remove all temporary debug statements.
- Remove any `breakpoint()` calls.
- Verify the fix is clean: `git diff` before committing.

## Common Patterns

| Symptom                 | Check                                        |
| ----------------------- | -------------------------------------------- |
| `TypeError`             | Wrong type passed — check function signature |
| `AttributeError`        | Missing attribute — check object type        |
| `ImportError`           | Missing dep or circular import               |
| `KeyError`              | Missing dict key — check input data shape    |
| `TimeoutError`          | Slow I/O or infinite loop                    |
| `ValidationError`       | Pydantic model mismatch — check payload      |
| Flaky test              | Shared state, timing, or ordering issue      |
| Works locally, fails CI | Env difference — deps, Python version, OS    |

## Constraints

- Do not guess and patch -- understand root cause first.
- Do not add broad try/except to silence errors.
- Do not change tests to match broken behavior.
- Do not mix bug fixes with refactoring.
