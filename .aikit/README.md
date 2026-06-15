# aikit

A copyable reference kit that gives AI coding agents durable memory, operational
state, and consistent workflows in any project.

<!-- This README is the entry point for humans AND agents. It explains what to copy
     where, so the kit works without reading every file first. -->

## What Is This

- `AGENTS.md` — operational instructions loaded by agents on every session
- Reference directories (`arch/`, `plan/`, `design/`, `mem/`, `spec/`, `TODO.md`)
  filled with a coherent example: a **Task Management API**
- Project templates (`templates/`) for Python, Node.js TypeScript, and Node.js
  JavaScript with the same validation vocabulary (`fmt`, `lint`, `type`, `test`, `check`)

Every example file contains `<!-- -->` comments explaining WHY each section
matters. The Task API content is a worked example — replace it with your
project's facts, keep the structure and the comments.

## How to Use in a New Project

Copy the kit contents into your project root with this mapping:

| Kit path | Destination in your project | Purpose |
| -------- | --------------------------- | ------- |
| `AGENTS.md` | `AGENTS.md` | Agent rules, always loaded |
| `TODO.md` | `TODO.md` | Now / Next / Blocked / Done |
| `spec/SPEC.md` | `SPEC.md` | Objective, scope, requirements |
| `design/DESIGN.md` | `DESIGN.md` | Architecture, API, design decisions |
| `arch/` | `.arch/` | System boundaries, data flow, deployment |
| `plan/` | `.plan/` | Phased implementation plans |
| `mem/` | `.mem/` | Durable memory: `hot.md`, `decisions.md`, `open-loops.md` |
| `spec/state.md`, `spec/checks.md`, `spec/handoff.md` | `.spec/` | Operational state, validation commands, handoffs |
| `templates/<stack>/` | project root | Scaffolding for a new Python or Node.js project |

<!-- The kit stores dotted directories (.mem, .spec, .arch, .plan) without the dot
     so their contents stay visible while browsing the kit itself. -->

Then:

1. Replace the Task Management API examples with your project's real facts.
2. Keep every `<!-- -->` comment — they teach future agents how to maintain each file.
3. Update `spec/checks.md` (→ `.spec/checks.md`) with your project's actual
   validation commands before the first agent session.

## Using a Project Template

1. Copy `templates/python/`, `templates/nodejs/ts/`, or `templates/nodejs/js/`
   into a new directory.
2. Rename `myapp` (package name in Python, `name` in `package.json` for Node.js).
3. Run `scripts/init.sh` to install the toolchain.
4. Run the full validation flow: `task check` (Python) or `npm run check` (Node.js).

## Rules

- All content in English — the kit is meant to be shared.
- No secrets, credentials, or real API keys anywhere.
- Examples must stay coherent: one domain story across all reference files.
- `mem/hot.md` stays under 80 lines; it is loaded on every session.
