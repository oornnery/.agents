# HTTPX Testing

## Testing Strategy

Test outbound HTTP in layers:

- unit tests with `MockTransport` or injected fake clients
- integration tests only when request wiring + real upstream behavior matter
- avoid real network calls in routine test suites

## MockTransport Pattern

```python
import httpx


def handler(request: httpx.Request) -> httpx.Response:
    assert request.url.path == "/users/123"
    return httpx.Response(
        200,
        json={"id": "123", "name": "Alice"},
    )


transport = httpx.MockTransport(handler)
client = httpx.Client(
    base_url="https://api.example.com",
    transport=transport,
)
```

Assert via `MockTransport`:

- method
- path
- query params
- headers
- body shape

## Async Testing

```python
import httpx


def handler(request: httpx.Request) -> httpx.Response:
    return httpx.Response(204)


transport = httpx.MockTransport(handler)


async def test_delete_user() -> None:
    async with httpx.AsyncClient(
        base_url="https://api.example.com",
        transport=transport,
    ) as client:
        response = await client.delete("/users/123")
        assert response.status_code == 204
```

## Inject Clients, Not Patches

Prefer:

```python
service = UpstreamAPI(client=test_client)
```

Avoid:

- patching `httpx.get`
- patching `httpx.post`
- patching many call sites to fake one upstream

Injection keeps adapters testable + tests close to verified behavior.

## Failure Testing

Test unhappy paths explicitly:

```python
def timeout_handler(request: httpx.Request) -> httpx.Response:
    raise httpx.ReadTimeout("timed out")
```

Also test:

- 4xx and 5xx responses
- invalid payload shape
- retry exhaustion
- partial/malformed line streams when relevant

## Integration Test Boundaries

Use real integration tests to verify:

- auth with real service or local stub server
- streaming semantics
- certificate, proxy, or redirect behavior
- compatibility with concrete upstream contract

Keep narrower + slower than unit tests.

## Guardrails

- no tests depending on public internet services
- no asserting exact internal order of unrelated headers unless contract requires it
- no hiding network calls in fixtures that make failures hard to trace
- no over-mock; test adapter contract, not implementation trivia