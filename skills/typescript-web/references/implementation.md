# Implementation

Use when writing code.

## Scripts

Prefer existing scripts. If starting fresh:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:e2e": "playwright test"
  }
}
```

Adjust for React Router Framework Mode and deployment target.

## Vertical Slice

Build one flow end-to-end before adding screens:

1. Zod contract
2. Drizzle table/migration
3. loader/action or Hono route
4. UI form/table/card
5. validation, empty/loading/error/success states
6. Vitest
7. Playwright smoke for critical path
8. docs update

## Feature Shape

```txt
features/<domain>/
  <domain>.schema.ts
  <domain>.types.ts
  <domain>.api.ts
  <domain>.queries.ts
  <Domain>Form.tsx
  <Domain>List.tsx
  <domain>.test.ts
```

Use only when useful; tiny features can stay smaller.

## Forms

Zod is source of truth. Client validation improves UX; server validation is mandatory. Show field errors, preserve input on failure, include success/failure states.

## Tables/Admin Lists

Use React Aria Table/Collections for sorting, selection, keyboard nav, pagination, or collection state. Static display can use semantic HTML.

## UI

Mobile-first, clear above-fold CTA, shadcn/ui primitives, lucide-react icons, practical copy, accessible contrast, semantic HTML.

## React Router

Use loaders for render data, actions for mutations/forms, redirects after success when appropriate, route error boundaries, thin route files with logic in feature modules.

## Hono

Small routes, Zod body/query/params validation, middleware for auth/logging/CORS/context, DB access in query/service modules.

## Drizzle

Clear schema module/package, committed migrations, explicit table names, simple relations, seed demo data only in dev/test.

## Tests

Vitest: schemas, pure rules, API handlers when easy, mappers.

Playwright: lead form, booking, order/cart, admin login/CRUD smoke. Do not over-test static marketing sections.
