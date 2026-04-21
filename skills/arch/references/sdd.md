# SDD

Use this reference when the work needs a system design document before or during
implementation.

## When to Use

- a feature spans several modules or layers
- the rollout has meaningful sequencing or migration risk
- several implementation options exist and the trade-offs matter
- the team needs one design artifact to align on boundaries

## Design Workflow

1. describe the problem and constraints first
2. capture the current state and the change trigger
3. list realistic design options
4. choose one direction with explicit trade-offs
5. define rollout, validation, and fallback

## Core Sections

```markdown
# SDD: {Title}

## Overview

## Goals

## Non-Goals

## Constraints

## Current State

## Proposed Design

## Boundaries and Interfaces

## Risks and Trade-offs

## Rollout Plan

## Validation Strategy
```

## Option Framing

Every useful SDD should make the decision visible:

- what options were considered
- why the chosen one fits the constraints
- what cost, complexity, or risk is being accepted
- what future path stays open or closes because of the choice

## Boundary Checklist

Spell out boundaries concretely:

- which modules or layers change
- which interfaces or contracts are added or modified
- where data crosses trust or ownership boundaries
- what remains explicitly out of scope

## Rollout and Validation

Prefer incremental rollout over one-shot cutovers.

- phase the change when possible
- include migration or compatibility notes
- define how each phase will be validated
- define the rollback or containment plan for risky changes

## Rules

- write the problem and constraints before the solution
- prefer concrete boundaries and file-level impact over vague architecture prose
- call out trade-offs explicitly
- keep the rollout incremental and verifiable
- document why one option was chosen over nearby alternatives
- make risk and validation as explicit as the design itself

## Good Outputs

- clear dependency direction
- explicit ownership of responsibilities
- migration or rollout steps that can be validated independently
- enough detail to guide implementation without becoming a line-by-line spec

## Anti-Patterns

- writing architecture prose without naming the decision
- documenting only the chosen option and hiding alternatives
- treating the SDD like a speculative future roadmap
- skipping rollout and validation because the design "seems obvious"
- turning the SDD into implementation notes that will instantly drift
