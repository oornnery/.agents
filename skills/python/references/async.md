# Async Python Patterns

Use async only when concurrent I/O pressure is real. Keep call path async end-to-end.

## Use When

- many concurrent HTTP/db/socket/file-ish waits
- streaming async APIs
- background tasks with non-blocking I/O
- WebSockets or long-lived connections
- rate-limited external calls needing concurrency control

Prefer sync when work is CPU-bound, simple CLI/script logic, or a single request path.

## Decision Guide

| Workload            | Use                                      |
| ------------------- | ---------------------------------------- |
| CPU-bound           | sync + multiprocessing/native/vectorized |
| one/few I/O calls   | sync                                     |
| many I/O calls      | async + bounded concurrency              |
| blocking library    | sync wrapper or thread pool              |
| async framework app | async all the way down                   |

## Core Concepts

- coroutine: async function object that must be awaited
- task: scheduled coroutine
- event loop: runs tasks cooperatively
- cancellation: normal control path, must be handled
- timeout: boundary around external waits
- async context manager/iterator: resource + stream lifecycle

## Essentials

```python
import asyncio

async def fetch_one(client, url):
    return await client.get(url)

async def fetch_all(client, urls):
    return await asyncio.gather(*(fetch_one(client, u) for u in urls))

asyncio.run(fetch_all(client, urls))
```

## Concurrency Rules

- Bound concurrency with `asyncio.Semaphore`.
- Use `asyncio.TaskGroup` on Python 3.11+ for structured concurrency.
- Use `asyncio.gather` for simple fan-out where shared failure behavior is OK.
- Keep task references or use task groups; do not spawn-and-forget silently.
- Always close async clients/resources.

## Timeouts and Cancellation

```python
async with asyncio.timeout(10):
    result = await call()
```

Rules:

- set timeouts at external boundaries
- let `CancelledError` propagate after cleanup
- make cleanup idempotent
- avoid swallowing cancellation in broad `except Exception`

## Resource Management

- use async clients as context managers
- pool connections for HTTP/db
- do not create new client per request
- close streams explicitly
- use async generators for streaming large results

## Producer/Consumer

Use `asyncio.Queue` when producers and consumers run at different rates. Bound queue size for backpressure. Send sentinel or cancel task group for shutdown.

## Locks and Shared State

- prefer no shared mutable state
- use `asyncio.Lock` only around small critical sections
- avoid holding lock while awaiting slow external I/O
- protect caches/session state consistently

## Blocking Work

Never call blocking I/O or CPU-heavy functions directly on event loop. Options:

- use async-native library
- `asyncio.to_thread()` for blocking I/O
- process pool for CPU-bound work

## Testing

- use project async test plugin/convention
- await every async call
- test timeout/cancellation paths
- avoid real sleeps; use events/fakes
- close clients/resources in fixtures

## Pitfalls

| Pitfall                      | Fix                                    |
| ---------------------------- | -------------------------------------- |
| forgot `await`               | await coroutine or schedule task       |
| event loop blocked           | async-native lib or `to_thread`        |
| unbounded `gather`           | semaphore/task pool                    |
| swallowed cancellation       | cleanup then re-raise                  |
| sync/async mixed mid-stack   | make boundary explicit                 |
| client per request           | reuse pooled client                    |
| fire-and-forget background   | task group, tracking, shutdown cleanup |

## Review Checklist

- [ ] async justified by I/O concurrency
- [ ] no blocking calls on event loop
- [ ] concurrency bounded
- [ ] timeouts at external waits
- [ ] cancellation handled safely
- [ ] resources closed
- [ ] tests cover error/timeout path
