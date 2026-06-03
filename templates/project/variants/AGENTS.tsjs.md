# Project Name

@.agents/templates/project/variants/AGENTS.base.md

<!--
TS/JS project overlay.
Use for TypeScript or JavaScript apps, packages, Node services, React/Vite
frontends, BFFs, CLIs, and internal tools.
-->

## Project Description

<!-- Brief description of what this TS/JS project does and its main constraints -->

## Stack Defaults

- **Runtime**: Node.js
- **Language**: TypeScript strict when the repo supports TS
- **Package Manager**: pnpm for greenfield; otherwise use the repo lockfile
- **Frontend Build**: Vite for greenfield React apps
- **UI App**: React + React Router for greenfield web apps
- **Validation**: Zod at external boundaries when validation is needed
- **Tests**: Vitest for unit/integration, Playwright for critical browser flows
- **Styling/UI**: Tailwind + shadcn/ui + lucide-react when a component system is useful
- **API/BFF**: Hono for small TS HTTP services or BFFs
- **Persistence**: Drizzle with SQLite/Postgres when persistence is needed

For new TS/JS web apps, prefer the simple modern stack: Vite, React, React Router, TypeScript, pnpm, Zod, Vitest, and Playwright for critical flows.

Do not replace an established repo stack with this default unless the request requires it. Avoid Next.js, Remix-style complexity, GraphQL, Redux, or heavy state/framework choices unless the product need is clear.

## Quick Commands

```bash
pnpm install
pnpm dev
pnpm typecheck
pnpm test
pnpm build
pnpm exec playwright test
```

## Validation Entry Points

Use configured scripts first.

```bash
pnpm lint
pnpm typecheck
pnpm test
pnpm build
pnpm exec playwright test
```

Run only installed/configured tools. Do not add ESLint, Biome, Vitest, Playwright, or typecheck scripts just because this template mentions them.

## TS/JS Discovery

- Identify package manager from lockfile before running commands
- Read `package.json` scripts, `tsconfig*`, build config, test config, route structure, and workspace layout
- Determine project type before editing: frontend, backend, package, CLI, fullstack, or monorepo
- For greenfield web UI, choose Vite + React + React Router unless the user requests another framework
- Inspect nearby components/modules/tests before adding new structure
- Prefer existing export style, import aliases, state management, validation, and test patterns

## Package and Tooling Rules

- Use the repo package manager; do not mix pnpm/npm/yarn/bun
- Add dependencies only when existing deps or platform APIs do not solve the request cleanly
- Prefer small, well-known libraries already present in the repo over new packages
- Keep generated files, lockfiles, and build artifacts out of edits unless the change requires them
- In workspaces, edit the correct package and run checks from the right root

## Layout Defaults

Frontend:

```text
app/
├── routes/
├── features/
├── components/
├── lib/
└── styles/
```

Service or monorepo:

```text
apps/web/
apps/api/
packages/schemas/
packages/db/
packages/ui/
packages/config/
```

Match the repo's actual layout over these examples.

## TypeScript Rules

- Keep `strict` types useful; do not silence errors with broad `any`, `as unknown as`, or non-null assertions
- Parse `unknown` data at boundaries, then pass typed values inward
- Use Zod or existing validators for external input, env, API responses, forms, webhooks, and DB-facing payloads
- Keep domain types, transport DTOs, DB models, and UI props separate when their shapes differ
- Prefer explicit return types on public functions, loaders/actions, handlers, and exported helpers
- Use type-only imports where the repo style expects them
- Prefer discriminated unions for state machines and result shapes

## Runtime Rules

- Do not hide async side effects inside helpers with harmless names
- Always handle promises intentionally: await, return, or explicitly detach with lifecycle/error handling
- Centralize env parsing, secrets, base URLs, timeout, retry, and fetch/client setup
- Never trust client-provided user id, role, tenant id, price, status, or ownership fields
- Keep deterministic routing, retry, status-code handling, and transforms in code, not AI/model calls
- Avoid module-level mutable state unless lifecycle and concurrency are understood

## Frontend Rules

- Prefer React Router routes/loaders/actions for app navigation and data flow when building a full React app
- Prefer simple local state, URL state, or server data before adding global state libraries
- Components should be small and purpose-named; extract only when reuse or complexity is real
- Keep server/client boundaries explicit in frameworks that have them
- Keep form validation, loading, empty, error, success, and disabled states visible
- Use accessible semantic HTML and keyboard/focus behavior for interactive controls
- Use existing design primitives before creating new UI patterns
- For greenfield UI, use lucide icons and shadcn/ui primitives when they simplify common controls
- Do not put business rules or permission decisions only in the browser

## API and Data Rules

- Keep handlers thin: parse, authorize, call service, shape response
- Keep shared contracts in one place when frontend and backend both depend on them
- Validate request bodies, query params, headers, cookies, webhooks, and external API responses
- Use parameterized queries/ORM APIs; never concatenate untrusted SQL
- Avoid N+1 queries, unbounded reads, and hidden per-item network/database calls
- Make pagination, sorting, filtering, idempotency, and error shapes explicit

## Testing Rules

- Unit-test pure logic and reducers/state machines
- Integration-test API contracts, loaders/actions, DB queries, and external boundary adapters
- Use Playwright for critical user flows, auth flows, and UI behavior that unit tests cannot prove
- Tests should encode intent and failure mode, not only snapshots or "renders without crashing"
- Mock network/provider boundaries, not business logic

## Review Focus

- broad `any`, unsafe casts, or ignored type errors
- unhandled promises, async races, stale closures, or effect dependency bugs
- server/client boundary leaks
- validation missing at API, env, form, webhook, or external-response boundaries
- auth/permission checks only in UI
- new dependency or framework introduced without real need
- tests asserting snapshots or constants without business intent
- build artifacts or generated output changed unnecessarily

## Project-Specific Guardrails

<!-- - Keep public package exports stable -->
<!-- - Do not bypass typed env parsing -->
<!-- - Keep shared contracts in packages/schemas -->
