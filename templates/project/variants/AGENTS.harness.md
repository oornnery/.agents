# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!--
Harness and runtime overlay.
Use for projects that turn model calls into an operational agent system with
context building, tools, permissions, sessions, memory, traces, and execution
control over time.
-->

## Project Description

<!-- Brief description of what the harness wraps, what it delegates, and what
its highest-risk surfaces are -->

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
- assemble instructions predictably from explicit sources
- expose a closed tool surface with documented schemas
- validate and permission tool requests before execution
- record tool calls, outputs, retries, and final answers explicitly
- bound execution with limits such as steps, retries, and timeouts
- preserve enough trace data to debug failures and regressions
- keep turn flow, session flow, and long-running execution visible and auditable
- separate immediate user turns from long-running jobs, retries, or worker
  tasks

## Preferred Libraries

- use `PydanticAI` as the default harness layer when the project is model-first
  and tool-using
- use `Pydantic` for request, tool, config, and structured output models
- use `HTTPX` for provider calls, external APIs, callbacks, and testable HTTP
  integrations
- keep provider adapters, tool contracts, and parser logic explicit even when a
  framework already supplies conveniences

## Design Boundary

- harness = turn-level context building, tool calling, parsing, approvals, and
  model interaction
- runtime = session-level execution, workers, retries, queues, recovery, and
  orchestration over time
- in most agent projects these boundaries stay tightly coupled, so this overlay
  treats them as one operational system
- keep the interfaces between harness pieces explicit even when they live in the
  same codebase

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

- keep base instructions stable and easy to inspect
- isolate dynamic context from static guidance
- avoid hidden instruction injection paths
- make precedence between config layers explicit
- prefer structured assembly over string concatenation spread across the codebase

## Tool Surface Rules

- keep tool names, args, and return shapes explicit
- validate input before execution and validate output before reuse
- distinguish read-only tools from state-changing tools
- make risky tools auditable and permission-gated
- avoid vague “do everything” tools that hide side effects

## Permission and Safety Rules

- every non-trivial action should have a clear approval path or safe default
- define blast radius before allowing writes, network calls, or external effects
- treat prompt injection, stale memory, and unsafe delegation as first-class risks
- fail closed for unsafe actions and fail open only for harmless convenience behavior

## State and Context Rules

- prefer stable snapshots over ad hoc prompt stuffing
- keep context growth bounded and measurable
- preserve enough state to resume or replay critical flows
- compact only at logical boundaries and preserve key state before compaction

## Runtime Design Rules

- keep orchestration, lifecycle, and state flow explicit and inspectable
- keep prompt assembly and tool execution integrated but replaceable
- record actions, results, events, retries, and final outcomes explicitly
- enforce circuit breakers such as max steps, retries, and timeouts
- separate interactive turns from queued or background work
- make idempotency, retry, and cancellation rules explicit

## Scheduling, Sessions, and Recovery Rules

- define what is synchronous, queued, or background
- keep turn lifecycle and session lifecycle distinct
- prevent duplicate or runaway execution
- preserve enough state for replay, audit, and recovery
- make delegation or worker spawning bounded and observable if used

## Essential Harness Checklist

### Entry and UI

- [ ] receive user input reliably
- [ ] stream output when supported
- [ ] show events, status, and useful errors
- [ ] expose control commands such as reset, help, tools, or session actions

### Turn Runner

- [ ] coordinate one full turn end-to-end
- [ ] build context before the model call
- [ ] detect and execute tool calls
- [ ] loop until final answer or stop condition
- [ ] enforce `max_steps`, cancellation, and timeout behavior

### Context Builder

- [ ] include base instructions
- [ ] include recent history
- [ ] include relevant memory only
- [ ] include mode or role instructions explicitly
- [ ] truncate or compact predictably

### Provider Adapter

- [ ] abstract the model provider behind a stable interface
- [ ] support streaming when available
- [ ] support tool or function calling
- [ ] support model config, timeout, retry, and fallback
- [ ] support OpenAI-like, Anthropic-like, local, or other adapters when needed

### Tools

- [ ] register tools explicitly
- [ ] define clear schemas and descriptions
- [ ] support sync or async execution
- [ ] normalize return values and errors
- [ ] group tools into clear toolsets when the surface grows

### Policy and Approvals

- [ ] classify actions as auto, confirm, or deny
- [ ] guard by command, argument, path, or scope
- [ ] require approval for risky actions
- [ ] audit what was allowed and denied

### Hooks and Middleware

- [ ] support hooks before and after model execution
- [ ] support hooks before and after tools
- [ ] support hooks at turn start and end
- [ ] use hooks for logging, tracing, metrics, redaction, and extensions without polluting the core

### Session, State, and Memory

- [ ] persist session history
- [ ] support reset, resume, and transcript export
- [ ] keep session metadata explicit
- [ ] separate short-term memory from persistent memory
- [ ] deduplicate and control what gets stored

### Scheduling and Work Management

- [ ] define whether work is synchronous, queued, or background
- [ ] separate short-lived user turns from long-running jobs
- [ ] prevent duplicate or runaway execution
- [ ] make retries, idempotency, and cancellation rules explicit

### Reliability and Evaluation

- [ ] keep regression fixtures or replay cases
- [ ] test failure recovery and timeout paths
- [ ] track latency, error rates, and operational health
- [ ] make risky changes observable before rollout

### Observability and Security

- [ ] log events, tool calls, errors, timing, and token or cost data when relevant
- [ ] validate paths and dangerous arguments
- [ ] keep secrets and config out of code
- [ ] bound writes, execution, and network access

### Testability

- [ ] mock the provider
- [ ] mock tool execution
- [ ] test turn running
- [ ] test policy and approval paths
- [ ] test hooks, parser recovery, retry behavior, and regression traces

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
