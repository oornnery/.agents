# Project Name

<!-- Load the shared agent knowledge base -->
@.claude/CLAUDE.md

## Project Description

<!-- Brief description of what this project does and why -->

## Stack

<!-- Override or extend the base stack if needed -->
<!-- Example: -->
<!-- - **Database**: PostgreSQL + SQLModel -->
<!-- - **Cache**: Redis -->
<!-- - **Queue**: Arq / Dramatiq -->

## Quick Commands

<!-- Project-specific commands beyond the base set -->

```bash
uv run fastapi dev         # Start dev server
uv run task check          # Run full validation
```

## Validation

<!-- Project-specific validation sequence -->

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest -v
```

## Rules

<!-- Project-specific rules that extend the base rules -->

### Python

<!-- Add project-specific Python conventions -->
<!-- - IO at edges only — services and domain must be pure -->
<!-- - Use Annotated style for FastAPI parameters -->
<!-- - Pydantic BaseModel for all request/response schemas -->

### Git

<!-- Add project-specific git conventions -->
<!-- - Feature branches from dev -->
<!-- - Squash merge for PRs -->
<!-- - PR required for all changes to main -->

### Security

<!-- Add project-specific security rules -->
<!-- - Never commit .env files -->
<!-- - All external input validated at API boundaries -->
<!-- - Parameterized queries only -->

## Architecture

<!-- Describe the project's architecture pattern and key decisions -->
<!-- Reference: skills/architecture/SKILL.md for DDD, Clean Architecture, SOLID -->

```text
src/myapp/
├── domain/        # Business logic, entities, value objects
├── application/   # Use cases, orchestration
├── infrastructure/# Database, external APIs, messaging
├── presentation/  # HTTP routes, CLI, schemas
│   ├── api/       # JSON endpoints
│   └── views/     # HTML pages (if applicable)
└── settings.py    # Configuration
```

## Key Modules

<!-- Describe the most important modules and their responsibilities -->
<!-- This helps agents understand the codebase quickly -->

## Environment Variables

<!-- List required environment variables -->
<!-- Example: -->
<!-- | Variable | Description | Required | -->
<!-- |----------|-------------|----------| -->
<!-- | DATABASE_URL | PostgreSQL connection string | Yes | -->
<!-- | SECRET_KEY | JWT signing key | Yes | -->
<!-- | REDIS_URL | Redis connection string | No | -->
