# DDD

Use this reference when the problem is not just persistence or transport, but
the business model itself.

## Core Concepts

| Concept             | Meaning                                              |
| ------------------- | ---------------------------------------------------- |
| Entity              | object with identity across state changes            |
| Value Object        | immutable object defined by attributes, not identity |
| Aggregate           | consistency boundary with a root entity              |
| Repository          | persistence boundary for aggregate roots             |
| Domain Service      | domain behavior that does not belong to one entity   |
| Application Service | orchestration layer around domain behavior           |
| Domain Event        | immutable fact that something happened               |
| Bounded Context     | model boundary where words have a specific meaning   |

## Modeling Rules

- keep domain code free of framework and persistence concerns
- put invariants where they belong: entities and value objects protect themselves
- use aggregates as transaction boundaries
- expose repositories only for aggregate roots
- publish domain events for important facts; handle side effects outside the domain
- keep application services thin and orchestration-focused

## Entities

- have identity
- can mutate while preserving invariants
- should own behavior, not just fields

Use entities when the lifecycle and identity matter.

## Value Objects

- compare by value
- are immutable by default
- are ideal for money, addresses, ranges, and similar concepts

Use value objects to make domain concepts explicit and safe.

## Aggregates

All external access goes through the aggregate root.

Rules:

- one aggregate per transaction unless there is a strong reason otherwise
- inner entities should not be mutated freely from outside
- use the root to enforce consistency

## Repositories

- defined by the domain or application boundary
- implemented in infrastructure
- return domain objects, not ORM models
- hide persistence details from callers

## Domain vs Application Services

Use a **domain service** when:

- the logic belongs to the domain
- it involves multiple entities or value objects
- it is still pure business behavior

Use an **application service** when:

- orchestrating a use case
- loading and saving aggregates
- handling transactions
- publishing events
- coordinating external side effects

## Bounded Contexts

Different parts of the system may model the same word differently.

Use bounded contexts when:

- one shared model keeps becoming ambiguous
- different teams or workflows need different rules
- integration between domains should happen through translation, not shared objects

## When to Use

- rich business rules
- non-trivial workflows and state transitions
- language in the business domain matters
- correctness depends on invariants and clear boundaries

## Anti-Patterns

- anemic domain models with all logic in services
- shared models across unrelated contexts
- repositories for every tiny entity instead of aggregate roots
- letting application services absorb business rules
- leaking ORM concerns into the domain
