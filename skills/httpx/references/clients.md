# HTTPX Clients

## Choose the Right Client Shape

- use `httpx.Client` in sync code
- use `httpx.AsyncClient` only when the full call path is async
- create one client per application boundary, request boundary, or job boundary
- do not create a fresh client inside a tight loop

## Shared Client Configuration

```python
import httpx


client = httpx.Client(
    base_url="https://api.example.com",
    headers={
        "Accept": "application/json",
        "User-Agent": "myapp/1.0",
    },
    timeout=httpx.Timeout(10.0, connect=3.0),
    follow_redirects=True,
    limits=httpx.Limits(max_connections=50, max_keepalive_connections=20),
)
```

Good defaults to centralize:

- `base_url`
- auth
- headers
- timeout
- redirect policy
- limits

## Dependency Injection Pattern

Prefer injecting a configured client or factory instead of constructing a new
client inside every function.

```python
import httpx


class UpstreamAPI:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get_user(self, user_id: str) -> dict:
        response = await self._client.get(f"/users/{user_id}")
        response.raise_for_status()
        return response.json()
```

This keeps:

- config centralized
- testing simpler
- retry, auth, and logging behavior consistent

## Auth Patterns

### Bearer Token

```python
client = httpx.Client(
    base_url="https://api.example.com",
    headers={"Authorization": f"Bearer {token}"},
)
```

### Basic Auth

```python
client = httpx.Client(auth=httpx.BasicAuth(username, password))
```

### Custom Auth

```python
import httpx


class APIKeyAuth(httpx.Auth):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def auth_flow(self, request: httpx.Request):
        request.headers["X-API-Key"] = self.api_key
        yield request
```

Use custom auth when:

- multiple requests share the same signing rule
- headers must be refreshed or computed consistently
- you want auth concerns out of business code

## Async Boundaries

- keep the whole adapter async if it does async HTTP
- do not call async client methods from sync code without an explicit async
  boundary
- do not wrap blocking filesystem or database calls into the same function that
  performs async HTTP unless that workflow is deliberately async end-to-end

## Limits and Lifecycle

For higher-throughput clients:

```python
limits = httpx.Limits(
    max_connections=100,
    max_keepalive_connections=20,
    keepalive_expiry=30.0,
)
```

Use lifecycle hooks that match the host app:

- app startup/shutdown for long-lived service clients
- request or job scope for short-lived integration units
- `with` or `async with` in scripts and one-off commands

## Event Hooks

Use event hooks for lightweight cross-cutting behavior such as:

- request or response logging
- metrics
- trace propagation

Keep them small. Do not bury business logic in hooks.

## Guardrails

- do not hide auth refresh, retries, and parsing inside one giant helper
- do not share one mutable client config object across unrelated upstreams
- do not silently swallow transport errors
- do not use global clients without a clear lifecycle owner
