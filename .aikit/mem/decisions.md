---
updated_at: 2025-03-22
---

# Decisions

<!-- Decisions live here so future agents know why the codebase looks the way it does. Rationale prevents endless re-debating settled questions. -->

## Accepted Decisions

These choices shape the architecture and are unlikely to change without a major version bump.

| Date       | Decision | Reason  | Impact  |
| ---------- | -------- | ------- | ------- |
| 2025-03-15 | Use PostgreSQL | JSONB support for flexible Task metadata; ACID for concurrent updates | Slightly higher hosting cost than SQLite, but no migration pain later |
| 2025-03-18 | JWT over server-side sessions | Stateless auth scales horizontally without Redis session store | Tokens must be revoked via blocklist table; adds one DB round-trip per check |
| 2025-03-19 | REST over GraphQL | Team knows REST; simpler caching and monitoring; no N+1 query risk from resolvers | Front-end may need more requests; mitigated by compound endpoints |
| 2025-03-20 | Deploy on Fly.io | Native Docker + Postgres; good free tier; close to team geography | Vendor lock-in is mild; container is portable to other Docker hosts |
| 2025-03-21 | Cursor-based pagination for Task feeds | Consistent ordering when new Tasks are created during pagination | Offset pagination kept for simple admin endpoints only |

## Rejected Alternatives

<!-- Record rejected paths so no one re-opens a settled debate without new evidence. -->

| Date       | Alternative | Reason for Rejection |
| ---------- | ----------- | -------------------- |
| 2025-03-15 | SQLite for production | No concurrent write scalability; no native JSONB |
| 2025-03-18 | Session cookies in Redis | Extra infra to manage; Fly.io free tier does not include managed Redis |
| 2025-03-19 | GraphQL via Strawberry | Steep learning curve; overkill for CRUD-heavy API; monitoring harder |
| 2025-03-21 | Offset pagination for Task feeds | Cursor pagination is more reliable for real-time collaborative lists where items shift |
