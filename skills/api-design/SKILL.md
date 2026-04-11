---
name: api-design
description: REST API design patterns -- RESTful conventions, OpenAPI, BFF, pagination, error handling, versioning. Load when designing APIs, defining contracts, or structuring HTTP endpoints.
---

# API Design

Conventions for consistent HTTP APIs.

## RESTful Conventions

- Resources are **nouns** (plural): `/users`, `/orders`, `/products`
- Actions are **HTTP verbs**: `POST /orders`, not `POST /create-order`
- Nested resources for relationships: `GET /users/{id}/orders`
- Limit nesting to 2 levels

### Status Codes

| Code | When                          |
| ---- | ----------------------------- |
| 200  | Successful GET, PUT, PATCH    |
| 201  | Successful POST               |
| 204  | Successful DELETE             |
| 400  | Malformed request body        |
| 401  | Missing or invalid auth       |
| 403  | Authenticated but not allowed |
| 404  | Resource does not exist       |
| 409  | Duplicate key, state conflict |
| 422  | Valid JSON, invalid data      |
| 429  | Rate limit exceeded           |

### Response Shapes

```python
# Single item
{"id": "abc", "name": "Alice", "email": "a@b.co"}

# Collection
{"items": [...], "total": 42, "page": 1, "page_size": 20}

# Error (RFC 7807)
{"type": "...", "title": "Validation Error", "status": 422, "detail": "...", "errors": [...]}
```

## Pagination

- **Offset-based**: `?page=2&page_size=20` -- for admin panels, small datasets.
- **Cursor-based**: `?cursor=...&limit=20` -- for infinite scroll, large datasets.
- Filtering: `?status=active&role=admin`
- Sorting: `?sort=-created_at` (prefix `-` for desc)
- Field selection: `?fields=id,name,email`

## Error Handling (RFC 7807)

Use Problem Details format with field-level errors for validation failures.
Return `Retry-After` header on 429 responses.

## Versioning

- **URL path** (recommended): `/api/v1/users`
- Start without versioning until the first breaking change.
- Support at most 2 versions simultaneously.
- Return `Sunset` and `Deprecation` headers for deprecated versions.

## BFF -- Backend for Frontend

Use when different frontends need different data shapes or aggregation.
Skip when: single frontend, API already well-suited, would just be pass-through.

## Related

- `skills/fastapi/SKILL.md` -- FastAPI implementation patterns
- `skills/pydantic/SKILL.md` -- request/response schema design
- `skills/httpx/SKILL.md` -- API client patterns
