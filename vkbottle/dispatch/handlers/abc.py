import typing
from abc import ABC, abstractmethod
from typing import Any

Event = typing.TypeVar("Event")


class ABCHandler(ABC, typing.Generic[Event]):
    blocking: bool

    @abstractmethod
    async def filter(
        self,
        event: Event,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any] | bool:
        pass

    @abstractmethod
    async def handle(self, event: Event, **context: Any) -> Any:
        pass


__all__ = ("ABCHandler",)
