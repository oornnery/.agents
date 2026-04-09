# SOLID Principles in Python

## S — Single Responsibility Principle

A class or module should have **one reason to change**.

```python
# BAD: UserService does auth, validation, persistence, and email
class UserService:
    def register(self, data): ...      # validation
    def authenticate(self, creds): ... # auth logic
    def save_to_db(self, user): ...    # persistence
    def send_welcome_email(self, user): ... # notification

# GOOD: each concern has its own module
class UserValidator:
    def validate(self, data: CreateUserRequest) -> User: ...

class AuthService:
    def authenticate(self, credentials: Credentials) -> Token: ...

class UserRepository(Protocol):
    def save(self, user: User) -> None: ...

class NotificationService:
    def send_welcome(self, user: User) -> None: ...
```

**Heuristic**: if you can describe what a class does without using "and",
it has a single responsibility.

## O — Open/Closed Principle

Open for **extension**, closed for **modification**.

```python
from typing import Protocol


# Define the extension point
class DiscountStrategy(Protocol):
    def calculate(self, total: int) -> int: ...


# Implementations extend behavior without modifying existing code
class PercentageDiscount:
    def __init__(self, percent: int) -> None:
        self.percent = percent

    def calculate(self, total: int) -> int:
        return total * self.percent // 100


class FixedDiscount:
    def __init__(self, amount: int) -> None:
        self.amount = amount

    def calculate(self, total: int) -> int:
        return min(self.amount, total)


# Usage — adding new discount types never touches this function
def apply_discount(total: int, strategy: DiscountStrategy) -> int:
    return total - strategy.calculate(total)
```

## L — Liskov Substitution Principle

Subtypes must be **substitutable** for their base types without breaking
callers.

```python
from typing import Protocol


class FileStorage(Protocol):
    def save(self, key: str, data: bytes) -> str: ...
    def load(self, key: str) -> bytes: ...


class LocalStorage:
    def save(self, key: str, data: bytes) -> str:
        path = Path(f"/tmp/{key}")
        path.write_bytes(data)
        return str(path)

    def load(self, key: str) -> bytes:
        return Path(f"/tmp/{key}").read_bytes()


class S3Storage:
    def save(self, key: str, data: bytes) -> str:
        self.client.put_object(Bucket=self.bucket, Key=key, Body=data)
        return f"s3://{self.bucket}/{key}"

    def load(self, key: str) -> bytes:
        return self.client.get_object(Bucket=self.bucket, Key=key)["Body"].read()


# Any FileStorage implementation works here — that's Liskov
def backup_data(storage: FileStorage, key: str, data: bytes) -> str:
    return storage.save(key, data)
```

**Violations to watch for:**

- Subclass raises `NotImplementedError` for a method the base defines
- Subclass changes return type or narrows parameter types
- Subclass has preconditions the base does not require

## I — Interface Segregation Principle

No client should depend on methods it does not use.

```python
# BAD: one fat interface
class Repository(Protocol):
    def get(self, id: str) -> Model: ...
    def save(self, model: Model) -> None: ...
    def delete(self, id: str) -> None: ...
    def search(self, query: str) -> list[Model]: ...
    def export_csv(self) -> bytes: ...  # not everyone needs this

# GOOD: small, focused interfaces
class Readable(Protocol):
    def get(self, id: str) -> Model: ...

class Writable(Protocol):
    def save(self, model: Model) -> None: ...

class Searchable(Protocol):
    def search(self, query: str) -> list[Model]: ...

# Compose as needed
class UserRepository(Readable, Writable, Searchable, Protocol): ...
```

In Python, `Protocol` makes this natural — compose small protocols
into larger ones as needed.

## D — Dependency Inversion Principle

High-level modules should not depend on low-level modules. Both should
depend on **abstractions**.

```python
# BAD: service depends directly on implementation
from myapp.infrastructure.persistence.sql_user_repo import SqlUserRepository

class UserService:
    def __init__(self) -> None:
        self.repo = SqlUserRepository()  # hard dependency

# GOOD: service depends on abstraction
from myapp.domain.repositories.user_repo import UserRepository

class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo  # injected Protocol

# Wiring happens at the composition root
service = UserService(repo=SqlUserRepository(session))
```

**In FastAPI**, use `Depends` for injection:

```python
from typing import Annotated
from fastapi import Depends

def get_user_repo(session: Annotated[Session, Depends(get_session)]) -> UserRepository:
    return SqlUserRepository(session)

@router.post("/users")
async def create_user(
    data: CreateUserRequest,
    repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> UserResponse:
    user = User(name=data.name, email=data.email)
    repo.save(user)
    return UserResponse.from_domain(user)
```
