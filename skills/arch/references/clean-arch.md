# Clean Arch

Use this reference when the main design problem is where code should live and
which direction dependencies should point.

## Core Rule

Dependencies point inward. The core business model does not know about
frameworks, databases, transports, or runtime entrypoints.

## Layer Responsibilities

| Layer          | Responsibilities                                                                           | Dependency Rule                              |
| -------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------- |
| Domain         | entities, value objects, aggregates, domain services, repository interfaces, domain events | depends on nothing outside the domain        |
| Application    | use case orchestration, handlers, DTOs, transactions                                       | depends on domain only                       |
| Infrastructure | repository implementations, API clients, storage, queues, framework wiring                 | depends on application and domain contracts  |
| Presentation   | routes, CLI commands, handlers, request/response schemas, auth middleware                  | depends on application and selected adapters |

## Vocabulary

- **Clean Architecture** emphasizes inner vs outer circles
- **Onion Architecture** emphasizes concentric layers around the domain
- **Hexagonal Architecture** emphasizes ports and adapters

These are variations of the same idea. Do not over-optimize the naming.

## Ports and Adapters

- **Port** = interface owned by the application core
- **Primary adapter** = drives the app, such as HTTP, CLI, tests
- **Secondary adapter** = is driven by the app, such as SQL, Redis, external APIs
- use `Protocol` or equivalent abstractions at the boundary

## Directory Shape

```text
src/myapp/
├── domain/
├── application/
├── infrastructure/
└── presentation/
```

Use this shape only if it clarifies the codebase. Do not force a large
directory split on a tiny project.

## Composition Root

Wire implementations to abstractions at the entrypoint:

- application startup
- main module
- dependency injection container
- route dependency factory

This should be the only place that knows about all layers at once.

## Testing by Layer

| Layer          | Preferred Tests                                 |
| -------------- | ----------------------------------------------- |
| Domain         | unit tests for business behavior and invariants |
| Application    | unit or integration tests with fake adapters    |
| Infrastructure | integration tests against the real dependency   |
| Presentation   | contract or end-to-end tests                    |

## Common Violations

- domain imports ORM, HTTP, or framework types
- route handlers contain business logic
- services return ORM rows instead of domain objects or DTOs
- infrastructure is called directly from domain code
- circular imports reveal broken dependency direction

## When to Use

- APIs with meaningful business rules and multiple integrations
- apps that need stable testable cores
- systems with more than one delivery mechanism, such as HTTP plus jobs or CLI
- codebases suffering from framework leakage into core logic

## When Not to Use

- tiny scripts and very small CRUD apps
- codebases where extra layers would outweigh the value
- one-off workflows with almost no domain behavior
