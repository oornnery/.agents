# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!--
UV inline script overlay.
Use for single-file Python scripts that declare dependencies directly inside the
`.py` file with inline metadata instead of a full project package layout.
-->

## Project Description

<!-- Brief description of what the script does, who runs it, and whether it is
for one-off automation, local tooling, or a checked-in operational script -->

## Stack

- **Python**: 3.12+
- **Runner**: uv
- **Packaging Style**: single-file script with inline metadata
<!-- - **Optional**: Rich / HTTPX / Pydantic / prompt-toolkit -->

## Quick Commands

```bash
uv run script.py
uv run --with pytest pytest -v
```

## Script Header Pattern

Use inline metadata at the top of the file:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx>=0.27",
#   "rich>=13.0",
# ]
# ///
```

Optional shebang when the file should run directly:

```python
#!/usr/bin/env -S uv run
```

## Validation Entry Points

- run the script directly with representative arguments
- verify failure paths as well as happy paths
- use lightweight focused tests when the script is important or reused often

## UV Script Rules

- keep dependencies inside the script metadata when the script is truly standalone
- move to a full `pyproject.toml` project once the script grows into a package, service, or reusable module set
- keep the script focused; if it grows multiple responsibilities, split logic into helper modules or promote it to a real project
- keep file, network, and subprocess actions explicit and easy to audit

## Pythonic Script Defaults

- keep the main flow easy to read top-to-bottom
- isolate helper functions instead of nesting everything in `main()`
- validate arguments early
- use explicit exit codes for automation-facing scripts
- keep operational output clear and actionable

## Suggested Layout

For a single-file script:

```text
script.py
```

For a small script plus helpers:

```text
scripts/
├── sync_data.py
└── _helpers.py
```

## UV Script Checklist

### Metadata

- [ ] inline metadata block is present and valid
- [ ] Python version is explicit
- [ ] dependencies are minimal and justified

### Script Design

- [ ] arguments and usage are clear
- [ ] side effects are explicit
- [ ] errors are useful and actionable
- [ ] output is readable or machine-friendly as needed

### Safety

- [ ] file paths are validated
- [ ] dangerous commands require explicit intent
- [ ] secrets do not live inside the script
- [ ] network and subprocess usage is obvious

### Verification

- [ ] happy path is exercised
- [ ] failure path is exercised
- [ ] representative sample input is tested
- [ ] repeated runs are safe when the script should be idempotent

## Project-Specific Guardrails

<!-- - Keep operational scripts deterministic -->
<!-- - Do not silently overwrite files -->
<!-- - Promote to a package once multiple modules or commands appear -->
