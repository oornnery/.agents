#!/usr/bin/env bash
# SessionStart hook: provide project context at session start.

# Detect project type
PROJECT_TYPE="unknown"
[ -f "pyproject.toml" ] && PROJECT_TYPE="python"
[ -f "package.json" ] && PROJECT_TYPE="node"
[ -f "pyproject.toml" ] && [ -f "package.json" ] && PROJECT_TYPE="fullstack"

# Git state
BRANCH=$(git branch --show-current 2>/dev/null || echo "none")
CHANGED=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
RECENT=$(git log --oneline -3 2>/dev/null | tr '\n' '; ' | sed 's/; $//')

# Skill suggestions based on detected files
SKILLS=""
[ -f "pyproject.toml" ] && SKILLS="python, uv"
grep -q "fastapi" pyproject.toml 2>/dev/null && SKILLS="${SKILLS}, fastapi, pydantic"
grep -q "typer" pyproject.toml 2>/dev/null && SKILLS="${SKILLS}, typer"
grep -q "httpx" pyproject.toml 2>/dev/null && SKILLS="${SKILLS}, httpx"
grep -q "sqlmodel" pyproject.toml 2>/dev/null && SKILLS="${SKILLS}, sqlmodel"

CONTEXT="Project: ${PROJECT_TYPE} | Branch: ${BRANCH} | Uncommitted: ${CHANGED} | Recent: ${RECENT}"
[ -n "$SKILLS" ] && CONTEXT="${CONTEXT} | Suggested skills: ${SKILLS}"

cat <<HOOK_EOF
{
  "additionalContext": "${CONTEXT}"
}
HOOK_EOF
