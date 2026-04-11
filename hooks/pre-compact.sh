#!/usr/bin/env bash
# PreCompact hook: save working state before context compaction.

BRANCH=$(git branch --show-current 2>/dev/null || echo "detached")
SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
CHANGED=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
STASHES=$(git stash list 2>/dev/null | wc -l | tr -d ' ')

STATE="branch=${BRANCH}, HEAD=${SHA}, uncommitted=${CHANGED}, stashes=${STASHES}"

cat <<HOOK_EOF
{
  "additionalContext": "Pre-compact state: ${STATE}. Restore context after compaction."
}
HOOK_EOF
