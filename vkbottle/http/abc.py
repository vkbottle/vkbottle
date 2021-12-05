from abc import ABC, abstractmethod
from typing import Any, Optional


class ABCHTTPClient(ABC):
    """Abstract class for http-clients
    Documentation: https://github.com/vkbottle/vkbottle/blob/master/docs/low-level/http/http-client.md
    """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def request_raw(
        self, url: str, method: str = "GET", data: Optional[dict] = None, **kwargs
    ) -> Any:
        pass

    @abstractmethod
    async def request_text(
        self, url: str, method: str = "GET", data: Optional[dict] = None, **kwargs
    ) -> str:
        pass

    @abstractmethod
    async def request_json(
        self, url: str, method: str = "GET", data: Optional[dict] = None, **kwargs
    ) -> dict:
        pass

    @abstractmethod
    async def request_content(
        self, url: str, method: str = "GET", data: Optional[dict] = None, **kwargs
    ) -> bytes:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    async def __aenter__(self) -> "ABCHTTPClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
