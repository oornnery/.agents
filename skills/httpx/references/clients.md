# HTTPX Clients

## Choose the Right Client Shape

- use `httpx.Client` in sync code
- use `httpx.AsyncClient` only when full call path async
- create one client per application, request, or job boundary
- do not create fresh client inside tight loop

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

Centralize:

- `base_url`
- auth
- headers
- timeout
- redirect policy
- limits

## Dependency Injection Pattern

Inject configured client or factory. Do not construct new client inside every function.

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

Keeps:

- config centralized
- testing simpler
- retry, auth, logging consistent

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

- multiple requests share same signing rule
- headers must be refreshed or computed consistently
- auth concerns out of business code

## Async Boundaries

- keep whole adapter async if doing async HTTP
- do not call async client methods from sync code without explicit async boundary
- do not wrap blocking filesystem or DB calls into same function doing async HTTP unless workflow deliberately async end-to-end

## Limits and Lifecycle

Higher-throughput clients:

```python
limits = httpx.Limits(
    max_connections=100,
    max_keepalive_connections=20,
    keepalive_expiry=30.0,
)
```

Match lifecycle hooks to host app:

- app startup/shutdown for long-lived service clients
- request or job scope for short-lived integration units
- `with` or `async with` in scripts and one-off commands

## Event Hooks

Use for lightweight cross-cutting behavior:

- request/response logging
- metrics
- trace propagation

Keep small. Do not bury business logic in hooks.

## Guardrails

- do not hide auth refresh, retries, parsing inside one giant helper
- do not share one mutable client config object across unrelated upstreams
- do not silently swallow transport errors
- do not use global clients without clear lifecycle owner