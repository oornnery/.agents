#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "sqlmodel",
# ]
# ///

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel


def now_utc() -> datetime:
    return datetime.now(UTC)


class TaskStatus(str, Enum):
    TODO = 'todo'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'


class TaskPriority(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class TimestampMixin(SQLModel):
    created_at: datetime = Field(default_factory=now_utc, nullable=False)
    updated_at: datetime = Field(default_factory=now_utc, nullable=False)


class UserTeamLink(SQLModel, table=True):
    __tablename__ = 'user_team_link'

    user_id: int = Field(foreign_key='users.id', primary_key=True)
    team_id: int = Field(foreign_key='teams.id', primary_key=True)
    role: str | None = None
    joined_at: datetime = Field(default_factory=now_utc)


class TaskTagLink(SQLModel, table=True):
    __tablename__ = 'task_tag_link'

    task_id: int = Field(foreign_key='tasks.id', primary_key=True)
    tag_id: int = Field(foreign_key='tags.id', primary_key=True)


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    email: str = Field(unique=True)
    full_name: str


class User(UserBase, TimestampMixin, table=True):
    __tablename__ = 'users'

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

    tasks: list['Task'] = Relationship(back_populates='owner')
    teams: list['Team'] = Relationship(
        back_populates='members',
        link_model=UserTeamLink,
    )


class Team(TimestampMixin, table=True):
    __tablename__ = 'teams'

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str | None = None

    members: list[User] = Relationship(
        back_populates='teams',
        link_model=UserTeamLink,
    )


class Tag(SQLModel, table=True):
    __tablename__ = 'tags'

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    color: str | None = None

    tasks: list['Task'] = Relationship(
        back_populates='tags',
        link_model=TaskTagLink,
    )


class Task(TimestampMixin, table=True):
    __tablename__ = 'tasks'

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str | None = None
    completed: bool = Field(default=False)
    status: TaskStatus = Field(default=TaskStatus.TODO)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: datetime | None = None
    owner_id: int = Field(foreign_key='users.id')

    owner: User = Relationship(back_populates='tasks')
    tags: list[Tag] = Relationship(
        back_populates='tasks',
        link_model=TaskTagLink,
    )


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime


class UserUpdate(SQLModel):
    username: str | None = None
    email: str | None = None
    full_name: str | None = None
    is_active: bool | None = None


class TaskCreate(SQLModel):
    title: str
    description: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: datetime | None = None


class TaskRead(SQLModel):
    id: int
    title: str
    description: str | None
    completed: bool
    status: TaskStatus
    priority: TaskPriority
    due_date: datetime | None
    created_at: datetime
    owner_id: int


class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None
