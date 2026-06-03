#!/usr/bin/env bash
# Stop hook: remind agents to update lightweight project state when work changed.

INPUT=$(cat)
ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')
[ "$ACTIVE" = "true" ] && exit 0

CHANGED=$(git status --porcelain 2>/dev/null || true)
[ -n "$CHANGED" ] || exit 0

NON_STATE=$(printf '%s\n' "$CHANGED" | grep -Ev ' (SPEC\.md|DESIGN\.md|TODO\.md|\.spec/|\.mem/)' | wc -l | tr -d ' ')
STATE_CHANGED=$(printf '%s\n' "$CHANGED" | grep -E ' (SPEC\.md|DESIGN\.md|TODO\.md|\.spec/|\.mem/)' | wc -l | tr -d ' ')

[ "$NON_STATE" -gt 0 ] 2>/dev/null || exit 0
[ "$STATE_CHANGED" -eq 0 ] 2>/dev/null || exit 0

if [ -d ".spec" ] || [ -d ".mem" ] || [ -f "SPEC.md" ] || [ -f "DESIGN.md" ] || [ -f "TODO.md" ]; then
  MSG="Project state may be stale. If this work changed scope, decisions, validation, or next steps, update SPEC.md, DESIGN.md, TODO.md, .spec/state.md, .spec/handoff.md, or .mem/open-loops.md before stopping."
else
  MSG="For multi-step work, consider initializing lightweight state from .agents/templates/project: SPEC.md, DESIGN.md, TODO.md, .spec/, and .mem/."
fi

jq -n --arg msg "$MSG" '{ additionalContext: $msg }'
