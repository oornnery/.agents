# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!--
FastAPI service overlay.
Python HTTP services — request handling, schema design, runtime behavior on top of base variant.
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

- `Annotated` for `Path`, `Query`, `Header`, `Depends`
- routes thin, orchestration in `services/` or `core/`
- explicit return types or `response_model` for public handlers
- prefer `def` over `async def` when blocking
- request validation, auth, permission checks explicit at edge
- no ORM/persistence shapes in API responses

## Preferred Libraries

- `Pydantic` for request, response, config models
- `HTTPX` for outbound HTTP
- `SQLModel` for typed SQLAlchemy-style persistence w/ aligned models + metadata

## Request, Response, and Dependency Rules

- request parsing + response shaping explicit
- centralize shared deps only if they improve repeated signatures
- response models or explicit return types for public handlers
- separate transport from reusable logic

## Runtime and Safety Defaults

- prefer `def` when internals block
- no hidden network/DB work in deps unless obvious
- uploads, downloads, callbacks, webhooks = high-risk
- auth, session, permission explicit in routes + deps

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

- consistent status codes + response shapes
- validation errors, auth failures, business conflicts distinguishable
- document pagination, filtering, sorting when relevant
- file uploads, webhooks, external callbacks = high-risk

## FastAPI Checklist

### API Surface

- [ ] route names + resource paths explicit
- [ ] request + response schemas explicit
- [ ] status codes intentional
- [ ] error shapes consistent

### Handler Design

- [ ] routes thin
- [ ] shared deps reusable + visible
- [ ] no blocking work in async handlers
- [ ] auth + permission checks at edge

### Data Boundaries

- [ ] no ORM/DB model leak in public responses
- [ ] pagination + filtering explicit when needed
- [ ] uploads, downloads, callbacks = high-risk

### Verification

- [ ] success + failure paths tested
- [ ] auth + permission boundaries tested
- [ ] invalid input + edge values tested
- [ ] startup, shutdown, integration tested

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