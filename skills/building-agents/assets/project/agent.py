from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext


@dataclass(slots=True)
class AgentDeps:
    current_user: str


class FinalAnswer(BaseModel):
    message: str


support_agent = Agent(
    'openai:gpt-4o-mini',
    deps_type=AgentDeps,
    output_type=FinalAnswer,
    system_prompt=(
        'You are a support agent. Use tools for external facts and return a '
        'concise final answer.'
    ),
)


@support_agent.tool
async def current_user(ctx: RunContext[AgentDeps]) -> str:
    return ctx.deps.current_user
