---
name: architecture
description: Software architecture patterns — DDD, Clean Architecture, Onion, SOLID, Clean Code, SDD. Load when designing system architecture, structuring domains, or applying design principles.
---

# Software Architecture

Patterns and principles for structuring maintainable, scalable systems.
This skill covers the patterns most commonly needed in Python web
applications.

## Domain-Driven Design (DDD)

DDD structures code around the business domain, not technical concerns.

### Core Concepts

| Concept                 | Description                                             |
| ----------------------- | ------------------------------------------------------- |
| **Bounded Context**     | A boundary within which a model has a specific meaning  |
| **Entity**              | Object with identity that persists across state changes |
| **Value Object**        | Immutable object defined by its attributes, no identity |
| **Aggregate**           | Cluster of entities treated as a unit for data changes  |
| **Repository**          | Abstraction for persistence (collection-like interface) |
| **Domain Service**      | Stateless operation that doesn't belong to an entity    |
| **Domain Event**        | Something that happened that domain experts care about  |
| **Application Service** | Orchestrates use cases, delegates to domain layer       |

### Python DDD Layout

```text
src/myapp/
├── domain/                 # Pure business logic — no framework imports
│   ├── models/             # Entities, value objects, aggregates
│   │   ├── user.py
│   │   └── order.py
│   ├── events/             # Domain events
│   │   └── order_placed.py
│   ├── services/           # Domain services
│   │   └── pricing.py
│   └── repositories/       # Repository interfaces (Protocol)
│       └── user_repo.py
├── application/            # Use case orchestration
│   ├── commands/           # Write operations
│   │   └── create_order.py
│   ├── queries/            # Read operations
│   │   └── get_user.py
│   └── services/           # Application services
│       └── order_service.py
├── infrastructure/         # External concerns
│   ├── persistence/        # Repository implementations
│   │   └── sql_user_repo.py
│   ├── messaging/          # Event bus, queues
│   └── external/           # Third-party API clients
└── presentation/           # HTTP/CLI layer
    ├── api/                # FastAPI routes
    ├── views/              # HTML pages
    └── schemas/            # Request/response DTOs
```

### Key Rules

- **Domain layer has zero external dependencies** — no SQLAlchemy,
  no FastAPI, no HTTP. Only stdlib and domain types.
- **Dependencies point inward** — presentation → application → domain.
  Never the reverse.
- **Aggregates are consistency boundaries** — modify one aggregate per
  transaction.
- **Repositories return domain objects**, not ORM models.

See `references/ddd.md` for detailed examples.

## Clean Architecture / Onion Architecture

Both patterns enforce the **Dependency Rule**: source code dependencies
point inward, from outer layers to inner layers. Inner layers know nothing
about outer layers.

### Layer Structure

```text
┌─────────────────────────────────────────┐
│  Presentation (API, CLI, UI)            │  ← Outermost
├─────────────────────────────────────────┤
│  Infrastructure (DB, HTTP, filesystem)  │
├─────────────────────────────────────────┤
│  Application (use cases, orchestration) │
├─────────────────────────────────────────┤
│  Domain (entities, value objects, rules)│  ← Innermost
└─────────────────────────────────────────┘
```

### The Dependency Rule

- Domain depends on **nothing**
- Application depends on **domain only**
- Infrastructure depends on **application and domain**
- Presentation depends on **application** (and sometimes infrastructure)

### Inversion at Boundaries

Use `Protocol` to invert dependencies at layer boundaries:

```python
# domain/repositories/user_repo.py — domain defines the interface
from typing import Protocol

class UserRepository(Protocol):
    def get(self, user_id: str) -> User | None: ...
    def save(self, user: User) -> None: ...

# infrastructure/persistence/sql_user_repo.py — infra implements it
class SqlUserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, user_id: str) -> User | None: ...
    def save(self, user: User) -> None: ...
```

See `references/clean-architecture.md` for full layout and examples.

## SOLID Principles

| Principle                     | Summary                                     | Python Application           |
| ----------------------------- | ------------------------------------------- | ---------------------------- |
| **S** — Single Responsibility | One reason to change                        | One module/class per concern |
| **O** — Open/Closed           | Open for extension, closed for modification | Strategy pattern, plugins    |
| **L** — Liskov Substitution   | Subtypes must be substitutable              | Consistent return types      |
| **I** — Interface Segregation | No client depends on unused methods         | Small `Protocol` classes     |
| **D** — Dependency Inversion  | Depend on abstractions, not concretions     | `Protocol` at boundaries     |

See `references/solid.md` for each principle with Python examples.

## Clean Code Principles

### Naming

- Functions: verbs (`create_user`, `calculate_total`, `validate_email`)
- Classes: nouns (`UserService`, `OrderRepository`, `PricingStrategy`)
- Booleans: questions (`is_active`, `has_permission`, `can_edit`)
- Constants: `UPPER_SNAKE` (`MAX_RETRIES`, `DEFAULT_TIMEOUT`)
- No abbreviations except universally known ones (`id`, `url`, `http`)

### Functions

- **Small** — 20 lines or fewer. Extract when longer.
- **One level of abstraction** — don't mix high-level orchestration with
  low-level details in the same function.
- **3 parameters max** — use a dataclass or config object for more.
- **Early returns** — handle edge cases first, keep the happy path at the
  bottom.
- **No side effects** unless explicitly stated in the name (`save_`, `send_`,
  `delete_`).

### Error Handling

- Catch specific exceptions, never bare `except:`
- Raise domain exceptions, not generic ones (`UserNotFoundError`, not `ValueError`)
- Error messages should help the developer fix the problem
- Use context managers for cleanup (`with` statements)

## Spec-Driven Development (SDD)

Specifications are the source of truth — code serves the specification.

1. Write **SPEC.md** (requirements, acceptance criteria)
2. Write **ARCH.md** (architecture, components, diagrams)
3. Write **SDD.md** (implementation plan, test strategy)
4. Implement following the spec — divergence requires spec update

See `commands/plan.md` for templates and workflow.

## Design Patterns (Python)

Common patterns used in well-architected Python projects:

| Pattern    | When to Use             | Python Approach                                   |
| ---------- | ----------------------- | ------------------------------------------------- |
| Repository | Persistence abstraction | `Protocol` + implementation                       |
| Factory    | Complex object creation | Classmethod or standalone function                |
| Strategy   | Swappable algorithms    | `Protocol` + implementations                      |
| Observer   | Event-driven decoupling | Callback registry or event bus                    |
| Decorator  | Cross-cutting concerns  | Python decorators (`@wraps`)                      |
| Facade     | Simplified interface    | Module-level functions wrapping complex subsystem |

See `references/patterns.md` for implementation examples.

## Architecture Decision Records (ADRs)

Document significant architecture decisions:

```markdown
# ADR-001: Use PostgreSQL over MongoDB

## Status

Accepted

## Context

We need a database for user and order data with complex relationships.

## Decision

Use PostgreSQL with SQLModel for ORM.

## Consequences

- Relational queries are natural and efficient
- Migrations via Alembic
- Team already has PostgreSQL expertise
- Less flexibility for schema changes (acceptable trade-off)
```

Store ADRs in `docs/adr/` or alongside ARCH.md.

## Related

- `references/ddd.md` — DDD in depth with Python examples
- `references/clean-architecture.md` — Onion/Hexagonal layout
- `references/solid.md` — SOLID with Python examples
- `references/patterns.md` — Design patterns in Python
- `commands/plan.md` — SDD workflow and SPEC/ARCH templates
- `commands/refactor.md` — applying architecture principles to existing code
