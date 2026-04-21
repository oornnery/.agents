---
name: checkpoint
description: Record or compare a known-good state during implementation. Use before risky work, after a stable milestone, or when comparing the current tree to a previous validated point.
---

# Checkpoint

Capture and compare known-good states during implementation.

## Operations

### Create

Record a named checkpoint after running the relevant validation suite.

Suggested local format:

```bash
mkdir -p .checkpoints
```

Store checkpoints in `.checkpoints/log.jsonl`, one JSON object per line.

Example:

```bash
jq -n \
  --arg name "<name>" \
  --arg sha "$(git rev-parse --short HEAD)" \
  --arg branch "$(git branch --show-current)" \
  --arg date "$(date -Iseconds)" \
  --arg status "green" \
  --arg note "" \
  '{name: $name, sha: $sha, branch: $branch, date: $date, status: $status, note: $note}' \
  >> .checkpoints/log.jsonl
```

Record:

- checkpoint name
- current short SHA
- current branch
- timestamp
- validation status: `green` or `yellow`
- optional note explaining why it is not green

A green checkpoint requires passing validation for the changed surface.

### Verify against a checkpoint

Compare the current state to a previous checkpoint:

1. pick the checkpoint SHA from `.checkpoints/log.jsonl`
2. rerun the relevant validation suite
3. inspect `git diff <checkpoint-sha>..HEAD --stat`
4. summarize what changed and whether validation still holds

### List

Show the recorded checkpoints and their status:

```bash
jq -r '[.name, .sha, .branch, .status, .date] | @tsv' .checkpoints/log.jsonl
```

## When to use

- before a risky refactor
- after finishing a milestone
- before comparing regressions
- before handing off to review or verification

## Constraints

- a checkpoint means "known validated state", not "feature complete"
- if validation is not green, mark it yellow and explain why
- do not treat stale checkpoints as proof the current tree is healthy
- do not create a checkpoint without recording what was actually validated

## Related

- `skills/git/SKILL.md`
- `commands/verify.md`
