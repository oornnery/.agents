# Python Project Structure & Module Architecture

Organize Python projects with clear module boundaries, explicit public interfaces, maintainable directory structures. Good organization = discoverable code, predictable changes.

## When to Use This Skill

- Starting new Python project
- Reorganizing existing codebase
- Defining module public APIs with `__all__`
- Choosing flat vs nested directory structures
- Determining test file placement
- Creating reusable library packages

## Core Concepts

### 1. Module Cohesion

Group related code that changes together. One module, one purpose.

### 2. Explicit Interfaces

`__all__` defines public. Unlisted = internal implementation detail.

### 3. Flat Hierarchies

Shallow directories preferred. Add depth only for genuine sub-domains.

### 4. Consistent Conventions

Apply naming and organization patterns uniformly across project.

## Quick Start

```text
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── services/
│       ├── models/
│       └── api/
├── tests/
├── pyproject.toml
└── README.md
```

## Fundamental Patterns

### Pattern 1: One Concept Per File

Each file focuses on single concept or closely related functions. Split when file:

- Handles multiple unrelated responsibilities
- Grows beyond 300-500 lines (varies by complexity)
- Contains classes that change for different reasons

```python
# Good: Focused files
# user_service.py - User business logic
# user_repository.py - User data access
# user_models.py - User data structures

# Avoid: Kitchen sink files
# user.py - Contains service, repository, models, utilities...
```

### Pattern 2: Explicit Public APIs with `__all__`

Define public interface for every module. Unlisted members = internal details.

```python
# mypackage/services/__init__.py
from .user_service import UserService
from .order_service import OrderService
from .exceptions import ServiceError, ValidationError

__all__ = [
    "UserService",
    "OrderService",
    "ServiceError",
    "ValidationError",
]

# Internal helpers remain private by omission
# from .internal_helpers import _validate_input  # Not exported
```

### Pattern 3: Flat Directory Structure

Minimal nesting preferred. Deep hierarchies = verbose imports, hard navigation.

```text
# Preferred: Flat structure
project/
├── api/
│   ├── routes.py
│   └── middleware.py
├── services/
│   ├── user_service.py
│   └── order_service.py
├── models/
│   ├── user.py
│   └── order.py
└── utils/
    └── validation.py

# Avoid: Deep nesting
project/core/internal/services/impl/user/
```

Add sub-packages only when genuine sub-domain requires isolation.

### Pattern 4: Test File Organization

Pick one approach, apply consistently across project.

#### Option A: Colocated Tests

```text
src/
├── user_service.py
├── test_user_service.py
├── order_service.py
└── test_order_service.py
```

Tests live next to code they verify. Easy to spot coverage gaps.

#### Option B: Parallel Test Directory

```text
src/
├── services/
│   ├── user_service.py
│   └── order_service.py
tests/
├── services/
│   ├── test_user_service.py
│   └── test_order_service.py
```

Clean separation between production and test code. Standard for larger projects.

## Advanced Patterns

### Pattern 5: Package Initialization

Use `__init__.py` to provide clean public interface for package consumers.

```python
# mypackage/__init__.py
"""MyPackage - A library for doing useful things."""

from .core import MainClass, HelperClass
from .exceptions import PackageError, ConfigError
from .config import Settings

__all__ = [
    "MainClass",
    "HelperClass",
    "PackageError",
    "ConfigError",
    "Settings",
]

__version__ = "1.0.0"
```

Consumers import directly from package:

```python
from mypackage import MainClass, Settings
```

### Pattern 6: Layered Architecture

Organize by architectural layer for clear separation of concerns.

```text
myapp/
├── api/           # HTTP handlers, request/response
│   ├── routes/
│   └── middleware/
├── services/      # Business logic
├── repositories/  # Data access
├── models/        # Domain entities
├── schemas/       # API schemas (Pydantic)
└── config/        # Configuration
```

Each layer depends only on layers below, never above.

### Pattern 7: Domain-Driven Structure

For complex apps, organize by business domain not technical layer.

```text
ecommerce/
├── users/
│   ├── models.py
│   ├── services.py
│   ├── repository.py
│   └── api.py
├── orders/
│   ├── models.py
│   ├── services.py
│   ├── repository.py
│   └── api.py
└── shared/
    ├── database.py
    └── exceptions.py
```

## File and Module Naming

### Conventions

- `snake_case` for all file and module names: `user_repository.py`
- Avoid abbreviations that obscure meaning: `user_repository.py` not `usr_repo.py`
- Match class names to file names: `UserService` in `user_service.py`

### Import Style

Absolute imports for clarity and reliability:

```python
# Preferred: Absolute imports
from myproject.services import UserService
from myproject.models import User

# Avoid: Relative imports
from ..services import UserService
from . import models
```

Relative imports break when modules moved or reorganized.

## Best Practices Summary

1. **Keep files focused** - One concept per file, split at 300-500 lines (varies)
2. **Define `__all__` explicitly** - Public interfaces clear
3. **Prefer flat structures** - Add depth only for genuine sub-domains
4. **Use absolute imports** - More reliable, clearer
5. **Be consistent** - Apply patterns uniformly
6. **Match names to content** - File names describe purpose
7. **Separate concerns** - Layers distinct, dependencies flow one direction
8. **Document your structure** - README explaining organization