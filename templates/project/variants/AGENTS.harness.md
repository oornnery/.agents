# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!-- Agent harness/runtime overlay. Keep details in skills/agent-harness. -->

## Project Description

<!-- What harness wraps, delegates, tools exposed, high-risk actions -->

## Stack Defaults

- **Agent Framework**: PydanticAI when it fits
- **Validation and Schemas**: Pydantic
- **HTTP Client**: HTTPX
- **State**: explicit sessions, memory, traces, and replay data
- **Evaluation**: regression fixtures, replays, or task suites

## Quick Commands

```bash
uv sync
uv run task check
uv run pytest -v
```

## Validation Entry Points

Use configured commands only:

```bash
uv run task check
uv run ruff format --check .
uv run ruff check .
uv run ty check src
uv run pytest -v
```

## Skill Routing

- Load `skills/agent-harness/SKILL.md` for harness/runtime/tool/context/memory design.
- Load `skills/building-agents/SKILL.md` for broader agent-building guidance.
- Load `skills/project-state/SKILL.md` for session state, memory policy, handoff, and open loops.
- Load `skills/verification/SKILL.md` for eval, replay, static checks, and validation gates.
- Load `skills/security/SKILL.md` for permissions, prompt injection, tool risk, secrets, and trust boundaries.

## Always-On Harness Rules

- Instruction precedence and prompt assembly must be inspectable.
- Tools need explicit schemas, return shapes, errors, and permission class.
- Risky actions need approval or a safe default.
- Context growth, memory writes, retries, timeouts, and max steps must be bounded.
- Preserve enough trace/state to debug and replay critical flows.

## Project-Specific Guardrails

<!-- - Keep tool allowlists explicit -->
<!-- - Persist enough traces for replay -->
