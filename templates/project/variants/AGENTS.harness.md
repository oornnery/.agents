# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!--
Harness + runtime overlay.
Model calls → operational agent system: context, tools, permissions,
sessions, memory, traces, execution control.
-->

## Project Description

<!-- What harness wraps, delegates, high-risk surfaces -->

## Stack

- **Agent Framework**: PydanticAI
- **Validation and Schemas**: Pydantic
- **HTTP Client**: HTTPX
<!-- - **Prompt Assembly**: template builder / instruction compiler -->
<!-- - **Tool Layer**: JSON schema / MCP / internal adapters -->
<!-- - **Permissions**: policy engine / allowlist / risk classifier -->
<!-- - **State**: snapshots / session store / traces -->
<!-- - **Runtime**: turn runner / workers / queues / schedulers -->
<!-- - **Evaluation**: regression harness / golden transcripts / task suites -->

## Quick Commands

```bash
uv sync
uv run task check
uv run pytest -v
```

## Validation Entry Points

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check src
uv run pytest -v
```

## Harness and Runtime Responsibilities

- collect stable runtime context before execution
- assemble instructions from explicit sources
- expose closed tool surface with documented schemas
- validate + permission tool requests before execution
- record tool calls, outputs, retries, final answers
- bound execution: steps, retries, timeouts
- preserve trace data for debug + regression
- keep turn flow, session flow, long-running execution visible + auditable
- separate user turns from long-running jobs, retries, worker tasks

## Preferred Libraries

- `PydanticAI` default harness layer for model-first tool-using projects
- `Pydantic` for request, tool, config, structured output models
- `HTTPX` for provider calls, external APIs, callbacks, testable HTTP integrations
- keep provider adapters, tool contracts, parser logic explicit even with framework conveniences

## Design Boundary

- harness = turn-level context building, tool calling, parsing, approvals, model interaction
- runtime = session-level execution, workers, retries, queues, recovery, orchestration
- boundaries stay tightly coupled in most agent projects → overlay treats as one operational system
- keep interfaces between harness pieces explicit even in same codebase

## Suggested Layout

```text
src/myapp/
├── harness/         # turn-level orchestration entrypoint
├── runtime/         # session lifecycle, workers, retries, and schedulers
├── prompts/         # prompt builders, templates, and instruction assembly
├── tools/           # tool schemas, adapters, and execution wrappers
├── permissions/     # allowlists, policy checks, risk classification
├── context/         # context collection, compaction, and snapshots
├── memory/          # short-term and persistent memory handling
├── parser/          # structured output parsing and retry logic
├── evals/           # regression suites, fixtures, and replay cases
├── storage/         # session, trace, or state persistence
└── traces/          # stored transcripts, events, or execution logs
```

## Prompt Assembly Rules

- base instructions stable + inspectable
- isolate dynamic context from static guidance
- no hidden instruction injection paths
- config layer precedence explicit
- structured assembly over string concatenation spread across codebase

## Tool Surface Rules

- tool names, args, return shapes explicit
- validate input before execution, output before reuse
- distinguish read-only vs state-changing tools
- risky tools auditable + permission-gated
- no vague "do everything" tools hiding side effects

## Permission and Safety Rules

- non-trivial actions need clear approval path or safe default
- define blast radius before allowing writes, network calls, external effects
- prompt injection, stale memory, unsafe delegation = first-class risks
- fail closed for unsafe actions, fail open only for harmless convenience

## State and Context Rules

- stable snapshots over ad hoc prompt stuffing
- context growth bounded + measurable
- preserve enough state to resume/replay critical flows
- compact at logical boundaries, preserve key state before compaction

## Runtime Design Rules

- orchestration, lifecycle, state flow explicit + inspectable
- prompt assembly + tool execution integrated but replaceable
- record actions, results, events, retries, final outcomes
- enforce circuit breakers: max steps, retries, timeouts
- separate interactive turns from queued/background work
- idempotency, retry, cancellation rules explicit

## Scheduling, Sessions, and Recovery Rules

- define sync vs queued vs background
- turn lifecycle + session lifecycle distinct
- prevent duplicate/runaway execution
- preserve state for replay, audit, recovery
- delegation/worker spawning bounded + observable

## Essential Harness Checklist

### Entry and UI

- [ ] receive user input reliably
- [ ] stream output when supported
- [ ] show events, status, useful errors
- [ ] expose control commands: reset, help, tools, session actions

### Turn Runner

- [ ] coordinate one full turn end-to-end
- [ ] build context before model call
- [ ] detect + execute tool calls
- [ ] loop until final answer or stop condition
- [ ] enforce `max_steps`, cancellation, timeout

### Context Builder

- [ ] include base instructions
- [ ] include recent history
- [ ] include relevant memory only
- [ ] include mode/role instructions explicitly
- [ ] truncate or compact predictably

### Provider Adapter

- [ ] abstract model provider behind stable interface
- [ ] support streaming when available
- [ ] support tool/function calling
- [ ] support model config, timeout, retry, fallback
- [ ] support OpenAI-like, Anthropic-like, local, or other adapters when needed

### Tools

- [ ] register tools explicitly
- [ ] define clear schemas + descriptions
- [ ] support sync or async execution
- [ ] normalize return values + errors
- [ ] group tools into clear toolsets when surface grows

### Policy and Approvals

- [ ] classify actions: auto, confirm, deny
- [ ] guard by command, argument, path, or scope
- [ ] require approval for risky actions
- [ ] audit allowed + denied

### Hooks and Middleware

- [ ] hooks before/after model execution
- [ ] hooks before/after tools
- [ ] hooks at turn start/end
- [ ] hooks for logging, tracing, metrics, redaction, extensions without polluting core

### Session, State, and Memory

- [ ] persist session history
- [ ] support reset, resume, transcript export
- [ ] session metadata explicit
- [ ] separate short-term vs persistent memory
- [ ] deduplicate + control what gets stored

### Scheduling and Work Management

- [ ] define sync vs queued vs background
- [ ] separate short-lived user turns from long-running jobs
- [ ] prevent duplicate/runaway execution
- [ ] retries, idempotency, cancellation rules explicit

### Reliability and Evaluation

- [ ] keep regression fixtures or replay cases
- [ ] test failure recovery + timeout paths
- [ ] track latency, error rates, operational health
- [ ] make risky changes observable before rollout

### Observability and Security

- [ ] log events, tool calls, errors, timing, token/cost data when relevant
- [ ] validate paths + dangerous arguments
- [ ] keep secrets + config out of code
- [ ] bound writes, execution, network access

### Testability

- [ ] mock provider
- [ ] mock tool execution
- [ ] test turn running
- [ ] test policy + approval paths
- [ ] test hooks, parser recovery, retry, regression traces

## Testing Focus

<!-- - prompt assembly precedence -->
<!-- - tool schema validation -->
<!-- - permission decisions -->
<!-- - malformed output and parser recovery -->
<!-- - retry, timeout, and max-step behavior -->
<!-- - session recovery and long-running job behavior -->
<!-- - regression replay against saved traces -->

## Environment Variables

<!-- | Variable | Description | Required | -->
<!-- |----------|-------------|----------| -->

## Project-Specific Guardrails

<!-- - No hidden tool execution paths -->
<!-- - All permission decisions must be explainable -->
<!-- - Prompt changes require regression replay -->
<!-- - Session state must be restorable after compaction -->