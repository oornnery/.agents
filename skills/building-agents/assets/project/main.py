from __future__ import annotations

import asyncio

from agent import AgentDeps, support_agent
from session import SessionState
import tools  # noqa: F401


async def run() -> None:
    session = SessionState()
    session.record('user: what is the refund policy?')
    result = await support_agent.run(
        'What is the refund policy?',
        deps=AgentDeps(current_user='alice@example.com'),
    )
    session.record(f'agent: {result.output.message}')
    print(session.transcript())


if __name__ == '__main__':
    asyncio.run(run())
