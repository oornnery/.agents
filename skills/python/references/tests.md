# Python Testing Patterns

Pytest guidance for unit, integration, async, property, database, and CI tests.

## Use When

- writing or refactoring tests
- setting up pytest fixtures/config
- testing async/concurrent code
- mocking external services
- debugging failing tests
- adding CI coverage gates

## Test Choice

| Need                   | Pattern                                      |
| ---------------------- | -------------------------------------------- |
| pure function/class    | unit test, no I/O                            |
| component interaction  | integration test with real boundary/fake I/O |
| user workflow          | functional/e2e test                          |
| many input variants    | `pytest.mark.parametrize`                    |
| env/fs/time mutation   | `monkeypatch`, `tmp_path`, time freezer      |
| external dependency    | fake first, mock only at boundary            |
| async behavior         | `pytest.mark.asyncio` or project async setup |
| broad invariants       | Hypothesis/property tests                    |

## Core Rules

- One behavior per test.
- Arrange/Act/Assert shape.
- Tests independent; no shared mutable state.
- Prefer real domain objects over over-mocking.
- Mock/fake at system boundaries, not internals.
- Test error paths and edge cases, not only happy path.
- Coverage is signal, not goal; focus on meaningful branches.
- Name tests as `test_<unit>_<scenario>_<expected>`.

## Pytest Essentials

```python
import pytest

@pytest.mark.parametrize("value,expected", [(1, True), (0, False)])
def test_rule(value, expected):
    assert rule(value) is expected

def test_error_path():
    with pytest.raises(ValueError, match="invalid"):
        parse("bad")
```

Fixtures:

- use `yield` for setup/teardown
- keep fixture scope narrow by default
- session/module scope only for expensive immutable resources
- put shared fixtures in `conftest.py`
- avoid hidden fixture coupling

## Mocking

Prefer:

- fakes for domain collaborators
- `monkeypatch` for env/path/time/simple functions
- `unittest.mock` for external boundary calls

Avoid:

- mocking code under test
- asserting implementation calls when visible behavior is enough
- broad mocks that make tests pass without exercising logic

## Async

- mark async tests per project convention
- await every coroutine
- test cancellation/timeouts where behavior depends on them
- avoid real sleeps; use controllable clocks/events when possible
- keep sync and async call paths separate

## Temporary Files

- use `tmp_path`
- write minimal fixtures inline
- assert paths/content/side effects directly
- avoid relying on cwd unless behavior requires it

## Database Tests

- use transactions or disposable databases
- isolate test data per test
- seed only required rows
- test constraints, relationships, migrations, and query behavior
- catch N+1 with query counters where supported

## Property-Based Tests

Use when invariants matter more than example cases:

- parsers/serializers round-trip
- normalization/idempotency
- ordering/sorting
- validation boundaries
- numeric/string edge cases

Keep strategies constrained enough to produce meaningful failures.

## Retry/Time Behavior

- test success after transient failure
- test max retries reached
- test backoff/timeout config without waiting wall-clock time
- inject sleeper/clock when practical

## Markers and Selection

Common markers:

- `unit`
- `integration`
- `e2e`
- `slow`
- `network`
- `db`

Commands:

```bash
pytest -m unit
pytest -m "not slow"
pytest tests/path/test_file.py -v
pytest --maxfail=1 --tb=short
pytest --cov=src --cov-report=term-missing
```

## CI Defaults

- run unit tests on every push/PR
- run integration/e2e when dependencies exist or in scheduled pipeline
- fail on unexpected warnings only if codebase can sustain it
- publish coverage as trend; avoid blocking on arbitrary high percentage
- cache deps, not test artifacts that hide failures

## Debugging Failures

1. rerun exact failing test with `-vv --tb=long`
2. isolate single test/file
3. inspect fixture setup and shared state
4. check async awaits, time, cwd, env, temp files
5. reproduce without mocks if possible
6. fix root cause; do not weaken assertions to match bug

## Anti-Patterns

| Anti-pattern                  | Fix                                           |
| ----------------------------- | --------------------------------------------- |
| many behaviors in one test    | split by behavior                             |
| mocks everywhere              | fake boundary, use real domain objects        |
| sleeps in tests               | inject clock/event, wait on condition         |
| tests depend on order         | isolate data/state                            |
| brittle exact text assertions | assert stable fields or meaningful substrings |
| coverage chasing              | test important branches and regressions       |

## Minimal Config

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra"
markers = [
  "unit: fast isolated tests",
  "integration: component or external boundary tests",
  "slow: long-running tests",
]
```
