from abc import ABC, abstractmethod
from typing import Any, Mapping


class ABCEventDeduplicator(ABC):
    @abstractmethod
    async def claim(self, event: Mapping[str, Any]) -> bool:
        pass


__all__ = ("ABCEventDeduplicator",)
