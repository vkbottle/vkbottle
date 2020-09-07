from abc import ABC, abstractmethod
from typing import Any, Union


class ABCHandler(ABC):
    blocking: bool

    @abstractmethod
    async def filter(self, event: Any) -> Union[dict, bool]:
        pass

    @abstractmethod
    async def handle(self, event: Any, **context) -> Any:
        pass
