---
globs: "**"
---

# Agents

Specialized personas in `agents/`. Each has constrained tools and a model
assignment. Domain knowledge lives in skills, not agents.

## Available Agents

| Agent             | Model  | When to use                                    |
| ----------------- | ------ | ---------------------------------------------- |
| planner           | opus   | Complex features, architecture decisions, SDD  |
| reviewer          | sonnet | Code review producing feedback (not changes)   |
| security-reviewer | sonnet | Security-focused analysis, OWASP, secrets      |
| build-fixer       | sonnet | Fix ruff/ty/pytest/uv errors with minimal diff |
| tdd-guide         | sonnet | Enforce Red/Green/Refactor cycle               |
| doc-updater       | haiku  | README, docstrings, CLAUDE.md maintenance      |
| diagnostician     | sonnet | Root cause analysis, system diagnostics        |

## Model Selection

- **opus** -- deep reasoning: planning, architecture, ambiguous requirements
- **sonnet** -- balanced: implementation, review, debugging, testing
- **haiku** -- fast and cheap: documentation, simple edits, formatting

## Agent vs Command Boundary

- **Agent** = persona with constrained tools. Lean (<60 lines). References
  skills for knowledge. Two types:
    - *Read-only* (planner, reviewer, security-reviewer, diagnostician) --
    produce artifacts/reports, never modify code.
    - *Execution* (build-fixer, tdd-guide, doc-updater) -- modify code with
    a narrow mandate (fix errors, write tests, update docs).
- **Command** = procedural workflow. Orchestrates steps, may invoke agents.
  Owns the methodology and output format.
- **Skill** = domain knowledge module. Referenced by agents and commands.
  Never invoked directly as a persona.

## Conventions

- Launch independent agents in parallel.
- Agents reference skills for deep knowledge (do not duplicate content).
- Commands own output format specs -- agents follow them.
