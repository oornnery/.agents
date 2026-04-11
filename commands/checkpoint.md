---
name: checkpoint
description: Create, verify, or list named checkpoints during implementation. Use to mark known-good states and verify no regressions.
---

# Checkpoint

Mark and verify known-good states during implementation.

## Operations

### Create

Save a named checkpoint at the current state:

```bash
# 1. Run full validation suite
uv run ruff format --check .
uv run ruff check .
uv run rumdl check .
uv run ty check
uv run pytest -v

# 2. Record state
mkdir -p .checkpoints
echo "{\"name\": \"<name>\", \"sha\": \"$(git rev-parse --short HEAD)\", \"branch\": \"$(git branch --show-current)\", \"date\": \"$(date -Iseconds)\", \"status\": \"green\"}" >> .checkpoints/log.jsonl
```

A checkpoint is only valid if all checks pass. If any check fails,
fix it first or record `"status": "yellow"` with a note.

### Verify

Compare current state against a named checkpoint:

1. Run the validation suite.
2. Check `git diff <checkpoint-sha>..HEAD --stat` for changes since checkpoint.
3. Report: what changed, what still passes, any regressions.

### List

```bash
cat .checkpoints/log.jsonl | jq -r '[.name, .sha, .date, .status] | @tsv'
```

## When to Use

- Before starting a risky refactor (create checkpoint)
- After completing a phase (create checkpoint)
- When something breaks (verify against last green checkpoint)
- Before merging (verify against initial checkpoint)

## Constraints

- Checkpoints are local state (`.checkpoints/` is gitignored).
- A checkpoint only means "validation passed" -- not "feature complete".
- If verification shows regressions, do not proceed until fixed.
