from abc import ABC, abstractmethod
from typing import Any


class ABCEventDeduplicator(ABC):
    @abstractmethod
    async def claim(self, event: dict[str, Any]) -> bool:
        pass


__all__ = ("ABCEventDeduplicator",)
