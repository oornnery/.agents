# Project Name

<!-- Load the shared agent knowledge base -->
@.claude/CLAUDE.md

## Project Description

<!-- Brief description of what this project does and why -->

## Stack

### Backend

- **Language**: Python 3.12+
- **Framework**: FastAPI
- **Database**: PostgreSQL + SQLModel
<!-- - **Cache**: Redis -->
<!-- - **Queue**: Arq -->

### Frontend

- **Framework**: SolidJS + SolidStart
- **Styling**: Tailwind CSS v4
- **Components**: Basecoat
<!-- - **State**: SolidJS signals -->

## Quick Commands

```bash
# Backend
uv run fastapi dev                    # Start API server
uv run pytest -v                      # Run backend tests

# Frontend
cd frontend && npm run dev            # Start frontend dev server
cd frontend && npm run test           # Run frontend tests
cd frontend && npm run build          # Production build

# Full stack
uv run task dev                       # Start both servers
uv run task check                     # Run all validation
```

## Validation

```bash
# Backend
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest -v

# Frontend
cd frontend && npm run lint
cd frontend && npm run typecheck
cd frontend && npm run test
```

## Rules

### Python

<!-- Backend-specific Python rules -->
<!-- - IO at edges only — services and domain must be pure -->
<!-- - Use Annotated style for FastAPI parameters -->
<!-- - Pydantic BaseModel for all request/response schemas -->

### Frontend

<!-- Frontend-specific rules -->
<!-- - Components in src/components/, pages in src/routes/ -->
<!-- - Tailwind utility classes only — no custom CSS unless necessary -->
<!-- - All interactive elements must be keyboard accessible -->

### Git

<!-- Project git conventions -->
<!-- - Feature branches from dev -->
<!-- - Squash merge for PRs -->

### Security

<!-- Project security rules -->
<!-- - Never commit .env files -->
<!-- - All API input validated via Pydantic -->
<!-- - CORS configured for allowed origins only -->

## Architecture

### Backend

```text
src/myapp/
├── domain/        # Business logic
├── application/   # Use cases
├── infrastructure/# Database, external APIs
└── presentation/
    ├── api/       # JSON endpoints
    ��── schemas/   # Pydantic models
```

### Frontend

```text
frontend/src/
├── components/    # Reusable UI components
├── routes/        # Page components (file-based routing)
├── lib/           # Utilities, API client, stores
├── styles/        # Global styles, tokens
└── app.tsx        # Root component
```

## API Contract

<!-- Define the API surface between frontend and backend -->
<!-- Example: -->
<!-- POST /api/auth/login  -> LoginRequest  -> TokenResponse (200) -->
<!-- GET  /api/users/me    -> (auth header) -> UserResponse (200) -->

## Environment Variables

<!-- | Variable | Description | Required | -->
<!-- |----------|-------------|----------| -->
<!-- | DATABASE_URL | PostgreSQL connection string | Yes | -->
<!-- | SECRET_KEY | JWT signing key | Yes | -->
<!-- | VITE_API_URL | Backend API URL for frontend | Yes | -->
