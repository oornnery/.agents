# API

Use this reference to shape HTTP contracts before implementation details.

The rules are framework-agnostic, but the examples here assume Python with
FastAPI and Pydantic because that is the current environment.

## When to Use

- creating new REST endpoints
- defining CRUD contracts
- designing query parameters, pagination, filtering, or sorting
- standardizing success and error shapes
- deciding route layout, auth boundaries, and nested resources

## Core REST Conventions

### Resource Naming

Resources are nouns and preferably plural.

| Resource | Endpoint        |
| -------- | --------------- |
| project  | `/api/projects` |
| user     | `/api/users`    |
| task     | `/api/tasks`    |

Avoid verb-heavy routes such as:

- `POST /api/create-project`
- `GET /api/getUsers`

Prefer:

- `GET /api/projects`
- `POST /api/projects`
- `GET /api/projects/{project_id}`

### HTTP Methods

| Method | Purpose         | Example                     |
| ------ | --------------- | --------------------------- |
| GET    | read            | `GET /api/projects`         |
| POST   | create          | `POST /api/projects`        |
| PATCH  | partial update  | `PATCH /api/projects/{id}`  |
| PUT    | full replace    | `PUT /api/projects/{id}`    |
| DELETE | remove          | `DELETE /api/projects/{id}` |

### URL Structure

```text
/api/{resource}
/api/{resource}/{id}
/api/{resource}/{id}/{sub_resource}
```

Rules:

- keep nesting depth to two levels
- route names should describe resources, not internal implementation
- path params should be explicit and stable: `{project_id}`, not `{x}`

Examples:

- `GET /api/projects`
- `POST /api/projects`
- `GET /api/projects/{project_id}`
- `PATCH /api/projects/{project_id}`
- `DELETE /api/projects/{project_id}`
- `GET /api/projects/{project_id}/tasks`

## Python Translation

When translating JS-oriented REST guidance to Python:

- use Pydantic models instead of Zod schemas
- use FastAPI `Annotated` parameters for `Path`, `Query`, `Header`, and `Depends`
- use `response_model` or explicit return types to keep response filtering stable
- keep routers thin; validation and contract logic live at the API boundary
- keep domain and persistence details out of route signatures and response types

## FastAPI Layout

Prefer a layout that separates routes, schemas, dependencies, and error
mapping.

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

Good defaults:

- one router module per resource or cohesive sub-resource
- shared pagination, error, and auth dependencies in `dependencies.py` or `responses.py`
- Pydantic request and response models in `schemas/`
- services injected into routes instead of writing DB logic inline

## Response Shapes

Choose one success family and keep it consistent across the API.

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

Delete:

- `204 No Content` with no response body

### Errors

Prefer a stable Problem Details style shape with optional field errors.

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

- keep error shape as stable as success shape
- include field-level issues for validation failures
- do not leak stack traces, raw SQL errors, or library internals
- map internal exceptions to client-facing HTTP errors at the boundary
- return `Retry-After` on `429` when rate limiting is enforced

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

Keep separate models for create, update, and read surfaces.

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

- request models reflect what clients may send, not your DB row
- response models reflect what clients may see, not your ORM entity
- `PATCH` models should usually have optional fields
- do not reuse internal persistence types as public contract types

## Boundary Helpers

Keep response and error helpers small and boring.

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

Use helpers when they stabilize envelopes and reduce duplication.
Do not build a response abstraction jungle for simple routes.

## FastAPI Example

Keep the route thin and the contract explicit.

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

- keep sort keys documented and whitelisted
- prefer one sort parameter over many loosely-defined combinations
- use `-field` or explicit `order=desc`, but stay consistent

### Search

```text
GET /api/projects?search=alpha
```

Rules:

- make search behavior predictable
- document whether it is prefix, substring, exact, or ranked
- enforce sensible limits on page size and result size

### Pagination

Use offset pagination for admin-style lists and modest datasets:

```text
GET /api/projects?page=2&page_size=20
```

Use cursor pagination for feeds, streams, and large datasets:

```text
GET /api/projects?cursor=opaque-token&limit=20
```

## Auth and Ownership

- authenticate before reading sensitive data or performing mutations
- authorize against the target resource, not only the route
- check ownership or tenant scope before update and delete operations
- do not let route convenience bypass domain authorization rules

## Contract Rules

- design the happy path and failure path together
- define create, list, read, update, and delete semantics explicitly
- do not mix raw ORM objects, DTOs, and response models in one surface
- keep nullability intentional and documented
- prefer additive evolution over breaking response changes

## BFF Boundary

If the client needs aggregated or reshaped payloads that do not match the core
resource model, load [bff.md](bff.md) instead of overloading the base API
contract.

## API Checklist

- plural resource names
- stable success and error shapes
- explicit status codes
- validated path, query, and body input
- response models that filter output intentionally
- pagination limits and documented defaults
- auth and ownership checks on sensitive routes
- no leaked internal exceptions or persistence types
