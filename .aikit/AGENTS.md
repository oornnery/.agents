# AGENTS.md

Operational instructions for AI coding agents.

## Purpose

- Provide standalone instructions for planning, implementation, review, debugging, verification, docs, and maintenance.
- Keep behavior consistent across modes, tools, and model providers.
- Prefer explicit workflows over vague references.
- Preserve project conventions before introducing patterns.
- Optimize for correctness, small diffs, faithful reporting, and maintainability.

## Operating Principles

### Scope Discipline

- Do requested work only.
- Do not add extra features, refactors, cleanup, or hypothetical future design.
- Extend existing patterns before creating new abstractions.
- Prefer small, reviewable, reversible changes.
- Preserve public behavior unless asked to change it.
- Do not add impossible-scenario error handling.
- Do not create abstractions for one-time operations.
- Validate at system boundaries.

### Accuracy and Trust

- Never claim a failed check passed.
- Never suppress failures to fake green.
- Never call incomplete work done.
- Never fabricate tool output, IDs, paths, test results, or command results.
- Verify unknown paths, commands, symbols, APIs, and identifiers before using them.
- Return `UNKNOWN` instead of guessing IDs or facts.
- Report outcomes plainly, including breakage.
- Do not hedge confirmed results.

### Change Discipline

- Make the smallest correct diff.
- Prefer targeted changes over broad rewrites.
- Do not rename files, modules, or public symbols unless required.
- Do not move code across boundaries without need.
- Fix the accessible root cause.
- Keep style churn out of functional changes.
- Do not add docs, comments, or annotations to unchanged code.

### Execution Discipline

- Understand the task before acting.
- Inspect only relevant context.
- Use the workflow matching the task.
- Validate touched surfaces before broad suites.
- Surface blockers plainly.

### Comment Discipline

- Explain WHY, not WHAT.
- Use comments for hidden constraints, workarounds, invariants, and business rules.
- Delete stale comments.
- Do not comment unchanged code.
- Prefer short inline clarification only.

## Core Workflow

1. **Understand** -- clarify task, constraints, and scope.
2. **Inspect** -- read minimum relevant files; prefer structured search over noisy broad output.
3. **Choose** -- match task to the right workflow.
4. **Execute** -- keep diffs tight, reuse existing patterns, keep side effects visible.
5. **Validate** -- validate touched surfaces first, then broader suite matching blast radius.
6. **Report** -- lead with result; include changed files, validation, and unresolved issues.

### Workflow Selection

| Situation                                       | Workflow            |
| ----------------------------------------------- | ------------------- |
| Onboarding, checking env                        | Onboarding Project  |
| New features, structure changes, ambiguous work | Planning            |
| Reproducing bugs, isolating causes              | Debugging           |
| Reviewing code for correctness and risks        | Reviewing Code      |
| Adversarial verification, trying to break       | Verifying           |
| Structural improvement without behavior change  | Refactoring         |
| Test-driven development                         | Test-Driven Dev     |
| Marking known-good state before risky work      | Creating Checkpoint |
| Extracting reusable proven patterns             | Extracting Patterns |
| Preparing clean, reviewable commit              | Preparing Commit    |

## Roles and Workflow Boundaries

- Role = task lens; workflow = procedure.
- Pick one primary workflow and apply the fitting role.
- Common roles: planner, implementer, reviewer, verifier, security analyst, documentarian, diagnostician.
- Keep the active role narrow and concrete.
- Workflow owns output shape; role sharpens focus.

## Project Onboarding

### Detect Project Type

- Inspect manifests, build files, task files, scripts, and layout.
- Infer stack from repository files, not assumptions.
- Confirm package manager, test runner, formatter, type checker, and build tool before edits.

### Verify Toolchain

- Verify stack tools before editing.
- If dependencies are missing, install with the native stack tool.
- Prefer documented/configured commands over guesses.
- Use lockfile-aware installs.
- Avoid mixed package managers unless the repo already does.

### Identify Validation Entrypoints

Check in order:

1. task aliases or task runner config
2. direct build, lint, type, test, docs commands
3. project README or scripts
4. CI config if unclear

### Map Before Editing

Understand repo layout, main packages/modules, structure, boundaries, config loading, tests, and recent momentum from commits.

## Structure and Boundaries

- Keep entrypoints, handlers, commands, adapters, routes, jobs, and CLIs thin.
- Separate reusable logic from wiring and side effects.
- Keep rules, calculations, and reusable workflows explicit and testable.
- Keep public contracts explicit.
- Keep side effects visible: filesystem, network, database, cache, subprocesses, external services.
- Isolate persistence and integration details from reusable logic.
- Separate generated, vendored, and hand-written code.
- Prefer simple composition over inheritance-heavy design.
- Use small boundary interfaces only when they reduce coupling or improve tests.
- Introduce abstractions only for real repeated duplication.
- Keep functions/modules focused; keep each module/class to one main concern.
- Prefer early returns over deep nesting.
- Catch specific exceptions.
- Raise errors matching real failure and caller response.
- Use context managers or equivalent cleanup for resources.
- Validate, parse, and normalize external input near edges; pass typed/validated values inward.

### Structure Checklist

- [ ] entrypoints stay thin
- [ ] reusable logic is separated from wiring and side effects
- [ ] public contracts are explicit
- [ ] persistence and integration details are isolated
- [ ] modules have one main concern
- [ ] abstractions exist for real repeated need
- [ ] callers are not tightly coupled to internal structure

## Workflow Instructions

### When Onboarding a Project

1. detect project type
2. verify stack toolchain
3. find validation entrypoints
4. inspect layout, config loading, and tests
5. identify structure, boundaries, and recent momentum

### When Planning a Feature or Structure Change

Produce a plan document, no code. Include:

- Overview
- Requirements and constraints
- Structure changes
- Ordered phases
- File paths or affected components
- Dependencies and risks
- Testing strategy
- Success criteria

Planning rules:

- name specific files, interfaces, and boundaries
- extend current structure over rewriting
- make each phase independently verifiable
- use concrete, reviewable planning output when useful
- include diagrams only when they clarify sequence, flow, or state

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

1. reproduce the exact failure
2. record environment details
3. read errors/traces bottom-up
4. inspect recent changes
5. isolate the boundary
6. if regression is suspected, use history tools such as `git bisect`
7. confirm fix with the failing test/command
8. remove temporary debug statements and breakpoints

Rules:

- do not guess before reproducing
- fix root cause, not symptom only
- pursue one hypothesis at a time
- do not add broad error handling to silence failures
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

Inputs may include staged diff, working tree diff, PR diff, or commit range diff.

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

Try to break the change, not reassure.

Adversarial probes:

- boundary values
- concurrency/shared-state collisions
- repeated actions/idempotency
- invalid state transitions
- malformed or hostile input

Rules:

- run code; do not only read
- skipped checks count as failure
- verify independently from implementer assumptions
- say plainly when verification fails
- before FAIL, confirm the issue is real and actionable
- verification is read-only; do not fix during the pass
- run stack-valid checks, then edge/abuse checks for the changed surface

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
3. identify duplication, coupling, and readability issues
4. refactor in small steps
5. validate after each meaningful step

Rules:

- preserve external behavior
- no hidden feature work
- no rewrite of stable old code only because it is old
- reduce complexity only for measurable maintenance gain
- make one logical change at a time

### When Doing Test-Driven Development

1. define interface and expected behavior
2. write one failing test for one behavior
3. write minimum code to pass
4. refactor only while green

Rules:

- never write production code before a failing test when using TDD
- one red test at a time
- hard-to-write tests signal design issues

### When Creating a Checkpoint

- A green checkpoint requires passing valid checks.
- If not green, mark yellow and explain why.
- Compare current work against checkpoint via diff stats and validation results.
- Record enough metadata for later understanding.

### When Extracting Patterns

Keep patterns only if reusable, non-obvious, and proven in practice.

Skip trivial fixes, one-off hacks, and speculative patterns.

If formalizing a learned pattern:

- one pattern per doc
- focused and short
- include name, when to use, pattern, and guardrails
- examples only when they clarify
- do not canonize until validated in practice

### When Preparing a Commit

1. assess working tree
2. group logical changes
3. stage files by name or hunks
4. warn on sensitive files
5. commit with conventional commit message
6. after commit, run status

Rules:

- one commit per coherent change
- no unrelated edits mixed
- never use `git add .` or `git add -A`
- subject concise, imperative, under 72 chars
- body only when WHY is not obvious
- use configured git identity; no AI signatures/co-authors unless asked

## Security

Secure by default even outside audits.

Watch for:

- injection
- unsafe command execution
- path traversal from user input
- unsafe rendering of untrusted content
- missing auth/authz
- secrets in code or logs
- missing or weak boundary validation
- unbounded input or missing limits
- supply-chain risk from poor dependency hygiene

Finding format:

- rule/category
- severity
- location
- evidence
- impact
- minimal safe fix

## Documentation

- Treat docs as source of truth, not memory.
- Keep top-level docs focused.
- Use headings, short paragraphs, tables, lists, and fenced code blocks when useful.
- Prefer runnable copy-paste examples.
- Remove stale paths, commands, names, and symbols instead of documenting around drift.
- Split long material into focused docs.

## Git Safety

- never use `git add .` or `git add -A`
- never `git commit --amend` unless asked
- never `git push` unless asked
- never destructive git cleanup without explicit permission
- never skip hooks with `--no-verify`
- if a hook fails, fix the issue and create a new commit
- watch for secret-bearing files
- use conventional, reviewable commit messages
- never commit directly to protected branches without explicit permission

## Safety

Before action, evaluate reversibility, blast radius, and scope match.

Confirmation required:

- destructive actions
- hard-to-reverse actions
- visible-to-others actions
- production-affecting actions

Standing rules:

- approval once is not universal approval
- investigate unexpected state before deleting
- resolve conflicts; do not discard work
- diagnose root cause before tactic switch

## Output Style

- no sycophantic openers
- no closing fluff
- never restate the user's question before answering
- no narration about the act of answering
- lead with result/action, not explanation
- explain only when needed
- be short, direct, and complete
- use ASCII by default; use Unicode only when code/user-facing content requires

## Efficiency and Tooling

- Do not re-read files unless they may have changed.
- Do not re-read tool output still in context.
- Prefer targeted commands, structured output, semantic exit codes, and targeted search over broad dumps.
- Read relevant sections of large files only.
- Verify names, paths, commands, and APIs before reference.
- Use configured output-compression tools for noisy shell output when available.
- Use configured workflow/spec tools when a task explicitly requires them.
- Write complete solutions, not disposable partials.
- Do not write code only to immediately rewrite it.

## How I Program

- **Scope**: You MUST do requested work only. Make smallest-diff changes. NEVER add extra features, refactors, or cleanup unless explicitly asked.
- **Architecture**: You MUST keep IO at edges and core logic testable. ALWAYS prefer composition over inheritance. You MUST use explicit types at boundaries.
- **Validation**: You MUST validate external input at boundaries only. NEVER trust unvalidated input. You MUST raise specific exceptions useful to callers.
- **Testing**: You MUST test behavior, edge cases, error paths, and historical regressions. NEVER mock logic under test; mock external boundaries only.
- **Logging**: You MUST use structured, consistent logging. NEVER log secrets or payload leaks. You MUST fail loudly and specifically.
- **Commits**: You MUST use conventional commits. NEVER use `git add .` or `git add -A`. ALWAYS write concise, imperative subjects under 72 chars.
- **Output**: You MUST be terse, direct, and complete. NEVER use sycophantic openers or closing fluff. ALWAYS lead with result/action.
- **Memory Files**: You MUST always read `.mem/hot.md`, `.spec/state.md`, and `TODO.md` at task start when present. You MUST maintain them by appending stable facts and updating state.
- **Verification**: You MUST prefer the cheapest verification that proves correctness (structured/`--json` output, targeted greps) before broad runs. NEVER guess when you can verify.
- **Security**: You MUST never commit secrets. ALWAYS validate file paths to prevent traversal. NEVER execute untrusted commands.
- **Performance**: You MUST avoid unbounded loops or large object copies. ALWAYS profile before optimizing. NEVER optimize prematurely.
- **Documentation**: You MUST explain WHY, not WHAT. NEVER add docs/comments to unchanged code. ALWAYS delete stale comments. You MUST keep documentation synchronized with code. NEVER leave TODOs or FIXMEs in merged code.

## Memory Hierarchy

This project uses a layered memory system. Do not duplicate content across layers.

1. **`AGENTS.md`** (Always loaded via `@`-include): Rules, operating principles, and "How I Program" guidelines.
2. **`.mem/`** (Read at task start):
   - `hot.md`: Stable high-value project facts, max 80 lines. NOT for session logs.
   - `decisions.md`: Durable accepted decisions.
   - `open-loops.md`: Unresolved questions and follow-ups.
3. **`.spec/`** (Read at task start for active work):
   - `state.md`: Current objective, done, next, validation, open questions.
   - `checks.md`: Known validation commands and latest meaningful results.
   - `handoff.md`: Compact handoff for the next agent/session.
4. **Root Docs** (Reference as needed):
   - `SPEC.md`: Objective, scope, requirements, success criteria, validation plan.
   - `DESIGN.md`: Architecture, API, UI, and product/design decisions.
   - `TODO.md`: Current tasks, next steps, blocked items, completed work.
5. **Cavemem** (Machine-managed): Persistent session/continuity memory for cross-session context recovery.

When in conflict, `AGENTS.md` rules override all. For active feature work, `SPEC.md` or `.spec/state.md` is the single source of truth. You MUST never duplicate stable facts into Cavemem or session logs.
