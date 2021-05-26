import typing
from abc import ABC, abstractmethod

from vkbottle.http.middleware.abc import ABCHTTPMiddleware
from vkbottle.http.middleware.justlog import JustLogHTTPMiddleware


class ABCHTTPClient(ABC):
    """ Abstract class for http-clients
    Documentation: https://github.com/timoniq/vkbottle/blob/master/docs/low-level/http/http-client.md
    """

    middleware: "ABCHTTPMiddleware" = JustLogHTTPMiddleware()

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def request_text(
        self, method: str, url: str, data: typing.Optional[dict] = None, **kwargs
    ) -> str:
        pass

    @abstractmethod
    async def request_json(
        self, method: str, url: str, data: typing.Optional[dict] = None, **kwargs
    ) -> dict:
        pass

    @abstractmethod
    async def request_content(
        self, method: str, url: str, data: typing.Optional[dict] = None, **kwargs
    ) -> bytes:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    async def __aenter__(self) -> "ABCHTTPClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
