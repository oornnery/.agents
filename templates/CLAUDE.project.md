# Project Name

@.claude/CLAUDE.md

## Project Description

<!-- Brief description of what this project does and why -->

## Stack

<!-- Only list additions beyond the base stack -->
<!-- - **Database**: PostgreSQL + SQLModel -->
<!-- - **Cache**: Redis -->

## Quick Commands

```bash
uv run fastapi dev         # Start dev server
uv run task check          # Run full validation
```

## Architecture

<!-- Describe key modules and architecture pattern -->
<!-- Reference: skills/architecture/SKILL.md -->

```text
src/myapp/
├── domain/        # Business logic, entities
├── application/   # Use cases, orchestration
├── infrastructure/# Database, external APIs
└── presentation/  # HTTP routes, CLI, schemas
```

## Environment Variables

<!-- | Variable | Description | Required | -->
<!-- |----------|-------------|----------| -->
