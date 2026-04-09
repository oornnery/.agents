# Design Patterns in Python

Practical implementations of patterns commonly used in Python web
applications. Prefer the simplest approach that solves the problem.

## Repository Pattern

Abstraction over persistence. The domain defines the interface, infrastructure
implements it.

```python
from typing import Protocol


class UserRepository(Protocol):
    def get(self, user_id: str) -> User | None: ...
    def save(self, user: User) -> None: ...
    def find_by_email(self, email: str) -> User | None: ...


# In-memory implementation (for tests)
class InMemoryUserRepository:
    def __init__(self) -> None:
        self._store: dict[str, User] = {}

    def get(self, user_id: str) -> User | None:
        return self._store.get(user_id)

    def save(self, user: User) -> None:
        self._store[user.id] = user

    def find_by_email(self, email: str) -> User | None:
        return next((u for u in self._store.values() if u.email == email), None)
```

Use when: you want to decouple domain logic from database specifics.

## Factory Pattern

Use a classmethod or standalone function — no `AbstractFactory` class needed.

```python
@dataclass
class Notification:
    recipient: str
    subject: str
    body: str
    channel: str

    @classmethod
    def email(cls, to: str, subject: str, body: str) -> "Notification":
        return cls(recipient=to, subject=subject, body=body, channel="email")

    @classmethod
    def sms(cls, to: str, body: str) -> "Notification":
        return cls(recipient=to, subject="", body=body, channel="sms")

    @classmethod
    def slack(cls, channel: str, body: str) -> "Notification":
        return cls(recipient=channel, subject="", body=body, channel="slack")
```

For more complex creation, use a standalone factory function:

```python
def create_payment_processor(provider: str, config: Config) -> PaymentProcessor:
    match provider:
        case "stripe":
            return StripeProcessor(api_key=config.stripe_key)
        case "paypal":
            return PayPalProcessor(client_id=config.paypal_id)
        case _:
            raise ValueError(f"Unknown provider: {provider}")
```

## Strategy Pattern

Swap algorithms at runtime via `Protocol`.

```python
from typing import Protocol


class SortStrategy(Protocol):
    def sort(self, items: list[dict]) -> list[dict]: ...


class SortByPrice:
    def sort(self, items: list[dict]) -> list[dict]:
        return sorted(items, key=lambda x: x["price"])


class SortByRating:
    def sort(self, items: list[dict]) -> list[dict]:
        return sorted(items, key=lambda x: x["rating"], reverse=True)


class SortByNewest:
    def sort(self, items: list[dict]) -> list[dict]:
        return sorted(items, key=lambda x: x["created_at"], reverse=True)


class ProductCatalog:
    def __init__(self, strategy: SortStrategy) -> None:
        self.strategy = strategy

    def list_products(self, products: list[dict]) -> list[dict]:
        return self.strategy.sort(products)
```

For simple cases, just pass a callable:

```python
def list_products(
    products: list[dict],
    sort_key: Callable[[dict], Any] = lambda x: x["price"],
) -> list[dict]:
    return sorted(products, key=sort_key)
```

## Observer / Event Bus

Decouple producers from consumers.

```python
from collections import defaultdict
from collections.abc import Callable
from typing import Any


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[type, list[Callable]] = defaultdict(list)

    def subscribe(self, event_type: type, handler: Callable) -> None:
        self._handlers[event_type].append(handler)

    def publish(self, event: Any) -> None:
        for handler in self._handlers.get(type(event), []):
            handler(event)


# Usage
bus = EventBus()
bus.subscribe(OrderPlaced, send_confirmation_email)
bus.subscribe(OrderPlaced, update_inventory)
bus.subscribe(OrderPlaced, notify_warehouse)

# When an order is placed
bus.publish(OrderPlaced(order_id="123", total=Money(5000)))
```

For async handlers:

```python
class AsyncEventBus:
    def __init__(self) -> None:
        self._handlers: dict[type, list[Callable]] = defaultdict(list)

    def subscribe(self, event_type: type, handler: Callable) -> None:
        self._handlers[event_type].append(handler)

    async def publish(self, event: Any) -> None:
        handlers = self._handlers.get(type(event), [])
        await asyncio.gather(*(h(event) for h in handlers))
```

## Decorator Pattern

Use Python's native decorators for cross-cutting concerns.

```python
import functools
import logging
import time

logger = logging.getLogger(__name__)


def log_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("Calling %s", func.__name__)
        result = func(*args, **kwargs)
        logger.info("Completed %s", func.__name__)
        return result
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay * attempt)
        return wrapper
    return decorator


def cache_result(ttl_seconds: int = 300):
    def decorator(func):
        _cache: dict[str, tuple[float, Any]] = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{args}:{kwargs}"
            if key in _cache:
                cached_at, value = _cache[key]
                if time.time() - cached_at < ttl_seconds:
                    return value
            result = func(*args, **kwargs)
            _cache[key] = (time.time(), result)
            return result
        return wrapper
    return decorator
```

## When to Use Each Pattern

| Situation               | Pattern    | Python Approach                 |
| ----------------------- | ---------- | ------------------------------- |
| Decouple persistence    | Repository | `Protocol` + implementation     |
| Complex object creation | Factory    | Classmethod or function         |
| Swappable algorithms    | Strategy   | `Protocol` or `Callable`        |
| Event-driven decoupling | Observer   | Event bus with handler registry |
| Cross-cutting concerns  | Decorator  | Python `@decorator`             |
| Simplified interface    | Facade     | Module-level functions          |
| State machines          | State      | `StrEnum` + match/case          |
