# DDD in Python — Detailed Guide

## Entities

Objects with identity. Two entities with the same attributes are different
if they have different IDs.

```python
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass
class User:
    name: str
    email: str
    id: str = field(default_factory=lambda: uuid4().hex)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True

    def deactivate(self) -> None:
        self.is_active = False

    def change_email(self, new_email: str) -> None:
        if not new_email or "@" not in new_email:
            raise ValueError(f"Invalid email: {new_email}")
        self.email = new_email
```

Entities encapsulate their own invariants. Validation lives in the entity,
not in the service.

## Value Objects

Immutable, no identity. Compared by value.

```python
@dataclass(frozen=True, slots=True)
class Money:
    amount: int  # cents to avoid floating point
    currency: str = "BRL"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(amount=self.amount + other.amount, currency=self.currency)


@dataclass(frozen=True, slots=True)
class Address:
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "BR"
```

Use `frozen=True` for value objects — they should never be mutated.

## Aggregates

A cluster of entities and value objects with a root entity. All external
access goes through the root.

```python
@dataclass
class Order:
    customer_id: str
    items: list["OrderItem"] = field(default_factory=list)
    id: str = field(default_factory=lambda: uuid4().hex)
    status: str = "pending"

    @property
    def total(self) -> Money:
        amounts = [item.subtotal for item in self.items]
        result = Money(0)
        for amount in amounts:
            result = result.add(amount)
        return result

    def add_item(self, product_id: str, quantity: int, unit_price: Money) -> None:
        if self.status != "pending":
            raise ValueError("Cannot modify a non-pending order")
        existing = next((i for i in self.items if i.product_id == product_id), None)
        if existing:
            existing.quantity += quantity
        else:
            self.items.append(OrderItem(product_id=product_id, quantity=quantity, unit_price=unit_price))

    def place(self) -> "OrderPlaced":
        if not self.items:
            raise ValueError("Cannot place an empty order")
        self.status = "placed"
        return OrderPlaced(order_id=self.id, total=self.total)


@dataclass
class OrderItem:
    product_id: str
    quantity: int
    unit_price: Money

    @property
    def subtotal(self) -> Money:
        return Money(amount=self.unit_price.amount * self.quantity, currency=self.unit_price.currency)
```

**Rules:**

- Only the aggregate root has a repository
- External code cannot hold references to inner entities
- One aggregate per transaction

## Domain Events

Record things that happened in the domain.

```python
@dataclass(frozen=True, slots=True)
class OrderPlaced:
    order_id: str
    total: Money
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
```

Events are immutable facts. They can trigger side effects (send email,
update inventory) in the application layer, not the domain.

## Repository Pattern

The domain defines the interface. Infrastructure implements it.

```python
from typing import Protocol


class OrderRepository(Protocol):
    def get(self, order_id: str) -> Order | None: ...
    def save(self, order: Order) -> None: ...
    def find_by_customer(self, customer_id: str) -> list[Order]: ...
```

```python
# infrastructure/persistence/sql_order_repo.py
class SqlOrderRepository:
    def __init__(self, session: "Session") -> None:
        self.session = session

    def get(self, order_id: str) -> Order | None:
        row = self.session.get(OrderModel, order_id)
        return row.to_domain() if row else None

    def save(self, order: Order) -> None:
        model = OrderModel.from_domain(order)
        self.session.merge(model)
        self.session.commit()

    def find_by_customer(self, customer_id: str) -> list[Order]:
        rows = self.session.query(OrderModel).filter_by(customer_id=customer_id).all()
        return [row.to_domain() for row in rows]
```

## Domain Services

Operations that don't belong to a single entity.

```python
class PricingService:
    def __init__(self, discount_repo: "DiscountRepository") -> None:
        self.discount_repo = discount_repo

    def calculate_final_price(self, order: Order, coupon_code: str | None = None) -> Money:
        total = order.total
        if coupon_code:
            discount = self.discount_repo.get_by_code(coupon_code)
            if discount and discount.is_valid():
                total = discount.apply(total)
        return total
```

## Application Services

Orchestrate use cases. Thin layer between presentation and domain.

```python
class PlaceOrderUseCase:
    def __init__(self, order_repo: OrderRepository, event_bus: "EventBus") -> None:
        self.order_repo = order_repo
        self.event_bus = event_bus

    def execute(self, order_id: str) -> Order:
        order = self.order_repo.get(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        event = order.place()
        self.order_repo.save(order)
        self.event_bus.publish(event)
        return order
```

Application services should:

- Be stateless
- Coordinate domain objects
- Handle transactions
- Publish domain events
- NOT contain business logic

## Bounded Contexts

Different parts of the system may have different models for the same concept.

```text
┌────────────────┐    ┌────────────────┐
│  Sales Context │    │ Shipping Context│
│                │    │                │
│  Order         │    │  Shipment      │
│  - items       │    │  - packages    │
│  - total       │    │  - tracking    │
│  - customer    │    │  - address     │
│                │    │                │
│  Customer      │    │  Recipient     │
│  - email       │    │  - name        │
│  - credit      │    │  - address     │
└────────────────┘    └────────────────┘
```

Contexts communicate through events or an anti-corruption layer, not
by sharing models.
