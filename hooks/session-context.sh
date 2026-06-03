#!/usr/bin/env bash
# SessionStart hook: provide project context at session start.

add_skill() {
  local skill="$1"
  case ",${SKILLS}," in
    *",${skill},"*) ;;
    *) SKILLS="${SKILLS:+${SKILLS}, }${skill}" ;;
  esac
}

append_state_file() {
  local label="$1"
  local path="$2"
  local max_lines="$3"

  [ -f "$path" ] || return 0

  local snippet
  snippet=$(sed -n "1,${max_lines}p" "$path")
  [ -n "$snippet" ] || return 0

  CONTEXT="${CONTEXT}

${label}:
${snippet}"
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
[ -f "pyproject.toml" ] && add_skill "verification"
[ -f "package.json" ] && add_skill "verification"
[ -f ".github/workflows/ci.yml" ] && add_skill "cicd"
grep -qi "fastapi" pyproject.toml 2>/dev/null && add_skill "design"
grep -qi "typer\|rich-argparse\|click" pyproject.toml 2>/dev/null && add_skill "python-cli"
grep -qi "hatchling\|setuptools\|flit\|maturin" pyproject.toml 2>/dev/null && add_skill "python-library"
grep -qi "pydantic-ai\|openai\|anthropic" pyproject.toml 2>/dev/null && add_skill "agent-harness"
grep -qi "sqlmodel" pyproject.toml 2>/dev/null && add_skill "sqlmodel"
grep -qi "rich" pyproject.toml 2>/dev/null && add_skill "rich"
grep -qi "rtk" pyproject.toml 2>/dev/null && add_skill "rtk"

[ -d ".claude/skills" ] && add_skill "arch"
[ -d ".claude/skills" ] && add_skill "design"
[ -d ".claude/skills" ] && add_skill "building-agents"

if [ -f "SPEC.md" ] || [ -f "DESIGN.md" ] || [ -f "TODO.md" ] || [ -d ".spec" ] || [ -d ".mem" ]; then
  add_skill "project-state"
fi

CONTEXT="Project: ${PROJECT_TYPE} | Branch: ${BRANCH} | Uncommitted: ${CHANGED} | Recent: ${RECENT}"
[ -n "$SKILLS" ] && CONTEXT="${CONTEXT} | Suggested skills: ${SKILLS}"

append_state_file ".spec/state.md" ".spec/state.md" 50
append_state_file ".mem/hot.md" ".mem/hot.md" 80

jq -n --arg msg "${CONTEXT}" '{ additionalContext: $msg }'
