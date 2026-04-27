# Implementation

Use when writing Python/FastAPI/Jinja2 code.

## Bootstrap

Prefer existing scripts/conventions. If starting fresh:

```bash
uv init --app
uv add fastapi uvicorn jinja2 python-multipart sqlmodel alembic pydantic-settings itsdangerous
uv add --dev ruff ty pytest pytest-asyncio httpx
```

HTMX/Alpine can load by script tag. Tailwind CDN is acceptable for quick MVP/dev if documented; otherwise use a minimal local Tailwind build when the project accepts Node tooling.

## `pyproject.toml` Baseline

```toml
[project]
name = "python-web-app"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
```

## App Bootstrap

```py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.features.public.routes import router as public_router


def create_app() -> FastAPI:
    app = FastAPI(title="Python Web App")
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    app.include_router(public_router)
    return app


app = create_app()
```

## Template Helper

```py
from fastapi import Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="app/templates")


def render(request: Request, template_name: str, context: dict | None = None):
    return templates.TemplateResponse(
        request=request,
        name=template_name,
        context=context or {},
    )
```

## Vertical Slice

1. Pydantic/SQLModel schema
2. SQLModel table when persistence exists
3. Alembic migration
4. service function
5. FastAPI GET route
6. FastAPI POST route
7. Jinja2 page/partial
8. validation, empty/error/success states
9. pytest
10. docs update

## Feature Shape

```txt
features/<domain>/
  __init__.py
  routes.py
  models.py
  schemas.py
  service.py
  tests/test_<domain>.py
```

Use only when useful; tiny features can stay smaller.

## Jinja2

Use `layouts/base.html` for public pages, `layouts/admin.html` for private pages, `partials/` for HTMX responses/fragments, `components/` for visual patterns. Keep Python logic out of templates; pass simple explicit context objects.

## Forms/Admin

Pydantic/SQLModel schema is source of truth; server validation mandatory. Show field errors, preserve input, include success/failure states. Use semantic HTML tables + Tailwind first; filters via GET params, pagination/status badges when needed. Avoid heavy JS tables unless scoped.

## FastAPI

Small route functions, dependency injection for DB/auth, explicit form/body/query validation, services for rules, redirects after successful POST when appropriate, background tasks only for non-critical notifications/webhooks.

## SQLModel/Alembic

Explicit small models, separate table models from request/form schemas when helpful, enums for statuses, consistent datetimes. Commit migrations; review autogenerate; test upgrade.

```bash
uv run alembic revision --autogenerate -m "create appointments"
uv run alembic upgrade head
```

## Tests

pytest for route smoke, form validation, service rules, DB CRUD for core entities, webhook payloads. Use `httpx.AsyncClient` or FastAPI test client depending on app style. Do not over-test static marketing sections.
