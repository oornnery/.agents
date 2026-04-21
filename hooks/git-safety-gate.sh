#!/usr/bin/env bash
# PreToolUse hook: block destructive git and shell commands.

INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
[ -z "$CMD" ] && exit 0

matches() {
  printf '%s\n' "$CMD" | grep -Eq "$1"
}

if matches '(^|[[:space:];|&])git[[:space:]]+add([[:space:]]+-[^[:space:]]+)*[[:space:]]+\.(($|[[:space:];|&]))'; then
  echo "Blocked: stage files by name, not 'git add .'" >&2
  exit 2
fi

if matches '(^|[[:space:];|&])git[[:space:]]+add([[:space:]]+-[^[:space:]]+)*[[:space:]]+(-A|--all)(($|[[:space:];|&]))'; then
  echo "Blocked: stage files by name, not 'git add -A' or 'git add --all'" >&2
  exit 2
fi

if matches '(^|[[:space:];|&])git[[:space:]]+reset[[:space:]]+--hard(($|[[:space:];|&]))'; then
  echo "Blocked: git reset --hard is destructive. Use git stash instead." >&2
  exit 2
fi

if matches '(^|[[:space:];|&])rm[[:space:]]+-rf[[:space:]]+(/|~)(($|[[:space:];|&]))'; then
  echo "Blocked: destructive rm command." >&2
  exit 2
fi

if matches '(^|[[:space:];|&])--no-verify(($|[[:space:];|&]))'; then
  echo "Blocked: never skip pre-commit hooks." >&2
  exit 2
fi

exit 0
