# API

Shape HTTP contracts before impl. Framework-agnostic rules; examples assume Python/FastAPI/Pydantic.

## When to Use

- new REST endpoints
- CRUD contracts
- query params, pagination, filtering, sorting
- standardizing success/error shapes
- route layout, auth boundaries, nested resources

## Core REST Conventions

### Resource Naming

Nouns, preferably plural.

| Resource | Endpoint        |
| -------- | --------------- |
| project  | `/api/projects` |
| user     | `/api/users`    |
| task     | `/api/tasks`    |

Avoid verb-heavy routes:

- `POST /api/create-project`
- `GET /api/getUsers`

Prefer:

- `GET /api/projects`
- `POST /api/projects`
- `GET /api/projects/{project_id}`

### HTTP Methods

| Method | Purpose        | Example                     |
| ------ | -------------- | --------------------------- |
| GET    | read           | `GET /api/projects`         |
| POST   | create         | `POST /api/projects`        |
| PATCH  | partial update | `PATCH /api/projects/{id}`  |
| PUT    | full replace   | `PUT /api/projects/{id}`    |
| DELETE | remove         | `DELETE /api/projects/{id}` |

### URL Structure

```text
/api/{resource}
/api/{resource}/{id}
/api/{resource}/{id}/{sub_resource}
```

Rules:

- nesting depth max two levels
- route names describe resources, not internal impl
- path params explicit and stable: `{project_id}`, not `{x}`

Examples:

- `GET /api/projects`
- `POST /api/projects`
- `GET /api/projects/{project_id}`
- `PATCH /api/projects/{project_id}`
- `DELETE /api/projects/{project_id}`
- `GET /api/projects/{project_id}/tasks`

## Python Translation

- Pydantic models over Zod schemas
- FastAPI `Annotated` params for `Path`, `Query`, `Header`, `Depends`
- `response_model` or explicit return types for stable response filtering
- thin routers; valid/contract logic at API boundary
- domain/persistence details out of route signatures and response types

## FastAPI Layout

Separate routes, schemas, dependencies, error mapping.

```text
src/myapp/api/
├── router.py
├── dependencies.py
├── errors.py
├── responses.py
├── routes/
│   ├── projects.py
│   └── users.py
└── schemas/
    ├── common.py
    └── projects.py
```

Defaults:

- one router module per resource or cohesive sub-resource
- shared pagination, error, auth dependencies in `dependencies.py` or `responses.py`
- Pydantic request/response models in `schemas/`
- services injected into routes, no inline DB logic

## Response Shapes

One success family, consistent across API.

### Success

Single item:

```json
{
  "data": {
    "id": "123",
    "name": "Project Alpha",
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

Collection:

```json
{
  "data": [
    { "id": "123", "name": "Project Alpha" },
    { "id": "124", "name": "Project Beta" }
  ],
  "meta": {
    "total": 42,
    "page": 1,
    "page_size": 20
  }
}
```

Delete: `204 No Content`, no body.

### Errors

Problem Details style, optional field errors.

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 422,
  "detail": "Request body failed validation",
  "errors": [
    { "field": "email", "message": "Invalid email format" }
  ]
}
```

Rules:

- error shape as stable as success shape
- field-level issues for valid failures
- no stack traces, raw SQL errors, or library internals
- map internal exceptions to HTTP errors at boundary
- `Retry-After` on `429` when rate limiting

## Status Codes

| Code | When                             |
| ---- | -------------------------------- |
| 200  | successful `GET`, `PUT`, `PATCH` |
| 201  | successful `POST`                |
| 204  | successful `DELETE`              |
| 400  | malformed request structure      |
| 401  | missing or invalid auth          |
| 403  | authenticated but not allowed    |
| 404  | resource does not exist          |
| 409  | duplicate key or state conflict  |
| 422  | well-formed input, invalid data  |
| 429  | rate limit exceeded              |

## Request Models

Separate models for create, update, read.

```python
from datetime import datetime

from pydantic import BaseModel, Field


class PageMeta(BaseModel):
    total: int
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=100)


class FieldError(BaseModel):
    field: str
    message: str


class ProblemDetail(BaseModel):
    type: str
    title: str
    status: int
    detail: str
    errors: list[FieldError] = Field(default_factory=list)


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None


class ProjectPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    status: str | None = None


class ProjectOut(BaseModel):
    id: str
    name: str
    description: str | None = None
    status: str
    created_at: datetime


class ProjectListOut(BaseModel):
    data: list[ProjectOut]
    meta: PageMeta
```

Rules:

- request models reflect what clients send, not DB rows
- response models reflect what clients see, not ORM entities
- `PATCH` models usually have optional fields
- no reusing internal persistence types as public contract types

## Boundary Helpers

Small, boring response/error helpers.

```python
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def data_response(data: object, status_code: int = 200, meta: dict | None = None) -> JSONResponse:
    payload = {"data": data}
    if meta is not None:
        payload["meta"] = meta
    return JSONResponse(status_code=status_code, content=jsonable_encoder(payload))


def problem_response(
    *,
    type_: str,
    title: str,
    status_code: int,
    detail: str,
    errors: list[dict] | None = None,
) -> JSONResponse:
    payload = {
        "type": type_,
        "title": title,
        "status": status_code,
        "detail": detail,
        "errors": errors or [],
    }
    return JSONResponse(status_code=status_code, content=payload)
```

Use helpers when they stabilize envelopes and reduce duplication. No response abstraction jungle for simple routes.

## FastAPI Example

Thin route, explicit contract.

```python
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Response, status

from myapp.api.schemas.projects import ProjectCreate, ProjectListOut, ProjectOut, ProjectPatch
from myapp.services.projects import ProjectService, get_project_service

router = APIRouter(prefix="/projects", tags=["projects"])
ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]


@router.get("", response_model=ProjectListOut)
def list_projects(
    service: ProjectServiceDep,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    status_filter: Annotated[str | None, Query(alias="status")] = None,
    search: Annotated[str | None, Query()] = None,
) -> ProjectListOut:
    return service.list_projects(
        page=page,
        page_size=page_size,
        status=status_filter,
        search=search,
    )


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    service: ProjectServiceDep,
) -> ProjectOut:
    return service.create_project(payload)


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
    project_id: Annotated[str, Path(min_length=1)],
    service: ProjectServiceDep,
) -> ProjectOut:
    return service.get_project(project_id)


@router.patch("/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: Annotated[str, Path(min_length=1)],
    payload: ProjectPatch,
    service: ProjectServiceDep,
) -> ProjectOut:
    return service.update_project(project_id, payload)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: Annotated[str, Path(min_length=1)],
    service: ProjectServiceDep,
) -> Response:
    service.delete_project(project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

## Query Parameters

### Filtering

```text
GET /api/projects?status=active&owner=alice
```

### Sorting

```text
GET /api/projects?sort=-created_at
```

Rules:

- sort keys documented and whitelisted
- one sort param over loosely-defined combinations
- `-field` or explicit `order=desc`, stay consistent

### Search

```text
GET /api/projects?search=alpha
```

Rules:

- predictable search behavior
- document prefix, substring, exact, or ranked
- enforce sensible page/result size limits

### Pagination

Offset pagination for admin lists, modest datasets:

```text
GET /api/projects?page=2&page_size=20
```

Cursor pagination for feeds, streams, large datasets:

```text
GET /api/projects?cursor=opaque-token&limit=20
```

## Auth and Ownership

- authenticate before reading sensitive data or mutations
- authorize against target resource, not only route
- check ownership/tenant scope before update/delete
- no route convenience bypassing domain authorization

## Contract Rules

- design happy path and failure path together
- define create, list, read, update, delete semantics explicitly
- no mixing raw ORM objects, DTOs, response models in one surface
- nullability intentional and documented
- prefer additive evolution over breaking response changes

## BFF Boundary

Client needs aggregated/reshaped payloads that don't match core resource model? Load [bff.md](bff.md) over overloading base API contract.

## API Checklist

- plural resource names
- stable success and error shapes
- explicit status codes
- validated path, query, body input
- response models filter output intentionally
- pagination limits and documented defaults
- auth/ownership checks on sensitive routes
- no leaked internal exceptions or persistence types
