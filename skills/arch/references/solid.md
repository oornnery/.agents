# SOLID

Use when code hard to extend, test, or overloaded w/ responsibilities.

## S -- Single Responsibility Principle

Module/class: one reason to change.

Heuristics:

- described w/ "and" = does too much
- split validation, persistence, notifications, orchestration when they drift apart
- prefer small focused modules over service objects that absorb everything

## O -- Open/Closed Principle

Prefer extension over repeated edits to stable code paths.

Good fits:

- strategy objects
- plugins
- registries
- dependency injection

Use when new behavior keeps arriving as another `if/elif` branch.

## L -- Liskov Substitution Principle

Substitutable implementations must preserve contract.

Watch for:

- subclasses raising `NotImplementedError`
- narrower parameter expectations than base contract
- incompatible return values or side effects

Use protocols and tests to verify substitutability.

## I -- Interface Segregation Principle

Clients depend only on methods they use.

Prefer:

- small `Protocol` interfaces
- narrow read/write/search boundaries
- composing interfaces over one large umbrella interface

## D -- Dependency Inversion Principle

High-level modules depend on abstractions, not low-level implementations.

Practical defaults:

- define interfaces at boundary
- inject adapters instead of instantiating deep in code
- wire implementations at composition root

## Python-Friendly Defaults

- use `Protocol` for structural interfaces
- prefer composition over inheritance-heavy hierarchies
- favor functions/small classes over elaborate abstract class trees
- add abstractions only when duplication or volatility justifies them

## When to Use

- refactoring "god classes"
- breaking tight coupling
- making code easier to test
- clarifying extension points

## When Not to Use

- tiny modules w/ no real abstraction pressure
- one-off code where extra interfaces add ceremony w/o value
- cases where duplication still cheaper than premature abstraction