# Project Name

<!-- Load the shared agent knowledge base -->
@.claude/CLAUDE.md

## Project Description

<!-- Brief description of what this project does -->

## Stack

<!-- Override or extend the base stack if needed -->
<!-- Example: -->
<!-- - **Database**: PostgreSQL + SQLModel -->
<!-- - **Cache**: Redis -->

## Quick Commands

<!-- Project-specific commands beyond the base set -->

```bash
uv run fastapi dev         # Start dev server
uv run task check          # Run full validation
```

## Project-Specific Conventions

<!-- Add conventions unique to this project -->

## Architecture

<!-- Describe the project's architecture and key modules -->

```text
src/myapp/
├── api/           # JSON endpoints
├── views/         # HTML pages
├── services/      # Business logic
├── domain/        # Models and types
└── settings.py    # Configuration
```
