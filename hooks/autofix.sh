#!/usr/bin/env bash
# PostToolUse hook: auto-fix supported text files after Edit/Write.

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
[ -f "$FILE" ] || exit 0

warn() {
  echo "[autofix] $1" >&2
}

run_with_fallback() {
  if [ -f "pyproject.toml" ] && command -v uv >/dev/null 2>&1; then
    if uv run "$@" >/dev/null 2>&1; then
      return 0
    fi
  fi

  if command -v uvx >/dev/null 2>&1; then
    if uvx "$@" >/dev/null 2>&1; then
      return 0
    fi
  fi

  warn "warning: failed: $*"
  return 1
}

case "$FILE" in
  *.py)
    run_with_fallback ruff format "$FILE"
    run_with_fallback ruff check --fix "$FILE"
    run_with_fallback ty check "$FILE"
    ;;
  *.md)
    run_with_fallback rumdl check --fix "$FILE"
    ;;
esac

exit 0
