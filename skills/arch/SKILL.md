---
name: arch
description: Architecture guidance for DDD, Clean Arch, SOLID, common patterns, and system design documents. Load when deciding how to structure modules, layers, boundaries, or design decisions.
---

# Arch

Use this skill when the design problem is broader than one pattern and you need
to choose the right architectural lens first.

Keep `arch` as the single entrypoint. Load only the relevant reference file for
the problem at hand.

## Pick the Right Reference

| If the problem is mainly about...          | Read                                |
| ------------------------------------------ | ----------------------------------- |
| domain language, invariants, model clarity | `references/ddd.md`                 |
| layers, dependency direction, adapters     | `references/clean-arch.md`          |
| responsibilities and abstractions          | `references/solid.md`               |
| recurring implementation shapes            | `references/patterns.md`            |
| system design decisions and rollout shape  | `references/sdd.md`                 |
| more than one of the above                 | start with one, then read the next  |

## Shared Rules

- keep business rules explicit and testable
- push IO and framework details to the edges
- prefer composition before deep inheritance trees
- add abstractions only when they reduce real duplication or coupling
- choose the simplest structure that preserves clarity

## Quick Checks

- is the domain model getting muddy -> read `references/ddd.md`
- are layers leaking into each other -> read `references/clean-arch.md`
- is one module doing too much -> read `references/solid.md`
- do you need a repeatable shape for a recurring problem -> read `references/patterns.md`
- do you need to capture the system design before implementation -> read `references/sdd.md`

## Workflow

1. identify the dominant architecture problem
2. read only the matching reference file
3. apply the smallest structure that solves that problem
4. combine references only when the design truly spans multiple concerns

## Adjacent Workflows

- use `quality` when you want TDD to drive structural changes safely or RCA to diagnose failures around boundaries and design
