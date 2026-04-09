---
name: api-design
description: REST API design patterns — RESTful conventions, OpenAPI, BFF, pagination, error handling, versioning. Load when designing APIs, defining contracts, or structuring HTTP endpoints.
---

# API Design

Conventions and patterns for designing consistent, well-documented HTTP APIs.

## RESTful Conventions

### Resources and Verbs

```text
GET    /api/users           → List users (paginated)
POST   /api/users           → Create user
GET    /api/users/{id}      �� Get user by ID
PUT    /api/users/{id}      → Replace user (full update)
PATCH  /api/users/{id}      → Partial update
DELETE /api/users/{id}      → Delete user
```

**Rules:**

- Resources are **nouns** (plural): `/users`, `/orders`, `/products`
- Actions are **HTTP verbs**, not URL paths: `POST /orders`, not `POST /create-order`
- Nested resources for relationships: `GET /users/{id}/orders`
- Limit nesting to 2 levels: `/users/{id}/orders/{id}` (not deeper)

### Status Codes

| Code | Meaning               | When                          |
| ---- | --------------------- | ----------------------------- |
| 200  | OK                    | Successful GET, PUT, PATCH    |
| 201  | Created               | Successful POST               |
| 204  | No Content            | Successful DELETE             |
| 400  | Bad Request           | Malformed request body        |
| 401  | Unauthorized          | Missing or invalid auth       |
| 403  | Forbidden             | Authenticated but not allowed |
| 404  | Not Found             | Resource does not exist       |
| 409  | Conflict              | Duplicate key, state conflict |
| 422  | Unprocessable Entity  | Valid JSON, invalid data      |
| 429  | Too Many Requests     | Rate limit exceeded           |
| 500  | Internal Server Error | Unexpected server failure     |

### Response Shapes

```python
# Success (single item)
{"id": "abc", "name": "Alice", "email": "a@b.co"}

# Success (collection)
{"items": [...], "total": 42, "page": 1, "page_size": 20}

# Error (RFC 7807 Problem Details)
{
    "type": "https://api.example.com/errors/validation",
    "title": "Validation Error",
    "status": 422,
    "detail": "Email is required",
    "errors": [
        {"field": "email", "message": "Field is required"}
    ]
}
```

## Pagination

### Offset-Based (Simple)

```text
GET /api/users?page=2&page_size=20

Response:
{
    "items": [...],
    "total": 150,
    "page": 2,
    "page_size": 20,
    "pages": 8
}
```

Best for: admin panels, dashboards, small datasets.

### Cursor-Based (Scalable)

```text
GET /api/users?cursor=eyJpZCI6MTAwfQ&limit=20

Response:
{
    "items": [...],
    "next_cursor": "eyJpZCI6MTIwfQ",
    "has_more": true
}
```

Best for: infinite scroll, large datasets, real-time feeds.

### Filtering and Sorting

```text
GET /api/users?status=active&role=admin&sort=-created_at&fields=id,name,email
```

- Filter by field: `?status=active`
- Multiple values: `?role=admin,editor`
- Sort: `?sort=name` (asc), `?sort=-name` (desc)
- Field selection: `?fields=id,name,email`

## Error Handling

### RFC 7807 Problem Details

Standardized error format:

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse


class ProblemDetail(BaseModel):
    type: str = "about:blank"
    title: str
    status: int
    detail: str
    errors: list[dict[str, str]] = []


def problem_response(status: int, title: str, detail: str, **kwargs) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content=ProblemDetail(status=status, title=title, detail=detail, **kwargs).model_dump(),
    )
```

### Validation Errors

Return structured errors with field-level detail:

```python
{
    "type": "https://api.example.com/errors/validation",
    "title": "Validation Error",
    "status": 422,
    "detail": "Request body has invalid fields",
    "errors": [
        {"field": "email", "message": "Not a valid email address"},
        {"field": "age", "message": "Must be at least 18"}
    ]
}
```

## Versioning

### URL Path (Recommended)

```text
/api/v1/users
/api/v2/users
```

Simple, explicit, easy to route. Use when: breaking changes are infrequent.

### Header-Based

```text
Accept: application/vnd.myapp.v2+json
```

Cleaner URLs but harder to test. Use when: URL cleanliness is critical.

### Strategy

- Start without versioning until the first breaking change
- Version the entire API, not individual endpoints
- Support at most 2 versions simultaneously
- Deprecation: return `Sunset` header and `Deprecation` header

## BFF — Backend for Frontend

A thin API layer tailored to each frontend's needs.

```text
┌──────────┐  ┌──────────┐  ┌──────���───┐
│  Mobile  │  │   Web    │  │   CLI    │
│   App    │  │   SPA    │  │   Tool   │
└────┬─────┘  └────┬─────┘  └���───┬─────┘
     │             │              │
     ▼             ▼              ▼
┌──────────┐  ┌─��────────┐  ┌──────────┐
│ Mobile   │  │  Web     │  │  CLI     │
│  BFF     │  │  BFF     │  │  BFF     │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │              │
     └─────────────┼──────────────┘
                   ▼
          ┌────────────────┐
          │  Core Services │
          └────────────────��
```

**When to use BFF:**

- Different frontends need different data shapes
- Mobile needs fewer fields, web needs more
- Frontend aggregation of multiple services
- Platform-specific auth flows

**When NOT to use BFF:**

- Single frontend
- API is already well-suited to the frontend
- Would just be a pass-through proxy

## Rate Limiting

```text
HTTP/1.1 429 Too Many Requests
Retry-After: 60
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1625000000
```

Communicate limits via headers so clients can self-regulate.

## OpenAPI / Documentation

FastAPI generates OpenAPI specs automatically. Enhance them:

```python
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
    summary="Create a new user",
    description="Creates a user account and sends a welcome email.",
    responses={
        409: {"description": "Email already registered"},
        422: {"description": "Validation error"},
    },
)
async def create_user(data: CreateUserRequest) -> UserResponse: ...
```

## Related

- `skills/fastapi/SKILL.md` — FastAPI implementation patterns
- `skills/pydantic/SKILL.md` — request/response schema design
- `skills/architecture/SKILL.md` — service layer and DDD patterns
- `commands/plan.md` — API route specification in ARCH.md
