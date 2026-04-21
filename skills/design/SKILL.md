---
name: design
description: Design guidance for APIs, user interfaces, and BFF boundaries. Load when shaping external contracts, response models, component systems, accessibility, or frontend/backend boundaries.
---

# Design

Use this skill when the main question is how the system should present itself to
clients or users.

## When to Load Each Reference

| Situation                                   | Read                                        |
| ------------------------------------------- | ------------------------------------------- |
| routes, contracts, errors, pagination       | `references/api.md`                         |
| tokens, components, states, accessibility   | `references/ui.md`                          |
| frontend-specific aggregation and reshaping | `references/bff.md`                         |
| both surface types matter                   | read the dominant one first, then the other |

## Workflow

1. decide whether the problem is API-facing, UI-facing, or both
2. define the contract before implementation details
3. keep naming, states, and failure behavior explicit
4. add a BFF only if the frontend really needs aggregation or reshaping
5. prefer stable patterns over clever shortcuts
6. keep the surface consistent across related endpoints or components

## Shared Rules

- design the happy path and failure path together
- keep APIs and components predictable before making them flexible
- add complexity only when the real use case demands it
