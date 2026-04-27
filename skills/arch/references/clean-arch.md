# Clean Arch

Use when design problem is where code lives and which way dependencies point.

## Core Rule

Dependencies point inward. Core business model unaware of frameworks, databases, transports, runtime entrypoints.

## Layer Responsibilities

| Layer          | Responsibilities                                                                           | Dependency Rule                      |
| -------------- | ------------------------------------------------------------------------------------------ | ------------------------------------ |
| Domain         | entities, value objects, aggregates, domain services, repository interfaces, domain events | depends on nothing outside domain    |
| App            | use case orchestration, handlers, DTOs, transactions                                       | depends on domain only               |
| Infrastructure | repository implementations, API clients, storage, queues, framework wiring                 | depends on app and domain contracts  |
| Presentation   | routes, CLI commands, handlers, request/response schemas, auth middleware                  | depends on app and selected adapters |

## Vocabulary

- **Clean Architecture** emphasizes inner vs outer circles
- **Onion Architecture** emphasizes concentric layers around domain
- **Hexagonal Architecture** emphasizes ports and adapters

Variations of same idea. Do not over-optimize naming.

## Ports and Adapters

- **Port** = interface owned by app core
- **Primary adapter** = drives app, such as HTTP, CLI, tests
- **Secondary adapter** = is driven by app, such as SQL, Redis, external APIs
- use `Protocol` or equivalent abstractions at boundary

## Directory Shape

```text
src/myapp/
├── domain/
├── application/
├── infrastructure/
└── presentation/
```

Use only if it clarifies codebase. Do not force large directory split on tiny project.

## Composition Root

Wire implementations to abstractions at entrypoint:

- app startup
- main module
- dependency injection container
- route dependency factory

Only place that knows about all layers at once.

## Testing by Layer

| Layer          | Preferred Tests                                 |
| -------------- | ----------------------------------------------- |
| Domain         | unit tests for business behavior and invariants |
| App            | unit or integration tests with fake adapters    |
| Infrastructure | integration tests against real dependency       |
| Presentation   | contract or end-to-end tests                    |

## Common Violations

- domain imports ORM, HTTP, or framework types
- route handlers contain business logic
- services return ORM rows over domain objects or DTOs
- infrastructure is called directly from domain code
- circular imports reveal broken dependency direction

## When to Use

- APIs with meaningful business rules and multiple integrations
- apps needing stable testable cores
- systems with multiple delivery mechanisms (HTTP plus jobs or CLI)
- codebases suffering framework leakage into core logic

## When Not to Use

- tiny scripts and very small CRUD apps
- codebases where extra layers outweigh value
- one-off workflows with almost no domain behavior
