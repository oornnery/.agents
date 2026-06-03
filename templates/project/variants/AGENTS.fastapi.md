# Project Name

@.agents/templates/project/variants/AGENTS.python.md

<!-- Python web/API overlay. Keep detailed web guidance in skills/python-web. -->

## Project Description

<!-- API/web app purpose, primary clients, critical trust boundaries -->

## Stack Defaults

- **Framework**: FastAPI
- **Validation**: Pydantic
- **HTTP Client**: HTTPX
- **Persistence**: SQLModel / SQLAlchemy when persistence is needed
- **Templates**: Jinja2 when server-rendered HTML is needed
- **Partial UI**: HTMX when HTML-over-the-wire simplifies flows
- **Tiny Client State**: Alpine.js only for local progressive behavior

Do not turn Python web projects into React/TS-first apps unless explicitly requested.

## Quick Commands

```bash
uv sync
uv run fastapi dev src/myapp/main.py
uv run task check
uv run pytest -v
```

## Validation Entry Points

Use configured commands only:

```bash
uv run task check
uv run ruff format --check .
uv run ruff check .
uv run ty check src
uv run pytest -v
uv run task sec
```

For persisted apps, verify migrations or schema setup with the repo's configured command.

## Skill Routing

- Load `skills/python-web/SKILL.md` for FastAPI, BFF, SSR, Jinja2, HTMX, SQLModel, route maps, product scopes, or web verification.
- Load `skills/security/SKILL.md` for auth, permissions, webhooks, uploads, callbacks, CORS, CSRF, tenant boundaries, or sensitive data.
- Load `skills/verification/SKILL.md` before final validation or security-sensitive checks.
- Load `skills/project-state/SKILL.md` when scope, decisions, memory, validation, or next steps changed.

## Always-On Web Rules

- Identify clients and trust boundaries before shaping routes or UI.
- Keep routes thin: parse, authorize, call service, shape response.
- Keep request, response, persistence, and domain models separate when their shapes differ.
- Never trust client-provided user id, role, tenant id, price, status, or ownership fields.
- Make status codes, pagination, filtering, sorting, and error shapes intentional.
- Templates receive explicit context; no hidden DB/business logic in templates.

## Project-Specific Guardrails

<!-- - Keep router prefixes stable -->
<!-- - Centralize auth dependencies -->
<!-- - Never perform blocking network calls inside async handlers -->
