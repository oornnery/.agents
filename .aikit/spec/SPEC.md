# SPEC

## Objective

<!-- A clear objective anchors every decision. Without it, scope creeps and priorities blur. -->

Build a RESTful Task Management API that lets users create, organize, and track personal and team tasks. The API supports projects, labels, due dates, priorities, and recurring task patterns. It is designed as a backend service consumed by web and mobile clients.

## Scope

- In scope:
  - CRUD operations for tasks, projects, and labels
  - Filtering and sorting tasks by status, priority, due date, and assignee
  - Recurring task rules (daily, weekly, monthly)
  - Task comments and activity history
  - Soft deletes and archive behavior
  - RESTful JSON API with OpenAPI documentation
- Out of scope:
  - Real-time collaboration or WebSocket features
  - File attachments and media storage
  - Email notifications and push alerts
  - Third-party calendar integrations
  - Frontend web or mobile applications

## Users and Actors

<!-- Naming actors early prevents ambiguous permission stories later. -->

- Primary user: Individual users managing personal task lists
- Secondary actors: Team leads who assign and review team tasks
- External systems: OAuth2 identity provider for authentication, SQL database for persistence

## Requirements

- Functional:
  - Users can create tasks with title, description, due date, priority, and assignee
  - Users can organize tasks into projects and tag them with labels
  - Users can filter tasks by multiple criteria in a single query
  - Recurring tasks automatically spawn new task instances based on defined rules
  - Soft-deleted tasks remain recoverable for 30 days before permanent removal
- Non-functional:
  - API response times under 200ms for 95th percentile read operations
  - Support for 1,000 concurrent users on standard deployment hardware
  - API versioning via URL path to allow gradual client migrations
- Security:
  - All endpoints require authenticated access via JWT bearer tokens
  - Users can only read and mutate tasks within their own scope or assigned team projects
  - Input validation prevents SQL injection and XSS through parameterized queries and output encoding
  - Rate limiting applied per user to prevent brute-force and abuse
- Accessibility:
  - API responses include consistent, human-readable error messages
  - Date and time fields use ISO 8601 format to support global clients
- Performance:
  - Database queries use indexed columns for common filters
  - Pagination enforced on list endpoints with a maximum page size of 100

## Success Criteria

- [ ] All endpoints return correct HTTP status codes and structured JSON responses
- [ ] Filtering and sorting produce deterministic, paginated results
- [ ] Recurring tasks generate child tasks according to schedule rules
- [ ] `uv run pytest` passes with 90% or higher code coverage
- [ ] `ruff check . --fix` reports zero lint errors
- [ ] `ty check src && pyright` passes with no type errors
- [ ] `bandit -r src` reports no high-severity security issues

## Interfaces

- UI: No frontend included; API is consumed by external clients
- API: RESTful JSON over HTTPS. Resources: `/tasks`, `/projects`, `/labels`, `/comments`
- CLI: Admin CLI for database migrations and user management (`uv run cli/manage.py`)
- Data: PostgreSQL for relational data. Migrations managed with Alembic.

## Constraints

- Technical:
  - Python 3.12+ with FastAPI and SQLModel
  - Deployed as a containerized service behind an HTTPS reverse proxy
- Product:
  - No real-time features in the initial release
  - Soft deletes required for user trust and recovery
- Operational:
  - Logs must be structured JSON for aggregation
  - Secrets managed through environment variables, never committed to version control

## Validation Plan

<!-- A validation plan turns subjective quality into repeatable, automated checks. -->

- Format: `uv run ruff format .` before every commit
- Lint: `uv run ruff check . --fix` to enforce style and catch common bugs
- Type/LSP: `uv run ty check src && uv run pyright` for static type correctness
- Tests: `uv run pytest -v` for unit, integration, and edge-case coverage
- Build: `uv run docker build -t task-api .` for container integrity
- Security: `uv run bandit -r src` and dependency audit with `uv run pip-audit`

## Open Questions

- Whether to add full-text search on task descriptions in the first release
- How to handle daylight-saving transitions for recurring task schedules
- Whether team project permissions need role-based access control beyond simple ownership
