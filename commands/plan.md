---
name: plan
description: Create a structured implementation plan or design document. Use when the user wants a SPEC, ARCH, or SDD before implementation.
---

# Plan

Produce a plan document, not code. The plan should make implementation,
testing, and rollout concrete without over-specifying the code.

## When to use

Use this command for:

- new features with multiple moving parts
- architecture or layering decisions
- ambiguous requests that need phased execution
- work that benefits from SPEC, ARCH, or SDD output

## Process

### 1. Clarify the request

Identify:

- goal and scope
- explicit constraints
- non-goals
- affected users or systems
- success criteria

### 2. Inspect the current system

Read only enough to answer:

- what architecture is already in use
- which files or modules are likely affected
- where boundaries already exist
- what validations and tests will prove success

Load supporting skills only when needed:

- `skills/arch/SKILL.md` for DDD, Clean Arch, SOLID, patterns, and SDD
- `skills/design/SKILL.md` for API, UI, or BFF surface work
- `skills/python/SKILL.md` for implementation and toolchain constraints
- `skills/quality/SKILL.md` for TDD or regression strategy
- `skills/security/SKILL.md` for trust boundaries and risk
- `skills/docs/SKILL.md` for ADR or design-doc formatting

### 3. Design the change

Define:

- architecture changes
- boundaries and interfaces
- ordered phases
- data flow or request flow
- risks and mitigations
- testing strategy

Use diagrams only when they add clarity.

### 4. Write the plan

Use this shape:

```text
# Implementation Plan: [Feature]

## Overview

## Architecture Changes

## Phases

## Testing Strategy

## Risks and Mitigations

## Success Criteria
```

### 5. Keep it implementation-ready

Each phase should be independently verifiable and specific about:

- file paths or affected components
- contracts or interfaces
- migration or rollout concerns
- how to validate completion

## Constraints

- do not implement during planning
- prefer extending current architecture over rewriting it
- do not hide uncertainty; surface assumptions and risks
- avoid speculative abstractions
