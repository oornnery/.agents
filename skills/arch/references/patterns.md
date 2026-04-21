# Patterns

Use this reference when you know you need a pattern, but want the lightest
shape that actually fits the problem.

## Selection Guide

| Situation                             | Pattern              | Default Shape                     |
| ------------------------------------- | -------------------- | --------------------------------- |
| decouple domain from persistence      | Repository           | `Protocol` plus implementation    |
| centralize object creation            | Factory              | classmethod or function           |
| swap algorithms at runtime            | Strategy             | `Protocol` or callable            |
| notify multiple consumers of an event | Observer / Event Bus | handler registry                  |
| wrap cross-cutting behavior           | Decorator            | Python decorator with `@wraps`    |
| expose a simpler subsystem interface  | Facade               | module-level helper or thin layer |
| model explicit state transitions      | State                | enum plus transition methods      |

## Pattern Workflow

1. name the problem before naming the pattern
2. choose the lightest shape that solves that problem
3. keep the boundary explicit
4. verify the pattern reduced duplication, coupling, or branching
5. stop if the pattern adds indirection without paying rent

## Repository

Use when business logic should not know about the database or storage engine.

- define the contract as a protocol
- keep implementations in infrastructure
- return domain objects or DTOs, not storage-specific models
- do not let repository APIs become ORM-shaped by accident

## Factory

Use when object creation has variants or configuration branching.

- start with a function or classmethod
- avoid abstract factories unless the creation problem is genuinely large
- keep creation logic together instead of leaking it across call sites

## Strategy

Use when behavior changes based on policy, provider, or algorithm choice.

- start with a protocol or callable
- inject the strategy instead of branching repeatedly in one function
- prefer a small stable contract over large class hierarchies

## Observer / Event Bus

Use when producers should not know all consumers.

- keep handlers explicit
- avoid hidden global event systems unless the project already standardizes on one
- use async fan-out only when concurrency is truly needed
- make failure and retry behavior explicit; silent event loss is a design bug

## Decorator

Use for cross-cutting concerns such as retries, logging, metrics, caching, or
authorization checks.

- always use `@wraps`
- keep decorators narrow and predictable
- avoid stacking many decorators when one explicit helper would be clearer
- prefer decorators for behavior that is truly cross-cutting, not for hiding core logic

## Facade

Use when a subsystem is noisy and callers need a stable simplified API.

- prefer a thin function or service wrapper
- do not hide important behavior or side effects behind a vague facade
- the facade should simplify; it should not become another god object

## State

Use when transitions matter more than raw flags.

- model states explicitly with enums
- keep valid transitions close to the stateful object
- reject impossible transitions early
- if transitions are not real, raw flags may still be simpler

## Testing Patterns

Validate the seam the pattern was supposed to create:

- Repository: test domain-facing contract separately from persistence adapter
- Strategy: test each implementation against the same expected behavior
- Decorator: test that the wrapper preserves the wrapped contract
- State: test valid and invalid transitions explicitly
- Observer: test ordering, fan-out, and failure handling where it matters

## Pattern Smells

- the pattern name sounds right, but the problem is still vague
- every new use case needs another layer of abstraction
- call sites become harder to read than before
- mocking the pattern is easier than understanding the code it wraps
- the pattern exists mainly to imitate a framework or a book example

## Pattern Rules

- start with the lightest implementation that solves the problem
- do not introduce a pattern only because the name sounds correct
- prefer explicitness over framework-heavy magic
- if a pattern increases indirection without reducing risk or duplication, stop
