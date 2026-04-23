# SDD

Use when work needs system design doc before or during implementation.

## When to Use

- feature spans several modules or layers
- rollout has meaningful sequencing or migration risk
- several impl options exist and trade-offs matter
- team needs one design artifact to align on boundaries

## Design Workflow

1. describe problem and constraints first
2. capture current state and change trigger
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

Every useful SDD makes decision visible:

- what options considered
- why chosen one fits constraints
- what cost, complexity, or risk accepted
- what future path stays open or closes because of choice

## Boundary Checklist

Spell out boundaries concretely:

- which modules or layers change
- which interfaces or contracts added or modified
- where data crosses trust or ownership boundaries
- what remains explicitly out of scope

## Rollout and Validation

Prefer incremental rollout over one-shot cutovers.

- phase change when possible
- include migration or compatibility notes
- define how each phase validated
- define rollback or containment plan for risky changes

## Rules

- write problem and constraints before solution
- prefer concrete boundaries and file-level impact over vague architecture prose
- call out trade-offs explicitly
- keep rollout incremental and verifiable
- document why one option chosen over nearby alternatives
- make risk and validation as explicit as design itself

## Good Outputs

- clear dep direction
- explicit ownership of responsibilities
- migration or rollout steps validated independently
- enough detail to guide impl without becoming line-by-line spec

## Anti-Patterns

- writing architecture prose without naming decision
- documenting only chosen option and hiding alternatives
- treating SDD like speculative future roadmap
- skipping rollout and validation because design "seems obvious"
- turning SDD into impl notes that will instantly drift