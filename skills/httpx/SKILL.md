---
name: httpx
description: HTTPX client patterns for Python services, scripts, and
  applications. Covers client lifetime, sync and async usage, timeouts,
  streaming, auth, retries, error handling, and testing with mock transports.
  Load when working with outbound HTTP in Python.
---

# HTTPX

Use when work is primarily outbound HTTP in Python.

## Boundary

Use this skill for:

- sync and async HTTP clients
- shared client config
- timeouts, limits, redirects, and connection reuse
- uploads, downloads, and streaming
- auth headers and custom auth flows
- testing HTTP integrations without real network calls

Pair with:

- `python` for general Python conventions and project workflow
- `security` when requests touch auth, secrets, SSRF risk, or untrusted URLs
- `quality` when flaky integrations or retry behavior need tighter guards

## Reference Map

- `references/clients.md` -- client lifetime, shared config, auth, limits, transports, and async boundaries
- `references/requests-and-streaming.md` -- request shapes, file transfer, pagination, and streaming patterns
- `references/testing.md` -- `MockTransport`, dependency injection, fake responses, and integration test boundaries

## Assets

- `assets/client.py` -- typed `crudcrud.com` client example with shared config and explicit CRUD methods
- `assets/testing.py` -- test of same `crudcrud.com` adapter using `MockTransport` over real network calls

## What Stays Here

Keep this file focused on defaults and guardrails.

- keep here: client lifetime rules, timeout defaults, error handling stance, review cues
- move to refs: long examples, auth variants, streaming details, transports, testing patterns
- use assets when runnable example clearer than another code block

## Core Defaults

- prefer shared `httpx.Client` or `httpx.AsyncClient` over top-level helpers when making more than one request
- set explicit timeouts; do not rely on vague defaults
- use `base_url` for service clients -- paths stay short, consistent
- one style per call path: sync code with `Client`, async code with `AsyncClient`
- call `raise_for_status()` when non-2xx should fail fast
- deserialize at boundary into typed objects, not raw JSON dicts spread through codebase
- keep retry logic outside business code; centralize in one wrapper or adapter
- do not build URLs or query strings with unsafe string concatenation
- do not create new client per request in hot paths

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
- use connection limits for high-concurrency clients, not unconstrained fan-out
- custom transports only for testing, in-process apps, or specific integration need
- keep proxy, SSL, and certificate config explicit in one place

For deeper client setup patterns, load `references/clients.md`.

## Error Handling Rules

- catch `httpx.TimeoutException` for timeouts
- catch `httpx.HTTPStatusError` when server responded with failing status
- catch `httpx.RequestError` for network and transport failures
- convert library exceptions into domain-relevant errors at boundary if rest of app should not know about HTTPX
- log request context helpful for debugging; do not log secrets or full sensitive payloads

## Guardrails

- validate or normalize untrusted URLs before requesting
- never forward user-supplied headers blindly to upstream
- do not bury `raise_for_status()` inside low-level helpers if callers need to branch on specific status codes
- do not mix retry loops, parsing, and domain logic in same function
- do not read large responses fully into memory when streaming more appropriate
- do not patch `httpx.get` or `httpx.post` all over tests; inject clients or transports instead

## Review Focus

- check client lifetime clear and reused where appropriate
- check timeouts and redirects explicit enough for use case
- check status handling consistent and intentional
- check auth and headers centralized, not repeated
- check request construction safe from URL or header injection
- check tests isolate network behavior with mock transports or injected clients
