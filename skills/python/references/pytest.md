# Pytest Reference

Complete Python testing workflow: environment setup, pytest ecosystem, test authoring, async/parallel execution, coverage, and failure diagnosis.

> **Gate Skill** — In gate mode, do not proceed if validation fails.
>
> *"Test behavior, not implementation."*

## Documentation

- pytest Docs: <https://docs.pytest.org/>
- pytest-asyncio: <https://pytest-asyncio.readthedocs.io/>
- pytest-cov: <https://pytest-cov.readthedocs.io/>
- pytest-xdist: <https://pytest-xdist.readthedocs.io/>

## Install

Core:

```bash
uv add --dev pytest pytest-cov
```

Recommended:

```bash
uv add --dev pytest-asyncio pytest-xdist pytest-mock
```

Optional (property-based):

```bash
uv add --dev hypothesis
```

## Baseline Pyproject.toml Config

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
  "-v",
  "--strict-markers",
  "--tb=short",
]
markers = [
  "slow: long-running tests",
  "integration: integration-level tests",
  "e2e: end-to-end flow tests",
]

[tool.coverage.run]
source = ["src"]
branch = true
omit = ["*/tests/*", "*/__init__.py"]

[tool.coverage.report]
show_missing = true
skip_covered = false
```

## Test Structure

```text
tests/
├── conftest.py
├── unit/
├── integration/
└── e2e/
```

Guidelines:

- Keep fixtures close to where they are used.
- Default to function-scoped fixtures for isolation.
- Avoid hidden global state between tests.
- Prefer explicit test data builders/factories.

## Test Authoring Patterns

### Unit Tests

- Mock external boundaries (network, DB, filesystem).
- One behavior assertion per test intent.
- Clear assertion messages for critical expectations.

### Integration Tests

- Validate real interactions between internal components.
- Isolate external systems via test containers/fakes.
- Mark with `@pytest.mark.integration`.

### API/contract Tests

- Validate status codes, payload shape, error contracts.
- Verify edge cases and invalid inputs.

## Async Testing

```python
import pytest


@pytest.mark.asyncio
async def test_async_flow():
    result = await service_call()
    assert result.status == "ok"
```

- Do not block the event loop inside async tests.
- Use async fixtures for async resources.
- Ensure teardown closes connections cleanly.

## Command Reference

### Fast Feedback

```bash
uv run pytest -v -x
```

### Specific File/test

```bash
uv run pytest tests/unit/test_users.py -v
uv run pytest tests/unit/test_users.py::test_create_user -v
```

### By Marker

```bash
uv run pytest -m "not slow" -v
uv run pytest -m integration -v
```

### Parallel (Xdist)

```bash
uv run pytest -n auto -v
uv run pytest -n 4 --dist=loadfile -v
```

### Coverage

```bash
uv run pytest -v --cov=src --cov-report=term-missing
uv run pytest -v --cov=src --cov-branch --cov-report=xml --cov-report=html --cov-report=term-missing
```

## Conftest and Fixtures

`tests/conftest.py` is the central config for shared fixtures, hooks, plugins, and markers.

- Function-scope fixtures for isolation.
- `tmp_path` for temporary files.
- Deterministic tests without timing/order dependencies.

## Failure Triage

### Debug Flags

```bash
uv run pytest -vv --maxfail=1 --tb=long
uv run pytest --lf -v        # last failed
uv run pytest --ff -v        # failed first
uv run pytest -rA -v         # full summary
uv run pytest --durations=10 -v  # slowest tests
```

### Failure Analysis

1. **What failed?** (test name)
2. **Expected?** vs **Actual?**
3. **Where?** (file:line)

| Symptom        | Likely Cause              |
| -------------- | ------------------------- |
| AssertionError | Logic bug                 |
| TypeError      | Wrong type passed         |
| AttributeError | Missing attribute         |
| Timeout        | Infinite loop or slow I/O |
| Flaky          | Race condition            |

### Fix Strategy

1. Reproduce locally.
2. Add minimal diagnostics.
3. Identify root cause.
4. Fix code (not only assertions).
5. Re-run affected checks.
6. Remove temporary diagnostics.

## Coverage Targets

| Type        | Target         |
| ----------- | -------------- |
| Unit        | > 80%          |
| Integration | Key flows      |
| E2E         | Critical paths |

- Prefer branch coverage for condition-heavy code.
- Track missing lines, justify intentional exclusions.
- Do not inflate coverage with low-value assertions.

## Test Quality Checklist

- [ ] Behavior-focused tests
- [ ] No shared mutable state
- [ ] No sleep/time coupling
- [ ] Fast and deterministic execution
- [ ] Clear assertions and failure messages
- [ ] Async tests do not block event loop
- [ ] Coverage report reviewed for real gaps
