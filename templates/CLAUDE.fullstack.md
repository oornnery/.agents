# Project Name

@.claude/CLAUDE.md

## Project Description

<!-- Brief description of what this project does and why -->

## Stack

### Backend

- **Framework**: FastAPI
- **Database**: PostgreSQL + SQLModel
<!-- - **Cache**: Redis -->

### Frontend

- **Framework**: SolidJS + SolidStart
- **Styling**: Tailwind CSS v4
- **Components**: Basecoat

## Quick Commands

```bash
# Backend
uv run fastapi dev                    # Start API server
uv run task check                     # Run all backend validation

# Frontend
cd frontend && npm run dev            # Start frontend dev server
cd frontend && npm run build          # Production build
```

## Architecture

### Backend

```text
src/myapp/
├── domain/        # Business logic
├── application/   # Use cases
├── infrastructure/# Database, external APIs
└── presentation/  # API endpoints, schemas
```

### Frontend

```text
frontend/src/
├── components/    # Reusable UI components
├── routes/        # Page components (file-based routing)
├── lib/           # Utilities, API client, stores
└── app.tsx        # Root component
```

## Environment Variables

<!-- | Variable | Description | Required | -->
<!-- |----------|-------------|----------| -->
