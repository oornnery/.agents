# Advanced SQLModel Patterns

Use when persistence modeling beyond simple CRUD.

## Model Design Defaults

- type all fields explicitly
- prefer separate base, table, create, read, update models
- use mixins for repeated timestamps, soft delete, audit fields
- use enums for constrained values
- keep field constraints explicit: lengths, uniqueness, nullable behavior, indexes, defaults

## Basic Model with Validation

```python
from datetime import datetime
from typing import Optional

from pydantic import EmailStr, field_validator
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    email: EmailStr = Field(unique=True)
    full_name: str
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("username must be alphanumeric")
        return value
```

Use field validators for real invariants, not cosmetic rewriting.

## Separate Read and Write Models

```python
from typing import Optional

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)
    full_name: str
    is_active: bool = True


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
```

Keep table shape, write shape, public shape separate when responsibilities differ.

## Mixins

```python
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TimestampMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class SoftDeleteMixin(SQLModel):
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)
    is_deleted: bool = Field(default=False)
```

Useful when fields and semantics genuinely shared. Do not hide project-specific behavior in overly magical mixins.

## One-to-Many

```python
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    heroes: List["Hero"] = Relationship(back_populates="team")


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heroes")
```

Use `back_populates` for bidirectional relationships. Index foreign keys when queried frequently.

## Many-to-Many

```python
from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class HeroTeamLink(SQLModel, table=True):
    __tablename__ = "hero_team_link"
    hero_id: Optional[int] = Field(default=None, foreign_key="hero.id", primary_key=True)
    team_id: Optional[int] = Field(default=None, foreign_key="team.id", primary_key=True)
    joined_at: datetime = Field(default_factory=datetime.utcnow)
    role: Optional[str] = None


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    teams: List["Team"] = Relationship(back_populates="heroes", link_model=HeroTeamLink)


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    heroes: List[Hero] = Relationship(back_populates="teams", link_model=HeroTeamLink)
```

Use explicit link tables when relationship has metadata or you want clearer control over indexes and constraints.

## Self-Referential Relationships

```python
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    manager_id: Optional[int] = Field(default=None, foreign_key="user.id")
    manager: Optional["User"] = Relationship(
        back_populates="subordinates",
        sa_relationship_kwargs={"remote_side": "User.id"},
    )
    subordinates: List["User"] = Relationship(back_populates="manager")
```

Self-referential relationships need careful query testing -- easy to misconfigure and over-fetch.

## Cascades

```python
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    posts: List["Post"] = Relationship(
        back_populates="author",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    user_id: int = Field(foreign_key="user.id")
    author: User = Relationship(back_populates="posts")
```

Be conservative with cascades. Powerful and easy to misuse.

## Inheritance and Polymorphism

- treat inheritance as advanced tool, not default
- prefer composition and explicit fields before polymorphic table layouts
- if using inheritance, document discriminator, nullability tradeoffs, query behavior clearly

Use inheritance only when persistence model genuinely reflects stable polymorphic concept.

## Composite Keys and Constraints

- use composite keys mainly for explicit link tables and domain-natural keys
- keep unique constraints and check constraints explicit in migrations and model metadata
- think about indexes together with constraints; correctness and performance evolve together

## Field Types and Indexes

- use enums for constrained categorical values
- use JSON or custom column types only when access pattern justifies them
- add single, composite, or partial indexes based on real read patterns
- review index costs for writes and migrations before adding casually

## Checklist

- [ ] fields are typed and constrained intentionally
- [ ] read, write, and table models are separated when needed
- [ ] relationships use explicit `back_populates`
- [ ] many-to-many links use explicit link tables
- [ ] foreign keys and frequent filters are indexed
- [ ] cascades are reviewed, not assumed
- [ ] inheritance is justified and documented
