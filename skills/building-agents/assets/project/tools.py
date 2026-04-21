from __future__ import annotations

from pydantic_ai import RunContext

from agent import AgentDeps, support_agent


@support_agent.tool
async def lookup_policy(ctx: RunContext[AgentDeps], topic: str) -> str:
    policies = {
        'refund': 'Refunds are allowed within 30 days.',
        'shipping': 'Standard shipping takes 3 to 5 business days.',
    }
    return policies.get(topic.lower(), 'No policy found for that topic.')
