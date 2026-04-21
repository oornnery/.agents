# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!--
Fullstack overlay for server-rendered Python web apps.
Use for FastAPI backends that render Jinja2 templates, use htmx for HTML-over-
the-wire interactions, and use Alpine.js only for small client-side behavior.
-->

## Project Description

<!-- Brief description of what this project does and why -->
<!-- Include the primary user flows and the highest-risk integration points -->

## Stack

### Backend

- **Framework**: FastAPI
- **Validation**: Pydantic
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

- backend owns core rules, persistence, auth enforcement, template context,
  and integration correctness
- Jinja2 owns server-rendered pages and fragments, not business rules
- htmx owns request triggering and fragment replacement, not application state
- Alpine owns small local behavior such as toggles, disclosure state, and
  progressive enhancement, not canonical data or permission decisions
- do not leak database or ORM shapes directly into page context or browser-
  facing contracts
- keep full-page responses, fragments, redirects, and error states explicit

## Backend and Frontend Defaults

### Backend

- keep routes, schemas, and service orchestration explicit
- keep persistence and integration code out of public contracts
- make auth, session, and permission behavior visible at the edge
- prefer `Pydantic` for request, response, and page-context shaping
- prefer `HTTPX` for server-side HTTP integrations
- prefer `SQLModel` when typed SQLAlchemy-style persistence is a good fit

### Frontend

- keep page context, fragment context, and shared template helpers explicit
- keep loading, empty, error, and success states explicit in rendered HTML
- prefer htmx-driven HTML responses over JSON plus custom client rendering for
  normal UI flows
- keep Alpine behavior local and small; if state must survive navigation or be
  shared across screens, move it back to the server or an explicit API
- keep accessibility, focus handling, and progressive enhancement part of the
  default implementation

## Shared Contract Rules

- keep page endpoints, fragment endpoints, and JSON endpoints clearly separated
- when htmx expects a fragment, return HTML intentionally instead of ad hoc
  strings
- use htmx headers, redirects, and swap behavior intentionally
- keep Alpine data shapes aligned with the rendered HTML they enhance
- avoid template or browser workarounds for backend contract drift
- document auth, file transfer, CSRF, and cache invalidation behavior clearly

## Integration Rules

<!-- Document how the sides fit together -->
<!-- - API base URL and environment switching -->
<!-- - auth token or cookie flow -->
<!-- - CSRF token handling for form and htmx posts -->
<!-- - file upload/download path -->
<!-- - fragment vs full-page response rules -->
<!-- - Alpine enhancement hooks and event conventions -->

## Fullstack Checklist

### Backend

- [ ] routes, schemas, and response shapes are explicit
- [ ] auth, session, and permission behavior are enforced server-side
- [ ] database models do not leak into browser-facing contracts or page context

### Templates, htmx, and Alpine

- [ ] templates receive explicit context and render predictable partials
- [ ] htmx swaps, targets, triggers, and redirects are intentional
- [ ] forms validate and fail clearly
- [ ] Alpine behavior stays local and progressive
- [ ] accessibility and responsive behavior are checked

### Integration

- [ ] rendered HTML and fragment endpoints match the real backend contract
- [ ] auth flow is consistent across both layers
- [ ] CSRF and unsafe methods are handled explicitly
- [ ] shared examples and docs stay in sync with contract changes

### Verification

- [ ] backend validation passes
- [ ] page and fragment rendering paths pass
- [ ] critical end-to-end flows pass
- [ ] failure and recovery paths are exercised

## Testing Focus

### Backend

<!-- - API contracts -->
<!-- - integration with database and external services -->
<!-- - permission and validation boundaries -->

### Frontend

<!-- - page rendering and partial rendering -->
<!-- - htmx request/response behavior -->
<!-- - form validation and submission -->
<!-- - accessibility and responsive behavior -->

### End-to-End

<!-- - sign-in or onboarding -->
<!-- - core user journey -->
<!-- - rollback or failure recovery path -->

## Environment Variables

<!-- | Variable | Description | Required | -->
<!-- |----------|-------------|----------| -->

## Fullstack Guardrails

- do not couple templates or Alpine behavior directly to persistence details
- do not hide backend contract changes behind template workarounds or browser
  scripts
- keep auth, session, CSRF, and permission behavior explicit in both layers
- keep htmx flows inspectable: request, target, swap, and response shape should
  all be obvious
- update docs and examples when shared contracts change
