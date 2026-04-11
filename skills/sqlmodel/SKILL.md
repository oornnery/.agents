---
name: sqlmodel
description: SQLModel async patterns with FastAPI -- models, relationships, CRUD,
  sessions, migrations. Load when working with databases, SQLModel, Alembic,
  or async database layers.
---

# SQLModel

Async database patterns with SQLModel, PostgreSQL, and Alembic.

## Install

```bash
uv add sqlmodel sqlalchemy[asyncio] asyncpg alembic
```

## Multiple Model Pattern

Separate concerns with Base, Table, Create, Public, Update models:

```python
from sqlmodel import SQLModel, Field


# Base -- shared fields (no table)
class UserBase(SQLModel):
    name: str = Field(max_length=100)
    email: str = Field(max_length=255, unique=True)


# Table -- database model
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


# Create -- input validation (no id, no hash)
class UserCreate(UserBase):
    password: str = Field(min_length=8)


# Public -- response model (no password)
class UserPublic(UserBase):
    id: int


# Update -- partial updates
class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
```

## Async Engine and Session

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    echo=False,
    pool_size=20,
    max_overflow=10,
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

## FastAPI Dependency

```python
from collections.abc import AsyncGenerator
from fastapi import Depends


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
```

## CRUD Patterns

```python
from sqlmodel import select
from sqlalchemy.orm import selectinload


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def list_users(session: AsyncSession, offset: int = 0, limit: int = 20) -> list[User]:
    result = await session.exec(select(User).offset(offset).limit(limit))
    return list(result.all())


async def create_user(session: AsyncSession, data: UserCreate) -> User:
    user = User.model_validate(data, update={"hashed_password": hash_pw(data.password)})
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
```

## Relationships

```python
from sqlmodel import Relationship


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    members: list["User"] = Relationship(back_populates="team")


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    team_id: int | None = Field(default=None, foreign_key="team.id")
    team: Team | None = Relationship(back_populates="members")
```

Prevent N+1 with `selectinload`:

```python
result = await session.exec(select(Team).options(selectinload(Team.members)))
```

## Alembic Async Setup

```bash
alembic init -t async alembic
```

In `alembic/env.py`:

```python
from sqlmodel import SQLModel
from app.models import *  # noqa: F401,F403 -- import all models for metadata

target_metadata = SQLModel.metadata
```

```bash
alembic revision --autogenerate -m "add users table"
alembic upgrade head
```

## Guardrails

- Use the multiple model pattern -- never expose table models in API responses
- Always use `expire_on_commit=False` for async sessions
- Use `selectinload` for relationships -- prevent N+1 queries
- Validate at boundaries with Create/Update models, not inside services
- Use transactions: `async with session.begin()` for multi-step operations
- Index columns used in WHERE/ORDER BY clauses
- Use `Field(sa_column_kwargs={"index": True})` for indexed fields
- Never format SQL strings -- use SQLModel/SQLAlchemy query builders

## Related

- `skills/fastapi/SKILL.md` -- FastAPI API patterns
- `skills/pydantic/SKILL.md` -- validation and serialization
- `skills/testing/SKILL.md` -- database testing with fixtures
