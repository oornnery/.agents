---
name: building-agents
description: Building tool-using LLM agents in Python -- runtime context, prompt shape, tools, validation, parsing, context reduction, memory, delegation. Load when designing or implementing agents, ReAct loops, or multi-agent systems.
---

# Building Tool-Using Agents in Python

A field guide for building **LLM agents** — systems that reason over context, call tools, persist state, and act inside a bounded runtime.

## Boundary

Use this skill for agent runtime architecture: context collection, prompt
shape, tool contracts, parsing, permissioning, context reduction, memory, and
delegation.

- pair with `python` for repo-specific Python implementation conventions and toolchain
- pair with `arch` when the agent runtime must fit a broader system architecture or SDD
- pair with `security` when tool risk, approval gates, trust boundaries, or threat modeling matter
- pair with `quality` when adding eval loops, regression checks, or RCA after agent failures
- pair with `docs` when the deliverable is a design doc or operational guide rather than the runtime itself

This skill should own the harness and control loop. It should not become a
grab-bag for every general Python, architecture, or security rule.

## Assets

Use these when a repo-shaped example is more useful than another excerpt.

- `assets/project/pyproject.toml` -- a small Python agent project setup
- `assets/project/main.py` -- the app entrypoint for a simple agent runtime
- `assets/project/agent.py` -- agent construction and result typing
- `assets/project/tools.py` -- tool registration and implementations
- `assets/project/session.py` -- session memory and transcript shaping
- `assets/project/tests/test_agent.py` -- a small test surface for the runtime

## The mental model

An agent is a **runtime harness** around an LLM that does the practical work of:

1. collecting relevant runtime context
2. building a stable prompt
3. exposing a closed set of tools the model can call
4. validating and permissioning every action
5. parsing the model's response into a structured intent
6. managing context growth so the prompt does not explode
7. persisting state between turns
8. optionally delegating bounded work to subagents

The model itself should do exactly one thing: emit either _a tool call_ or _a final answer_. Everything else is the harness. The famous quote applies: **"a lot of apparent model quality is really context quality."**

The control flow is the classic **ReAct loop**:

```text
user input
   │
   ▼
collect context
   │
   ▼
build prompt
   │
   ▼
call model
   │
   ▼
parse response
   │
   ├──► tool call ──► validate ──► approve ──► execute ──► record ──┐
   │                                                                 │
   ├──► retry notice ──► record ──────────────────────────────────────┤
   │                                                                 │
   └──► final answer ──► record ──► return to user                   │
                                                                     │
   ◄─────────────────────────────────────────────────────────────────┘
```

Two things make this loop production-grade rather than a toy:

- **Circuit breakers** — `max_steps` and `max_attempts` so the agent cannot loop forever.
- **Self-healing parser** — when the model emits malformed output, the runtime returns a `retry` notice the model sees on the next turn, instead of crashing.

Everything below is _how to make each box in that diagram good_.

---

## The eight components

### 1. Runtime context

**Why it matters.** "Fix the failing tests" is meaningless without knowing which repo, which branch, which test runner. "Schedule a meeting" is meaningless without knowing the user's calendar and time zone. The agent should never start blind.

**What goes in context depends on the domain**, but the shape is always the same: an **immutable snapshot** with a **render method** that produces text for the prompt.

For a generic agent, runtime context may include:

- current working directory
- active task or user goal
- user preferences
- environment metadata (OS, time zone, locale)
- available tools and connectors
- relevant files, documents, or memories
- recent activity summary

For a **coding agent specifically**, it includes:

- resolved repo root (`git rev-parse --show-toplevel`)
- current branch and default branch
- `git status` (short form) and recent commits
- contents of anchor files: `templates/project/variants/AGENTS.base.md`,
  project `AGENTS.*.md` variants, `README.md`, `pyproject.toml`, `package.json`

**Generic implementation.** Use `dataclass(frozen=True, slots=True)` for the immutable snapshot, `pathlib.Path` for filesystem work, and a `render` method that returns the prompt-ready text.

```python
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class RuntimeContext:
    cwd: Path
    summary: str = ""
    environment: dict[str, str] = field(default_factory=dict)
    resources: dict[str, str] = field(default_factory=dict)

    def render(self) -> str:
        parts = [f"cwd: {self.cwd}"]
        if self.summary:
            parts.append(f"summary: {self.summary}")
        if self.environment:
            env = ", ".join(f"{k}={v}" for k, v in self.environment.items())
            parts.append(f"environment: {env}")
        if self.resources:
            parts.append("resources:")
            parts.extend(f"  - {k}: {v}" for k, v in self.resources.items())
        return "\n".join(parts)
```

**Coding-agent specialization.** Same shape, more fields:

```python
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

ANCHOR_FILES = (
    "templates/project/variants/AGENTS.base.md",
    "README.md",
    "pyproject.toml",
    "package.json",
)
DOC_SNIPPET_LIMIT = 1200


def _git(args: list[str], cwd: Path, fallback: str = "") -> str:
    """Run git silently. Return stdout or fallback on any failure."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
    except (subprocess.SubprocessError, FileNotFoundError):
        return fallback
    return result.stdout.strip() or fallback


@dataclass(frozen=True, slots=True)
class WorkspaceContext:
    cwd: Path
    repo_root: Path
    branch: str
    status: str
    recent_commits: tuple[str, ...]
    project_docs: dict[str, str] = field(default_factory=dict)

    @classmethod
    def discover(cls, cwd: Path | str = ".") -> WorkspaceContext:
        cwd = Path(cwd).resolve()
        repo_root = Path(_git(["rev-parse", "--show-toplevel"], cwd, str(cwd))).resolve()

        docs: dict[str, str] = {}
        for name in ANCHOR_FILES:
            path = repo_root / name
            if path.is_file():
                text = path.read_text(encoding="utf-8", errors="replace")
                docs[name] = text[:DOC_SNIPPET_LIMIT]

        return cls(
            cwd=cwd,
            repo_root=repo_root,
            branch=_git(["branch", "--show-current"], cwd, "-"),
            status=_git(["status", "--short"], cwd, "clean"),
            recent_commits=tuple(_git(["log", "--oneline", "-5"], cwd).splitlines()),
            project_docs=docs,
        )

    def render(self) -> str:
        commits = "\n".join(f"  - {c}" for c in self.recent_commits) or "  - none"
        docs = "\n".join(f"## {name}\n{body}" for name, body in self.project_docs.items())
        return (
            f"Workspace:\n"
            f"  cwd: {self.cwd}\n"
            f"  repo_root: {self.repo_root}\n"
            f"  branch: {self.branch}\n"
            f"  status:\n{self.status}\n"
            f"  recent_commits:\n{commits}\n"
            f"  project_docs:\n{docs}"
        )
```

---

### 2. Prompt shape and cache reuse

**Why it matters.** Agent sessions are repetitive. Tool definitions, agent rules, and runtime context barely change between turns. Rebuilding them from scratch every call wastes tokens and breaks **prompt caching** on commercial APIs (Anthropic and OpenAI both reward identical prefixes — typically ~10% of input cost on hits).

**The pattern.** Split the prompt into a _stable prefix_ and a _volatile suffix_:

```text
┌─────────────────────────────────┐
│  STABLE PREFIX (built once)     │
│  - agent rules                  │
│  - tool descriptions            │
│  - role / operating mode        │
│  - runtime context              │
├─────────────────────────────────┤
│  VOLATILE SUFFIX (every turn)   │
│  - working memory               │
│  - compacted transcript         │
│  - current user message         │
└─────────────────────────────────┘
```

**Implementation.**

```python
from textwrap import dedent

AGENT_RULES = dedent("""\
    You are an agent. Rules:
    - Use tools instead of guessing about the world.
    - Return exactly one <tool>...</tool> or one <final>...</final>.
    - Never invent tool results.
    - Required tool arguments must not be empty.
    - Do not repeat the same tool call with the same arguments.
""").strip()


def build_stable_prefix(context: RuntimeContext, tools: dict[str, "Tool"]) -> str:
    tool_lines = "\n".join(
        f"- {name}({tool.signature}) [{tool.risk}] {tool.description}"
        for name, tool in tools.items()
    )
    return f"{AGENT_RULES}\n\nTools:\n{tool_lines}\n\nContext:\n{context.render()}"


def build_prompt(prefix: str, memory: str, transcript: str, user_message: str) -> str:
    return (
        f"{prefix}\n\n"
        f"Memory:\n{memory}\n\n"
        f"Transcript:\n{transcript}\n\n"
        f"User: {user_message}"
    )
```

The prefix is computed **once** in the agent's `__post_init__` and stored. Only `build_prompt` runs per turn. With Anthropic's API you would mark the prefix portion with `cache_control={"type": "ephemeral"}`; with OpenAI, identical prefixes are auto-cached.

---

### 3. Structured tools

**Why it matters.** Letting a model emit arbitrary shell commands is reckless. The harness should expose a **closed set of named tools** with typed inputs, descriptions, and risk flags.

**Generic tool examples** that show up in many domains:

| Tool                                                            | Domain                           |
| --------------------------------------------------------------- | -------------------------------- |
| `read_file`, `write_file`, `patch_file`, `list_files`, `search` | coding, ops, research            |
| `run_shell`                                                     | coding, ops                      |
| `fetch_url`, `web_search`                                       | research, personal assistant     |
| `query_memory`, `save_note`                                     | personal assistant, RAG          |
| `create_task`, `list_tasks`, `complete_task`                    | personal assistant, project ops  |
| `call_api`                                                      | automation, integration          |
| `delegate`                                                      | every agent that needs subagents |

**The pythonic shape.** A `Tool` is a frozen dataclass with a callable. The registry is a plain `dict[str, Tool]`. No metaclass, no plugin system, no `BaseTool → AbstractTool → ConcreteTool` hierarchy. **Flat is better than nested.**

```python
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal

Risk = Literal["safe", "risky"]


@dataclass(frozen=True, slots=True)
class Tool:
    name: str
    description: str
    signature: str   # human-readable, e.g. "path: str, start: int = 1"
    risk: Risk
    run: Callable[[dict[str, Any]], str]
```

**Building a tool** is just a function that returns a `Tool`. Closures capture whatever resources the tool needs (workspace, http client, db handle) without globals.

```python
def make_read_file_tool(workspace: WorkspaceContext) -> Tool:
    def run(args: dict[str, Any]) -> str:
        path = safe_path(workspace.repo_root, args["path"])
        start = int(args.get("start", 1))
        end = int(args.get("end", 200))
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        return "\n".join(
            f"{i:>4}: {line}"
            for i, line in enumerate(lines[start - 1 : end], start)
        )

    return Tool(
        name="read_file",
        description="Read a UTF-8 file by line range.",
        signature="path: str, start: int = 1, end: int = 200",
        risk="safe",
        run=run,
    )


def make_fetch_url_tool(http_client: "HttpClient") -> Tool:
    def run(args: dict[str, Any]) -> str:
        return http_client.get(args["url"]).text[:5000]

    return Tool(
        name="fetch_url",
        description="Fetch the contents of a URL.",
        signature="url: str",
        risk="safe",
        run=run,
    )


tools: dict[str, Tool] = {
    "read_file": make_read_file_tool(workspace),
    "fetch_url": make_fetch_url_tool(http),
    # ...
}
```

---

### 4. Validation and permissions

**Why it matters.** The model **suggests** actions. The runtime **decides** whether they are valid and allowed. This separation is the most important distinction in safe agent design.

**Validation should check:**

- the tool exists
- required arguments are present and non-empty
- argument types and shapes are acceptable
- paths stay inside allowed roots
- network calls hit allowed domains
- mutations require approval if needed
- recursion / delegation depth is bounded

**The two non-negotiable safety primitives for any agent that touches a filesystem:**

**Path containment.** Every filesystem operation must verify the resolved path stays inside the workspace. This is the single most common bug in homebrew agents.

```python
from pathlib import Path


def safe_path(root: Path, raw: str) -> Path:
    """Resolve `raw` against `root`. Raise if it escapes."""
    candidate = Path(raw).resolve() if Path(raw).is_absolute() else (root / raw).resolve()
    try:
        candidate.relative_to(root)  # raises ValueError if outside
    except ValueError as exc:
        raise PermissionError(f"path escapes workspace: {raw}") from exc
    return candidate
```

`Path.relative_to` is the pythonic containment check — cleaner than `os.path.commonpath` string comparisons.

**Approval gating.** Risky tools require explicit consent. Use a `StrEnum`, not a callback hierarchy.

```python
from enum import StrEnum


class ApprovalPolicy(StrEnum):
    ASK = "ask"
    AUTO = "auto"
    NEVER = "never"


def approve(name: str, args: dict[str, Any], policy: ApprovalPolicy) -> bool:
    if policy is ApprovalPolicy.AUTO:
        return True
    if policy is ApprovalPolicy.NEVER:
        return False
    answer = input(f"approve {name} {args}? [y/N] ").strip().lower()
    return answer in {"y", "yes"}
```

**The dispatcher.** Wraps validation, approval, execution, and error capture in one place. Errors become _strings the model sees_, not exceptions that crash the loop — the model can self-correct on the next turn.

```python
def run_tool(
    name: str,
    args: dict[str, Any],
    tools: dict[str, Tool],
    policy: ApprovalPolicy,
) -> str:
    tool = tools.get(name)
    if tool is None:
        return f"error: unknown tool {name!r}"
    if tool.risk == "risky" and not approve(name, args, policy):
        return f"error: approval denied for {name}"
    try:
        return clip(tool.run(args))
    except (KeyError, ValueError, PermissionError) as exc:
        return f"error: {name} failed: {exc}"
```

This is the discipline that turns a fragile script into something you can leave running.

---

### 5. Parsing model output

**Why it matters.** The runtime needs a structured contract with the model. The simplest one is: every response is either _one tool call_ or _one final answer_.

Two viable formats:

- **JSON** inside `<tool>` tags — clean for simple args
- **XML attributes with body** — necessary for multi-line content (escaping newlines in JSON is painful)

```text
<tool>{"name":"search","args":{"query":"latest python release"}}</tool>

<tool name="write_file" path="hello.py"><content>
print("hello world")
</content></tool>

<final>The latest Python release is 3.13.</final>
```

**Implementation.** Compile the regexes at module level, use the walrus operator for the match-and-bind pattern, and return a tagged tuple the loop can branch on.

```python
import json
import re
from typing import Any, Literal

ParseKind = Literal["tool", "final", "retry"]
ParseResult = tuple[ParseKind, Any]

_TOOL_RE = re.compile(r"<tool>(?P<body>.*?)</tool>", re.DOTALL)
_FINAL_RE = re.compile(r"<final>(?P<body>.*?)</final>", re.DOTALL)


def parse_response(raw: str) -> ParseResult:
    if match := _TOOL_RE.search(raw):
        try:
            payload = json.loads(match.group("body"))
        except json.JSONDecodeError:
            return "retry", "tool block was not valid JSON"
        if not isinstance(payload, dict) or "name" not in payload:
            return "retry", "tool payload missing name"
        return "tool", payload

    if match := _FINAL_RE.search(raw):
        return "final", match.group("body").strip()

    return "retry", "no <tool> or <final> tag found"
```

**The `retry` branch is critical.** Instead of raising, it produces a message the model sees on the next turn so it can fix its own mistake. This single design choice makes agents survive flaky models.

---

### 6. Context reduction (defeating bloat)

**Why it matters.** A naive agent reads three large files, runs three test suites, and suddenly the prompt is 80k tokens. This is the most underrated component — a lot of apparent "agent intelligence" is really good context hygiene.

Two strategies, both small.

**Clipping.** Cap any single piece of text. Show the head, mark the truncation.

```python
MAX_TOOL_OUTPUT = 4000


def clip(text: str, limit: int = MAX_TOOL_OUTPUT) -> str:
    if len(text) <= limit:
        return text
    return f"{text[:limit]}\n...[truncated {len(text) - limit} chars]"
```

**Recency-weighted transcript with deduplication.** Recent events get full fidelity; older ones get aggressively compressed; duplicate file reads from earlier in the session are dropped entirely.

```python
from typing import Any

RECENT_WINDOW = 6
RECENT_LIMIT = 900
OLD_LIMIT = 180
MAX_HISTORY = 12_000


def render_history(history: list[dict[str, Any]]) -> str:
    if not history:
        return "- empty"

    seen_reads: set[str] = set()
    recent_start = max(0, len(history) - RECENT_WINDOW)
    lines: list[str] = []

    for i, item in enumerate(history):
        is_recent = i >= recent_start

        # dedupe old read_file calls — they bloat fast
        if not is_recent and item.get("tool") == "read_file":
            path = str(item.get("args", {}).get("path", ""))
            if path in seen_reads:
                continue
            seen_reads.add(path)

        limit = RECENT_LIMIT if is_recent else OLD_LIMIT
        lines.append(f"[{item['role']}] {clip(item['content'], limit)}")

    return clip("\n".join(lines), MAX_HISTORY)
```

This is the "boring" component. It is also what separates an agent that survives 30 turns from one that derails at turn 8.

---

### 7. Sessions and working memory

**Why it matters.** Two layers, two jobs:

- **Full transcript** — durable, append-only, lives on disk as JSON. Used for resuming sessions and for compacting into the prompt.
- **Working memory** — small, distilled, mutable. Holds the current task, the last few touched resources, and a handful of notes. Goes into the prompt directly each turn.

A useful analogy: the transcript is your hard drive, the working memory is your RAM.

**Pythonic separation of concerns.** Dataclasses hold the data; a `SessionStore` handles persistence. No ORM, no lock files — `Path.write_text` with JSON is enough until you need more.

```python
import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class WorkingMemory:
    task: str = ""
    files: list[str] = field(default_factory=list)   # for coding agents
    entities: list[str] = field(default_factory=list)  # for personal assistants
    notes: list[str] = field(default_factory=list)

    def remember(self, bucket: list[str], item: str, limit: int) -> None:
        if not item:
            return
        if item in bucket:
            bucket.remove(item)
        bucket.append(item)
        del bucket[:-limit]

    def render(self) -> str:
        return (
            f"task: {self.task or '-'}\n"
            f"files: {', '.join(self.files) or '-'}\n"
            f"entities: {', '.join(self.entities) or '-'}\n"
            f"notes:\n" + ("\n".join(f"  - {n}" for n in self.notes) or "  - none")
        )


@dataclass(slots=True)
class Session:
    id: str = field(
        default_factory=lambda: f"{datetime.now():%Y%m%d-%H%M%S}-{uuid.uuid4().hex[:6]}"
    )
    created_at: str = field(default_factory=utcnow)
    history: list[dict[str, Any]] = field(default_factory=list)
    memory: WorkingMemory = field(default_factory=WorkingMemory)


class SessionStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, session_id: str) -> Path:
        return self.root / f"{session_id}.json"

    def save(self, session: Session) -> None:
        self._path(session.id).write_text(
            json.dumps(asdict(session), indent=2),
            encoding="utf-8",
        )

    def load(self, session_id: str) -> Session:
        data = json.loads(self._path(session_id).read_text(encoding="utf-8"))
        memory = WorkingMemory(**data.pop("memory"))
        return Session(memory=memory, **data)

    def latest(self) -> str | None:
        files = sorted(self.root.glob("*.json"), key=lambda p: p.stat().st_mtime)
        return files[-1].stem if files else None
```

`asdict` from `dataclasses` handles JSON serialization for free. Use `pathlib` everywhere instead of `os.path`.

---

### 8. Bounded delegation

**Why it matters.** When the main agent is mid-task and needs to answer a side question — _"which file defines this symbol?"_, _"what does this URL say?"_, _"verify this hypothesis"_ — spawning a **subagent** keeps the main transcript clean and parallelizes work. But unbounded subagents become the same problem twice.

**The constraints that make it safe:**

- `read_only=True` — subagents cannot mutate state
- `approval_policy=NEVER` — no human in the loop for the child
- `max_depth` — children cannot recurse past a small limit (typically 1)
- smaller `max_steps` — bounded work budget
- a summary of the parent's history is passed in, but the child has its own `Session`
- often, a narrower tool subset

```python
def delegate(parent: "Agent", task: str, max_steps: int = 3) -> str:
    if parent.depth >= parent.max_depth:
        raise PermissionError("delegate depth exceeded")

    child = Agent(
        model=parent.model,
        tools=parent.read_only_tools(),
        store=parent.store,
        context=parent.context,
        depth=parent.depth + 1,
        max_depth=parent.max_depth,
        max_steps=max_steps,
        read_only=True,
        approval_policy=ApprovalPolicy.NEVER,
    )
    child.session.memory.task = task
    child.session.memory.notes = [clip(render_history(parent.session.history), 300)]
    return f"delegate_result:\n{child.ask(task)}"
```

The same `Agent` class is used recursively — the bounding is just construction parameters. **No `SubAgent` subclass is needed.** Subagents are useful when they reduce noise in the main loop, not because they are "smarter."

---

## The full agent loop

Everything above feeds into one method. This is `Agent.ask`, ≈50 lines, the heart of the harness.

```python
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Agent:
    model: "ModelClient"
    tools: dict[str, Tool]
    store: SessionStore
    context: RuntimeContext
    session: Session = field(default_factory=Session)
    approval_policy: ApprovalPolicy = ApprovalPolicy.ASK
    max_steps: int = 6
    depth: int = 0
    max_depth: int = 1
    read_only: bool = False

    def __post_init__(self) -> None:
        self._prefix = build_stable_prefix(self.context, self.tools)

    def ask(self, user_message: str) -> str:
        if not self.session.memory.task:
            self.session.memory.task = user_message[:300]
        self._record({"role": "user", "content": user_message, "at": utcnow()})

        for _ in range(self.max_steps):
            prompt = build_prompt(
                self._prefix,
                self.session.memory.render(),
                render_history(self.session.history),
                user_message,
            )
            raw = self.model.complete(prompt)
            kind, payload = parse_response(raw)

            if kind == "final":
                self._record({"role": "assistant", "content": payload, "at": utcnow()})
                return payload

            if kind == "retry":
                self._record({
                    "role": "assistant",
                    "content": f"[retry] {payload}",
                    "at": utcnow(),
                })
                continue

            # tool call
            result = run_tool(
                payload["name"],
                payload.get("args", {}),
                self.tools,
                self.approval_policy,
            )
            self._record({
                "role": "tool",
                "tool": payload["name"],
                "args": payload.get("args", {}),
                "content": result,
                "at": utcnow(),
            })
            self._note_tool(payload["name"], payload.get("args", {}), result)

        return "Stopped after reaching the step limit without a final answer."

    def _record(self, item: dict[str, Any]) -> None:
        self.session.history.append(item)
        self.store.save(self.session)

    def _note_tool(self, name: str, args: dict[str, Any], result: str) -> None:
        if name in {"read_file", "write_file", "patch_file"} and "path" in args:
            self.session.memory.remember(self.session.memory.files, str(args["path"]), 8)
        snippet = clip(result.replace("\n", " "), 220)
        self.session.memory.remember(self.session.memory.notes, f"{name}: {snippet}", 5)
```

That is the entire agent. Every other piece — `RuntimeContext`, `Tool`, `Session`, `parse_response` — is supporting it.

**The `ModelClient` protocol** is a one-method `Protocol` so you can swap implementations (Ollama, Anthropic, OpenAI, OpenRouter, a fake for tests) without touching the agent:

```python
from typing import Protocol


class ModelClient(Protocol):
    def complete(self, prompt: str, max_new_tokens: int = 512) -> str: ...
```

The canonical test pattern is a `FakeModelClient` that returns canned outputs from a list — that is how `mini-coding-agent` does its tests, and it is the right pattern.

---

---

## Specialization recipes

The base agent above is intentionally generic. Here is how to specialize it for the four most common domains.

### Coding agent

**Replace `RuntimeContext` with `WorkspaceContext`** (the git-aware one shown in component 1).

**Tools to implement first:**

```python
tools = {
    "list_files":  make_list_files_tool(workspace),
    "read_file":   make_read_file_tool(workspace),
    "search":      make_search_tool(workspace),     # ripgrep with fallback
    "write_file":  make_write_file_tool(workspace), # risky
    "patch_file":  make_patch_file_tool(workspace), # risky, exact-string replace
    "run_shell":   make_run_shell_tool(workspace),  # risky, with timeout
    "delegate":    make_delegate_tool(),
}
```

**Working memory holds** the current task, the last 8 touched files, and the last 5 tool result notes.

**Reference implementation:** `rasbt/mini-coding-agent` is exactly this — read it.

### Research agent

**`RuntimeContext` holds** the user's question, the deadline, and known constraints.

**Tools to implement first:**

```python
tools = {
    "web_search":    make_web_search_tool(http),
    "fetch_url":     make_fetch_url_tool(http),
    "read_file":     make_read_file_tool(workspace),
    "save_note":     make_save_note_tool(notes_dir),
    "list_notes":    make_list_notes_tool(notes_dir),
    "delegate":      make_delegate_tool(),
}
```

**Working memory holds** the question, the current hypothesis, sources cited so far, and open subquestions. Aggressively dedupe URLs in `render_history`.

### Personal assistant

**`RuntimeContext` holds** the user's name, time zone, calendar handle, task list handle, and recent activity summary.

**Tools to implement first:**

```python
tools = {
    "list_tasks":    make_list_tasks_tool(tasks),
    "create_task":   make_create_task_tool(tasks),    # risky
    "complete_task": make_complete_task_tool(tasks),  # risky
    "query_memory":  make_query_memory_tool(memory_db),
    "save_note":     make_save_note_tool(notes_dir),
    "fetch_calendar": make_fetch_calendar_tool(cal),
    "web_search":    make_web_search_tool(http),
}
```

**Working memory holds** the active goal, the last few entities mentioned (people, projects, places), and recent decisions. Persist long-term memory to a separate store outside the session JSON.

### Ops / support agent

**`RuntimeContext` holds** the connected systems, the on-call schedule, and the active incident if any.

**Tools to implement first:**

```python
tools = {
    "query_logs":    make_query_logs_tool(loki),
    "query_metrics": make_query_metrics_tool(prom),
    "list_alerts":   make_list_alerts_tool(alertmanager),
    "run_runbook":   make_run_runbook_tool(runbooks),  # risky
    "page_oncall":   make_page_oncall_tool(pager),     # risky
    "post_status":   make_post_status_tool(slack),     # risky
}
```

**Approval policy is `ASK` by default for everything risky** — operators want a human in the loop on production.

**The same loop, the same parser, the same memory layer.** Specialization is just _which `Tool`s you put in the registry_ and _what fields go in the context_.

---

## Suggested project layout

The `mini_coding_agent.py` file is one script of ≈1000 lines on purpose — it is teaching material. For real work, split along the components.

**Generic agent runtime:**

```text
src/agent_runtime/
├── __init__.py
├── cli.py              # argparse + REPL
├── agent.py            # the Agent class and ask() loop
├── context.py          # RuntimeContext (specializable)
├── prompt.py           # build_stable_prefix, build_prompt, AGENT_RULES
├── parser.py           # parse_response, ParseKind types
├── compaction.py       # clip, render_history
├── permissions.py      # safe_path, approve, ApprovalPolicy
├── session.py          # Session, WorkingMemory, SessionStore
├── models/
│   ├── base.py         # ModelClient Protocol
│   ├── fake.py         # FakeModelClient for tests
│   ├── ollama.py
│   ├── anthropic.py    # native tool use
│   ├── openai.py
│   └── openrouter.py
└── tools/
    ├── base.py         # Tool dataclass, Risk type
    ├── fs.py           # read_file, write_file, patch_file, list_files
    ├── search.py       # ripgrep wrapper with fallback
    ├── shell.py        # run_shell with timeout
    ├── web.py          # fetch_url, web_search
    ├── memory.py       # query_memory, save_note
    ├── tasks.py        # create_task, list_tasks, complete_task
    └── delegate.py     # bounded subagent spawner
tests/
    test_parser.py
    test_permissions.py
    test_compaction.py
    test_loop.py        # uses FakeModelClient
```

**Specialization** lives in a thin layer on top:

```text
src/coding_agent/
├── workspace.py        # WorkspaceContext (git-aware)
├── tools.py            # registry assembling fs/search/shell tools
└── cli.py              # entrypoint that wires it together

src/personal_assistant/
├── context.py          # PersonalContext (calendar, time zone, prefs)
├── tools.py            # registry assembling memory/tasks/web tools
└── cli.py
```

**The runtime is shared. The specializations are 200 lines each.** This is the architecture lesson from `pi-mono` — separate provider, runtime, and domain so you can ship four different products from the same core.

---

## What to build first, what to defer

### Build now (v1)

- `RuntimeContext` (or specialized variant)
- `SessionStore` writing JSON
- `WorkingMemory` with LRU helpers
- The four-way parser (`tool` / `final` / `retry` / empty)
- A handful of core tools for your domain
- `safe_path` containment check (if touching files)
- `ApprovalPolicy` with `ask` / `auto` / `never`
- Recency-weighted `render_history`
- One read-only delegated subagent
- A `FakeModelClient` and pytest tests for the loop

That is a real agent. Stop here, use it for two weeks, then iterate.

### Defer (v2 and beyond)

- Persistent agent teams
- Background tasks
- Worktree isolation per task
- Web UI / Slack / Discord bridges
- Automatic risk classification
- Skill loading from directories
- Full MCP server with discovery and OAuth
- Streaming tool output
- Multi-model routing
- Workflow planner / executor split
- Stateful long-horizon orchestration

These show up in `pi-mono` and `learn-coding-agent` as **later layers**, not prerequisites. Adding them before the core loop is solid is a great way to ship a buggy framework instead of a working agent.

---

## References

The original sources this skill is built from:

- **Sebastian Raschka — _Components of A Coding Agent_** (the foundational article that defines the framing)
  [https://magazine.sebastianraschka.com/p/components-of-a-coding-agent](https://magazine.sebastianraschka.com/p/components-of-a-coding-agent)

- **Sebastian Raschka — video walkthrough**
  [https://www.youtube.com/watch?v=SQm3-NpOvJU&t=1098s](https://www.youtube.com/watch?v=SQm3-NpOvJU&t=1098s)

- **`rasbt/mini-coding-agent`** — the canonical ≈1000-line reference implementation in pure stdlib Python; the components in this skill map directly onto its code comments
  [https://github.com/rasbt/mini-coding-agent](https://github.com/rasbt/mini-coding-agent)
  [https://github.com/rasbt/mini-coding-agent/blob/main/mini_coding_agent.py](https://github.com/rasbt/mini-coding-agent/blob/main/mini_coding_agent.py)

- **`badlogic/pi-mono`** — production-grade modularization (unified LLM API, agent core, CLI, TUI, web UI, Slack bot, vLLM pods); the model for splitting a monolithic agent into reusable packages
  [https://github.com/badlogic/pi-mono/tree/main](https://github.com/badlogic/pi-mono/tree/main)

- **`sanbuphy/learn-coding-agent`** — research on Claude-Code-style architecture; documents the 12 progressive mechanisms beyond the basic loop (planning, knowledge on demand, background tasks, worktree isolation, etc.)
  [https://github.com/sanbuphy/learn-coding-agent](https://github.com/sanbuphy/learn-coding-agent)

- **`Leonxlnx/agentic-ai-prompt-research`** — reconstructed prompt patterns, agent coordination, and security classification from commercial agents; the source for _how_ the big systems write their system prompts
  [https://github.com/Leonxlnx/agentic-ai-prompt-research](https://github.com/Leonxlnx/agentic-ai-prompt-research)

- **The Zen of Python** — `python -c "import this"`

The recommended reading order is: Raschka's article first (mental model), then `mini-coding-agent` source (concrete reference), then `pi-mono` (modularization), then the prompt-research repo (how the commercial agents actually phrase things).
