# Architecture

Use when defining routes, data model, API/BFF, auth, storage, deployment, or module boundaries.

## Decision Flow

1. Marketing/content only: React Router app; no DB/backend unless forms/webhooks exist.
2. Forms/orders/bookings/admin/persistence: add Hono, Zod contracts, Drizzle schema, SQLite local; Supabase Postgres for production persistence.
3. Accounts/admin: Supabase Auth only when login is required; prefer admin-only auth for small systems.
4. Uploads: Supabase Storage or small provider adapter; never commit uploads.

## Layouts

Simple app:

```txt
app/{routes,components,features,lib,styles}
```

System/monorepo only when boundaries are real:

```txt
apps/web/app/{routes,features,components,lib}
apps/api/src/{routes,modules,middleware}
packages/schemas/src
packages/db/src
packages/ui/src
packages/config/src
```

## Boundaries

- Zod owns request/response contracts.
- Drizzle owns persistence.
- UI never imports DB.
- Feature modules own routes/components/actions.
- Shared packages exist only for reused code.
- Provider integrations sit behind adapters.

## Route Map Template

```md
| Route | Type | Purpose | Data source | Auth |
| --- | --- | --- | --- | --- |
| `/` | public | homepage | static/loader | no |
| `/services` | public | service list | loader/db | no |
| `/book` | public | create appointment | action/api | no |
| `/admin` | private | dashboard | api/db | yes |
```

## Data Model Template

```md
| Entity | Purpose | Main fields | Notes |
| --- | --- | --- | --- |
| Customer | contact/person | name, phone, email | minimize data |
| Appointment | scheduled service | serviceId, date, status | no medical records |
| Order | customer order | total, status, channel | payment optional |
```

## API Rules

- Validate every input with Zod.
- Return typed success/error envelopes.
- Use consistent status codes.
- Keep errors safe/useful; do not leak DB internals.

```ts
type ApiSuccess<T> = { ok: true; data: T };
type ApiError = {
  ok: false;
  error: { code: string; message: string; fieldErrors?: Record<string, string[]> };
};
```

## Security/LGPD Baseline

Collect minimum personal data, protect admin routes/APIs, validate server-side, keep secrets in env vars, never commit `.env`, add rate limiting/bot protection when public forms are abused.
