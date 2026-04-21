#!/usr/bin/env bash
set -euo pipefail

jq -n \
  --arg cwd "$(pwd)" \
  --arg branch "$(git branch --show-current 2>/dev/null || printf '%s' '-')" \
  '{
    hookSpecificOutput: {
      hookEventName: "SessionStart",
      additionalContext: "cwd: \($cwd)\nbranch: \($branch)"
    }
  }'
