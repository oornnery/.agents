# Pydantic Reference

Data validation, serialization, settings management, and model patterns with Pydantic v2.

## Documentation

- Pydantic Docs: <https://docs.pydantic.dev/latest/>
- Validators: <https://docs.pydantic.dev/latest/concepts/validators/>
- Serialization: <https://docs.pydantic.dev/latest/concepts/serialization/>
- Settings: <https://docs.pydantic.dev/latest/concepts/pydantic_settings/>
- Field: <https://docs.pydantic.dev/latest/concepts/fields/>

## Install

```bash
uv add pydantic
uv add pydantic-settings  # for config/env management
```

## Model Basics

```python
from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    model_config = ConfigDict(strict=True, frozen=True)

    name: str = Field(min_length=1, max_length=100)
    email: str
    age: int = Field(ge=0, le=150)
    tags: list[str] = Field(default_factory=list)
```

### ConfigDict Options

```python
model_config = ConfigDict(
    strict=True,           # No type coercion
    frozen=True,           # Immutable instances
    extra="forbid",        # Reject unknown fields
    str_strip_whitespace=True,
    populate_by_name=True, # Allow field name and alias
)
```

## Validators

### Field Validators

```python
from pydantic import BaseModel, field_validator


class SignupForm(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v.lower().strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v
```

### Model Validators

```python
from pydantic import BaseModel, model_validator


class DateRange(BaseModel):
    start: date
    end: date

    @model_validator(mode="after")
    def validate_range(self) -> "DateRange":
        if self.end <= self.start:
            raise ValueError("end must be after start")
        return self
```

### Before Vs After Validators

```python
# mode="before" — runs on raw input before Pydantic parses
@field_validator("tags", mode="before")
@classmethod
def split_tags(cls, v):
    if isinstance(v, str):
        return [t.strip() for t in v.split(",")]
    return v

# mode="after" — runs on the parsed, typed value (default)
@field_validator("name")
@classmethod
def normalize_name(cls, v: str) -> str:
    return v.title()
```

## Serialization

### Model_dump and Model_dump_json

```python
user = User(name="Alice", email="alice@example.com", age=30)

# To dict
data = user.model_dump()
data = user.model_dump(exclude_none=True)
data = user.model_dump(include={"name", "email"})

# To JSON string
json_str = user.model_dump_json(indent=2)
```

### Computed Fields

```python
from pydantic import BaseModel, computed_field


class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height
```

### Custom Serialization

```python
from pydantic import BaseModel, field_serializer
from datetime import datetime


class Event(BaseModel):
    name: str
    timestamp: datetime

    @field_serializer("timestamp")
    def serialize_ts(self, v: datetime) -> str:
        return v.isoformat()
```

## Aliases

```python
from pydantic import BaseModel, Field


class APIResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: int = Field(alias="userId")
    full_name: str = Field(alias="fullName")

# Both work
APIResponse(userId=1, fullName="Alice")
APIResponse(user_id=1, full_name="Alice")
```

## Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    country: str = "BR"


class Company(BaseModel):
    name: str
    address: Address
    employees: list[User] = Field(default_factory=list)


# Parsing nested data
company = Company.model_validate({
    "name": "Acme",
    "address": {"street": "Rua X", "city": "SP"},
    "employees": [{"name": "Alice", "email": "a@b.com", "age": 30}],
})
```

## Discriminated Unions

```python
from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field


class TextMessage(BaseModel):
    type: Literal["text"] = "text"
    body: str


class ImageMessage(BaseModel):
    type: Literal["image"] = "image"
    url: str
    alt: str = ""


Message = Annotated[
    Union[TextMessage, ImageMessage],
    Field(discriminator="type"),
]


class Chat(BaseModel):
    messages: list[Message]
```

## Settings Management

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        case_sensitive=False,
    )

    debug: bool = False
    database_url: str
    redis_url: str = "redis://localhost:6379"
    secret_key: str
    allowed_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])


# Reads from APP_DEBUG, APP_DATABASE_URL, etc.
settings = Settings()
```

## Generic Models

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int

    @computed_field
    @property
    def has_next(self) -> bool:
        return self.page * self.page_size < self.total


# Usage
response = PaginatedResponse[User](items=[...], total=100, page=1, page_size=20)
```

## Parsing and Validation

```python
# From dict
user = User.model_validate({"name": "Alice", "email": "a@b.com", "age": 30})

# From JSON string
user = User.model_validate_json('{"name": "Alice", "email": "a@b.com", "age": 30}')

# Generate JSON Schema
schema = User.model_json_schema()
```

## Error Handling

```python
from pydantic import ValidationError

try:
    user = User(name="", email="bad", age=-1)
except ValidationError as e:
    for error in e.errors():
        print(f"{error['loc']}: {error['msg']}")
    # ('name',): String should have at least 1 character
    # ('age',): Input should be greater than or equal to 0
```

## Guardrails

- Use `ConfigDict(strict=True)` to prevent silent type coercion.
- Use `ConfigDict(extra="forbid")` for API inputs to catch typos.
- Use `frozen=True` for immutable data objects.
- Validate at boundaries — don't re-validate inside business logic.
- Prefer `field_validator` over `model_validator` when validating a single field.
- Use `model_validate` over direct constructor for external data.
