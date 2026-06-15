"""HTTP routes for the Task Management API skeleton.

Routes stay thin: validate at the boundary, delegate to plain
functions, and return explicit response models.
"""

from __future__ import annotations

from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()

# In-memory store (replace with a repository layer in production).
# Module-level so tests can patch `myapp.routes.task_store`.
task_store: list[dict[str, str]] = [
    {'id': '1', 'title': 'Learn FastAPI', 'status': 'pending'},
    {'id': '2', 'title': 'Build something cool', 'status': 'in_progress'},
]


class TaskCreate(BaseModel):
    """Payload accepted by POST /tasks. Validation happens at this boundary."""

    title: str


class Task(BaseModel):
    """Task as returned by the API."""

    id: str
    title: str
    status: str


@router.get('/health')
async def health_check() -> dict[str, str]:
    """Return service health for orchestrator and load balancer probes."""
    return {'status': 'ok'}


@router.get('/tasks')
async def list_tasks() -> list[Task]:
    """Return all tasks.

    A real implementation would delegate to a repository layer and
    accept pagination and filter parameters.
    """
    return [Task.model_validate(task) for task in task_store]


@router.post('/tasks', status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate) -> Task:
    """Create a task and return it with an assigned id."""
    task = Task(id=str(len(task_store) + 1), title=payload.title, status='pending')
    task_store.append(task.model_dump())
    return task
