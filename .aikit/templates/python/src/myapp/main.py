"""FastAPI application entrypoint.

Keeps HTTP wiring thin so business logic stays testable outside
of the web framework.  Routes validate at the boundary and delegate
to plain functions.
"""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title='myapp', version='0.0.1')


@app.get('/health')
async def health_check() -> dict[str, str]:
    """Return service health status.

    Used by orchestrators and load balancers to decide whether
traffic should be routed to this instance.
    """
    return {'status': 'ok'}


@app.get('/tasks')
async def list_tasks() -> list[dict[str, str]]:
    """Return example tasks demonstrating the Task Management API pattern.

    In a real implementation this would delegate to a repository
layer and accept pagination/filter parameters.  The skeleton shows
where boundary validation stops and core logic begins.
    """
    return [
        {'id': '1', 'title': 'Learn FastAPI', 'status': 'pending'},
        {'id': '2', 'title': 'Build something cool', 'status': 'in_progress'},
    ]
