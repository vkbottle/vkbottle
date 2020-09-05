from abc import ABC, abstractmethod
from typing import Any


class ABCHandler(ABC):
    blocking: bool

    @abstractmethod
    async def filter(self, event: Any) -> bool:
        pass

    @abstractmethod
    async def handle(self, event: Any) -> Any:
        pass
