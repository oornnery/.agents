#!/usr/bin/env bash
# Stop hook: suggest pattern extraction if significant work was done.

CHANGED=$(git diff --stat HEAD~3 2>/dev/null | tail -1 | grep -oP '\d+ file' | grep -oP '\d+' || echo "0")

# Only suggest if substantial work happened (>5 files changed in last 3 commits)
[ "$CHANGED" -lt 5 ] 2>/dev/null && exit 0

cat <<'HOOK_EOF'
{
  "additionalContext": "Significant work detected in this session. Consider running /learn to extract reusable patterns before ending."
}
HOOK_EOF
