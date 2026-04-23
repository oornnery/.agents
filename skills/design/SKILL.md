---
name: design
description: Design guidance for APIs, user interfaces, and BFF boundaries. Load when shaping external contracts, response models, component systems, accessibility, or frontend/backend boundaries.
---

# Design

Use skill when main question = how system presents to clients/users.

## When to Load Each Reference

| Situation                                   | Read                                        |
| ------------------------------------------- | ------------------------------------------- |
| routes, contracts, errors, pagination       | `references/api.md`                         |
| tokens, components, states, accessibility   | `references/ui.md`                          |
| frontend-specific aggregation and reshaping | `references/bff.md`                         |
| both surface types matter                   | read the dominant one first, then the other |

## Workflow

1. decide whether problem is API-facing, UI-facing, or both
2. define contract before implementation details
3. keep naming, states, failure behavior explicit
4. add BFF only if frontend needs aggregation/reshaping
5. prefer stable patterns over clever shortcuts
6. keep surface consistent across related endpoints/components

## Shared Rules

- design happy path + failure path together
- keep APIs/components predictable before flexible
- add complexity only when real use case demands