from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SessionState:
    messages: list[str] = field(default_factory=list)

    def record(self, message: str) -> None:
        self.messages.append(message)

    def transcript(self) -> str:
        return '\n'.join(self.messages[-10:])
