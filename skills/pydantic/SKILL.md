---
name: pydantic
description: Data validation, serialization, settings, and model patterns with Pydantic v2. Load when defining models, validating data, or managing config.
---

# Pydantic

Data validation, serialization, and settings with Pydantic v2.
See [Pydantic docs](https://docs.pydantic.dev/latest/).

```bash
uv add pydantic
uv add pydantic-settings                    # config/env management
```

## Project Conventions

- Use `ConfigDict(strict=True, extra="forbid")` for API inputs.
- Use `ConfigDict(frozen=True)` for immutable domain models.
- Prefer `field_validator` over `model_validator` for single-field validation.
- Prefer `Annotated` + functional validators for reusable validation logic.
- Use `model_validate` over direct constructor for external data.
- Use `TypeAdapter` for standalone type validation without models.

## Settings Pattern

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        case_sensitive=False,
    )

    debug: bool = False
    database_url: str
    secret_key: str
```

## Guardrails

- `strict=True` prevents silent type coercion.
- `extra="forbid"` catches typos in API inputs.
- Validate at boundaries -- don't re-validate inside business logic.
- Use `computed_field` for derived values, `field_serializer` for custom output.
- Use discriminated unions (`Field(discriminator="type")`) for polymorphic models.
