from __future__ import annotations

from session import SessionState


def test_session_transcript_keeps_recent_messages() -> None:
    session = SessionState()
    session.record('user: hello')
    session.record('agent: hi')
    assert 'user: hello' in session.transcript()
    assert 'agent: hi' in session.transcript()
