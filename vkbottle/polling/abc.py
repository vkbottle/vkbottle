from abc import ABC, abstractmethod
from typing import AsyncIterator, Any


class ABCPolling(ABC):
    """ Abstract Polling class
    Documentation: https://github.com/timoniq/vkbottle/tree/v3.0/docs/polling/polling.md
    """

    @abstractmethod
    async def get_server(self) -> Any:
        pass

    @abstractmethod
    async def get_event(self, server: Any) -> dict:
        pass

    @abstractmethod
    async def listen(self) -> AsyncIterator[dict]:
        pass
