---
name: testing
description: Testing strategy and pytest workflow — test pyramid, what to test, mocking, fixtures, async, coverage, failure diagnosis. Load when writing, planning, or debugging tests.
---

# Testing

Complete testing skill: strategy, pytest mechanics, async, parallel
execution, coverage, and failure diagnosis.

> _"Test behavior, not implementation."_

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

## Test Pyramid

```text
         /  E2E  \          <- few, slow, high confidence
        / Integration \     <- moderate, real interactions
       /     Unit      \    <- many, fast, isolated
```

| Layer       | Purpose                         | Speed  | Count    |
| ----------- | ------------------------------- | ------ | -------- |
| Unit        | Single function/class behavior  | Fast   | Many     |
| Integration | Component interactions, real IO | Medium | Moderate |
| E2E         | Full user flows, API contracts  | Slow   | Few      |

## What to Test

- **Business logic** — the core of your application.
- **Edge cases** — empty inputs, boundaries, nulls, max values.
- **Error paths** — what happens when things fail.
- **API contracts** — status codes, response shapes, error formats.
- **Security boundaries** — auth, authorization, input validation.

## What NOT to Test

- **Framework internals** — don't test that FastAPI routes work.
- **Implementation details** — don't test private methods directly.
- **Trivial code** — simple getters, `__init__` with assignment.
- **Generated code** — migrations, lock files, vendor code.
- **Third-party libraries** — they have their own tests.

## Test Structure

```text
tests/
├── conftest.py
├── unit/
├── integration/
└── e2e/
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

## Test Authoring Patterns

### Unit Tests

- Mock external boundaries (network, DB, filesystem).
- One behavior assertion per test intent.
- Clear assertion messages for critical expectations.

### Integration Tests

- Validate real interactions between internal components.
- Isolate external systems via test containers/fakes.
- Mark with `@pytest.mark.integration`.

### API/Contract Tests

- Validate status codes, payload shape, error contracts.
- Verify edge cases and invalid inputs.

### Test Naming

```python
# Good — describes the behavior
def test_expired_token_returns_401():
def test_empty_cart_has_zero_total():
def test_duplicate_email_raises_conflict():

# Bad — says nothing
def test_user():
def test_api():
def test_error():
```

## Mocking Strategy

### When to Mock

- External APIs and services (network boundaries).
- Time-dependent behavior (`datetime.now`, `time.time`).
- Expensive operations you've already tested elsewhere.
- Non-deterministic behavior (random, UUIDs).

### When NOT to Mock

- Your own code — test the real thing.
- Database queries in integration tests — use a real test DB.
- Simple utilities — they're fast enough to run directly.

### Mock Hierarchy (Prefer Higher)

1. **Fakes** — in-memory implementations (best for repositories).
2. **Stubs** — return fixed values (good for external services).
3. **Mocks** — verify interactions (use sparingly, couples to implementation).

```python
# PREFER: Fake repository
class FakeUserRepo:
    def __init__(self):
        self.users = {}

    def get(self, user_id: str) -> User | None:
        return self.users.get(user_id)

    def save(self, user: User) -> None:
        self.users[user.id] = user
```

## Fixtures

- **Function scope** by default — isolation between tests.
- **Session scope** only for expensive, read-only resources (DB connection).
- **Factory fixtures** over static data — each test gets unique instances.
- **Keep fixtures close** — conftest.py in the same directory.

```python
import pytest
from uuid import uuid4


@pytest.fixture
def make_user():
    def _make(name: str = "Test User", **kwargs) -> User:
        return User(id=str(uuid4()), name=name, **kwargs)
    return _make


def test_user_creation(make_user):
    user = make_user(name="Alice")
    assert user.name == "Alice"
```

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

### Specific File/Test

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

- **Branch coverage** over line coverage — catches missed conditions.
- **Don't chase 100%** — diminishing returns after ~90%.
- Track missing lines, justify intentional exclusions.
- Never inflate coverage with meaningless assertions.

## Test Isolation Checklist

- No shared mutable state between tests.
- No dependency on test execution order.
- No `time.sleep` or real timers.
- No network calls in unit tests.
- Each test can run independently.
- Cleanup after yourself (tmp files, DB records).

## BDD and Property-Based Testing

See `skills/tdd/SKILL.md` for BDD patterns (Given/When/Then, acceptance
criteria mapping) and property-based testing with Hypothesis.

## Test Integrity

- **Prioritize immediate correction of failing tests** — a red suite is
  a broken feedback loop.
- Never skip or `xfail` a test without a linked issue or clear reason.
- Never delete a failing test to make the suite green.
- If a test is flaky, fix the root cause (race condition, shared state,
  time dependency) — do not add retries.

## Related Skills

- `skills/tdd/SKILL.md` — TDD cycle and methodology.
- `frontend/references/testing.md` — Vitest, Solid Testing Library.
