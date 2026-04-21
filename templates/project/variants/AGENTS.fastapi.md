# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!--
FastAPI service overlay.
Use for Python HTTP services where request handling, schema design, and runtime
behavior need project-specific instructions on top of the base variant.
-->

## Project Description

<!-- Brief description of the API, its clients, and its critical trust boundaries -->

## Stack

- **Framework**: FastAPI
- **Validation**: Pydantic
- **HTTP Client**: HTTPX
- **Preferred Persistence**: SQLModel
<!-- - **Persistence**: SQLModel / SQLAlchemy -->
<!-- - **Auth**: JWT / session cookies / API keys -->

## Quick Commands

```bash
uv sync
uv run fastapi dev src/myapp/main.py   # Start API server
uv run task check                      # Run full validation
uv run pytest tests/integration -v     # Focused API integration tests
```

## Validation Entry Points

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check src
uv run pytest -v
```

## API Conventions

- use `Annotated` for `Path`, `Query`, `Header`, and `Depends`
- keep routes thin and move orchestration into `services/` or `core/`
- use explicit return types or `response_model` for public handlers
- prefer `def` over `async def` when the implementation blocks
- keep request validation, auth, and permission checks explicit at the edge
- do not leak ORM or persistence shapes directly through API responses

## Preferred Libraries

- use `Pydantic` for request, response, and config models
- use `HTTPX` for outbound HTTP calls
- use `SQLModel` when the service uses typed SQLAlchemy-style persistence and
  benefits from aligned models and metadata

## Request, Response, and Dependency Rules

- keep request parsing and response shaping explicit
- centralize shared dependencies only when they improve repeated signatures
- use response models or explicit return types for public handlers
- separate transport concerns from reusable logic

## Runtime and Safety Defaults

- prefer `def` when the internals block
- avoid hidden network or database work in dependencies unless obvious from the code
- treat uploads, downloads, callbacks, and webhooks as high-risk boundaries
- keep auth, session, and permission behavior explicit in routes and dependencies

## Layout

```text
src/myapp/
├── api/
│   ├── app.py          # app factory, middleware, startup wiring
│   ├── deps.py         # shared dependency helpers
│   └── routes/         # route modules grouped by feature
├── schemas/            # request and response shapes
├── core/               # reusable business rules and policies
├── services/           # orchestration and integration flows
├── database/           # engine, sessions, queries, migrations
└── models/             # persisted data models
```

## Error and Contract Rules

- use consistent status codes and response shapes
- keep validation errors, auth failures, and business conflicts distinguishable
- document pagination, filtering, and sorting rules when relevant
- treat file uploads, webhooks, and external callbacks as high-risk surfaces

## FastAPI Checklist

### API Surface

- [ ] route names and resource paths are explicit
- [ ] request and response schemas are explicit
- [ ] status codes are intentional
- [ ] error shapes are consistent

### Handler Design

- [ ] routes stay thin
- [ ] shared dependencies are reusable and visible
- [ ] blocking work does not run inside async handlers
- [ ] auth and permission checks happen at the edge

### Data Boundaries

- [ ] ORM or database models do not leak into public responses
- [ ] pagination and filtering are explicit when needed
- [ ] uploads, downloads, and callbacks are treated as high-risk inputs

### Verification

- [ ] success and failure paths are tested
- [ ] auth and permission boundaries are tested
- [ ] invalid input and edge values are tested
- [ ] startup, shutdown, and integration behavior are tested

## Testing Focus

<!-- - response shapes -->
<!-- - auth and permission boundaries -->
<!-- - invalid input and edge values -->
<!-- - startup/shutdown behavior -->
<!-- - integration with database and upstream services -->

## Environment Variables

<!-- | Variable | Description | Required | -->
<!-- |----------|-------------|----------| -->

## Project-Specific Guardrails

<!-- - Keep router prefixes stable -->
<!-- - Centralize auth dependencies -->
<!-- - Never perform blocking network calls inside async handlers -->
