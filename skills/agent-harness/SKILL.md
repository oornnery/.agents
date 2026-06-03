---
name: agent-harness
description: Build, review, or validate AI agent harnesses and runtimes. Use for prompt assembly, context builders, memory, tools, permissions, approvals, model providers, turn runners, sessions, hooks, traces, evals, replay, and operational safety.
---

# Agent Harness

Use for model-calling systems where context, tools, permissions, memory, traces, and runtime control must be explicit.

## Boundaries

- Harness: prompt assembly, context building, model calls, tool calling, parsing, approvals.
- Runtime: sessions, workers, retries, queues, recovery, orchestration.
- Memory: short-term context, durable project facts, retrieval, compaction, redaction.
- Tools: schemas, adapters, execution wrappers, permission gates.

Pair with:

- `skills/building-agents/SKILL.md` for broader agent-building guidance
- `skills/project-state/SKILL.md` for state/memory files
- `skills/security/SKILL.md` for permissions, prompt injection, secrets, and tool risk
- `skills/verification/SKILL.md` for evals, replay, static checks, and runtime validation

## Workflow

1. Map actors, model providers, tool surface, permissions, memory, session lifecycle, and high-risk actions.
2. Make instruction precedence and prompt assembly inspectable.
3. Keep tool schemas, arguments, return values, and errors explicit.
4. Gate risky tools by action, path, scope, or approval.
5. Bound execution with max steps, retries, cancellation, and timeouts.
6. Persist enough trace/state to debug and replay critical flows.
7. Verify with provider mocks, tool mocks, policy tests, parser recovery, and replay/eval cases.

## Core Rules

- No hidden instruction injection paths.
- No vague "do everything" tools hiding side effects.
- Validate tool input before execution and output before reuse.
- Separate read-only, write, network, execution, and destructive tool classes.
- Treat stale memory, prompt injection, unsafe delegation, and over-broad permissions as first-class risks.
- Fail closed for unsafe actions; fail open only for harmless convenience helpers.

## Suggested Layout

```text
src/myapp/
├── harness/
├── runtime/
├── prompts/
├── tools/
├── permissions/
├── context/
├── memory/
├── parser/
├── evals/
├── storage/
└── traces/
```

## Verification

- prompt assembly precedence
- provider mock and streaming behavior
- tool schema validation
- permission and approval decisions
- malformed output and parser recovery
- retry, timeout, cancellation, max-step behavior
- replay/eval fixtures for important tasks
