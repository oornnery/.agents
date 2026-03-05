---
name: python
description: Python best practices, conventions, and uv-based toolchain. Use when writing, reviewing, or refactoring Python code. Covers code style, type hints, async patterns, logging, dependency management, validation pipeline, and routes to submodules (FastAPI, JX, testing, HTTP client, TUI, CLI).
---

# Python

Official Python skill for writing clean, Pythonic code with modern tooling.

> *"Beautiful is better than ugly. Explicit is better than implicit. Simple is better than complex."*
> — The Zen of Python

## Documentation

- Python: <https://docs.python.org/3/>
- uv: <https://docs.astral.sh/uv/>
- uv LLMs: <https://docs.astral.sh/uv/llms.txt>
- Ruff: <https://docs.astral.sh/ruff/>
- Ruff LLMs: <https://docs.astral.sh/ruff/llms.txt>
- Ty: <https://ty.astral.sh/>
- pytest: <https://docs.pytest.org/>
- rumdl: <https://rumdl.com/docs/>
- Rich: <https://rich.readthedocs.io/en/stable/>
- httpx: <https://www.python-httpx.org/>
- Pydantic: <https://docs.pydantic.dev/latest/>
- Typer: <https://typer.tiangolo.com/>

## Submodules

| Submodule                | When to load                                    |
| ------------------------ | ----------------------------------------------- |
| `fastapi/SKILL.md`       | FastAPI APIs and Pydantic models                |
| `jx/SKILL.md`            | Jinja-based server-rendered components          |
| `references/pytest.md`   | Test authoring, coverage, failure triage        |
| `references/httpx.md`    | Outbound HTTP calls (sync/async)                |
| `references/typer.md`    | CLI applications                                |
| `references/rich.md`     | Console output, tables, progress bars           |
| `references/pydantic.md` | Validation, serialization, model patterns       |
| `references/uv.md`       | uv, ruff, ty, rumdl, pytest, taskipy, packaging |
| Architecture (below)     | Layer boundaries and project layout             |

---

## The Zen of Python

Key principles to apply as a design lens:

- **Explicit over implicit** — no magic, make intent clear.
- **Simple over complex** — the simplest solution that works.
- **Flat over nested** — early returns, avoid deep indentation.
- **Readability counts** — code is read far more than written.
- **Errors should never pass silently** — handle or propagate, never swallow.
- **One obvious way** — follow established patterns, don't invent new ones.

Full text: `python -c "import this"`

---

## Code Conventions

### Style

- `pathlib` over `os.path` — always.
- f-strings only — avoid `.format()` and `%` formatting.
- Prefer early returns over deep nesting.
- Avoid mutable global state.
- Use `__all__` to define public API in modules.

```python
# DO THIS
from pathlib import Path

def load_config(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())
```

```python
# DO NOT DO THIS
import os

def load_config(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.loads(f.read())
    else:
        return {}
```

### Naming

- `snake_case` for functions, variables, modules.
- `PascalCase` for classes.
- `UPPER_SNAKE` for constants.
- Prefix private helpers with `_`.
- Descriptive names over abbreviations — `user_count`, not `uc`.

### Imports

- Group: stdlib → third-party → local, separated by blank lines.
- Absolute imports preferred over relative.
- Let Ruff sort and organize via `isort` rules.

### Data Structures

- Use `dataclasses` for plain data containers.
- Use Pydantic `BaseModel` when validation/serialization is needed.
- Use `TypedDict` for dictionaries with known keys.
- Use `NamedTuple` for lightweight immutable records.
- Prefer `enum.Enum` over string constants for fixed sets.

```python
from dataclasses import dataclass, field
from enum import Enum


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass(frozen=True, slots=True)
class User:
    name: str
    email: str
    status: Status = Status.ACTIVE
    tags: list[str] = field(default_factory=list)
```

---

## Type Hints

- Use modern syntax: `str | None`, `list[str]`, `dict[str, int]`.
- Type all public functions and methods.
- Use `TypeVar` and `Generic` for reusable typed containers.
- Use `Protocol` for structural subtyping (duck typing with types).

```python
from typing import TypedDict


class UserPayload(TypedDict):
    name: str
    email: str
    active: bool
```

```python
from typing import Protocol


class Serializable(Protocol):
    def to_dict(self) -> dict: ...
```

---

## Async

- Use `asyncio` patterns only — never block the event loop.
- Prefer `async with` for async resources.
- Use `asyncio.gather` with explicit error handling.
- Use `asyncio.TaskGroup` (3.11+) for structured concurrency.

```python
import asyncio


async def fetch_all(urls: list[str]) -> list[dict]:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch(url)) for url in urls]
    return [t.result() for t in tasks]
```

### Async Anti-Patterns

```python
# DO NOT DO THIS — blocks the event loop
import time

async def bad_handler():
    time.sleep(5)  # blocks everything

# DO THIS
import asyncio

async def good_handler():
    await asyncio.sleep(5)
```

---

## Logging and Console Output

- Use stdlib `logging` — **never `print` in application/library code.**
- Configure logging once at the entrypoint with `RichHandler`.
- `logging` → operational logs. `rich.console.Console` → user-facing CLI output.

```python
import logging

logger = logging.getLogger(__name__)

# Entrypoint setup
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],
)
```

See `references/rich.md` for full console output patterns.

---

## Toolchain

| Tool      | Purpose                                            |
| --------- | -------------------------------------------------- |
| `uv`      | Package manager, virtualenv, runner                |
| `ruff`    | Formatter + linter (replaces black, isort, flake8) |
| `ty`      | Type checker (Astral)                              |
| `rumdl`   | Markdown linter and formatter                      |
| `pytest`  | Test runner                                        |
| `taskipy` | Optional task runner                               |

Config lives in `pyproject.toml`. Lock file: `uv.lock`.

### Quick Reference

```bash
uv sync                                   # Install from lockfile
uv add <pkg>                              # Add runtime dep
uv add --dev <pkg>                        # Add dev dep
uv run ruff format . && uv run ruff check . --fix  # Format + lint
uv run ty check                           # Type check
uv run rumdl check . && uv run rumdl fmt .          # Markdown lint + format
uv run pytest -v                          # Test
```

### Validation Sequence (Fail Fast)

```bash
uv run ruff format --check .     # 1. Format
uv run ruff check .              # 2. Lint
uv run rumdl check .             # 3. Markdown
uv run ty check                  # 4. Types
uv run pytest -v                 # 5. Tests
```

See `references/uv.md` for full uv workflow, pyproject.toml config, packaging, publishing, and taskipy setup.

---

## Error Handling

- Use specific exceptions — never bare `except:`.
- Let unexpected errors propagate.
- Create domain exceptions for business logic errors.
- Use `from` for exception chaining.

```python
class UserNotFoundError(Exception):
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        super().__init__(f"User not found: {user_id}")


def get_user(user_id: str) -> User:
    try:
        return repo.fetch(user_id)
    except KeyError as exc:
        raise UserNotFoundError(user_id) from exc
```

---

## Context Managers

- Use `contextlib.contextmanager` / `asynccontextmanager` for resource management.
- Prefer `with`/`async with` over manual setup/teardown.

```python
from contextlib import asynccontextmanager
import httpx


@asynccontextmanager
async def http_session():
    async with httpx.AsyncClient(timeout=10.0) as client:
        yield client
```

---

## Pattern Matching (3.10+)

Use `match`/`case` for structural dispatch — type routing, command handling, data destructuring. Use `if/elif` for simple boolean/range checks.

```python
match response.status_code:
    case 200:
        return response.json()
    case 404:
        raise NotFoundError()
    case status if 500 <= status < 600:
        raise ServerError(status)

match event:
    case {"type": "click", "button": button}:
        return f"Clicked {button}"
    case {"type": "scroll", "direction": "up" | "down" as d}:
        return f"Scrolled {d}"
    case _:
        return "Unknown event"
```

Do not use `match` for trivial boolean checks (`match x > 0: case True: ...`).

---

## Iterators and Generators

Use generators for lazy evaluation — process large data without loading everything into memory. Prefer generator expressions over list comprehensions when you don't need the full list.

```python
from collections.abc import Iterator

def read_chunks(path: Path, size: int = 8192) -> Iterator[bytes]:
    with open(path, "rb") as f:
        while chunk := f.read(size):  # walrus operator
            yield chunk

# Lazy (memory efficient) vs eager (loads all)
total = sum(len(line) for line in open("data.txt"))  # generator
lines = [line.strip() for line in open("data.txt")]   # list
```

Key `itertools`: `chain` (merge iterables), `islice` (take N), `batched` (3.12+, chunk items), `groupby` (group sorted data).

Walrus operator (`:=`) — use for assignment in expressions. Avoid in complex expressions where it hurts readability.

---

## Decorators

- Always use `@wraps` — without it, the decorated function loses `__name__`, `__doc__`, `__module__`.
- Use `ParamSpec` + `TypeVar` for typed decorators.

```python
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        logger.info("Calling %s", func.__name__)
        return func(*args, **kwargs)
    return wrapper
```

For parameterized decorators (e.g., `@retry(max_attempts=3)`), use a three-level nesting: outer function → decorator → wrapper, all with `@wraps`.

---

## Comprehensions

- Use for simple transforms and filters. Max one level of nesting.
- If the logic needs nested loops, complex conditions, or side effects — use a regular loop.

```python
names = [user.name for user in users if user.active]   # list
lookup = {user.id: user for user in users}              # dict
unique_roles = {user.role for user in users}             # set
inverted = {v: k for k, v in mapping.items()}            # invert
```

---

## Concurrency

| Need                         | Tool                               |
| ---------------------------- | ---------------------------------- |
| I/O-bound (HTTP, DB, files)  | `asyncio` or `ThreadPoolExecutor`  |
| CPU-bound (compute, parsing) | `ProcessPoolExecutor`              |
| Simple parallel tasks        | `concurrent.futures` (easiest API) |
| Full async app               | `asyncio` (see Async section)      |

- Use `asyncio.to_thread` to bridge blocking code into async contexts.
- Never mix `asyncio` and `threading` without `to_thread`.
- Set explicit `max_workers` — don't rely on defaults.
- Always handle exceptions from futures.

---

## Abstract Base Classes Vs Protocol

### When to Use Which

| Need                                        | Use        |
| ------------------------------------------- | ---------- |
| Enforce method implementation in subclasses | `ABC`      |
| Structural typing (duck typing with types)  | `Protocol` |
| Third-party classes you can't modify        | `Protocol` |
| Internal class hierarchies                  | `ABC`      |

### ABC Pattern

```python
from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def get(self, id: str) -> dict: ...

    @abstractmethod
    def save(self, id: str, data: dict) -> None: ...


class PostgresRepo(Repository):
    def get(self, id: str) -> dict:
        return self.db.fetch(id)

    def save(self, id: str, data: dict) -> None:
        self.db.upsert(id, data)
```

### Protocol Pattern (Preferred for Loose Coupling)

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Renderable(Protocol):
    def render(self) -> str: ...


# Any class with a render() method satisfies this — no inheritance needed
class HtmlPage:
    def render(self) -> str:
        return "<html>...</html>"


def output(item: Renderable) -> None:
    print(item.render())  # HtmlPage works here without inheriting Renderable
```

---

## Security

### Secrets and Credentials

```python
import secrets
from os import environ

# Generate secure tokens
token = secrets.token_urlsafe(32)
api_key = secrets.token_hex(16)

# Read secrets from environment — never hardcode
db_password = environ["DB_PASSWORD"]
```

### Hashing

```python
import hashlib

# For integrity checks (not passwords)
digest = hashlib.sha256(data).hexdigest()

# For passwords — use a proper KDF
from hashlib import scrypt

hashed = scrypt(password.encode(), salt=salt, n=16384, r=8, p=1)
```

### Input Sanitization

- Validate all external input at system boundaries.
- Use Pydantic models for structured validation (see `references/pydantic.md`).
- Never use `eval()`, `exec()`, or `__import__()` with user input.
- Use parameterized queries — never format SQL strings.

```python
# DO NOT DO THIS
query = f"SELECT * FROM users WHERE id = '{user_id}'"

# DO THIS
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### File System Safety

```python
from pathlib import Path

# Prevent path traversal
def safe_path(base: Path, user_input: str) -> Path:
    resolved = (base / user_input).resolve()
    if not resolved.is_relative_to(base.resolve()):
        raise ValueError("Path traversal detected")
    return resolved
```

---

## Performance and Caching

- **Profile before optimizing** — `uv run python -m cProfile -s cumtime app/main.py`
- `@cache` — unbounded, for pure functions with hashable args.
- `@lru_cache(maxsize=N)` — bounded, for functions with many unique inputs.
- `__slots__` / `@dataclass(slots=True)` — memory efficiency for data-heavy classes.
- Prefer generators over lists for large sequences.
- Use `str.join()` over `+` concatenation in loops.

---

## Docstrings

Use Google style. Only document non-obvious behavior — don't restate what the signature already says.

```python
def retry_request(
    url: str,
    max_attempts: int = 3,
    backoff: float = 1.0,
) -> httpx.Response:
    """Send a GET request with exponential backoff retry.

    Retries on 5xx responses and connection errors.
    Does not retry on 4xx client errors.

    Args:
        url: Target URL.
        max_attempts: Maximum number of attempts before raising.
        backoff: Initial delay between retries in seconds, doubled each attempt.

    Returns:
        The successful HTTP response.

    Raises:
        httpx.HTTPStatusError: If all attempts fail with a server error.
        httpx.ConnectError: If the server is unreachable after all attempts.
    """
```

### Rules

- Type all parameters in the signature, not in the docstring.
- Document `Raises` only for exceptions callers should handle.
- Skip docstrings on trivial/obvious methods (`__init__` with simple assignment, one-liner helpers).
- Modules and classes get a one-line docstring if the name isn't self-explanatory.

---

## Pydantic (Brief)

Pydantic v2 is the standard for data validation and serialization in Python. Use it for API payloads, config, and any data that crosses system boundaries.

```bash
uv add pydantic pydantic-settings
```

```python
from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    model_config = ConfigDict(strict=True, frozen=True)

    name: str = Field(min_length=1, max_length=100)
    email: str
    age: int = Field(ge=0, le=150)
```

See `references/pydantic.md` for validators, serialization, settings, and advanced patterns.

---

## Key Libraries (Brief)

### Rich — Console Output and Formatting

Rich provides styled console output, tables, progress bars, tracebacks, and logging integration. Use it for all user-facing CLI output.

```bash
uv add rich
```

See `references/rich.md` for full patterns.

### Httpx — HTTP Client

Modern async/sync HTTP client with connection pooling, timeouts, and typed responses. Use instead of `requests` in new projects.

```bash
uv add httpx
```

See `references/httpx.md` for client factories, error mapping, and testing.

### Typer — CLI Framework

Type-hint-driven CLI builder on top of Click. Handles argument parsing, help generation, and shell completion.

```bash
uv add typer rich
```

See `references/typer.md` for command patterns, async integration, and testing.

---

## Architecture Boundaries

### Layer Model

```text
Edges    → app/views/ (HTML) + app/api/ (JSON)
Core     → app/services/ + app/models/
Infra    → app/db.py, app/config.py, adapters/
```

### Rules

- IO at edges only — services and domain must be pure.
- Business logic lives in `services/` and `domain/`.
- Keep adapters isolated — wrap external APIs behind interfaces.
- Dependencies point inward: edges → core → infra (never reverse).

### Canonical Layout

```text
src/myapp/
├── main.py          # Entry point
├── api/             # JSON endpoints
├── views/           # HTML pages
├── services/        # Business logic
├── domain/          # Models, types, enums
├── adapters/        # External service wrappers
├── middlewares/     # Request/response processing
├── models/          # Pydantic models (if separate from domain)
├── templates/       # Jinja templates (if using server-side rendering)
├── core/            # Core utilities, exceptions, context managers
└── settings.py      # Configuration
tests/
├── conftest.py
├── unit/
├── integration/
└── e2e/
```

### Guidelines

- Keep layers thin — a route handler should call a service, not contain logic.
- Domain models should have no framework imports.
- Use dependency injection to wire adapters into services.
- Config comes from environment, not hardcoded values.

---

## Guardrails

- Prefer `uv` over direct `pip` workflows.
- Keep local checks aligned with CI.
- Fail fast on lint/type errors before running full test suites.
- Never commit code that fails `ruff check`.
- Type check public APIs before merging.
- Review coverage gaps — don't inflate with low-value assertions.
