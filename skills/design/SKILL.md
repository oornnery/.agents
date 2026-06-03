---
name: design
description: Design guidance for APIs, user interfaces, and BFF boundaries. Load when shaping external contracts, response models, component systems, accessibility, or frontend/backend boundaries.
---

# Design

Use skill when main question = how system presents to clients/users.

## When to Load Each Reference

| Situation                                   | Read                                |
| ------------------------------------------- | ----------------------------------- |
| routes, contracts, errors, pagination       | `references/api.md`                 |
| tokens, components, states, accessibility   | `references/ui.md`                  |
| frontend-specific aggregation and reshaping | `references/bff.md`                 |
| both surface types matter                   | read dominant one first, then other |

## Workflow

1. decide whether problem is API-facing, UI-facing, or both
2. define contract before impl details
3. keep naming, states, failure behavior explicit
4. add BFF only if frontend needs aggregation/reshaping
5. prefer stable patterns over clever shortcuts
6. update `DESIGN.md` when API, UI, BFF, or product/design decisions need to persist
7. keep surface consistent across related endpoints/components

## Shared Rules

- design happy path + failure path together
- keep APIs/components predictable before flexible
- add complexity only when real use case demands
- durable design decisions belong in `DESIGN.md`; short active notes belong in `.spec/state.md`
