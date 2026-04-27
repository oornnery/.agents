---
name: typescript-web
description: Plan, sell, design, and implement TypeScript web apps with React Router Framework Mode, Vite, Hono, Zod, Drizzle, SQLite/Supabase, Tailwind, shadcn/ui, lucide-react, Vitest, and Playwright.
---

# TypeScript Web

Use for JS/TS-first websites, landings, booking/order/catalog/admin systems, dashboards, BFFs, and small productized business apps. Local-business projects are a primary use case, not the skill name/boundary.

Do not use Python implementation patterns. Borrow architecture/design/quality/security concepts from repo skills only as guidance; code stays in the JS/TS stack.

## Triggers

- build/plan a TypeScript React site/app
- create a landing, small commerce/catalog, booking, ordering, dashboard, CRM/leads, cash-flow, or admin system
- scope a sellable web package from public/user-provided business data
- design React Router + Hono + Zod + Drizzle boundaries
- implement with Tailwind/shadcn/ui/lucide, Vitest, Playwright

## Boundary

Covers:

- public-data discovery, brief, scope, SDD-lite, route map, data model, API/contracts
- React Router Framework Mode, Vite, Hono, Zod, Drizzle, SQLite/Supabase
- responsive UI, accessibility, tests, deployment readiness

Excludes:

- Python backends/tooling
- paid ads ops, fake reviews, spam, ToS bypass, private scraping
- sensitive medical records or unnecessary personal data
- enterprise architecture unless explicitly required

## Stack

Default unless repo already has compatible conventions:

- TypeScript strict, Node.js, pnpm
- React + React Router Framework Mode + Vite
- Tailwind CSS + shadcn/ui + lucide-react
- React Aria Table/Collections for interactive admin tables
- Hono API/BFF
- Zod contracts/validation
- Drizzle ORM; SQLite local; Supabase Postgres/Auth/Storage only when persistence/auth/storage needs it
- Vitest; Playwright for critical flows

Avoid extra frameworks/deps without a real requirement.

## Product Profiles

Pick one primary profile; list secondary modules separately.

| Profile              | Use when                      | Core scope                                     |
| -------------------- | ----------------------------- | ---------------------------------------------- |
| `static-site`        | presence/content              | pages, SEO, CTA, contact, map/social           |
| `conversion-landing` | one offer/campaign            | offer, proof, FAQ, lead form, WhatsApp/events  |
| `booking-system`     | appointments                  | services, availability, booking, admin status  |
| `ordering-system`    | food/service orders           | menu, cart, customer info, WhatsApp/admin hand |
| `catalog-commerce`   | products/light commerce       | catalog, search, cart intent, admin catalog    |
| `admin-dashboard`    | internal ops/cash-flow/leads  | CRUD, summaries, filters, export, permissions  |
| `custom-ops`         | specific workflow             | domain model + one vertical slice              |

## Reference Map

- Research/business facts/sales positioning: `references/discovery.md`
- Package/module selection: `references/product-catalog.md`
- Routes, DB, API, auth, deployment: `references/architecture.md`
- Coding workflow/patterns: `references/implementation.md`
- Final verification: `references/checklists.md`

## Workflow

1. Inspect repo: package manager, scripts, TS config, routing, DB, tests. Reuse conventions.
2. Build `Business Brief` if business context matters: confirmed facts, user facts, assumptions, unknowns, goals.
3. Choose profile/package; define MVP, phase 2, out of scope.
4. Produce/update SDD-lite before nontrivial code:
   - `docs/business-brief.md`
   - `docs/SPEC.md`
   - `docs/ARCHITECTURE.md`
   - `docs/DELIVERY_PLAN.md`
5. Define route map, flows, entities/tables, Zod contracts, auth/deployment assumptions, acceptance criteria.
6. Implement one vertical slice first: contract -> schema/migration -> loader/action or Hono route -> UI -> tests -> docs.
7. Validate with repo scripts; prefer `pnpm typecheck`, `pnpm test`, `pnpm build`, `pnpm exec playwright test`.

## Architecture Defaults

Simple site:

```txt
app/{routes,components,features,lib,styles}
```

Persisted system:

```txt
apps/web/app/{routes,features,components,lib}
apps/api/src/{routes,modules,middleware}
packages/{schemas,db,ui,config}
```

Dependency direction:

```txt
web -> schemas -> db types/contracts
api -> schemas -> db
ui -> no db imports
features -> shared only through extracted package/module
```

Keep business rules testable; IO/framework/provider code stays at edges.

## Output

Planning responses include: summary, package/profile, MVP, phase 2, out of scope, route map, data model, architecture, checklist, risks/questions.

Implementation responses include: files changed, behavior added, validation run, assumptions/remaining confirmations.
