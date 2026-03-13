# rumdl Reference

Use this reference when the task includes Markdown linting, formatting, or
project-wide docs validation.

## Install

```bash
uv tool install rumdl
```

## Common Commands

```bash
uv run rumdl check .
uv run rumdl check --fix .
uv run rumdl fmt .
uv run rumdl init
```

## Recommended `.rumdl.toml`

```toml
[global]
extend-enable = ["MD060"]
disable = ["MD013"]
include = ["README.md", "docs/**/*.md"]
line_length = 0

[MD060]
enabled = true
style = "aligned"
```

## Validation Checklist

```bash
rumdl --version
uv run rumdl check .
```

## Usage Notes

- Use `check` in CI and validation flows.
- Use `check --fix` when the repo accepts automatic Markdown rewrites.
- Use `fmt` when you want formatting without applying other lint fixes.
- Keep config close to the repo root unless the project already centralizes it
  elsewhere.
