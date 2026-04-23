---
name: checkpoint
description: Record or compare known-good state during implementation. Use before risky work, after stable milestone, or when comparing current tree to previous validated point.
---

# Checkpoint

Capture, compare known-good states during implementation.

## Operations

### Create

Record named checkpoint after running relevant validation suite.

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
- optional note explaining why not green

Green checkpoint requires passing validation for changed surface.

### Verify against a checkpoint

Compare current state to previous checkpoint:

1. pick checkpoint SHA from `.checkpoints/log.jsonl`
2. rerun relevant validation suite
3. inspect `git diff <checkpoint-sha>..HEAD --stat`
4. summarize what changed, whether validation still holds

### List

Show recorded checkpoints and status:

```bash
jq -r '[.name, .sha, .branch, .status, .date] | @tsv' .checkpoints/log.jsonl
```

## When to use

- before risky refactor
- after finishing milestone
- before comparing regressions
- before handing off to review or verification

## Constraints

- checkpoint means "known validated state", not "feature complete"
- if validation not green, mark yellow and explain why
- do not treat stale checkpoints as proof current tree is healthy
- do not create checkpoint without recording what was actually validated

## Related

- `skills/git/SKILL.md`
- `commands/verify.md`