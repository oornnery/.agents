---
name: python-web
description: Plan, sell, design, and implement Python/HTML-first web apps with FastAPI, Jinja2, Tailwind, HTMX/Alpine when useful, Pydantic, SQLModel, Alembic, SQLite/Postgres, pytest, ruff, ty, and uv.
---

# Python Web

Use for Python/SSR-first websites, landings, booking/order/catalog/admin systems, dashboards, BFFs, and small productized business apps. Local-business projects are a primary use case, not the skill name/boundary.

Prefer server-rendered HTML with FastAPI + Jinja2. Use HTMX for partial forms/updates and Alpine.js for tiny client-side state only when they simplify UX. Do not turn this into a React/TS-first app unless explicitly requested.

## Triggers

- build/plan a Python FastAPI/Jinja2 site/app
- create a landing, small catalog/commerce, booking, ordering, dashboard, CRM/leads, cash-flow, or admin system
- scope a sellable web package from public/user-provided business data
- design FastAPI routes, Jinja templates, forms, SQLModel/Alembic persistence, auth/admin boundaries
- implement with uv, Tailwind, pytest, ruff, ty

## Boundary

Covers:

- public-data discovery, brief, scope, project state, route map, template map, data model, form contracts
- FastAPI, Jinja2, Tailwind, HTMX/Alpine optional, Pydantic, SQLModel, Alembic
- SQLite local, PostgreSQL/Supabase/managed Postgres production
- responsive UI, accessibility, tests, deployment readiness

Excludes:

- frontend-heavy React/Next.js/SPAs by default
- fake reviews, spam, ToS bypass, private scraping
- sensitive medical records or unnecessary personal data
- enterprise architecture unless explicitly required

## Stack

Default unless repo already has compatible Python conventions:

- Python 3.12+, uv
- FastAPI, Uvicorn, Jinja2
- Tailwind CSS; HTMX optional for partial updates/forms; Alpine.js optional for tiny state
- Pydantic validation; SQLModel ORM/models; Alembic migrations
- SQLite local; PostgreSQL/Supabase/Neon/Railway Postgres in production when needed
- Session-based admin auth by default; external auth only when required
- pytest, ruff format/check, ty check

Avoid Celery, Redis, React, GraphQL, or complex frontend build systems unless the requirement truly demands it.

## Product Profiles

Pick one primary profile; list secondary modules separately.

| Profile              | Use when                     | Core scope                                      |
| -------------------- | ---------------------------- | ----------------------------------------------- |
| `static-site`        | presence/content             | pages, SEO, CTA, contact, map/social            |
| `conversion-landing` | one offer/campaign           | offer, proof, FAQ, lead form, WhatsApp/events   |
| `booking-system`     | appointments                 | services, availability, booking, admin status   |
| `ordering-system`    | food/service orders          | menu, cart, customer info, WhatsApp/admin hand  |
| `catalog-commerce`   | products/light commerce      | catalog, search, cart intent, admin catalog     |
| `admin-dashboard`    | internal ops/cash-flow/leads | CRUD, summaries, filters, export, permissions   |
| `custom-ops`         | specific workflow            | domain model + one vertical slice               |

## Reference Map

- Research/business facts/sales positioning: `references/discovery.md`
- Package/module selection: `references/product-catalog.md`
- Routes, templates, DB, migrations, auth, deployment: `references/architecture.md`
- Coding workflow/patterns: `references/implementation.md`
- Final verification: `references/checklists.md`

## Workflow

1. Inspect repo: uv/pyproject, scripts, FastAPI app, routes, templates, DB, migrations, tests. Reuse conventions.
2. Build `Business Brief` if business context matters: confirmed facts, user facts, assumptions, unknowns, goals.
3. Choose profile/package; define MVP, phase 2, out of scope.
4. Produce/update project state before nontrivial code:
   - `SPEC.md`
   - `DESIGN.md`
   - `TODO.md`
   - `.spec/state.md`
   - `.spec/handoff.md`
   - `.mem/open-loops.md`
5. Define route map, template map, flows, entities/tables, form contracts, auth/deployment assumptions, acceptance criteria.
6. Implement one vertical slice first: schema/model -> migration -> service -> FastAPI route -> Jinja page/partial -> validation states -> tests -> docs.
7. Validate with repo scripts; prefer `uv run ruff format --check .`, `uv run ruff check .`, `uv run ty check`, `uv run pytest`; for DB, `uv run alembic upgrade head`.

## Architecture Defaults

Simple app:

```txt
app/{main.py,core,routes,templates,static,components,services}
```

Persisted/admin system:

```txt
app/
  main.py
  core/{config.py,security.py,templates.py}
  db/{session.py,models.py}
  features/{public,admin,bookings,orders,catalog,cashflow}
  templates/{layouts,pages,partials,components}
  static/{css,js}
  tests/
alembic/versions/
```

Dependency direction:

```txt
routes -> services -> db/session/models
routes -> templates
services -> db/session/models
models -> no routes/templates imports
templates -> no business logic
```

Keep business rules testable; IO/framework/provider code stays at edges.

## Output

Planning responses include: summary, package/profile, MVP, phase 2, out of scope, route map, template map, data model, architecture, checklist, risks/questions, and state files updated.

Implementation responses include: files changed, behavior added, validation run, assumptions/remaining confirmations, and state updates when decisions or next steps changed.
