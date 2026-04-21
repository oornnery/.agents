from __future__ import annotations

from myapp.main import build_message
from myapp.settings import Settings


def test_build_message_uses_settings() -> None:
    settings = Settings(app_name='demo', environment='test')
    assert build_message(settings) == 'demo: test'
