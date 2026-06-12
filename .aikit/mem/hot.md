# Hot Memory

<!-- This file is loaded at the start of every session. Keep facts stable and high-value so agents immediately know the project landscape without re-discovering basics. -->

Keep this file under 80 lines. Store only stable, verified, cross-session facts.

## Stack

- [2024-03-15] FastAPI + SQLModel + PostgreSQL + uv
- [2024-03-15] Alembic for migrations, pytest for tests
- [2024-03-20] Deployed on Fly.io via Docker

## Auth

- [2024-03-18] JWT access tokens (15 min) + refresh tokens (7 days) in httpOnly cookies
- [2024-03-18] Password hashing with bcrypt, no plain text ever

## Data Model

- [2024-03-16] Core entities: User, Task, Project, Comment, Tag
- [2024-03-16] Task statuses: backlog, todo, in_progress, in_review, done, cancelled
- [2024-03-17] Tasks belong to one Project; Users can belong to many Projects via Membership

## API Constraints

- [2024-03-19] RESTful JSON API, versioned via /v1/ prefix
- [2024-03-19] Pagination default 20, max 100; cursor-based for real-time feeds
- [2024-03-21] Rate limit: 100 req/min per IP, 1000 req/min per authenticated user

## Key Invariants

<!-- Invariants are rules that rarely change. Stating them here prevents agents from accidentally breaking them during refactors. -->

- [2024-03-22] Task due_date must be >= created_at; enforced at DB + API layer
- [2024-03-22] Deleting a Project soft-deletes its Tasks (cascade flag, not hard delete)
