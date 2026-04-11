---
name: httpx
description: HTTP client patterns with httpx -- sync/async, typed responses, retries, timeouts, testing. Load when making HTTP requests or integrating with external APIs.
---

# Httpx

HTTP client patterns. See [httpx docs](https://www.python-httpx.org/).

```bash
uv add httpx
uv add tenacity                      # Retry with backoff/jitter
```

## Canonical Async Client Factory

```python
import httpx


def build_async_http_client() -> httpx.AsyncClient:
    timeout = httpx.Timeout(connect=3.0, read=10.0, write=10.0, pool=3.0)
    limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)
    return httpx.AsyncClient(timeout=timeout, limits=limits, follow_redirects=False)
```

## FastAPI Lifecycle

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
import httpx


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = build_async_http_client()
    yield
    await app.state.http_client.aclose()


def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client
```

## Testing with MockTransport

```python
def handler(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/users/1":
        return httpx.Response(200, json={"id": 1, "email": "a@example.com"})
    return httpx.Response(404, json={"detail": "not found"})


async def test_fetch_user() -> None:
    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport, base_url="https://test") as client:
        response = await client.get("/users/1")
        assert response.status_code == 200
```

## Guardrails

- Set explicit timeout values -- never use defaults in production.
- Reuse client instances for connection pooling.
- Use `AsyncClient` in async apps, `Client` in sync scripts.
- Validate responses with Pydantic models.
- Map transport/status errors to domain errors at boundaries.
- Retry only idempotent methods (`GET`, `HEAD`), with backoff and jitter.
- Use `http2=True` for multiplexed connections to HTTP/2 servers.
