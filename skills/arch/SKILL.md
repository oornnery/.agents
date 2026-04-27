---
name: arch
description: Architecture guidance for DDD, Clean Arch, SOLID, common patterns, and system design documents. Load when deciding how to structure modules, layers, boundaries, or design decisions.
---

# Arch

Use when design problem broader than one pattern. Need pick right architectural lens first.

Keep `arch` as single entrypoint. Load only relevant reference file for problem at hand.

## Pick the Right Reference

| If problem is mainly about...              | Read                           |
| ------------------------------------------ | ------------------------------ |
| domain language, invariants, model clarity | `references/ddd.md`            |
| layers, dependency direction, adapters     | `references/clean-arch.md`     |
| responsibilities and abstractions          | `references/solid.md`          |
| recurring impl shapes                      | `references/patterns.md`       |
| system design decisions and rollout shape  | `references/sdd.md`            |
| more than one of above                     | start with one, then read next |

## Shared Rules

- keep business rules explicit and testable
- push IO and framework details to edges
- prefer composition before deep inheritance trees
- add abstractions only when they reduce real duplication or coupling
- choose simplest structure that preserves clarity

## Quick Checks

- domain model getting muddy -> read `references/ddd.md`
- layers leaking into each other -> read `references/clean-arch.md`
- one module doing too much -> read `references/solid.md`
- need repeatable shape for recurring problem -> read `references/patterns.md`
- need capture system design before impl -> read `references/sdd.md`

## Workflow

1. identify dominant architecture problem
2. read only matching reference file
3. apply smallest structure that solves that problem
4. combine references only when design truly spans multiple concerns

## Adjacent Workflows

- use `quality` when want TDD to drive structural changes safely or RCA to diagnose failures around boundaries and design
