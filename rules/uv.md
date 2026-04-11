---
description: uv package management conventions -- applies to Python projects
globs: "**"
---

# Uv Conventions

- Always use `uv` over `pip` -- never `pip install`, `pip freeze`, `python -m pip`
- Use `uv run` to execute project commands -- never activate venvs manually
- Use `uvx` for one-off tool execution outside the project environment
- Add dependencies with `uv add`, dev deps with `uv add --dev`
- Commit `uv.lock` for reproducible installs
- Use `uv sync --frozen` in CI to catch lockfile drift
- Use `uv sync --no-dev` for production installs
- Pin Python version with `.python-version`
- Use `uv tool install` for global tooling (ruff, ty, rumdl)
