# Checks

<!-- checks.md exists so every agent knows exactly which commands prove correctness without rediscovering the toolchain. -->

> Known validation commands and latest meaningful results.

## Validation Commands

<!-- This table maps each quality surface to a concrete command so any agent can run checks without guessing the toolchain. -->

| Surface  | Command                               | When                   | Notes                              |
| -------- | ------------------------------------- | ---------------------- | ---------------------------------- |
| format   | `uv run ruff format .`                | before completion      | auto-fixes style in place          |
| lint     | `uv run ruff check . --fix`           | before completion      | catches bugs and style violations  |
| type/LSP | `uv run ty check src && uv run pyright` | typed code changes     | two-pass type checking for safety  |
| tests    | `uv run pytest -v`                    | behavior changes       | runs unit and integration suites   |
| build    | `uv run docker build -t task-api .`   | app/package changes    | verifies container image builds    |
| security | `uv run bandit -r src`                | trust-boundary changes | scans for known Python vulnerabilities |
| markdown | `uv run rumdl check .`                | doc changes            | lints markdown files               |
| audit    | `uv run pip-audit`                    | dependency changes     | checks for CVEs in dependencies    |

## Latest Results

<!-- Recording latest results here creates a quick health dashboard and catches regressions without re-running the full suite. -->

| Date       | Command                               | Result | Notes                                      |
| ---------- | ------------------------------------- | ------ | ------------------------------------------ |
| 2025-06-12 | `uv run ruff format .`                | PASS   | no changes needed                          |
| 2025-06-12 | `uv run ruff check . --fix`           | PASS   | 0 errors, 0 warnings                       |
| 2025-06-12 | `uv run ty check src && uv run pyright` | PASS   | 0 type errors across 12 modules            |
| 2025-06-12 | `uv run pytest -v`                    | PASS   | 42 tests, 85% coverage, 2 skipped          |
| 2025-06-12 | `uv run bandit -r src`                | PASS   | no high-severity issues found              |
| 2025-06-12 | `uv run rumdl check .`                | PASS   | 0 markdown lint errors                     |
| 2025-06-11 | `uv run pip-audit`                    | PASS   | 0 known CVEs in locked dependencies        |
