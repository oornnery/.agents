#!/usr/bin/env bash
# SessionStart hook: inject convention reminders after context compaction.

INPUT=$(cat)
SOURCE=$(echo "$INPUT" | jq -r '.source // empty')
[ "$SOURCE" != "compact" ] && exit 0

cat <<'HOOK_EOF'
{
  "additionalContext": "Context was compacted. Key conventions to remember:\n\n[python] pathlib, f-strings, type all public functions, Pydantic for validation, IO at edges, no gold-plating, comments explain WHY not WHAT, report outcomes faithfully.\n\n[git] Stage files by name (never git add .), never amend/push unless asked, never --no-verify, Conventional Commits format, never commit to main directly -- use PRs.\n\n[safety] Evaluate reversibility and blast radius before actions. Confirm destructive/visible/prod-affecting ops. Diagnose root causes before switching tactics.\n\n[uv] Always uv over pip, uv run for commands, uvx for one-off tools, commit uv.lock, uv sync --frozen in CI.\n\n[output] No sycophantic openers/closers, no narration, result first, ASCII-only, never invent paths/names -- verify with tools, write complete solutions in one pass.\n\n[docs] Scannable structure, fenced code blocks with language tags, run rumdl check before committing markdown.\n\nAll CLI commands go through RTK automatically (handled by hook)."
}
HOOK_EOF
