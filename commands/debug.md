---
name: debug
description: Systematic debugging workflow for reproducing failures, isolating boundaries, finding root causes, and confirming fixes.
---

# Debug

Debug by evidence, not intuition. Reproduce the failure, isolate the boundary,
confirm the cause, then validate the fix.

## Process

### 1. Reproduce exactly

Capture:

- the exact failing command, request, or test
- expected behavior vs observed behavior
- traceback or error message
- relevant environment details

Examples:

```bash
uv run pytest tests/path/to/failing_test.py -v --tb=long
```

### 2. Inspect recent change surfaces

Read the traceback from the bottom up, then inspect:

```bash
git log --oneline -10
git diff
```

If the bug looks like a regression, use `git bisect`.

### 3. Isolate the boundary

Narrow the problem:

- input shape
- module boundary
- integration boundary
- state transition
- environment or configuration difference

Prefer one hypothesis at a time.

### 4. Verify the root cause

Use targeted checks only:

- temporary `logging.debug(...)`
- temporary narrow probes
- `breakpoint()` when interactive debugging is needed

Confirm the suspected cause with a minimal reproduction, not a guess.

### 5. Fix the root cause

Apply the smallest correct change:

- do not patch only the symptom
- do not mix the fix with refactoring
- do not broaden try/except to hide the error
- add or update a test when appropriate

### 6. Validate and clean up

Run the failing check first, then the broader validation that matches the blast
radius. Remove all temporary debug statements and `breakpoint()` calls before
finishing.

## Common checks

| Symptom                 | Check                                         |
| ----------------------- | --------------------------------------------- |
| `TypeError`             | wrong type passed; inspect the signature      |
| `AttributeError`        | wrong object type or missing initialization   |
| `ImportError`           | bad import path or circular import            |
| `KeyError`              | unexpected input shape                        |
| `TimeoutError`          | slow I/O, deadlock, or infinite loop          |
| `ValidationError`       | boundary model mismatch                       |
| flaky test              | shared state, timing, ordering, global state  |
| works locally, fails CI | dependency, Python version, or env mismatch   |

## Constraints

- do not guess before reproducing
- do not change tests to match broken behavior
- do not leave debug artifacts in the code
- do not claim root cause without confirming it
