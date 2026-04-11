#!/usr/bin/env bash
# Stop hook: warn about uncommitted changes before ending.

INPUT=$(cat)
ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')
[ "$ACTIVE" = "true" ] && exit 0

STATUS=$(git status --porcelain 2>/dev/null)
if [ -n "$STATUS" ]; then
  CHANGED=$(echo "$STATUS" | wc -l | tr -d ' ')
  jq -n --arg msg "There are $CHANGED uncommitted changes. Consider committing before ending." \
    '{ additionalContext: $msg }'
fi
exit 0
