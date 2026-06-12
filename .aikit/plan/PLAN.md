# Implementation Plan: Task Management API

## Overview

Build a REST API for managing tasks with CRUD operations, status transitions, and due date tracking. The API serves a single-page frontend and integrates with the existing FastAPI service layer.

<!-- WHY: Overview grounds every decision maker in the problem and boundaries before diving into files and phases. Without it, reviewers cannot judge whether later choices are proportionate. -->

## Requirements

- Functional:
  - Create, read, update, and delete tasks
  - Filter tasks by status, assignee, and due date
  - Validate state transitions (todo -> in_progress -> in_review -> done)
- Non-functional:
  - Response time under 200ms for list queries
  - JSON:API compliant error responses
- Security:
  - Owner-scoped access control on every endpoint
  - Input validation on all user-provided fields

<!-- WHY: Requirements are listed explicitly so the plan can be audited against the spec. If a phase does not map to a requirement, it should be cut. -->

## Structure Changes

- Add `src/tasks/` domain module
- Add `src/api/routes/tasks.py` for HTTP handlers
- Add `src/models/task.py` for SQLModel entity
- Add `src/schemas/task.py` for request/response DTOs
- Add `src/services/task_service.py` for business rules
- Add `tests/unit/services/test_task_service.py`
- Add `tests/integration/api/test_tasks.py`

<!-- WHY: Naming structure changes up front prevents mid-implementation debates about where files belong and keeps the repository layout predictable. -->

## Phases

### Phase 1: Domain Model and Database Migration

Add `src/models/task.py` with the SQLModel definition including `id`, `title`, `description`, `status`, `assignee_id`, `due_date`, and `created_at`. Generate Alembic migration `migrations/versions/20240612_add_tasks_table.py`. Verify with `alembic upgrade head` and a quick row insertion script.

### Phase 2: Service Layer with Business Rules

Implement `src/services/task_service.py` with `create_task`, `get_task`, `update_task`, `delete_task`, and `list_tasks`. Enforce status transition rules in `src/services/task_service.py` before persisting changes. Write `tests/unit/services/test_task_service.py` covering happy paths, invalid transitions, and due date validation.

### Phase 3: API Routes and Input Validation

Wire FastAPI routes in `src/api/routes/tasks.py` for `POST /tasks`, `GET /tasks`, `GET /tasks/{task_id}`, `PUT /tasks/{task_id}`, and `DELETE /tasks/{task_id}`. Use `src/schemas/task.py` Pydantic models for request bodies and query parameters. Return proper HTTP status codes and JSON:API error shapes.

### Phase 4: Authentication and Authorization

Add owner checks to `src/services/task_service.py` using the current user from `src/auth/dependencies.py`. Update `src/api/routes/tasks.py` to inject the current user and reject cross-tenant access with 403 responses. Update integration tests in `tests/integration/api/test_tasks.py` to include authenticated fixtures.

### Phase 5: Integration Testing and Performance Baseline

Run `tests/integration/api/test_tasks.py` against the full stack. Add `tests/load/locustfile.py` with a basic task-list query scenario. Verify p95 latency under 200ms on a local database with seeded data.

## File Paths Summary

| File | Purpose |
|---|---|
| `src/models/task.py` | SQLModel entity and table definition |
| `src/schemas/task.py` | Pydantic request/response DTOs |
| `src/services/task_service.py` | Business logic and state transition rules |
| `src/api/routes/tasks.py` | FastAPI HTTP route handlers |
| `src/api/dependencies.py` | Shared route dependencies (pagination, current user) |
| `tests/unit/services/test_task_service.py` | Service layer unit tests |
| `tests/integration/api/test_tasks.py` | Full-stack API integration tests |
| `tests/load/locustfile.py` | Performance baseline scenario |
| `migrations/versions/20240612_add_tasks_table.py` | Alembic migration |

<!-- WHY: A file path summary acts as a checklist during review and prevents orphaned work. Reviewers can confirm every new file has a clear owner and that no path duplicates existing conventions. -->

## Dependencies

- `fastapi` >= 0.111
- `sqlmodel` >= 0.0.19
- `alembic` >= 1.13
- `pytest` >= 8.0
- `httpx` >= 0.27 (for integration test client)
- `locust` >= 2.28 (for load testing)

<!-- WHY: Dependencies are listed with minimum versions so the team can assess supply-chain risk and ensure the CI environment matches before merging any phase. -->

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Status transition rules become inconsistent | Centralize all logic in `src/services/task_service.py`; never check status in routes |
| List queries slow with large datasets | Add composite index on `(assignee_id, status)` in migration; measure before and after |
| Auth scope leaks between tenants | Add integration tests for 403 cases; never default to unscoped queries |

## Testing Strategy

- Unit tests: `tests/unit/services/test_task_service.py` using an in-memory SQLite database and direct service calls
- Integration tests: `tests/integration/api/test_tasks.py` spinning up the full FastAPI app with TestClient
- Load tests: `tests/load/locustfile.py` running a 60-second baseline before release
- Security tests: Add adversarial cases for missing auth, malformed UUIDs, and oversized payloads in `tests/integration/api/test_tasks.py`

<!-- WHY: Testing strategy is defined before coding so that reviewers can reject any phase that lacks a verifiable exit criteria. -->

## Success Criteria

- [ ] `src/models/task.py` migration applies cleanly to an empty database
- [ ] `tests/unit/services/test_task_service.py` passes with 100% branch coverage on state transitions
- [ ] `tests/integration/api/test_tasks.py` passes for all CRUD endpoints including 403 cases
- [ ] `tests/load/locustfile.py` shows p95 list latency under 200ms
- [ ] No `UNKNOWN` placeholders or `YYYY-MM-DD` dates remain in the codebase

<!-- WHY: Success criteria turn the plan into a contract. If every box is checked, the feature is done; if not, the remaining work is explicit. -->
