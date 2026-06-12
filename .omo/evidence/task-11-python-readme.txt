QA Evidence: task-11-python-readme
====================================

Line count check:
146 /home/oornnery/proj/agents/.aikit/templates/python/README.md
PASS: 146 lines >= 60 required

Section check (all H2 headings present):
  3:## Overview
  7:## Quick Start
 20:## Project Structure
 67:## Available Commands
 88:## Configuration
116:## Docker Usage
126:## CI/CD Setup
PASS: All 7 required sections found

Task references check:
PASS: fmt mentioned in Available Commands
PASS: lint mentioned in Available Commands
PASS: type mentioned in Available Commands
PASS: test mentioned in Available Commands
PASS: check mentioned in Available Commands
PASS: mdlint mentioned in Available Commands
PASS: mdfmt mentioned in Available Commands
PASS: sec mentioned in Available Commands

Validation flow check:
PASS: "fmt → lint → type → mdlint → test" found in check task description

Broken reference check:
PASS: All files referenced in README exist in template:
  - src/myapp/ exists
  - tests/ exists
  - scripts/init.sh exists
  - pyproject.toml exists
  - ruff.toml exists
  - ty.toml exists
  - .rumdl.toml exists
  - .pre-commit-config.yaml exists
  - docker/Dockerfile exists
  - docker/compose.yml exists
  - .github/ci.yml exists
  - .github/publish.yml exists

No uv installation instructions: PASS
Not a tutorial (reference document): PASS
