"""Shared pytest fixtures for the test suite."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def app() -> FastAPI:
    """Return the FastAPI application instance for testing."""
    from myapp.main import create_app

    return create_app()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Return a TestClient wired to the app."""
    return TestClient(app)


@pytest.fixture
def sample_task() -> dict[str, str]:
    """Return a representative task payload for arrange/act/assert tests."""
    return {
        'id': '1',
        'title': 'write tests',
        'status': 'pending',
    }


@pytest.fixture
def sample_tasks() -> list[dict[str, str]]:
    """Return a list of task payloads for list-endpoint tests."""
    return [
        {'id': '1', 'title': 'write tests', 'status': 'pending'},
        {'id': '2', 'title': 'refactor code', 'status': 'done'},
    ]


@pytest_asyncio.fixture
async def mock_async_service() -> AsyncGenerator[AsyncMock, None]:
    """Yield an async mock for boundary services used in async tests."""
    mock = AsyncMock()
    mock.fetch_status.return_value = {'status': 'ok', 'version': '0.0.1'}
    yield mock
