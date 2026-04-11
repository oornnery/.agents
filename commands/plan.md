---
name: plan
description: Create structured planning documents (SDD, SPEC, ARCH) for a feature or project. Use when the user asks to plan, design, architect, spec out, or create a design document before implementation.
---

# Plan

Create structured planning documents following Spec-Driven Development
(SDD) methodology. Specifications are the source of truth -- code serves
the specification.

**Agent routing:** For complex planning tasks requiring deep reasoning,
invoke `agents/planner.md` (model: opus). The agent produces SPEC/ARCH/SDD
artifacts following this methodology.

## Process

### Phase 1: Requirements Gathering

Understand what needs to be built:

1. Ask the user for the goal, scope, and constraints.
2. Identify stakeholders, users, and key use cases.
3. List functional and non-functional requirements.
4. Identify dependencies (internal and external).
5. Define acceptance criteria — measurable, testable outcomes.

### Phase 2: Architecture Design

Design the system architecture:

1. Choose the architecture pattern (layered, hexagonal, MVC, microservices).
   See `skills/architecture/SKILL.md` for DDD, Clean Architecture, and Onion patterns.
2. Define components and their responsibilities.
3. Map data flow between components.
4. Define API contracts (routes, types, payloads).
   See `skills/api-design/SKILL.md` for REST conventions and BFF patterns.
5. Choose technology stack and justify decisions.
6. Identify integration points and external services.
7. Write ADRs for significant decisions (database, framework, patterns).
   See `skills/documentation/SKILL.md` for ADR template.

Produce a **Mermaid architecture diagram** (see examples below).

### Phase 3: Module Design

Break down into implementable modules:

1. Define each module's interface (inputs, outputs, side effects).
2. Map dependencies between modules.
3. Design data models (entities, DTOs, events).
4. Define API routes with types:

```text
POST /api/users          -> CreateUserRequest  -> UserResponse (201)
GET  /api/users/:id      -> PathParam(id: str) -> UserResponse (200)
PUT  /api/users/:id      -> UpdateUserRequest  -> UserResponse (200)
DELETE /api/users/:id    -> PathParam(id: str) -> None (204)
```

5. If frontend exists, design the UI in ASCII or describe components.

### Phase 4: Create Documents

Generate the planning artifacts as Markdown files.

## Output Artifacts

### SPEC.md -- Requirements Specification

Structure: Overview, Requirements (Functional/Non-Functional), User Flows,
Acceptance Criteria (BDD format: Given/When/Then), Edge Cases, Dependencies.

### ARCH.md -- Architecture Document

Structure: System Context, ADRs, Component Diagram (Mermaid),
Data Models, API Design (routes + types), Sequence Diagram,
Security Considerations, Infrastructure.

### SDD.md -- Software Design Document

Structure: Foundation (principles), Specification, Architecture,
Implementation Plan (ordered tasks), Test Strategy, Design Principles.

## Mermaid Diagrams

Use Mermaid for all visual documentation: `graph`/`flowchart` for architecture,
`sequenceDiagram` for API flows, `erDiagram` for schema, `classDiagram` for
domain models, `stateDiagram` for workflows.

## Frontend Planning

When planning frontend components, include ASCII wireframes and component trees.

## What NOT to Do

- **Do not implement during planning.** Planning produces documents, not code.
- **Do not over-specify.** Leave room for implementation decisions.
- **Do not skip diagrams.** Visual representations catch design issues early.
- **Do not plan alone.** Validate assumptions with the user at each phase.

### DDD Considerations

If the project uses Domain-Driven Design:

1. Identify **bounded contexts** — separate domains with their own models.
2. Define **aggregates** — consistency boundaries for data changes.
3. Map **domain events** — what happens when state changes.
4. Design **repository interfaces** — data access abstraction.
5. Separate **application services** (orchestration) from **domain services**
   (business logic).

See `skills/architecture/references/ddd.md` for detailed examples.

## Checklist

Before finishing a plan, verify:

- [ ] All requirements have acceptance criteria (BDD format preferred)
- [ ] Architecture diagram exists
- [ ] API routes defined with types
- [ ] Data models specified
- [ ] Dependencies identified
- [ ] Edge cases listed
- [ ] Test strategy outlined (TDD where applicable)
- [ ] Security considerations addressed
- [ ] ADRs written for key decisions

## Related

- `skills/architecture/SKILL.md` — DDD, Clean Architecture, SOLID
- `skills/api-design/SKILL.md` — API design patterns
- `skills/tdd/SKILL.md` — test-first workflow
- `skills/documentation/SKILL.md` — ADR templates and documentation
