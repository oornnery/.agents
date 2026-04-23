# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!-- CLI app overlay. Terminal tools, interactive prompts, automation CLIs needing stronger UX/exit/output rules. -->

## Project Description

<!-- Who uses CLI, what workflows supported -->

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

- `--help` output accurate, scannable
- exit `0` success, non-zero failure
- machine-readable -> stdout, human-readable errors -> stderr
- interactive prompts optional when automation expected
- quiet by default; verbose opt-in
- colors/rich formatting helpful, not required for correctness

## CLI Technology Defaults

- `argparse` + `rich-argparse` for simple tools with few commands/flags
- `Typer` + `Rich` for multiple subcommands, richer output, structured workflows
- `Textual` for real TUI, not just colored CLI
- parsing, workflow execution, terminal rendering = separate concerns
- no TUI when CLI sufficient

## Command Design Rules

- subcommands explicit, predictable
- flags > hidden positional magic
- destructive ops obvious before running
- separate parsing, orchestration, output formatting

## Output and Automation Rules

- machine-readable output stable when promised
- no mixing logs with pipeable output
- interactive prompts skippable in CI/scripts
- terminal formatting optional, not required for correctness

## CLI Checklist

### User Experience

- [ ] `--help` accurate, readable
- [ ] success -> stdout, errors -> stderr
- [ ] exit codes consistent
- [ ] verbose/debug opt-in

### Automation

- [ ] interactive prompts bypassable when scripting
- [ ] machine-readable output stable if promised
- [ ] errors actionable, not noisy

### Safety

- [ ] secrets never printed
- [ ] dangerous ops require explicit intent
- [ ] path handling, file writes validated

### Verification

- [ ] help text tested
- [ ] stdout/stderr behavior tested
- [ ] exit codes tested
- [ ] interactive + non-interactive flows tested

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