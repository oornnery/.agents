---
name: verify
description: Adversarial verification of an implementation. Use after a feature, fix, refactor, or CI change to prove it works and try to break it.
---

# Verify

Verify adversarially. Goal: find what broken, not reassure self change looks fine.

## Mindset

- run code, do not only read it
- verify independent from implementer assumptions
- skipped checks = failure
- report failures plain, no softening

## Verification Phases

### Phase 1: Classify the changed surface

Read diff, classify change:

- backend API
- frontend or UI
- database migration
- bug fix
- refactor
- CLI tool
- config
- dependencies

Load only relevant skills for surface:

- `skills/python/SKILL.md` for Python code, typing, valid commands, runtime behavior
- `skills/design/SKILL.md` for API, UI, BFF contracts
- `skills/security/SKILL.md` for auth, trust boundaries, abuse paths, exposure risk
- `skills/quality/SKILL.md` when regression thinking or RCA should shape verification
- `skills/cicd/SKILL.md` for GitHub Actions workflow verification
- `skills/docs/SKILL.md` for docs-only changes

### Phase 2: Run the baseline validation suite

Python repos, default order:

```bash
uv run ruff format --check .
uv run ruff check .
uv run rumdl check .
uv run ty check
uv run pyright
uv run pytest -v
```

If repo exposes task aliases, prefer them.

Other surfaces, run closest equivalent first:

- CI changes: workflow or lint entrypoints from `skills/cicd/SKILL.md`
- docs-only changes: `uv run rumdl check .`
- mixed changes: baseline suite plus surface-specific command

If baseline validation fails, record before moving on.
For security-sensitive Python changes, also run the explicit security task when present:

```bash
uv run task sec
```

Bandit findings require triage; do not hide them by folding Bandit into unrelated checks.

### Phase 3: Check changed behaviors directly

For each important behavior, record:

```text
## Check: [description]
Command: ...
Expected: ...
Observed: ...
Result: PASS | FAIL
```

Check without command = not PASS.

### Phase 4: Probe adversarially

Try break change with:

- boundary values: empty, null, max, negative, unicode, long input
- concurrency: simultaneous calls, shared state, locking, transaction boundaries
- idempotency: repeat op, retry request, double-submit
- state transitions: invalid orderings, partial state, missing valid

### Phase 5: Review security and unintended drift

Check for:

- missing or weakened valid at boundaries
- auth, permission, or trust-boundary regressions
- unexpected file changes or generated churn in diff
- docs or workflow drift if change touched commands, skills, hooks, or CI

### Phase 6: Confirm failures are real

Before issuing FAIL, check:

- is behavior intentional
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

- verification = read-only; do not fix issues during pass
- do not run only happy path
- do not mark PASS because it "looks correct"
- do not skip validations to save time
