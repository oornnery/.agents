# Node.js JavaScript Template

## Overview

A minimal Node.js project skeleton using native JavaScript with ESM, Vitest for testing, and Prettier/ESLint for code quality. There is no build step. The goal is to copy, rename, run the init script, and start writing code.

## Quick Start

1. Copy this template into a new project directory.
2. Update `name` in `package.json` to match your project.
3. Run the init script to install dependencies and verify the setup:

```bash
bash scripts/init.sh
```

This installs all dependencies and runs the full validation suite to confirm everything works.

## Project Structure

```
.
├── .env.example
├── .gitignore
├── README.md
├── package.json
├── scripts/
│   └── init.sh
├── src/
│   └── (your source files)
└── tests/
    └── (your test files)
```

| Path | Purpose |
|------|---------|
| `src/` | JavaScript source code. |
| `tests/` | Vitest test suite. |
| `scripts/init.sh` | One-time environment setup and validation script. |
| `package.json` | Project metadata, dependencies, and npm scripts. |
| `.env.example` | Template for environment variables. |
| `.gitignore` | Exclusions for dependencies, secrets, logs, and OS files. |

## Available Commands

| Script | Description |
|--------|-------------|
| `npm run test` | Run the test suite with Vitest |
| `npm run fmt` | Format code with Prettier |
| `npm run lint` | Lint with ESLint |
| `npm run check` | Full validation flow: `fmt`, `lint`, `test` |

Run the full validation flow before committing:

```bash
npm run check
```

## Configuration

### Code style

Add Prettier and ESLint to the project if you want automated formatting and linting. Configure them in `.prettierrc` and `eslint.config.js` respectively.

### Tests

Vitest is the test runner. Place test files in `tests/` or alongside source files with a `.test.js` suffix.

## Docker Usage

Build the image from the project root:

```bash
docker build -t myapp:latest .
```

A sample Dockerfile:

```dockerfile
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
CMD ["node", "src/index.js"]
```

## CI/CD Setup

A sample GitHub Actions workflow:

```yaml
name: CI
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npm ci
      - run: npm run check
```

This installs dependencies and runs the full validation flow on every pull request and push to `main`.
