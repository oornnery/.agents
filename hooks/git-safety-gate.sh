#!/usr/bin/env bash
# PreToolUse hook: block destructive git and shell commands.

INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
[ -z "$CMD" ] && exit 0

case "$CMD" in
  *"git add ."*|*"git add -A"*|*"git add --all"*)
    echo "Blocked: stage files by name, not 'git add .'" >&2
    exit 2 ;;
  *"git reset --hard"*)
    echo "Blocked: git reset --hard is destructive. Use git stash instead." >&2
    exit 2 ;;
  *"rm -rf /"*|*"rm -rf ~"*)
    echo "Blocked: destructive rm command." >&2
    exit 2 ;;
  *"--no-verify"*)
    echo "Blocked: never skip pre-commit hooks." >&2
    exit 2 ;;
esac
exit 0
