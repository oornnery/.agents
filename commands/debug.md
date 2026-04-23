---
name: debug
description: Systematic debugging workflow for reproducing failures, isolating boundaries, finding root causes, and confirming fixes.
---

# Debug

Debug by evidence, not intuition. Reproduce failure, isolate boundary, confirm cause, validate fix.

## Process

### 1. Reproduce exactly

Capture:

- exact failing command, request, or test
- expected vs observed behavior
- traceback or error message
- relevant environment details

Examples:

```bash
uv run pytest tests/path/to/failing_test.py -v --tb=long
```

### 2. Inspect recent change surfaces

Read traceback bottom-up, then inspect:

```bash
git log --oneline -10
git diff
```

If regression likely, use `git bisect`.

### 3. Isolate the boundary

Narrow problem:

- input shape
- module boundary
- integration boundary
- state transition
- environment or configuration difference

One hypothesis at a time.

### 4. Verify the root cause

Targeted checks only:

- temporary `logging.debug(...)`
- temporary narrow probes
- `breakpoint()` when interactive debugging needed

Confirm suspected cause with minimal reproduction, not guess.

### 5. Fix the root cause

Smallest correct change:

- do not patch only symptom
- do not mix fix with refactoring
- do not broaden try/except to hide error
- add or update test when appropriate

### 6. Validate and clean up

Run failing check first, then broader validation matching blast radius. Remove all temporary debug statements and `breakpoint()` calls before finishing.

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
- do not leave debug artifacts in code
- do not claim root cause without confirming