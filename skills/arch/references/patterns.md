# Patterns

Use when need pattern, want lightest shape fitting problem.

## Selection Guide

| Situation | Pattern | Default Shape |
| --- | --- | --- |
| decouple domain from persistence | Repository | `Protocol` plus implementation |
| centralize object creation | Factory | classmethod or function |
| swap algorithms at runtime | Strategy | `Protocol` or callable |
| notify multiple consumers of event | Observer / Event Bus | handler registry |
| wrap cross-cutting behavior | Decorator | Python decorator with `@wraps` |
| expose simpler subsystem interface | Facade | module-level helper or thin layer |
| model explicit state transitions | State | enum plus transition methods |

## Pattern Workflow

1. name problem before naming pattern
2. choose lightest shape solving that problem
3. keep boundary explicit
4. verify pattern reduced duplication, coupling, or branching
5. stop if pattern adds indirection without paying rent

## Repository

Use when business logic should not know about database or storage engine.

- define contract as protocol
- keep implementations in infrastructure
- return domain objects or DTOs, not storage-specific models
- do not let repository APIs become ORM-shaped by accident

## Factory

Use when object creation has variants or configuration branching.

- start with function or classmethod
- avoid abstract factories unless creation problem genuinely large
- keep creation logic together instead of leaking across call sites

## Strategy

Use when behavior changes based on policy, provider, or algorithm choice.

- start with protocol or callable
- inject strategy instead of branching repeatedly in one function
- prefer small stable contract over large class hierarchies

## Observer / Event Bus

Use when producers should not know all consumers.

- keep handlers explicit
- avoid hidden global event systems unless project already standardizes on one
- use async fan-out only when concurrency truly needed
- make failure and retry behavior explicit; silent event loss is design bug

## Decorator

Use for cross-cutting concerns: retries, logging, metrics, caching, authorization checks.

- always use `@wraps`
- keep decorators narrow and predictable
- avoid stacking many decorators when one explicit helper would be clearer
- prefer decorators for truly cross-cutting behavior, not hiding core logic

## Facade

Use when subsystem is noisy and callers need stable simplified API.

- prefer thin function or service wrapper
- do not hide important behavior or side effects behind vague facade
- facade should simplify; it should not become another god object

## State

Use when transitions matter more than raw flags.

- model states explicitly with enums
- keep valid transitions close to stateful object
- reject impossible transitions early
- if transitions not real, raw flags may still be simpler

## Testing Patterns

Validate seam pattern was supposed to create:

- Repository: test domain-facing contract separately from persistence adapter
- Strategy: test each implementation against same expected behavior
- Decorator: test wrapper preserves wrapped contract
- State: test valid and invalid transitions explicitly
- Observer: test ordering, fan-out, and failure handling where it matters

## Pattern Smells

- pattern name sounds right, but problem still vague
- every new use case needs another abstraction layer
- call sites harder to read than before
- mocking pattern easier than understanding code it wraps
- pattern exists mainly to imitate framework or book example

## Pattern Rules

- start with lightest implementation solving problem
- do not introduce pattern only because name sounds correct
- prefer explicitness over framework-heavy magic
- if pattern increases indirection without reducing risk or duplication, stop