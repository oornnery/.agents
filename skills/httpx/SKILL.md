---
name: httpx
description: HTTPX client patterns for Python services, scripts, and
  applications. Covers client lifetime, sync and async usage, timeouts,
  streaming, auth, retries, error handling, and testing with mock transports.
  Load when working with outbound HTTP in Python.
---

# HTTPX

Use this skill when the work is primarily outbound HTTP in Python.

## Boundary

Use this skill for:

- sync and async HTTP clients
- shared client configuration
- timeouts, limits, redirects, and connection reuse
- uploads, downloads, and streaming
- auth headers and custom auth flows
- testing HTTP integrations without real network calls

Pair with:

- `python` for general Python conventions and project workflow
- `security` when requests touch auth, secrets, SSRF risk, or untrusted URLs
- `quality` when flaky integrations or retry behavior need tighter guards

## Reference Map

- `references/clients.md` -- client lifetime, shared config, auth, limits,
  transports, and async boundaries
- `references/requests-and-streaming.md` -- request shapes, file transfer,
  pagination, and streaming patterns
- `references/testing.md` -- `MockTransport`, dependency injection, fake
  responses, and integration test boundaries

## Assets

- `assets/client.py` -- a small typed `crudcrud.com` client example with shared
  configuration and explicit CRUD methods
- `assets/testing.py` -- a focused test of the same `crudcrud.com` adapter
  using `MockTransport` instead of real network calls

## What Stays Here

Keep this file focused on defaults and guardrails.

- keep here: client lifetime rules, timeout defaults, error handling stance,
  and review cues
- move to refs: long examples, auth variants, streaming details, transports,
  and testing patterns
- use assets when a runnable example is clearer than another long code block

## Core Defaults

- prefer a shared `httpx.Client` or `httpx.AsyncClient` over top-level helpers
  when making more than one request
- set explicit timeouts; do not rely on vague defaults
- use `base_url` for service clients so paths stay short and consistent
- keep one style per call path: sync code with `Client`, async code with
  `AsyncClient`
- call `raise_for_status()` when non-2xx responses should fail fast
- deserialize at the boundary into typed objects instead of spreading raw JSON
  dicts through the codebase
- keep retry logic outside business code; centralize it in one wrapper or
  adapter
- do not build URLs or query strings with unsafe string concatenation
- do not create a new client for every request inside hot paths

## Quick Start

```python
from collections.abc import AsyncIterator

import httpx


def build_client() -> httpx.Client:
    return httpx.Client(
        base_url="https://api.example.com",
        timeout=httpx.Timeout(10.0, connect=3.0),
        headers={"User-Agent": "myapp/1.0"},
        follow_redirects=True,
    )


async def build_async_client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(
        base_url="https://api.example.com",
        timeout=httpx.Timeout(10.0, connect=3.0),
    ) as client:
        yield client
```

## Timeout and Transport Rules

- use `httpx.Timeout(...)` when connect, read, or write behavior matters
- use connection limits for high-concurrency clients instead of unconstrained
  fan-out
- use custom transports only for testing, in-process apps, or a very specific
  integration need
- keep proxy, SSL, and certificate config explicit in one place

For deeper client setup patterns, load `references/clients.md`.

## Error Handling Rules

- catch `httpx.TimeoutException` for timeouts
- catch `httpx.HTTPStatusError` when the server responded but with a failing
  status
- catch `httpx.RequestError` for network and transport failures
- convert library exceptions into domain-relevant errors at the boundary if the
  rest of the application should not know about HTTPX
- log request context that helps debugging, but do not log secrets or full
  sensitive payloads

## Guardrails

- validate or normalize untrusted URLs before requesting them
- never forward user-supplied headers blindly to upstream services
- do not bury `raise_for_status()` inside low-level helpers if callers need to
  branch on specific status codes
- do not mix retry loops, parsing, and domain logic in the same function
- do not read large responses fully into memory when streaming is more
  appropriate
- do not patch `httpx.get` or `httpx.post` all over tests; inject clients or
  transports instead

## Review Focus

- check whether client lifetime is clear and reused where appropriate
- check whether timeouts and redirects are explicit enough for the use case
- check whether status handling is consistent and intentional
- check whether auth and headers are centralized instead of repeated
- check whether request construction is safe from URL or header injection
- check whether tests isolate network behavior with mock transports or injected
  clients
