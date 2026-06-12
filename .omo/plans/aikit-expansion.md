# AIKit Expansion — Reference Kit for AI Agents

## TL;DR

> **Quick Summary**: Expand `.aikit/` into a comprehensive, copyable reference kit for AI coding agents — filling empty directories with example-rich templates, completing the Python template, and creating Node.js TS + JS templates.
>
> **Deliverables**:
> - 6 filled `.md` reference directories (arch, plan, design, mem, spec, TODO)
> - Completed Python project template (7 files)
> - Node.js TypeScript template (14 files)
> - Node.js JavaScript template (13 files)
>
> **Estimated Effort**: Large
> **Parallel Execution**: YES — 4 waves (6 + 5 + 4 + 4 tasks)
> **Critical Path**: Wave 1 → Wave 2 → Wave 3 → Wave 4 → Final Review

---

## Context

### Original Request
Expand and improve `.aikit/` to be a reference kit for agents and `AGENTS.md` to assist agents in any project. Improve `.md` examples with design, plan, arch, mem, spec — adding examples and comments like already done in mem and spec. Finish and improve the Python template. Create Node.js (TS and JS) templates based on the Python one. Usage: download this aikit and copy to any project.

### Interview Summary
**Key Discussions**:
- Domain for all examples: Task Management API (API de Tarefas)
- Node.js stack: npm + Node, pure (no framework), utility libs OK
- Two separate Node.js templates: TypeScript and JavaScript
- Keep current directory structure (arch/, design/, mem/, plan/, spec/)
- Don't touch `AGENTS.md` or `init.sh`
- All content in English (shareable kit)
- HTML comments `<!-- -->` for explanatory notes in `.md` files

**Research Findings**:
- Python template uses: uv, ruff, ty, pyright, bandit, pytest, pre-commit, taskipy, rumdl
- Python template has hatchling build backend, Python 3.12+
- `pyproject.toml` references `src/` but no `src/` directory exists — needs creation
- `AGENTS.md` references `.mem/` and `.spec/` as operational state directories

### Metis Review
**Identified Gaps** (addressed):
- TODO.md was not mentioned → added to scope
- Cross-file coherence → all examples tell one consistent Task API story
- Python `src/` missing → create `src/myapp/` minimal structure
- Node.js directory structure → `templates/nodejs/ts/` and `templates/nodejs/js/`
- "Pure Node.js" ambiguity → no framework, but utility libs (zod, etc.) are fine
- Language → English for all content

---

## Work Objectives

### Core Objective
Transform `.aikit/` from a skeleton with empty directories into a fully populated, example-rich reference kit that any developer can copy into a new project and immediately understand how to use each file.

### Concrete Deliverables
- `arch/README.md` + `arch/ARCH.md` — architecture documentation template with Task API example
- `plan/README.md` + `plan/PLAN.md` — implementation plan template with Task API example
- `design/DESIGN.md` — filled with Task API example + explanatory comments
- `mem/hot.md`, `mem/decisions.md`, `mem/open-loops.md` — filled with Task API examples + comments
- `spec/SPEC.md`, `spec/state.md`, `spec/checks.md`, `spec/handoff.md` — filled with Task API examples + comments
- `TODO.md` — filled with Task API example
- Python template: `src/myapp/`, `tests/`, `docker/`, `.github/container.yml`, `README.md` completed
- Node.js TS template: full project scaffolding (14 files)
- Node.js JS template: full project scaffolding (13 files)

### Definition of Done
- [ ] All empty directories have README + filled template
- [ ] All `.md` templates have real examples (no `UNKNOWN` or `YYYY-MM-DD` in filled sections)
- [ ] All `.md` templates have `<!-- -->` explanatory comments
- [ ] Python template has no empty files
- [ ] Node.js TS template is copyable and `npm run check` passes
- [ ] Node.js JS template is copyable and `npm run check` passes
- [ ] All examples reference the same Task Management API domain

### Must Have
- Every `.md` file has both a template structure AND a filled example
- Explanatory comments explain WHY each section matters, not WHAT it is
- All examples are coherent (same Task API across all files)
- Templates are self-contained (copyable without other files)
- Node.js TS and JS are separate complete templates

### Must NOT Have (Guardrails)
- No changes to `.aikit/AGENTS.md`
- No changes to `.aikit/templates/python/scripts/init.sh`
- No changes to existing filled files (pyproject.toml, ci.yml, Dockerfile, ruff.toml, ty.toml, etc.)
- No new directories beyond what already exists (plus `nodejs/ts/` and `nodejs/js/`)
- No framework dependencies in Node.js templates (no Express, Fastify, Hono)
- No secrets, credentials, or real API keys in any file
- No Portuguese content (all English for shareability)
- No `UNKNOWN` or `YYYY-MM-DD` placeholders remaining in filled sections

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: N/A (this is template/doc creation, not app code)
- **Automated tests**: None (templates are verified by structure and content review)
- **Agent-Executed QA**: EVERY task includes QA scenarios

### QA Policy
Every task MUST include agent-executed QA scenarios:
- **Markdown files**: Read file, verify structure, check no remaining placeholders, verify comments exist
- **Config files**: Validate YAML/JSON syntax, check required fields present
- **Shell scripts**: Run `bash -n` syntax check
- **Docker files**: Validate YAML syntax with `docker compose config` (dry-run)
- Evidence saved to `.omo/evidence/task-{N}-{scenario-slug}.{ext}`

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — .md reference files, MAX PARALLEL):
├── Task 1: arch/ — README.md + ARCH.md [writing]
├── Task 2: plan/ — README.md + PLAN.md [writing]
├── Task 3: design/ — DESIGN.md filled [writing]
├── Task 4: mem/ — hot.md, decisions.md, open-loops.md filled [writing]
├── Task 5: spec/ — SPEC.md, state.md, checks.md, handoff.md filled [writing]
└── Task 6: TODO.md filled [writing]

Wave 2 (After Wave 1 — Python template completion):
├── Task 7: Python src/myapp/ structure [quick]
├── Task 8: Python tests/ files [quick]
├── Task 9: Python docker/ files [quick]
├── Task 10: Python .github/container.yml [quick]
└── Task 11: Python README.md [writing]

Wave 3 (After Wave 2 — Node.js TypeScript template):
├── Task 12: TS config files (package.json, tsconfig, eslint, vitest, prettier) [quick]
├── Task 13: TS source + tests (src/index.ts, tests/) [quick]
├── Task 14: TS infra (docker/, .github/ci.yml) [quick]
└── Task 15: TS misc (scripts/, README.md, .gitignore, .env.example) [writing]

Wave 4 (After Wave 3 — Node.js JavaScript template):
├── Task 16: JS config files (package.json, eslint, vitest, prettier) [quick]
├── Task 17: JS source + tests (src/index.js, tests/) [quick]
├── Task 18: JS infra (docker/, .github/ci.yml) [quick]
└── Task 19: JS misc (scripts/, README.md, .gitignore, .env.example) [writing]

Wave FINAL (After ALL tasks — 4 parallel reviews):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Content quality review (unspecified-high)
├── Task F3: Cross-file consistency check (deep)
└── Task F4: Template copyability test (unspecified-high)
-> Present results -> Get explicit user okay

Critical Path: Wave 1 → Wave 2 → Wave 3 → Wave 4 → F1-F4 → user okay
Parallel Speedup: ~60% faster than sequential (6+5+4+4 tasks in waves)
Max Concurrent: 6 (Wave 1)
```

### Dependency Matrix

- **1-6**: Independent — no dependencies, all can start immediately
- **7-11**: Independent of Wave 1, but grouped after for organizational clarity
- **12-15**: Independent of Waves 1-2, but grouped after for organizational clarity
- **16-19**: Independent of Waves 1-3, but grouped after for organizational clarity
- **F1-F4**: Depends on ALL implementation tasks (1-19)

### Agent Dispatch Summary

- **Wave 1**: 6 tasks → `writing`
- **Wave 2**: 5 tasks → `quick` (4) + `writing` (1)
- **Wave 3**: 4 tasks → `quick` (3) + `writing` (1)
- **Wave 4**: 4 tasks → `quick` (3) + `writing` (1)
- **FINAL**: 4 tasks → `oracle` (1) + `unspecified-high` (2) + `deep` (1)

---

## TODOs

> Implementation + Test = ONE Task. Never separate.
> EVERY task MUST have: Recommended Agent Profile + Parallelization info + QA Scenarios.
> **A task WITHOUT QA Scenarios is INCOMPLETE. No exceptions.**
> **FORMAT**: Task labels MUST use bare numbers: `1.`, `2.`, `3.` — NOT `T1.`, `Task 1.`, `Phase 1:`.

- [x] 1. Create arch/ directory documentation

  **What to do**:
  - Create `.aikit/arch/README.md` explaining the purpose of the arch/ directory (architecture documentation for projects)
  - Create `.aikit/arch/ARCH.md` as a filled template with a complete Task Management API architecture example
  - Include `<!-- -->` HTML comments explaining WHY each section matters (e.g., "<!-- Core boundaries define where responsibilities split. This prevents feature creep across modules. -->")
  - Sections to fill: System Overview, Core Boundaries, Data Flow, External Integrations, Runtime Assumptions, Technology Stack, Deployment Model
  - Use the Task Management API domain: REST API with tasks, users, authentication, PostgreSQL storage

  **Must NOT do**:
  - Do not modify any other directory
  - Do not add diagrams unless they clarify (text-based ASCII diagrams OK if needed)
  - Do not reference specific frameworks not in the Python/Node.js templates

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: none needed
  - **Reason**: Pure documentation authoring task

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2, 3, 4, 5, 6)
  - **Blocks**: None
  - **Blocked By**: None

  **References**:
  - `.aikit/mem/README.md` — pattern for directory README style (explains purpose, rules, file list)
  - `.aikit/spec/SPEC.md` — current template structure to understand what ARCH.md should complement
  - `.aikit/AGENTS.md:9-11` — "Preserve project conventions before introducing patterns" (guides architecture documentation philosophy)

  **Acceptance Criteria**:
  - [ ] `.aikit/arch/README.md` exists and explains directory purpose in ≤20 lines
  - [ ] `.aikit/arch/ARCH.md` exists with filled Task Management API example
  - [ ] ARCH.md contains at least 5 `<!-- -->` explanatory comments
  - [ ] No `UNKNOWN` or `YYYY-MM-DD` placeholders remain in filled sections
  - [ ] All content in English

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify arch/ files exist and have content
    Tool: Bash
    Steps:
      1. Run: wc -l .aikit/arch/README.md .aikit/arch/ARCH.md
      2. Assert: README.md has 10-25 lines
      3. Assert: ARCH.md has 80-200 lines
    Expected Result: Both files exist with substantial content
    Evidence: .omo/evidence/task-1-arch-files-exist.txt

  Scenario: Verify no placeholders remain
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c "UNKNOWN\|YYYY-MM-DD" .aikit/arch/ARCH.md
      2. Assert: count is 0
    Expected Result: No placeholder strings found
    Evidence: .omo/evidence/task-1-arch-no-placeholders.txt

  Scenario: Verify explanatory comments exist
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c "<!--" .aikit/arch/ARCH.md
      2. Assert: count >= 5
    Expected Result: At least 5 HTML comments explaining sections
    Evidence: .omo/evidence/task-1-arch-comments.txt
  ```

  **Commit**: NO (groups with Wave 1)

- [x] 2. Create plan/ directory documentation

  **What to do**:
  - Create `.aikit/plan/README.md` explaining the purpose of the plan/ directory (implementation planning documents)
  - Create `.aikit/plan/PLAN.md` as a filled template with a complete Task Management API implementation plan example
  - Include `<!-- -->` HTML comments explaining WHY each section matters
  - Sections to fill: Overview, Requirements, Structure Changes, Ordered Phases, File Paths, Dependencies, Risks, Testing Strategy, Success Criteria
  - Use the Task Management API domain: show a realistic multi-phase plan for building the API

  **Must NOT do**:
  - Do not modify any other directory
  - Do not create a plan that contradicts the arch/ARCH.md architecture
  - Do not include vague phases like "implement the backend" — be specific about files and interfaces

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 3, 4, 5, 6)
  - **Blocks**: None
  - **Blocked By**: None

  **References**:
  - `.aikit/AGENTS.md:164-200` — "When Planning a Feature" section shows the expected plan output shape
  - `.aikit/mem/README.md` — pattern for directory README style
  - `.aikit/spec/SPEC.md` — understand what spec defines so plan complements it

  **Acceptance Criteria**:
  - [ ] `.aikit/plan/README.md` exists and explains directory purpose in ≤20 lines
  - [ ] `.aikit/plan/PLAN.md` exists with filled Task Management API plan example
  - [ ] PLAN.md contains at least 5 `<!-- -->` explanatory comments
  - [ ] Plan has specific file paths, not vague descriptions
  - [ ] No `UNKNOWN` or `YYYY-MM-DD` placeholders remain

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify plan/ files exist and have content
    Tool: Bash
    Steps:
      1. Run: wc -l .aikit/plan/README.md .aikit/plan/PLAN.md
      2. Assert: README.md has 10-25 lines
      3. Assert: PLAN.md has 100-250 lines
    Expected Result: Both files exist with substantial content
    Evidence: .omo/evidence/task-2-plan-files-exist.txt

  Scenario: Verify plan has specific file paths
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c "\.py\|\.ts\|\.js\|src/" .aikit/plan/PLAN.md
      2. Assert: count >= 10
    Expected Result: Plan references specific files, not just abstract concepts
    Evidence: .omo/evidence/task-2-plan-specific-paths.txt

  Scenario: Verify explanatory comments exist
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c "<!--" .aikit/plan/PLAN.md
      2. Assert: count >= 5
    Expected Result: At least 5 HTML comments
    Evidence: .omo/evidence/task-2-plan-comments.txt
  ```

  **Commit**: NO (groups with Wave 1)

- [x] 3. Fill design/DESIGN.md with example and comments

  **What to do**:
  - Fill `.aikit/design/DESIGN.md` with a complete Task Management API design example
  - Add `<!-- -->` HTML comments explaining WHY each section matters
  - Fill all sections: Product Context, Architecture, UI and Interaction, API and Data Contracts, Design Decisions table, Risks, References
  - Design Decisions table should have 3-4 realistic entries (e.g., "Use JWT for auth", "PostgreSQL over SQLite", "REST over GraphQL")
  - API section should show concrete endpoints: POST /tasks, GET /tasks, PUT /tasks/:id, DELETE /tasks/:id

  **Must NOT do**:
  - Do not change the existing section headings (they are the template structure)
  - Do not add new sections beyond what exists
  - Do not remove the References section at the bottom

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2, 4, 5, 6)
  - **Blocks**: None
  - **Blocked By**: None

  **References**:
  - `.aikit/design/DESIGN.md` — current template structure (45 lines, sections already defined)
  - `.aikit/AGENTS.md:124-151` — "Structure and Boundaries" section for architecture guidance
  - `.aikit/templates/python/docker/Dockerfile` — shows the Python deployment pattern to reference

  **Acceptance Criteria**:
  - [ ] DESIGN.md has all sections filled with Task API content
  - [ ] Design Decisions table has at least 3 entries with Date, Decision, Reason, Impact
  - [ ] API section shows concrete endpoints with HTTP methods
  - [ ] At least 5 `<!-- -->` explanatory comments
  - [ ] No `UNKNOWN` or `YYYY-MM-DD` placeholders remain (except in the table template row if kept)

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify DESIGN.md is filled
    Tool: Bash
    Steps:
      1. Run: wc -l .aikit/design/DESIGN.md
      2. Assert: line count >= 80 (was 45 as template)
    Expected Result: File has grown substantially with filled content
    Evidence: .omo/evidence/task-3-design-filled.txt

  Scenario: Verify API endpoints are concrete
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c "GET\|POST\|PUT\|DELETE\|PATCH" .aikit/design/DESIGN.md
      2. Assert: count >= 4
    Expected Result: At least 4 HTTP method references in API section
    Evidence: .omo/evidence/task-3-design-api.txt

  Scenario: Verify Design Decisions table has entries
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c "^|" .aikit/design/DESIGN.md
      2. Assert: count >= 5 (header + separator + 3 entries)
    Expected Result: Table has real decision entries
    Evidence: .omo/evidence/task-3-design-decisions.txt
  ```

  **Commit**: NO (groups with Wave 1)

- [x] 4. Fill mem/ files with examples and comments

  **What to do**:
  - Fill `.aikit/mem/hot.md` with a Task Management API example: 5-8 stable facts about the project (stack, auth choice, DB, deployment target, key constraints)
  - Fill `.aikit/mem/decisions.md` with 3-4 accepted decisions (e.g., "Use PostgreSQL", "JWT over sessions", "REST over GraphQL") with rationale and impact
  - Fill `.aikit/mem/open-loops.md` with 2-3 unresolved questions (e.g., "Rate limiting strategy TBD", "WebSocket support evaluation")
  - Add `<!-- -->` HTML comments in each file explaining WHY that file matters and what kind of content belongs there
  - Keep hot.md under 80 lines (as per its own rule)

  **Must NOT do**:
  - Do not modify `.aikit/mem/README.md` (already good)
  - Do not exceed 80 lines in hot.md
  - Do not add secrets, real API keys, or credentials
  - Do not store session logs or raw transcripts

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2, 3, 5, 6)
  - **Blocks**: None
  - **Blocked By**: None

  **References**:
  - `.aikit/mem/README.md` — explains the temperature model (hot/decisions/open-loops) and rules
  - `.aikit/mem/hot.md` — current template (5 lines, just header + one UNKNOWN entry)
  - `.aikit/mem/decisions.md` — current template (18 lines, has table structure)
  - `.aikit/mem/open-loops.md` — current template (5 lines, has table structure)
  - `.aikit/AGENTS.md:501-519` — Memory Hierarchy section explains how .mem/ fits in the system

  **Acceptance Criteria**:
  - [ ] `hot.md` has 5-8 stable facts, ≤80 lines total
  - [ ] `decisions.md` has at least 3 accepted decisions with Date, Decision, Reason, Impact
  - [ ] `open-loops.md` has at least 2 unresolved questions with Date, Item, Owner, Next Action
  - [ ] Each file has at least 2 `<!-- -->` explanatory comments
  - [ ] No `UNKNOWN` or `YYYY-MM-DD` placeholders remain in filled sections
  - [ ] All content is coherent with the same Task Management API domain

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify mem/ files are filled
    Tool: Bash
    Steps:
      1. Run: wc -l .aikit/mem/hot.md .aikit/mem/decisions.md .aikit/mem/open-loops.md
      2. Assert: hot.md has 15-80 lines
      3. Assert: decisions.md has 30-60 lines
      4. Assert: open-loops.md has 10-20 lines
    Expected Result: All files have substantial content
    Evidence: .omo/evidence/task-4-mem-files-filled.txt

  Scenario: Verify hot.md stays under 80 lines
    Tool: Bash
    Steps:
      1. Run: wc -l < .aikit/mem/hot.md
      2. Assert: result <= 80
    Expected Result: hot.md respects its own size limit
    Evidence: .omo/evidence/task-4-mem-hot-limit.txt

  Scenario: Verify no placeholders remain
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c "UNKNOWN\|YYYY-MM-DD" .aikit/mem/hot.md .aikit/mem/decisions.md .aikit/mem/open-loops.md
      2. Assert: total count is 0
    Expected Result: No placeholder strings in any mem file
    Evidence: .omo/evidence/task-4-mem-no-placeholders.txt
  ```

  **Commit**: NO (groups with Wave 1)

- [x] 5. Fill spec/ files with examples and comments

  **What to do**:
  - Fill `.aikit/spec/SPEC.md` with a complete Task Management API spec: objective, scope (in/out), users/actors, requirements (functional, non-functional, security), success criteria, interfaces, constraints, validation plan
  - Fill `.aikit/spec/state.md` with current project state: active objective, scope, done items, next steps, validation status, open questions
  - Fill `.aikit/spec/checks.md` with validation commands table: format (ruff), lint (ruff), type (ty+pyright), tests (pytest), build (uv build), security (bandit) with actual commands
  - Fill `.aikit/spec/handoff.md` with a realistic handoff: context, current state, completed work, remaining work, validation status, risks
  - Add `<!-- -->` HTML comments explaining WHY each section matters

  **Must NOT do**:
  - Do not modify `.aikit/spec/README.md` (already good)
  - Do not change existing section headings
  - Do not add sections that don't exist in the templates

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2, 3, 4, 6)
  - **Blocks**: None
  - **Blocked By**: None

  **References**:
  - `.aikit/spec/README.md` — explains .spec/ purpose and rules
  - `.aikit/spec/SPEC.md` — current template (55 lines, all sections defined)
  - `.aikit/spec/state.md` — current template (46 lines, has frontmatter + sections)
  - `.aikit/spec/checks.md` — current template (24 lines, has validation commands table)
  - `.aikit/spec/handoff.md` — current template (25 lines, has sections)
  - `.aikit/AGENTS.md:501-519` — Memory Hierarchy section explains how .spec/ fits
  - `.aikit/templates/python/pyproject.toml:118-135` — taskipy tasks show actual validation commands to reference in checks.md

  **Acceptance Criteria**:
  - [ ] `SPEC.md` has all sections filled with Task API content (objective, scope, requirements, etc.)
  - [ ] `state.md` has realistic project state with done/next/validation sections filled
  - [ ] `checks.md` has actual commands in the validation table (not UNKNOWN)
  - [ ] `handoff.md` has a realistic handoff scenario
  - [ ] Each file has at least 3 `<!-- -->` explanatory comments
  - [ ] No `UNKNOWN` or `YYYY-MM-DD` placeholders remain in filled sections

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify spec/ files are filled
    Tool: Bash
    Steps:
      1. Run: wc -l .aikit/spec/SPEC.md .aikit/spec/state.md .aikit/spec/checks.md .aikit/spec/handoff.md
      2. Assert: SPEC.md >= 80 lines (was 55)
      3. Assert: state.md >= 50 lines (was 46)
      4. Assert: checks.md >= 30 lines (was 24)
      5. Assert: handoff.md >= 35 lines (was 25)
    Expected Result: All files have grown with filled content
    Evidence: .omo/evidence/task-5-spec-files-filled.txt

  Scenario: Verify checks.md has real commands
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c "uv run\|ruff\|pytest\|ty\|pyright\|bandit" .aikit/spec/checks.md
      2. Assert: count >= 6
    Expected Result: Real validation commands, not UNKNOWN
    Evidence: .omo/evidence/task-5-spec-real-commands.txt

  Scenario: Verify no placeholders remain
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c "UNKNOWN\|YYYY-MM-DD" .aikit/spec/SPEC.md .aikit/spec/state.md .aikit/spec/checks.md .aikit/spec/handoff.md
      2. Assert: total count is 0
    Expected Result: No placeholder strings in any spec file
    Evidence: .omo/evidence/task-5-spec-no-placeholders.txt
  ```

  **Commit**: NO (groups with Wave 1)

- [x] 6. Fill TODO.md with example

  **What to do**:
  - Fill `.aikit/TODO.md` with a realistic Task Management API project TODO
  - Now section: 1 active task (e.g., "Implement task pagination endpoint")
  - Next section: 2-3 upcoming tasks (e.g., "Add task filtering by status", "Write integration tests for auth flow")
  - Blocked section: 1 blocked item with blocker and owner (e.g., "Rate limiting — blocked by infra team decision")
  - Done section: 2-3 completed items with dates and validation notes
  - Add `<!-- -->` HTML comments explaining the purpose of each section

  **Must NOT do**:
  - Do not change the section structure (Now, Next, Blocked, Done)
  - Do not add more than 10 items total (keep it focused)

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2, 3, 4, 5)
  - **Blocks**: None
  - **Blocked By**: None

  **References**:
  - `.aikit/TODO.md` — current template (17 lines, 4 sections: Now, Next, Blocked, Done)
  - `.aikit/AGENTS.md:501-519` — Memory Hierarchy mentions TODO.md as a root doc

  **Acceptance Criteria**:
  - [ ] TODO.md has all 4 sections filled (Now, Next, Blocked, Done)
  - [ ] Now has exactly 1 active task
  - [ ] Next has 2-3 upcoming tasks
  - [ ] Blocked has 1 item with blocker identified
  - [ ] Done has 2-3 items with dates and validation notes
  - [ ] At least 2 `<!-- -->` explanatory comments
  - [ ] No `UNKNOWN` or `YYYY-MM-DD` placeholders remain

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify TODO.md is filled
    Tool: Bash
    Steps:
      1. Run: wc -l .aikit/TODO.md
      2. Assert: line count >= 25 (was 17)
    Expected Result: File has grown with filled content
    Evidence: .omo/evidence/task-6-todo-filled.txt

  Scenario: Verify all sections have content
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c "\- \[" .aikit/TODO.md
      2. Assert: count >= 6 (at least 6 checkbox items across sections)
    Expected Result: All sections have task items
    Evidence: .omo/evidence/task-6-todo-sections.txt

  Scenario: Verify no placeholders remain
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c "UNKNOWN\|YYYY-MM-DD" .aikit/TODO.md
      2. Assert: count is 0
    Expected Result: No placeholder strings
    Evidence: .omo/evidence/task-6-todo-no-placeholders.txt
  ```

  **Commit**: YES — `docs(aikit): add filled examples for arch, plan, design, mem, spec, TODO`
  - Files: `.aikit/arch/`, `.aikit/plan/`, `.aikit/design/`, `.aikit/mem/`, `.aikit/spec/`, `.aikit/TODO.md`
  - Pre-commit: `grep -r "UNKNOWN\|YYYY-MM-DD" .aikit/arch/ .aikit/plan/ .aikit/design/ .aikit/mem/ .aikit/spec/ .aikit/TODO.md` (must return 0 matches)

- [x] 7. Create Python src/myapp/ structure

  **What to do**:
  - Create `.aikit/templates/python/src/myapp/__init__.py` with package metadata (version, description)
  - Create `.aikit/templates/python/src/myapp/main.py` with a minimal FastAPI application skeleton showing the Task Management API entry point
  - Include: FastAPI app creation, health check endpoint, one example route (GET /tasks), proper error handling pattern
  - Add docstrings explaining the module purpose
  - Follow the patterns established in pyproject.toml (Python 3.12+, type hints, single quotes)

  **Must NOT do**:
  - Do not modify pyproject.toml, ruff.toml, ty.toml, or any existing config file
  - Do not add dependencies not already in pyproject.toml
  - Do not create a full CRUD implementation — just the skeleton showing the pattern
  - Do not add alembic/migration files

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 8, 9, 10, 11)
  - **Blocks**: None
  - **Blocked By**: None (independent of Wave 1 .md files)

  **References**:
  - `.aikit/templates/python/pyproject.toml:34-41` — ruff config shows src = ["src", "tests"] and target-version = "py312"
  - `.aikit/templates/python/pyproject.toml:79-96` — ty and pyright config shows type checking targets
  - `.aikit/templates/python/docker/Dockerfile:17-18` — CMD references "src/myapp/main.py" as the FastAPI entrypoint
  - `.aikit/templates/python/ruff.toml:57` — known-first-party = ["myapp"] confirms the package name

  **Acceptance Criteria**:
  - [ ] `src/myapp/__init__.py` exists with version and description
  - [ ] `src/myapp/main.py` exists with FastAPI app, health check, and one example route
  - [ ] All code uses type hints (consistent with pyproject.toml strict type checking)
  - [ ] All code uses single quotes (consistent with ruff.toml quote-style = "single")
  - [ ] No syntax errors: `python -c "import ast; ast.parse(open('.aikit/templates/python/src/myapp/main.py').read())"` passes

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify Python files exist and parse
    Tool: Bash
    Steps:
      1. Run: ls .aikit/templates/python/src/myapp/__init__.py .aikit/templates/python/src/myapp/main.py
      2. Assert: both files exist
      3. Run: python3 -c "import ast; ast.parse(open('.aikit/templates/python/src/myapp/main.py').read())"
      4. Assert: no syntax error
    Expected Result: Files exist and are valid Python
    Evidence: .omo/evidence/task-7-python-src-exists.txt

  Scenario: Verify code style matches config
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c '"' .aikit/templates/python/src/myapp/main.py
      2. Assert: double quotes minimal (single quotes preferred per ruff.toml)
      3. Run: grep -c "def .*->" .aikit/templates/python/src/myapp/main.py
      4. Assert: at least 2 functions with return type hints
    Expected Result: Code follows project conventions
    Evidence: .omo/evidence/task-7-python-style.txt
  ```

  **Commit**: NO (groups with Wave 2)

- [x] 8. Fill Python tests/ files

  **What to do**:
  - Fill `.aikit/templates/python/tests/conftest.py` with pytest fixtures: a FastAPI TestClient fixture, a sample task fixture, and an async event loop fixture
  - Fill `.aikit/templates/python/tests/test_app.py` with 3-4 example tests: test health check, test create task, test get tasks, test invalid input
  - Show the testing pattern: arrange/act/assert, fixture usage, async test pattern
  - Follow pytest conventions from pyproject.toml (test_*.py files, test_* functions, strict markers)

  **Must NOT do**:
  - Do not modify pyproject.toml pytest config
  - Do not add test dependencies not already in pyproject.toml
  - Do not create integration tests requiring a real database

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 7, 9, 10, 11)
  - **Blocks**: None
  - **Blocked By**: Task 7 (needs src/myapp/main.py to import from)

  **References**:
  - `.aikit/templates/python/pyproject.toml:97-107` — pytest config: testpaths=["tests"], python_files=["test_*.py"], markers (slow, integration, e2e)
  - `.aikit/templates/python/pyproject.toml:26-32` — test dependencies: pytest, pytest-cov, pytest-asyncio, pytest-xdist, pytest-mock
  - `.aikit/templates/python/ruff.toml:50` — per-file-ignores: tests/**/*.py allows S101 (assert)

  **Acceptance Criteria**:
  - [ ] `conftest.py` has at least 2 fixtures (TestClient, sample data)
  - [ ] `test_app.py` has at least 3 test functions
  - [ ] Tests use arrange/act/assert pattern
  - [ ] At least one async test using pytest-asyncio
  - [ ] All code uses type hints and single quotes

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify test files exist and parse
    Tool: Bash
    Steps:
      1. Run: python3 -c "import ast; ast.parse(open('.aikit/templates/python/tests/conftest.py').read())"
      2. Run: python3 -c "import ast; ast.parse(open('.aikit/templates/python/tests/test_app.py').read())"
      3. Assert: no syntax errors
    Expected Result: Both files are valid Python
    Evidence: .omo/evidence/task-8-python-tests-parse.txt

  Scenario: Verify test count and patterns
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c "def test_" .aikit/templates/python/tests/test_app.py
      2. Assert: count >= 3
      3. Run: grep -c "@pytest.fixture" .aikit/templates/python/tests/conftest.py
      4. Assert: count >= 2
    Expected Result: Sufficient test coverage examples
    Evidence: .omo/evidence/task-8-python-test-count.txt
  ```

  **Commit**: NO (groups with Wave 2)

- [x] 9. Fill Python docker/ files

  **What to do**:
  - Fill `.aikit/templates/python/docker/compose.yml` with a Docker Compose configuration: app service (builds from Dockerfile, maps port 8000), PostgreSQL service (with volume), optional Redis service
  - Fill `.aikit/templates/python/docker/.dockerignore` with appropriate exclusions: .venv, __pycache__, .git, tests, .env, .coverage, node_modules, .aikit, .omo
  - Use environment variables consistent with .env.example (APP_DATABASE_URL, APP_REDIS_URL, APP_SECRET_KEY)

  **Must NOT do**:
  - Do not modify the existing Dockerfile
  - Do not add services beyond what .env.example suggests
  - Do not hardcode secrets or real credentials

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 7, 8, 10, 11)
  - **Blocks**: None
  - **Blocked By**: None

  **References**:
  - `.aikit/templates/python/docker/Dockerfile` — existing Dockerfile (18 lines, python:3.12-slim, uv, FastAPI entrypoint)
  - `.aikit/templates/python/.env.example` — shows expected env vars: APP_DATABASE_URL (postgresql), APP_REDIS_URL (redis), APP_SECRET_KEY, APP_ALLOWED_ORIGINS

  **Acceptance Criteria**:
  - [ ] `compose.yml` is valid YAML with app + postgresql services
  - [ ] `compose.yml` references the existing Dockerfile
  - [ ] `.dockerignore` has at least 10 exclusion patterns
  - [ ] Environment variables in compose.yml match .env.example
  - [ ] No hardcoded secrets

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify docker files exist and are valid
    Tool: Bash
    Steps:
      1. Run: python3 -c "import yaml; yaml.safe_load(open('.aikit/templates/python/docker/compose.yml'))"
      2. Assert: no YAML parse error
      3. Run: wc -l .aikit/templates/python/docker/.dockerignore
      4. Assert: at least 10 lines
    Expected Result: Files are valid and have content
    Evidence: .omo/evidence/task-9-docker-valid.txt

  Scenario: Verify no hardcoded secrets
    Tool: Bash (grep)
    Steps:
      1. Run: grep -ic "password\|secret\|token" .aikit/templates/python/docker/compose.yml
      2. Assert: any matches use ${VAR} or env_file references, not literal values
    Expected Result: No hardcoded secrets
    Evidence: .omo/evidence/task-9-docker-no-secrets.txt
  ```

  **Commit**: NO (groups with Wave 2)

- [x] 10. Fill Python .github/container.yml

  **What to do**:
  - Fill `.aikit/templates/python/.github/container.yml` with a GitHub Actions workflow for building and publishing the Docker container to GHCR (GitHub Container Registry)
  - Trigger: push to main branch and version tags
  - Steps: checkout, set up Docker Buildx, login to GHCR, build and push with metadata labels
  - Use standard actions: actions/checkout@v4, docker/setup-buildx-action@v3, docker/login-action@v3, docker/build-push-action@v6

  **Must NOT do**:
  - Do not modify ci.yml or publish.yml
  - Do not add secrets beyond GITHUB_TOKEN
  - Do not add deployment steps (just build and push)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 7, 8, 9, 11)
  - **Blocks**: None
  - **Blocked By**: None

  **References**:
  - `.aikit/templates/python/.github/ci.yml` — existing CI workflow (20 lines, shows action version patterns)
  - `.aikit/templates/python/.github/publish.yml` — existing publish workflow (18 lines, shows PyPI publish pattern)
  - `.aikit/templates/python/docker/Dockerfile` — the Dockerfile this workflow will build

  **Acceptance Criteria**:
  - [ ] `container.yml` is valid YAML
  - [ ] Workflow has name, on (trigger), jobs sections
  - [ ] Uses docker/build-push-action with GHCR login
  - [ ] References the Dockerfile in docker/ directory
  - [ ] Uses only GITHUB_TOKEN for authentication

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify container.yml is valid YAML
    Tool: Bash
    Steps:
      1. Run: python3 -c "import yaml; yaml.safe_load(open('.aikit/templates/python/.github/container.yml'))"
      2. Assert: no YAML parse error
    Expected Result: Valid GitHub Actions workflow
    Evidence: .omo/evidence/task-10-container-yaml.txt

  Scenario: Verify GHCR references
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c "ghcr.io" .aikit/templates/python/.github/container.yml
      2. Assert: count >= 1
    Expected Result: References GitHub Container Registry
    Evidence: .omo/evidence/task-10-container-ghcr.txt
  ```

  **Commit**: NO (groups with Wave 2)

- [x] 11. Create Python template README.md

  **What to do**:
  - Create `.aikit/templates/python/README.md` documenting the Python template
  - Sections: Overview, Quick Start (copy template, rename myapp, run init.sh), Project Structure (file tree), Available Commands (task fmt, task lint, task type, task test, task check), Configuration (how to customize ruff, ty, pytest), Docker Usage, CI/CD Setup
  - Include a file tree showing the complete template structure
  - Show the validation command flow: fmt → lint → type → test → check

  **Must NOT do**:
  - Do not modify any other file
  - Do not add installation instructions for uv (assume user has it)
  - Do not create a tutorial — keep it as a reference document

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 7, 8, 9, 10)
  - **Blocks**: None
  - **Blocked By**: Tasks 7, 8, 9, 10 (README should document the completed structure)

  **References**:
  - `.aikit/templates/python/pyproject.toml:118-135` — taskipy tasks (fmt, lint, type, test, check, mdlint, mdfmt, sec)
  - `.aikit/templates/python/scripts/init.sh` — init script (uv python pin, uv sync, uv add)
  - `.aikit/templates/python/docker/Dockerfile` — Docker setup to document
  - `.aikit/templates/python/.github/ci.yml` — CI workflow to document

  **Acceptance Criteria**:
  - [ ] README.md has Overview, Quick Start, Structure, Commands, Docker, CI sections
  - [ ] File tree shows all template files
  - [ ] Commands section lists all taskipy tasks with descriptions
  - [ ] At least 60 lines of content
  - [ ] No broken references to files that don't exist

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify README exists and has content
    Tool: Bash
    Steps:
      1. Run: wc -l .aikit/templates/python/README.md
      2. Assert: line count >= 60
    Expected Result: Substantial README document
    Evidence: .omo/evidence/task-11-python-readme.txt

  Scenario: Verify file tree is present
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c "src/\|tests/\|docker/\|\.github/" .aikit/templates/python/README.md
      2. Assert: count >= 4
    Expected Result: File tree references key directories
    Evidence: .omo/evidence/task-11-python-readme-tree.txt
  ```

  **Commit**: YES — `feat(aikit): complete Python template with src, tests, docker, CI`
  - Files: `.aikit/templates/python/src/`, `.aikit/templates/python/tests/`, `.aikit/templates/python/docker/compose.yml`, `.aikit/templates/python/docker/.dockerignore`, `.aikit/templates/python/.github/container.yml`, `.aikit/templates/python/README.md`
  - Pre-commit: `python3 -c "import ast; ast.parse(open('.aikit/templates/python/src/myapp/main.py').read())"` (must pass)

- [x] 12. Create Node.js TS config files

  **What to do**:
  - Create `.aikit/templates/nodejs/ts/package.json` with: name "myapp", scripts (fmt, lint, type, test, check), devDependencies (typescript, eslint, @typescript-eslint/parser, @typescript-eslint/eslint-plugin, prettier, vitest, @types/node), engines (node >=20)
  - Create `.aikit/templates/nodejs/ts/tsconfig.json` with strict mode, ES2022 target, NodeNext module, outDir "dist", rootDir "src", include ["src"], exclude ["node_modules", "dist", "tests"]
  - Create `.aikit/templates/nodejs/ts/eslint.config.js` using flat config format with TypeScript parser and recommended rules
  - Create `.aikit/templates/nodejs/ts/vitest.config.ts` with basic config (test dir, coverage provider)
  - Create `.aikit/templates/nodejs/ts/.prettierrc` with single quotes, trailing commas, 100 print width (matching Python template style)

  **Must NOT do**:
  - Do not add any framework (Express, Fastify, Hono, etc.)
  - Do not add runtime dependencies (only devDependencies for tooling)
  - Do not use legacy ESLint config format (.eslintrc)
  - Do not add monorepo/workspace configuration

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 13, 14, 15)
  - **Blocks**: Task 13 (source files need tsconfig to exist)
  - **Blocked By**: None

  **References**:
  - `.aikit/templates/python/pyproject.toml:118-135` — taskipy tasks pattern to mirror in package.json scripts (fmt, lint, type, test, check)
  - `.aikit/templates/python/ruff.toml:6-8` — line-length=100, target-version patterns to mirror in tsconfig/prettier
  - `.aikit/templates/python/.pre-commit-config.yaml` — shows the validation toolchain pattern

  **Acceptance Criteria**:
  - [ ] `package.json` is valid JSON with scripts: fmt, lint, type, test, check
  - [ ] `tsconfig.json` is valid JSON with strict: true
  - [ ] `eslint.config.js` uses flat config format (export default [...])
  - [ ] `vitest.config.ts` exists with basic configuration
  - [ ] `.prettierrc` is valid JSON with singleQuote: true
  - [ ] No framework dependencies in package.json

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify all config files exist and are valid
    Tool: Bash
    Steps:
      1. Run: node -e "JSON.parse(require('fs').readFileSync('.aikit/templates/nodejs/ts/package.json'))"
      2. Run: node -e "JSON.parse(require('fs').readFileSync('.aikit/templates/nodejs/ts/tsconfig.json'))"
      3. Run: node -e "JSON.parse(require('fs').readFileSync('.aikit/templates/nodejs/ts/.prettierrc'))"
      4. Assert: all pass without error
    Expected Result: All JSON files are valid
    Evidence: .omo/evidence/task-12-ts-config-valid.txt

  Scenario: Verify no framework dependencies
    Tool: Bash (grep)
    Steps:
      1. Run: grep -ic "express\|fastify\|hono\|koa\|next\|nuxt" .aikit/templates/nodejs/ts/package.json
      2. Assert: count is 0
    Expected Result: No framework dependencies
    Evidence: .omo/evidence/task-12-ts-no-framework.txt

  Scenario: Verify package.json scripts mirror Python taskipy
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c '"fmt"\|"lint"\|"type"\|"test"\|"check"' .aikit/templates/nodejs/ts/package.json
      2. Assert: count >= 5
    Expected Result: Same command vocabulary as Python template
    Evidence: .omo/evidence/task-12-ts-scripts.txt
  ```

  **Commit**: NO (groups with Wave 3)

- [x] 13. Create Node.js TS source and tests

  **What to do**:
  - Create `.aikit/templates/nodejs/ts/src/index.ts` with a minimal HTTP server using node:http module showing the Task Management API pattern: health check endpoint, GET /tasks example route, proper error handling, structured logging
  - Create `.aikit/templates/nodejs/ts/tests/index.test.ts` with 3-4 vitest tests: test health check, test get tasks, test 404 handling, test invalid method
  - Use TypeScript strict mode features: explicit types, proper error handling, no `any`
  - Show the pattern for a framework-less Node.js API that's still production-quality

  **Must NOT do**:
  - Do not use any framework (Express, Fastify, Hono)
  - Do not use `any` type
  - Do not create a full CRUD implementation — just the skeleton showing the pattern
  - Do not add database connections (use in-memory data for the example)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 12, 14, 15)
  - **Blocks**: None
  - **Blocked By**: Task 12 (needs tsconfig.json for imports to resolve)

  **References**:
  - `.aikit/templates/python/src/myapp/main.py` — Python equivalent showing the same Task API pattern (to be created in Task 7)
  - `.aikit/templates/python/tests/test_app.py` — Python test pattern to mirror in vitest

  **Acceptance Criteria**:
  - [ ] `src/index.ts` has HTTP server with health check and at least one route
  - [ ] `src/index.ts` uses no `any` types
  - [ ] `tests/index.test.ts` has at least 3 test cases
  - [ ] Tests use vitest (describe/it/expect pattern)
  - [ ] All TypeScript compiles without errors (verified by tsconfig strict mode)

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify source and test files exist
    Tool: Bash
    Steps:
      1. Run: ls .aikit/templates/nodejs/ts/src/index.ts .aikit/templates/nodejs/ts/tests/index.test.ts
      2. Assert: both files exist
    Expected Result: Files exist
    Evidence: .omo/evidence/task-13-ts-source-exists.txt

  Scenario: Verify no any types
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c ": any\|as any\|<any>" .aikit/templates/nodejs/ts/src/index.ts
      2. Assert: count is 0
    Expected Result: No any types in source code
    Evidence: .omo/evidence/task-13-ts-no-any.txt

  Scenario: Verify test count
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c "it(\|test(" .aikit/templates/nodejs/ts/tests/index.test.ts
      2. Assert: count >= 3
    Expected Result: At least 3 test cases
    Evidence: .omo/evidence/task-13-ts-test-count.txt
  ```

  **Commit**: NO (groups with Wave 3)

- [x] 14. Create Node.js TS docker and CI files

  **What to do**:
  - Create `.aikit/templates/nodejs/ts/docker/Dockerfile` with multi-stage build: builder stage (node:20-slim, npm ci, npm run build), production stage (node:20-slim, copy dist, run with node)
  - Create `.aikit/templates/nodejs/ts/docker/compose.yml` with app service (builds from Dockerfile, maps port 3000) and optional PostgreSQL service
  - Create `.aikit/templates/nodejs/ts/docker/.dockerignore` with: node_modules, dist, .git, tests, .env, coverage, .aikit, .omo
  - Create `.aikit/templates/nodejs/ts/.github/ci.yml` with: checkout, setup Node.js 20, npm ci, npm run check (fmt + lint + type + test)

  **Must NOT do**:
  - Do not use Docker Buildx unless necessary (keep it simple)
  - Do not add deployment steps to CI (just validate)
  - Do not hardcode secrets

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 12, 13, 15)
  - **Blocks**: None
  - **Blocked By**: None

  **References**:
  - `.aikit/templates/python/docker/Dockerfile` — Python Dockerfile pattern to mirror
  - `.aikit/templates/python/.github/ci.yml` — Python CI workflow pattern to mirror
  - `.aikit/templates/python/docker/compose.yml` — Python compose pattern (to be created in Task 9)

  **Acceptance Criteria**:
  - [ ] `Dockerfile` has multi-stage build (builder + production)
  - [ ] `compose.yml` is valid YAML with app service
  - [ ] `.dockerignore` has at least 8 exclusion patterns
  - [ ] `ci.yml` is valid YAML with checkout, setup-node, npm ci, npm run check
  - [ ] CI uses node 20 (matching package.json engines)

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify docker and CI files exist and are valid
    Tool: Bash
    Steps:
      1. Run: python3 -c "import yaml; yaml.safe_load(open('.aikit/templates/nodejs/ts/docker/compose.yml'))"
      2. Run: python3 -c "import yaml; yaml.safe_load(open('.aikit/templates/nodejs/ts/.github/ci.yml'))"
      3. Assert: both pass without error
    Expected Result: All YAML files are valid
    Evidence: .omo/evidence/task-14-ts-docker-ci-valid.txt

  Scenario: Verify Dockerfile has multi-stage build
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c "^FROM" .aikit/templates/nodejs/ts/docker/Dockerfile
      2. Assert: count >= 2 (multi-stage)
    Expected Result: Multi-stage Docker build
    Evidence: .omo/evidence/task-14-ts-dockerfile-stages.txt
  ```

  **Commit**: NO (groups with Wave 3)

- [x] 15. Create Node.js TS misc files

  **What to do**:
  - Create `.aikit/templates/nodejs/ts/scripts/init.sh` with: npm install, npm run check (verify setup works)
  - Create `.aikit/templates/nodejs/ts/README.md` documenting: Overview, Quick Start (copy template, rename, run init.sh), Project Structure (file tree), Available Commands (npm run fmt/lint/type/test/check), Configuration (tsconfig, eslint, prettier customization), Docker Usage, CI/CD Setup
  - Create `.aikit/templates/nodejs/ts/.gitignore` with: node_modules, dist, coverage, .env, .env.local, *.log, .DS_Store, .aikit, .omo
  - Create `.aikit/templates/nodejs/ts/.env.example` with: NODE_ENV=development, PORT=3000, DATABASE_URL=postgresql://user:pass@localhost:5432/myapp, LOG_LEVEL=info

  **Must NOT do**:
  - Do not add secrets or real credentials
  - Do not create a tutorial — keep README as a reference document
  - Do not add framework-specific documentation

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 12, 13, 14)
  - **Blocks**: None
  - **Blocked By**: Tasks 12, 13, 14 (README should document the completed structure)

  **References**:
  - `.aikit/templates/python/scripts/init.sh` — Python init script pattern
  - `.aikit/templates/python/.gitignore` — Python gitignore pattern to mirror
  - `.aikit/templates/python/.env.example` — Python env example pattern to mirror

  **Acceptance Criteria**:
  - [ ] `scripts/init.sh` exists and passes `bash -n` syntax check
  - [ ] `README.md` has Overview, Quick Start, Structure, Commands, Docker, CI sections
  - [ ] `README.md` file tree shows all template files
  - [ ] `.gitignore` has at least 10 exclusion patterns
  - [ ] `.env.example` has at least 4 environment variables
  - [ ] README is at least 60 lines

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify misc files exist
    Tool: Bash
    Steps:
      1. Run: ls .aikit/templates/nodejs/ts/scripts/init.sh .aikit/templates/nodejs/ts/README.md .aikit/templates/nodejs/ts/.gitignore .aikit/templates/nodejs/ts/.env.example
      2. Assert: all 4 files exist
    Expected Result: All misc files present
    Evidence: .omo/evidence/task-15-ts-misc-exists.txt

  Scenario: Verify init.sh syntax
    Tool: Bash
    Steps:
      1. Run: bash -n .aikit/templates/nodejs/ts/scripts/init.sh
      2. Assert: no syntax error
    Expected Result: Valid shell script
    Evidence: .omo/evidence/task-15-ts-init-syntax.txt

  Scenario: Verify README has content
    Tool: Bash
    Steps:
      1. Run: wc -l .aikit/templates/nodejs/ts/README.md
      2. Assert: line count >= 60
    Expected Result: Substantial README
    Evidence: .omo/evidence/task-15-ts-readme-size.txt
  ```

  **Commit**: YES — `feat(aikit): add Node.js TypeScript template`
  - Files: `.aikit/templates/nodejs/ts/`
  - Pre-commit: `node -e "JSON.parse(require('fs').readFileSync('.aikit/templates/nodejs/ts/package.json'))"` (must pass)

- [x] 16. Create Node.js JS config files

  **What to do**:
  - Create `.aikit/templates/nodejs/js/package.json` with: name "myapp", type "module", scripts (fmt, lint, test, check), devDependencies (eslint, prettier, vitest), engines (node >=20). NO TypeScript dependencies.
  - Create `.aikit/templates/nodejs/js/eslint.config.js` using flat config format WITHOUT TypeScript parser (use espree or default parser)
  - Create `.aikit/templates/nodejs/js/vitest.config.js` (not .ts) with basic config
  - Create `.aikit/templates/nodejs/js/.prettierrc` with same settings as TS template (single quotes, trailing commas, 100 print width)

  **Must NOT do**:
  - Do not include tsconfig.json
  - Do not include any TypeScript dependencies (typescript, @typescript-eslint/*, @types/*)
  - Do not include a "type" script in package.json (no type checking in JS)
  - Do not add any framework

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 17, 18, 19)
  - **Blocks**: Task 17 (source files need config to exist)
  - **Blocked By**: None

  **References**:
  - `.aikit/templates/nodejs/ts/package.json` — TS version to base JS version on (remove TS deps and scripts)
  - `.aikit/templates/nodejs/ts/eslint.config.js` — TS ESLint config to simplify for JS
  - `.aikit/templates/python/pyproject.toml:118-135` — taskipy tasks pattern

  **Acceptance Criteria**:
  - [ ] `package.json` is valid JSON with scripts: fmt, lint, test, check (NO "type" script)
  - [ ] `package.json` has NO TypeScript dependencies
  - [ ] `eslint.config.js` uses flat config format WITHOUT TypeScript parser
  - [ ] `vitest.config.js` exists (not .ts extension)
  - [ ] `.prettierrc` is valid JSON
  - [ ] No tsconfig.json exists in the directory

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify JS config files exist and are valid
    Tool: Bash
    Steps:
      1. Run: node -e "JSON.parse(require('fs').readFileSync('.aikit/templates/nodejs/js/package.json'))"
      2. Run: node -e "JSON.parse(require('fs').readFileSync('.aikit/templates/nodejs/js/.prettierrc'))"
      3. Assert: all pass without error
    Expected Result: All JSON files are valid
    Evidence: .omo/evidence/task-16-js-config-valid.txt

  Scenario: Verify NO TypeScript artifacts
    Tool: Bash
    Steps:
      1. Run: ls .aikit/templates/nodejs/js/tsconfig.json 2>&1
      2. Assert: file does NOT exist
      3. Run: grep -ic "typescript\|@typescript-eslint\|@types/" .aikit/templates/nodejs/js/package.json
      4. Assert: count is 0
    Expected Result: Zero TypeScript traces in JS template
    Evidence: .omo/evidence/task-16-js-no-ts.txt

  Scenario: Verify no type script in package.json
    Tool: Bash (grep)
    Steps:
      1. Run: grep '"type"' .aikit/templates/nodejs/js/package.json
      2. Assert: only "type": "module" exists (not a "type" script)
      3. Run: grep -c '"type":' .aikit/templates/nodejs/js/package.json | grep -v "module"
      4. Assert: no "type" check script
    Expected Result: No type checking script in JS template
    Evidence: .omo/evidence/task-16-js-no-type-script.txt
  ```

  **Commit**: NO (groups with Wave 4)

- [x] 17. Create Node.js JS source and tests

  **What to do**:
  - Create `.aikit/templates/nodejs/js/src/index.js` with the same minimal HTTP server as the TS version but in plain JavaScript using node:http module: health check endpoint, GET /tasks example route, proper error handling, structured logging
  - Create `.aikit/templates/nodejs/js/tests/index.test.js` with 3-4 vitest tests: test health check, test get tasks, test 404 handling, test invalid method
  - Use JSDoc comments for type documentation where helpful
  - Show the pattern for a framework-less Node.js API in plain JavaScript

  **Must NOT do**:
  - Do not use any framework
  - Do not use TypeScript syntax (no type annotations, no interfaces, no enums)
  - Do not create a full CRUD implementation
  - Do not add database connections

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 16, 18, 19)
  - **Blocks**: None
  - **Blocked By**: Task 16 (needs config files)

  **References**:
  - `.aikit/templates/nodejs/ts/src/index.ts` — TS version to convert to plain JS (to be created in Task 13)
  - `.aikit/templates/nodejs/ts/tests/index.test.ts` — TS test version to convert to plain JS

  **Acceptance Criteria**:
  - [ ] `src/index.js` has HTTP server with health check and at least one route
  - [ ] `src/index.js` uses NO TypeScript syntax
  - [ ] `tests/index.test.js` has at least 3 test cases
  - [ ] Tests use vitest (describe/it/expect pattern)
  - [ ] All files use .js extension (not .ts)

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify JS source and test files exist
    Tool: Bash
    Steps:
      1. Run: ls .aikit/templates/nodejs/js/src/index.js .aikit/templates/nodejs/js/tests/index.test.js
      2. Assert: both files exist
    Expected Result: Files exist with .js extension
    Evidence: .omo/evidence/task-17-js-source-exists.txt

  Scenario: Verify no TypeScript syntax
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c ": string\|: number\|: boolean\|interface \|type \|enum \|as const\|<T>" .aikit/templates/nodejs/js/src/index.js
      2. Assert: count is 0
    Expected Result: No TypeScript syntax in JS files
    Evidence: .omo/evidence/task-17-js-no-ts-syntax.txt

  Scenario: Verify test count
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c "it(\|test(" .aikit/templates/nodejs/js/tests/index.test.js
      2. Assert: count >= 3
    Expected Result: At least 3 test cases
    Evidence: .omo/evidence/task-17-js-test-count.txt
  ```

  **Commit**: NO (groups with Wave 4)

- [x] 18. Create Node.js JS docker and CI files

  **What to do**:
  - Create `.aikit/templates/nodejs/js/docker/Dockerfile` with: node:20-slim base, npm ci, copy src, run with node (NO build step since no TypeScript)
  - Create `.aikit/templates/nodejs/js/docker/compose.yml` with app service (builds from Dockerfile, maps port 3000) and optional PostgreSQL service
  - Create `.aikit/templates/nodejs/js/docker/.dockerignore` with: node_modules, .git, tests, .env, coverage, .aikit, .omo
  - Create `.aikit/templates/nodejs/js/.github/ci.yml` with: checkout, setup Node.js 20, npm ci, npm run check (fmt + lint + test, NO type check)

  **Must NOT do**:
  - Do not include a build step in Dockerfile (no TypeScript to compile)
  - Do not include type checking in CI
  - Do not hardcode secrets

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 16, 17, 19)
  - **Blocks**: None
  - **Blocked By**: None

  **References**:
  - `.aikit/templates/nodejs/ts/docker/Dockerfile` — TS version to simplify (remove build step)
  - `.aikit/templates/nodejs/ts/.github/ci.yml` — TS CI to simplify (remove type check)

  **Acceptance Criteria**:
  - [ ] `Dockerfile` has single-stage build (no build step needed)
  - [ ] `compose.yml` is valid YAML with app service
  - [ ] `.dockerignore` has at least 8 exclusion patterns
  - [ ] `ci.yml` is valid YAML with checkout, setup-node, npm ci, npm run check
  - [ ] CI does NOT include type checking step

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify docker and CI files exist and are valid
    Tool: Bash
    Steps:
      1. Run: python3 -c "import yaml; yaml.safe_load(open('.aikit/templates/nodejs/js/docker/compose.yml'))"
      2. Run: python3 -c "import yaml; yaml.safe_load(open('.aikit/templates/nodejs/js/.github/ci.yml'))"
      3. Assert: both pass without error
    Expected Result: All YAML files are valid
    Evidence: .omo/evidence/task-18-js-docker-ci-valid.txt

  Scenario: Verify Dockerfile has NO build step
    Tool: Bash (grep)
    Steps:
      1. Run: grep -c "npm run build\|tsc\|typescript" .aikit/templates/nodejs/js/docker/Dockerfile
      2. Assert: count is 0
    Expected Result: No TypeScript build in JS Dockerfile
    Evidence: .omo/evidence/task-18-js-no-build.txt
  ```

  **Commit**: NO (groups with Wave 4)

- [x] 19. Create Node.js JS misc files

  **What to do**:
  - Create `.aikit/templates/nodejs/js/scripts/init.sh` with: npm install, npm run check (verify setup works)
  - Create `.aikit/templates/nodejs/js/README.md` documenting: Overview, Quick Start, Project Structure (file tree), Available Commands (npm run fmt/lint/test/check — note: no type command), Configuration (eslint, prettier customization), Docker Usage, CI/CD Setup
  - Create `.aikit/templates/nodejs/js/.gitignore` with: node_modules, .env, .env.local, *.log, coverage, .DS_Store, .aikit, .omo (NO dist/ since no build)
  - Create `.aikit/templates/nodejs/js/.env.example` with: NODE_ENV=development, PORT=3000, DATABASE_URL=postgresql://user:pass@localhost:5432/myapp, LOG_LEVEL=info

  **Must NOT do**:
  - Do not add secrets or real credentials
  - Do not document TypeScript configuration (this is the JS template)
  - Do not include dist/ in .gitignore (no build output)

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 16, 17, 18)
  - **Blocks**: None
  - **Blocked By**: Tasks 16, 17, 18 (README should document the completed structure)

  **References**:
  - `.aikit/templates/nodejs/ts/README.md` — TS README to adapt for JS (remove TS-specific sections)
  - `.aikit/templates/nodejs/ts/.gitignore` — TS gitignore to simplify (remove dist/)
  - `.aikit/templates/python/.env.example` — Python env example pattern

  **Acceptance Criteria**:
  - [ ] `scripts/init.sh` exists and passes `bash -n` syntax check
  - [ ] `README.md` has Overview, Quick Start, Structure, Commands, Docker, CI sections
  - [ ] `README.md` does NOT mention TypeScript or tsconfig
  - [ ] `.gitignore` has at least 8 exclusion patterns, does NOT include dist/
  - [ ] `.env.example` has at least 4 environment variables
  - [ ] README is at least 50 lines

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Verify misc files exist
    Tool: Bash
    Steps:
      1. Run: ls .aikit/templates/nodejs/js/scripts/init.sh .aikit/templates/nodejs/js/README.md .aikit/templates/nodejs/js/.gitignore .aikit/templates/nodejs/js/.env.example
      2. Assert: all 4 files exist
    Expected Result: All misc files present
    Evidence: .omo/evidence/task-19-js-misc-exists.txt

  Scenario: Verify init.sh syntax
    Tool: Bash
    Steps:
      1. Run: bash -n .aikit/templates/nodejs/js/scripts/init.sh
      2. Assert: no syntax error
    Expected Result: Valid shell script
    Evidence: .omo/evidence/task-19-js-init-syntax.txt

  Scenario: Verify README has no TypeScript references
    Tool: Bash (grep)
    Steps:
      1. Run: grep -ic "typescript\|tsconfig\|tsc" .aikit/templates/nodejs/js/README.md
      2. Assert: count is 0
    Expected Result: No TypeScript references in JS README
    Evidence: .omo/evidence/task-19-js-readme-no-ts.txt
  ```

  **Commit**: YES — `feat(aikit): add Node.js JavaScript template`
  - Files: `.aikit/templates/nodejs/js/`
  - Pre-commit: `node -e "JSON.parse(require('fs').readFileSync('.aikit/templates/nodejs/js/package.json'))"` (must pass)

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.
>
> **Do NOT auto-proceed after verification. Wait for user's explicit approval before marking work complete.**
> **Never mark F1-F4 as checked before getting user's okay.** Rejection or user feedback -> fix -> re-run -> present again -> wait for okay.

- [x] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, check content). For each "Must NOT Have": search for forbidden patterns — reject with file:line if found. Check evidence files exist in .omo/evidence/. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [x] F2. **Content Quality Review** — `unspecified-high`
  Read all filled .md files. Check: examples are coherent (same Task API domain), comments explain WHY not WHAT, no remaining UNKNOWN/YYYY-MM-DD placeholders, English only, no secrets/credentials. Check all README files explain directory purpose clearly.
  Output: `Coherence [PASS/FAIL] | Comments [N/N files] | Placeholders [CLEAN/N remaining] | Language [EN/N non-EN] | VERDICT`

- [x] F3. **Cross-File Consistency Check** — `deep`
  Verify all .md examples reference the same Task Management API consistently. Check: architecture decisions in arch/ match design/, spec requirements match plan phases, mem/decisions match design decisions, TODO items match spec/state next steps. Flag any contradictions.
  Output: `Consistency [N/N aligned] | Contradictions [CLEAN/N found] | Cross-refs [N/N valid] | VERDICT`

- [x] F4. **Template Copyability Test** — `unspecified-high`
  For each template (Python, Node.js TS, Node.js JS): verify all files exist, config files are valid (JSON/YAML syntax), shell scripts pass `bash -n`, Docker files are valid YAML, no broken references between files. Simulate "copy to new project" by checking all paths are relative and self-contained.
  Output: `Python [N/N files] | Node-TS [N/N files] | Node-JS [N/N files] | Syntax [N/N valid] | VERDICT`

---

## Commit Strategy

- **Wave 1**: `docs(aikit): add filled examples for arch, plan, design, mem, spec, TODO` — all .md files
- **Wave 2**: `feat(aikit): complete Python template with src, tests, docker, CI` — Python template files
- **Wave 3**: `feat(aikit): add Node.js TypeScript template` — Node.js TS files
- **Wave 4**: `feat(aikit): add Node.js JavaScript template` — Node.js JS files

---

## Success Criteria

### Verification Commands
```bash
# Check no empty files remain
find .aikit/ -type f -empty | grep -v __pycache__  # Expected: no output

# Check no UNKNOWN placeholders in filled sections
grep -r "UNKNOWN" .aikit/arch/ .aikit/plan/ .aikit/design/ .aikit/mem/ .aikit/spec/ .aikit/TODO.md  # Expected: no matches

# Check no YYYY-MM-DD placeholders in filled sections
grep -r "YYYY-MM-DD" .aikit/arch/ .aikit/plan/ .aikit/design/ .aikit/mem/ .aikit/spec/ .aikit/TODO.md  # Expected: no matches

# Validate JSON files
for f in $(find .aikit/templates/nodejs -name "*.json"); do node -e "JSON.parse(require('fs').readFileSync('$f'))"; done  # Expected: no errors

# Validate YAML files
for f in $(find .aikit/templates -name "*.yml" -o -name "*.yaml"); do python -c "import yaml; yaml.safe_load(open('$f'))"; done  # Expected: no errors

# Check shell scripts
find .aikit/templates -name "*.sh" -exec bash -n {} \;  # Expected: no errors

# Verify all expected files exist
ls .aikit/arch/README.md .aikit/arch/ARCH.md .aikit/plan/README.md .aikit/plan/PLAN.md  # Expected: all exist
ls .aikit/templates/nodejs/ts/package.json .aikit/templates/nodejs/js/package.json  # Expected: all exist
```

### Final Checklist
- [ ] All "Must Have" present
- [ ] All "Must NOT Have" absent
- [ ] All empty files filled
- [ ] All .md files have examples + comments
- [ ] All templates are self-contained and copyable
- [ ] All examples reference the same Task Management API
- [ ] No placeholders remain in filled sections
