# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!--
CLI application overlay.
Use for terminal tools, interactive prompts, or automation-oriented command
line apps where UX, exit behavior, and output discipline need stronger rules.
-->

## Project Description

<!-- Brief description of who uses the CLI and what workflows it supports -->

## Stack

- **Python**: 3.12+
- **Simple CLI**: argparse + rich-argparse
- **Complex CLI**: Typer + Rich
- **TUI**: Textual

## Quick Commands

```bash
uv sync
uv run python -m myapp --help
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

## CLI UX Rules

- `--help` output must be accurate and easy to scan
- use exit code `0` for success and non-zero for failure
- write machine-readable output to stdout and human-readable errors to stderr
- keep interactive prompts optional when automation use is expected
- avoid noisy output by default; make verbose output explicit
- keep colors and rich formatting helpful, not required for correctness

## CLI Technology Defaults

- use `argparse` plus `rich-argparse` for simple command-line tools with a small
  number of commands and flags
- use `Typer` plus `Rich` when the CLI grows multiple subcommands, richer
  output, or more structured operator workflows
- use `Textual` when the project is a real TUI, not just a CLI with colored
  output
- keep parsing, workflow execution, and terminal rendering as separate concerns
- do not introduce a TUI when a normal CLI is enough

## Command Design Rules

- keep subcommands explicit and predictable
- prefer flags over hidden positional magic
- make destructive operations obvious before they run
- separate parsing, workflow orchestration, and output formatting

## Output and Automation Rules

- keep machine-readable output stable when promised
- avoid mixing logs with command output meant for piping
- make interactive prompts skippable in CI or script contexts
- keep terminal formatting optional rather than required for correctness

## CLI Checklist

### User Experience

- [ ] `--help` is accurate and readable
- [ ] success goes to stdout and errors go to stderr
- [ ] exit codes are consistent
- [ ] verbose or debug output is opt-in

### Automation

- [ ] interactive prompts can be bypassed when scripting
- [ ] machine-readable output stays stable if promised
- [ ] errors are actionable and not overly noisy

### Safety

- [ ] secrets are never printed
- [ ] dangerous operations require explicit user intent
- [ ] path handling and file writes are validated

### Verification

- [ ] help text is tested
- [ ] stdout and stderr behavior is tested
- [ ] exit codes are tested
- [ ] interactive and non-interactive flows are tested

## Layout

```text
src/myapp/
├── cli/             # command parsing, dispatch, and subcommands
├── core/            # reusable business logic
├── services/        # workflows and orchestration
├── models/          # typed inputs, outputs, and config models
└── views/           # terminal rendering helpers, prompts, and output formatting
```

## Testing Focus

<!-- - help output -->
<!-- - exit codes -->
<!-- - stdout/stderr separation -->
<!-- - interactive vs non-interactive mode -->
<!-- - failure recovery and invalid input -->

## Environment Variables

<!-- | Variable | Description | Required | -->
<!-- |----------|-------------|----------| -->

## Project-Specific Guardrails

<!-- - Never print secrets -->
<!-- - Preserve machine-readable output shape -->
<!-- - Keep prompts skippable for CI and scripts -->
