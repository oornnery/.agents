# TODO

<!-- Now = the single highest-value task in flight. Limit to 1 to maintain focus and reduce context-switching overhead. -->

## Now

- [ ] Add sorting by due date and priority to task list endpoint
  - Compose with existing pagination and filtering.

<!-- Next = verified, ready-to-start work queued behind Now. These keep momentum when the current task completes. -->

## Next

- [ ] Write integration tests for auth flow (JWT login, refresh, logout)
  - Cover token expiry edge cases and concurrent refresh race.

## Blocked

- [ ] Implement rate limiting middleware for public endpoints
  - Blocker: infra team decision on Redis vs in-memory rate limiter (owner: @sarah-infra, ETA: 2025-06-16)

## Done

- [x] Scaffold FastAPI project structure with SQLModel and Alembic (2025-06-02)
  - Validation: `pytest` passes, `alembic revision --autogenerate` produces clean migrations.

- [x] Implement CRUD endpoints for tasks with input validation (2025-06-06)
  - Validation: load test with `locust` at 100 RPS shows zero 5xx responses.

- [x] Add OAuth2 password flow and JWT token generation (2025-06-10)
  - Validation: token payload verified with `jose` library; refresh token rotation tested.

- [x] Implement task pagination endpoint (2025-06-12)
  - Validation: cursor-based pagination tested against 10k task dataset; p95 < 50ms.

- [x] Add task filtering by status, priority, and assignee (2025-06-12)
  - Validation: index-backed filters composed with pagination; integration tests pass.
