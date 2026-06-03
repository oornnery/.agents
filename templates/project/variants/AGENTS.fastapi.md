# Project Name

@.agents/templates/project/variants/AGENTS.python.md

<!--
Python web/API overlay.
Use for FastAPI APIs, BFFs, server-rendered Python web apps, dashboards,
admin systems, booking/order/catalog apps, and webhook/callback services.
-->

## Project Description

<!-- Brief description of API/web app, primary clients, and critical trust boundaries -->

## Stack Defaults

- **Framework**: FastAPI
- **Validation**: Pydantic
- **HTTP Client**: HTTPX
- **Persistence**: SQLModel / SQLAlchemy when persistence is needed
- **Templates**: Jinja2 when server-rendered HTML is needed
- **Partial UI**: HTMX when HTML-over-the-wire simplifies flows
- **Tiny Client State**: Alpine.js only for local progressive behavior
<!-- - **Auth**: session cookies / JWT / API keys -->
<!-- - **Migrations**: Alembic -->

Do not turn Python web projects into React/TS-first apps unless explicitly requested.

## Quick Commands

```bash
uv sync
uv run fastapi dev src/myapp/main.py
uv run task check
uv run pytest -v
uv run pytest tests/integration -v
```

## Validation Entry Points

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check src
uv run pytest -v
```

For persisted apps, also verify migrations or schema setup with the repo's configured command.

## Web Discovery

- Find app factory/main module, routers, dependencies, middleware, settings, DB session, migrations, templates, and tests
- Identify clients: browser, mobile app, internal service, webhook sender, admin user, public visitor
- Identify trust boundaries: auth, permissions, uploads, callbacks, webhooks, payments, external APIs, admin actions
- Check whether the app is API-only, SSR-first, HTMX-enhanced, or mixed before adding UI/API shape

## Layout Defaults

```text
src/myapp/
├── api/
│   ├── app.py
│   ├── deps.py
│   └── routes/
├── schemas/
├── core/
├── services/
├── database/
├── models/
├── templates/
└── static/
```

Match the repo's actual layout over this example.

## API Rules

- Use `Annotated` for `Path`, `Query`, `Header`, `Cookie`, and `Depends`
- Keep routes thin: parse, authorize, call service, shape response
- Keep business rules in `core/` or `services/`, not route bodies
- Use explicit response models or explicit return types for public handlers
- Keep request, response, persistence, and domain models separate when their shapes differ
- Do not leak ORM/session objects into response models, templates, or browser contracts
- Status codes, pagination, filtering, sorting, and error shapes must be intentional

## Dependency and Runtime Rules

- Prefer `def` handlers when internals block; use `async def` only when the path is async end-to-end
- Do not perform hidden network, DB, or expensive work inside dependencies unless the dependency name makes it obvious
- Startup/shutdown behavior, connection lifetimes, and background tasks must be explicit
- Centralize outbound HTTP clients, timeouts, retry policy, and base URLs
- Do not block the event loop with sync file, DB, network, or CPU work inside async handlers

## Auth and Safety Rules

- Authn, authz, tenant/user scoping, and permission checks happen at the edge and in tested services
- Unsafe methods, admin actions, uploads, downloads, callbacks, and webhooks are high-risk by default
- Validate webhook signatures, callback source, idempotency keys, replay windows, and payload size when applicable
- CSRF rules must be explicit for cookie-authenticated browser forms and HTMX requests
- Never trust client-provided user id, role, tenant id, price, status, or ownership fields

## Server-Rendered UI Rules

- Templates receive explicit context; no hidden DB/business logic inside templates
- Full-page routes, fragment routes, redirects, empty states, error states, and success states must be distinct
- HTMX responses return intentional fragments, not ad hoc strings
- Use HTMX headers, targets, swaps, and redirects deliberately
- Alpine state stays local and progressive; canonical data and permission decisions stay server-side
- Forms must show validation failures clearly and preserve safe user input

## Testing Rules

- Test success, invalid input, auth failure, permission failure, and business conflict paths
- Test response shapes and status codes for public API endpoints
- Test startup/shutdown or DB wiring when touched
- Test webhooks/callbacks with invalid signature, replay/duplicate delivery, malformed payload, and happy path
- Test rendered page and fragment behavior when templates or HTMX paths change

## Review Focus

- route doing business logic instead of orchestration
- missing auth, authz, tenant scoping, or CSRF handling
- blocking work inside async handler
- ORM model leaked into public response or template context
- inconsistent status codes or error shapes
- unbounded upload/download/body/query behavior
- webhook without signature, idempotency, or replay handling
- templates compensating for backend contract drift

## Project-Specific Guardrails

<!-- - Keep router prefixes stable -->
<!-- - Centralize auth dependencies -->
<!-- - Never perform blocking network calls inside async handlers -->
