# SOLID

Use this reference when code feels hard to extend, hard to test, or overloaded
with responsibilities.

## S -- Single Responsibility Principle

A module or class should have one reason to change.

Heuristics:

- if you describe it with "and", it probably does too much
- split validation, persistence, notifications, and orchestration when they drift apart
- prefer small focused modules over service objects that absorb everything

## O -- Open/Closed Principle

Prefer extension over repeated edits to stable code paths.

Good fits:

- strategy objects
- plugins
- registries
- dependency injection

Use this when new behavior keeps arriving as another `if/elif` branch.

## L -- Liskov Substitution Principle

Substitutable implementations must preserve the contract.

Watch for:

- subclasses that raise `NotImplementedError`
- narrower parameter expectations than the base contract
- incompatible return values or side effects

Use protocols and tests to verify substitutability.

## I -- Interface Segregation Principle

Clients should depend only on the methods they use.

Prefer:

- small `Protocol` interfaces
- narrow read/write/search boundaries
- composing interfaces instead of one large umbrella interface

## D -- Dependency Inversion Principle

High-level modules depend on abstractions, not low-level implementations.

Practical defaults:

- define interfaces at the boundary
- inject adapters instead of instantiating them deep in the code
- wire implementations at the composition root

## Python-Friendly Defaults

- use `Protocol` for structural interfaces
- prefer composition over inheritance-heavy hierarchies
- favor functions or small classes over elaborate abstract class trees
- add abstractions only when duplication or volatility justifies them

## When to Use

- refactoring "god classes"
- breaking tight coupling
- making code easier to test
- clarifying extension points

## When Not to Use

- tiny modules with no real abstraction pressure
- one-off code where extra interfaces add ceremony without value
- cases where duplication is still cheaper than a premature abstraction
