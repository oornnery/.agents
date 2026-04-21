from __future__ import annotations

from myapp.main import get_status


def test_get_status_returns_ok() -> None:
    assert get_status() == {'status': 'ok'}
