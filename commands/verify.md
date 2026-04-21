---
name: verify
description: Adversarial verification of an implementation. Use after a feature, fix, refactor, or CI change to prove it works and try to break it.
---

# Verify

Verify adversarially. The goal is to find what is broken, not to reassure
yourself that the change looks fine.

## Mindset

- run the code, do not only read it
- verify independently from the implementer's assumptions
- skipped checks count as failure
- report plain failures without softening them

## Verification Phases

### Phase 1: Classify the changed surface

Read the diff and classify the change:

- backend API
- frontend or UI
- database migration
- bug fix
- refactor
- CLI tool
- configuration
- dependencies

Load only the relevant skills for that surface:

- `skills/python/SKILL.md` for Python code, typing, validation commands, and runtime behavior
- `skills/design/SKILL.md` for API, UI, and BFF contracts
- `skills/security/SKILL.md` for auth, trust boundaries, abuse paths, and exposure risk
- `skills/quality/SKILL.md` when regression thinking or RCA should shape the verification
- `skills/cicd/SKILL.md` for GitHub Actions workflow verification
- `skills/docs/SKILL.md` for documentation-only changes

### Phase 2: Run the baseline validation suite

For Python repos, the default order is:

```bash
uv run ruff format --check .
uv run ruff check .
uv run rumdl check .
uv run ty check
uv run pytest -v
```

If the repo exposes task aliases, prefer them.

For other surfaces, run the closest equivalent first:

- CI changes: workflow or lint entrypoints from `skills/cicd/SKILL.md`
- docs-only changes: `uv run rumdl check .`
- mixed changes: baseline suite plus the surface-specific command

If baseline validation fails, record it before moving on.

### Phase 3: Check changed behaviors directly

For each important behavior, record:

```text
## Check: [description]
Command: ...
Expected: ...
Observed: ...
Result: PASS | FAIL
```

A check without a command is not a PASS.

### Phase 4: Probe adversarially

Try to break the change with:

- boundary values: empty, null, max, negative, unicode, long input
- concurrency: simultaneous calls, shared state, locking, transaction boundaries
- idempotency: repeat the operation, retry the request, double-submit
- state transitions: invalid orderings, partial state, missing validation

### Phase 5: Review security and unintended drift

Check for:

- missing or weakened validation at boundaries
- auth, permission, or trust-boundary regressions
- unexpected file changes or generated churn in the diff
- docs or workflow drift if the change touched commands, skills, hooks, or CI

### Phase 6: Confirm failures are real

Before issuing FAIL, check:

- is the behavior intentional
- is it handled elsewhere
- is it actionable and reproducible

## Output

Use this format:

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

## Constraints

- verification is read-only; do not fix issues during the pass
- do not run only the happy path
- do not mark something PASS because it "looks correct"
- do not skip validations to save time
