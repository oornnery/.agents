# Clean Architecture / Onion / Hexagonal

All three patterns share the same core idea: **dependencies point inward**.
The domain is at the center and knows nothing about the outer layers.

## Layer Responsibilities

### Domain (Innermost)

- Entities, value objects, aggregates
- Domain services and rules
- Repository interfaces (`Protocol`)
- Domain events
- **No imports from other layers, no framework dependencies**

### Application

- Use case orchestration
- Command/query handlers
- Application services
- DTOs (data transfer objects between layers)
- Transaction management
- **Imports from domain only**

### Infrastructure

- Repository implementations (SQL, NoSQL, in-memory)
- External API clients
- Message queue adapters
- File storage, email services
- Framework configuration
- **Imports from domain and application**

### Presentation (Outermost)

- HTTP routes (FastAPI, Flask)
- CLI commands (Typer)
- WebSocket handlers
- Request/response schemas
- Authentication/authorization middleware
- **Imports from application (and sometimes infrastructure for DI)**

## Directory Layout

```text
src/myapp/
├── domain/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # Entity
│   │   └── order.py         # Aggregate
│   ├── events/
│   │   └── order_events.py  # Domain events
│   ├── services/
│   │   └── pricing.py       # Domain service
│   └── repositories/
│       ├── __init__.py
│       ├── user_repo.py     # Protocol
│       └── order_repo.py    # Protocol
├── application/
│   ├── __init__.py
│   ├── commands/
│   │   ├── create_user.py   # Use case
│   │   └── place_order.py   # Use case
│   ├── queries/
│   │   ├── get_user.py
│   │   └── list_orders.py
│   └── dtos/
│       └── user_dto.py
├── infrastructure/
│   ├── __init__.py
│   ├── persistence/
│   │   ├── database.py      # Engine, session factory
│   │   ├── models.py        # ORM models
│   │   ├── user_repo.py     # SqlUserRepository
│   │   └── order_repo.py    # SqlOrderRepository
│   ├── external/
│   │   └── payment_client.py
│   └── messaging/
│       └── event_bus.py
├── presentation/
│   ├── __init__.py
│   ├── api/
│   │   ├── users.py         # FastAPI router
│   │   └── orders.py
│   ├── schemas/
│   │   ├── user_schemas.py  # Pydantic request/response
│   │   └── order_schemas.py
│   └── dependencies.py      # FastAPI dependency injection
└── main.py                   # Composition root
```

## Composition Root

Wire everything together at the entry point — this is the only place
that knows about all layers.

```python
# main.py
from fastapi import FastAPI
from myapp.infrastructure.persistence.database import get_session
from myapp.infrastructure.persistence.user_repo import SqlUserRepository
from myapp.application.commands.create_user import CreateUserUseCase
from myapp.presentation.api.users import router as users_router


def create_app() -> FastAPI:
    app = FastAPI()

    # Wire dependencies
    session = get_session()
    user_repo = SqlUserRepository(session)
    create_user = CreateUserUseCase(user_repo)

    # Inject into routes via FastAPI depends or app.state
    app.state.create_user = create_user
    app.include_router(users_router)
    return app
```

## Hexagonal Architecture (Ports and Adapters)

Same dependency rule, different vocabulary:

- **Port** = interface defined by the application (`Protocol`)
- **Adapter** = implementation of a port (SQL adapter, HTTP adapter)
- **Primary/Driving adapter** = triggers the application (HTTP route, CLI)
- **Secondary/Driven adapter** = called by the application (database, API)

```text
┌────────────────────────────────────────────┐
│              Primary Adapters              │
│         (HTTP routes, CLI, tests)          │
│                    │                       │
│                    ▼                       │
│  ┌──────────────────────────────────┐     │
│  │        Application Core          │     │
│  │  ┌────────────────────────┐      │     │
│  │  │   Domain (Entities,    │      │     │
│  │  │   Services, Rules)     │      │     │
│  │  └────────────────────────┘      │     │
│  │                                  │     │
│  │  Ports (Protocol interfaces)     │     │
│  └──────────────────────────────────┘     │
│                    │                       │
│                    ▼                       │
│           Secondary Adapters               │
│     (SQL, Redis, HTTP clients, MQ)        │
└────────────────────────────────────────────┘
```

## Testing by Layer

| Layer          | Test Type        | What to Test                                              |
| -------------- | ---------------- | --------------------------------------------------------- |
| Domain         | Unit             | Entity behavior, value object invariants, domain services |
| Application    | Unit/Integration | Use case orchestration with fake repos                    |
| Infrastructure | Integration      | Repository implementations against real DB                |
| Presentation   | E2E/Contract     | HTTP status codes, response shapes, auth                  |

The domain layer should have the highest test coverage since it contains
the core business logic and has no external dependencies.

## Common Violations

| Violation                              | Fix                                                       |
| -------------------------------------- | --------------------------------------------------------- |
| Domain imports SQLAlchemy              | Extract ORM model to infrastructure, map to domain entity |
| Service returns ORM model              | Return domain entity or DTO                               |
| Route contains business logic          | Extract to application service                            |
| Circular import between layers         | Check dependency direction, introduce interface           |
| Infrastructure used directly in domain | Inject via Protocol                                       |
