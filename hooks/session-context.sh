#!/usr/bin/env bash
# SessionStart hook: provide project context at session start.

add_skill() {
  local skill="$1"
  case ",${SKILLS}," in
    *",${skill},"*) ;;
    *) SKILLS="${SKILLS:+${SKILLS}, }${skill}" ;;
  esac
}

PROJECT_TYPE="unknown"
[ -f "pyproject.toml" ] && PROJECT_TYPE="python"
[ -f "package.json" ] && PROJECT_TYPE="node"
[ -f "pyproject.toml" ] && [ -f "package.json" ] && PROJECT_TYPE="fullstack"

BRANCH=$(git branch --show-current 2>/dev/null || echo "none")
CHANGED=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
RECENT=$(git log --oneline -3 2>/dev/null | tr '\n' '; ' | sed 's/; $//')

SKILLS=""
[ -f "pyproject.toml" ] && add_skill "python"
[ -f "pyproject.toml" ] && add_skill "quality"
[ -f "pyproject.toml" ] && add_skill "security"
[ -f "pyproject.toml" ] && add_skill "docs"
[ -f ".github/workflows/ci.yml" ] && add_skill "cicd"
grep -qi "fastapi" pyproject.toml 2>/dev/null && add_skill "design"
grep -qi "sqlmodel" pyproject.toml 2>/dev/null && add_skill "sqlmodel"
grep -qi "rich" pyproject.toml 2>/dev/null && add_skill "rich"
grep -qi "rtk" pyproject.toml 2>/dev/null && add_skill "rtk"

[ -d ".claude/skills" ] && add_skill "arch"
[ -d ".claude/skills" ] && add_skill "design"
[ -d ".claude/skills" ] && add_skill "building-agents"

CONTEXT="Project: ${PROJECT_TYPE} | Branch: ${BRANCH} | Uncommitted: ${CHANGED} | Recent: ${RECENT}"
[ -n "$SKILLS" ] && CONTEXT="${CONTEXT} | Suggested skills: ${SKILLS}"

jq -n --arg msg "${CONTEXT}" '{ additionalContext: $msg }'
