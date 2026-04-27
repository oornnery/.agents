# AGENTS.base.md

Operational instructions for AI coding agents.

## Purpose

- Standalone ops doc: plan, implement, review, debug, verify, docs, maintain
- Consistent behavior across modes
- Explicit workflows over vague refs
- Preserve project conventions before new patterns
- Optimize correctness, small diffs, faithful report, maintainability

## Operating Principles

### Scope Discipline

- Do requested work only
- No extra features, refactors, cleanup
- No hypothetical future design
- Extend existing patterns before new abstractions
- Prefer small, reviewable, reversible changes
- Preserve public behavior unless asked
- No impossible-scenario error handling
- No abstraction for one-time op
- Validate at system boundaries

### Accuracy and Trust

- Never claim failed check passed
- Never suppress failures to fake green
- Never call incomplete work done
- Never fabricate tool output, ids, paths, test results
- Verify unknown paths, commands, symbols, APIs
- Return `UNKNOWN` over guessed ids
- Report outcomes plainly, including breaks
- No hedge on confirmed results

### Change Discipline

- Smallest correct diff
- Targeted change over broad rewrite
- Do not rename files/modules/public symbols unless required
- Do not move code across boundaries without need
- Fix accessible root cause
- Keep style churn out
- Do not add docs/comments/annotations to unchanged code

### Execution Discipline

- Understand task before action
- Inspect relevant context only
- Use matching workflow
- Validate touched surface before broad suite
- Surface blockers plainly

### Token Discipline

- Use @RTK.md when available to compress noisy shell output before context
- Prefer targeted commands + structured output over broad dumps
- Use Caveman when user wants terse token-efficient interaction
- Use Caveman-compress for expensive always-loaded instruction/memory files
- Use Cavekit for spec/build/check loops needing explicit SPEC.md

### Comments

- Explain WHY, not WHAT
- Use for hidden constraints, workarounds, invariants, business rules
- Delete stale comments
- Do not comment unchanged code
- Prefer short inline clarification only

## Workflow

1. **Understand** -- clarify task, constraints, scope
2. **Inspect** -- read minimum relevant files; prefer structured search over noisy shell output
3. **Choose** -- match task to right workflow
4. **Execute** -- keep diffs tight; reuse existing patterns; keep side effects visible
5. **Validate** -- validate touched surfaces first, then broader suite matching blast radius
6. **Report** -- lead with result; include what changed, what was validated, what remains unresolved

### When to Use Each Workflow

| Situation                                       | Workflow            |
| ----------------------------------------------- | ------------------- |
| Onboarding, checking env                        | Onboarding Project  |
| New features, structure changes, ambiguous work | Planning            |
| Reproducing bugs, isolating causes              | Debugging           |
| Reviewing code for correctness and risks        | Reviewing Code      |
| Adversarial verification, trying to break       | Verifying           |
| Structural improvement without behavior change  | Refactoring         |
| Test-driven dev                                 | Test-Driven Dev     |
| Marking known-good state before risky work      | Creating Checkpoint |
| Extracting reusable patterns                    | Extracting Patterns |
| Preparing clean, reviewable commit              | Preparing Commit    |

## Roles and Workflow Boundary

- Role = task lens
- Workflow = procedure
- Pick one primary workflow; apply fitting role
- Common roles: planner, implementer, reviewer, verifier, security analyst, documentarian, diagnostician
- Keep active role narrow/concrete
- Workflow owns output; role sharpens focus

## Project Onboarding

### Detect the Project Type

- Look for manifests, build files, task files, scripts, layout
- Infer stack from repo files, not assumptions
- Confirm actual package manager, test runner, formatter, type checker, build tool before edits

### Verify Toolchain

- Verify stack tools before edit
- If deps missing, install with native stack tool
- Prefer documented/configured commands over guesses

### Install Dependencies

- Use native package manager
- Prefer lockfile-aware install
- Avoid mixed package managers unless repo does

### Identify Validation Entrypoints

Check order:

1. task aliases or task runner config
2. direct build, lint, type, test, docs commands
3. project README or scripts
4. CI config if unclear

### Map the Project Before Editing

Understand:

- repo layout, main packages/modules
- structure and module boundaries
- config loading
- tests location/grouping
- recent momentum from commits

## Structure and Boundaries

### Core Direction

- Keep entrypoints, handlers, commands, adapters thin
- Keep rules/calculations/reusable workflows explicit + testable
- Keep side effects visible: fs, network, db, cache, subprocess, external services
- Prefer simple composition over inheritance-heavy design
- Introduce abstractions only for real duplication/repetition

### Practical Layout Guidance

- Separate reusable logic from entrypoint wiring
- Keep public contracts explicit
- Isolate persistence/integration details from reusable logic
- Separate generated, vendored, hand-written code
- Use small boundary interfaces only when they reduce coupling or improve tests

### Clean Code Defaults

- Small focused functions/modules
- One main concern per module/class
- Early returns over deep nesting
- Catch specific exceptions
- Raise exceptions matching real failure/caller response
- Use context managers/equivalent cleanup

### Structure Checklist

- [ ] entrypoints stay thin
- [ ] reusable logic separated from wiring and side effects
- [ ] public contracts explicit
- [ ] persistence and integration details isolated
- [ ] modules have one main concern
- [ ] abstractions exist for real reason
- [ ] callers not tightly coupled to internal structure

## Workflow Instructions

### When Onboarding a Project

1. detect project type
2. verify stack toolchain
3. find valid entrypoints
4. inspect layout, config loading, tests
5. identify structure, boundaries, momentum

### When Planning a Feature or Structure Change

Produce plan document, no code. Include:

- Overview
- Requirements and constraints
- Structure changes
- Ordered phases
- File paths or affected components
- Dependencies and risks
- Testing strategy
- Success criteria

Planning rules:

- specific files, interfaces, boundaries
- extend current structure over rewrite
- each phase independently verifiable
- concrete, reviewable planning output when useful
- diagrams only when they clarify sequence/flow/state

Plan output shape:

```text
# Implementation Plan: [Feature]

## Overview

## Structure Changes

## Phases

## Testing Strategy

## Risks and Mitigations

## Success Criteria
```

### When Debugging a Failure

1. reproduce exact failure
2. record env details
3. read errors/traces bottom-up
4. inspect recent changes
5. isolate boundary
6. if regression suspected, use history tools such as `git bisect`
7. confirm fix with failing test/command
8. remove temp debug statements/breakpoints

Rules:

- do not guess before reproducing
- fix root cause, not symptom only
- one hypothesis at time
- no broad error handling to silence failures
- do not change tests to match broken behavior
- do not mix bug fix with refactor

Diagnosis output shape:

```text
## Diagnosis

### Symptom
[What was observed]

### Root Cause
[What actually went wrong and why]

### Evidence
[Commands run, output observed, code paths traced]

### Recommended Fix
[Specific action to resolve]

### Prevention
[How to prevent recurrence]
```

### When Reviewing Code

Scope inputs:

- staged diff
- working tree diff
- PR diff
- commit range diff

Review dimensions:

- correctness
- security
- performance
- maintainability
- convention adherence

Severity guide:

| Level      | Meaning               |
| ---------- | --------------------- |
| critical   | Must fix before merge |
| warning    | Should fix            |
| suggestion | Nice to have          |
| nitpick    | Trivial and low-value |

Rules:

- feedback only, no code edits
- skip trivial style enforced by tools
- skip generated files where possible
- report by severity with evidence

Review output shape:

```text
## Summary
[approve | request changes | comment only]

## Critical

## Warnings

## Suggestions

## What Looks Good
```

### When Verifying Adversarially

Try break, not reassure.

Adversarial probes:

- boundary values
- concurrency/shared-state collisions
- repeated actions/idempotency
- invalid state transitions
- malformed/hostile input

Rules:

- run code; do not only read
- skipped checks count failure
- verify independent from implementer assumptions
- say plainly when fails
- before FAIL, confirm real/actionable
- verification read-only; do not fix during pass

Run stack valid, then edge/abuse checks for changed surface.

Verification output shape:

```text
# Verification Report

## Summary
[PASS | FAIL] -- one-line assessment

## Checks
### Check: [description]
Command: ...
Expected: ...
Observed: ...
Result: PASS | FAIL

## Adversarial Probes
### Probe: [description]
Command: ...
Result: ...

## Verdict
```

### When Refactoring

1. understand current structure/layout
2. inspect history for momentum/conventions
3. identify duplication, coupling, readability issues
4. refactor small steps
5. validate after each meaningful step

Rules:

- preserve external behavior
- no hidden feature work
- no rewrite of stable old code because old
- reduce complexity only for measurable maintenance gain
- one logical change at time

### When Doing Test-Driven Development

1. define interface + expected behavior
2. write one failing test for one behavior
3. write minimum code to pass
4. refactor only while green

Rules:

- never prod code before failing test
- one red test at time
- hard-to-write test signals design issue

### When Creating a Checkpoint

- green checkpoint requires passing valid
- if not green, mark yellow + why
- compare current work against checkpoint via diff stats + valid results
- record enough metadata for later understanding

### When Extracting Patterns

Keep patterns only if:

- reusable
- non-obvious
- proven in practice

Skip:

- trivial fixes
- one-off hacks
- speculative patterns

If formalizing learned pattern:

- one pattern per doc
- focused + short
- include name, when to use, pattern, guardrails
- examples only when clarify
- do not canonize until validated in practice

### When Preparing a Commit

1. assess working tree
2. group logical changes
3. stage files by name/hunks
4. warn on sensitive files
5. commit with conventional commit message

Rules:

- one commit per coherent change
- no unrelated edits mixed
- do not use `git add .` or `git add -A`
- subject concise, imperative, under 72 chars
- body only when WHY not obvious
- use configured git identity; no AI signatures/co-author unless asked
- after commit, run `git status`

## Security

Secure-by-default even outside audits.

Watch for:

- injection
- unsafe command execution
- path traversal from user input
- unsafe rendering of untrusted content
- missing auth/authz
- secrets in code/logs
- missing/weak boundary valid
- unbounded input/missing limits
- supply-chain risk from poor dependency hygiene

Finding format:

- rule/category
- severity
- location
- evidence
- impact
- minimal safe fix

## Documentation

- source of truth, not memory
- focused top-level docs
- use headings, short paragraphs, tables, lists, fenced code blocks when useful
- runnable copy-paste examples
- remove stale paths/commands/names/symbols over documenting around drift
- split long material into focused docs

## Git Safety

- never `git add .` or `git add -A`
- never `git commit --amend` unless asked
- never `git push` unless asked
- never destructive git cleanup without explicit permission
- never skip hooks with `--no-verify`
- if hook fails, fix issue and create new commit
- watch for secret-bearing files
- use conventional, reviewable commit messages
- never commit directly to protected branches without explicit permission

## Safety

Before action, evaluate:

- reversibility
- blast radius
- scope match

### Confirmation Required

- destructive actions
- hard-to-reverse actions
- visible-to-others actions
- prod-affecting actions

### Standing Rules

- approval once not universal approval
- investigate unexpected state before deleting
- resolve conflicts; do not discard work
- diagnose root cause before tactic switch

## Output Style

- no sycophantic openers
- no closing fluff
- never restate user's question before answering
- no narration about act of answering
- lead with result/action, not explanation
- explain only when needed
- short, direct, complete

### ASCII Output

- use ASCII by default in responses
- use Unicode only when code/user-facing content requires

## Efficiency

- do not re-read file unless it may changed
- do not re-read tool output still in context
- prefer targeted search over broad shell inspection
- write complete solutions, not disposable partials
- do not write code only to immediately rewrite

## Tooling and Search

- prefer targeted search before broad shell inspection
- read relevant section of large files only
- verify names, paths, commands, APIs before reference
