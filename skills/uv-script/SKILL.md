---
name: uv-script
description: Build, review, or validate standalone Python scripts run with uv inline metadata. Use for one-file automation, operational scripts, script dependencies, shebangs, idempotency, safety, representative runs, and promoting scripts to packages.
---

# UV Script

Use for single-file or small-folder Python scripts where a full package would be unnecessary.

## Header Pattern

Use inline metadata for true standalone scripts:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx>=0.27",
#   "rich>=13.0",
# ]
# ///
```

Optional executable shebang:

```python
#!/usr/bin/env -S uv run
```

## Workflow

1. Inspect script purpose, arguments, side effects, dependencies, and repeatability.
2. Keep the main flow readable top-to-bottom.
3. Isolate helpers, but do not over-structure a one-off script.
4. Validate arguments early and fail with actionable errors.
5. Run a representative happy path and failure path.
6. Promote to a package when script gains modules, commands, shared logic, or tests that need project structure.

## Rules

- Dependencies live in inline metadata when the script is truly standalone.
- Use `uv run script.py` for execution.
- Side effects must be explicit and idempotent when repeat runs are expected.
- Do not silently overwrite files.
- Secrets stay outside the script.
- File, network, and subprocess operations must be easy to audit.

## Verification

- representative happy path
- representative failure path
- sample input/output
- repeated run behavior when idempotency matters
- lightweight tests when reused or critical
