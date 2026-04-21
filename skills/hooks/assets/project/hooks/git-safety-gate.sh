#!/usr/bin/env bash
set -euo pipefail

input="${1:-}"

case "$input" in
  "git add ."|"git add -A"|"git reset --hard")
    printf '%s\n' "unsafe git command blocked" >&2
    exit 2
    ;;
  *)
    exit 0
    ;;
esac
