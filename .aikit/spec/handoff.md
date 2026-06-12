# Handoff

## Context

<!-- Context tells the next agent why the project exists and what success looks like, reducing repeated onboarding. -->

This is a Task Management API built with FastAPI, SQLModel, and PostgreSQL. The goal is a clean, secure REST backend for personal and team task tracking. The current sprint focuses on core CRUD for tasks, projects, and labels, plus a passing validation pipeline.

## Current State

<!-- Current state orients the next agent to the immediate situation so they do not start with stale assumptions. -->

The project structure is in place. Database migrations exist for users, tasks, projects, and labels. Task and project endpoints are functional. Unit tests cover the service layer at 85%. The next priority is adding sorting, soft deletes, and running the full validation suite.

## Completed

- Project scaffolding with FastAPI and SQLModel
- Alembic migrations for core tables
- JWT authentication with registration and login
- Task CRUD with filtering and pagination
- Project and label endpoints
- Service-layer unit tests

## Remaining

- Add sorting by due date and priority on task lists
- Implement soft-delete and archive behavior
- Enforce unique project names per user
- Run `ruff`, `ty`, `pyright`, `pytest`, and `bandit` and resolve any issues
- Update OpenAPI annotations for all endpoints
- Add integration tests for the full request lifecycle

## Validation

- `uv run pytest -v`: PASS (42 tests, 85% coverage)
- `uv run ruff check . --fix`: PASS
- `uv run ty check src && uv run pyright`: PASS
- `uv run bandit -r src`: PASS
- Next validation target: reach 90% coverage and zero skipped tests before recurring tasks

## Risks

<!-- Calling out risks early prevents surprises and lets the next agent prioritize defensively. -->

- The two skipped integration tests mask a potential database fixture conflict that could block CI
- Soft-delete logic must not break existing foreign-key constraints on tasks linked to projects
- Mobile clients may push back on the 15-minute JWT window, requiring refresh-token work sooner than planned
