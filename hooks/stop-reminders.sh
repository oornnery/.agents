#!/usr/bin/env bash
# Stop hook: summarize important reminders before ending.

INPUT=$(cat)
ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')
[ "$ACTIVE" = "true" ] && exit 0

CHANGED=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
MESSAGE=""

if [ "$CHANGED" -gt 0 ] 2>/dev/null; then
  MESSAGE="There are ${CHANGED} uncommitted changes. Consider committing before ending."
fi

if [ "$CHANGED" -ge 5 ] 2>/dev/null; then
  EXTRA="Significant in-progress work detected. Consider extracting reusable patterns into skills or the base/variant AGENTS files before ending."
  if [ -n "$MESSAGE" ]; then
    MESSAGE="${MESSAGE}\n\n${EXTRA}"
  else
    MESSAGE="${EXTRA}"
  fi
fi

[ -n "$MESSAGE" ] || exit 0

jq -n --arg msg "$MESSAGE" '{ additionalContext: $msg }'
