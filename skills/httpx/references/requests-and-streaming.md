# HTTPX Requests and Streaming

## Request Shapes

### Query Parameters

```python
response = client.get(
    "/users",
    params={"page": 1, "page_size": 20, "status": "active"},
)
```

### JSON Body

```python
response = client.post(
    "/users",
    json={"name": "Alice", "email": "alice@example.com"},
)
```

### Form Data

```python
response = client.post(
    "/login",
    data={"username": username, "password": password},
)
```

### Multipart Upload

```python
with open("report.csv", "rb") as handle:
    response = client.post(
        "/upload",
        files={"file": ("report.csv", handle, "text/csv")},
    )
```

Use right request shape for upstream contract. Do not manually build multipart bodies or query strings -- HTTPX already supports them.

## Pagination Pattern

Keep pagination explicit:

```python
async def list_all(client: httpx.AsyncClient) -> list[dict]:
    page = 1
    items: list[dict] = []
    while True:
        response = await client.get("/items", params={"page": page})
        response.raise_for_status()
        payload = response.json()
        items.extend(payload["items"])
        if not payload["has_more"]:
            return items
        page += 1
```

Guardrails:

- cap page count when upstream can misbehave
- prefer cursors when service exposes them
- keep pagination policy in adapter, not sprinkled across callers

## Streaming Downloads

Use streaming for large or unbounded responses.

```python
with client.stream("GET", "/exports/report.csv") as response:
    response.raise_for_status()
    with open("report.csv", "wb") as handle:
        for chunk in response.iter_bytes():
            handle.write(chunk)
```

Async version:

```python
async with client.stream("GET", "/exports/report.csv") as response:
    response.raise_for_status()
    async for chunk in response.aiter_bytes():
        ...
```

Use streaming when:

- downloading large files
- proxying another response
- reading line-delimited or chunked data

## Streaming Uploads

```python
def iter_chunks() -> bytes:
    for chunk in chunks:
        yield chunk


response = client.post("/upload", content=iter_chunks())
```

Keep upload generators focused on bytes prod. Do not mix domain logic and transport iteration.

## NDJSON or Line Streams

```python
async with client.stream("GET", "/events") as response:
    response.raise_for_status()
    async for line in response.aiter_lines():
        if not line:
            continue
        process_line(line)
```

## Response Parsing

Keep response parsing explicit, close to adapter boundary.

```python
from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str


def parse_user(response: httpx.Response) -> User:
    response.raise_for_status()
    return User.model_validate(response.json())
```

## Guardrails

- do not call `.json()` repeatedly on same response -- one parse enough
- do not load huge payload into memory if iteration suffices
- do not return raw `httpx.Response` from higher-level service adapters unless callers genuinely need transport access
- do not parse untrusted content types blindly; check contract assumptions when needed
