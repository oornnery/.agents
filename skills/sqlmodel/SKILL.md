---
name: sqlmodel
description: SQLModel async patterns with FastAPI -- models, relationships, CRUD,
  sessions, migrations. Load when working with databases, SQLModel, Alembic,
  or async database layers.
---

# SQLModel

Async database patterns with SQLModel and Alembic.

```bash
uv add sqlmodel sqlalchemy[asyncio] asyncpg alembic
```

## Multiple Model Pattern

```python
from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    name: str = Field(max_length=100)
    email: str = Field(max_length=255, unique=True)

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserPublic(UserBase):
    id: int

class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
```

## Async Engine and Session

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

engine = create_async_engine("postgresql+asyncpg://...", pool_size=20, max_overflow=10)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

## FastAPI Dependency

```python
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
```

## Relationships

```python
class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    members: list["User"] = Relationship(back_populates="team")
```

Prevent N+1: `select(Team).options(selectinload(Team.members))`

## Alembic Async

```bash
alembic init -t async alembic
alembic revision --autogenerate -m "add users table"
alembic upgrade head
```

Set `target_metadata = SQLModel.metadata` in `alembic/env.py`.

## Guardrails

- Use multiple model pattern -- never expose table models in responses
- Always `expire_on_commit=False` for async sessions
- Use `selectinload` for relationships -- prevent N+1
- Validate at boundaries with Create/Update models
- Use `async with session.begin()` for multi-step transactions
- Index columns in WHERE/ORDER BY clauses
- Never format SQL strings -- use query builders

## Related

- `skills/fastapi/SKILL.md` -- FastAPI API patterns
- `skills/pydantic/SKILL.md` -- validation and serialization
