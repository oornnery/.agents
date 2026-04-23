# DDD

Use when problem is business model itself, not just persistence or transport.

## Core Concepts

| Concept             | Meaning                                              |
| ------------------- | ---------------------------------------------------- |
| Entity              | object with identity across state changes            |
| Value Object        | immutable, defined by attributes not identity         |
| Aggregate           | consistency boundary with root entity                 |
| Repository          | persistence boundary for aggregate roots             |
| Domain Service      | domain behavior not belonging to one entity           |
| Application Service | orchestration layer around domain behavior           |
| Domain Event        | immutable fact that something happened               |
| Bounded Context     | model boundary where words have specific meaning     |

## Modeling Rules

- keep domain code free of framework and persistence concerns
- put invariants where they belong: entities and value objects protect themselves
- use aggregates as transaction boundaries
- expose repositories only for aggregate roots
- publish domain events for important facts; handle side effects outside domain
- keep application services thin and orchestration-focused

## Entities

- have identity
- mutate while preserving invariants
- own behavior, not just fields

Use when lifecycle and identity matter.

## Value Objects

- compare by value
- immutable by default
- ideal for money, addresses, ranges, similar concepts

Use to make domain concepts explicit and safe.

## Aggregates

All external access goes through aggregate root.

Rules:

- one aggregate per transaction unless strong reason otherwise
- inner entities not mutated freely from outside
- use root to enforce consistency

## Repositories

- defined by domain or application boundary
- implemented in infrastructure
- return domain objects, not ORM models
- hide persistence details from callers

## Domain vs Application Services

Use **domain service** when:

- logic belongs to domain
- involves multiple entities or value objects
- still pure business behavior

Use **application service** when:

- orchestrating use case
- loading and saving aggregates
- handling transactions
- publishing events
- coordinating external side effects

## Bounded Contexts

Different parts of system may model same word differently.

Use when:

- one shared model keeps becoming ambiguous
- different teams or workflows need different rules
- integration between domains through translation, not shared objects

## When to Use

- rich business rules
- non-trivial workflows and state transitions
- language in business domain matters
- correctness depends on invariants and clear boundaries

## Anti-Patterns

- anemic domain models with all logic in services
- shared models across unrelated contexts
- repositories for every tiny entity instead of aggregate roots
- application services absorbing business rules
- leaking ORM concerns into domain