#!/usr/bin/env bash
# PostToolUse hook: auto-fix Markdown lint after Edit/Write.

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
[[ "$FILE" == *.md ]] || exit 0

uvx rumdl check --fix "$FILE" 2>/dev/null
exit 0
