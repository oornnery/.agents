"""Application-level API tests using pytest and TestClient."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Synchronous tests
# ---------------------------------------------------------------------------


def test_health_check(client: TestClient) -> None:
    """GET /health returns 200 and a status payload."""
    # Arrange
    expected_status = 'ok'

    # Act
    response = client.get('/health')

    # Assert
    assert response.status_code == 200
    data: dict[str, Any] = response.json()
    assert data.get('status') == expected_status


def test_get_tasks_returns_list(client: TestClient, sample_tasks: list[dict[str, Any]]) -> None:
    """GET /tasks returns the stored task list."""
    # Arrange
    with patch('myapp.routes.task_store', sample_tasks):
        # Act
        response = client.get('/tasks')

    # Assert
    assert response.status_code == 200
    data: list[dict[str, Any]] = response.json()
    assert isinstance(data, list)
    assert len(data) == len(sample_tasks)
    assert data[0]['title'] == 'write tests'


def test_create_task_with_valid_payload(client: TestClient, sample_task: dict[str, Any]) -> None:
    """POST /tasks creates a task and returns it with an assigned id."""
    # Arrange
    payload = {'title': sample_task['title']}

    # Act
    response = client.post('/tasks', json=payload)

    # Assert
    assert response.status_code == 201
    data: dict[str, Any] = response.json()
    assert data['title'] == payload['title']
    assert 'id' in data
    assert data.get('done') is False


def test_create_task_rejects_invalid_payload(client: TestClient) -> None:
    """POST /tasks with a missing title returns 422 validation error."""
    # Arrange
    payload: dict[str, Any] = {'done': False}

    # Act
    response = client.post('/tasks', json=payload)

    # Assert
    assert response.status_code == 422
    data: dict[str, Any] = response.json()
    assert 'detail' in data


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_async_health_probe(mock_async_service: AsyncMock) -> None:
    """Async service boundary returns the expected status structure."""
    # Arrange
    expected_version = '0.0.1'

    # Act
    result = await mock_async_service.fetch_status()

    # Assert
    assert result['status'] == 'ok'
    assert result['version'] == expected_version
    mock_async_service.fetch_status.assert_awaited_once()
