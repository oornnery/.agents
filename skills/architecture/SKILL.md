---
name: architecture
description: Software architecture patterns -- DDD, Clean Architecture, Onion, SOLID, Clean Code, SDD. Load when designing system architecture, structuring domains, or applying design principles.
---

# Software Architecture

Patterns for structuring maintainable, scalable Python systems.

## Domain-Driven Design (DDD)

### Core Concepts

| Concept             | Description                                             |
| ------------------- | ------------------------------------------------------- |
| Bounded Context     | Boundary within which a model has a specific meaning    |
| Entity              | Object with identity that persists across state changes |
| Value Object        | Immutable object defined by its attributes, no identity |
| Aggregate           | Cluster of entities treated as a unit for data changes  |
| Repository          | Abstraction for persistence (collection-like interface) |
| Domain Service      | Stateless operation that doesn't belong to an entity    |
| Application Service | Orchestrates use cases, delegates to domain layer       |

### Key Rules

- **Domain layer has zero external dependencies** -- no SQLAlchemy,
  no FastAPI, no HTTP. Only stdlib and domain types.
- **Dependencies point inward** -- presentation -> application -> domain.
- **Aggregates are consistency boundaries** -- one aggregate per transaction.
- **Repositories return domain objects**, not ORM models.

See `references/ddd.md` for layout and examples.

## Clean Architecture / Onion

Dependencies point inward: Presentation -> Infrastructure -> Application -> Domain.

- Domain depends on **nothing**
- Application depends on **domain only**
- Use `Protocol` to invert dependencies at layer boundaries

See `references/clean-architecture.md` for layout and examples.

## SOLID Principles

| Principle | Python Application                               |
| --------- | ------------------------------------------------ |
| **S**RP   | One module/class per concern                     |
| **O**CP   | Strategy pattern, plugins                        |
| **L**SP   | Consistent return types in subtypes              |
| **I**SP   | Small `Protocol` classes                         |
| **D**IP   | `Protocol` at boundaries, depend on abstractions |

See `references/solid.md` for examples.

## Clean Code

- Functions: <=20 lines, one level of abstraction, <=3 parameters.
- Early returns, no side effects unless named `save_`, `send_`, `delete_`.
- Catch specific exceptions, raise domain exceptions.
- Use context managers for cleanup.

## Design Patterns

| Pattern    | Python Approach                                   |
| ---------- | ------------------------------------------------- |
| Repository | `Protocol` + implementation                       |
| Factory    | Classmethod or standalone function                |
| Strategy   | `Protocol` + implementations                      |
| Observer   | Callback registry or event bus                    |
| Decorator  | Python decorators (`@wraps`)                      |
| Facade     | Module-level functions wrapping complex subsystem |

See `references/patterns.md` for examples.

## Related

- `commands/plan.md` -- SDD workflow, SPEC/ARCH templates, ADRs
- `commands/refactor.md` -- applying architecture principles
