---
name: python-cli
description: Build, review, or validate Python command-line applications and terminal tools. Use for argparse, Typer, Rich, Textual-adjacent CLI UX, stdout/stderr contracts, exit codes, automation-friendly flags, help output, and CLI tests.
---

# Python CLI

Use for Python terminal applications where user experience, automation behavior, and command contracts matter.

## Defaults

- Simple commands: `argparse` + optional `rich-argparse`
- Multi-command apps: Typer + Rich
- Real TUI: load `skills/textual/SKILL.md`
- Presentation: load `skills/rich/SKILL.md`
- Implementation: load `skills/python/SKILL.md`
- Final checks: load `skills/verification/SKILL.md`

## Workflow

1. Inspect command entrypoints, parser, help text, scripts, and tests.
2. Separate parsing, orchestration, business logic, and rendering.
3. Define stdout/stderr, exit codes, interactive behavior, and machine-readable output.
4. Implement the smallest changed command surface.
5. Verify help, success path, failure path, and automation mode.

## UX Rules

- `--help` must be accurate, scannable, and current.
- Success exits `0`; failures exit non-zero.
- Machine-readable output goes to stdout; human-readable errors go to stderr.
- Interactive prompts must be optional when CI/scripts may call the command.
- Verbose/debug output is opt-in.
- Color and Rich formatting help usability but are not correctness.

## Safety Rules

- Secrets are never printed.
- Dangerous operations require explicit flags or confirmation.
- File paths and overwrites are validated.
- Network, subprocess, and filesystem side effects are visible from command names or flags.

## Suggested Layout

```text
src/myapp/
├── cli/       # parsing, dispatch, commands
├── core/      # reusable logic
├── services/  # orchestration
├── models/    # typed inputs/outputs/config
└── views/     # terminal rendering
```

## Verification

- `uv run python -m myapp --help`
- command success path
- command failure path
- stdout/stderr behavior
- exit codes
- interactive and non-interactive modes
