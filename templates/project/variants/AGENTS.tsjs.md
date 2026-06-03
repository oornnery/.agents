# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!-- TS/JS overlay. Keep detailed TS/JS guidance in skills/typescript-web. -->

## Project Description

<!-- What this TS/JS project does, main constraints, critical boundaries -->

## Stack Defaults

- **Runtime**: Node.js
- **Language**: TypeScript strict when supported
- **Package Manager**: pnpm for greenfield; otherwise use the repo lockfile
- **Frontend Build**: Vite for greenfield React apps
- **UI App**: React + React Router for greenfield web apps
- **Validation**: Zod at external boundaries when validation is needed
- **Tests**: Vitest and Playwright for critical browser flows
- **Styling/UI**: Tailwind + shadcn/ui + lucide-react when useful
- **API/BFF**: Hono for small TS HTTP services or BFFs
- **Persistence**: Drizzle with SQLite/Postgres when persistence is needed

Do not replace an established repo stack with these defaults unless the request requires it.

## Quick Commands

```bash
pnpm install
pnpm dev
pnpm typecheck
pnpm test
pnpm build
```

## Validation Entry Points

Use configured commands only:

```bash
pnpm check
pnpm lint
pnpm typecheck
pnpm test
pnpm build
pnpm exec playwright test
pnpm audit --prod
```

Do not add tools only because this template lists them.

## Skill Routing

- Load `skills/typescript-web/SKILL.md` for TS/JS, Vite, React, React Router, Hono, Zod, Drizzle, frontend, API, or productized web work.
- Load `skills/design/SKILL.md` or an installed UI critique skill for meaningful UI work.
- Load `skills/verification/SKILL.md` before final validation or check repair.
- Load `skills/project-state/SKILL.md` when scope, decisions, memory, validation, or next steps changed.
- Load `skills/security/SKILL.md` when work touches trust boundaries.

## Always-On TS/JS Rules

- Identify package manager from lockfile before running commands.
- Keep `strict` types useful; do not silence errors with broad `any` or unsafe casts.
- Parse `unknown` data at boundaries before passing typed values inward.
- Keep env parsing, secrets, base URLs, timeout, retry, and fetch/client setup centralized.
- Do not put business rules or permission decisions only in the browser.
- Avoid new dependencies or framework complexity without a real need.

## Project-Specific Guardrails

<!-- - Keep public package exports stable -->
<!-- - Do not bypass typed env parsing -->
<!-- - Keep shared contracts in packages/schemas -->
