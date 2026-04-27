# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!--
Fullstack overlay for server-rendered Python web apps.
Use for FastAPI backends that render Jinja2 templates, use htmx for HTML-over-
-wire interactions, and use Alpine.js only for small client-side behavior.
-->

## Project Description

<!-- Brief description of what this project does and why -->
<!-- Include primary user flows and highest-risk integration points -->

## Stack

### Backend

- **Framework**: FastAPI
- **Valid**: Pydantic
- **HTTP Client**: HTTPX
- **Database**: PostgreSQL + SQLModel
<!-- - **Cache**: Redis -->

### Frontend

- **Templates**: Jinja2
- **HTML Interaction**: htmx
- **Client-Side State**: Alpine.js
<!-- - **Styling**: CSS / Tailwind -->

## Quick Commands

```bash
uv sync
uv run fastapi dev src/myapp/main.py  # Start the app in development
uv run task check                     # Run full validation
uv run pytest -v                      # Run backend and template-facing tests
```

## Validation Entry Points

### Backend

<!-- - `uv run pytest tests/unit -q` -->
<!-- - `uv run pytest tests/integration -q` -->
<!-- - `uv run ruff check . && uv run ty check src` -->

### Frontend

<!-- - template rendering checks -->
<!-- - htmx fragment or partial response checks -->
<!-- - browser interaction smoke tests when Alpine behavior matters -->

### Fullstack

<!-- - API contract checks -->
<!-- - auth flow verification -->
<!-- - end-to-end happy path and failure path -->

## Architecture

### Backend

```text
src/myapp/
├── api/           # app entrypoint, middleware, dependency wiring
├── routes/        # HTTP routes grouped by feature
├── schemas/       # request and response shapes
├── core/          # core rules and reusable logic
├── services/      # orchestration and integration flows
├── database/      # sessions, queries, migrations
└── models/        # database or persisted data models
```

### Templates and UI

```text
src/myapp/
├── views/         # render helpers and page/fragment composition
├── templates/     # Jinja2 pages, partials, and shared fragments
└── static/        # Alpine scripts, CSS, images, and browser assets
```

## Surface Boundaries

- backend owns core rules, persistence, auth, template context, integration correctness
- Jinja2 owns server-rendered pages/fragments, not business rules
- htmx owns request triggering + fragment replacement, not app state
- Alpine owns small local behavior (toggles, disclosure, progressive enhancement), not canonical data or permission decisions
- no leaking DB/ORM shapes into page context or browser contracts
- keep full-page, fragment, redirect, error states explicit

## Backend and Frontend Defaults

### Backend

- routes, schemas, service orchestration explicit
- persistence + integration code out of public contracts
- auth, session, permission behavior visible at edge
- prefer `Pydantic` for request, response, page-context shaping
- prefer `HTTPX` for server-side HTTP integrations
- prefer `SQLModel` for typed SQLAlchemy-style persistence

### Frontend

- page context, fragment context, shared template helpers explicit
- loading, empty, error, success states explicit in rendered HTML
- prefer htmx-driven HTML responses over JSON + custom client rendering for normal UI flows
- Alpine behavior local + small; state surviving navigation or shared across screens moves back to server or explicit API
- accessibility, focus handling, progressive enhancement part of default impl

## Shared Contract Rules

- page endpoints, fragment endpoints, JSON endpoints clearly separated
- htmx expects fragment → return intentional HTML, not ad hoc strings
- use htmx headers, redirects, swap behavior intentionally
- Alpine data shapes aligned with rendered HTML they enhance
- no template/browser workarounds for backend contract drift
- document auth, file transfer, CSRF, cache invalidation behavior clearly

## Integration Rules

<!-- Document how sides fit together -->
<!-- - API base URL and env switching -->
<!-- - auth token or cookie flow -->
<!-- - CSRF token handling for form and htmx posts -->
<!-- - file upload/download path -->
<!-- - fragment vs full-page response rules -->
<!-- - Alpine enhancement hooks and event conventions -->

## Fullstack Checklist

### Backend

- [ ] routes, schemas, response shapes explicit
- [ ] auth, session, permission enforced server-side
- [ ] DB models not leaked into browser contracts or page context

### Templates, htmx, and Alpine

- [ ] templates receive explicit context, render predictable partials
- [ ] htmx swaps, targets, triggers, redirects intentional
- [ ] forms validate + fail clearly
- [ ] Alpine behavior local + progressive
- [ ] accessibility + responsive behavior checked

### Integration

- [ ] rendered HTML + fragment endpoints match real backend contract
- [ ] auth flow consistent across layers
- [ ] CSRF + unsafe methods handled explicitly
- [ ] shared examples + docs sync with contract changes

### Verification

- [ ] backend valid passes
- [ ] page + fragment rendering paths pass
- [ ] critical end-to-end flows pass
- [ ] failure + recovery paths exercised

## Testing Focus

### Backend

<!-- - API contracts -->
<!-- - integration with database and external services -->
<!-- - permission and valid boundaries -->

### Frontend

<!-- - page rendering and partial rendering -->
<!-- - htmx request/response behavior -->
<!-- - form valid and submission -->
<!-- - accessibility and responsive behavior -->

### End-to-End

<!-- - sign-in or onboarding -->
<!-- - core user journey -->
<!-- - rollback or failure recovery path -->

## Environment Variables

<!-- | Variable | Description | Required | -->
<!-- |----------|-------------|----------| -->

## Fullstack Guardrails

- no coupling templates/Alpine directly to persistence details
- no hiding backend contract changes behind template workarounds or browser scripts
- auth, session, CSRF, permission explicit in both layers
- htmx flows inspectable: request, target, swap, response shape all obvious
- update docs + examples when shared contracts change
