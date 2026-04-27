# Architecture

Use when defining routes, templates, data model, migrations, auth, storage, deployment, or module boundaries.

## Decision Flow

1. Marketing/content only: FastAPI + Jinja2 pages + Tailwind; no DB unless forms/leads/webhooks exist.
2. Forms/orders/bookings/admin/persistence: add SQLModel, Alembic, SQLite local; Postgres/Supabase for production.
3. Dynamic partial UI: HTMX for partial forms, filters, search, admin refresh, modal/dialog flows; Alpine.js only for tiny state. Keep business logic out of JS.
4. Accounts/admin: prefer simple session-based admin auth; use external auth/Supabase Auth only for real multi-user complexity.
5. Uploads: local storage in dev, S3-compatible/Supabase/provider adapter in production; never commit uploads.

## Layout

```txt
app/
  __init__.py
  main.py
  core/{config.py,security.py,templates.py}
  db/{session.py,models.py}
  features/
    public/{routes.py,service.py}
    leads/{routes.py,models.py,schemas.py,service.py}
    bookings/{routes.py,models.py,schemas.py,service.py}
    orders/{routes.py,models.py,schemas.py,service.py}
    admin/{routes.py,auth.py}
  templates/{layouts,pages,partials,components}
  static/{css,js}
alembic/versions/
tests/
pyproject.toml
alembic.ini
```

Collapse modules for simple projects.

## Boundaries

- FastAPI routes handle HTTP.
- Pydantic/SQLModel schemas validate data.
- Services contain business rules.
- DB/session code stays out of templates.
- Templates render data; they do not decide business rules.
- Provider integrations sit behind adapters.

## Route Map Template

```md
| Route       | Method   | Purpose            | Template/Response      | Auth |
| ----------- | -------- | ------------------ | ---------------------- | ---- |
| `/`         | GET      | homepage           | `pages/home.html`      | no   |
| `/services` | GET      | service list       | `pages/services.html`  | no   |
| `/contact`  | GET/POST | lead form          | page/partial           | no   |
| `/book`     | GET/POST | create appointment | page/partial           | no   |
| `/admin`    | GET      | dashboard          | `admin/dashboard.html` | yes  |
```

## Data Model Template

```md
| Entity      | Purpose            | Main fields                  | Notes                 |
| ----------- | ------------------ | ---------------------------- | --------------------- |
| Lead        | interested contact | name, phone, message, source | minimal personal data |
| Customer    | contact/person     | name, phone, email           | minimize data         |
| Appointment | scheduled service  | service_id, date, status     | no medical records    |
| Order       | customer order     | total, status, channel       | payment optional      |
```

## SQLModel Baseline

```py
from datetime import datetime
from enum import StrEnum
from typing import Optional

from sqlmodel import Field, SQLModel


class AppointmentStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"


class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str = Field(min_length=2, max_length=120)
    customer_phone: str = Field(min_length=8, max_length=30)
    service_name: str = Field(min_length=2, max_length=120)
    starts_at: datetime
    status: AppointmentStatus = Field(default=AppointmentStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## Forms

Validate every POST with Pydantic/SQLModel or explicit schemas. On failure, return field errors and preserve safe input. Use PRG when appropriate; for HTMX, return consistent partial success/error blocks.

## Security/LGPD Baseline

Collect minimum personal data, avoid sensitive health data by default, protect admin GET/POST with session auth, add CSRF for cookie sessions, validate server-side, keep secrets in env vars, never commit `.env`, rate-limit abused public forms, sign webhooks when possible.
