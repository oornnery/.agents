#!/usr/bin/env bash
# SessionStart hook: inject compact-specific reminders after compaction.

INPUT=$(cat)
SOURCE=$(echo "$INPUT" | jq -r '.source // empty')
[ "$SOURCE" != "compact" ] && exit 0

jq -n --arg msg "Context was compacted. Re-anchor on the base and relevant AGENTS variants if needed. Keep diffs small, verify names and paths with tools, use uv over pip, stage files by name, and avoid destructive git. Current local skills: python, arch, design, quality, security, docs, cicd, sqlmodel, rich, rtk, building-agents." \
  '{ additionalContext: $msg }'
