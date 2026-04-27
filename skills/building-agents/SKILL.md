---
name: building-agents
description: Building tool-using LLM agents in Python -- runtime context, prompt shape, tools, validation, parsing, context reduction, memory, delegation. Load when designing or implementing agents, ReAct loops, or multi-agent systems.
---

# Building Tool-Using Agents in Python

Use for agent runtime architecture: context collection, prompt shape, tool contracts, parsing, permissioning, context reduction, memory, delegation.

## Boundary

- Pair with `python` for Python impl/toolchain.
- Pair with `arch` when runtime must fit system architecture or SDD.
- Pair with `security` for tool risk, approvals, trust boundaries, threat modeling.
- Pair with `quality` for eval loops, regression checks, RCA after agent failures.
- Pair with `docs` when deliverable is design/ops doc.
- Own harness + control loop. Do not absorb generic Python/arch/security rules.

## Assets

Use assets over inline examples when implementing:

- `assets/project/pyproject.toml` -- Python agent project setup
- `assets/project/main.py` -- entrypoint
- `assets/project/agent.py` -- agent construction/result typing
- `assets/project/tools.py` -- tool registry + implementations
- `assets/project/session.py` -- memory/transcript shaping
- `assets/project/tests/test_agent.py` -- runtime tests

## Mental Model

Agent = runtime harness around model. Model emits tool call or final answer; harness owns everything else.

Core loop:

1. collect runtime context
2. build stable prompt
3. call model
4. parse response as tool/final/retry
5. validate + approve tool call
6. execute + record result
7. reduce context/memory
8. stop on final or circuit breaker

Non-negotiables:

- `max_steps` and `max_attempts`; no infinite loops.
- Malformed output becomes retry notice; no crash.
- Tool results are recorded before next model call.
- Runtime decides; model only suggests.
- Apparent model quality is often context quality.

## Components

| Component         | Contract                                                                   |
| ----------------- | -------------------------------------------------------------------------- |
| Runtime context   | immutable snapshot + `render()` prompt text                                |
| Prompt shape      | stable prefix + volatile suffix; cache stable parts                        |
| Tools             | closed registry of typed `Tool` objects                                    |
| Validation        | check tool name, args, paths, domains, mutation risk, recursion/delegation |
| Permissions       | `ASK` / `AUTO` / `NEVER`; risky tools require approval                     |
| Parser            | one response = one tool call, one final answer, or retry                   |
| Context reduction | clip tool output, dedupe old reads, summarize old transcript               |
| Sessions          | append-only transcript + small working memory                              |
| Delegation        | bounded read-only child agents with smaller step budget and depth limit    |

## Runtime Context

Default shape:

- `dataclass(frozen=True, slots=True)`
- `pathlib.Path`
- domain fields only
- `render() -> str`

Coding context includes:

- repo root: `git rev-parse --show-toplevel`
- branch, short status, recent commits
- selected anchor docs: `AGENTS*`, `README.md`, manifests
- snippet limits for docs

Use assets for concrete code.

## Prompt Shape

Split prompt:

- stable prefix: rules, tools, operating mode, runtime context
- volatile suffix: working memory, compact transcript, current user message

Build stable prefix once. Cache if provider supports it; otherwise keep text identical for auto-cache hits.

Prompt rules:

- force exact output contract
- tell model to use tools over guessing
- forbid invented tool results
- forbid repeated same tool call/args
- require one `<tool>...</tool>` or one `<final>...</final>`

## Tools

Expose closed set of named tools. Avoid arbitrary command execution by default.

Tool contract:

- frozen dataclass
- `name`
- `description`
- human-readable `signature`
- `risk`: `safe` or `risky`
- `run(args: dict[str, Any]) -> str`

Common tools:

- coding: `list_files`, `read_file`, `search`, `write_file`, `patch_file`, `run_shell`
- research: `web_search`, `fetch_url`, `read_file`, `save_note`
- assistant: `list_tasks`, `create_task`, `complete_task`, `query_memory`
- ops: `query_logs`, `query_metrics`, `list_alerts`, `run_runbook`, `page_oncall`
- all domains: `delegate`

Flat registry beats plugin hierarchy until real extension pressure exists.

## Validation and Permissions

Validate before execution:

- tool exists
- required args present and non-empty
- arg types/shapes acceptable
- paths stay inside allowed roots
- network calls hit allowed domains
- risky mutations have approval
- recursion/delegation depth bounded

Filesystem invariant:

- resolve path
- compare against workspace root with `Path.relative_to`
- reject escapes

Approval invariant:

- `ASK`: ask human
- `AUTO`: allow
- `NEVER`: deny

Dispatcher owns validation, approval, execution, error capture. Return errors as strings the model can see and correct next turn.

## Parsing

Response contract: exactly one tool call or one final answer.

Supported formats:

- JSON inside `<tool>` for simple args
- XML attrs/body for multiline content
- `<final>...</final>` for final answer

Parser returns tagged result:

- `("tool", payload)`
- `("final", text)`
- `("retry", message)`

Retry message is recorded into next turn. This makes weak/malformed model output recoverable.

## Context Reduction

Context hygiene keeps agents alive after turn 8.

Rules:

- cap every tool output; mark truncation
- preserve recent events at higher fidelity
- compress older events aggressively
- dedupe repeated old reads
- keep working memory small and current
- separate stable prefix from volatile history

Suggested limits:

- tool output: ~4k chars
- recent item: ~900 chars
- old item: ~180 chars
- full rendered history: ~12k chars

## Sessions and Memory

Two layers:

- full transcript: durable append-only JSON for resume/compaction
- working memory: small mutable prompt state

Working memory tracks:

- current task
- recent files/entities
- decisions
- short notes from recent tool results

Use `Path.write_text` + JSON first. Add database only after persistence pressure is real.

## Delegation

Delegation reduces main transcript noise and parallelizes bounded side work.

Constraints:

- child is read-only by default
- child approval policy = `NEVER`
- `max_depth` small, usually `1`
- child `max_steps` smaller than parent
- pass summary of parent history, not whole transcript
- expose narrower tool subset

Do not create `SubAgent` subclass unless responsibilities truly diverge. Same `Agent` class with stricter config is enough.

## Full Agent Loop

`Agent.ask` should stay small:

1. record user message
2. build prompt from stable prefix + memory + rendered history
3. call model
4. parse result
5. on final: record + return
6. on retry: record retry notice + continue
7. on tool: dispatch, record tool result, update memory
8. stop at step limit

Use `ModelClient` `Protocol` with one method:

```python
class ModelClient(Protocol):
    def complete(self, prompt: str, max_new_tokens: int = 512) -> str: ...
```

Test loop with `FakeModelClient` returning canned outputs.

## Specialization Recipes

| Agent              | Context                                     | First Tools                                    | Memory                            |
| ------------------ | ------------------------------------------- | ---------------------------------------------- | --------------------------------- |
| Coding             | `WorkspaceContext`, git state, anchor docs  | files, search, patch/write, shell, delegate    | task, last files, tool notes      |
| Research           | question, deadline, constraints             | search, fetch, read, save/list notes, delegate | sources, hypotheses, subquestions |
| Personal assistant | user, time zone, calendar/tasks handles     | tasks, memory, notes, calendar, web            | goal, entities, decisions         |
| Ops/support        | connected systems, on-call, active incident | logs, metrics, alerts, runbook, page, status   | incident state, actions, evidence |

Risky prod tools use approval.

## Project Layout

Generic runtime:

```text
src/agent_runtime/
├── agent.py
├── context.py
├── prompt.py
├── parser.py
├── compaction.py
├── permissions.py
├── session.py
├── models/
└── tools/
tests/
```

Specializations stay thin:

```text
src/coding_agent/
├── workspace.py
├── tools.py
└── cli.py
```

Runtime shared. Domain layer chooses tools/context.

## Build Order

Build v1:

- runtime/specialized context
- JSON `SessionStore`
- `WorkingMemory`
- parser: tool/final/retry/empty
- core domain tools
- `safe_path` if touching files
- approval policy
- recency-weighted history
- one read-only delegated child
- fake model + pytest tests

Defer:

- persistent agent teams
- background tasks
- per-task worktrees
- web/Slack/Discord bridges
- automatic risk classification
- directory skill loading
- full MCP server/OAuth
- streaming tool output
- multi-model routing
- planner/executor split
- long-horizon orchestration

## References

- Raschka, _Components of Coding Agent_: <https://magazine.sebastianraschka.com/p/components-of-a-coding-agent>
- `rasbt/mini-coding-agent`: <https://github.com/rasbt/mini-coding-agent>
- `badlogic/pi-mono`: <https://github.com/badlogic/pi-mono/tree/main>
- `sanbuphy/learn-coding-agent`: <https://github.com/sanbuphy/learn-coding-agent>
- `Leonxlnx/agentic-ai-prompt-research`: <https://github.com/Leonxlnx/agentic-ai-prompt-research>
- Zen of Python: `python -c "import this"`
