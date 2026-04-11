#!/usr/bin/env bash
# Notification hook: desktop alert when Claude needs input.

INPUT=$(cat)
TITLE=$(echo "$INPUT" | jq -r '.title // "Claude Code"')
MSG=$(echo "$INPUT" | jq -r '.message // "Needs attention"')
notify-send "$TITLE" "$MSG" 2>/dev/null || true
exit 0
