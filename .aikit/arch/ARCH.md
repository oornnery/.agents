# ARCH

## System Overview

A REST API for managing tasks across teams. Users create, assign, and track tasks through a state-driven lifecycle. Authentication controls access, and all task data persists in PostgreSQL.

The system serves three clients: a web frontend, a mobile app, and programmatic integrations via API keys. All clients share the same REST surface and authorization rules.

<!-- System overview anchors every decision to a concrete product. Without this, architecture debates drift into abstraction without a shared target. -->

## Core Boundaries

| Layer | Responsibility | What It Must Not Do |
| ----- | -------------- | ------------------- |
| API Routes | Parse HTTP, validate input, serialize responses | Direct database queries |
| Services | Enforce business rules, orchestrate operations | HTTP concerns or raw SQL |
| Repositories | Execute database queries, map rows to models | Business logic or authorization |
| Auth Middleware | Verify tokens, attach user context | Task state changes |
| Database | Store and retrieve data | Validate business invariants |

Routes call services. Services call repositories. No layer skips ahead. This keeps business logic testable without a running HTTP server or database.

<!-- Core boundaries define where responsibilities split. This prevents feature creep across modules and keeps each layer replaceable without rewriting the whole system. -->

## Data Flow

A client sends an authenticated request to create a task:

1. API route parses JSON body and validates required fields
2. Auth middleware confirms the bearer token and attaches the user ID
3. Service layer checks the assignee exists and the project is active
4. Repository layer inserts the task into PostgreSQL and returns the row
5. Service layer formats the response model
6. API route serializes JSON and returns HTTP 201

Task updates follow the same path. Reads skip the service layer when no business rule applies.

<!-- Data flow makes bottlenecks and failure points visible. Teams spot where latency or contention lives before they optimize the wrong layer. -->

## External Integrations

| System | Purpose | Protocol | Failure Mode |
| ------ | ------- | -------- | ------------ |
| PostgreSQL | Persistent task, user, and project storage | TCP/SQL | Return 503, retry on transient errors |
| SMTP relay | Future: email notifications for task assignments (out of scope v1) | TCP/TLS | Log failure, do not block the API response |

All external calls use connection pooling and explicit timeouts. The API remains available if external email services are down.

<!-- External integrations document failure expectations. This prevents the API from hard-coupling to every downstream and defines graceful degradation. -->

## Runtime Assumptions

- PostgreSQL 15+ with row-level locking on concurrent task updates
- API processes run behind a reverse proxy that handles TLS termination
- Clock skew between API nodes is under one second for token expiry checks
- File uploads are not supported; attachments use presigned URLs to object storage

<!-- Runtime assumptions state environmental constraints. Without these, operators and developers make conflicting guesses about deployment targets. -->

## Technology Stack

| Layer | Choice | Rationale |
| ----- | ------ | --------- |
| Language | Python 3.12+ | Team expertise, strong async ecosystem |
| Web framework | FastAPI | Native OpenAPI generation, async support |
| ORM | SQLModel | Type-safe models shared with Pydantic schemas |
| Database | PostgreSQL 15 | ACID compliance, JSON support for flexible metadata |
| Migrations | Alembic | Version-controlled schema changes |
| Testing | pytest with httpx | Async test client, database fixtures |

No additional languages or runtimes are required for core operation.

<!-- Technology stack records concrete choices and trade-offs. This stops future debates from revisiting settled decisions without new evidence. -->

## Deployment Model

The API runs as a stateless container fleet behind a load balancer. Each container connects to the same PostgreSQL instance.

| Environment | Nodes | Purpose |
| ----------- | ----- | ------- |
| Production | 3+ | Serve live traffic with rolling updates |
| Staging | 2 | Validate releases against production-like data |
| Local | 1 | Developer workflow with Docker Compose |

Configuration loads from environment variables. Secrets mount through the platform secret store, never committed to source control.

Health checks expose `/health` for load balancer probes and `/ready` for database connectivity. Unready pods receive no traffic.

<!-- Deployment model describes how the system lives in production. This bridges architecture and operations so scaling and rollout decisions have a shared baseline. -->
