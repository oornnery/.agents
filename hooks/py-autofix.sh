#!/usr/bin/env bash
# PostToolUse hook: auto-format Python files after Edit/Write.

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
[[ "$FILE" == *.py ]] || exit 0

uvx ruff format "$FILE" 2>/dev/null
uvx ruff check --fix "$FILE" 2>/dev/null
uvx ty check "$FILE" 2>/dev/null
exit 0
