# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!--
UV inline script overlay.
Single-file Python scripts declare dependencies inside `.py` file with inline metadata, no full project layout.
-->

## Project Description

<!-- What script does, who runs it, one-off automation / local tooling / checked-in operational script -->

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

Use inline metadata at top of file:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx>=0.27",
#   "rich>=13.0",
# ]
# ///
```

Optional shebang when file should run directly:

```python
#!/usr/bin/env -S uv run
```

## Validation Entry Points

- run script with representative arguments
- verify failure paths and happy paths
- lightweight focused tests when script important or reused

## UV Script Rules

- keep dependencies inside script metadata when script truly standalone
- move to full `pyproject.toml` project once script grows into package, service, or reusable module set
- keep script focused; multiple responsibilities = split into helpers or promote to real project
- keep file, network, subprocess actions explicit and easy to audit

## Pythonic Script Defaults

- main flow readable top-to-bottom
- isolate helper functions, avoid nesting everything in `main()`
- validate arguments early
- explicit exit codes for automation-facing scripts
- operational output clear and actionable

## Suggested Layout

Single-file script:

```text
script.py
```

Small script plus helpers:

```text
scripts/
├── sync_data.py
└── _helpers.py
```

## UV Script Checklist

### Metadata

- [ ] inline metadata block present and valid
- [ ] Python version explicit
- [ ] dependencies minimal and justified

### Script Design

- [ ] arguments and usage clear
- [ ] side effects explicit
- [ ] errors useful and actionable
- [ ] output readable or machine-friendly as needed

### Safety

- [ ] file paths validated
- [ ] dangerous commands require explicit intent
- [ ] no secrets inside script
- [ ] network and subprocess usage obvious

### Verification

- [ ] happy path exercised
- [ ] failure path exercised
- [ ] representative sample input tested
- [ ] repeated runs safe when script should be idempotent

## Project-Specific Guardrails

<!-- - Keep operational scripts deterministic -->
<!-- - Do not silently overwrite files -->
<!-- - Promote to package once multiple modules or commands appear -->
