# Httpx Reference

HTTP client patterns with httpx for sync and async integrations, typed responses, retries, timeouts, and testing.

## Documentation

- httpx Docs: <https://www.python-httpx.org/>
- Timeouts: <https://www.python-httpx.org/advanced/timeouts/>
- Exceptions: <https://www.python-httpx.org/exceptions/>
- Transports and MockTransport: <https://www.python-httpx.org/advanced/transports/>

## Install

```bash
uv add httpx
```

## Client Selection

- Use `httpx.AsyncClient` in async apps (FastAPI, workers, async services).
- Use `httpx.Client` in sync-only scripts and CLIs.
- Reuse clients — do not create one per request.

## Canonical Async Client Factory

```python
import httpx


def build_async_http_client() -> httpx.AsyncClient:
    timeout = httpx.Timeout(connect=3.0, read=10.0, write=10.0, pool=3.0)
    limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)
    return httpx.AsyncClient(timeout=timeout, limits=limits, follow_redirects=False)
```

## FastAPI Lifecycle Pattern

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
import httpx


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = build_async_http_client()
    yield
    await app.state.http_client.aclose()


app = FastAPI(lifespan=lifespan)


def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client
```

## Request Pattern with Error Mapping

```python
import httpx


async def fetch_user(client: httpx.AsyncClient, user_id: int) -> dict:
    try:
        response = await client.get(f"https://api.example.com/users/{user_id}")
        response.raise_for_status()
        return response.json()
    except httpx.TimeoutException as exc:
        raise RuntimeError("Upstream timeout") from exc
    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code
        if status == 404:
            raise RuntimeError("User not found in upstream") from exc
        raise RuntimeError(f"Upstream error: {status}") from exc
```

## Typed Responses with Pydantic

```python
from pydantic import BaseModel, ConfigDict
import httpx


class UpstreamUser(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: int
    email: str
    active: bool


async def fetch_typed_user(client: httpx.AsyncClient, user_id: int) -> UpstreamUser:
    response = await client.get(f"https://api.example.com/users/{user_id}")
    response.raise_for_status()
    return UpstreamUser.model_validate(response.json())
```

## Retry Guidance

`httpx` has no built-in retry policy.

- Retry only idempotent methods by default (`GET`, `HEAD`).
- Use bounded attempts with backoff and jitter.
- Avoid retrying most `4xx` errors (except `429`).

Example with `tenacity`:

```python
from tenacity import retry, stop_after_attempt, wait_exponential_jitter
import httpx


@retry(stop=stop_after_attempt(3), wait=wait_exponential_jitter(initial=0.5, max=5))
async def fetch_with_retry(client: httpx.AsyncClient, url: str) -> httpx.Response:
    response = await client.get(url)
    response.raise_for_status()
    return response
```

## Testing with MockTransport

```python
import httpx
import pytest


def handler(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/users/1":
        return httpx.Response(200, json={"id": 1, "email": "a@example.com", "active": True})
    return httpx.Response(404, json={"detail": "not found"})


@pytest.mark.asyncio
async def test_fetch_typed_user() -> None:
    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport, base_url="https://api.example.com") as client:
        user = await fetch_typed_user(client, 1)
        assert user.id == 1
```

## Guardrails

- Set explicit timeout values — never use defaults in production.
- Reuse client instances for connection pooling.
- Validate payloads with typed schemas.
- Map transport/status errors to domain errors at boundaries.
- Log request metadata without leaking secrets.
