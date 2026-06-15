# DESIGN

<!-- Product Context grounds every technical choice in actual user need; without it, engineers optimize for the wrong problems and ship features no one asked for. -->

## Product Context

Who uses this project, what they are trying to do, and what must feel true in the final experience.

Small product and engineering squads use this Task Management API to coordinate daily work. Team members create tasks, assign owners, track status through a workflow, and close items when complete. Managers need visibility into workload and bottlenecks without interrupting individual contributors. The experience must feel reliable: status is always accurate, assignments are clear, and nothing silently disappears or changes without an audit trail.

<!-- Architecture documents boundaries so teams do not accidentally couple HTTP handlers to storage or leak side effects into reusable logic. -->

## Architecture

- Core boundaries:
  - FastAPI routes handle HTTP concerns only; they validate input and serialize output.
  - Business logic lives in service modules that are independent of HTTP and database details.
  - SQLModel repositories own persistence queries. Routes never call the database directly.
- Data flow:
  - Client → FastAPI router → Pydantic request model → service layer → SQLModel repository → PostgreSQL.
  - Responses travel back through the same layers with explicit Pydantic output models.
  - No raw dictionaries pass between layers; all boundaries use explicit types.
- External integrations:
  - JWT issuer for auth tokens; tokens are signed and verified on every request.
  - PostgreSQL for persistence. No external message queue or cache at current scope.
  - Future email notifications may use an external SMTP provider.
- Runtime assumptions:
  - Python 3.12+, uv-managed dependencies, containerized via Docker on port 8000.
  - Stateless horizontal scaling is possible because all state lives in PostgreSQL.

<!-- UI and Interaction matter even for APIs because client developers are the users; predictable URLs, clear states, and consistent responses reduce integration friction and bugs. -->

## UI and Interaction

- Surfaces:
  - This is a backend API; primary surfaces are HTTP clients, CLI tools, and future web frontends consuming JSON.
- Navigation:
  - REST resource-oriented URLs: `/tasks`, `/tasks/{id}`, `/tasks/{id}/comments`.
  - Predictable paths reduce client integration time and make caching straightforward.
- States:
  - A task moves through `todo`, `in_progress`, `in_review`, `done`.
  - Only the assignee or an admin may transition status.
- Accessibility:
  - API returns consistent JSON shapes and readable, structured error messages so client developers can build accessible frontends.
- Responsive behavior:
  - Pagination on list endpoints with a default of 20 items per page (cursor-based for real-time task feeds, offset for simple admin endpoints — see `.mem/decisions.md`).
  - `429` rate-limit headers returned under overload.

<!-- API and Data Contracts are the binding agreement between backend and clients; changing them breaks integrations, so explicit documentation prevents accidental drift. -->

## API and Data Contracts

- Inputs:
  - `POST /tasks` accepts `{ title: str, description: str, assignee_id: int, priority: low|medium|high }`
  - `GET /tasks` accepts query params `status`, `assignee_id`, `page`, `limit`
  - `PUT /tasks/:id` accepts partial updates to any writable task field
  - `DELETE /tasks/:id` accepts no body; returns `204` on success and is idempotent on missing resources
- Outputs:
  - All single-resource endpoints return `{ id: int, title: str, description: str, status: str, assignee_id: int, priority: str, created_at: datetime, updated_at: datetime }`.
  - List endpoints wrap items in `{ items: [], total: int, page: int, per_page: int }`.
- Errors:
  - `400` for validation failures with per-field detail.
  - `404` when a task ID does not exist.
  - `403` when the caller lacks permission to mutate.
  - `500` errors are logged internally with trace IDs but return a generic message to the client.
- Auth and permissions:
  - Bearer JWT required on all endpoints.
  - Token payload contains `sub` (user id) and `role`.
  - Only admins or the assigned user may update or delete a task.

<!-- Design Decisions capture context that code cannot express; they prevent recurring debates and help future maintainers understand why constraints exist. -->

## Design Decisions

| Date | Decision | Reason | Impact |
| ---- | -------- | ------ | ------ |
| 2025-03-15 | PostgreSQL over SQLite | Concurrent writers, team size exceeds SQLite comfort zone | Requires managed DB or container in local dev |
| 2025-03-18 | Use JWT for auth | Stateless, horizontally scalable, industry standard | No session store needed; tokens expire client-side |
| 2025-03-18 | SQLModel over raw SQL | Type safety, Pydantic integration, reduces boilerplate | Slight ORM learning curve for new contributors |
| 2025-03-19 | REST over GraphQL | Team familiarity, simpler HTTP caching, fewer moving parts | Slightly more round-trips for nested data acceptable |

<!-- Risks surface assumptions early so the team can monitor or mitigate instead of being surprised in production. -->

## Risks

- Technical:
  - Rapid growth could make PostgreSQL a bottleneck before read replicas are introduced.
  - Rate limiting must be added before public exposure.
  - Background job needs may outgrow the current synchronous design.
- Product:
  - Without due dates, notifications, or file attachments, the API is essentially a shared list.
  - Users may abandon it for richer project management tools if the feature set stalls.
- Security:
  - JWT secret rotation is currently manual.
  - Missing input size limits on title and description fields could allow abuse or excessive storage.
  - File attachments are out of scope but often requested later and expand the attack surface significantly.

## References

- SPEC.md
- TODO.md
- .spec/state.md
